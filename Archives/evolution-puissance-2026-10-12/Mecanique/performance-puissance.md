# Prévisions — moteurs 37D, roues 80 mm, LiPo 3S

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Calcul du 12 octobre 2026. **Objectif 6–8 km/h**, priorité vitesse. Aucune mesure réelle ; ce
rapport vérifie la plausibilité du choix, pas les performances d'un prototype construit. Voir les
[hypothèses][hyp], le [résultat JSON][res] et le [calcul reproductible][script].

## Données et hypothèses

CQRobot CQR37D12V-C 18,8:1 : 530 tr/min à vide sous 12 V, couple de blocage 8,5 kg·cm (0,834 N·m),
courant de blocage 5,5 A ; 265 tr/min sous 6 V selon fabricant. Le couple de blocage n'est pas un
couple de fonctionnement continu. Les 12 W de puissance maximale ne donnent pas la consommation
nominale du robot.

Roues de 80 mm, voie supposée 160 mm, essieu à x = 55 mm et appui à x = 153 mm. Masse estimée
**1,058 kg**, dont 500 g pour les deux ensembles moteur/équerre et 137 g pour le seul pack
embarqué. Le chargeur et le second pack ne sont pas embarqués. Centre de gravité calculé à x =
77,5 mm et z = 54,8 mm, sur des masses et positions hypothétiques, sans utiliser les volumes des
anciens STEP.

Roulement Crr = 0,05 ; adhérence µ = 0,5 ; chute pilote 0,25 V supposée ; Pi et vidéo 3 W,
rendement UBEC 85 %. Ces paramètres doivent être remplacés par des mesures.

## Vitesse

Modèle DC linéaire : Vm = tension pack × PWM − chute pilote ; n0 = 530 × Vm/12 ; couple moteur
requis = résistance × rayon / 2 ; n = n0 × (1 − couple requis/couple de blocage). Vitesse = n × π
× diamètre / 60. Le traitement PWM par tension moyenne est une approximation, particulièrement à
faible PWM.

| État du pack | PWM cible | Vitesse estimée sur sol lisse |
| --- | --- | --- |
| 12,6 V, plein | 95 % | 7,71 km/h |
| 11,1 V, nominal | 95 % | 6,76 km/h |
| 10,5 V, seuil total proposé | 95 % | 6,38 km/h |

L'objectif est plausible dans ces conditions. **8 km/h n'est pas garanti**, notamment sur sol
rugueux. Le profil livré limite l'avance à **25 %**, avec rampe de 0,30 par seconde : ce profil
d'essai n'atteint pas la vitesse cible. Monter progressivement dans un profil local après
validation thermique et mécanique ; viser au maximum 95 % sous pack 12,6 V afin de garder une
tension moyenne moteur inférieure à 12 V dans ce modèle.

## Force et montée

Froulement = Crr × m × g = **0,519 N**. Répartition statique supposée : 77,1 % du poids sur
l'essieu moteur. Adhérence motrice estimée **4,00 N**. En prenant 25 % du couple de blocage comme
hypothèse de travail, le couple disponible excède cette limite d'adhérence : le sol devient
limitant.

Marge de traction sur plat : environ **7,7 fois** la résistance au roulement. Effort estimé pour
une pente de 10 % : **1,55 N**, inférieur à la traction supposée. La vitesse en pente diminuera.
Ni le courant permanent, ni la pente admissible, ni la température du réducteur ne sont certifiés
par ces calculs. Un sol peu adhérent, une roulette mal alignée ou une marche peuvent invalider ce
résultat.

Accélération théorique limitée par traction : **3,29 m/s²**. C'est une borne mécanique, pas
l'accélération produite par la rampe PWM. Au blocage et à pleine tension : environ **5,78 A par
moteur**, **11,83 A à la source** avec Pi ; interrompre immédiatement, pas de test de blocage
prolongé.

## Autonomie et distance

Un pack : 11,1 V × 2,2 Ah = **24,42 Wh**. Énergie exploitable supposée : 80 %, soit **19,54 Wh**.
Cette fraction réserve de la marge pour tension de coupure, pertes et variation de capacité ; elle
n'est pas une capacité mesurée.

