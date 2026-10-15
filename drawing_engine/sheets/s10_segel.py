# -*- coding: utf-8 -*-
from common import *
import models as M
from vw import cl
from sym import *
sh.frame(10,'Segel Ujung dan Cincin Hidung','','1:6','R01-108','GAMBAR SUSUNAN + BAGIAN',material='Lihat daftar bagian',mass='—',treat='—')
ri=M.DSI/2; ro=ri+M.TSH; rb=M.DI/2            # 3350, 3388, 3150
RS=ro+60.0                                     # puncak cincin segel 3448
RF=3880.0                                      # muka bawah flens tudung
LEAF=610.0; UB=(-320.0,-160.0)                 # panjang pelat daun, posisi baut
uc=-240.0-(RF-RS)                               # titik sentuh daun pada cincin segel (45°)
# tabel bagian dulu (zona terlarang bagi penempatan otomatis)
rows=[['1','Dinding tudung pembakaran (referensi)','—','Baja karbon'],
      ['2','Pelat daun pegas — TAMPAK L','90','Baja pegas 51CrV4'],
      ['3','Cincin segel (lengan aus)','1','S355J2'],
      ['4','Segmen cincin hidung — POTONGAN K-K','24','GX40CrNiSi25-12'],
      ['5','Isolasi','—','Bata isolasi'],
      ['6','Bata kerja','—','Bata alumina tinggi'],
      ['7','Cangkang (R01-101)','—','ASTM A36'],
      ['8','Baut heksagon M30 X 150, ISO 4014','48','Kelas 8.8']]
kt.table(14.0,219.0,[9,100,12,62],['NO.','NAMA BAGIAN','JML.','BAHAN'],rows,size=3.0,aligns=['m','l','m','l'],minh=5.6,hdr_size=3.0,title='DAFTAR BAGIAN',tsize=3.5)
# ===================== DETAIL G 1:8 (susunan ujung pelepasan)
S3=6.0; gx,gy=207.0,178.0
G=lambda u,r:(gx+u/S3, gy-(r-rb)/S3)
def blk(poly,an,sp,w=.5):
    P_=[G(u,r) for u,r in poly]; PG(P_,w,None); hatch([P_],an,sp)
blk([(-1000,ri),(0,ri),(0,ro),(-1000,ro)],45,1.0)                                   # 7 cangkang
blk([(-900,ro),(-400,ro),(-400,RS),(-900,RS)],135,1.0)                               # 3 cincin segel
blk([(-1000,ri-70),(-650,ri-70),(-650,ri),(-1000,ri)],135,0.9)                      # 5 isolasi
blk([(-1000,rb),(-650,rb),(-650,ri-70),(-1000,ri-70)],45,1.8)                        # 6 bata kerja
blk([(-650,rb),(0,rb),(0,ri),(-80,ri),(-80,ri-40),(-650,ri-40)],45,2.6)             # 4 cincin hidung
for ub in UB:                                                                         # 8 baut
    PG([G(ub-15,ri-40-50),G(ub+15,ri-40-50),G(ub+15,ro),G(ub-15,ro)],.35,None)
    PG([G(ub-23,ro),G(ub+23,ro),G(ub+23,ro+20),G(ub-23,ro+20)],.35,None)
