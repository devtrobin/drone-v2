"""Essais hors matériel : validation, mixage, arrêt, clavier et chaîne vidéo."""
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
import unittest
from unittest.mock import patch

from drone.config import Config
from drone.motors import GPIOBackend, MotorController, SimBackend, mix
from drone.pilot import Keyboard
from drone.protocol import create_key, decode_command, read_key, signed_command
from drone.server import DEFAULT_CONFIG
from drone.video import stream_command, view_command

KEY = bytes(range(32))


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.config = Config.load(DEFAULT_CONFIG)

    def test_mix_limits_and_direction(self):
        self.assertEqual(mix(1, 0, 0.35), (0.35, 0.35))
        self.assertEqual(mix(0, 1, 0.35), (0.35, -0.35))
        self.assertEqual(mix(-1, 0, 0.35), (-0.35, -0.35))
        self.assertEqual(mix(1, 1, 0.35), (0.35, 0))
        for throttle in (-1, -0.5, 0, 0.5, 1):
            for turn in (-1, -0.5, 0, 0.5, 1):
                self.assertTrue(all(abs(x) <= 0.35 for x in mix(throttle, turn, 0.35)))

    def test_motor_disarmed_at_boot_and_on_stop(self):
        backend = SimBackend()
        controller = MotorController(backend, self.config)
        self.assertFalse(backend.enabled)
        controller.command(False, 1, 1)
        self.assertEqual(controller.last, (0, 0))
        controller.command(True, 1, 0)
        self.assertTrue(backend.enabled)
        controller.close()
        self.assertFalse(backend.enabled)
        self.assertEqual((backend.left, backend.right), (0, 0))

    def test_direction_change_includes_off_interval(self):
        clock = [1.0]
        backend = SimBackend()
        controller = MotorController(backend, self.config, lambda: clock[0])
        controller.command(True, 1, 0)
        controller.command(True, -1, 0)
        self.assertFalse(backend.enabled)
        clock[0] += 0.04
        controller.command(True, -1, 0)
        self.assertEqual(controller.last, (0, 0))
        clock[0] += 0.02
        controller.command(True, -1, 0)
        self.assertEqual(controller.last, (-0.35, -0.35))

    def test_stop_then_reverse_cannot_bypass_off_interval(self):
        clock = [1.0]
        controller = MotorController(SimBackend(), self.config, lambda: clock[0])
        controller.command(True, 1, 0)
        controller.command(False, 0, 0)
        controller.command(True, -1, 0)
        self.assertEqual(controller.last, (0, 0))
        clock[0] += 0.06
        controller.command(True, -1, 0)
        self.assertEqual(controller.last, (-0.35, -0.35))

    def test_inversion_is_per_wheel(self):
        controller = MotorController(SimBackend(), replace(self.config, invert_left=True))
        controller.command(True, 1, 0)
        self.assertEqual(controller.last, (-0.35, 0.35))

    def test_bad_configs_are_rejected_before_gpio(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "robot.json"
            original = json.loads(DEFAULT_CONFIG.read_text())
            for key, value in (("max_duty", float("nan")), ("max_duty", 1.1),
                               ("hardware_confirmed", "oui"), ("command_timeout_s", 0),
                               ("pwm_hz", True)):
                data = dict(original)
                data[key] = value
                path.write_text(json.dumps(data))
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    Config.load(path)
            original["pins"]["sleep"] = original["pins"]["left_forward"]
            path.write_text(json.dumps(original))
            with self.assertRaises(ValueError):
                Config.load(path)

    def test_hardware_requires_confirmed_wiring(self):
        with self.assertRaisesRegex(ValueError, "non confirmé"):
            GPIOBackend(self.config)

    def test_valid_authenticated_command(self):
        frame = signed_command(KEY, 0, "fresh-ticket", True, 0.8, -0.2)
        self.assertEqual(decode_command(frame, KEY, "fresh-ticket", -1), (0, True, 0.8, -0.2))

    def test_corrupt_replayed_and_invalid_commands(self):
        valid = signed_command(KEY, 1, "ticket", True, 1, 0)
        bad = json.loads(valid)
        bad["throttle"] = 0
        bad_signature = json.loads(valid)
        bad_signature["mac"] = "é" * 64
        frames = [b"not-json", b"[]", b"x" * 1025, json.dumps(bad).encode(),
                  json.dumps(bad_signature).encode(),
                  signed_command(bytes(32), 2, "ticket", True, 1, 0),
                  signed_command(KEY, 2, "old-ticket", True, 1, 0),
                  signed_command(KEY, 2, "ticket", 1, 1, 0),
                  signed_command(KEY, 2, "ticket", True, 2, 0),
                  signed_command(KEY, True, "ticket", True, 1, 0), valid]
        for frame in frames:
            with self.subTest(frame=frame[:40]), self.assertRaises(ValueError):
                decode_command(frame, KEY, "ticket", 1)
        for value in (float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                signed_command(KEY, 2, "ticket", True, value, 0)

    def test_secret_exclusive_and_private(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "secret.key"
            create_key(path)
            key = read_key(path)
            self.assertEqual(len(key), 32)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                create_key(path)
            self.assertEqual(key, read_key(path))

    def test_keyboard_deadman_opposite_keys_and_focus_loss(self):
        keyboard = Keyboard()
        keyboard.keys = {"Up", "Right"}
        self.assertEqual(keyboard.values(), (False, 1, 1))
        keyboard.keys.add("space")
        self.assertEqual(keyboard.values(), (True, 1, 1))
        keyboard.keys.update({"Down", "Left"})
        self.assertEqual(keyboard.values(), (True, 0, 0))
        keyboard.clear()
        self.assertEqual(keyboard.values(), (False, 0, 0))

    def test_video_copies_bitstream_and_separates_processes(self):
        camera, mux = stream_command("192.168.1.10", 5000)
        self.assertIn("h264", camera)
        self.assertEqual(mux[mux.index("-c:v") + 1], "copy")
        self.assertIn("mpegts", mux)
        self.assertIn("udp://192.168.1.10:5000?pkt_size=1316", mux)
        self.assertIn("ffplay", view_command(5000))
        for host in ("localhost;touch file", "", "999.0.0.1"):
            with self.assertRaises(ValueError):
                stream_command(host, 5000)
        with self.assertRaises(ValueError):
            view_command(80)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg optionnel")
    def test_mpegts_pipeline_with_real_ffmpeg_and_synthetic_video(self):
        # A synthetic clip verifies transport arguments, not the camera or Raspberry Pi encoder.
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "test.h264"
            output = Path(directory) / "test.ts"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                            "-i", "testsrc2=size=320x240:rate=30", "-t", "0.5", "-an",
                            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
                            "-f", "h264", str(raw)], check=True, capture_output=True, timeout=15)
            _, mux = stream_command("127.0.0.1", 5000)
            mux[mux.index("pipe:0")] = str(raw)
            mux[-1] = str(output)
            subprocess.run(mux, check=True, capture_output=True, timeout=15)
            result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                     "-show_entries", "stream=codec_name,r_frame_rate",
                                     "-of", "json", str(output)],
                                    check=True, capture_output=True, text=True, timeout=15)
            stream = json.loads(result.stdout)["streams"][0]
            self.assertEqual(stream["codec_name"], "h264")
            self.assertEqual(stream["r_frame_rate"], "30/1")

    @unittest.skipUnless(importlib.util.find_spec("gpiozero"), "gpiozero optionnel sur Mac")
    def test_real_gpiozero_api_with_mock_pins(self):
        from gpiozero.pins.mock import MockFactory, MockPWMPin
        factory = MockFactory(pin_class=MockPWMPin)
        config = replace(self.config, hardware_confirmed=True)
        backend = GPIOBackend(config, factory=factory)
        controller = MotorController(backend, config)
        with patch("drone.motors.time.sleep"):
            controller.command(True, 1, 0)
        self.assertEqual(factory.pin(17).state, 0.35)
        self.assertEqual(factory.pin(27).state, 0)
        self.assertTrue(factory.pin(24).state)
        controller.stop()
        self.assertFalse(factory.pin(24).state)
        self.assertEqual(factory.pin(17).state, 0)
        controller.close()


if __name__ == "__main__":
    unittest.main()
