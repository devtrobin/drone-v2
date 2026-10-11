# Câblage — Drone V2

Schéma de principe candidat : à valider sur le module réellement livré avant raccordement.
Le DRV8833 est acheté déjà assemblé. Aucune gravure, fabrication de PCB ou carte KiCad nécessaire.

```text
Batterie USB 5 V → câble USB-A → point de distribution en étoile
  ├─ fusible Pi → embout micro-USB conservé → Pi PWR IN → caméra par CSI
  └─ fusible moteurs → VM du DRV8833 → deux moteurs
Retours GND des deux branches et GND logique du Pi communs
Pi GPIO 3,3 V → commandes et nSLEEP du module
```

Couper un câble chiffré et conserver les deux moitiés : USB-A vers source, micro-USB vers Pi.
Identifier VBUS/GND par continuité ; isoler les fils USB de données non utilisés.
Créer des branches courtes avec les fils prévus, gaine sur chaque soudure et maintien mécanique.
Ne pas appliquer 5 V aux GPIO ou au 3V3 ; ne pas raccorder de moteur directement au Pi.
Garder la prise USB de la batterie accessible pour couper physiquement l’énergie.
Pour une extinction normale, arrêter Linux avant de débrancher afin de préserver la microSD.

## GPIO candidats

Numérotation BCM et position physique de l’empreinte GPIO, même sans barrette soudée :

| Signal du module | GPIO BCM | Position physique Pi |
| --- | ---: | ---: |
| AIN1 | 17 | 11 |
| AIN2 | 27 | 13 |
| BIN1 | 22 | 15 |
| BIN2 | 23 | 16 |
| nSLEEP | 24 | 18 |
| GND logique | GND | 6 |

Relever les connexions réelles : EEP/ULT dans l’annonce ne sont pas une preuve de brochage.
nFAULT est une sortie ; nSLEEP est l’autorisation. Vérifier les ponts et résistances du module.
Aucun rappel vers 5 V ne doit arriver aux GPIO. Contrôler l’arrêt pendant boot, reset et extinction.
Le Pi nu reçoit des fils soudés directement, immobilisés sans traction sur les pastilles.

## Condensateurs, résistances et protections

Le DRV8833 intègre des rappels vers GND sur ses commandes et sur nSLEEP.
Ils ne prouvent pas l’état du module assemblé : son constructeur peut ajouter un rappel ou un pont.
Les quatre 10 kΩ et le rappel nSLEEP envisagés dans V5 ne sont pas imposés automatiquement.
Décider des rappels externes seulement après relevé du module et contrôle de l’état au démarrage.

Un 100 nF aux bornes de chaque moteur est une piste pour réduire les parasites.
Les 470 µF envisagés près des branches sont une piste de stabilisation, pas une valeur validée.
Contrôler d’abord les éléments de découplage du module ; mesurer les chutes de tension sous charge.
Ne pas remplacer un condensateur du module requis par sa notice par une valeur arbitraire.
Les électrolytiques supplémentaires doivent respecter polarité et tension nominale suffisante.
Quelques compléments peuvent être soudés au faisceau ou au moteur, sans carte sur mesure.

Dimensionner les deux fusibles selon mesures et fils réels, sans reprendre le 10 A de Drone V1.
Le lot comporte plusieurs calibres, mais aucun n’est validé pour cet ensemble à ce stade.
La notice TI distingue 500 mA RMS par pont pour PW et 1,5 A pour PWP/RTY ;
identifier le boîtier réel, mesurer le démarrage et le courant sous charge des moteurs.
Les protections du pilote et de la batterie ne remplacent pas un dimensionnement du faisceau.
Les [lots conditionnels](../listeAchat.md#compléments-électroniques-à-confirmer) restent à décider.

## Relevé avant montage

| Contrôle | Résultat actuel |
| --- | --- |
| Modèle, boîtier et repérage des bornes DRV8833 | Non relevés |
| Rappels et ponts nSLEEP / commandes | Non relevés |
| Condensateurs et résistances présents sur le module | Non relevés |
| Courants des deux moteurs, démarrage et charge | Non mesurés |
| 5 V au Pi pendant vidéo et démarrages | Non mesuré |
| Protections et tenue de sortie de la batterie | Non vérifiées |
| Calibres des fusibles et compléments retenus | Non déterminés |

Commencer les essais sur alimentation limitée en courant, roues levées, pilote désactivé.
Suivre la [validation](../Validation/README.md) avant déplacement sur le sol.

[Notice TI DRV8833](https://www.ti.com/lit/ds/symlink/drv8833.pdf).
