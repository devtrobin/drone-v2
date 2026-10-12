"""Build the Drone V2 placement assembly from the actual component STEP files.

Outputs a robot, a workshop view covering all 19 purchase lots, geometry checks,
placements, views and an explicit list of extra fixtures. No physical measures.
"""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import math
import os
import tempfile
import argparse

os.environ.setdefault('XDG_CACHE_HOME', str(Path(tempfile.gettempdir())/'drone-cad-cache'))
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'drone-mpl-cache'))
import cadquery as cq
import generate_component_step as cad
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Assemblage'
PURPLE=(.40,.36,.58)


def write_json(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def unit(v):
    length=math.sqrt(sum(x*x for x in v))
    return tuple(x/length for x in v)


def path_length(points):
    return sum(math.dist(a,b) for a,b in zip(points,points[1:]))


def exact_bbox(shape):
    """Ignore cached preview triangulations when comparing STEP geometry bounds."""
    bounds=Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped,bounds,False,False)
    values=bounds.Get()
    return {'min_mm':list(values[:3]),'max_mm':list(values[3:]),
            'size_mm':[b-a for a,b in zip(values[:3],values[3:])]}


def render_view(model,path,direction):
    target=cq.Vector(math.cos(math.radians(28))*.5,
                     -math.cos(math.radians(28))*math.sqrt(3)/2,
                     math.sin(math.radians(28)))
    origin=cq.Vector(*direction).normalized()
    axis=origin.cross(target).normalized()
    angle=math.degrees(math.acos(origin.dot(target)))
    original_up=cq.Vector(0,1,0) if direction[2] else cq.Vector(0,0,1)
    radians=math.radians(angle)
    rotated_up=(original_up.multiply(math.cos(radians))
                +axis.cross(original_up).multiply(math.sin(radians))
                +axis.multiply(axis.dot(original_up)*(1-math.cos(radians))))
    screen_up=target.cross(cq.Vector(math.sqrt(3)/2,.5,0))
    roll=math.degrees(math.atan2(target.dot(rotated_up.cross(screen_up)),
                                rotated_up.dot(screen_up)))
    view=cad.Model(path.stem,'Vue orthographique de l’assemblage.')
    view.parts=[(n,s.rotate((0,0,0),axis.toTuple(),angle)
                  .rotate((0,0,0),target.toTuple(),roll),c) for n,s,c in model.parts]
    cad.preview(view,path)


def routed_wire(points,radius):
    pieces=[]
    for a,b in zip(points,points[1:]):
        pieces.append(cad.cyl(radius,math.dist(a,b),a,unit(tuple(y-x for x,y in zip(a,b)))))
    for p in points[1:-1]:
        pieces.append(cq.Solid.makeSphere(radius,cq.Vector(*p),angleDegrees1=-90))
    shape=(pieces[0].fuse(*pieces[1:]) if len(pieces)>1 else pieces[0]).clean()
    assert shape.isValid() and len(shape.Solids())==1
    return shape


def ribbon_shape(points):
    """Piecewise placement envelope; parallel sections within each folded segment.

    A single loft around the whole loop can create a hollow enclosing solid.
    Segment lofts preserve the ribbon thickness and expose each bend approximation.
    """
    pieces=[]
    distance=0
    for a,b in zip(points,points[1:]):
        length=math.dist(a,b)
        tangent=cq.Vector(*unit(tuple(y-x for x,y in zip(a,b))))
        width_axis=cq.Vector(0,1,0)
        thickness_axis=tangent.cross(width_axis).normalized()
        wires=[]
        for p,d in [(a,distance),(b,distance+length)]:
            width=11.5+4.5*min(d/12,1)
            center=cq.Vector(*p)
            vertices=[center+width_axis.multiply(sign*width/2)
                      +thickness_axis.multiply(side*.1)
                      for sign,side in [(-1,-1),(1,-1),(1,1),(-1,1)]]
            wires.append(cq.Wire.makePolygon(vertices,close=True))
        segment=cq.Solid.makeLoft(wires,ruled=True)
        assert segment.isValid() and segment.Volume()>0
        pieces.append(segment)
        distance+=length
    result=cq.Compound.makeCompound(pieces)
    assert result.isValid() and 100<result.Volume()<700,result.Volume()
    return result


