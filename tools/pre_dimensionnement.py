"""Estimations 2D de stabilité et d'autonomie à partir de relevés, sans fichier 3D."""
import argparse
import json
import math
from pathlib import Path


def finite(value, label, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value) or (positive and value <= 0):
        raise ValueError(f"{label} : nombre fini {'strictement positif' if positive else ''} requis")
    return float(value)


def stability(supports, masses):
    """Three contact points define the support triangle; distances are signed in mm."""
    if not isinstance(supports, list) or len(supports) != 3 or not masses:
        raise ValueError("Trois appuis et la liste complète des masses sont nécessaires")
    points = []
    for point in supports:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("Un appui doit contenir [x, y]")
        points.append(tuple(finite(value, "appui") for value in point))
    area2 = sum(points[i][0] * points[(i + 1) % 3][1]
                - points[(i + 1) % 3][0] * points[i][1] for i in range(3))
    if abs(area2) < 1e-9:
        raise ValueError("Les appuis sont alignés ou confondus")
    if area2 < 0:
        points.reverse()
    mass_sum, weighted = 0.0, [0.0, 0.0, 0.0]
    for item in masses:
        mass = finite(item["mass_g"], "masse", True)
        position = item["center_mm"]
        if len(position) != 3:
            raise ValueError("Le centre d'une pièce doit contenir [x, y, z]")
        xyz = [finite(value, "centre") for value in position]
        if xyz[2] < 0:
            raise ValueError("La hauteur depuis le sol ne peut pas être négative")
        mass_sum += mass
        weighted = [acc + mass * value for acc, value in zip(weighted, xyz)]
    x, y, z = [value / mass_sum for value in weighted]
    margins = []
    for i, (ax, ay) in enumerate(points):
        bx, by = points[(i + 1) % 3]
        margins.append(((bx - ax) * (y - ay) - (by - ay) * (x - ax))
                       / math.hypot(bx - ax, by - ay))
    margin = min(margins)
    return {"total_mass_g": mass_sum, "center_of_mass_mm": [x, y, z],
            "minimum_static_margin_mm": margin, "strictly_inside_triangle": margin > 0,
            "ideal_tipping_acceleration_m_s2": 9.81 * margin / z if z > 0 and margin > 0 else None}


def autonomy(energy_wh, efficiency, power_w):
    energy = finite(energy_wh, "énergie interne Wh", True)
    efficiency = finite(efficiency, "rendement", True)
    power = finite(power_w, "puissance moyenne au 5 V", True)
    if efficiency > 1:
        raise ValueError("Le rendement doit être compris entre 0 et 1")
    return {"usable_energy_wh": energy * efficiency,
            "estimated_runtime_min": energy * efficiency / power * 60}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.file.read_text(encoding="utf8"))
        results = {"status": "estimation, pas une validation physique"}
        missing = []
        if data.get("support_points_mm") and data.get("masses"):
            results["stability"] = stability(data["support_points_mm"], data["masses"])
        else:
            missing.append("Appuis et masses non relevés")
        keys = ("battery_energy_wh", "conversion_efficiency", "average_power_5v_w")
        if all(data.get(key) is not None for key in keys):
            results["energy"] = autonomy(*(data[key] for key in keys))
        else:
            missing.append("Énergie, rendement ou puissance moyenne inconnus")
        results["missing_measurements"] = missing
        print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False))
        return 2 if missing else 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
