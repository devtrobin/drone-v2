# Dimensions estimées - Drone V2

Les 19 composants ont été examinés. 30 groupes de cotes manquantes sont estimés
sur 16 composants ; les dimensions utiles des trois autres sont déjà documentées.
Valeurs en millimètres, sans mesure physique.
Ces hypothèses alimentent les [modèles STEP](../Composants/modeles-3d.md).

## Utilisation

Les valeurs centrales servent à une première implantation ; les plages couvrent les doutes
sur la variante, l’échelle des photos et la méthode. Ce ne sont ni des tolérances fabricant
ni des intervalles statistiques. Utiliser la borne haute pour réserver un encombrement.
Les sources analogues ne remplacent pas les références d’achat V5.
Confirmer dimensions et perçages avant fabrication. Les masses ne sont pas estimées ici.
Le fichier releves.json reste réservé aux mesures du prototype.

## Par composant

### Raspberry Pi Zero 2 W

[Fiche][fiche-raspberry-pi-zero-2-w]
[Données][dims-raspberry-pi-zero-2-w]
[PDF][pdf-raspberry-pi-zero-2-w]

- **Hauteur carte nue** : 5,5 mm.
  Axes : h. Plages : 5-7 mm.
  analogie + photo ; confiance moyenne. Le Zero original est donné pour 5 mm. Le Zero 2 W
conserve les prises de cette famille ; marge pour composants dessous. Hors fils, nappe et
supports.

La hauteur avec fils et fixations dépend du montage ; la masse reste à relever.

- [E1 : Raspberry Pi Zero original : format de famille][source-raspberry-pi-zero-2-w-E1]
  Zero original : 65 × 30 × 5 mm ; hauteur non certifiée pour Zero 2 W

### Camera Module 3 Standard

[Fiche][fiche-camera-module-3-standard]
[Données][dims-camera-module-3-standard]
[PDF][pdf-camera-module-3-standard]

Dimensions utiles déjà documentées ; pas d’estimation supplémentaire.

Dimensions utiles déjà documentées ; aucune estimation supplémentaire nécessaire.

### Carte microSD QUMOX 16 Go

[Fiche][fiche-microsd-16go]
[Données][dims-microsd-16go]
[PDF][pdf-microsd-16go]

Dimensions utiles déjà documentées ; pas d’estimation supplémentaire.

Dimensions utiles déjà documentées ; aucune estimation supplémentaire nécessaire.

### Nappes CSI GeeekPi pour Pi Zero

[Fiche][fiche-nappe-csi-pi-zero]
[Données][dims-nappe-csi-pi-zero]
[PDF][pdf-nappe-csi-pi-zero]

- **Largeurs aux contacts** : 16 × 11,5 mm.
  Axes : camera / Pi. Plages : 15-17 / 11-12.5 mm.
  calcul du pas + photo ; confiance moyenne. Largeur entre centres : (15-1) × 1 = 14 mm et
(22-1) × 0,5 = 10,5 mm. Ajouter les marges isolantes visibles ; les oreilles peuvent dépasser.

- **Épaisseur** : 0,2 × 0,3 mm.
  Axes : ruban / bout renforce. Plages : 0.1-0.3 / 0.25-0.4 mm.
  analogie FFC ; confiance faible. Ordre de grandeur du ruban flexible ; exemple Molex pour les
bouts renforcés. Le ruban doré GeeekPi peut être un FPC différent.

Les longueurs commerciales restent 160 et 300 mm ; les oreilles ne sont pas des largeurs cotées.

- [E1 : Molex Premo-Flex : exemple FFC 0,5 mm][source-nappe-csi-pi-zero-E1]
  Exemple FFC : extrémité 0,30 ± 0,05 mm ; référence Molex distincte de GeeekPi

### Châssis DollaTek 2WD équipé

[Fiche][fiche-chassis-2wd]
[Données][dims-chassis-2wd]
[PDF][pdf-chassis-2wd]

