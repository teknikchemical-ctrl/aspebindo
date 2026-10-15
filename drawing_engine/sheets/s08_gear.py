# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
from gearg import gear_outline
m=M.MG; z=M.Z2; d2=M.D2; da=M.DA2; df=M.DF2
RIM_I=df/2-260; FL_I=3780.0; FL_O=3900.0; WEB=140.0; FLW=300.0; NPL=16
g3=M.girth_gear_simple(); mg=g3.val().Volume()*7.85e-9
sh.frame(8,'Roda Gigi Gelang','','1:100','R01-106','GAMBAR BAGIAN',material='Baja cor G34CrMo4 (EN 10293)',mass=f'{mg:.0f} t',treat='Q+T')
# ======== tampak depan 1:100 (representasi konvensional ASME Y14.7.1)
S1=100.0; cx,cy=78.0,104.0
Pf=lambda r,a:(cx+r/S1*math.cos(math.radians(a)),cy-r/S1*math.sin(math.radians(a)))
C(cx,cy,da/2/S1,.5); C(cx,cy,RIM_I/S1,.35); C(cx,cy,FL_I/S1,.5); C(cx,cy,FL_O/S1,.35)
with own(None,'cl'): L([Pf(d2/2,a) for a in range(0,361,3)],.25,CLD,'sig')
for a0 in (0,180): L([Pf(FL_I,a0),Pf(da/2,a0)],.5)
# lubang baut braket pelat pegas pada flens (16X 2 lubang)
PCD=FL_I+FL_O     # Ø7680
for i in range(32):
    th=360.0*i/32+5.625
    p=Pf(PCD/2,th); C(p[0],p[1],0.45,.3)
with own(None,'cl'): L([Pf(PCD/2,a) for a in range(0,361,3)],.18,CLD,'sig')
cline((cx-52,cy),(cx+52,cy)); cline((cx,cy-52),(cx,cy+52))
view_box('depan',(cx-da/2/S1,cy-da/2/S1,cx+da/2/S1,cy+da/2/S1))
r_=auto_leader(Pf(FL_I,300),'Ø'+fn(2*FL_I)+' H11',pref=-40); datum_on_leader(r_,'A')
auto_leader_fcf(Pf(PCD/2,5.625+11.25*11),'32X Ø45 SAMA JARAK','pos','1.5',('A',),dia=True,pref=135,rmin=12,rmax=60)
auto_leader(Pf(PCD/2,5.625+11.25*5+3),'Ø'+fn(PCD),pref=50,rmin=12,rmax=60); boxlast()
auto_leader(Pf((RIM_I+da/2)/2,0),'BIDANG BELAH',pref=-35,rmin=10,rmax=50)
angdim((cx,cy),FL_O/S1+0.0,0,5.625,'5.625°',owner='a5') if False else None
ar=[Pf(5000,a) for a in range(205,246,2)]
with own(('rot',),'ld'):
    L(ar,.35,None,'inst'); q=ar[-1]; p0=ar[-2]; dx,dy=q[0]-p0[0],q[1]-p0[1]; n_=math.hypot(dx,dy); arrow(q[0],q[1],dx/n_,dy/n_)
T(Pf(5000,225)[0]-3,Pf(5000,225)[1]+6,'ARAH PUTARAN',3.0,'r',owner=('rot',))
cutplane(cx,cy-da/2/S1-7,cy+da/2/S1+7,'D',1)
pe=Pf(da/2,35); detcircle(pe[0],pe[1],5,'E',ang=20)
vlabel(cx,cy+da/2/S1+18,'TAMPAK DEPAN','1:100')
# ======== detail E 1:5
S3=5.0; ex,ey=349.0,60.0
pts=gear_outline(z,m,20.0,teeth=range(-2,3),center_ang=90.0)
G=lambda x,y:(ex+x/S3, ey-(y-d2/2)/S3)
L([G(x,y) for x,y in pts],.5)
with own(None,'cl'): L([G(d2/2*math.cos(math.radians(90+t)),d2/2*math.sin(math.radians(90+t))) for t in [k*0.25 for k in range(-12,13)]],.25,CLD,'sig')
yt_=G(0,da/2)[1]; yf_=G(0,df/2)[1]; yp_=G(0,d2/2)[1]
view_box('E',(G(-280,0)[0],yt_,G(280,0)[0],yf_+2))
xrr=G(-300,0)[0]-6
dim_v(yt_,yp_,xrr,'36',G(-150,0)[0],G(-150,0)[0],out=True,side=-1)
dim_v(yp_,yf_,xrr+0,'45',None,None,out=True,side=-1)
pw=math.pi*m
dim_h(G(-pw/2,0)[0],G(pw/2,0)[0],yt_-10,'113.1',yp_,yp_)
vlabel(ex,yf_+10,'DETAIL E','1:5')
rows=[['Modul','m','36'],['Jumlah gigi','z','252'],['Sudut tekan','α','20°'],['Sudut heliks','β','0°'],
      ['Diameter jarak bagi','d','9072'],['Diameter kepala','da','9144'],['Diameter kaki','df','8982'],
      ['Lebar gigi','b','850'],['Koefisien geser profil','x','0'],['Pinion pasangan','—','R01-107, z 15'],['Jarak sumbu','a','4806'],
      ['Kualitas (ISO 1328-1)','—','9'],['Konstruksi','—','2 belahan'],['Kekasaran sayap gigi','Ra','3.2']]
