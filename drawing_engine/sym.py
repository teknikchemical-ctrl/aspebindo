# -*- coding: utf-8 -*-
"""Simbol ASME: GD&T (Y14.5-2018), tekstur permukaan (Y14.36), las (AWS A2.4), bidang potong (Y14.3), lingkar detail."""
from kd import *
import kd as _kd
FH=7.0
def _l(pts,w=.3): L(pts,w,None,'inst')
def _g(kind,cx,cy):
    w=.3
    if kind=='crun':
        _l([(cx-1.6,cy+1.8),(cx+1.2,cy-1.4)]); arrow(cx+1.6,cy-1.8,0.7071,-0.7071)
    elif kind=='trun':
        for dx in (-1.6,0.8):
            _l([(cx+dx-0.6,cy+1.6),(cx+dx+1.4,cy-1.2)]); arrow(cx+dx+1.8,cy-1.6,0.7071,-0.7071)
        _l([(cx-2.6,cy+1.6),(cx+1.2,cy+1.6)])
    elif kind=='par':
        for dx in (-.9,.9): _l([(cx+dx-.8,cy+1.8),(cx+dx+.8,cy-1.8)])
    elif kind=='perp':
        _l([(cx-2,cy+1.8),(cx+2,cy+1.8)]); _l([(cx,cy+1.8),(cx,cy-2.0)])
    elif kind=='cyl':
        d.circ(cx,cy,1.3,w,None,'inst'); _l([(cx-2.4,cy+1.8),(cx-0.6,cy-1.8)]); _l([(cx+0.6,cy+1.8),(cx+2.4,cy-1.8)])
    elif kind=='circ':
        d.circ(cx,cy,1.8,w,None,'inst')
    elif kind=='flat':
        d.poly([(cx-2.2,cy+1.1),(cx+1.1,cy+1.1),(cx+2.2,cy-1.1),(cx-1.1,cy-1.1)],w,None,K,'inst')
    elif kind=='pos':
        d.circ(cx,cy,1.6,w,None,'inst'); _l([(cx-2.4,cy),(cx+2.4,cy)]); _l([(cx,cy-2.4),(cx,cy+2.4)])
def fcf_size(tol,datums=(),dia=False):
    txt=('Ø' if dia else '')+tol
    return 8.0+twidth(txt,3.5)+4+sum(max(7.0,twidth(dd,3.5)+4) for dd in datums), FH
def fcf(x,y,kind,tol,datums=(),owner=None,lead=None,dia=False):
    ow=owner or ('fcf',round(x,1),round(y,1))
    txt=('Ø' if dia else '')+tol
    cells=[8.0,twidth(txt,3.5)+4]+[max(7.0,twidth(dd,3.5)+4) for dd in datums]
    W=sum(cells); xx=x
    with own(ow,'sym'):
        d.rect(x,y,W,FH,0,'#ffffff','inst'); d.rect(x,y,W,FH,.35,None,'inst')
        for i,cw in enumerate(cells):
            if i>0: _l([(xx,y),(xx,y+FH)],.35)
            if i==0: _g(kind,xx+cw/2,y+FH/2)
            xx+=cw
        if lead:
            px,py=lead
            sx=x if abs(px-x)<=abs(px-(x+W)) else x+W
            q=(sx+(-4 if sx==x else 4),y+FH/2)
            with own(ow,'ld'):
                _l([(sx,y+FH/2),q],.25); _l([q,(px,py)],.25)
                dx,dy=px-q[0],py-q[1]; n=math.hypot(dx,dy) or 1; arrow(px,py,dx/n,dy/n)
    xx=x
    for i,cw in enumerate(cells):
        if i==1: TC(xx+cw/2,y+FH/2,txt,3.5,'m',owner=ow)
        elif i>1: TC(xx+cw/2,y+FH/2,datums[i-2],3.5,'m',owner=ow)
        xx+=cw
    d.texts.append(dict(bb=(x,y,x+W,y+FH),t='fcf',owner=ow,layer='inst',h=3.5,kind='sym'))
    return W