| Usage supposé | Puissance du robot | Durée | Distance à vitesse moyenne choisie |
| --- | --- | --- | --- |
| Sol lisse, peu de virages | 12 W | 98 min | 9,77 km à 6 km/h |
| Vidéo et manœuvres, central | 15 W | 78 min | 5,21 km à 4 km/h |
| Sol difficile, relances | 30 W | 39 min | 1,95 km à 3 km/h |

Le modèle idéal en ligne droite donne environ 9,7 W au nominal. Le scénario central de 15 W ajoute
une marge pour relances et virages. Ce sont trois hypothèses d'usage, pas des bornes garanties.
L'ancienne estimation proche de 5 h utilisait une batterie USB plus énergétique et une
motorisation lente ; elle ne se transpose pas à ce modèle.

Les distances sont des distances parcourues cumulées ; **pas une portée Wi-Fi**. La portée radio
et la vidéo doivent être mesurées sur le site d'utilisation. Le second pack de réserve permet une
autre session après échange, sans augmenter l'autonomie d'un pack.

## Virages et stabilité

Le logiciel réduit l'avance selon l'intensité de virage, et limite le terme de rotation à 8 % PWM.
Il réduit aussi ce terme quand le drone avance. Modèle différentiel idéal : v = (vg + vd)/2 et ω =
(vg − vd)/voie. Pivot à faible PWM : environ **19 tr/min** au nominal, mais le seuil de démarrage
réel peut empêcher un mouvement régulier à 8 %. Tester frottements de roulette et moteurs ;
ajuster seulement après mesures.

Avec 95 % d'avance et 8 % de rotation maximale, exploration du mixage idéal : accélération
latérale maximale environ **1,24 m/s²**. Ce n'est pas une limite physique garantie : inertie,
glissement, jeu, réponse PWM et retard des deux moteurs ne sont pas modélisés. À 8 km/h, garder
1,5 m/s² demanderait un rayon d'environ **3,3 m** ; un virage serré demande donc de ralentir.

Sur le triangle de support hypothétique, accélérations statiques de basculement : environ **4,02
m/s²** longitudinale et **8,55 m/s²** vers le bord oblique le plus proche. Une roue passant un
obstacle ou un appui qui accroche invalide ce modèle. Le freinage MD13S à PWM nul n'est pas limité
par la rampe : vérifier décélération et glissement avant essais rapides.

## Implantation à revoir

Proposition de travail : plaque 200 × 140 mm, dessous vers z = 62 mm et essieu à z = 40 mm. Corps
moteur Ø37 mm : sommet vers 58,5 mm, laissant quelques millimètres sous la plaque. Perçages et
équerres à confirmer. Appui passif à rehausser jusqu'au sol selon sa géométrie réelle ; l'ancienne
rehausse de 18 mm ne convient plus nécessairement.

Batterie centrée vers x = 92,5 mm ; Pi vers l'arrière ; pilotes vers x = 160 mm de part et d'autre
; circuit de coupure isolé des GPIO. Conserver place pour fusibles, fils et ventilation. Utiliser
la nappe CSI 30 cm déjà comprise dans le lot si la 16 cm ne suffit plus. Les dimensions du module
de coupure ne sont pas publiées : mesurer avant perçage.

Les roues TT et supports TT sont inutilisés. Les moyeux 6 mm restent conditionnés par leur cercle
de fixation ; les vis de roue viennent du lot FandWay. Les équerres moteur sont incluses ;
respecter la profondeur maximale de vissage de **3 mm** indiquée par CQRobot dans la face du
moteur.

La petite roulette et la plaque du kit n'ont pas de vitesse ni charge admissible documentées.
Examiner rigidité, jeu et tenue à la vitesse visée. Réaliser la nouvelle CAO après mesures ; les
STEP existants restent la maquette historique.

[hyp]: hypotheses-puissance.json
[res]: ../Validation/resultats/performance-puissance.json
[script]: ../tools/performance_puissance.py

[statut-archive]: ../README.md
