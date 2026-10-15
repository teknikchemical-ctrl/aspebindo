# -*- coding: utf-8 -*-
"""Lembar 2: Bejana standar / reaktor AnMBR R-201..R-214 (elevasi, orientasi nosel, jadwal nosel, data desain, isometri)."""
from dcommon import *
import bgmodels as M
import math

frame(2, "Reaktor AnMBR Standar\nR-201 s/d R-214", "BG-V-201", "1:80 / 1:60", "Equipment Drawing")
V = M.vessel("reactor", ladder=False)
body = [s for n, s, c in V if not n.startswith(("baut", "kursi", "klading"))]
SC = 80.0
# ---------------- elevasi (dari selatan)
E = View((0, -1, 0), (1, 0, 0), SC, 72, 250, name='elev')
E.draw(body, hidden=True)
kd.OPEN_VIEWS.add('elev')
P = E.P
cl(P((0, 0, -300)), P((0, 0, M.ZT + M.HB + 900)))
xL = P((-M.VR - M.VT, 0, 0))[0]; xR = P((M.VR + M.VT, 0, 0))[0]
y0 = P((0, 0, 0))[1]; ybt = P((0, 0, M.ZB))[1]; ytt = P((0, 0, M.ZT))[1]
ytop = P((0, 0, M.ZT + M.HB - 60 + 600))[1]
dim_v(y0, ytop, xL - 26, fn(M.ZT + M.HB - 60 + 600), xL, xL, tdy=-50)
dim_v(ybt, ytt, xL - 13, "T/T " + fn(M.VH), xL, xL, tdy=30)
dim_v(y0, ybt, xR + 22, fn(M.HS), xR, xR, out=True, side=1)
dim_v(ytt, P((0, 0, M.ZT + M.HB))[1], xR + 22, fn(M.HB), xR, xR, out=True, side=1)
dim_h(xL, xR, y0 + 9, "Ø" + fn(M.VD + 2 * M.VT) + " OD", y0, y0)
# muka cairan normal
yl = P((0, 0, M.ZB + M.LIQ - M.HB))[1]
with own(('nll',)):
    L([(xL - 4, yl), (xR + 4, yl)], .25, [2, 1], 'inst')
    PG([(xR + 6, yl - 2.6), (xR + 9, yl - 2.6), (xR + 7.5, yl - .2)], .25, None, 'inst')
T(xR + 11, yl + 1.2, "NLL", 3.0, 'l')
vlabel((xL + xR) / 2 + 6, y0 + 13.5, "ELEVASI (DARI SELATAN)", "1:80")
# label nosel di elevasi (kiri / kanan otomatis)
for tag, srv, dn, ang, z, proj in M.NOZ:
    if z in ("top", "top2", "top3"): continue
    a = math.radians(ang)
    xr = (M.VR + M.INS + proj) * math.cos(a)
    if abs(math.sin(a)) > .97: continue
    auto_leader(P((xr, 0, z)), tag, pref=0 if xr > 0 else 180, rmin=8, rmax=40, size=3.0)
auto_leader(P((0, 0, M.ZT + M.HB + 520)), "N7", pref=150, rmin=8, rmax=40, size=3.0)
auto_leader(P((1100, 0, M.ZT + M.HB + 600)), "N8 (PVRV)", pref=30, rmin=8, rmax=40, size=3.0)
# ---------------- tampak atas: orientasi nosel (skala 1:60)
S2 = 60.0
A = View((0, 0, 1), (1, 0, 0), S2, 175, 82, name='atas')
Ash = [s for n, s, c in V if n in ("shell", "klading-shell", "cincin-dasar") or n[0] in "NM" and n not in ("N13",)]
A.draw(Ash, hidden=False, w=.4)
kd.OPEN_VIEWS.add('atas')
c = A.P((0, 0, 0))
cl((c[0] - 50, c[1]), (c[0] + 50, c[1])); cl((c[0], c[1] - 50), (c[0], c[1] + 50))
for tag, srv, dn, ang, z, proj in M.NOZ:
    if ang is None: continue
    a = math.radians(ang); rr = M.VR + M.INS + proj
    auto_leader(A.P((rr * math.cos(a), rr * math.sin(a), 0)), "%s  %d°" % (tag, (90 - ang) % 360), pref=math.degrees(a), rmin=6, rmax=34, size=3.0)