- **Plaque** : 200 × 140 × 3 mm.
  Axes : L / l / e. Plages : 180-220 / 125-155 / 2-4 mm.
  analogie + photo ; confiance faible. E1 donne 200 × 140 mm. Sur vue-01 : plaque environ 590 ×
410 px ; boîtier AA environ 190 × 185 px. Avec E3 comme échelle approximative on obtient environ
194 × 133 mm. Épaisseur 3 mm hypothèse de plaque PMMA de kit.

- **Roue motrice** : 65 × 25 mm.
  Axes : D / l. Plages : 60-70 / 22-30 mm.
  analogie ; confiance moyenne. Même famille visuelle de roues jaunes TT que le kit E1 ;
diamètre et largeur restent ceux d’un analogue.

- **Corps moteur TT** : 70 × 22 × 18 mm.
  Axes : L / l / h. Plages : 65-75 / 20-25 / 16-22 mm.
  analogie ; confiance moyenne. Géométrie de moteur TT jaune similaire à E2. Hors axes, disques
encodeurs, fils et équerres ; aucun courant ni rapport de réduction déduit.

- **Appui pivotant** : 40 × 32 × 25 mm.
  Axes : L / l / h. Plages : 30-50 / 25-40 / 20-35 mm.
  rapport photo ; confiance faible. Vue-01 : appui environ 130 × 105 px, rapporté au boîtier AA
190 × 185 px et E3. Hauteur 20-35 mm hypothèse liée à la roue et aux entretoises visibles ;
roulette pivotante, pas bille fixe certifiée.

- **Boîtier quatre AA** : 63 × 58 × 16 mm.
  Axes : L / l / h. Plages : 60-70 / 55-65 / 15-20 mm.
  analogie ; confiance moyenne. Boîtier du kit visuellement proche de E3. Boîtier inutilisé dans
l’alimentation V2 ; aucun achat ajouté.

- **Kit assemblé** : 200 × 185 × 70 mm.
  Axes : L / l / h. Plages : 180-230 / 160-210 / 60-85 mm.
  enveloppe par analogie ; confiance faible. Enveloppe de la plaque et des roues visibles, sans
Pi, batterie USB ni caméra. Largeur dépend du déport des roues et hauteur dominée par leur
diamètre.

- **Voie entre roues** : 160 mm.
  Axes : entraxe. Plages : 140-180 mm.
  hypothèse géométrique ; confiance faible. Enveloppe largeur 185 mm moins une largeur de pneu
25 mm : 160 mm entre plans médians. Ce n’est pas la distance entre contacts d’appui mesurée.

- **Perçages ronds** : 3,2 mm.
  Axes : D. Plages : 2.7-4 mm.
  photo + visserie probable ; confiance faible. Trous visibles compatibles avec visserie de
petit kit ; hypothèse M3 seulement. Les positions et lumières ne peuvent pas être déduites
proprement de cette perspective.

La vue éclatée contient probablement des éléments redimensionnés ; les roues de cette vue ne
servent pas à étalonner la plaque.
Les plages sont des hypothèses de travail, pas des tolérances fabricant. Ne pas reporter les
anciens perçages V1.

- [E1 : SunRobotics : kit 2WD acrylique similaire][source-chassis-2wd-E1]
  Kit analogue : plaque 200 × 140 mm ; roues Ø 65 × 25 mm. Autre marque et couleur.

- [E2 : Adafruit 3777 : motoréducteur TT similaire][source-chassis-2wd-E2]
  Moteur analogue : corps 70 × 22 × 18 mm, hors arbre et câbles ; caractéristiques électriques
non transférées.

- [E3 : Adafruit 3784 : support quatre AA similaire][source-chassis-2wd-E3]
  Boîtier ouvert analogue 62,5 × 57,3 × 16 mm ; sortie DC différente.

### Module double pont en H DRV8833

