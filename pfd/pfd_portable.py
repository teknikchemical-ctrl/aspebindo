# -*- coding: utf-8 -*-
"""
PFD A2 Rev 1 - Generator Biogas Portabel: AnMBR termofilik POME (EIC 2026).
Membaca ../process/outputs/results.json + portable_modules.json, menggambar dengan eng.py.
Gaya EPC: callout peralatan di atas, tag aliran (No / T / P), loop kendali ISA-5.1 (LIC pada setiap bejana),
batas modul portabel PM-1..PM-10, tanpa tabel neraca massa (lihat biogas_balance.py / results.json).
Keluaran: outputs/PFD_BG-002_Rev1.pdf, .dxf, .svg
Acuan gambar: ISO 10628-1/-2 (simbol diagram alir), ISA-5.1-2022 (identifikasi instrumen), PIP PIC001 (kriteria P&ID/PFD),
ISO 7200 (blok judul). Jalankan: python3 pfd_portable.py
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eng
from eng import Doc, W, H

TEAM = "NAMA TIM"
UNIV = "UNIVERSITAS"
EVENT = "ASPEBINDO EIC 2026 - Business Plan Competition"
DWG_NO = "PFD-BG-002"
REV = "1"
DWG_DATE = "15-10-2026"
eng.DOC_TITLE = "PFD Generator Biogas Portabel AnMBR Termofilik"
eng.DOC_AUTHOR = TEAM

R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(HERE, "..", "process", "outputs", "portable_modules.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
EQ = R["equipment"]; EN = R["energy"]; NOM = R["nominal"]; STR = {r["id"]: r for r in R["streams"]}
RV = EQ["reactor_vessel"]; NR = RV["count"]; MB = EQ["membrane"]
d = Doc()

def idn(x, dec=0):
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
def sig(key, pts): d.conn(key, None, None, pts=pts, cls='sig', arrow=False)
def stag(num, x, y, side='t', lead=2.4):
    s = STR[num]
    d.stag(x, y, num, "%s °C" % idn(s["T"]), "%s bar" % idn(s["P"], 2 if s["P"] < 1.1 else 1), side, lead)
def flag(text, x, y, dr='r', kind='in', util=False): return d.flag(text, x, y, dr, kind, util=util)

# =====================================================================================================
# 1. BINGKAI + BLOK JUDUL (ISO 7200, kanan bawah)
# =====================================================================================================
PX = 470; PW = W - 10 - PX            # panel kanan
def frame():
    d.rect(4, 4, W - 8, H - 8, .35, None, 'frame'); d.rect(10, 10, W - 20, H - 20, .7, None, 'frame')
    for i in range(12):
        x0 = 10 + (W - 20) * i / 12; x1 = 10 + (W - 20) * (i + 1) / 12
        if i: d.line([(x0, 4), (x0, 10)], .25, None, '#000000', 'frame'); d.line([(x0, H - 10), (x0, H - 4)], .25, None, '#000000', 'frame')
        for yy in (8.2, H - 5.6): d.text((x0 + x1) / 2, yy, str(i + 1), 2.0, 'm', False, layer='frame', chk=False)
    for j in range(8):
        y0 = 10 + (H - 20) * j / 8; y1 = 10 + (H - 20) * (j + 1) / 8
        if j: d.line([(4, y0), (10, y0)], .25, None, '#000000', 'frame'); d.line([(W - 10, y0), (W - 4, y0)], .25, None, '#000000', 'frame')
        for xx in (7.2, W - 6.8): d.text(xx, (y0 + y1) / 2 + .7, "ABCDEFGH"[j], 2.0, 'm', False, layer='frame', chk=False)
    d.line([(PX, 10), (PX, H - 10)], .7, None, '#000000', 'frame')
    # blok judul
    yt = 352
    L = lambda pts, w=.35: d.line(pts, w, None, '#000000', 'frame')
    L([(PX, yt), (W - 10, yt)], .7)
    rows = [yt + 9, yt + 17, yt + 33, yt + 41, yt + 49]
    for y in rows: L([(PX, y), (W - 10, y)])
    T = lambda x, y, t, s=1.6, a='l', b=False: d.text(x, y, t, s, a, b, layer='frame', chk=False)
    T(PX + PW / 2, yt + 4.2, TEAM, 3.0, 'm', True); T(PX + PW / 2, yt + 7.6, UNIV, 1.8, 'm', False)
    T(PX + 2, yt + 12.0, "KOMPETISI", 1.3); T(PX + PW / 2, yt + 15.3, EVENT, 1.55, 'm', True)
    T(PX + PW / 2, yt + 22.0, "PROCESS FLOW DIAGRAM", 3.6, 'm', True)
    T(PX + PW / 2, yt + 26.6, "GENERATOR BIOGAS PORTABEL - AnMBR TERMOFILIK POME", 1.9, 'm', True)
    T(PX + PW / 2, yt + 30.6, "PKS 45 t TBS/jam (set 30 / 45 / 60 t TBS/jam)", 1.7, 'm', False)
    xs = [PX, PX + 40, PX + 70, PX + 92, W - 10]
    for x in xs[1:-1]: L([(x, yt + 33), (x, yt + 49)])
    hdr = ["No. Gambar", "Tanggal", "Rev.", "Lembar / Skala"]; val = [DWG_NO, DWG_DATE, REV, "1/1  -  NTS, A2"]
    for i in range(4):
        T(xs[i] + 1.5, yt + 35.8, hdr[i], 1.25); T((xs[i] + xs[i + 1]) / 2, yt + 39.8, val[i], 1.9, 'm', True)
    T(xs[0] + 1.5, yt + 43.8, "Disusun", 1.25); T(xs[0] + 1.5, yt + 47.6, "Tim (dengan bantuan alat AI)", 1.45)
    T(xs[1] + 1.5, yt + 43.8, "Diperiksa", 1.25); T(xs[2] + 1.5, yt + 43.8, "Disetujui", 1.25); T(xs[3] + 1.5, yt + 43.8, "Status", 1.25)
    T(xs[3] + 1.5, yt + 47.6, "UNTUK KOMPETISI", 1.45, 'l', True)
    T(PX + 1.5, yt + 53.0, "Rev 0: CSTR mesofilik POME+TKKS (PFD-BG-001). Rev 1: AnMBR 55 °C portabel, TKKS dikeluarkan.", 1.25)

# =====================================================================================================
# 2. CALLOUT PERALATAN (pita atas, gaya EPC)
# =====================================================================================================
CALL = [
 ("SC-101", "SARINGAN PUTAR", ["%s m³/jam, celah 0,75 mm" % idn(EQ["screen"]["flow_m3h"], 1), "%.0f kW, SS316" % R["EQ"]["screen_kW"]]),
 ("P-101", "POMPA DESANDER", ["%s m³/jam, H %.0f m" % (idn(EQ["desander"]["flow_m3h"], 1), R["EQ"]["H_desander"]), "sentrifugal, VSD"]),
 ("HC-101", "HIDROSIKLON DESANDER", ["%s m³/jam, η pasir %.0f %%" % (idn(EQ["desander"]["flow_m3h"], 1), EQ["desander"]["grit_removal"] * 100), "poliuretan, d50 75 µm"]),
 ("E-101", "PENDINGIN POME (PHE)", ["%s kWth" % idn(EQ["pome_cooler"]["duty_kW"]), "85 → %s °C, SS316" % idn(EQ["pome_cooler"]["T_out"])]),
 ("TK-101", "TANGKI PENYANGGA UMPAN", ["Ø%s × %s m, %s m³" % (idn(RV["D_m"], 1), idn(RV["H_shell_m"], 1), idn(RV["V_liq_m3"])), "bejana standar, CS+epoksi"]),
 ("P-201 A/B", "POMPA UMPAN REAKTOR", ["%s m³/jam, H %.0f m" % (idn(EQ["feed_pump"]["flow_m3_h"], 1), R["EQ"]["H_feed"]), "%s kW, 1+1, VSD" % idn(EQ["feed_pump"]["kW"], 1)]),
 ("R-201..R-2%02d" % NR, "REAKTOR AnMBR 55 °C", ["%d × %s m³, Ø%s × %s m" % (NR, idn(RV["V_liq_m3"]), idn(RV["D_m"], 1), idn(RV["H_shell_m"], 1)), "HRT %s d / SRT %.0f d" % (idn(RV["hrt_d"], 1), RV["srt_d"])]),
 ("P-202", "POMPA JET MIXING", ["1 per reaktor, %s kW" % idn(RV["mixer_kW"], 1), "%.0f W/m³, nosel jet" % R["EQ"]["mix_W_m3_T"]]),
 ("TK-201/P-203", "DOSING NaOH 30 %", ["P95 %s kg/hari NaOH" % idn(EQ["alkali_dosing"]["NaOH_kg_d_P95"]), "tangki 2 m³ + pompa dosis"]),
 ("TK-202/P-204", "DOSING UREA-N", ["P95 %s kg N/hari" % idn(EQ["nutrient_dosing"]["N_kg_d_P95"]), "tangki 2 m³ + pompa dosis"]),
 ("P-301 A/B", "POMPA CROSS-FLOW", ["%s m³/jam, H 40 m" % idn(MB["loop_m3h"]), "1+1, VSD"]),
 ("MB-301", "MEMBRAN UF TUBULAR", ["%s m², %d modul, %.0f LMH" % (idn(MB["area_m2"]), MB["modules"], MB["flux"]), "%s kWe, 1 kontainer 40 ft" % idn(MB["kW"])]),
 ("P-302", "POMPA PERMEAT", ["%s m³/jam" % idn(MB["Q_perm"] / 24, 1), "vakum ringan, VSD"]),
 ("TK-302", "TANGKI CIP", ["4 m³, NaOCl / asam sitrat", "pemanas listrik 40 °C"]),
 ("P-303", "POMPA LUMPUR BUANGAN", ["%s m³/hari (SRT %.0f d)" % (idn(EQ["waste_sludge"]["Qw_m3d"]), RV["srt_d"]), "progressive cavity"]),
 ("PR-501", "SCREW PRESS", ["kue %s t/hari, 20 %% DS" % idn(EQ["waste_sludge"]["cake_t_d"], 1), "dengan dosis polimer"]),
 ("TK-301", "TANGKI PERMEAT", ["Ø%s × %s m (bejana standar)" % (idn(RV["D_m"], 1), idn(RV["H_shell_m"], 1)), "hold-up %.0f jam" % EQ["permeate_tank"]["hold_h"]]),
 ("P-501", "POMPA EFLUEN", ["%s m³/jam" % idn((MB["Q_perm"] + EQ["waste_sludge"]["Qw_m3d"] * .9) / 24, 1), "ke kolam polishing"]),
 ("GH-301", "PENAMPUNG GAS", ["%s m³, membran ganda" % idn(EQ["gas_holder"]["V_m3"]), "%.0f jam @ P95, 2-3 mbar" % EQ["gas_holder"]["hours"]]),
 ("BTF-301", "BIO-TRICKLING FILTER", ["%s m³ media, η H₂S %.0f %%" % (idn(EQ["bio_desulfurizer"]["V_m3"], 1), EQ["bio_desulfurizer"]["eff"] * 100), "%s Nm³/jam biogas" % idn(EQ["bio_desulfurizer"]["gas_Nm3_h"])]),
 ("K-301", "BLOWER UDARA BTF", ["%s Nm³/jam" % idn(EQ["bio_desulfurizer"]["air_Nm3_h"], 1), "O₂ ≤ 1 %-vol"]),
 ("HX-301/V-301", "CHILLER GAS + KO POT", ["%s kWth, embun 5 °C" % idn(EQ["gas_chiller"]["duty_kW"], 1), "chiller paket R-134a"]),
 ("K-302 A/B", "BLOWER BIOGAS", ["%s m³/jam, ΔP %.0f kPa" % (idn(EQ["gas_blower"]["flow_m3_h"]), EQ["gas_blower"]["dP_kPa"]), "%s kW, ATEX, 1+1" % idn(EQ["gas_blower"]["kW"], 1)]),
 ("AC-301", "FILTER KARBON AKTIF", ["poles H₂S → %s ppm" % idn(NOM["h2s_ppm_fuel"]), "KI-impregnated, 2 bed"]),
 ("FL-301", "FLARE TERTUTUP", ["%s Nm³/jam" % idn(EQ["flare"]["cap_Nm3_h"]), "enclosed, ≥ 1000 °C"]),
 ("GE-401/402", "GENSET BIOGAS", ["%d × %s kWe, ηel %s %%" % (EQ["chp"]["N"], idn(EQ["chp"]["unit_kWe"]), idn(EQ["chp"]["eta_el_nom"] * 100, 1)), "kontainer 40 ft HC"]),
 ("HX-401", "PEMULIH PANAS", ["%s kWth air panas" % idn(EN["Q_heat_avail"]), "jaket + gas buang"]),
 ("CT-601", "MENARA PENDINGIN", ["%s kWth, sel modular" % idn(EQ["cooling_tower"]["duty_kW"]), "CWS 30 / CWR 40 °C"]),
]
def callouts():
    n = len(CALL); per = (n + 1) // 2
    x0, x1, y0 = 12, PX - 2, 12
    cw = (x1 - x0) / per
    for k, (tg, nm, dat) in enumerate(CALL):
        r, c = divmod(k, per)
        x = x0 + c * cw + 1.0; y = y0 + r * 19.5
        tw = eng.twidth(tg, 1.75, True)
        d.text(x, y + 2.6, tg, 1.75, 'l', True, layer='table', chk=False)
        d.line([(x, y + 3.3), (x + tw, y + 3.3)], .22, None, '#000000', 'table')
        d.text(x, y + 6.2, nm, 1.3, 'l', True, layer='table', chk=False)
        for i, t in enumerate(dat): d.text(x, y + 9.2 + 2.6 * i, t, 1.25, 'l', False, layer='table', chk=False)
    d.line([(10, 52), (PX, 52)], .5, None, '#000000', 'frame')

# =====================================================================================================
# 3. PERALATAN
# =====================================================================================================
RX1, RX2, RY, RW, RH = 166, 222, 166, 18, 64        # reaktor R-201 dan R-2NN (digambar 2 dari NR)
RT = 'R-2%02d' % NR
YF = 252                                            # header umpan reaktor
YG = 148                                            # header biogas
def equipment():
    # ---- PM-1 skid praolah
    d.eq('screen', 'SC-101', 36, 179, 18, 13, lab=(45, 175.5, 'm'), nz={'in': (0, .52, 'L'), 'out': (1, .77, 'R'), 'scr': (.7, 1.11, 'D')})
    d.eq('pump', 'P-101', 60, 196, 6, 6, lab=(63, 208.6, 'm'))
    d.eq('hcyc', 'HC-101', 74, 170, 10, 24, lab=(72.5, 187, 'r'), nz={'in': (0, .12, 'L'), 'of': (.68, -.05, 'U'), 'uf': (.5, 1, 'D')})
    d.eq('phx', 'E-101', 92, 168, 16, 10, lab=(90.5, 182.5, 'r'))
    # ---- PM-2 tangki penyangga (bejana standar)
    d.eq('vessel', 'TK-101', 120, RY, 16, RH, lab=(128, RY - 2.2, 'm'), nz={'in': (0, 7 / 64, 'L'), 'out': (.5, 1, 'D')})
    d.eq('pump', 'P-201', 139, YF + 6, 7, 7, lab=(142.5, YF + 18.6, 'm'))
    # ---- PM-3 reaktor
    for tg, x in (("R-201", RX1), (RT, RX2)):
        d.eq('reactor', tg, x, RY, RW, RH, lab=(x + RW / 2, RY + RH + 9.0, 'm'),
             nz={'gas': (.5, 0, 'U'), 'fd': (.3, 1, 'D'), 'js': (.75, 1, 'D'), 'jr': (1, .86, 'R'), 'mo': (1, .74, 'R'), 'ret': (1, .40, 'R'), 'ws': (.75, 1, 'D')})
    d.eq('pump', 'P-202', 194, 234, 6, 6, lab=(197, 246.6, 'm'))
    # ---- PM-5 skid dosing
    d.eq('dtank', 'TK-201', 112, 290, 12, 18, lab=(118, 313.5, 'm'), nz={'out': (1, 2 / 3, 'R')})
    d.eq('pump', 'P-203', 130, 299, 6, 6, lab=(137.3, 308.2, 'l'))
    d.eq('dtank', 'TK-202', 148, 290, 12, 18, lab=(154, 313.5, 'm'), nz={'out': (1, 2 / 3, 'R')})
    d.eq('pump', 'P-204', 166, 299, 6, 6, lab=(173.3, 308.2, 'l'))
    # ---- PM-4 kontainer membran
    d.eq('pump', 'P-301', 250, 215, 7, 7, lab=(253.5, 228.6, 'm'))
    d.eq('membrane', 'MB-301', 266, 193, 30, 10, lab=(281, 189.5, 'm'), nz={'in': (0, .5, 'L'), 'ret': (1, .3, 'R'), 'perm': (.75, 1, 'D'), 'cip': (.0667, 1, 'D')})
    d.eq('pump', 'P-302', 300, 214, 6, 6, lab=(303, 226.6, 'm'))
    d.eq('tankf', 'TK-302', 262, 214, 12, 16, lab=(268, 234.6, 'm'), nz={'out': (.5, 0, 'U')})
    d.eq('pump', 'P-303', 244, 268, 6, 6, lab=(247, 280.6, 'm'))
    # ---- PM-10 tangki permeat + lumpur
    d.eq('vessel', 'TK-301', 324, RY, 16, RH, lab=(332, RY - 2.2, 'm'), nz={'in': (0, .4, 'L'), 'fi': (0, .55, 'L'), 'out': (.5, 1, 'D')})
    d.eq('pump', 'P-501', 343, YF + 6, 7, 7, lab=(346.5, YF + 18.6, 'm'))
    d.eq('spress', 'PR-501', 256, 296, 34, 15, lab=(294, 303, 'l'), nz={'in': (.23, -.16, 'U'), 'poly': (.40, -.16, 'U'), 'cake': (0, .6, 'L'), 'f': (.625, 1.12, 'D')})
    # ---- PM-6/7 gas
    d.eq('gasholder', 'GH-301', 196, 98, 40, 30, lab=(216, 133.5, 'm'), hitbox=[(.1, .05, .9, 1), (0, .55, 1, 1)], nz={'in': (.2, 1, 'D'), 'out': (.8, 1, 'D')})
    d.eq('column', 'BTF-301', 262, 70, 13, 52, lab=(260, 80, 'r'), packed=True, nz={'in': (0, .80, 'L'), 'top': (.5, 0, 'U'), 'air': (1, .92, 'R'), 'bd': (.5, 1, 'D')})
    d.eq('ccomp', 'K-301', 284, 104, 7, 7, lab=(282.6, 108.3, 'r'), nz={'in': (.25, 0, 'U'), 'out': (.75, 1, 'D')})
    d.eq('hx', 'HX-301', 292, 72, 18, 9, lab=(301, 86.3, 'm'), nz={'in': (0, .5, 'L'), 'out': (1, .5, 'R'), 'cs': (.25, 1, 'D'), 'cr': (.75, 1, 'D')})
    d.eq('kopot', 'V-301', 318, 66, 9, 24, lab=(328.6, 72.5, 'l'), nz={'in': (0, .25, 'L'), 'out': (.5, 0, 'U'), 'dr': (.5, 1, 'D')})
    d.eq('ccomp', 'K-302', 340, 72, 9, 9, lab=(340.5, 88.5, 'r'), nz={'in': (.25, 0, 'U'), 'out': (.75, 1, 'D')})
    d.eq('gasfilter', 'AC-301', 364, 66, 12, 34, lab=(378, 72, 'l'), nz={'in': (0, .2, 'L'), 'out': (.5, 1, 'D'), 'sp': (1, .9, 'R')})
    d.eq('flare', 'FL-301', 446, 88, 10, 36, lab=(451, 128.6, 'm'), nz={'in': (0, .80, 'L')})
    # ---- PM-8/9 CHP + panas
    d.eq('genset', 'GE-401', 404, 166, 44, 20, lab=(422, 162.5, 'm'), inner_label=True, nz={'gas': (0, .5, 'L'), 'air': (.15, 1, 'D'), 'ex': (.85, 1, 'D'), 'el': (.85, 0, 'U')})
    d.eq('hx', 'HX-401', 420, 206, 30, 11, lab=(435, 221.6, 'm'), nz={'in': ((441.4 - 420) / 30, 0, 'U'), 'out': (1, .5, 'R'), 'hs': (0, .3, 'L'), 'hr': (0, .7, 'L')})
    d.eq('stack', 'ST-401', 458, 178, 6, 24, lab=(457, 182, 'r'), nz={'in': (.5, 1, 'D')})
    d.eq('ct', 'CT-601', 24, 280, 26, 30, lab=(37, 315, 'm'), hitbox=[(.34, 0, .66, .16), (.13, .16, .87, .5), (.06, .5, .94, .86), (0, .86, 1, 1)], nz={'cwr': (.09, .3, 'L'), 'cws': (-.023, .93, 'L'), 'mk': (1.023, .973, 'R')})

# =====================================================================================================
# 4. ALIRAN
# =====================================================================================================
def streams():
    P = lambda r: d.pt(r)[:2]
    # ---------------- praolah
    y1 = P('SC-101.in')[1]
    f1 = flag("POME mentah", 28, y1, 'r', 'in'); d.conn('s1', f1, 'SC-101.in', stub_b=0); stag(1, 31.6, y1, 'b')
    f2 = flag("Residu + pasir", 88, 214, 'r', 'out')
    sc = P('SC-101.scr'); uf = P('HC-101.uf')
    d.conn('s2a', None, None, pts=[sc, (sc[0], 214), (f2['pt'][0], 214)]); stag(2, 66, 214, 'b')
    d.conn('s2b', None, None, pts=[uf, (uf[0], 214)], arrow=False); d.junction(uf[0], 214)
    o = P('SC-101.out'); pl = P('P-101.l')
    d.conn('s3a', None, None, pts=[o, (57, o[1]), (57, pl[1]), pl])
    hi = P('HC-101.in'); pt_ = P('P-101.t')
    d.conn('s3b', None, None, pts=[pt_, (pt_[0], hi[1]), hi])
    of = P('HC-101.of'); el = P('E-101.l')
    d.conn('s3', None, None, pts=[of, (of[0], 160), (88, 160), (88, el[1]), el]); stag(3, 84.4, 160, 't')
    er = P('E-101.r'); ti = P('TK-101.in')
    d.conn('s4', None, None, pts=[er, ti]); stag(4, 114.5, ti[1], 'b')
    # air pendingin E-101 (dari CT-601)
    cs = d.pt('E-101.b@0.35'); cr = d.pt('E-101.b@0.8')
    fcws = flag("CWS", 94.5, 192, 'r', 'in', util=True)
    d.conn('u1', None, None, cls='util', pts=[fcws['pt'][:2], (cs[0], 192), cs[:2]])
    fcwr = flag("CWR", cr[0] + 4, 198, 'r', 'out', util=True)
    d.conn('u2', None, None, cls='util', pts=[cr[:2], (cr[0], 198), fcwr['pt'][:2]])
    # ---------------- umpan reaktor + dosing
    to = P('TK-101.out'); p2 = P('P-201.l')
    d.conn('s7a', None, None, pts=[to, (to[0], p2[1]), p2])
    pt2 = P('P-201.t'); f_end = (RX2 + RW * .3, YF)
    d.conn('s7', None, f_end, pts=[pt2, (pt2[0], YF), f_end], arrow=False)
    for x, tg in ((RX1, 'R-201'), (RX2, RT)):
        d.conn('f' + tg, ('J', x + RW * .3, YF), tg + '.fd', stub=0)
    d.junction(RX1 + RW * .3, YF)
    stag(7, 200, YF, 'b')
    d.conn('n1', 'TK-201.out', 'P-203.l'); d.conn('n2', 'TK-202.out', 'P-204.l')
    a = P('P-203.t'); d.conn('s5', None, ('J', 148, YF), pts=[a, (a[0], 284), (150, 284), (150, YF)]); d.junction(150, YF); stag(5, 141.5, 284, 't')
    b = P('P-204.t'); d.conn('s6', None, ('J', 156, YF), pts=[b, (b[0], 278), (158, 278), (158, YF)]); d.junction(158, YF); stag(6, 163.5, 278, 't')
    # jet mixing (setiap reaktor; digambar pada R-201)
    js = P('R-201.js'); pl = P('P-202.l'); d.conn('jm1', None, None, pts=[js, (js[0], pl[1]), pl])
    jt = P('P-202.t'); jr = P('R-201.jr'); d.conn('jm2', None, None, pts=[jt, (jt[0], jr[1]), jr])
    xm = (RX1 + RW + RX2) / 2
    d.text(xm + 1, 192, "R-202 s/d", 1.7, 'm', True); d.text(xm + 1, 195.6, "R-2%02d" % (NR - 1), 1.7, 'm', True); d.text(xm + 1, 199.2, "identik, paralel", 1.4, 'm', False)
    # ---------------- loop membran (digambar pada R-2NN; manifold ke semua reaktor)
    mo = P(RT + '.mo'); pl = P('P-301.l')
    d.conn('s8a', None, None, pts=[mo, (245, mo[1]), (245, pl[1]), pl])
    pt3 = P('P-301.t'); mi = P('MB-301.in')
    d.conn('s8', None, None, pts=[pt3, (pt3[0], mi[1]), mi]); stag(8, 259.5, mi[1], 't')
    ret = P(RT + '.ret'); mr = P('MB-301.ret')
    d.conn('s9', None, None, pts=[mr, (300, mr[1]), (300, 182), (247, 182), (247, ret[1]), ret]); stag(9, 285, 182, 't')
    pp = P('MB-301.perm'); pl = P('P-302.l')
    d.conn('s10a', None, None, pts=[pp, (pp[0], pl[1]), pl])
    pt4 = P('P-302.t'); tin = P('TK-301.in')
    d.conn('s10', None, None, pts=[pt4, (pt4[0], tin[1]), tin]); stag(10, 314.5, tin[1], 't')
    d.conn('cip', None, None, pts=[P('TK-302.out'), P('MB-301.cip')], dash=[1.6, .8])
    # lumpur buangan -> screw press
    ws = P(RT + '.ws'); pl = P('P-303.l')
    d.conn('s11a', None, None, pts=[ws, (ws[0], pl[1]), pl])
    pt5 = P('P-303.t'); pin = P('PR-501.in')
    d.conn('s11', None, None, pts=[pt5, (pt5[0], 262), (pin[0], 262), pin]); stag(11, 258.5, 262, 't')
    f26 = flag("Polimer", 296, 286, 'l', 'in'); ppo = P('PR-501.poly')
    d.conn('s26', None, None, pts=[f26['pt'][:2], (ppo[0], 286), ppo]); stag(26, 280, 286, 't')
    ck = P('PR-501.cake'); f12 = flag("Kue lumpur ke kebun", 246, ck[1], 'l', 'out')
    d.conn('s12', None, None, pts=[ck, f12['pt'][:2]]); stag(12, 251, ck[1], 'b')
    fp = P('PR-501.f'); tf = P('TK-301.fi')
    d.conn('s13', None, None, pts=[fp, (fp[0], 326), (316, 326), (316, tf[1]), tf]); stag(13, 300, 326, 'b')
    to = P('TK-301.out'); pl = P('P-501.l'); d.conn('s14a', None, None, pts=[to, (to[0], pl[1]), pl])
    pt6 = P('P-501.t'); f14 = flag("Efluen ke kolam polishing", 366, YF - 8, 'r', 'out')
    d.conn('s14', None, None, pts=[pt6, (pt6[0], YF - 8), f14['pt'][:2]]); stag(14, 357, YF - 8, 'b')
    # ---------------- biogas
    g1 = P('R-201.gas'); g2 = P(RT + '.gas'); gi = P('GH-301.in')
    d.conn('s15a', None, None, pts=[g1, (g1[0], YG), (gi[0], YG)], arrow=False)
    d.conn('s15b', None, None, pts=[g2, (g2[0], YG), (gi[0], YG)], arrow=False)
    d.conn('s15', None, None, pts=[(gi[0], YG), gi]); d.junction(gi[0], YG)
    stag(15, 190, YG, 'b')
    go = P('GH-301.out'); bi = P('BTF-301.in')
    d.conn('s16', None, None, pts=[go, (go[0], 140), (252, 140), (252, bi[1]), bi]); stag(16, 237.5, 140, 'b')
    ki = P('K-301.in'); fa = flag("Udara", 300, 98, 'l', 'in')
    d.conn('s17', None, None, pts=[fa['pt'][:2], (ki[0], 98), ki]); stag(17, 292.5, 98, 't')
    ko = P('K-301.out'); ba = P('BTF-301.air')
    d.conn('s17b', None, None, pts=[ko, (ko[0], ba[1]), ba])
    bd = P('BTF-301.bd'); fbd = flag("Blowdown S ke IPAL", 272, 152, 'r', 'out')
    d.conn('s19', None, None, pts=[bd, (bd[0], 152), fbd['pt'][:2]]); stag(19, bd[0], 136, 'l')
    tp = P('BTF-301.top'); hi = P('HX-301.in')
    d.conn('s18', None, None, pts=[tp, (tp[0], 62), (286, 62), (286, hi[1]), hi]); stag(18, 280.5, 62, 'b')
    vo = P('HX-301.out'); vi = P('V-301.in')
    d.conn('g2a', None, None, pts=[vo, (314, vo[1]), (314, vi[1]), vi])
    dr = P('V-301.dr'); fcd = flag("Kondensat", 326, 104, 'r', 'out')
    d.conn('s20', None, None, pts=[dr, (dr[0], 104), fcd['pt'][:2]]); stag(20, dr[0], 100, 'l')
    vt = P('V-301.out'); ki = P('K-302.in')
    d.conn('g2b', None, None, pts=[vt, (vt[0], 60), (ki[0], 60), ki])
    ko = P('K-302.out'); ai = P('AC-301.in')
    d.conn('g2c', None, None, pts=[ko, (ko[0], 92), (357, 92), (357, ai[1]), ai])
    sp = P('AC-301.sp'); fsp = flag("Karbon jenuh", 386, sp[1], 'r', 'out'); d.conn('s25', None, None, pts=[sp, fsp['pt'][:2]]); stag(25, 381, sp[1], 'b')
    ao = P('AC-301.out'); fi = P('FL-301.in'); gg = P('GE-401.gas')
    d.conn('s21a', None, None, pts=[ao, (ao[0], fi[1])], arrow=False); d.junction(ao[0], fi[1])
    d.conn('s22', None, None, pts=[(ao[0], fi[1]), fi]); stag(22, 426, fi[1], 't')
    d.conn('s21', None, None, pts=[(ao[0], fi[1]), (ao[0], gg[1]), gg]); stag(21, 386, gg[1], 'b')
    # ---------------- CHP
    ga = P('GE-401.air'); fair = flag("Udara bakar", 396, 196, 'r', 'in')
    d.conn('s23', None, None, pts=[fair['pt'][:2], (ga[0], 196), ga]); stag(23, 403, 196, 'b')
    ge = P('GE-401.ex'); hx = P('HX-401.in'); d.conn('ex1', None, None, pts=[ge, hx])
    hxo = P('HX-401.out'); si = P('ST-401.in'); d.conn('s24', None, None, pts=[hxo, (si[0], hxo[1]), si]); stag(24, 455.5, hxo[1], 'b')
    el = P('GE-401.el'); fel = flag("Listrik ke PKS", 444, 156, 'r', 'out', util=True)
    d.conn('u_el', None, None, cls='util', pts=[el, (el[0], 156), fel['pt'][:2]])
    hs = P('HX-401.hs'); hr = P('HX-401.hr')
    fhs = flag("Air panas ke PKS", hs[0] - 8, hs[1], 'l', 'out', util=True); d.conn('u_hs', None, None, cls='util', pts=[hs, fhs['pt'][:2]])
    fhr = flag("Air balik", hr[0] - 8, hr[1], 'r', 'in', util=True); d.conn('u_hr', None, None, cls='util', pts=[fhr['pt'][:2], hr])
    # ---------------- menara pendingin
    cwr = P('CT-601.cwr'); cws = P('CT-601.cws'); mk = P('CT-601.mk')
    f = flag("CWR", 20, cwr[1], 'r', 'in', util=True); d.conn('u_ct1', None, None, cls='util', pts=[f['pt'][:2], cwr])
    f = flag("CWS", 20, cws[1], 'l', 'out', util=True); d.conn('u_ct2', None, None, cls='util', pts=[cws, f['pt'][:2]])
    f = flag("Air baku", 66, mk[1], 'l', 'in', util=True); d.conn('u_ct3', None, None, cls='util', pts=[f['pt'][:2], mk])
    return dict(fhr=fhr, fel=fel)

def wire(F):
    pass

# =====================================================================================================
# 5. INSTRUMENTASI
# =====================================================================================================
RB = 2.9
def _trim(pts):
    (x0, y0), (x1, y1) = pts[0], pts[1]
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    return [(x0 + (x1 - x0) / L * RB, y0 + (y1 - y0) / L * RB)] + list(pts[1:])
_ns = [0]
def loop(fn, num, x, y, *lines, note=None, nd='b'):
    """gelembung ISA-5.1 di (x,y); setiap garis sinyal dimulai dari pusat gelembung (dipotong di tepi)."""
    d.inst2(x, y, fn, num, RB)
    for p in lines:
        _ns[0] += 1; sig('sg%d' % _ns[0], _trim(p))
    if note:
        if nd == 'b': d.text(x, y + RB + 2.1, note, 1.25, 'm', False, layer='inst')
        elif nd == 'r': d.text(x + RB + .8, y + .45, note, 1.25, 'l', False, layer='inst')
        else: d.text(x - RB - .8, y + .45, note, 1.25, 'r', False, layer='inst')
def cv(x, y, vert=False): return d.cvalve(x, y, vert)[:2]

LOOPS = [("TIC-102", "Suhu umpan (stream 4) → katup CWR E-101; SP dari TIC-206"),
         ("LIC-103", "Level TK-101 → VSD P-201 (laju umpan merata 24 jam)"),
         ("FQI-201", "Laju + total umpan reaktor (OLR)"),
         ("AIC-202", "pH reaktor 7,0 → laju pompa NaOH P-203"),
         ("AIC-203", "NH₄-N reaktor ≥ 100 mg/L → pompa urea P-204"),
         ("LI-204/205", "Level tangki dosing, alarm rendah (LAL)"),
         ("TIC-206", "Suhu reaktor 55 °C → SP kaskade TIC-102"),
         ("LIC-207", "Level reaktor → VSD pompa permeat P-302"),
         ("FIC-301", "Laju cross-flow (4 m/s) → VSD P-301"),
         ("PDI-302", "TMP membran → pemicu backflush / CIP"),
         ("LI-303", "Level tangki CIP TK-302"),
         ("FIC-304", "Laju lumpur buangan → P-303 (SRT %.0f hari)" % RV["srt_d"]),
         ("LIC-305", "Level TK-301 → VSD pompa efluen P-501"),
         ("LIC-401", "Isi penampung gas GH-301 → SP beban JIC-501"),
         ("AIC-402", "O₂ biogas keluar BTF → VSD blower K-301"),
         ("LIC-403", "Level sump BTF → katup blowdown"),
         ("LIC-404", "Level KO pot V-301 → katup kondensat"),
         ("PIC-405", "Tekanan buang K-302 → VSD K-302"),
         ("AIA-406", "CH₄ / H₂S gas bahan bakar, alarm + trip GE"),
         ("PIC-407", "Tekanan header gas tinggi → katup flare FL-301"),
         ("JIC-501", "Beban genset → katup gas (governor) GE-401/402"),
         ("LIC-601", "Level bak CT-601 → katup air baku")]

def instruments():
    P = lambda r: d.pt(r)[:2]
    # TIC-102 : suhu stream 4 -> katup CWR
    cr = P('E-101.b@0.8'); vx, vy = cv(cr[0], 191, True)
    loop('TIC', 102, 118, 157, [(118, 157), (118, 173)], [(118, 157), (109.3, 157), (109.3, vy), (vx, vy)])
    # LIC-103 : TK-101 -> P-201
    loop('LIC', 103, 148, 176, [(148, 176), (136, 176)], [(148, 176), (148, 261.5), (146, 261.5)])
    # FQI-201 : header umpan
    loop('FQI', 201, 164, 241, [(164, 241), (164, YF)])
    # AIC-202 / AIC-203 : pH dan NH4-N -> pompa dosing
    loop('AIC', 202, 140, 323, [(140, 323), (133, 323), (133, 305.6)], note="pH R-2xx", nd='r')
    loop('AIC', 203, 176, 323, [(176, 323), (169, 323), (169, 305.6)], note="NH₄-N R-2xx", nd='r')
    loop('LI', 204, 106, 296, [(106, 296), (112, 296)])
    loop('LI', 205, 164.5, 291.5, [(164.5, 291.5), (160, 291.5)])
    # TIC-206 : suhu reaktor
    loop('TIC', 206, 156, 190, [(156, 190), (166, 190)], note="SP → TIC-102", nd='b')
    # LIC-207 : level reaktor -> P-302 (permeat)
    loop('LIC', 207, 253, 170, [(253, 170), (240, 170)], [(253, 170), (307, 170), (307, 217), (306, 217)])
    # FIC-301 : cross-flow -> P-301
    loop('FIC', 301, 260, 209, [(260, 209), (253.5, 209)], [(260, 209), (260, 218.5), (257, 218.5)])
    # PDI-302 : TMP membran
    loop('PDI', 302, 283, 209, [(283, 209), (283, 203)])
    loop('LI', 303, 279.5, 224, [(279.5, 224), (274, 224)])
    # FIC-304 : lumpur buangan -> P-303
    loop('FIC', 304, 256, 271, [(256, 271), (256, 262)], [(256, 271), (250, 271)])
    # LIC-305 : TK-301 -> P-501
    loop('LIC', 305, 351, 178, [(351, 178), (340, 178)], [(351, 178), (351, 261.5), (350, 261.5)])
    # LIC-401 : penampung gas -> beban CHP
    loop('LIC', 401, 189, 112, [(189, 112), (197.6, 112)], note="SP → JIC-501", nd='b')
    # AIC-402 : O2 keluar BTF -> K-301
    loop('AIC', 402, 298, 107.5, [(298, 107.5), (291, 107.5)], note="O₂ BTF", nd='b')
    # LIC-403 : sump BTF -> katup blowdown
    vx, vy = cv(P('BTF-301.bd')[0], 145, True)
    loop('LIC', 403, 282, 128, [(282, 128), (282, 121), (275, 121)], [(282, 128), (282, vy), (vx, vy)])
    # LIC-404 : KO pot -> katup kondensat
    vx, vy = cv(P('V-301.dr')[0], 95, True)
    loop('LIC', 404, 333, 84, [(333, 84), (327, 84)], [(333, 84), (333, vy), (vx, vy)])
    # PIC-405 : blower biogas
    loop('PIC', 405, 352, 85.5, [(352, 85.5), (346.75, 85.5)], [(352, 85.5), (352, 76.5), (349, 76.5)])
    # AIA-406 : analis gas bahan bakar
    loop('AIA', 406, 379, 142, [(379, 142), (370, 142)], note="CH₄ / H₂S", nd='b')
    # PIC-407 : katup flare
    fi = P('FL-301.in'); vx, vy = cv(414, fi[1])
    loop('PIC', 407, 414, 104, [(414, 104), (402, 104), (402, fi[1])], [(414, 104), (vx, vy)])
    # JIC-501 : beban genset -> katup gas
    gg = P('GE-401.gas'); vx, vy = cv(396, gg[1])
    loop('JIC', 501, 396, 158, [(396, 158), (vx, vy)])
    # LIC-601 : bak CT -> katup air baku
    mk = P('CT-601.mk'); vx, vy = cv(58, mk[1])
    loop('LIC', 601, 62, 297, [(62, 297), (48.9, 297)], [(62, 297), (62, 302.5), (vx, 302.5), (vx, vy)])

def modules():
    dash = [3.0, 1.6]; lw = .4
    def box(x0, y0, x1, y1, label, lx=None, ly=None, anchor='l'):
        d.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], lw, None, '#000000', 'frame', dash)
        d.text(x0 + 1.2 if lx is None else lx, y0 + 2.9 if ly is None else ly, label, 1.6, anchor, True, layer='frame', chk=False)
    box(24, 148, 112, 222, "PM-1  SKID PRAOLAH")
    box(115, 161, 141, 238, "PM-2", 116, 164.2)
    box(152, 140, 243, 252, "PM-3  REAKTOR (×%d)" % NR, 153, 138.6)
    box(244, 165, 312, 240, "PM-4  KONTAINER MEMBRAN", 245, 163.6)
    box(100, 256, 186, 332, "PM-5  SKID DOSING + POMPA UMPAN", 101, 337.2)
    d.poly([(248, 55), (392, 55), (392, 112), (312, 112), (312, 158), (248, 158)], lw, None, '#000000', 'frame', dash)
    d.text(249, 156.6, "PM-6  SKID PENGOLAHAN GAS", 1.6, 'l', True, layer='frame', chk=False)
    box(184, 94, 243, 137.5, "PM-7", 185, 136.2)
    box(436, 80, 464, 135, "PM-7", 437, 133.6)
    box(398, 150, 466, 192, "PM-8  KONTAINER CHP (×2)", 399, 148.6)
    box(408, 199, 466, 229, "PM-9", 409, 227.6)
    box(10.5, 268, 70, 320, "PM-9  MENARA PENDINGIN", 12, 266.6)
    box(316, 156, 372, 272, "PM-10", 317, 154.6)
    box(234, 258, 312, 334, "PM-10  SKID LUMPUR", 235, 337.2)
    d.text(426, 190.0, "GE-402 identik (2 unit)", 1.4, 'm', False, chk=False)

# =====================================================================================================
# 6. PANEL INFORMASI
# =====================================================================================================
def tc(x, y, t, size=1.35, anchor='l', bold=False): d.text(x, y, t, size, anchor, bold, layer='table', chk=False)
def head(y0, h, title):
    d.rect(PX + 1.5, y0, PW - 3, h, .45, None, 'table'); d.rect(PX + 1.5, y0, PW - 3, 4.2, .45, '#e6e6e6', 'table')
    tc(PX + PW / 2, y0 + 3.1, title, 1.85, 'm', True)
def wrap(t, wmax, size):
    out = []; line = ""
    for w_ in t.split():
        if eng.twidth((line + " " + w_).strip(), size) > wmax: out.append(line.strip()); line = w_
        else: line += " " + w_
    out.append(line.strip()); return out
def panels():
    x = PX + 3.5
    # ---------------- LEGENDA
    y0 = 13; head(y0, 98, "LEGENDA")
    y = y0 + 8.5
    def row(lbl, fn, y):
        fn(x, y); tc(x + 22, y + .5, lbl)
    L = lambda w, dash=None, col='#000000': (lambda x, y: d.line([(x, y), (x + 18, y)], w, dash, col, 'table'))
    row("Aliran proses utama", L(.5), y); y += 4.3
    row("Aliran utilitas (CW, air panas, listrik)", L(.26, None, '#505050'), y); y += 4.3
    row("Sinyal instrumen (elektrik)", L(.18, [.9, .6]), y); y += 4.3
    row("Aliran berkala (CIP)", L(.5, [1.6, .8]), y); y += 4.3
    row("Batas modul portabel PM-1 s/d PM-10", L(.4, [3.0, 1.6]), y); y += 5.4
    def tagbox(x, y):
        hr = 2.4; xx = x + 9; d.rect(xx - 3.6, y - 3.6, 7.2, 3 * hr, .3, '#ffffff', 'table')
        for k in (1, 2): d.line([(xx - 3.6, y - 3.6 + k * hr), (xx + 3.6, y - 3.6 + k * hr)], .18, None, '#000000', 'table')
        tc(xx, y - 1.8, "No.", 1.2, 'm', True); tc(xx, y + .6, "T °C", 1.1, 'm'); tc(xx, y + 3.0, "P bar", 1.1, 'm')
    tagbox(x, y); tc(x + 22, y - 1.2, "Tag aliran: nomor / suhu °C /"); tc(x + 22, y + 1.4, "tekanan bar absolut"); y += 9.2
    def bub(x, y):
        d.circ(x + 9, y, 2.7, .28, '#ffffff', 'table'); d.line([(x + 6.3, y), (x + 11.7, y)], .2, None, '#000000', 'table')
        tc(x + 9, y - .6, "LIC", 1.25, 'm', True); tc(x + 9, y + 1.9, "103", 1.25, 'm')
    bub(x, y); tc(x + 22, y - .7, "Instrumen di DCS/PLC, dapat diakses"); tc(x + 22, y + 1.8, "operator (ISA-5.1)"); y += 7.2
    def cvs(x, y):
        xx = x + 9; eng.Sym.valve(d, xx, y + 1, False, 'table', 1.5); d.line([(xx, y + .25), (xx, y - .8)], .22, None, '#000000', 'table')
        d.poly(d.arcpts(xx, y - .8, 1.2, 1.2, 0, 180), .22, '#ffffff', '#000000', 'table')
    cvs(x, y); tc(x + 22, y + .6, "Katup kendali, aktuator diafragma"); y += 5.2
    def flg(x, y):
        d.poly([(x + 2, y - 1.6), (x + 14, y - 1.6), (x + 16, y), (x + 14, y + 1.6), (x + 2, y + 1.6)], .3, '#ffffff', '#000000', 'table')
    flg(x, y); tc(x + 22, y + .5, "Batas baterai (masuk / keluar)"); y += 4.6
    def jn(x, y): d.line([(x, y), (x + 18, y)], .5, None, '#000000', 'table'); d.line([(x + 9, y), (x + 9, y + 2.5)], .5, None, '#000000', 'table'); d.circ(x + 9, y, .62, .05, '#000000', 'table', '#000000')
    jn(x, y); tc(x + 22, y + .5, "Percabangan / sambungan"); y += 5.0
    tc(x, y, "Huruf (ISA-5.1): A analisis, F laju, J daya, L level, P tekanan,", 1.2); y += 2.6
    tc(x, y, "PD beda tekanan, T suhu; I indikasi, C kendali, Q total, A alarm.", 1.2); y += 2.6
    tc(x, y, "Simbol alat: ISO 10628-2; identifikasi alat: PIP PIC-001.", 1.2); y += 2.6
    tc(x, y, "Utilitas: CWS/CWR air pendingin 30/40 °C dari CT-601.", 1.2)
    # ---------------- KINERJA
    y0 = 113; rows = [
        ("Umpan POME", "%s m³/hari, COD %s kg/m³" % (idn(R["design_basis"]["pome_m3d"]), idn(R["design_basis"]["cod_blend"], 1))),
        ("Reaktor", "%d × %s m³, 55 °C, pH %s" % (NR, idn(RV["V_liq_m3"]), idn(NOM["pH"], 2))),
        ("HRT / SRT / OLR", "%s d / %.0f d / %s kg COD/m³·d" % (idn(RV["hrt_d"], 2), RV["srt_d"], idn(NOM["olr"], 1))),
        ("MLSS / FOS-TAC", "%s g/L / %s" % (idn(NOM["mlss"], 1), idn(NOM["fos_tac"], 3))),
        ("Biogas", "%s Nm³/hari, CH₄ %s %%" % (idn(NOM["biogas_Nm3d"]), idn(NOM["ch4_frac"] * 100, 1))),
        ("H₂S mentah / ke mesin", "%s / %s ppm" % (idn(NOM["h2s_ppm_raw"]), idn(NOM["h2s_ppm_fuel"]))),
        ("Listrik bruto / neto", "%s / %s kWe" % (idn(EN["P_gross"]), idn(EN["P_net"]))),
        ("Pemakaian sendiri", "%s kWe (%s %%)" % (idn(EN["P_par"]), idn(EN["P_par"] / EN["P_gross"] * 100, 1))),
        ("Panas tersedia", "%s kWth air panas 90 °C" % idn(EN["Q_heat_avail"])),
        ("Penyisihan COD", "%s %% (reaktor + membran)" % idn(NOM["cod_rem"] * 100, 1)),
        ("Daya neto P5/P50/P95", "%s / %s / %s kWe (MC)" % tuple(idn(R["monte_carlo"]["P_net"][k]) for k in ("P5", "P50", "P95"))),
        ("Emisi dihindari", "%s tCO₂e/tahun" % idn(R["emissions"]["avoided_t"])),
    ]
    head(y0, 6 + 2.85 * len(rows), "KINERJA TITIK RANCANGAN (45 t TBS/jam)")
    y = y0 + 7.4
    for a, b in rows: tc(x, y, a, 1.3, 'l', True); tc(x + 37, y, b, 1.3); y += 2.85
    # ---------------- LOOP KENDALI
    y0 = y + 1.2; head(y0, 6 + 2.6 * len(LOOPS), "LOOP KENDALI UTAMA")
    y = y0 + 7.2
    for a, b in LOOPS: tc(x, y, a, 1.25, 'l', True); tc(x + 17, y, b, 1.25); y += 2.6
    # ---------------- CATATAN
    NOTES = ["Neraca massa dan energi lengkap per aliran: process/biogas_balance.py → outputs/results.json (tidak ditabelkan pada PFD ini).",
             "Titik rancangan 45 t TBS/jam × 20 jam/hari; T dan P pada tag aliran adalah kondisi operasi normal.",
             "R-201 s/d R-2%02d identik dan paralel; loop membran, jet mixing dan sensor digambar pada satu reaktor, manifold ke semua." % NR,
             "Semua bejana adalah satu desain standar Ø%s × %s m, dikirim rebah di trailer low-bed; alat lain dalam kontainer ISO/skid." % (idn(RV["D_m"], 1), idn(RV["H_shell_m"], 1)),
             "Pompa A/B = 1 operasi + 1 cadangan. Katup manual, PSV/PVRV reaktor dan instrumen lokal hanya di P&ID.",
             "Aliran 22 (flare) nol pada operasi normal; flare menyala bila GE berhenti atau penampung gas penuh."]
    y0 = y + 1.2; yl = []
    for k, t in enumerate(NOTES): yl.append(wrap("%d. %s" % (k + 1, t), PW - 8, 1.22))
    h = 6 + sum(len(q) for q in yl) * 2.35 + len(yl) * .5
    head(y0, h, "CATATAN"); y = y0 + 7.0
    for q in yl:
        for k, ln in enumerate(q): tc(x + (0 if k == 0 else 2.6), y, ln, 1.22); y += 2.35
        y += .5
    return y0 + h

def band():
    """pita bawah: set modul portabel + skala produk"""
    y0 = 342; x0 = 12; x1 = 330
    d.rect(x0, y0, x1 - x0, 64, .45, None, 'table'); d.rect(x0, y0, x1 - x0, 4.2, .45, '#e6e6e6', 'table')
    tc((x0 + x1) / 2, y0 + 3.1, "SET MODUL PORTABEL (45 t TBS/jam) - SEMUA DIRAKIT DI BENGKEL, DIKIRIM DENGAN TRUK", 1.85, 'm', True)
    cols = [x0, x0 + 13, x0 + 75, x0 + 162, x0 + 172, x0 + 233, x0 + 251, x1]
    hd = ["Modul", "Nama", "Isi (tag)", "Jml", "Bentuk pengiriman", "Massa t", "Muatan truk"]
    yy = y0 + 4.2; hr = 4.55
    for k, t in enumerate(hd): tc(cols[k] + 1.2, yy + 3.1, t, 1.3, 'l', True)
    yy += hr; d.line([(x0, yy), (x1, yy)], .3, None, '#000000', 'table')
    for m in PM["modules"]:
        v = [m["id"], m["name"], ", ".join(m["tags"]), str(m["qty"]), m["unit"], idn(m["mass_t_total"], 1), str(m["ship_units"])]
        for k, t in enumerate(v):
            tc(cols[k] + 1.2, yy + 3.0, t, 1.22, 'l', k == 0)
        yy += 4.6
    for c in cols[1:-1]: d.line([(c, y0 + 4.2), (c, y0 + 64)], .15, None, '#000000', 'table')
    # skala produk
    x2 = 334; x3 = 466
    d.rect(x2, y0, x3 - x2, 64, .45, None, 'table'); d.rect(x2, y0, x3 - x2, 4.2, .45, '#e6e6e6', 'table')
    tc((x2 + x3) / 2, y0 + 3.1, "SKALA SET UNTUK PKS SUMATERA", 1.85, 'm', True)
    T = R["tiers"]; S = PM["scaling"]
    cc = [x2, x2 + 46, x2 + 74, x2 + 102, x3]
    rows = [("Kapasitas PKS", ["%s t TBS/jam" % k for k in ("30", "45", "60")]),
            ("POME, m³/hari", [idn(T[k]["POME_m3d"]) for k in ("30", "45", "60")]),
            ("Reaktor standar", ["%d" % T[k]["N_modules"] for k in ("30", "45", "60")]),
            ("Bejana total (+TK-101, TK-301)", ["%d" % S[k]["vessels"] for k in ("30", "45", "60")]),
            ("Membran UF, m²", [idn(S[k]["membrane_m2"]) for k in ("30", "45", "60")]),
            ("Genset", ["%d × %s kWe" % (T[k]["chp"]["N_gen"], idn(T[k]["chp"]["P_unit"])) for k in ("30", "45", "60")]),
            ("Daya bruto, kWe", [idn(T[k]["P_gross"]) for k in ("30", "45", "60")]),
            ("Daya neto, kWe", [idn(T[k]["P_net"]) for k in ("30", "45", "60")]),
            ("Kebutuhan PKS, kW", [idn(T[k]["P_mill"]) for k in ("30", "45", "60")]),
            ("Listrik neto, GWh/tahun", [idn(T[k]["GWh_y"], 1) for k in ("30", "45", "60")])]
    yy = y0 + 4.2
    for k, (a, b) in enumerate(rows):
        bold = k == 0
        tc(cc[0] + 1.2, yy + 3.1, a, 1.25, 'l', True)
        for i, t in enumerate(b): tc((cc[i + 1] + cc[i + 2]) / 2, yy + 3.1, t, 1.25, 'm', bold)
        yy += 4.6
        d.line([(x2, yy), (x3, yy)], .3 if k == 0 else .12, None, '#000000', 'table')
    for c in cc[1:-1]: d.line([(c, y0 + 4.2), (c, yy)], .15, None, '#000000', 'table')
    tc(x2 + 1.2, yy + 3.2, "Satu desain bejana untuk semua ukuran; PKS < 30 t/jam: set tanpa membran tidak dianjurkan.", 1.15)
    tc(x2 + 1.2, yy + 5.6, "Plot 45 t/jam ± %s m² (%s ha); total %d muatan truk, ± %s t." % (idn(PM["plot_area_m2_estimate"]["total"]), idn(PM["plot_area_m2_estimate"]["total"] / 1e4, 2), PM["ship_units_total"], idn(PM["mass_t_total"])), 1.15)

if __name__ == "__main__":
    frame(); callouts(); equipment(); F = streams(); instruments(); modules(); panels(); band()
    d.finalize()
    d.pdf(os.path.join(OUT, "PFD_BG-002_Rev1.pdf")); d.svg(os.path.join(OUT, "PFD_BG-002_Rev1.svg")); d.dxf(os.path.join(OUT, "PFD_BG-002_Rev1.dxf"))
    iss = d.check(verbose=False)
    print("isu pemeriksa:", len(iss))
    for q in iss[:80]: print("  !", q)
