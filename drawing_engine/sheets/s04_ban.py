# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
ty=M.tyre(); mt=ty.val().Volume()*7.85e-9
sh.frame(4,'Ban (Riding Ring)','','1:75','R01-102','GAMBAR BAGIAN',material='ZG42CrMo, ≥ 200 HB',mass=f'{mt:.1f} t',treat='N+T')
# ---- tampak depan 1:75
SF=75.0
F=View((-1,0,0),(0,-1,0),SF,92,128,name='depan')
F.draw(ty,hidden=False)
c=F.P((0,0,0)); ro=M.TY_OD/2/SF; rb=M.TY_BORE/2/SF
cl((c[0]-64,c[1]),(c[0]+64,c[1])); cl((c[0],c[1]-64),(c[0],c[1]+64))
cutplane(c[0],c[1]-70,c[1]-ro+8,'B',1) if False else None
dim_h(c[0]-ro,c[0]+ro,c[1]-ro-12,'Ø'+fn(M.TY_OD)+' ±1',c[1],c[1],tdx=-28)
a=math.radians(225); pb=(c[0]+rb*math.cos(a),c[1]-rb*math.sin(a))
datum(c[0]+rb*math.cos(math.radians(150)),c[1]-rb*math.sin(math.radians(150)),'A',(0.866,0.5))
auto_leader(pb,'Ø'+fn(M.TY_BORE)+' +0.5/0',pref=40)
vlabel(c[0],c[1]+ro+10,'TAMPAK DEPAN','1:75')
# ---- potongan B-B 1:10 (penampang atas)
SC=10.0; zc=(M.TY_OD+M.TY_BORE)/4
B=View((0,1,0),(-1,0,0),SC,300,0,name='B-B')
B.oy=118+zc/SC
win=cq.Workplane('XY').box(1400,400,1200).translate((0,0,zc)).val()
clip=cq.Workplane().add(ty.val().intersect(win))
B.section(clip,(0,0,0),hatch_sp=3.0,ang=45,draw_rest=False)
X=lambda u:B.P((u,0,0))[0]; Y=lambda r:B.P((0,0,r))[1]
yt=Y(M.TY_OD/2); yb=Y(M.TY_BORE/2); xl=X(M.TY_W/2); xr=X(-M.TY_W/2)
cl((X(0),yt-6),(X(0),yb+6))
dim_h(xl,xr,yt-14,fn(M.TY_W)+' ±0.5',yt,yt)
dim_v(yt,yb,xr+42,'('+fn((M.TY_OD-M.TY_BORE)/2)+')',xr,xr)
datum(X(250),yb,'A',(0,1)) if False else None
datum(xl,Y(zc+150),'B',(-1,0))
auto_leader((X(-M.TY_W/2+8),Y(M.TY_OD/2-8)),'2X 20 X 45°',pref=60)
auto_leader((X(-M.TY_W/2+4),Y(M.TY_BORE/2+4)),'2X 8 X 45°',pref=-60)
auto_fcf((X(-250),yt),'trun','0.5',('A',),pref=95)
auto_fcf((xr,Y(zc-150)),'perp','0.2',('A',),pref=-25,rmax=40)
auto_fcf((X(380),yb),'cyl','0.3',(),pref=-135,rmax=60)
auto_fcf((X(300),yb),'par','0.2',('B',),pref=-100) if False else None
auto_surf([(X(u),yt,False) for u in range(450,-460,-50)],'1.6')
auto_surf([(X(u),yb,True) for u in (200,0,-200)],'3.2')
vlabel(X(0),yb+16,'POTONGAN B-B','1:10')
# ---- isometri
I=View((-1.0,1.3,0.9),(-1,-0.8,0),130.0,0,0,name='iso')
I.fit(ty,(150,196,226,284)); I.iso(ty)
finish('s04')