class Robot:
    def __init__(self):
        self.model=cad.Model('drone-v2','Implantation provisoire du robot roulant.')
        self.sources={}
        self.placements=[]
        self.routes=[]
        self.drilling=[]
        self.adaptations=[]
        self.kinds={}
        self.source_cache={}

    def load(self,slug):
        if slug not in self.source_cache:
            path=ROOT/'Composants'/slug/(slug+'.step')
            meta=ROOT/'Composants'/slug/'modele-3d.json'
            self.sources[slug]={'file':str(path.relative_to(ROOT)), 'sha256':cad.digest(path),
                                'metadata_file':str(meta.relative_to(ROOT)),
                                'metadata_sha256':cad.digest(meta)}
            assembly=cq.Assembly.load(str(path))
            parts={}
            for shape,name,loc,color in assembly:
                parts[name.rsplit('/',1)[-1]]=(shape.moved(loc),
                                             color.toTuple()[:3] if color else cad.BLACK)
            expected={p['name'] for p in json.loads(meta.read_text())['parts']}
            assert set(parts)==expected,(slug,set(parts)^expected)
            self.source_cache[slug]=parts
        return self.source_cache[slug]

    def add(self,group,name,shape,color,kind='rigid'):
        key=group+'__'+name
        self.model.add(key,shape,color)
        self.kinds[key]=kind

    def place(self,slug,group,translation=(0,0,0),rotation=None,names=None,omit=()):
        parts=self.load(slug)
        selected=names if names is not None else [n for n in parts if n not in omit]
        for name in selected:
            shape,color=parts[name]
            if rotation:
                shape=shape.rotate((0,0,0),rotation[0],rotation[1])
            self.add(group,name,shape.translate(translation),color)
        self.placements.append({'source_slug':slug,'group':group,
                                'selected_parts':list(selected),'translation_mm':list(translation),
                                'rotation_axis_degrees':rotation})

    def route(self,name,points,radius,color,source_slug,net='illustratif'):
        self.load(source_slug)
        self.add('FAISCEAU',name,routed_wire(points,radius),color,'wire')
        self.routes.append({'name':name,'source_slug':source_slug,'net':net,
                            'diameter_mm':radius*2,'points_mm':points,
                            'polyline_length_mm':path_length(points),
                            'status':'cheminement indicatif, broches et longueurs à confirmer'})

    def hole(self,x,y,d,reason):
        self.drilling.append({'center_xy_mm':[x,y],'diameter_mm':d,'reason':reason,
                              'physically_measured':False,'drill_template_validated':False})

    def vertical_bolt(self,group,label,x,y,bottom,top,diameter,head_r=2.5):
        self.add(group,label+'_shaft',cad.cyl(diameter/2,top-bottom,(x,y,bottom)),cad.SILVER)
        self.add(group,label+'_head',cad.cyl(head_r,1.8,(x,y,top)),cad.SILVER)
        self.add(group,label+'_nut',cad.ring(head_r,diameter/2+.1,2,(x,y,bottom)),cad.SILVER)


