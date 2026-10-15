# -*- coding: utf-8 -*-
from common import *
import models as M, cadquery as cq
from vw import View, cl
from sym import *
P=M.station()
asm=[P[k] for k in ('shell','tyre','fb','sb','rollers','frame','thrust','pier')]
ms=sum(P[k].val().Volume() for k in ('tyre','fb','sb','rollers','frame','thrust'))*7.85e-9
sh.frame(2,'Stasiun Penumpu','Stasiun 2 dengan Rol Dorong','1:100','R01-100','GAMBAR SUSUNAN',material='Lihat daftar bagian',mass=f'{ms:.0f} t (baja)',treat='—')
SC=100.0
# ================= POTONGAN A-A (tegak lurus sumbu kiln)
F=View((-1,0,0),(0,-1,0),SC,78,84,name='A-A')
F.section(asm,(0,0,0),hatch_sp=1.8)
c=F.P((0,0,0))
cl((c[0]-50,c[1]),(c[0]+50,c[1])); cl((c[0],c[1]-50),(c[0],F.P((0,0,-M.RY-M.HB_H-M.BF_H))[1]+4))
for sy in (-1,1):
    rc=F.P((0,sy*M.RX,-M.RY))
    cl((rc[0]-18,rc[1]),(rc[0]+18,rc[1])); cl((rc[0],rc[1]-18),(rc[0],rc[1]+18))
    with own(('garis-sudut',sy),'cl'): L([c,(c[0]+(rc[0]-c[0])*1.2,c[1]+(rc[1]-c[1])*1.2)],.25,CLD,'sig')
top=F.P((0,0,M.TY_OD/2))[1]
dim_h(F.P((0,M.TY_OD/2,0))[0],F.P((0,-M.TY_OD/2,0))[0],top-10,'Ø'+fn(M.TY_OD),c[1],c[1],tdx=-28)
ya=c[1]; yr=F.P((0,0,-M.RY))[1]; yf=F.P((0,0,-M.RY-M.HB_H-M.BF_H))[1]; ypb=F.P((0,0,-M.RY-M.HB_H-M.BF_H-1500))[1]
xedge=F.P((0,-(M.BF_LAT/2+200),0))[0]
xr=xedge+12
dim_v(ya,yr,xr,fn(M.RY),c[0]+50,F.P((0,-M.RX,0))[0]+18)
dim_v(yr,yf,xr,fn(M.HB_H+M.BF_H),F.P((0,-M.RX,0))[0]+18,xedge)
dim_v(yf,ypb,xr+12,'1500',xedge,xedge)
xa=F.P((0,M.RX,0))[0]; xb=F.P((0,-M.RX,0))[0]
dim_h(xa,xb,ypb+10,fn(2*M.RX),yr+18,yr+18)
dim_h(F.P((0,M.BF_LAT/2+200,0))[0],xedge,ypb+20,fn(M.BF_LAT+400),ypb,ypb)
angdim(c,20,-90,-60,'30°',owner='a1'); angdim(c,20,-120,-90,'30°',owner='a2')
rcL=F.P((0,M.RX,-M.RY)); r_=M.DR/2/SC
ang=lambda a,r:(c[0]+r/SC*math.cos(math.radians(a)),c[1]-r/SC*math.sin(math.radians(a)))
auto_balloon('2',ang(152,M.DSI/2+M.TTY+35),pref=165,rmax=60)
auto_balloon('4',ang(200,M.DSI/2+45),pref=190,rmax=60)
auto_balloon('5',F.P((0,M.RX+800,-M.RY-500)),pref=200,rmax=60)
auto_balloon('10',F.P((0,M.BF_LAT/2-200,-M.RY-M.HB_H-M.BF_H-800)),pref=200,rmax=60)
vlabel(c[0],ypb+28,'POTONGAN A-A','1:100')
# ================= TAMPAK SAMPING
S=View((0,1,0),(-1,0,0),SC,190,84,name='samping')
S.draw(asm,hidden=False)
cs=S.P((0,0,0)); cl((cs[0]-30,cs[1]),(cs[0]+30,cs[1]))
rcs=S.P((0,0,-M.RY)); cl((rcs[0]-22,rcs[1]),(rcs[0]+22,rcs[1]))
tt=S.P((0,0,M.TY_OD/2))[1]
dim_h(S.P((M.TY_W/2,0,0))[0],S.P((-M.TY_W/2,0,0))[0],tt-10,fn(M.TY_W),tt,tt)
dim_h(S.P((M.SPAN_B/2,0,0))[0],S.P((-M.SPAN_B/2,0,0))[0],ypb+10,fn(M.SPAN_B),yr+10,yr+10)
dim_h(S.P((M.BF_AX/2+200,0,0))[0],S.P((-M.BF_AX/2-200,0,0))[0],ypb+20,fn(M.BF_AX+400),ypb,ypb)
auto_balloon('1',S.P((-M.TY_W/2,0,M.TY_OD/2-400)),pref=150,rmax=70)
auto_balloon('3',S.P((-M.TY_W/2-90,0,M.DSI/2+M.TTY+M.TFB+90)),pref=60,rmax=60)
auto_balloon('6',S.P((-(M.SPAN_B/2+M.L_JRN/2+60),M.RX,-M.RY)),pref=20,rmax=60)
auto_balloon('7',S.P((M.SPAN_B/2,M.RX,-M.RY+M.BRG_D/2+100)),pref=160,rmax=60)
auto_balloon('9',S.P((-(M.TY_W/2+380),0,-4300)),pref=-20,rmax=60)
vlabel(cs[0],ypb+28,'TAMPAK SAMPING','1:100')
# ================= DENAH
Pl=View((0,0,1),(0,-1,0),SC,78,236,name='denah')
Pl.draw([P[k] for k in ('tyre','rollers','frame','thrust','pier')],hidden=False)
cp=Pl.P((0,0,0)); cl((cp[0]-56,cp[1]),(cp[0]+56,cp[1]))
for sy in (-1,1):
    q=Pl.P((0,sy*M.RX,0)); cl((q[0],q[1]-22),(q[0],q[1]+22))
