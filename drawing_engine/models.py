# -*- coding: utf-8 -*-
"""Model 3D komponen kiln R-01 (mm). Sumbu kiln = X (umpan -> pelepasan), Z ke atas, Y lateral."""
import math, json, os as _os, cadquery as cq
R=json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'kiln_results.json')))
# ---------------- parameter utama (mm)
DI=6300.0; DSI=6700.0; TSH=38.0; TTY=90.0; TFB=70.0
LK=63000.0; XT=[10500.0,33000.0,54000.0]; XG=29500.0
TY_BORE=round(R['tyre_bore']*1000); TY_OD=round(R['tyre_OD']*1000/10)*10; TY_W=1000.0   # 7032, 8650
DR=2900.0; BR=1150.0; ANG=30.0
RC=TY_OD/2+DR/2; RY=RC*math.cos(math.radians(ANG)); RX=RC*math.sin(math.radians(ANG))
TYPAD_L=3000.0; TAPER=4.0
# rol dan poros
D_SEAT=700.0; D_COL=780.0; D_JRN=600.0; L_JRN=420.0; L_COL=120.0; L_TR=80.0
BRG_D=980.0; BRG_B=300.0
SPAN_B=BR+2*(L_COL+L_TR+L_JRN/2)        # jarak pusat bantalan
L_SHAFT=BR+2*(L_COL+L_TR+L_JRN)+2*180    # termasuk ujung untuk mur/tutup
HUB_OD=1350.0; RIM_ID=2300.0; WEB_T=320.0
# rumah bantalan
HB_H=900.0      # tinggi pusat poros di atas alas rumah bantalan
HB_W=1700.0     # lebar alas (tegak lurus poros)
HB_L=560.0      # panjang alas (sejajar poros)
# rangka dasar
BF_H=500.0; BF_W=4100.0; BF_AX=3200.0; BF_LAT=2*RX+BF_W
# gigi gelang
MG=36.0; Z2=252; Z1=15; BG=850.0; BP=900.0
D2=MG*Z2; DA2=D2+2*MG; DF2=D2-2.5*MG
D1=MG*Z1; DA1=D1+2*MG; DF1=D1-2.5*MG
A_C=(D1+D2)/2

def revolve_x(profile,angle=360):
    """profil (x,r) di bidang XZ diputar terhadap sumbu X"""
    wp=cq.Workplane('XZ').polyline(profile).close()
    return wp.revolve(angle,(0,0,0),(1,0,0))

def roller():
    r=DR/2; h=BR/2; c=25
    prof=[(-h,HUB_OD/2),(-h,RIM_ID/2),(-WEB_T/2,RIM_ID/2-150),(-WEB_T/2,RIM_ID/2),(-h,RIM_ID/2),(-h,r-c),(-h+c,r),(h-c,r),(h,r-c),(h,RIM_ID/2),(WEB_T/2,RIM_ID/2),(WEB_T/2,RIM_ID/2-150),(h,RIM_ID/2),(h,HUB_OD/2)]
    # profil sederhana: pelek + badan + hub (penampang setengah)
    prof=[(-h,D_SEAT/2),(-h,HUB_OD/2),(-WEB_T/2,HUB_OD/2+120),(-WEB_T/2,RIM_ID/2-120),(-h,RIM_ID/2),(-h,r-c),(-h+c,r),(h-c,r),(h,r-c),(h,RIM_ID/2),(WEB_T/2,RIM_ID/2-120),(WEB_T/2,HUB_OD/2+120),(h,HUB_OD/2),(h,D_SEAT/2)]
    return revolve_x(prof)

def shaft():
    h=BR/2
    xs=[]; 
    x1=h; x2=x1+L_COL; x3=x2+L_TR; x4=x3+L_JRN; x5=x4+180
    prof=[(-x5,0),(-x5,D_JRN/2-60),(-x4,D_JRN/2-60),(-x4,D_JRN/2),(-x3,D_JRN/2),(-x3+20,D_JRN/2+20),(-x2,D_COL/2-30),(-x2,D_COL/2),(-x1,D_COL/2),(-x1,D_SEAT/2),
          (x1,D_SEAT/2),(x1,D_COL/2),(x2,D_COL/2),(x2,D_COL/2-30),(x3-20,D_JRN/2+20),(x3,D_JRN/2),(x4,D_JRN/2),(x4,D_JRN/2-60),(x5,D_JRN/2-60),(x5,0)]
    return revolve_x(prof)

