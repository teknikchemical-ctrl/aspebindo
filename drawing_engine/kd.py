# -*- coding: utf-8 -*-
"""Inti gambar teknik: registri geometri, dimensi ASME, rujukan, balon, pemeriksa kerapihan, penempatan otomatis."""
import sys, math
sys.path.insert(0,'.')
import eng
eng.W,eng.H=420.0,297.0
def _r1(s):
    out=[]
    for k,part in enumerate(s.split('₂')):
        if k>0: out.append(('2',True))
        if part: out.append((part,False))
    return out
eng._runs1=_r1
from eng import *
from reportlab.pdfbase import pdfmetrics as _pm
from reportlab.pdfbase.ttfonts import TTFont as _TT
import os as _os
_FD=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'fonts')+'/'
_pm.registerFont(_TT('OSI',_FD+'osifont-lgpl3fe.ttf')); _pm.registerFont(_TT('OSII',_FD+'osifont-italic.ttf'))
eng.font=lambda bold,ital=False:'OSII' if ital else 'OSI'
EMF=1/0.7373
_tw=eng.twidth
def twidth(s,size,bold=False,ital=False): return _tw(s,size*EMF,bold,ital)
d=Doc()
# ======================================================================= registri
SEG=[]          # (a,b,kind,owner)   kind: obj hat cl dl ext ld bal arr frm tbl
GRID={}; GS=6.0
ZONES=[]        # (bb,name) area terlarang bagi teks/tampak
VIEWS=[]        # (bb,name)
BALL=[]         # (cx,cy,r,num)
_OWN=[None]; _KIND=[None]
class own:
    def __init__(s,owner,kind=None): s.o=owner; s.k=kind
    def __enter__(s): _OWN.append(s.o); _KIND.append(s.k)
    def __exit__(s,*a): _OWN.pop(); _KIND.pop()
_LK={'equip':'obj','proc':'hat','sig':'cl','inst':'dl','frame':'frm','table':'tbl','util':'iso','label':'lbl'}
def _cells(x0,y0,x1,y1):
    for i in range(int(math.floor(min(x0,x1)/GS)),int(math.floor(max(x0,x1)/GS))+1):
        for j in range(int(math.floor(min(y0,y1)/GS)),int(math.floor(max(y0,y1)/GS))+1):
            yield (i,j)
def regseg(a,b,kind,owner=None):
    k=len(SEG); SEG.append((a,b,kind,owner))
    for c in _cells(a[0],a[1],b[0],b[1]): GRID.setdefault(c,[]).append(k)
_line0=Doc.line; _poly0=Doc.poly; _circ0=Doc.circ
def _kind(layer,dash):
    k=_KIND[-1] or _LK.get(layer,'obj')
    if layer=='inst' and _KIND[-1] is None: k='dl'
    return k
def _line(s,pts,w=.35,dash=None,col=K,layer='equip',cap='butt',reg=True):
    _line0(s,pts,w,dash,col,layer,cap)
    if reg and layer not in ('util','label'):
        k=_kind(layer,dash)
        for i in range(len(pts)-1): regseg(tuple(pts[i]),tuple(pts[i+1]),k,_OWN[-1])
def _poly(s,pts,w=.35,fill=None,col=K,layer='equip',dash=None):
    _poly0(s,pts,w,fill,col,layer,dash)
    if layer=='util': return
    k=_kind(layer,dash)
    if layer=='inst' and fill==K and len(pts)==3: k='arr'
    if w>0 or k=='arr':
        n=len(pts)
        for i in range(n): regseg(tuple(pts[i]),tuple(pts[(i+1)%n]),k,_OWN[-1])
def _circ(s,cx,cy,r,lw=.35,fill=None,layer='equip',col=K):
    _circ0(s,cx,cy,r,lw,fill,layer,col)
    if lw>0 and layer!='util':
        k=_kind(layer,None); n=max(12,int(r*2))
        for i in range(n):
            a0=2*math.pi*i/n; a1=2*math.pi*(i+1)/n
            regseg((cx+r*math.cos(a0),cy+r*math.sin(a0)),(cx+r*math.cos(a1),cy+r*math.sin(a1)),k,_OWN[-1])
