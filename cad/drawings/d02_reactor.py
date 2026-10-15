# -*- coding: utf-8 -*-
"""Lembar 2: Bejana standar / reaktor AnMBR R-201..R-214: elevasi, orientasi nosel, detail A (nosel + pad penguat) dan
detail B (kursi baut angkur), jadwal nosel, data desain, daftar material (massa dari model 3D), catatan las/uji, isometri."""
from dcommon import *
import bgmodels as M
import math

frame(2, "Reaktor AnMBR Standar\nR-201 s/d R-214", "BG-V-201", "1:80/1:10/1:15", "Equipment Drawing")
V = M.vessel("reactor", ladder=False)
VL = M.vessel("reactor", ladder=True)
body = [s for n, s, c in V if not n.startswith(("baut", "kursi", "klading", "las-", "lug-bumi", "papan"))]
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
yl = P((0, 0, M.ZB + M.LIQ - M.HB))[1]
with own(('nll',)):
    L([(xL - 4, yl), (xR + 4, yl)], .25, [2, 1], 'inst')
    PG([(xR + 6, yl - 2.6), (xR + 9, yl - 2.6), (xR + 7.5, yl - .2)], .25, None, 'inst')
T(xR + 11, yl + 1.2, "NLL", 3.0, 'l')
vlabel((xL + xR) / 2 + 6, y0 + 13.5, "ELEVASI (DARI SELATAN)", "1:80")
for tag, srv, dn, ang, z, proj in M.NOZ:
    if z in ("top", "top2", "top3"): continue
    a = math.radians(ang)
    xr = (M.VR + M.INS + proj) * math.cos(a)
    if abs(math.sin(a)) > .97: continue
    auto_leader(P((xr, 0, z)), tag, pref=0 if xr > 0 else 180, rmin=8, rmax=40, size=3.0)
auto_leader(P((0, 0, M.ZT + M.HB + 520)), "N7", pref=150, rmin=8, rmax=40, size=3.0)
auto_leader(P((1100, 0, M.ZT + M.HB + 600)), "N8 (PVRV)", pref=30, rmin=8, rmax=40, size=3.0)
# rujukan detail
N4 = [n for n in M.NOZ if n[0] == "N4"][0]
callout(P(((M.VR + 250) * math.cos(math.radians(20)), 0, N4[4])), 400 / SC + 1.8, "A", ang=60)
callout(P((M.VR + 50, 0, 250)), 450 / SC + 1.5, "B", ang=20)
# ---------------- tampak atas: orientasi nosel 1:80
A = View((0, 0, 1), (1, 0, 0), SC, 186, 56, name='atas')
Ash = [s for n, s, c in V if n in ("shell", "klading-shell", "cincin-dasar") or (n[0] in "NM" and "-" not in n and n != "N13")]
A.draw(Ash, hidden=False, w=.4)
kd.OPEN_VIEWS.add('atas')
c = A.P((0, 0, 0))
cl((c[0] - 40, c[1]), (c[0] + 40, c[1])); cl((c[0], c[1] - 40), (c[0], c[1] + 40))
for tag, srv, dn, ang, z, proj in M.NOZ:
    if ang is None: continue
    a = math.radians(ang); rr = M.VR + M.INS + proj
    auto_leader(A.P((rr * math.cos(a), rr * math.sin(a), 0)), "%s %d°" % (tag, (90 - ang) % 360), pref=math.degrees(a), rmin=5, rmax=30, size=3.0)
nx, ny = c[0] + 46, c[1] - 30
PG([(nx, ny - 7), (nx - 2.2, ny), (nx + 2.2, ny)], .3, '#000000')
TC(nx, ny + 3.5, "U", 3.5, 'm')
vlabel(c[0], c[1] + 43, "ORIENTASI NOSEL", "1:80")
# ---------------- DETAIL A: nosel N4 DN150 + pad penguat (potongan radial) 1:15
sel = [s for n, s, c in V if n in ("shell", "klading-shell", "N4", "N4-pad") or n.startswith("las-course")]
zA = N4[4]; rA0, rA1 = M.VR - 120, M.VR + M.VT + M.INS + 400 + 40
cA = crop(sel, 20, rA0, rA1, zA - 260, zA + 260, 360)
SA = 10.0; kA = 1 / SA
oxA = 131 - rA0 * kA; oyA = 133 + zA * kA
DA = detail_view(cA, 20, (0, 0, zA), SA, oxA, oyA, 'detA')
rp = M.DN_OD[150] / 2
pA = lambda r, z: (oxA + r * kA, oyA - z * kA)
dim_h(pA(M.VR + M.VT, 0)[0], pA(rA1 - 40, 0)[0], pA(0, zA - 260)[1] + 4, fn(rA1 - 40 - M.VR - M.VT), pA(0, zA - rp * 2)[1], pA(0, zA - rp - 30)[1], size=3.0)
for lab_, pt, pr in (("SHELL t8", (M.VR + 4, zA - 200), 200), ("PAD t8 Ø337", (M.VR + M.VT + 4, zA + 150), 100),
                     ("INSULASI 100", (M.VR + M.VT + 50, zA - 210), 240), ("DN150 SCH40", (M.VR + 300, zA + rp - 4), 70),
                     ("FLENS PN10 RF", (rA1 - 55, zA - 120), -60)):
    auto_leader(pA(*pt), lab_, pref=pr, rmin=6, rmax=26, size=3.0)
