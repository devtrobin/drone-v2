# Architecture — Drone terrestre V2

Conception de départ issue de V5, avec composants du commerce et montage intérieur.
Les références, prix datés et décisions d’achat sont dans [achats.json](achats.json).
Le Pi et la caméra conservent la base informatique initiale ; le châssis est un kit équipé.
Aucun assemblage, logiciel robot, alimentation ou comportement mécanique encore validé.

```mermaid
flowchart LR
    Mac[Mac : commandes et affichage] <-->|Wi-Fi local| Routeur[Routeur disponible]
    Routeur <-->|Wi-Fi 2,4 GHz| Pi[Pi Zero 2 W]
    SD[microSD : système et logiciel] --- Pi
    Camera[Camera Module 3 Standard] -->|CSI| Pi
    Pi -->|Commandes GPIO 3,3 V| Pilote[Module DRV8833 assemblé]
    Pilote --> Gauche[Moteur gauche]
    Pilote --> Droit[Moteur droit]
```

Le Pi acquiert la caméra et diffuse une cible H.264 720p30 en MPEG-TS/UDP vers ffplay.
Il traite les commandes et l’arrêt sur absence de commande ; la vidéo ne doit pas bloquer cet arrêt.
Le système prévu est Raspberry Pi OS Lite, sur microSD 16 Go sans enregistrement vidéo.
Utiliser la pile caméra rpicam/libcamera ; raspivid ne prend pas en charge la Camera Module 3.
La caméra nécessite une nappe 15 vers 22 broches adaptée au Pi Zero.

## Énergie et mécanique

La batterie USB fournit le 5 V à deux branches protégées : Pi/caméra et pilote/moteurs.
Le Pi est alimenté par PWR IN, pas par une broche de commande.
Les masses sont communes ; les pointes moteurs partagent la même source avec la vidéo.
L’annonce 3 A ne garantit pas les démarrages simultanés : mesurer les tensions et courants.
La recharge est prévue séparément depuis le Mac ; ne pas supposer une fonction pass-through.

Le châssis DollaTek regroupe plaque, motoréducteurs, roues et fixations.
La roulette visible sur sa photo doit être confirmée dans le contenu réel du lot.
Les capteurs d’encodeur et les piles AA ne sont pas prévus.
La caméra reste orientée vers l’avant ; ses supports et le passage de nappe sont à définir.
Positionner la batterie bas, conserver accès aux prises et immobiliser les fils.

## Pas de carte électronique sur mesure

Pi et DRV8833 sont des cartes déjà assemblées. Le travail électronique est le câblage.
Les condensateurs et résistances supplémentaires sont à confirmer après inspection et essais.
Leurs lots restent chiffrés dans la référence V5, sans obligation de tout monter ou acheter.
La carte Pi seule n’inclut pas de barrette GPIO ; des soudures directes sont prévues.
La capacité de soudure et le maintien des fils doivent être confirmés au fablab.

Voir le [câblage détaillé](Electronique/README.md), l’[implantation](Mecanique/README.md),
le [montage](Assemblage/README.md), le [logiciel](Logiciel/README.md)
et les [essais](Validation/README.md).

## Sources techniques de la conception

- [Raspberry Pi Zero 2 W officiel][pi]
- [Installation des caméras et nappes Raspberry Pi][camera]
- [Logiciel caméra Raspberry Pi][logiciel]
- [Notice TI DRV8833][ti]

[pi]: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/
[camera]: https://www.raspberrypi.com/documentation/accessories/camera.html
[logiciel]: https://www.raspberrypi.com/documentation/computers/camera_software.html
[ti]: https://www.ti.com/lit/ds/symlink/drv8833.pdf
