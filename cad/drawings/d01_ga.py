# -*- coding: utf-8 -*-
"""Lembar 1: Tata letak umum (General Arrangement) set portabel 45 t TBS/jam - denah dari model 3D susunan pabrik."""
from dcommon import *
import bgmodels as M
import json, math

frame(1, "Tata Letak Umum Set Portabel\nPKS 45 t TBS/jam", "BG-GA-001", "1 : 300", "General Arrangement")
out, tags, (X0, Y0, X1, Y1) = M.plant(simple=True)
skip = ('baut', 'kursi', 'rib-', 'sirip', 'anak-tangga', 'sangkar', 'rel-', 'skid-lintang', 'cetakan', 'kunci', 'nosel-jet', 'plot-lantai',
        'header-jet', 'pipa-jet', 'louvre', 'bantalan', 'kopling', 'GE-kepala', 'MB-301-tutup', '-siku-', 'MB-301-tabung', 'MB-301-cermin', 'sirip-motor', 'pelindung', '-baut-', 'GH-baut', '-pad', 'klading-sabuk', 'las-', 'TT-', '-LT', 'SG-', 'davit', 'GE-runner', 'GE-peredam', 'GE-manifold', 'BTF-rel', 'kipas-motor', 'kotak-terminal', 'flens')
sh = [s for n, s, c in out if not any(k in n for k in skip)]
SC = 300.0
A = View((0, 0, 1), (1, 0, 0), SC, 22 - X0 / SC, 128 + Y0 / SC, name='denah')
A.draw(sh, hidden=False, w=.3); kd.OPEN_VIEWS.add('denah')
P = A.P
# batas plot (garis rantai tebal)
pa, pb = P((X0, Y0, 0)), P((X1, Y1, 0))
with own(('plot',)):
    L([pa, (pb[0], pa[1]), pb, (pa[0], pb[1]), pa], .5, [6, 1.5, 1.5, 1.5], 'equip')
dim_h(pa[0], pb[0], pb[1] - 7, fn(X1 - X0), pb[1], pb[1])
dim_v(pb[1], pa[1], pb[0] + 8, fn(Y1 - Y0), pb[0], pb[0])
# label bejana: baris selatan di bawah, baris utara di atas
for tg, x, y in tags:
    c = P((x, y, 0)); r = (M.VR + 300) / SC
    row_s = y < 20000
    TC(c[0], c[1] + r + 3.6 if row_s else c[1] - r - 3.6, tg, 3.0, 'm')
x0v, y0v = tags[0][1], tags[0][2]
c1, c2 = P((x0v, y0v, 0)), P((x0v + M.PITCH, y0v, 0))
dim_h(c1[0], c2[0], c1[1] + 19, fn(M.PITCH), c1[1] + 15, c2[1] + 15)
r7 = P((x0v, y0v + M.PITCH, 0))
# label modul
def cen(prefix):
    bb = None
    for n, s, c in out:
        if n.startswith(prefix):
            b = s.BoundingBox(); bb = [b.xmin, b.ymin, b.xmax, b.ymax] if bb is None else [min(bb[0], b.xmin), min(bb[1], b.ymin), max(bb[2], b.xmax), max(bb[3], b.ymax)]
    return ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2, 0), bb
LAB = [("PM-1/", "PM-1 PRAOLAH", -90), ("PM-5/", "PM-5 DOSING", -90), ("PM-10/", "PM-10 LUMPUR", -90), ("PM-9/", "PM-9 CT-601", 180),
       ("PM-4/", "PM-4 MEMBRAN", 90), ("PM-6/C6", "PM-6 GAS", 90), ("PM-6/BTF", "BTF-301", 90), ("PM-7/GH", "PM-7 GH-301", 60),
       ("PM-7/FL", "FL-301", -60), ("PM-8A/", "PM-8 CHP (x2)", -120)]
for pre, t, pr in LAB:
    cpt, bb = cen(pre)
    if pre == "PM-7/GH": cpt = (cpt[0] + 3200, bb[3] - 900, 0)
    auto_leader(P(cpt), t, pref=pr, rmin=8, rmax=45, size=3.0)
# panah utara
nx, ny = pb[0] - 10, pb[1] + 22
PG([(nx, ny - 8), (nx - 2.5, ny), (nx + 2.5, ny)], .3, '#000000'); TC(nx, ny - 12, "U", 3.5, 'm')
vlabel((pa[0] + pb[0]) / 2, pa[1] + 6, "DENAH TATA LETAK (DARI MODEL 3D)", "1:300")
# ---------------- tabel modul
PMJ = json.load(open(os.path.join(ROOT, "process", "outputs", "portable_modules.json"), encoding="utf-8"))
def cap(t): t = t.replace("Bejana standar: ", ""); return t[0].upper() + t[1:]
rows = [[m["id"], cap(m["name"])[:40], m["qty"], m["unit"].replace(" (membran terlipat)", "")[:40], fn(m["mass_t_total"], 1)] for m in PMJ["modules"]]
yt = table(196, 152, [("Modul", 14, 'm'), ("Nama", 70, 'l'), ("Jml", 10, 'm'), ("Pengiriman", 72, 'l'), ("Massa t", 16, 'm')], rows, "SET MODUL PORTABEL", rh=4.4, size=2.5, hsize=2.6)
T(196, yt + 5, "Total %d muatan truk, ± %s t. Plot %s x %s m = %s ha (termasuk jalan 3 m)." % (PMJ["ship_units_total"], fn(PMJ["mass_t_total"]),
  fn((X1 - X0) / 1000, 1), fn((Y1 - Y0) / 1000, 1), fn((X1 - X0) * (Y1 - Y0) / 1e10, 2)), 3.0, 'l')
TR = M.R["tiers"]
yt2 = table(196, yt + 10, [("PKS", 22, 'l'), ("Reaktor", 22, 'm'), ("Genset", 34, 'm'), ("Neto kWe", 26, 'm'), ("GWh/thn", 24, 'm'), ("Membran m²", 26, 'm')],
            [["%s t/jam" % k, str(TR[k]["N_modules"]), "%d x %s kWe" % (TR[k]["chp"]["N_gen"], fn(TR[k]["chp"]["P_unit"])), fn(TR[k]["P_net"]), fn(TR[k]["GWh_y"], 1), fn(TR[k]["membrane"]["area_m2"])] for k in ("30", "45", "60")],
            "SKALA SET (DESAIN BEJANA SAMA)", rh=4.4, size=2.5, hsize=2.6)
# ---------------- isometri
image("PLANT_iso-depan.png", 16, 150, 176, 98, name='ISO')
TC(104, 252, "ISOMETRI SUSUNAN PABRIK (TANPA SKALA)", 3.5, 'm')
json.dump({"plot_x_m": (X1 - X0) / 1000, "plot_y_m": (Y1 - Y0) / 1000, "plot_m2": (X1 - X0) * (Y1 - Y0) / 1e6},
          open(os.path.join(ROOT, "cad", "out", "ga.json"), "w"), indent=1)
finish("BG-GA-001")
