# Logiciel — Drone V2


Première version du pilotage : serveur Pi, interface clavier Mac, simulation et lanceur vidéo.
Le code de commande est testé hors matériel ; la caméra et les GPIO réels restent à valider.
Python 3.10 ou supérieur ; bibliothèque standard pour la simulation et le réseau.

| Document / dossier | Rôle |
| --- | --- |
| [Installation](installation.md) | Préparation Mac, microSD et Pi |
| [Utilisation](utilisation.md) | Simulation, connexion, GPIO et vidéo |
| [Protocole](protocole.md) | Messages, délais et comportement d’arrêt |
| [Code](drone/) | Serveur, pilote, moteurs et vidéo |
| [Configuration](config/robot.example.json) | GPIO BCM candidats, validation désactivée |
| [Tests](tests/) | Commandes, TCP local et broches simulées |

## Essayer sans matériel

Depuis ce dossier, sans bibliothèque supplémentaire :

```bash
python3 -m drone.demo
python3 -m unittest discover -s tests -v
```

La démonstration utilise TCP local et des moteurs simulés. Elle fait avancer, tourner et reculer
les sorties, puis vérifie l’arrêt sur absence de commande. Aucun GPIO ni clé persistante.
Pour les broches simulées de GPIO Zero, voir l’[installation](installation.md).
Le contrôle global et le rapport sont décrits dans les [outils](../tools/README.md).

## Choix de cette première version

- Commandes sur TCP 8765, un seul pilote ; vidéo séparée sur UDP 5000.
- Tkinter : maintenir Espace et les flèches ; Échap ou perte de focus demande l’arrêt.
- HMAC, séquences croissantes et ticket serveur neuf à chaque échange.
- Délai initial 300 ms, boucle avec attente réseau maximale de 20 ms.
- À expiration : sorties nulles, nSLEEP bas, session fermée ; reconnexion manuelle.
- PWM initial 100 Hz, limite à 35 %, pause de 50 ms après arrêt ou inversion.
- H.264 avec rpicam-vid, transport MPEG-TS par ffmpeg sans réencodage.

L’arrêt libère les ponts : roue libre, sans freinage actif. Fréquence PWM, puissance et inertie
restent à mesurer. L’interface graphique n’a pas encore été essayée manuellement sur le Mac.
Le gel complet du processus, SIGKILL ou une panne Linux ne sont pas couverts par ce watchdog.
V10 doit vérifier ces cas ; une coupure indépendante reste à définir si nécessaire.
Aucun démarrage moteur automatique au boot n’est installé.
Les GPIO exigent une configuration locale confirmée et l’option explicite --hardware.
Les choix techniques s’appuient sur les [sources officielles](../Sources/verification-technique.md).
