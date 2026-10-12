# Relevés électriques — Drone V2


Feuille à remplir au banc. **Aucune valeur mesurée à ce jour.**
Noter date, module, instruments, réglage de limitation et référence des deux moteurs.

## Module DRV8833

| Relevé | Valeur / preuve |
| --- | --- |
| Marquage puce et boîtier PW / PWP / RTY | À relever |
| Photo recto et verso, noms des bornes | À ajouter |
| AIN1, AIN2, BIN1, BIN2, VM et GND | À confirmer |
| Borne nSLEEP accessible et état sans Pi | À relever |
| Présence d’un pont ou rappel nSLEEP | À relever |
| Rappels des quatre commandes, tension de rappel | À relever |
| nFAULT identifié, absence de confusion avec entrée | À confirmer |
| Découplage VM et composants déjà présents | À relever |
| Limitation de courant effective et thermique | À établir |

Vérifier l’état au boot avant de valider hardware_confirmed.
Si nSLEEP est relié à une tension incompatible avec le Pi, adapter le module avant raccordement.
La capacité nominale de la puce dépend du boîtier ; ne pas retenir le seul chiffre du vendeur.

## Alimentation et moteurs

| Mesure | Gauche / Pi | Droite / ensemble | Conditions |
| --- | --- | --- | --- |
| Courant moteur à vide | À mesurer | À mesurer | 5 V, roue levée |
| Pointe de démarrage | À mesurer | À mesurer | Limitation documentée |
| Courant sous charge | À mesurer | À mesurer | Sol et PWM notés |
| Tension source USB | Sans moteurs | Avec deux moteurs | Capture transitoire |
| Tension PWR IN | Vidéo seule | Vidéo + démarrages | Minimum observé |
| Courant branche Pi | Au repos | Avec vidéo | Réglages notés |
| Température pilote | Un moteur | Deux moteurs | Après durée notée |
| Coupure USB automatique | À observer | À observer | Faible charge / charge |
| Chute dans fils et fusibles | À mesurer | À mesurer | Longueurs notées |

Mesurer les pointes avec un instrument adapté ; un multimètre seul peut manquer un transitoire.
Éviter un blocage prolongé alimenté par la batterie ; débuter avec une alimentation limitée.
Consigner les besoins d’outillage dans [listeMateriel](../listeMateriel.md).

## Décisions après relevés

| Décision | Valeur / justification |
| --- | --- |
| Fusible Pi : calibre, type, tenue des pointes | À déterminer |
| Fusible moteurs : calibre, type, tenue des pointes | À déterminer |
| Sections et longueurs du faisceau | À déterminer |
| 100 nF aux bornes moteurs | À décider |
| Capacité de réserve supplémentaire | À décider |
| Rappels externes 3,3 V compatibles | À décider |
| PWM et rapport maximal à retenir | À mesurer |
| Gel processus / SIGKILL : besoin de coupure indépendante | À tester |

Enregistrer les essais V03 à V10 dans [Validation](../Validation/README.md).
