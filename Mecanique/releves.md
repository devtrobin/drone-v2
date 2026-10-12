# Implantation et relevés — Drone V2

Les STEP des composants sont disponibles ; ce document suit les mesures physiques à effectuer.
Vue de dessus : x vers l’avant, y vers la gauche ; z mesuré depuis le sol.

Les [estimations documentées](estimations.md) servent à préparer la disposition des composants.
Elles sont conservées séparément : releves.json attend toujours des mesures physiques.

## Relever le kit

| Élément | Relevés attendus |
| --- | --- |
| Plaque | Longueur, largeur, épaisseur, repère d’origine |
| Perçages | Coordonnées, diamètres et accès aux écrous |
| Deux moteurs | Fixation, encombrement, polarité et sortie de fils |
| Roues | Diamètre, largeur, entraxe et contact au sol |
| Appui passif | Type livré, position, hauteur et débattement |
| Batterie | Masse, dimensions, ports et maintien |
| Pi et pilote | Masse, encombrement, trous et accès |
| Caméra | Fixations, hauteur, orientation et passage de nappe |

Photographier avec une règle et noter l’instrument. Aucune cote vendeur non vérifiée
ne sert à produire un plan de fixation final.

## Préparer une implantation sur papier

Batterie basse au centre, caméra à l’avant, Pi près de la nappe.
Garder antenne, optique et prises dégagées ; pilote accessible avec passage des fils moteurs.
Vérifier le dégagement sous plaque et le débattement des roues et de l’appui.
Les colliers immobilisent les câbles ; la mousse seule ne valide pas la tenue mécanique.
Choisir supports et visserie après mesures, puis actualiser la liste si des pièces manquent.

## Calculs disponibles

Renseigner [releves.json](releves.json) avec trois contacts au sol et la liste complète
des masses embarquées, chacune avec mass_g et center_mm = [x, y, z].
Inclure plaque, moteurs, roues, batterie, cartes, fils et fixations.
Lancer depuis la racine Drone V2 :

```bash
python3 tools/pre_dimensionnement.py Mecanique/releves.json
```

Sans mesure, l’outil annonce les données manquantes et sort avec le code 2.
Il calcule masse totale, barycentre, marge signée dans le triangle d’appui et seuil idéal
de basculement sous accélération horizontale dans la direction la plus défavorable.
Une marge positive indique uniquement une stabilité statique sur sol horizontal rigide.
Déformation, jeu, glissement, chocs, mouvement de roulette et freinage restent à tester.

Pour l’énergie, renseigner battery_energy_wh, conversion_efficiency entre 0 et 1,
et average_power_5v_w mesurée avec les deux moteurs et la vidéo.
Le calcul est énergie interne × rendement / puissance moyenne, converti en minutes.
Ne pas assimiler 10 000 mAh annoncés à 10 Ah utilisables sous 5 V.
L’autonomie calculée est une estimation ; seul V13 confirme la cible de 15 minutes.
