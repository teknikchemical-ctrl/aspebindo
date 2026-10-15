# -*- coding: utf-8 -*-
"""Lembar 3: PM-4 Kontainer membran 40 ft HC (denah atap dilepas, tampak samping dinding dilepas, tampak ujung, isometri potong, daftar bagian)."""
from dcommon import *
import bgmodels as M

frame(3, "PM-4 Kontainer Membran UF\n(MB-301, P-301, P-302, TK-302)", "BG-M-004", "1 : 60", "Assembly Drawing")
SC = 60.0
full = M.pm4()
def pick(excl): return [s for n, s, c in full if not any(e in n for e in excl)]
plan_sh = pick(("-atap", "-rib-", "-louvre", "-sirip", "-cetakan"))
elev_sh = pick(("-dinding-left", "-rib-left", "-pintu-samping", "-rib-right", "-louvre", "-sirip", "-dinding-right"))
# ---------------- denah
A = View((0, 0, 1), (1, 0, 0), SC, 25, 72, name='denah')
A.draw(plan_sh, hidden=False, w=.35)
kd.OPEN_VIEWS.add('denah')
P = A.P
x0, x1 = P((0, 0, 0))[0], P((M.CL, 0, 0))[0]; yb, yt = P((0, 0, 0))[1], P((0, M.CW, 0))[1]
dim_v(yt, yb, x1 + 8, fn(M.CW), x1, x1, out=True, side=1)
vlabel((x0 + x1) / 2, yb + 6, "DENAH (ATAP DILEPAS)", "1:60")
# ---------------- tampak samping
B = View((0, -1, 0), (1, 0, 0), SC, 25, 160, name='samping')
B.draw(elev_sh, hidden=False, w=.35)
kd.OPEN_VIEWS.add('samping')
Q = B.P
yg, yh = Q((0, 0, 0))[1], Q((0, 0, M.CH))[1]
dim_v(yg, yh, x1 + 8, fn(M.CH), x1, x1, out=True, side=1)
for k, xb in enumerate((900, 4500)):
    dim_h(Q((xb, 0, 0))[0], Q((xb + M.MOD_L, 0, 0))[0], yg + 7, fn(M.MOD_L), yg, yg)
dim_h(x0, x1, yg + 15, fn(M.CL), yg, yg)
vlabel((x0 + x1) / 2, yg + 20, "TAMPAK SAMPING (DINDING DILEPAS)", "1:60")
# ---------------- tampak ujung (pintu)
C = View((1, 0, 0), (0, 1, 0), SC, 274, 226, name='ujung')
C.draw(pick(("-rib-", "-louvre", "-sirip")), hidden=False, w=.35)
cx0, cx1 = C.P((0, 0, 0))[0], C.P((0, M.CW, 0))[0]
dim_h(cx0, cx1, C.P((0, 0, 0))[1] + 7, fn(M.CW), C.P((0, 0, 0))[1], C.P((0, 0, 0))[1])
vlabel((cx0 + cx1) / 2, C.P((0, 0, 0))[1] + 12, "TAMPAK UJUNG", "1:60")
# chain dimensi posisi bank modul (denah, sisi atas)
yA = yt - 6
xs_ = [0, 900 - 300, 4500 - 300, 4500 + M.MOD_L + 300, M.CL]
for i in range(len(xs_) - 1):
    dim_h(P((xs_[i], 0, 0))[0], P((xs_[i + 1], 0, 0))[0], yA, fn(xs_[i + 1] - xs_[i]), yt, yt, size=3.0)
# tanda potongan C-C pada tampak samping
xc_ = Q((1500, 0, 0))[0]
for yy_, dd in ((Q((0, 0, M.CH))[1] - 3, -1), (yg + 16.5, 1)):
    with own(('cutC', yy_)):
        L([(xc_, yy_), (xc_, yy_ + dd * 4)], .7, None, 'inst')
    TC(xc_ - 3.5, yy_ + dd * 2, "C", 3.5, 'm')
# ---------------- balon
items = [(1, "MB-301", "Modul UF tubular \u00d8220 x 3000, 30 m\u00b2", "%d (+%d cad.)" % (M.EQ["membrane"]["modules"], 40 - M.EQ["membrane"]["modules"]), ('B', (2400, 0, 1700), 90)),
         (2, "-", "Rak modul baja galvanis 2 bank", "2", ('B', (4500 + 3240, 0, 2000), 90)),
         (3, "P-301A/B", "Pompa cross-flow %s m\u00b3/jam, 30 kW" % fn(M.EQ["membrane"]["loop_m3h"]), "2", ('B', (8900, 0, 600), 90)),
         (4, "P-302", "Pompa permeat, VSD", "1", ('A', (10400, 600, 0), -90)),
         (5, "TK-302", "Tangki CIP \u00d81600 x 1800, 4 m\u00b3", "1", ('B', (10900, 0, 2150), 90)),
         (6, "P-304", "Pompa CIP", "1", ('A', (10350, 1650, 0), 90)),
         (7, "-", "Panel MCC + PLC membran", "1", ('B', (700, 0, 2200), 90)),
         (8, "-", "Header umpan / retentat DN150", "4", ('A', (900 - 160, 300, 0), -90)),
         (9, "-", "Header permeat DN80", "2", ('A', (900 + 1500, 300 + 5 * 270 + 120, 0), 120)),
         (10, "-", "Nosel dinding ke reaktor (DN150/80)", "3", ('B', (0, 0, 900), 180))]
