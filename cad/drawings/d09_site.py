# -*- coding: utf-8 -*-
"""Lembar 9: Denah lokasi - PKS proksi 45 t TBS/jam + sistem kolam POME + set generator biogas portabel.
Digambar dari data model 3D lokasi (site3d.py): jejak bangunan, kolam, rute pipa/kabel (panjang = CAPEX), luas lahan, jarak aman."""
from dcommon import *
import json, math
import site3d as SI
import bgmodels as M

frame(9, "Denah Lokasi PKS 45 t TBS/jam\n+ Set Generator Biogas", "BG-GA-002", "1 : 1750", "Site Plan")
P_, info = SI.site(); js = SI.write_info(info)
SC = 1750.0; k = 1000.0 / SC
OX, OY = 20.0, 147.5                       # kertas untuk (x=0, y=0) m
PT = lambda x, y: (OX + x * k, OY - y * k)
VB = [PT(-8, -24), PT(474, 236)]
VIEWS.append(((VB[0][0], VB[1][1], VB[1][0], VB[0][1]), 'lokasi')); kd.OPEN_VIEWS.add('lokasi')
def rect(x, y, L_, W_, w=.35, fill=None, dash=None, layer='equip'):
    a = PT(x, y); b = PT(x + L_, y + W_)
    PG([a, (b[0], a[1]), b, (a[0], b[1])], w, fill, layer, dash)
# jalan umum + pagar
with own(('jalan',)):
    rect(-8, -21, 482, 7, .25, '#d9d9d9', layer='util')
TC(PT(120, -17.5)[0], PT(120, -17.5)[1], "JALAN UMUM", 3.0, 'm')
for pts in ([(-5, -5), (227, -5), (227, 200), (-5, 200), (-5, -5)], [(227, -5), (470, -5), (470, 205), (227, 205)]):
    with own(('pagar', pts[0])):
        L([PT(*p) for p in pts], .3, [3, 1, .6, 1], 'inst')
# jejak bangunan / kolam
codes = []
for f in info["foot"]:
    if f["grp"] == "PRODUK" and f["tag"] == "PRODUK": continue
    if f["kind"] == "rect":
        x, y, L_, W_ = f["geom"]
        pond = f["grp"] == "KOLAM" and f["tag"] != "LA"
        freed = pond and info["ponds"][f["tag"]]["status"] == "dibebaskan"
        with own(('fp', f["tag"])):
            rect(x, y, L_, W_, .35)
            if pond:
                A_ = info["ponds"][f["tag"]]
                rect(A_["x"], A_["y"], A_["L"], A_["W"], .2)
        if pond:
            A_ = info["ponds"][f["tag"]]; a = PT(A_["x"], A_["y"]); b = PT(A_["x"] + A_["L"], A_["y"] + A_["W"])
            ring = [a, (b[0], a[1]), b, (a[0], b[1])]
            cc = PT(A_["x"] + A_["L"] / 2, A_["y"] + A_["W"] / 2)
            hole = [(cc[0] - 5.5, cc[1] - 3), (cc[0] + 5.5, cc[1] - 3), (cc[0] + 5.5, cc[1] + 3), (cc[0] - 5.5, cc[1] + 3)]
            hatch([ring, hole], 45 if freed else 0, 2.2 if freed else 1.6, .15, 'proc', None if freed else [1.2, 1.2])
            if freed: hatch([ring, hole], -45, 2.2, .15, 'proc')
        codes.append((f["tag"], f["label"]))
        c = PT(x + L_ / 2, y + W_ / 2)
        if L_ * k > 9 and W_ * k > 5 and f["tag"] not in ("WB", "GI"):
            with own(('fpt', f["tag"])):
                d.rect(c[0] - 4.2, c[1] - 2.2, 8.4, 4.4, 0, '#ffffff', 'inst')
            TC(c[0], c[1], f["tag"], 3.0, 'm', owner=('fpt', f["tag"]))
        else:
            auto_leader(c, f["tag"], pref={"WB": -20, "GI": -150}.get(f["tag"], 135), rmin=6, rmax=26, size=3.0)
    else:
        cx, cy, r = f["geom"]
        with own(('fp', f["tag"])):
            C(*PT(cx, cy), max(r * k, .8), .35)
# produk: batas plot + reaktor + GH + CHP
bb = info["pts"]["prod_bb"]
with own(('produk',)):
    rect(bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1], .7, None, [4, 1])
dx, dy = SI.PRODUCT_ORIGIN
out, tags, _ = M.plant(simple=True)
for tg, x, y in tags:
    with own(('rx', tg)):
        C(*PT(x / 1000 + dx, y / 1000 + dy), 2.21 * k, .3)
gh = info["pts"]["GH"]
with own(('gh',)):
    C(*PT(*gh), 7.4 * k, .35)
for tg, x0, y0, L_, W_ in (("CHP", 49.3 + dx, 5.0 + dy, 12.2, 2.4), ("CHP2", 49.3 + dx, 9.0 + dy, 12.2, 2.4), ("PM4", 22.3 + dx, 27.1 + dy, 12.2, 2.4), ("PM6", 36.1 + dx, 27.1 + dy, 12.2, 2.4),
                           ("PM1", 8.0 + dx, 6.0 + dy, 12.2, 2.4), ("PM5", 24.3 + dx, 6.0 + dy, 6.1, 2.4), ("PM10", 36.1 + dx, 6.0 + dy, 6.1, 2.4)):
    with own(('mod', tg)):
        rect(x0, y0, L_, W_, .25)
