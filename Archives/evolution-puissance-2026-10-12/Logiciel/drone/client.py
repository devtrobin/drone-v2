"""Client synchrone : un seul message en attente, aucune reconnexion automatique."""
import json
import socket

from .protocol import MAX_FRAME, signed_command
from .config import number


class Pilot:
    def __init__(self, host, port, key):
        self.connection = socket.create_connection((host, port), timeout=1)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.connection.settimeout(0.12)
        self.key, self.seq, self.buffer = key, 0, b""
        try:
            self.state = self.receive()
            # First authenticated command is always a stop.
            self.command(False, 0, 0)
        except BaseException:
            self.close()
            raise

    def receive(self):
        while b"\n" not in self.buffer:
            chunk = self.connection.recv(MAX_FRAME + 1)
            if not chunk:
                raise ConnectionError("Serveur déconnecté")
            self.buffer += chunk
            if len(self.buffer) > MAX_FRAME:
                raise ValueError("Réponse trop longue")
        line, self.buffer = self.buffer.split(b"\n", 1)
        state = json.loads(line)
        if (not isinstance(state, dict) or type(state.get("v")) is not int or state["v"] != 1
                or not isinstance(state.get("ticket"), str) or len(state["ticket"]) != 32
                or any(char not in "0123456789abcdef" for char in state["ticket"])
                or type(state.get("enabled")) is not bool or type(state.get("seq")) is not int):
            raise ValueError("Réponse du serveur invalide")
        number(state.get("left"), "left", -1, 1)
        number(state.get("right"), "right", -1, 1)
        number(state.get("timeout_s"), "timeout_s", 0.1, 0.5)
        return state

    def command(self, enabled, throttle, turn):
        frame = signed_command(self.key, self.seq, self.state["ticket"], enabled, throttle, turn)
        self.connection.sendall(frame)
        state = self.receive()
        if state.get("seq") != self.seq:
            raise ValueError("Accusé de réception incorrect")
        self.state = state
        self.seq += 1
        return state

    def close(self):
        self.connection.close()
