# Logiciel — Drone V2

Ce dossier prépare le développement ; aucun programme de pilotage robot n’est encore livré.
La base choisie est Raspberry Pi OS Lite sur microSD, configuré depuis le Mac sans écran.
Le routeur externe relie Pi et Mac sur un réseau local ; aucun service Internet requis.

## Fonctions à développer

| Partie | Responsabilité |
| --- | --- |
| Commande sur le Mac | Envoyer avance, recul, virage et arrêt, renouveler les commandes |
| Réception sur le Pi | Contrôler les messages, traiter seulement une commande valide et récente |
| Pilotage moteur | Deux canaux indépendants et autorisation nSLEEP, GPIO après relevé matériel |
| Arrêt sur absence de commande | Temporisation indépendante de la vidéo, watchdog à tester |
| Vidéo | Acquisition rpicam/libcamera, H.264 720p30 visé, MPEG-TS/UDP |
| Affichage sur le Mac | ffplay ; cadence et latence à mesurer |
| Extinction | Arrêt des moteurs, puis arrêt propre de Linux |

Au démarrage, mettre les commandes à zéro et garder nSLEEP désactivé avant toute réception.
Une commande valide récente autorise le déplacement ; absence de commande : arrêt.
Une valeur initiale de 300 ms est proposée, à ajuster aux essais.
Après reconnexion, exiger une nouvelle commande ; ne pas relancer un mouvement mémorisé.
La vidéo ne doit pas empêcher l’arrêt moteur. Tester aussi l’arrêt et le blocage du processus.
Les rappels électriques complètent le logiciel mais ne constituent pas une validation du watchdog.

La bibliothèque GPIO, le protocole, les ports, la fréquence PWM et l’interface Mac restent à
choisir.
Ne pas publier les ports sur Internet ; le fonctionnement prévu est sur le réseau local.
Les [GPIO candidats][lien-1] sont une proposition de câblage.

## Première étape logicielle

Préparer le système et détecter la Camera Module 3, puis vérifier une capture et un flux
avant d’ajouter les moteurs. Utiliser rpicam/libcamera ou Picamera2, pas raspivid.
Consigner versions et commandes réellement testées dans les [résultats][lien-2].
Le prototype doit ensuite passer les [essais de validation][lien-3].

[Documentation caméra Raspberry Pi][camera].

[camera]: https://www.raspberrypi.com/documentation/computers/camera_software.html

<!-- Liens utilisés dans ce document. -->

[lien-1]:
  <../Electronique/README.md#gpio-candidats>
[lien-2]:
  <../Validation/resultats/README.md>
[lien-3]:
  <../Validation/README.md>
