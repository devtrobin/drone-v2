"""Generate named, coloured STEP assemblies and verify their imported B-reps.

All dimensions are mm. These are documented placement models, not vendor CAD.
Run in the separate CAD venv; no FreeCAD installation or GUI is required.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import tempfile

os.environ.setdefault('XDG_CACHE_HOME', str(Path(tempfile.gettempdir())/'drone-cad-cache'))
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'drone-mpl-cache'))
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
GREEN = (0.10, 0.40, 0.24)
BLACK = (0.13, 0.14, 0.16)
SILVER = (0.65, 0.69, 0.73)
GOLD = (0.85, 0.65, 0.20)
YELLOW = (0.95, 0.75, 0.12)
WHITE = (0.87, 0.87, 0.84)
RED = (0.75, 0.16, 0.12)
BLUE = (0.15, 0.30, 0.60)


def box(l, w, h, p=(0, 0, 0), radius=0):
    result = cq.Workplane('XY').box(l, w, h, centered=False)
    if radius:
        result = result.edges('|Z').fillet(radius)
    return result.val().translate(p)


def cyl(r, h, p=(0, 0, 0), axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*axis))


def ring(ro, ri, h, p=(0, 0, 0), axis=(0, 0, 1)):
    return cyl(ro, h, p, axis).cut(cyl(ri, h, p, axis))


def poly(points, h, z=0):
    return cq.Workplane('XY').polyline(points).close().extrude(h).val().translate((0, 0, z))


class Model:
    def __init__(self, slug, representation):
        self.slug = slug
        self.representation = representation
        self.parts = []
        self.assumptions = []
        self.confirmed = []

    def add(self, name, shape, color=BLACK):
        assert shape.isValid() and shape.Volume() > 0, (self.slug, name)
        self.parts.append((name, shape, color))

    def estimate(self, detail):
        self.assumptions.append(detail)

    def known(self, detail):
        self.confirmed.append(detail)


def pi():
    m = Model('raspberry-pi-zero-2-w', 'Carte nue sans barrette GPIO, connecteurs et puces simplifiés.')
    pcb = box(65, 30, 1, radius=3.5)
    for x in (3.5, 61.5):
        for y in (3.5, 26.5):
            pcb = pcb.cut(cyl(1.375, 1, (x, y, 0)))
    for x in [8.37+2.54*i for i in range(20)]:
        for y in (25.23, 27.77):
            pcb = pcb.cut(cyl(0.5, 1, (x, y, 0)))
            m.add(f'GPIO_pad_{x:.2f}_{y:.2f}', ring(0.85, 0.5, 0.03, (x,y,1)), GOLD)
    m.add('PCB', pcb, GREEN)
    # USB openings face the lower edge of the official top view.
    for label, center in [('micro_USB_data',41.4), ('micro_USB_power',54)]:
        shell = box(8, 5.8, 2.8, (center-4,-0.5,1), radius=0.5)
        shell = shell.cut(box(6.8, 3.2, 1.8, (center-3.4,-0.6,1.5)))
        m.add(label, shell, SILVER)
    hdmi = box(11, 7.5, 4.5, (6.9,-0.5,1), radius=0.6)
    hdmi = hdmi.cut(box(9,4,3,(7.9,-0.6,1.7)))
    m.add('mini_HDMI', hdmi, SILVER)
    sd = box(12, 11, 1.8, (1,11,1))
    sd = sd.cut(box(11,9,1.1,(0.9,12,1.3)))
    m.add('microSD_socket', sd, SILVER)
    m.add('CSI_22_pins',box(3.5,12,2.3,(61.5,8,1)), WHITE)
    m.add('RP3A0',box(15,15,1.6,(20,6,1)), BLACK)
    m.add('shield',box(12,12,1.3,(38,7,1)), SILVER)
    m.known('R1 : PCB 65 × 30 ; centres de fixations (3,5 / 61,5 ; 3,5 / 26,5).')
    m.known('R1 : axes mini-HDMI / USB à x=12,4 / 41,4 / 54 du bord gauche.')
    m.estimate('PCB épaisseur 1,0 ; trous fixation Ø2,75 ; GPIO Ø1 et pas 2,54 : hypothèses.')
    m.estimate('Gabarits connecteurs, puces et placements non cotés estimés du plan / photos.')
    m.estimate('Mini-HDMI à z=5,5 au maximum ; débord au bord y=-0,5 estimé.')
    return m


def camera():
    m = Model('camera-module-3-standard', 'Module Standard, optique et connecteur simplifiés.')
    pcb = box(25,23.862,1.12,radius=1.8)
    for x in (2,23):
        for y in (2,16.5):
            pcb = pcb.cut(cyl(1.1,1.12,(x,y,0)))
    m.add('PCB',pcb,GREEN)
    # Drawing side view: rear plane z=-2.75, front plane z=8.55: 11.3 overall.
    rear=box(19.61,12,2.75,(2.695,10.5,-2.75))
    for x in (2,23):
        rear=rear.cut(cyl(1.1,2.75,(x,16.5,-2.75)))
    m.add('rear_sensor_envelope',rear,BLACK)
    m.add('AF_optical_housing',box(10.8,10.8,5.86,(7.1,11.1,1.12)),BLACK)
    m.add('lens_barrel',ring(2.875,2.375,1.57,(12.5,16.5,6.98)),BLACK)
    m.add('lens_glass',cyl(2.375,0.2,(12.5,16.5,8.35)),BLUE)
    m.add('CSI_15_socket',box(17,3.3,2.4,(4,5.65,1.12)),WHITE)
    m.known('R2 : PCB 25 × 23,862 × 1,12 ; profondeur totale du plan 11,3.')
    m.known('R2 : trous Ø2,2 aux coordonnées x=2 / 23, y=2 / 16,5 ; entraxes 21 × 14,5.')
    m.known('R2 : diamètres optiques 5,75 et 4,75 ; centre optique x=12,5, y=16,5.')
    m.estimate('Carters et arrière optique simplifiés, longueur arrière 12 estimée.')
    m.estimate('Connecteur FFC : volume 17 × 3,3 × 2,4 et placement estimés de la vue.')
    m.estimate('Le product brief arrondit à 24 et 11,5 ; modèle fondé sur le plan Standard R2.')
    return m


def microsd():
    m = Model('microsd-16go', 'Une microSD et son adaptateur SD, présentés côte à côte.')
    card = poly([(0,0),(11,0),(11,12),(9.5,15),(0,15)],1)
    m.add('microSD',card,BLACK)
    for i in range(8):
        m.add(f'microSD_contact_{i+1}',box(.8,3,.03,(1+i*1.2,0,1)),GOLD)
    adapter = poly([(20,0),(44,0),(44,28),(40,32),(20,32)],2.1)
    adapter = adapter.cut(box(11.2,12,1.2,(26,0,0.45)))
    m.add('SD_adapter',adapter,BLACK)
    m.known('Dimensions de format : microSD 11 × 15 × 1 ; SD 24 × 32 × 2,1.')
    m.estimate('Biseaux, contacts, logement et séparation de présentation de 9 mm estimés.')
    return m


def ribbon():
    m = Model('nappe-csi-pi-zero', 'Les deux nappes à plat : 160 et 300 mm, séparées de 30 mm.')
    for length,y in [(160,0),(300,30)]:
        outline=[(0,y),(length-10,y),(length,y+2.25),(length,y+13.75),
                 (length-10,y+16),(0,y+16)]
        m.add(f'FPC_{length}mm',poly(outline,.2),GOLD)
        m.add(f'camera_stiffener_{length}',box(5,16,.08,(0,y,.2)),WHITE)
        m.add(f'pi_stiffener_{length}',box(5,11.5,.08,(length-5,y+2.25,.2)),WHITE)
        for i in range(15):
            m.add(f'camera_contact_{length}_{i}',box(4,.6,.02,(0,y+1+i,.28)),GOLD)
        for i in range(22):
            m.add(f'pi_contact_{length}_{i}',box(4,.3,.02,(length-4,y+2.60+.5*i,.28)),GOLD)
    m.known('A : longueurs commerciales 160 et 300 ; contacts 15 au pas 1 et 22 au pas 0,5.')
    m.estimate('dimensions.json : largeurs 16 / 11,5 ; ruban 0,2 et bouts renforcés 0,3.')
    m.estimate('Longueur des contacts 4, renforts 5 et transition 10 estimées ; cuivre interne omis.')
    return m


def chassis():
    m = Model('chassis-2wd', 'Kit monté provisoirement : plaque, 2 moteurs, roues, appui, boîtier AA.')
    # x=longitudinal, y=transverse, z=vertical; wheel floor at zero.
    outline=[(0,-35),(4,-45),(12,-47),(169,-47),(169,-70),(180,-64),
             (190,-47),(198,-25),(200,0),(198,25),(190,47),(180,64),
             (169,70),(169,47),(12,47),(4,45),(0,35)]
    plate = poly(outline,3,43)
    for x,y,r in [(178,0,9),(98,0,4),(18,-20,1.6),(18,20,1.6),
                  (153,-20,1.6),(153,20,1.6),(50,-37,1.6),(50,37,1.6),
                  (100,-37,1.6),(100,37,1.6),(155,-37,1.6),(155,37,1.6)]:
        plate=plate.cut(cyl(r,3,(x,y,43)))
    for x in (48,115,165):
        for y in (-28,20):
            plate=plate.cut(box(4,8,3,(x,y,43)))
    m.add('acrylic_plate_estimated',plate,(0.65,0.49,0.29))
    for side, sign in [('left',1),('right',-1)]:
        motor=box(70,22,18,(25,44 if sign==1 else -66,23.5),radius=2)
        m.add(f'TT_motor_{side}',motor,YELLOW)
        m.add(f'motor_can_{side}',box(20,18,16,(25,46 if sign==1 else -64,24.5),radius=2),SILVER)
        # Gearmotor body includes metal can visually; can is removed from the gearbox below.
        m.parts[-2]=(m.parts[-2][0],motor.cut(m.parts[-1][1]),YELLOW)
        axis=(0,sign,0)
        m.add(f'TT_shaft_{side}',cyl(2.5,17.5,(55,sign*66,32.5),axis),WHITE)
        base=(55,sign*67.5,32.5)
        tyre=ring(32.5,26,25,base,axis)
        hub=ring(26,2.5,25,base,axis)
        for i in range(5):
            a=2*math.pi*i/5
            hub=hub.cut(cyl(5,25,(55+17*math.cos(a),sign*67.5,32.5+17*math.sin(a)),axis))
        m.add(f'tyre_{side}',tyre,BLACK)
        m.add(f'hub_{side}',hub,YELLOW)
    # 25 mm caster plus estimated 18 mm spacers brings the support to the plate.
    m.add('caster_mount',box(40,32,2,(133,-16,23)),SILVER)
    m.add('caster_pivot',cyl(5,12,(153,0,11)),SILVER)
    for y in (-7,5):
        m.add(f'caster_fork_{y}',box(14,2,15,(146,y,3)),SILVER)
    m.add('caster_wheel',cyl(7,10,(153,-5,7),(0,1,0)),WHITE)
    for x,y in [(140,-10),(166,10)]:
        m.add(f'caster_spacer_{x}',ring(3,1.6,18,(x,y,25)),GOLD)
    # Tray is included in the purchase kit, electrically unused in Drone V2.
    tray=box(63,58,16,(8,-29,46),radius=2)
    tray=tray.cut(box(59,54,14,(10,-27,48)))
    for y in (-14.5,0,14.5):
        tray=tray.fuse(box(59,1,12,(10,y-.5,48)))
    m.add('AA_holder_included_not_used',tray,BLACK)
    m.estimate('dimensions.json : plaque 200 × 140 × 3 ; moteurs 70 × 22 × 18 ; roues Ø65 × 25.')
    m.estimate('Contour plaque et découpes adaptés de vue-01 ; emplacements estimés, pas un gabarit de perçage.')
    m.estimate('Implantation arbitraire : axes roues x=55, y=±80, z=32,5 ; plaque z=43 ; moteur et appui à confirmer.')
    m.estimate('Appui 40 × 32 × 25, roue Ø14 et deux entretoises supposées de 18 entre z=25 et 43.')
    m.estimate('Entretoises et positions à contrôler dans le kit ; aucune stabilité validée par ce modèle.')
    m.estimate('Boîtier AA 63 × 58 × 16 inclus mais inutilisé ; visserie, codeurs et faisceaux omis.')
    m.estimate('Encombrement assemblé 200 × 185 × 65 ; assemblage indicatif, non validé sur matériel.')
    return m


def driver():
    m=Model('drv8833','Un module nu ; barrettes non montées et câblage omis.')
    pcb=box(18.5,16,1.6)
    for x in (1.4,17.1):
        for i in range(6):
            y=1.65+2.54*i
            pcb=pcb.cut(cyl(.5,1.6,(x,y,0)))
            m.add(f'pad_{x}_{i}',ring(.85,.5,.03,(x,y,1.6)),GOLD)
    m.add('PCB',pcb,GREEN)
    m.add('driver_IC',box(5,6.5,1.5,(6.75,4.8,1.6)),BLACK)
    for x in (5.5,11.75):
        for i in range(8):
            m.add(f'IC_pin_{x}_{i}',box(1.25,.35,.4,(x,5+.75*i,1.6)),SILVER)
    m.add('input_capacitor',box(3.5,2.8,3.4,(10,12.2,1.6)),YELLOW)
    for i,(x,y) in enumerate([(4,3),(4,10),(13,2)]):
        m.add(f'SMD_{i}',box(1.5,2,0.8,(x,y,1.6)),WHITE)
    m.add('LED',box(3,1.5,.8,(7,1,1.6)),WHITE)
    m.known('A : PCB 18,5 × 16.')
    m.estimate('dimensions.json : hauteur 5 ; contacts estimés au pas 2,54, trous Ø1.')
    m.estimate('Carte épaisseur 1,6 ; positions et boîtiers composants estimés de vue-03.')
    m.estimate('Trous de contact électriques, aucun trou de fixation mécanique ajouté.')
    return m


def battery():
    m=Model('batterie-usb','Boîtier fermé de batterie USB ; ports et écran indicatifs.')
    body=box(106,68,15,radius=5)
    for y in (8,47):
        body=body.cut(box(5,12,4.5,(-.1,y,5.25)))
        m.add(f'USB_A_tongue_{y}',box(4.7,10,1,(0,y+1,6)),BLACK)
    body=body.cut(box(5,8.4,2.6,(-.1,26,6.2)))
    body=body.cut(box(5,7,1.8,(-.1,36.5,6.6)))
    body=body.cut(cyl(10,.4,(19,34,14.6)))
    m.add('battery_enclosure',body,BLACK)
    m.add('display_window',cyl(9.8,.3,(19,34,14.6)),BLUE)
    m.known('A : 106 × 68 × 15.')
    m.estimate('Rayons 5, écran Ø20 et détails USB / placements estimés des photos ; aucune cellule interne.')
    m.estimate('Dégagement des câbles de 40 mm non inclus dans la géométrie du produit.')
    return m


def cable():
    m=Model('cables-usb','Un câble entier droit, 300 mm de pointe à pointe, embouts inclus.')
    m.add('USB_A_grip',box(18,15,7,(12,-7.5,-3.5),radius=1),BLACK)
    shell=box(12,12,4.5,(0,-6,-2.25)).cut(box(12,10.8,3.3,(0,-5.4,-1.65)))
    m.add('USB_A_shell',shell,SILVER)
    m.add('USB_A_tongue',box(10,10,1,(2,-5,-1.3)),WHITE)
    m.add('cable',cyl(1.75,245,(30,0,0),(1,0,0)),BLACK)
    m.add('micro_USB_grip',box(18,10,5,(275,-5,-2.5),radius=1),BLACK)
    m.add('micro_USB_shell',box(7,6.85,1.8,(293,-3.425,-.9),radius=.3),SILVER)
    m.known('A : longueur commerciale 300.')
    m.estimate('dimensions.json : embouts USB-A 30 × 15 × 7 et micro-B 25 × 10 × 5 ; câble Ø3,5.')
    m.estimate('Longueur 300 interprétée embouts compris : 30 + 245 + 25 ; câble droit, pas de rayon imposé.')
    m.estimate('Embouts et tongues simplifiés ; métal micro-B 6,85 × 1,8 inspiré du catalogue Hirose analogue.')
    return m


def wire():
    m=Model('fil-22awg','Deux échantillons droits de 100 mm : fil rouge et fil noir, extrémités dénudées.')
    for y,c,label in [(0,RED,'red'),(5,BLACK,'black')]:
        m.add(f'insulation_{label}',ring(.85,.3,90,(5,y,0),(1,0,0)),c)
        m.add(f'copper_{label}',cyl(.3,100,(0,y,0),(1,0,0)),GOLD)
    m.known('A : diamètre isolé 1,7 ± 0,1 ; fil 22 AWG, 60 brins de 0,08 annoncés.')
    m.estimate('Échantillons de 100, dénudage 5 de chaque côté : choix de présentation, pas longueur du lot.')
    m.estimate('Cuivre remplacé par cylindre Ø0,6 ; brins non modélisés, pas une preuve de section électrique.')
    return m


def fuse():
    m=Model('fusibles','Un porte-fusible avec deux fils ; un fusible présenté séparément.')
    m.add('holder_body',cyl(6,47,(106.5,0,0),(1,0,0)),BLACK)
    for name,x,length in [('input',0,106.5),('output',153.5,106.5)]:
        m.add(f'holder_wire_{name}',cyl(1.5,length,(x,0,0),(1,0,0)),RED)
    m.add('fuse_glass',ring(2.5,2.1,12,(124,20,0),(1,0,0)),WHITE)
    for x in (120,136):
        m.add(f'fuse_cap_{x}',cyl(2.5,4,(x,20,0),(1,0,0)),SILVER)
    m.add('fuse_link',cyl(.1,12,(124,20,0),(1,0,0)),SILVER)
    m.known('A : cartouche Ø5 × 20 ; corps du porte-fusible 47 ; longueur image 260.')
    m.estimate('dimensions.json : corps Ø12 et fils Ø3 ; chaque fil 106,5 pour total 260.')
    m.estimate('Longueur image 260 retenue malgré texte 270 ; corps intérieur, verrouillage et calibre omis.')
    return m


def ceramic():
    m=Model('ceramique-100nf','Un condensateur radial 100 nF, corps monolithique simplifié.')
    m.add('body',box(5,3,4,(-2.5,-1.5,20),radius=.7),YELLOW)
    for x in (-1.25,1.25):
        m.add(f'lead_{x}',cyl(.25,20,(x,0,0)),SILVER)
    m.estimate('dimensions.json : corps 5 × 4 × 3, pas 2,5, fils Ø0,5 et longueur 20.')
    m.estimate('Axes : largeur x=5, profondeur y=3, hauteur z=4 ; enrobage arrondi, inscription omise.')
    return m


def electrolytics(profile):
    m=Model('electrolytiques','15 valeurs du lot, une pièce par valeur en grille de présentation.')
    for i,(value,voltage,quantity,size) in enumerate(profile['assortment']):
        d,h=[float(s.strip().replace(',','.')) for s in size.split('×')]
        x,y=(i%5)*15,(i//5)*18
        pitch=2 if d<=4 else 2.5 if d<=6 else 3.5
        name=f'{value.replace(",","p")}uF_{voltage}V'
        m.add(f'{name}_body',cyl(d/2,h,(x,y,20)),BLACK)
        m.add(f'{name}_top',cyl(d/2-.2,.08,(x,y,20+h)),SILVER)
        for j in (-1,1):
            m.add(f'{name}_lead_{j}',cyl(.3,20,(x+j*pitch/2,y,0)),SILVER)
    m.known('A : diamètres et hauteurs des 15 valeurs de la table de Sources/fiches-techniques.json.')
    m.estimate('Tous les fils Ø0,6 × 20 ; pas 2 pour Ø4, 2,5 pour Ø5/6, 3,5 pour Ø8 : analogie.')
    m.estimate('Pas 470 µF repris de dimensions.json ; autres pas adaptés des familles radiales Panasonic.')
    m.estimate('Grille 5 × 3 espacée 15 / 18 : présentation du lot ; quantités réelles non dupliquées.')
    return m


def resistors():
    m=Model('resistances','Deux résistances axiales : 1 kΩ et 10 kΩ, même encombrement représentatif.')
    for y,label in [(0,'1kOhm'),(8,'10kOhm')]:
        m.add(f'{label}_body',cyl(1.2,6,(27,y,0),(1,0,0)),BLUE)
        for x in (0,33):
            m.add(f'{label}_lead_{x}',cyl(.275,27,(x,y,0),(1,0,0)),SILVER)
    m.known('A : corps longueur 6, fils longueur 27 de chaque côté ; format 1/4 W.')
    m.estimate('dimensions.json : corps Ø2,4, fil Ø0,55 ; bagues et autres valeurs du lot omises.')
    return m


def shrink():
    m=Model('gaine','Un tronçon pour chacun des 8 diamètres, avant rétreint, côte à côte.')
    y=0
    for d in (2,2.5,3.5,5,6,8,10,13):
        length=40 if d<=3.5 else 80
        m.add(f'tube_ID_{str(d).replace(".","p")}mm',ring(d/2+.2,d/2,length,(0,y,0),(1,0,0)),BLACK)
        y+=d+5
    m.known('A : diamètres intérieurs avant rétreint 2 / 2,5 / 3,5 / 5 / 6 / 8 / 10 / 13 ; ratio 2:1.')
    m.estimate('dimensions.json : paroi 0,2 avant rétreint ; longueurs 40 petits / 80 grands de la matrice vendeur.')
    m.estimate('Tronçons circulaires droits, non rétreints ; espacements de présentation, aucun lot complet.')
    return m


def tie():
    m=Model('colliers','Un collier non fermé, déployé à plat, longueur totale 150.')
    head=box(5,4,3,(0,-2,0),radius=.5)
    head=head.cut(box(5.2,2.6,1.2,(-.1,-1.3,.8)))
    m.add('locking_head',head,BLACK)
    tail=poly([(5,-1.25),(143,-1.25),(150,0),(143,1.25),(5,1.25)],1)
    m.add('nylon_band',tail,BLACK)
    m.known('A : longueur 150, largeur ruban 2,5.')
    m.estimate('dimensions.json : ruban épaisseur 1 ; tête 5 × 4 × 3.')
    m.estimate('Ouverture tête 2,6 × 1,2, pointe 7, longueur incluant tête : hypothèses ; denture omise.')
    return m


def foam():
    m=Model('mousse','Rouleau de fourniture et un échantillon de mousse de 50 mm, séparés.')
    m.add('foam_roll_envelope',ring(82.5,17.5,12),WHITE)
    m.add('50mm_cut_sample',box(50,12,2,(95,-6,0)),WHITE)
    m.known('A : bande largeur 12, épaisseur 2, longueur commerciale 10 m.')
    m.estimate('dimensions.json : rouleau Ø165, trou central Ø35 ; liner et spirale omis.')
    m.estimate('Rouleau représenté comme enveloppe annulaire, pas comme volume de matière mesuré.')
    m.estimate('Échantillon 50 : choix de présentation / fixation provisoire, pas cote du produit vendu.')
    return m


def adapter():
    m=Model('adaptateur-usb','Un adaptateur USB-C mâle vers USB-A femelle, corps et ports simplifiés.')
    body=box(17.5,14,7,(0,-7,-3.5),radius=1.5)
    body=body.cut(box(7,12,4.5,(-.1,-6,-2.25)))
    m.add('adapter_body',body,SILVER)
    m.add('USB_A_tongue',box(5,10,1,(.5,-5,-1.4)),BLACK)
    shell=box(7.5,8.4,2.6,(17.5,-4.2,-1.3),radius=1.1)
    shell=shell.cut(box(7.5,7.4,1.6,(17.5,-3.7,-.8),radius=.6))
    m.add('USB_C_shell',shell,SILVER)
    m.estimate('dimensions.json : enveloppe totale estimée 25 × 14 × 7, USB-C compris.')
    m.estimate('Projection USB-C 7,5 ; sections ports et profondeurs estimées ; pas de détail électrique.')
    return m


def solder():
    m=Model('fil-a-souder','Bobine représentative et un échantillon droit de fil à souder de 50 mm.')
    m.add('spool_lower_flange',ring(30,6,1.5),BLACK)
    m.add('spool_hub',ring(12,6,12,(0,0,1.5)),BLACK)
    m.add('spool_upper_flange',ring(30,6,1.5,(0,0,13.5)),BLACK)
    m.add('wound_solder_envelope',ring(25,12,11,(0,0,2)),SILVER)
    m.add('wire_sample',cyl(.3,50,(40,0,0),(1,0,0)),SILVER)
    m.known('A : fil diamètre 0,6 et lot de 20 g ; dimensions colis exclues.')
    m.estimate('dimensions.json : bobine Ø60 et largeur 15 ; moyeu Ø24, trou Ø12 et flasques 1,5 estimés.')
    m.estimate('Volume bobiné est une enveloppe, pas 20 g de métal ; noyau flux et spires omis.')
    m.estimate('Échantillon 50 : choix de présentation, sans lien avec longueur totale du lot.')
    return m


def reader():
    m=Model('lecteur-microsd','Lecteur USB-C et adaptateur USB-A du lot, côte à côte ; lien omis.')
    # Infographic view ambiguously bounds the full reader. Choose inclusive 23.4 conservatively.
    body=box(16.4,16.2,10.3,(0,-8.1,-5.15),radius=2)
    body=body.cut(box(9,11.2,1.2,(-.1,-5.6,-.6)))
    m.add('reader_body',body,SILVER)
    m.add('reader_USB_C',box(7,8.4,2.6,(16.4,-4.2,-1.3),radius=1.1),SILVER)
    adapt=box(15,16,8,(0,21,-4),radius=1.5)
    adapt=adapt.cut(box(6,8.4,2.6,(-.1,24.8,-1.3)))
    m.add('USB_A_adapter_body',adapt,SILVER)
    shell=box(12,12,4.5,(15,23,-2.25)).cut(box(12,10.8,3.3,(15,23.6,-1.65)))
    m.add('USB_A_adapter_shell',shell,SILVER)
    m.known('A vue-07 : lecteur annoncé 23,4 × 16,2 × 10,3, périmètre de cote non explicite.')
    m.estimate('23,4 interprété connecteur compris : corps 16,4 + USB-C 7 ; hypothèse à contrôler.')
    m.estimate('dimensions.json : adaptateur 27 × 16 × 8, métal inclus ; port et logement estimés.')
    m.estimate('Lanière omise car souple et hors implantation embarquée ; accessoires non embarqués.')
    return m


BUILDERS=[pi,camera,microsd,ribbon,chassis,driver,battery,cable,wire,fuse,ceramic,
          electrolytics,resistors,shrink,tie,foam,adapter,solder,reader]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bbox(shape):
    b=shape.BoundingBox()
    return {'min_mm':[b.xmin,b.ymin,b.zmin], 'max_mm':[b.xmax,b.ymax,b.zmax],
            'size_mm':[b.xlen,b.ylen,b.zlen]}


def preview(m, path):
    """Orthographic software rasterizer with per-pixel depth; no GPU/display needed."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    from matplotlib.font_manager import findfont
    width,height=1200,850
    rgb=np.full((height,width,3),255,dtype=np.uint8)
    zbuffer=np.full((height,width),-np.inf)
    az,el=math.radians(-60),math.radians(28)
    view=np.array([math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)])
    right=np.array([-math.sin(az),math.cos(az),0])
    up=np.cross(view,right)
    basis=np.array([right,-up,view]).T
    meshes=[]
    all_projected=[]
    for _,shape,color in m.parts:
        vertices,triangles=shape.tessellate(.12,.12)
        world=np.array([v.toTuple() for v in vertices])
        projected=world@basis
        meshes.append((world,projected,triangles,np.array(color)))
        all_projected.append(projected)
    points=np.vstack(all_projected)
    low,high=points[:,:2].min(axis=0),points[:,:2].max(axis=0)
    scale=min((width-140)/max(high[0]-low[0],.1),
              (height-200)/max(high[1]-low[1],.1))
    midpoint=(high+low)/2
    light=np.array([.3,-.45,.84]); light/=np.linalg.norm(light)
    for world,projected,triangles,color in meshes:
        screen=projected.copy()
        screen[:,:2]=(screen[:,:2]-midpoint)*scale+np.array([width/2,height/2])
        for t in triangles:
            a,b,c=screen[list(t)]
            den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-8:
                continue
            x0=max(0,int(math.floor(min(a[0],b[0],c[0]))))
            x1=min(width-1,int(math.ceil(max(a[0],b[0],c[0]))))
            y0=max(60,int(math.floor(min(a[1],b[1],c[1]))))
            y1=min(height-60,int(math.ceil(max(a[1],b[1],c[1]))))
            if x1<x0 or y1<y0:
                continue
            xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
            u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
            w=1-u-v
            depth=u*a[2]+v*b[2]+w*c[2]
            old=zbuffer[y0:y1+1,x0:x1+1]
            mask=(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)&(depth>old)
            normal=np.cross(world[t[1]]-world[t[0]],world[t[2]]-world[t[0]])
            norm=np.linalg.norm(normal)
            shade=.62+.38*abs(np.dot(normal/norm,light)) if norm else 1
            rgb[y0:y1+1,x0:x1+1][mask]=np.clip(color*shade*255,0,255).astype(np.uint8)
            old[mask]=depth[mask]
    result=Image.fromarray(rgb)
    draw=ImageDraw.Draw(result)
    font_file=findfont('DejaVu Sans')
    draw.text((width/2,24),m.slug+' — STEP / mm',anchor='mt',
              font=ImageFont.truetype(font_file,27),fill='#111111')
    draw.text((width/2,height-35),
              'Modèle simplifié • cotes estimées à confirmer sur le matériel',
              anchor='mm',font=ImageFont.truetype(font_file,20),fill='#555555')
    result.save(path)


