# État du projet — Drone terrestre V2

Mise à jour : **12 octobre 2026**. Retour demandé à la base V5 : moteurs TT du kit, roues
d'origine, DRV8833 et batterie USB 5 V. Pi Zero 2 W, Camera Module 3 Standard et pilotage Wi-Fi
avec vidéo conservés. Aucun achat, montage ou essai physique enregistré.

## Version active

- Panier précédent restauré : 19 lots V5 et quatre lots de fixation.
- Budget prévisionnel **257,03 € hors livraison**, dont fixations **51,66 €**.
- Moteurs TT du kit 2WD, pilote double DRV8833 et batterie USB 10 000 mAh retenus.
- Alimentation 5 V en deux branches protégées et recharge séparée depuis le Mac.
- Profil logiciel DRV8833 restauré : GPIO non confirmés, PWM maximale initiale de 35 %.
- Schéma, architecture, spécifications, achats et guides remis en cohérence.
- Les 19 fiches PDF, STEP et assemblages existants redeviennent les références actives.
- Prévisions de force, autonomie, stabilité et virages de la base lente rétablies.

**Vitesse estimée à pleine PWM : 2,18 km/h**, soit environ 2,2 km/h. Avec la limite initiale de 35
%, estimation de 0,67 km/h. Ces calculs utilisent un moteur analogue TT, pas une mesure des
moteurs reçus. La limite de mise au point reste inchangée.

Autonomie centrale estimée : **4 h 53 min**, avec 5,8 W supposés ; les pointes électriques restent
à vérifier. Aucun roulage, virage, autonomie ou démarrage matériel n'est validé.

## Évolution reportée

La version rapide à 508,07 € est écartée du panier actif. Les moteurs 37D, les roues 80 mm, les
MD13S, la LiPo 3S et le nouveau circuit de puissance seront réétudiés plus tard. Les documents,
références, calculs et logiciel de cette proposition sont conservés dans l'[archive][archive].

Le dossier actif ne contient plus le profil MD13S ni ses composants supplémentaires. L'archive est
une étude pour une évolution future, pas une instruction de montage pour la V2 actuelle.

## Reste à faire

- Revalider prix historiques, stocks et disponibilité du Pi hors Amazon.
- Contrôler contenu du kit, roulette, moteurs et fixations à réception.
- Mesurer boîtier DRV8833, courant moteur, pointes et chute de tension 5 V.
- Adapter les supports à l'ABS 3 mm et aux entretoises 5 mm retenus.
- Installer le Pi, essayer caméra, vidéo, interface Mac et GPIO réels.
- Mesurer roulage, rotation, arrêt, température, vitesse et autonomie.

Le plafond historique de **150 € reste non atteint**, même après retour : dépassement **107,03
€**. Sans les trois lots électroniques conditionnels, sous-total **232,06 €** ; il ne constitue
pas un panier final garanti. Prix non actualisés lors de cette restauration.

Les [tâches](TACHES.md), le [câblage](Electronique/schema.md), les [achats](listeAchat.md) et les
[calculs](Mecanique/performance.md) sont les références pour poursuivre. Les [contrôles de
retour][rapport] consignent les vérifications hors matériel ; la checklist de
[validation](Validation/README.md) reste à exécuter sur le robot.

[archive]: Archives/evolution-puissance-2026-10-12/README.md
[rapport]: Validation/resultats/retour-version-precedente.json
