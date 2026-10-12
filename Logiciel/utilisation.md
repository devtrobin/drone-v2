# Utilisation — Drone V2


Commandes à lancer depuis Logiciel. Remplacer les IP d’exemple par celles du Mac et du Pi.

## Simulation sur le Mac

Créer la clé une seule fois, puis démarrer :

```bash
python3 -m drone.server --key-file secrets/control.key --create-key
python3 -m drone.server --key-file secrets/control.key
```

Dans un second terminal au même emplacement :

```bash
python3 -m drone.pilot --key-file secrets/control.key
```

Cliquer Connecter. Maintenir Espace et une flèche ; relâcher Espace demande l’arrêt.
Up avance, Down recule, Right tourne à droite, Left tourne à gauche.
Échap, perte de focus, bouton d’arrêt et fermeture de fenêtre arrêtent la commande.
Le terminal serveur montre les sorties simulées. Ctrl+C ferme le serveur.
Après une perte de liaison, reprendre avec Connecter ; aucun mouvement mémorisé n’est repris.

## Premier essai GPIO sur le Pi

Terminer les relevés du module, les contrôles de faisceau et le dimensionnement des branches.
Commencer roues levées et sous limitation de courant. Dans config/robot.local.json,
vérifier GPIO, inversion de chaque moteur et limite de puissance.
Passer hardware_confirmed à true seulement après ces contrôles documentés.

Sur le Pi, remplacer 192.168.1.20 par son IP locale :

```bash
python3 -m drone.server --host 192.168.1.20 --key-file secrets/control.key \
  --config config/robot.local.json --hardware
```

Sur le Mac, avec la même clé :

```bash
python3 -m drone.pilot --host 192.168.1.20 --key-file secrets/control.key
```

Autoriser l’accès local à TCP 8765 ; aucun transfert de port Internet.
Par défaut : écoute 127.0.0.1 et simulation si --hardware est absent.
Pour inverser une roue, arrêter, modifier invert_left ou invert_right, puis tester roue levée.
Les valeurs sont des rapports PWM ; aucune vitesse de roue mesurée.

## Vidéo indépendante

Sur le Mac, afficher les arguments, puis lancer ffplay :

```bash
python3 -m drone.video view
python3 -m drone.video view --run
```

Sur le Pi, remplacer 192.168.1.10 par l’IP du Mac :

```bash
python3 -m drone.video stream --host 192.168.1.10
python3 -m drone.video stream --host 192.168.1.10 --run
```

Sans --run, le lanceur affiche seulement la commande.
Les deux processus vidéo restent séparés du serveur moteur ; Ctrl+C termine la chaîne vidéo.
Le Mac accepte UDP 5000 depuis le Pi. Aucun audio ni enregistrement.
Paramètres initiaux : 720p30, 2 Mbit/s, autofocus continu ; qualité et latence à mesurer.

## Dépannage

| Symptôme | Premier contrôle |
| --- | --- |
| Connexion refusée | IP Pi, serveur, réseau local, port TCP 8765 |
| Authentification invalide | Même clé copiée par SSH, sans l’imprimer |
| GPIO refusés | Configuration confirmée, lgpio, accès utilisateur |
| Caméra absente | Modèle, nappe 15/22 broches, verrouillage hors tension |
| Image absente | IP Mac destinataire, ffplay, UDP 5000 |
| Reset avec moteurs | Tension au Pi, pointes, faisceau et fusibles |
| Arrêts intempestifs | RTT réseau, charge CPU et régularité des commandes |

Consigner commandes, versions et mesures dans le [modèle de résultat](../Validation/modele.md).