def build_robot():
    r=Robot()
    # Kit AA tray is not needed with a USB battery.
    r.place('chassis-2wd','CHASSIS',omit=('AA_holder_included_not_used',))
    r.place('batterie-usb','BATTERIE',(5,-34,48),omit=('USB_A_tongue_8',))
    r.place('raspberry-pi-zero-2-w','PI',(121,-44,52),omit=('microSD_socket','micro_USB_power'))
    # Retain external dimensions; reopen simplified socket volumes for inserted accessories.
    sd=cad.box(12,12,1.8,(122,-33,53))
    sd=sd.cut(cad.box(12.2,11.2,1.2,(121.9,-32.6,53.3)))
    r.add('PI','microSD_socket_assembly_envelope',sd,cad.SILVER)
    port=cad.box(8,5.8,2.8,(171,-44.5,53),radius=.5)
    port=port.cut(cad.box(7.2,3.2,2,(171.4,-44.6,53.4)))
    r.add('PI','micro_USB_power_assembly_envelope',port,cad.SILVER)
    sd_names=[n for n in r.load('microsd-16go') if n!='SD_adapter']
    r.place('microsd-16go','MICROSD',(118,-21.5,53.3),((0,0,1),-90),sd_names)
    r.place('drv8833','DRV8833',(132,23,51))
    r.place('camera-module-3-standard','CAMERA',(186,-12.5,60),((1,1,1),120))
    r.adaptations += [
        'Boîtier AA retiré du robot et montré à côté dans la vue atelier.',
        'Logements microSD et PWR IN du Pi rouverts dans le gabarit assemblé pour représenter les insertions.',
        'Languette interne USB-A batterie utilisée omise ; contacts USB non modélisés comme accouplement précis.',
        'Plaque du kit percée virtuellement pour les fixations proposées ; positions à confirmer, pas gabarit de perçage.'
    ]
    # Two short foam pads selected from the roll; no spool carried onboard.
    r.load('mousse')
    for i,p in enumerate([(15,-25,46),(60,13,46)]):
        r.add('MOUSSE',f'pad_battery_{i}',cad.box(50,12,2,p),cad.WHITE)
    r.add('MOUSSE','pad_driver',cad.box(16,12,2,(133.25,25,49)),cad.WHITE)
    # Extra fittings, clearly distinguished from purchased components.
    for i,(x,y) in enumerate([(124.5,-40.5),(182.5,-40.5),(124.5,-17.5),(182.5,-17.5)]):
        r.add('AJOUT_PI',f'nylon_spacer_{i}',cad.ring(2.5,1.35,6,(x,y,46)),PURPLE)
        r.hole(x,y,2.7,'Fixation Pi proposée')
        r.vertical_bolt('AJOUT_PI',str(i),x,y,41,53,2.5,2.2)
    carrier=cad.box(26,24,3,(128,19,46),radius=1)
    for x,y in [(130,21),(152,41)]:
        carrier=carrier.cut(cad.cyl(1.7,3,(x,y,46)))
        r.hole(x,y,3.4,'Porte-module DRV8833 proposé')
        r.vertical_bolt('AJOUT_DRV',f'{x}',x,y,41,49,3)
    r.add('AJOUT_DRV','isolating_carrier',carrier,PURPLE)
    foot=cad.box(14,36,2,(166,-18,46))
    for x,y in [(170,-14),(170,14)]:
        foot=foot.cut(cad.cyl(1.7,2,(x,y,46)))
        r.hole(x,y,3.4,'Pied du support caméra proposé')
        r.vertical_bolt('AJOUT_CAMERA',f'base_{y}',x,y,40,48,3)
    # Keep the upright out of the Pi board at y=-14.
    back=cad.box(2,28,40,(178,-14,48))
    back=back.cut(cad.box(2.2,18,26,(177.9,-9,64)))
    for y in (-10.5,10.5):
        back=back.cut(cad.cyl(1.1,2,(178,y,62),(1,0,0)))
        r.add('AJOUT_CAMERA',f'spacer_{y}',cad.ring(2,1.1,6,(180,y,62),(1,0,0)),PURPLE)
        r.add('AJOUT_CAMERA',f'M2_shaft_{y}',cad.cyl(1,10.62,(176.5,y,62),(1,0,0)),cad.SILVER)
        r.add('AJOUT_CAMERA',f'M2_head_{y}',cad.cyl(1.6,1.2,(187.12,y,62),(1,0,0)),cad.SILVER)
        r.add('AJOUT_CAMERA',f'M2_nut_{y}',cad.ring(1.9,1.1,1.5,(176.5,y,62),(1,0,0)),cad.SILVER)
    foot=foot.cut(cad.cyl(2.7,2,(166,10,46)))
    r.add('AJOUT_CAMERA','camera_bracket',foot.fuse(back).clean(),PURPLE)
    # Battery loops are NEW long straps; the listed 150 mm ties do not fit the battery.
    for x in (31,85):
        outer=cad.box(10,72,22.4,(x,-36,41.8))
        inner=cad.box(10,70,20.4,(x,-35,42.8))
        r.add('AJOUT_BATTERIE',f'long_strap_{x}',outer.cut(inner),cad.BLACK)
    # Estimated included motor clamps; attach through a wide inner flange.
    for sign in (-1,1):
        mount=cad.box(10,29,1.5,(70,38,41.5))
        mount=mount.fuse(cad.box(10,1,18.5,(70,43,23)),
                         cad.box(10,1,18.5,(70,66,23)),
                         cad.box(10,24,.5,(70,43,23))).clean()
        for x in (72.5,77.5):
            mount=mount.cut(cad.cyl(1.6,2,(x,40,41.4)))
            r.hole(x,sign*40,3.2,'Fixation moteur du kit supposée')
            r.vertical_bolt('KIT_FIXATIONS',f'motor_{sign}_{x}',x,sign*40,39.5,46,3)
        if sign==-1:
            mount=mount.mirror('XZ')
        r.add('KIT_FIXATIONS',f'motor_clamp_{sign}',mount,cad.SILVER)
    for x,y in [(140,-10),(166,10)]:
        r.hole(x,y,3.2,'Entretoise appui du kit supposée')
        r.vertical_bolt('KIT_FIXATIONS',f'caster_{x}',x,y,21,46,3)
    # Cartridges sit in cavities, not in intersecting solid envelope holders.
    fuse_parts=r.load('fusibles')
    for label,y,clipx in [('PI',-2,124),('MOTEURS',11.5,148)]:
        holder=fuse_parts['holder_body'][0].translate((12.5,y,54))
        holder=holder.cut(cad.cyl(2.7,20,(132.5,y,54),(1,0,0)))
        holder=holder.cut(cad.cyl(1.6,3,(119,y,54),(1,0,0)))
        r.add('FUSIBLE_'+label,'holder',holder,cad.BLACK)
        for n in ('fuse_glass','fuse_cap_120','fuse_cap_136','fuse_link'):
            shape,color=fuse_parts[n]
            r.add('FUSIBLE_'+label,n,shape.translate((12.5,y-20,54)),color)
        clip=cad.ring(7.1,6.1,10,(clipx,y,54),(1,0,0))
        clip=clip.cut(cad.box(10,6,10,(clipx,y-3,58)))
        clip=clip.fuse(cad.box(10,14,2,(clipx,y-7,46))).clean()
        r.add('AJOUT_FUSIBLES',f'clip_{label}',clip,PURPLE)
    r.adaptations.append('Porte-fusibles : cavités ajoutées pour montrer les cartouches ; fils pré-équipés recoupés et routés.')
    # Screw holes must also go through the kit caster plate.
    replaced=[]
    for name,shape,color in r.model.parts:
        if name=='CHASSIS__acrylic_plate_estimated':
            for hole in r.drilling:
                x,y=hole['center_xy_mm']
                shape=shape.cut(cad.cyl(hole['diameter_mm']/2,3,(x,y,43)))
            for x in (31,85):
                for y in (-36.25,34.75):
                    shape=shape.cut(cad.box(10.5,1.5,3,(x-.25,y,43)))
        if name=='CHASSIS__caster_mount':
            for x,y in [(140,-10),(166,10)]:
                shape=shape.cut(cad.cyl(1.6,2,(x,y,23)))
        replaced.append((name,shape,color))
    r.model.parts=replaced
    # CSI slack loop: preserve the commercial centreline length of 160 mm.
    csi=[(186,-30,53.5),(197,-30,53.5),(206,-23,68),(205,-21,89),
         (190,0,90),(199,25,79),(199,25,64),(199,0,61),
         (188,0,64.5),(188,0,65.65)]
    lo,hi=86,94
    for _ in range(50):
        z=(lo+hi)/2; csi[3]=(205,-21,z)
        if path_length(csi)>160:
            hi=z
        else:
            lo=z
    assert abs(path_length(csi)-160)<1e-6
    r.load('nappe-csi-pi-zero')
    r.add('CSI','160mm_routed_envelope',ribbon_shape(csi),cad.GOLD,'flexible')
    r.routes.append({'name':'CSI_160','source_slug':'nappe-csi-pi-zero','points_mm':csi,
                     'polyline_length_mm':path_length(csi),'status':'enveloppe pliée indicative, rayons et insertion à relever'})
    # Two of the five USB cables are cut: supplied lengths suffice independently.
    r.place('cables-usb','USB_BATTERIE',(9,-20,55.5),((0,0,1),180),
            ['USB_A_grip','USB_A_shell'])
    r.place('cables-usb','USB_PI',(175,-343,54.4),((0,0,1),90),
            ['micro_USB_grip','micro_USB_shell'])
    r.route('USB_source',[(-21,-20,55.5),(-29,-20,55.5),(-29,0,55.5),
                          (-5,0,68),(100,0,68),(119,0,68)],1.75,cad.BLACK,'cables-usb','VBUS+GND')
    r.route('USB_Pi',[(168,-2,54),(169,-2,63),(116,-10,65),
                     (116,-44,65),(116,-75,54.4),(175,-75,54.4),(175,-68,54.4)],
            1.75,cad.BLACK,'cables-usb','Pi_5V+GND')
    r.route('fuse_input_PI',[(119,-2,54),(116.8,-2,54),(116.8,-2,66),(119,0,68)],
            1.5,cad.RED,'fusibles','VBUS')
    r.route('fuse_input_MOTEURS',[(119,11.5,54),(116.8,11.5,54),(116.8,11.5,68),(119,0,68)],
            1.5,cad.RED,'fusibles','VBUS')
    r.route('fuse_output_PI',[(166,-2,54),(168,-2,54)],1.5,cad.RED,'fusibles','Pi_5V')
    r.route('fuse_output_MOTEURS',[(166,11.5,54),(168,11.5,54),(170,16,64),(149.1,18,64),
                                 (149.1,24.65,53.48)],.85,cad.RED,'fil-22awg','VM')
    r.route('ground_Pi',[(119,-4,68),(119,-8,68),(119,-12,60),(165,-12,60),
                         (170,-6,57),(168,-2,54)],
            .85,cad.BLACK,'fil-22awg','GND')
    r.route('ground_DRV',[(119,-4,68),(123,-8,68),(127,-8,65),(127,18,65),
                          (156,18,65),(156,27.19,60),(149.1,27.19,53.48)],
            .85,cad.BLACK,'fil-22awg','GND')
    r.route('ground_logic',[(134.45,-18.77,53.88),(134.45,-16,59),(122,-10,63),
                            (123,11,63),(157,18,61),(149.1,27.19,53.48)],
            .85,cad.BLACK,'fil-22awg','GND')
    endpoints=[(149.1,29.73),(149.1,32.27),(149.1,34.81),(133.4,29.73),(133.4,32.27)]
    pi_start=[(142.07,-16.23),(144.61,-16.23),(147.15,-16.23),
              (147.15,-18.77),(149.69,-18.77)]
    for i,((px,py),(dx,dy),pin) in enumerate(zip(pi_start,endpoints,[17,27,22,23,24])):
        h=64+2.5*i
        r.route(f'BCM{pin}_candidate',[(px,py,53.88),(px,py,h),(dx,-8,h),
                                     (dx,dy,h),(dx,dy,53.48)],.85,
                (0.2+.1*i,.35,.7-.1*i),'fil-22awg',f'BCM{pin}')
    for sign,pads in [(1,[(24.65,116,23),(27.19,118,25)]),
                      (-1,[(34.81,116,-23),(37.35,116,-26)])]:
        for i,(py,sx,sy) in enumerate(pads):
            h=(60+2*i) if sign==1 else (76+2*i)
            points=[(133.4,py,53.48),(133.4,py,h),(sx,sy,h),(sx,sy,19),
                    (100,sign*(60+2*i),19),(24,sign*(54+2*i),19),
                    (24,sign*(54+2*i),32.5)]
            r.route(f'motor_{sign}_{i}',points,.85,cad.RED if i==0 else cad.BLACK,
                    'fil-22awg',f'motor_{sign}_{i}')
    # Small supplied ties bind the cable; they are not the new battery straps.
    r.load('colliers')
    for x in (70,96):
        r.add('COLLIERS',f'cable_loop_{x}',cad.ring(2.9,1.9,2.5,(x,0,68),(1,0,0)),cad.BLACK)
        r.add('COLLIERS',f'cable_head_{x}',cad.box(5,4,3,(x-1.25,-2,70.9)),cad.BLACK)
    r.load('gaine')
    r.add('GAINE','USB_splice_shrink',cad.ring(2.2,1.8,8,(107,0,68),(1,0,0)),cad.BLACK)
    r.adaptations += [
        'Nappe 160 déformée en enveloppe par loft ; longueur de ligne centrale 160, rayons non validés.',
        'USB : deux câbles du lot de cinq recoupés ; gaines et colliers déformés / recoupés pour implantation.',
        'Fils 22 AWG routés avec extrémités au-dessus des pastilles ; sections et soudures non dimensionnées.',
        'Bornes du DRV8833 illustratives, jamais un brochage certifié ; liaisons électriques à confirmer.',
        'Supports violets, sangles longues et visserie sont ajoutés à la maquette, pas déjà achetés.'
    ]
    assert len(r.sources)==13
    return r


