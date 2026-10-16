# -*- coding: utf-8 -*-
"""Lembar 2 (Rev 2): Reaktor kontak termofilik R-201..R-203 - tangki GFS dibaut: elevasi, orientasi nosel, detail A (nosel menembus
panel + insulasi) dan detail B (ring beam + sudut penahan + angkur), jadwal nosel, data desain, daftar material (massa dari model 3D), isometri."""
from dcommon import *
import bgmodels as M
import math

frame(2, "Reaktor Kontak Termofilik\nR-201 s/d R-203 (GFS)", "BG-V-201", "1:125/1:250/1:20", "Equipment Drawing", rev="2")
V = M.gfs_tank("reactor", ladder=False)
VL = M.gfs_tank("reactor", ladder=True)
R_ = M.TR; Ro = M.TR + M.TP + M.TINS; zt = M.TZ0 + M.THs; hc = 0.25 * M.TD
body = [s for n, s, c in V if not n.startswith(("angkur", "klading-sabuk", "blower", "sensor", "header-jet", "nosel-jet"))]
SC = 125.0
# ---------------- elevasi (dari selatan)
E = View((0, -1, 0), (1, 0, 0), SC, 93, 246, name='elev')
E.draw(body, hidden=True)
kd.OPEN_VIEWS.add('elev')
P = E.P
cl(P((0, 0, -300)), P((0, 0, zt + hc + 600)))
xL = P((-Ro, 0, 0))[0]; xR = P((Ro, 0, 0))[0]
y0 = P((0, 0, 0))[1]; yf = P((0, 0, M.TZ0))[1]; yt_ = P((0, 0, zt))[1]; ytop = P((0, 0, zt + hc))[1]
dim_v(y0, ytop, xL - 24, fn(zt + hc), xL, xL, tdy=-40)
dim_v(yf, yt_, xL - 13, fn(M.THs), xL, xL, tdy=-60)
dim_v(y0, yf, xR + 20, fn(M.TZ0), xR, xR, out=True, side=1)
dim_v(yt_, ytop, xL - 12, fn(hc), xL, xL)
dim_h(P((-R_ - M.TP, 0, 0))[0], P((R_ + M.TP, 0, 0))[0], y0 + 9, "Ø" + fn(M.TD + 2 * M.TP) + " OD PANEL", y0, y0)
yl = P((0, 0, M.TZ0 + M.TLIQ))[1]
with own(('nll',)):
    L([(xL - 4, yl), (xR + 4, yl)], .25, [2, 1], 'inst')
    PG([(xR + 6, yl - 2.6), (xR + 9, yl - 2.6), (xR + 7.5, yl - .2)], .25, None, 'inst')
T(xR + 11, yl + 1.2, "NLL", 3.0, 'l')
T(xL + 3, P((0, 0, 6500))[1], "N1/N2/N3/N11/N12: lihat orientasi", 3.0, 'l')
vlabel((xL + xR) / 2 + 6, y0 + 14, "ELEVASI (DARI SELATAN)", "1:125")
for tag, srv, dn, ang, z, proj in M.TNOZ:
    a = math.radians(ang); xr = (Ro + proj) * math.cos(a)
    if abs(math.sin(a)) > .97 or tag in ("N1", "N2", "N3", "N11", "N12"): continue
    auto_leader(P((xr, 0, z)), tag, pref=0 if xr > 0 else 180, rmin=6, rmax=36, size=3.0)
auto_leader(P((0, 0, zt + hc - 200)), "ATAP MEMBRAN GANDA", pref=60, rmin=8, rmax=40, size=3.0)
N4 = [n for n in M.TNOZ if n[0] == "N4"][0]
callout(P((Ro * math.cos(math.radians(20)) + 250, 0, N4[4])), 500 / SC + 1.6, "A", ang=60)
callout(P((R_ + 50, 0, 300)), 600 / SC + 1.4, "B", ang=-30)
# ---------------- tampak atas: orientasi nosel 1:200
SA_ = 250.0
A = View((0, 0, 1), (1, 0, 0), SA_, 196, 58, name='atas')
Ash = [s for n, s, c in V if n in ("dinding-GFS", "klading-insulasi", "ring-beam") or (n[0] in "NM" and "-" not in n)]
A.draw(Ash, hidden=False, w=.4)
kd.OPEN_VIEWS.add('atas')
c = A.P((0, 0, 0))
cl((c[0] - 29, c[1]), (c[0] + 29, c[1])); cl((c[0], c[1] - 29), (c[0], c[1] + 29))
for tag, srv, dn, ang, z, proj in M.TNOZ:
    a = math.radians(ang); rr = Ro + proj
    auto_leader(A.P((rr * math.cos(a), rr * math.sin(a), 0)), "%s %d°" % (tag, (90 - ang) % 360), pref=math.degrees(a), rmin=4, rmax=30, size=3.0)
