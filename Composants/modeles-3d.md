# Modèles 3D des composants — STEP


Les 19 dossiers composants possèdent un STEP en millimètres, avec solides nommés et couleurs.
Chaque dossier contient aussi un aperçu modele-3d.png et un registre modele-3d.json.
Création : **11 octobre 2026**, depuis les cotes, plans, photos et estimations déjà collectés.

Ce sont des modèles d’implantation simplifiés créés pour le projet, pas des CAO natives vendeur.
Les dimensions publiées, les hypothèses supplémentaires et les sources sont séparées
dans chaque registre 3D. Les pièces n’ont pas été reçues ni mesurées.
Les détails internes, filetages, sérigraphies et caractéristiques électriques sont simplifiés.
Confirmer les dimensions et perçages sur le matériel avant de fabriquer un support.

## Fichiers et contenu

| Composant / STEP | Aperçu | Représentation |
| --- | --- | --- |
| [Pi Zero 2 W][step-1] | [Vue][vue-1] | Carte nue, connecteurs, GPIO non peuplé |
| [Camera Module 3][step-2] | [Vue][vue-2] | Version Standard, trous et optique |
| [microSD][step-3] | [Vue][vue-3] | Carte et adaptateur SD séparés |
| [Nappes CSI][step-4] | [Vue][vue-4] | 160 et 300 mm, déployées |
| [Châssis 2WD][step-5] | [Vue][vue-5] | Kit monté avec appui estimé |
| [DRV8833][step-6] | [Vue][vue-6] | Un module, sans barrettes |
| [Batterie USB][step-7] | [Vue][vue-7] | Boîtier et ports simplifiés |
| [Câble USB][step-8] | [Vue][vue-8] | Un câble droit de 300 mm |
| [Fil 22 AWG][step-9] | [Vue][vue-9] | Rouge et noir, échantillons 100 mm |
| [Fusibles][step-10] | [Vue][vue-10] | Porte-fusible et cartouche séparée |
| [100 nF][step-11] | [Vue][vue-11] | Un condensateur radial |
| [Électrolytiques][step-12] | [Vue][vue-12] | Les 15 valeurs, une pièce par valeur |
| [Résistances][step-13] | [Vue][vue-13] | 1 kΩ et 10 kΩ représentatives |
| [Gaines][step-14] | [Vue][vue-14] | Huit diamètres avant rétreint |
| [Collier][step-15] | [Vue][vue-15] | Un collier à plat |
| [Mousse][step-16] | [Vue][vue-16] | Rouleau et échantillon 50 mm |
| [Adaptateur USB][step-17] | [Vue][vue-17] | USB-C mâle vers USB-A femelle |
| [Fil à souder][step-18] | [Vue][vue-18] | Bobine et échantillon 50 mm |
| [Lecteur microSD][step-19] | [Vue][vue-19] | Lecteur et adaptateur du lot |

Les pièces côte à côte et les grilles servent à montrer les variantes du lot.
L’encombrement total de ces présentations n’est pas la dimension d’un composant individuel.
Les limites propres aux variantes, aux accessoires et aux longueurs sont dans les registres 3D.

## Sources et niveau de détail

Pi : [plan officiel][pi-plan] et product brief conservé dans le dossier.
Caméra : [plan Standard officiel][camera-plan] conservé dans le dossier.
Les coordonnées de fixation de la caméra et les entraxes du Pi suivent ces plans.
Les épaisseurs et connecteurs du Pi non cotés dans le document restent estimés.

Les autres composants suivent les dimensions vendeur et la [synthèse des estimations][estimations].
Les cotes ajoutées pour créer une forme 3D restent des hypothèses explicites.
La bobine et le rouleau sont des enveloppes : leur volume ne donne pas une masse de matière.
Le châssis conserve le boîtier AA du lot, inutilisé électriquement dans Drone V2.
Sa forme, les découpes, les positions des moteurs et les entretoises d’appui sont estimées.
Il ne constitue pas un plan de fabrication ou un assemblage final validé du robot.
La [maquette complète](../Assemblage/README.md) reprend les STEP dans une implantation provisoire.

