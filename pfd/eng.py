# -*- coding: utf-8 -*-
"""Mesin gambar PFD A2: primitif, teks kimia bersubskrip, simbol bernosel, routing ortogonal,
pemutusan persilangan, pemeriksa tumpang-tindih, keluaran PDF (reportlab) + SVG berlapis."""
import math, re, os as _os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FD=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'fonts')+'/'
pdfmetrics.registerFont(TTFont('LS',FD+'LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LSB',FD+'LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LSI',FD+'LiberationSans-Italic.ttf'))
W,H=594.0,420.0
K='#000000'; UG='#505050'; SG='#000000'
LAYERS=['frame','table','util','proc','sig','equip','inst','label']
LAYER_NAME={'frame':'Bingkai dan Blok Judul','table':'Tabel Aliran dan Panel','util':'Aliran Utilitas',
            'proc':'Aliran Material','sig':'Sinyal Instrumen','equip':'Peralatan','inst':'Instrumen','label':'Teks dan Nomor Aliran'}
# ---------------------------------------------------------------- teks kimia
TOK=re.compile(r"[A-Za-z0-9()·]+|[^A-Za-z0-9()·]+")
FORM=re.compile(r"^(\(|\)\d*|[A-Z][a-z]?\d*|·\d*)+$")
NOFORM={'A2','A3','A4','B2'}
def _runs1(s):
    out=[]
    for t in TOK.findall(s):
        if FORM.match(t) and re.search(r'[A-Za-z)]\d',t) and t.strip('()') not in NOFORM and re.search(r'[A-Z]',t):
            i=0
            for m in re.finditer(r'\d+',t):
                a,b=m.span()
                if a>i: out.append((t[i:a],False))
                prev=t[a-1] if a>0 else ''
                out.append((t[a:b], bool(prev) and (prev.isalpha() or prev==')')))
                i=b
            if i<len(t): out.append((t[i:],False))
        else: out.append((t,False))
    return out
def runs(s):
    """pecah teks menjadi [(teks, subskrip?, miring?)]; *...* = huruf miring (istilah asing, PUEBI)"""
    out=[]
    for k,seg in enumerate(s.split('*')):
        it=(k%2==1)
        for t,sb in _runs1(seg): out.append((t,sb,it))
    m=[]
    for t,sb,it in out:
        if not t: continue
        if m and m[-1][1]==sb and m[-1][2]==it: m[-1]=(m[-1][0]+t,sb,it)
        else: m.append((t,sb,it))
    return m
SUBF=0.70; SUBD=0.28
TEXT_STROKE=0.028
DOC_TITLE='Process Flow Diagram'
DOC_AUTHOR=''
CAPC=0.345
TAG_FS=2.0; DIA_R=2.15; DIA_FS=1.55; INST_FS=1.45; FLAG_FS=1.75; FLAG_H=3.6
LW_PROC=.5; LW_UTIL=.26; LW_SIG=.18; AH_PROC=(2.1,1.35); AH_UTIL=(1.6,1.0)
TM=0.35       # jarak bebas minimum teks terhadap garis/alat pada pemeriksa   # baseline = pusat kotak + CAPC*ukuran -> teks tepat di tengah vertikal
pdfmetrics.registerFont(TTFont('LSBI',FD+'LiberationSans-BoldItalic.ttf'))
def font(bold,ital=False): return ('LSBI' if ital else 'LSB') if bold else ('LSI' if ital else 'LS')
def twidth(s,size,bold=False,ital=False):
    return sum(pdfmetrics.stringWidth(t,font(bold,ital or it),size*(SUBF if sb else 1)) for t,sb,it in runs(s))
