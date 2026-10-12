# Validation matérielle — révision puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Aucun essai de cette liste effectué. Les calculs et tests logiciels sont des préparations.

- [ ] P01 — Confirmer le budget, tous les stocks, variantes et identité des deux MD13S.
- [ ] P02 — Confirmer contenu du chargeur, cordon secteur et prise d'équilibrage 3S.
- [ ] P03 — Mesurer roues, moyeux, équerres, plaque, appui, masses et centres de gravité.
- [ ] P04 — Confirmer rigidité du kit et réaliser la nouvelle implantation avant perçage.
- [ ] P05 — Documenter pouvoir de coupure DC et coordination fusibles/sections/pack.
- [ ] P06 — Contrôler faisceau hors tension : polarité, isolement, rappels et maintien.
- [ ] P07 — Régler UBEC 5 V et mesurer tension Pi avec caméra et moteurs.
- [ ] P08 — Tester seuils et mémorisation de coupure, retour sans démarrage imprévu.
- [ ] P09 — Vérifier alarme par cellule, seuil 3,6 V et procédure de déconnexion.
- [ ] P10 — Tester PWM/DIR roues levées avec alimentation limitée, sens et rampe.
- [ ] P11 — Mesurer pointes, températures et surtensions d'arrêt/inversion/coupure.
- [ ] P12 — Mesurer démarrage, boot, perte réseau, gel et SIGKILL ; coupure indépendante.
- [ ] P13 — Vérifier arrêt logiciel 300 ms et distance d'arrêt avec vidéo active.
- [ ] P14 — Commencer au sol à PWM 25 %, tester appui, fixation et virages.
- [ ] P15 — Monter progressivement vers 95 % après validation, mesurer vitesse et freinage.
- [ ] P16 — Mesurer autonomie, tensions par cellule et comportement sur sols/pentes.
- [ ] P17 — Recalculer prévisions avec mesures et réviser budget/protections si nécessaire.
- [ ] P18 — Mettre à jour STEP, supports et fiches illustrées des nouveaux composants.

Un alarme par cellule sans coupure automatique impose un opérateur présent. Ne pas considérer le
seuil de tension totale comme une protection de chaque cellule. Relever les critères et résultats
avec le [modèle][archive-lien-1] ; conserver photos et valeurs mesurées.

Les contrôles électriques détaillés figurent dans le [circuit][archive-lien-2]. Les
[calculs][archive-lien-3] expliquent les valeurs à confronter aux essais.
Aucun résultat logiciel ne coche automatiquement une case matérielle.

[archive-lien-1]: ../../../Validation/modele.md
[archive-lien-2]: ../Electronique/puissance.md
[archive-lien-3]: ../Mecanique/performance-puissance.md

[statut-archive]: ../README.md
