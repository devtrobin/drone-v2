"""Validation du nouveau PWM/DIR et de l'arrêt, sur broches simulées."""
from dataclasses import replace
from pathlib import Path
import unittest

from drone.config import Config
from drone.motors import MD13SBackend, MotorController, gpio_backend, limited_mix

PROFILE = Path(__file__).resolve().parents[1]/'config/robot.puissance.example.json'


class MD13STests(unittest.TestCase):
    def test_profile_keeps_hardware_disabled(self):
        config = Config.load(PROFILE)
        self.assertEqual(config.driver, 'md13s')
        self.assertFalse(config.hardware_confirmed)
        with self.assertRaisesRegex(ValueError, 'non confirmé'):
            gpio_backend(config)

    def test_direction_pwm_disable_and_reversal_pause(self):
        from gpiozero.pins.mock import MockFactory, MockPWMPin
        config = replace(Config.load(PROFILE), hardware_confirmed=True, ramp_per_s=0)
        factory = MockFactory(pin_class=MockPWMPin)
        backend = MD13SBackend(config, factory)
        clock = [1.0]
        controller = MotorController(backend, config, lambda: clock[0])
        try:
            self.assertEqual((factory.pin(17).state, factory.pin(22).state), (0, 0))
            controller.command(True, 1, 0)
            self.assertEqual((factory.pin(17).state, factory.pin(22).state), (.25, .25))
            self.assertFalse(factory.pin(27).state)
            controller.command(True, -1, 0)
            self.assertEqual((factory.pin(17).state, factory.pin(22).state), (0, 0))
            clock[0] += .16
            controller.command(True, -1, 0)
            self.assertTrue(factory.pin(27).state)
            self.assertTrue(factory.pin(23).state)
            self.assertEqual(factory.pin(17).state, .25)
            controller.stop()
            self.assertEqual((factory.pin(17).state, factory.pin(22).state), (0, 0))
            backend.outputs(1, 1)
            self.assertEqual((factory.pin(17).state, factory.pin(22).state), (0, 0))
        finally:
            controller.close()

    def test_ramp_limits_first_command_and_delayed_packets(self):
        from drone.motors import SimBackend
        config = Config.load(PROFILE)
        clock = [1.0]
        controller = MotorController(SimBackend(), config, lambda: clock[0])
        controller.command(True, 1, 0)
        self.assertEqual(controller.last, (0, 0))
        clock[0] += .05
        controller.command(True, 1, 0)
        self.assertAlmostEqual(controller.last[0], .015)
        clock[0] += 10
        controller.command(True, 1, 0)
        self.assertAlmostEqual(controller.last[0], .045)
        controller.stop()
        self.assertEqual(controller.last, (0, 0))

    def test_turn_reduces_forward_speed_and_has_separate_cap(self):
        self.assertEqual(limited_mix(0, 1, .95, .08), (.08, -.08))
        left, right = limited_mix(1, 1, .95, .08)
        self.assertAlmostEqual((left + right) / 2, .475)
        self.assertAlmostEqual(left - right, .08)


if __name__ == '__main__':
    unittest.main()
