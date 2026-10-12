# Électronique — Drone V2

Conception active rétablie le 12 octobre 2026 : batterie USB VEGER 5 V, module double DRV8833 et
moteurs TT du kit. Le Raspberry Pi et sa caméra partagent la source avec les moteurs, via deux
branches protégées et une masse commune.

Le [schéma du faisceau](schema.md) précise les branchements GPIO candidats, les contrôles et les
compléments possibles. Le Pi est alimenté par micro-USB PWR IN. Recharge USB séparée depuis le Mac
; aucune fonction pass-through supposée.

Pi et DRV8833 sont des cartes du commerce déjà assemblées : le travail est le câblage soudé, sans
PCB personnalisé. Condensateurs et résistances restent des compléments conditionnels après
inspection du module et mesures, déjà comptés dans le budget de référence.

Les [relevés](releves.md) sont à renseigner avant branchement. Mesurer les pointes moteurs et la
tension au Pi avec vidéo ; les 3 A annoncés de la batterie ne garantissent pas les démarrages
simultanés. Aucun essai physique enregistré.

La LiPo 3S, les MD13S et le circuit de puissance de la version rapide sont exclus de cette
conception. Leur [étude archivée][archive] pourra être reprise ultérieurement.

[archive]: ../Archives/evolution-puissance-2026-10-12/README.md