Doc.line=_line; Doc.poly=_poly; Doc.circ=_circ
def fn(v,dec=0): return f'{v:.{dec}f}'
# ======================================================================= primitif
def L(pts,w=.5,dash=None,layer='equip',col=K,reg=True,cap='butt'):
    d.line(pts,w,dash,col,layer,cap,reg=reg or layer=='inst')
def PG(pts,w=.5,fill=None,layer='equip',dash=None,reg=True):
    d.poly(pts,w,fill,K,layer,dash)
def C(cx,cy,r,w=.5,fill=None,layer='equip',reg=True):
    d.circ(cx,cy,r,w,fill,layer)
def T(x,y,t,size=3.5,a='l',b=False,rot=0,owner=None,ital=False,chk=True,layer='label',kind=None):
    bb=d.text(x,y,t,size*EMF,a,b,rot=rot,layer=layer,owner=owner if owner is not None else _OWN[-1],ital=ital,chk=chk,pad=.35)
    if chk:
        d.texts[-1]['h']=size; d.texts[-1]['kind']=kind or ('frm' if layer=='frame' else 'tbl' if layer=='table' else 'txt')
    return bb
def TC(x,y,t,size=3.5,a='m',b=False,rot=0,owner=None,chk=True,layer='label',kind=None):
    return T(x,y+0.5*size,t,size,a,b,rot,owner,chk=chk,layer=layer,kind=kind)
def hatch(rings,ang=45,sp=2.0,w=.18,layer='proc',dash=None):
    ca,sa=math.cos(math.radians(ang)),math.sin(math.radians(ang))
    rot=lambda p:(p[0]*ca+p[1]*sa,-p[0]*sa+p[1]*ca)
    inv=lambda p:(p[0]*ca-p[1]*sa,p[0]*sa+p[1]*ca)
    R=[[rot(p) for p in r] for r in rings]
    ys=[p[1] for r in R for p in r]; y0,y1=min(ys),max(ys)
    y=math.floor(y0/sp)*sp+sp/2
    while y<y1:
        xs=[]
        for r in R:
            n=len(r)
            for i in range(n):
                a,b=r[i],r[(i+1)%n]
                if (a[1]<=y<b[1]) or (b[1]<=y<a[1]):
                    t=(y-a[1])/(b[1]-a[1]); xs.append(a[0]+t*(b[0]-a[0]))
        xs.sort()
        for i in range(0,len(xs)-1,2):
            if xs[i+1]-xs[i]>.3: d.line([inv((xs[i],y)),inv((xs[i+1],y))],w,dash,K,'proc')
        y+=sp
CLD=[8,1.5,1.5,1.5]
def cline(p0,p1,w=.25):
    with own(None,'cl'): L([p0,p1],w,CLD,'sig')
# ======================================================================= dimensi ASME
ARW=3.0
def arrow(x,y,ux,uy):
    with own(_OWN[-1],'arr'):
        d.poly([(x,y),(x-ux*ARW-uy*.5,y-uy*ARW+ux*.5),(x-ux*ARW+uy*.5,y-uy*ARW-ux*.5)],.05,K,K,'inst')
def _seg(p,q,kind):
    with own(_OWN[-1],kind): L([p,q],.25,None,'inst')
def dim_h(x1,x2,y,text,yobj1=None,yobj2=None,size=3.5,ext=2.5,out=False,tdx=0,owner=None):
    owner=owner or ('dim',round(x1,1),round(x2,1),round(y,1))
    if x1>x2: x1,x2=x2,x1
    with own(owner):
        for xo,yo in ((x1,yobj1),(x2,yobj2)):
            if yo is not None:
                s=1 if y>yo else -1
                _seg((xo,yo+s*1.5),(xo,y+s*ext),'ext')
        tw=twidth(text,size); gap=tw+2.4
        if abs(x2-x1)>=gap+2*ARW+2 and not out:
            tx=min(max((x1+x2)/2+tdx,x1+ARW+1+gap/2),x2-ARW-1-gap/2)
            arrow(x1,y,-1,0); arrow(x2,y,1,0)
            _seg((x1,y),(tx-gap/2,y),'dl'); _seg((tx+gap/2,y),(x2,y),'dl')
            TC(tx,y,text,size,'m',owner=owner)
        else:
            arrow(x1,y,1,0); arrow(x2,y,-1,0)
            _seg((x1-ARW*2.2,y),(x2+ARW*2.2,y),'dl')
            if out=='left': TC(x1-ARW*2.2-1.2,y,text,size,'r',owner=owner)
            elif out=='right': TC(x2+ARW*2.2+1.2,y,text,size,'l',owner=owner)
            else: T((x1+x2)/2+tdx,y-2.0,text,size,'m',owner=owner)
