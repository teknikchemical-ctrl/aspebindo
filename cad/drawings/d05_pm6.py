# -*- coding: utf-8 -*-
"""Lembar 5: PM-6 Skid pengolahan biogas: kontainer gas 40 ft + BTF-301 (bejana terpisah)."""
from dcommon import *
import bgmodels as M

frame(5, "PM-6 Skid Pengolahan Biogas\n(BTF-301, K-302, AC-301)", "BG-M-006", "1:100 / 1:60", "Assembly Drawing")
full = M.pm6()
plan_sh = [s for n, s, c in full if not any(e in n for e in ("-atap", "-rib-", "-louvre", "-sirip", "-cetakan", "tangga", "anak-tangga"))]
elev_sh = [s for n, s, c in full if not any(e in n for e in ("-dinding-left", "-rib-left", "-pintu-samping", "-rib-right", "-louvre", "-sirip", "-dinding-right", "anak-tangga"))]
# ---------------- denah 1:100
A = View((0, 0, 1), (1, 0, 0), 100.0, 30, 100, name='denah')
A.draw(plan_sh, hidden=False, w=.35); kd.OPEN_VIEWS.add('denah')
P = A.P
x0, x1 = P((0, 0, 0))[0], P((M.CL, 0, 0))[0]; yb = P((0, 0, 0))[1]; ytop = P((0, M.CW + 1200 + 3600, 0))[1]
dim_h(x0, x1, yb + 8, fn(M.CL), yb, yb)
dim_v(yb, ytop, x1 + 10, fn(M.CW + 1200 + 3600), x1, x1, out=True, side=1)
vlabel((x0 + x1) / 2, yb + 14, "DENAH (ATAP DILEPAS)", "1:100")
# ---------------- tampak depan 1:100
B = View((0, -1, 0), (1, 0, 0), 100.0, 30, 222, name='depan')
B.draw(elev_sh, hidden=False, w=.35); kd.OPEN_VIEWS.add('depan')
Q = B.P
yg = Q((0, 0, 0))[1]
htop = 258 + 400 + M.BTF_H + 400 + 350 + 500
dim_v(yg, Q((0, 0, htop))[1], x0 - 14, fn(htop), x0, x0)
dim_v(yg, Q((0, 0, M.CH))[1], x0 - 6, fn(M.CH), x0, x0)
vlabel((x0 + x1) / 2, yg + 4, "TAMPAK DEPAN (DINDING DILEPAS)", "1:100")
# ---------------- BTF-301 elevasi 1:60
bt = M.btf()
Cv = View((0, -1, 0), (1, 0, 0), 60.0, 212, 222, name='btf')
Cv.draw([s for n, s, c in bt if not n.startswith(("P-305", "K-301", "BTF-anak", "BTF-tangga"))], hidden=True, w=.4); kd.OPEN_VIEWS.add('btf')
R_ = M.BTF_D / 2; z0 = 258
cxl, cxr = Cv.P((-R_ - 8, 0, 0))[0], Cv.P((R_ + 8, 0, 0))[0]; yg2 = Cv.P((0, 0, 0))[1]
dim_h(cxl, cxr, yg2 + 8, "Ø" + fn(M.BTF_D) + " ID", yg2, yg2)
dim_v(Cv.P((0, 0, z0 + 400))[1], Cv.P((0, 0, z0 + 400 + M.BTF_H))[1], cxr + 22, fn(M.BTF_H), cxr, cxr)
zz_ = [0, z0 + 400, z0 + 400 + 910, z0 + 400 + 3610, z0 + 400 + 6310, z0 + 400 + M.M_DIST, z0 + 400 + M.BTF_H]
for i in range(len(zz_) - 1):
    dim_v(Cv.P((0, 0, zz_[i]))[1], Cv.P((0, 0, zz_[i + 1]))[1], cxr + 9, fn(zz_[i + 1] - zz_[i]), cxr, cxr, size=3.0, out=(zz_[i + 1] - zz_[i]) < 1000, side=1)
