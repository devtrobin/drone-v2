# Résultats — Drone V2

Le [rapport logiciel](logiciel-hors-materiel.json) contient les commandes réellement exécutées,
leur sortie et leur code retour, ainsi que Python, système et version GPIO Zero.
Ces tests utilisent TCP local et des sorties simulées, sans caméra ni robot.
Le pipeline MPEG-TS est vérifié avec une courte vidéo synthétique si FFmpeg est installé.

Aucun résultat matériel V01 à V14 enregistré.
Pour un essai physique, copier le [modèle](../modele.md) et nommer le fichier par date et ID.
Ne pas remplacer une mesure absente par une sortie de simulation.

Le [rapport des PDF](fiches-pdf.json) recense les 19 fichiers, pages, photos, liens et empreintes.
Il consigne le contrôle visuel des pages rendues et la vérification des contenus attendus.
Cette validation porte sur les documents, pas sur les composants ni leur réception.

Le [rapport STEP](modeles-step.json) couvre les 19 fichiers CAO rangés avec les composants.
Il conserve les contrôles de réimportation, les empreintes et la revue visuelle des aperçus.
Les registres modele-3d.json distinguent les données documentées des hypothèses supplémentaires.
La géométrie valide et l’apparence du modèle ne valident pas une dimension physique du produit.

La [vérification d’assemblage](../../Assemblage/verification.json) couvre robot et atelier STEP,
sources, cinq vues et contrôles des interférences entre groupes et du champ optique estimé.
Ces vérifications CAO ne valident ni perçages réels, ni brochage, ni stabilité physique du robot.
# Calculs de performance

Le [résultat prévisionnel](performance.json) provient du script performance_drone.py.
Il utilise des hypothèses, sans robot mesuré ni essai physique.
Voir [le rapport et ses réserves](../../Mecanique/performance.md).
