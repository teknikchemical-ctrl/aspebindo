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
C = View((1, 0, 0), (0, 1, 0), SC, 250, 160, name='ujung')
C.draw(pick(("-rib-", "-louvre", "-sirip")), hidden=False, w=.35)
cx0, cx1 = C.P((0, 0, 0))[0], C.P((0, M.CW, 0))[0]
dim_h(cx0, cx1, C.P((0, 0, 0))[1] + 7, fn(M.CW), C.P((0, 0, 0))[1], C.P((0, 0, 0))[1])
vlabel((cx0 + cx1) / 2, C.P((0, 0, 0))[1] + 12, "TAMPAK UJUNG", "1:60")
# ---------------- balon
items = [(1, "MB-301", "Modul UF tubular \u00d8220 x 3000, 30 m\u00b2", "%d (+%d cad.)" % (M.EQ["membrane"]["modules"], 40 - M.EQ["membrane"]["modules"]), ('B', (2400, 0, 1700), 90)),
         (2, "-", "Rak modul baja galvanis 2 bank", "2", ('B', (4500 + 3240, 0, 2000), 90)),
         (3, "P-301A/B", "Pompa cross-flow %s m\u00b3/jam, 30 kW" % fn(M.EQ["membrane"]["loop_m3h"]), "2", ('B', (8900, 0, 600), 90)),
         (4, "P-302", "Pompa permeat, VSD", "1", ('A', (10400, 600, 0), -90)),
         (5, "TK-302", "Tangki CIP \u00d81600 x 1800, 4 m\u00b3", "1", ('B', (10900, 0, 2150), 90)),
         (6, "P-304", "Pompa CIP", "1", ('A', (10350, 1650, 0), 90)),
         (7, "-", "Panel MCC + PLC membran", "1", ('B', (700, 0, 2200), 90)),
         (8, "-", "Header umpan / retentat DN150", "4", ('A', (900 - 160, 300, 0), -90)),
         (9, "-", "Header permeat DN80", "2", ('A', (900 + 1500, 300 + 5 * 270 + 120, 0), 90)),
         (10, "-", "Nosel dinding ke reaktor (DN150/80)", "3", ('B', (0, 0, 900), 180))]
for num, tg, ds, q, (vw_, p, pr) in items:
    auto_balloon(num, (A if vw_ == 'A' else B).P(p), pref=pr, rmin=9, rmax=60)
rows = [[n, t, ds, q] for n, t, ds, q, p in items]
rows += [[11, "-", "Kontainer ISO 40 ft HC, kisi ventilasi + pintu samping", "1"]]
table(22, 196, [("No", 9, 'm'), ("Tag", 22, 'm'), ("Uraian", 92, 'l'), ("Jml", 18, 'm')], rows, "DAFTAR BAGIAN", rh=4.6, size=2.6, hsize=2.6)
# ---------------- isometri potong
image("PM-4-potong_iso-potong.png", 262, 16, 146, 92, name='ISO')
TC(335, 112, "ISOMETRI POTONG (TANPA SKALA)", 3.5, 'm')
note(300, 128, ["1. Modul 2 bank x 5 kolom x 4 tingkat (40 posisi),", "   jarak antar tingkat 520 mm.",
                "2. Fluks rancangan %s LMH, luas total %s m²." % (fn(M.EQ["membrane"]["flux"]), fn(M.EQ["membrane"]["area_m2"])),
                "3. Massa angkut ± 16 t; kontainer ISO 40 ft HC.",
                "4. Lorong servis 850 mm di sisi pompa.", "5. Dinding kiri & atap dilepas pada", "   tampak / denah untuk kejelasan."], 3.0)
finish("BG-M-004")
