# -*- coding: utf-8 -*-
"""Lembar 6: PM-8 Kontainer CHP 40 ft HC (GE-401/402) + PM-9 HX-401 + ST-401."""
from dcommon import *
import bgmodels as M

frame(6, "PM-8 Kontainer CHP 800 kWe\n+ HX-401 / ST-401 (PM-9)", "BG-M-008", "1 : 75", "Assembly Drawing")
SC = 75.0
full = M.pm8()
elev_sh = [s for n, s, c in full if not any(e in n for e in ("-dinding-left", "-rib-left", "-pintu-samping", "-rib-right", "-louvre", "-sirip", "-dinding-right"))]
plan_sh = [s for n, s, c in full if not any(e in n for e in ("-atap", "-rib-", "-louvre", "-sirip", "-cetakan", "radiator", "silencer"))]
# ---------------- tampak depan
B = View((0, -1, 0), (1, 0, 0), SC, 58, 172, name='depan')
B.draw(elev_sh, hidden=False, w=.35); kd.OPEN_VIEWS.add('depan')
Q = B.P
x0, x1 = Q((-2300, 0, 0))[0], Q((M.CL, 0, 0))[0]; xc0 = Q((0, 0, 0))[0]; yg = Q((0, 0, 0))[1]
dim_h(xc0, x1, yg + 8, fn(M.CL), yg, yg)
dim_h(x0, xc0, yg + 8, "2300", yg, yg)
ztop = 2400 + 7500
dim_v(yg, Q((0, 0, ztop))[1], x0 - 10, fn(ztop), x0, x0)
dim_v(yg, Q((0, 0, M.CH + 1100 + 120))[1], x1 + 10, fn(M.CH + 1220), x1, x1)
vlabel((x0 + x1) / 2, yg + 14, "TAMPAK DEPAN (DINDING DILEPAS)", "1:75")
# ---------------- denah
A = View((0, 0, 1), (1, 0, 0), SC, 58, 232, name='denah')
A.draw(plan_sh, hidden=False, w=.35); kd.OPEN_VIEWS.add('denah')
P = A.P
yb, yt = P((0, 0, 0))[1], P((0, M.CW, 0))[1]
dim_v(yt, yb, x1 + 10, fn(M.CW), x1, x1)
vlabel((x0 + x1) / 2, yb + 3, "DENAH (ATAP DILEPAS)", "1:75")
# ---------------- tampak ujung (sisi pintu, dari timur) 1:75
Cn = View((1, 0, 0), (0, 1, 0), SC, 266, 96, name='ujung')
Cn.draw([s_ for n, s_, c in full if not n.startswith(("HX-401", "ST-401", "pipa-buang", "pipa-HW"))], hidden=False, w=.35); kd.OPEN_VIEWS.add('ujung')
ux0, ux1 = Cn.P((0, 0, 0))[0], Cn.P((0, M.CW, 0))[0]; uyg = Cn.P((0, 0, 0))[1]
dim_h(ux0, ux1, uyg + 7, fn(M.CW), uyg, uyg, size=3.0)
dim_v(uyg, Cn.P((0, 0, M.CH))[1], ux1 + 8, fn(M.CH), ux1, ux1, size=3.0)
vlabel((ux0 + ux1) / 2 + 4, uyg + 11, "TAMPAK UJUNG", "1:75", size=3.5)
# ---------------- tabel + isometri
EQ = M.EQ
items = [(1, "GE-401", "Mesin gas V-12, %s kWe, ηel %s %%" % (fn(EQ["chp"]["unit_kWe"]), fn(EQ["chp"]["eta_el_nom"] * 100, 1)), "1", ('B', (3500, 0, 1400), 90)),
         (2, "-", "Generator sinkron 400 V, 50 Hz", "1", ('B', (6600, 0, 1200), 90)),
         (3, "-", "Rangka dasar + peredam getar", "1", ('B', (5000, 0, 280), -90)),
         (4, "-", "Radiator / dump cooler 3 kipas", "1", ('B', (9000, 0, M.CH + 600), 90)),
         (5, "-", "Silencer gas buang Ø900 x 3200", "1", ('B', (3300, 0, M.CH + 700), 90)),
         (6, "HX-401", "Pemulih panas gas buang + jaket, %s kWth" % fn(M.R["energy"]["Q_heat_avail"]), "1", ('B', (-1600, 0, 1200), 180)),
         (7, "ST-401", "Cerobong Ø600, tinggi 9,9 m", "1", ('B', (-1600, 0, 7000), 150)),
         (8, "-", "Panel kontrol + sinkronisasi", "1", ('A', (11250, 1200, 0), -90)),
         (9, "-", "Katup gas train + pengatur tekanan", "1", ('A', (850, 1900, 0), 90)),
         (10, "-", "Pipa air panas HWS/HWR DN80", "2", ('A', (-400, 900, 0), -90))]