def auto_fcf(target,kind,tol,datums=(),pref=45,dia=False,rmin=10,rmax=48,prefix=None):
    W,H=fcf_size(tol,datums,dia)
    best=None
    for dist in [rmin+4*i for i in range(int((rmax-rmin)/4)+1)]:
        for da in [0,20,-20,40,-40,60,-60,90,-90,120,-120,150,-150,180]:
            a=math.radians(pref+da); qx=target[0]+dist*math.cos(a); qy=target[1]-dist*math.sin(a)
            if abs(math.sin(a))<0.34 or abs(math.cos(a))<0.17: continue   # leader miring (ASME Y14.2)
            left=math.cos(a)>=0   # kotak di kanan titik siku
            x=qx+4 if left else qx-4-W; y=qy-H/2
            bb=(x-0.5,y-(5.5 if prefix else 0.5),x+W+0.5,y+H+0.5)
            if not free_box(bb): continue
            if not free_line(target,(qx,qy)): continue
            if not free_line((qx,qy),(x if left else x+W,qy)): continue
            _n=math.hypot(qx-target[0],qy-target[1]) or 1
            if obj_cross_count((target[0]+(qx-target[0])*4.0/_n,target[1]+(qy-target[1])*4.0/_n),(qx,qy))>0: continue
            sc=dist*0.6+abs(da)*0.25+obj_cross_count(target,(qx,qy))*6
            if best is None or sc<best[0]: best=(sc,x,y)
        if best and best[0]<dist*0.6+12: break
    if best is None:
        print('  ! fcf',tol,'tanpa posisi bebas'); x,y=target[0]+rmin,target[1]-rmin
    else: _,x,y=best
    fcf(x,y,kind,tol,datums,lead=target,dia=dia)
    if prefix: T(x,y-1.4,prefix,3.5,'l',owner=('fcf',round(x,1),round(y,1)))
def datum(x,y,letter,dirn=(0,1),owner=None,stem=6.0):
    ow=owner or ('dat',letter,round(x,1),round(y,1))
    ux,uy=dirn; n=math.hypot(ux,uy); ux,uy=ux/n,uy/n; px,py=-uy,ux
    s=FH; e=(x+ux*(3+stem),y+uy*(3+stem)); bx,by=e[0]+ux*s/2,e[1]+uy*s/2
    with own(ow,'sym'):
        d.poly([(x+px*1.8,y+py*1.8),(x-px*1.8,y-py*1.8),(x+ux*3.0,y+uy*3.0)],.2,K,K,'inst')
        _l([(x+ux*3,y+uy*3),e])
        d.rect(bx-s/2,by-s/2,s,s,0,'#ffffff','inst'); d.rect(bx-s/2,by-s/2,s,s,.35,None,'inst')
    TC(bx,by,letter,3.5,'m',owner=ow)
    d.texts.append(dict(bb=(bx-s/2,by-s/2,bx+s/2,by+s/2),t='fcf',owner=ow,layer='inst',h=3.5,kind='sym'))
def surf(x,y,ra='1.6',owner=None,flip=False):
    ow=owner or ('rough',round(x,1),round(y,1)); s=-1 if flip else 1
    h1,h2=3.6,7.4
    a=(x-h1*0.58,y-s*h1); b=(x+h2*0.58,y-s*h2)
    tw=twidth('Ra '+ra,3.0)
    with own(ow,'sym'):
        _l([a,(x,y),b]); _l([a,(a[0]+2*h1*0.58,a[1])]); _l([b,(b[0]+tw+2,b[1])])
    T(b[0]+1,b[1]-(1.0 if not flip else -4.2),'Ra '+ra,3.0,'l',owner=ow)
def surf_ok(x,y,ra='1.6',flip=False):
    s=-1 if flip else 1; tw=twidth('Ra '+ra,3.0)
    if not flip: bb=(x-2.5,y-7.4-4.6,x+4.3+tw+2.5,y-2.2)
    else: bb=(x-2.5,y+2.2,x+4.3+tw+2.5,y+7.4+4.6)
    return free_box(bb)