[Fiche][fiche-drv8833]
[Données][dims-drv8833]
[PDF][pdf-drv8833]

- **Hauteur module nu** : 5 mm.
  Axes : h. Plages : 3.5-6.5 mm.
  photo + hypothèse PCB ; confiance faible. Carte 18,5 × 16 mm connue de l’annonce ;
condensateur le plus haut sur vue-03. Estimation : PCB environ 1,6 mm + composant 2-4 mm. Hors
barrettes à souder et fils.

- **Pas / trou de contact** : 2,54 × 1 mm.
  Axes : pas / D. Plages : 2.4-2.7 / 0.8-1.3 mm.
  rapport photo ; confiance moyenne. Vue-03 : cinq intervalles couvrent environ 13 mm sur un
bord de carte 16 mm. Pas standard 2,54 mm plausible ; ces trous sont électriques, pas des
fixations mécaniques.

Aucun trou de fixation dédié confirmé. Hauteur avec barrettes dépend du montage ; le poids 10 g
de colis reste exclu.

### Batterie USB VEGER 10 000 mAh

[Fiche][fiche-batterie-usb]
[Données][dims-batterie-usb]
[PDF][pdf-batterie-usb]

- **Dégagement devant USB** : 40 mm.
  Axes : recul. Plages : 30-60 mm.
  enveloppe de branchement ; confiance faible. Embout USB estimé 25-40 mm + marge de sortie et
courbure. Cette valeur est un espace à réserver, pas une nouvelle cote du corps VEGER.

Le corps reste 106 × 68 × 15 mm annoncé ; ajouter le recul du côté des prises utilisées.

- [E1 : Adafruit 898 : câble USB-A / micro-B analogue][source-batterie-usb-E1]
  Câble analogue Ø 4,1 mm ; longueur distincte de la référence V5.

### Câbles USB-A vers micro-USB, 30 cm

[Fiche][fiche-cables-usb]
[Données][dims-cables-usb]
[PDF][pdf-cables-usb]

- **Diamètre câble** : 3,5 mm.
  Axes : D. Plages : 2.5-4.5 mm.
  analogie + photo ; confiance faible. E1 fournit Ø 4,1 mm ; les câbles V5 paraissent plus fins.
Fourchette élargie pour gaine et variante.

- **Embout USB-A** : 30 × 15 × 7 mm.
  Axes : L / l / h. Plages : 25-40 / 13-17 / 5.5-9 mm.
  rapport photo ; confiance faible. Vue-01 : surmoulage et métal comparés aux proportions
usuelles de l’USB-A. Longueur inclut le départ de protection, pas le rayon de courbure du câble.

- **Embout micro-USB** : 25 × 10 × 5 mm.
  Axes : L / l / h. Plages : 20-35 / 8-12 / 4-7 mm.
  analogie + photo ; confiance faible. Métal Micro-B 6,85 mm de E2 utilisé comme repère de
famille ; surmoulage et protection estimés sur la photo V5.

Ces enveloppes ne prouvent ni section cuivre ni tenue à 3 A. Prévoir en plus le rayon de
courbure du câble.

- [E1 : Adafruit 898 : câble USB-A / micro-B analogue][source-cables-usb-E1]
  Câble analogue Ø 4,1 mm ; longueur distincte de la référence V5.

- [E2 : Hirose ZX : géométrie micro-USB][source-cables-usb-E2]
  Plug Micro-B : largeur métallique 6,85 mm et hauteur 1,8 mm ; exemple assemblé longueur 22,6
mm, pas le surmoulage du lot V5.

### Fil souple Gebildet 22 AWG

[Fiche][fiche-fil-22awg]
[Données][dims-fil-22awg]
[PDF][pdf-fil-22awg]

Dimensions utiles déjà documentées ; pas d’estimation supplémentaire.

Dimensions utiles déjà documentées ; aucune estimation supplémentaire nécessaire.

### Porte-fusibles et fusibles 5 × 20 mm