def export(model,path):
    root=cq.Assembly(name=model.slug)
    groups={}
    for name,shape,color in model.parts:
        group,_,part=name.partition('__')
        if not part:
            group,part='PIECES',name
        if group not in groups:
            groups[group]=cq.Assembly(name=group)
        groups[group].add(shape,name=part,color=cq.Color(*color))
    for group in groups.values():
        root.add(group)
    root.export(str(path),exportType='STEP',unit='MM',outputUnit='MM',mode='default')
    shape=cq.Compound.makeCompound([s for _,s,_ in model.parts])
    loaded=cq.importers.importStep(str(path)).val()
    assert loaded.isValid() and all(s.isValid() and s.Volume()>0 for s in loaded.Solids())
    assert len(shape.Solids())==len(loaded.Solids())
    error=abs(shape.Volume()-loaded.Volume())/shape.Volume()
    assert error<1e-7
    bb0,bb1=exact_bbox(shape),exact_bbox(loaded)
    bbox_error=max(abs(a-b) for k in ('min_mm','max_mm') for a,b in zip(bb0[k],bb1[k]))
    assert bbox_error<1e-5,(path.name,bbox_error,bb0,bb1)
    reloaded=cq.Assembly.load(str(path))
    assert len(list(reloaded))==len(model.parts)
    return {'file':str(path.relative_to(ROOT)),'sha256':cad.digest(path),
            'solids':len(loaded.Solids()),'named_parts':len(model.parts),'reimport_valid':True,
            'relative_volume_error':error,'bbox_error_mm':bbox_error,'bbox':bb1,
            'unit':'mm','named_assembly_reimport_valid':True}