def dim_v(y1,y2,x,text,xobj1=None,xobj2=None,size=3.5,ext=2.5,out=False,tdy=0,side=1,owner=None):
    owner=owner or ('dimv',round(x,1),round(y1,1),round(y2,1))
    if y1>y2: y1,y2=y2,y1
    with own(owner):
        for yo,xo in ((y1,xobj1),(y2,xobj2)):
            if xo is not None:
                s=1 if x>xo else -1
                _seg((xo+s*1.5,yo),(x+s*ext,yo),'ext')
        tw=twidth(text,size); gap=size+2.6
        ty=(y1+y2)/2+tdy
        if abs(y2-y1)>=gap+2*ARW+2 and not out:
            ty=min(max(ty,y1+ARW+1+gap/2),y2-ARW-1-gap/2)
            arrow(x,y1,0,-1); arrow(x,y2,0,1)
            _seg((x,y1),(x,ty-gap/2),'dl'); _seg((x,ty+gap/2),(x,y2),'dl')
            d.rect(x-tw/2-0.8,ty-size/2-0.8,tw+1.6,size+1.6,0,'#ffffff','inst')
            TC(x,ty,text,size,'m',owner=owner)
        else:
            arrow(x,y1,0,1); arrow(x,y2,0,-1)
            _seg((x,y1-ARW*2.2),(x,y2+ARW*2.2),'dl')
            if side>0: TC(x+1.6,ty,text,size,'l',owner=owner)
            else: TC(x-1.6,ty,text,size,'r',owner=owner)
def leader(px,py,tx,ty,text,size=3.5,anchor='l',shoulder=4.0,dot=False,owner=None,lines=None):
    owner=owner or ('ld',round(px,1),round(py,1))
    with own(owner):
        _seg((px,py),(tx,ty),'ld')
        ex=tx+shoulder if anchor=='l' else tx-shoulder
        _seg((tx,ty),(ex,ty),'ld')
        if dot: d.circ(px,py,.55,.05,K,'inst')
        else:
            dx,dy=px-tx,py-ty; n=math.hypot(dx,dy) or 1; arrow(px,py,dx/n,dy/n)
        ls=lines or [text]; lh=size*1.7
        for i,l_ in enumerate(ls):
            TC(ex+(1.2 if anchor=='l' else -1.2),ty+(i-(len(ls)-1)/2)*lh,l_,size,anchor,owner=owner)
BR=5.0
def balloon(num,bx,by,px,py,r=BR,size=4.0):
    owner=('bal',num,round(bx,1),round(by,1))
    with own(owner,'bal'):
        d.circ(bx,by,r,.35,'#ffffff','inst')
        dxx,dyy=px-bx,py-by; n=math.hypot(dxx,dyy) or 1
        _seg((bx+dxx/n*r,by+dyy/n*r),(px,py),'bal')
        d.circ(px,py,.65,.05,K,'inst')
    TC(bx,by,str(num),size,'m',owner=owner,kind='bal')
    BALL.append((bx,by,r,num))
def vlabel(cx,y,text,scale=None,size=5.0):
    T(cx,y+size,text,size,'m',owner=('vl',text),kind='vl')
    if scale: T(cx,y+size+2.4+3.5,'SKALA '+scale,3.5,'m',owner=('vl',text),kind='vl')
def view_box(name,bb):
    VIEWS.append((bb,name))
def zone(name,bb): ZONES.append((bb,name))
# ======================================================================= geometri bantu
def _segs_near(bb):
    ks=set()
    for c in _cells(bb[0],bb[1],bb[2],bb[3]): ks.update(GRID.get(c,()))
    return ks
