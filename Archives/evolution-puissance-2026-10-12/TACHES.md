# Liste des tâches — Drone V2

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Révision active : **puissance, 12 octobre 2026, objectif 6–8 km/h**.
Les sections historiques ci-dessous prouvent le travail de la base V5 ; les essais physiques
restent ouverts. Aucun achat, nouveau PDF ou nouveau STEP enregistré pour les nouveaux lots.

## Évolution puissance

- [x] P-D01 — Sélectionner moteurs 37D, roues 80 mm et chaîne LiPo 3S pour priorité vitesse.
- [x] P-D02 — Relever 12 nouveaux lots Amazon et créer les dossiers de provenance.
- [x] P-D03 — Créer le panier actif et recalculer le total à 508,07 € hors livraison.
- [x] P-D04 — Documenter circuit à câbler, GPIO, décharge, recharge et réserves électriques.
- [x] P-L01 — Ajouter pilote deux MD13S, rampe et rotation séparément limitée.
- [x] P-L02 — Tester le pilote sur broches simulées et conserver GPIO non confirmés.
- [x] P-L03 — Passer 42 tests de pilotage/calculs et les contrôles du dossier.
- [x] P-D05 — Calculer force, vitesse, autonomie et stabilité avec hypothèses séparées.
- [ ] P-A01 — Résoudre dépassement du plafond 150 € et revalider prix, stocks et identité.
- [ ] P-E01 — Valider fusibles DC, coupure relais, UBEC et surtensions de freinage.
- [ ] P-M01 — Mesurer moyeux, perçages, appui et nouvelles masses ; confirmer implantation.
- [ ] P-M02 — Refaire STEP / PDF pour la révision puissance après consolidation des choix.
- [ ] P-V01 — Exécuter la checklist matérielle, d'abord 25 % PWM puis montée progressive.

Preuves : [panier][archive-lien-1], [circuit][archive-lien-2],
[calculs][archive-lien-3], [guide][archive-lien-4].
Les étapes matérielles détaillées sont dans la [validation puissance][archive-lien-5].

## Historique de la base V5


Mise à jour : **11 octobre 2026**. Cases cochées : travail réellement effectué.
Les essais de logiciel sont hors matériel ; aucune commande, fabrication ou mesure du robot.
Les modèles STEP des composants ont été demandés ensuite ; supports personnalisés à concevoir.

## Dossier et conception préparés

- [x] D01 — Créer un dossier autonome et conserver Drone V1.
- [x] D02 — Reprendre les 19 lots V5 avec archive et budget traçables.
- [x] D03 — Préparer les fiches composants et les champs de réception.
- [x] D04 — Définir objectifs, architecture, implantation et étapes de montage.
- [x] D05 — Préparer schéma, repérage du faisceau et relevés électriques.
- [x] D06 — Créer checklist de montage et modèle de résultat d’essai.
- [x] D07 — Préparer calculs de stabilité et d’autonomie, sans cotes inventées.
- [x] D08 — Contrôler liens, JSON, budget et périmètre des fichiers.
- [x] D09 — Consulter les sources techniques officielles et le stock du Pi.
- [x] D10 — Collecter les photos et notices des 19 composants avec leur provenance.
- [x] D11 — Créer les 19 PDF : dimensions, caractéristiques, réserves et galeries illustrées.
- [x] D12 — Vérifier texte, liens, empreintes et rendu des 94 pages des PDF mis à jour.
- [x] D13 — Ranger chaque PDF dans son dossier composant et adapter les liens et outils.
- [x] D14 — Estimer 30 groupes de cotes sur 16 composants, avec méthodes, sources et plages.

Preuves : [accueil][archive-lien-6], [câblage][archive-lien-7],
[relevés][archive-lien-8], [sources][archive-lien-9]
et [rapport][archive-lien-10].

Fiches illustrées : [index PDF][archive-lien-11] et [rapport PDF][rapport-pdf].
Dimensions : [synthèse des estimations][archive-lien-12] et registres des 19 composants.

## Logiciel préparé et testé hors matériel

- [x] L01 — Écrire le mixage différentiel et les sorties simulées.
- [x] L02 — Écrire le pilote GPIO Zero, avec nSLEEP bas au démarrage et à l’arrêt.
- [x] L03 — Ajouter pause d’inversion, limite PWM et validation de configuration.
- [x] L04 — Développer serveur / client TCP, authentification et tickets périssables.
- [x] L05 — Tester expiration, déconnexion, rejeu et messages invalides sur TCP local.
- [x] L06 — Développer l’interface clavier avec Espace, arrêt et reconnexion manuelle.
- [x] L07 — Préparer acquisition H.264, transport MPEG-TS et réception ffplay.
- [x] L08 — Tester l’API GPIO Zero avec broches simulées.
- [x] L09 — Écrire guides d’installation, d’utilisation et protocole.
- [x] L10 — Exécuter démonstration et tests automatiques, enregistrer le rapport.
- [ ] L11 — Essayer manuellement la fenêtre Tkinter et ses touches sur le Mac de pilotage.
- [ ] L12 — Installer l’OS et les dépendances sur le Pi réel.
- [ ] L13 — Tester GPIO, PWM, sens des roues et accès utilisateur sur le Pi.
- [ ] L14 — Détecter la caméra réelle, tester capture puis transmission.
- [ ] L15 — Mesurer charge CPU, latence et fiabilité avec moteurs + vidéo.
- [ ] L16 — Tester gel complet / SIGKILL et définir une coupure indépendante si nécessaire.

Preuves et mode d’emploi : [Logiciel][archive-lien-13].
L’interface est écrite et sa logique testée ; son ergonomie reste à vérifier manuellement.
Le pipeline vidéo est préparé ; il ne prouve pas que la caméra et le Pi ont été testés.

