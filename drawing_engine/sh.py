# -*- coding: utf-8 -*-
"""Format A3 (ASME Y14.1 / ISO 5457): bingkai berzona, blok judul dengan blok toleransi, blok revisi."""
from kd import *
import kd as _kd, kt
def T(*a,**k):
    k.setdefault('layer','frame'); return _kd.T(*a,**k)
def TC(*a,**k):
    k.setdefault('layer','frame'); return _kd.TC(*a,**k)
FX0,FY0,FX1,FY1=10.0,10.0,410.0,287.0
TBX,TBY,TBW,TBH=228.0,229.0,182.0,58.0
RVX,RVY,RVW,RVH=290.0,10.0,120.0,23.6
NS=10
def zones():
    d.rect(5,5,410,287,.25,None,'frame'); d.rect(FX0,FY0,FX1-FX0,FY1-FY0,.7,None,'frame')
    nx,ny=8,6; zw=(FX1-FX0)/nx; zh=(FY1-FY0)/ny
    for i in range(nx+1):
        x=FX0+i*zw
        for ya,yb in ((5,FY0),(FY1,292)): d.line([(x,ya),(x,yb)],.25,None,K,'frame')
        if i<nx:
            for yc in (7.5,289.5): TC(x+zw/2,yc,str(i+1),2.5,'m')
    for j in range(ny+1):
        y=FY0+j*zh
        for xa,xb in ((5,FX0),(FX1,415)): d.line([(xa,y),(xb,y)],.25,None,K,'frame')
        if j<ny:
            for xc in (7.5,412.5): TC(xc,y+zh/2,'ABCDEF'[j],2.5,'m')
    # tanda pusat
    for (x0,y0,x1,y1) in ((210,5,210,FY0+5),(210,FY1-5,210,292),(5,148.5,FX0+5,148.5),(FX1-5,148.5,415,148.5)):
        d.line([(x0,y0),(x1,y1)],.7,None,K,'frame')
def _cell(x,y,w,h,label,value,vsize=3.5,lsize=2.0,align='m'):
    d.rect(x,y,w,h,.3,None,'frame')
    T(x+1.2,y+3.1,label,lsize,'l')
    if value is not None:
        if align=='m': TC(x+w/2,y+max(h*0.62,4.3+vsize/2+0.6),value,vsize,'m')
        else: TC(x+2,y+max(h*0.62,4.3+vsize/2+0.6),value,vsize,'l')
