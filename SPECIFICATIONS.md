# Spécifications — Drone terrestre V2

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
| Budget | Cible 150 € hors livraison ; référence V5 205,37 €, cible non atteinte |

La carte est un Pi Zero 2 W et la caméra une Module 3 Standard SC0872 avec autofocus.
La microSD 16 Go est destinée à Raspberry Pi OS Lite, sans enregistrement vidéo prévu.
Les 12 MP du capteur ne sont pas la résolution du flux vidéo visé.
L’éclairage, la conduite autonome, la cartographie, l’usage extérieur humide et les encodeurs
électroniques sont hors du premier prototype. Les disques fournis ne nécessitent pas de capteurs.

Les trois lots de condensateurs et résistances sont des compléments conditionnels.
Ils ne justifient pas la création d’une carte ; contrôler le module existant et les mesures.
Le sous-total de 180,40 € avant ces lots n’est pas un coût final garanti et dépasse aussi 150 €.
Les ressources du fablab et les frais de port restent à confirmer séparément.

Voir l’[architecture](architecture.md), les [achats](listeAchat.md)
et les [essais de validation](Validation/README.md). Aucune cible n’est encore mesurée.