# ---------------------------------------------------------------- dokumen
class Doc:
    def __init__(s):
        s.items={l:[] for l in LAYERS}
        s.texts=[]; s.eqs={}; s.eqrange={}; s.paths=[]; s.diamonds=[]; s.flags=[]; s.boxes=[]; s.junc=[]
    # primitif
    def line(s,pts,w=.35,dash=None,col=K,layer='equip',cap='butt'):
        s.items[layer].append(('line',[tuple(map(float,p)) for p in pts],w,dash,col,cap))
    def poly(s,pts,w=.35,fill=None,col=K,layer='equip',dash=None):
        s.items[layer].append(('poly',[tuple(map(float,p)) for p in pts],w,fill,col,dash))
    def rect(s,x,y,w,h,lw=.35,fill=None,layer='equip',col=K,dash=None):
        s.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],lw,fill,col,layer,dash)
    def circ(s,cx,cy,r,lw=.35,fill=None,layer='equip',col=K):
        s.items[layer].append(('circ',cx,cy,r,lw,fill,col))
    def arcpts(s,cx,cy,rx,ry,a0,a1,n=28):
        return [(cx+rx*math.cos(math.radians(a0+(a1-a0)*i/n)),cy-ry*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
    def arc(s,cx,cy,rx,ry,a0,a1,lw=.35,layer='equip',col=K):
        s.line(s.arcpts(cx,cy,rx,ry,a0,a1),lw,None,col,layer,'round')
    def text(s,x,y,t,size=1.8,anchor='l',bold=False,rot=0,layer='label',col=K,chk=True,owner=None,ital=False,pad=.15):
        t=str(t)
        s.items[layer].append(('text',x,y,t,size,anchor,bold,rot,col,ital))
        wd=twidth(t,size,bold,ital)
        x0={'l':x,'m':x-wd/2,'r':x-wd}[anchor]
        if rot==0: bb=(x0-pad,y-.74*size-pad,x0+wd+pad,y+.22*size+pad)
        else:      # rot 90: membaca dari bawah ke atas, baseline vertikal di x
            y0={'l':y,'m':y+wd/2,'r':y+wd}[anchor]
            bb=(x-.74*size-pad,y0-wd-pad,x+.22*size+pad,y0+pad)
        if chk: s.texts.append(dict(bb=bb,t=t,owner=owner,layer=layer))
        return bb
    # -------------------------------------------------------- peralatan
    def eq(s,kind,tag,x,y,w,h,lab='b',dx=0,dy=0,**kw):
        e=Eq(s,kind,tag,x,y,w,h,**kw); s.eqs[tag]=e
        b0={L:len(s.items[L]) for L in LAYERS}
        getattr(Sym,kind)(s,e)
        if lab: s.tag(e,lab,dx,dy)
        s.eqrange[tag]={L:(b0[L],len(s.items[L])) for L in LAYERS if len(s.items[L])>b0[L]}
        return e
    def tag(s,e,lab,dx=0,dy=0,size=None):
        size=size or TAG_FS
        x,y,w,h=e.x,e.y,e.w,e.h
        if lab=='b': s.text(x+w/2+dx,y+h+2.3+dy,e.tag,size,'m',True,owner=e.tag)
        elif lab=='t': s.text(x+w/2+dx,y-1.0+dy,e.tag,size,'m',True,owner=e.tag)
        elif lab=='l': s.text(x-1.0+dx,y+h/2+.7+dy,e.tag,size,'r',True,owner=e.tag)
        elif lab=='r': s.text(x+w+1.0+dx,y+h/2+.7+dy,e.tag,size,'l',True,owner=e.tag)
        elif lab=='c': s.text(x+w/2+dx,y+h/2+.7+dy,e.tag,size,'m',True,owner=e.tag)
        elif isinstance(lab,tuple): s.text(lab[0],lab[1],e.tag,size,lab[2] if len(lab)>2 else 'l',True,owner=e.tag)
    # -------------------------------------------------------- titik / nosel
    def pt(s,ref):
        """ref: 'TAG.side@f' | 'TAG.nama' | (x,y,dir) | ('J',x,y) | flag dict"""
        if isinstance(ref,dict): return ref['pt']
        if isinstance(ref,tuple):
            if ref[0]=='J': return (ref[1],ref[2],None)
            return ref
        tag,nz=ref.split('.',1)
        return s.eqs[tag].nozzle(nz)
    # -------------------------------------------------------- bendera batas
    def flag(s,text,x,y,d='r',kind='in',size=None,w=None,h=None,layer='proc',util=False):
        size=size or FLAG_FS; h=h or FLAG_H
        """bendera pentagon; (x,y)=pusat ujung yang tersambung garis.
        d = arah ujung lancip ('r' atau 'l'). kind 'in': garis keluar dari ujung lancip; 'out': garis masuk dari pangkal."""
        tw=twidth(text,size)
        w=w or tw+4.2
        p=1.6
        if d=='r':
            # ujung lancip di kanan
            if kind=='in': xt=x; x0=x-w
            else: x0=x; xt=x+w
            pts=[(x0,y-h/2),(xt-p,y-h/2),(xt,y),(xt-p,y+h/2),(x0,y+h/2)]
            cx=(x0+xt-p)/2
            conn=(xt,y,'R') if kind=='in' else (x0,y,'L')
        else:
            if kind=='in': xt=x; x0=x+w
            else: x0=x; xt=x-w
            pts=[(x0,y-h/2),(xt+p,y-h/2),(xt,y),(xt+p,y+h/2),(x0,y+h/2)]
            cx=(x0+xt+p)/2
            conn=(xt,y,'L') if kind=='in' else (x0,y,'R')
        col=UG if util else K
        s.poly(pts,.3 if not util else .22,'#ffffff',col,'label')
        s.text(cx,y+CAPC*size,text,size,'m',False,owner='flag',col=col)
        bb=(min(p_[0] for p_ in pts),y-h/2,max(p_[0] for p_ in pts),y+h/2)
        f=dict(pt=conn,bb=bb,text=text); s.flags.append(f); s.texts[-1]['owner']=('flag',id(f))
        return f
    # -------------------------------------------------------- routing
    def route(s,a,b,via=(),stub=2.2,stub_b=None):
        pa=s.pt(a); pb=s.pt(b)
        D={'L':(-1,0),'R':(1,0),'U':(0,-1),'D':(0,1),None:(0,0)}
        ax,ay,ad=pa; bx,by,bd=pb
        sb=stub if stub_b is None else stub_b
        P=[(ax,ay)]
        if ad: P.append((ax+D[ad][0]*stub,ay+D[ad][1]*stub))
        Q=(bx+D[bd][0]*sb,by+D[bd][1]*sb) if bd else (bx,by)
        for v in via:
            c,val=v[0],float(v[1:]) if isinstance(v,str) else v
            if isinstance(v,str):
                lx,ly=P[-1]
                P.append((val,ly) if c=='x' else (lx,val))
            else:
                P.append(tuple(v))
        # sambung ke Q
        lx,ly=P[-1]
        if abs(lx-Q[0])>1e-6 and abs(ly-Q[1])>1e-6:
            # pilih siku sehingga segmen terakhir masuk searah nosel
            if bd in ('U','D'): P.append((Q[0],ly))
            elif bd in ('L','R'): P.append((lx,Q[1]))
            else:
                # sambungan ke junction: lanjutkan orientasi segmen terakhir
                if len(P)>=2 and abs(P[-2][1]-ly)<1e-6: P.append((Q[0],ly))
                else: P.append((lx,Q[1]))
        P.append(Q)
        if bd: P.append((bx,by))
        return simplify(P)
    def conn(s,key,a,b,via=(),cls='proc',num=None,dseg=None,dpos=.5,util=None,arrow=True,stub=2.2,stub_b=None,
             dash=None,w=None,label=None,lpos=None,pts=None,arrow_mid=False):
        P=pts or s.route(a,b,via,stub,stub_b)
        p=dict(key=key,pts=P,cls=cls,num=num,util=util,arrow=arrow,dash=dash,w=w,arrow_mid=arrow_mid)
        s.paths.append(p)
        if isinstance(b,tuple) and b[0]=='J': p['arrow']=False
        if num is not None: s.diamond(p,num,dseg,dpos)
        return p
    def diamond(s,p,num,dseg=None,dpos=.5):
        P=p['pts']
        if dseg is None:
            L=[(math.dist(P[i],P[i+1]),i) for i in range(len(P)-1)]
            dseg=max(L)[1]
        if dseg<0: dseg=len(P)-1+dseg
        dseg=max(0,min(dseg,len(P)-2))
        (x0,y0),(x1,y1)=P[dseg],P[dseg+1]
        x=x0+(x1-x0)*dpos; y=y0+(y1-y0)*dpos
        d=dict(x=x,y=y,num=num,path=p,r=DIA_R if num<100 else DIA_R*1.14)
        s.diamonds.append(d); p['dia']=d
        return d
    def junction(s,x,y): s.junc.append((x,y))
    # -------------------------------------------------------- render jalur
    def finalize(s):
        """hitung celah persilangan, tulis jalur ke lapisan"""
        segs=[]
        for pi,p in enumerate(s.paths):
            for i in range(len(p['pts'])-1):
                segs.append((pi,i,p['pts'][i],p['pts'][i+1]))
        rank={'proc':3,'util':2,'sig':1}
        gaps={}  # (pi,i) -> list of param positions
        for (pa,ia,a0,a1) in segs:
            for (pb,ib,b0,b1) in segs:
                if pa>=pb: continue
                X=cross(a0,a1,b0,b1)
                if not X: continue
                ca,cb=s.paths[pa]['cls'],s.paths[pb]['cls']
                if 'sig' in (ca,cb): continue
                ha=abs(a0[1]-a1[1])<1e-6; hb=abs(b0[1]-b1[1])<1e-6
                if rank[ca]!=rank[cb]: brk=(pa,ia,a0,a1) if rank[ca]<rank[cb] else (pb,ib,b0,b1)
                else: brk=(pa,ia,a0,a1) if not ha else (pb,ib,b0,b1)
                gaps.setdefault((brk[0],brk[1]),[]).append(X)
        s.gaps=gaps
        for pi,p in enumerate(s.paths):
            cls=p['cls']
            if cls=='proc': w=p['w'] or LW_PROC; col=K; layer='proc'; dash=p['dash']; ah=AH_PROC
            elif cls=='util': w=p['w'] or LW_UTIL; col=UG; layer='util'; dash=p['dash']; ah=AH_UTIL
            else: w=p['w'] or LW_SIG; col=K; layer='sig'; dash=p['dash'] or [.9,.6]; ah=None
            P=list(p['pts'])
            if p['arrow'] and ah and len(P)>=2:
                (x0,y0),(x1,y1)=P[-2],P[-1]
                L=math.dist((x0,y0),(x1,y1)); ux,uy=(x1-x0)/L,(y1-y0)/L
                s.poly([(x1,y1),(x1-ux*ah[0]-uy*ah[1]/2,y1-uy*ah[0]+ux*ah[1]/2),(x1-ux*ah[0]+uy*ah[1]/2,y1-uy*ah[0]-ux*ah[1]/2)],.05,col,col,layer)
                P[-1]=(x1-ux*ah[0]*.85,y1-uy*ah[0]*.85)
            if p.get('arrow_mid') and ah:
                i=max(range(len(P)-1),key=lambda i:math.dist(P[i],P[i+1]))
                (x0,y0),(x1,y1)=P[i],P[i+1]; L=math.dist((x0,y0),(x1,y1)); ux,uy=(x1-x0)/L,(y1-y0)/L
                mx,my=(x0+x1)/2+ux*ah[0]/2,(y0+y1)/2+uy*ah[0]/2
                s.poly([(mx,my),(mx-ux*ah[0]-uy*ah[1]/2,my-uy*ah[0]+ux*ah[1]/2),(mx-ux*ah[0]+uy*ah[1]/2,my-uy*ah[0]-ux*ah[1]/2)],.05,col,col,layer)
            # pecah per celah
            pieces=[[P[0]]]
            for i in range(len(P)-1):
                a,b=P[i],P[i+1]
                g=sorted(s.gaps.get((pi,i),[]),key=lambda q:math.dist(a,q))
                L=math.dist(a,b)
                for q in g:
                    if L<1e-9: break
                    ux,uy=(b[0]-a[0])/L,(b[1]-a[1])/L
                    gp=.75 if cls!='util' else .6
                    pieces[-1].append((q[0]-ux*gp,q[1]-uy*gp)); pieces.append([(q[0]+ux*gp,q[1]+uy*gp)])
                pieces[-1].append(b)
            for pc in pieces:
                pc=simplify(pc)
                if len(pc)>=2: s.line(pc,w,dash,col,layer,'butt')
        for (x,y) in s.junc: s.circ(x,y,.62,.05,K,'proc',K)
        for d in s.diamonds:
            r=d['r']; x,y=d['x'],d['y']
            s.poly([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],.3,'#ffffff',K,'label')
            fs=DIA_FS if d['num']<100 else DIA_FS*.93; s.text(x,y+CAPC*fs,str(d['num']),fs,'m',True,owner=('dia',id(d)),chk=False)
    # -------------------------------------------------------- pemeriksa
    def check(s,verbose=True):
        issues=[]
        T=s.texts
        def ov(a,b,m=0): return a[0]<b[2]-m and b[0]<a[2]-m and a[1]<b[3]-m and b[1]<a[3]-m
        dbb=[((d['x']-d['r'],d['y']-d['r'],d['x']+d['r'],d['y']+d['r']),d) for d in s.diamonds]
        fbb=[(f['bb'],f) for f in s.flags]
        eqb=[(e.hit(),e) for e in s.eqs.values()]
        for i in range(len(T)):
            for j in range(i+1,len(T)):
                if ov(T[i]['bb'],T[j]['bb']): issues.append(('teks-teks',T[i]['t'],T[j]['t']))
        for t in T:
            for bb,d in dbb:
                if ov(t['bb'],bb): issues.append(('teks-diamond',t['t'],d['num']))
            for bb,f in fbb:
                if t['owner']==('flag',id(f)): continue
                if ov(t['bb'],bb): issues.append(('teks-bendera',t['t'],f['text']))
            for hb,e in eqb:
                if t['owner']==e.tag and e.inner_label: continue
                for h_ in hb:
                    bq=t['bb']; bq=(bq[0]-TM,bq[1]-TM,bq[2]+TM,bq[3]+TM)
                    if ov(bq,h_): issues.append(('teks-alat',t['t'],e.tag)); break
            if t.get('layer') in ('table',): continue
            for p in s.paths:
                if p['key'] in t.get('skip',()): continue
                for i in range(len(p['pts'])-1):
                    bq=t['bb']; bq=(bq[0]-TM,bq[1]-TM,bq[2]+TM,bq[3]+TM)
                    if seg_box(p['pts'][i],p['pts'][i+1],bq):
                        issues.append(('teks-garis',t['t'],p['key'])); break
        for i in range(len(dbb)):
            for j in range(i+1,len(dbb)):
                if ov(dbb[i][0],dbb[j][0]): issues.append(('diamond-diamond',dbb[i][1]['num'],dbb[j][1]['num']))
            for hb,e in eqb:
                for h_ in hb:
                    if ov(dbb[i][0],h_): issues.append(('diamond-alat',dbb[i][1]['num'],e.tag)); break
            for p in s.paths:
                if p is dbb[i][1]['path']: continue
                for k in range(len(p['pts'])-1):
                    if seg_box(p['pts'][k],p['pts'][k+1],dbb[i][0]): issues.append(('diamond-garis',dbb[i][1]['num'],p['key'])); break
            for bb,f in fbb:
                if ov(dbb[i][0],bb): issues.append(('diamond-bendera',dbb[i][1]['num'],f['text']))
        for i in range(len(fbb)):
            for j in range(i+1,len(fbb)):
                if ov(fbb[i][0],fbb[j][0]): issues.append(('bendera-bendera',fbb[i][1]['text'],fbb[j][1]['text']))
            for hb,e in eqb:
                for h_ in hb:
                    if ov(fbb[i][0],h_): issues.append(('bendera-alat',fbb[i][1]['text'],e.tag)); break
        E=list(s.eqs.values())
        for i in range(len(E)):
            for j in range(i+1,len(E)):
                if any(ov(a,b) for a in E[i].hit() for b in E[j].hit()): issues.append(('alat-alat',E[i].tag,E[j].tag))
        for p in s.paths:
            for k in range(len(p['pts'])-1):
                a,b=p['pts'][k],p['pts'][k+1]
                for hb,e in eqb:
                    for h_ in hb:
                        sh=(h_[0]+.45,h_[1]+.45,h_[2]-.45,h_[3]-.45)
                        if sh[0]<sh[2] and sh[1]<sh[3] and seg_box(a,b,sh): issues.append(('garis-alat',p['key'],e.tag)); break
                for bb,f in fbb:
                    sh=(bb[0]+.3,bb[1]+.3,bb[2]-.3,bb[3]-.3)
                    if seg_box(a,b,sh): issues.append(('garis-bendera',p['key'],f['text']))
        # garis kolinear bertumpuk
        segs=[(p['key'],p['pts'][k],p['pts'][k+1]) for p in s.paths for k in range(len(p['pts'])-1)]
        for i in range(len(segs)):
            for j in range(i+1,len(segs)):
                if segs[i][0]==segs[j][0]: continue
                if colin(segs[i][1],segs[i][2],segs[j][1],segs[j][2]): issues.append(('garis-tumpuk',segs[i][0],segs[j][0]))
        # di luar kertas
        for t in T:
            if t['bb'][0]<0 or t['bb'][2]>W or t['bb'][1]<0 or t['bb'][3]>H: issues.append(('teks-luar',t['t'],''))
        seen=set(); out=[]
        for q in issues:
            k=tuple(map(str,q))
            if k in seen: continue
            seen.add(k); out.append(q)
        if verbose:
            for q in out: print('  !',q)
        return out
    def xform(s,layers,sc,ox,oy,bx,by):
        """skala seragam lapisan gambar: x' = ox+(x-bx)*sc"""
        X=lambda x,y:(ox+(x-bx)*sc,oy+(y-by)*sc)
        for L in layers:
            new=[]
            for it in s.items[L]:
                t=it[0]
                if t=='line': new.append(('line',[X(*p) for p in it[1]])+it[2:])
                elif t=='poly': new.append(('poly',[X(*p) for p in it[1]])+it[2:])
                elif t=='circ': x,y=X(it[1],it[2]); new.append(('circ',x,y,it[3]*sc)+it[4:])
                elif t=='text': x,y=X(it[1],it[2]); new.append(('text',x,y,it[3],it[4]*sc)+it[5:])
            s.items[L]=new
        s.X=X
    # -------------------------------------------------------- keluaran
    def pdf(s,path):
        from reportlab.pdfgen import canvas
        k=72/25.4
        c=canvas.Canvas(path,pagesize=(W*k,H*k))
        c.setTitle(DOC_TITLE); c.setAuthor(DOC_AUTHOR)
        def col(cc):
            h=cc.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
        for L in LAYERS:
            for it in s.items[L]:
                t=it[0]
                if t=='line':
                    _,pts,w,dash,cl,cap=it
                    c.setLineWidth(w*k); c.setStrokeColorRGB(*col(cl)); c.setDash([d*k for d in dash] if dash else [])
                    c.setLineCap({'butt':0,'round':1,'square':2}[cap]); c.setLineJoin(0 if cap=='butt' else 1)
                    pth=c.beginPath(); pth.moveTo(pts[0][0]*k,(H-pts[0][1])*k)
                    for x,y in pts[1:]: pth.lineTo(x*k,(H-y)*k)
                    c.drawPath(pth,stroke=1,fill=0)
                elif t=='poly':
                    _,pts,w,fill,cl,dash=it
                    c.setLineWidth(w*k); c.setStrokeColorRGB(*col(cl)); c.setDash([d*k for d in dash] if dash else []); c.setLineJoin(0)
                    if fill: c.setFillColorRGB(*col(fill))
                    pth=c.beginPath(); pth.moveTo(pts[0][0]*k,(H-pts[0][1])*k)
                    for x,y in pts[1:]: pth.lineTo(x*k,(H-y)*k)
                    pth.close(); c.drawPath(pth,stroke=1 if w>0 else 0,fill=1 if fill else 0)
                elif t=='circ':
                    _,cx,cy,r,w,fill,cl=it
                    c.setLineWidth(w*k); c.setStrokeColorRGB(*col(cl)); c.setDash([])
                    if fill: c.setFillColorRGB(*col(fill))
                    c.circle(cx*k,(H-cy)*k,r*k,stroke=1 if w>0 else 0,fill=1 if fill else 0)
                elif t=='text':
                    _,x,y,tx,size,anchor,bold,rot,cl,ital=it
                    c.saveState(); c.setFillColorRGB(*col(cl)); c.translate(x*k,(H-y)*k)
                    if rot: c.rotate(rot)
                    wd=twidth(tx,size,bold,ital); xx={'l':0,'m':-wd/2,'r':-wd}[anchor]
                    for r_,sb,it in runs(tx):
                        fs=size*(SUBF if sb else 1); fn=font(bold,ital or it)
                        to=c.beginText(); to.setTextRenderMode(2); to.setFont(fn,fs*k)
                        c.setStrokeColorRGB(*col(cl)); c.setLineWidth(TEXT_STROKE*fs*k); c.setLineJoin(1); c.setDash([])
                        to.setTextOrigin(xx*k,(-size*SUBD if sb else 0)*k); to.textOut(r_); c.drawText(to)
                        xx+=pdfmetrics.stringWidth(r_,fn,fs)
                    c.restoreState()
        c.showPage(); c.save()
    def svg(s,path):
        o=['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" font-family="Arial, \'Liberation Sans\', Helvetica, sans-serif">',
           '<rect width="594" height="420" fill="#ffffff"/>']
        def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        for L in LAYERS:
            o.append(f'<g inkscape:groupmode="layer" inkscape:label="{LAYER_NAME[L]}" id="lapisan-{L}">')
            for it in s.items[L]:
                t=it[0]
                if t=='line':
                    _,pts,w,dash,cl,cap=it
                    d=' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)
                    da=f' stroke-dasharray="{" ".join(f"{v:g}" for v in dash)}"' if dash else ''
                    o.append(f'<polyline points="{d}" fill="none" stroke="{cl}" stroke-width="{w:g}" stroke-linecap="{cap}" stroke-linejoin="{"miter" if cap=="butt" else "round"}"{da}/>')
                elif t=='poly':
                    _,pts,w,fill,cl,dash=it
                    d=' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)
                    da=f' stroke-dasharray="{" ".join(f"{v:g}" for v in dash)}"' if dash else ''
                    st=f'stroke="{cl}" stroke-width="{w:g}"' if w>0 else 'stroke="none"'
                    o.append(f'<polygon points="{d}" fill="{fill or "none"}" {st}{da}/>')
                elif t=='circ':
                    _,cx,cy,r,w,fill,cl=it
                    st=f'stroke="{cl}" stroke-width="{w:g}"' if w>0 else 'stroke="none"'
                    o.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="{fill or "none"}" {st}/>')
                elif t=='text':
                    _,x,y,tx,size,anchor,bold,rot,cl,ital=it
                    an={'l':'start','m':'middle','r':'end'}[anchor]
                    tr=f' transform="rotate({-rot} {x:.3f} {y:.3f})"' if rot else ''
                    fw=' font-weight="bold"' if bold else ''
                    fi=' font-style="italic"' if ital else ''
                    sp=[]; low=False
                    for r_,sb,it in runs(tx):
                        st=' font-style="italic"' if it else ''
                        if sb and not low: sp.append(f'<tspan font-size="{size*SUBF:.3f}" dy="{size*SUBD:.3f}"{st}>{esc(r_)}</tspan>'); low=True
                        elif sb: sp.append(f'<tspan font-size="{size*SUBF:.3f}"{st}>{esc(r_)}</tspan>')
                        elif low: sp.append(f'<tspan font-size="{size:.3f}" dy="{-size*SUBD:.3f}"{st}>{esc(r_)}</tspan>'); low=False
                        else: sp.append(f'<tspan{st}>{esc(r_)}</tspan>')
                    o.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size:g}" text-anchor="{an}" fill="{cl}"{fw}{fi}{tr} xml:space="preserve">{"".join(sp)}</text>')
            o.append('</g>')
        o.append('</svg>')
        open(path,'w',encoding='utf-8').write('\n'.join(o))
# ---------------------------------------------------------------- geometri
def simplify(P):
    Q=[]
    for p in P:
        p=(round(p[0],4),round(p[1],4))
        if Q and abs(Q[-1][0]-p[0])<1e-6 and abs(Q[-1][1]-p[1])<1e-6: continue
        Q.append(p)
    R=[]
    for p in Q:
        while len(R)>=2 and ((abs(R[-2][0]-R[-1][0])<1e-6 and abs(R[-1][0]-p[0])<1e-6) or (abs(R[-2][1]-R[-1][1])<1e-6 and abs(R[-1][1]-p[1])<1e-6)):
            R.pop()
        R.append(p)
    return R
def cross(a0,a1,b0,b1):
    ha=abs(a0[1]-a1[1])<1e-6; va=abs(a0[0]-a1[0])<1e-6
    hb=abs(b0[1]-b1[1])<1e-6; vb=abs(b0[0]-b1[0])<1e-6
    if ha and vb: h0,h1,v0,v1=a0,a1,b0,b1
    elif va and hb: h0,h1,v0,v1=b0,b1,a0,a1
    else: return None
    x=v0[0]; y=h0[1]
    e=.5
    if min(h0[0],h1[0])+e<x<max(h0[0],h1[0])-e and min(v0[1],v1[1])+e<y<max(v0[1],v1[1])-e: return (x,y)
    return None
def seg_box(a,b,bb):
    x0,y0,x1,y1=bb
    if abs(a[1]-b[1])<1e-6:
        y=a[1]; lo,hi=sorted((a[0],b[0]))
        return y0<y<y1 and lo<x1 and hi>x0
    if abs(a[0]-b[0])<1e-6:
        x=a[0]; lo,hi=sorted((a[1],b[1]))
        return x0<x<x1 and lo<y1 and hi>y0
    # miring: sampel
    for i in range(21):
        x=a[0]+(b[0]-a[0])*i/20; y=a[1]+(b[1]-a[1])*i/20
        if x0<x<x1 and y0<y<y1: return True
    return False
def colin(a0,a1,b0,b1,e=.35):
    if abs(a0[1]-a1[1])<1e-6 and abs(b0[1]-b1[1])<1e-6 and abs(a0[1]-b0[1])<e:
        lo=max(min(a0[0],a1[0]),min(b0[0],b1[0])); hi=min(max(a0[0],a1[0]),max(b0[0],b1[0]))
        return hi-lo>.4
    if abs(a0[0]-a1[0])<1e-6 and abs(b0[0]-b1[0])<1e-6 and abs(a0[0]-b0[0])<e:
        lo=max(min(a0[1],a1[1]),min(b0[1],b1[1])); hi=min(max(a0[1],a1[1]),max(b0[1],b1[1]))
        return hi-lo>.4
    return False
# ---------------------------------------------------------------- peralatan
class Eq:
    def __init__(s,doc,kind,tag,x,y,w,h,nz=None,hitbox=None,inner_label=False,**kw):
        s.__dict__.update(kw); s.doc=doc; s.kind=kind; s.tag=tag; s.x,s.y,s.w,s.h=x,y,w,h; s.nz=nz or {}; s.hitbox=hitbox; s.inner_label=inner_label
    def hit(s):
        hb=s.hitbox
        if not hb and s.kind in ('vessel','agit','column','evap','quench'): hb=[(.18,.03,.82,.97),(0,.12,1,.88)]
        if not hb and s.kind=='cryst': hb=[(.18,0,.82,1),(0,.12,1,.62),(.3,.62,.7,1)]
        if not hb and s.kind in ('silo','cyclone','classifier','thick','bag'): hb=[(0,.06,1,.55),(.3,.55,.7,1)]
        if hb: return [(s.x+a*s.w,s.y+b*s.h,s.x+c*s.w,s.y+d*s.h) for a,b,c,d in hb]
        return [(s.x,s.y,s.x+s.w,s.y+s.h)]
    def nozzle(s,nz):
        if nz in s.nz:
            fx,fy,d=s.nz[nz]; return (s.x+fx*s.w,s.y+fy*s.h,d)
        side,_,f=nz.partition('@'); f=float(f) if f else .5
        x,y,w,h=s.x,s.y,s.w,s.h
        sf=getattr(Surf,s.kind,None)
        if sf:
            r=sf(s,side,f)
            if r: return r
        return {'l':(x,y+f*h,'L'),'r':(x+w,y+f*h,'R'),'t':(x+f*w,y,'U'),'b':(x+f*w,y+h,'D')}[side]
class Surf:
    """titik permukaan khusus per bentuk"""
    @staticmethod
    def _head(e,side,f,r):
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2; xx=x+f*w
        u=min(1,abs(xx-cx)/(w/2)); dy=r*(1-math.sqrt(max(0,1-u*u)))
        if side=='t': return (xx,y+dy,'U')
        if side=='b': return (xx,y+h-dy,'D')
    @staticmethod
    def vessel(e,side,f): return Surf._head(e,side,f,min(e.w/2,e.h*.15)) if side in 'tb' else None
    @staticmethod
    def agit(e,side,f):
        if side=='b': return Surf._head(e,side,f,min(e.w/2,e.h*.15))
        if side=='t': return Surf._head(e,side,f,min(e.w/2,e.h*.15))
    @staticmethod
    def column(e,side,f): return Surf._head(e,side,f,min(e.w/2,e.h*.06)) if side in 'tb' else None
    @staticmethod
    def evap(e,side,f): return Surf._head(e,side,f,min(e.w/2,e.h*.14)) if side in 'tb' else None
    @staticmethod
    def pump(e,side,f):
        r=e.w/2; cx,cy=e.x+r,e.y+e.h-r
        if side=='l': return (cx-r,cy,'L')
        if side=='r': return (cx+r,cy,'R')
        if side=='t': return (cx,cy-r,'U')
        if side=='b': return (cx,cy+r,'D')
    fan=pump
# ---------------------------------------------------------------- simbol
class Sym:
    """setiap simbol menggambar dalam kotak (x,y,w,h) dengan isian putih"""
    WF='#ffffff'
    @staticmethod
    def vessel(d,e,heads=True):
        x,y,w,h=e.x,e.y,e.w,e.h; r=min(w/2,h*.15)
        pts=d.arcpts(x+w/2,y+r,w/2,r,180,0)+d.arcpts(x+w/2,y+h-r,w/2,r,360,180)
        d.poly(pts,.4,Sym.WF)
    @staticmethod
    def agit(d,e):
        Sym.vessel(d,e); x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2; r=min(w/2,h*.15)
        d.rect(cx-1.3,y-2.6,2.6,1.6,.3,Sym.WF)          # motor
        d.line([(cx,y-1.0),(cx,y+h*.74)],.3)
        d.line([(cx-w*.24,y+h*.74),(cx+w*.24,y+h*.74)],.6)  # impeler
        d.line([(x+.0,y+r+.0),(x,y+r)],.1)
        for f in (.25,.75):  # baffle
            pass
    @staticmethod
    def tank(d,e):   # tangki atap datar
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF); d.line([(x,y+1.0),(x+w,y+1.0)],.2)
    @staticmethod
    def ctank(d,e):  # tangki dengan atap kerucut + agitator (bubur)
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y+1.2),(cx,y),(x+w,y+1.2),(x+w,y+h),(x,y+h)],.4,Sym.WF)
        d.rect(cx-1.1,y-2.2,2.2,1.4,.3,Sym.WF); d.line([(cx,y-.8),(cx,y+h*.72)],.3); d.line([(cx-w*.22,y+h*.72),(cx+w*.22,y+h*.72)],.55)
    @staticmethod
    def column(d,e,trays=10,packed=False):
        x,y,w,h=e.x,e.y,e.w,e.h; r=min(w/2,h*.06)
        pts=d.arcpts(x+w/2,y+r,w/2,r,180,0)+d.arcpts(x+w/2,y+h-r,w/2,r,360,180)
        d.poly(pts,.45,Sym.WF)
        n=e.__dict__.get('trays',trays)
        if e.__dict__.get('packed'):
            for (a,b) in ((.18,.45),(.55,.82)):
                ya,yb=y+h*a,y+h*b
                d.line([(x,ya),(x+w,ya)],.2); d.line([(x,yb),(x+w,yb)],.2)
                d.line([(x,ya),(x+w,yb)],.15); d.line([(x+w,ya),(x,yb)],.15)
        else:
            for i in range(n):
                yy=y+h*(.14+.72*i/(n-1));
                if i%2: d.line([(x+w*.3,yy),(x+w,yy)],.2)
                else: d.line([(x,yy),(x+w*.7,yy)],.2)
    @staticmethod
    def thick(d,e):   # thickener: tangki lebar dangkal + dasar kerucut + rake
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y),(x+w,y),(x+w,y+h*.55),(cx+w*.06,y+h),(cx-w*.06,y+h),(x,y+h*.55)],.45,Sym.WF)
        d.line([(cx,y-2.4),(cx,y+h*.72)],.3); d.rect(cx-1.4,y-3.6,2.8,1.3,.3,Sym.WF)
        d.line([(x+w*.12,y+h*.5),(cx,y+h*.74),(x+w*.88,y+h*.5)],.3)  # rake
        d.line([(x+w*.30,y+h*.10),(x+w*.30,y+h*.30)],.15); d.line([(x+w*.70,y+h*.10),(x+w*.70,y+h*.30)],.15)  # feedwell
        d.line([(x+w*.30,y+h*.30),(x+w*.70,y+h*.30)],.15)
        d.line([(x+w-2,y+h*.06),(x+w-.3,y+h*.06)],.2)  # launder
    @staticmethod
    def cyclone(d,e):
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y),(x+w,y),(x+w,y+h*.38),(cx+w*.1,y+h),(cx-w*.1,y+h),(x,y+h*.38)],.4,Sym.WF)
        d.line([(cx-w*.18,y-1.6),(cx-w*.18,y+h*.3)],.25); d.line([(cx+w*.18,y-1.6),(cx+w*.18,y+h*.3)],.25)
        d.line([(cx-w*.18,y-1.6),(cx+w*.18,y-1.6)],.25)
    @staticmethod
    def hydrocyclone(d,e): Sym.cyclone(d,e)
    @staticmethod
    def bag(d,e):     # baghouse: kotak + kantong + hopper
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y),(x+w,y),(x+w,y+h*.62),(x+w*.6,y+h),(x+w*.4,y+h),(x,y+h*.62)],.4,Sym.WF)
        n=4
        for i in range(n):
            xx=x+w*(i+1)/(n+1); d.line([(xx,y+h*.08),(xx,y+h*.52)],.55)
        d.line([(x,y+h*.06),(x+w,y+h*.06)],.2)
    @staticmethod
    def esp(d,e):
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y),(x+w,y),(x+w,y+h*.66),(x+w*.82,y+h),(x+w*.62,y+h),(x+w*.5,y+h*.72),(x+w*.38,y+h),(x+w*.18,y+h),(x,y+h*.66)],.4,Sym.WF)
        for i in range(5):
            xx=x+w*(i+1)/6
            if i%2==0: d.line([(xx,y+h*.08),(xx,y+h*.6)],.35)
            else:
                pts=[(xx+(.5 if k%2 else -.5),y+h*.08+k*(h*.52/8)) for k in range(9)]; d.line(pts,.18)
    @staticmethod
    def mill(d,e):     # ball mill: drum + ujung kerucut + trunnion + bola
        x,y,w,h=e.x,e.y,e.w,e.h; cy=y+h/2; c=w*.1
        d.poly([(x,cy-h*.18),(x+c,y),(x+w-c,y),(x+w,cy-h*.18),(x+w,cy+h*.18),(x+w-c,y+h),(x+c,y+h),(x,cy+h*.18)],.45,Sym.WF)
        d.line([(x+c,y),(x+c,y+h)],.2); d.line([(x+w-c,y),(x+w-c,y+h)],.2)
        d.rect(x+w*.55,y-.9,w*.1,h+1.8,.3,Sym.WF)  # girth gear
        import random; rnd=random.Random(3)
        for i in range(9):
            bx=x+c+1.2+(w-2*c-2.4)*((i*0.37)%1); by=cy+h*.05+rnd.uniform(0,h*.3)
            if abs(bx-(x+w*.6))>w*.07: d.circ(bx,by,.55,.18,None)
    @staticmethod
    def kiln(d,e):     # kiln rotari: silinder panjang miring + riding ring + hood
        x,y,w,h=e.x,e.y,e.w,e.h
        hw=w*.07
        d.rect(x,y-h*.35,hw,h*1.7,.4,Sym.WF)          # hood umpan
        d.rect(x+w-hw,y-h*.35,hw,h*1.7,.4,Sym.WF)     # hood bakar
        d.rect(x+hw,y,w-2*hw,h,.45,Sym.WF)
        for f in (.25,.55,.82):
            xx=x+hw+(w-2*hw)*f; d.rect(xx-.8,y-.8,1.6,h+1.6,.3,Sym.WF)
        d.line([(x+hw+1,y+h*.72),(x+w-hw-1,y+h*.86)],.15)   # bed
        d.line([(x+w*.40,y+h+.8),(x+w*.40,y+h+2.2)],.2); d.line([(x+w*.40-1.5,y+h+2.2),(x+w*.40+1.5,y+h+2.2)],.2)
    @staticmethod
    def drum(d,e):     # pendingin/pengering rotari
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.45,Sym.WF)
        for f in (.22,.78):
            xx=x+w*f; d.rect(xx-.7,y-.7,1.4,h+1.4,.3,Sym.WF)
        d.line([(x+w*.06,y+h*.25),(x+w*.94,y+h*.25)],.12); d.line([(x+w*.06,y+h*.75),(x+w*.94,y+h*.75)],.12)
    @staticmethod
    def dryer(d,e): Sym.drum(d,e)
    @staticmethod
    def boiler(d,e):   # boiler/WHRB: casing + tube bank + steam drum
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y+h*.18,w,h*.82,.45,Sym.WF)
        dr=h*.16
        d.poly(d.arcpts(x+w*.2+dr/2,y+dr/2+.2,dr/2,dr/2,90,270)+d.arcpts(x+w*.8-dr/2,y+dr/2+.2,dr/2,dr/2,-90,90),.4,Sym.WF)
        for i in range(6):
            xx=x+w*(.16+.68*i/5); d.line([(xx,y+h*.24),(xx,y+h*.9)],.2)
        d.line([(x+w*.16,y+h*.9),(x+w*.84,y+h*.9)],.2)
    @staticmethod
    def fboiler(d,e):  # boiler berbahan bakar (dengan nyala)
        Sym.boiler(d,e); x,y,w,h=e.x,e.y,e.w,e.h
        fx,fy=x+w*.5,y+h*.78
        d.poly([(fx-1.6,fy+1.6),(fx-.4,fy-1.4),(fx,fy-.2),(fx+.5,fy-2.0),(fx+1.6,fy+1.6)],.2,Sym.WF)
    @staticmethod
    def hx(d,e):      # penukar panas shell-and-tube (horizontal)
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF)
        d.line([(x,y+h/2),(x+w*.15,y+h/2)],.3)
        n=6; pts=[(x+w*.15,y+h/2)]
        for i in range(n): pts.append((x+w*(.15+.7*(i+.5)/n),y+h*(.15 if i%2==0 else .85)))
        pts.append((x+w*.85,y+h/2)); pts.append((x+w,y+h/2)); d.line(pts,.3)
    @staticmethod
    def hxc(d,e):     # penukar panas simbol lingkaran (ISO) untuk pendingin kecil
        x,y,w,h=e.x,e.y,e.w,e.h; r=min(w,h)/2; cx,cy=x+w/2,y+h/2
        d.circ(cx,cy,r,.4,Sym.WF)
        d.line([(cx-r,cy),(cx-r*.45,cy),(cx-r*.15,cy-r*.55),(cx+r*.15,cy+r*.55),(cx+r*.45,cy),(cx+r,cy)],.3)
    @staticmethod
    def reboiler(d,e):  # kettle
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly(d.arcpts(x+h*.35,y+h*.65,h*.35,h*.35,90,270)+[(x+w*.35,y+h),(x+w*.55,y+h)]+d.arcpts(x+w-h*.5,y+h/2,h*.5,h*.5,-90,90)+[(x+w*.55,y),(x+w*.35,y+h*.3)],.4,Sym.WF)
        d.line([(x+.4,y+h*.65),(x+w*.7,y+h*.65)],.25)
    @staticmethod
    def pump(d,e):    # pompa sentrifugal: lingkaran + segitiga ke arah buang (atas)
        r=e.w/2; cx,cy=e.x+r,e.y+e.h-r
        d.circ(cx,cy,r,.4,Sym.WF)
        d.line([(cx-r*.866,cy+r*.5),(cx,cy-r),(cx+r*.866,cy+r*.5)],.3)
        d.line([(cx-r*.75,cy+r+.6),(cx+r*.75,cy+r+.6)],.3)
        d.line([(cx-r*.5,cy+r*.86),(cx-r*.75,cy+r+.6)],.3); d.line([(cx+r*.5,cy+r*.86),(cx+r*.75,cy+r+.6)],.3)
    @staticmethod
    def fan(d,e):     # fan sentrifugal: lingkaran + rumah volute
        r=e.w/2; cx,cy=e.x+r,e.y+e.h-r
        d.circ(cx,cy,r,.4,Sym.WF)
        for a in (90,210,330):
            d.line([(cx,cy),(cx+r*.8*math.cos(math.radians(a)),cy-r*.8*math.sin(math.radians(a)))],.25)
        d.circ(cx,cy,r*.18,.2,'#000000')
    @staticmethod
    def comp(d,e):    # kompresor/blower: trapesium (sisi lebar = hisap)
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y),(x+w,y+h*.28),(x+w,y+h*.72),(x,y+h)],.4,Sym.WF)
        d.circ(x+w*.4,y+h*.5,min(w,h)*.12,.2,None)
    @staticmethod
    def bfilter(d,e):  # filter sabuk vakum: sabuk + rol + kotak vakum
        x,y,w,h=e.x,e.y,e.w,e.h; r=h*.32
        d.poly(d.arcpts(x+r,y+r,r,r,90,270)+d.arcpts(x+w-r,y+r,r,r,-90,90),.45,Sym.WF)
        d.circ(x+r,y+r,r*.55,.25,None); d.circ(x+w-r,y+r,r*.55,.25,None)
        for i in range(4):
            xx=x+w*(.24+.15*i); d.poly([(xx,y+2*r+.0),(xx+w*.11,y+2*r),(xx+w*.08,y+h),(xx+w*.03,y+h)],.25,Sym.WF)
        for i in range(3): d.line([(x+w*(.3+.18*i),y-.2),(x+w*(.3+.18*i),y-1.4)],.2)
    @staticmethod
    def press(d,e):    # filter press: rangka + pelat
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF)
        n=max(5,int(w/1.3))
        for i in range(1,n):
            xx=x+w*i/n; d.line([(xx,y+h*.12),(xx,y+h*.88)],.18)
        d.rect(x-1.2,y+h*.25,1.2,h*.5,.3,Sym.WF)
    @staticmethod
    def centr(d,e):    # sentrifus (keranjang)
        x,y,w,h=e.x,e.y,e.w,e.h; cx,cy=x+w/2,y+h/2
        d.rect(x,y,w,h,.4,Sym.WF)
        d.circ(cx,cy,min(w,h)*.33,.3,None)
        d.line([(cx,cy-min(w,h)*.33),(cx,y-1.0)],.25)
        d.line([(cx-min(w,h)*.2,cy),(cx+min(w,h)*.2,cy)],.2)
    @staticmethod
    def evap(d,e):     # evaporator: badan uap + kalandria (tabung)
        x,y,w,h=e.x,e.y,e.w,e.h; r=min(w/2,h*.14)
        pts=d.arcpts(x+w/2,y+r,w/2,r,180,0)+d.arcpts(x+w/2,y+h-r,w/2,r,360,180)
        d.poly(pts,.45,Sym.WF)
        ya,yb=y+h*.5,y+h*.84
        d.line([(x,ya),(x+w,ya)],.25); d.line([(x,yb),(x+w,yb)],.25)
        for i in range(5):
            xx=x+w*(.18+.64*i/4); d.line([(xx,ya),(xx,yb)],.2)
        d.line([(x+w*.12,y+h*.28),(x+w*.88,y+h*.28)],.12)  # pemisah droplet
        d.line([(x+w*.12,y+h*.25),(x+w*.88,y+h*.31)],.12); d.line([(x+w*.12,y+h*.31),(x+w*.88,y+h*.25)],.12)
    @staticmethod
    def cryst(d,e):    # kristaliser DTB: badan + kerucut + draft tube + agitator
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly(d.arcpts(cx,y+w*.18,w/2,w*.18,180,0)+[(x+w,y+h*.62),(cx+w*.08,y+h),(cx-w*.08,y+h),(x,y+h*.62)],.45,Sym.WF)
        d.line([(cx-w*.2,y+h*.22),(cx-w*.2,y+h*.58)],.2); d.line([(cx+w*.2,y+h*.22),(cx+w*.2,y+h*.58)],.2)
        d.line([(cx,y-1.8),(cx,y+h*.6)],.3); d.rect(cx-1.1,y-3.0,2.2,1.3,.3,Sym.WF)
        d.line([(cx-w*.14,y+h*.6),(cx+w*.14,y+h*.6)],.5)
    @staticmethod
    def stack(d,e):
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x+w*.22,y),(x+w*.78,y),(x+w,y+h),(x,y+h)],.4,Sym.WF)
        d.line([(x+w*.18,y+h*.12),(x+w*.82,y+h*.12)],.2)
    @staticmethod
    def silo(d,e):     # silo/bin: badan + hopper kerucut
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y+h*.06),(cx,y),(x+w,y+h*.06),(x+w,y+h*.62),(cx+w*.1,y+h),(cx-w*.1,y+h),(x,y+h*.62)],.4,Sym.WF)
    @staticmethod
    def hopper(d,e):   # hopper penerima + grizzly
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y),(x+w,y),(cx+w*.14,y+h),(cx-w*.14,y+h)],.4,Sym.WF)
        for i in range(5):
            xx=x+w*(.1+.2*i); d.line([(xx,y+.6),(xx+w*.08,y+.6)],.3)
        d.line([(x-.8,y+.6),(x+w+.8,y+.6)],.2)
    @staticmethod
    def feeder(d,e):   # belt/weigh/apron feeder: sabuk pendek + rol
        x,y,w,h=e.x,e.y,e.w,e.h; r=h/2
        d.poly(d.arcpts(x+r,y+r,r,r,90,270)+d.arcpts(x+w-r,y+r,r,r,-90,90),.35,Sym.WF)
        d.circ(x+r,y+r,r*.5,.2,None); d.circ(x+w-r,y+r,r*.5,.2,None)
    @staticmethod
    def wfeeder(d,e):  # weigh feeder: feeder + sel beban (segitiga)
        Sym.feeder(d,e); x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x+w/2,y+h),(x+w/2-.9,y+h+1.2),(x+w/2+.9,y+h+1.2)],.25,Sym.WF)
    @staticmethod
    def conv(d,e):     # konveyor sabuk (garis miring/horizontal antar rol)
        x,y,w,h=e.x,e.y,e.w,e.h; r=h/2
        d.poly(d.arcpts(x+r,y+r,r,r,90,270)+d.arcpts(x+w-r,y+r,r,r,-90,90),.35,Sym.WF)
        d.circ(x+r,y+r,r*.45,.2,None); d.circ(x+w-r,y+r,r*.45,.2,None)
        for i in range(1,6): d.circ(x+r+(w-2*r)*i/6,y+h,.28,.12,None)
    @staticmethod
    def elev(d,e):     # elevator ember
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF); d.circ(x+w/2,y+w/2,w*.32,.2,None); d.circ(x+w/2,y+h-w/2,w*.32,.2,None)
        d.line([(x+w*.18,y+w/2),(x+w*.18,y+h-w/2)],.15); d.line([(x+w*.82,y+w/2),(x+w*.82,y+h-w/2)],.15)
        for i in range(6):
            yy=y+w*.8+(h-w*1.6)*i/5; d.line([(x+w*.82,yy),(x+w*.95,yy+.4)],.15)
    @staticmethod
    def stock(d,e):    # stockpile + reklaimer
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y+h),(x+w*.38,y),(x+w*.62,y),(x+w,y+h)],.4,Sym.WF)
        d.line([(x-1.0,y+h),(x+w+1.0,y+h)],.3)
        d.line([(x+w*.2,y+h*.62),(x+w*.8,y+h*.62)],.15)
    @staticmethod
    def screw(d,e):    # screw feeder
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.35,Sym.WF)
        pts=[(x+.5+i*(w-1)/12,y+(h*.18 if i%2 else h*.82)) for i in range(13)]; d.line(pts,.2)
    @staticmethod
    def pugmill(d,e):  # pencampur pugmill: palung + poros berpedal
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y),(x+w,y),(x+w,y+h*.6),(x+w-h*.4,y+h),(x+h*.4,y+h),(x,y+h*.6)],.4,Sym.WF)
        d.line([(x-.8,y+h*.5),(x+w+.8,y+h*.5)],.3)
        for i in range(7):
            xx=x+w*(.12+.76*i/6); d.line([(xx-.5,y+h*.3),(xx+.5,y+h*.7)],.25)
    @staticmethod
    def hims(d,e):     # separator magnetik drum basah: bak + drum berputar + busur magnet tetap
        x,y,w,h=e.x,e.y,e.w,e.h; r=h*.34; cx,cy=x+w/2,y+h*.4
        d.poly([(x,y+h*.3),(x+w,y+h*.3),(x+w,y+h*.72),(x+w*.6,y+h),(x+w*.4,y+h),(x,y+h*.72)],.4,Sym.WF)
        d.circ(cx,cy,r,.4,Sym.WF)
        d.arc(cx,cy,r*.7,r*.7,200,340,.7)
        d.line([(cx-r*.15,cy),(cx+r*.15,cy)],.2); d.line([(cx,cy-r*.15),(cx,cy+r*.15)],.2)
    @staticmethod
    def vrm(d,e):      # vertical roller mill: badan + meja + rol + separator atas
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x+w*.18,y),(x+w*.82,y),(x+w*.82,y+h*.28),(x+w,y+h*.42),(x+w,y+h),(x,y+h),(x,y+h*.42),(x+w*.18,y+h*.28)],.45,Sym.WF)
        d.line([(x+w*.12,y+h*.82),(x+w*.88,y+h*.82)],.5)
        d.circ(x+w*.32,y+h*.7,h*.1,.3,None); d.circ(x+w*.68,y+h*.7,h*.1,.3,None)
        for i in range(4):
            xx=x+w*(.3+.4*i/3); d.line([(xx,y+h*.06),(xx,y+h*.24)],.2)
        d.line([(cx,y+h*.82),(cx,y+h+1.2)],.3)
    @staticmethod
    def hgg(d,e):      # generator gas panas
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF)
        fx,fy=x+w*.42,y+h*.55
        d.poly([(fx-1.8,fy+1.6),(fx-.5,fy-1.6),(fx,fy-.2),(fx+.6,fy-2.2),(fx+1.8,fy+1.6)],.2,Sym.WF)
        d.line([(x+w*.72,y+h*.2),(x+w*.72,y+h*.8)],.2)
    @staticmethod
    def pulv(d,e):     # pulverizer batubara
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF)
        d.circ(x+w*.35,y+h*.65,h*.18,.25,None); d.circ(x+w*.65,y+h*.65,h*.18,.25,None)
        d.line([(x+w*.15,y+h*.86),(x+w*.85,y+h*.86)],.35)
    @staticmethod
    def classifier(d,e):  # klasifier dinamis: badan silinder + rotor sangkar + kerucut
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y),(x+w,y),(x+w,y+h*.55),(cx+w*.12,y+h),(cx-w*.12,y+h),(x,y+h*.55)],.4,Sym.WF)
        d.rect(cx-w*.22,y+h*.1,w*.44,h*.32,.25,None)
        for i in range(4):
            xx=cx-w*.22+w*.44*(i+.5)/4; d.line([(xx,y+h*.1),(xx,y+h*.42)],.15)
        d.line([(cx,y-1.6),(cx,y+h*.1)],.3); d.rect(cx-1.0,y-2.8,2.0,1.2,.3,Sym.WF)
    @staticmethod
    def mixsettle(d,e):   # mixer-settler bertahap
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.45,Sym.WF)
        n=e.__dict__.get('stages',3)
        for i in range(n):
            x0=x+w*i/n; x1=x+w*(i+1)/n
            if i: d.line([(x0,y),(x0,y+h)],.35)
            m=x0+(x1-x0)*.28
            d.line([(m,y),(m,y+h)],.18)
            cx=(x0+m)/2; d.line([(cx,y-1.2),(cx,y+h*.6)],.22); d.line([(cx-(m-x0)*.3,y+h*.6),(cx+(m-x0)*.3,y+h*.6)],.4)
            d.line([(m+.4,y+h*.42),(x1-.4,y+h*.42)],.12)
    @staticmethod
    def ct(d,e):       # menara pendingin induced draft
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x+w*.12,y+h*.16),(x+w*.88,y+h*.16),(x+w,y+h*.86),(x,y+h*.86)],.45,Sym.WF)
        d.rect(x-.6,y+h*.86,w+1.2,h*.14,.4,Sym.WF)   # basin
        d.rect(x+w*.34,y,w*.32,h*.16,.35,Sym.WF)     # cerobong fan
        d.line([(x+w*.36,y+h*.1),(x+w*.64,y+h*.1)],.45)
        for f in (.45,.6,.72):
            d.line([(x+w*.1,y+h*f),(x+w*.9,y+h*f)],.12,[1,.6])
    @staticmethod
    def deaer(d,e):    # deaerator: menara kecil di atas tangki horizontal
        x,y,w,h=e.x,e.y,e.w,e.h
        tw=w*.3; tx=x+w*.35
        d.rect(tx,y,tw,h*.42,.4,Sym.WF)
        r=h*.29
        d.poly(d.arcpts(x+r,y+h-r,r,r,90,270)+d.arcpts(x+w-r,y+h-r,r,r,-90,90),.45,Sym.WF)
        for i in range(3): d.line([(tx,y+h*(.1+.1*i)),(tx+tw*.7,y+h*(.1+.1*i))] if i%2==0 else [(tx+tw*.3,y+h*(.1+.1*i)),(tx+tw,y+h*(.1+.1*i))],.15)
    @staticmethod
    def box(d,e):
        x,y,w,h=e.x,e.y,e.w,e.h; d.rect(x,y,w,h,.4,Sym.WF)
    @staticmethod
    def wtp(d,e):      # unit pengolahan air (paket): kotak + klarifier mini + kolom demin
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.4,Sym.WF)
        d.poly([(x+w*.08,y+h*.25),(x+w*.45,y+h*.25),(x+w*.45,y+h*.55),(x+w*.27,y+h*.8),(x+w*.08,y+h*.55)],.25,None)
        for i in range(2): d.rect(x+w*(.58+.2*i),y+h*.18,w*.12,h*.64,.25,None)
    @staticmethod
    def prv(d,e):      # stasiun reduksi tekanan: badan katup + desuperheater
        x,y,w,h=e.x,e.y,e.w,e.h; cy=y+h/2; m=x+w*.38
        d.poly([(x,cy-h*.45),(m,cy),(x,cy+h*.45)],.35,Sym.WF); d.poly([(m+(m-x),cy-h*.45),(m,cy),(m+(m-x),cy+h*.45)],.35,Sym.WF)
        d.line([(m,cy),(m,cy-h*.75)],.25); d.arc(m,cy-h*.75,h*.35,h*.35,0,180,.25); d.line([(m-h*.35,cy-h*.75),(m+h*.35,cy-h*.75)],.25)
        d.rect(x+w*.82,y,w*.18,h,.3,Sym.WF)
    @staticmethod
    def n2pk(d,e):     # paket nitrogen (PSA dua bejana)
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.35,'#ffffff',dash=[1.2,.6])
        for i in range(2):
            bx=x+w*(.18+.38*i); Sym.vessel(d,Eq(d,'vessel','_',bx,y+h*.12,w*.26,h*.76))
    @staticmethod
    def kcomp(d,e):    # kompresor udara paket: trapesium + tangki penerima
        x,y,w,h=e.x,e.y,e.w,e.h
        d.poly([(x,y),(x+w*.45,y+h*.25),(x+w*.45,y+h*.75),(x,y+h)],.4,Sym.WF)
        Sym.vessel(d,Eq(d,'vessel','_',x+w*.62,y-h*.1,w*.38,h*1.2))
        d.line([(x+w*.45,y+h*.5),(x+w*.62,y+h*.5)],.3)
    @staticmethod
    def manifold(d,e): # header penggabung (pipa besar)
        x,y,w,h=e.x,e.y,e.w,e.h
        d.rect(x,y,w,h,.45,Sym.WF); d.line([(x+w*.5,y+1),(x+w*.5,y+h-1)],.12,[1,.8])
    @staticmethod
    def diverter(d,e): # diverter / chute pembagi
        x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.poly([(x,y),(x+w,y),(x+w,y+h*.5),(cx,y+h),(x,y+h*.5)],.4,Sym.WF)
        d.line([(cx,y+h*.2),(cx+w*.28,y+h*.62)],.3); d.circ(cx,y+h*.2,.35,.2,'#000000')
    @staticmethod
    def granul(d,e):   # granulator drum
        Sym.drum(d,e)
    @staticmethod
    def splitter(d,e): Sym.tank(d,e)
    @staticmethod
    def storage(d,e):  # fasilitas penyimpanan residu bertanggul (penampang)
        x,y,w,h=e.x,e.y,e.w,e.h
        d.line([(x-2,y),(x,y)],.35); d.line([(x+w,y),(x+w+2,y)],.35)
        d.poly([(x,y),(x+w,y),(x+w*.9,y+h),(x+w*.1,y+h)],.45,Sym.WF)
        d.line([(x+w*.04,y+h*.4),(x+w*.96,y+h*.4)],.15,[1.2,.6])
        for i in range(9):
            xx=x+w*(.14+.08*i); d.line([(xx,y+h*.65),(xx+1.2,y+h*.65)],.15)
    @staticmethod
    def quench(d,e):   # menara quench: bejana dengan nosel semprot
        Sym.vessel(d,e); x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
        d.line([(x+w*.15,y+h*.3),(x+w*.85,y+h*.3)],.2)
        for i in range(3):
            xx=x+w*(.28+.22*i); d.line([(xx,y+h*.3),(xx-.8,y+h*.42)],.12); d.line([(xx,y+h*.3),(xx+.8,y+h*.42)],.12)
    @staticmethod
    def valve(d,x,y,vert=False,layer='equip',s=1.3):
        if vert: d.poly([(x-s/2,y-s/2),(x+s/2,y-s/2),(x-s/2,y+s/2),(x+s/2,y+s/2)],.25,'#ffffff',K,layer)
        else: d.poly([(x-s/2,y-s/2),(x+s/2,y+s/2),(x+s/2,y-s/2),(x-s/2,y+s/2)],.25,'#ffffff',K,layer)