nx, ny = c[0] - 40, c[1] - 34
PG([(nx, ny - 7), (nx - 2.2, ny), (nx + 2.2, ny)], .3, '#000000')
TC(nx, ny + 3.5, "U", 3.5, 'm')
vlabel(c[0], c[1] + 40, "ORIENTASI NOSEL", "1:250")
# ---------------- DETAIL A: nosel N4 DN200 menembus panel GFS + insulasi (potongan radial) 1:10
sel = [s for n, s, c in V if n in ("dinding-GFS", "klading-insulasi", "N4")]
zA = N4[4]; rA0, rA1 = R_ - 150, Ro + 400 + 60
cA = crop(sel, 20, rA0, rA1, zA - 200, zA + 200, 360)
SD = 20.0; kA = 1 / SD
oxA = 166 - rA0 * kA; oyA = 130 + zA * kA
detail_view(cA, 20, (0, 0, zA), SD, oxA, oyA, 'detA')
pA = lambda r, z: (oxA + r * kA, oyA - z * kA)
dim_h(pA(R_ + M.TP, 0)[0], pA(Ro, 0)[0], pA(0, zA - 200)[1] + 7, fn(Ro - R_ - M.TP), pA(0, zA - 140)[1], pA(0, zA - 140)[1], size=3.0)
for lab_, pt, pr in (("PANEL GFS t6", (R_ + 3, zA - 150), -100), ("INSULASI 100", (R_ + M.TP + 50, zA + 170), 75),
                     ("DN200 SS316L", (Ro + 200, zA + 105), 30), ("FLENS PN10", (rA1 - 60, zA - 140), -30)):
    auto_leader(pA(*pt), lab_, pref=pr, rmin=6, rmax=26, size=3.0)
vlabel(pA((rA0 + rA1) / 2, 0)[0], pA(0, zA - 200)[1] + 11, "DETAIL A", "1:20", size=3.5)
# ---------------- DETAIL B: ring beam + panel awal + angkur (potongan radial 7,5°) 1:15
selB = [s for n, s, c in V if n in ("pelat-dasar-beton", "ring-beam", "dinding-GFS", "klading-insulasi", "cincin-awal-GFS", "angkur-0")]
rB0, rB1 = R_ - 400, R_ + 450
cB = crop(selB, 7.5, rB0, rB1, 0, 1000, 300)
SB = 20.0; kB = 1 / SB
oxB = 168 - rB0 * kB; oyB = 222
detail_view(cB, 7.5, (0, 0, 0), SB, oxB, oyB, 'detB')
pB = lambda r, z: (oxB + r * kB, oyB - z * kB)
dim_v(pB(0, 0)[1], pB(0, M.TZ0)[1], pB(rB0, 0)[0] - 5, fn(M.TZ0), pB(rB0, 0)[0], pB(rB0, 0)[0], size=3.0)
for lab_, pt, pr in (("ANGKUR M20", (R_ + M.TP + 60, M.TZ0 + 120), 20), ("RING BEAM", (R_ + 300, M.TZ0 - 80), -20),
                     ("PELAT DASAR", (R_ - 300, M.TZ0 - 300), 200), ("PANEL AWAL", (R_ + 2, M.TZ0 + 900), 160)):
    auto_leader(pB(*pt), lab_, pref=pr, rmin=6, rmax=26, size=3.0)
vlabel(pB((rB0 + rB1) / 2, 0)[0], pB(0, 0)[1] + 11, "DETAIL B", "1:20", size=3.5)
# ---------------- jadwal nosel
rows = [[tag, "DN" + str(dn), "PN10 RF", srv, fn(z), "%d°" % ((90 - ang) % 360)] for tag, srv, dn, ang, z, proj in M.TNOZ]
yt = table(244, 14, [("Tag", 11, 'm'), ("Ukuran", 14, 'm'), ("Rating", 16, 'm'), ("Layanan", 78, 'l'), ("Elev.", 17, 'm'), ("Orient.", 18, 'm')],
           rows, "JADWAL NOSEL", rh=4.3, size=2.5, hsize=2.5)
