# Archive — évolution moteurs et puissance

> Étude reportée, hors version active ; voir le [statut de l’archive][statut-archive].

**Étude reportée le 12 octobre 2026 à la demande de l'utilisateur**, en raison du coût. Elle n'est
pas la conception active et ses composants ne sont pas à acheter pour la V2 actuelle.

La [version active](../../ReadMe.md) revient aux moteurs TT et à la batterie USB 5 V, avec une
vitesse maximale estimée d'environ 2,2 km/h et un budget prévisionnel de 257,03 € hors port.

## Contenu conservé pour une reprise ultérieure

- [Panier proposé](listeAchat.md) et [données d'achat](achats.json), total 508,07 € historique.
- [Architecture](architecture.md) et [spécifications](SPECIFICATIONS.md) de la version rapide.
- [Circuit LiPo 3S / MD13S](Electronique/puissance.md) et réserves électriques.
- [Calculs et hypothèses](Mecanique/performance-puissance.md), objectifs 6–8 km/h.
- [Guide logiciel](Logiciel/puissance.md), profils, sources Python et tests de cette étude.
- Dossiers des 12 nouveaux composants avec prix, sources et réserves.
- [Résultats de contrôle](Validation/resultats/logiciel-puissance.json) obtenus avant le retour.
- [Inventaire](inventaire.json) des fichiers sauvegardés et de leurs empreintes.

Les liens Markdown ont été réorientés vers l'archive ou les documents conservés dans la base. Les
JSON, les sources de calcul et le code ont été sauvegardés sans modification. Les résultats
restent historiques ; ils ne constituent pas les tests du projet actif après retour.

L'archive est documentaire : tous les fichiers du projet V5 ne sont pas recopiés. Le vérificateur
check_project.py conservé ici est une capture de l'ancienne logique ; exécuter celui du dossier
tools de la version active. Aucun nouveau PDF ou STEP n'avait été généré pour ces composants.

Avant reprise, revalider budget, annonces, identité des pilotes, fusibles DC, géométrie et
protections de décharge. La sauvegarde ne lève aucune réserve matérielle de l'étude.

[statut-archive]: README.md
