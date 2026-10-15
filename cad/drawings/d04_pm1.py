# -*- coding: utf-8 -*-
"""Lembar 4: PM-1 Skid praolah POME 40 ft (SC-101, P-101A/B, HC-101, E-101)."""
from dcommon import *
import bgmodels as M

frame(4, "PM-1 Skid Praolah POME\n(SC-101, HC-101, E-101)", "BG-M-001", "1 : 60", "Assembly Drawing")
SC = 60.0
full = M.pm1()
allsh = [s for n, s, c in full]
z0 = 258
# ---------------- denah
A = View((0, 0, 1), (1, 0, 0), SC, 40, 72, name='denah')
A.draw([s for n, s, c in full if not n.startswith("rel-")], hidden=False, w=.35)
kd.OPEN_VIEWS.add('denah')
P = A.P
x0, x1 = P((0, 0, 0))[0], P((M.CL, 0, 0))[0]; yb, yt = P((0, 0, 0))[1], P((0, M.CW, 0))[1]
dim_v(yt, yb, x1 + 9, fn(M.CW), x1, x1)
vlabel((x0 + x1) / 2, yb + 6, "DENAH", "1:60")
# ---------------- tampak depan
B = View((0, -1, 0), (1, 0, 0), SC, 40, 172, name='depan')
B.draw(allsh, hidden=False, w=.35)
kd.OPEN_VIEWS.add('depan')
Q = B.P
yg = Q((0, 0, 0))[1]
dim_h(x0, x1, yg + 8, fn(M.CL), yg, yg)
zt = z0 + 2200 + 600
dim_v(yg, Q((0, 0, zt))[1], x0 - 9, fn(zt), x0, x0, out=True, side=-1)
dim_v(yg, Q((0, 0, z0))[1], x1 + 12, fn(z0), x1, x1, out=True, side=1)
vlabel((x0 + x1) / 2, yg + 14, "TAMPAK DEPAN", "1:60")
# ---------------- tampak ujung
C = View((1, 0, 0), (0, 1, 0), SC, 278, 172, name='ujung')
C.draw(allsh, hidden=False, w=.35)
cx0, cx1 = C.P((0, 0, 0))[0], C.P((0, M.CW, 0))[0]
dim_h(cx0, cx1, C.P((0, 0, 0))[1] + 8, fn(M.CW), C.P((0, 0, 0))[1], C.P((0, 0, 0))[1])
vlabel((cx0 + cx1) / 2, C.P((0, 0, 0))[1] + 14, "TAMPAK UJUNG", "1:60")
# chain dimensi posisi alat (tampak depan, atas)
ytop_ = Q((0, 0, zt))[1] - 7
xs_ = [0, 400, 3400, 5650, 7400, 10600, M.CL]
for i in range(len(xs_) - 1):
    dim_h(Q((xs_[i], 0, 0))[0], Q((xs_[i + 1], 0, 0))[0], ytop_, fn(xs_[i + 1] - xs_[i]), Q((0, 0, zt - 300))[1], Q((0, 0, zt - 300))[1], size=3.0)
# ---------------- balon
EQ = M.EQ
items = [(1, "SC-101", "Saringan drum putar Ø900 x 2600, celah 0,75 mm, %s m³/jam" % fn(EQ["screen"]["flow_m3h"], 1), "1", ('B', (1900, 0, z0 + 2000), 90)),
         (2, "-", "Bak sump 3 m³ di bawah saringan", "1", ('B', (300, 0, z0 + 500), 180)),
         (3, "P-101A/B", "Pompa umpan desander, H 20 m, VSD", "2", ('A', (4450, 600, 0), -90)),
         (4, "HC-101", "Hidrosiklon desander 2 x Ø300", "2", ('B', (6000, 0, z0 + 2200), 90)),
         (5, "-", "Bak pasir (grit bin) 0,4 m³", "1", ('A', (6100, 1220, 0), 90)),
         (6, "E-101", "Pendingin POME pelat %s kWth, SS316" % fn(EQ["pome_cooler"]["duty_kW"]), "1", ('B', (8100, 0, z0 + 1600), 90)),
         (7, "-", "Panel kontrol lokal", "1", ('A', (11000, 500, 0), -90)),
         (8, "-", "Skid baja UNP 250, 12192 x 2438", "1", ('B', (11500, 0, 120), -60)),
         (9, "-", "Pegangan tangan Ø42,4", "1", ('B', (2000, 0, z0 + 1100), -110))]
for num, tg, ds, q, (vw_, p, pr) in items:
    auto_balloon(num, (A if vw_ == 'A' else B).P(p), pref=pr, rmin=9, rmax=60)
SH = {1: ("Saringan drum Ø900x2600, 0,75 mm", "SS304", "1450"), 2: ("Bak sump 3 m³", "SS304 t4", "620"), 3: ("Pompa desander H 20 m, VSD", "CD4MCu, 11 kW", "2x310"),
      4: ("Hidrosiklon Ø300", "PU-lined CS", "2x140"), 5: ("Bak pasir 0,4 m³", "S275 galv.", "180"), 6: ("PHE %s kWth" % fn(EQ["pome_cooler"]["duty_kW"]), "SS316/EPDM", "1850"),
      7: ("Panel kontrol lokal", "IP65", "220"), 8: ("Skid UNP 250 12192x2438", "S275, cat", "3900"), 9: ("Pegangan tangan Ø42,4", "S275 galv.", "240")}
rows = [[n, t, SH[n][0], SH[n][1], q, SH[n][2]] for n, t, ds, q, p in items]
rows.append([10, "-", "Pipa, katup, kabel", "SS304 / PVC", "1 lot", "1100"])
yb_ = table(22, 200, [("No", 8, 'm'), ("Tag", 18, 'm'), ("Uraian", 58, 'l'), ("Bahan", 30, 'l'), ("Jml", 14, 'm'), ("kg", 18, 'm')], rows, "DAFTAR BAGIAN", rh=4.4, size=2.5, hsize=2.6)
cons = [["N-A", "DN150", "POME panas masuk (85 °C)", "PKS → SC-101"], ["N-B", "DN100", "POME tersaring ke TK-101", "E-101 → TK-101"],
        ["N-C", "DN80", "Air pendingin masuk / keluar", "CT-601 ↔ E-101"], ["N-D", "DN50", "Underflow pasir", "HC-101 → bak"],
        ["N-E", "-", "Daya 400 V, 3 fasa, 45 kVA", "MCC → panel"]]
table(262, 202, [("Tag", 14, 'm'), ("Ukuran", 16, 'm'), ("Layanan", 66, 'l'), ("Dari → ke", 50, 'l')], cons, "SAMBUNGAN SKID", rh=4.4, size=2.5, hsize=2.6)
image("PM-1_iso-depan.png", 262, 16, 146, 92, name='ISO')
TC(335, 112, "ISOMETRI (TANPA SKALA)", 3.5, 'm')
note(316, 128, ["1. Seluruh alat dirakit & diuji di bengkel.", "2. Pengiriman: 1 truk trailer 40 ft, ± 12 t.",
                "3. Sambungan: POME masuk DN150 (kiri),", "   POME keluar DN100 ke TK-101 (kanan)."], 3.0)
finish("BG-M-001")
