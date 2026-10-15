# -*- coding: utf-8 -*-
import math
def inv(a): return math.tan(a)-a
def gear_outline(z,m,alpha=20.0,teeth=None,center_ang=90.0,n=24):
    """garis tepi roda gigi involut (polar), teeth = daftar indeks gigi relatif terhadap center_ang; return list titik (x,y) koordinat model (mm), y ke atas"""
    a=math.radians(alpha); r=m*z/2; rb=r*math.cos(a); ra=r+m; rf=r-1.25*m
    pitch=2*math.pi/z
    pts=[]
    idx=teeth if teeth is not None else range(z)
    for k in idx:
        th0=math.radians(center_ang)+k*pitch
        # flank kiri (sudut lebih besar) dari kaki ke kepala, lalu kanan dari kepala ke kaki
        def psi(rr):
            ar=math.acos(min(1.0,rb/rr)); return math.pi/(2*z)+inv(a)-inv(ar)
        rs=[max(rb,rf)+(ra-max(rb,rf))*i/n for i in range(n+1)]
        left=[(rr,th0+psi(rr)) for rr in rs]
        right=[(rr,th0-psi(rr)) for rr in rs[::-1]]
        start=[(rf,th0+psi(max(rb,rf))+0.0)]
        # kaki: dari tengah celah sebelumnya
        gap_l=th0+pitch/2; gap_r=th0-pitch/2
        seg=[(rf,gap_l)]+[(rf,th0+psi(max(rb,rf)))]+left+right+[(rf,th0-psi(max(rb,rf))),(rf,gap_r)]
        pts+= [(rr*math.cos(t),rr*math.sin(t)) for rr,t in seg]
    return pts