## Utilisation et vérification

Ouvrir les STEP dans un logiciel CAO acceptant les assemblages STEP en mm.
Sélectionner la pièce nommée nécessaire lorsque le fichier contient plusieurs variantes.
Les noms et couleurs sont exportés ; leur affichage dépend du logiciel d’import.
La disposition des pièces est conservée, sans contraintes mécaniques ni simulation électrique.

Le [rapport CAO][rapport] enregistre la réimportation des 19 fichiers : B-rep valide,
solides de volume positif, conservation du nombre de solides, du volume et des bornes.
L’unité millimètre et les empreintes des fichiers sont contrôlées.
Les aperçus des 19 modèles ont également été examinés.
Ces contrôles portent sur les fichiers ; les mesures physiques restent à effectuer.

Le [générateur][generateur] recrée tous les STEP et aperçus à partir des fichiers locaux.
Voir les [instructions des outils][outils] pour les dépendances et la commande.

[step-1]: raspberry-pi-zero-2-w/raspberry-pi-zero-2-w.step
[vue-1]: raspberry-pi-zero-2-w/modele-3d.png
[step-2]: camera-module-3-standard/camera-module-3-standard.step
[vue-2]: camera-module-3-standard/modele-3d.png
[step-3]: microsd-16go/microsd-16go.step
[vue-3]: microsd-16go/modele-3d.png
[step-4]: nappe-csi-pi-zero/nappe-csi-pi-zero.step
[vue-4]: nappe-csi-pi-zero/modele-3d.png
[step-5]: chassis-2wd/chassis-2wd.step
[vue-5]: chassis-2wd/modele-3d.png
[step-6]: drv8833/drv8833.step
[vue-6]: drv8833/modele-3d.png
[step-7]: batterie-usb/batterie-usb.step
[vue-7]: batterie-usb/modele-3d.png
[step-8]: cables-usb/cables-usb.step
[vue-8]: cables-usb/modele-3d.png
[step-9]: fil-22awg/fil-22awg.step
[vue-9]: fil-22awg/modele-3d.png
[step-10]: fusibles/fusibles.step
[vue-10]: fusibles/modele-3d.png
[step-11]: ceramique-100nf/ceramique-100nf.step
[vue-11]: ceramique-100nf/modele-3d.png
[step-12]: electrolytiques/electrolytiques.step
[vue-12]: electrolytiques/modele-3d.png
[step-13]: resistances/resistances.step
[vue-13]: resistances/modele-3d.png
[step-14]: gaine/gaine.step
[vue-14]: gaine/modele-3d.png
[step-15]: colliers/colliers.step
[vue-15]: colliers/modele-3d.png
[step-16]: mousse/mousse.step
[vue-16]: mousse/modele-3d.png
[step-17]: adaptateur-usb/adaptateur-usb.step
[vue-17]: adaptateur-usb/modele-3d.png
[step-18]: fil-a-souder/fil-a-souder.step
[vue-18]: fil-a-souder/modele-3d.png
[step-19]: lecteur-microsd/lecteur-microsd.step
[vue-19]: lecteur-microsd/modele-3d.png
[pi-plan]: https://pip-assets.raspberrypi.com/categories/584-raspberry-pi-zero-2-w/documents/RP-008358-DS-1-raspberry-pi-zero-2-w-mechanical-drawing.pdf
[camera-plan]: https://datasheets.raspberrypi.com/camera/camera-module-3-standard-mechanical-drawing.pdf
[estimations]: ../Mecanique/estimations.md
[rapport]: ../Validation/resultats/modeles-step.json
[generateur]: ../tools/generate_component_step.py
[outils]: ../tools/README.md
