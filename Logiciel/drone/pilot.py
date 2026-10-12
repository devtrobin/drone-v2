"""Interface clavier Mac : maintenir Espace et une flèche pour déplacer le robot."""
import argparse
from pathlib import Path

from .client import Pilot
from .protocol import read_key


class Keyboard:
    def __init__(self):
        self.keys = set()

    def clear(self):
        self.keys.clear()

    def values(self):
        throttle = float(("Up" in self.keys) - ("Down" in self.keys))
        turn = float(("Right" in self.keys) - ("Left" in self.keys))
        return "space" in self.keys, throttle, turn


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--key-file", type=Path, required=True)
    args = parser.parse_args(argv)
    key = read_key(args.key_file)
    import tkinter as tk
    root = tk.Tk()
    root.title("Drone V2 — pilotage")
    root.geometry("560x250")
    keyboard = Keyboard()
    pilot = None
    status = tk.StringVar(value="Déconnecté — moteurs arrêtés")

    def disconnect():
        nonlocal pilot
        keyboard.clear()
        if pilot is not None:
            try:
                pilot.command(False, 0, 0)
            except (OSError, ValueError):
                pass
            pilot.close()
            pilot = None
        status.set("Déconnecté — reconnecter explicitement")

    def connect():
        nonlocal pilot
        disconnect()
        try:
            pilot = Pilot(args.host, args.port, key)
            status.set("Connecté — maintenir Espace + flèches")
            root.focus_force()
        except (OSError, ValueError) as error:
            status.set(f"Connexion impossible : {error}")

    def stop_keys(event=None):
        keyboard.clear()
        if pilot is not None:
            try:
                pilot.command(False, 0, 0)
            except (OSError, ValueError):
                disconnect()

    def press(event):
        if event.keysym == "Escape":
            stop_keys()
        else:
            keyboard.keys.add(event.keysym)

    def release(event):
        keyboard.keys.discard(event.keysym)

    def tick():
        if pilot is not None:
            try:
                state = pilot.command(*keyboard.values())
                status.set(f"Connecté — G {state['left']:.2f} / D {state['right']:.2f}")
            except (OSError, ValueError):
                disconnect()
        root.after(50, tick)

    def quit_app():
        disconnect()
        root.destroy()

    tk.Label(root, text="Maintenir Espace + flèches\nÉchap ou perte de focus : arrêt",
             font=("Helvetica", 16)).pack(pady=20)
    tk.Label(root, textvariable=status).pack(pady=10)
    tk.Button(root, text="Connecter", command=connect).pack()
    tk.Button(root, text="Arrêter / déconnecter", command=disconnect).pack(pady=8)
    root.bind("<KeyPress>", press)
    root.bind("<KeyRelease>", release)
    root.bind("<FocusOut>", stop_keys)
    root.protocol("WM_DELETE_WINDOW", quit_app)
    root.after(50, tick)
    root.mainloop()


if __name__ == "__main__":
    main()
