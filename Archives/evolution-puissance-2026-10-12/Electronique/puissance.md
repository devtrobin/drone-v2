# Circuit de puissance — LiPo 3S et deux MD13S

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Conception prévisionnelle du 12 octobre 2026. Aucun câblage ni essai physique réalisé. Les
annonces de modules sont des caractéristiques vendeur, pas des mesures. Le budget est complet en
prix mais plusieurs références et protections restent à qualifier.

## Faisceau à fabriquer

```text
LiPo 3S XT60 (+) -> F0 -> coupure basse tension (mode OUT) -> étoile (+)
LiPo 3S XT60 (-) ---------------------------------------> étoile GND

étoile (+) -> F1 -> MD13S gauche VM -> moteur gauche
étoile (+) -> F2 -> MD13S droit VM  -> moteur droit
étoile (+) -> F3 -> UBEC entrée ; sortie 5 V -> F4 -> Pi micro-USB PWR IN
GND : retour séparé de chaque module au point étoile
GPIO Pi : PWM/DIR vers chaque MD13S + GND de signal commun

Après la coupure : TVS entre (+) et GND
À chaque pilote : 1000 µF / 35 V entre VM et GND
À chaque moteur : 100 nF céramique directement entre ses deux bornes
Prise équilibre du pack : alarme 3S pendant usage surveillé
```

Les bornes entrée/sortie de la coupure et des pilotes doivent être identifiées sur les cartes
reçues, avec leurs notices. Ne pas déduire les bornes physiques de ce schéma fonctionnel. Ne pas
contourner le relais avec une seconde liaison positive.

Fabriquer la distribution par soudures isolées et modules du commerce ; une carte imprimée n'est
pas requise. Les résistances et condensateurs sont montés directement près des signaux ou charges
concernés. Prévoir retenue mécanique des fils et accès au XT60 pour déconnexion.

## Dimensionnement préliminaire

Un moteur : courant de blocage constructeur 5,5 A sous 12 V. Sous 12,6 V, extrapolation 5,78 A,
soit environ **11,83 A au total** avec le Pi. Cette pointe n'est pas une consommation continue
admissible du moteur. Ne pas maintenir une roue bloquée. Ni fusible ni rampe PWM ne réalisent une
limitation électronique précise du courant moteur.

Cytron indique 6–30 V, 13 A continus par MD13S et logique 3,3 V. Ces valeurs ne s'appliquent à
l'annonce sélectionnée que si la carte est bien cette référence. Vérifier marque Generchin/Cytron,
notice, sérigraphie et authenticité avant commande. Un MD13S est monocanal ; il en faut deux.

Hypothèses de départ pour sélection de protection : F0 15 A, F1/F2 8 A, F3 2 A côté pack et F4 2 A
côté 5 V. Ces calibres sont des pistes à coordonner avec courant de démarrage, section, thermique,
courbe de fusion et courant de court-circuit du pack. Ils ne constituent pas un choix de fusibles
final.

**Le pouvoir de coupure en courant continu des fusibles 5×20 du lot historique n'est pas publié.**
La seule indication 250 V ne prouve pas l'aptitude à interrompre un court-circuit LiPo. Obtenir la
notice fabricant et valider la coordination, sinon remplacer fusibles et porte-fusibles par une
référence DC documentée avant raccordement. F0 doit être le plus proche possible du pack ; toute
portion avant F0 reste non protégée.

Bus et moteurs en 14 AWG court, retours séparés. Le lot XT60 fournit deux rallonges rouge/noir de
30 cm, soit 1,20 m de conducteur ; les cinq porte-fusibles offrent 1,25 m de fils 16 AWG
supplémentaires. Relever le cheminement et les longueurs réellement disponibles après découpe. Si
insuffisant, ajouter du fil chiffré avant montage. Fil 22 AWG réservé aux GPIO et branche Pi
courte, après contrôle de chute de tension. Aucun courant moteur dans un câble USB.

## Pi et commandes

UBEC réglé sur **5 V**, jamais 6 V. Identifier VBUS/GND d'un câble micro-USB coupé au multimètre,
isoler les fils de données. Mesurer la sortie à vide et pendant vidéo, puis aux pointes moteurs.
Ne pas alimenter simultanément le Pi par deux sources 5 V. Pas de liaison VM au GPIO ni à la
broche 5 V du Pi.