vlabel(pA((rA0 + rA1) / 2, 0)[0], pA(0, zA - 260)[1] + 8, "DETAIL A", "1:10", size=3.5)
# ---------------- DETAIL B: kursi baut angkur (potongan radial 11,25°) 1:20
selB = [s for n, s, c in V if n in ("rok", "cincin-dasar", "baut-0", "kursi-0")]
grout = M.box(800, 600, 300, 0, -300, -300).translate(M.cq.Vector(M.VR - 300, 0, 0)).rotate(M.cq.Vector(0, 0, 0), M.cq.Vector(0, 0, 1), 11.25)
rB0, rB1 = M.VR - 250, M.VR + 380
cB = crop(selB + [grout], 11.25, rB0, rB1, -250, 450, 300)
SB = 15.0; kB = 1 / SB
oxB = 150 - rB0 * kB; oyB = 213
DB = detail_view(cB, 11.25, (0, 0, 0), SB, oxB, oyB, 'detB')
pB = lambda r, z: (oxB + r * kB, oyB - z * kB)
dim_h(pB(M.VR - 180, 0)[0], pB(M.VR + 260, 0)[0], pB(0, -250)[1] + 4, "440", pB(0, -300)[1], pB(0, -300)[1], size=3.0)
for lab_, pt, pr in (("ROK t12", (M.VR + M.VT + 6, 380), 150), ("CINCIN t40", (M.VR - 120, 20), 160),
                     ("BAUT M36 x16", (M.VR + 140, 150), 60), ("GROUT", (M.VR - 200, -150), 200)):
    auto_leader(pB(*pt), lab_, pref=pr, rmin=6, rmax=26, size=3.0)
vlabel(pB((rB0 + rB1) / 2, 0)[0], pB(0, -250)[1] + 8, "DETAIL B", "1:15", size=3.5)
# ---------------- jadwal nosel
rows = []
for tag, srv, dn, ang, z, proj in M.NOZ:
    el = {"top": "puncak", "top2": "kepala", "top3": "kepala"}[z] if isinstance(z, str) else fn(z)
    ori = "-" if ang is None else "%d°" % ((90 - ang) % 360)
    pad = "Ø%s" % fn(M.DN_OD[dn] * 2) if (dn >= 100 and ang is not None and dn < 600) else ("Ø%s" % fn(M.DN_OD[dn] + 400) if dn >= 600 else "-")
    rows.append([tag, "DN" + str(dn), "PN10 RF", srv, el, ori, pad])
rows.append(["N13", "DN80", "PN10 RF", "Pengurasan (kepala bawah)", fn(M.ZB - M.HB - 220), "-", "-"])
yt = table(244, 14, [("Tag", 11, 'm'), ("Ukuran", 14, 'm'), ("Rating", 16, 'm'), ("Layanan", 66, 'l'), ("Elev.", 17, 'm'), ("Orient.", 16, 'm'), ("Pad", 14, 'm')],
           rows, "JADWAL NOSEL", rh=4.4, size=2.5, hsize=2.5)