# =====================================================================================================
#  EKSTENSI (EIC 2026): simbol modul biogas, gelembung instrumen, katup kendali, keluaran DXF
# =====================================================================================================
def _sym_digester(d,e):
    """digester CSTR: dinding silinder berinsulasi + atap membran ganda (kubah) + mixer samping + koil pemanas"""
    x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2; dh=min(w*.24,h*.3)
    d.poly(d.arcpts(cx,y+dh,w/2,dh,180,0)+[(x+w,y+h),(x,y+h)],.45,Sym.WF)            # badan + kubah luar
    d.line(d.arcpts(cx,y+dh+.2,w/2-1.0,dh-1.1,180,0),.2,[1.0,.6])                      # membran dalam
    d.line([(x+.5,y+dh+.2),(x+w-.5,y+dh+.2)],.15,[.8,.5])                              # batas gas/cair
    d.line([(x+.4,y+dh+(h-dh)*.2),(x+w-.4,y+dh+(h-dh)*.2)],.12)                        # muka cairan
    for f in (.36,.60):                                                                # mixer samping
        yy=y+dh+(h-dh)*f
        d.rect(x-3.4,yy-1.1,2.4,2.2,.3,Sym.WF); d.line([(x-1.0,yy),(x+w*.30,yy)],.3)
        d.line([(x+w*.30,yy-1.5),(x+w*.30,yy+1.5)],.55)
    zz=[(x+w*.15+i*(w*.7)/10,y+h-3.2-(1.6 if i%2 else 0)) for i in range(11)]          # koil pemanas
    d.line(zz,.22)
    d.line([(x-2.2,y+h),(x+w+2.2,y+h)],.7)                                             # pondasi