[Fiche][fiche-fusibles]
[Données][dims-fusibles]
[PDF][pdf-fusibles]

- **Corps du porte-fusible** : 12 mm.
  Axes : D. Plages : 10-15 mm.
  rapport photo ; confiance faible. Vue-07 : rapport épaisseur/longueur du corps proche de 1/4,
longueur cotée 47 mm. Forme et angle justifient une plage large.

- **Fil isolé 16 AWG** : 3 mm.
  Axes : D. Plages : 2.5-4 mm.
  photo + analogie de fil ; confiance faible. 16 AWG annoncé ne définit que le conducteur.
L’enveloppe de la gaine est une hypothèse visible sur vue-07, sans spécification de l’isolant.

Les longueurs 260 mm illustrée et environ 270 mm textuelle restent contradictoires ; ni l’une ni
l’autre n’est une mesure.

### Condensateurs céramiques 100 nF

[Fiche][fiche-ceramique-100nf]
[Données][dims-ceramique-100nf]
[PDF][pdf-ceramique-100nf]

- **Corps enrobé** : 5 × 4 × 3 mm.
  Axes : L / h / e. Plages : 4-7 / 3-6 / 2-4 mm.
  analogie + photo ; confiance faible. Photo V5 compatible avec petites céramiques monolithiques
jaunes. E1 fournit un 100 nF / 50 V radial ; élargissement pour enrobage et série inconnue.

- **Pattes** : 2,5 × 0,5 × 20 mm.
  Axes : entraxe / D / longueur. Plages : 2.5-5 / 0.4-0.7 / 10-30 mm.
  analogie + photo ; confiance faible. Entraxe d’analogue 2,5 mm ; une variante 5 mm reste
possible. Diamètre et longueur des pattes inférés visuellement, sans échelle absolue dans la
photo V5.

Les propriétés électriques et le diélectrique Murata ne sont pas attribués au lot XINGZHI TECH.

- [E1 : Murata RDE : céramique radiale analogue][source-ceramique-100nf-E1]
  RDER71H104K0P1H03B : 100 nF / 50 V, corps 5 × 3,5 × 2,5 mm, entraxe 2,5 mm ; autre fabricant
et tolérance.

### Assortiment de condensateurs électrolytiques

[Fiche][fiche-electrolytiques]
[Données][dims-electrolytiques]
[PDF][pdf-electrolytiques]

- **Pattes du 470 µF** : 3,5 × 0,6 × 20 mm.
  Axes : entraxe / D / longueur libre. Plages : 3-4 / 0.5-0.7 / 5-30 mm.
  analogie + photo ; confiance moyenne. Corps Ø 8 mm annoncé. Famille Panasonic radiale pour
entraxe et fil ; longueur de pattes varie selon fourniture et coupe, photos du lot non cotées.

Les corps des quinze valeurs restent ceux du tableau vendeur. Les pattes des autres tailles ne
sont pas supposées identiques.

- [E1 : Panasonic SU : dimensions de radiaux analogues][source-electrolytiques-E1]
  Géométrie de famille radiale : corps Ø 8 mm, entraxe typique 3,5 mm ; fils et série distincts
du lot TYS OE.

### Résistances ALLECIN 1/4 W, 1 %

[Fiche][fiche-resistances]
[Données][dims-resistances]
[PDF][pdf-resistances]

- **Diamètres** : 2,4 × 0,55 mm.
  Axes : corps / fil. Plages : 2-3 / 0.45-0.65 mm.
  analogie ; confiance moyenne. Longueur 6 mm dans le visuel V5 proche de la MFR-25 Yageo 6,3
mm. Diamètres élargis pour marque inconnue.

Les fils 27 mm par côté restent annoncés. La puissance et les matériaux de l’analogue ne
certifient pas le lot ALLECIN.

