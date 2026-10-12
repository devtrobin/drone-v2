"""Commandes vidéo sans shell ; aperçu des arguments par défaut."""
import argparse
import ipaddress
import subprocess


def stream_command(host, port):
    ipaddress.IPv4Address(host)
    if not 1024 <= port <= 65535:
        raise ValueError("Port vidéo entre 1024 et 65535")
    # Hardware H.264 bitstream is copied into MPEG-TS, without software re-encoding.
    return (["rpicam-vid", "--timeout", "0", "--nopreview", "--codec", "h264",
             "--width", "1280", "--height", "720", "--framerate", "30",
             "--bitrate", "2000000", "--inline", "--intra", "30",
             "--autofocus-mode", "continuous", "--output", "-"],
            ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-fflags", "+genpts",
             "-r", "30", "-f", "h264",
             "-i", "pipe:0", "-c:v", "copy", "-an", "-f", "mpegts",
             f"udp://{host}:{port}?pkt_size=1316"])


def view_command(port):
    if not 1024 <= port <= 65535:
        raise ValueError("Port vidéo entre 1024 et 65535")
    return ["ffplay", "-fflags", "nobuffer", "-flags", "low_delay", "-framedrop",
            "-probesize", "32768", "-analyzeduration", "100000", "-f", "mpegts",
            f"udp://0.0.0.0:{port}?fifo_size=8192&overrun_nonfatal=1"]


def run_pipeline(camera_args, mux_args):
    camera = mux = None
    try:
        camera = subprocess.Popen(camera_args, stdout=subprocess.PIPE)
        mux = subprocess.Popen(mux_args, stdin=camera.stdout)
        camera.stdout.close()
        while camera.poll() is None and mux.poll() is None:
            try:
                mux.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                pass
        camera_code, mux_code = camera.poll(), mux.poll()
        return 1 if camera_code not in (None, 0) or mux_code not in (None, 0) else 0
    except KeyboardInterrupt:
        return 0
    finally:
        for process in (mux, camera):
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("stream", "view"))
    parser.add_argument("--host", help="IPv4 du Mac destinataire, pour stream")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--run", action="store_true", help="Exécuter ; sinon afficher seulement")
    args = parser.parse_args(argv)
    import shlex
    try:
        if args.mode == "stream":
            commands = stream_command(args.host or "", args.port)
            if args.run:
                return run_pipeline(*commands)
            print(" | ".join(shlex.join(command) for command in commands))
        else:
            command = view_command(args.port)
            if args.run:
                return subprocess.call(command)
            print(shlex.join(command))
        return 0
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