def seg_box2(a,b,bb):
    # Liang-Barsky clip
    x0,y0,x1,y1=bb; dx=b[0]-a[0]; dy=b[1]-a[1]; t0,t1=0.0,1.0
    for p,q in ((-dx,a[0]-x0),(dx,x1-a[0]),(-dy,a[1]-y0),(dy,y1-a[1])):
        if abs(p)<1e-12:
            if q<0: return False
        else:
            t=q/p
            if p<0:
                if t>t1: return False
                t0=max(t0,t)
            else:
                if t<t0: return False
                t1=min(t1,t)
    return t0<=t1
def seg_x(a,b,c,d_,eps=1e-6):
    def orient(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    o1=orient(a,b,c); o2=orient(a,b,d_); o3=orient(c,d_,a); o4=orient(c,d_,b)
    return (o1*o2< -eps) and (o3*o4< -eps)
def inflate(bb,m): return (bb[0]-m,bb[1]-m,bb[2]+m,bb[3]+m)
def bb_ov(a,b,m=0): return a[0]<b[2]+m and b[0]<a[2]+m and a[1]<b[3]+m and b[1]<a[3]+m
CONTAINER=('balon','fcf','weld','nz')
# ======================================================================= pemeriksa kerapihan
CLR=0.6
def check(verbose=True,overlay=None):
    iss=[]
    TX=[t for t in d.texts]
    # R1 teks-teks
    for i in range(len(TX)):
        for j in range(i+1,len(TX)):
            a,b=TX[i],TX[j]
            if a.get('owner') is not None and a.get('owner')==b.get('owner'): continue
            if bb_ov(a['bb'],b['bb'],CLR*0.5): iss.append(('teks-teks',a['t'],b['t'],a['bb']))
    # R2 teks vs garis
    for t in TX:
        bb=inflate(t['bb'],-0.05); kind=t.get('kind','txt')
        for k in _segs_near(bb):
            a,b,sk,ow=SEG[k]
            if ow is not None and ow==t.get('owner'): continue
            if kind in ('frm','tbl') and sk in ('frm','tbl'): continue
            if kind=='bal' and sk in ('bal',): continue
            if seg_box2(a,b,bb): iss.append(('teks-garis:'+sk,t['t'],'',t['bb'])); break
    # R3 zona terlarang & di luar bingkai
    for t in TX:
        if t.get('kind') in ('frm','tbl'): continue
        for zb,zn in ZONES+SOLIDS:
            if bb_ov(t['bb'],zb): iss.append(('teks-zona',t['t'],zn,t['bb']))
        bb=t['bb']
        if bb[0]<10.5 or bb[2]>409.5 or bb[1]<10.5 or bb[3]>286.5: iss.append(('teks-luar-bingkai',t['t'],'',bb))
    # R4 persilangan rujukan / garis dimensi (pemilik berbeda)
    L_=[(k,s) for k,s in enumerate(SEG) if s[2] in ('ld','bal','dl')]
    seen=set()
    for k,(a,b,sk,ow) in L_:
        bb=(min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1]))
        for j in _segs_near(bb):
            if j<=k: continue
            c,e,sk2,ow2=SEG[j]
            if sk2 not in ('ld','bal','dl','ext') or ow2==ow: continue
            if sk2=='ext' and sk=='dl': continue
            if seg_x(a,b,c,e):
                key=(str(ow),str(ow2))
                if key in seen: continue
                seen.add(key); iss.append(('silang:'+sk+'/'+sk2,str(ow)[:30],str(ow2)[:30],bb))
    # R5 jarak balon
    for i in range(len(BALL)):
        for j in range(i+1,len(BALL)):
            a,b=BALL[i],BALL[j]
            if math.hypot(a[0]-b[0],a[1]-b[1])<a[2]+b[2]+1.5: iss.append(('balon-dempet',a[3],b[3],(a[0]-5,a[1]-5,a[0]+5,a[1]+5)))
    # R6 tampak saling tumpang / menabrak zona
    for i in range(len(VIEWS)):
        for j in range(i+1,len(VIEWS)):
            if bb_ov(VIEWS[i][0],VIEWS[j][0],4): iss.append(('tampak-tumpang',VIEWS[i][1],VIEWS[j][1],VIEWS[i][0]))
        for zb,zn in ZONES:
            if bb_ov(VIEWS[i][0],zb,2): iss.append(('tampak-zona',VIEWS[i][1],zn,VIEWS[i][0]))
    # R7 tinggi huruf
    for t in TX:
        h=t.get('h',3.5); kind=t.get('kind','txt')
        lim=2.0 if kind in ('frm',) else 2.5 if kind=='tbl' else 3.0
        if h<lim-1e-6: iss.append(('huruf-kecil',t['t'],h,t['bb']))
    if verbose:
        for q in iss[:60]: print('  !',q[:3])
        if len(iss)>60: print('  ... +',len(iss)-60)
    if overlay:
        for q in iss:
            bb=q[3]; d.rect(bb[0]-.5,bb[1]-.5,bb[2]-bb[0]+1,bb[3]-bb[1]+1,.4,None,'label','#ff0000')
    return iss
