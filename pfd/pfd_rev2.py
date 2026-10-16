# -*- coding: utf-8 -*-
"""
PFD A2 Rev 3 - Set biogas kontak termofilik yang dapat dipindah (tangki GFS) untuk POME (EIC 2026).
Tata letak mengikuti acuan PEFD Rute B: area proses penuh-lebar dengan label area, header utilitas (PW, CWS, CWR)
dan air panas digambar, nomor aliran belah ketupat; pita bawah berisi legenda, daftar peralatan, kondisi aliran,
loop kendali, catatan, dan blok judul. Simbol detail: sym2.py (ISO 10628-2). Instrumen: ISA-5.1.
Membaca ../process/outputs/results.json + portable_modules.json.
Keluaran: outputs/PFD_BG-002_Rev2.pdf, .dxf, .svg.  Jalankan: python3 pfd_rev2.py
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eng
import sym2  # noqa: F401  (mendaftarkan simbol *2)
from eng import Doc, W, H

TEAM = "NAMA TIM"
UNIV = "UNIVERSITAS"
EVENT = "ASPEBINDO Energy Innovation Strategy Competition 2026"
DWG_NO = "PFD-BG-002"
REV = "3"
DWG_DATE = "15-10-2026"
eng.DOC_TITLE = "PFD Set Biogas Kontak Termofilik"
eng.DOC_AUTHOR = TEAM
# ketebalan garis (mm) dan kepala panah
eng.LW_PROC = .75; eng.LW_UTIL = .42; eng.LW_SIG = .25
eng.AH_PROC = (2.8, 1.7); eng.AH_UTIL = (2.2, 1.35)
eng.UG = '#000000'

R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(HERE, "..", "process", "outputs", "portable_modules.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
EQ = R["equipment"]; EN = R["energy"]; NOM = R["nominal"]; STR = {r["id"]: r for r in R["streams"]}
RV = EQ["reactor_vessel"]; NR = RV["count"]; LS = EQ["lamella_settler"]
RT = 'R-2%02d' % NR
d = Doc()

UD = {'CWS': [3.0, 1.0], 'CWR': [3.0, 1.0, .6, 1.0], 'PW': [1.2, .8], 'HW': [4.0, 1.0, .6, 1.0, .6, 1.0], 'EL': [.6, .8], 'CIP': [1.6, .8]}

def idn(x, dec=0):
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
P = lambda r: d.pt(r)[:2]
def L(key, pts, num=None, dseg=None, dpos=.5, arrow=True, mid=False):
    return d.conn(key, None, None, pts=pts, num=num, dseg=dseg, dpos=dpos, arrow=arrow, arrow_mid=mid)
def U(key, pts, kind, arrow=True):
    return d.conn(key, None, None, pts=pts, cls='util', dash=UD[kind], arrow=arrow)
def flag(text, x, y, dr='r', kind='in', util=False): return d.flag(text, x, y, dr, kind, util=util)
def J(x, y): d.junction(x, y)

# =====================================================================================================
# 1. BINGKAI (zona 1-12 / A-H)
# =====================================================================================================
YR = 340            # batas atas pita bawah
def frame():
    d.rect(4, 4, W - 8, H - 8, .35, None, 'frame'); d.rect(10, 10, W - 20, H - 20, .8, None, 'frame')
    for i in range(12):
        x0 = 10 + (W - 20) * i / 12; x1 = 10 + (W - 20) * (i + 1) / 12
        if i: d.line([(x0, 4), (x0, 10)], .25, None, '#000000', 'frame'); d.line([(x0, H - 10), (x0, H - 4)], .25, None, '#000000', 'frame')
        for yy in (8.2, H - 5.6): d.text((x0 + x1) / 2, yy, str(i + 1), 2.0, 'm', False, layer='frame', chk=False)
    for j in range(8):
        y0 = 10 + (H - 20) * j / 8; y1 = 10 + (H - 20) * (j + 1) / 8
        if j: d.line([(4, y0), (10, y0)], .25, None, '#000000', 'frame'); d.line([(W - 10, y0), (W - 4, y0)], .25, None, '#000000', 'frame')
        for xx in (7.2, W - 6.8): d.text(xx, (y0 + y1) / 2 + .7, "ABCDEFGH"[j], 2.0, 'm', False, layer='frame', chk=False)
    d.line([(10, YR), (W - 10, YR)], .8, None, '#000000', 'frame')

def area(x, y, title, sub):
    d.text(x, y, title, 2.0, 'l', True, layer='frame', chk=False)
    tw = eng.twidth(title, 2.0, True)
    d.line([(x, y + .8), (x + tw, y + .8)], .3, None, '#000000', 'frame')
    d.text(x, y + 3.6, sub, 1.45, 'l', False, layer='frame', chk=False)

# =====================================================================================================
# 2. PERALATAN
# =====================================================================================================
RY, RW, RH = 168, 24, 84         # reaktor & bejana standar
X_TK1, X_R1, X_R2, X_TK3 = 120, 176, 236, 350
YH = 262                          # header umpan reaktor
YG = 150                          # header biogas
Y_PW, Y_CWS, Y_CWR = 308, 313, 318
def equipment():
    E = d.eq
    # ---- A-100 praolah (PM-1) + PM-2
    E('rscreen2', 'SC-101', 30, 170, 28, 20, lab=(44, 166.5, 'm'), nz={'in': (0, .09, 'L'), 'out': (.6, 1, 'D'), 'scr': (.3, 1, 'D')})
    E('pump2', 'P-101', 60, 204, 8, 8, lab=(64, 219, 'm'))
    E('hcyc2', 'HC-101', 72, 160, 12, 30, lab=(88, 186, 'l'), nz={'in': (0, .08, 'L'), 'of': (.66, -.047, 'U'), 'uf': (.5, 1, 'D')})
    E('phe2', 'E-101', 88, 156, 22, 14, lab=(99, 176.5, 'm'), nz={'in': (0, .5, 'L'), 'out': (1.055, .5, 'R'), 'cs': (.3, 0, 'U'), 'cr': (.7, 0, 'U')})
    E('vtank2', 'TK-101', X_TK1, RY, RW, RH, lab=(X_TK1 + 12, 260.5, 'm'), hitbox=[(.04, .02, .96, 1.03)],
      nz={'in': (.25, 0, 'U'), 'out': (1, .9, 'R')})
    E('pump2', 'P-201', 150, 266, 8, 8, lab=(148.6, 275.5, 'r'))
    # ---- A-200 reaktor (PM-3) + dosing (PM-5)
    for tg, x in (('R-201', X_R1), (RT, X_R2)):
        E('reactor2', tg, x, RY, RW, RH, lab=(x + RW / 2, 260.5, 'm'), hitbox=[(.04, .02, .96, 1.03)],
          nz={'gas': (.5, 0, 'U'), 'fd': (0, (236 - RY) / RH, 'L'), 'js': (1, .86, 'R'), 'jr': (1, (222 - RY) / RH, 'R'),
              'mo': (1, (200 - RY) / RH, 'R'), 'ret': (1, (226 - RY) / RH, 'R')})
    E('pump2', 'P-202', 206, 236.24, 8, 8, lab=(210, 251.5, 'm'))
    E('dtank2', 'TK-201', 178, 282, 14, 18, lab=(185, 304.8, 'm'), nz={'out': (1, (293.5 - 282) / 18, 'R'), 'pw': (0, .85, 'L'), 'li': (.5, 0, 'U')})
    E('pd_pump2', 'P-203', 196, 290, 7, 7, lab=(199.5, 302.4, 'm'))
    E('dtank2', 'TK-202', 214, 282, 14, 18, lab=(221, 304.8, 'm'), nz={'out': (1, (293.5 - 282) / 18, 'R'), 'pw': (0, .85, 'L'), 'li': (.5, 0, 'U')})
    E('pd_pump2', 'P-204', 232, 290, 7, 7, lab=(235.5, 302.4, 'm'))
    # ---- A-300 proses kontak (PM-4: degasser + settler lamella) + efluen/lumpur (PM-10)
    E('kopot2', 'DG-301', 278, 188, 12, 26, lab=(276.5, 196, 'r'), nz={'in': (0, (200 - 188) / 26, 'L'), 'gas': (.5, 0, 'U'), 'out': (.5, 1, 'D')})
    E('lamella2', 'LS-301', 300, 204, 40, 24, lab=(320, 201.2, 'm'), nz={'in': (0, (216 - 204) / 24, 'L'), 'of': (1, (207 - 204) / 24, 'R'), 'uf1': (.25, 1, 'D'), 'uf2': (.75, 1, 'D')})
    E('pump2', 'P-301', 296, 238, 8, 8, lab=(294.5, 249.5, 'r'))
    E('pd_pump2', 'P-303', 334, 240, 8, 8, lab=(331, 251.5, 'r'))
    E('spress2', 'PR-501', 290, 268, 40, 16, lab=(318, 291.6, 'l'), nz={'in': (.23, -.16, 'U'), 'poly': (.40, -.16, 'U'), 'cake': (0, .6, 'L'), 'f': (.625, 1.12, 'D')})
    E('vtank2', 'TK-301', X_TK3, RY, RW, RH, lab=(X_TK3 + 12, 260.5, 'm'), hitbox=[(.04, .02, .96, 1.03)],
      nz={'in': (0, (193.2 - RY) / RH, 'L'), 'fi': (0, (218.4 - RY) / RH, 'L'), 'out': (1, .9, 'R')})
    E('pump2', 'P-501', 380, 239.6, 8, 8, lab=(384, 255, 'm'))
    # ---- A-400 biogas (PM-6, PM-7)
    E('gasholder2', 'GH-301', 176, 96, 56, 40, lab=(204, 125, 'm'), inner_label=True, hitbox=[(.08, .1, .92, 1), (0, .5, 1, 1)],
      nz={'in': (.3, 1, 'D'), 'out': (.7, 1, 'D')})
    E('btf2', 'BTF-301', 270, 40, 16, 84, lab=(268, 60, 'r'), hitbox=[(0, 0, 1, 1.03)],
      nz={'in': (0, .78, 'L'), 'top': (.5, 0, 'U'), 'air': (1, (116 - 40) / 84, 'R'), 'sump': (0, (118 - 40) / 84, 'L'), 'dist': (0, (55.96 - 40) / 84, 'L')})
    E('pump2', 'P-305', 254, 114, 8, 8, lab=(258, 129.5, 'm'))
    E('blower2', 'K-301', 292, 112, 8, 8, lab=(306, 113.6, 'l'), nz={'in': (.25, 0, 'U'), 'out': (0, .5, 'L')})
    E('shtx2', 'HX-301', 300, 25, 30, 10, lab=(315, 22, 'm'), nz={'in': (0, .5, 'L'), 'out': (1, .5, 'R'), 'cs': (.3, 1, 'D'), 'cr': (.7, 1, 'D')})
    E('box', 'CH-301', 304, 44, 22, 10, lab=(315, 50.3, 'm'), inner_label=True, nz={'s': (.2273, 0, 'U'), 'r': (.7727, 0, 'U')})
    E('kopot2', 'V-301', 342, 20, 12, 30, lab=(356, 26, 'l'), nz={'in': (0, (30 - 20) / 30, 'L'), 'out': (.5, 0, 'U'), 'dr': (.5, 1, 'D')})
    E('blower2', 'K-302', 366, 22, 10, 10, lab=(379, 25, 'l'), nz={'in': (.25, 0, 'U'), 'out': (.75, 1, 'D')})
    E('acf2', 'AC-301', 390, 20, 16, 44, lab=(388, 16.5, 'm'), hitbox=[(0, 0, 1, 1.05)], nz={'in': (0, (40 - 20) / 44, 'L'), 'out': (1, .88, 'R'), 'sp': (1, .2, 'R')})
    E('flare2', 'FL-301', 440, 40, 12, 46, lab=(446, 91.5, 'm'), hitbox=[(0, -.06, 1, 1)], nz={'in': (0, .74, 'L')})
    # ---- A-500 CHP + panas (PM-8, PM-9)
    E('genset2', 'GE-401', 452, 200, 84, 34, lab=(494, 240, 'm'), inner_label=True, hitbox=[(0, 0, 1, 1), (.6, -.1, .94, 0)],
      nz={'gas': (0, .6, 'L'), 'air': (0, .25, 'L'), 'ex': (.97, 0, 'U'), 'jo': (1, .3, 'R'), 'ji': (1, .7, 'R'), 'el': (.3, 1, 'D')})
    E('wherb2', 'HX-401', 525.5, 140, 16, 30, lab=(523, 150, 'r'), nz={'in': (.5, 1, 'D'), 'out': (.5, 0, 'U'), 'ho': (1, .3, 'R'), 'hi': (1, .7, 'R')})
    E('stack2', 'ST-401', 552, 50, 12, 64, lab=(558, 46.5, 'm'), hitbox=[(.2, 0, .8, 1.03)], nz={'in': (.06, .8, 'L')})
    # ---- A-600 utilitas (PM-9)
    E('ctower2', 'CT-601', 40, 36, 36, 40, lab=(58, 82, 'm'), hitbox=[(.28, 0, .72, .16), (.08, .16, .92, .84), (-.02, .84, 1.02, 1)],
      nz={'cwr': (.929, .36, 'R'), 'cws': (1.02, .92, 'R'), 'mk': (-.02, .95, 'L')})
    E('pump2', 'P-601', 80.4, 68.8, 8, 8, lab=(84.4, 84, 'm'))

# =====================================================================================================
# 3. ALIRAN PROSES + UTILITAS
# =====================================================================================================
def streams():
    # ---------------- A-100
    y1 = P('SC-101.in')[1]
    f = flag("POME", 22, y1, 'r', 'in'); L('s1', [f['pt'][:2], P('SC-101.in')], 1, dpos=.5)
    so = P('SC-101.out'); pl = P('P-101.l')
    L('s3a', [so, (so[0], pl[1]), pl])
    pt = P('P-101.t'); hi = P('HC-101.in')
    L('s3b', [pt, (pt[0], hi[1]), hi], 3, dseg=0, dpos=.55)
    of = P('HC-101.of'); ei = P('E-101.in')
    L('s3c', [of, (of[0], 148), (84, 148), (84, ei[1]), ei])
    eo = P('E-101.out'); ti = P('TK-101.in')
    L('s4', [eo, (ti[0], eo[1]), ti], 4, dseg=0, dpos=.3)
    # residu saringan + pasir
    sc = P('SC-101.scr'); uf = P('HC-101.uf')
    fr = flag("Residu ke PKS", 28, 228, 'l', 'out')
    L('s2', [uf, (uf[0], 228), fr['pt'][:2]], 2, dseg=1, dpos=.4)
    L('s2b', [sc, (sc[0], 228)], arrow=False); J(sc[0], 228)
    # ---------------- umpan reaktor + dosing
    to = P('TK-101.out'); pl = P('P-201.l')
    L('s7a', [to, (147, to[1]), (147, pl[1]), pl])
    pt = P('P-201.t')
    L('s7', [pt, (pt[0], YH), (230, YH)], 7, dseg=1, dpos=.55, arrow=False)
    for x, tg in ((170, 'R-201'), (230, RT)):
        fd = P(tg + '.fd'); L('f' + tg, [(x, YH), (x, fd[1]), fd])
    J(170, YH)
    a = P('P-203.t'); L('s5', [a, (a[0], 269), (160, 269), (160, YH)], 5, dseg=1, dpos=.5); J(160, YH)
    b = P('P-204.t'); L('s6', [b, (b[0], 265.5), (165, 265.5), (165, YH)], 6, dseg=1, dpos=.18); J(165, YH)
    d.conn('n1', 'TK-201.out', 'P-203.l'); d.conn('n2', 'TK-202.out', 'P-204.l')
    # jet mixing (digambar pada R-201, identik pada semua reaktor)
    js = P('R-201.js'); pl = P('P-202.l'); L('jm1', [js, (203, js[1]), (203, pl[1]), pl] if abs(js[1] - pl[1]) > .01 else [js, pl])
    jt = P('P-202.t'); jr = P('R-201.jr'); L('jm2', [jt, (jt[0], jr[1]), jr])
    xm = (X_R1 + RW + X_R2) / 2
    d.text(xm, 186, "R-202 s/d", 1.8, 'm', True); d.text(xm, 189.8, "R-2%02d" % (NR - 1), 1.8, 'm', True); d.text(xm, 193.4, "identik", 1.45, 'm', False)
    # ---------------- A-300 proses kontak
    mo = P(RT + '.mo'); L('s8', [mo, P('DG-301.in')], 8, dpos=.45)
    do = P('DG-301.out'); li = P('LS-301.in'); L('s8b', [do, (do[0], li[1]), li])
    dg = P('DG-301.gas'); gx = P(RT + '.gas')[0]; L('s8g', [dg, (dg[0], YG), (gx, YG)], arrow=False); J(gx, YG)
    of = P('LS-301.of'); tin = P('TK-301.in'); L('s10', [of, (345, of[1]), (345, tin[1]), tin], 10, dseg=1, dpos=.5)
    u1 = P('LS-301.uf1'); pr = P('P-301.r'); L('s9a', [u1, (u1[0], pr[1]), pr])
    pt = P('P-301.t'); ret = P(RT + '.ret'); L('s9', [pt, (pt[0], 234), (264, 234), (264, ret[1]), ret], 9, dseg=1, dpos=.5)
    u2 = P('LS-301.uf2'); pl = P('P-303.l'); L('s11a', [u2, (u2[0], pl[1]), pl])
    pt = P('P-303.t'); pin = P('PR-501.in'); L('s11', [pt, (pt[0], 236), (343.5, 236), (343.5, 255), (pin[0], 255), pin], 11, dseg=3, dpos=.2)
    po = P('PR-501.poly'); fp = flag("Polimer", 318, 258, 'l', 'in'); L('s26', [fp['pt'][:2], (po[0], 258), po], 26, dseg=0, dpos=.45)
    ck = P('PR-501.cake'); fk = flag("Kue lumpur ke kebun", 286, ck[1], 'l', 'out'); L('s12', [ck, fk['pt'][:2]])
    fi = P('PR-501.f'); tf = P('TK-301.fi'); L('s13', [fi, (fi[0], 294), (347, 294), (347, tf[1]), tf], 13, dseg=1, dpos=.55)
    to = P('TK-301.out'); L('s14a', [to, P('P-501.l')])
    pt = P('P-501.t'); fe = flag("Efluen ke kolam polishing / aplikasi lahan", 392, 228, 'r', 'out')
    L('s14', [pt, (pt[0], 228), fe['pt'][:2]], 14, dseg=0, dpos=.5)
    # ---------------- A-400 biogas
    g1 = P('R-201.gas'); g2 = P(RT + '.gas'); gi = P('GH-301.in')
    L('s15a', [g1, (g1[0], YG), (gi[0], YG)], arrow=False)
    L('s15b', [g2, (g2[0], YG), (gi[0], YG)], 15, dseg=1, dpos=.6, arrow=False)
    L('s15', [(gi[0], YG), gi]); J(gi[0], YG)
    go = P('GH-301.out'); bi = P('BTF-301.in')
    L('s16', [go, (go[0], 142), (266, 142), (266, bi[1]), bi], 16, dseg=1, dpos=.45)
    # resirkulasi BTF + blowdown
    su = P('BTF-301.sump'); pr = P('P-305.r'); L('rc1', [su, pr])
    pt = P('P-305.t'); di = P('BTF-301.dist'); L('rc2', [pt, (pt[0], di[1]), di])
    fb = flag("Blowdown S ke IPAL", 240, 92, 'l', 'out'); L('s19', [(pt[0], 92), fb['pt'][:2]], 19, dpos=.75); J(pt[0], 92)
    ki = P('K-301.in'); fa = flag("Udara", 310, 104, 'l', 'in'); L('s17', [fa['pt'][:2], (ki[0], 104), ki], 17, dseg=0, dpos=.5)
    ko = P('K-301.out'); L('s17b', [ko, P('BTF-301.air')])
    tp = P('BTF-301.top'); hi = P('HX-301.in'); L('s18', [tp, (tp[0], hi[1]), hi], 18, dseg=1, dpos=.5)
    ho = P('HX-301.out'); vi = P('V-301.in'); L('g1', [ho, (336, ho[1]), (336, vi[1]), vi] if abs(ho[1] - vi[1]) > .01 else [ho, vi])
    dr = P('V-301.dr'); fc = flag("Kondensat ke IPAL", 352, 68, 'r', 'out'); L('s20', [dr, (dr[0], 68), fc['pt'][:2]], 20, dseg=0, dpos=.7)
    vt = P('V-301.out'); ki = P('K-302.in'); L('g2', [vt, (vt[0], 15), (ki[0], 15), ki])
    ko = P('K-302.out'); ai = P('AC-301.in'); L('g3', [ko, (ko[0], ai[1]), ai])
    sp = P('AC-301.sp'); fs = flag("Karbon jenuh (berkala)", 412, sp[1], 'r', 'out'); L('s25', [sp, fs['pt'][:2]], 25)
    ao = P('AC-301.out'); fl = P('FL-301.in'); gg = P('GE-401.gas')
    L('s21a', [ao, (412, ao[1]), (412, fl[1])], arrow=False); J(412, fl[1])
    L('s22', [(412, fl[1]), fl], 22, dpos=.8)
    L('s21', [(412, fl[1]), (412, gg[1]), gg], 21, dseg=0, dpos=.82)
    # ---------------- A-500 CHP
    ga = P('GE-401.air'); fair = flag("Udara bakar", 444, ga[1], 'r', 'in'); L('s23', [fair['pt'][:2], ga], 23, dpos=.4)
    ex = P('GE-401.ex'); hx = P('HX-401.in'); L('ex1', [ex, hx])
    hxo = P('HX-401.out'); si = P('ST-401.in'); L('s24', [hxo, (hxo[0], si[1]), si], 24, dseg=1, dpos=.5)
    # sirkuit air panas: HWR -> jaket GE -> HX-401 -> HWS
    ji = P('GE-401.ji'); jo = P('GE-401.jo'); hi_ = P('HX-401.hi'); ho_ = P('HX-401.ho')
    fhr = flag("HWR 70 \u00b0C dari PKS", 548, 252, 'r', 'in', util=True)
    U('hw1', [fhr['pt'][:2], (562, 252), (562, ji[1]), ji], 'HW')
    U('hw2', [jo, (550, jo[1]), (550, hi_[1]), hi_], 'HW')
    fhs = flag("HWS 90 \u00b0C ke PKS", 568, 262, 'l', 'out', util=True)
    U('hw3', [ho_, (574, ho_[1]), (574, 262), fhs['pt'][:2]], 'HW')
    el = P('GE-401.el'); fe2 = flag("Listrik 400 V ke MCC / PKS", 480, 262, 'r', 'out', util=True)
    U('el1', [el, (el[0], 262), fe2['pt'][:2]], 'EL')
    # ---------------- A-600 utilitas: CT-601 -> E-101, header PW
    cw = P('CT-601.cws'); pl = P('P-601.l'); U('cw0', [cw, pl], 'CWS')
    pt = P('P-601.t'); a = P('E-101.cs'); b = P('E-101.cr'); cr = P('CT-601.cwr')
    U('cw1', [pt, (pt[0], 62), (a[0], 62), a], 'CWS')
    q1 = P('HX-301.cs'); q2 = P('HX-301.cr'); c1 = P('CH-301.s'); c2 = P('CH-301.r')
    U('ch1', [c1, (q1[0], q1[1])], 'CWS'); U('ch2', [q2, c2], 'CWR')
    U('cw2', [b, (b[0], cr[1]), cr], 'CWR')
    d.text(a[0] - 1.2, 100, "CWS 30 \u00b0C", 1.4, 'r', True); d.text(b[0] + 1.2, 100, "CWR 40 \u00b0C", 1.4, 'l', True)
    mk = P('CT-601.mk'); fm = flag("Air baku", 28, mk[1], 'r', 'in', util=True); U('mk', [fm['pt'][:2], mk], 'PW')
    fpw = flag("Air baku (PW)", 40, Y_PW, 'r', 'in', util=True)
    U('pw0', [fpw['pt'][:2], (210, Y_PW)], 'PW')
    for k, (tg, x) in enumerate((('TK-201', 174), ('TK-202', 210))):
        q = P(tg + '.pw'); U('pw%d' % (k + 1), [(x, Y_PW), (x, q[1]), q], 'PW')
        if x != 210: J(x, Y_PW)
    d.text(44, Y_PW + 3.4, "Header air baku / proses (PW)", 1.4, 'l', True)

# =====================================================================================================
# 4. INSTRUMENTASI (ISA-5.1)
# =====================================================================================================
RB = 2.7
_ns = [0]
def _trim(pts):
    (x0, y0), (x1, y1) = pts[0], pts[1]
    Lg = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    return [(x0 + (x1 - x0) / Lg * RB, y0 + (y1 - y0) / Lg * RB)] + list(pts[1:])
def loop(fn, num, x, y, *lines):
    d.inst2(x, y, fn, num, RB)
    for p in lines:
        _ns[0] += 1; d.conn('sg%d' % _ns[0], None, None, pts=_trim(p), cls='sig', arrow=False)
def cv(x, y, vert=False): return d.cvalve(x, y, vert)[:2]

LOOPS = [("TIC-102", "T umpan reaktor → katup CWR E-101 (SP dari TIC-206)"),
         ("LIC-103", "Level TK-101 → VSD P-201"),
         ("FQI-201", "Laju + total umpan reaktor (OLR)"),
         ("AIC-202", "pH reaktor 7,0 → pompa NaOH P-203"),
         ("AIC-203", "NH₄-N < 50 mg/L → pompa urea P-204 (siaga)"),
         ("LI-204/205", "Level tangki dosing, alarm rendah"),
         ("TIC-206", "T reaktor 55 °C → SP kaskade TIC-102"),
         ("LIA-207", "Level reaktor (luapan gravitasi), alarm"),
         ("FIC-301", "Resirkulasi lumpur %s m³/hari → VSD P-301" % idn(LS["recycle_m3d"])),
         ("PIC-302", "Vakum DG-301 -0,3 bar → VSD pompa vakum"),
         ("LIC-303", "Selimut lumpur LS-301 → P-303"),
         ("FIC-304", "Lumpur buangan → P-303 (SRT %.0f d)" % RV["srt_d"]),
         ("LIC-305", "Level TK-301 → VSD P-501"),
         ("LIC-401", "Isi GH-301 → SP beban JIC-501"),
         ("LIC-402", "Level sump BTF → katup blowdown"),
         ("AIC-403", "O₂ keluar BTF → VSD blower K-301"),
         ("LIC-404", "Level V-301 → katup kondensat"),
         ("PIC-405", "P buang K-302 → VSD K-302"),
         ("AIA-406", "CH₄ / H₂S gas mesin, alarm + trip"),
         ("PIC-407", "P header tinggi → katup flare FL-301"),
         ("JIC-501", "Beban genset → katup gas GE-401/402"),
         ("TI-502", "Suhu HWS ke PKS"),
         ("LIC-601", "Level bak CT-601 → katup air baku")]

def instruments():
    # TIC-102
    b = P('E-101.cr'); vx, vy = cv(b[0], 118, True)
    loop('TIC', 102, 122, 140, [(122, 140), (122, 163)], [(122, 140), (122, vy), (vx, vy)])
    # LIC-103
    loop('LIC', 103, 152, 185, [(152, 185), (144, 185)], [(152, 185), (152, 265.6)])
    # FQI-201
    loop('FQI', 201, 220, 252, [(220, 252), (220, YH)])
    # dosing
    loop('LI', 204, 185, 275.3, [(185, 275.3), P('TK-201.li')])
    loop('LI', 205, 221, 275.3, [(221, 275.3), P('TK-202.li')])
    loop('AIC', 202, 207.5, 283, [(207.5, 283), (207.5, 293.5), (203, 293.5)])
    loop('AIC', 203, 243.5, 283, [(243.5, 283), (243.5, 293.5), (239, 293.5)])
    # reaktor
    loop('TIC', 206, 166, 200, [(166, 200), (176, 200)])
    loop('LIA', 207, 270, 180, [(270, 180), (260, 180)])
    # proses kontak
    loop('FIC', 301, 276, 228, [(276, 228), (276, 234)])
    loop('PIC', 302, 296, 192, [(296, 192), (290, 192)])
    loop('LIC', 303, 330, 196, [(330, 196), (330, 204)])
    loop('FIC', 304, 318, 248, [(318, 248), (318, 255)])
    loop('LIC', 305, 382, 185, [(382, 185), (374, 185)], [(382, 185), (390, 185), (390, 243.6), (388, 243.6)])
    # gas
    loop('LIC', 401, 170, 110, [(170, 110), (180.3, 110)])
    vx, vy = cv(252, 92)
    loop('LIC', 402, 264, 80, [(264, 80), (270, 80)], [(264, 80), (252, 80), (vx, vy)])
    loop('AIC', 403, 304, 124, [(304, 124), (296, 124), (296, 120)])
    dr = P('V-301.dr'); vx, vy = cv(dr[0], 54.5, True)
    loop('LIC', 404, 362, 47, [(362, 47), (354, 47)], [(362, 47), (362, vy), (vx, vy)])
    loop('PIC', 405, 382, 50, [(382, 50), (382, 40)], [(382, 50), (371, 50), (371, 32)])
    loop('AIA', 406, 422, 150, [(422, 150), (412, 150)])
    fl = P('FL-301.in'); vx, vy = cv(423, fl[1])
    loop('PIC', 407, 423, 60, [(423, 60), (416, 60), (416, fl[1])], [(423, 60), (vx, vy)])
    gg = P('GE-401.gas'); vx, vy = cv(420, gg[1])
    loop('JIC', 501, 420, 196, [(420, 196), (vx, vy)])
    loop('TI', 502, 566, 140, [(566, 140), (566, 149)])
    mk = P('CT-601.mk'); vx, vy = cv(34, mk[1])
    loop('LIC', 601, 34, 60, [(34, 60), (41.3, 60)], [(34, 60), (vx, vy)])

# =====================================================================================================
# 5. PITA BAWAH: LEGENDA | DAFTAR PERALATAN | KONDISI ALIRAN + CATATAN | LOOP KENDALI | BLOK JUDUL
# =====================================================================================================
Y0, Y1 = YR, H - 10
def tc(x, y, t, size=1.3, anchor='l', bold=False): d.text(x, y, t, size, anchor, bold, layer='table', chk=False)
def hl(x0, x1, y, w=.15): d.line([(x0, y), (x1, y)], w, None, '#000000', 'table')
def vl(x, y0, y1, w=.15): d.line([(x, y0), (x, y1)], w, None, '#000000', 'table')
def panel(x0, x1, title):
    vl(x1, Y0, Y1, .6)
    d.rect(x0, Y0, x1 - x0, 4.6, .0, '#e6e6e6', 'table'); hl(x0, x1, Y0 + 4.6, .4)
    tc((x0 + x1) / 2, Y0 + 3.4, title, 1.9, 'm', True)
    return Y0 + 4.6

EQL = [
 ("SC-101", "Saringan drum putar, %s m³/jam, celah 0,75 mm" % idn(EQ["screen"]["flow_m3h"], 1), "PM-1"),
 ("P-101", "Pompa umpan desander, H %.0f m, VSD" % R["EQ"]["H_desander"], "PM-1"),
 ("HC-101", "Hidrosiklon desander, η pasir %.0f %%" % (EQ["desander"]["grit_removal"] * 100), "PM-1"),
 ("E-101", "Pendingin POME pelat, %s kWth, 85 → %s °C" % (idn(EQ["pome_cooler"]["duty_kW"]), idn(EQ["pome_cooler"]["T_out"])), "PM-1"),
 ("TK-101", "Tangki penyangga umpan, GFS Ø5,73 m, ± 100 m³", "PM-2"),
 ("P-201 A/B", "Pompa umpan reaktor, %s m³/jam, H %.0f m, VSD" % (idn(EQ["feed_pump"]["flow_m3_h"], 1), R["EQ"]["H_feed"]), "PM-5"),
 ("R-201..2%02d" % NR, "Reaktor kontak 55 °C, GFS %d × %s m³, Ø%s × %s m" % (NR, idn(RV["V_liq_m3"]), idn(RV["D_m"], 2), idn(RV["H_shell_m"], 1)), "PM-3"),
 ("P-202", "Pompa jet mixing, 1 per reaktor, %s kW" % idn(RV["mixer_kW"], 1), "PM-3"),
 ("TK-201/P-203", "Dosing NaOH 30 %%, P95 %s kg/hari" % idn(EQ["alkali_dosing"]["NaOH_kg_d_P95"]), "PM-5"),
 ("TK-202/P-204", "Dosing urea-N (siaga), P95 %s kg N/hari" % idn(EQ["nutrient_dosing"]["N_kg_d_P95"]), "PM-5"),
 ("DG-301", "Degasser vakum Ø1,6 × 4 m, CH₄ terlarut → gas", "PM-4"),
 ("LS-301", "Settler lamella %s m² proyeksi, tangkapan %.0f %%" % (idn(LS["A_proj_m2"]), LS["capture"] * 100), "PM-4"),
 ("P-301 A/B", "Pompa resirkulasi lumpur %s m³/hari, VSD" % idn(LS["recycle_m3d"]), "PM-4"),
 ("P-303", "Pompa lumpur buangan (PC), %s m³/hari" % idn(EQ["waste_sludge"]["Qw_m3d"]), "PM-4"),
 ("PR-501", "Screw press, kue %s t/hari, 20 %% DS" % idn(EQ["waste_sludge"]["cake_t_d"], 1), "PM-10"),
 ("TK-301", "Tangki efluen, GFS Ø6,88 m, ± 150 m³", "PM-10"),
 ("P-501", "Pompa efluen ke kolam polishing", "PM-10"),
 ("GH-301", "Penampung gas membran ganda, %s m³" % idn(EQ["gas_holder"]["V_m3"]), "PM-7"),
 ("BTF-301", "Bio-trickling filter, %s m³ media, η H₂S %.0f %%" % (idn(EQ["bio_desulfurizer"]["V_m3"], 1), EQ["bio_desulfurizer"]["eff"] * 100), "PM-6"),
 ("P-305", "Pompa resirkulasi nutrien BTF", "PM-6"),
 ("K-301", "Blower udara BTF, %s Nm³/jam" % idn(EQ["bio_desulfurizer"]["air_Nm3_h"], 1), "PM-6"),
 ("HX-301", "Pendingin gas ke titik embun 5 °C, %s kWth" % idn(EQ["gas_chiller"]["duty_kW"], 1), "PM-6"),
 ("CH-301", "Chiller paket berpendingin udara", "PM-6"),
 ("V-301", "KO pot kondensat dengan demister", "PM-6"),
 ("K-302 A/B", "Blower biogas, %s m³/jam, ΔP %.0f kPa" % (idn(EQ["gas_blower"]["flow_m3_h"]), EQ["gas_blower"]["dP_kPa"]), "PM-6"),
 ("AC-301", "Filter karbon aktif, H₂S → %s ppm" % idn(NOM["h2s_ppm_fuel"]), "PM-6"),
 ("FL-301", "Flare tertutup, %s Nm³/jam" % idn(EQ["flare"]["cap_Nm3_h"]), "PM-7"),
 ("GE-401/402", "Genset biogas %d × %s kWe, ηel %s %%" % (EQ["chp"]["N"], idn(EQ["chp"]["unit_kWe"]), idn(EQ["chp"]["eta_el_nom"] * 100, 1)), "PM-8"),
 ("HX-401", "Pemulih panas gas buang + jaket, %s kWth" % idn(EN["Q_heat_avail"]), "PM-9"),
 ("ST-401", "Cerobong gas buang", "PM-8"),
 ("CT-601", "Menara pendingin modular, %s kWth" % idn(EQ["cooling_tower"]["duty_kW"]), "PM-9"),
 ("P-601", "Pompa air pendingin", "PM-9"),
]
SN = {1: "POME mentah", 2: "Residu + pasir", 3: "POME bebas pasir", 4: "POME dingin", 5: "Larutan NaOH", 6: "Urea-N", 7: "Umpan reaktor",
      8: "Ke degasser + settler", 9: "Resirkulasi lumpur", 10: "Luapan settler", 11: "Lumpur buangan", 12: "Kue lumpur", 13: "Filtrat", 14: "Efluen akhir",
      15: "Biogas mentah", 16: "Biogas ke BTF", 17: "Udara BTF", 18: "Biogas keluar BTF", 19: "Blowdown BTF", 20: "Kondensat",
      21: "Biogas ke genset", 22: "Gas ke flare", 23: "Udara bakar", 24: "Gas buang", 25: "Karbon jenuh", 26: "Polimer"}
NOTES = ["Neraca massa dan energi lengkap: process/biogas_balance.py → outputs/results.json.",
         "Titik rancangan 45 t TBS/jam × 20 jam/hari; laju aliran rata-rata harian.",
         "R-201 s/d R-2%02d paralel; jet mixing & sensor digambar pada satu reaktor; membran = opsi PM-11." % NR,
         "A/B = 1 operasi + 1 cadangan. PSV/PVRV dan katup manual hanya di P&ID.",
         "Aliran 22 nol saat normal; 25 berkala (penggantian karbon)."]

def ribbon():
    # ---------------- A. LEGENDA
    x0, x1 = 10, 104; y = panel(x0, x1, "LEGENDA") + 3.2
    def row(lbl, fn):
        nonlocal y
        fn(x0 + 3, y); tc(x0 + 23, y + .5, lbl, 1.2); y += 3.5
    ln = lambda w, dash=None: (lambda x, yy: d.line([(x, yy), (x + 16, yy)], w, dash, '#000000', 'table'))
    def arr(x, yy):
        ln(.75)(x, yy); d.poly([(x + 16, yy), (x + 13.4, yy - .85), (x + 13.4, yy + .85)], .05, '#000000', '#000000', 'table')
    row("Aliran proses utama", arr)
    row("Air pendingin CWS / CWR", lambda x, yy: (ln(.42, UD['CWS'])(x, yy - .5), ln(.42, UD['CWR'])(x, yy + .7)))
    row("Air panas HWS / HWR", ln(.42, UD['HW']))
    row("Air baku / proses (PW)", ln(.42, UD['PW']))
    row("Listrik", ln(.42, UD['EL']))
    row("Sinyal instrumen (elektrik)", ln(.25, [.9, .6]))
    row("Larutan CIP (berkala)", ln(.75, UD['CIP']))
    def dia(x, yy):
        r = 1.45; xx = x + 8; d.poly([(xx, yy - r), (xx + r, yy), (xx, yy + r), (xx - r, yy)], .3, '#ffffff', '#000000', 'table'); tc(xx, yy + .4, "7", 1.0, 'm', True)
    row("Nomor aliran (lihat kondisi aliran)", dia)
    def bub(x, yy):
        xx = x + 8; d.circ(xx, yy, 1.5, .25, '#ffffff', 'table'); d.line([(xx - 1.5, yy), (xx + 1.5, yy)], .18, None, '#000000', 'table')
    row("Instrumen DCS/PLC (ISA-5.1)", bub)
    def cvs(x, yy):
        xx = x + 8; eng.Sym.valve(d, xx, yy + .8, False, 'table', 1.1); d.line([(xx, yy + .25), (xx, yy - .5)], .2, None, '#000000', 'table')
        d.poly(d.arcpts(xx, yy - .5, .8, .8, 0, 180), .2, '#ffffff', '#000000', 'table')
    row("Katup kendali, aktuator diafragma", cvs)
    def flg(x, yy): d.poly([(x + 1, yy - 1.3), (x + 13.5, yy - 1.3), (x + 15, yy), (x + 13.5, yy + 1.3), (x + 1, yy + 1.3)], .25, '#ffffff', '#000000', 'table')
    row("Batas baterai (masuk / keluar)", flg)
    def jn(x, yy): ln(.75)(x, yy); d.circ(x + 8, yy, .6, .05, '#000000', 'table', '#000000')
    row("Percabangan", jn)
    hl(x0, x1, y - 1.4, .3); y += 1.2
    for t in ("Huruf ISA-5.1: A analisis, F laju, J daya, L level, P tekanan,",
              "PD beda tekanan, T suhu; I indikasi, C kendali, Q total, A alarm.",
              "Simbol ISO 10628-2; penomoran alat PIP PIC-001.",
              "PM-x = modul portabel (skid / kontainer ISO / bejana standar)."):
        tc(x0 + 2, y, t, 1.1); y += 2.3
    # ---------------- B. DAFTAR PERALATAN
    x0, x1 = 104, 318; y = panel(x0, x1, "DAFTAR PERALATAN DAN MODUL PORTABEL")
    half = (len(EQL) + 1) // 2; cw = (x1 - x0) / 2; rh = (Y1 - y - 3.4) / half
    for c in range(2):
        xa = x0 + c * cw
        tc(xa + 1.5, y + 2.5, "Kode", 1.2, 'l', True); tc(xa + 21, y + 2.5, "Uraian dan ukuran utama", 1.2, 'l', True); tc(xa + cw - 1.5, y + 2.5, "Modul", 1.2, 'r', True)
        vl(xa + 19.5, y, Y1); vl(xa + cw - 10.5, y, Y1)
        for k, (tg, ds, pm) in enumerate(EQL[c * half:(c + 1) * half]):
            yy = y + 3.4 + rh * k
            tc(xa + 1.5, yy + rh * .72, tg, 1.18, 'l', True); tc(xa + 21, yy + rh * .72, ds, 1.18); tc(xa + cw - 1.5, yy + rh * .72, pm, 1.18, 'r')
            hl(xa, xa + cw, yy, .1)
    vl(x0 + cw, y, Y1, .35)
    # ---------------- C. KONDISI ALIRAN + CATATAN
    x0, x1 = 318, 434; y = panel(x0, x1, "KONDISI ALIRAN (TITIK RANCANGAN)")
    cw = (x1 - x0) / 2; rh = 2.5; ids = sorted(STR)
    cols = [(1.2, "No.", 'l'), (6.5, "Aliran", 'l'), (36.5, "T °C", 'r'), (44.5, "P bar", 'r'), (56.5, "kg/jam", 'r')]
    for c in range(2):
        xa = x0 + c * cw
        for dx, t, a in cols: tc(xa + (dx if a == 'l' else dx - 1.2), y + 2.4, t, 1.15, a, True)
        for k, i in enumerate(ids[c * 13:(c + 1) * 13]):
            s_ = STR[i]; yy = y + 3.3 + rh * k
            hl(xa, xa + cw, yy, .1)
            v = [str(i), SN[i], idn(s_["T"]), idn(s_["P"], 2), idn(s_["kg_h"]) if s_["kg_h"] >= 1 else "<1"]
            for (dx, _, a), t in zip(cols, v): tc(xa + (dx if a == 'l' else dx - 1.2), yy + 2.0, t, 1.12, a, dx < 2)
    vl(x0 + cw, y, y + 3.3 + 13 * rh, .35)
    yn = y + 3.3 + 13 * rh; hl(x0, x1, yn, .4)
    d.rect(x0, yn, x1 - x0, 3.6, .0, '#e6e6e6', 'table'); hl(x0, x1, yn + 3.6, .3); tc((x0 + x1) / 2, yn + 2.7, "CATATAN", 1.6, 'm', True)
    yy = yn + 6.0
    for k, t in enumerate(NOTES): tc(x0 + 1.5, yy, "%d. %s" % (k + 1, t), 1.1); yy += 2.25
    # ---------------- D. LOOP KENDALI
    x0, x1 = 434, 514; y = panel(x0, x1, "LOOP KENDALI UTAMA")
    rh = (Y1 - y - 1.0) / len(LOOPS)
    for k, (a, b) in enumerate(LOOPS):
        yy = y + rh * (k + .78) + .4
        tc(x0 + 1.2, yy, a, 1.12, 'l', True); tc(x0 + 15.5, yy, b, 1.12)
    vl(x0 + 14.5, y, Y1)
    # ---------------- E. BLOK JUDUL
    x0, x1 = 514, W - 10; xm = (x0 + x1) / 2
    T = lambda y, t, s_=1.4, b=False, a='m', x=None: tc(xm if x is None else x, y, t, s_, a, b)
    T(Y0 + 4.6, TEAM, 2.5, True); T(Y0 + 7.8, UNIV, 1.45)
    hl(x0, x1, Y0 + 9.2, .3)
    T(Y0 + 12.0, "ASPEBINDO EIC 2026 - Business Plan Competition", 1.25, True)
    hl(x0, x1, Y0 + 13.4, .3)
    T(Y0 + 17.6, "PROCESS FLOW DIAGRAM", 2.7, True)
    T(Y0 + 21.0, "SET BIOGAS DAPAT DIPINDAH", 1.5, True); T(Y0 + 23.7, "KONTAK TERMOFILIK 55 \u00b0C - POME", 1.5, True)
    T(Y0 + 26.4, "PKS 45 t TBS/jam (set 30 / 45 / 60 t/jam)", 1.15)
    hl(x0, x1, Y0 + 27.8, .3)
    T(Y0 + 30.6, "Biogas %s Nm\u00b3/hari, CH\u2084 %s %%; listrik %s / %s kWe" % (idn(NOM["biogas_Nm3d"]), idn(NOM["ch4_frac"] * 100, 1), idn(EN["P_gross"]), idn(EN["P_net"])), 1.08)
    T(Y0 + 33.0, "MC P5/P50/P95 neto %s / %s / %s kWe" % tuple(idn(R["monte_carlo"]["P_net"][k]) for k in ("P5", "P50", "P95")), 1.08)
    T(Y0 + 35.4, "%d muatan kontainer, \u00b1 %s t, plot \u00b1 %s ha" % (PM["ship_units_total"], idn(PM["mass_t_total"]), idn(PM["plot_area_m2_estimate"]["total"] / 1e4, 2)), 1.08)
    hl(x0, x1, Y0 + 37.0, .3)
    xs = [x0, x0 + 24, x0 + 46, x1]
    for xx in xs[1:-1]: vl(xx, Y0 + 37.0, Y0 + 45.6)
    for i, (h_, v_) in enumerate((("No. gambar", DWG_NO), ("Tanggal", DWG_DATE), ("Rev. / Skala", REV + "  /  NTS, A2"))):
        tc(xs[i] + 1.0, Y0 + 39.2, h_, 1.05); tc((xs[i] + xs[i + 1]) / 2, Y0 + 43.6, v_, 1.6, 'm', True)
    hl(x0, x1, Y0 + 45.6, .3)
    tc(x0 + 1.0, Y0 + 47.8, "Rev", 1.05, 'l', True); tc(x0 + 7, Y0 + 47.8, "Tgl", 1.05, 'l', True); tc(x0 + 21, Y0 + 47.8, "Keterangan", 1.05, 'l', True)
    hl(x0, x1, Y0 + 48.8, .12)
    revs = [("1", "15-10-26", "AnMBR 55 \u00b0C portabel"), ("2", "15-10-26", "Tata letak EPC, utilitas, simbol"), ("3", "16-10-26", "Kontak termofilik + tangki GFS")]
    for k, (a, b, c) in enumerate(revs):
        yy = Y0 + 51.2 + 2.4 * k; tc(x0 + 1.0, yy, a, 1.08); tc(x0 + 7, yy, b, 1.08); tc(x0 + 21, yy, c, 1.08)
    hl(x0, x1, Y0 + 57.6, .12)
    tc(x0 + 1.0, Y0 + 60.0, "Disusun: tim (dibantu alat AI)", 1.05); tc(x0 + 1.0, Y0 + 62.4, "Diperiksa / Disetujui: -       Status: kompetisi", 1.05)

def scale_table():
    x0, x1, y0 = 438, 580, 280
    T = R["tiers"]; S = PM["scaling"]; ks = ("30", "45", "60")
    rows = [("Kapasitas PKS, t TBS/jam", ks),
            ("POME, m\u00b3/hari", [idn(T[k]["POME_m3d"]) for k in ks]),
            ("Tangki GFS standar %s m\u00b3" % idn(RV["V_liq_m3"]), ["%d" % T[k]["N_modules"] for k in ks]),
            ("Settler lamella, m\u00b2", [idn(S[k]["lamella_m2"]) for k in ks]),
            ("Genset", ["%d \u00d7 %s kWe" % (T[k]["chp"]["N_gen"], idn(T[k]["chp"]["P_unit"])) for k in ks]),
            ("Listrik neto / kebutuhan PKS, kW", ["%s / %s" % (idn(T[k]["P_net"]), idn(T[k]["P_mill"])) for k in ks]),
            ("Listrik neto, GWh/tahun", [idn(T[k]["GWh_y"], 1) for k in ks])]
    rh = 3.3; h = 4.4 + rh * len(rows)
    d.rect(x0, y0, x1 - x0, h, .45, None, 'table'); d.rect(x0, y0, x1 - x0, 4.4, .0, '#e6e6e6', 'table')
    d.line([(x0, y0 + 4.4), (x1, y0 + 4.4)], .35, None, '#000000', 'table')
    d.text((x0 + x1) / 2, y0 + 3.2, "SKALA SET PRODUK UNTUK PKS SUMATERA (satu desain bejana)", 1.5, 'm', True, layer='table', chk=False)
    cx = [x0 + 52, x0 + 82, x0 + 112, x1]
    for k, (a, b) in enumerate(rows):
        yy = y0 + 4.4 + rh * k
        if k: d.line([(x0, yy), (x1, yy)], .1, None, '#000000', 'table')
        d.text(x0 + 1.5, yy + 2.35, a, 1.2, 'l', True, layer='table', chk=False)
        for i, t in enumerate(b): d.text((cx[i] + cx[i + 1]) / 2 if i < 3 else 0, yy + 2.35, t, 1.25, 'm', k == 0 or i == 1, layer='table', chk=False)
    for c in cx[:-1]: d.line([(c, y0 + 4.4), (c, y0 + h)], .12, None, '#000000', 'table')

def areas():
    area(14, 146, "A-100  PRAOLAH POME", "PM-1 skid praolah, PM-2 tangki umpan")
    area(150, 18, "A-400  PENGOLAHAN DAN PENYIMPANAN BIOGAS", "PM-6 skid gas, PM-7 penampung gas + flare")
    area(252, 160.5, "A-200  REAKTOR KONTAK 55 \u00b0C", "PM-3 reaktor GFS (\u00d7%d), PM-5 dosing + pompa umpan" % NR)
    area(392, 262, "A-300  DEGASSER, SETTLER, EFLUEN, LUMPUR", "PM-4 skid kontak, PM-10 efluen + lumpur")
    area(452, 182, "A-500  CHP DAN PEMULIHAN PANAS", "PM-8 kontainer genset (\u00d72), PM-9 HX-401")
    area(14, 18, "A-600  UTILITAS", "PM-9 menara pendingin, air baku")

if __name__ == "__main__":
    frame(); equipment(); streams(); instruments(); areas(); scale_table(); ribbon()
    d.finalize()
    d.pdf(os.path.join(OUT, "PFD_BG-002_Rev3.pdf")); d.svg(os.path.join(OUT, "PFD_BG-002_Rev3.svg")); d.dxf(os.path.join(OUT, "PFD_BG-002_Rev3.dxf"))
    iss = d.check(verbose=False)
    print("isu pemeriksa:", len(iss))
    for q in iss[:80]: print("  !", q)
