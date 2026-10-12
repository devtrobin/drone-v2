# Prévision de roulage — Drone V2


Calcul du **11 octobre 2026**, sur l’implantation STEP provisoire et des hypothèses documentées.
**Roulage et rotation paraissent possibles sur sol lisse.**
Le démarrage électrique reste à valider.
Aucun essai physique ne permet encore d’affirmer que le robot roule ou tourne correctement.
Les moteurs DollaTek n’ont pas de couple, vitesse ni courant de blocage vérifiés.
L’[analogue Adafruit TT][tt] sert uniquement de scénario de dimensionnement.

Les [données](hypotheses-performance.json), le [résultat JSON][resultat]
et le [script](../tools/performance_drone.py) rendent le calcul reproductible.
Les relevés réels restent séparés dans [releves.json](releves.json), toujours non renseignés.

## Résultats sous les hypothèses centrales

| Grandeur | Prévision |
| --- | --- |
| Masse embarquée | 453 g ; sensibilité étudiée de 380 à 650 g |
| Force nécessaire sur plat | 0,222 N |
| Force de travail retenue | 0,925 N ; marge ×4,16 sur plat |
| Vitesse au PWM 100 % | 0,606 m/s = 2,18 km/h |
| Vitesse avec limite actuelle de 35 % | Environ 0,187 m/s = 0,67 km/h, extrapolation |
| Autonomie de roulage avec vidéo | 4 h 53 min à 5,8 W supposés |
| Plage énergétique explorée | 2 h 22 min à 6 h 20 min, pour 5 à 10 W et pertes variables |
| Rotation sur place | Possible dans le scénario d’appui libre ; marge de moment ×4,20 |
| Enveloppe balayée en pivot | Diamètre environ 36 cm, d’après les bornes CAO |
| Démarrage simultané à pleine commande | Environ 3,06 à 3,22 A, contre 3 A annoncés |

La vitesse maximale physique est inconnue : 2,18 km/h est une estimation avec un moteur analogue.
La configuration logicielle reste volontairement à 35 % ; aucune limite n’a été relevée.
Une PWM de 35 % ne garantit pas le démarrage : frottements, chute de tension et PWM 100 Hz à tester.

## Masse et appuis

| Ensemble embarqué | Masse supposée | Origine |
| --- | ---: | --- |
| Batterie | 165 g | Annonce VEGER, à peser |
| Plaque du kit | 80 g | Estimation pour plaque évidée de 200 × 140 × 3 mm |
| Deux moteurs | 61,2 g | 30,6 g chacun sur l’analogue TT |
| Deux roues | 60 g | Estimation |
| Appui passif et rehausse | 20 g | Estimation |
| Pi avec microSD | 10 g | Estimation |
| Caméra et DRV8833 | 7 g | Estimation |
| Faisceau, nappe, fusibles, mousse et gaine | 30 g | Estimation des portions utilisées |
| Supports, brides, visserie et attaches | 20 g | Estimation des pièces utilisées |
| **Total embarqué** | **453,2 g** | **Pas une pesée ni une masse déduite des volumes STEP** |

Les lots de vis, les chutes ABS, le lecteur et les autres fournitures restent hors du robot.
La plage de 380 à 650 g est une sensibilité de travail, pas un intervalle statistique garanti.
Les positions viennent de la maquette : appuis aux points (55, ±80) et (153, 0) mm.
La voie des roues est de 160 mm, leur rayon de 32,5 mm.

Centre de masse pondéré : **(81,04 ; −0,43 ; 46,27) mm**.
Réactions statiques : gauche 1,620 N, droite 1,644 N, appui avant 1,181 N.
Les roues motrices portent environ 73,4 % du poids ; les trois réactions sont positives.
Le centre est à 26,0 mm au minimum du bord du triangle d’appui.
Le seuil idéal de basculement est environ 5,52 m/s², hors chocs et flexion.
Une courbe à 0,20 m/s et rayon 0,20 m donne v²/R = 0,20 m/s², bien inférieur dans ce scénario.
Les pentes et le déplacement réel de l’appui peuvent modifier les réactions.

## Force motrice et couple nécessaire