def _sym_chp(d,e):
    """kontainer CHP: mesin gas + generator dalam kontainer"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x,y,w,h,.45,Sym.WF); d.rect(x+.9,y+.9,w-1.8,h-1.8,.15,None,dash=[1.2,.7])
    r=h*.30; ex=x+w*.30; gx=x+w*.68; cy=y+h*.55
    d.circ(ex,cy,r,.35,Sym.WF)
    for a in range(0,360,60): d.line([(ex,cy),(ex+r*.75*math.cos(math.radians(a)),cy-r*.75*math.sin(math.radians(a)))],.18)
    d.line([(ex+r,cy),(gx-r,cy)],.45)
    d.circ(gx,cy,r,.35,Sym.WF); d.text(gx,cy+CAPC*2.4,'G',2.4,'m',True,owner=e.tag)
    d.line([(ex,cy-r),(ex,y-2.2)],.35); d.line([(ex-1.3,y-2.2),(ex+1.3,y-2.2)],.35)     # knalpot
def _sym_shredder(d,e):
    """hammer mill: rumah + rotor berpalu + corong umpan + motor di atas"""
    x,y,w,h=e.x,e.y,e.w,e.h; cx,cy=x+w*.46,y+h*.58; r=h*.30
    d.rect(x,y+h*.18,w,h*.82,.4,Sym.WF)
    d.poly([(cx-w*.20,y),(cx+w*.20,y),(cx+w*.10,y+h*.18),(cx-w*.10,y+h*.18)],.35,Sym.WF)
    d.circ(cx,cy,r,.3,None)
    for a in range(0,360,45): d.line([(cx,cy),(cx+r*.95*math.cos(math.radians(a)),cy-r*.95*math.sin(math.radians(a)))],.2)
    d.rect(x+w*.74,y-1.8,w*.22,1.8,.3,Sym.WF); d.line([(x+w*.85,y),(x+w*.85,y+h*.34),(cx+r*.6,cy-r*.6)],.2)
    d.line([(x+w*.1,y+h*.9),(x+w*.9,y+h*.9)],.15,[.8,.5])
def _sym_screen(d,e):
    """saringan drum putar (fine screen)"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x,y+h*.2,w,h*.8,.4,Sym.WF)
    n=int(w/1.6)
    for i in range(1,n): d.line([(x+w*i/n,y+h*.2),(x+w*i/n+h*.3,y+h)],.12)
    d.poly([(x+w*.12,y),(x+w*.42,y),(x+w*.34,y+h*.2),(x+w*.20,y+h*.2)],.3,Sym.WF)
    d.line([(x+w*.7,y+h),(x+w*.7,y+h+1.4)],.25)
