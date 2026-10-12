# Drone terrestre V2

Version active rétablie le **12 octobre 2026** : base V5 avec moteurs TT du kit 2WD, roues
d'origine, pilote DRV8833 et batterie USB 5 V. Raspberry Pi Zero 2 W, Camera Module 3 Standard et
pilotage Wi-Fi avec vidéo conservés.

**Vitesse maximale estimée : environ 2,2 km/h**, sous les hypothèses du moteur analogue, à pleine
commande. Le profil reste limité à 35 % pour les premiers essais ; cette limite ne permet pas
d'atteindre la vitesse maximale estimée. Aucun essai physique n'est enregistré.

**Budget prévisionnel restauré : 257,03 € hors livraison**, dont 205,37 € de base V5 et 51,66 € de
fixations. La cible historique de 150 € reste non atteinte. Prix historiques, Pi indisponible au
dernier relevé ; revalider avant achat.

| Pour reprendre le projet | Document |
| --- | --- |
| État et travail restant | [État](project_state.md), [tâches](TACHES.md) |
| Références, prix, total | [Achats](listeAchat.md), [JSON](achats.json) |
| Conception actuelle | [Architecture](architecture.md), [spécifications][spec] |
| Alimentation et câblage | [Électronique](Electronique/README.md) |
| Force, autonomie et virages | [Prévisions](Mecanique/performance.md) |
| Logiciel et essais | [Logiciel](Logiciel/README.md), [validation][validation] |
| Composants et fiches | [Composants](Composants/README.md) |
| Assemblage 3D de référence | [Maquette](Assemblage/README.md) |

Les 19 PDF, STEP et assemblages existants redeviennent les références de la conception active.
Leurs cotes restent documentées ou estimées, et les supports restent à adapter après réception. Le
faisceau utilise des cartes du commerce ; aucun PCB personnalisé nécessaire.

Le changement des moteurs et du système batterie/puissance est **reporté**. L'[étude de la version
rapide][archive], ses prix et son logiciel sont conservés en archive pour une évolution
ultérieure. Ses composants sont exclus du panier actif.

Contrôles depuis ce dossier :

```bash
python3 tools/check_project.py
python3 tools/run_checks.py
```

Le profil actif est Logiciel/config/robot.example.json, DRV8833 et GPIO non confirmés. Voir
l'installation avant tout essai matériel.

[spec]: SPECIFICATIONS.md
[validation]: Validation/README.md
[archive]: Archives/evolution-puissance-2026-10-12/README.md
