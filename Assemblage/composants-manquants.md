# Pièces complémentaires révélées par l’assemblage


Implantation provisoire du **11 octobre 2026**, sans matériel reçu ni mesure physique.
Les supports violets, la visserie et les longues sangles de la maquette sont des ajouts proposés.
Ils ne sont pas déjà achetés et ne sont pas automatiquement inclus dans la référence V5.
Le [registre CAO initial](composants-manquants.json) conserve quantités et hypothèses géométriques.
Le [panier actif](../achats.json) contient maintenant les prix et solutions d’approvisionnement.

## À prévoir pour cette implantation

| ID | Élément | Quantité | Fonction |
| --- | --- | --- | --- |
| M01 | Équerre de caméra isolante | 1 | Tenir la caméra face avant |
| M02 | Entretoises caméra, passage M2, longueur 6 mm | 2 | Dégager l’arrière du module |
| M03 | Vis M2 vers 12 mm et écrous | 2 jeux | Fixer les deux trous inférieurs |
| M04 | Entretoises Pi, passage M2,5, hauteur 6 mm | 4 | Dégager carte et soudures |
| M05 | Vis M2,5 vers 12 mm et écrous | 4 jeux | Fixer le Pi sur ses quatre trous |
| M06 | Porte-module DRV8833 isolant | 1 | Maintenir une carte sans trous mécaniques |
| M07 | Vis M3 et écrous, longueurs à ajuster | 4 jeux | Porte-module et pied caméra |
| M08 | Sangles réutilisables de 250 mm ou plus | 2 | Retenir la batterie amovible |
| M09 | Clips porte-fusible compatibles Ø12 estimé | 2 | Immobiliser les deux porte-fusibles |

M01 : gabarit d’équerre, pied 14 × 36 × 2 mm et montant 28 × 40 × 2 mm.
Une ouverture centrale dégage l’arrière optique ; fixation par les deux trous du bas.
M06 : gabarit de plateau 26 × 24 × 3 mm, avec mousse et fixation de la carte à confirmer.
Les pièces personnalisées montrées ne sont pas des plans validés pour impression ou découpe.
Le maintien du DRV8833 doit laisser libres bornes, puce et condensateur.

Les dimensions du Pi et les trous de la caméra suivent leurs documents sources.
M2 / M2,5 indiquent les tailles proposées ; vérifier la visserie et les dégagements au montage.
Les vis sont représentées sans filet ; les écrous sont des enveloppes cylindriques.
Les longueurs données ne constituent pas une commande de visserie définitive.

### Pourquoi les colliers actuels ne suffisent pas pour la batterie

La batterie est annoncée 68 mm de large et 15 mm d’épaisseur.
Son périmètre rectangulaire est déjà 2 × (68 + 15) = **166 mm**, avant le châssis et le serrage.
Un collier de **150 mm** ne peut donc pas entourer cette section.
Dans la maquette, le passage sous la plaque demande environ 181 mm de boucle.
Une longueur de 250 mm laisse de la marge pour fermeture et réglage.
Quatre passages de sangle de 10,5 × 1,5 mm sont proposés dans la plaque.
Leur présence réelle ou leur réalisation reste à confirmer ; la maquette les montre évidés.
Les colliers de la liste V5 restent utiles pour le faisceau.
Le [RF250 fabricant][sangle] confirme l’existence de colliers réutilisables de 250 mm ;
c’est un exemple de format, pas une référence Amazon retenue ni une garantie de fixation.

## Contenu du kit à confirmer avant de racheter

| Élément | Hypothèse dans la maquette | Action |
| --- | --- | --- |
| Supports et visserie des deux moteurs | Deux brides reconstruites | Vérifier le kit reçu |
| Appui passif, axe et visserie | Roulette du modèle composant | Vérifier le contenu et la hauteur |
| Rehausse de l’appui | Deux entretoises de 18 mm | Mesurer, ajuster seulement si nécessaire |
| Fixations des porte-fusibles | Deux clips proposés | Choisir maintien adapté au corps reçu |

Les entretoises de 18 mm permettent aux trois roues de toucher le plan du sol dans la maquette.
Cette valeur vient du modèle estimé du kit ; elle ne prouve pas qu’il faut les acheter.
Ne pas doubler les supports moteurs ou la visserie fournie sans contrôler le contenu réel.

## Déjà présents dans V5, mais à préparer ou dimensionner

- Deux porte-fusibles et deux cartouches du lot ; **calibres à déterminer par mesure**.
- Deux câbles du lot de cinq, recoupés pour conserver USB-A et micro-USB.
- Fil 22 AWG, gaine, mousse et petits colliers pour le faisceau ; sections à vérifier.
- Une nappe de 160 mm ; longueur et rayons de courbure à confirmer sur le montage réel.
- Condensateurs et résistances : trois lots conditionnels, montrés en atelier et non montés.

Une distribution soudée et gainée est prévue : aucune carte de distribution supplémentaire imposée.
Les bornes DRV8833 représentées ne donnent pas un brochage électrique validé.
Voir le [schéma candidat](../Electronique/schema.md) et les [relevés](../Electronique/releves.md).

## Budget et approvisionnement

Les [achats](../listeAchat.md) ajoutent **51,66 €** de lots Amazon,
pour un total matériel prévisionnel de **257,03 € hors port**. Aucun achat effectué.
Le [relevé Amazon daté](../Sources/fixations-amazon.json) conserve annonces et variantes.

| Besoins | Solution dans le panier | Coût du lot entier |
| --- | --- | ---: |
| M01 et M06 | Plaques ABS à travailler pour supports caméra et pilote | 13,49 € |
| M02 et M04 | Kit nylon Gueenky, entretoises 5 mm | 20,49 € |
| M03, M05 et M07 | Kit FandWay, visserie M2 / M2,5 / M3 | 10,99 € |
| M08 | 50 colliers réutilisables Zenitech de 250 × 7,6 mm | 6,69 € |
| M09 | Colliers 150 mm et mousse déjà dans V5, maintien à préparer | 0 € de plus |

La matière des supports est chiffrée ; leur fabrication reste à faire et peut coûter en plus.
Pour M09, les clips rigides du STEP sont remplacés par une retenue par colliers proposée.
Les entretoises disponibles sont de 5 mm au lieu de 6 mm, l’ABS de 3 mm au lieu de 2 mm.
Les colliers de batterie font 7,6 mm de large au lieu du gabarit de 10 mm.
Adapter dégagements, vis et passages à réception : le STEP conserve ses cotes initiales.
Le registre CAO non chiffré est une archive d’hypothèses, pas le budget courant.
Voir aussi les [calculs de performance](../Mecanique/performance.md).

[sangle]: https://www.hellermanntyton.com/products/cable-ties-releasable/rf250/115-00054
