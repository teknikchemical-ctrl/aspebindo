# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
# model bagian tunggal
bar=cq.Workplane('XY').box(1400,220,70).edges('|Y').chamfer(10)
blk=cq.Workplane('XY').box(160,200,180).edges('|Y and >Z').chamfer(15)
mb=bar.val().Volume()*7.85e-6; mk=blk.val().Volume()*7.85e-6
sh.frame(5,'Bar Pengisi dan Blok Penahan','','1:5','R01-103','GAMBAR BAGIAN',material='S355JR (EN 10025-2)',mass=f'{mb:.0f} / {mk:.0f} kg',treat='—')
# ======== BAGIAN 1: bar pengisi (1:10)
S1=10.0
F=View((0,-1,0),(1,0,0),S1,110,72,name='bar-depan'); F.draw(bar,hidden=False)
P=View((0,0,1),(1,0,0),S1,110,112,name='bar-atas'); P.draw(bar,hidden=False)
E=View((1,0,0),(0,1,0),S1,22+8,72,name='bar-ujung') if False else None
X=lambda u:F.P((u,0,0))[0]
yt=F.P((0,0,35))[1]; yb=F.P((0,0,-35))[1]
dim_h(X(-700),X(700),yt-12,'1400',yt,yt)
dim_v(yt,yb,X(700)+12,'70',X(700),X(700))
yp1=P.P((0,110,0))[1]; yp2=P.P((0,-110,0))[1]
dim_v(yp1,yp2,X(700)+12,'220',X(700),X(700))
auto_leader((X(-700+5),F.P((0,0,30))[1]),'4X 10 X 45°',pref=150)
T(110,yp2+10,'BAGIAN 1 — BAR PENGISI',5.0,'m',owner='b1',kind='vl'); T(110,yp2+17.5,'64X PER BAN · SKALA 1:10',3.5,'m',owner='b1',kind='vl')
# ======== BAGIAN 2: blok penahan (1:5)
S2=5.0
G=View((0,-1,0),(1,0,0),S2,300,78,name='blok-depan'); G.draw(blk,hidden=False)
Q=View((1,0,0),(0,1,0),S2,360,78,name='blok-samping'); Q.draw(blk,hidden=False)
Xg=lambda u:G.P((u,0,0))[0]; Yg=lambda z:G.P((0,0,z))[1]
dim_h(Xg(-80),Xg(80),Yg(90)-12,'160',Yg(90),Yg(90))
dim_v(Yg(90),Yg(-90),Xg(-80)-12,'180',Xg(-80),Xg(-80),side=-1)
Xq=lambda v:Q.P((0,v,0))[0]
dim_h(Xq(-100),Xq(100),Yg(90)-12,'200',Yg(90),Yg(90))
auto_leader((Xg(80-7),Yg(90-7)),'15 X 45°',pref=30)
T(330,Yg(-90)+14,'BAGIAN 2 — BLOK PENAHAN',5.0,'m',owner='b2',kind='vl'); T(330,Yg(-90)+21.5,'32X PER BAN · SKALA 1:5',3.5,'m',owner='b2',kind='vl')
# ======== DETAIL PEMASANGAN (1:5): blok dilas pada bar pengisi
S3=5.0; hx,hy=300.0,182.0
def H(u,v): return (hx+u/S3, hy-v/S3)
r0=0
barp=[(-80,0),(200,0),(200,60),(190,70),(-80,70)]
blkp=[(10,70),(170,70),(170,235),(155,250),(10,250)]
for poly,an,sp in ((barp,135,1.4),(blkp,45,2.2)):
    Pp=[H(u,v) for u,v in poly]; PG(Pp,.5,None); hatch([Pp],an,sp,.18)
breakline(H(-80,-6),H(-80,76))
dim_h(H(0,0)[0],H(200,0)[0],H(0,0)[1]+10,'200',H(0,60)[1],H(200,0)[1])
with own(None,'cl'): L([H(0,60),H(0,280)],.25,[2,1],'sig')
dim_h(H(0,0)[0],H(10,0)[0],H(0,250)[1]-10,'10',H(0,262)[1],H(0,250)[1],out='left')
auto_leader(H(0,240),'MUKA SAMPING BAN',pref=160)
weld(H(170,70)[0],H(170,70)[1],H(170,70)[0]+10,H(170,70)[1]-26,'12',both=False,all_round=True)
T(hx+12,hy+21,'DETAIL PEMASANGAN',5.0,'m',owner='dp',kind='vl'); T(hx+12,hy+28.5,'SKALA 1:5',3.5,'m',owner='dp',kind='vl')
T(hx+12,hy+35,'64X BAR SAMA JARAK 5.625°',3.0,'m',owner='dp2'); T(hx+12,hy+40.5,'2 X 16 BLOK SAMA JARAK 22.5°',3.0,'m',owner='dp3')
I=View((-1.0,1.3,0.9),(-1,-0.8,0),10.0,0,0,name='iso'); I.fit(bar,(40,205,200,280)); I.iso(bar)
finish('s05')