## Achats à finaliser

- [ ] A01 — Trouver un Pi seul disponible hors Amazon, avec prix et frais vérifiés.
- [ ] A02 — Revalider prix, variantes, stock et livraison des 18 lots Amazon.
- [ ] A03 — Confirmer présence de l’appui passif et de toute la visserie dans le kit.
- [ ] A04 — Décider les compléments après relevé du module et essais électriques.
- [ ] A05 — Recalculer le budget réel ; la cible 150 € reste non atteinte.
- [ ] A06 — Commander les lots retenus puis enregistrer les réceptions.

Aucun achat automatisé. Voir [listeAchat][archive-lien-14].
Le Pi de référence reste en rupture à 22,50 € ; aucune date de retour confirmée.

## Mesures, implantation et montage

- [ ] M01 — Relever dimensions, perçages, appuis, masses et centres des pièces.
- [ ] M02 — Définir l’implantation sur papier et confirmer supports et fixations.
- [ ] M03 — Renseigner les relevés et calculer la stabilité prévisionnelle.
- [ ] E01 — Relever bornes, boîtier, rappels et découplage du DRV8833.
- [ ] E02 — Mesurer courants moteurs et tenue du 5 V commun.
- [ ] E03 — Choisir fusibles, sections, longueurs et éventuels compléments.
- [ ] E04 — Réaliser le faisceau, gainer et contrôler hors tension.
- [ ] M04 — Assembler et maintenir cartes, caméra, batterie et câbles.
- [ ] M05 — Réaliser les essais roues levées, puis autoriser le déplacement au sol.

Supports : [électricité][archive-lien-15], [mécanique][archive-lien-16],
[montage][archive-lien-17].

## Validation du prototype

- [ ] V01 — Réception et contenu confirmés.
- [ ] V02 — microSD, lecteur et démarrage vérifiés.
- [ ] V03 — Module moteur relevé.
- [ ] V04 — Faisceau hors tension contrôlé.
- [ ] V05 — Courants des moteurs compatibles avec le pilote.
- [ ] V06 — Pi et caméra réels fonctionnels.
- [ ] V07 — Charge simultanée sans reset ni coupure USB.
- [ ] V08 — Boot, reset et extinction sans mouvement.
- [ ] V09 — Perte Wi-Fi / commandes : arrêt mesuré.
- [ ] V10 — Arrêt / gel processus : comportement mesuré et corrigé.
- [ ] V11 — Déplacement au sol et tenue mécanique.
- [ ] V12 — Vidéo en mouvement, cadence et latence mesurées.
- [ ] V13 — Autonomie d’au moins 15 minutes, chauffe compatible.
- [ ] V14 — Budget réel enregistré.

Les critères et preuves sont dans [Validation][archive-lien-18].
Les cases V01 à V14 restent ouvertes malgré les tests de simulation.

## Modèles 3D des composants

- [x] D15 — Créer 19 STEP avec noms des pièces, unités mm et hypothèses traçables.
- [x] D16 — Réimporter les STEP et vérifier solides, volumes, dimensions et rendu.
- [ ] M06 — Ajuster les modèles après réception et mesure des composants.
- [x] D17 — Assembler les modèles STEP et proposer les supports / cheminements dans la maquette.
- [x] D18 — Créer les vues, réimporter l’assemblage et vérifier les interférences entre groupes.
- [x] D19 — Lister les supports et fixations manquants, hors budget V5 inchangé.
- [ ] M07 — Confirmer supports, dimensions et implantation de la maquette sur le matériel reçu.
- [ ] M08 — Ajuster et valider les pièces personnalisées avant fabrication.
- [x] A07 — Choisir quatre lots Amazon pour les fixations et chiffrer le budget prévisionnel.
- [x] D20 — Calculer traction, vitesse, autonomie et rotation avec hypothèses et sensibilités.
- [ ] A08 — Contrôler kit et fixations reçus, ajuster supports et recalculer le coût réel.
- [ ] M09 — Remplacer les masses et paramètres moteurs estimés par des mesures, puis recalculer.

Preuves : [index des modèles][archive-lien-19] et [rapport STEP][rapport-step].
La [maquette][archive-lien-20] et les [compléments][archive-lien-21]
préparent l’assemblage. Aucune fabrication ou mesure physique validée.

[rapport-step]: ../../Validation/resultats/modeles-step.json

[rapport-pdf]: ../../Validation/resultats/fiches-pdf.json

[archive-lien-1]: listeAchat.md
[archive-lien-2]: Electronique/puissance.md
[archive-lien-3]: Mecanique/performance-puissance.md
[archive-lien-4]: Logiciel/puissance.md
[archive-lien-5]: Validation/puissance.md
[archive-lien-6]: ReadMe.md
[archive-lien-7]: Electronique/schema.md
[archive-lien-8]: ../../Mecanique/releves.md
[archive-lien-9]: ../../Sources/verification-technique.md
[archive-lien-10]: ../../Validation/resultats/logiciel-hors-materiel.json
[archive-lien-11]: ../../Composants/fiches-pdf.md
[archive-lien-12]: ../../Mecanique/estimations.md
[archive-lien-13]: Logiciel/README.md
[archive-lien-14]: listeAchat.md
[archive-lien-15]: ../../Electronique/releves.md
[archive-lien-16]: ../../Mecanique/releves.md
[archive-lien-17]: ../../Assemblage/checklist.md
[archive-lien-18]: ../../Validation/README.md
[archive-lien-19]: ../../Composants/modeles-3d.md
[archive-lien-20]: ../../Assemblage/README.md
[archive-lien-21]: ../../Assemblage/composants-manquants.md

[statut-archive]: README.md
