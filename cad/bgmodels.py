# -*- coding: utf-8 -*-
"""
Model 3D (CadQuery, satuan mm, sumbu Z ke atas) produk Generator Biogas Portabel - AnMBR termofilik POME.
Setiap fungsi modul mengembalikan daftar (nama_bagian, cq.Shape, warna_hex). Ukuran utama dibaca dari
../process/outputs/results.json; ukuran detail (tebal pelat, nosel, rangka) adalah praktik desain umum [ASUMSI].

Modul (sesuai PFD-BG-002):
  vessel()      bejana standar 194 m3: reaktor R-201..R-214 (berinsulasi) / TK-101 / TK-301
  pm1()         skid praolah 40 ft: SC-101, P-101, HC-101, E-101, sump
  pm4()         kontainer membran 40 ft HC: MB-301 (34 modul UF), P-301A/B, P-302, TK-302, MCC
  pm5()         skid dosing + pompa umpan 20 ft: TK-201/202, P-203/204, P-201A/B
  pm6()         skid gas: BTF-301 + P-305 + K-301 (bejana terpisah) dan kontainer 40 ft (HX-301, CH-301, V-301, K-302A/B, AC-301A/B)
  pm7()         penampung gas GH-301 membran ganda + flare FL-301
  pm8()         kontainer CHP 40 ft HC: GE-401 (800 kWe) + radiator + silencer; HX-401 + ST-401 (PM-9)
  pm9_ct()      menara pendingin modular CT-601 + P-601
  pm10()        skid lumpur 20 ft: P-303, PR-501, P-501
  plant()       susunan lengkap 45 t TBS/jam
"""
import os, json, math
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
EQ = R["equipment"]; RV = EQ["reactor_vessel"]

# ------------------------------------------------------------------ warna
STEEL = "#9aa7b4"; CLAD = "#c9cfd6"; PAINT_G = "#6f8f74"; PAINT_B = "#3f6d9a"; YELLOW = "#e2b23a"; DARK = "#4b5157"
CONT = "#7c8b99"; CONT_IN = "#d7dde2"; MOTOR = "#2f5d8a"; PIPE = "#8e969e"; GRATE = "#a3a07a"; RED = "#b6463d"; MEMB = "#e9ecef"
CONC = "#bdb8ad"; WHITE = "#f2f2f2"; FRP = "#7fa6a0"

# ------------------------------------------------------------------ primitif
def box(lx, ly, lz, x=0, y=0, z=0):
    """kotak dengan sudut minimum di (x,y,z)"""
    return cq.Workplane("XY").box(lx, ly, lz, centered=False).translate((x, y, z)).val()
def cyl(r, h, x=0, y=0, z=0, axis="z"):
    """silinder jari-jari r panjang h, dasar di (x,y,z), sepanjang sumbu axis (+)"""
    d = {"z": (0, 0, 1), "x": (1, 0, 0), "y": (0, 1, 0), "-x": (-1, 0, 0), "-y": (0, -1, 0), "-z": (0, 0, -1)}[axis]
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(*d))
def tube(ro, ri, h, x=0, y=0, z=0, axis="z"):
    return cyl(ro, h, x, y, z, axis).cut(cyl(ri, h, x, y, z, axis))
def cyl_dir(r, h, p, d):
    return cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d))
def cone(r1, r2, h, x=0, y=0, z=0):
    return cq.Solid.makeCone(r1, r2, h, cq.Vector(x, y, z), cq.Vector(0, 0, 1))
def ellhead(R_, b, t, zc, up=True, x=0, y=0):
    """kepala elipsoidal 2:1 (setengah elipsoid) berongga, bidang tangen di zc"""
    def ell(a, bb):
        s = cq.Solid.makeSphere(1.0, angleDegrees1=0 if up else -90, angleDegrees2=90 if up else 0)
        m = cq.Matrix([[a, 0, 0, 0], [0, a, 0, 0], [0, 0, bb, 0]])
        return s.transformGeometry(m)
    o = ell(R_ + t, b + t); i = ell(R_, b)
    return o.cut(i).translate(cq.Vector(x, y, zc))
def union(shapes):
    return cq.Compound.makeCompound(shapes)
def rot(sh, ang, axis=(0, 0, 1), c=(0, 0, 0)):
    return sh.rotate(cq.Vector(*c), cq.Vector(c[0] + axis[0], c[1] + axis[1], c[2] + axis[2]), ang)
def mv(sh, x=0, y=0, z=0): return sh.translate(cq.Vector(x, y, z))

def _wall(dn): return 6.0 if dn <= 80 else 7.1 if dn <= 150 else 8.2 if dn <= 300 else 10.0
def flange(r_pipe, x, y, z, d, dn, blind=False):
    """flens leher-las: diameter luar ~ 2 x pipa, berlubang (atau buta untuk lubang orang)"""
    rf = max(r_pipe * 2.0, r_pipe + 45); tf = 22 if dn <= 100 else 28 if dn <= 300 else 40
    f = cyl_dir(rf, tf, (x, y, z), d)
    if not blind: f = f.cut(cyl_dir(r_pipe - _wall(dn), tf, (x, y, z), d))
    return f
def nozzle_radial(Rshell, ang, z, dn, proj, x0=0, y0=0):
    """nosel radial berongga: leher dari dalam dinding ke luar; muka flens pada jari-jari Rshell+proj"""
    rp = DN_OD[dn] / 2; t = _wall(dn); blind = dn >= 600
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    tf = 22 if dn <= 100 else 28 if dn <= 300 else 40
    r0 = Rshell - 40; L_ = Rshell + proj - tf - r0
    neck = cyl_dir(rp, L_, (x0 + ux * r0, y0 + uy * r0, z), (ux, uy, 0)).cut(cyl_dir(rp - t, L_, (x0 + ux * r0, y0 + uy * r0, z), (ux, uy, 0)))
    fl = flange(rp, x0 + ux * (r0 + L_), y0 + uy * (r0 + L_), z, (ux, uy, 0), dn)
    out = neck.fuse(fl)
    if blind: out = out.fuse(cyl_dir(max(rp * 2, rp + 45), 36, (x0 + ux * (r0 + L_ + tf), y0 + uy * (r0 + L_ + tf), z), (ux, uy, 0)))
    return out
def nozzle_vert(x, y, z0, dn, h):
    rp = DN_OD[dn] / 2; t = _wall(dn); tf = 22 if dn <= 100 else 28 if dn <= 300 else 40
    out = tube(rp, rp - t, h - tf, x, y, z0).fuse(flange(rp, x, y, z0 + h - tf, (0, 0, 1), dn))
    if dn >= 600: out = out.fuse(cyl(max(rp * 2, rp + 45), 36, x, y, z0 + h))
    return out
