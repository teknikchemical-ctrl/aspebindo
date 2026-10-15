# -*- coding: utf-8 -*-
from common import *
import models as M
from vw import View, cl
from sym import *
shf=M.shaft(); ms=shf.val().Volume()*7.85e-9
sh.frame(7,'Poros Rol Penumpu','','1:10','R01-105','GAMBAR BAGIAN',material='42CrMo4 (EN 10083-3)',mass=f'{ms:.1f} t',treat='Q+T 280–320 HB')
SC=10.0; h=M.BR/2
x1=h; x2=x1+M.L_COL; x3=x2+M.L_TR; x4=x3+M.L_JRN; x5=x4+180
S=View((0,-1,0),(1,0,0),SC,200,118,name='poros')
S.draw(shf,hidden=False); kd.OPEN_VIEWS.add('poros')
_h=M.BR/2; _x1=_h; _x2=_x1+M.L_COL; _x3=_x2+M.L_TR; _x4=_x3+M.L_JRN; _x5=_x4+180
kd.solid_profile(S,[(-_x5,M.D_JRN/2-60),(-_x4,M.D_JRN/2-60),(-_x4,M.D_JRN/2),(-_x3,M.D_JRN/2),(-_x2,M.D_COL/2),(-_x1,M.D_COL/2),(-_x1,M.D_SEAT/2),(_x1,M.D_SEAT/2),(_x1,M.D_COL/2),(_x2,M.D_COL/2),(_x3,M.D_JRN/2),(_x4,M.D_JRN/2),(_x4,M.D_JRN/2-60),(_x5,M.D_JRN/2-60)])
cs=S.P((0,0,0)); cl((cs[0]-145,cs[1]),(cs[0]+145,cs[1]))
yo=S.P((0,0,M.D_COL/2))[1]; yj=S.P((0,0,M.D_JRN/2))[1]; yjb=S.P((0,0,-M.D_JRN/2))[1]; ycb=S.P((0,0,-M.D_COL/2))[1]
X=lambda u:S.P((u,0,0))[0]
# rantai dimensi panjang (atas) — semua dihitung dari model
xs=[-x5,-x4,-x2,-x1,x1,x2,x4,x5]
yd=yo-32
for i in range(len(xs)-1):
    a_,b_=xs[i],xs[i+1]
    dim_h(X(a_),X(b_),yd,fn(b_-a_),yo,yo)
for s_ in (-1,1):
    dim_h(X(s_*x3),X(s_*x2),yo-18,fn(x3-x2),yj,yo,out=True)
dim_h(X(-x5),X(x5),yd-11,fn(2*x5),yo,yo)
# diameter (bawah) sebagai dimensi vertikal di samping
def dv(u,D,txt,xoff,tdy=0):
    dim_v(S.P((0,0,D/2))[1],S.P((0,0,-D/2))[1],X(u)+xoff,txt,X(u),X(u),tdy=tdy)
dv(-x5,M.D_JRN-120,'Ø480',-12)
dv(x5,M.D_JRN-120,'Ø480',12)
datum(X(-x3-300),yjb,'A',(0,1)); datum(X(x3+300),yjb,'B',(0,1))
# leher, kerah, dudukan: label diameter otomatis
auto_leader_fcf((X(-x4+120),yjb),'Ø600 m6','cyl','0.02',pref=-120)
auto_leader_fcf((X(x4-120),yjb),'Ø600 m6','cyl','0.02',pref=-60)
auto_leader((X(-x2+50),ycb),'2X Ø780',pref=-100)
auto_leader((X(250),S.P((0,0,-M.D_SEAT/2))[1]),'Ø700 s6',pref=-75)
auto_leader((X(-x3+10),S.P((0,0,-M.D_JRN/2-10))[1]),'2X 20 X 45°',pref=-150)
auto_leader((X(x2-2),S.P((0,0,-(M.D_COL/2-31)))[1]),'2X Ø720',pref=-30)
for sg_ in (-1,1):
    auto_surf([(X(sg_*u),yj,False) for u in range(int(x3+20),int(x4-20),20)]+[(X(sg_*u),yjb,True) for u in range(int(x3+20),int(x4-20),20)],'0.8')
auto_fcf((X(-300),S.P((0,0,-M.D_SEAT/2))[1]),'trun','0.03',('A-B',),pref=-60,rmax=80)
auto_fcf((X(-x1-60),S.P((0,0,M.D_COL/2-10))[1]),'perp','0.03',('A-B',),pref=135,prefix='2X',rmax=70)
auto_surf([(X(u),S.P((0,0,M.D_SEAT/2))[1],False) for u in range(-540,560,40)]+[(X(u),S.P((0,0,-M.D_SEAT/2))[1],True) for u in range(-540,560,40)],'1.6')
vlabel(cs[0],S.P((0,0,-M.D_COL/2))[1]+36,'POROS ROL','1:10')
I=View((-1.0,1.4,0.8),(-1,-0.7,0),30.0,110,236,name='iso')
I.iso([shf])
finish('s07')
