# Drone terrestre V2

Base du nouveau drone, créée le **11 octobre 2026** à partir de la liste d’achat V5.
Robot intérieur à deux roues motrices, piloté depuis un Mac avec vidéo en direct par Wi-Fi.
**Pi Zero 2 W, Camera Module 3 Standard, châssis 2WD, module DRV8833 et batterie USB 5 V.**
Tous les achats sont prévus sur Amazon.fr sauf le Pi seul, acheté chez un autre vendeur.
L’éclairage est exclu. Aucune carte électronique sur mesure n’est prévue ; câblage à réaliser.

**État : préparation documentaire.** Aucun achat, montage, logiciel robot ou essai validé.
Le budget V5 de référence est **205,37 € TTC hors livraison**, supérieur à la cible de 150 €.
Le Pi retenu à 22,50 € était en rupture au relevé ; prix et stock restent à revalider.
Les lots de condensateurs et résistances sont des compléments à confirmer, chiffrés à 24,97 €.
Ils restent dans la référence V5 ; leur retrait éventuel ne vaut pas validation du circuit.

## Documents pour commencer

| Document | Utilité |
| --- | --- |
| [État du projet](project_state.md) | Prochaine action et avancement réel |
| [Spécifications](SPECIFICATIONS.md) | Fonctions, contraintes et critères de réussite |
| [Achats](listeAchat.md) | Lots V5, prix datés et achats conditionnels |
| [Sources des achats](achats.json) | Références, quantités, vendeurs et budget calculé |
| [Architecture](architecture.md) | Relations entre mécanique, énergie et logiciel |
| [Composants](Composants/README.md) | Fiche individuelle des 19 lots de référence |
| [Assemblage](Assemblage/README.md) | Implantation et ordre de montage |
| [Câblage](Electronique/README.md) | Alimentation et GPIO candidats à valider |
| [Logiciel](Logiciel/README.md) | Développement du pilotage et de la vidéo |
| [Validation](Validation/README.md) | Essais à réaliser et résultats à consigner |
| [Matériel disponible](listeMateriel.md) | Mac, routeur et moyens du fablab |

Le dossier est autonome : les liens nécessaires pointent vers ses propres fichiers.
La [copie originale V5](Sources/achats-v5-original.json) permet de retrouver les données de départ.
« Drone V2 » désigne ce nouveau projet ; ce nom ne désigne pas l’ancienne liste d’achat V2.
L’ancien dossier Drone V1 conserve ses listes, fichiers et modèles.
Les plans, masses et calculs de son châssis PMMA ne valident pas le nouveau châssis équipé.

## Organisation

```text
Drone V2/
  ReadMe.md, project_state.md, SPECIFICATIONS.md
  listeAchat.md, achats.json, listeMateriel.md, architecture.md
  Composants/        Fiches et sources des 19 lots
  Electronique/      Câblage et relevés nécessaires, sans PCB sur mesure
  Mecanique/         Dimensions à mesurer et préparation de l’implantation
  Assemblage/        Ordre de montage
  Logiciel/          Conception du futur pilotage, aucun logiciel robot livré
  Validation/       Protocole et emplacement des résultats d’essai
  Sources/          Manifeste V5 original et provenance
  tools/            Vérification locale de la documentation et du budget
```

Après une réception ou un essai, mettre à jour la fiche concernée et l’état du projet.
Modifier achats.json avant de mettre à jour les prix de la liste et des fiches ; garder les sources.
Vérifier ensuite depuis ce dossier : `python3 tools/check_project.py`.