codes.append(("PRODUK", "Set biogas portabel, plot %s m²" % fn((bb[2] - bb[0]) * (bb[3] - bb[1]))))
pp = PT(bb[0] + 30, bb[1] - 4)
auto_leader(PT(bb[2], bb[3] - 6), "PRODUK", pref=10, rmin=6, rmax=30, size=3.5)
# rute (panjang = CAPEX)
STY = {"POME": ([3, 1], .6), "EFLUEN": ([4, 1, 1, 1], .5), "BYPASS": ([1, 1], .4), "20kV": ([6, 1, 1, 1, 1, 1], .4), "20kV-PKS": ([6, 1, 1, 1, 1, 1], .4)}
pts_r = {"20kV": info["routes"]["20kV"]["pts"], "20kV-PKS": info["pts"]["mill_power"]}
for kk, r_ in info["routes"].items():
    pts = pts_r.get(kk, r_["pts"])
    with own(('rute', kk)):
        L([PT(*p) for p in pts], STY[kk][1], STY[kk][0], 'proc')
# label rute
for kk, (x, y, pr) in {"POME": (236, 120, 180), "EFLUEN": (240, 140, 0), "20kV-PKS": (231, 60, 180)}.items():
    auto_leader(PT(x, y), {"POME": "POME DN150", "EFLUEN": "EFLUEN DN150", "20kV-PKS": "20 kV KE PKS", "BYPASS": "BYPASS"}[kk], pref=pr, rmin=6, rmax=30, size=3.0)
# panah utara + skala grafis
nx, ny = PT(455, 225)
PG([(nx, ny - 7), (nx - 2.2, ny), (nx + 2.2, ny)], .3, '#000000'); TC(nx, ny + 3.5, "U", 3.5, 'm')
sb = PT(0, -30)
for i in range(5):
    with own(('skala', i)):
        PG([(sb[0] + i * 50 * k, sb[1]), (sb[0] + (i + 1) * 50 * k, sb[1]), (sb[0] + (i + 1) * 50 * k, sb[1] + 1.5), (sb[0] + i * 50 * k, sb[1] + 1.5)], .2, '#000000' if i % 2 == 0 else '#ffffff', 'inst')
T(sb[0] + 250 * k + 2, sb[1] + 1.2, "250 m", 3.0, 'l')
vlabel(PT(360, 0)[0], PT(0, -30)[1] - 2, "DENAH LOKASI (DARI MODEL 3D)", "1:1750")
# ---------------- tabel kode (kiri bawah)
half = (len(codes) + 1) // 2
cw = [("Kode", 14, 'm'), ("Uraian", 66, 'l')]
y_ = 183
def short(l): return (l.replace(" - DIBEBASKAN", " (bebas)").replace("Kolam ", "K. ")[:44])
y1 = table(14, y_, cw, [[c, short(l)] for c, l in codes[:half]], "LEGENDA", rh=4.4, size=2.5, hsize=2.6)
table(96, y_ + 6, cw, [[c, short(l)] for c, l in codes[half:]], None, rh=4.4, size=2.5, hsize=2.6)
# ---------------- tabel kanan: rute + luas + jarak aman
SHORT = {"POME": "POME DN150 fat pit -> PM-1", "EFLUEN": "Efluen DN150 -> kolam polishing", "BYPASS": "Bypass darurat -> kolam pendingin",
         "20kV": "20 kV gardu -> jaringan PLN", "20kV-PKS": "20 kV ke rumah mesin PKS + trafo"}
rows = [[SHORT.get(k_, v_["label"][:36]), fn(v_["L_m"]), fn(v_["cost"])] for k_, v_ in js["routes"].items()]
rows.append(["Total (masuk CAPEX)", "", fn(js["interconnect_cost"])])
yr = table(296, 14, [("Rute (model 3D)", 68, 'l'), ("m", 14, 'm'), ("USD", 18, 'm')], rows, "INTERKONEKSI", rh=4.4, size=2.5, hsize=2.6)
ar = [["Kolam POME sebelum", fn(js["pond_area_before_m2"])], ["Kolam tetap (polishing)", fn(js["pond_area_after_m2"])],
      ["Kolam dibebaskan", fn(js["land_freed_m2"])], ["Plot produk", fn((bb[2] - bb[0]) * (bb[3] - bb[1]))]]
ya = table(296, yr + 3, [("Luas lahan", 70, 'l'), ("m²", 30, 'm')], ar, "LAHAN", rh=4.4, size=2.5, hsize=2.6)
sf = [[c["item"].replace("FL-301 ", "").replace("GH-301", "GH")[:34], fn(c["dist"], 1), fn(c["min"]), "Ya" if c["ok"] else "TIDAK"] for c in js["safety"]]
ys = table(296, ya + 3, [("Jarak aman", 58, 'l'), ("m", 14, 'm'), ("min", 14, 'm'), ("OK", 14, 'm')], sf, "PEMERIKSAAN JARAK AMAN", rh=4.4, size=2.5, hsize=2.6)
note(296, ys + 5, ["1. Arsir silang = kolam dibebaskan; arsir putus = air.", "2. Efluen produk tetap ke kolam polishing",
                   "   sebelum aplikasi lahan.", "3. Garis rantai = kabel 20 kV (PKS & PLN)."], 3.0)
finish("BG-GA-002")
