# -*- coding: utf-8 -*-
"""
PFD Rev 3 - format presentasi 16:9 (480 x 270 mm) untuk ditempel di slide PPT.
Teks besar (tag 2,4 mm, bendera 2,0 mm), pompa/blower diperbesar, tata letak dipadatkan,
pita bawah ringkas: legenda | daftar peralatan 4 kolom | data utama | blok judul.
Neraca aliran per nomor aliran tetap di process/outputs/results.json (tidak ditabelkan agar terbaca di slide).
Keluaran: outputs/PFD_BG-002_Rev3_deck.pdf/.dxf/.svg/.png.  Jalankan: python3 pfd_deck.py
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eng
import sym2  # noqa: F401  (mendaftarkan simbol *2)
from eng import Doc

W, H = 480.0, 270.0
eng.W, eng.H = W, H
TEAM = "NAMA TIM"
UNIV = "UNIVERSITAS"
DWG_NO = "PFD-BG-002"
REV = "3"
DWG_DATE = "15-10-2026"
eng.DOC_TITLE = "PFD Generator Biogas Portabel AnMBR Termofilik"
eng.DOC_AUTHOR = TEAM
eng.LW_PROC = .62; eng.LW_UTIL = .36; eng.LW_SIG = .22
eng.AH_PROC = (2.5, 1.55); eng.AH_UTIL = (2.0, 1.25)
eng.UG = '#000000'
eng.TAG_FS = 2.4; eng.DIA_R = 2.3; eng.DIA_FS = 1.8; eng.INST_FS = 1.55; eng.FLAG_FS = 2.0; eng.FLAG_H = 4.2

R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(HERE, "..", "process", "outputs", "portable_modules.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
EQ = R["equipment"]; EN = R["energy"]; NOM = R["nominal"]
RV = EQ["reactor_vessel"]; NR = RV["count"]; MB = EQ["membrane"]
RT = 'R-2%02d' % NR
d = Doc()
UD = {'CWS': [2.6, .9], 'CWR': [2.6, .9, .6, .9], 'PW': [1.1, .7], 'HW': [3.4, .9, .6, .9, .6, .9], 'EL': [.55, .7], 'CIP': [1.5, .7]}

def idn(x, dec=0):
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
P = lambda r: d.pt(r)[:2]
def L(key, pts, num=None, dseg=None, dpos=.5, arrow=True):
    return d.conn(key, None, None, pts=pts, num=num, dseg=dseg, dpos=dpos, arrow=arrow)
def U(key, pts, kind, arrow=True):
    return d.conn(key, None, None, pts=pts, cls='util', dash=UD[kind], arrow=arrow)
def flag(text, x, y, dr='r', kind='in', util=False): return d.flag(text, x, y, dr, kind, util=util)
def J(x, y): d.junction(x, y)

YR = 213            # batas atas pita bawah
def frame():
    d.rect(3, 3, W - 6, H - 6, .3, None, 'frame'); d.rect(5, 5, W - 10, H - 10, .7, None, 'frame')
    d.line([(5, YR), (W - 5, YR)], .7, None, '#000000', 'frame')
def area(x, y, title):
    d.text(x, y, title, 2.4, 'l', True, layer='frame', chk=False)
    d.line([(x, y + .8), (x + eng.twidth(title, 2.4, True), y + .8)], .3, None, '#000000', 'frame')

# =====================================================================================================
# PERALATAN
# =====================================================================================================
VY, VW, VH = 92, 16, 50           # bejana standar (TK-101, reaktor, TK-301)
YH = 154                          # header umpan reaktor
YG = 82                           # header biogas
Y_PW = 204
def equipment():
    E = d.eq
    vbox = [(.04, .02, .96, 1.04)]
    # A-600 utilitas
    E('ctower2', 'CT-601', 22, 16, 30, 32, lab=(37, 53.4, 'm'), hitbox=[(.28, 0, .72, .16), (.08, .16, .92, .5), (.06, .5, .94, .84), (0, .84, 1, 1)],
      nz={'cwr': (.929, .36, 'R'), 'cws': (1.02, .92, 'R'), 'mk': (-.02, .95, 'L')})
    E('pump2', 'P-601', 56, 41.9, 7, 7, lab=(59.5, 54.6, 'm'))
    # A-100 praolah
    E('rscreen2', 'SC-101', 20, 96, 20, 14, lab=(30, 93, 'm'), nz={'in': (0, .09, 'L'), 'out': (.6, 1, 'D'), 'scr': (.45, 1, 'D')})
    E('pump2', 'P-101', 40, 116, 7, 7, lab=(43.5, 129.8, 'm'))
    E('hcyc2', 'HC-101', 48, 84, 9, 22, lab=(59, 101, 'l'), nz={'in': (0, .08, 'L'), 'of': (.66, -.047, 'U'), 'uf': (.5, 1, 'D')})
    E('phe2', 'E-101', 64, 80, 16, 10, lab=(72, 95.6, 'm'), nz={'in': (0, .5, 'L'), 'out': (1.055, .5, 'R'), 'cs': (.3, 0, 'U'), 'cr': (.7, 0, 'U')})
    E('vtank2', 'TK-101', 88, VY, VW, VH, lab=(96, 149.6, 'm'), hitbox=vbox, nz={'in': (.25, 0, 'U'), 'out': (1, .9, 'R')})
    E('pump2', 'P-201', 108, 158, 7, 7, lab=(111.5, 171.6, 'm'))
    # A-200 reaktor
    for tg, x in (('R-201', 124), (RT, 166)):
        E('reactor2', tg, x, VY, VW, VH, lab=(x + VW / 2, 149.6, 'm'), hitbox=vbox, skirt=2.5,
          nz={'gas': (.5, 0, 'U'), 'fd': (0, .72, 'L'), 'js': (1, .86, 'R'), 'jr': (1, .56, 'R'),
              'mo': (1, .86, 'R'), 'ret': (1, .24, 'R'), 'ws': (1, .95, 'R')})
    E('pump2', 'P-202', 146, 131.5, 7, 7, lab=(154, 137.4, 'l'))
    E('dtank2', 'TK-201', 124, 172, 12, 16, lab=(130, 193.2, 'm'), nz={'out': (1, (183.5 - 172) / 16, 'R'), 'pw': (0, .85, 'L')})
    E('pd_pump2', 'P-203', 140, 180, 7, 7, lab=(143.5, 193.2, 'm'))
    E('dtank2', 'TK-202', 156, 172, 12, 16, lab=(162, 193.2, 'm'), nz={'out': (1, (183.5 - 172) / 16, 'R'), 'pw': (0, .85, 'L')})
    E('pd_pump2', 'P-204', 172, 180, 7, 7, lab=(175.5, 193.2, 'm'))
    # A-300 membran, efluen, lumpur
    E('pump2', 'P-301', 186, 131.5, 7, 7, lab=(189.5, 145, 'm'))
    E('membrane2', 'MB-301', 200, 108, 32, 10, lab=(216, 123, 'm'), inner_label=True,
      nz={'in': (0, .5, 'L'), 'ret': (1, .25, 'R'), 'perm': (.9, 1, 'D'), 'cip': (.28, 1, 'D')})
    E('ftank2', 'TK-302', 204, 128, 10, 13, lab=(215.5, 139.2, 'l'), nz={'out': (.5, 0, 'U')})
    E('pump2', 'P-302', 238, 124, 7, 7, lab=(241.5, 137.6, 'm'))
    E('pd_pump2', 'P-303', 190, 150, 7, 7, lab=(186.6, 159, 'r'))
    E('spress2', 'PR-501', 212, 172, 32, 12, lab=(214, 190.4, 'l'), nz={'in': (.23, -.16, 'U'), 'poly': (.40, -.16, 'U'), 'cake': (0, .6, 'L'), 'f': (.625, 1.12, 'D')})
    E('vtank2', 'TK-301', 256, VY, VW, VH, lab=(264, 149.6, 'm'), hitbox=vbox, nz={'in': (0, .16, 'L'), 'fi': (0, .85, 'L'), 'out': (1, .9, 'R')})
    E('pump2', 'P-501', 276, 133.5, 7, 7, lab=(279.5, 147, 'm'))
    # A-400 biogas
    E('gasholder2', 'GH-301', 128, 48, 40, 26, lab=(148, 69, 'm'), inner_label=True, hitbox=[(.08, .1, .92, 1), (0, .5, 1, 1)],
      nz={'in': (.35, 1, 'D'), 'out': (.75, 1, 'D')})
    E('btf2', 'BTF-301', 196, 18, 12, 54, lab=(194, 32, 'r'), hitbox=[(0, 0, 1, 1.04)],
      nz={'in': (0, (59.2 - 18) / 54, 'L'), 'top': (.5, 0, 'U'), 'sump': (1, (68 - 18) / 54, 'R'), 'dist': (1, (27 - 18) / 54, 'R')})
    E('pump2', 'P-305', 212, 64.5, 7, 7, lab=(221, 70.5, 'l'))
    E('blower2', 'K-301', 180, 60, 7, 7, lab=(184.5, 75.4, 'r'), nz={'in': (.25, 0, 'U'), 'out': (.75, 1, 'D')})
    E('shtx2', 'HX-301', 226, 9, 24, 8, lab=(222.5, 22, 'r'), nz={'in': (0, .5, 'L'), 'out': (1, .5, 'R'), 'cs': (.3, 1, 'D'), 'cr': (.7, 1, 'D')})
    E('box', 'CH-301', 228, 25, 20, 7, lab=(238, 29.6, 'm'), inner_label=True, nz={'s': (.26, 0, 'U'), 'r': (.74, 0, 'U')})
    E('kopot2', 'V-301', 258, 8, 9, 24, lab=(256, 26, 'r'), nz={'in': (0, (13 - 8) / 24, 'L'), 'out': (1, .12, 'R'), 'dr': (.5, 1, 'D')})
    E('blower2', 'K-302', 274, 14, 8, 8, lab=(284, 17, 'l'), nz={'in': (.25, 0, 'U'), 'out': (.75, 1, 'D')})
    E('acf2', 'AC-301', 296, 10, 12, 34, lab=(294, 47.5, 'r'), hitbox=[(0, 0, 1, 1.05)], nz={'in': (0, (28 - 10) / 34, 'L'), 'out': (1, .88, 'R'), 'sp': (1, .2, 'R')})
    E('flare2', 'FL-301', 336, 20, 10, 38, lab=(341, 62.6, 'm'), hitbox=[(0, -.06, 1, 1)], nz={'in': (0, .74, 'L')})
    # A-500 CHP
    E('genset2', 'GE-401', 330, 94, 62, 24, lab=None, inner_label=True, hitbox=[(0, 0, 1, 1), (.6, -.12, .94, 0)],
      nz={'gas': (0, .6, 'L'), 'air': (.1, 0, 'U'), 'ex': (.97, 0, 'U'), 'jo': (1, .3, 'R'), 'ji': (1, .7, 'R'), 'el': (.3, 1, 'D')})
    E('wherb2', 'HX-401', 382.1, 52, 16, 26, lab=(380, 62, 'r'), nz={'in': (.5, 1, 'D'), 'out': (.5, 0, 'U'), 'ho': (1, .3, 'R'), 'hi': (1, .7, 'R')})
    E('stack2', 'ST-401', 430, 22, 10, 44, lab=(435, 18.6, 'm'), hitbox=[(.2, 0, .8, 1.03)], nz={'in': (.125, .5, 'L')})

# =====================================================================================================
# ALIRAN
# =====================================================================================================
def streams():
    # ---------------- A-600 utilitas
    cw = P('CT-601.cws'); U('cw0', [cw, P('P-601.l')], 'CWS')
    pt = P('P-601.t'); a = P('E-101.cs'); b = P('E-101.cr'); cr = P('CT-601.cwr')
    U('cw1', [pt, (pt[0], 36), (a[0], 36), a], 'CWS')
    U('cw2', [b, (b[0], cr[1]), cr], 'CWR')
    d.text(a[0] - 1.0, 62, "CWS", 1.7, 'r', True); d.text(b[0] + 1.0, 62, "CWR", 1.7, 'l', True)
    mk = P('CT-601.mk'); fm = flag("PW", 15, mk[1], 'r', 'in', util=True); U('mk', [fm['pt'][:2], mk], 'PW')
    # ---------------- A-100 praolah
    y1 = P('SC-101.in')[1]
    f = flag("POME", 16, y1, 'r', 'in'); L('s1', [f['pt'][:2], P('SC-101.in')])
    so = P('SC-101.out'); pl = P('P-101.l'); L('s3a', [so, (so[0], pl[1]), pl])
    pt = P('P-101.t'); hi = P('HC-101.in'); L('s3b', [pt, (pt[0], hi[1]), hi], 3, dseg=0, dpos=.4)
    of = P('HC-101.of'); ei = P('E-101.in'); L('s3c', [of, (of[0], 76), (61, 76), (61, ei[1]), ei])
    eo = P('E-101.out'); ti = P('TK-101.in'); L('s4', [eo, (ti[0], eo[1]), ti], 4, dseg=0, dpos=.25)
    sc = P('SC-101.scr'); uf = P('HC-101.uf')
    fr = flag("Residu", 24, 134, 'l', 'out')
    L('s2', [uf, (uf[0], 134), fr['pt'][:2]], 2, dseg=1, dpos=.6)
    L('s2b', [sc, (sc[0], 134)], arrow=False); J(sc[0], 134)
    # ---------------- umpan reaktor + dosing
    to = P('TK-101.out'); pl = P('P-201.l'); L('s7a', [to, (106, to[1]), (106, pl[1]), pl])
    pt = P('P-201.t'); L('s7', [pt, (pt[0], YH), (161, YH)], 7, dseg=1, dpos=.72, arrow=False)
    for x, tg in ((119, 'R-201'), (161, RT)):
        fd = P(tg + '.fd'); L('f' + tg, [(x, YH), (x, fd[1]), fd])
    J(119, YH)
    a = P('P-203.t'); L('s5', [a, (a[0], 166), (125, 166), (125, YH)], 5, dseg=1, dpos=.5); J(125, YH)
    b = P('P-204.t'); L('s6', [b, (b[0], 162), (130, 162), (130, YH)], 6, dseg=1, dpos=.25); J(130, YH)
    d.conn('n1', 'TK-201.out', 'P-203.l'); d.conn('n2', 'TK-202.out', 'P-204.l')
    js = P('R-201.js'); L('jm1', [js, P('P-202.l')])
    jt = P('P-202.t'); jr = P('R-201.jr'); L('jm2', [jt, (jt[0], jr[1]), jr])
    d.text(153, 101, "R-202 s/d", 2.0, 'm', True); d.text(153, 104.4, "R-2%02d" % (NR - 1), 2.0, 'm', True); d.text(153, 107.6, "identik", 1.7, 'm', False)
    # ---------------- membran
    mo = P(RT + '.mo'); L('s8a', [mo, P('P-301.l')])
    pt = P('P-301.t'); mi = P('MB-301.in'); L('s8', [pt, (pt[0], mi[1]), mi], 8, dseg=0, dpos=.8)
    mr = P('MB-301.ret'); ret = P(RT + '.ret'); L('s9', [mr, (236, mr[1]), (236, ret[1]), ret], 9, dseg=2, dpos=.5)
    pp = P('MB-301.perm'); pl = P('P-302.l'); L('s10a', [pp, (pp[0], pl[1]), pl])
    pt = P('P-302.t'); tin = P('TK-301.in'); L('s10', [pt, (pt[0], tin[1]), tin], 10, dseg=1, dpos=.25)
    d.conn('cip', None, None, pts=[P('TK-302.out'), P('MB-301.cip')], dash=UD['CIP'])
    ws = P(RT + '.ws'); pl = P('P-303.l'); L('s11a', [ws, (185, ws[1]), (185, pl[1]), pl])
    pt = P('P-303.t'); pin = P('PR-501.in'); L('s11', [pt, (pt[0], 146), (pin[0], 146), pin], 11, dseg=2, dpos=.55)
    po = P('PR-501.poly'); fp = flag("Polimer", 236, 160, 'l', 'in'); L('s26', [fp['pt'][:2], (po[0], 160), po])
    ck = P('PR-501.cake'); fk = flag("Kue lumpur", 208, ck[1], 'l', 'out'); L('s12', [ck, fk['pt'][:2]])
    fi = P('PR-501.f'); tf = P('TK-301.fi'); L('s13', [fi, (fi[0], 196), (252, 196), (252, tf[1]), tf], 13, dseg=1, dpos=.5)
    to = P('TK-301.out'); L('s14a', [to, P('P-501.l')])
    pt = P('P-501.t'); fe = flag("Efluen ke kolam polishing", 292, 126, 'r', 'out'); L('s14', [pt, (pt[0], 126), fe['pt'][:2]], 14, dseg=0, dpos=.5)
    # ---------------- biogas
    g1 = P('R-201.gas'); g2 = P(RT + '.gas'); gi = P('GH-301.in')
    L('s15a', [g1, (g1[0], YG), (gi[0], YG)], arrow=False)
    L('s15b', [g2, (g2[0], YG), (gi[0], YG)], 15, dseg=1, dpos=.4, arrow=False)
    L('s15', [(gi[0], YG), gi]); J(gi[0], YG)
    go = P('GH-301.out'); bi = P('BTF-301.in')
    L('s16', [go, (go[0], 78), (190, 78), (190, bi[1]), bi], 16, dseg=2, dpos=.5)
    ko = P('K-301.out'); L('s17', [ko, (ko[0], 78)], arrow=True); J(ko[0], 78)
    fa = flag("Udara", 176, 46, 'r', 'in')
    ki = P('K-301.in'); L('s17a', [fa['pt'][:2], (ki[0], 46), ki], 17, dseg=1, dpos=.5)
    su = P('BTF-301.sump'); L('rc1', [su, P('P-305.l')])
    pt = P('P-305.t'); di = P('BTF-301.dist'); L('rc2', [pt, (pt[0], di[1]), di])
    fb = flag("Blowdown", 232, 40, 'r', 'out'); L('s19', [(pt[0], 40), fb['pt'][:2]], 19, dpos=.72); J(pt[0], 40)
    tp = P('BTF-301.top'); hi = P('HX-301.in'); L('s18', [tp, (tp[0], hi[1]), hi], 18, dseg=1, dpos=.45)
    L('g1', [P('HX-301.out'), P('V-301.in')])
    dr = P('V-301.dr'); fc = flag("Kondensat", 266, 46, 'r', 'out'); L('s20', [dr, (dr[0], 46), fc['pt'][:2]], 20, dseg=0, dpos=.72)
    vo = P('V-301.out'); ki = P('K-302.in'); L('g2', [vo, (ki[0], vo[1]), ki])
    ko = P('K-302.out'); ai = P('AC-301.in'); L('g3', [ko, (ko[0], ai[1]), ai])
    sp = P('AC-301.sp'); fs = flag("Karbon jenuh", 314, sp[1], 'r', 'out'); L('s25', [sp, fs['pt'][:2]], 25)
    ao = P('AC-301.out'); fl = P('FL-301.in'); gg = P('GE-401.gas')
    L('s21a', [ao, (312, ao[1]), (312, fl[1])], arrow=False); J(312, fl[1])
    L('s22', [(312, fl[1]), fl], 22, dpos=.75)
    L('s21', [(312, fl[1]), (312, gg[1]), gg], 21, dseg=0, dpos=.6)
    q1 = P('HX-301.cs'); q2 = P('HX-301.cr'); U('ch1', [P('CH-301.s'), q1], 'CWS'); U('ch2', [q2, P('CH-301.r')], 'CWR')
    # ---------------- CHP
    ga = P('GE-401.air'); fair = flag("Udara bakar", 332, 86, 'r', 'in'); L('s23', [fair['pt'][:2], (ga[0], 86), ga])
    d.text(372, 122.8, "GE-401/402 (\u00d72)", 2.4, 'm', True)
    L('ex1', [P('GE-401.ex'), P('HX-401.in')])
    hxo = P('HX-401.out'); si = P('ST-401.in'); L('s24', [hxo, (hxo[0], si[1]), si], 24, dseg=1, dpos=.55)
    ji = P('GE-401.ji'); jo = P('GE-401.jo'); hi_ = P('HX-401.hi'); ho_ = P('HX-401.ho')
    U('hw2', [jo, (400, jo[1]), (400, hi_[1]), hi_], 'HW')
    fhr = flag("HWR dari PKS", 404, 128, 'r', 'in', util=True); U('hw1', [fhr['pt'][:2], (412, 128), (412, ji[1]), ji], 'HW')
    fhs = flag("HWS ke PKS", 416, 140, 'l', 'out', util=True); U('hw3', [ho_, (420, ho_[1]), (420, 140), fhs['pt'][:2]], 'HW')
    el = P('GE-401.el'); fe2 = flag("Listrik ke PKS", 352, 134, 'r', 'out', util=True); U('el1', [el, (el[0], 134), fe2['pt'][:2]], 'EL')
    # ---------------- header PW
    fpw = flag("PW", 15, Y_PW, 'r', 'in', util=True)
    U('pw0', [fpw['pt'][:2], (153.5, Y_PW), (153.5, P('TK-202.pw')[1]), P('TK-202.pw')], 'PW')
    q = P('TK-201.pw'); U('pw1', [(121, Y_PW), (121, q[1]), q], 'PW'); J(121, Y_PW)
    d.text(26, Y_PW - 1.2, "Header air baku / proses (PW)", 1.8, 'l', True)

# =====================================================================================================
# INSTRUMENTASI (ISA-5.1)
# =====================================================================================================
RB = 3.0
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

def instruments():
    b = P('E-101.cr'); vx, vy = cv(b[0], 56, True)
    loop('TIC', 102, 88, 66, [(88, 66), (88, 85)], [(88, 66), (88, vy), (vx, vy)])
    loop('LIC', 103, 110, 100, [(110, 100), (104, 100)], [(110, 100), (110, 158.4)])
    loop('TIC', 206, 116, 113, [(116, 113), (124, 113)])
    loop('LI', 204, 119, 178, [(119, 178), (124, 178)])
    loop('LI', 205, 151, 178, [(151, 178), (156, 178)])
    loop('AIC', 202, 151, 198, [(151, 198), (151, 183.5), (147, 183.5)])
    loop('AIC', 203, 183, 198, [(183, 198), (183, 183.5), (179, 183.5)])
    loop('LIC', 207, 190, 96, [(190, 96), (182, 96)], [(190, 96), (250, 96), (250, 127.5), (245, 127.5)])
    loop('FIC', 301, 196, 122, [(196, 122), (189.5, 122)], [(196, 122), (196, 135), (193, 135)])
    loop('LI', 303, 219, 131, [(219, 131), (214, 131)])
    loop('FIC', 304, 201, 153.5, [(201, 153.5), (201, 146)], [(201, 153.5), (197, 153.5)])
    loop('LIC', 305, 278, 100, [(278, 100), (272, 100)], [(278, 100), (286, 100), (286, 137), (283, 137)])
    loop('LIC', 401, 122, 60, [(122, 60), (130.8, 60)])
    bd = P('P-305.t'); vx, vy = cv(221, 40)
    loop('LIC', 402, 224, 52, [(224, 52), (208, 52)], [(224, 52), (vx, 52), (vx, vy)])
    dr = P('V-301.dr'); vx, vy = cv(dr[0], 37, True)
    loop('LIC', 404, 271, 30, [(271, 30), (267, 30)], [(271, 30), (271, vy), (vx, vy)])
    loop('PIC', 405, 285, 34, [(285, 34), (285, 28)], [(285, 34), (276, 34), (276, 21.6)])
    loop('AIA', 406, 319, 70, [(319, 70), (312, 70)])
    fl = P('FL-301.in'); vx, vy = cv(320, fl[1])
    loop('PIC', 407, 320, 34, [(320, 34), (312, 34), (312, 39.9)], [(320, 34), (vx, vy)])
    gg = P('GE-401.gas'); vx, vy = cv(320, gg[1])
    loop('JIC', 501, 320, 97, [(320, 97), (vx, vy)])
    mk = P('CT-601.mk'); vx, vy = cv(18.2, mk[1])
    loop('LIC', 601, 12, 30, [(12, 30), (23.6, 30)], [(12, 30), (12, 40), (vx, 40), (vx, vy)])

def areas():
    area(8, 10.5, "A-600 UTILITAS")
    area(8, 76, "A-100 PRAOLAH")
    area(104, 10.5, "A-400 BIOGAS")

# =====================================================================================================
# PITA BAWAH
# =====================================================================================================
def tc(x, y, t, size=2.0, anchor='l', bold=False): d.text(x, y, t, size, anchor, bold, layer='table', chk=False)
def hl(x0, x1, y, w=.15): d.line([(x0, y), (x1, y)], w, None, '#000000', 'table')
def vl(x, y0, y1, w=.15): d.line([(x, y0), (x, y1)], w, None, '#000000', 'table')
Y0, Y1 = YR, H - 5
def head(x0, x1, title):
    d.rect(x0, Y0, x1 - x0, 5.2, .0, '#e6e6e6', 'table'); hl(x0, x1, Y0 + 5.2, .4)
    tc((x0 + x1) / 2, Y0 + 3.9, title, 2.3, 'm', True)
    vl(x1, Y0, Y1, .7)
    return Y0 + 5.2

EQL = [("SC-101", "Saringan drum putar"), ("P-101", "Pompa desander"), ("HC-101", "Hidrosiklon desander"), ("E-101", "Pendingin POME (PHE)"),
       ("TK-101", "Tangki penyangga umpan"), ("P-201", "Pompa umpan reaktor"), ("R-201..2%02d" % NR, "Reaktor AnMBR ×%d" % NR), ("P-202", "Pompa jet mixing"),
       ("TK/P-201..204", "Dosing NaOH dan urea"), ("P-301", "Pompa cross-flow"), ("MB-301", "Membran UF tubular"), ("P-302", "Pompa permeat"),
       ("TK-302", "Tangki CIP"), ("P-303", "Pompa lumpur buangan"), ("PR-501", "Screw press"), ("TK-301", "Tangki permeat"),
       ("P-501", "Pompa efluen"), ("GH-301", "Penampung gas"), ("BTF-301", "Bio-trickling filter H₂S"), ("P-305", "Pompa resirkulasi BTF"),
       ("K-301", "Blower udara BTF"), ("HX-301", "Pendingin gas 5 °C"), ("CH-301", "Chiller paket"), ("V-301", "KO pot kondensat"),
       ("K-302", "Blower biogas"), ("AC-301", "Filter karbon aktif"), ("FL-301", "Flare tertutup"), ("GE-401/402", "Genset biogas 2 × 800 kWe"),
       ("HX-401", "Pemulih panas"), ("ST-401", "Cerobong"), ("CT-601", "Menara pendingin"), ("P-601", "Pompa air pendingin")]

def ribbon():
    # ---- legenda
    x0, x1 = 5, 92; y = head(x0, x1, "LEGENDA") + 4.0
    ln = lambda w, dash=None: (lambda x, yy: d.line([(x, yy), (x + 14, yy)], w, dash, '#000000', 'table'))
    def arr(x, yy):
        ln(.62)(x, yy); d.poly([(x + 14, yy), (x + 11.5, yy - .8), (x + 11.5, yy + .8)], .05, '#000000', '#000000', 'table')
    def dia(x, yy):
        r = 1.6; d.poly([(x + 7, yy - r), (x + 7 + r, yy), (x + 7, yy + r), (x + 7 - r, yy)], .3, '#ffffff', '#000000', 'table')
    def bub(x, yy):
        d.circ(x + 7, yy, 1.7, .25, '#ffffff', 'table'); d.line([(x + 5.3, yy), (x + 8.7, yy)], .18, None, '#000000', 'table')
    def cvs(x, yy):
        eng.Sym.valve(d, x + 7, yy + .7, False, 'table', 1.2); d.line([(x + 7, yy + .1), (x + 7, yy - .6)], .2, None, '#000000', 'table')
        d.poly(d.arcpts(x + 7, yy - .6, .8, .8, 0, 180), .2, '#ffffff', '#000000', 'table')
    items = [(arr, "Proses"), (ln(.36, UD['CWS']), "Air pendingin CWS/CWR"), (ln(.36, UD['HW']), "Air panas HWS/HWR"), (ln(.36, UD['PW']), "Air baku (PW)"),
             (ln(.36, UD['EL']), "Listrik"), (ln(.22, [.9, .6]), "Sinyal instrumen"), (dia, "Nomor aliran"), (bub, "Instrumen (ISA-5.1)"), (cvs, "Katup kendali")]
    cw = (x1 - x0) / 2
    for k, (fn, t) in enumerate(items):
        c, r = divmod(k, 5)
        xx = x0 + 1.5 + c * cw; yy = y + r * 5.6
        fn(xx, yy); tc(xx + 16, yy + .7, t, 1.75)
    tc(x0 + 1.5 + cw, y + 4 * 5.6 + .7, "L level, T suhu, F laju, P tekanan,", 1.45)
    tc(x0 + 1.5 + cw, y + 4 * 5.6 + 3.0, "A analisis, J daya; C kendali, I indikasi", 1.45)
    # ---- daftar peralatan
    x0, x1 = 92, 330; y = head(x0, x1, "DAFTAR PERALATAN") + .6
    nc = 4; nr = (len(EQL) + nc - 1) // nc; cw = (x1 - x0) / nc; rh = (Y1 - y - .6) / nr
    for k, (tg, nm) in enumerate(EQL):
        c, r = divmod(k, nr)
        xx = x0 + c * cw; yy = y + rh * (r + .72)
        tc(xx + 1.5, yy, tg, 1.85, 'l', True); tc(xx + 21.5, yy, nm, 1.85)
        if r: hl(xx, xx + cw, y + rh * r - .1, .08)
    for c in range(1, nc): vl(x0 + c * cw, Y0 + 5.2, Y1, .3)
    # ---- data utama
    x0, x1 = 330, 404; y = head(x0, x1, "DATA UTAMA (45 t TBS/jam)") + .4
    rows = [("POME", "%s m³/hari, 85 °C" % idn(R["design_basis"]["pome_m3d"])),
            ("Reaktor", "%d × %s m³, 55 °C" % (NR, idn(RV["V_liq_m3"]))),
            ("Biogas", "%s Nm³/hari" % idn(NOM["biogas_Nm3d"])),
            ("CH₄ / H₂S", "%s %% / %s ppm" % (idn(NOM["ch4_frac"] * 100, 1), idn(NOM["h2s_ppm_fuel"]))),
            ("Listrik", "%s / %s kWe neto" % (idn(EN["P_gross"]), idn(EN["P_net"]))),
            ("Panas", "%s kWth air panas" % idn(EN["Q_heat_avail"])),
            ("Modul", "%d truk, ± %s ha" % (PM["ship_units_total"], idn(PM["plot_area_m2_estimate"]["total"] / 1e4, 2))),
            ("Emisi", "−%s tCO₂e/tahun" % idn(R["emissions"]["avoided_t"]))]
    rh = (Y1 - y - .4) / len(rows)
    for k, (a, b) in enumerate(rows):
        yy = y + rh * (k + .72); tc(x0 + 1.5, yy, a, 1.85, 'l', True); tc(x0 + 20, yy, b, 1.85)
    # ---- blok judul
    x0, x1 = 404, W - 5; xm = (x0 + x1) / 2
    tc(xm, Y0 + 5.0, TEAM, 3.0, 'm', True); tc(xm, Y0 + 9.0, UNIV, 1.8, 'm')
    hl(x0, x1, Y0 + 10.8, .35)
    tc(xm, Y0 + 15.6, "PROCESS FLOW DIAGRAM", 3.1, 'm', True)
    tc(xm, Y0 + 19.6, "Generator Biogas Portabel", 2.0, 'm', True); tc(xm, Y0 + 22.9, "AnMBR termofilik 55 °C dari POME", 1.8, 'm')
    hl(x0, x1, Y0 + 25.0, .35)
    tc(xm, Y0 + 28.6, "ASPEBINDO EIC 2026", 1.9, 'm', True); tc(xm, Y0 + 31.6, "Business Plan Competition", 1.6, 'm')
    hl(x0, x1, Y0 + 33.4, .35)
    xs = [x0, x0 + 30, x0 + 52, x1]
    for xx in xs[1:-1]: vl(xx, Y0 + 33.4, Y1)
    for i, (h_, v_) in enumerate((("No. gambar", DWG_NO), ("Rev.", REV), ("Tanggal", DWG_DATE))):
        tc(xs[i] + 1.2, Y0 + 36.6, h_, 1.4); tc((xs[i] + xs[i + 1]) / 2, Y0 + 42.4, v_, 2.1, 'm', True)

if __name__ == "__main__":
    frame(); equipment(); streams(); instruments(); areas(); ribbon()
    d.finalize()
    base = os.path.join(OUT, "PFD_BG-002_Rev3_deck")
    d.pdf(base + ".pdf"); d.svg(base + ".svg"); d.dxf(base + ".dxf")
    iss = d.check(verbose=False)
    print("isu pemeriksa:", len(iss))
    for q in iss[:80]: print("  !", q)
