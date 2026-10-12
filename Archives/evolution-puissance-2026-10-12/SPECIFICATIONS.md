# Spécifications — Drone V2 puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Révision du 12 octobre 2026, prototype terrestre à deux roues motrices et appui passif.

| Élément | Choix / objectif |
| --- | --- |
| Vitesse | 6–8 km/h visés ; prévision 6,4–7,7 km/h |
| Calculateur | Raspberry Pi Zero 2 W, hors Amazon |
| Caméra | Camera Module 3 Standard d'origine V1 |
| Communication | Wi-Fi local 2,4 GHz, Mac et routeur |
| Vidéo | H.264 720p30 / UDP ; à tester sur Pi |
| Motorisation | 2 CQRobot 37D 18,8:1, 12 V, sans encodeur |
| Roues | Pololu 80 mm et moyeux 6 mm à adapter |
| Pilotes | 2 MD13S PWM/DIR ; annonce à identifier |
| Batterie | 1 LiPo 3S 2200 mAh, second pack en réserve |
| Alimentation Pi | UBEC 5 V, micro-USB PWR IN |
| Décharge | Coupure pack + alarme par cellule, usage surveillé |
| Recharge | SkyRC e3 3S, hors robot, secteur |
| Autonomie | 78 min centrales estimées ; 39–98 min selon usage |
| Essai initial | PWM 25 %, rotation 8 %, rampe 0,30/s |
| Arrêt réseau | Délai logiciel 300 ms ; arrêt réel à mesurer |
| Budget prévisionnel | 508,07 € hors livraison, fabrication et outils |
| Plafond historique | 150 € hors livraison, non atteint |
| CAO | STEP existants historiques, nouvelle implantation à réaliser |

Sans éclairage, enregistrement vidéo, encodeurs ou PCB personnalisé. Aucun achat ni essai physique
validé. Voir les [achats][archive-lien-1], le [circuit][archive-lien-2] et les
[calculs][archive-lien-3].

[archive-lien-1]: listeAchat.md
[archive-lien-2]: Electronique/puissance.md
[archive-lien-3]: Mecanique/performance-puissance.md

[statut-archive]: README.md