Sur un sol supposé lisse : coefficient de roulement Crr = 0,05 et adhérence μ = 0,5.
Ces valeurs sont des hypothèses ; elles ne sont pas mesurées pour les pneus du kit.
Le modèle de moteur analogue à 4,6 V donne un couple de blocage de 0,0601 N·m.
Cette tension suppose 0,4 V de pertes dans la distribution et le pont moteur.
On retient **25 % du couple de blocage** comme marge de dimensionnement,
soit 0,0150 N·m par moteur ; ce n’est pas un couple continu certifié.

Formules, avec m en kg, r en m, angle θ et accélération a :

```text
Fnécessaire = m × g × (Crr × cos θ + sin θ) + m × a
Couple nécessaire par moteur = Fnécessaire × r / 2
Ftravail moteurs = 2 × Couple de travail / r
Fadhérence = μ × Réaction totale roues motrices × cos θ
Futilisable = minimum(Ftravail moteurs, Fadhérence)
```

| Situation | Force nécessaire | Couple par moteur | Marge de force |
| --- | ---: | ---: | ---: |
| Plat, vitesse constante | 0,222 N | 0,00361 N·m | ×4,16 |
| Plat, accélération 0,30 m/s² | 0,358 N | 0,00582 N·m | ×2,58 |
| Pente 5°, vitesse constante | 0,609 N | 0,00990 N·m | ×1,52 |
| Pente 10°, vitesse constante | 0,991 N | 0,01610 N·m | ×0,93, marge insuffisante |

Sur plat, l’adhérence centrale limiterait à 1,632 N ; le couple de travail limite à 0,925 N.
La répartition de charge est gardée approximativement constante pour les petites pentes.
Ce calcul ne valide ni le franchissement de seuils ni un tapis ; l’appui estimé Ø14 mm
sera particulièrement sensible aux irrégularités.

En scénario défavorable (650 g, Crr = 0,10, moteur moitié moins coupleux),
l’effort de 0,638 N dépasse les 0,463 N retenus : **le roulage n’est plus assuré par le modèle**.
À Crr = 0,15, la marge tombe à ×0,48. La masse, le sol et les moteurs reçus sont déterminants.

## Vitesse

L’analogue est mesuré à vide à 185 tr/min sous 4,5 V et 250 tr/min sous 6 V.
Une interpolation donne 189,3 tr/min à 4,6 V ; la vitesse nominale du kit reste inconnue.
Le modèle linéaire de moteur à courant continu donne :

```text
Fraction de charge = Fnécessaire × r / (2 × Couple de blocage)
n = nà_vide × max(0, PWM − Fraction de charge)
v = 2 × π × r × n / 60
```

Sur plat, charge centrale : 178,0 tr/min et 0,606 m/s à 100 %.
À 35 % : 54,9 tr/min et 0,187 m/s, par extrapolation moyenne de la PWM.
Ce modèle ignore notamment le seuil de démarrage, les ondulations du courant et les jeux.
La sensibilité à une tension moteur de 4 à 5 V figure dans le résultat JSON.
Ni la vitesse à vide ni le couple de blocage ne sont une vitesse ou un couple de service garantis.

## Tourner et pivoter

La [cinématique différentielle][cinematique] donne, pour voie b = 0,160 m :

```text
vcentre_essieu = (vdroite + vgauche) / 2
ω = (vdroite − vgauche) / b
Rayon du milieu d’essieu = vcentre_essieu / ω
```

Roues opposées : rayon nul au **milieu de l’essieu**, pas au centre géométrique du robot.
Une roue arrêtée : rayon 80 mm pour ce même point ; la caméra décrit un cercle plus grand.
Dans le scénario central à 35 %, le modèle chargé en rotation donne environ 134°/s
et environ 2,7 s pour un tour complet ; valeurs idéales, pas une précision de commande.
Les moteurs sans capteurs n’assurent ni maintien de vitesse égale ni angle exact.

Le calcul de moment tient compte du frottement équivalent de l’appui et du roulement des pneus :

```text
Mrésistant = μappui × Réaction appui × Distance appui–essieu
             + Crr × Réaction roues × b / 2
Mnécessaire = Mrésistant + Inertie en lacet × Accélération angulaire
Mdisponible = minimum(2 × Couple travail / r, 2 × μ × Réaction roue moins chargée) × b / 2
```

Inertie approchée : 0,00216 kg·m² ; accélération angulaire choisie : 0,5 rad/s².