| Fonction | GPIO BCM | Broche physique Pi |
| --- | --- | --- |
| PWM moteur gauche | 17 | 11 |
| DIR moteur gauche | 27 | 13 |
| PWM moteur droit | 22 | 15 |
| DIR moteur droit | 23 | 16 |
| Masse signal | GND | 6 |

Ajouter un rappel externe 10 kΩ vers GND à chaque entrée PWM et DIR. Le GPIO 24/nSLEEP de la base
DRV8833 n'est plus utilisé. Vérifier absence de rappel à une tension supérieure à 3,3 V sur les
entrées des cartes reçues. Montage direct sur pastilles Pi avec fils maintenus, barrette non
supposée.

**PWM bas produit le freinage du MD13S**, alors que le DRV8833 historique était commandé en roue
libre. Arrêt, boot, perte de liaison et inversion doivent donc être vérifiés mécaniquement et
électriquement. Le gel du processus n'est pas couvert par le seul délai logiciel. Déconnexion XT60
accessible et essai de coupure indépendante à prévoir pour ce cas.

## Décharge et recharge

Coupure Vegena 6–60 V en mode **OUT** (décharge). Réglages proposés : DN 10,5 V, UP 12,0 V, DOP 30
s, démarrage forcé FOP 0. Vérifier dans la notice reçue leur signification, mémorisation et
comportement ; pas de sortie forcée automatique. Le délai filtre les creux mais laisse la décharge
continuer pendant 30 s. Seuil de tension totale seulement : il ne détecte pas une cellule
déséquilibrée.

Alarme ARCELI sur la prise d'équilibrage 3S, seuil proposé **3,6 V par cellule**. Le réglage
vendeur 3,3 V doit être changé. À la première alarme, arrêter, éteindre le Pi proprement et
débrancher pack et moniteur. Ne pas attendre la coupure générale : elle éteindrait brutalement le
Pi. Ne pas laisser la batterie branchée au stockage. Cette protection exige un opérateur présent
et n'est pas un BMS autonome par cellule.

Un seul pack alimentant le drone ; **jamais les deux en parallèle**. SkyRC e3 réservé à ce pack
LiPo 3S, recharge hors robot, par prise d'équilibrage vérifiée, conformément à sa notice et sous
surveillance. Le chargeur équilibre les cellules ; la coupure OUT n'est ni un chargeur ni un
équilibreur. Vérifier la fourniture du cordon secteur européen et la compatibilité JST-XH.

## Surtensions et essais à mener

TVS 1.5KE18A : cathode repérée sur (+), anode sur GND, après coupure. La fiche Vishay de famille
donne 15,3 V de maintien et 25,2 V d'écrêtage au courant de test. L'UBEC vendeur accepte jusqu'à
26 V : **marge réduite**, montage non qualifié par cette comparaison. Les condensateurs 35 V et la
TVS doivent être identifiés et leur dissipation vérifiée.

À 8 km/h, énergie cinétique estimée 2,61 J. Deux 1000 µF ne suffisent pas à absorber l'énergie
d'un freinage complet sans hausse importante de tension. La TVS amortit des transitoires, elle
n'est pas une résistance de freinage permanente. Mesurer les pics à l'oscilloscope lors d'arrêt,
inversion et coupure relais, pack plein puis plus vide. Si les limites des modules sont dépassées,
revoir la protection/régulation avant essais rapides.

1. Identifier modules et documenter fusibles DC avant branchement LiPo.
2. Contrôler polarités, isolement, serrages et rappels sans alimentation.
3. Tester avec alimentation de laboratoire limitée, moteurs déconnectés, puis roues levées.
4. Mesurer 5 V, démarrage, échauffement, freinage et état des sorties au boot/arrêt.
5. Tester coupure de décharge par alimentation réglable, sans vider abusivement la LiPo.
6. Vérifier alarme, coupure relais et arrêt sur perte réseau ; consigner les résultats.
7. Monter progressivement la PWM au sol avec protection mécanique et espace dégagé.

Les caractéristiques et achats sont dans le [registre][sources]. Voir la [notice Cytron][cytron],
le [chargeur SkyRC][skyrc] et la [fiche TVS][tvs].

[sources]: ../Sources/motorisation-puissance.json
[cytron]: https://my.cytron.io/p-13a-6v-30v-dc-motor-driver
[skyrc]: https://www.skyrc.com/e3_Charger
[tvs]: https://www.vishay.com/docs/88301/15ke.pdf

[statut-archive]: ../README.md
