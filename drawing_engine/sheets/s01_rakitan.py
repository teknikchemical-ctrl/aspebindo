# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
sh.frame(1,'Kiln Rotari Sulfasi R-01','Rakitan Utama','1:250','R01-000','GAMBAR RAKITAN UTAMA',material='Lihat daftar bagian',mass=f"± {M.R['W_total_t']:.0f} t (berputar)",treat='—')
# ================= DAFTAR BAGIAN & NOSEL
rows=[['1','R01-101','Cangkang','1','ASTM A36'],
      ['2','R01-102','Ban','3','ZG42CrMo, ≥ 200 HB'],
      ['3','R01-103','Bar pengisi dan blok penahan','3 set','S355JR'],
      ['4','R01-100','Stasiun penumpu (2 rol)','3','Lihat R01-100'],
      ['5','R01-106','Roda gigi gelang','1','G34CrMo4'],
      ['6','R01-107','Pinion','2','42CrMo4 Q+T'],
      ['7','PEMASOK','Reduktor + motor 250 kW','2','Rakitan'],
      ['8','R01-108','Segel ujung dan cincin hidung','2','Lihat R01-108'],
      ['9','—','Tudung umpan','1','Baja karbon + tahan api'],
      ['10','—','Tudung pembakaran','1','Baja karbon + tahan api'],
      ['11','PEMASOK','Pembakar','1','Rakitan'],
      ['12','SIPIL','Fondasi','3','Beton bertulang']]
kt.table(14.0,188.0,[9,22,78,12,80],['NO.','NO. GAMBAR','NAMA BAGIAN','JML.','BAHAN / KETERANGAN'],rows,size=3.0,aligns=['m','m','l','m','l'],minh=5.4,hdr_size=3.0,title='DAFTAR BAGIAN',tsize=3.5)
nr=[['N1','Umpan padatan (talang)','—','Pemasok'],['N2','Gas keluar ke CY-02','DN2400','Flens fabrikasi'],['N3','Udara panas','DN1900','Flens fabrikasi'],
    ['N4','Injeksi SO₂','DN500','ASME B16.5 Cl.150 RF'],['N5','Pembakar aksial','—','Pemasok'],['N6','Pelepasan kalsin','—','Pemasok']]
kt.table(232.0,181.2,[13,62,22,78],['TANDA','LAYANAN','UKURAN','FLENS'],nr,size=3.0,aligns=['m','l','m','l'],minh=5.2,hdr_size=3.0,title='DAFTAR NOSEL',tsize=3.5)
rot,st,dr=M.kiln_local()
ROT=[M.place(p) for p in rot]; DRV=[M.ground_clip(M.place(p)) for p in dr]
ST=[M.ground_clip(M.place(p)) for p in st]
HD=M.hoods(); ALL=ROT+ST+DRV+HD
SC=250.0; phi=M.PHI
xe=M.LK*math.cos(phi); ze=M.EL0-M.LK*math.sin(phi)
def A(x,r=0.0): return (x*math.cos(phi)+r*math.sin(phi),0,M.EL0-x*math.sin(phi)+r*math.cos(phi))
# ================= TAMPAK SAMPING (elevasi)
X0=60.0; YG=112.0
E=View((0,-1,0),(1,0,0),SC,X0,YG,name='elevasi')
E.draw(ALL,hidden=False); kd.OPEN_VIEWS.add('elevasi')
g=E.P((0,0,0))
with own('tanah','obj'): L([(E.P((-9000,0,0))[0],g[1]),(E.P((76500,0,0))[0],g[1])],.6,None,'equip')
for i in range(40):
    x_=E.P((-9000+i*2150,0,0))[0]
    with own('tanah','hat'): L([(x_,g[1]),(x_-2.2,g[1]+2.2)],.25,None,'proc')
cl(E.P(A(-5000)),E.P(A(M.LK+10500)))
xs=[0,M.XT[0],M.XG,M.XT[1],M.XT[2],M.LK]
tops=[E.P(A(x,M.TY_OD/2 if x in M.XT else (M.DA2/2 if x==M.XG else M.DSI/2+M.TSH))) for x in xs]
yc=46.0
for i in range(5):
    dim_h(tops[i][0],tops[i+1][0],yc,fn(xs[i+1]-xs[i]),tops[i][1],tops[i+1][1])
dim_h(tops[0][0],tops[5][0],yc-11,fn(M.LK),tops[0][1],tops[5][1])
# lokasi nosel (horizontal)
pN1=E.P((-7643,0,13838)); pN2=E.P((-2100,0,18355)); pN3=E.P((xe+1800,0,ze+200+4600+3800)); pN4=E.P((xe+3900,0,ze+200+4600+2800))
pK=E.P(A(M.LK)); pK0=E.P(A(0))
dim_h(pN1[0],pN2[0],46,fn(7643-2100),pN1[1],pN2[1])
dim_h(pN2[0],tops[0][0],22,'2100',pN2[1],pK0[1],out='right',size=3.0)
yN=58.0
dim_h(pK[0],pN3[0],yN,'1800',pK[1],pN3[1],out='left',size=3.0)
dim_h(pN3[0],pN4[0],yN,'2100',None,pN4[1],out='right',size=3.0)
pN6=E.P((xe+1700,0,0))
dim_h(pK[0],pN6[0],g[1]+7,'1700',None,g[1],out='left',size=3.0)
with own('ext-k6','ext'): L([(pK[0],pK[1]+1.5),(pK[0],g[1]+9.5)],.25,None,'inst')
def level(x,y,txt,left=True,below=False):
    ow=('lv',round(x,1),round(y,1))
    with own(ow,'sym'):
        d.poly([(x,y),(x-2,y-3.2),(x+2,y-3.2)],.3,None,K,'inst')
        L([(x-2,y-3.2),(x+(-20 if left else 20),y-3.2)],.25,None,'inst')
    T(x+(-2.8 if left else 2.8),y-4.6 if not below else y+1.0,txt,3.0,'r' if left else 'l',owner=ow)