def _sym_phx(d,e):
    """penukar panas pelat"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x,y,1.4,h,.3,Sym.WF); d.rect(x+w-1.4,y,1.4,h,.3,Sym.WF)
    n=max(5,int((w-3)/1.1))
    for i in range(n): d.line([(x+1.4+(w-2.8)*(i+.5)/n,y+.5),(x+1.4+(w-2.8)*(i+.5)/n,y+h-.5)],.22)
    d.line([(x+.7,y-.5),(x+w-.7,y-.5)],.2); d.line([(x+.7,y+h+.5),(x+w-.7,y+h+.5)],.2)
def _sym_spress(d,e):
    """screw press: badan miring berulir + saringan + motor"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.poly([(x,y+h*.2),(x+w*.86,y),(x+w*.86,y+h*.72),(x,y+h*.92)],.4,Sym.WF)
    for i in range(1,9):
        xx=x+w*.86*i/9; d.line([(xx,y+h*.2-(h*.2)*i/9+.3),(xx+w*.04,y+h*.92-(h*.2)*i/9-.3)],.2)
    d.rect(x+w*.86,y+h*.12,w*.14,h*.5,.35,Sym.WF)
    d.poly([(x+w*.1,y-2.4),(x+w*.36,y-2.4),(x+w*.30,y+h*.19),(x+w*.16,y+h*.21)],.3,Sym.WF)
    d.poly([(x+w*.55,y+h*.74),(x+w*.7,y+h*.74),(x+w*.66,y+h+1.8),(x+w*.59,y+h+1.8)],.25,Sym.WF)
