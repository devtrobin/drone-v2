# Achats — Drone V2, base issue de V5

Version active rétablie le **12 octobre 2026** : moteurs TT et batterie USB 5 V.
Prix historiques conservés ; aucune actualisation ni commande lors du retour.

**Total matériel avec fixations : 257,03 € TTC hors livraison, sans éclairage.**
Base V5 : 205,37 € ; nouveaux lots Amazon : 51,66 €. Aucun achat effectué.
Les prix de la base restent ceux de V5 ; les fixations ont été relevées le **11 octobre 2026**.
Seul le Pi Zero 2 W est prévu hors Amazon chez Letmeknow : 22,50 € affichés, en rupture au relevé.
Le total dépend de son retour à ce prix. Les autres 18 lots sont prévus sur Amazon.fr.
La cible de 150 € est dépassée de 107,03 €. Les deux livraisons restent non chiffrées.

La liste reprend tous les lots V5 pour conserver une référence complète et traçable.
**Les trois lots de condensateurs et résistances sont à confirmer, pas à acheter automatiquement.**
Le [manifeste actif](achats.json) précise chaque besoin et la décision d’achat ;
la [copie originale](Sources/achats-v5-original.json) conserve les données V5 de départ.

| Lot de référence | Prix TTC |
| --- | ---: |
| [Pi Zero 2 W seul, hors Amazon][achat-1] | 22,50 € |
| [Camera Module 3 Standard SC0872][achat-2] | 36,00 € |
| [microSD QUMOX 16 Go][achat-3] | 8,80 € |
| [2 nappes CSI pour Pi Zero][achat-4] | 6,99 € |
| [Châssis DollaTek 2WD équipé][achat-5] | 13,99 € |
| [3 modules DRV8833, un utilisé][achat-6] | 6,99 € |
| [Batterie USB VEGER 10 000 mAh][achat-7] | 18,99 € |
| [5 câbles USB-A / micro-USB 30 cm][achat-8] | 7,99 € |
| [Fil cuivre 22 AWG, 10 m][achat-9] | 7,99 € |
| [Porte-fusibles et fusibles 5 × 20 mm][achat-10] | 9,99 € |
| [100 condensateurs 100 nF][achat-11] | 6,99 € |
| [145 condensateurs, dont 470 µF][achat-12] | 8,99 € |
| [250 résistances, dont 1 kΩ et 10 kΩ][achat-13] | 8,99 € |
| [Gaine thermorétractable, 150 tronçons][achat-14] | 8,99 € |
| [Colliers nylon, 200 pièces][achat-15] | 3,10 € |
| [Mousse double face][achat-16] | 7,32 € |
| [2 adaptateurs USB-C / USB-A][achat-17] | 7,18 € |
| [Fil à souder avec flux, 20 g][achat-18] | 6,59 € |
| [Lecteur microSD AXFEE USB-C][achat-19] | 6,99 € |
| **Composants principaux** | **114,26 €** |
| **Fournitures, lecteur compris** | **91,11 €** |
| **Total de référence V5** | **205,37 €** |

Les prix correspondent à un lot entier par ligne, même si seule une partie sera utilisée.
Le lecteur et l’adaptateur Mac sont du matériel de préparation/recharge, pas des cartes embarquées.

## Compléments électroniques à confirmer

| Lot conditionnel | Prix TTC |
| --- | ---: |
| Céramiques 100 nF | 6,99 € |
| Électrolytiques dont 470 µF | 8,99 € |
| Résistances | 8,99 € |
| **Total conditionnel déjà inclus dans V5** | **24,97 €** |

Sous-total avec fixations avant ces lots : **232,06 €**, soit 82,06 € au-dessus de 150 €.
Ce sous-total n’est pas un panier final validé : des pièces restent potentiellement nécessaires.
Le DRV8833 possède des rappels internes ; le module peut aussi intégrer du découplage.
Relever ce qui est présent et mesurer l’alimentation avant de décider des compléments.
Une ou deux pièces utiles ne signifient pas que tous les composants d’un assortiment seront montés.
Voir le [câblage](Electronique/README.md). Aucune carte électronique sur mesure n’est prévue.

## Fixations ajoutées après l’assemblage

Prix des **lots entiers**, pages Amazon lues directement, sans coupon ni abonnement.
Voir le [relevé daté](Sources/fixations-amazon.json) pour vendeurs, variantes et contenu.

| Lot Amazon | Besoins couverts | Prix TTC |
| --- | --- | ---: |
| [940 pièces nylon Gueenky][fix-1] | M02 et M04 : entretoises caméra et Pi | 20,49 € |
| [900 vis, écrous et rondelles FandWay][fix-2] | M03, M05 et M07 : M2, M2,5 et M3 | 10,99 € |
| [4 plaques ABS 300 × 200 × 3 mm][fix-3] | M01 et M06 : matière pour supports | 13,49 € |
| [50 colliers Zenitech 250 × 7,6 mm][fix-4] | M08 : deux attaches batterie | 6,69 € |
| **Total supplémentaire** | **4 lots commandables au relevé** | **51,66 €** |