xl=E.P((-5000,0,0))[0]
level(xl,g[1],'EL ±0.000')
ya=E.P((0,0,M.EL0))[1]
with own('lv-ext','ext'): L([(E.P((-4450,0,0))[0]-1,ya),(xl+2.2,ya)],.25,None,'inst')
level(xl,ya,'EL +9.355',below=True)
pa=E.P(A(M.LK)); xr_=E.P((xe+11500,0,0))[0]
with own('lv-ext2','ext'): L([(E.P((xe+10500,0,0))[0]+1,pa[1]),(xr_+14,pa[1])],.25,None,'inst')
level(xr_,pa[1],'EL +7.150',False)
level(pN2[0]-5.4,pN2[1],'EL +18.355')
dim_v(pN4[1],pa[1],393,'7600',pN4[0]+1.2,xr_+14)
dim_v(pN3[1],pa[1],404,'8600',pN3[0]+4,xr_+14)
p1=(112.0,25.5)
T(p1[0],p1[1],'KEMIRINGAN SUMBU 3.5% (2.0°)',3.0,'m',owner='slp'); T(p1[0],p1[1]+5,'DIMENSI AKSIAL DIUKUR SEJAJAR SUMBU',3.0,'m',owner='slp')
# balon
auto_leader(E.P(A(42000,-(M.DSI/2+M.TSH))),'Ø'+fn(M.DSI+2*M.TSH),pref=-60,rmax=40)
auto_balloon('1',E.P(A(20000,M.DSI/2+M.TSH)),pref=100,rmax=40)
auto_balloon('2',E.P(A(M.XT[2],M.TY_OD/2)),pref=80,rmax=40)
auto_balloon('3',E.P(A(M.XT[1]+M.TY_W/2+150,M.DSI/2+M.TTY+80)),pref=70,rmax=40)
auto_balloon('4',E.P(A(M.XT[0],-M.RY-M.HB_H)),pref=-110,rmax=40)
auto_balloon('5',E.P(A(M.XG,M.DA2/2)),pref=100,rmax=40)
auto_balloon('8',E.P(A(650,M.DSI/2+M.TSH+60)),pref=70,rmax=40)
auto_balloon('9',E.P((-3900,0,M.EL0-2500)),pref=-120,rmax=40)
auto_balloon('10',E.P((xe+6000,0,ze-2500)),pref=-60,rmax=40)
auto_balloon('11',E.P((xe+6650+2500,0,ze)),pref=-45,rmax=40)
auto_balloon('12',E.P((M.XT[2]*math.cos(phi),0,1200)),pref=-100,rmax=40)
# tanda nosel
auto_nz('N1',E.P((-7300,0,13500)),pref=150)
auto_nz('N2',E.P((-2100,0,18355)),pref=120)
auto_nz('N3',E.P((xe+1800,0,ze+200+4600+400)),pref=-100,rmin=8)
auto_nz('N4',E.P((xe+3900,0,ze+200+4600+400)),pref=-80,rmin=8)
auto_nz('N5',E.P((xe+6650+3800,0,ze)),pref=30)
auto_nz('N6',E.P((xe+1700,0,1500)),pref=-150)
T(E.P((30000,0,0))[0],g[1]+9,'TAMPAK SAMPING',5.0,'m',owner='vl-e',kind='vl'); T(E.P((30000,0,0))[0]+31,g[1]+9,'SKALA 1:250',3.5,'l',owner='vl-e',kind='vl')
# ================= DENAH
Pn=View((0,0,1),(1,0,0),SC,X0,155,name='denah')
Pn.draw(ALL,hidden=False); kd.OPEN_VIEWS.add('denah')
cp=Pn.P((0,0,0)); cl((Pn.P((-6000,0,0))[0],cp[1]),(Pn.P((76000,0,0))[0],cp[1]))
for xt in M.XT:
    q=Pn.P((xt*math.cos(phi),0,0)); cl((q[0],q[1]-26),(q[0],q[1]+26))
auto_balloon('6',Pn.P(((M.XG-M.BP/2)*math.cos(phi)+100,-M.A_C*math.cos(math.radians(20)),0)),pref=0,rmax=40)
auto_balloon('7',Pn.P(((M.XG-M.BP/2-1700-1200)*math.cos(phi),M.A_C*math.cos(math.radians(20))+900,0)),pref=150,rmax=30)
yb=Pn.P((0,-6000,0))[1]
xd=Pn.P((17000,0,0))[0]
for sg in (1,-1):
    q=Pn.P(((M.XG-M.BP/2-1700-2400-500-1900)*math.cos(phi),sg*M.A_C*math.cos(math.radians(20)),0))
    dim_v(cp[1],q[1],xd,fn(M.A_C*math.cos(math.radians(20))),None,q[0])
dim_h(Pn.P((M.XT[0]*math.cos(phi),M.BF_LAT/2+200,0))[0],Pn.P((M.XT[0]*math.cos(phi),-(M.BF_LAT/2+200),0))[0],0,'',0,0) if False else None
T(372,140,'DENAH',5.0,'l',owner='vl-p',kind='vl'); T(372,147.5,'SKALA 1:250',3.5,'l',owner='vl-p',kind='vl')
finish('s01')