# ======================================================================= penempatan otomatis
OPEN_VIEWS=set()
SOLIDS=[]   # persegi badan benda (tampak terbuka) - teks dilarang di dalamnya
def solid_profile(V,prof):
    for (u0,r0),(u1,r1) in zip(prof,prof[1:]):
        if abs(u1-u0)<1: continue
        r=min(r0,r1)
        if r<1: continue
        a=V.P((u0,0,r)); b=V.P((u1,0,-r))
        SOLIDS.append(((min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])),'BENDA'))
def free_box(bb,owner=None,ignore=(),allow=()):
    if bb[0]<11 or bb[2]>409 or bb[1]<11 or bb[3]>286: return False
    for zb,zn in ZONES+SOLIDS:
        if bb_ov(bb,zb,0.8): return False
    for vb,vn in VIEWS:
        if vn in ignore or vn in OPEN_VIEWS: continue
        if bb_ov(bb,vb,1.0): return False
    for t in d.texts:
        if bb_ov(bb,t['bb'],CLR): return False
    for k in _segs_near(inflate(bb,CLR)):
        a,b,sk,ow=SEG[k]
        if sk in allow: continue
        if seg_box2(a,b,inflate(bb,CLR)): return False
    for bx,by,r,n in BALL:
        if bb_ov(bb,(bx-r,by-r,bx+r,by+r),1.0): return False
    return True
def free_line(p,q,kinds=('ld','bal','dl','ext','obj','hat','frm','tbl','arr'),skip_end=1.2,ignore_obj_near_target=True):
    """garis rujukan tidak boleh memotong rujukan/dimensi lain; boleh memotong objek hanya dekat titik sasaran"""
    bb=(min(p[0],q[0]),min(p[1],q[1]),max(p[0],q[0]),max(p[1],q[1]))
    for k in _segs_near(bb):
        a,b,sk,ow=SEG[k]
        if sk not in kinds: continue
        if sk in ('obj','hat'):
            continue
        if seg_x(p,q,a,b): return False
    for t in d.texts:
        if seg_box2(p,q,inflate(t['bb'],0.8)): return False
    for bx,by,r,n in BALL:
        # jarak titik ke segmen
        vx,vy=q[0]-p[0],q[1]-p[1]; L2=vx*vx+vy*vy or 1
        t_=max(0,min(1,((bx-p[0])*vx+(by-p[1])*vy)/L2)); cx,cy=p[0]+t_*vx,p[1]+t_*vy
        if math.hypot(bx-cx,by-cy)<r+0.8: return False
    return True
def obj_cross_count(p,q,kinds=('obj',)):
    bb=(min(p[0],q[0]),min(p[1],q[1]),max(p[0],q[0]),max(p[1],q[1])); n=0
    for k in _segs_near(bb):
        a,b,sk,ow=SEG[k]
        if sk in kinds and seg_x(p,q,a,b): n+=1
    return n
