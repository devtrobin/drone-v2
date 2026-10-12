# Châssis DollaTek 2WD équipé

Base mécanique : plaque, deux motoréducteurs, roues, fixations et appui passif à confirmer.

**État : non acheté, intégration à valider.** Décision : prévu dans la base.
Référence issue de V5 ; données de prix et stock relevées le 2026-10-11, non actualisées.

## Achat de référence

- [Annonce retenue][achat] — vendeur relevé : DollaTek.
- Variante : Plaque acrylique, 2 motoréducteurs, 2 roues, supports, visserie, disques encodeurs,
  boîtier 4 AA ; roulette montrée sur la photo.
- Un lot entier : **13,99 € TTC hors livraison**.
- Lots prévus : 1 ; total de référence : **13,99 €**.
- Besoin initial : 1 châssis avec 2 moteurs, roues et appui passif.
- Contenu annoncé : Plaque acrylique, 2 motoréducteurs, 2 roues, supports, visserie, disques
  encodeurs, boîtier 4 AA ; roulette montrée sur la photo.
- Disponibilité au relevé : 1 exemplaire annoncé. Revalider avant commande.

## Intégration et points à confirmer

La liste textuelle n’explicite pas la roulette visible sur la photo : confirmer le contenu. Aucun
courant de blocage ni couple moteur vérifié. Piles non incluses et non nécessaires pour
l’architecture USB du Drone V2.

## Suivi de réception

| Information | État |
| --- | --- |
| Date et quantité reçues | À renseigner |
| Référence réelle / variante | À contrôler |
| Dimensions et masse utiles | À mesurer si embarqué |
| Essai de réception | Non réalisé |

[Sources de cette fiche][lien-1] · [Liste complète][lien-2]
· [Architecture][lien-3] · [Validation][lien-4].

[achat]: https://www.amazon.fr/dp/B07F73HY34

<!-- Liens utilisés dans ce document. -->

[lien-1]:
  <sources.json>
[lien-2]:
  <../../listeAchat.md>
[lien-3]:
  <../../architecture.md>
[lien-4]:
  <../../Validation/README.md>

## Fiche PDF et documentation

- [Fiche illustrée](chassis-2wd.pdf).
- [Galerie locale](photos/README.md) : vues pertinentes et crédits de provenance.
- [Registre documentaire](documentation.json) : URL, dates et empreintes des sources.

Dimensions vendeur et fabricant distinguées des relevés à effectuer sur le matériel.
Les prix restent ceux de la sélection V5 ; ce PDF ne valide ni achat ni réception.

## Dimensions disponibles et estimées

[Données et méthodes](dimensions.json) : cotes publiées, estimations et références.
Les plages sont des incertitudes de travail ; aucune dimension physique mesurée.

| Élément | Hypothèse en mm | Confiance |
| --- | --- | --- |
| Plaque | 200 × 140 × 3 | faible |
| Roue motrice | 65 × 25 | moyenne |
| Corps moteur TT | 70 × 22 × 18 | moyenne |
| Appui pivotant | 40 × 32 × 25 | faible |
| Boîtier quatre AA | 63 × 58 × 16 | moyenne |
| Kit assemblé | 200 × 185 × 70 | faible |
| Voie entre roues | 160 | faible |
| Perçages ronds | 3,2 | faible |

Valeurs centrales uniquement dans ce tableau. Plages et justification dans dimensions.json
et dans le PDF. Les cotes publiées figurent aussi dans ces deux documents.

La vue éclatée contient probablement des éléments redimensionnés ; les roues de cette vue ne
servent pas à étalonner la plaque.

Les plages sont des hypothèses de travail, pas des tolérances fabricant. Ne pas reporter les
anciens perçages V1.

- [E1 : SunRobotics : kit 2WD acrylique similaire][est-source-1] ; référence analogue.
- [E2 : Adafruit 3777 : motoréducteur TT similaire][est-source-2] ; référence analogue.
- [E3 : Adafruit 3784 : support quatre AA similaire][est-source-3] ; référence analogue.

[est-source-1]: https://www.sunrobotics.in/products/robot-chassis-2wd-cars-diy-kit

[est-source-2]: https://www.adafruit.com/product/3777

[est-source-3]: https://www.adafruit.com/product/3784

## Modèle 3D STEP

- [Modèle STEP en millimètres](chassis-2wd.step).
- [Aperçu du modèle](modele-3d.png).
- [Représentation, cotes et hypothèses](modele-3d.json).

Modèle de placement simplifié, créé depuis les cotes et images de ce dossier.
Les détails supplémentaires estimés sont explicités dans le registre 3D.
Confirmer sur le matériel avant perçage, fabrication ou choix définitif des supports.