DN_OD = {25: 33.4, 50: 60.3, 80: 88.9, 100: 114.3, 150: 168.3, 200: 219.1, 250: 273.0, 300: 323.9, 600: 610.0}

def pump(L_=900, Wb=450, motor_r=150, casing_r=200, x=0, y=0, z=0, name="pump"):
    """pompa sentrifugal end-suction di alas: alas, motor, kopling, rumah volute, nosel isap (-x) & buang (+z)"""
    parts = []
    parts.append((name + "-alas", box(L_, Wb, 80, x, y - Wb / 2, z), DARK))
    mL = L_ * 0.48
    parts.append((name + "-motor", cyl(motor_r, mL, x + L_ - mL - 30, y, z + 80 + motor_r + 20, "x"), MOTOR))
    parts.append((name + "-kaki", box(mL * 0.8, motor_r * 1.6, motor_r + 20, x + L_ - mL, y - motor_r * .8, z + 80), MOTOR))
    parts.append((name + "-kopling", cyl(motor_r * .45, 120, x + L_ - mL - 150, y, z + 80 + motor_r + 20, "x"), YELLOW))
    cx = x + casing_r + 60
    vol = cyl(casing_r, casing_r * .7, cx, y - casing_r * .35, z + 80 + motor_r + 20, "y")
    parts.append((name + "-volute", vol, PAINT_B))
    parts.append((name + "-isap", cyl(casing_r * .42, 160, cx - casing_r * .35, y, z + 80 + motor_r + 20, "-x"), PAINT_B))
    parts.append((name + "-buang", cyl(casing_r * .35, casing_r + 140, cx + casing_r * .3, y, z + 80 + motor_r + 20, "z"), PAINT_B))
    parts.append((name + "-bantalan", box(220, 180, 160, cx + casing_r * .4, y - 90, z + 80 + motor_r - 60), PAINT_B))
    return parts