PG([G(-150,RF),G(-130,RF),G(-130,4000),G(-150,4000)],.5,'#000000')                  # 1 dinding tudung
breakline(G(-175,4000),G(-105,4000))
PG([G(-260,RF),G(-130,RF),G(-130,RF+40),G(-260,RF+40)],.5,'#000000')                # flens
with own('daun','obj'): L([G(-240,RF),G(uc,RS)],.8,None,'equip')                    # 2 pelat daun 45°
breakline(G(-1000,rb-15),G(-1000,RS+15))
view_box('G',(G(-1000,0)[0],G(0,RS)[1],G(0,0)[0],G(0,rb)[1]))
view_box('G-tudung',(G(-280,0)[0],G(0,4000)[1],G(-100,0)[0],G(0,RF)[1]))
# --- dimensi susunan
yb=G(0,rb)[1]
dim_h(G(-650,0)[0],G(0,0)[0],yb+22,'650',yb,yb)
xR=G(0,0)[0]
dim_v(G(0,ri)[1],G(0,rb)[1],xR+10,fn(ri-rb),xR,xR)
dim_v(G(0,ro)[1],G(0,ri)[1],xR+10,fn(ro-ri),xR,xR,out=True)
dim_v(G(0,RF)[1],G(0,RS)[1],xR+24,fn(RF-RS),G(-130,0)[0],G(-400,0)[0])
xL=G(-1000,0)[0]
dim_v(G(0,ri-70)[1],G(0,rb)[1],xL-20,'130',xL,xL,side=1)
dim_v(G(0,ri)[1],G(0,ri-70)[1],xL-9,'70',xL,xL,out=True,side=-1)
dim_v(G(0,RS)[1],G(0,ro)[1],G(-900,0)[0]-7,'60',G(-900,0)[0],G(-900,0)[0],out=True,side=-1)
yS=G(0,RS)[1]-20
dim_h(G(-900,0)[0],G(-400,0)[0],yS,'500',yS+20,yS+20,tdx=-10)
dim_h(G(-400,0)[0],G(0,0)[0],yS,'400',yS+20,G(0,ro)[1])
dim_h(G(-130,0)[0],G(0,0)[0],G(0,4000)[1]-8,'130',G(0,4000)[1],G(0,ro)[1])
angdim(G(-240,RF),16,180,225,'45°',owner='a45')
auto_leader(G(UB[0]+10,ro+20),'',pref=110,rmin=14,rmax=90,lines=['48X Ø33 PADA','CANGKANG, BOR','SAAT PASANG'])
auto_leader(G(-600,RS),'Ø'+fn(2*RS),pref=150,rmax=60)
num={'1':(-140,3950),'2':((-240+uc)/2,(RF+RS)/2),'3':(-860,ro+30),'4':(-80,3200),'5':(-900,ri-35),'6':(-850,3230),'7':(-960,ro-19),'8':(UB[0],ri-70)}
for n,(u,r) in num.items():
    auto_balloon(n,G(u,r),pref={'3':120,'5':-100,'6':-80,'7':150,'4':-80,'8':-90,'2':20}.get(n,60),rmin=12,rmax=60)
T(G(-500,0)[0],yb+33,'DETAIL G',5.0,'m',owner='dg',kind='vl'); T(G(-500,0)[0]+18,yb+33,'SKALA 1:6',3.5,'l',owner='dg',kind='vl')
# ===================== BAGIAN 4: segmen cincin hidung — tampak ujung 1:10
S5=10.0; cx,cy=300.0,47.0
a0,a1=82.5,97.5
oc=(cx,cy+3350/S5+2)
arc=lambda r,a:(oc[0]+r/S5*math.cos(math.radians(a)), oc[1]-r/S5*math.sin(math.radians(a)))
pts=[arc(rb,a0+(a1-a0)*i/24) for i in range(25)]+[arc(ri,a1-(a1-a0)*i/24) for i in range(25)]
PG(pts,.5,None)
view_box('segmen',(min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)))
with own('rad','cl'):
    for a_ in (a0,a1): L([arc(rb-190,a_),arc(rb-2,a_)],.25,CLD,'sig')
angdim(oc,rb/S5-16,a0,a1,'15°',owner='a15')
auto_leader(arc(ri,86),'R'+fn(ri),pref=20)
auto_leader(arc(rb,93),'R'+fn(rb),pref=-150)
cutplane(oc[0],arc(ri,90)[1]-7,arc(rb,90)[1]+7,'K',1)
T(cx-5,arc(rb,a0)[1]+30,'BAGIAN 4 — SEGMEN CINCIN HIDUNG',5.0,'m',owner='sc',kind='vl'); T(cx-5,arc(rb,a0)[1]+37.5,'TAMPAK UJUNG · 24X · SKALA 1:10',3.5,'m',owner='sc',kind='vl')
# ===================== POTONGAN K-K 1:10 (profil aksial segmen)
kx,ky=380.0,197.0
K_=lambda u,r:(kx+u/5.0, ky-(r-rb)/5.0)
prof=[(-650,rb),(0,rb),(0,ri),(-80,ri),(-80,ri-40),(-650,ri-40)]
holes=[]
for ub in UB:
    holes.append([(ub-13.2,ri-40-60),(ub+13.2,ri-40-60),(ub+13.2,ri-40-0.01),(ub-13.2,ri-40-0.01)])
