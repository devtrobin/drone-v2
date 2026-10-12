"""Trames JSON bornées, HMAC et ticket serveur renouvelé à chaque commande."""
import hashlib
import hmac
import json
from pathlib import Path
import secrets

from .config import number

MAX_FRAME = 1024
FIELDS = {"v", "seq", "ticket", "enabled", "throttle", "turn", "mac"}


def read_key(path):
    raw = Path(path).read_text(encoding="ascii").strip()
    try:
        key = bytes.fromhex(raw)
    except ValueError as error:
        raise ValueError("Clé attendue : 64 caractères hexadécimaux") from error
    if len(key) != 32 or len(raw) != 64:
        raise ValueError("Clé attendue : 64 caractères hexadécimaux")
    return key


def create_key(path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never replace the robot's existing shared secret.
    import os
    with os.fdopen(os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as out:
        out.write(secrets.token_hex(32) + "\n")


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def signed_command(key, seq, ticket, enabled, throttle, turn):
    data = {"v": 1, "seq": seq, "ticket": ticket, "enabled": enabled,
            "throttle": throttle, "turn": turn}
    data["mac"] = hmac.new(key, canonical(data), hashlib.sha256).hexdigest()
    return canonical(data) + b"\n"


def decode_command(frame, key, ticket, previous_seq):
    if len(frame) > MAX_FRAME:
        raise ValueError("Trame trop longue")
    try:
        data = json.loads(frame)
    except (ValueError, UnicodeError) as error:
        raise ValueError("Trame JSON invalide") from error
    if not isinstance(data, dict) or set(data) != FIELDS:
        raise ValueError("Champs de commande invalides")
    if type(data["v"]) is not int or data["v"] != 1:
        raise ValueError("Version inconnue")
    if type(data["seq"]) is not int or not previous_seq < data["seq"] <= 2**53:
        raise ValueError("Séquence périmée ou invalide")
    if not isinstance(data["ticket"], str) or data["ticket"] != ticket:
        raise ValueError("Ticket périmé")
    if type(data["enabled"]) is not bool:
        raise ValueError("Autorisation invalide")
    throttle = number(data["throttle"], "throttle", -1, 1)
    turn = number(data["turn"], "turn", -1, 1)
    signature = data.pop("mac")
    expected = hmac.new(key, canonical(data), hashlib.sha256).hexdigest()
    if (not isinstance(signature, str) or len(signature) != 64
            or any(char not in "0123456789abcdef" for char in signature)
            or not hmac.compare_digest(signature, expected)):
        raise ValueError("Authentification invalide")
    return data["seq"], data["enabled"], throttle, turn
