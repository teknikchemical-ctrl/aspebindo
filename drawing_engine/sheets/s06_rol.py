# -*- coding: utf-8 -*-
from common import *
import models as M
from vw import View, cl
from sym import *
rol=M.roller(); shf=M.shaft()
mr=rol.val().Volume()*7.85e-9
sh.frame(6,'Rol Penumpu','','1:15','R01-104','GAMBAR BAGIAN',material='ZG42CrMo, ≥ 200 HB',mass=f'{mr:.1f} t',treat='N+T')
SC=15.0; h=M.BR/2; r=M.DR/2
# ---- potongan C-C (rol saja, lubang Ø700 H7)
C=View((0,-1,0),(1,0,0),SC,118,138,name='C-C')
C.section(rol,(0,0,0),hatch_sp=2.4,ang=45,draw_rest=True); kd.OPEN_VIEWS.add('C-C')
c=C.P((0,0,0)); cl((c[0]-48,c[1]),(c[0]+48,c[1])); cl((c[0],c[1]-104),(c[0],c[1]+104))
yt=C.P((0,0,r))[1]; yb=C.P((0,0,-r))[1]; xL=C.P((-h,0,0))[0]; xR=C.P((h,0,0))[0]
dim_h(xL,xR,yt-24,fn(M.BR)+' ±0.5',yt,yt)
dim_v(yt,yb,xR+14,'Ø'+fn(M.DR)+' h9',xR,xR,tdy=-40)
dim_v(C.P((0,0,M.RIM_ID/2))[1],C.P((0,0,-M.RIM_ID/2))[1],xL-28,'Ø'+fn(M.RIM_ID),xL,xL,tdy=-40)
dim_v(C.P((0,0,M.HUB_OD/2))[1],C.P((0,0,-M.HUB_OD/2))[1],xL-14,'Ø'+fn(M.HUB_OD),xL,xL,tdy=-14)
dim_v(C.P((0,0,M.D_SEAT/2))[1],C.P((0,0,-M.D_SEAT/2))[1],xR+28,'Ø'+fn(M.D_SEAT)+' H7',xR,xR,tdy=0)
yw=C.P((0,0,-(M.HUB_OD/2+M.RIM_ID/2)/2))[1]
dim_h(C.P((-M.WEB_T/2,0,0))[0],C.P((M.WEB_T/2,0,0))[0],yb+10,fn(M.WEB_T),yw,yw)
auto_leader(C.P((h-8,0,-r+8)),'2X 25 X 45°',pref=-45)
auto_leader(C.P((-M.WEB_T/2,0,(M.RIM_ID/2-120))),'4X Ø'+fn(M.RIM_ID-240),pref=200,rmin=6,rmax=30)
auto_leader(C.P((-M.WEB_T/2,0,(M.HUB_OD/2+120))),'4X Ø'+fn(M.HUB_OD+240),pref=160,rmin=6,rmax=30)
datum(c[0]+6,C.P((0,0,M.D_SEAT/2))[1],'A',(0.0,1.0)) if False else datum(C.P((-200,0,0))[0],C.P((0,0,-M.D_SEAT/2))[1],'A',(0,-1))
auto_fcf((C.P((-250,0,0))[0],yt),'trun','0.2',('A',),pref=60,rmax=60)
auto_fcf((xL,C.P((0,0,r-120))[1]),'perp','0.1',('A',),pref=170,prefix='2X')
auto_surf([(C.P((xx,0,0))[0],yt,False) for xx in (300,150,-100,-300)]+[(C.P((xx,0,0))[0],yb,True) for xx in (300,150,-100)],'1.6')
vlabel(c[0],yb+16,'POTONGAN C-C','1:15')
# ---- isometri
I=View((-1.0,1.4,0.8),(-1,-0.7,0),30.0,320,128,name='iso')
I.iso([rol])
auto_surf([(C.P((u,0,0))[0],C.P((0,0,M.D_SEAT/2))[1],True) for u in range(-500,520,40)],'1.6')
finish('s06')