kt.table(298.0,108.0,[54,14,42],['BESARAN','SIMBOL','NILAI'],rows,size=3.0,aligns=['l','m','m'],minh=5.6,hdr_size=3.0,title='DATA RODA GIGI',tsize=3.5)
# ======== potongan D-D 1:10
S2=10.0; ox,oy=224.0,172.0; r0=3700.0
Q=lambda u,r:(ox+u/S2, oy-(r-r0)/S2)
h=M.BG/2; ch=5.0
rim=[(-h,RIM_I),(-h,da/2-ch),(-h+ch,da/2),(h-ch,da/2),(h,da/2-ch),(h,RIM_I),(WEB/2,RIM_I),(WEB/2,FL_O),(FLW/2,FL_O),(FLW/2,FL_I),(-FLW/2,FL_I),(-FLW/2,FL_O),(-WEB/2,FL_O),(-WEB/2,RIM_I)]
R1=[Q(u,r) for u,r in rim]; PG(R1,.5,None); hatch([R1],45,2.6)
L([Q(-h,df/2),Q(h,df/2)],.25,None,'equip')
with own(None,'cl'): L([Q(-h-12,d2/2),Q(h+12,d2/2)],.25,CLD,'sig')
cline(Q(0,FL_I-120),Q(0,da/2+120))
view_box('D-D',(Q(-h,0)[0],Q(0,da/2)[1],Q(h,0)[0],Q(0,FL_I)[1]))
yt=Q(0,da/2)[1]
dim_h(Q(-h,0)[0],Q(h,0)[0],yt-30,fn(M.BG),yt,yt,tdx=-22)
dim_h(Q(-FLW/2,0)[0],Q(FLW/2,0)[0],Q(0,FL_I)[1]+10,fn(FLW),Q(0,FL_I)[1],Q(0,FL_I)[1],tdx=8)
xr=Q(h,0)[0]+10
dim_v(yt,Q(0,RIM_I)[1],Q(-h,0)[0]-10,fn(da/2-RIM_I),Q(-h,0)[0],Q(-h,0)[0],side='left')
dim_v(Q(0,FL_O)[1],Q(0,FL_I)[1],xr,'120',Q(FLW/2,0)[0],Q(FLW/2,0)[0],out=True)
dim_h(Q(-WEB/2,0)[0],Q(WEB/2,0)[0],Q(0,(RIM_I+FL_O)/2)[1],fn(WEB),None,None,out='left')
datum(Q(-FLW/2,0)[0],Q(0,(FL_I+FL_O)/2)[1],'B',(-1,0))
auto_leader(Q(h-3,da/2-3),'2X 5 X 45°',pref=45)
auto_leader(Q(-h+150,RIM_I),'Ø'+fn(2*RIM_I),pref=-150,rmax=50)
auto_leader(Q(FLW/2-40,FL_O),'Ø'+fn(2*FL_O),pref=-20,rmax=50)
auto_leader_fcf((Q(-250,0)[0],yt),'Ø'+fn(da)+' h11','crun','0.5',('A',),pref=60,rmax=40)
auto_fcf((Q(h,0)[0],Q(0,4350)[1]),'crun','0.8',('A',),pref=-35,rmax=60)

vlabel(ox,Q(0,FL_I)[1]+18,'POTONGAN D-D','1:10')
I=View((-1.0,1.2,0.9),(-1,-0.8,0),150.0,0,0,name='iso'); I.fit(g3,(30,196,200,282)); I.iso(g3)
finish('s08')
