# 100 condensateurs 100 nF

Complément antiparasite aux bornes des moteurs et découplage local, selon montage réel.

**État : non acheté, intégration à valider.** Décision : à confirmer après inspection et essais.
Référence issue de V5 ; données de prix et stock relevées le 2026-10-11, non actualisées.

## Achat de référence

- [Annonce retenue][achat] — vendeur relevé : XINGZHI TECH.
- Variante : 100 condensateurs céramiques 100 nF / 50 V.
- Un lot entier : **6,99 € TTC hors livraison**.
- Lots prévus : 1 ; total de référence : **6,99 €**.
- Besoin initial : 2 antiparasites moteur + découplage local.
- Contenu annoncé : 100 condensateurs céramiques 100 nF / 50 V.
- Disponibilité au relevé : En stock. Revalider avant commande.

## Intégration et points à confirmer

Variante 100NF, composants traversants. Pattes courtes ; un aux bornes de chaque moteur et
découplage local des cartes.

## Décision sur ce complément

Lot conditionnel, chiffré dans la référence V5 mais pas définitivement indispensable.
Le besoin ci-dessus est une proposition initiale, pas une quantité de montage validée.
Contrôler les composants déjà intégrés au module et les mesures avant achat.
Le DRV8833 possède des résistances internes de rappel ; le module réel peut les compléter.
Les valeurs de capacité supplémentaires dépendent du moteur, des fils et de la source 5 V.
Quelques pièces se soudent au câblage ou aux moteurs ; aucun PCB sur mesure n’est prévu.

## Suivi de réception

| Information | État |
| --- | --- |
| Date et quantité reçues | À renseigner |
| Référence réelle / variante | À contrôler |
| Dimensions et masse utiles | À mesurer si embarqué |
| Essai de réception | Non réalisé |

[Sources de cette fiche][lien-1] · [Liste complète][lien-2]
· [Architecture][lien-3] · [Validation][lien-4].

[achat]: https://www.amazon.fr/dp/B0CLQRL6VB

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

- [Fiche illustrée](ceramique-100nf.pdf).
- [Galerie locale](photos/README.md) : vues pertinentes et crédits de provenance.
- [Registre documentaire](documentation.json) : URL, dates et empreintes des sources.

Dimensions vendeur et fabricant distinguées des relevés à effectuer sur le matériel.
Les prix restent ceux de la sélection V5 ; ce PDF ne valide ni achat ni réception.

## Dimensions disponibles et estimées

[Données et méthodes](dimensions.json) : cotes publiées, estimations et références.
Les plages sont des incertitudes de travail ; aucune dimension physique mesurée.

| Élément | Hypothèse en mm | Confiance |
| --- | --- | --- |
| Corps enrobé | 5 × 4 × 3 | faible |
| Pattes | 2,5 × 0,5 × 20 | faible |

Valeurs centrales uniquement dans ce tableau. Plages et justification dans dimensions.json
et dans le PDF. Les cotes publiées figurent aussi dans ces deux documents.

Les propriétés électriques et le diélectrique Murata ne sont pas attribués au lot XINGZHI TECH.

- [E1 : Murata RDE : céramique radiale analogue][est-source-1] ; référence analogue.

[est-source-1]: https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/RDE_X7R_X7S_25V-100V_E.pdf

## Modèle 3D STEP

- [Modèle STEP en millimètres](ceramique-100nf.step).
- [Aperçu du modèle](modele-3d.png).
- [Représentation, cotes et hypothèses](modele-3d.json).

Modèle de placement simplifié, créé depuis les cotes et images de ce dossier.
Les détails supplémentaires estimés sont explicités dans le registre 3D.
Confirmer sur le matériel avant perçage, fabrication ou choix définitif des supports.