SH = {1: ("Mesin gas V-12, %s kWe" % fn(EQ["chp"]["unit_kWe"]), "blok besi cor", "7800"), 2: ("Generator sinkron 400 V 50 Hz", "IP23, H", "3100"),
      3: ("Rangka dasar + peredam", "S355 + karet", "1400"), 4: ("Radiator / dump cooler", "Al/Cu, 3 kipas", "1250"), 5: ("Silencer Ø900x3200", "CS, 35 dB(A)", "650"),
      6: ("Pemulih panas gas buang", "SS316L/CS", "1900"), 7: ("Cerobong Ø600 x 9,9 m", "CS galv.", "850"), 8: ("Panel kontrol + sinkron", "IP54, 1600 A", "900"),
      9: ("Gas train + regulator", "DN100, ATEX", "260"), 10: ("Pipa HWS/HWR DN80", "CS Sch40 insul.", "2x60")}
rows = [[n, t, SH[n][0], SH[n][1], q, SH[n][2]] for n, t, ds, q, p in items] + [[11, "-", "Kontainer 40 ft HC, 75 dB(A)", "Corten + insul.", "1", "5200"]]
yb_ = table(262, 118, [("No", 7, 'm'), ("Tag", 17, 'm'), ("Uraian", 56, 'l'), ("Bahan", 34, 'l'), ("Jml", 10, 'm'), ("kg", 22, 'm')], rows, "DAFTAR BAGIAN (PER UNIT)", rh=4.4, size=2.5, hsize=2.6)
ch = M.R["energy"]["chp"]
gd = [["Daya listrik terpasang / operasi", "%s kWe / %s kWe (beban %s %%)" % (fn(EQ["chp"]["unit_kWe"]), fn(ch["P_el"] / ch["n_run"]), fn(ch["load"] * 100))],
      ["Efisiensi listrik (beban parsial)", "%s %%" % fn(ch["eta_el"] * 100, 1)],
      ["Bahan bakar per unit", "%s kW (LHV)" % fn(ch["burned_kW"] / ch["n_run"])],
      ["Panas pulih (jaket + gas buang)", "%s kWth" % fn((ch["Q_jacket"] + ch["Q_exh"]) / ch["n_run"])],
      ["Suhu gas buang masuk HX / cerobong", "%s °C / 150 °C" % fn(ch["T_exh"])],
      ["Emisi (Permen LHK 11/2021)", "NOx ≤ 500, CO ≤ 1000 mg/Nm³"]]
yd_ = table(262, yb_ + 3, [("Data genset", 60, 'l'), ("Nilai", 86, 'l')], gd, "DATA KINERJA GE-401", rh=4.4, size=2.5, hsize=2.6)
image("PM-8_iso-depan.png", 316, 16, 92, 88, name='ISO')
TC(362, 110, "ISOMETRI (TANPA SKALA)", 3.5, 'm')
note(262, yd_ + 6, ["1. Dua unit identik GE-401 / GE-402 (2 kontainer).", "2. Bahan bakar: biogas H₂S ≤ 50 ppm dari PM-6.",
                "3. HX-401 & ST-401 dikirim sebagai skid PM-9.", "4. Massa angkut ± 24 t per kontainer."], 3.0)
for num, tg, ds, q, (vw_, p, pr) in items:
    auto_balloon(num, (A if vw_ == 'A' else B).P(p), pref=pr, rmin=9, rmax=60)
finish("BG-M-008")