# ---------------- data desain
mass = M.gfs_mass("reactor")
Vg = math.pi * R_ ** 2 * M.THs * 1e-9
npan = int(math.ceil(math.pi * M.TD / M.PANEL_W)) * int(math.ceil(M.THs / M.PANEL_H))
dd = [["Fungsi / jumlah", "Reaktor kontak termofilik, 3 unit identik (2 / 4 untuk 30 / 60 t/jam)"],
      ["Kode desain", "AWWA D103-09 (tangki baja dibaut) + ISO 28765 (enamel)"],
      ["Tekanan / suhu desain", "+50 / -5 mbar(g) + hidrostatik penuh; 70 °C (op. 55 °C)"],
      ["Volume dinding / kerja", "%s m³ / %s m³, NLL %s mm dari lantai" % (fn(Vg), fn(M.RV["V_liq_m3"]), fn(M.TLIQ))],
      ["Panel", "%d panel %s x %s mm, t 5-10 mm (rata-rata %s), enamel 2 lapis" % (npan, fn(M.PANEL_W), fn(M.PANEL_H), fn(M.TP))],
      ["Atap", "Membran ganda PVC-PES (dalam: gas, luar: udara), tinggi %s mm" % fn(hc)],
      ["Angin / gempa", "SNI 1727:2020 (40 m/s) / SNI 1726:2019, Kelas D"],
      ["Insulasi / kladding", "Mineral wool %s mm 100 kg/m³ / Al 0,8 mm + sabuk" % fn(M.TINS)],
      ["Massa baja / operasi", "± %s t / ± %s t" % (fn(mass, 1), fn(mass + M.RV["V_liq_m3"] * 1.02))],
      ["Pengiriman / relokasi", "Panel datar dalam 2 kontainer 40 ft; ereksi ± 3 minggu; dapat dibongkar"]]
yd = table(244, yt + 3, [("Data desain", 40, 'l'), ("Nilai", 114, 'l')], dd, "DATA DESAIN", rh=4.3, size=2.5, hsize=2.5)
# ---------------- daftar material (massa dari model 3D)
def m_(pred, rho=7.85, k=1.0): return sum(s.Volume() for n, s, c in VL if pred(n)) * rho * 1e-6 * k
v_ins = math.pi * ((Ro) ** 2 - (R_ + M.TP) ** 2) * M.THs * 1e-9
bom = [["1", "Panel dinding GFS", "S355 + enamel 2 lapis", str(npan), fn(m_(lambda n: n.startswith(("dinding", "cincin-awal"))))],
       ["2", "Baut panel + sealant", "M12 galv. + mastik", "± %d" % (npan * 60), "-"],
       ["3", "Sudut penahan + angkur M20", "S275 galv.", "24", fn(m_(lambda n: n.startswith("angkur")))],
       ["4", "Leher nosel + flens", "SS316L / SA-105", str(len(M.TNOZ)), fn(m_(lambda n: n[0] in "NM" and "-" not in n))],
       ["5", "Header jet internal + 8 nosel", "SS316L DN150 sch10", "%s m" % fn(2 * math.pi * 0.6 * R_ / 1000 + 4, 1), fn((2 * math.pi * 0.6 * R_ / 1000 + 4) * 11.0)],
       ["6", "Atap membran ganda + klem", "PVC-PES 1.100 g/m² / Al", "1", "± 950"],
       ["7", "Blower udara membran luar", "0,75 kW + katup cek", "1", "60"],
       ["8", "Tangga + sangkar + platform", "S275 galv., grating", "1", fn(m_(lambda n: n.startswith(("tangga", "anak-tangga", "sangkar", "rel-"))) + m_(lambda n: n.startswith("platform"), k=.3))],
       ["9", "Insulasi mineral wool", "100 kg/m³", "%s m³" % fn(v_ins, 1), fn(v_ins * 100)],
       ["10", "Kladding + sabuk", "Al 3003 t0,8", "1", fn(m_(lambda n: n.startswith("klading"), 2.7))],
       ["11", "Ring beam + pelat dasar", "Beton K-300 (sipil lokal)", "1", "-"]]
yb = table(244, yd + 3, [("No", 8, 'm'), ("Bagian", 54, 'l'), ("Material", 50, 'l'), ("Jml", 18, 'm'), ("Massa kg", 24, 'm')], bom, "DAFTAR MATERIAL (MASSA DARI MODEL 3D)", rh=4.3, size=2.5, hsize=2.5)
note(244, yb + 4, ["1. Panel dibaut dengan sealant; tanpa las di lokasi.",
                   "2. Uji: isi air 24 jam (kebocoran), uji udara atap 5 mbar.",
                   "3. Elevasi dari muka tanah (EL 0); orientasi dari utara.",
                   "4. Relokasi: bongkar panel, ganti sealant & ring beam."], 3.0)
image("R-201_iso-depan.png", 352, 206, 52, 40, name='ISO')
TC(378, 249, "ISOMETRI", 3.0, 'm')
finish("BG-V-201")