# panah utara
nx, ny = c[0] + 58, c[1] + 46
PG([(nx, ny - 7), (nx - 2.2, ny), (nx + 2.2, ny)], .3, '#000000')
TC(nx, ny - 11, "U", 3.5, 'm')
vlabel(c[0], c[1] + 52, "ORIENTASI NOSEL (TAMPAK ATAS)", "1:60")
# ---------------- jadwal nosel
rows = []
for tag, srv, dn, ang, z, proj in M.NOZ:
    el = {"top": "puncak", "top2": "kepala atas", "top3": "kepala atas"}[z] if isinstance(z, str) else fn(z)
    ori = "-" if ang is None else "%d°" % ((90 - ang) % 360)
    rows.append([tag, "DN" + str(dn), "PN10 RF", srv, el, ori])
rows.append(["N13", "DN80", "PN10 RF", "Pengurasan (kepala bawah)", fn(M.ZB - M.HB - 220), "-"])
yt = table(244, 16, [("Tag", 13, 'm'), ("Ukuran", 15, 'm'), ("Rating", 17, 'm'), ("Layanan", 61, 'l'), ("Elev.", 16, 'm'), ("Orient.", 16, 'm')],
           rows, "JADWAL NOSEL", rh=4.6, size=2.6, hsize=2.6)
# ---------------- data desain
mass = M.vessel_mass()
Vg = math.pi * M.VR ** 2 * M.VH * 1e-9 + 2 * (2 / 3) * math.pi * M.VR ** 2 * M.HB * 1e-9
dd = [["Fungsi", "Reaktor AnMBR termofilik (14 unit identik)"],
      ["Kode desain", "API 650 / ASME VIII-1 (acuan), bejana atmosferik"],
      ["Tekanan desain", "+50 / -5 mbar(g) + hidrostatik penuh"],
      ["Suhu desain / operasi", "70 °C / 55 °C"],
      ["Volume total / kerja", "%s m³ / %s m³" % (fn(Vg), fn(M.RV["V_liq_m3"]))],
      ["Bahan shell / kepala", "SA-516-70, %s mm, CA 3 mm, lapisan epoksi" % fn(M.VT)],
      ["Kepala", "Elipsoidal 2:1, %s mm" % fn(M.VT)],
      ["Insulasi", "Mineral wool %s mm + kladding Al 0,8 mm" % fn(M.INS)],
      ["Massa kosong / operasi", "± %s t / ± %s t" % (fn(mass), fn(mass + M.RV["V_liq_m3"] * 1.02))],
      ["Transport", "rebah di low-bed, %s x %s m" % (fn((M.VH + 2 * M.HB) / 1000, 1), fn((M.VD + 2 * M.INS) / 1000, 1))]]
yd = table(244, yt + 4, [("Data desain", 46, 'l'), ("Nilai", 92, 'l')], dd, "DATA DESAIN", rh=4.6, size=2.6, hsize=2.6)
# ---------------- isometri
image("R-201_iso-depan.png", 128, 147, 106, 92, name='ISO')
TC(181, 245.5, "ISOMETRI (TANPA SKALA)", 3.5, 'm')
note(244, yd + 6, ["1. Elevasi diukur dari dasar cincin rok (EL 0).", "2. Orientasi nosel: derajat dari utara, searah jarum jam.",
                   "3. Tangga, sangkar & platform atas: lihat isometri.", "4. Bejana sama dipakai TK-101 / TK-301 (tanpa insulasi & internal).", "5. Header jet internal (6 nosel) ditunjukkan garis tersembunyi."], 3.0)
finish("BG-V-201")
