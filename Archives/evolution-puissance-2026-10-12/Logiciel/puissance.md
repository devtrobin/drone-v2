# Profil de commande — deux MD13S

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

Le nouveau pilote PWM/DIR est sélectionné par driver = md13s. Le [profil d'exemple][profil]
conserve hardware_confirmed = false. Aucun test sur GPIO physique, moteur ou caméra réalisé.

## Simulation de la révision puissance

Après préparation Python et clé suivant l'[installation][archive-lien-1], depuis Logiciel :

```bash
python3 -m drone.server --key-file secrets/control.key   --config
config/robot.puissance.example.json
python3 -m drone.pilot --key-file secrets/control.key
```

Ces deux processus se lancent dans des terminaux distincts. Sans --hardware, seules les sorties
simulées sont utilisées. Le serveur garde le profil DRV8833 si --config est absent.

## Préparer le Pi réel

```bash
cp config/robot.puissance.example.json config/robot.local.json
```

Ne passer hardware_confirmed à true qu'après identification du MD13S et contrôles du
[circuit][circuit]. Le guide d'installation commun mentionne aussi le profil DRV8833 historique :
le présent choix de profil s'applique à la révision puissance.

| Paramètre initial | Valeur / rôle |
| --- | --- |
| driver | md13s, deux modules monocanal |
| max_duty | 0,25 pour mise au point |
| max_turn_duty | 0,08, rotation séparément limitée |
| ramp_per_s | 0,30 de PWM par seconde |
| command_timeout_s | 0,30 s |
| reverse_pause_s | 0,15 s |
| pwm_hz | 100 Hz, à contrôler au banc |

La rampe limite l'écart de commande par temps écoulé, plafonné à 100 ms pour éviter un saut après
retard. L'arrêt demandé reste immédiat, sans rampe de freinage. La pause d'inversion empêche une
inversion instantanée après une commande non nulle.

Le mixage diminue l'avance en virage et le terme de rotation en déplacement. Pas de mesure de
vitesse ou de courant : ces limites PWM ne garantissent ni accélération ni vitesse réelle. Si 8 %
ne suffit pas à démarrer une rotation régulière, mesurer avant augmentation.

Après validation électrique, mécanique et thermique, augmenter progressivement max_duty dans le
profil local. Les prévisions 6,4–7,7 km/h supposent 0,95 ; ne pas confondre cette valeur cible
avec les 0,25 livrés pour essais. Ne pas désactiver la limite de rotation pour chercher la vitesse
en ligne droite.

## Arrêt et limitations

PWM = 0 correspond au freinage sur MD13S ; aucune entrée nSLEEP n'est utilisée. Les quatre signaux
ont des rappels externes à GND. La protection contre commande absente et déconnexion reste
logicielle ; gel du Pi ou SIGKILL peut laisser une sortie active. Tester et prévoir coupure
indépendante avant usage rapide.

Les tests sur MockFactory couvrent PWM/DIR, arrêt, inversion, démarrage progressif et virages ;
les tests TCP existants couvrent le protocole. Ils ne prouvent ni fonctionnement d'une carte
Generchin, ni freinage réel, ni stabilité. Le pipeline vidéo commun reste inchangé.

[profil]: config/robot.puissance.example.json
[circuit]: ../Electronique/puissance.md

[archive-lien-1]: installation.md

[statut-archive]: ../README.md
