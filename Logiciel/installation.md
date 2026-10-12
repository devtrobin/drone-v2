# Installation — Drone V2


Guide pour Raspberry Pi OS Lite ; installation sur le Pi encore à réaliser.
Sur le Mac, utiliser un Python récent fourni par python.org avec Tkinter fonctionnel.

## Sur le Mac

Vérifier Python et, pour l’interface, la fenêtre de démonstration Tk :

```bash
python3 --version
python3 -m tkinter
ffmpeg -version
ffplay -version
```

La simulation sans fenêtre ne nécessite pas Tkinter.
Pour un Python Homebrew, installer le paquet Tk correspondant à sa version.
Installer FFmpeg pour la vidéo ; la commande seule ne nécessite pas FFmpeg.

Pour vérifier aussi GPIO Zero avec des broches simulées, depuis Logiciel :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m unittest discover -s tests -v
```

Cet environnement reste local et ignoré par Git.

## Préparer la microSD

1. Dans Raspberry Pi Imager, sélectionner Pi Zero 2 W et Raspberry Pi OS Lite compatible.
2. Choisir son utilisateur ; ne pas supposer l’existence du compte historique pi.
3. Configurer le nom drone-v2, le pays Wi-Fi FR et le réseau local 2,4 GHz.
4. Activer SSH avec sa clé personnelle ; vérifier le lecteur avant écriture.
5. Retrouver l’IP sur le routeur si drone-v2.local ne résout pas.
6. Brancher la nappe caméra hors tension et verrouiller les deux connecteurs.

Le Mac et le Pi utilisent le même réseau local, sans isolation entre clients Wi-Fi.
Imager écrit la carte sélectionnée ; vérifier sa capacité et le lecteur.

## Sur le Pi, moteurs débranchés

Après connexion SSH avec l’utilisateur choisi :

```bash
sudo apt update
sudo apt install python3-gpiozero python3-lgpio rpicam-apps-lite ffmpeg
rpicam-hello --list-cameras
rpicam-still --nopreview --timeout 2000 --output camera-test.jpg
```

Copier Logiciel dans son répertoire personnel par scp ou via le dépôt du projet.
Noter versions OS, Python, GPIO Zero, lgpio, rpicam et FFmpeg dans le résultat V06.
Vérifier l’accès utilisateur à /dev/gpiochip0 et son appartenance au groupe gpio.
La capture caméra et l’installation sont des essais à faire, pas des résultats obtenus.

## Préparer les paramètres

Depuis le dossier Logiciel du Pi :

```bash
cp config/robot.example.json config/robot.local.json
python3 -m drone.server --key-file secrets/control.key --create-key
```

La clé n’est jamais imprimée ; fichier créé en mode 600, sans écrasement.
Copier cette clé sur le Mac par SSH dans Logiciel/secrets/control.key et garder le mode 600.
Laisser hardware_confirmed à false jusqu’au contrôle du module et du faisceau.
Le logiciel ne réalise pas cette validation à la place du montage.
Voir l’[utilisation](utilisation.md) et les [sources](../Sources/verification-technique.md).