for num, tg, ds, q, (vw_, p, pr) in items:
    auto_balloon(num, (A if vw_ == 'A' else B).P(p), pref=pr, rmin=9, rmax=60)
# ---------------- POTONGAN C-C: modul UF (19 tabung PVDF) 1:4
mod0 = [s_ for n, s_, c in full if n in ("MB-301-modul-00", "MB-301-tabung-00")]
z00 = 160 + 300; y00 = 380
SCc = 4.0
Cc = View((1, 0, 0), (0, 1, 0), SCc, 0, 0, origin=(1500, y00, z00), name='potC')
Cc.ox, Cc.oy = 70, 222
Cc.section(mod0, (1500, y00, z00), hatch_sp=1.0, ang=45, draw_rest=False)
kd.OPEN_VIEWS.add('potC')
pc = Cc.P((1500, y00, z00))
cl((pc[0] - 32, pc[1]), (pc[0] + 32, pc[1])); cl((pc[0], pc[1] - 32), (pc[0], pc[1] + 32))
dim_h(Cc.P((0, y00 - 110, 0))[0], Cc.P((0, y00 + 110, 0))[0], pc[1] - 32, "Ø220", pc[1] - 27.5, pc[1] - 27.5, size=3.0)
auto_leader(Cc.P((1500, y00 + 42, z00)), "TABUNG PVDF Ø32 x 19", pref=-20, rmin=8, rmax=30, size=3.0)
pr_ = Cc.P((1500, y00 + 76, z00 - 76)); leader(pr_[0], pr_[1], pr_[0] + 9, pr_[1] + 5, "RUMAH PVC-U t6", 3.0, "l")
auto_leader(Cc.P((1500, y00 + 21, z00 + 36)), "PITCH 42", pref=30, rmin=8, rmax=30, size=3.0)
vlabel(pc[0], pc[1] + 30, "POTONGAN C-C (MODUL UF)", "1:4", size=3.5)
# ---------------- daftar bagian (bahan + massa)
mat = {1: ("PVDF/PVC-U", "%d" % (34 * 62)), 2: ("S275 galv.", "1450"), 3: ("CF8M, 30 kW", "2x520"), 4: ("CF8M, 5,5 kW", "140"),
       5: ("SS304", "380"), 6: ("CF8M, 4 kW", "110"), 7: ("IP54, VSD", "650"), 8: ("SS316L Sch10S", "4x60"), 9: ("PVC-U PN10", "2x15"), 10: ("SS316L", "3x25")}
short = {1: "Modul UF tubular Ø220x3000, 30 m²", 2: "Rak modul 2 bank", 3: "Pompa cross-flow %s m³/jam" % fn(M.EQ["membrane"]["loop_m3h"]),
         4: "Pompa permeat", 5: "Tangki CIP 4 m³", 6: "Pompa CIP", 7: "Panel MCC + PLC", 8: "Header umpan/retentat DN150",
         9: "Header permeat DN80", 10: "Nosel dinding DN150/80"}
rows = [[n, t, short[n], mat[n][0], q.split(" ")[0], mat[n][1]] for n, t, ds, q, p in items]
rows += [[11, "-", "Kontainer ISO 40 ft HC", "Corten, insul.", "1", "4200"], [12, "-", "Pipa, katup, kabel, CIP", "-", "1 lot", "900"]]
yb_ = table(262, 104, [("No", 7, 'm'), ("Tag", 18, 'm'), ("Uraian", 55, 'l'), ("Bahan", 32, 'l'), ("Jml", 12, 'm'), ("kg", 22, 'm')], rows, "DAFTAR BAGIAN", rh=4.4, size=2.5, hsize=2.6)
T(262, yb_ + 4.5, "Total kering ± 12,1 t; transport ± 16 t (berisi air uji).", 3.0, 'l')
# ---------------- isometri potong
image("PM-4-potong_iso-potong.png", 262, 14, 146, 80, name='ISO')
TC(335, 98, "ISOMETRI POTONG (TANPA SKALA)", 3.5, 'm')
note(122, 198, ["1. 2 bank x 5 kolom x 4 tingkat (40 posisi),", "   34 terpasang + 6 cadangan.",
                "2. Fluks %s LMH, luas %s m², cross-flow 4 m/s." % (fn(M.EQ["membrane"]["flux"]), fn(M.EQ["membrane"]["area_m2"])),
                "3. Lorong servis 850 mm di sisi pompa.", "4. Dinding kiri & atap dilepas untuk kejelasan.",
                "5. CIP: NaOCl 500 ppm + asam sitrat 2 %, tiap 30 hari."], 3.0)
finish("BG-M-004")