# ---------------- data desain
mass = M.vessel_mass()
Vg = math.pi * M.VR ** 2 * M.VH * 1e-9 + 2 * (2 / 3) * math.pi * M.VR ** 2 * M.HB * 1e-9
dd = [["Fungsi / jumlah", "Reaktor AnMBR termofilik, 14 unit identik + TK-101/TK-301"],
      ["Kode desain / las", "API 650 (acuan) + ASME VIII-1 nosel; las ASME IX"],
      ["Tekanan / suhu desain", "+50 / -5 mbar(g) + hidrostatik penuh; 70 °C (op. 55 °C)"],
      ["Volume total / kerja", "%s m³ / %s m³, NLL %s mm dari BTL" % (fn(Vg), fn(M.RV["V_liq_m3"]), fn(M.LIQ))],
      ["Bahan shell / kepala", "SA-516-70N, %s mm (6 course x 2400), CA 3 mm" % fn(M.VT)],
      ["Angin / gempa", "SNI 1727:2020 (40 m/s) / SNI 1726:2019, Kelas D"],
      ["Insulasi / kladding", "Mineral wool %s mm 100 kg/m³ / Al 0,8 mm + sabuk" % fn(M.INS)],
      ["Pelapisan", "Dalam: SA 2,5 + epoksi fenolik 400 µm; luar: zinc-epoksi-PU"],
      ["Massa kosong / operasi", "± %s t / ± %s t" % (fn(mass, 1), fn(mass + M.RV["V_liq_m3"] * 1.02))],
      ["Transport", "rebah di low-bed, %s x %s m, 2 trunnion" % (fn((M.VH + 2 * M.HB) / 1000, 1), fn((M.VD + 2 * M.INS) / 1000, 1))]]
yd = table(244, yt + 3, [("Data desain", 40, 'l'), ("Nilai", 114, 'l')], dd, "DATA DESAIN", rh=4.4, size=2.5, hsize=2.5)
# ---------------- daftar material (massa dari model 3D)
def m_(pred, rho=7.85, k=1.0): return sum(s.Volume() for n, s, c in VL if pred(n)) * rho * 1e-6 * k
Ro = M.VR + M.VT
v_ins = (math.pi * ((Ro + M.INS) ** 2 - Ro ** 2) * M.VH + 1.08 * math.pi * Ro ** 2 * M.INS) * 1e-9
bom = [["1", "Shell (6 course)", "SA-516-70N t8", "1", fn(m_(lambda n: n == "shell"))],
       ["2", "Kepala 2:1 atas / bawah", "SA-516-70N t8", "2", fn(m_(lambda n: n.startswith("kepala")))],
       ["3", "Rok + rangka akses + vent", "SA-516-70N t12", "1", fn(m_(lambda n: n.startswith("rok")))],
       ["4", "Cincin dasar + kursi", "SA-36 t40", "1", fn(m_(lambda n: n.startswith(("cincin-dasar", "kursi"))))],
       ["5", "Baut angkur M36", "F1554 Gr.36 galv.", "16", fn(m_(lambda n: n.startswith("baut")))],
       ["6", "Leher nosel + flens", "SA-106B / SA-105", "15", fn(m_(lambda n: n[0] in "NM" and "-" not in n))],
       ["7", "Pad penguat", "SA-516-70N t8", "8", fn(m_(lambda n: n.endswith("-pad")))],
       ["8", "Header jet internal", "SS316L DN100", "1", fn(m_(lambda n: "jet" in n, 8.0))],
       ["9", "Trunnion angkat", "SA-106B DN200", "2", fn(m_(lambda n: n.startswith("lug-angkat")))],
       ["10", "Tangga + sangkar + platform", "S275 galv., grating", "1", fn(m_(lambda n: n.startswith(("tangga", "anak-tangga", "sangkar", "rel-", "braket", "davit"))) + m_(lambda n: n == "platform", k=.3))],
       ["11", "Insulasi mineral wool", "100 kg/m³", "%s m³" % fn(v_ins, 1), fn(v_ins * 100)],
       ["12", "Kladding + sabuk", "Al 3003 t0,8", "1", fn(m_(lambda n: n.startswith("klading"), 2.7))],
       ["13", "Gasket + baut flens", "EPDM / A193 B7-2H", "15 set", "-"]]
yb = table(244, yd + 3, [("No", 8, 'm'), ("Bagian", 54, 'l'), ("Material", 50, 'l'), ("Jml", 18, 'm'), ("Massa kg", 24, 'm')], bom, "DAFTAR MATERIAL (MASSA DARI MODEL 3D)", rh=4.4, size=2.5, hsize=2.5)
note(244, yb + 4, ["1. Las butt penuh-tembus; RT spot 10 %, nosel & pad 100 % MT/PT.",
                   "2. Uji hidrostatik: isi penuh air 24 jam; uji pneumatik pad 1 bar.",
                   "3. Toleransi umum ISO 2768-mK; elevasi dari dasar cincin (EL 0).",
                   "4. Orientasi dari utara searah jarum jam; header jet = garis putus."], 3.0)
# ---------------- isometri
image("R-201_iso-depan.png", 206, 176, 34, 66, name='ISO')
TC(223, 246, "ISOMETRI", 3.0, 'm')
finish("BG-V-201")
