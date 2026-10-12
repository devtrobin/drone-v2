# 5 câbles USB-A / micro-USB 30 cm

Recharge et fabrication du faisceau USB 5 V avec embouts conservés.

**État : non acheté, intégration à valider.** Décision : prévu dans la base.
Référence issue de V5 ; données de prix et stock relevées le 2026-10-11, non actualisées.

## Achat de référence

- [Annonce retenue][achat] — vendeur relevé : HisureFR.
- Variante : 5 câbles noirs de 30 cm.
- Un lot entier : **7,99 € TTC hors livraison**.
- Lots prévus : 1 ; total de référence : **7,99 €**.
- Besoin initial : 1 câble coupé pour étoile 5 V ; conserver son embout micro-USB pour PWR IN du Pi.
- Contenu annoncé : 5 câbles noirs de 30 cm.
- Disponibilité au relevé : En stock. Revalider avant commande.

## Intégration et points à confirmer

Variante 30 cm noire. Le vendeur annonce jusqu’à 3 A ; section et chute de tension restent à
contrôler. Identifier VBUS/GND au multimètre après coupe ; ne pas se fier seulement aux couleurs.

## Suivi de réception

| Information | État |
| --- | --- |
| Date et quantité reçues | À renseigner |
| Référence réelle / variante | À contrôler |
| Dimensions et masse utiles | À mesurer si embarqué |
| Essai de réception | Non réalisé |

[Sources de cette fiche][lien-1] · [Liste complète][lien-2]
· [Architecture][lien-3] · [Validation][lien-4].

[achat]: https://www.amazon.fr/dp/B095JZSHXQ

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

- [Fiche illustrée](cables-usb.pdf).
- [Galerie locale](photos/README.md) : vues pertinentes et crédits de provenance.
- [Registre documentaire](documentation.json) : URL, dates et empreintes des sources.

Dimensions vendeur et fabricant distinguées des relevés à effectuer sur le matériel.
Les prix restent ceux de la sélection V5 ; ce PDF ne valide ni achat ni réception.

## Dimensions disponibles et estimées

[Données et méthodes](dimensions.json) : cotes publiées, estimations et références.
Les plages sont des incertitudes de travail ; aucune dimension physique mesurée.

| Élément | Hypothèse en mm | Confiance |
| --- | --- | --- |
| Diamètre câble | 3,5 | faible |
| Embout USB-A | 30 × 15 × 7 | faible |
| Embout micro-USB | 25 × 10 × 5 | faible |

Valeurs centrales uniquement dans ce tableau. Plages et justification dans dimensions.json
et dans le PDF. Les cotes publiées figurent aussi dans ces deux documents.

Ces enveloppes ne prouvent ni section cuivre ni tenue à 3 A. Prévoir en plus le rayon de
courbure du câble.

- [E1 : Adafruit 898 : câble USB-A / micro-B analogue][est-source-1] ; référence analogue.
- [E2 : Hirose ZX : géométrie micro-USB][est-source-2] ; référence analogue.

[est-source-1]: https://www.adafruit.com/product/898

[est-source-2]: https://www.hirose.com/ko/product/document?clcode=&documentid=D31704_en&documenttype=Catalog&lang=ko&productname=&series=ZX

## Modèle 3D STEP

- [Modèle STEP en millimètres](cables-usb.step).
- [Aperçu du modèle](modele-3d.png).
- [Représentation, cotes et hypothèses](modele-3d.json).

Modèle de placement simplifié, créé depuis les cotes et images de ce dossier.
Les détails supplémentaires estimés sont explicités dans le registre 3D.
Confirmer sur le matériel avant perçage, fabrication ou choix définitif des supports.
