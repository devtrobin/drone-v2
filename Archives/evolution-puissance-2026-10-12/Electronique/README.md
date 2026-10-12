# Électronique — Drone V2 puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Le [schéma actif][archive-lien-1] décrit un pack LiPo 3S, deux MD13S, les protections et un UBEC 5 V
pour le Pi. Le circuit de puissance sera un faisceau utilisant des modules ; aucun PCB
personnalisé requis.

Les résistances de rappel et condensateurs antiparasites sont nécessaires pour cette révision. Le
lot fusibles historique ne peut être validé sans sa capacité de coupure DC. Identité des pilotes,
réglages de décharge et comportement en freinage doivent être vérifiés avant montage.

Les [relevés historiques][archive-lien-2] concernent le DRV8833 et l'USB 5 V. Pour la révision
puissance, consigner les mesures suivant la checklist du nouveau circuit et la
[validation][archive-lien-3].

[archive-lien-1]: puissance.md
[archive-lien-2]: ../../../Electronique/releves.md
[archive-lien-3]: ../Validation/puissance.md

[statut-archive]: ../README.md