def _sym_flare(d,e):
    """flare tertutup"""
    x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
    d.rect(x,y+h*.12,w,h*.88,.4,Sym.WF); d.line([(x,y+h*.4),(x+w,y+h*.4)],.15)
    d.poly([(cx-w*.3,y+h*.12),(cx-w*.1,y-1.8),(cx,y+h*.02),(cx+w*.12,y-3.0),(cx+w*.3,y+h*.12)],.25,Sym.WF)
def _sym_gasfilter(d,e):
    """bejana adsorpsi karbon aktif"""
    Sym.vessel(d,e); x,y,w,h=e.x,e.y,e.w,e.h
    d.line([(x,y+h*.28),(x+w,y+h*.28)],.2,[1,.6]); d.line([(x,y+h*.78),(x+w,y+h*.78)],.2,[1,.6])
    for i in range(6):
        d.circ(x+w*(.2+.12*i),y+h*.52,.35,.12,None)
def _sym_dtank(d,e):
    """tangki dosis kecil + agitator"""
    Sym.ctank(d,e)
Sym.digester=staticmethod(_sym_digester); Sym.chp=staticmethod(_sym_chp); Sym.shredder=staticmethod(_sym_shredder)
Sym.screen=staticmethod(_sym_screen); Sym.phx=staticmethod(_sym_phx); Sym.spress=staticmethod(_sym_spress)
Sym.flare=staticmethod(_sym_flare); Sym.gasfilter=staticmethod(_sym_gasfilter); Sym.dtank=staticmethod(_sym_dtank)

