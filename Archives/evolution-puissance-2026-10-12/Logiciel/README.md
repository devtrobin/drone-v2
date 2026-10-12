# Logiciel — Drone V2

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

> Révision du 12 octobre 2026 : voir la [conception puissance][archive-lien-1].
> Choisir le profil MD13S puissance explicitement ; le profil par défaut reste DRV8833.


Première version du pilotage : serveur Pi, interface clavier Mac, simulation et lanceur vidéo.
Le code de commande est testé hors matériel ; la caméra et les GPIO réels restent à valider.
Python 3.10 ou supérieur ; bibliothèque standard pour la simulation et le réseau.

| Document / dossier | Rôle |
| --- | --- |
| [Installation][archive-lien-2] | Préparation Mac, microSD et Pi |
| [Utilisation][archive-lien-3] | Simulation, connexion, GPIO et vidéo |
| [Protocole][archive-lien-4] | Messages, délais et comportement d’arrêt |
| [Code][archive-lien-5] | Serveur, pilote, moteurs et vidéo |
| [Configuration][archive-lien-6] | GPIO BCM candidats, validation désactivée |
| [Tests][archive-lien-7] | Commandes, TCP local et broches simulées |

## Essayer sans matériel

Depuis ce dossier, sans bibliothèque supplémentaire :

```bash
python3 -m drone.demo
python3 -m unittest discover -s tests -v
```

La démonstration utilise TCP local et des moteurs simulés. Elle fait avancer, tourner et reculer
les sorties, puis vérifie l’arrêt sur absence de commande. Aucun GPIO ni clé persistante.
Pour les broches simulées de GPIO Zero, voir l’[installation][archive-lien-8].
Le contrôle global et le rapport sont décrits dans les [outils][archive-lien-9].

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
Les choix techniques s’appuient sur les [sources officielles][archive-lien-10].

[archive-lien-1]: puissance.md
[archive-lien-2]: installation.md
[archive-lien-3]: utilisation.md
[archive-lien-4]: protocole.md
[archive-lien-5]: ../../../Logiciel/drone
[archive-lien-6]: config/robot.example.json
[archive-lien-7]: ../../../Logiciel/tests
[archive-lien-8]: installation.md
[archive-lien-9]: ../tools/README.md
[archive-lien-10]: ../../../Sources/verification-technique.md

[statut-archive]: ../README.md