def housing():
    """rumah bantalan terbelah (plummer block) berpusat pada sumbu poros (sumbu X lokal)"""
    base=cq.Workplane('XY').box(HB_L,HB_W,90).translate((0,0,-HB_H+45))
    body=cq.Workplane('YZ').circle(BRG_D/2+110).extrude(BRG_B+160).translate((-(BRG_B+160)/2,0,0))
    ped=cq.Workplane('XY').box(BRG_B+160,BRG_D+220,HB_H-90).translate((0,0,-(HB_H-90)/2-0))
    ped=ped.translate((0,0,-45+0))
    lug=cq.Workplane('XY').box(BRG_B+160,BRG_D+620,110).translate((0,0,-20))
    h=base.union(ped).union(body).union(lug)
    h=h.cut(cq.Workplane('YZ').circle(D_JRN/2+15).extrude(2000).translate((-1000,0,0)))
    # baut alas
    for sx in (-1,1):
        for sy in (-1,1):
            h=h.union(cq.Workplane('XY').circle(40).extrude(160).translate((sx*(HB_L/2-110),sy*(HB_W/2-130),-HB_H+90)))
    # baut tutup
    for sy in (-1,1):
        h=h.union(cq.Workplane('XY').circle(36).extrude(200).translate((0,sy*(BRG_D/2+200),-20+55)))
    return h

def roller_unit():
    """rol + poros + 2 rumah bantalan, pusat rol di (0,0,0), poros sejajar X"""
    u=roller().union(shaft())
    for sx in (-1,1):
        u=u.union(housing().translate((sx*SPAN_B/2,0,0)))
    return u

def base_frame_one():
    """rangka dasar satu rol: balok di bawah rumah bantalan + balok samping, berlubang di bawah rol; pusat rol di (0,0,0)"""
    H=BF_H; z0=-HB_H-H
    fr=None
    for sx in (-1,1):
        b=cq.Workplane('XY').box(600,BF_W,H).translate((sx*SPAN_B/2,0,z0+H/2))
        fr=b if fr is None else fr.union(b)
    for sy in (-1,1):
        b=cq.Workplane('XY').box(BF_AX,400,H).translate((0,sy*(BF_W/2-200),z0+H/2))
        fr=fr.union(b)
    # blok penyetel di kedua sisi tiap rumah bantalan
    for sx in (-1,1):
        for sy in (-1,1):
            fr=fr.union(cq.Workplane('XY').box(300,200,280).translate((sx*SPAN_B/2,sy*(HB_W/2+130),z0+H+140)))
    return fr

def base_frame():
    return base_frame_one().translate((0,RX,-RY)).union(base_frame_one().translate((0,-RX,-RY)))

def tyre():
    a=TY_BORE/2; b=TY_OD/2; h=TY_W/2; c=20; ci=8
    prof=[(-h,a+ci),(-h+ci,a),(h-ci,a),(h,a+ci),(h,b-c),(h-c,b),(-h+c,b),(-h,b-c)]
    return revolve_x(prof)

def shell_segment(x0,x1,xt=None):
    """cangkang (OD bertingkat di zona ban) antara x0..x1 pada koordinat lokal, ID 6700"""
    ri=DSI/2; ro=ri+TSH; rt=ri+TTY; tl=(TTY-TSH)*TAPER
    pts=[(x0,ri)]
    if xt is not None:
        a=xt-TYPAD_L/2; b=xt+TYPAD_L/2
        pts+=[(x0,ro),(a-tl,ro),(a,rt),(b,rt),(b+tl,ro),(x1,ro),(x1,ri)]
    else: pts+=[(x0,ro),(x1,ro),(x1,ri)]
    return revolve_x(pts)

def filler_bars(xc=0.0,n=64,w=220.0,L=1400.0):
    r0=DSI/2+TTY; bars=None
    for i in range(n):
        a=360.0*i/n
        b=cq.Workplane('XY').box(L,w,TFB).translate((xc,0,r0+TFB/2)).rotate((0,0,0),(1,0,0),a)
        bars=b if bars is None else bars.union(b)
    return bars