def _inst(s,x,y,fn,loop,r=2.55,layer='inst'):
    """gelembung instrumen (ISA-5.1): huruf fungsi di atas, nomor loop di bawah. Mengembalikan titik sambungan sinyal."""
    s.circ(x,y,r,.28,'#ffffff',layer)
    s.text(x,y-.25,fn,1.5,'m',True,layer=layer,owner=('inst',fn+str(loop)))
    s.text(x,y+1.55,str(loop),1.5,'m',False,layer=layer,owner=('inst',fn+str(loop)))
    return dict(pt=(x,y,None),x=x,y=y,r=r)
def _cvalve(s,x,y,vert=False,sz=1.5):
    """katup kendali dengan aktuator diafragma (gambar di atas jalur)"""
    Sym.valve(s,x,y,vert,'equip',sz*1.0)
    if not vert:
        s.line([(x,y-sz*.5),(x,y-sz*1.5)],.22,None,K,'equip')
        s.poly(s.arcpts(x,y-sz*1.5,sz*.8,sz*.8,0,180),.22,'#ffffff',K,'equip')
        return (x,y-sz*2.3,'U')
    s.line([(x+sz*.5,y),(x+sz*1.5,y)],.22,None,K,'equip')
    s.poly(s.arcpts(x+sz*1.5,y,sz*.8,sz*.8,-90,90),.22,'#ffffff',K,'equip')
    return (x+sz*2.3,y,'R')
Doc.inst=_inst; Doc.cvalve=_cvalve

_DXF_LAYERS={'frame':'PFD-BINGKAI','table':'PFD-TABEL','util':'PFD-UTILITAS','proc':'PFD-PROSES','sig':'PFD-SINYAL','equip':'PFD-PERALATAN','inst':'PFD-INSTRUMEN','label':'PFD-TEKS'}
_SUBS=str.maketrans('0123456789','\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089')
def _dxf(s,path,title=None):
    """tulis DXF R2010 (satuan mm, sumbu Y ke atas) satu lapisan per kelompok gambar. Isian putih/abu dibuang (CAD tanpa isian agar terbaca di latar gelap maupun terang); isian hitam -> HATCH ACI 7."""
    import ezdxf
    from ezdxf.enums import TextEntityAlignment as TA
    doc=ezdxf.new('R2010',setup=True); doc.units=4
    msp=doc.modelspace()
    for L in LAYERS: doc.layers.add(_DXF_LAYERS[L],color=8 if L=='util' else 7)
    doc.styles.add('PFD',font='arial.ttf')
    valid=[0,5,9,13,15,18,20,25,30,35,40,50,53,60,70,80,90,100,106,120,140,158,200,211]
    lw=lambda w:min(valid,key=lambda v:abs(v-w*100))
    def rgb(cl): h=cl.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
    Y=lambda y:H-y
    for L in LAYERS:
        ly=_DXF_LAYERS[L]
        for it in s.items[L]:
            t=it[0]
            if t=='line':
                _,pts,w,dash,cl,cap=it
                at=dict(layer=ly,lineweight=lw(w),linetype='DASHED' if dash else 'Continuous',ltscale=0.35)
                if cl!='#000000': at['true_color']=ezdxf.colors.rgb2int(rgb(cl))
                msp.add_lwpolyline([(x,Y(y)) for x,y in pts],dxfattribs=at)
            elif t=='poly':
                _,pts,w,fill,cl,dash=it
                P=[(x,Y(y)) for x,y in pts]
                if fill and fill.lower()=='#000000':                                    # hanya isian hitam (kepala panah): warna ACI 7 (adaptif terang/gelap)
                    hh=msp.add_hatch(color=7,dxfattribs=dict(layer=ly)); hh.paths.add_polyline_path(P,is_closed=True)
                if w>0 or (fill and fill.lower()=='#000000' and w==0):
                    at=dict(layer=ly,lineweight=lw(w),linetype='DASHED' if dash else 'Continuous',ltscale=0.35)
                    if cl!='#000000': at['true_color']=ezdxf.colors.rgb2int(rgb(cl))
                    msp.add_lwpolyline(P,close=True,dxfattribs=at)
            elif t=='circ':
                _,cx,cy,r,w,fill,cl=it
                if fill and fill.lower()=='#000000':
                    hh=msp.add_hatch(color=7,dxfattribs=dict(layer=ly))
                    ep=hh.paths.add_edge_path(); ep.add_arc((cx,Y(cy)),r,0,360)
                if w>0: msp.add_circle((cx,Y(cy)),r,dxfattribs=dict(layer=ly,lineweight=lw(w)))
            elif t=='text':
                _,x,y,tx,size,anchor,bold,rot,cl,ital=it
                txt=''.join(r_.translate(_SUBS) if sb else r_ for r_,sb,_i in runs(tx))
                e=msp.add_text(txt,height=size*.72,dxfattribs=dict(layer=ly,style='PFD',rotation=rot))
                e.set_placement((x,Y(y)),align={'l':TA.LEFT,'m':TA.CENTER,'r':TA.RIGHT}[anchor])
                if cl!='#000000': e.dxf.true_color=ezdxf.colors.rgb2int(rgb(cl))
    doc.saveas(path)