- [E1 : Yageo MFR-25 : résistance 1/4 W analogue][source-resistances-E1]
  MFR-25 : corps 6,3 ± 0,5 mm, Ø 2,4 ± 0,2 mm ; fil Ø 0,55 ± 0,05 mm. Ce n’est pas une référence
ALLECIN identifiée.

### Gaine thermorétractable Treki

[Fiche][fiche-gaine]
[Données][dims-gaine]
[PDF][pdf-gaine]

- **Paroi avant / après** : 0,2 × 0,4 mm.
  Axes : avant / apres. Plages : 0.15-0.35 / 0.3-0.7 mm.
  photo + conservation matière ; confiance faible. Paroi fine visible en photo ; après retrait
2:1, ordre de grandeur doublé si longueur peu modifiée. Hypothèse d’enveloppe, pas une
spécification commune à tous les diamètres du lot.

Les diamètres 2-13 mm et longueurs 40/80 mm restent des données vendeur.

### Colliers nylon DONAU TECH

[Fiche][fiche-colliers]
[Données][dims-colliers]
[PDF][pdf-colliers]

- **Ruban et tête** : 1 × 5 × 4 × 3 mm.
  Axes : epaisseur / tete L / tete l / tete h. Plages : 0.8-1.3 / 4-7 / 3.5-5.5 / 2.5-4.5 mm.
  rapport photo ; confiance faible. Vue-02 rapportée à la largeur annoncée 2,5 mm : tête environ
deux largeurs de ruban, épaisseur proche de 1 mm ; perspective non corrigée.

Les 150 × 2,5 mm annoncés restent inchangés ; la tête dépasse la largeur du ruban.

### Ruban mousse double face

[Fiche][fiche-mousse]
[Données][dims-mousse]
[PDF][pdf-mousse]

- **Rouleau complet** : 165 × 35 × 12 mm.
  Axes : D externe / D mandrin / largeur. Plages : 150-190 / 25-50 / 12-14 mm.
  calcul + rapport photo ; confiance moyenne. Vue-01 : axes majeurs mandrin environ 200 px et
rouleau 960 px, soit r≈0,21. Avec L=10000 mm et e=2 mm : D=sqrt(4Le/[pi(1-r²)])≈163 mm. Élargir
pour compression et papier protecteur. Largeur 12 mm connue, 12-14 mm enveloppe avec protecteur.

Le rouleau complet ne sera pas embarqué : seuls des morceaux coupés sont prévus.
Formule fondée sur un enroulement uniforme ; pas de mesure physique.

### Adaptateurs UGREEN USB-C vers USB-A

[Fiche][fiche-adaptateur-usb]
[Données][dims-adaptateur-usb]
[PDF][pdf-adaptateur-usb]

- **Enveloppe totale** : 25 × 14 × 7 mm.
  Axes : L / l / h. Plages : 22-28 / 12-16 / 6-8 mm.
  analogie fabricant ; confiance moyenne. E1 fournit l’enveloppe d’un produit compact UGREEN
comparable. Les 0,47 × 0,44 × 0,22 pouce du visuel V5 ne sont pas considérés comme l’enveloppe
totale certifiée.

SKU analogue, pas équivalence commerciale confirmée. L’adaptateur sert au Mac, pas au Pi.

- [E1 : UGREEN 40702P : adaptateur compact analogue][source-adaptateur-usb-E1]
  Adaptateur compact même marque et fonction : 25 × 14 × 7 mm. SKU 40702P ; correspondance avec
ASIN V5 non établie.

### Fil de soudure sans plomb, 0,6 mm

[Fiche][fiche-fil-a-souder]
[Données][dims-fil-a-souder]
[PDF][pdf-fil-a-souder]

- **Bobine plastique** : 60 × 15 mm.
  Axes : D / largeur. Plages : 40-85 / 10-20 mm.
  photo + borne colis ; confiance faible. Photo montrant une petite bobine 20 g. Colis annoncé
110 × 93 × 20 mm : il fournit seulement une borne de conditionnement, pas la cote produit.
Nominal 60 mm hypothèse centrale, plage très large faute d’échelle fiable.