def generate(render=True):
    profiles=json.loads((ROOT/'Sources/fiches-techniques.json').read_text())['profiles']
    records=[]
    for builder in BUILDERS:
        m=builder(profiles['electrolytiques']) if builder is electrolytics else builder()
        folder=ROOT/'Composants'/m.slug
        step=folder/(m.slug+'.step')
        a=cq.Assembly(name=m.slug)
        for name,shape,color in m.parts:
            a.add(shape,name=name,color=cq.Color(*color))
        a.export(str(step),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
        original=cq.Compound.makeCompound([s for _,s,_ in m.parts])
        imported=cq.importers.importStep(str(step)).val()
        assert imported.isValid(), m.slug
        solids=imported.Solids()
        assert solids and all(s.isValid() and s.Volume()>0 for s in solids),m.slug
        assert len(solids)==len(original.Solids()),m.slug
        volume_error=abs(imported.Volume()-original.Volume())/original.Volume()
        assert volume_error<1e-7,(m.slug,volume_error)
        bb0,bb1=bbox(original),bbox(imported)
        bbox_error=max(abs(x-y) for key in ('min_mm','max_mm')
                       for x,y in zip(bb0[key],bb1[key]))
        assert bbox_error<1e-5,(m.slug,bbox_error)
        text=step.read_text()
        assert text.startswith('ISO-10303-21;') and text.rstrip().endswith('END-ISO-10303-21;')
        assert "SI_UNIT(.MILLI.,.METRE.)" in text,m.slug
        if render:
            preview(m,folder/'modele-3d.png')
        sources=[{'file':str(p.relative_to(ROOT)), 'sha256':digest(p)} for p in
                 [folder/'dimensions.json',folder/'documentation.json',
                  ROOT/'Sources/fiches-techniques.json',Path(__file__)]]
        sources += [{'file':str(p.relative_to(ROOT)), 'sha256':digest(p)}
                    for p in sorted((folder/'photos').glob('*.jpg'))]
        sources += [{'file':str(p.relative_to(ROOT)), 'sha256':digest(p)}
                    for p in sorted((folder/'notices').glob('*.pdf'))]
        metadata={
            'slug':m.slug,'generated_on':'2026-10-11','unit':'mm',
            'format':'STEP assemblage avec noms et couleurs / OpenCascade',
            'file':str(step.relative_to(ROOT)), 'sha256':digest(step),
            'generator':'tools/generate_component_step.py','cadquery_version':cq.__version__,
            'hardware_measured':False,'vendor_native_cad':False,
            'use':'implantation provisoire ; confirmer sur matériel avant fabrication',
            'representation':m.representation,'documented_dimensions':m.confirmed,
            'additional_assumptions':m.assumptions,'sources':sources,
            'online_sources':profiles[m.slug]['sources']+
                [[s['code'],s['label'],s['url']] for s in
                 json.loads((folder/'dimensions.json').read_text())['comparison_sources']],
            'parts':[{'name':name,'bbox':bbox(shape),'solids':len(shape.Solids())}
                     for name,shape,_ in m.parts],
            'assembly_bbox':bb1,
            'presentation_offsets_are_product_dimensions':False,
            'validation':{'reimport_valid':True,'all_solids_valid':True,
                          'solids':len(solids),'named_parts':len(m.parts),
                          'relative_volume_error':volume_error,'bbox_error_mm':bbox_error}
        }
        if render:
            p=folder/'modele-3d.png'
            metadata['preview']={'file':str(p.relative_to(ROOT)),'sha256':digest(p)}
        (folder/'modele-3d.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
        records.append({'slug':m.slug,'file':metadata['file'],'sha256':metadata['sha256'],
                        'metadata_file':str((folder/'modele-3d.json').relative_to(ROOT)),
                        'validation':metadata['validation']})
        print(f'{m.slug}: {len(solids)} solides valides, STEP réimporté.',flush=True)
    report={'generated_on':'2026-10-11','unit':'mm','models':records,
            'count':len(records),'hardware_measured':False,
            'checks':'B-rep valide, solides positifs, nombre, volume, bbox, unité millimètre après réimport',
            'visual_review':{'status':'à vérifier','count':0}}
    (ROOT/'Validation/resultats/modeles-step.json').write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-preview',action='store_true')
    args=parser.parse_args()
    generate(not args.no_preview)