Doc.dxf=_dxf

# =====================================================================================================
#  EKSTENSI Rev 1: simbol ISO 10628 tambahan, tag aliran (No/T/P), gelembung ISA-5.1 dengan garis
# =====================================================================================================
def _sym_reactor(d,e):
    """reaktor tegak berinsulasi (kepala elipsoidal) dengan cincin nosel jet dan muka cairan"""
    x,y,w,h=e.x,e.y,e.w,e.h; r=min(w/2,h*.12)
    Sym.vessel(d,e)
    d.line([(x-.9,y+h-r)]+d.arcpts(x+w/2,y+r,w/2+.9,r+.9,180,0)[::-1][::-1]+[(x+w+.9,y+h-r)],.15,[.9,.6])   # insulasi
    d.line(d.arcpts(x+w/2,y+h-r,w/2+.9,r+.9,180,360),.15,[.9,.6])
    d.line([(x+.5,y+h*.20),(x+w-.5,y+h*.20)],.15,[.8,.5])                                # muka cairan
    yy=y+h*.86
    d.line([(x+w*.12,yy),(x+w*.88,yy)],.25)
    for f in (.22,.5,.78):
        cx=x+w*f; d.poly([(cx-.7,yy),(cx+.7,yy),(cx,yy-1.4)],.15,'#ffffff')
def _sym_membrane(d,e):
    """unit membran (ISO 10628): persegi panjang dibagi diagonal"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x,y,w,h,.45,Sym.WF); d.line([(x,y+h),(x+w,y)],.3)
    for i in range(1,4): d.line([(x+w*i/4,y+h*.08),(x+w*i/4,y+h*.92)],.12,[.6,.6])
def _sym_gasholder(d,e):
    """penampung gas membran ganda: alas + kubah luar + membran dalam putus-putus"""
    x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2; hb=h*.28
    d.poly(d.arcpts(cx,y+h-hb,w/2,h-hb,180,0)+[(x+w,y+h),(x,y+h)],.45,Sym.WF)
    d.line(d.arcpts(cx,y+h-hb,w/2-1.2,h-hb-1.6,180,0),.2,[1.0,.6])
    d.line([(x,y+h-hb),(x+w,y+h-hb)],.25)
    d.line([(x-1.8,y+h),(x+w+1.8,y+h)],.7)
def _sym_genset(d,e):
    """genset gas dalam kontainer: mesin (M) + generator (G)"""
    x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x,y,w,h,.45,Sym.WF); d.rect(x+.8,y+.8,w-1.6,h-1.6,.15,None,dash=[1.2,.7])
    r=h*.30; cy=y+h*.5; ex=x+w*.32; gx=x+w*.70
    d.rect(ex-r*1.15,cy-r,r*2.3,r*2,.35,Sym.WF); d.text(ex,cy+CAPC*2.2,'M',2.2,'m',True,owner=e.tag)
    d.line([(ex+r*1.15,cy),(gx-r,cy)],.45)
    d.circ(gx,cy,r,.35,Sym.WF); d.text(gx,cy+CAPC*2.2,'G',2.2,'m',True,owner=e.tag)
def _sym_kopot(d,e):
    """pot pemisah kondensat (KO pot) dengan demister"""
    Sym.vessel(d,e); x,y,w,h=e.x,e.y,e.w,e.h
    d.rect(x+w*.12,y+h*.20,w*.76,h*.08,.15,None)
    for i in range(4): d.line([(x+w*(.18+.2*i),y+h*.2),(x+w*(.28+.2*i),y+h*.28)],.1)
Sym.reactor=staticmethod(_sym_reactor); Sym.membrane=staticmethod(_sym_membrane); Sym.gasholder=staticmethod(_sym_gasholder)
Sym.genset=staticmethod(_sym_genset); Sym.kopot=staticmethod(_sym_kopot)

def _stag(s,x,y,num,T,P,side='t',lead=2.4,w=7.6):
    """tag aliran gaya EPC: kotak tiga baris (No, T degC, P bar) di atas/bawah garis, dengan garis penunjuk."""
    hr=2.7; h=3*hr
    if side in 'lr':                                   # garis vertikal: kotak di kiri/kanan, penunjuk horizontal
        xc=x-lead-w/2 if side=='l' else x+lead+w/2
        s.line([(x,y),(xc+(w/2 if side=='l' else -w/2),y)],.18,None,K,'label')
        x=xc; y0=y-h/2; y1=y0+h
    elif side=='t': y1=y-lead; y0=y1-h
    else: y0=y+lead; y1=y0+h
    if side in 'tb': s.line([(x,y),(x,y1 if side=='t' else y0)],.18,None,K,'label')
    s.rect(x-w/2,y0,w,h,.3,'#ffffff','label')
    s.line([(x-w/2,y0+hr),(x+w/2,y0+hr)],.18,None,K,'label'); s.line([(x-w/2,y0+2*hr),(x+w/2,y0+2*hr)],.18,None,K,'label')
    s.text(x,y0+hr*.5+CAPC*1.65,str(num),1.65,'m',True,chk=False,layer='label')
    s.text(x,y0+hr*1.5+CAPC*1.35,T,1.35,'m',False,chk=False,layer='label')
    s.text(x,y0+hr*2.5+CAPC*1.35,P,1.35,'m',False,chk=False,layer='label')
    bb=(x-w/2-.2,y0-.2,x+w/2+.2,y1+.2)
    s.texts.append(dict(bb=bb,t='STAG%s'%num,owner=('stag',num),layer='label',skip=()))
    return bb
def _inst2(s,x,y,fn,loop,r=2.9,layer='inst'):
    """gelembung ISA-5.1 (instrumen pada panel/DCS yang dapat diakses operator): lingkaran dengan garis horizontal"""
    s.circ(x,y,r,.28,'#ffffff',layer)
    s.line([(x-r,y),(x+r,y)],.2,None,K,layer)
    s.text(x,y-r*.2,fn,INST_FS,'m',True,layer=layer,chk=False)
    s.text(x,y+r*.2+INST_FS*.74,str(loop),INST_FS,'m',False,layer=layer,chk=False)
    q=r*.62; s.texts.append(dict(bb=(x-q,y-q,x+q,y+q),t='%s-%s'%(fn,loop),owner=('inst',fn,loop),layer=layer))
    return dict(x=x,y=y,r=r)
Doc.stag=_stag; Doc.inst2=_inst2

def _sym_ccomp(d,e):
    """kompresor/blower sentrifugal ISO 10628-2: lingkaran + dua garis menyempit ke arah buang (kanan)"""
    r=min(e.w,e.h)/2; cx,cy=e.x+e.w/2,e.y+e.h/2
    d.circ(cx,cy,r,.4,Sym.WF)
    a=math.radians(122); b=math.radians(32)
    d.line([(cx+r*math.cos(a),cy-r*math.sin(a)),(cx+r*math.cos(b),cy-r*math.sin(b))],.3)
    d.line([(cx+r*math.cos(a),cy+r*math.sin(a)),(cx+r*math.cos(b),cy+r*math.sin(b))],.3)
def _sym_tankf(d,e):
    """tangki atap kerucut (API 650 kecil) tanpa agitator"""
    x,y,w,h=e.x,e.y,e.w,e.h; rf=min(h*.12,w*.18)
    d.poly([(x,y+rf),(x+w/2,y),(x+w,y+rf),(x+w,y+h),(x,y+h)],.4,Sym.WF)
    d.line([(x+.4,y+rf+(h-rf)*.18),(x+w-.4,y+rf+(h-rf)*.18)],.12,[.8,.5])
def _sym_hcyc(d,e):
    """hidrosiklon: silinder pendek + kerucut panjang"""
    x,y,w,h=e.x,e.y,e.w,e.h; cx=x+w/2
    d.poly([(x,y),(x+w,y),(x+w,y+h*.28),(cx+w*.12,y+h),(cx-w*.12,y+h),(x,y+h*.28)],.4,Sym.WF)
    d.line([(cx-w*.18,y-1.2),(cx-w*.18,y+h*.34)],.25); d.line([(cx+w*.18,y-1.2),(cx+w*.18,y+h*.34)],.25)
Sym.ccomp=staticmethod(_sym_ccomp); Sym.tankf=staticmethod(_sym_tankf); Sym.hcyc=staticmethod(_sym_hcyc)
def _surf_ccomp(e,side,f):
    r=min(e.w,e.h)/2; cx,cy=e.x+e.w/2,e.y+e.h/2
    if side=='l': return (cx-r,cy,'L')
    if side=='r': return (cx+r,cy,'R')
    if side in 'tb':
        xx=e.x+f*e.w; u=min(1,abs(xx-cx)/r); dy=r*math.sqrt(max(0,1-u*u))
        return (xx,cy-dy,'U') if side=='t' else (xx,cy+dy,'D')
Surf.ccomp=staticmethod(_surf_ccomp)
def _surf_tankf(e,side,f):
    if side=='t':
        rf=min(e.h*.12,e.w*.18); xx=e.x+f*e.w; return (xx,e.y+rf*abs(xx-(e.x+e.w/2))/(e.w/2),'U')
Surf.tankf=staticmethod(_surf_tankf)
Surf.reactor=staticmethod(lambda e,side,f: Surf._head(e,side,f,min(e.w/2,e.h*.12)) if side in 'tb' else None)