def handrail(pts, z, h=1100, post=1500, r=21):
    """pegangan tangan sepanjang polilinia pts (x,y) pada lantai z"""
    out = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L_, (y1 - y0) / L_
        for zz in (z + h, z + h / 2):
            out.append(cyl_dir(r, L_, (x0, y0, zz), (ux, uy, 0)))
        n = max(1, int(L_ // post))
        for i in range(n + 1):
            out.append(cyl(r, h, x0 + ux * L_ * i / n, y0 + uy * L_ * i / n, z))
    return out

# =====================================================================================================
# 1. BEJANA STANDAR (reaktor / tangki)
# =====================================================================================================
VD = RV["D_m"] * 1000.0          # 4200 ID
VR = VD / 2
VT = 8.0                          # tebal shell (SA-516-70, 1,5 bar hidrostatik + CA 3 mm)
VH = RV["H_shell_m"] * 1000.0     # 15200 T/T
HB = VD / 4                       # tinggi kepala 2:1 = 1050
HS = 1600.0                       # tinggi rok
INS = 100.0                       # insulasi
ZB = HS                           # garis tangen bawah (BTL)
ZT = HS + VH                      # garis tangen atas (TTL)
LIQ = RV["H_liq_m"] * 1000.0      # muka cairan normal di atas BTL (termasuk kepala bawah)
# daftar nosel: (tag, layanan, DN, sudut (deg), elevasi z dari dasar rok (mm) atau 'top'/'bot', proyeksi dari dinding)
NOZ = [("N1", "Umpan reaktor (dari P-201)", 100, 200, ZB + 1200, 400),
       ("N2", "Isap jet mixing (ke P-202)", 150, 160, ZB + 700, 400),
       ("N3", "Balik jet mixing (header nosel jet)", 100, 180, ZB + 1600, 400),
       ("N4", "Lumpur ke membran (ke P-301)", 150, 20, ZB + 900, 400),
       ("N5", "Retentat balik (dari MB-301)", 150, 0, ZB + 11400, 400),
       ("N6", "Lumpur buangan (ke P-303)", 80, 340, ZB + 500, 400),
       ("N7", "Keluaran biogas", 200, None, "top", 600),
       ("N8", "PVRV / relief tekanan-vakum", 150, None, "top2", 500),
       ("N9", "Pemancar level LT (atas / bawah)", 50, 90, ZB + 14600, 300),
       ("N10", "Pemancar level LT bawah", 50, 90, ZB + 800, 300),
       ("N11", "Termometer TT / pH / NH4", 50, 120, ZB + 4000, 300),
       ("N12", "Kaca intip muka cairan", 100, 60, ZB + LIQ - HB, 300),
       ("M1", "Lubang orang bawah", 600, 270, ZB + 1100, 350),
       ("M2", "Lubang orang atas", 600, None, "top3", 450)]

def vessel(kind="reactor", ladder=True):
    """bejana standar D 4200 x T/T 15200 + kepala 2:1 + rok 1600. kind: 'reactor' (berinsulasi, cincin jet) atau 'tank'"""
    P_ = []
    shell = tube(VR + VT, VR, VH, 0, 0, ZB)
    P_.append(("shell", shell, STEEL if kind != "reactor" else STEEL))
    P_.append(("kepala-atas", ellhead(VR, HB, VT, ZT, True), STEEL))
    P_.append(("kepala-bawah", ellhead(VR, HB, VT, ZB, False), STEEL))
    # rok + cincin dasar + baut angkur
    sk = tube(VR + VT + 12, VR + VT, HS - 40, 0, 0, 40)
    sk = sk.cut(cyl_dir(450, 2000, (0, -2000, 650), (0, 1, 0)))   # bukaan akses rok
    P_.append(("rok", sk, STEEL))
    P_.append(("cincin-dasar", tube(VR + 260, VR - 180, 40, 0, 0, 0), DARK))
    for i in range(16):
        a = 2 * math.pi * (i + .5) / 16
        P_.append(("baut-%d" % i, cyl(18, 180, (VR + 140) * math.cos(a), (VR + 140) * math.sin(a), -60), DARK))
        if i % 2 == 0: P_.append(("kursi-%d" % i, box(30, 30, 260, (VR + 140) * math.cos(a) - 15, (VR + 140) * math.sin(a) - 15, 40), DARK))
    if kind == "reactor":
        ins = tube(VR + VT + INS + 1, VR + VT + INS, VH, 0, 0, ZB)
        P_.append(("klading-shell", ins, CLAD))
        P_.append(("klading-atas", ellhead(VR + VT + INS, HB + INS, 1.0, ZT, True), CLAD))
    Ro = VR + VT + (INS if kind == "reactor" else 0)
    # nosel
    for tag, srv, dn, ang, z, proj in NOZ:
        if kind != "reactor" and tag in ("N2", "N3", "N4", "N5", "N11"): continue
        if z == "top":
            P_.append((tag, nozzle_vert(0, 0, ZT + HB - 60, dn, 600), STEEL))
        elif z == "top2":
            zz = ZT + HB * math.sqrt(max(0, 1 - (1100 / VR) ** 2)) - 40
            P_.append((tag, nozzle_vert(1100, 0, zz, dn, 500), STEEL))
            P_.append(("PVRV", box(420, 420, 380, 1100 - 210, -210, zz + 500), YELLOW))
        elif z == "top3":
            zz = ZT + HB * math.sqrt(max(0, 1 - (1300 / VR) ** 2)) - 60
            P_.append((tag, nozzle_vert(-1300, 600, zz, dn, 450), STEEL))
        else:
            P_.append((tag, nozzle_radial(VR, ang, z, dn, (Ro - VR) + proj), STEEL))
    # nosel bawah (pengurasan) lewat rok
    P_.append(("N13", cyl(DN_OD[80] / 2, HB + 200, 0, 0, ZB - HB - 220), STEEL))
    # internal: header cincin jet
    if kind == "reactor":
        zr = ZB + 350
        ring = cq.Solid.makeTorus(VR * 0.62, 57).translate(cq.Vector(0, 0, zr))
        P_.append(("header-jet", ring, PIPE))
        for k in range(6):
            a = 2 * math.pi * k / 6 + .3
            P_.append(("nosel-jet-%d" % k, cyl_dir(40, 380, (VR * .62 * math.cos(a), VR * .62 * math.sin(a), zr), (-math.sin(a), math.cos(a), -0.25)), PIPE))
        P_.append(("pipa-jet", cyl_dir(57, VR * .38 + 50, (-VR - 10, 0, ZB + 1600), (1, 0, 0)), PIPE))
        P_.append(("pipa-jet-v", cyl(57, 1250 + 57, -VR * .62, 0, zr), PIPE))
    # tangga + sangkar + platform atas
    if ladder:
        a = math.radians(225); rL = Ro + 250
        lx, ly = rL * math.cos(a), rL * math.sin(a)
        px, py = -math.sin(a), math.cos(a)
        ztop = ZT + 300
        for s in (-1, 1):
            P_.append(("tangga-rel%+d" % s, cyl(25, ztop + 1100 - 300, lx + px * 230 * s, ly + py * 230 * s, 300), YELLOW))
        for k in range(int((ztop - 300) // 300)):
            P_.append(("anak-tangga-%d" % k, cyl_dir(12, 460, (lx - px * 230, ly - py * 230, 300 + 300 * (k + 1)), (px, py, 0)), YELLOW))
        hc = (lx + math.cos(a) * 330, ly + math.sin(a) * 330)
        for k in range(int((ztop + 1000 - 2400) // 1200) + 1):
            zz = 2400 + 1200 * k
            hoop = cq.Solid.makeTorus(360, 12).translate(cq.Vector(hc[0], hc[1], zz))
            hoop = hoop.cut(cyl(330, 40, lx - math.cos(a) * 60, ly - math.sin(a) * 60, zz - 20))
            P_.append(("sangkar-%d" % k, hoop, YELLOW))
        for j in range(5):
            t_ = a + math.radians(-80 + 40 * j)
            P_.append(("sangkar-tali-%d" % j, box(50, 8, ztop + 1100 - 2400, hc[0] + 360 * math.cos(t_) - 25, hc[1] + 360 * math.sin(t_) - 4, 2400), YELLOW))
        # platform setengah lingkar di atas kepala
        zp = ZT + 300
        plat = cq.Workplane("XY").circle(Ro + 1000).circle(Ro + 50).extrude(40).val().translate(cq.Vector(0, 0, zp))
        cutter = box(3 * VR, 6 * VR, 200, 0, -3 * VR, zp - 50).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 45 + 90)
        plat = plat.cut(cutter)
        P_.append(("platform", plat, GRATE))
        # pegangan tangan busur
        pts = [((Ro + 950) * math.cos(math.radians(t)), (Ro + 950) * math.sin(math.radians(t))) for t in range(135, 316, 15)]
        for i_, s_ in enumerate(handrail(pts, zp + 40, 1100, 1300, 20)): P_.append(("rel-%d" % i_, s_, YELLOW))
        for sgn in (-1, 1):
            t = math.radians(225 + sgn * 90)
            for k in range(3):
                rr = Ro + 100 + 300 * k
                P_.append(("braket-%d%d" % (sgn, k), box(60, 60, 300, rr * math.cos(t) - 30, rr * math.sin(t) - 30, zp - 300), DARK))
    # lug angkat (trunnion transport)
    for s in (-1, 1):
        P_.append(("lug-angkat%+d" % s, cyl_dir(110, 260, (0, s * (VR + VT), ZT - 600), (0, s, 0)), DARK))
    return [p for p in P_ if p]

def vessel_mass():
    """massa kosong bejana (t) dari volume baja"""
    st = 0.0
    for n, s, c in vessel("reactor", ladder=False):
        if n.startswith(("shell", "kepala", "rok", "cincin", "N", "M")): st += s.Volume()
    return st * 7.85e-9

# =====================================================================================================
# 2. KONTAINER ISO 40 ft HC (rangka + dinding bergelombang; dinding dapat dibuang untuk tampilan potong)
# =====================================================================================================
CL, CW, CH = 12192.0, 2438.0, 2896.0
def container(prefix="C", walls=("back", "left", "right", "roof", "front"), louvres=0, side_doors=0, color=CONT, hc=True):
    h = CH if hc else 2591.0
    P_ = []
    # rel bawah, rel atas, tiang sudut
    for y in (0, CW - 160):
        P_.append((prefix + "-rel-bawah-%d" % y, box(CL, 160, 160, 0, y, 0), DARK))
        P_.append((prefix + "-rel-atas-%d" % y, box(CL, 160, 120, 0, y, h - 120), color))
    for x in (0, CL - 160):
        P_.append((prefix + "-balok-ujung-b-%d" % x, box(160, CW, 160, x, 0, 0), DARK))
        P_.append((prefix + "-balok-ujung-a-%d" % x, box(160, CW, 120, x, 0, h - 120), color))
        for y in (0, CW - 160):
            P_.append((prefix + "-tiang-%d-%d" % (x, y), box(160, 160, h, x, y, 0), color))
            P_.append((prefix + "-cetakan-%d-%d" % (x, y), box(178, 162, 118, x - 9 if x == 0 else x - 9, y - 1, h - 118), DARK))
    P_.append((prefix + "-lantai", box(CL - 320, CW - 320, 28, 160, 160, 132), "#6b5a45"))
    # dinding bergelombang
    nrib = int((CL - 320) // 278)
    for side, y0, yy in (("left", 0, 0), ("right", CW - 30, CW - 60)):
        if side not in walls: continue
        P_.append((prefix + "-dinding-" + side, box(CL - 320, 2, h - 280, 160, y0 + (28 if side == "left" else 0), 160), color))
        for k in range(nrib):
            P_.append((prefix + "-rib-%s-%d" % (side, k), box(140, 30, h - 280, 180 + 278 * k, yy if side == "left" else CW - 30, 160), color))
    if "roof" in walls:
        P_.append((prefix + "-atap", box(CL - 320, CW - 320, 4, 160, 160, h - 30), color))
    if "back" in walls:
        P_.append((prefix + "-dinding-belakang", box(30, CW - 320, h - 280, 0, 160, 160), color))
    if "front" in walls:
        # pintu ganda + batang kunci
        for k in range(2):
            y0 = 160 + k * (CW - 320) / 2
            P_.append((prefix + "-pintu-%d" % k, box(30, (CW - 320) / 2 - 10, h - 280, CL - 30, y0 + 5, 160), color))
            for j in range(2):
                yb = y0 + (CW - 320) / 2 * (.25 + .5 * j)
                P_.append((prefix + "-kunci-%d%d" % (k, j), cyl(16, h - 400, CL + 10, yb, 220), DARK))
    # kisi ventilasi (louvre) di dinding kanan
    for k in range(louvres):
        x0 = 900 + k * 2200
        P_.append((prefix + "-louvre-%d" % k, box(1400, 60, 1200, x0, CW - 40, 1200), "#5b6670"))
        for j in range(8):
            P_.append((prefix + "-sirip-%d-%d" % (k, j), box(1400, 70, 30, x0, CW - 20, 1260 + 140 * j), DARK))
    for k in range(side_doors):
        x0 = 1500 + k * 7000
        P_.append((prefix + "-pintu-samping-%d" % k, box(1000, 50, 2100, x0, -30, 300), "#5b6670"))
    return P_

def frame_skid(Lx, Ly, x=0, y=0, z=0, h=250, color=PAINT_B, deck=True):
    """skid baja UNP 250: 2 balok memanjang, balok lintang tiap 1.5 m, pelat lantai checker"""
    P_ = []
    for yy in (0, Ly - 100):
        P_.append(("skid-memanjang-%d" % yy, box(Lx, 100, h, x, y + yy, z), color))
    n = int(Lx // 1500)
    for k in range(n + 1):
        P_.append(("skid-lintang-%d" % k, box(100, Ly - 200, h - 50, x + min(k * 1500, Lx - 100), y + 100, z + 25), color))
    if deck: P_.append(("skid-lantai", box(Lx, Ly, 8, x, y, z + h), "#8d9399"))
    for xx in (0, Lx - 200):
        for yy in (0, Ly - 200):
            P_.append(("skid-pengunci-%d-%d" % (xx, yy), box(200, 200, 120, x + xx, y + yy, z), DARK))
    return P_

def pipe_run(pts, r, name, color=PIPE):
    """pipa lurus antar titik 3D (ortogonal), dengan siku bola sederhana"""
    out = []
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        L_ = math.dist(a, b)
        if L_ < 1: continue
        d_ = tuple((b[k] - a[k]) / L_ for k in range(3))
        out.append(("%s-%d" % (name, i), cyl_dir(r, L_, a, d_), color))
        if i > 0: out.append(("%s-siku-%d" % (name, i), cq.Solid.makeSphere(r * 1.05).translate(cq.Vector(*a)), color))
    return out

# =====================================================================================================
# 3. PM-4 KONTAINER MEMBRAN
# =====================================================================================================
MOD_D, MOD_L = 220.0, 3000.0
def pm4(walls=("back", "left", "roof", "front", "right")):
    P_ = container("C4", walls=walls, louvres=2, side_doors=1)
    z0 = 160
    # dua rak modul UF (5 kolom x 4 tingkat), modul horizontal sepanjang kontainer; 34 terpasang
    n = 0
    for b, xb in enumerate((900, 4500)):
        for yy in (230, 230 + 5 * 270 + 70):
            for xx in (xb - 300, xb + MOD_L / 2 - 30, xb + MOD_L + 240):
                P_.append(("rak-tiang-%d-%d-%d" % (b, xx, yy), box(60, 60, 2300, xx, yy, z0 + 40), PAINT_G))
            for j in range(5):
                P_.append(("rak-rel-%d-%d-%d" % (b, yy, j), box(MOD_L + 600, 60, 50, xb - 300, yy, z0 + 40 + 120 + j * 520), PAINT_G))
        for j in range(4):
            for xx in (xb - 300, xb + MOD_L / 2 - 30, xb + MOD_L + 240):
                P_.append(("rak-lintang-%d-%d-%d" % (b, xx, j), box(60, 5 * 270 + 70, 40, xx, 290, z0 + 300 - 150 + j * 520), PAINT_G))
        for i in range(5):
            for j in range(4):
                if n >= 40: break
                yy = 380 + i * 270; zz = z0 + 300 + j * 520
                inst = n < EQ["membrane"]["modules"]
                P_.append(("MB-301-modul-%02d" % n, cyl(MOD_D / 2, MOD_L, xb, yy, zz, "x"), MEMB if inst else "#cfd4d9"))
                if inst:
                    P_.append(("MB-301-tutup-a%02d" % n, cyl(MOD_D / 2 + 15, 90, xb - 90, yy, zz, "x"), PAINT_B))
                    P_.append(("MB-301-tutup-b%02d" % n, cyl(MOD_D / 2 + 15, 90, xb + MOD_L, yy, zz, "x"), PAINT_B))
                n += 1
        # header umpan / retentat / permeat
        P_ += pipe_run([(xb - 160, 300, z0 + 300), (xb - 160, 300, z0 + 1860)], 84, "header-umpan-%d" % b, PAINT_B)
        P_ += pipe_run([(xb + MOD_L + 160, 300, z0 + 300), (xb + MOD_L + 160, 300, z0 + 1860)], 84, "header-retentat-%d" % b, PAINT_B)
        P_ += pipe_run([(xb + MOD_L / 2, 300 + 5 * 270 + 120, z0 + 250), (xb + MOD_L / 2, 300 + 5 * 270 + 120, z0 + 2150)], 45, "header-permeat-%d" % b, "#4e8fbf")
    # pompa cross-flow A/B + permeat + CIP di ujung belakang (lorong 850 mm di sisi kanan)
    P_ += pump(1500, 600, 230, 300, 8200, 620, z0 + 30, "P-301A")
    P_ += pump(1500, 600, 230, 300, 8200, 1400, z0 + 30, "P-301B")
    P_ += pump(900, 420, 140, 170, 10000, 600, z0 + 30, "P-302")
    P_.append(("TK-302", tube(800, 794, 1800, 10900, 1250, z0 + 30).fuse(cyl(800, 6, 10900, 1250, z0 + 30)), "#d8dcd2"))
    P_.append(("TK-302-tutup", cone(806, 300, 250, 10900, 1250, z0 + 1830), "#d8dcd2"))
    P_ += pump(700, 360, 110, 140, 10050, 1650, z0 + 30, "P-304")
    P_.append(("MCC-panel", box(600, 1600, 2200, 400, 400, z0 + 30), "#c7c9b8"))
    P_.append(("MCC-pintu", box(10, 1500, 2000, 1000, 450, z0 + 130), "#b5b7a6"))
    # nosel dinding (sambungan ke reaktor)
    for k, (yy, r_) in enumerate(((600, 84), (1000, 84), (1800, 45))):
        P_.append(("nosel-dinding-%d" % k, cyl(r_, 300, 0, yy, 600 + 300 * k, "-x"), PAINT_B))
    return P_

# =====================================================================================================
# 4. PM-1 SKID PRAOLAH (40 ft, terbuka)
# =====================================================================================================
def pm1():
    P_ = frame_skid(CL, CW)
    z0 = 258
    # sump 3 m3 di bawah saringan
    P_.append(("TK-sump", box(3200, 1900, 900, 300, 270, z0), "#9fb0a2"))
    # SC-101 saringan drum putar: rumah + drum + motor
    P_.append(("SC-101-rumah", box(3000, 1500, 1300, 400, 470, z0 + 900), "#8ea7b7"))
    P_.append(("SC-101-drum", cyl(450, 2600, 600, 1220, z0 + 1550, "x"), "#d0d6da"))
    P_.append(("SC-101-inlet", box(500, 700, 600, 400, 870, z0 + 2200), "#8ea7b7"))
    P_.append(("SC-101-motor", cyl(140, 500, 3400, 1220, z0 + 1550, "x"), MOTOR))
    P_.append(("SC-101-chute", box(500, 500, 500, 3400, 300, z0 + 900), "#8ea7b7"))
    P_ += pipe_run([(-400, 1220, z0 + 2500), (650, 1220, z0 + 2500)], 84, "N-inlet-POME", PIPE)
    # P-101 A/B
    P_ += pump(1100, 480, 160, 200, 3900, 600, z0, "P-101A")
    P_ += pump(1100, 480, 160, 200, 3900, 1500, z0, "P-101B")
    # HC-101 cluster 2 siklon di rangka
    for k, yy in enumerate((800, 1500)):
        P_.append(("HC-101-%d-kepala" % k, cyl(150, 400, 6000, yy, z0 + 2000), "#c2c7cc"))
        P_.append(("HC-101-%d-kerucut" % k, cone(150, 30, 1100, 6000, yy, z0 + 900), "#c2c7cc"))
        P_.append(("HC-101-%d-apex" % k, cyl(45, 300, 6000, yy, z0 + 600), DARK))
    P_.append(("HC-101-rangka", box(700, 1500, 60, 5650, 450, z0 + 1700), PAINT_B))
    for xx in (5650, 6290):
        for yy in (450, 1890):
            P_.append(("HC-101-kaki-%d-%d" % (xx, yy), box(60, 60, 1700, xx, yy, z0), PAINT_B))
    P_.append(("TK-pasir", box(900, 900, 550, 5650, 770, z0), "#7d6f5d"))
    # E-101 PHE: rangka + paket pelat
    P_.append(("E-101-pelat-tetap", box(120, 700, 1900, 7400, 870, z0), PAINT_B))
    P_.append(("E-101-paket", box(1300, 560, 1500, 7520, 940, z0 + 200), "#b8c4cf"))
    P_.append(("E-101-pelat-tekan", box(100, 650, 1700, 8820, 895, z0 + 100), PAINT_B))
    P_.append(("E-101-tiang", box(80, 120, 1900, 9900, 1160, z0), PAINT_B))
    for zz in (z0 + 120, z0 + 1750):
        P_.append(("E-101-batang-%d" % zz, box(2500, 40, 40, 7400, 1180, zz), DARK))
    for k, (zz, yy) in enumerate(((z0 + 400, 1000), (z0 + 1500, 1000), (z0 + 400, 1340), (z0 + 1500, 1340))):
        P_.append(("E-101-nosel-%d" % k, cyl(57, 300, 7400, yy, zz, "-x"), STEEL))
    # pipa antar alat
    P_ += pipe_run([(4300, 1220, z0 + 2200), (5850, 1220, z0 + 2200)], 57, "pipa-a", PIPE)
    P_ += pipe_run([(6000, 1150, z0 + 2400), (6000, 1150, z0 + 2700), (7250, 1150, z0 + 2700), (7250, 1000, z0 + 1500)], 57, "pipa-b", PIPE)
    P_ += pipe_run([(10200, 1150, z0 + 1500), (12400, 1150, z0 + 1500)], 57, "pipa-keluar", PIPE)
    # panel lokal + pegangan tangan
    P_.append(("panel-lokal", box(800, 400, 1800, 10600, 300, z0), "#c7c9b8"))
    for i_, s_ in enumerate(handrail([(0, 40), (CL, 40)], z0, 1100, 1500, 20)): P_.append(("rel-%d" % i_, s_, YELLOW))
    return P_

# =====================================================================================================
# 5. PM-5 SKID DOSING + POMPA UMPAN (20 ft)
# =====================================================================================================
L20 = 6058.0
def pm5():
    P_ = frame_skid(L20, CW)
    z0 = 258
    for k, (x, col, tg) in enumerate(((400, "#e6e1c8", "TK-201"), (2000, "#d9e6cf", "TK-202"))):
        P_.append((tg, cyl(650, 1600, x + 650, 700, z0), col))
        P_.append((tg + "-tutup", cyl(660, 30, x + 650, 700, z0 + 1600), col))
        P_.append((tg + "-motor", cyl(110, 350, x + 650, 700, z0 + 1630), MOTOR))
        P_.append((tg + "-bund", tube(800, 790, 300, x + 650, 700, z0), "#9a9a9a"))
    for k, (x, tg) in enumerate(((1200, "P-203"), (2800, "P-204"))):
        P_ += pump(600, 300, 90, 110, x, 1700, z0, tg)
    P_ += pump(1200, 480, 170, 200, 3700, 700, z0, "P-201A")
    P_ += pump(1200, 480, 170, 200, 3700, 1650, z0, "P-201B")
    P_ += pipe_run([(4000, 700, z0 + 800), (4000, 1650, z0 + 800)], 57, "header-umpan", PIPE)
    P_ += pipe_run([(4000, 1175, z0 + 800), (L20 + 300, 1175, z0 + 800)], 57, "keluar-umpan", PIPE)
    P_.append(("panel-dosing", box(500, 900, 1800, 5300, 200, z0), "#c7c9b8"))
    return P_

# =====================================================================================================
# 6. PM-6 SKID GAS: BTF-301 (bejana terpisah) + kontainer gas
# =====================================================================================================
BTF_D, BTF_H = 2400.0, 8000.0
M_DIST = 7300.0
def btf():
    P_ = frame_skid(3600, 3600, -1800, -1800, 0, 250, PAINT_B)
    z0 = 258
    r = BTF_D / 2
    P_.append(("BTF-301-shell", tube(r + 8, r, BTF_H, 0, 0, z0 + 400), FRP))
    P_.append(("BTF-301-atap", ellhead(r, 400, 8, z0 + 400 + BTF_H, True), FRP))
    P_.append(("BTF-301-dasar", cyl(r + 8, 400, 0, 0, z0), FRP))
    for k, zz in enumerate((z0 + 400 + 1500, z0 + 400 + 4300)):
        P_.append(("BTF-301-cincin-%d" % k, tube(r + 60, r + 8, 120, 0, 0, zz), FRP))
        P_.append(("BTF-301-unggun-%d" % k, cyl(r - 5, 2600, 0, 0, zz - 1300 + 60 + 650), "#7b8f5a"))
        P_.append(("BTF-301-grid-%d" % k, cyl(r - 5, 40, 0, 0, zz - 1300 + 60 + 610), DARK))
    P_.append(("BTF-301-distributor", cyl_dir(45, 2 * r - 40, (-r + 20, 0, z0 + 400 + M_DIST), (1, 0, 0)), PIPE))
    for tag, ang, zz, dn in (("Gas-in", 180, z0 + 1300, 250), ("Gas-out-top", None, "top", 250), ("Udara", 135, z0 + 1000, 50),
                             ("Resirk", 165, z0 + BTF_H - 300, 80), ("Sump", 300, z0 + 600, 80), ("MH", 240, z0 + 2200, 600)):
        if zz == "top": P_.append(("BTF-noz-" + tag, nozzle_vert(0, 0, z0 + 400 + BTF_H + 350, dn, 500), FRP)); continue
        P_.append(("BTF-noz-" + tag, nozzle_radial(r, ang, zz, dn, 350), FRP))
    P_ += pump(900, 420, 120, 150, 1200, -1500, z0, "P-305")
    P_.append(("K-301", cyl(260, 300, -1450, 1000, z0 + 200, "y"), PAINT_B))
    P_.append(("K-301-motor", cyl(110, 350, -1450, 1300, z0 + 460, "y"), MOTOR))
    # tangga
    for s in (-1, 1):
        P_.append(("BTF-tangga-%+d" % s, cyl(22, BTF_H + 600, -r - 300, s * 230, z0), YELLOW))
    for k in range(int((BTF_H + 400) // 300)):
        P_.append(("BTF-anak-tangga-%d" % k, cyl(12, 460, -r - 300, -230, z0 + 300 * (k + 1), "y"), YELLOW))
    return P_
def gas_container():
    P_ = container("C6", walls=("back", "left", "roof", "front", "right"), louvres=3, side_doors=1)
    z0 = 160
    # HX-301 pendingin gas shell-tube + CH-301 chiller
    P_.append(("HX-301", cyl(250, 2400, 700, 700, z0 + 1500, "x"), STEEL))
    for x in (700, 2900): P_.append(("HX-301-kaki-%d" % x, box(150, 400, 1300, x, 500, z0), DARK))
    P_.append(("CH-301", box(2200, 1100, 1600, 700, 1150, z0), "#d5d9dd"))
    # V-301
    P_.append(("V-301", cyl(350, 1500, 4200, 800, z0 + 300), STEEL))
    P_.append(("V-301-kepala", ellhead(350, 175, 6, z0 + 1800, True, 4200, 800), STEEL))
    P_.append(("V-301-kaki", cyl(200, 300, 4200, 800, z0), DARK))
    # K-302 A/B blower
    for k, yy in enumerate((800, 1650)):
        P_.append(("K-302%s" % "AB"[k], cyl(380, 450, 5600, yy - 225, z0 + 700, "y").rotate(cq.Vector(5600, yy, 0), cq.Vector(5600, yy, 1), 0), PAINT_B))
        P_.append(("K-302%s-motor" % "AB"[k], cyl(200, 700, 6300, yy, z0 + 700, "x"), MOTOR))
        P_.append(("K-302%s-alas" % "AB"[k], box(1500, 600, 300, 5500, yy - 300, z0), DARK))
    # AC-301 A/B
    for k, xx in enumerate((8200, 9800)):
        P_.append(("AC-301%s" % "AB"[k], cyl(600, 1800, xx, 1219, z0 + 350), "#8c99a6"))
        P_.append(("AC-301%s-atas" % "AB"[k], ellhead(600, 250, 6, z0 + 2150, True, xx, 1219), "#8c99a6"))
        P_.append(("AC-301%s-kaki" % "AB"[k], tube(560, 540, 350, xx, 1219, z0), DARK))
    P_.append(("panel-gas", box(500, 1200, 2100, 11300, 300, z0), "#c7c9b8"))
    P_ += pipe_run([(1000, 300, 2400), (11000, 300, 2400)], 125, "header-gas", "#c8a23a")
    return P_
def pm6():
    P_ = [(n, mv(s, 1800, 1800 + CW + 1200, 0), c) for n, s, c in btf()]
    P_ += gas_container()
    return P_

# =====================================================================================================
# 7. PM-7 PENAMPUNG GAS + FLARE
# =====================================================================================================
def gasholder():
    # kubah 3/4 bola: V = (2/3+1/4..)~ pakai tinggi h = 0.75 D: volume tutup bola
    Dg = 14000.0; h = 0.75 * Dg
    Rs = (Dg ** 2 / 4 + h ** 2) / (2 * h)
    P_ = []
    P_.append(("GH-pondasi", tube(Dg / 2 + 400, Dg / 2 - 300, 500, 0, 0, 0), CONC))
    P_.append(("GH-lantai", cyl(Dg / 2 - 300, 300, 0, 0, 0), CONC))
    def capshell(Rsph, zc, t):
        sph = cq.Solid.makeSphere(Rsph).translate(cq.Vector(0, 0, zc)).cut(cq.Solid.makeSphere(Rsph - t).translate(cq.Vector(0, 0, zc)))
        return sph.cut(box(4 * Rsph, 4 * Rsph, 2 * Rsph, -2 * Rsph, -2 * Rsph, 500 + 250 - 2 * Rsph))
    P_.append(("GH-membran-luar", capshell(Rs, 500 + h - Rs, 40), "#e7ecef"))
    hi = 0.55 * h; Ri = ((Dg / 2 - 150) ** 2 + hi ** 2) / (2 * hi)
    P_.append(("GH-membran-dalam", capshell(Ri, 500 + 250 + hi - Ri, 20), "#cfd6dc"))
    P_.append(("GH-cincin-angkur", tube(Dg / 2 + 120, Dg / 2 - 20, 250, 0, 0, 500), DARK))
    P_.append(("GH-blower", cyl(400, 600, Dg / 2 + 900, 0, 500, "z"), PAINT_B))
    P_.append(("GH-blower-motor", cyl(180, 500, Dg / 2 + 900, -300, 1300, "y"), MOTOR))
    P_ += pipe_run([(Dg / 2 + 900, 0, 1100), (Dg / 2 + 120, 0, 1100)], 100, "GH-udara", PIPE)
    P_.append(("GH-katup-pengaman", cyl(300, 1400, -Dg / 2 - 700, 0, 0), "#7d8a6b"))
    P_.append(("GH-tangga-ukur", box(200, 200, 2500, -Dg / 2 - 300, 600, 0), YELLOW))
    for k, a in enumerate((90, 270)):
        P_ += pipe_run([(math.cos(math.radians(a)) * (Dg / 2 + 1200), math.sin(math.radians(a)) * (Dg / 2 + 1200), 300), (math.cos(math.radians(a)) * 2500, math.sin(math.radians(a)) * 2500, 300)], 110, "GH-pipa-%d" % k, "#c8a23a")
    return P_, Dg, h
def flare():
    P_ = frame_skid(2500, 2500, -1250, -1250, 0, 250, PAINT_B)
    P_.append(("FL-301-badan", cyl(700, 6500, 0, 0, 258), "#b9b2a7"))
    P_.append(("FL-301-topi", tube(760, 700, 400, 0, 0, 258 + 6100), DARK))
    for k in range(4):
        a = math.pi / 2 * k
        P_.append(("FL-louvre-%d" % k, box(500, 80, 600, 700 * math.cos(a) - 250, 700 * math.sin(a) - 40, 500).rotate(cq.Vector(700 * math.cos(a), 700 * math.sin(a), 0), cq.Vector(700 * math.cos(a), 700 * math.sin(a), 1), math.degrees(a) + 90), "#7d756b"))
    P_ += pipe_run([(-1250, 0, 900), (-700, 0, 900)], 84, "FL-gas", "#c8a23a")
    P_.append(("FL-panel", box(500, 300, 1400, 600, -1200, 258), "#c7c9b8"))
    return P_
def pm7():
    P_, Dg, h = gasholder()
    P_ += [(n, mv(s, Dg / 2 + 5000, 0, 0), c) for n, s, c in flare()]
    return P_

# =====================================================================================================
# 8. PM-8 KONTAINER CHP + PM-9 HX-401 + ST-401
# =====================================================================================================
def pm8(walls=("back", "left", "roof", "front", "right")):
    P_ = container("C8", walls=walls, louvres=3, side_doors=1)
    z0 = 160
    # mesin gas V-12 + generator di rangka dasar
    P_.append(("GE-rangka", box(6800, 1300, 250, 1500, 570, z0), DARK))
    P_.append(("GE-mesin-blok", box(3600, 1100, 1300, 1700, 670, z0 + 250), "#4f7a4f"))
    for k in range(6):
        for s in (0, 1):
            P_.append(("GE-kepala-%d%d" % (k, s), box(450, 380, 300, 1850 + k * 560, 690 + s * 680, z0 + 1550), "#5f8a5f"))
    P_.append(("GE-turbo", cyl(260, 500, 5350, 1220, z0 + 1500, "x"), STEEL))
    P_.append(("GE-roda-gila", cyl(650, 300, 5300, 1220, z0 + 950, "x"), DARK))
    P_.append(("GE-generator", cyl(600, 2000, 5600, 1220, z0 + 950, "x"), "#2f5d8a"))
    P_.append(("GE-terminal", box(500, 700, 500, 6500, 870, z0 + 1550), "#2f5d8a"))
    P_.append(("GE-panel", box(700, 1600, 2200, 10900, 400, z0), "#c7c9b8"))
    P_.append(("GE-katup-gas", box(900, 400, 900, 400, 1700, z0), "#c8a23a"))
    # atap: radiator + silencer
    P_.append(("radiator", box(4000, 2200, 1100, 7000, 120, CH), "#7a8590"))
    for k in range(3):
        P_.append(("radiator-kipas-%d" % k, cyl(550, 120, 7700 + k * 1300, 1219, CH + 1100), DARK))
    P_.append(("silencer", cyl(450, 3200, 1700, 1219, CH + 700, "x"), STEEL))
    P_ += pipe_run([(5350, 1219, z0 + 1760), (5350, 1219, CH + 700), (4900, 1219, CH + 700)], 160, "pipa-turbo-silencer", STEEL)
    for x in (2000, 4500): P_.append(("silencer-dudukan-%d" % x, box(200, 800, 700, x, 819, CH), DARK))
    # HX-401 pemulih panas gas buang (PM-9) dan cerobong ST-401
    P_.append(("HX-401", box(1200, 1200, 2400, -2200, 600, 0), "#9aa7b4"))
    P_.append(("HX-401-kaki", box(1400, 1400, 300, -2300, 500, 0), DARK))
    P_.append(("ST-401", cyl(300, 7500, -1600, 1200, 2400), STEEL))
    P_ += pipe_run([(1700, 1219, CH + 700), (-1600, 1219, CH + 700)], 220, "pipa-buang", STEEL)
    P_ += pipe_run([(-1600, 1219, CH + 700), (-1600, 1219, 2450)], 220, "pipa-buang-turun", STEEL)
    P_ += pipe_run([(-1000, 900, 1500), (300, 900, 1500)], 70, "pipa-HW-a", RED)
    P_ += pipe_run([(-1000, 1500, 1200), (300, 1500, 1200)], 70, "pipa-HW-b", RED)
    return P_

# =====================================================================================================
# 9. CT-601 + P-601 ; 10. PM-10 SKID LUMPUR
# =====================================================================================================
def pm9_ct():
    P_ = frame_skid(4200, 3400, 0, 0, 0, 250, PAINT_B)
    z0 = 258
    P_.append(("CT-601-bak", box(3800, 3000, 600, 200, 200, z0), "#5f7f8f"))
    P_.append(("CT-601-badan", box(3600, 2800, 2600, 300, 300, z0 + 600), "#8fb1bf"))
    P_.append(("CT-601-cerobong-kipas", cyl(1150, 900, 2100, 1700, z0 + 3200), "#5f7f8f"))
    P_.append(("CT-601-motor", cyl(200, 300, 2100, 1700, z0 + 4100), MOTOR))
    for k in range(5): P_.append(("CT-louvre-%d" % k, box(3600, 40, 120, 300, 280, z0 + 700 + 200 * k), "#4f6b78"))
    P_ += pump(1100, 450, 160, 190, 4200 - 1150, 3600, z0 - 258, "P-601")
    return P_
def pm10():
    P_ = frame_skid(L20, CW)
    z0 = 258
    P_ += pump(1300, 420, 140, 170, 300, 600, z0, "P-303")
    P_.append(("PR-501-badan", cyl(380, 3200, 1900, 1400, z0 + 1000, "x").rotate(cq.Vector(1900, 1400, z0 + 1000), cq.Vector(1900, 1401, z0 + 1000), -8), "#b9c2c9"))
    P_.append(("PR-501-corong", cone(250, 600, 600, 2300, 1400, z0 + 1300), "#b9c2c9"))
    P_.append(("PR-501-motor", cyl(250, 700, 5100, 1400, z0 + 1450, "x"), MOTOR))
    P_.append(("PR-501-kaki", box(3200, 1000, 700, 1900, 900, z0), DARK))
    P_.append(("PR-501-chute", box(600, 600, 900, 1500, 1100, z0 - 100), "#b9c2c9"))
    P_.append(("TK-polimer", cyl(400, 1000, 5400, 500, z0), "#e6e1c8"))
    P_ += pump(600, 260, 70, 90, 4300, 500, z0, "P-polimer")
    return P_

# =====================================================================================================
# 11. SUSUNAN PABRIK 45 t TBS/jam
# =====================================================================================================
PITCH = 6400.0
def plant(simple=True):
    """reaktor 2 baris x 7, TK-101 dan TK-301 di ujung, modul di sekitarnya. Origin: sudut barat-daya plot."""
    out = []
    def add(parts, dx, dy, dz=0, rz=0, pre=""):
        for n, s, c in parts:
            s2 = s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rz) if rz else s
            out.append((pre + n, mv(s2, dx, dy, dz), c))
    rv = vessel("reactor", ladder=not simple)
    tk = vessel("tank", ladder=not simple)
    x0, y0 = 9500, 15500
    tags = []
    for row in range(2):
        for k in range(7):
            n = row * 7 + k + 1
            add(rv, x0 + PITCH * (k + 1), y0 + PITCH * row, pre="R-2%02d/" % n); tags.append(("R-2%02d" % n, x0 + PITCH * (k + 1), y0 + PITCH * row))
    add(tk, x0, y0, pre="TK-101/"); tags.append(("TK-101", x0, y0))
    add(tk, x0, y0 + PITCH, pre="TK-301/"); tags.append(("TK-301", x0, y0 + PITCH))
    # pipe rack di tengah antar baris
    yr = y0 + PITCH / 2
    for k in range(9):
        xx = x0 + PITCH * k - 300
        out.append(("rack-tiang-%d" % k, box(250, 1200, 5000, xx, yr - 600, 0), PAINT_B))
    out.append(("rack-balok", box(PITCH * 8 + 600, 1200, 250, x0 - 300, yr - 600, 5000), PAINT_B))
    for j, (dy, r_, col) in enumerate(((-350, 84, PIPE), (0, 109, "#c8a23a"), (350, 84, PIPE))):
        out.append(("rack-pipa-%d" % j, cyl(r_, PITCH * 8 + 600, x0 - 300, yr + dy, 5250 + r_, "x"), col))
    # modul
    yb = y0 + PITCH + 5200
    add(pm4(), x0 + PITCH * 2, yb, pre="PM-4/")
    add(pm1(), x0 - 1500, y0 - 9500, pre="PM-1/")
    add(pm5(), x0 + PITCH * 2 + 2000, y0 - 9500, pre="PM-5/")
    add(pm10(), x0 + PITCH * 4 + 1000, y0 - 9500, pre="PM-10/")
    add(pm9_ct(), x0 - 8800, y0 + PITCH / 2 - 1700, pre="PM-9/")
    add(gas_container(), x0 + PITCH * 4 + 1000, yb, pre="PM-6/")
    add(btf(), x0 + PITCH * 8 + 3500, yb + 1200, pre="PM-6/")
    gh, Dg, hgh = gasholder()
    add(gh, x0 + PITCH * 8 + 15500, y0 + PITCH / 2, pre="PM-7/")
    add(flare(), x0 + PITCH * 8 + 22000, y0 - 10000, pre="PM-7/")
    add(pm8(), x0 + PITCH * 8 + 4500, y0 - 10500, pre="PM-8A/")
    add(pm8(), x0 + PITCH * 8 + 4500, y0 - 6500, pre="PM-8B/")
    # jalan + pagar batas plot
    # batas plot = kotak pembatas peralatan + jalan akses 3 m
    xs, ys = [], []
    for n, s_, c in out:
        bb = s_.BoundingBox(); xs += [bb.xmin, bb.xmax]; ys += [bb.ymin, bb.ymax]
    X0, X1, Y0, Y1 = min(xs) - 3000, max(xs) + 3000, min(ys) - 3000, max(ys) + 3000
    out.append(("plot-lantai", box(X1 - X0, Y1 - Y0, 10, X0, Y0, -10), "#dcd8cf"))
    return out, tags, (X0, Y0, X1, Y1)

MODULES = {"R-201": lambda: vessel("reactor"), "TK-101": lambda: vessel("tank"), "PM-1": pm1, "PM-4": pm4, "PM-5": pm5,
           "PM-6": pm6, "PM-7": pm7, "PM-8": pm8, "PM-9": pm9_ct, "PM-10": pm10}
