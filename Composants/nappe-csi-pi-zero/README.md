# 2 nappes CSI pour Pi Zero

Adaptation entre le connecteur CSI miniature du Pi Zero et celui de la caméra.

**État : non acheté, intégration à valider.** Décision : prévu dans la base.
Référence issue de V5 ; données de prix et stock relevées le 2026-10-11, non actualisées.

## Achat de référence

- [Annonce retenue][achat] — vendeur relevé : GeeekPi-FR.
- Variante : Golden-2. : 1 nappe 16 cm + 1 nappe 30 cm.
- Un lot entier : **6,99 € TTC hors livraison**.
- Lots prévus : 1 ; total de référence : **6,99 €**.
- Besoin initial : 1 nappe Standard–Mini entre Camera Module 3 et Pi Zero 2 W.
- Contenu annoncé : Golden-2. : 1 nappe 16 cm + 1 nappe 30 cm.
- Disponibilité au relevé : En stock. Revalider avant commande.

## Intégration et points à confirmer

Annonce : 15 broches pas 1,0 mm côté caméra, 22 broches pas 0,5 mm côté Zero. Vérifier sens des
contacts et passage mécanique, installer hors tension.

## Suivi de réception

| Information | État |
| --- | --- |
| Date et quantité reçues | À renseigner |
| Référence réelle / variante | À contrôler |
| Dimensions et masse utiles | À mesurer si embarqué |
| Essai de réception | Non réalisé |

[Sources de cette fiche][lien-1] · [Liste complète][lien-2]
· [Architecture][lien-3] · [Validation][lien-4].

[achat]: https://www.amazon.fr/dp/B07MW7V3Y7

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

- [Fiche illustrée](nappe-csi-pi-zero.pdf).
- [Galerie locale](photos/README.md) : vues pertinentes et crédits de provenance.
- [Registre documentaire](documentation.json) : URL, dates et empreintes des sources.

Dimensions vendeur et fabricant distinguées des relevés à effectuer sur le matériel.
Les prix restent ceux de la sélection V5 ; ce PDF ne valide ni achat ni réception.

## Dimensions disponibles et estimées

[Données et méthodes](dimensions.json) : cotes publiées, estimations et références.
Les plages sont des incertitudes de travail ; aucune dimension physique mesurée.

| Élément | Hypothèse en mm | Confiance |
| --- | --- | --- |
| Largeurs aux contacts | 16 × 11,5 | moyenne |
| Épaisseur | 0,2 × 0,3 | faible |

Valeurs centrales uniquement dans ce tableau. Plages et justification dans dimensions.json
et dans le PDF. Les cotes publiées figurent aussi dans ces deux documents.

Les longueurs commerciales restent 160 et 300 mm ; les oreilles ne sont pas des largeurs cotées.

- [E1 : Molex Premo-Flex : exemple FFC 0,5 mm][est-source-1] ; référence analogue.

[est-source-1]: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/173/17331/173310406_sd.pdf

## Modèle 3D STEP

- [Modèle STEP en millimètres](nappe-csi-pi-zero.step).
- [Aperçu du modèle](modele-3d.png).
- [Représentation, cotes et hypothèses](modele-3d.json).

Modèle de placement simplifié, créé depuis les cotes et images de ce dossier.
Les détails supplémentaires estimés sont explicités dans le registre 3D.
Confirmer sur le matériel avant perçage, fabrication ou choix définitif des supports.