def collision_check(r):
    records=[]
    parts=r.model.parts
    tested=0
    for (n,a,_),(m,b,_) in combinations(parts,2):
        # Contacts internal to a component or a same-net junction are intentional.
        ga,gb=n.split('__')[0],m.split('__')[0]
        if ga==gb:
            continue
        ba,bb=a.BoundingBox(),b.BoundingBox()
        if min(ba.xmax,bb.xmax)-max(ba.xmin,bb.xmin)<=1e-6 or \
           min(ba.ymax,bb.ymax)-max(ba.ymin,bb.ymin)<=1e-6 or \
           min(ba.zmax,bb.zmax)-max(ba.zmin,bb.zmin)<=1e-6:
            continue
        tested+=1
        volume=a.intersect(b).Volume()
        if volume>1e-4:
            records.append({'a':n,'b':m,'overlap_mm3':volume,
                            'kind':'flexible' if r.kinds[n] in ('wire','flexible') or
                            r.kinds[m] in ('wire','flexible') else 'rigid'})
    return {'tolerance_mm3':1e-4,'broadphase_candidates_tested':tested,
            'scope':'Pièces de groupes distincts ; contacts internes et même groupe de faisceau exclus.',
            'interferences':records,'physical_clearance_validated':False}


def optical_check(model):
    # Standard Camera Module 3: nominal 66° horizontal / 41° vertical from its brief.
    # Conservative rectangular frustum around the 4.75 mm optical aperture.
    wires=[]
    for distance in (0,40):
        x=194.65+distance
        width=2.375+distance*math.tan(math.radians(33))
        height=2.375+distance*math.tan(math.radians(20.5))
        vertices=[cq.Vector(x,y,76.5+z) for y,z in
                  [(-width,-height),(width,-height),(width,height),(-width,height)]]
        wires.append(cq.Wire.makePolygon(vertices,close=True))
    frustum=cq.Solid.makeLoft(wires,ruled=True)
    blocked=[]
    for name,shape,color in model.parts:
        if name.startswith('CAMERA__'):
            continue
        b=shape.BoundingBox()
        if b.xmax<194.65:
            continue
        intersection=shape.intersect(frustum)
        volume=intersection.Volume()
        if volume>1e-4:
            blocked.append({'part':name,'overlap_with_frustum_mm3':volume,
                            'intersection_bbox':exact_bbox(intersection)})
    return {'camera_axis':'+x','lens_front_center_mm':[194.55,0,76.5],
            'nominal_fov_degrees':{'horizontal':66,'vertical':41},
            'checked_distance_mm':40,'obstructions':blocked,
            'method':'Frustum rectangulaire conservateur, aperture Ø4,75 ; optique et calibration non mesurées.',
            'hardware_verified':False}


