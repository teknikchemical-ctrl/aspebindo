# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
pn=M.pinion(); mp=pn.val().Volume()*7.85e-9
sh.frame(9,'Pinion Penggerak','','1:10','R01-107','GAMBAR BAGIAN',material='42CrMo4 (EN 10083-3)',mass=f'{mp:.1f} t',treat='Q+T 300–340 HB')
SC=10.0; h=M.BP/2
S=View((0,-1,0),(1,0,0),SC,150,112,name='pinion'); S.draw(pn,hidden=False); kd.OPEN_VIEWS.add('pinion')
_h=M.BP/2; _ra=M.DA1/2
kd.solid_profile(S,[(-_h-400,180),(-_h-100,180),(-_h-100,200),(-_h,200),(-_h,_ra),(_h,_ra),(_h,200),(_h+100,200),(_h+100,180),(_h+400,180),(_h+400,160),(_h+900,160)])
X=lambda u:S.P((u,0,0))[0]; Y=lambda z:S.P((0,0,z))[1]
cline((X(-h-430),Y(0)),(X(h+930),Y(0)))
# garis lingkaran jarak bagi (konvensional)
with own(None,'cl'): L([(X(-h),Y(M.D1/2)),(X(h),Y(M.D1/2))],.25,CLD,'sig'); L([(X(-h),Y(-M.D1/2)),(X(h),Y(-M.D1/2))],.25,CLD,'sig')
xs=[-h-400,-h-100,-h,h,h+100,h+400,h+900]
labs=['300','100',fn(M.BP),'100','300','500']
yt=Y(M.DA1/2)
for i in range(len(xs)-1): dim_h(X(xs[i]),X(xs[i+1]),yt-12,labs[i],Y(200) if i!=2 else yt,Y(200) if i+1!=3 else yt) if False else None
yd=yt-24
dim_h(X(-h-400),X(-h-100),yd,'300',Y(180),Y(200)); dim_h(X(-h-100),X(-h),yd,'100',Y(200),yt)
dim_h(X(-h),X(h),yd,fn(M.BP),yt,yt); dim_h(X(h),X(h+100),yd,'100',yt,Y(200)); dim_h(X(h+100),X(h+400),yd,'300',Y(200),Y(180)); dim_h(X(h+400),X(h+900),yd,'500',Y(180),Y(160))
dim_h(X(-h-400),X(h+900),yd-11,fn(2*h+1300),Y(180),Y(160))
# ---- potongan F-F pada alur pasak
XK=h+670.0
cutplane(X(XK),Y(160)-7,Y(-160)+7,'F',-1)
E=View((-1,0,0),(0,-1,0),SC,372,124,name='F-F')
E.section(pn,(XK,0,0),hatch_sp=2.0,draw_rest=False)
ce=E.P((0,0,0)); cline((ce[0]-22,ce[1]),(ce[0]+22,ce[1])); cline((ce[0],ce[1]-22),(ce[0],ce[1]+22))
yk=E.P((0,0,121))[1]; yb_=E.P((0,0,-160))[1]
xk1=E.P((0,40,0))[0]; xk2=E.P((0,-40,0))[0]
dim_h(xk1,xk2,E.P((0,0,160))[1]-10,'80 P9',E.P((0,0,158))[1],E.P((0,0,158))[1])
dim_v(yk,yb_,ce[0]+26,'281',xk2,ce[0]+2)
vlabel(ce[0],yb_+12,'POTONGAN F-F','1:10')
datum(X(-h-250),Y(-180),'A',(0,1)); datum(X(h+250),Y(-180),'B',(0,1))
auto_leader((X(-h-330),Y(-180)),'Ø360 m6',pref=-150)
auto_leader((X(h+330),Y(-180)),'Ø360 m6',pref=-30)
auto_leader((X(h+700),Y(-160)),'Ø320 k6',pref=-40)
dim_h(X(h+470),X(h+870),Y(160)-12,'400',Y(160),Y(160))
dim_h(X(h+870),X(h+900),Y(160)-12,'30',Y(160),Y(160),out='right')
auto_leader((X(-h-100+50),Y(200)),'2X Ø400',pref=120)
auto_leader((X(h-2),Y(_ra-2)),'2X 5 X 45°',pref=60)
auto_leader_fcf((X(120),Y(-_ra)),'Ø612 h11','trun','0.05',('A-B',),pref=-60,rmin=10)
auto_fcf((X(-h-150),Y(-180)),'cyl','0.01',(),pref=-60,rmax=70)
vlabel(X(250),Y(-M.DA1/2)+28,'PINION','1:10')
rows=[['Modul','m','36'],['Jumlah gigi','z','15'],['Sudut tekan','α','20°'],['Diameter jarak bagi','d','540'],['Diameter kepala','da','612'],
      ['Diameter kaki','df','450'],['Lebar gigi','b','900'],['Koefisien geser profil','x','0'],['Pasangan','—','R01-106, z 252'],['Kualitas (ISO 1328-1)','—','8'],['Kekasaran sayap gigi','Ra','1.6']]
kt.table(14.0,186.0,[64,14,46],['BESARAN','SIMBOL','NILAI'],rows,size=3.0,aligns=['l','m','m'],minh=5.6,hdr_size=3.0,title='DATA RODA GIGI',tsize=3.5)
I=View((-1.0,1.3,0.9),(-1,-0.8,0),30.0,0,0,name='iso'); I.fit(pn,(150,190,226,284)); I.iso(pn)
finish('s09')
