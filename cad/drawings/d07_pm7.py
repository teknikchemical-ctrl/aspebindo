# -*- coding: utf-8 -*-
"""Lembar 7: PM-7 Penampung gas membran ganda GH-301 + flare tertutup FL-301."""
from dcommon import *
import bgmodels as M
import math

frame(7, "PM-7 Penampung Gas GH-301\n+ Flare Tertutup FL-301", "BG-M-007", "1:150 / 1:60", "Assembly Drawing")
gh, Dg, hgh = M.gasholder()
fl = M.flare()
EQ = M.EQ
# ---------------- potongan GH 1:150
S = View((0, -1, 0), (1, 0, 0), 150.0, 85, 118, name='ghpot')
S.section([s for n, s, c in gh], (0, 0, 0), hatch_sp=1.6, ang=45, draw_rest=True); kd.OPEN_VIEWS.add('ghpot')
P = S.P
xl, xr = P((-Dg / 2 - 400, 0, 0))[0], P((Dg / 2 + 400, 0, 0))[0]; yg = P((0, 0, 0))[1]
cl(P((0, 0, -500)), P((0, 0, hgh + 1500)))
dim_h(P((-Dg / 2, 0, 0))[0], P((Dg / 2, 0, 0))[0], yg + 8, "Ø" + fn(Dg), yg, yg)
dim_v(yg, P((0, 0, 500 + hgh))[1], xl - 8, fn(500 + hgh), xl, xl)
vlabel((xl + xr) / 2, yg + 14, "POTONGAN A-A  GH-301", "1:150")
# ---------------- denah GH 1:150
A = View((0, 0, 1), (1, 0, 0), 150.0, 85, 205, name='ghdenah')
A.draw([s for n, s, c in gh], hidden=False, w=.35); kd.OPEN_VIEWS.add('ghdenah')
c = A.P((0, 0, 0))
cl((c[0] - 54, c[1]), (c[0] + 54, c[1])); cl((c[0], c[1] - 52), (c[0], c[1] + 52))
cutplane = lambda: None
for s_ in (-1, 1):
    x = c[0] + s_ * 58
    with own(('cut', s_)):
        L([(x - 3 * s_, c[1]), (x + 2 * s_, c[1])], .7, None, 'inst')
    TC(x + 2 * s_ + (3 if s_ > 0 else -3), c[1] - 3, "A", 3.5, 'm')
vlabel(c[0] + 30, c[1] + 54, "DENAH GH-301", "1:150")
# ---------------- FL-301 elevasi 1:60
F = View((0, -1, 0), (1, 0, 0), 60.0, 200, 160, name='flare')
F.draw([s for n, s, c in fl], hidden=True, w=.4); kd.OPEN_VIEWS.add('flare')
fx0, fx1 = F.P((-1250, 0, 0))[0], F.P((1250, 0, 0))[0]; fy = F.P((0, 0, 0))[1]
dim_h(fx0, fx1, fy + 8, "2500", fy, fy)
dim_v(fy, F.P((0, 0, 258 + 6500))[1], fx1 + 10, fn(258 + 6500), fx1, fx1)
dim_h(F.P((-700, 0, 0))[0], F.P((700, 0, 0))[0], F.P((0, 0, 258 + 6500))[1] - 8, "Ø1400", F.P((0, 0, 6758))[1], F.P((0, 0, 6758))[1])
vlabel((fx0 + fx1) / 2, fy + 14, "FL-301 (ELEVASI)", "1:60")
# ---------------- tabel data + isometri
V_ = math.pi * hgh ** 2 * (3 * ((Dg ** 2 / 4 + hgh ** 2) / (2 * hgh)) - hgh) / 3 * 1e-9
rows = [["GH-301", "Volume gas berguna", "%s m³ (± %.0f jam P95)" % (fn(EQ["gas_holder"]["V_m3"]), EQ["gas_holder"]["hours"])],
        ["", "Volume kubah total", "%s m³, Ø%s x %s m" % (fn(V_), fn(Dg / 1000, 1), fn(hgh / 1000, 1))],
        ["", "Membran luar / dalam", "PVC-poliester 1100 g/m² / PE kedap metana"],
        ["", "Tekanan operasi", "2 - 3 mbar(g), blower udara penyangga"],
        ["", "Pondasi", "Cincin beton Ø%s, lantai beton 300 mm" % fn(Dg + 800)],
        ["", "Pengiriman", "membran terlipat di 1 kontainer 20 ft"],
        ["FL-301", "Kapasitas", "%s Nm³/jam, suhu nyala ≥ 1000 °C" % fn(EQ["flare"]["cap_Nm3_h"])],
        ["", "Tipe", "Flare tertutup, pilot otomatis, skid 2,5 x 2,5 m"]]
table(240, 124, [("Tag", 18, 'm'), ("Parameter", 44, 'l'), ("Nilai", 106, 'l')], rows, "DATA DESAIN", rh=4.8, size=2.6, hsize=2.6)
image("PM-7_iso-depan.png", 240, 16, 168, 92, name='ISO')
TC(324, 112, "ISOMETRI (TANPA SKALA)", 3.5, 'm')
note(240, 182, ["1. Membran luar dijaga tegang oleh blower udara penyangga.", "2. Membran dalam naik-turun sesuai isi gas (LIC-401).",
                "3. Flare menyala otomatis saat GE berhenti / GH penuh (PIC-407).", "4. Jarak aman GH ke flare ≥ 15 m (lihat tata letak BG-GA-001)."], 3.0)
for lab_, pt, pr, V__ in (("MEMBRAN LUAR", (-Dg / 2 * .55, 0, 500 + hgh * .82), 150, S), ("MEMBRAN DALAM (GAS)", (Dg / 2 * .2, 0, 500 + 250 + hgh * .55 - 120), 30, S),
                          ("PONDASI BETON", (Dg / 2 + 100, 0, 250), -30, S), ("BLOWER PENYANGGA", (Dg / 2 + 900, 0, 900), 20, S),
                          ("PILOT + BURNER", (0, 0, 1150), 160, F), ("KISI UDARA", (700, 0, 800), 10, F)):
    auto_leader(V__.P(pt), lab_, pref=pr, rmin=8, rmax=60, size=3.0)
finish("BG-M-007")
