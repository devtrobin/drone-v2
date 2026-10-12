# Liste des tâches — Drone V2

Mise à jour : **12 octobre 2026**. Retour à la base TT / USB 5 V.
Cases cochées : travail réellement effectué.
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

Preuves : [accueil](ReadMe.md), [câblage](Electronique/schema.md),
[relevés](Mecanique/releves.md), [sources](Sources/verification-technique.md)
et [rapport](Validation/resultats/logiciel-hors-materiel.json).

Fiches illustrées : [index PDF](Composants/fiches-pdf.md) et [rapport PDF][rapport-pdf].
Dimensions : [synthèse des estimations](Mecanique/estimations.md) et registres des 19 composants.

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

Preuves et mode d’emploi : [Logiciel](Logiciel/README.md).
L’interface est écrite et sa logique testée ; son ergonomie reste à vérifier manuellement.
Le pipeline vidéo est préparé ; il ne prouve pas que la caméra et le Pi ont été testés.

## Achats à finaliser

- [ ] A01 — Trouver un Pi seul disponible hors Amazon, avec prix et frais vérifiés.
- [ ] A02 — Revalider prix, variantes, stock et livraison des 18 lots Amazon.
- [ ] A03 — Confirmer présence de l’appui passif et de toute la visserie dans le kit.
- [ ] A04 — Décider les compléments après relevé du module et essais électriques.
- [ ] A05 — Recalculer le budget réel ; la cible 150 € reste non atteinte.
- [ ] A06 — Commander les lots retenus puis enregistrer les réceptions.

Aucun achat automatisé. Voir [listeAchat](listeAchat.md).
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

Supports : [électricité](Electronique/releves.md), [mécanique](Mecanique/releves.md),
[montage](Assemblage/checklist.md).

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

Les critères et preuves sont dans [Validation](Validation/README.md).
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

Preuves : [index des modèles](Composants/modeles-3d.md) et [rapport STEP][rapport-step].
La [maquette](Assemblage/README.md) et les [compléments](Assemblage/composants-manquants.md)
préparent l’assemblage. Aucune fabrication ou mesure physique validée.

[rapport-step]: Validation/resultats/modeles-step.json

[rapport-pdf]: Validation/resultats/fiches-pdf.json

## Retour à la base lente et évolution future

- [x] R01 — Archiver la proposition rapide et ses références, calculs et logiciel.
- [x] R02 — Restaurer achats, architecture, câblage et profil DRV8833 de la base V5.
- [x] R03 — Réactiver les fiches et assemblages 3D existants sans modifier leurs cotes.
- [ ] F01 — Réétudier moteurs et batterie/puissance plus tard, selon essais et budget.

La base actuelle vise environ 2,2 km/h estimés à pleine commande ; les premiers essais
restent limités à 35 % PWM. L'évolution rapide est exclue du panier actif.
Voir l'[étude archivée][archive-evolution] pour la reprendre ultérieurement.

[archive-evolution]: Archives/evolution-puissance-2026-10-12/README.md