M09 : immobiliser les deux porte-fusibles avec les [colliers V5][achat-15]
et la [mousse V5][achat-16], déjà comptés ; **0 € supplémentaire**.
Prévoir le passage des colliers dans la plaque, puis vérifier la retenue.
Cette solution remplace les clips rigides provisoires du STEP.

Les plaques sont de la matière première : découpe, perçage et pliage des supports restent à faire.
Leur fabrication au fablab n’est pas incluse dans le coût matériel ; aucun support fini fourni.
Une petite chute suffit pour le porte-pilote et une équerre caméra avec fenêtre arrière.
Maintenir le pilote avec les petits colliers disponibles, hors composants et pistes exposées.

**Écarts à adapter avant fabrication :** la CAO proposait 6 mm d’entretoise et 2 mm d’équerre.
Le lot nylon contient des M2 / M2,5 de **5 mm**, le lot ABS des plaques de **3 mm**.
Contrôler l’accès aux prises et les dégagements, ajuster les vis et l’implantation.
Le lot FandWay contient M2×12, M2,5×12 et M3×8/12 notamment ; choisir après empilage.
L’isolation nylon/ABS doit empêcher la visserie métallique de toucher les pistes.
Les colliers batterie de 7,6 mm passent en largeur dans les fentes proposées de 10,5 mm ;
leur épaisseur et leur tête restent à mesurer avant d’ajuster la hauteur des passages.

La roulette et les brides moteurs sont supposées dans le kit : pas de rachat en double.
Si une rehausse de 18 mm est nécessaire, étudier les M3 de 15 mm et une cale ABS de 3 mm
des lots ci-dessus ; géométrie et résistance à confirmer, pas une hauteur garantie du kit.

| Budget matériel | Montant TTC hors port |
| --- | ---: |
| Base V5 complète | 205,37 € |
| Fixations et matière pour supports | 51,66 € |
| **Total matériel prévisionnel** | **257,03 €** |
| Dont Amazon | 234,53 € |
| Dont Pi hors Amazon | 22,50 € |
| Avant les trois lots électroniques conditionnels | 232,06 € |
| Dépassement de la cible 150 € | 107,03 € |

Ce total conserve les prix historiques de la base et le Pi indisponible à son relevé.
Revalider le panier avant commande. Port et prestations fablab restent à ajouter s’ils sont payants.
Les [calculs de roulage](Mecanique/performance.md) donnent les performances sous hypothèses.

## Avant une commande

- Revalider stock du vrai Pi Zero 2 W, référence caméra SC0872 et prix des lots.
- Confirmer roulette dans le châssis, courant des moteurs et boîtier du DRV8833.
- Décider des compléments après inspection, sans supposer un stock gratuit au fablab.
- Vérifier l’adaptateur Mac : retirer 7,18 € seulement si le port ou l’adaptateur est disponible.
- Ajouter les deux livraisons au montant réellement payé ; elles sont hors plafond matériel.

Les [fiches](Composants/README.md) indiquent contenu, quantité utile et réserves de chaque lot.
Après un remplacement, modifier le manifeste et recalculer tous les totaux.

[achat-1]: https://letmeknow.fr/fr/cartes-officielles/2497-raspberry-pi-zero-2-w-5056561800004.html
[achat-2]: https://www.amazon.fr/dp/B0BRY6MVXL
[achat-3]: https://www.amazon.fr/dp/B00IPC1OUA
[achat-4]: https://www.amazon.fr/dp/B07MW7V3Y7
[achat-5]: https://www.amazon.fr/dp/B07F73HY34
[achat-6]: https://www.amazon.fr/dp/B076KFRJWL
[achat-7]: https://www.amazon.fr/dp/B096MN8FBV
[achat-8]: https://www.amazon.fr/dp/B095JZSHXQ
[achat-9]: https://www.amazon.fr/dp/B0BG3W15YT
[achat-10]: https://www.amazon.fr/dp/B07KQ46H6K
[achat-11]: https://www.amazon.fr/dp/B0CLQRL6VB
[achat-12]: https://www.amazon.fr/dp/B0F4K5922R
[achat-13]: https://www.amazon.fr/dp/B0BTP88DZN
[achat-14]: https://www.amazon.fr/dp/B0C2GXY7SF
[achat-15]: https://www.amazon.fr/dp/B0GW1D8PB9
[achat-16]: https://www.amazon.fr/dp/B09DQ5FDV6
[achat-17]: https://www.amazon.fr/dp/B0B9N3QSL3
[achat-18]: https://www.amazon.fr/dp/B0DBSZQG44
[achat-19]: https://www.amazon.fr/dp/B0DCVDVMQ3

[fix-1]: https://www.amazon.fr/dp/B0CLD4DVVY
[fix-2]: https://www.amazon.fr/dp/B0F3HGKQD2
[fix-3]: https://www.amazon.fr/dp/B0F8BG9GYH
[fix-4]: https://www.amazon.fr/dp/B07D7G47WZ