Bobine d’atelier, non embarquée. La longueur du fil ne peut pas être déduite sûrement des 20 g
annoncés comme poids brut.

### Lecteur microSD AXFEE USB-C

[Fiche][fiche-lecteur-microsd]
[Données][dims-lecteur-microsd]
[PDF][pdf-lecteur-microsd]

- **Adaptateur USB-A / USB-C** : 27 × 16 × 8 mm.
  Axes : L / l / h. Plages : 22-35 / 13-20 / 6-11 mm.
  rapport photo ; confiance faible. Vue-01 : adaptateur à droite comparé au lecteur 23,4 × 16,2
× 10,3 mm. Les pièces peuvent être à des échelles différentes, d’où une large plage. Métal USB-A
inclus.

- **Lien de retenue** : 40 × 1 mm.
  Axes : longueur libre / D. Plages : 20-70 / 0.5-2 mm.
  rapport photo ; confiance faible. Petite liaison rouge de la vue-01 comparée au lecteur de
23,4 mm ; longueur visible, pas longueur déployée certifiée.

Accessoire de préparation microSD, non embarqué. Les dimensions du lecteur restent celles de
l’infographie vendeur.

## Provenance et suivi

Chaque dimensions.json conserve les photos utilisées avec leurs empreintes et les URL
des références comparables. Le registre général se trouve dans
[Sources/estimations-dimensions.json](../Sources/estimations-dimensions.json).
Le générateur des PDF utilise ces données, sans remplir les mesures du prototype.
Voir les [relevés réels](releves.md) et les [PDF](../Composants/fiches-pdf.md).