Pp=[K_(u,r) for u,r in prof]; PG(Pp,.5,None)
hatch([Pp]+[[K_(u,r) for u,r in h_] for h_ in holes],45,2.2)
for ub in UB:
    for s_ in (-1,1):
        L([K_(ub+s_*13.2,ri-40),K_(ub+s_*13.2,ri-40-60)],.5,None,'equip')
        with own(('ulir',ub),'hat'): L([K_(ub+s_*15,ri-40),K_(ub+s_*15,ri-40-60)],.25,None,'proc')
    L([K_(ub-13.2,ri-40-60),K_(ub+13.2,ri-40-60)],.5,None,'equip')
view_box('K-K',(K_(-650,0)[0],K_(0,ri)[1],K_(0,0)[0],K_(0,rb)[1]))
yk=K_(0,rb)[1]; ykt=K_(0,ri)[1]
dim_h(K_(-650,0)[0],K_(0,0)[0],yk+11,'650',yk,yk)
yc=ykt-10
dim_h(K_(UB[0],0)[0],K_(UB[1],0)[0],yc,fn(UB[1]-UB[0]),K_(0,ri-40)[1],K_(0,ri-40)[1])
dim_h(K_(UB[1],0)[0],K_(-80,0)[0],yc,fn(-80-UB[1]),K_(0,ri-40)[1],K_(0,ri)[1])
dim_h(K_(-80,0)[0],K_(0,0)[0],yc,'80',K_(0,ri)[1],K_(0,ri)[1])
dim_v(K_(0,ri)[1],yk,K_(0,0)[0]+10,fn(ri-rb),K_(0,0)[0],K_(0,0)[0])
dim_v(K_(0,ri-40)[1],yk,K_(-650,0)[0]-10,fn(ri-40-rb),K_(-650,0)[0],K_(-650,0)[0],side=-1)
auto_leader(K_(UB[0]-13.2,ri-40-30),'2X M30-6H DALAM 60',pref=-140,rmax=50)
T(kx-65,yk+21,'POTONGAN K-K',5.0,'m',owner='kk',kind='vl'); T(kx-65+26,yk+21,'SKALA 1:5',3.5,'l',owner='kk',kind='vl')
# ===================== BAGIAN 2: pelat daun pegas 1:10
lx,ly=372.0,60.0
Lp=lambda a,b:(lx+a/10.0, ly+b/10.0)      # a lebar (−125..125), b panjang (0..610)
PG([Lp(-125,0),Lp(125,0),Lp(125,LEAF),Lp(-125,LEAF)],.5,None)
for a_ in (-75,75): C(Lp(a_,20)[0],Lp(a_,20)[1],0.9,.35)
cline(Lp(0,-6),Lp(0,LEAF+6))
view_box('daun',(Lp(-125,0)[0],Lp(0,0)[1],Lp(125,0)[0],Lp(0,LEAF)[1]))
dim_h(Lp(-125,0)[0],Lp(125,0)[0],Lp(0,0)[1]-20,'250',Lp(0,0)[1],Lp(0,0)[1])
dim_h(Lp(-75,0)[0],Lp(75,0)[0],Lp(0,0)[1]-9,'150',Lp(0,20)[1]-1,Lp(0,20)[1]-1)
dim_v(Lp(0,0)[1],Lp(0,LEAF)[1],Lp(-125,0)[0]-10,fn(LEAF),Lp(-125,0)[0],Lp(-125,0)[0],side=-1)
dim_v(Lp(0,0)[1],Lp(0,20)[1],Lp(125,0)[0]+8,'20',Lp(125,0)[0],Lp(75,0)[0]+1.2,out=True)
auto_leader(Lp(75+6.4,20+6.4),'2X Ø18',pref=-40,rmax=40)
T(lx-6,Lp(0,LEAF)[1]+10,'BAGIAN 2 — PELAT DAUN',5.0,'m',owner='pd',kind='vl'); T(lx-6,Lp(0,LEAF)[1]+17.5,'TAMPAK L · t 3 · SKALA 1:10',3.5,'m',owner='pd',kind='vl')
finish('s10')
