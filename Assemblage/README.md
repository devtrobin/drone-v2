# Assemblage — Drone V2


## Maquette 3D

Ouvrir [drone-v2.step](drone-v2.step) pour le robot assemblé, avec pièces nommées et couleurs.
Le [fichier atelier](atelier-v2.step) ajoute les accessoires et lots conditionnels non embarqués.
Les 19 références de composants sont ainsi représentées, sans porter les bobines et outils
sur le robot. Le boîtier AA et l’adaptateur SD sont également montrés à côté dans l’atelier.

- [Vue générale](vue-iso.png).
- [Vue de dessus](vue-dessus.png), [vue de face](vue-face.png) et [profil](vue-profil.png).
- [Vue atelier](vue-atelier.png).
- [Pièces complémentaires à prévoir](composants-manquants.md).
- [Implantation et cheminements](implantation.json), [vérification CAO](verification.json).

Les coordonnées sont en mm : x vers l’avant, y vers la gauche, z depuis le sol.
La caméra regarde vers +x. Batterie centrée, Pi sur entretoises et pilote sur un plateau isolant.
La nappe de 160 mm est représentée avec sa réserve de longueur, sous forme d’enveloppe pliée.
Son retour passe sur le côté de la caméra pour dégager l’objectif.
Le faisceau montre la distribution, deux fusibles, les commandes et les liaisons moteurs.
Les bornes du DRV8833 sont illustratives et restent à identifier sur la carte reçue.

Les supports violets, les longues sangles et la visserie sont des ajouts proposés.
La [liste structurée](composants-manquants.json) les distingue du contenu du kit à confirmer.
Le budget V5 ne les chiffre pas encore. Aucun achat ajouté ni aucune fabrication validée.
La maquette est une implantation provisoire fondée sur des composants parfois estimés.

La plaque contient des perçages virtuels et quatre passages de sangles.
Ces modifications indiquent des besoins de montage, sans valider un plan de perçage.
Les connecteurs simplifiés ont été adaptés localement pour représenter les insertions.
Les vues n’attestent pas la tenue des fixations, les rayons de courbure ou la stabilité réelle.
Le contrôle d’interférences compare les groupes de pièces ; le faisceau interne est exclu.
Il complète le réimport STEP, sans remplacer les mesures et les essais physiques.
Un contrôle de champ de vision approximatif vérifie aussi les pièces devant l’objectif.

Recréation : voir les [outils](../tools/README.md) et build_drone_assembly.py.

## Montage physique

Ordre de travail proposé. Chaque étape reste à réaliser ; noter les résultats dans les fiches
et dans l’[état du projet](../project_state.md).

1. Confirmer stocks, contenus et achats conditionnels avec la [liste](../listeAchat.md).
2. À réception, contrôler Pi, caméra, nappe, microSD, deux moteurs, roues et roulette.
3. Monter le châssis avec ses supports et sa visserie, sans alimentation.
4. Relever dimensions et masses dans la [mécanique](../Mecanique/README.md).
5. Préparer la microSD depuis le Mac et tester Pi/caméra séparément des moteurs.
6. Identifier le vrai brochage du DRV8833, ses rappels et son boîtier.
7. Préparer le [faisceau](../Electronique/README.md) et choisir les fusibles après mesures.
8. Installer cartes, batterie et caméra ; garder les connexions accessibles et immobiliser les fils.
9. Contrôler continuité, polarité et alimentation avant de raccorder les cartes.
10. Tester sur alimentation limitée, roues levées, puis un moteur à la fois.
11. Tester vidéo et deux démarrages simultanés, reset et perte de commandes.
12. Passer au sol après ces contrôles ; mesurer latence, température et autonomie.

Le [logiciel](../Logiciel/README.md) et les [essais](../Validation/README.md)
font partie du prototype à développer. Le pilotage est disponible et testé hors matériel ;
une fiche n’est pas une validation de montage.
Suivre la [checklist à cocher](checklist.md) à réception des composants.