def frame(sheet,title,sub,scale,docno,dtype='GAMBAR SUSUNAN',material='Lihat daftar bagian',mass='—',treat='—'):
    zones()
    x,y,w,h=TBX,TBY,TBW,TBH
    d.rect(x,y,w,h,0,'#ffffff','frame'); d.rect(x,y,w,h,.7,None,'frame')
    # ----- kolom kiri: blok toleransi, bahan, proyeksi (lebar 70)
    wl=70.0
    d.rect(x,y,wl,24,.3,None,'frame')
    lines=['KECUALI DINYATAKAN LAIN:','DIMENSI DALAM mm','TOLERANSI: X ±1   X.X ±0.5','SUDUT ±0.5°   KEKASARAN Ra (µm)','TAFSIR GD&T: ASME Y14.5-2018']
    for i,l_ in enumerate(lines): T(x+1.5,y+4.0+i*4.4,l_,2.3,'l')
    _cell(x,y+24,wl,9,'BAHAN',material,2.8,2.0,'l')
    _cell(x,y+33,wl*0.5,9,'MASSA',mass,2.8)
    _cell(x+wl*0.5,y+33,wl*0.5,9,'PERLAKUAN',treat,2.8)
    d.rect(x,y+42,wl,16,.3,None,'frame')
    cx,cy=x+15,y+50
    d.poly([(cx-9,cy-3.4),(cx-2.5,cy-2.0),(cx-2.5,cy+2.0),(cx-9,cy+3.4)],.3,None,K,'frame')
    d.circ(cx+6,cy,3.4,.3,None,'frame'); d.circ(cx+6,cy,1.7,.3,None,'frame')
    d.line([(cx-11,cy),(cx+10.5,cy)],.18,[3,.8,.8,.8],K,'frame')
    T(x+30,y+48.2,'PROYEKSI',2.5,'l'); T(x+30,y+53.2,'SUDUT PERTAMA',2.5,'l')
    # ----- kolom kanan
    xr=x+wl; wr=w-wl
    d.rect(xr,y,wr,10,.3,None,'frame')
    TC(xr+wr/2,y+3.4,'UNIVERSITAS GADJAH MADA · DEPARTEMEN TEKNIK KIMIA',2.2,'m')
    TC(xr+wr/2,y+7.4,'TIM LAGI PENGEN · THE 21st MnMs WEEK 2026',2.2,'m')
    d.rect(xr,y+10,wr,16,.3,None,'frame')
    T(xr+1.2,y+13.2,'JUDUL',2.0,'l')
    ls=kt.wrapw(title,4.2,wr-6)
    for i,l_ in enumerate(ls): TC(xr+wr/2,y+18.8+(i-(len(ls)-1)/2)*6.0,l_,4.2,'m')
    cw=wr/3
    for i,(lab,val) in enumerate((('DIGAMBAR','Tim LP'),('DIPERIKSA','—'),('DISETUJUI','—'))):
        _cell(xr+i*cw,y+26,cw,10,lab,val,2.8)
    _cell(xr,y+36,16,11,'UKURAN','A3',3.2)
    _cell(xr+16,y+36,wr-16-14,11,'NO. GAMBAR',docno,3.5)
    _cell(xr+wr-14,y+36,14,11,'REV','B',3.5)
    _cell(xr,y+47,wr*0.36,11,'SKALA',scale,3.2)
    _cell(xr+wr*0.36,y+47,wr*0.40,11,'JENIS',dtype,2.6)
    _cell(xr+wr*0.76,y+47,wr*0.24,11,'LEMBAR',f'{sheet} / {NS}',3.2)
    zone('BLOK JUDUL',(x,y,x+w,y+h))
    # ----- blok revisi (kanan atas)
    X,Y=RVX,RVY
    d.rect(X,Y,RVW,RVH,0,'#ffffff','frame')
    TC(X+RVW/2,Y+2.6,'REVISI',2.5,'m'); d.rect(X,Y,RVW,RVH,.5,None,'frame'); d.line([(X,Y+5.2),(X+RVW,Y+5.2)],.3,None,K,'frame')
    cols=[(10,'REV'),(60,'URAIAN'),(26,'TANGGAL'),(24,'DISETUJUI')]
    xx=X
    for i,(cw_,lab) in enumerate(cols):
        if i: d.line([(xx,Y+5.2),(xx,Y+RVH)],.25,None,K,'frame')
        TC(xx+cw_/2,Y+7.8,lab,2.0,'m')
        xx+=cw_
    d.line([(X,Y+10.4),(X+RVW,Y+10.4)],.25,None,K,'frame')
    d.line([(X,Y+17.0),(X+RVW,Y+17.0)],.25,None,K,'frame')
    for k_,vals in enumerate((['A','Terbit untuk tinjauan','2026-10-11','—'],['B','Dimensi dilengkapi','2026-10-11','—'])):
        xx=X
        for (cw_,_),v in zip(cols,vals):
            TC(xx+cw_/2,Y+13.7+6.6*k_,v,2.5,'m'); xx+=cw_
    zone('BLOK REVISI',(X,Y,X+RVW,Y+RVH))
def wave(x,y0,y1,amp=1.2,w=.25):
    n=14; pts=[(x+amp*math.sin(i/n*math.pi*3),y0+(y1-y0)*i/n) for i in range(n+1)]
    d.line(pts,w,None,K,'equip')
