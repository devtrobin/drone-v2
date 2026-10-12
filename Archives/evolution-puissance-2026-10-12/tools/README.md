# Outils — Drone V2

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Révision puissance : [calculs][archive-lien-1],
[script][archive-lien-2] et [hypothèses][archive-lien-3].
Le script performance_drone.py ci-dessous reste celui de la base TT / USB 5 V.


Depuis la racine Drone V2 :

```bash
python3 tools/check_project.py
python3 tools/run_checks.py
python3 tools/run_checks.py --report Validation/resultats/logiciel-hors-materiel.json
python3 tools/pre_dimensionnement.py Mecanique/releves.json
```

check_project contrôle liens, tableaux, lignes à 100 caractères (hors références URL), JSON, V5,
budget, fiches, syntaxe Python, GPIO candidats et intégrité des 19 modèles STEP.
Il ignore environnements locaux et fichiers privés.

run_checks ajoute les tests de pilotage, réseau local et calculs analytiques.
Les tests GPIO Zero sont exécutés si cette bibliothèque est installée dans le Python utilisé.
Les tests vidéo synthétique exigent FFmpeg et ffprobe. Les tests absents sont signalés,
pas comptés comme une validation matérielle. Le rapport conserve les sorties brutes et versions.

Pour tous les tests, utiliser le Python de l’environnement décrit dans
[Logiciel/installation][archive-lien-4] :

```bash
Logiciel/.venv/bin/python tools/run_checks.py
```

pre_dimensionnement ne modifie pas les relevés et ne crée aucun fichier 3D.
Il retourne 2 lorsque les données sont manquantes ; ce comportement est attendu avant réception.
Voir la [méthode][archive-lien-5].

Les outils ne remplacent pas les essais électriques et mécaniques.
Après une modification de sélection, adapter les références actives et les contrôles
en conservant l’archive V5 originale. Les prix actuels ne doivent pas réécrire cette archive.

## Fiches PDF illustrées

Les [PDF][archive-lien-6] sont générés depuis les fichiers locaux, sans accès réseau.
Créer un environnement dédié, puis lancer depuis la racine Drone V2 :

```bash
python3 -m venv /tmp/drone-pdf-env
/tmp/drone-pdf-env/bin/python -m pip install -r tools/requirements-pdf.txt
/tmp/drone-pdf-env/bin/python tools/generate_component_pdfs.py
```

Le générateur lit achats.json, Sources/fiches-techniques.json et les registres des composants.
Les dimensions.json regroupent cotes publiées, hypothèses, plages, méthodes et sources comparables.
Il vérifie les photos par SHA-256, les textes et liens attendus, puis rend toutes les pages.
Chaque PDF est écrit dans Composants/<slug>/<slug>.pdf, auprès de la fiche du composant.
Les PNG et planches de contrôle sont écrits dans tmp/pdfs/rendered.
L’index des PDF et la synthèse mécanique doivent être adaptés si le nombre de pages ou cotes change.
Le rapport est écrit dans Validation/resultats/fiches-pdf.json, avec revue visuelle à réaliser.
Examiner toutes les pages après régénération, consigner cette revue et supprimer les temporaires.
La vérification automatique des marges ne détecte pas toutes les erreurs visuelles.

collect_pdf_sources.py effectue une nouvelle collecte réseau des annonces et de leurs galeries.
Cette commande écrase documentation.json et peut remplacer les images locales : elle ne sert pas
à une simple régénération des PDF. Avant de la relancer, conserver une copie du dossier.
Après collecte, revoir les images, variantes et cotes.
Réintégrer les notices et photos officielles.
Adapter ensuite les indices selected des fiches techniques et les registres des galeries.
La collecte ne constitue ni une mise à jour des prix ni une validation de réception.
Après toute collecte, contrôler aussi les photos citées dans dimensions.json et leurs empreintes.

## Modèles STEP des composants

Créer un environnement CAO séparé ; génération sans réseau depuis la racine Drone V2 :

```bash
python3 -m venv /tmp/drone-cad-env
/tmp/drone-cad-env/bin/python -m pip install -r tools/requirements-step.txt
/tmp/drone-cad-env/bin/python tools/generate_component_step.py
```

Le générateur écrit les 19 STEP, les aperçus et modele-3d.json dans les dossiers composants.
Il exporte des assemblages en mm avec noms et couleurs, sans fusionner les pièces distinctes.
Les dimensions de la table des condensateurs proviennent directement des fiches techniques.
Les autres valeurs et formes paramétrées dans le script suivent les registres dimensions.json.
Chaque modèle indique les hypothèses supplémentaires et les SHA-256 de ses sources locales.
Après un changement de cote, adapter les paramètres et les hypothèses dans le script.
Après changement d’une source locale ou du générateur, régénérer les modèles
pour remettre les empreintes à jour.

La réimportation vérifie B-rep, solides, volume, bornes et unité millimètre.
Le rapport est [modeles-step.json][archive-lien-7].
La revue visuelle y est remise à « à vérifier » à chaque génération.
Examiner les 19 aperçus puis consigner la revue avant de lancer check_project.
Le drapeau --no-preview sert au diagnostic ; produire les aperçus pour une livraison complète.
Les [modèles][archive-lien-8] restent des hypothèses d’implantation.

## Assemblage 3D

Depuis la racine Drone V2, avec le même environnement CAO :

```bash
/tmp/drone-cad-env/bin/python tools/build_drone_assembly.py
python3 tools/check_project.py
```

Le générateur importe les STEP composants existants avec leurs noms et couleurs.
Il conserve leurs empreintes ; les adaptations locales sont listées dans implantation.json.
Il crée drone-v2.step, atelier-v2.step et cinq vues dans Assemblage.
Le robot utilise 13 références ; les six autres sont montrées en atelier.
Les fixations ajoutées et les pièces du kit à confirmer restent dans composants-manquants.json.
Ces compléments n’ajoutent pas de prix arbitraires au budget de référence.

verification.json conserve les sources, les réimports, les volumes et les bornes exactes.
Le calcul des bornes ignore la triangulation des aperçus pour comparer les surfaces STEP.

## Prévision des performances

```bash
python3 tools/performance_drone.py
python3 -m unittest discover -s tools/tests -v
```

Le premier script lit Mecanique/hypotheses-performance.json et écrit
Validation/resultats/performance.json avec les empreintes de ses sources.
Il calcule effort, couple, réactions, vitesse, moment de rotation et autonomie.
Les hypothèses restent séparées des relevés réels et les cas défavorables sont inclus.
Voir [le rapport][archive-lien-9] pour les limites du moteur analogue.
La nomenclature géométrique initiale de l’assemblage reste archivée ;
le prix des quatre lots ajoutés et le total courant sont dans achats.json et listeAchat.md.
Le contrôle de chevauchement compare les groupes distincts, hors intérieur du faisceau.
La revue des cinq vues doit être consignée après génération.
Les mesures physiques, le brochage DRV8833 et les fixations définitives restent à valider.

[archive-lien-1]: ../Mecanique/performance-puissance.md
[archive-lien-2]: performance_puissance.py
[archive-lien-3]: ../Mecanique/hypotheses-puissance.json
[archive-lien-4]: ../Logiciel/installation.md
[archive-lien-5]: ../../../Mecanique/releves.md
[archive-lien-6]: ../../../Composants/fiches-pdf.md
[archive-lien-7]: ../../../Validation/resultats/modeles-step.json
[archive-lien-8]: ../../../Composants/modeles-3d.md
[archive-lien-9]: ../../../Mecanique/performance.md

[statut-archive]: ../README.md
