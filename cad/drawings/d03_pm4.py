# -*- coding: utf-8 -*-
"""Lembar 3 (Rev 2): PM-4 skid kontak - PM-4A degasser vakum DG-301 + pompa resirkulasi, PM-4B settler lamella LS-301
(denah + tampak samping PM-4A, potongan memanjang B-B LS-301 memperlihatkan pelat miring 60° dan corong lumpur, tampak ujung, isometri, daftar bagian)."""
from dcommon import *
import bgmodels as M

frame(3, "PM-4 Skid Kontak\nDG-301 + LS-301", "BG-M-004", "1 : 80", "Assembly Drawing", rev="2")
SC = 80.0
A4 = M.pm4a(); B4 = M.pm4b()
LS = M.EQ["lamella_settler"]
shA = [s for n, s, c in A4]
# ---------------- PM-4A denah + tampak samping
PA = View((0, 0, 1), (1, 0, 0), SC, 24, 50, name='denahA'); PA.draw(shA, hidden=False, w=.35); kd.OPEN_VIEWS.add('denahA')
EA = View((0, -1, 0), (1, 0, 0), SC, 24, 128, name='sampingA'); EA.draw(shA, hidden=False, w=.35); kd.OPEN_VIEWS.add('sampingA')
x0, x1 = EA.P((0, 0, 0))[0], EA.P((M.CL, 0, 0))[0]; yg = EA.P((0, 0, 0))[1]
dim_h(x0, x1, yg + 7, fn(M.CL), yg, yg)
dim_v(PA.P((0, M.CW, 0))[1], PA.P((0, 0, 0))[1], x0 - 7, fn(M.CW), x0, x0)
dim_v(yg, EA.P((0, 0, 258 + 4600 + 400))[1], x1 + 9, fn(258 + 5000), x1, x1, out=True, side=1)
TC((x0 + x1) / 2, PA.P((0, 0, 0))[1] + 6, "PM-4A DENAH  1:80", 3.2, 'm')
TC((x0 + x1) / 2, yg + 15, "PM-4A TAMPAK SAMPING  1:80", 3.5, 'm')
# ---------------- PM-4B potongan memanjang B-B (bidang tengah LS-301)
ymid = 69 + 2300 / 2
B = View((0, -1, 0), (1, 0, 0), SC, 0, 0, origin=(0, ymid, 0), name='potB')
B.ox, B.oy = 36, 238
B.section([s for n, s, c in B4 if n.startswith(("LS-301-badan", "LS-301-pelat-0", "LS-301-pelat-1", "LS-301-talang"))], (0, ymid, 0), hatch_sp=1.2, ang=45, draw_rest=False)
B.draw([s for n, s, c in B4 if not n.startswith(("LS-301-badan", "LS-301-pelat-0", "LS-301-pelat-1", "LS-301-talang", "LS-301-penutup", "LS-301-pelat-nama"))], hidden=False, w=.3)
kd.OPEN_VIEWS.add('potB')
bx0, bx1 = B.P((0, ymid, 0))[0], B.P((M.CL, ymid, 0))[0]; byg = B.P((0, ymid, 0))[1]
zt = 258 + 1500
dim_h(B.P((400, ymid, 0))[0], B.P((7400, ymid, 0))[0], byg + 7, "7000", byg, byg)
dim_v(byg, B.P((0, ymid, zt + 3400))[1], bx0 - 7, fn(zt + 3400), bx0, bx0)
dim_v(byg, B.P((0, ymid, zt))[1], bx0 - 15, fn(zt), bx0, bx0)
TC((bx0 + bx1) / 2, byg + 15, "PM-4B POTONGAN B-B (SETTLER LAMELLA)  1:80", 3.5, 'm')
for lab_, pt, pr in (("PELAT MIRING 60° @80 (%d)" % int((7000 - 1600) // 80), (3900, ymid, zt + 1600), 75), ("CORONG LUMPUR 2x", (2150, ymid, zt - 600), -150),
                     ("TALANG LUAPAN 4x", (6500, ymid, zt + 3200), 45),
                     ("EFLUEN KE TK-301", (7800, ymid, zt + 3000), 20)):
    auto_leader(B.P(pt), lab_, pref=pr, rmin=8, rmax=40, size=3.0)
# ---------------- tampak ujung PM-4B 1:60
C = View((1, 0, 0), (0, 1, 0), 80.0, 212, 222, name='ujungB')
C.draw([s for n, s, c in B4 if "pelat-0" not in n], hidden=False, w=.35); kd.OPEN_VIEWS.add('ujungB')
cx0, cx1 = C.P((0, 0, 0))[0], C.P((0, M.CW, 0))[0]
dim_h(cx0, cx1, C.P((0, 0, 0))[1] + 7, fn(M.CW), C.P((0, 0, 0))[1], C.P((0, 0, 0))[1])
TC((cx0 + cx1) / 2, C.P((0, 0, 0))[1] + 15, "PM-4B UJUNG 1:80", 3.2, 'm')
# ---------------- balon komponen
items = [(1, "DG-301", "Degasser vakum Ø1600 x 4000, 8 m³", "SA-516-70 / epoksi", "1", "1850", (EA, (2200, 0, 258 + 2800), 120)),
         (2, "K-303", "Pompa vakum cincin cair + separator", "CF8M, 5,5 kW", "1", "420", (PA, (4800, 500, 0), 90)),
         (3, "P-301A/B", "Pompa resirkulasi lumpur %s m³/hari" % fn(LS["recycle_m3d"]), "CF8M, 7,5 kW, VSD", "2", "2x560", (PA, (6600, 1450, 0), 60)),
         (4, "P-302", "Pompa umpan settler", "CF8M, 5,5 kW", "1", "430", (PA, (8900, 250, 0), -60)),
         (5, "P-303", "Pompa lumpur buangan -> PM-10", "PC, 3 kW", "1", "260", (PA, (8600, 1450, 0), 60)),
         (6, "-", "Panel MCC + PLC + analis FOS/TAC", "IP54", "1", "820", (EA, (10900, 0, 258 + 1500), 60)),
         (7, "LS-301", "Settler lamella %s m² proyeksi" % fn(LS["A_proj_m2"]), "S275 + epoksi", "1", "6900", (B, (1000, ymid, zt + 3000), 150)),
         (8, "-", "Paket pelat miring 60°, jarak 80 mm", "PP / FRP", "1", "1300", (B, (5000, ymid, zt + 900), -60)),
         (9, "-", "Tangga + platform akses", "S275 galv.", "1", "540", (B, (7400 + 800, ymid, zt + 2000), 30))]
for num, tg, ds, mt, q, kg, (vw_, p, pr) in items:
    auto_balloon(num, vw_.P(p), pref=pr, rmin=9, rmax=60)
rows = [[n, t, ds, mt, q, kg] for n, t, ds, mt, q, kg, _ in items] + [[10, "-", "Skid 40 ft x 2 + perpipaan, katup", "S275 galv.", "2", "2x2600"]]
yb_ = table(262, 104, [("No", 7, 'm'), ("Tag", 18, 'm'), ("Uraian", 62, 'l'), ("Bahan", 30, 'l'), ("Jml", 10, 'm'), ("kg", 19, 'm')], rows, "DAFTAR BAGIAN", rh=4.4, size=2.5, hsize=2.6)
note(262, yb_ + 5, ["1. Proses kontak: reaktor -> DG-301 (vakum -0,3 bar, CH4",
                    "   terlarut kembali ke jalur gas) -> LS-301 -> underflow",
                    "   %s m³/hari kembali ke reaktor (P-301), buangan" % fn(LS["recycle_m3d"]),
                    "   %s m³/hari ke screw press (P-303)." % fn(M.EQ["waste_sludge"]["Qw_m3d"]),
                    "2. Tangkapan padatan %d %%; SRT %s hari." % (round(LS["capture"] * 100), fn(M.R["process_decisions"]["srt_d"])),
                    "3. Masuk LS-301 dari DG-301 di ujung barat (kiri B-B).", "4. Membran AnMBR = opsi PM-11 (tidak termasuk)."], 3.0)
image("PM-4_iso-depan.png", 262, 14, 146, 82, name='ISO')
TC(335, 99, "ISOMETRI PM-4A + PM-4B (TANPA SKALA)", 3.5, 'm')
finish("BG-M-004")