[fiche-raspberry-pi-zero-2-w]: ../Composants/raspberry-pi-zero-2-w/README.md
[dims-raspberry-pi-zero-2-w]: ../Composants/raspberry-pi-zero-2-w/dimensions.json
[pdf-raspberry-pi-zero-2-w]: ../Composants/raspberry-pi-zero-2-w/raspberry-pi-zero-2-w.pdf
[source-raspberry-pi-zero-2-w-E1]: https://www.raspberrypi.com/news/raspberry-pi-zero/
[fiche-camera-module-3-standard]: ../Composants/camera-module-3-standard/README.md
[dims-camera-module-3-standard]: ../Composants/camera-module-3-standard/dimensions.json
[pdf-camera-module-3-standard]: ../Composants/camera-module-3-standard/camera-module-3-standard.pdf
[fiche-microsd-16go]: ../Composants/microsd-16go/README.md
[dims-microsd-16go]: ../Composants/microsd-16go/dimensions.json
[pdf-microsd-16go]: ../Composants/microsd-16go/microsd-16go.pdf
[fiche-nappe-csi-pi-zero]: ../Composants/nappe-csi-pi-zero/README.md
[dims-nappe-csi-pi-zero]: ../Composants/nappe-csi-pi-zero/dimensions.json
[pdf-nappe-csi-pi-zero]: ../Composants/nappe-csi-pi-zero/nappe-csi-pi-zero.pdf
[source-nappe-csi-pi-zero-E1]: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/173/17331/173310406_sd.pdf
[fiche-chassis-2wd]: ../Composants/chassis-2wd/README.md
[dims-chassis-2wd]: ../Composants/chassis-2wd/dimensions.json
[pdf-chassis-2wd]: ../Composants/chassis-2wd/chassis-2wd.pdf
[source-chassis-2wd-E1]: https://www.sunrobotics.in/products/robot-chassis-2wd-cars-diy-kit
[source-chassis-2wd-E2]: https://www.adafruit.com/product/3777
[source-chassis-2wd-E3]: https://www.adafruit.com/product/3784
[fiche-drv8833]: ../Composants/drv8833/README.md
[dims-drv8833]: ../Composants/drv8833/dimensions.json
[pdf-drv8833]: ../Composants/drv8833/drv8833.pdf
[fiche-batterie-usb]: ../Composants/batterie-usb/README.md
[dims-batterie-usb]: ../Composants/batterie-usb/dimensions.json
[pdf-batterie-usb]: ../Composants/batterie-usb/batterie-usb.pdf
[source-batterie-usb-E1]: https://www.adafruit.com/product/898
[fiche-cables-usb]: ../Composants/cables-usb/README.md
[dims-cables-usb]: ../Composants/cables-usb/dimensions.json
[pdf-cables-usb]: ../Composants/cables-usb/cables-usb.pdf
[source-cables-usb-E1]: https://www.adafruit.com/product/898
[source-cables-usb-E2]: https://www.hirose.com/ko/product/document?clcode=&documentid=D31704_en&documenttype=Catalog&lang=ko&productname=&series=ZX
[fiche-fil-22awg]: ../Composants/fil-22awg/README.md
[dims-fil-22awg]: ../Composants/fil-22awg/dimensions.json
[pdf-fil-22awg]: ../Composants/fil-22awg/fil-22awg.pdf
[fiche-fusibles]: ../Composants/fusibles/README.md
[dims-fusibles]: ../Composants/fusibles/dimensions.json
[pdf-fusibles]: ../Composants/fusibles/fusibles.pdf
[fiche-ceramique-100nf]: ../Composants/ceramique-100nf/README.md
[dims-ceramique-100nf]: ../Composants/ceramique-100nf/dimensions.json
[pdf-ceramique-100nf]: ../Composants/ceramique-100nf/ceramique-100nf.pdf
[source-ceramique-100nf-E1]: https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/RDE_X7R_X7S_25V-100V_E.pdf
[fiche-electrolytiques]: ../Composants/electrolytiques/README.md
[dims-electrolytiques]: ../Composants/electrolytiques/dimensions.json
[pdf-electrolytiques]: ../Composants/electrolytiques/electrolytiques.pdf
[source-electrolytiques-E1]: https://api.pim.na.industrial.panasonic.com/file_stream/main/fileversion/250108
[fiche-resistances]: ../Composants/resistances/README.md
[dims-resistances]: ../Composants/resistances/dimensions.json
[pdf-resistances]: ../Composants/resistances/resistances.pdf
[source-resistances-E1]: https://yageogroup.com/content/datasheet/asset/file/YAGEO-MFR_DATASHEET
[fiche-gaine]: ../Composants/gaine/README.md
[dims-gaine]: ../Composants/gaine/dimensions.json
[pdf-gaine]: ../Composants/gaine/gaine.pdf
[fiche-colliers]: ../Composants/colliers/README.md
[dims-colliers]: ../Composants/colliers/dimensions.json
[pdf-colliers]: ../Composants/colliers/colliers.pdf
[fiche-mousse]: ../Composants/mousse/README.md
[dims-mousse]: ../Composants/mousse/dimensions.json
[pdf-mousse]: ../Composants/mousse/mousse.pdf
[fiche-adaptateur-usb]: ../Composants/adaptateur-usb/README.md
[dims-adaptateur-usb]: ../Composants/adaptateur-usb/dimensions.json
[pdf-adaptateur-usb]: ../Composants/adaptateur-usb/adaptateur-usb.pdf
[source-adaptateur-usb-E1]: https://www.ugreen.com/en-au/products/au-40702p
[fiche-fil-a-souder]: ../Composants/fil-a-souder/README.md
[dims-fil-a-souder]: ../Composants/fil-a-souder/dimensions.json
[pdf-fil-a-souder]: ../Composants/fil-a-souder/fil-a-souder.pdf
[fiche-lecteur-microsd]: ../Composants/lecteur-microsd/README.md
[dims-lecteur-microsd]: ../Composants/lecteur-microsd/dimensions.json
[pdf-lecteur-microsd]: ../Composants/lecteur-microsd/lecteur-microsd.pdf
