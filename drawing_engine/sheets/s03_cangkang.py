# -*- coding: utf-8 -*-
from common import *
import models as M
from vw import cl
from sym import *
sh.frame(3,'Cangkang Kiln','','1:250','R01-101','GAMBAR BAGIAN',material='ASTM A36',mass='477 t',treat='—')
ri=M.DSI/2; ro=ri+M.TSH; rt=ri+M.TTY; tl=(M.TTY-M.TSH)*M.TAPER
S=250.0; ox,oy=36.0,86.0
E=lambda x,r:(ox+x/S, oy-r/S)
segs=[]; cur=0.0
zones=[(xt-1500-tl,xt+1500+tl) for xt in M.XT]
def courses(x0,x1):
    n=max(1,math.ceil((x1-x0)/3000)); Lc=round((x1-x0)/n); out=[]; x=x0
    for i in range(n):
        xe_=x1 if i==n-1 else x+Lc; out.append((x,xe_,'38')); x=xe_
    return out
for a,b in zones:
    segs+=courses(cur,a)
    segs.append((a,a+tl,'tr')); segs.append((a+tl,b-tl,'90')); segs.append((b-tl,b,'tr')); cur=b
segs+=courses(cur,M.LK)
def rad(x):
    for a,b,k in segs:
        if a<=x<=b:
            if k=='38': return ro
            if k=='90': return rt
            f=(x-a)/(b-a); prev=[s for s in segs if s[1]==a]
            return ro+(rt-ro)*(f if prev and prev[0][2]=='38' else 1-f)
    return ro
xs=sorted(set([p for s in segs for p in s[:2]]))
for sg in (1,-1): L([E(x,sg*rad(x)) for x in xs],.5)
L([E(0,ro),E(0,-ro)],.5); L([E(M.LK,ro),E(M.LK,-ro)],.5)
for a,b,k in segs: L([E(a,rad(a)),E(a,-rad(a))],.25)
with own(None,'cl'):
    L([E(0,ri),E(M.LK,ri)],.25,[2,1],'sig'); L([E(0,-ri),E(M.LK,-ri)],.25,[2,1],'sig')
view_box('cangkang',(E(0,0)[0],E(0,rt)[1],E(M.LK,0)[0],E(0,-rt)[1]))
cl(E(-2500,0),E(M.LK+2500,0))
for a,b,k in segs:
    if k in ('38','90'):
        p=E((a+b)/2,0); TC(p[0],p[1]+7,k,3.0,'m',owner=('t',a))
ys=oy-rt/S-12
pts=[0.0]+[p for z_ in zones for p in z_]+[M.LK]
for i in range(len(pts)-1):
    dim_h(E(pts[i],0)[0],E(pts[i+1],0)[0],ys,fn(pts[i+1]-pts[i]),E(0,rad(pts[i]+1))[1],E(0,rad(pts[i+1]-1))[1])
dim_h(E(0,0)[0],E(M.LK,0)[0],ys-11,fn(M.LK),E(0,ro)[1],E(0,ro)[1])
ys2=oy+rt/S+25
for a,b,k in segs:
    if k=='38': dim_h(E(a,0)[0],E(b,0)[0],ys2,fn(b-a),E(0,-rad(a+1))[1],E(0,-rad(b-1))[1],out=True,size=3.0)
cf=E(M.XT[1]-1500-tl/2,-rad(M.XT[1]-1500-tl/2)); detcircle(cf[0],cf[1],4.5,'F',ang=-50)
cutplane(E(27900,0)[0],oy-ro/S-5,oy+ro/S+3,'E',-1)
T(E(M.LK,0)[0],oy+rt/S+36,'ANGKA DI DALAM COURSE = TEBAL PELAT',3.0,'r',owner='tp')
vlabel(E(M.LK/2,0)[0]-40,oy+rt/S+37,'CANGKANG (TAMPAK)','1:250')
# ---- detail F 1:5
S2=5.0; fx,fy=80.0,206.0
F_=lambda u,v:(fx+u/S2, fy-v/S2)
p90=[(-250,0),(0,0),(0,M.TTY),(-250,M.TTY)]; p38=[(0,0),(420,0),(420,M.TSH),(tl,M.TSH),(0,M.TTY)]
for poly,an in ((p90,45),(p38,135)):
    P_=[F_(u,v) for u,v in poly]; PG(P_,.5,None); hatch([P_],an,2.0)
breakline(F_(-250,-12),F_(-250,M.TTY+12)); breakline(F_(420,-12),F_(420,M.TSH+12))
L([F_(0,0),F_(0,M.TTY)],.6)
view_box('F',(F_(-250,0)[0],F_(0,M.TTY)[1],F_(420,0)[0],F_(0,0)[1]))
dim_v(F_(0,M.TTY)[1],F_(0,0)[1],F_(-250,0)[0]-10,fn(M.TTY),F_(-250,0)[0],F_(-250,0)[0],side=-1)
dim_v(F_(0,M.TSH)[1],F_(0,0)[1],F_(420,0)[0]+10,fn(M.TSH),F_(420,0)[0],F_(420,0)[0],out=True)
dim_h(F_(0,0)[0],F_(tl,0)[0],F_(0,M.TTY)[1]-12,fn(tl),F_(0,M.TTY)[1],F_(tl,M.TSH)[1])
T(F_(0,0)[0],F_(0,0)[1]+7.5,'SISI DALAM RATA',3.0,'m',owner='sd')
auto_leader(F_(tl/2,(M.TTY+M.TSH)/2),'KEMIRINGAN 1:4',pref=40)
weld(F_(0,M.TTY)[0],F_(0,M.TTY)[1],F_(0,M.TTY)[0]-14,F_(0,M.TTY)[1]-18,'',both=True,kind='V',right=False)
T(F_(0,M.TTY)[0]-14-11,F_(0,M.TTY)[1]-18-6.0,'60°',3.0,'m',owner='wa1'); T(F_(0,M.TTY)[0]-14-11,F_(0,M.TTY)[1]-18+9.6,'60°',3.0,'m',owner='wa2')
vlabel(fx+17,F_(0,0)[1]+14,'DETAIL F','1:5')
# ---- potongan E-E 1:100
S4=100.0; ex,ey=344.0,152.0
cc=[(ex+ro/S4*math.cos(math.radians(t)),ey-ro/S4*math.sin(math.radians(t))) for t in range(0,361,3)]
ci=[(ex+ri/S4*math.cos(math.radians(t)),ey-ri/S4*math.sin(math.radians(t))) for t in range(0,361,3)]
L(cc,.5); L(ci,.5); hatch([cc[:-1],ci[:-1]],45,0.25)
cline((ex-38,ey),(ex+38,ey)); cline((ex,ey-38),(ex,ey+38))
view_box('E-E',(ex-ro/S4,ey-ro/S4,ex+ro/S4,ey+ro/S4))
dim_h(ex-ro/S4,ex+ro/S4,ey-ro/S4-10,'Ø'+fn(2*ro),ey,ey,tdx=-12)
auto_leader((ex+ri/S4*math.cos(math.radians(60)),ey-ri/S4*math.sin(math.radians(60))),'Ø'+fn(2*ri),pref=30)
vlabel(ex,ey+ro/S4+7,'POTONGAN E-E','1:100')
finish('s03')