def auto_balloon(num,target,pref=45,rmin=12,rmax=46,r=BR,region=None,avoid_obj=True):
    """cari posisi balon bebas tabrakan di sekitar sasaran; pref = sudut arah layar (derajat, CCW, 0 = kanan)"""
    best=None
    for dist in [rmin+4*i for i in range(int((rmax-rmin)/4)+1)]:
        for da in [0,15,-15,30,-30,45,-45,60,-60,75,-75,90,-90,120,-120,150,-150,180]:
            a=math.radians(pref+da)
            bx=target[0]+dist*math.cos(a); by=target[1]-dist*math.sin(a)
            bb=(bx-r-0.5,by-r-0.5,bx+r+0.5,by+r+0.5)
            if region and not (region[0]<=bx<=region[2] and region[1]<=by<=region[3]): continue
            if not free_box(bb): continue
            # garis rujukan dari tepi balon
            ux,uy=target[0]-bx,target[1]-by; n=math.hypot(ux,uy) or 1
            p=(bx+ux/n*r,by+uy/n*r)
            if not free_line(p,target): continue
            sc=dist*0.6+abs(da)*0.25+(obj_cross_count(p,target)*15 if avoid_obj else 0)
            if best is None or sc<best[0]: best=(sc,bx,by)
        if best and best[0]<dist*0.6+12: break
    if best is None:
        print('  ! balon',num,'tidak menemukan posisi bebas'); bx=target[0]+rmin; by=target[1]-rmin
    else: _,bx,by=best
    balloon(num,bx,by,target[0],target[1],r)
    return bx,by
def auto_leader(target,text,pref=45,rmin=10,rmax=50,size=3.5,lines=None,dot=False,region=None,below=None):
    ls=lines or [text]; tw=max(twidth(l,size) for l in ls); th=size*1.7*(len(ls)-1)+size
    best=None
    for dist in [rmin+4*i for i in range(int((rmax-rmin)/4)+1)]:
        for da in [0,15,-15,30,-30,45,-45,60,-60,90,-90,120,-120,150,-150,180]:
            a=math.radians(pref+da)
            tx=target[0]+dist*math.cos(a); ty=target[1]-dist*math.sin(a)
            an='l' if math.cos(a)>=0 else 'r'
            ex=tx+4 if an=='l' else tx-4
            x0=ex+1.2 if an=='l' else ex-1.2-tw
            bb=(min(x0,tx)-0.4,ty-(th-size)/2-0.55*size-0.5,max(x0+tw,tx)+0.4,ty+(th-size)/2+0.85*size+0.5)
            if below:
                bW,bH=below
                bb=(bb[0],bb[1],max(bb[2],x0+bW+0.5),ty+4.4+bH+0.6)
                if seg_box2(target,(tx,ty),(x0-0.8,ty+3.6,x0+bW+0.8,ty+4.4+bH+0.8)): continue
            if region and not (region[0]<=bb[0] and bb[2]<=region[2] and region[1]<=bb[1] and bb[3]<=region[3]): continue
            if not free_box(bb): continue
            if not free_line(target,(tx,ty)): continue
            _n=math.hypot(tx-target[0],ty-target[1]) or 1
            _p=(target[0]+(tx-target[0])*4.0/_n,target[1]+(ty-target[1])*4.0/_n)
            sc=dist*0.6+abs(da)*0.25+obj_cross_count(_p,(tx,ty))*40+min(obj_cross_count(_p,(tx,ty),('hat',)),6)*8+(25 if abs(math.sin(a))<0.26 or abs(math.cos(a))<0.17 else 0)
            if best is None or sc<best[0]: best=(sc,tx,ty,an)
        if best and best[0]<dist*0.6+12: break
    if best is None:
        print('  ! label',text,'tidak menemukan posisi bebas'); tx,ty,an=target[0]+rmin,target[1]-rmin,'l'
    else: _,tx,ty,an=best
    leader(target[0],target[1],tx,ty,text,size,an,lines=lines,dot=dot)
    ex=tx+4 if an=='l' else tx-4
    return (tx,ty,an,ex,tw)
def boxlast(pad=0.9):
    """bingkai dimensi dasar (BASIC, ASME Y14.5) di sekeliling teks terakhir"""
    t=d.texts[-1]; x0,y0,x1,y1=t['bb']
    with own(t['owner'],'sym'):
        L([(x0-pad,y0-pad),(x1+pad,y0-pad),(x1+pad,y1+pad),(x0-pad,y1+pad),(x0-pad,y0-pad)],.3,None,'inst')
    t['bb']=(x0-pad-0.3,y0-pad-0.3,x1+pad+0.3,y1+pad+0.3)