yp=Pl.P((-(M.BF_AX/2+200),0,0))[1]
cutplane_h(cp[1],Pl.P((0,M.BF_LAT/2+200,0))[0],Pl.P((0,-(M.BF_LAT/2+200),0))[0],'A',diry=-1)
auto_balloon('8',Pl.P((-(M.BF_AX/2)+150,M.BF_LAT/2-150,0)),pref=170,rmax=60)
dim_h(Pl.P((0,M.RX,0))[0],Pl.P((0,-M.RX,0))[0],yp+10,fn(2*M.RX),yp,yp)
dim_h(Pl.P((0,M.RX+M.BF_W/2,0))[0],Pl.P((0,M.RX-M.BF_W/2,0))[0],Pl.P((M.BF_AX/2+200,0,0))[1]-8,fn(M.BF_W),Pl.P((M.BF_AX/2,0,0))[1],Pl.P((M.BF_AX/2,0,0))[1])
vlabel(150,yp-20,'DENAH','1:100') if False else None
T(152,cp[1]-3,'DENAH',5.0,'l',owner='dn',kind='vl'); T(152,cp[1]+4.5,'SKALA 1:100',3.5,'l',owner='dn',kind='vl')
# ================= ISOMETRI + DAFTAR BAGIAN
I=View((-1.0,1.25,0.85),(-1,-0.8,0),150.0,0,0,name='iso')
I.fit(asm,(250,30,405,118)); I.iso(asm,tol=12,lmax=400)
rows=[['1','R01-102','Ban (*riding ring*)','1','ZG42CrMo, ≥ 200 HB'],
      ['2','R01-103','Bar pengisi','64','S355JR'],
      ['3','R01-103','Blok penahan','32','S355JR'],
      ['4','R01-101','Cangkang (referensi)','—','ASTM A36'],
      ['5','R01-104','Rol penumpu','2','ZG42CrMo, ≥ 200 HB'],
      ['6','R01-105','Poros rol','2','42CrMo4 Q+T'],
      ['7','PEMASOK','Rumah bantalan + bantalan rol','4','Baja cor (rakitan)'],
      ['8','R01-100','Rangka dasar (las)','2','S355JR'],
      ['9','PEMASOK','Rol dorong hidrolik','2','Rakitan'],
      ['10','SIPIL','Fondasi','1','Beton bertulang']]
kt.table(240.0,126.0,[9,22,66,10,59],['NO.','NO. GAMBAR','NAMA BAGIAN','JML.','BAHAN'],rows,size=3.0,aligns=['m','m','l','m','l'],minh=6.0,hdr_size=3.0,title='DAFTAR BAGIAN',tsize=3.5)
finish('s02')