def weld(px,py,bx,by,size='12',both=True,kind='fillet',all_round=False,owner=None,right=True,length=''):
    ow=owner or ('weld',round(px,1),round(py,1))
    s=1 if right else -1; Lr=24.0; cx=bx+s*11.0
    with own(ow,'ld'):
        _l([(bx,by),(px,py)],.25)
        dx,dy=px-bx,py-by; n=math.hypot(dx,dy) or 1; arrow(px,py,dx/n,dy/n)
        _l([(bx,by),(bx+s*Lr,by)],.35)
    with own(ow,'sym'):
        if kind=='fillet':
            d.poly([(cx-2,by),(cx-2,by+3.6),(cx+1.8,by)],.3,None,K,'inst')
            if both: d.poly([(cx-2,by),(cx-2,by-3.6),(cx+1.8,by)],.3,None,K,'inst')
        elif kind=='V':
            d.line([(cx-2.2,by+3.6),(cx,by),(cx+2.2,by+3.6)],.3,None,K,'inst')
            if both: d.line([(cx-2.2,by-3.6),(cx,by),(cx+2.2,by-3.6)],.3,None,K,'inst')
        if all_round: d.circ(bx,by,1.6,.3,None,'inst')
    if size:
        T(cx-3.2,by+3.4,size,3.0,'r',owner=ow)
        if both and kind=='fillet': T(cx-3.2,by-0.6,size,3.0,'r',owner=ow)
    if length: T(cx+3.0,by+3.4,length,3.0,'l',owner=ow)
    d.texts.append(dict(bb=(min(bx,bx+s*Lr),by-4.4,max(bx,bx+s*Lr),by+4.4),t='weld',owner=ow,layer='inst',h=3.0,kind='sym'))
def breakline(p0,p1,amp=1.2,w=.25):
    n=16; x0,y0=p0; x1,y1=p1; dx,dy=x1-x0,y1-y0; ln=math.hypot(dx,dy); px,py=-dy/ln,dx/ln
    pts=[(x0+dx*i/n+px*amp*math.sin(i/n*math.pi*3),y0+dy*i/n+py*amp*math.sin(i/n*math.pi*3)) for i in range(n+1)]
    d.line(pts,w,None,K,'equip')
def angdim(c,r,a0,a1,text,owner=None,size=3.5):
    ow=owner or ('ang',round(c[0],1),round(c[1],1),a0)
    pts=[(c[0]+r*math.cos(math.radians(a0+(a1-a0)*i/24)),c[1]-r*math.sin(math.radians(a0+(a1-a0)*i/24))) for i in range(25)]
    with own(ow,'dl'):
        L(pts,.25,None,'inst')
        for p,q in ((pts[0],pts[1]),(pts[-1],pts[-2])):
            dx,dy=p[0]-q[0],p[1]-q[1]; n=math.hypot(dx,dy) or 1; arrow(p[0],p[1],dx/n,dy/n)
    am=math.radians((a0+a1)/2); tx,ty=c[0]+(r+4.5)*math.cos(am),c[1]-(r+4.5)*math.sin(am)
    TC(tx,ty,text,size,'m',owner=ow)
def cutplane(x,y0,y1,letter,dirx,size=5.0):
    ow=('cut',letter)
    with own(ow,'ld'):
        L([(x,y0),(x,y1)],.7,[12,2,2.5,2],'inst')
        for ye in (y0,y1):
            L([(x,ye),(x+dirx*9,ye)],.7,None,'inst'); arrow(x+dirx*9,ye,dirx,0)
    T(x+dirx*12,y0+size/2,letter,size,'l' if dirx>0 else 'r',owner=ow)
    T(x+dirx*12,y1+size/2,letter,size,'l' if dirx>0 else 'r',owner=ow)
def detcircle(cx,cy,r,letter,ang=45,size=5.0):
    ow=('det',letter)
    a=math.radians(ang); p=(cx+r*math.cos(a),cy-r*math.sin(a)); q=(cx+(r+7)*math.cos(a),cy-(r+7)*math.sin(a))
    with own(ow,'ld'):
        d.circ(cx,cy,r,.35,None,'inst'); L([p,q],.25,None,'inst')
    T(q[0]+(1.5 if math.cos(a)>=0 else -1.5),q[1]+(0 if math.sin(a)>0 else size),letter,size,'l' if math.cos(a)>=0 else 'r',owner=ow)