vlabel((cxl + cxr) / 2, yg2 + 14, "BTF-301 (ELEVASI)", "1:60")
# ---------------- balon (denah)
EQ = M.EQ
items = [(1, "BTF-301", "Bio-trickling filter Ø2400 x 8000, media PP %s m³" % fn(EQ["bio_desulfurizer"]["V_m3"], 1), "1", (1800, 5438, 0), 90),
         (2, "P-305", "Pompa resirkulasi nutrien BTF", "1", (1800 + 1500, 5438 - 1500, 0), 0),
         (3, "K-301", "Blower udara BTF %s Nm³/jam" % fn(EQ["bio_desulfurizer"]["air_Nm3_h"], 1), "1", (1800 - 1450, 5438 + 1100, 0), 150),
         (4, "HX-301", "Pendingin gas shell-tube, %s kWth" % fn(EQ["gas_chiller"]["duty_kW"], 1), "1", (1900, 700, 0), -90),
         (5, "CH-301", "Chiller paket berpendingin udara", "1", (1800, 1700, 0), 90),
         (6, "V-301", "KO pot Ø700 + demister", "1", (4200, 800, 0), -90),
         (7, "K-302A/B", "Blower biogas %s m³/jam, ΔP %s kPa" % (fn(EQ["gas_blower"]["flow_m3_h"]), fn(EQ["gas_blower"]["dP_kPa"])), "2", (6300, 1650, 0), 90),
         (8, "AC-301A/B", "Filter karbon aktif Ø1200, 2 bed", "2", (9800, 1219, 0), -90),
         (9, "-", "Panel kontrol + analis gas", "1", (11500, 900, 0), 90),
         (10, "-", "Header gas DN250", "1", (7000, 300, 0), -60)]
for num, tg, ds, q, p, pr in items:
    auto_balloon(num, P(p), pref=pr, rmin=8, rmax=60)
SH = {1: ("Bio-trickling filter Ø2400x8000", "FRP vinilester", "3800"), 2: ("Pompa resirkulasi nutrien", "PP, 1,5 kW", "60"),
      3: ("Blower udara BTF", "Al, 0,75 kW", "45"), 4: ("Pendingin gas shell-tube", "SS316L", "650"), 5: ("Chiller paket", "R-32, 15 kWe", "780"),
      6: ("KO pot Ø700 + demister", "SS304", "210"), 7: ("Blower biogas %s m³/jam" % fn(EQ["gas_blower"]["flow_m3_h"]), "Al, ATEX 18,5 kW", "2x420"),
      8: ("Filter karbon aktif Ø1200", "CS epoksi + KI-AC", "2x1650"), 9: ("Panel kontrol + analis gas", "IP54, ATEX", "380"), 10: ("Header gas DN250", "SS304", "420")}
rows = [[n, t, SH[n][0], SH[n][1], q, SH[n][2]] for n, t, ds, q, p, pr in items] + [[11, "-", "Kontainer 40 ft HC, ATEX z2", "Corten", "1", "4300"], [12, "-", "Skid BTF 3600 + tangga", "S275 galv.", "1", "1650"]]
yb_ = table(262, 124, [("No", 7, 'm'), ("Tag", 19, 'm'), ("Uraian", 56, 'l'), ("Bahan", 32, 'l'), ("Jml", 10, 'm'), ("kg", 22, 'm')], rows, "DAFTAR BAGIAN", rh=4.4, size=2.5, hsize=2.6)
image("PM-6_iso-depan.png", 262, 16, 146, 90, name='ISO')
TC(335, 110, "ISOMETRI (TANPA SKALA)", 3.5, 'm')
noz = [["G1", "DN250", "Gas masuk (bawah)"], ["G2", "DN250", "Gas keluar (puncak)"], ["A1", "DN50", "Udara dari K-301"], ["L1", "DN80", "Resirkulasi ke distributor"],
       ["L2", "DN80", "Sump / blowdown"], ["MH", "DN600", "Lubang orang"]]
table(262, yb_ + 3, [("Tag", 14, 'm'), ("Ukuran", 18, 'm'), ("Layanan BTF-301", 64, 'l')], noz, "NOSEL BTF-301", rh=4.4, size=2.5, hsize=2.6)
note(364, yb_ + 7, ["1. BTF dikirim terpisah", "   di trailer.", "2. H₂S %s → %s ppm." % (fn(M.R["nominal"]["h2s_ppm_raw"]), fn(M.R["nominal"]["h2s_ppm_fuel"])),
                    "3. Kontainer: ventilasi", "   paksa + detektor gas."], 3.0)
tg = Cv.P((-R_ - 350, 0, z0 + 1300)); leader(tg[0], tg[1], tg[0] - 5, tg[1] - 11, "GAS MASUK DN250", 3.0, "r")
tg = Cv.P((-R_ + 250, 0, z0 + 400 + 3600)); leader(tg[0], tg[1], cxl - 8, tg[1] - 8, "UNGGUN MEDIA PP 2 x 2600", 3.0, 'r')
for lab_, pt, pr in (("GAS KELUAR DN250", (0, 0, z0 + 400 + M.BTF_H + 850), 160),
                     ("RESIRKULASI DN80", (-R_ - 340, 0, z0 + M.BTF_H - 300), 200),
                     ("DISTRIBUTOR", (R_ - 300, 0, z0 + 400 + M.M_DIST), 30)):
    auto_leader(Cv.P(pt), lab_, pref=pr, rmin=8, rmax=60, size=3.0)
finish("BG-M-006")
