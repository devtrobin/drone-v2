# Spécifications — Drone terrestre V2

Version active rétablie le **12 octobre 2026** : moteurs TT et batterie USB 5 V.
Vitesse maximale estimée environ 2,2 km/h ; essais initiaux à PWM 35 %.

Premier prototype intérieur roulant, commandé à distance depuis le Mac déjà disponible.

| Fonction | Cible à démontrer |
| --- | --- |
| Déplacement | Avancer, reculer, tourner par commande différentielle des deux roues |
| Pilotage | Commandes Wi-Fi sur le réseau local du routeur disponible |
| Vidéo | Camera Module 3, cible H.264 1280 × 720 à 30 images/s |
| Réception | MPEG-TS sur UDP vers ffplay sur Mac, latence à mesurer |
| Autonomie | Au moins 15 minutes en pilotage avec vidéo |
| Absence de commande | Arrêt moteur ; délai initial proposé 300 ms, à tester |
| Démarrage / reconnexion | Moteurs arrêtés jusqu’à une nouvelle commande explicite |
| Alimentation | Batterie USB 5 V, branches Pi/caméra et moteurs protégées |
| Fabrication | Châssis équipé du commerce, câblage soudé, pas de PCB sur mesure |
| Achats | Amazon.fr, exception limitée au Raspberry Pi seul |
| Budget | Cible 150 € ; matériel avec fixations 257,03 € hors port, cible non atteinte |

La carte est un Pi Zero 2 W et la caméra une Module 3 Standard SC0872 avec autofocus.
La microSD 16 Go est destinée à Raspberry Pi OS Lite, sans enregistrement vidéo prévu.
Les 12 MP du capteur ne sont pas la résolution du flux vidéo visé.
L’éclairage, la conduite autonome, la cartographie, l’usage extérieur humide et les encodeurs
électroniques sont hors du premier prototype. Les disques fournis ne nécessitent pas de capteurs.

Les trois lots de condensateurs et résistances sont des compléments conditionnels.
Ils ne justifient pas la création d’une carte ; contrôler le module existant et les mesures.
Avec fixations, le sous-total de 232,06 € avant ces lots dépasse aussi 150 €.
Les ressources du fablab et les frais de port restent à confirmer séparément.

Voir l’[architecture](architecture.md), les [achats](listeAchat.md)
et les [essais de validation](Validation/README.md).
Le logiciel de commande est testé hors matériel ; les cibles physiques restent à mesurer.
TCP 8765 et UDP 5000 sont les ports initiaux ; voir le [protocole](Logiciel/protocole.md).
Les [STEP des composants](Composants/modeles-3d.md) sont des modèles d’implantation provisoire.
Les supports et l’implantation proposés dans la maquette restent à confirmer après mesure.
Les [prévisions de performance](Mecanique/performance.md) ne sont pas des performances mesurées.