def nz(label,bx,by,px,py,w=12.0,h=7.0,size=3.5):
    ow=('nz',label)
    dx,dy=px-bx,py-by
    if abs(dy)*w>=abs(dx)*h: sx,sy=bx,by+(h/2 if dy>0 else -h/2)
    else: sx,sy=bx+(w/2 if dx>0 else -w/2),by
    with own(ow,'ld'):
        d.rect(bx-w/2,by-h/2,w,h,0,'#ffffff','inst'); d.rect(bx-w/2,by-h/2,w,h,.35,None,'inst')
        L([(sx,sy),(px,py)],.25,None,'inst'); d.circ(px,py,.6,.05,K,'inst')
    TC(bx,by,label,size,'m',owner=ow)
    d.texts.append(dict(bb=(bx-w/2,by-h/2,bx+w/2,by+h/2),t='nz'+label,owner=ow,layer='inst',h=3.5,kind='sym'))
    BALL.append((bx,by,6.5,label))
def auto_nz(label,target,pref=90,rmin=10,rmax=40):
    best=None
    for dist in [rmin+3*i for i in range(int((rmax-rmin)/3)+1)]:
        for da in [0,20,-20,40,-40,60,-60,90,-90,135,-135,180]:
            a=math.radians(pref+da); bx=target[0]+dist*math.cos(a); by=target[1]-dist*math.sin(a)
            bb=(bx-6.5,by-4,bx+6.5,by+4)
            if not free_box(bb): continue
            if not free_line(target,(bx,by)): continue
            sc=dist*0.6+abs(da)*0.25
            if best is None or sc<best[0]: best=(sc,bx,by)
        if best and best[0]<dist*0.6+10: break
    if best is None: print('  ! nosel',label,'tanpa posisi'); bx,by=target[0],target[1]-rmin
    else: _,bx,by=best
    nz(label,bx,by,target[0],target[1])

def auto_surf(cands,ra):
    """cands: daftar (x,y,flip) pada permukaan; pilih yang pertama bebas"""
    for x,y,fl in cands:
        if surf_ok(x,y,ra,fl): surf(x,y,ra,flip=fl); return True
    print('  ! Ra',ra,'tanpa posisi'); return False

def datum_on_leader(res,letter):
    """lekatkan simbol datum pada bahu rujukan dimensi ukuran (ASME Y14.5)"""
    tx,ty,an,ex,tw=res
    xm=(tx+ex)/2
    datum(xm,ty+0.2,letter,(0,1),stem=4.0)
def cutplane_h(y,x0,x1,letter,diry=-1,size=5.0):
    """bidang potong ASME Y14.3 (hanya ujung tebal) memanjang horizontal; panah menunjuk arah pandang"""
    ow=('cut',letter)
    with own(ow,'ld'):
        for xa,xb in ((x0-8,x0+6),(x1-6,x1+8)):
            L([(xa,y),(xb,y)],.7,None,'inst')
        for xe in (x0-8,x1+8):
            L([(xe,y),(xe,y+diry*8)],.7,None,'inst'); arrow(xe,y+diry*8,0,diry)
    for xe in (x0-8,x1+8):
        TC(xe,y+diry*12.5+(size/2 if diry>0 else -0.5),letter,size,'m',owner=ow) if False else T(xe-size*0.35,y+diry*11+(size if diry>0 else 0),letter,size,'l',owner=ow)
def fcf_under(res,kind,tol,datums=(),dia=False):
    """kotak kendali fitur di bawah label ukuran (ASME Y14.5 §6.4.1 — dihubungkan ke ukuran fitur)"""
    tx,ty,an,ex,tw=res
    x0=ex+1.2 if an=='l' else ex-1.2-tw
    fcf(x0,ty+4.4,kind,tol,datums,dia=dia)

def auto_leader_fcf(target,text,kind,tol,datums=(),dia=False,**kw):
    W,H=fcf_size(tol,datums,dia)
    res=auto_leader(target,text,below=(W,H),**kw)
    fcf_under(res,kind,tol,datums,dia); return res
