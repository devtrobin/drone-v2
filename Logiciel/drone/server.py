"""Serveur TCP à un pilote ; aucune commande conservée après perte de liaison."""
import argparse
import json
import logging
from pathlib import Path
import secrets
import signal
import socket
import threading
import time

from .config import Config
from .motors import GPIOBackend, MotorController, SimBackend
from .protocol import MAX_FRAME, create_key, decode_command, read_key

LOG = logging.getLogger(__name__)
DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config" / "robot.example.json"


def reply(connection, ticket, timeout, seq, controller):
    data = {"v": 1, "ticket": ticket, "timeout_s": timeout, "seq": seq,
            "left": controller.last[0], "right": controller.last[1],
            "enabled": controller.enabled}
    connection.sendall(json.dumps(data, separators=(",", ":")).encode("ascii") + b"\n")


def serve_connection(connection, controller, key, config, shutdown):
    controller.stop()
    connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    connection.settimeout(0.02)
    ticket = secrets.token_hex(16)
    seq = -1
    deadline = time.monotonic() + config.command_timeout_s
    buffer = b""
    try:
        reply(connection, ticket, config.command_timeout_s, seq, controller)
        while not shutdown.is_set():
            if time.monotonic() >= deadline:
                LOG.warning("Délai de commande dépassé : arrêt et fermeture de session")
                break
            if b"\n" not in buffer:
                try:
                    chunk = connection.recv(MAX_FRAME + 1)
                except socket.timeout:
                    continue
                if not chunk:
                    break
                buffer += chunk
                if len(buffer) > MAX_FRAME:
                    raise ValueError("Buffer trop long")
                continue
            frame, buffer = buffer.split(b"\n", 1)
            # Check lease again after receiving bytes; queued old commands cannot renew it.
            if time.monotonic() >= deadline:
                break
            seq, enabled, throttle, turn = decode_command(frame, key, ticket, seq)
            controller.command(enabled, throttle, turn)
            ticket = secrets.token_hex(16)
            deadline = time.monotonic() + config.command_timeout_s
            reply(connection, ticket, config.command_timeout_s, seq, controller)
    except (OSError, ValueError) as error:
        LOG.warning("Session interrompue : %s", error)
    finally:
        controller.stop()


def serve(listener, controller, key, config, shutdown):
    listener.settimeout(0.05)
    controller.stop()
    try:
        while not shutdown.is_set():
            try:
                connection, address = listener.accept()
            except socket.timeout:
                continue
            LOG.info("Connexion de %s", address[0])
            with connection:
                serve_connection(connection, controller, key, config, shutdown)
    finally:
        controller.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="IP d'écoute, boucle locale par défaut")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--key-file", type=Path, required=True)
    parser.add_argument("--hardware", action="store_true", help="Activer les GPIO confirmés")
    parser.add_argument("--create-key", action="store_true", help="Créer la clé puis quitter")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        if args.create_key:
            create_key(args.key_file)
            print("Clé créée. Garder ce fichier privé et le copier au pilote par SSH.")
            return 0
        key = read_key(args.key_file)
        config = Config.load(args.config)
        # Bind before GPIO initialization: a busy port must never leave active hardware behind.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((args.host, args.port))
            listener.listen(1)
            backend = GPIOBackend(config) if args.hardware else SimBackend()
            try:
                controller = MotorController(backend, config)
            except BaseException:
                backend.close()
                raise
            shutdown = threading.Event()
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, lambda *_: shutdown.set())
            LOG.info("Mode %s, écoute %s:%s", "GPIO" if args.hardware else "SIMULATION",
                     *listener.getsockname())
            serve(listener, controller, key, config, shutdown)
        return 0
    except (OSError, ValueError, ImportError) as error:
        LOG.error("Démarrage refusé : %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
