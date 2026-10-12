"""Démonstration réseau locale, sans interface graphique, sans GPIO ni clé persistante."""
import secrets
import socket
import threading
import time

from .client import Pilot
from .config import Config
from .motors import MotorController, SimBackend
from .server import DEFAULT_CONFIG, serve


def main():
    config = Config.load(DEFAULT_CONFIG)
    backend = SimBackend()
    controller = MotorController(backend, config)
    shutdown = threading.Event()
    key = secrets.token_bytes(32)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        thread = threading.Thread(target=serve,
                                  args=(listener, controller, key, config, shutdown), daemon=True)
        thread.start()
        client = None
        try:
            client = Pilot("127.0.0.1", listener.getsockname()[1], key)
            for label, throttle, turn in (("Avancer", 1, 0), ("Tourner à droite", 0, 1),
                                          ("Reculer", -1, 0), ("Arrêter", 0, 0)):
                for _ in range(4):
                    state = client.command(True, throttle, turn)
                    time.sleep(0.05)
                print(f"{label} : gauche={state['left']:.2f}, droite={state['right']:.2f}")
            client.command(True, 1, 0)
            time.sleep(config.command_timeout_s + 0.08)
            if backend.enabled or controller.last != (0, 0):
                raise RuntimeError("L'arrêt sur absence de commande a échoué")
            print("Perte de commande : moteurs simulés arrêtés, session fermée.")
            print("Démonstration terminée : aucun GPIO utilisé.")
            return 0
        finally:
            if client is not None:
                client.close()
            shutdown.set()
            thread.join(timeout=1)


if __name__ == "__main__":
    raise SystemExit(main())
