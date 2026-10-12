"""Contrôles du dossier et tests hors matériel, avec rapport JSON facultatif."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    checks = [
        ("pilotage", ROOT / "Logiciel",
         [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("calculs", ROOT, [sys.executable, "-m", "unittest", "discover",
                         "-s", "tools/tests", "-v"]),
        ("documentation", ROOT, [sys.executable, "tools/check_project.py"]),
    ]
    try:
        gpiozero = importlib.metadata.version("gpiozero")
    except importlib.metadata.PackageNotFoundError:
        gpiozero = None
    results = []
    report = {"executed_at_utc": datetime.now(timezone.utc).isoformat(),
              "python": platform.python_version(), "platform": platform.platform(),
              "gpiozero": gpiozero, "hardware_used": False, "checks": results,
              "note": "Tests TCP locaux et broches simulées ; aucun essai du robot ni de caméra"}
    for name, cwd, command in checks:
        run = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=60)
        results.append({"name": name, "command": command[1:], "returncode": run.returncode,
                        "stdout": run.stdout, "stderr": run.stderr})
        print(f"{name} : {'OK' if run.returncode == 0 else 'ÉCHEC'}")
        if run.returncode:
            print(run.stdout + run.stderr)
        # Save completed checks before checking links that refer to this first report.
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf8")
    if args.report:
        print("Rapport enregistré :", args.report)
    return int(any(result["returncode"] != 0 for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
