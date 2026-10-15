# -*- coding: utf-8 -*-
from kd import *
import kd as _kd
def TC(*a,**kw):
    kw.setdefault('layer','table'); return _kd.TC(*a,**kw)
HDR='#e6e6e6'
def wrapw(t,size,maxw,bold=False):
    out=[]
    for para in str(t).split('\n'):
        words=para.split(' '); cur=''
        for w_ in words:
            cand=(cur+' '+w_) if cur else w_
            test=cand+('*' if cand.count('*')%2 else '')
            if cur and twidth(test.replace('**',''),size,bold)>maxw:
                if cur.count('*')%2: out.append(cur+'*'); cur='*'+w_
                else: out.append(cur); cur=w_
            else: cur=cand
        out.append(cur)
    return [l.replace('**','') for l in out]
def table(x,y,cols,header,rows,size=2.9,bold_first=False,minh=5.2,pad=1.3,title=None,tsize=3.8,aligns=None,hdr_size=None,numcol=None):
    """gambar tabel; kolom berlebar 'cols' (mm). rows: list of list of str (atau ('A',judul) untuk baris judul). return y akhir"""
    W=sum(cols); aligns=aligns or ['l']*len(cols); hs=hdr_size or size
    if title:
        d.rect(x,y,W,6.4,.35,HDR,'table'); TC(x+W/2,y+3.2,title,tsize,'m',True,chk=True); y+=6.4
    # header
    hl=[wrapw(h,hs,cols[i]-2*pad,True) for i,h in enumerate(header)]
    hh=hs+(max(len(l) for l in hl)-1)*hs*1.7+2.6
    hh=max(hh,minh)
    d.rect(x,y,W,hh,.3,HDR,'table')
    xx=x
    for i,l in enumerate(hl):
        for k,ln in enumerate(l):
            TC(xx+cols[i]/2,y+hh/2+(k-(len(l)-1)/2)*hs*1.7,ln,hs,'m',True)
        xx+=cols[i]
    y0=y; y+=hh
    for r in rows:
        if r and r[0]=='A':
            rh=minh
            d.rect(x,y,W,rh,.2,'#f3f3f3','table'); TC(x+pad,y+rh/2,r[1],size,'l',True)
            y+=rh; continue
        cl=[wrapw(c,size,cols[i]-2*pad,bold_first and i==0) for i,c in enumerate(r)]
        n=max(len(l) for l in cl); rh=max(minh,size+(n-1)*size*1.7+2.6)
        xx=x
        for i,l in enumerate(cl):
            for k,ln in enumerate(l):
                yy=y+rh/2+(k-(len(l)-1)/2)*size*1.7
                a=aligns[i]
                tx={'l':xx+pad,'m':xx+cols[i]/2,'r':xx+cols[i]-pad}[a]
                TC(tx,yy,ln,size,a,bold_first and i==0)
            xx+=cols[i]
        d.line([(x,y+rh),(x+W,y+rh)],.12,None,K,'table')
        y+=rh
    # garis kolom dan bingkai
    xx=x
    for i in range(len(cols)-1):
        xx+=cols[i]; d.line([(xx,y0),(xx,y)],.15,None,K,'table')
    d.rect(x,y0-(6.4 if title else 0),W,y-y0+(6.4 if title else 0),.5,None,'table')
    zone('TABEL '+(title or ''),(x,y0-(6.4 if title else 0),x+W,y))
    return y
