# -*- coding: utf-8 -*-
"""Tampilan gambar dari model 3D: tampak (HLR), potongan berarsir, isometri berbayang."""
import math, numpy as np, cadquery as cq
from kd import *
import cadview as CV
VIS_W=.5; THIN=.25
def _simp(pl,tol=.05):
    out=[pl[0]]
    for p in pl[1:]:
        if abs(p[0]-out[-1][0])+abs(p[1]-out[-1][1])>tol: out.append(p)
    return out
class View:
    def __init__(s,N,X,scale,ox,oy,origin=(0,0,0),name=None):
        s.name=name; s.bb=None
        s.N=np.array(N,float); s.N/=np.linalg.norm(s.N)
        s.X=np.array(X,float); s.X-=s.N*s.X.dot(s.N); s.X/=np.linalg.norm(s.X)
        s.Y=np.cross(s.N,s.X); s.k=1.0/scale; s.ox,s.oy=ox,oy
        s.o=np.array(origin,float)
    def _acc(s,pts):
        if not pts or not s.name: return
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        b=(min(xs),min(ys),max(xs),max(ys))
        s.bb=b if s.bb is None else (min(s.bb[0],b[0]),min(s.bb[1],b[1]),max(s.bb[2],b[2]),max(s.bb[3],b[3]))
        for i,(vb,vn) in enumerate(VIEWS):
            if vn==s.name: VIEWS[i]=(s.bb,vn); break
        else: VIEWS.append((s.bb,s.name))
    def uv(s,p):
        p=np.array(p,float)-s.o; return p.dot(s.X),p.dot(s.Y)
    def P(s,p):
        u,v=s.uv(p); return (s.ox+u*s.k, s.oy-v*s.k)
    def Puv(s,u,v): return (s.ox+(u-s.o.dot(s.X)*0)*s.k, s.oy-v*s.k)
    def tp(s,u,v):
        # u,v absolut dari HLR (origin dunia) -> kertas
        uo,vo=s.o.dot(s.X),s.o.dot(s.Y)
        return (s.ox+(u-uo)*s.k, s.oy-(v-vo)*s.k)
    def draw(s,shape,hidden=True,w=VIS_W,defl=None,reg=True,hid_w=THIN):
        defl=defl or max(.5,0.15/s.k)
        vis,hid=CV.hlr(shape,tuple(s.N),tuple(s.X),defl,hidden)
        for pl in vis:
            pts=_simp([s.tp(u,v) for u,v in pl])
            if len(pts)>1: L(pts,w,None,'equip',reg=reg); s._acc(pts)
        for pl in hid:
            pts=_simp([s.tp(u,v) for u,v in pl])
            if len(pts)>1: L(pts,hid_w,[2.0,1.0],'sig',reg=False)
        return vis,hid
    def section(s,shape,origin,w=VIS_W,hatch_sp=2.5,ang=45,defl=None,keep_behind=True,draw_rest=True,hidden=False,extra_hatch=None):
        """potongan: bagian di sisi pengamat dibuang; permukaan potong diarsir"""
        sh_=CV.toshape(shape)
        org=np.array(origin,float)
        if draw_rest:
            big=2e5
            pl=cq.Plane(origin=tuple(org),xDir=tuple(s.X),normal=tuple(s.N))
            box=cq.Workplane(pl).rect(2*big,2*big).extrude(big).val()
            rest=sh_.cut(box)
            s.draw(rest,hidden=hidden,w=w,defl=defl)
        rings=CV.section_faces(sh_,tuple(org),tuple(s.N),tuple(s.X),defl=max(.5,0.15/s.k))
        uo,vo=org.dot(s.X)-s.o.dot(s.X),org.dot(s.Y)-s.o.dot(s.Y)
        R=[[(s.ox+(u+uo)*s.k, s.oy-(v+vo)*s.k) for u,v in r] for r in rings]
        if R:
            hatch([r[:-1] if r[0]==r[-1] else r for r in R],ang,hatch_sp,.18,'proc')
            for r in R: L(r+[r[0]],w,None,'equip',reg=True); s._acc(r)
        return R
    def fit(s,shape,region,margin=3.0,tol=None):
        """atur skala & posisi agar proyeksi (tanpa gambar) muat di region (x0,y0,x1,y1)"""
        sh_=CV.toshape(shape); bb=sh_.BoundingBox()
        P=[np.array([x,y,z]) for x in (bb.xmin,bb.xmax) for y in (bb.ymin,bb.ymax) for z in (bb.zmin,bb.zmax)]
        us=[p.dot(s.X) for p in P]; vs=[p.dot(s.Y) for p in P]
        W=max(us)-min(us); H=max(vs)-min(vs)
        rw=region[2]-region[0]-2*margin; rh=region[3]-region[1]-2*margin
        k=min(rw/W,rh/H)*0.97; s.k=k
        cu=(max(us)+min(us))/2; cv=(max(vs)+min(vs))/2
        s.o=np.zeros(3); s.ox=(region[0]+region[2])/2-cu*k; s.oy=(region[1]+region[3])/2+cv*k
        return 1/k
    def iso(s,shape,tol=None,edges=True,w=.3,ang=.35,lmax=None):
        tol=tol or max(1.0,0.4/s.k)
        lmax=lmax or 5.0/s.k
        tris=CV.iso_mesh(shape,tuple(s.N),tuple(s.X),tol,ang,lmax)
        uo,vo=s.o.dot(s.X),s.o.dot(s.Y)
        for pts,dep,sh in tris:
            g=int(70+170*sh); c='#%02x%02x%02x'%(g,g,g)
            P_=[(s.ox+(u-uo)*s.k, s.oy-(v-vo)*s.k) for u,v in pts]
            d.poly(P_,.06,c,c,'util'); s._acc(P_)
        if edges:
            vis,_=CV.hlr(shape,tuple(s.N),tuple(s.X),max(.5,0.15/s.k),False)
            for pl in vis:
                pts=_simp([s.tp(u,v) for u,v in pl])
                if len(pts)>1: d.line(pts,w,None,K,'equip')
def cl(p0,p1,w=.25):
    L([p0,p1],w,[8,1.5,1.5,1.5],'sig',reg=False)
