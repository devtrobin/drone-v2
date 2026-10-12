"""TCP réel sur boucle locale ; moteurs simulés et arrêt observé côté serveur."""
import json
import socket
import threading
import time
import unittest

from drone.client import Pilot
from drone.config import Config
from drone.motors import MotorController, SimBackend
from drone.protocol import signed_command
from drone.server import DEFAULT_CONFIG, serve

KEY = bytes(range(32))


class NetworkTests(unittest.TestCase):
    def setUp(self):
        self.config = Config.load(DEFAULT_CONFIG)
        self.backend = SimBackend()
        self.controller = MotorController(self.backend, self.config)
        self.shutdown = threading.Event()
        self.listener = socket.socket()
        self.listener.bind(("127.0.0.1", 0))
        self.listener.listen(1)
        self.port = self.listener.getsockname()[1]
        self.errors = []

        def run():
            try:
                serve(self.listener, self.controller, KEY, self.config, self.shutdown)
            except BaseException as error:
                self.errors.append(error)

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        self.clients = []

    def tearDown(self):
        for client in self.clients:
            client.close()
        self.shutdown.set()
        self.thread.join(timeout=1)
        self.listener.close()
        self.assertFalse(self.thread.is_alive(), "Le serveur ne s'arrête pas")
        self.assertEqual(self.errors, [])
        self.assertFalse(self.backend.enabled)

    def pilot(self, key=KEY):
        pilot = Pilot("127.0.0.1", self.port, key)
        self.clients.append(pilot)
        return pilot

    def wait_stopped(self, timeout=0.5):
        until = time.monotonic() + timeout
        while self.backend.enabled and time.monotonic() < until:
            time.sleep(0.005)
        self.assertFalse(self.backend.enabled)
        self.assertEqual(self.controller.last, (0, 0))

    def test_move_stop_and_disconnect(self):
        client = self.pilot()
        self.assertFalse(client.state["enabled"])
        self.assertTrue(client.command(True, 1, 0)["enabled"])
        self.assertFalse(client.command(False, 0, 0)["enabled"])
        time.sleep(0.06)
        self.assertTrue(client.command(True, 1, 0)["enabled"])
        client.close()
        self.wait_stopped()

    def test_timeout_closes_session_and_reconnection_starts_stopped(self):
        client = self.pilot()
        client.command(True, 1, 0)
        start = time.monotonic()
        self.wait_stopped()
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.25)
        self.assertLess(elapsed, 0.45)
        with self.assertRaises((OSError, ValueError)):
            client.command(True, 1, 0)
        new_client = self.pilot()
        self.assertFalse(new_client.state["enabled"])
        self.assertEqual((new_client.state["left"], new_client.state["right"]), (0, 0))

    def test_bad_authentication(self):
        with self.assertRaises((OSError, ValueError)):
            self.pilot(bytes(32))
        self.assertFalse(self.backend.enabled)

    def test_invalid_packet_during_motion_stops(self):
        client = self.pilot()
        client.command(True, 1, 0)
        client.connection.sendall(b"{}\n")
        self.wait_stopped()

    def test_old_ticket_cannot_replay_motion(self):
        client = self.pilot()
        old_ticket = client.state["ticket"]
        old_seq = client.seq
        client.command(True, 1, 0)
        client.connection.sendall(signed_command(KEY, old_seq + 1, old_ticket, True, 1, 0))
        self.wait_stopped()

    def test_partial_line_does_not_keep_motor_running(self):
        client = self.pilot()
        client.command(True, 1, 0)
        client.connection.sendall(b'{"v":')
        self.wait_stopped()

    def test_oversized_packet_stops(self):
        client = self.pilot()
        client.command(True, 1, 0)
        client.connection.sendall(b"x" * 2048)
        self.wait_stopped()

    def test_fragmented_command_is_accepted(self):
        connection = socket.create_connection(("127.0.0.1", self.port))
        connection.settimeout(1)
        self.clients.append(connection)
        stream = connection.makefile("rb")
        self.addCleanup(stream.close)
        welcome = json.loads(stream.readline())
        frame = signed_command(KEY, 0, welcome["ticket"], True, 1, 0)
        connection.sendall(frame[:20])
        connection.sendall(frame[20:])
        result = json.loads(stream.readline())
        self.assertTrue(result["enabled"])
        connection.sendall(signed_command(KEY, 1, result["ticket"], False, 0, 0))
        self.assertFalse(json.loads(stream.readline())["enabled"])

    def test_shutdown_while_moving(self):
        client = self.pilot()
        client.command(True, 1, 0)
        self.shutdown.set()
        self.wait_stopped(timeout=0.15)


if __name__ == "__main__":
    unittest.main()
