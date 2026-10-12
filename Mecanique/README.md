# Mécanique — Drone V2


Base : châssis DollaTek 2WD équipé, référence B07F73HY34.
La plaque du kit remplace le châssis PMMA découpé au laser de Drone V1.
Le [modèle STEP du kit](../Composants/chassis-2wd/chassis-2wd.step) est un assemblage estimé.
Les calculs sont préparés mais attendent les dimensions et masses réelles.

La [synthèse des estimations](estimations.md) donne des valeurs provisoires, plages et méthodes.
Les dossiers composants les conservent dans dimensions.json et dans leur PDF local.
Ces hypothèses servent à préparer l’implantation ; les relevés ci-dessous restent à effectuer.

| Donnée à relever | État |
| --- | --- |
| Dimensions et épaisseur de la plaque | À mesurer |
| Perçages, entraxes et dégagement sous plaque | À mesurer |
| Roulette, supports et visserie réellement fournis | À contrôler |
| Diamètre des roues et hauteur de l’appui passif | À mesurer |
| Position des axes et polarité de chaque moteur | À relever |
| Pi, caméra et module réels : encombrements et trous | À contrôler |
| Masse du robot et répartition des charges | À mesurer |

La batterie était annoncée 106 × 68 × 15 mm, 165 g dans V5 ; dimensions à confirmer à réception.
Installer la batterie bas et centrée, le Pi et le pilote avec accès aux prises,
et la caméra vers l’avant. Garder une courbure douce de la nappe, dégagée des roues.
Utiliser visserie du kit et du fablab après contrôle, puis colliers et tampons chiffrés.
La mousse ne remplace pas une fixation mécanique ; garder les soudures hors des vis métalliques.
Ne pas comprimer l’optique, la batterie, l’antenne ou les composants chauds.

Le boîtier 4 AA du kit reste inutilisé électriquement ; aucune pile ajoutée.
Définir l’appui et les fixations de la caméra après mesure, sans supposer un support déjà adapté.
Recalculer stabilité et dégagements après implantation ; les anciennes masses ne s’appliquent pas.
Voir l’[assemblage](../Assemblage/README.md) et les [fiches](../Composants/README.md).

Voir les [relevés et calculs](releves.md) et leur [fichier de données](releves.json).
Les [19 STEP des composants](../Composants/modeles-3d.md) sont prêts pour une implantation CAO.
La [maquette d’assemblage](../Assemblage/README.md) propose leur implantation avec supports estimés.
Confirmer le châssis et ses perçages avant de réaliser les supports et le montage définitifs.

Les [calculs de performance](performance.md) utilisent l’implantation et des masses estimées.
Le [jeu d’hypothèses](hypotheses-performance.json) est séparé des relevés physiques.
Les [achats](../listeAchat.md) chiffrent les fixations et la matière première des supports.
