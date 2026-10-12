"""Configuration validée avant toute ouverture de GPIO."""
from dataclasses import dataclass
import json
import math
from pathlib import Path

PIN_NAMES = {"left_forward", "left_reverse", "right_forward", "right_reverse", "sleep"}


def number(value, name, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} doit être un nombre entre {low} et {high}")
    return float(value)


@dataclass(frozen=True)
class Config:
    pins: dict
    hardware_confirmed: bool = False
    invert_left: bool = False
    invert_right: bool = False
    max_duty: float = 0.35
    pwm_hz: float = 100
    command_timeout_s: float = 0.3
    reverse_pause_s: float = 0.05
    wake_delay_s: float = 0.002

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf8"))
        if not isinstance(data, dict):
            raise ValueError("La configuration doit être un objet JSON")
        if set(data) != set(cls.__dataclass_fields__):
            raise ValueError("Champs de configuration manquants ou inconnus")
        pins = data["pins"]
        if not isinstance(pins, dict) or set(pins) != PIN_NAMES:
            raise ValueError("GPIO BCM du pilote manquants ou inconnus")
        if any(type(pin) is not int or not 2 <= pin <= 27 for pin in pins.values()):
            raise ValueError("GPIO BCM invalide")
        if len(set(pins.values())) != len(PIN_NAMES):
            raise ValueError("Un même GPIO ne peut pas commander deux signaux")
        for key in ("hardware_confirmed", "invert_left", "invert_right"):
            if type(data[key]) is not bool:
                raise ValueError(f"{key} doit être un booléen")
        limits = {"max_duty": (0.01, 1), "pwm_hz": (10, 1000),
                  "command_timeout_s": (0.1, 0.5), "reverse_pause_s": (0.01, 0.5),
                  "wake_delay_s": (0.001, 0.1)}
        for key, (low, high) in limits.items():
            data[key] = number(data[key], key, low, high)
        return cls(**data)
