# 3 modules DRV8833, un utilisé

Module déjà assemblé : deux ponts en H pour commander les moteurs indépendamment.

**État : non acheté, intégration à valider.** Décision : prévu dans la base.
Référence issue de V5 ; données de prix et stock relevées le 2026-10-11, non actualisées.

## Achat de référence

- [Annonce retenue][achat] — vendeur relevé : Easy Word Mall.
- Variante : 3 cartes DRV8833.
- Un lot entier : **6,99 € TTC hors livraison**.
- Lots prévus : 1 ; total de référence : **6,99 €**.
- Besoin initial : 1 pilote pour les 2 moteurs.
- Contenu annoncé : 3 cartes DRV8833.
- Disponibilité au relevé : En stock. Revalider avant commande.

## Intégration et points à confirmer

Vendeur : 3–10 V, 1,5 A. TI distingue 500 mA RMS (PW) de 1,5 A (PWP/RTY) : courant continu du lot
non certifié. Noms EEP/ULT ambigus : relever nSLEEP/nFAULT et les résistances avant raccordement.

## Suivi de réception

| Information | État |
| --- | --- |
| Date et quantité reçues | À renseigner |
| Référence réelle / variante | À contrôler |
| Dimensions et masse utiles | À mesurer si embarqué |
| Essai de réception | Non réalisé |

[Sources de cette fiche][lien-1] · [Liste complète][lien-2]
· [Architecture][lien-3] · [Validation][lien-4].

[achat]: https://www.amazon.fr/dp/B076KFRJWL

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

- [Fiche illustrée](drv8833.pdf).
- [Galerie locale](photos/README.md) : vues pertinentes et crédits de provenance.
- [Registre documentaire](documentation.json) : URL, dates et empreintes des sources.
- [Notice source : datasheet-ti-drv8833.pdf](notices/datasheet-ti-drv8833.pdf).

Dimensions vendeur et fabricant distinguées des relevés à effectuer sur le matériel.
Les prix restent ceux de la sélection V5 ; ce PDF ne valide ni achat ni réception.

## Dimensions disponibles et estimées

[Données et méthodes](dimensions.json) : cotes publiées, estimations et références.
Les plages sont des incertitudes de travail ; aucune dimension physique mesurée.

| Élément | Hypothèse en mm | Confiance |
| --- | --- | --- |
| Hauteur module nu | 5 | faible |
| Pas / trou de contact | 2,54 × 1 | moyenne |

Valeurs centrales uniquement dans ce tableau. Plages et justification dans dimensions.json
et dans le PDF. Les cotes publiées figurent aussi dans ces deux documents.

Aucun trou de fixation dédié confirmé. Hauteur avec barrettes dépend du montage ; le poids 10 g
de colis reste exclu.

## Modèle 3D STEP

- [Modèle STEP en millimètres](drv8833.step).
- [Aperçu du modèle](modele-3d.png).
- [Représentation, cotes et hypothèses](modele-3d.json).

Modèle de placement simplifié, créé depuis les cotes et images de ce dossier.
Les détails supplémentaires estimés sont explicités dans le registre 3D.
Confirmer sur le matériel avant perçage, fabrication ou choix définitif des supports.