def main():
    r=build_robot()
    report={'generated_on':'2026-10-11','hardware_measured':False,
            'robot':export(r.model,OUT/'drone-v2.step')}
    report['collisions']=collision_check(r)
    print('Interferences:',json.dumps(report['collisions']['interferences'],indent=2),flush=True)
    report['optical_clearance']=optical_check(r.model)
    print('Optical obstructions:',report['optical_clearance']['obstructions'],flush=True)
    cad.preview(r.model,OUT/'vue-iso.png')
    render_view(r.model,OUT/'vue-dessus.png',(0,0,1))
    render_view(r.model,OUT/'vue-face.png',(1,0,0))
    render_view(r.model,OUT/'vue-profil.png',(0,1,0))
    # Distinct workshop presentation to account for all 19 sources without carrying supplies.
    workshop=cad.Model('atelier-v2','Robot et accessoires, fournitures, compléments non embarqués.')
    workshop.parts=list(r.model.parts)
    offboard=['ceramique-100nf','electrolytiques','resistances','adaptateur-usb',
              'fil-a-souder','lecteur-microsd']
    for i,slug in enumerate(offboard):
        parts=r.load(slug)
        compound=cq.Compound.makeCompound([s for s,c in parts.values()])
        bb=compound.BoundingBox()
        translation=(350+(i%3)*200-bb.xmin,-80+(i//3)*180-bb.ymin,-bb.zmin)
        for name,(shape,color) in parts.items():
            workshop.add('ATELIER_'+slug+'__'+name,shape.translate(translation),color)
    for slug,name,p in [('chassis-2wd','AA_holder_included_not_used',(350,-180,0)),
                         ('microsd-16go','SD_adapter',(460,-180,0))]:
        shape,color=r.load(slug)[name]
        bb=shape.BoundingBox()
        workshop.add('NON_UTILISE__'+name,shape.translate((p[0]-bb.xmin,p[1]-bb.ymin,p[2]-bb.zmin)),color)
    assert len(r.sources)==19
    report['workshop']=export(workshop,OUT/'atelier-v2.step')
    cad.preview(workshop,OUT/'vue-atelier.png')
    report['sources']=list(r.sources.values())
    report['generator_sources']=[{'file':str(p.relative_to(ROOT)),'sha256':cad.digest(p)}
                                 for p in (Path(__file__),ROOT/'tools/generate_component_step.py')]
    report['coverage']={'onboard':list(r.sources)[:13],'offboard':offboard,'reference_lots':19}
    report['visual_review']={'status':'à vérifier'}
    report['previews']=[{'file':str(p.relative_to(ROOT)),'sha256':cad.digest(p)}
                        for p in [OUT/'vue-iso.png',OUT/'vue-dessus.png',OUT/'vue-face.png',
                                  OUT/'vue-profil.png',OUT/'vue-atelier.png']]
    write_json(OUT/'implantation.json',{'unit':'mm','hardware_measured':False,
               'axes':'x vers avant, y gauche, z depuis sol ; origine au bord arrière de la plaque',
               'placements':r.placements,'routes':r.routes,'adaptations':r.adaptations,
               'proposed_drilling':r.drilling,'drill_template_validated':False,
               'proposed_strap_slots':{'count':4,'size_mm':[10.5,1.5],
                   'center_xy_mm':[[36,-35.5],[36,35.5],[90,-35.5],[90,35.5]],
                   'physically_measured':False,'fabrication_validated':False},
               'supports_are_provisional':True,'bom_file':'composants-manquants.json'})
    report['additional_sources']=[{'file':str(p.relative_to(ROOT)),'sha256':cad.digest(p)}
                                  for p in [OUT/'implantation.json',OUT/'composants-manquants.json']]
    write_json(OUT/'verification.json',report)
    assert not report['collisions']['interferences'], 'Assembly interferences must be resolved'
    assert not report['optical_clearance']['obstructions'], 'Lens view must be clear'
    print('Robot and workshop STEP assemblies exported and reimported.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate-only',action='store_true',
                        help='Check placement geometry without exporting or rendering files')
    args=parser.parse_args()
    if args.validate_only:
        robot=build_robot()
        collisions=collision_check(robot)
        optical=optical_check(robot.model)
        print(json.dumps({'collisions':collisions,'optical':optical},indent=2),flush=True)
        assert not collisions['interferences'] and not optical['obstructions']
    else:
        main()
