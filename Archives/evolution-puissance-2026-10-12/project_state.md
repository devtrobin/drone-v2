# État du projet — Drone V2 puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Mise à jour : **12 octobre 2026**. Objectif accepté : **6–8 km/h, priorité vitesse**. Pi Zero 2 W
et caméra V1 conservés. Achats Amazon sauf Pi, sans éclairage. Aucun achat, fabrication ou essai
physique enregistré.

## Préparation terminée

- Deux moteurs 37D 18,8:1 retenus en prévision, roues 80 mm et moyeux 6 mm documentés.
- Pack LiPo 3S, chargeur équilibré et circuit de puissance à base de modules sélectionnés.
- Douze nouveaux lots Amazon relevés avec prix, variantes et réserves dans leurs dossiers.
- Panier actif de 31 lignes et budget **508,07 € hors port**, hausse de **251,04 €**.
- Architecture, faisceau, protections proposées et vérifications matérielles documentés.
- Pilote deux MD13S PWM/DIR, rampe d'avance et limite de rotation implémentés.
- Nouveau profil non confirmé et limité à 25 % pour les premiers essais.
- Calculs reproductibles de traction, vitesse, autonomie, rotation et stabilité disponibles.
- Archive avant puissance conservée ; les 19 PDF/STEP et assemblages restent historiques.

Prévisions : **6,4–7,7 km/h** à PWM cible 95 %, **78 minutes** centrales, masse supposée **1,058
kg**. Scénarios d'autonomie 39–98 minutes. Ce ne sont pas des mesures.

## Réserves ouvertes

Le plafond historique **150 € n'est pas atteint** : dépassement 358,07 €. Le Pi de référence reste
indisponible au dernier relevé et les prix conservés sont historiques. Les cartes vendues comme
MD13S ont une marque d'annonce différente de Cytron ; faire confirmer identité avant commande.
Cercle des moyeux et contenu du chargeur restent à vérifier.

Fusibles DC et protection de surtension non qualifiés. La coupure générale ne protège pas
individuellement les cellules ; l'alarme impose d'arrêter et débrancher sous surveillance. La
batterie ne se recharge plus depuis le Mac. Le circuit est à fabriquer par câblage de modules,
sans PCB personnalisé.

La plaque, la roulette, les rehausses et les cheminements changent : **l'assemblage 3D existant ne
représente pas cette révision**. Aucun nouveau STEP généré dans cette évolution. La nouvelle CAO
et les nouveaux PDF restent à réaliser après consolidation des références et cotes.

## Suite concrète

Suivre les [tâches][archive-lien-1] et la [validation puissance][archive-lien-2], puis relever
le matériel avant montage. Les [achats][archive-lien-3], le [circuit][archive-lien-4] et
les [prévisions][archive-lien-5] constituent la base de reprise.

Le [rapport de contrôles][archive-lien-6] consigne les tests locaux
et la cohérence documentaire ; aucun essai de caméra réelle ou GPIO physique. L'interface Tkinter
reste à essayer sur le Mac.

[archive-lien-1]: TACHES.md
[archive-lien-2]: Validation/puissance.md
[archive-lien-3]: listeAchat.md
[archive-lien-4]: Electronique/puissance.md
[archive-lien-5]: Mecanique/performance-puissance.md
[archive-lien-6]: Validation/resultats/logiciel-puissance.json

[statut-archive]: README.md
