# -*- coding: utf-8 -*-
"""
PFD A2 - Generator Biogas Modular POME + TKKS (EIC 2026).
Membaca ../process/outputs/results.json (neraca massa dan energi) dan menggambar dengan mesin PFD (eng.py).
Keluaran: outputs/PFD_BG-001_Rev0.pdf, .dxf, .svg
Jalankan: python3 pfd_biogas.py
SUDAH DIGANTI oleh pfd_portable.py (Rev 1). Skrip ini memerlukan results.json Rev 0 dan tidak lagi jalan dengan keluaran Rev 1;
PDF/DXF Rev 0 disimpan di outputs/ sebagai arsip.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eng
from eng import Doc, W, H

# ---- identitas (ISI SESUAI TIM) ------------------------------------------------------------------
TEAM = "NAMA TIM"
UNIV = "UNIVERSITAS"
EVENT = "ASPEBINDO Energy Innovation Strategy Competition (EIC) 2026 - Business Plan Competition"
DWG_NO = "PFD-BG-001, Rev. 0"
DWG_DATE = "15-10-2026"
eng.DOC_TITLE = "PFD Generator Biogas Modular POME-TKKS"
eng.DOC_AUTHOR = TEAM

R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(HERE, "..", "process", "outputs", "portable_modules.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
EQ = R["equipment"]; EN = R["energy"]; NOM = R["nominal"]; STR = {r["id"]: r for r in R["streams"]}
NMOD = EQ["digester_module"]["count"]

d = Doc()
def idn(x, dec=0):
    if abs(x) < 10 ** -dec / 2 and x != 0 or (x == 0): return "–" if x == 0 else ("<0,01" if dec >= 2 else "<1")
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

# =====================================================================================================
# 1. BINGKAI, BLOK JUDUL, GRID
# =====================================================================================================
def frame():
    d.rect(4, 4, W - 8, H - 8, .35, None, 'frame'); d.rect(10, 10, W - 20, H - 20, .7, None, 'frame')
    for i in range(12):
        x0 = 10 + (W - 20) * i / 12; x1 = 10 + (W - 20) * (i + 1) / 12
        if i: d.line([(x0, 4), (x0, 10)], .25, None, '#000000', 'frame'); d.line([(x0, H - 10), (x0, H - 4)], .25, None, '#000000', 'frame')
        d.text((x0 + x1) / 2, 8.2, str(i + 1), 2.0, 'm', False, layer='frame', chk=False); d.text((x0 + x1) / 2, H - 5.6, str(i + 1), 2.0, 'm', False, layer='frame', chk=False)
    for j in range(8):
        y0 = 10 + (H - 20) * j / 8; y1 = 10 + (H - 20) * (j + 1) / 8
        if j: d.line([(4, y0), (10, y0)], .25, None, '#000000', 'frame'); d.line([(W - 10, y0), (W - 4, y0)], .25, None, '#000000', 'frame')
        for xx in (7.2, W - 6.8): d.text(xx, (y0 + y1) / 2 + .7, "ABCDEFGH"[j], 2.0, 'm', False, layer='frame', chk=False)
    # blok judul
    d.line([(10, 32), (W - 10, 32)], .7, None, '#000000', 'frame')
    xa, xb = 130, 470
    d.line([(xa, 10), (xa, 32)], .5, None, '#000000', 'frame'); d.line([(xb, 10), (xb, 32)], .5, None, '#000000', 'frame')
    d.text(70, 17.5, "PROGRAM KOMPETISI", 2.0, 'm', True, layer='frame', chk=False)
    d.text(70, 22.5, EVENT.split(" - ")[0][:44], 1.45, 'm', False, layer='frame', chk=False)
    d.text(70, 27.0, UNIV, 2.0, 'm', True, layer='frame', chk=False)
    d.text((xa + xb) / 2, 19.0, "PROCESS FLOW DIAGRAM", 6.5, 'm', True, layer='frame', chk=False)
    d.text((xa + xb) / 2, 26.0, "GENERATOR BIOGAS MODULAR PORTABEL DARI POME DAN TKKS, 45 t TBS/JAM (PM-A s/d PM-F)", 2.4, 'm', False, layer='frame', chk=False)
    d.text((xa + xb) / 2, 30.0, "Co-digestion POME + TKKS, CSTR mesofilik %d x %d m³, CHP %d x %s kWe" % (NMOD, EQ["digester_module"]["V_liq_m3"], EQ["chp"]["N"], idn(EQ["chp"]["unit_kWe"])), 1.9, 'm', False, layer='frame', chk=False)
    d.text((xb + W - 10) / 2, 17.0, TEAM, 3.0, 'm', True, layer='frame', chk=False)
    d.text((xb + W - 10) / 2, 22.5, "No. Gambar: " + DWG_NO, 2.1, 'm', False, layer='frame', chk=False)
    d.text((xb + W - 10) / 2, 27.5, "Tanggal: " + DWG_DATE + " | A2, tanpa skala", 1.8, 'm', False, layer='frame', chk=False)

# =====================================================================================================
# 2. PERALATAN DAN ALIRAN
# =====================================================================================================
xA, xB, yD, hD, wD = 192, 268, 76, 60, 34          # digester R-201 / R-207
yf, yd, ym = 148, 158, 64                           # header umpan, header digestat, manifold gas
BX = 316                                            # kolom BTF-301

def equipment():
    # ---------------- PM-A / PM-B : persiapan umpan
    d.eq('screen', 'SC-101', 42, 54, 16, 16, 'b', dx=-4, nz={'in': (0, .5, 'L'), 'out': (1, .5, 'R'), 'scr': (.7, 1.09, 'D')})
    d.eq('phx', 'E-101', 78, 56, 18, 12, 'b')
    d.eq('ctank', 'TK-101', 112, 52, 26, 60, 'r', nz={'pome': (0, 1 / 6, 'L'), 'efb': (0, 46 / 60, 'L'), 'out': (.5, 1, 'D')})
    d.eq('shredder', 'SH-101', 40, 90, 20, 16, 'b', nz={'in': (0, .5, 'L'), 'out': (1, .5, 'R')})
    d.eq('conv', 'CV-101', 82, 94, 26, 8, 't')
    d.eq('pump', 'P-201', 115.5, 120, 7, 7, 'l')
    # ---------------- PM-C : bank digester
    for tg, x in (("R-201", xA), ("R-207", xB)):
        d.eq('digester', tg, x, yD, wD, hD, lab=(x + wD / 2, yD + hD + 5.2, 'm'),
             nz={'gas': (.5, 0, 'U'), 'fi': (.3, 1, 'D'), 'do': (.7, 1, 'D'), 'hws': (0, .95, 'L'), 'hwr': (0, .82, 'L')})
    # ---------------- PM-D : gas
    d.eq('column', 'BTF-301', BX, 58, 22, 76, 'b', dx=7, packed=True, nz={'in': (0, .79, 'L'), 'top': (.5, 0, 'U'), 'air': (1, .9, 'R'), 'sl': (.3, 1, 'D')})
    d.eq('phx', 'HX-301', BX + 38, 42, 18, 12, 'b', dx=-8)
    d.eq('comp', 'K-302', BX + 66, 42, 9, 12, 'b')
    d.eq('gasfilter', 'AC-301', BX + 88, 40, 12, 36, 'l', nz={'in': (0, 8 / 36, 'L'), 'out': (.5, 1, 'D'), 'sp': (1, .9, 'R')})
    d.eq('fan', 'K-301', BX + 30, 123, 7, 7, 'b')
    d.eq('flare', 'FL-301', 424, 86, 10, 40, 'b', nz={'in': (0, .25, 'L')})
    # ---------------- PM-F : dosing + dewatering
    d.eq('dtank', 'TK-201', 112, 190, 16, 24, 'b', nz={'out': (1, .875, 'R')})
    d.eq('pump', 'P-203', 136, 208, 6, 6, 'r')
    d.eq('dtank', 'TK-202', 150, 190, 16, 24, 'b', nz={'out': (1, .875, 'R')})
    d.eq('pump', 'P-204', 174, 208, 6, 6, 'r')
    d.eq('spress', 'PR-501', 212, 206, 36, 16, lab=(224, 228, 'r'), nz={'in': (.23, -.15, 'U'), 'poly': (.40, -.15, 'U'), 'cake': (0, .6, 'L'), 'f': (.62, 1.11, 'D')})
    d.eq('pump', 'P-202', 296.5, 178, 7, 7, 'b')
    # ---------------- PM-E : CHP
    d.eq('chp', 'GE-401', 336, 206, 50, 24, lab=(334, 236, 'r'), inner_label=True, nz={'gas': (0, .3, 'L'), 'air': (.72, 0, 'U'), 'ex': (1, .35, 'R'), 'el': (.5, 1, 'D')})
    d.eq('hx', 'HX-401', 398, 236, 36, 14, 'b', nz={'in': (0, .2, 'L'), 'out': (.86, 1, 'D'), 'hws': (0, .75, 'L'), 'hwr': (.3, 1, 'D')})
    d.eq('stack', 'ST-401', 424, 268, 10, 34, 'b', nz={'in': (.5, 0, 'U')})
    # ---------------- utilitas
    d.eq('ct', 'CT-601', 32, 262, 30, 34, 'b', nz={'cwr': (0, .3, 'L'), 'cws': (0, .85, 'L'), 'mk': (1, .8, 'R')})

def streams():
    # --- persiapan umpan
    d.flag("POME dari pabrik", 31, 62, 'r', 'in'); fp = d.flags[-1]
    d.flag("TKKS dari pabrik", 31, 98, 'r', 'in'); fe = d.flags[-1]
    d.flag("Residu saringan", 58, 80, 'r', 'out'); fs = d.flags[-1]
    d.conn('p1', fp, 'SC-101.in', num=1)
    d.conn('p4', 'SC-101.out', 'E-101.l', num=4)
    d.conn('p5', 'E-101.r', 'TK-101.pome', num=5)
    d.conn('p3', 'SC-101.scr', fs, num=3)
    d.conn('p2', fe, 'SH-101.in', num=2)
    d.conn('p6', 'SH-101.out', 'CV-101.l', num=6)
    d.conn('p6b', 'CV-101.r', 'TK-101.efb')
    d.flag("CWS", 79, 43, 'r', 'in', util=True); cws = d.flags[-1]
    d.flag("CWR", 96, 43, 'r', 'out', util=True); cwr = d.flags[-1]
    d.conn('u_cws1', cws, 'E-101.t@0.25', cls='util')
    d.conn('u_cwr1', 'E-101.t@0.8', cwr, cls='util', arrow=False)
    # --- pompa umpan dan header umpan
    d.conn('t_out', 'TK-101.out', 'P-201.t')
    d.conn('hf', 'P-201.r', ('J', xB + .3 * wD, yf), via=['x150', 'y%d' % yf], num=7, dseg=1)
    d.conn('hf1', ('J', xA + .3 * wD, yf), 'R-201.fi')
    d.conn('hf2', ('J', xB + .3 * wD, yf), 'R-207.fi')
    d.junction(xA + .3 * wD, yf); d.junction(xB + .3 * wD, yf)
    d.conn('hd1', 'R-201.do', ('J', xA + .7 * wD, yd))
    d.conn('hd2', 'R-207.do', ('J', xB + .7 * wD, yd))
    d.junction(xA + .7 * wD, yd); d.junction(xB + .7 * wD, yd)
    d.text(247, 99, "R-202 s/d R-206 identik", 1.7, 'm', True); d.text(247, 103, "(7 modul paralel)", 1.7, 'm', False)
    # --- digestat -> P-202 -> PR-501
    d.conn('hd', ('J', xA + .7 * wD, yd), 'P-202.t', pts=[(xA + .7 * wD, yd), (300, yd), (300, 178)], num=10, dseg=0)
    d.conn('pr_in', 'P-202.l', 'PR-501.in')
    d.flag("Kue digestat", 204, 215.6, 'l', 'out'); fk = d.flags[-1]
    d.conn('cake', 'PR-501.cake', fk, num=19)
    d.flag("Filtrat (efluen)", 238, 242, 'r', 'out'); ff = d.flags[-1]
    d.conn('filt', 'PR-501.f', ff, num=20)
    d.flag("Polimer", 230, 194, 'l', 'in'); fpo = d.flags[-1]
    d.conn('poly', fpo, 'PR-501.poly', num=21)
    # --- dosing
    d.conn('n1', 'TK-201.out', 'P-203.l')
    d.conn('n2', 'TK-202.out', 'P-204.l')
    d.conn('n3', 'P-203.t', ('J', 160, yf), via=['y176', 'x160'], num=8, dseg=1)
    d.conn('n4', 'P-204.t', ('J', 168, yf), via=['y184', 'x168'], num=23, dseg=0)
    d.junction(160, yf); d.junction(168, yf)
    # --- gas
    d.conn('g1', 'R-201.gas', 'BTF-301.in', via=['y%d' % ym, 'x308', 'y118'], num=9)
    d.conn('g2', 'R-207.gas', ('J', xB + wD / 2, ym))
    d.junction(xB + wD / 2, ym)
    d.flag("HWS", 176, 76 + .95 * hD, 'r', 'in', util=True); hws = d.flags[-1]
    d.flag("HWR", 176, 76 + .82 * hD, 'l', 'out', util=True); hwr = d.flags[-1]
    d.conn('u_hws', hws, 'R-201.hws', cls='util'); d.conn('u_hwr', 'R-201.hwr', hwr, cls='util')
    d.conn('gt', 'BTF-301.top', 'HX-301.l', via=['y48'], num=12)
    d.conn('gh', 'HX-301.r', 'K-302.l')
    d.conn('gk', 'K-302.r', 'AC-301.in')
    d.flag("Udara", BX + 42, 126.5, 'l', 'in'); fa_ = d.flags[-1]
    d.conn('ga', fa_, 'K-301.r', num=11)
    d.conn('ga2', 'K-301.l', 'BTF-301.air')
    d.flag("Lumpur S / blowdown", BX + 10, 146, 'r', 'out'); fsl = d.flags[-1]
    d.conn('gs', 'BTF-301.sl', fsl, num=13)
    d.flag("Kondensat", BX + 50, 62, 'r', 'out'); fc = d.flags[-1]
    d.conn('gc', 'HX-301.b@0.5', fc, num=14)
    d.flag("CHWS", BX + 38, 37, 'r', 'in', util=True); fch = d.flags[-1]
    d.flag("CHWR", BX + 56, 37, 'r', 'out', util=True); fcr2 = d.flags[-1]
    d.conn('u_ch1', fch, 'HX-301.t@0.2', cls='util'); d.conn('u_ch2', 'HX-301.t@0.8', fcr2, cls='util', arrow=False)
    d.flag("Karbon jenuh", BX + 106, 72.4, 'r', 'out'); fkj = d.flags[-1]
    d.conn('ac_sp', 'AC-301.sp', fkj, num=16)
    # gas bersih -> flare dan CHP
    d.conn('gg', 'AC-301.out', ('J', 410, 96), num=None, pts=[(410, 76), (410, 96)], arrow=False)
    d.junction(410, 96)
    d.conn('gfl', ('J', 410, 96), 'FL-301.in', num=22)
    d.conn('gge', ('J', 410, 96), 'GE-401.gas', via=['x410', 'y186', 'x330'], num=15, dseg=1, dpos=.22)
    d.flag("Udara pembakaran", 366, 196, 'r', 'in'); fac = d.flags[-1]
    d.conn('ch_air', fac, 'GE-401.air', num=17)
    d.conn('ch_ex', 'GE-401.ex', 'HX-401.in')
    d.conn('ch_ex2', 'HX-401.out', 'ST-401.in', num=18)
    d.flag("Listrik %s kWe (bruto)" % idn(EN["P_gross"]), 364, 258, 'r', 'out', util=True); fel = d.flags[-1]
    d.conn('u_el', 'GE-401.el', fel, cls='util', pts=[(361, 230), (361, 258), (364, 258)])
    d.flag("HWS ke digester + pabrik", 392, 246.5, 'l', 'out', util=True); fhs = d.flags[-1]
    d.conn('u_hws2', 'HX-401.hws', fhs, cls='util')
    d.flag("HWR balik", 404, 266, 'r', 'in', util=True); fhr = d.flags[-1]
    d.conn('u_hwr2', fhr, 'HX-401.hwr', cls='util')
    # cooling tower
    d.flag("CWR", 29, 272.2, 'r', 'in', util=True); fcr = d.flags[-1]
    d.flag("CWS", 29, 291.8, 'l', 'out', util=True); fcs = d.flags[-1]
    d.flag("Air make-up", 66, 289, 'l', 'in', util=True); fmk = d.flags[-1]
    d.conn('u_ct1', fcr, 'CT-601.cwr', cls='util'); d.conn('u_ct2', 'CT-601.cws', fcs, cls='util'); d.conn('u_ct3', fmk, 'CT-601.mk', cls='util')

# =====================================================================================================
# 3. INSTRUMENTASI
# =====================================================================================================
LOOPS = [("TIC 101", "Suhu keluar E-101 \u2192 katup CWR (target 39 \u00b0C)"), ("LIC 102", "Level TK-101 \u2192 kecepatan P-201"),
         ("FIC 201", "Laju umpan digester \u2192 kecepatan P-201"), ("TIC 202", "Suhu R-201 (38 \u00b0C) \u2192 katup HWS koil"),
         ("AIC 203", "pH digester (7,0) \u2192 pompa NaOH P-203"), ("AIC 204", "TAN digester (\u2265100 mg N/L) \u2192 pompa urea P-204"),
         ("AIC 302", "H\u2082S keluar BTF \u2192 kipas udara K-301"), ("AIA 303", "H\u2082S gas ke mesin (alarm, trip GE)"),
         ("JIC 401", "Beban mesin \u2192 katup gas ke GE-401/402"), ("FIC 501", "Laju umpan screw press \u2192 kecepatan P-202")]
def sig(key, pts, arrow=True): d.conn(key, None, None, pts=pts, cls='sig', arrow=arrow)

def instruments():
    r = 2.8
    # TIC-101 : katup pada jalur CWR, sensor pada aliran 5
    d.cvalve(92.4, 49.5, vert=True)
    d.inst(107, 50, 'TIC', 101, r)
    sig('s101a', [(107, 52.8), (107, 62)], arrow=False); sig('s101b', [(104.2, 50), (96.0, 50)])
    # LIC-102 -> P-201
    d.inst(153, 66, 'LIC', 102, r)
    sig('s102a', [(150.2, 66), (138, 66)], arrow=False); sig('s102b', [(153, 68.8), (153, 116), (124.5, 116), (124.5, 121.5)])
    # FIC-201 pada jalur keluar P-201
    d.inst(140, 112, 'FIC', 201, r)
    sig('s201a', [(140, 114.8), (140, 123.5)], arrow=False); sig('s201b', [(137.2, 112), (128, 112), (128, 121), (123.0, 121)])
    # TIC-202 : katup HWS koil
    d.cvalve(184, 133, vert=False)
    d.inst(181, 112, 'TIC', 202, r)
    sig('s202a', [(183.8, 112), (192, 112)], arrow=False); sig('s202b', [(181, 114.8), (181, 128), (184, 128), (184, 129.6)])
    # AIC-203 / AIC-204 (dekat pompa dosing)
    d.inst(124, 226, 'AIC', 203, r); d.text(124, 232.5, "pH R-201", 1.5, 'm', False)
    sig('s203', [(126.8, 226), (139, 226), (139, 214.4)])
    d.inst(162, 226, 'AIC', 204, r); d.text(162, 232.5, "TAN R-201", 1.5, 'm', False)
    sig('s204', [(164.8, 226), (177, 226), (177, 214.4)])
    # AIC-302 : H2S keluar BTF -> K-301
    d.inst(343, 62, 'AIC', 302, r)
    sig('s302a', [(343, 59.2), (343, 48)], arrow=False); sig('s302b', [(343, 64.8), (343, 119), (349.5, 119), (349.5, 123.4)])
    # AIA-303 alarm H2S gas mesin
    d.inst(402, 140, 'AIA', 303, r)
    sig('s303', [(404.8, 140), (410, 140)], arrow=False)
    # JIC-401 : katup gas
    d.cvalve(355, 186, vert=False)
    d.inst(355, 172, 'JIC', 401, r)
    sig('s401', [(355, 174.8), (355, 182.4)])
    # FIC-501 : umpan screw press
    d.inst(310, 168, 'FIC', 501, r)
    sig('s501a', [(307.2, 168), (300, 168)], arrow=False); sig('s501b', [(310, 170.8), (310, 181.5), (303.8, 181.5)])

# =====================================================================================================
# 4. BATAS MODUL PORTABEL
# =====================================================================================================
def modules():
    dash = [3.0, 1.6]; lw = .4
    def box(x0, y0, x1, y1, label, lx, ly, anchor='l'):
        d.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], lw, None, '#000000', 'frame', dash)
        d.text(lx, ly, label, 1.7, anchor, True, layer='label', chk=False)
    d.poly([(34, 46), (76, 46), (76, 84), (110, 84), (110, 110), (34, 110)], lw, None, '#000000', 'frame', dash)
    d.text(35, 49.4, "PM-A  SKID PERSIAPAN UMPAN", 1.7, 'l', True, chk=False)
    box(77, 49, 99, 79, "PM-B", 79, 77.6)
    box(24, 252, 96, 306, "PM-B  MENARA PENDINGIN MODULAR", 26, 255.2)
    for x in (xA, xB):
        box(x - 7, 73, x + wD + 7, 146, "PM-C", x - 6, 71.0)
    d.text(xA + wD / 2 + 8, 71.0, "MODUL DIGESTER 2.000 m\u00b3 (\u00d77)", 1.7, 'l', True, chk=False)
    box(312, 37, 420, 152, "PM-D  SKID PENGOLAHAN GAS", 314, 40.5)
    box(421, 78, 438, 131, "PM-D2", 422, 76.2)
    box(108, 170, 186, 236, "PM-F  SKID DOSING", 110, 173.5)
    box(194, 186, 312, 252, "PM-F  SKID DEWATERING", 196, 189.5)
    box(322, 190, 440, 306, "PM-E  KONTAINER CHP (\u00d72)", 324, 193.5)
    d.text(334, 241, "GE-402 identik (2 unit)", 1.7, 'r', False, chk=False)

# =====================================================================================================
# 5. PANEL KANAN: LEGENDA, DAFTAR PERALATAN, CATATAN, LOOP
# =====================================================================================================
PX, PW = 446, 138
def tcell(x, y, t, size=1.45, anchor='l', bold=False):
    d.text(x, y, t, size, anchor, bold, layer='table', chk=False)
def panels():
    d.rect(PX, 36, PW, 62, .5, None, 'table'); d.rect(PX, 36, PW, 4.4, .5, '#e6e6e6', 'table'); tcell(PX + PW / 2, 39.4, "LEGENDA", 2.0, 'm', True)
    y = 45.5; xs = PX + 2
    def row(label, drawfn, y):
        drawfn(xs, y); tcell(xs + 24, y + .55, label, 1.45)
    row("Aliran material (bernomor)", lambda x, y: d.line([(x, y), (x + 20, y)], .5, None, '#000000', 'table'), y); y += 4.9
    row("Aliran utilitas: HW/HWS/HWR air panas, CW/CHW air pendingin, listrik", lambda x, y: d.line([(x, y), (x + 20, y)], .26, None, '#505050', 'table'), y); y += 4.9
    row("Sinyal instrumen", lambda x, y: d.line([(x, y), (x + 20, y)], .18, [.9, .6], '#000000', 'table'), y); y += 4.9
    def dia(x, y): r = 2.15; d.poly([(x + 10, y - r), (x + 10 + r, y), (x + 10, y + r), (x + 10 - r, y)], .3, '#ffffff', '#000000', 'table'); tcell(x + 10, y + .5, "12", 1.5, 'm', True)
    row("Nomor aliran material (lihat tabel aliran)", dia, y); y += 5.2
    def bub(x, y): d.circ(x + 10, y, 2.8, .28, '#ffffff', 'table'); tcell(x + 10, y - .2, "TIC", 1.5, 'm', True); tcell(x + 10, y + 1.5, "101", 1.5, 'm')
    row("Gelembung instrumen: huruf fungsi (ISA-5.1) + nomor loop", bub, y); y += 5.6
    def cv(x, y): Sym_valve(x + 10, y)
    row("Katup kendali dengan aktuator", cv, y); y += 4.6
    def flg(x, y):
        pts = [(x + 4, y - 1.8), (x + 16, y - 1.8), (x + 18, y), (x + 16, y + 1.8), (x + 4, y + 1.8)]; d.poly(pts, .3, '#ffffff', '#000000', 'table')
    row("Bendera batas baterai (masuk / keluar)", flg, y); y += 4.8
    row("Batas modul portabel (PM-A s/d PM-F)", lambda x, y: d.line([(x, y), (x + 20, y)], .4, [3.0, 1.6], '#000000', 'table'), y); y += 4.2
    tcell(xs, y + .4, "Huruf instrumen: F laju, L level, P tekanan, T suhu, A analisis, W berat, J daya; I indikasi, C pengendali, A alarm.", 1.3)
    tcell(xs, y + 3.4, "Fasa: C cair, G gas, P padat, PB padat basah, B bubur, CP cair-padat.", 1.3)
    # daftar peralatan
    top = 100; rows = EQUIP
    h_row = 2.72; h = 4.4 + h_row * len(rows) + 1
    d.rect(PX, top, PW, h, .5, None, 'table'); d.rect(PX, top, PW, 4.4, .5, '#e6e6e6', 'table'); tcell(PX + PW / 2, top + 3.3, "DAFTAR PERALATAN", 2.0, 'm', True)
    yy = top + 4.4 + 2.2
    for kind, a, b in rows:
        if kind == 'g':
            d.rect(PX, yy - 2.0, PW, h_row, .15, '#f2f2f2', 'table'); tcell(PX + 2, yy, a, 1.45, 'l', True)
        else:
            tcell(PX + 2, yy, a, 1.4, 'l', True); tcell(PX + 22, yy, b, 1.4)
        yy += h_row
    return top + h
def Sym_valve(x, y):
    eng.Sym.valve(d, x, y, False, 'table', 1.5); d.line([(x, y - .75), (x, y - 2.2)], .22, None, '#000000', 'table'); d.poly(d.arcpts(x, y - 2.2, 1.2, 1.2, 0, 180), .22, '#ffffff', '#000000', 'table')

EQUIP = [
 ('g', "PM-A  SKID PERSIAPAN UMPAN", ""), ('e', "SC-101", "Saringan halus putar (rotary screen) POME"), ('e', "SH-101", "Penghancur TKKS (hammer mill), produk 10 mm, %.0f kW" % EQ["efb_shredder"]["power_kW"]), ('e', "CV-101", "Konveyor TKKS"),
 ('g', "PM-B  SKID PENDINGIN POME", ""), ('e', "E-101", "Pendingin pelat POME, %s kWth (85 \u2192 %.0f \u00b0C)" % (idn(EQ["pome_cooler"]["duty_kW"]), EQ["pome_cooler"]["T_out"])), ('e', "CT-601", "Menara pendingin modular, %s kWth" % idn(EQ["cooling_tower"]["duty_kW"])),
 ('g', "TANGKI LAPANGAN (flat-pack)", ""), ('e', "TK-101", "Tangki campur / penyangga, %s m\u00b3 (4 jam)" % idn(EQ["blend_tank"]["V_m3"])), ('e', "P-201 A-H", "Pompa umpan digester (7+1), %s m\u00b3/jam total" % idn(EQ["feed_pump"]["flow_m3_h"], 1)),
 ('g', "PM-C  KIT MODUL DIGESTER (\u00d7%d)" % NMOD, ""), ('e', "R-201..R-20%d" % NMOD, "Digester CSTR 38 \u00b0C, %s m\u00b3, \u00d8%s m, atap membran ganda" % (idn(EQ["digester_module"]["V_liq_m3"]), idn(EQ["digester_module"]["D_m"], 1))), ('e', "MX-201..", "Mixer samping, 2 per modul (%.0f kW/modul)" % EQ["digester_module"]["mixer_kW"]),
 ('g', "PM-D  SKID PENGOLAHAN GAS", ""), ('e', "BTF-301", "Filter trickling biologis (desulfurisasi), %.0f m\u00b3 media" % EQ["bio_desulfurizer"]["V_m3"]), ('e', "K-301", "Kipas udara BTF, %s Nm\u00b3/jam" % idn(EQ["bio_desulfurizer"]["air_Nm3_h"], 1)),
 ('e', "HX-301", "Chiller gas, %s kWth, titik embun 5 \u00b0C" % idn(EQ["gas_chiller"]["duty_kW"])), ('e', "K-302", "Blower biogas, %s m\u00b3/jam, %.0f kPa" % (idn(EQ["gas_blower"]["flow_m3_h"]), EQ["gas_blower"]["dP_kPa"])),
 ('e', "AC-301", "Filter karbon aktif (poles H\u2082S)"), ('e', "FL-301", "Flare tertutup, %s Nm\u00b3/jam (PM-D2)" % idn(EQ["flare"]["cap_Nm3_h"])),
 ('g', "PM-E  KONTAINER CHP (\u00d7%d)" % EQ["chp"]["N"], ""), ('e', "GE-401/402", "Genset biogas %s kWe, kontainer 40 ft" % idn(EQ["chp"]["unit_kWe"])), ('e', "HX-401", "Pemulih panas (jaket + gas buang) \u2192 air panas"), ('e', "ST-401", "Cerobong gas buang"),
 ('g', "PM-F  SKID DEWATERING DAN DOSING", ""), ('e', "P-202", "Pompa digestat"), ('e', "PR-501", "Screw press, %s m\u00b3/jam, kue 22 %% DS" % idn(EQ["screw_press"]["feed_m3_h"], 1)),
 ('e', "TK-201/P-203", "Tangki + pompa NaOH (P95 %s kg/hari)" % idn(EQ["alkali_dosing"]["NaOH_kg_d_P95"])), ('e', "TK-202/P-204", "Tangki + pompa urea-N (P95 %s kg N/hari)" % idn(EQ["nutrient_dosing"]["N_kg_d_P95"])),
]

def notes(y0):
    h = 41
    d.rect(PX, y0 + 1.5, PW, h, .5, None, 'table'); d.rect(PX, y0 + 1.5, PW, 4.4, .5, '#e6e6e6', 'table'); tcell(PX + PW / 2, y0 + 4.8, "CATATAN", 2.0, 'm', True)
    N_ = ["1. Laju aliran dalam kg/jam pada titik rancangan: 45 t TBS/jam x 20 jam/hari, beban 100 %%, %.0f hari/tahun (hasil biogas_balance.py)." % R["design_basis"]["days_yr"],
          "2. Tekanan dalam bar absolut dan suhu dalam \u00b0C. Komposisi per kelompok senyawa; CO\u2082, H\u2082O, NH\u2083 dan sulfat dari neraca unsur.",
          "3. R-201 s/d R-207 identik (7 modul paralel, digambar 2); GE-401/402 identik (2 unit, digambar 1).",
          "4. Pompa transfer kecil, katup manual, dan instrumen lokal tidak digambar. Aliran 22 (flare) nol pada operasi normal.",
          "5. Garis putus-putus tebal = batas modul portabel (kontainer ISO / skid); digester dikirim sebagai kit panel baja berbaut.",
          "6. Aliran 8 (NaOH) dan 23 (urea-N) ditunjukkan pada rata-rata P50; kebutuhan P95 ada pada daftar peralatan.",
          "7. Ketidakpastian: Monte Carlo 400 sampel \u2014 daya bersih P5/P50/P95 = %s / %s / %s kWe." % (idn(R["monte_carlo"]["P_net"]["P5"]), idn(R["monte_carlo"]["P_net"]["P50"]), idn(R["monte_carlo"]["P_net"]["P95"]))]
    yy = y0 + 9.5
    for t in N_:
        words = t.split(); line = ""; 
        for w_ in words:
            if eng.twidth(line + " " + w_, 1.4) > PW - 4: tcell(PX + 2, yy, line.strip(), 1.4); yy += 2.9; line = "   " + w_
            else: line += " " + w_
        tcell(PX + 2, yy, line.strip(), 1.4); yy += 3.2
    return y0 + 1.5 + h

def loops(y0):
    n = len(LOOPS); h = 4.4 + 2.8 * n + 1.6
    d.rect(PX, y0 + 1.5, PW, h, .5, None, 'table'); d.rect(PX, y0 + 1.5, PW, 4.4, .5, '#e6e6e6', 'table'); tcell(PX + PW / 2, y0 + 4.8, "LOOP KONTROL UTAMA", 2.0, 'm', True)
    yy = y0 + 9.4
    for c, f in LOOPS:
        tcell(PX + 2, yy, c, 1.4, 'l', True); tcell(PX + 20, yy, f, 1.4); yy += 2.8

# =====================================================================================================
# 6. TABEL ALIRAN
# =====================================================================================================
SHORT = {1: "POME mentah", 2: "TKKS ke digester", 3: "Residu saringan", 4: "POME tersaring", 5: "POME dingin", 6: "TKKS cacah", 7: "Umpan campur", 8: "Larutan NaOH",
         9: "Biogas mentah", 10: "Digestat", 11: "Udara BTF", 12: "Biogas setelah BTF", 13: "Lumpur S / blowdown", 14: "Kondensat", 15: "Biogas bersih ke CHP",
         16: "Karbon jenuh", 17: "Udara bakar CHP", 18: "Gas buang CHP", 19: "Kue digestat", 20: "Filtrat", 21: "Polimer", 22: "Gas ke flare", 23: "Urea-N"}
GL = dict(water="Air", carb="Karbohidrat partikulat", lignin="Lignin dan residu", protbio="Protein dan biomassa", lipid="Minyak/lemak, LCFA", solorg="Organik terlarut",
          inertp="Inert partikulat", mineral="Mineral dan garam", tan="Amonium (sbg NH\u2083)", sulf="Sulfat dan sulfida", ic="Karbon anorganik (CO\u2082)", dgas="CH\u2084/H\u2082 terlarut",
          g_ch4="CH\u2084", g_co2="CO\u2082", g_h2="H\u2082", g_h2s="H\u2082S", g_h2o="Uap air", g_n2="N\u2082 (+Ar)", g_o2="O\u2082", g_so2="SO\u2082", sulfur="Belerang (S)", chem="Bahan kimia")
def wrap2(t, wmax, size):
    if eng.twidth(t, size) <= wmax: return [t]
    w = t.split(); a = ""
    for i, x in enumerate(w):
        if eng.twidth((a + " " + x).strip(), size) > wmax: return [a.strip(), " ".join(w[i:])]
        a += " " + x
    return [a.strip()]
def table(y0):
    ids = sorted(STR); keys = [k for k in eng.__dict__.get('GRP_ORDER', []) ]
    order = ["water", "carb", "lignin", "protbio", "lipid", "solorg", "inertp", "mineral", "tan", "sulf", "ic", "dgas", "g_ch4", "g_co2", "g_h2", "g_h2s", "g_h2o", "g_n2", "g_o2", "g_so2", "sulfur", "chem"]
    rows = [k for k in order if any(STR[i]["comp"].get(k, 0) > 1e-9 for i in ids)]
    x0 = 10; lw_ = 50; cw = (W - 20 - lw_) / len(ids)
    hh = 3.2; hn = 6.4; hr = 2.55
    H_ = hh + hn + 4 * hr + len(rows) * hr + 4.6
    d.rect(x0, y0, W - 20, H_, .5, None, 'table')
    d.rect(x0, y0, W - 20, 4.4, .5, '#e6e6e6', 'table'); tcell(W / 2, y0 + 3.3, "TABEL ALIRAN MATERIAL (LAJU MASSA DALAM kg/jam, TITIK RANCANGAN)", 2.0, 'm', True)
    yy = y0 + 4.4
    def hline(y, w=.18): d.line([(x0, y), (W - 10, y)], w, None, '#000000', 'table')
    d.line([(x0 + lw_, y0 + 4.4), (x0 + lw_, y0 + H_)], .3, None, '#000000', 'table')
    for k in range(1, len(ids)): d.line([(x0 + lw_ + cw * k, y0 + 4.4), (x0 + lw_ + cw * k, y0 + H_)], .12, None, '#000000', 'table')
    tcell(x0 + 1.5, yy + 2.3, "No. Aliran", 1.5, 'l', True)
    for k, i in enumerate(ids): tcell(x0 + lw_ + cw * (k + .5), yy + 2.3, str(i), 1.7, 'm', True)
    yy += hh; hline(yy, .3)
    tcell(x0 + 1.5, yy + 2.6, "Nama aliran", 1.45, 'l', True)
    for k, i in enumerate(ids):
        L = wrap2(SHORT[i], cw - 1.2, 1.2)
        for q, ln in enumerate(L): tcell(x0 + lw_ + cw * (k + .5), yy + 2.4 + q * 2.4, ln, 1.2, 'm')
    yy += hn; hline(yy, .3)
    for lab, f in (("Fasa", lambda r_: r_["ph"]), ("Suhu (\u00b0C)", lambda r_: idn(r_["T"], 0)), ("Tekanan (bar)", lambda r_: idn(r_["P"], 2)), ("Laju total (kg/jam)", lambda r_: idn(r_["kg_h"], 0))):
        tcell(x0 + 1.5, yy + 1.8, lab, 1.45, 'l', True)
        for k, i in enumerate(ids): tcell(x0 + lw_ + cw * (k + .5), yy + 1.8, f(STR[i]), 1.4, 'm', lab.startswith("Laju"))
        yy += hr
    hline(yy, .3)
    for key in rows:
        tcell(x0 + 1.5, yy + 1.8, GL[key], 1.4, 'l')
        for k, i in enumerate(ids):
            v = STR[i]["comp"].get(key, 0.0)
            tcell(x0 + lw_ + cw * (k + .5), yy + 1.8, "\u2013" if v < 1e-9 else ("<0,1" if v < 0.05 else idn(v, 1 if v < 100 else 0)), 1.35, 'm')
        yy += hr
    hline(yy, .3)
    tcell(x0 + 1.5, yy + 2.6, "Neraca massa total pabrik: masuk %s kg/hari, keluar %s kg/hari; galat relatif %s" % (idn(R["closure"]["plant_mass"] * 0 + sum(STR[i]["kg_h"] for i in (1, 2, 8, 11, 17, 21, 23)) * 24), idn(sum(STR[i]["kg_h"] for i in (3, 13, 14, 16, 18, 19, 20, 22)) * 24), "%.1e" % abs(R["closure"]["plant_mass"])), 1.4, 'l', True)

# =====================================================================================================
if __name__ == "__main__":
    frame(); equipment(); streams(); instruments(); modules()
    yb = panels(); yb = notes(yb); loops(yb)
    table(322)
    d.finalize()
    d.pdf(os.path.join(OUT, "PFD_BG-001_Rev0.pdf")); d.svg(os.path.join(OUT, "PFD_BG-001_Rev0.svg")); d.dxf(os.path.join(OUT, "PFD_BG-001_Rev0.dxf"))
    iss = d.check()
    print("isu pemeriksa:", len(iss))
