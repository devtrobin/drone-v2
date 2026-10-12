# Vérification des sources — Drone V2

Consultation du **11 octobre 2026** pour préparer le logiciel et le câblage.

| Source primaire | Utilisation |
| --- | --- |
| [TI DRV8833][ti] | États des ponts, nSLEEP, PWM et délai de réveil |
| [GPIO Zero, sorties][gpio] | API PWMOutputDevice et DigitalOutputDevice |
| [GPIO Zero, broches][pins] | lgpio réel et broches simulées |
| [Raspberry Pi, caméra][camera] | rpicam, acquisition H.264 et transport réseau |
| [Raspberry Pi, installation][install] | Imager, SSH et préparation du système |
| [FFmpeg, formats][ffmpeg] | Encapsulation MPEG-TS et sorties UDP |

TI : arrêter par nSLEEP bas et commandes à zéro ; PWM sur une entrée, autre entrée basse.
Le réveil exige jusqu’à 1 ms ; délai logiciel initial de 2 ms.
GPIO Zero 2.0.1 est utilisé pour l’essai avec MockPWMPin, sans GPIO physique.
Le pipeline proposé copie le H.264 de rpicam-vid dans MPEG-TS ; aucun réencodage logiciel prévu.
Ces sources ne certifient pas le module DRV8833 du vendeur ni les moteurs du kit.

## Disponibilité du Pi

La [fiche Letmeknow][achat-pi] affiche encore **22,50 € TTC** et **rupture de stock**.
Aucune date de retour vérifiée. Les autres prix et stocks Amazon restent le relevé V5.
Aucun achat effectué ; budget de référence et archive V5 conservés.
La liste n’est pas déclarée intégralement disponible.

[ti]: https://www.ti.com/lit/ds/symlink/drv8833.pdf
[gpio]: https://gpiozero.readthedocs.io/en/stable/api_output.html
[pins]: https://gpiozero.readthedocs.io/en/stable/api_pins.html
[camera]: https://www.raspberrypi.com/documentation/computers/camera_software.html
[install]: https://www.raspberrypi.com/documentation/computers/getting-started.html
[ffmpeg]: https://ffmpeg.org/ffmpeg-formats.html
[achat-pi]: https://letmeknow.fr/fr/cartes-officielles/2497-raspberry-pi-zero-2-w-5056561800004.html