| État hypothétique de l’appui | Moment nécessaire | Moment disponible | Marge |
| --- | ---: | ---: | ---: |
| Libre et aligné, coefficient 0,03 | 0,0176 N·m | 0,0740 N·m | ×4,20 |
| Mal orienté, coefficient 0,30 | 0,0489 N·m | 0,0740 N·m | ×1,51 |
| Bloqué, coefficient 0,50 | 0,0720 N·m | 0,0740 N·m | ×1,03, presque aucune réserve |

Ces coefficients sont des scénarios, pas une caractérisation de la roulette.
L’appui doit rouler et s’orienter librement ; identifier roulette pivotante ou bille à réception.
Avec un moteur moitié moins coupleux, la marge du cas mal orienté devient inférieure à 1.
Les roues ne doivent pas frotter sur la plaque ; contrôler également nappe et faisceau.

## Autonomie et alimentation

La batterie annonce 10 000 mAh. Hypothèse : capacité des cellules à 3,7 V :
**10 Ah × 3,7 V = 37 Wh**, et non 50 Wh à la sortie USB.
Avec rendement USB de 85 % et fraction utilisable de 90 %, énergie disponible : **28,305 Wh**.
Équivalent à 5 V : environ 5,66 Ah. L’étiquette Wh et les Wh USB doivent être vérifiés.

```text
Autonomie (heures) = Énergie cellules × Rendement × Fraction utilisable / Puissance moyenne
```

| Scénario de puissance supposée au 5 V | Puissance | Autonomie estimée |
| --- | ---: | ---: |
| Vidéo, robot stationnaire | 4 W | 7 h 05 min |
| Roulage normal avec vidéo | 5,8 W | 4 h 53 min |
| Roulage plus chargé | 9 W | 3 h 09 min |

Le scénario 5,8 W suppose Pi/caméra/Wi-Fi 3 W, deux moteurs 2,5 W et pertes aval 0,3 W.
Ce budget de puissance est indépendant d’une mesure, à remplacer par des courants réels.
Avec 5 à 10 W, rendement 75 à 90 % et fraction disponible 85 à 95 %, plage 2,36 à 6,33 h.
Une batterie vide, vieillie, une capacité surestimée ou une sortie coupée change ces résultats.
L’objectif 15 minutes paraît confortable en énergie, **si l’alimentation tient les pointes**.

L’analogue bloqué demande environ 1,22 A par moteur à 4,6 V :
2 × 1,22 + 0,60 pour Pi/caméra + 0,02 pour pilote = **3,06 A**.
À 5 V, interpolation : environ 3,22 A au total, contre **3 A annoncés** pour la batterie.
Les démarrages simultanés et roues bloquées peuvent donc couper la sortie ou redémarrer le Pi.
La vraie limite du port USB-A et les courants des moteurs peuvent être différents.

Le [DRV8833 TI][ti] est donné à 0,5 A RMS par pont en PW ou 1,5 A en PWP/RTY,
avec limites thermiques ; le boîtier et le refroidissement du module reçu restent à identifier.
Une pointe de 2 A autorisée par la puce ne garantit pas la carte ni la batterie.
Ne pas choisir un calibre de fusible ou retirer un découplage à partir de ces seuls calculs.

## Essais qui permettront de conclure

1. Peser le robot et identifier les moteurs, l’appui et le boîtier DRV8833.
2. Mesurer régime à vide, courant de roulage et pointe de démarrage avec alimentation limitée.
3. Contrôler tension au Pi et au pilote pendant démarrage, freinage et inversion.
4. Mesurer l’effort de traction lente sur le sol visé ; comparer au modèle de résistance.
5. À faible commande, tester avance, recul, une roue arrêtée puis roues opposées.
6. Mesurer vitesse sur 1 m, angle sur plusieurs pivots et température après 15 minutes.
7. Faire un essai d’autonomie vidéo + roulage, puis mesurer Wh USB et arrêts intempestifs.

Les [achats](../listeAchat.md) incluent maintenant la matière et la visserie pour les supports.
Les entretoises 5 mm et l’ABS 3 mm achetés diffèrent du STEP initial : ajuster après réception.
Ce calcul concerne l’encombrement initial, pas une validation des fixations après adaptation.

[tt]: https://www.adafruit.com/product/3777
[ti]: https://www.ti.com/lit/ds/symlink/drv8833.pdf
[cinematique]: https://modernrobotics.northwestern.edu/nu-gm-book-resource/13-3-1-modeling-of-nonholonomic-wheeled-mobile-robots/
[resultat]: ../Validation/resultats/performance.json