def stop_blocks(xc=0.0,n=16,gap=10.0):
    r0=DSI/2+TTY+TFB; out=None
    for side in (-1,1):
        for i in range(n):
            a=360.0*i/n
            b=cq.Workplane('XY').box(160,200,180).translate((xc+side*(TY_W/2+gap+80),0,r0+90)).rotate((0,0,0),(1,0,0),a)
            out=b if out is None else out.union(b)
    return out

def thrust_unit(side):
    """rol dorong hidrolik pada muka samping ban bagian bawah (side=-1 hulu, +1 hilir); sumbu rol vertikal"""
    xr=side*(TY_W/2+380)
    z0=-RY-HB_H          # puncak rangka dasar
    roll=cq.Workplane('XY').circle(380).extrude(260).translate((xr,0,-4100))
    roll=roll.edges().chamfer(15)
    shaft_=cq.Workplane('XY').circle(120).extrude(300).translate((xr,0,-4400))
    z0=z0-BF_H
    body=cq.Workplane('XY').box(820,900,z0*-1-4400).translate((xr,0,(-4400+z0)/2))
    cyl=cq.Workplane('YZ').circle(170).extrude(700).translate((xr+side*410 if side>0 else xr-410-700,0,(-4400+z0)/2+250))
    return roll.union(shaft_).union(body).union(cyl)

def pier(h=1500.0):
    z0=-RY-HB_H-BF_H
    p=cq.Workplane('XY').box(BF_AX+400,BF_LAT+400,h).translate((0,0,z0-h/2))
    for sy in (-1,1):
        p=p.cut(cq.Workplane('XY').box(BR+250,DR+200,400).translate((0,sy*RX,z0-200+1)))
    return p

def station(thrust=True,shell_half=2400.0):
    parts={}
    parts['shell']=shell_segment(-shell_half,shell_half,0.0)
    parts['tyre']=tyre()
    parts['fb']=filler_bars()
    parts['sb']=stop_blocks()
    ru=roller_unit()
    parts['rollers']=ru.translate((0,RX,-RY)).union(ru.translate((0,-RX,-RY)))
    parts['frame']=base_frame()
    if thrust: parts['thrust']=thrust_unit(-1).union(thrust_unit(1))
    parts['pier']=pier()
    return parts

def girth_gear_simple():
    """roda gigi gelang representasi konvensional: cincin Ø kepala, badan, flens dalam"""
    h=BG/2
    prof=[(-h,DF2/2-260),(-h,DA2/2),(h,DA2/2),(h,DF2/2-260),(70,DF2/2-260),(70,3900),(150,3900),(150,3780),(-150,3780),(-150,3900),(-70,3900),(-70,DF2/2-260)]
    return revolve_x(prof)


# ===================== rakitan keseluruhan (GA)
PHI=math.atan(0.035); EL0=9355.0
def kiln_local():
    """bagian berputar + stasiun + penggerak dalam koordinat lokal sumbu kiln (x sepanjang sumbu)"""
    ri=DSI/2; ro=ri+TSH; rt=ri+TTY; tl=(TTY-TSH)*TAPER
    pts=[(0,ri),(0,ro)]
    for xt in XT:
        a=xt-TYPAD_L/2; b=xt+TYPAD_L/2
        pts+=[(a-tl,ro),(a,rt),(b,rt),(b+tl,ro)]
    pts+=[(LK,ro),(LK,ri)]
    shell=revolve_x(pts)
    # cincin segel di kedua ujung
    seal=revolve_x([(400,ro),(400,ro+60),(900,ro+60),(900,ro)]).union(revolve_x([(LK-900,ro),(LK-900,ro+60),(LK-400,ro+60),(LK-400,ro)]))
    rot=[shell,seal]
    for xt in XT: rot.append(tyre().translate((xt,0,0)))
    rot.append(girth_gear_simple().translate((XG,0,0)))
    st=[]
    for k,xt in enumerate(XT):
        ru=roller_unit()
        st.append(ru.translate((xt,RX,-RY))); st.append(ru.translate((xt,-RX,-RY)))
        st.append(base_frame().translate((xt,0,0)))
        if k==1: st.append(thrust_unit(-1).translate((xt,0,0)).union(thrust_unit(1).translate((xt,0,0))))
        z0=-RY-HB_H-BF_H
        st.append(cq.Workplane('XY').box(BF_AX+400,BF_LAT+400,9000).translate((xt,0,z0-4500)))
    # penggerak ganda: pinion di kedua sisi pada 20 derajat di bawah horizontal
    dr=[]
    for sgn in (-1,1):
        ang=math.radians(-20)
        py=sgn*A_C*math.cos(ang); pz=A_C*math.sin(ang)
        x0=XG-BP/2
        pin=cq.Workplane('YZ').circle(DA1/2).extrude(BP).translate((x0,py,pz))
        sh_=cq.Workplane('YZ').circle(160).extrude(1700).translate((x0-1700,py,pz))
        brg=cq.Workplane('XY').box(500,900,900).translate((x0-500,py,pz-200))
        red=cq.Workplane('XY').box(2400,2000,1800).translate((x0-1700-1200,py,pz-150))
        cp=cq.Workplane('YZ').circle(320).extrude(500).translate((x0-1700-2400-500,py,pz))
        mot=cq.Workplane('YZ').circle(430).extrude(1900).translate((x0-1700-2400-500-1900,py,pz))
        mf=cq.Workplane('XY').box(1700,900,350).translate((x0-1700-2400-500-950,py,pz-430-175))
        plinth=cq.Workplane('XY').box(7400,2400,12000).translate((x0-3700,py,pz-1050-6000))
        dr+=[pin,sh_,brg,red,cp,mot,mf,plinth]
    return rot,st,dr
