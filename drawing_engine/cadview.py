# -*- coding: utf-8 -*-
"""Proyeksi HLR (garis tampak/tersembunyi), potongan, dan isometri berbayang dari model CadQuery."""
import math, numpy as np
import cadquery as cq
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Pln
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.BRepLib import BRepLib

def toshape(x):
    if isinstance(x,cq.Workplane):
        vs=[v for v in x.vals() if isinstance(v,cq.Shape)]
        return vs[0] if len(vs)==1 else cq.Compound.makeCompound(vs)
    if isinstance(x,(list,tuple)): return cq.Compound.makeCompound([toshape(i) for i in x])
    return x
def _edges(comp,defl):
    out=[]
    if comp is None or comp.IsNull(): return out
    BRepLib.BuildCurves3d_s(comp)
    ex=TopExp_Explorer(comp,TopAbs_EDGE)
    while ex.More():
        e=TopoDS.Edge_s(ex.Current())
        try:
            c=BRepAdaptor_Curve(e)
            dsc=GCPnts_QuasiUniformDeflection(c,defl)
            if dsc.IsDone() and dsc.NbPoints()>1:
                out.append([(dsc.Value(i).X(),dsc.Value(i).Y()) for i in range(1,dsc.NbPoints()+1)])
        except Exception: pass
        ex.Next()
    return out

def hlr(shape,vdir,xdir,defl=1.0,hidden=True):
    """kembalikan (tampak, tersembunyi) sebagai daftar polilinia (u,v) mm, u ke kanan, v ke atas.
    vdir: arah pandang (dari pengamat ke objek dibalik: OCC memakai arah normal bidang proyeksi menuju pengamat)"""
    s=toshape(shape).wrapped
    algo=HLRBRep_Algo(); algo.Add(s)
    ax=gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*vdir),gp_Dir(*xdir))
    algo.Projector(HLRAlgo_Projector(ax)); algo.Update(); algo.Hide()
    h=HLRBRep_HLRToShape(algo)
    vis=[]
    for comp in (h.VCompound(),h.OutLineVCompound(),h.Rg1LineVCompound()):
        vis+=_edges(comp,defl)
    hid=[]
    if hidden:
        for comp in (h.HCompound(),h.OutLineHCompound()):
            hid+=_edges(comp,defl)
    return vis,hid

def _wire_pts(w,f,defl):
    from OCP.BRepTools import BRepTools_WireExplorer
    from OCP.TopAbs import TopAbs_REVERSED
    from OCP.GeomAbs import GeomAbs_Line
    ex=BRepTools_WireExplorer(w.wrapped,f.wrapped)
    pts=[]
    while ex.More():
        e=ex.Current(); c=BRepAdaptor_Curve(e)
        if c.GetType()==GeomAbs_Line:
            ps=[c.Value(c.FirstParameter()),c.Value(c.LastParameter())]
        else:
            dsc=GCPnts_QuasiUniformDeflection(c,defl)
            ps=[dsc.Value(i) for i in range(1,dsc.NbPoints()+1)]
        if e.Orientation()==TopAbs_REVERSED: ps=ps[::-1]
        pts+=[(p.X(),p.Y(),p.Z()) for p in ps]
        ex.Next()
    return pts
def section_faces(shape,origin,normal,xdir,defl=1.0):
    """irisan bidang -> daftar cincin poligon (u,v) pada sistem bidang (xdir, normal x xdir)"""
    s=toshape(shape)
    pl=cq.Plane(origin=origin,xDir=xdir,normal=normal)
    big=cq.Face.makePlane(1e6,1e6,basePnt=cq.Vector(*origin),dir=cq.Vector(*normal))
    cut=s.intersect(big)
    rings=[]
    for f in cut.Faces():
        for w in f.Wires():
            P=_wire_pts(w,f,defl)
            loc=[pl.toLocalCoords(cq.Vector(*p)) for p in P]
            rings.append([(p.x,p.y) for p in loc])
    return rings

def iso_mesh(shape,vdir,xdir,tol=2.0,ang=0.3,lmax=None):
    """tessellasi untuk isometri berbayang: kembalikan list (poly2d, depth, shade)"""
    s=toshape(shape)
    V=np.array(vdir,float); V/=np.linalg.norm(V)
    X=np.array(xdir,float); X-=V*X.dot(V); X/=np.linalg.norm(X)
    Y=np.cross(V,X)
    Lgt=np.array([0.35,0.45,0.82]); Lgt=Lgt/np.linalg.norm(Lgt)
    # cahaya relatif terhadap pandangan: dari kiri atas depan
    Lw=(-0.45*X+0.55*Y+0.70*V); Lw/=np.linalg.norm(Lw)
    tris=[]
    for f in s.Faces():
        vs,ts=f.tessellate(tol,ang)
        P=np.array([[v.x,v.y,v.z] for v in vs])
        stack=[(P[a],P[b],P[c]) for a,b,c in ts]
        while stack:
            p0,p1,p2=stack.pop()
            if lmax:
                e=[np.linalg.norm(p1-p0),np.linalg.norm(p2-p1),np.linalg.norm(p0-p2)]
                k=int(np.argmax(e))
                if e[k]>lmax:
                    if k==0: m_=(p0+p1)/2; stack+=[(p0,m_,p2),(m_,p1,p2)]
                    elif k==1: m_=(p1+p2)/2; stack+=[(p0,p1,m_),(p0,m_,p2)]
                    else: m_=(p2+p0)/2; stack+=[(p0,p1,m_),(m_,p1,p2)]
                    continue
            nrm=np.cross(p1-p0,p2-p0); ln=np.linalg.norm(nrm)
            if ln<1e-9: continue
            nrm/=ln
            if nrm.dot(V)<0: continue   # buang muka belakang
            sh=0.30+0.62*max(0.0,nrm.dot(Lw))+0.08
            pts=[(p.dot(X),p.dot(Y)) for p in (p0,p1,p2)]
            dep=(p0+p1+p2).dot(V)/3
            tris.append((pts,dep,min(sh,1.0)))
    tris.sort(key=lambda t:t[1])
    return tris
