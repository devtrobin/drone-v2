# Architecture — Drone V2 puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Révision du 12 octobre 2026 : **6–8 km/h visés**, priorité vitesse, sans éclairage. Le Pi Zero 2 W
et la Camera Module 3 Standard de V1 restent retenus. Wi-Fi, vidéo et commandes Mac sont
conservés.

## Chaîne mécanique

Deux CQRobot CQR37D12V-C 37D, rapport 18,8:1, sans encodeur, avec équerres ; roues Pololu 80 mm
montées par moyeux 6 mm. Le trou D 3 mm des roues ne se monte pas directement sur les arbres 6 mm.
Vérifier cercle de vis et maintien des moyeux.

La plaque et l'appui passif du kit 2WD sont conservés comme base. Les moteurs TT, leurs supports,
leurs roues et le boîtier AA sont exclus du montage. Leur prix reste dans le lot entier du kit.
Reperçage et rigidité de la plaque à vérifier ; les supports de la maquette précédente ne sont pas
réutilisables tels quels.

## Chaîne électrique

Un pack LiPo 3S 2200 mAh : 11,1 V nominal, 12,6 V plein. Le second pack du lot reste à l'atelier.
Deux pilotes MD13S proposés, un par moteur, pilotés en PWM/DIR par GPIO 3,3 V. L'annonce Amazon
indique Generchin : identité Cytron à confirmer avant de retenir ses caractéristiques.

Distribution en étoile avec fusible général proche du pack, coupure de décharge, puis branches
moteurs protégées. Une branche distincte alimente l'UBEC réglé sur **5 V**, puis micro-USB PWR IN
du Pi. Masses communes au point étoile ; aucun courant moteur dans les pistes du Pi.

Le chargeur SkyRC e3 recharge le pack déconnecté du robot, par prise d'équilibrage 3S. Pas de
recharge USB depuis le Mac. Le [circuit de puissance][archive-lien-1] précise les
protections et les vérifications restant nécessaires. Assemblage de modules et fils soudés : **pas
de PCB sur mesure nécessaire**.

## Logiciel

Serveur TCP authentifié, vidéo H.264 indépendante, délai d'absence de commande de 300 ms. Nouveau
pilote MD13S, rampe PWM et limite séparée de rotation. Ce délai est logiciel : un gel complet du
Pi peut laisser une sortie active. Pas d'encodeur, de mesure de vitesse ni de régulation de
courant.

Le profil [puissance][profil] est livré non confirmé, limite d'avance 25 %, rotation 8 %, rampe
0,30 par seconde. Le profil DRV8833 historique reste disponible pour compatibilité. Le serveur
utilise ce dernier si aucun --config n'est donné : choisir explicitement le nouveau profil.

## Prévisions et état de validation

Les [calculs][archive-lien-2] donnent environ 6,4–7,7 km/h avec une limite PWM
cible de 95 %, à utiliser seulement après essais. Autonomie centrale 78 min, hypothèses non
mesurées. Budget complet **508,07 € hors port**, cible historique de 150 € dépassée.

Les 19 PDF, STEP et assemblages existants décrivent la base V5 à moteurs TT et USB 5 V. Ils sont
conservés comme référence historique, et ne valident pas cette implantation. Aucune nouvelle CAO
générée dans cette évolution. Les [achats][archive-lien-3], [tâches][archive-lien-4] et
[état][archive-lien-5] portent désormais sur la révision puissance.

[profil]: Logiciel/config/robot.puissance.example.json

[archive-lien-1]: Electronique/puissance.md
[archive-lien-2]: Mecanique/performance-puissance.md
[archive-lien-3]: listeAchat.md
[archive-lien-4]: TACHES.md
[archive-lien-5]: project_state.md

[statut-archive]: README.md