def place(wp):
    return wp.rotate((0,0,0),(0,1,0),math.degrees(PHI)).translate((0,0,EL0))
def hoods():
    xe=LK*math.cos(PHI); ze=EL0-LK*math.sin(PHI)
    fh=cq.Workplane('XY').box(4400,8400,9000).translate((-4200/2+150,0,EL0+300))
    fd=cq.Workplane('XY').circle(1200).extrude(4200).translate((-2100,0,EL0+300+4500))
    fc=cq.Workplane('XY').circle(500).extrude(5200).rotate((0,0,0),(0,1,0),-40).translate((-4300,0,EL0+500))
    legs=None
    for sx in (-3900,-400):
        for sy in (-3800,3800):
            l=cq.Workplane('XY').box(400,400,EL0+300-4500).translate((sx,sy,(EL0+300-4500)/2))
            legs=l if legs is None else legs.union(l)
    dh=cq.Workplane('XY').box(6800,8400,9200).translate((xe+3250-150,0,ze+200))
    dd=cq.Workplane('XY').circle(950).extrude(3800).translate((xe+1800,0,ze+200+4600))
    ds=cq.Workplane('XY').circle(250).extrude(2800).translate((xe+3900,-1800,ze+200+4600))
    bu=cq.Workplane('YZ').circle(450).extrude(3800).translate((xe+6650,0,ze))
    ch=cq.Workplane('XY').rect(1600,2400).workplane(offset=-(ze+200-4600)).rect(900,1200).loft().translate((xe+1700,0,ze+200-4600)).mirror('XY',(0,0,ze+200-4600)) if False else cq.Workplane('XY').box(1400,2000,ze+200-4600).translate((xe+1700,0,(ze+200-4600)/2))
    legs2=None
    for sx in (xe+500,xe+5900):
        for sy in (-3800,3800):
            l=cq.Workplane('XY').box(400,400,ze+200-4600).translate((sx,sy,(ze+200-4600)/2))
            legs2=l if legs2 is None else legs2.union(l)
    return [fh,fd,fc,legs,dh,dd,ds,bu,ch,legs2]
def ground_clip(wp):
    big=cq.Workplane('XY').box(300000,100000,60000).translate((30000,0,30000))
    return wp.intersect(big)

def pinion():
    """pinion z15 m36 (representasi konvensional: silinder kepala) dengan poros"""
    h=BP/2; ra=DA1/2
    prof=[(-h-100-300-0,0),(-h-100-300,180),(-h-100,180),(-h-100,200),(-h,200),(-h,ra-5),(-h+5,ra),(h-5,ra),(h,ra-5),(h,200),(h+100,200),(h+100,180),(h+100+300,180),(h+100+300,160),(h+100+300+500,160),(h+100+300+500,0)]
    p=revolve_x(prof)
    kw=cq.Workplane('XY').box(400,80,40).translate((h+100+300+250+20,0,160-20+1))
    return p.cut(kw)
