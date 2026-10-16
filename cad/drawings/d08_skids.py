# -*- coding: utf-8 -*-
"""Lembar 8: skid kecil - PM-5 dosing + pompa umpan, PM-9 menara pendingin CT-601, PM-10 skid lumpur."""
from dcommon import *
import bgmodels as M

frame(8, "Skid PM-5, PM-9 dan PM-10\n(Dosing, CT-601, Lumpur)", "BG-M-005", "1 : 60", "Assembly Drawing")
SC = 60.0
EQ = M.EQ
def col(parts, ox, oyF, oyP, name, Lx, Ly, labels_F, labels_P, title):
    sh = [s for n, s, c in parts]
    F = View((0, -1, 0), (1, 0, 0), SC, ox, oyF, name=name + 'F'); F.draw(sh, hidden=False, w=.35); kd.OPEN_VIEWS.add(name + 'F')
    Pv = View((0, 0, 1), (1, 0, 0), SC, ox, oyP, name=name + 'P'); Pv.draw(sh, hidden=False, w=.35); kd.OPEN_VIEWS.add(name + 'P')
    x0, x1 = F.P((0, 0, 0))[0], F.P((Lx, 0, 0))[0]; yg = F.P((0, 0, 0))[1]
    dim_h(x0, x1, yg + 7, fn(Lx), yg, yg)
    yb, yt = Pv.P((0, 0, 0))[1], Pv.P((0, Ly, 0))[1]
    dim_v(yt, yb, x0 - 7, fn(Ly), x0, x0)
    TC((x0 + x1) / 2, yg + 15, title, 3.8, 'm')
    TC((x0 + x1) / 2, yb + 6, "DENAH  1:60", 3.0, 'm')
    return F, Pv, (x0, x1, yg, yb)
p5 = M.pm5(); p9 = M.pm9_ct(); p10 = M.pm10()
F5, P5, b5 = col(p5, 26, 88, 166, 'pm5', M.L20, M.CW, [], [], "PM-5 TAMPAK DEPAN 1:60")
F9, P9, b9 = col(p9, 168, 95, 182, 'pm9', 4200, 3400, [], [], "PM-9 TAMPAK DEPAN 1:60")
F10, P10, b10 = col(p10, 284, 88, 166, 'pm10', M.L20, M.CW, [], [], "PM-10 TAMPAK DEPAN 1:60")
# tinggi
dim_v(b5[2], F5.P((0, 0, 258 + 1600 + 380))[1], b5[1] + 11, fn(258 + 1600 + 380), b5[1], b5[1])
dim_v(b9[2], F9.P((0, 0, 258 + 3200 + 900 + 300))[1], b9[1] + 9, fn(258 + 4400), b9[1], b9[1])
dim_v(b10[2], F10.P((0, 0, 258 + 1300 + 600))[1], b10[1] + 7, fn(258 + 1900), b10[1], b10[1])
# isometri
image("PM-5_iso-depan.png", 14, 190, 96, 56, name='ISO5')
image("PM-9_iso-depan.png", 114, 190, 52, 56, name='ISO9')
image("PM-10_iso-depan.png", 178, 190, 80, 52, name='ISO10')
TC(62, 250, "ISOMETRI PM-5", 3.0, 'm'); TC(140, 250, "ISOMETRI PM-9", 3.0, 'm'); TC(214, 246, "ISOMETRI PM-10", 3.0, 'm')
bom = [["PM-5", "TK-201/202", "Tangki NaOH / urea (siaga) 2 m³", "HDPE + bund", "2x260"], ["", "P-201A/B", "Pompa umpan reaktor", "CF8M, 7,5 kW", "2x260"],
       ["", "P-203/204", "Pompa dosing", "PVDF, 0,37 kW", "2x45"], ["", "-", "Panel dosing + skid 20 ft", "IP65 / S275", "2080"],
       ["PM-9", "CT-601", "Menara pendingin %s kWth" % fn(EQ["cooling_tower"]["duty_kW"]), "FRP, 7,5 kW", "2900"], ["", "P-601", "Pompa air pendingin", "GG25, 11 kW", "210"],
       ["", "-", "Skid 4200 x 3400", "S275 galv.", "1500"], ["PM-10", "P-501", "Pompa umpan press (PC)", "CS/NBR, 4 kW", "380"],
       ["", "PR-501", "Screw press lumpur", "SS304, 5,5 kW", "2600"], ["", "TK/P-polimer", "Tangki + pompa polimer 1 m³", "HDPE / PVDF", "160"],
       ["", "-", "Skid 20 ft + chute kue", "S275 galv.", "1900"]]
table(262, 180, [("Skid", 14, 'm'), ("Tag", 24, 'm'), ("Uraian", 52, 'l'), ("Bahan / daya", 34, 'l'), ("kg", 22, 'm')], bom, "DAFTAR BAGIAN SKID", rh=4.4, size=2.5, hsize=2.6)
# label komponen (rujukan)
for V_, pt, t, pr in ((F5, (1050, 0, 258 + 1400), "TK-201 NaOH 2 m³", 120), (F5, (2650, 0, 258 + 1400), "TK-202 UREA (SIAGA)", 70),
                      (P5, (4300, 700, 0), "P-201A/B", -60), (P5, (1500, 1700, 0), "P-203", 120), (P5, (3100, 1700, 0), "P-204", 70),
                      (F9, (2100, 0, 258 + 3600), "CT-601 %s kWth" % fn(EQ["cooling_tower"]["duty_kW"]), 60), (P9, (3600, 3800, 0), "P-601", 20),
                      (F10, (3300, 0, 258 + 1150), "PR-501 SCREW PRESS", 60), (P10, (950, 600, 0), "P-501", -90), (P10, (5400, 500, 0), "TK-POLIMER", -60)):
    auto_leader(V_.P(pt), t, pref=pr, rmin=8, rmax=55, size=3.0)
finish("BG-M-005")
