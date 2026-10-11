# Outils de documentation — Drone V2

Depuis le dossier Drone V2, lancer :

```bash
python3 tools/check_project.py
```

Ce contrôle lit les fichiers sans les modifier : liens internes, largeur des lignes Markdown,
tableaux, JSON, provenance de V5, prix des lots, budgets et fiches composants.
Il vérifie aussi que seul le Pi est acheté hors Amazon et que les trois lots électroniques
restent conditionnels dans cette base. Il ne remplace pas les essais physiques ou logiciels.

Le script utilise uniquement la bibliothèque standard de Python, sans paquet à installer.
Après une décision d’achat ou un changement de composant, adapter les données et le contrôle
de référence V5 en conservant la copie originale. Garder l’archive intacte lors de ces adaptations.
