# -*- coding: utf-8 -*-
"""
Model 3D lokasi lengkap: PKS proksi 45 t TBS/jam + sistem kolam POME + produk (set generator biogas portabel) + kebun sawit.
Satuan mm, origin = sudut barat-daya pagar PKS, X timur, Y utara, Z atas.

Ukuran proksi PKS mengikuti praktik umum PKS 45 t/jam di Sumatera (kapasitas tercantum di setiap fungsi).
Kolam POME diukur dari debit POME hasil neraca (results.json) dan HRT tipikal sistem kolam Indonesia.
Fungsi site() mengembalikan (parts, info): info berisi jejak 2D untuk denah, panjang rute pipa/kabel, luas kolam
dan pemeriksaan jarak aman -> ditulis ke cad/out/site.json dan dipakai model keuangan.
"""
import math, json, os
import cadquery as cq
import bgmodels as M
from bgmodels import box, cyl, tube, cone, cyl_dir, pipe_run, mv, union

HERE = os.path.dirname(os.path.abspath(__file__))
m = 1000.0
# warna
GROUND = "#9fb27a"; YARD = "#cfc3a5"; ROAD = "#6e6e6e"; ROOF = "#8aa1b4"; WALL = "#d9d6cc"; STEELC = "#9aa7b4"; RUST = "#9c6b4e"
CPO = "#c56b2a"; WATER_A = "#4a3b2c"; WATER_F = "#6b6a3d"; WATER_O = "#5f8a6a"; WATER_C = "#7a5a3a"; WATER_R = "#5d86a3"; BUND = "#b49c78"
GRASS = "#8fb46a"; TRUNK = "#6b5136"; CROWN = "#3f7a3a"; CONCR = "#bdb8ad"; PIPEC = "#8e969e"; HOT = "#b6463d"; PLN = "#2f5d8a"

R = M.R
POME = R["design_basis"]["pome_m3d"]            # m3/d

def gable(x, y, L, W, he, hr, color=ROOF, name="atap"):
    """atap pelana sepanjang X: lebar W (Y), tinggi tritis he, bubungan hr"""
    pts = [cq.Vector(x, y - 300, he), cq.Vector(x, y + W / 2, hr), cq.Vector(x, y + W + 300, he), cq.Vector(x, y + W + 300, he - 150),
           cq.Vector(x, y + W / 2, hr - 150), cq.Vector(x, y - 300, he - 150)]
    f = cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))
    return (name, cq.Solid.extrudeLinear(f, cq.Vector(L, 0, 0)), color)

def building(name, x, y, L, W, H, roof=True, wall=WALL, rc=ROOF, ridge=2500, windows=True):
    P = [(name + "-dinding", box(L, W, H, x, y, 0), wall)]
    if roof: P.append(gable(x - 300, y, L + 600, W, H, H + ridge, rc, name + "-atap"))
    if windows:
        for side in (y - 20, y + W - 30):
            P.append((name + "-jendela-%d" % side, box(L - 2000, 50, 1200, x + 1000, side, H - 2200), "#5d7486"))
    return P

class Site:
    def __init__(s):
        s.P = []; s.foot = []; s.routes = {}; s.area = {}; s.pts = {}
    def add(s, parts, dx=0, dy=0, dz=0, rz=0, pre=""):
        for n, sh, c in parts:
            sh2 = sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rz) if rz else sh
            s.P.append((pre + n, mv(sh2, dx, dy, dz), c))
    def fp(s, kind, tag, geom, label=None, grp="PKS"):
        """jejak denah: kind 'rect' geom=(x,y,L,W) | 'circ' geom=(cx,cy,r)"""
        s.foot.append(dict(kind=kind, tag=tag, geom=geom, label=label or tag, grp=grp))

# ============================================================================================ PKS proksi
def mill(S):
    # halaman PKS (laterit dipadatkan) + jalan beton
    S.add([("halaman-PKS", box(232 * m, 205 * m, 40, -5 * m, -5 * m, 0), YARD)])
    for nm, (x, y, L, W) in {"jalan-utama": (36, -5, 8, 200), "jalan-timur": (36, 50, 200, 8), "jalan-proses": (44, 140, 190, 7),
                             "jalan-site": (228, -5, 6, 150)}.items():
        S.add([(nm, box(L * m, W * m, 60, x * m, y * m, 40), ROAD)])
    # pos jaga + jembatan timbang (2 x 60 t)
    S.add([("pos-jaga", box(4 * m, 4 * m, 3 * m, 30 * m, 2 * m, 0), WALL), gable(29.7 * m, 2 * m, 4.6 * m, 4 * m, 3 * m, 4 * m, "#b85c3a", "pos-atap")])
    for k in range(2):
        S.add([("jembatan-timbang-%d" % k, box(18 * m, 3.4 * m, 350, 46 * m, (12 + 6 * k) * m, 40), "#55595e")])
    S.add(building("rumah-timbang", 66 * m, 13 * m, 6 * m, 5 * m, 3.2 * m, ridge=1200))
    S.fp("rect", "WB", (46, 12, 18, 9.4), "Jembatan timbang 2 x 60 t")
    # kantor, laboratorium, bengkel, gudang, musala
    for tag, nm, (x, y, L, W, H) in (("OF", "kantor", (4, 12, 24, 14, 7)), ("LB", "laboratorium", (4, 32, 16, 10, 4)),
                                     ("WS", "bengkel", (150, 15, 30, 18, 8)), ("ST", "gudang", (150, 37, 22, 12, 7)), ("MS", "musala", (4, 48, 12, 10, 5))):
        S.add(building(nm, x * m, y * m, L * m, W * m, H * m, ridge=2000 if H > 5 else 1200))
        S.fp("rect", tag, (x, y, L, W), nm.capitalize())
    # loading ramp TBS (20 pintu x 15 t) + atap
    x0, y0 = 60, 58
    S.add([("loading-ramp-dek", box(60 * m, 14 * m, 4 * m, x0 * m, y0 * m, 0), CONCR)])
    for k in range(21):
        S.add([("loading-ramp-sekat-%d" % k, box(250, 9 * m, 1500, (x0 + k * 3) * m - 125, (y0 + 2) * m, 4 * m), "#7f7f7f")])
    for k in range(7):
        for yy in (y0, y0 + 13.6):
            S.add([("loading-ramp-tiang-%d-%d" % (k, yy), box(300, 300, 5 * m, (x0 + k * 10) * m, yy * m, 4 * m), STEELC)])
    S.add([gable(x0 * m - 1000, y0 * m, 62 * m, 14 * m, 9 * m, 10.5 * m, "#7f97a8", "loading-ramp-atap")])
    S.fp("rect", "LR", (x0, y0, 60, 14), "Loading ramp TBS 20 pintu")
    # rel lori + 3 rebusan horizontal Ø2,7 x 30 m (kapasitas 3 x 10 lori x 2,5 t)
    for k in range(3):
        yc = 78 + 5.5 * k
        S.add([("rebusan-%d" % k, cyl(1350, 30 * m, 70 * m, yc * m, 1900, "x"), "#8f9aa5"),
               ("rebusan-pintu-%d" % k, cyl(1500, 400, 69.6 * m, yc * m, 1900, "x"), "#5a6570")])
        for j in range(5):
            S.add([("rebusan-sadel-%d-%d" % (k, j), box(800, 2600, 600, (72 + j * 6.5) * m, yc * m - 1300, 0), CONCR)])
        for dy in (-500, 500):
            S.add([("rel-%d-%d" % (k, dy), box(70 * m, 80, 150, 40 * m, yc * m + dy, 40), "#555555")])
    S.fp("rect", "ST", (70, 76.6, 30, 13.8), "Rebusan 3 x 30 m")
    # bangunan pabrik utama (penebah, digester & press, klarifikasi, nut & kernel)
    S.add(building("pabrik-utama", 60 * m, 95 * m, 70 * m, 30 * m, 18 * m, ridge=4000))
    S.fp("rect", "MB", (60, 95, 70, 30), "Pabrik utama: penebah, press, klarifikasi, kernel")
    # tangki klarifikasi luar (CST Ø8 x 7, tangki minyak murni 2 x Ø6 x 6, tangki sludge Ø5 x 5)
    for tag, (x, y, r, h, c) in {"CST": (138, 104, 4, 7, CPO), "OT1": (140, 116, 3, 6, CPO), "OT2": (147, 116, 3, 6, CPO), "SLT": (147, 105, 2.5, 5, RUST)}.items():
        S.add([("tangki-" + tag, cyl(r * m, h * m, x * m, y * m, 0), c), ("tangki-atap-" + tag, cone(r * m + 50, 300, 700, x * m, y * m, h * m), c)])
    S.fp("rect", "CL", (134, 101, 16.5, 18), "Stasiun klarifikasi (CST, tangki minyak)")
    # silo kernel 3 x Ø4 x 10 di kaki 4 m
    for k in range(3):
        xx = (64 + 6 * k) * m
        S.add([("silo-kernel-%d" % k, cyl(2 * m, 8 * m, xx, 132 * m, 4 * m), "#c9c4b5"), ("silo-kernel-kerucut-%d" % k, cone(300, 2 * m, 2 * m, xx, 132 * m, 2 * m), "#c9c4b5")])
        for dx in (-1500, 1500):
            for dy in (-1500, 1500): S.add([("silo-kaki-%d-%d-%d" % (k, dx, dy), box(200, 200, 4 * m, xx + dx, 132 * m + dy, 0), STEELC)])
    S.fp("rect", "KS", (61.5, 129.5, 17, 5), "Silo kernel")
    # rumah boiler (2 x 30 t/jam uap, bahan bakar serat + cangkang) + cerobong Ø2,5 x 40 m
    S.add(building("rumah-boiler", 156 * m, 95 * m, 28 * m, 22 * m, 20 * m, wall="#c9bfa8", ridge=3000))
    S.add([("cerobong-boiler", cyl(1250, 40 * m, 190 * m, 106 * m, 0), "#77736d"), ("cerobong-dasar", box(5 * m, 5 * m, 3 * m, 187.5 * m, 103.5 * m, 0), CONCR)])
    S.add([("dust-collector", cyl(1800, 6 * m, 190 * m, 99 * m, 5 * m), "#8f8a83"), ("dust-kaki", box(3 * m, 3 * m, 5 * m, 188.5 * m, 97.5 * m, 0), STEELC)])
    S.fp("rect", "BH", (156, 95, 28, 22), "Rumah boiler 2 x 30 t uap/jam")
    S.fp("circ", "CH", (190, 106, 1.25), "Cerobong boiler 40 m")
    # konveyor serat & cangkang (pabrik -> boiler)
    S.add([("konveyor-serat", cyl_dir(700, 27 * m, (130 * m, 110 * m, 9 * m), (1, 0, .33)), "#a0a7ad")])
    # rumah mesin: turbin uap 1,2 MW back-pressure + 2 genset diesel 500 kVA (cadangan) + BPV
    S.add(building("rumah-mesin", 156 * m, 122 * m, 26 * m, 16 * m, 9 * m, ridge=2000))
    S.fp("rect", "ER", (156, 122, 26, 16), "Rumah mesin: turbin uap 1,2 MW + genset diesel")
    S.add([("tangki-solar", cyl(1600, 5 * m, 186 * m, 132 * m, 0), "#d8d0b0")])
    # pengolahan air: kolam air baku, 2 klarifier Ø12, filter, menara air Ø7 di 18 m
    S.add([("kolam-air-baku-tanggul", box(42 * m, 40 * m, 1.2 * m, -2 * m, 148 * m, 0), BUND), ("kolam-air-baku", box(38 * m, 36 * m, 1.25 * m, 0, 150 * m, 0), WATER_R)])
    S.fp("rect", "RW", (-2, 148, 42, 40), "Kolam air baku")
    for k in range(2):
        S.add([("klarifier-air-%d" % k, tube(6 * m, 5.8 * m, 4 * m, (52 + 15 * k) * m, 163 * m, 0).fuse(cyl(5.8 * m, 3.5 * m, (52 + 15 * k) * m, 163 * m, 0)), "#9fb3c0")])
    S.add([("menara-air", cyl(3.5 * m, 5 * m, 82 * m, 170 * m, 18 * m), "#9fb3c0")])
    for dx in (-2500, 2500):
        for dy in (-2500, 2500): S.add([("menara-kaki-%d-%d" % (dx, dy), box(300, 300, 18 * m, 82 * m + dx, 170 * m + dy, 0), STEELC)])
    S.fp("rect", "WT", (46, 157, 40, 18), "Pengolahan air + menara air")
    # tangki timbun CPO 2 x 2.000 t (Ø16 x 12 m) dalam tanggul
    S.add([("tanggul-CPO", box(62 * m, 30 * m, 1.5 * m, 96 * m, 154 * m, 0).cut(box(60 * m, 28 * m, 2 * m, 97 * m, 155 * m, 0)), CONCR)])
    for k, xx in enumerate((112, 140)):
        S.add([("tangki-CPO-%d" % k, cyl(8 * m, 12 * m, xx * m, 169 * m, 0), "#d9d5cc"), ("tangki-CPO-atap-%d" % k, cone(8.05 * m, 300, 1.2 * m, xx * m, 169 * m, 12 * m), "#c7c3ba")])
    S.add([("depot-muat-CPO", box(12 * m, 6 * m, 6 * m, 160 * m, 160 * m, 0), STEELC)])
    S.fp("rect", "CT", (96, 154, 62, 30), "Tangki CPO 2 x 2.000 t")
    # hopper tandan kosong (TKS) di kaki 6 m + truk
    S.add([("hopper-TKS", box(10 * m, 8 * m, 4 * m, 132 * m, 64 * m, 6 * m), "#7d7366")])
    for dx in (0, 9.5):
        for dy in (0, 7.5): S.add([("hopper-kaki-%d-%d" % (dx, dy), box(400, 400, 6 * m, (132 + dx) * m, (64 + dy) * m, 0), STEELC)])
    S.fp("rect", "EF", (132, 64, 10, 8), "Hopper TKS")
    # truk TBS di ramp
    for k in range(3):
        S.add(truck((52 + 0) * m, (60 + 4 * k) * m, "truk-TBS-%d" % k))
    # fat pit + sludge pit (kolam pengutip minyak, beton)
    S.add([("fat-pit-dinding", box(26 * m, 12 * m, 1.0 * m, 190 * m, 140 * m, 0).cut(box(25 * m, 11 * m, 2 * m, 190.5 * m, 140.5 * m, -0.5 * m)), CONCR),
           ("fat-pit-isi", box(25 * m, 11 * m, 600, 190.5 * m, 140.5 * m, 0), WATER_C)])
    S.fp("rect", "FP", (190, 140, 26, 12), "Fat pit (sumber POME)")
    S.pts["fatpit_out"] = (216, 146)
    S.pts["boiler"] = (184, 100)
    # pagar PKS
    fence(S, [(-5, -5), (227, -5), (227, 200), (-5, 200), (-5, -5)], gate=(36, 44))

def truck(x, y, name):
    return [(name + "-kabin", box(2.3 * m, 2.4 * m, 2.6 * m, x, y, 0), "#c9d1d8"), (name + "-bak", box(5.5 * m, 2.4 * m, 2.4 * m, x + 2.4 * m, y, 900), "#6f7d5d"),
            (name + "-muatan", box(5.3 * m, 2.2 * m, 900, x + 2.5 * m, y + 100, 3300), "#7a4b2f")]

def fence(S, pts, gate=None, h=2100):
    for i, ((ax, ay), (bx, by)) in enumerate(zip(pts[:-1], pts[1:])):
        Lg = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / Lg, (by - ay) / Lg
        segs = [(0, Lg)]
        if gate and i == 0 and ay == by: segs = [(0, gate[0] - ax), (gate[1] - ax, Lg)]
        for a, b in segs:
            if b - a < .5: continue
            S.P.append(("pagar-%d-%d" % (i, a), cyl_dir(30, (b - a) * m, ((ax + ux * a) * m, (ay + uy * a) * m, h - 200), (ux, uy, 0)), "#5d7a5d"))
            S.P.append(("pagar-b-%d-%d" % (i, a), cyl_dir(30, (b - a) * m, ((ax + ux * a) * m, (ay + uy * a) * m, 400), (ux, uy, 0)), "#5d7a5d"))
            n = max(1, int((b - a) // 4))
            for j in range(n + 1):
                t = a + (b - a) * j / n
                S.P.append(("pagar-t-%d-%d-%d" % (i, a, j), box(80, 80, h, (ax + ux * t) * m - 40, (ay + uy * t) * m - 40, 0), "#5d7a5d"))

# ============================================================================================ kolam POME
# HRT tipikal sistem kolam PKS Indonesia: pendingin 2 d, pengasaman 5 d, anaerobik 60 d, fakultatif 15 d, aerobik 2 x 7,5 d
PONDS = [  # tag, nama, HRT d, kedalaman m, x, y, L (x), status setelah produk ('tetap'/'dibebaskan'), warna air
    ("CP1", "Kolam pendingin 1", 1.0, 2.5, 244, 90, 26, "tetap", WATER_C),
    ("CP2", "Kolam pendingin 2", 1.0, 2.5, 244, 112, 26, "tetap", WATER_C),
    ("AC", "Kolam pengasaman", 5.0, 3.5, 278, 90, 40, "dibebaskan", WATER_C),
    ("AN1", "Kolam anaerobik 1", 30.0, 5.0, 326, 90, 66, "dibebaskan", WATER_A),
    ("AN2", "Kolam anaerobik 2", 30.0, 5.0, 400, 90, 66, "dibebaskan", WATER_A),
    ("FA", "Kolam fakultatif", 15.0, 3.0, 244, 154, 70, "tetap", WATER_F),
    ("AE1", "Kolam aerobik 1", 7.5, 2.0, 322, 154, 70, "tetap", WATER_O),
    ("AE2", "Kolam aerobik 2", 7.5, 2.0, 400, 154, 66, "tetap", WATER_O),
]
def ponds(S):
    tot_before = tot_after = 0.0
    for tag, nm, hrt, dep, x, y, L, st, col in PONDS:
        V = POME * hrt                       # m3
        W = V / (dep * L) + 2 * 1.5 * dep * .5    # lebar permukaan (lereng 1:1,5 dipertimbangkan kasar)
        Wb = W + 6
        S.add([(tag + "-tanggul", box((L + 6) * m, Wb * m, 1.2 * m, (x - 3) * m, (y - 3) * m, 0).cut(box(L * m, W * m, 3 * m, x * m, y * m, -0.5 * m)), BUND)])
        if st == "tetap":
            S.add([(tag + "-air", box(L * m, W * m, 0.9 * m, x * m, y * m, 0), col)])
            if tag.startswith("AN") or tag == "AC": pass
        else:
            S.add([(tag + "-lahan-dibebaskan", box(L * m, W * m, 1.0 * m, x * m, y * m, 0), GRASS)])
        S.fp("rect", tag, (x - 3, y - 3, L + 6, Wb), "%s (%s m³, HRT %s d)%s" % (nm, format(round(V), ","), hrt, "" if st == "tetap" else " - DIBEBASKAN"), grp="KOLAM")
        S.area[tag] = dict(name=nm, V_m3=V, area_m2=(L + 6) * Wb, status=st, hrt=hrt, depth=dep, x=x, y=y, L=L, W=W)
        tot_before += (L + 6) * Wb
        if st == "tetap": tot_after += (L + 6) * Wb
    S.area["_total_before_m2"] = tot_before; S.area["_total_after_m2"] = tot_after
    # lahan aplikasi (land application) flatbed di kebun utara
    for k in range(8):
        S.add([("flatbed-%d" % k, box(40 * m, 4 * m, 300, (250 + 45 * (k % 4)) * m, (214 + 8 * (k // 4)) * m, 0), WATER_F)])
    S.fp("rect", "LA", (250, 212, 175, 16), "Flatbed aplikasi lahan (efluen ke kebun)", grp="KOLAM")

# ============================================================================================ kebun sawit
def palms(S, region, exclude, sp=9.0):
    x0, y0, x1, y1 = region; n = 0; row = 0
    y = y0
    while y < y1:
        x = x0 + (sp / 2 if row % 2 else 0)
        while x < x1:
            if not any(a <= x <= c and b <= y <= d for a, b, c, d in exclude):
                S.P.append(("sawit-batang-%d" % n, cyl(300, 6 * m, x * m, y * m, 0), TRUNK))
                S.P.append(("sawit-tajuk-%d" % n, cone(600, 4.5 * m, 2.2 * m, x * m, y * m, 5.6 * m), CROWN))
                S.P.append(("sawit-tajuk-atas-%d" % n, cone(4.5 * m, 400, 1.2 * m, x * m, y * m, 7.8 * m), CROWN))
                n += 1
            x += sp
        y += sp * math.sqrt(3) / 2; row += 1
    return n

# ============================================================================================ produk + interkoneksi
PRODUCT_ORIGIN = (247.3, 28.0)        # m: pergeseran koordinat lokal model pabrik produk -> koordinat site
def product(S):
    out, tags, (X0, Y0, X1, Y1) = M.plant(simple=False)
    dx, dy = PRODUCT_ORIGIN
    for n, sh, c in out:
        if n == "plot-lantai": c = "#c9c4b8"
        S.P.append(("PRODUK/" + n, mv(sh, dx * m, dy * m, 0), c))
    S.fp("rect", "PRODUK", (X0 / m + dx, Y0 / m + dy, (X1 - X0) / m, (Y1 - Y0) / m), "PRODUK: set generator biogas portabel", grp="PRODUK")
    S.pts["prod_bb"] = (X0 / m + dx, Y0 / m + dy, X1 / m + dx, Y1 / m + dy)
    S.pts["PM1_in"] = ((9500 - 1500 - 400) / m + dx, (15500 - 9500 + 1220) / m + dy)        # nosel masuk POME PM-1
    S.pts["TK301"] = (9500 / m + dx, (15500 + 6400) / m + dy)                             # tangki permeat (efluen)
    S.pts["HX401"] = ((49300 - 1600) / m + dx, (15500 - 10500 + 1200) / m + dy)           # HX-401 pemulih panas
    S.pts["CHP"] = ((49300 + 6000) / m + dx, (15500 - 10500) / m + dy)
    S.pts["GH"] = ((9500 + 51200 + 15500) / m + dx, (15500 + 6900) / m + dy)
    S.pts["FL"] = (92.0 + dx, 5.0 + dy)
    S.pts["TK101"] = (9500 / m + dx, 15500 / m + dy)
    return out

def route(S, name, pts, r, color, z=600, factor=1, label=None, cost_m=0.0):
    """pipa di atas sleeper beton (z) mengikuti polilinia (m). panjang dicatat untuk CAPEX"""
    P3 = [(x * m, y * m, z) for x, y in pts]
    S.P.extend(pipe_run(P3, r, "rute-" + name, color))
    L = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:])) * factor
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        n = int(math.dist(a, b) // 6)
        for j in range(1, n + 1):
            t = j / (n + 1); px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            S.P.append(("sleeper-%s-%d-%d" % (name, i, j), box(600, 600, z - r, px * m - 300, py * m - 300, 0), CONCR))
    S.routes[name] = dict(pts=pts, L_m=L, label=label or name, cost_m=cost_m, cost=L * cost_m)

def interconnect(S):
    p = S.pts
    # 1 POME panas DN150 (CS sch40, insulasi) fat pit -> PM-1
    route(S, "POME", [p["fatpit_out"], (236, 146), (236, p["PM1_in"][1]), p["PM1_in"]], 84, "#7a5a3a", label="POME 85 °C DN150 (fat pit -> PM-1)", cost_m=140.0)
    # 2 efluen DN150 HDPE TK-301 -> kolam fakultatif (dipertahankan sbg kolam polishing)
    fa = S.area["FA"]
    route(S, "EFLUEN", [p["TK301"], (240, p["TK301"][1]), (240, fa["y"] + fa["W"] / 2), (fa["x"], fa["y"] + fa["W"] / 2)], 84, "#5f8a6a", z=400,
          label="Efluen AnMBR DN150 HDPE (TK-301 -> kolam fakultatif)", cost_m=70.0)
    # 3 bypass darurat DN150 TK-101 -> kolam pendingin CP1 (saat set berhenti)
    cp = S.area["CP1"]
    route(S, "BYPASS", [p["TK101"], (238, p["TK101"][1]), (238, cp["y"] + cp["W"] / 2), (cp["x"], cp["y"] + cp["W"] / 2)], 84, "#9c6b4e", z=900,
          label="Bypass darurat DN150 (TK-101 -> kolam pendingin)", cost_m=70.0)
    # 5 saluran 20 kV: gardu step-up di sisi CHP -> tiang ke jaringan PLN di jalan umum (selatan)
    chp = p["CHP"]
    gx, gy = chp[0] + 2, chp[1] - 6
    S.P.append(("gardu-trafo", box(4 * m, 3 * m, 2.6 * m, (gx - 2) * m, (gy - 1.5) * m, 0), PLN))
    S.P.append(("gardu-pagar", box(9 * m, 7 * m, 2 * m, (gx - 4.5) * m, (gy - 3.5) * m, 0).cut(box(8.8 * m, 6.8 * m, 3 * m, (gx - 4.4) * m, (gy - 3.4) * m, 0)), "#7d8c7d"))
    S.fp("rect", "GI", (gx - 4.5, gy - 3.5, 9, 7), "Gardu step-up 0,4/20 kV 1,25 MVA", grp="PRODUK")
    poles = [(gx, gy), (gx, -6), (gx - 40, -6), (gx - 80, -6)]
    for k, (x, y) in enumerate(poles):
        S.P.append(("tiang-20kV-%d" % k, cyl(180, 11 * m, x * m, y * m, 0), "#8a8a8a"))
        S.P.append(("tiang-20kV-palang-%d" % k, box(2.4 * m, 150, 150, (x - 1.2) * m, y * m, 10.6 * m), "#555555"))
    for a, b in zip(poles[:-1], poles[1:]):
        for dxk in (-1.0, 0.0, 1.0):
            S.P.append(("kabel-20kV-%s-%s-%s" % (a, b, dxk), cyl_dir(20, math.dist(a, b) * m, ((a[0] + (dxk if a[0] == b[0] else 0)) * m, (a[1] + (0 if a[0] == b[0] else dxk * .1)) * m, 10.75 * m),
                                                                        ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b), 0)), "#222222"))
    L = sum(math.dist(a, b) for a, b in zip(poles[:-1], poles[1:]))
    S.routes["20kV"] = dict(pts=poles, L_m=L, label="Saluran udara 20 kV di lokasi (gardu -> jaringan PLN)", cost_m=45.0, cost=L * 45.0)
    # kabel 20 kV ke rumah mesin PKS (pasokan listrik ke PKS & perumahan di luar jam olah)
    mp = [(gx, gy), (gx, 12), (231, 12), (231, 131), (183, 131)]
    S.pts["mill_power"] = mp
    for i, (a, b) in enumerate(zip(mp[:-1], mp[1:])):
        n = max(1, int(math.dist(a, b) // 35))
        for j in range(n + (1 if i == len(mp) - 2 else 0)):
            t = j / n; x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            S.P.append(("tiang-PKS-%d-%d" % (i, j), cyl(160, 10 * m, x * m, y * m, 0), "#8a8a8a"))
        S.P.append(("kabel-PKS-%d" % i, cyl_dir(25, math.dist(a, b) * m, (a[0] * m, a[1] * m, 9.8 * m), ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b), 0)), "#222222"))
    L2 = sum(math.dist(a, b) for a, b in zip(mp[:-1], mp[1:]))
    S.routes["20kV-PKS"] = dict(pts=mp, L_m=L2, label="Saluran 20 kV ke rumah mesin PKS (+ trafo 20/0,4 kV di PKS)", cost_m=40.0, cost=L2 * 40.0 + 18000)
    # jaringan PLN 20 kV sepanjang jalan umum
    for k in range(9):
        x = -40 + 60 * k
        S.P.append(("PLN-tiang-%d" % k, cyl(180, 11 * m, x * m, -12 * m, 0), "#8a8a8a"))
    for dxk in (-0.8, 0, 0.8):
        S.P.append(("PLN-kabel-%s" % dxk, cyl_dir(20, 480 * m, (-40 * m, (-12 + dxk * .1) * m, 10.75 * m), (1, 0, 0)), "#222222"))
    # jalan akses produk dari jalan site
    S.add([("jalan-produk", box(16 * m, 7 * m, 60, 232 * m, 20 * m, 40), ROAD)])

# ============================================================================================ garis alir skematis (overlay)
FLOW = {"POME": "#8b4f1f", "BIOGAS": "#f2b705", "LISTRIK": "#1f6fd1", "EFLUEN": "#1f9e8f", "LUMPUR": "#5a5a5a"}
def _ribbon(name, pts, col, r=900, arrow_every=28.0):
    out = []
    P3 = [(x * m, y * m, z * m) for x, y, z in pts]
    for i, (a, b) in enumerate(zip(P3[:-1], P3[1:])):
        L = math.dist(a, b)
        if L < 1: continue
        d = tuple((b[k] - a[k]) / L for k in range(3))
        out.append(("ALIR/%s-%d" % (name, i), cyl_dir(r, L, a, d), col))
        if i: out.append(("ALIR/%s-siku-%d" % (name, i), cq.Solid.makeSphere(r).translate(cq.Vector(*a)), col))
        n = max(1, int(L / (arrow_every * m)))
        for j in range(n):
            t = (j + .6) / n if n > 1 else .55
            c = [a[k] + (b[k] - a[k]) * t for k in range(3)]
            out.append(("ALIR/%s-panah-%d-%d" % (name, i, j), cq.Solid.makeCone(r * 2.6, 0, 6.0 * m, cq.Vector(*c), cq.Vector(*d)), col))
    return out

def flows(info):
    """garis alir skematis (bukan pipa nyata): POME -> biogas -> listrik ke PKS & PLN; efluen -> kolam; lumpur -> kebun"""
    p = info["pts"]; A = info["ponds"]; bb = p["prod_bb"]
    dx, dy = PRODUCT_ORIGIN
    L = lambda x, y: (x / m + dx, y / m + dy)             # lokal produk (mm) -> site (m)
    R1 = L(9500 + 6400, 15500); R7 = L(9500 + 6400 * 7, 15500); RN = L(9500 + 6400 * 7, 15500 + 6400)
    TK1 = L(9500, 15500); TK3 = L(9500, 21900); PM1 = L(14000, 7200); PM4 = L(9500 + 12800 + 6000, 15500 + 6400 + 5200 + 1200)
    GH = p["GH"]; BTF = L(9500 + 51200 + 3500, 15500 + 6400 + 5200 + 1200); PM6 = L(9500 + 25600 + 1000 + 6000, 15500 + 6400 + 5200 + 1200)
    CHP = L(49300 + 6000, 15500 - 8500); PM10 = L(9500 + 25600 + 1000 + 3000, 15500 - 8300)
    ER = (183, 131); gx, gy = p["mill_power"][0]
    fa = A["FA"]; ae1 = A["AE1"]; ae2 = A["AE2"]
    F = []
    F += _ribbon("POME", [(203, 146, 4), (236, 146, 4), (236, PM1[1], 4), (PM1[0], PM1[1], 4), (PM1[0], TK1[1], 4), (TK1[0], TK1[1], 4)], FLOW["POME"])
    F += _ribbon("POME-reaktor", [(TK1[0], TK1[1] - 3.2, 4), (R7[0], R1[1] - 3.2, 4)], FLOW["POME"], r=700)
    F += _ribbon("POME-membran", [(R1[0] + 6.4, (R1[1] + RN[1]) / 2 + 3.2, 6), (PM4[0], (R1[1] + RN[1]) / 2 + 3.2, 6), (PM4[0], PM4[1], 6)], FLOW["POME"], r=600)
    F += _ribbon("BIOGAS", [(R1[0], (R1[1] + RN[1]) / 2, 22), (R7[0], (R1[1] + RN[1]) / 2, 22), (GH[0], GH[1], 22), (GH[0], GH[1], 13)], FLOW["BIOGAS"])
    F += _ribbon("BIOGAS-bersih", [(GH[0] - 6, GH[1] + 4, 10), (BTF[0], BTF[1], 12), (PM6[0], PM6[1], 7), (PM6[0] + 14, PM6[1] - 4, 7), (CHP[0], CHP[1] + 6, 7), (CHP[0], CHP[1], 7)], FLOW["BIOGAS"])
    F += _ribbon("LISTRIK", [(CHP[0], CHP[1], 9), (gx, gy, 9)], FLOW["LISTRIK"])
    F += _ribbon("LISTRIK-PKS", [(gx, gy, 12), (gx, 12, 12), (231, 12, 12), (231, ER[1], 12), (ER[0], ER[1], 12)], FLOW["LISTRIK"])
    F += _ribbon("LISTRIK-PLN", [(gx, gy, 12), (gx, -12, 12)], FLOW["LISTRIK"])
    F += _ribbon("EFLUEN", [(TK3[0], TK3[1], 3), (240, TK3[1], 3), (240, fa["y"] + fa["W"] / 2, 3), (fa["x"] + fa["L"], fa["y"] + fa["W"] / 2, 3),
                            (ae1["x"] + ae1["L"], ae1["y"] + ae1["W"] / 2, 3), (ae2["x"] + 30, ae2["y"] + ae2["W"] / 2, 3), (ae2["x"] + 30, 220, 3), (300, 220, 3)], FLOW["EFLUEN"])
    F += _ribbon("LUMPUR", [(PM10[0], PM10[1], 3), (PM10[0], 6, 3), (455, 6, 3), (455, -3, 3), (478, -3, 3)], FLOW["LUMPUR"], r=600)
    RC = ((R1[0] + R7[0]) / 2, (R1[1] + RN[1]) / 2)
    marks = [(1, (203, 146, 2)), (2, (PM1[0], PM1[1], 4)), (3, (RC[0], RC[1] - 3.2, 19.5)), (4, (PM4[0], PM4[1], 4)), (5, (GH[0], GH[1], 12)),
             (6, (PM6[0], PM6[1], 4)), (7, (CHP[0], CHP[1], 5)), (8, (gx, gy, 4)), (9, (231, 70, 13)), (10, (gx, -12, 13)),
             (11, (fa["x"] + fa["L"] / 2, fa["y"] + fa["W"] / 2, 2)), (12, (330, 220, 2)), (13, (PM10[0], 6, 4)),
             (14, (A["AN1"]["x"] + A["AN1"]["L"] / 2, A["AN1"]["y"] + A["AN1"]["W"] / 2, 2))]
    return F, [(n, (x * m, y * m, z * m)) for n, (x, y, z) in marks]

def safety(S):
    p = S.pts
    def d(a, b, ra=0, rb=0): return math.dist(a, b) - ra - rb
    bh = (170, 106)
    chk = [("Flare FL-301 -> tepi GH-301", d(p["FL"], p["GH"], 0, 7.4), 15, "API 537 / praktik biogas"),
           ("Flare FL-301 -> kontainer CHP", d(p["FL"], (p["CHP"][0] + 6.2, p["CHP"][1])), 15, "Sumber nyala vs zona gas"),
           ("GH-301 -> rumah boiler PKS", d(p["GH"], bh, 7.4, 14), 30, "Sumber nyala terbuka"),
           ("GH-301 -> tangki CPO", d(p["GH"], (140, 169), 7.4, 8), 30, "Bahan mudah terbakar"),
           ("Flare -> batas pagar lokasi", min(p["FL"][1] - (-5), 440 - p["FL"][0]), 10, "Radiasi panas di batas"),
           ("Reaktor -> kolam pendingin (tanah)", S.area["CP1"]["y"] - 3 - S.pts["prod_bb"][3], 20, "Stabilitas lereng / pondasi"),
           ("Cerobong boiler -> GH-301", d((190, 106), p["GH"], 1.25, 7.4), 30, "Bunga api cerobong")]
    return [dict(item=a, dist=round(b, 1), min=c, basis=e, ok=b >= c) for a, b, c, e in chk]

def site():
    S = Site()
    S.add([("tanah-kebun", box(560 * m, 420 * m, 100, -70 * m, -40 * m, -100), GROUND)])
    S.add([("jalan-umum", box(560 * m, 9 * m, 80, -70 * m, -22 * m, 0), "#4f4f4f")])
    mill(S)
    ponds(S)
    product(S)
    # pagar area pengolahan limbah + produk (menyatu dengan pagar PKS)
    fence(S, [(227, -5), (470, -5), (470, 205), (227, 205)])
    S.add([("halaman-site", box(243 * m, 210 * m, 30, 227 * m, -5 * m, 0), "#d3c9ae")])
    interconnect(S)
    n = palms(S, (-60, -10, 500, 375), [(-12, -14, 234, 207), (226, -14, 476, 211), (244, 210, 432, 232), (-80, -30, 600, -8)])
    info = dict(foot=S.foot, routes=S.routes, ponds=S.area, safety=safety(S), palms=n, pts=S.pts,
                pome_m3d=POME, site_bb=(-70, -40, 490, 380))
    return S.P, info

def write_info(info, path=os.path.join(HERE, "out", "site.json")):
    js = dict(routes={k: dict(L_m=v["L_m"], label=v["label"], cost_m=v["cost_m"], cost=v["cost"]) for k, v in info["routes"].items()},
              ponds={k: v for k, v in info["ponds"].items()}, safety=info["safety"], palms=info["palms"],
              land_freed_m2=sum(v["area_m2"] for k, v in info["ponds"].items() if not k.startswith("_") and v["status"] == "dibebaskan"),
              pond_area_before_m2=info["ponds"]["_total_before_m2"], pond_area_after_m2=info["ponds"]["_total_after_m2"],
              interconnect_cost=sum(v["cost"] for v in info["routes"].values()))
    json.dump(js, open(path, "w"), indent=1, default=float)
    return js

if __name__ == "__main__":
    import time; t = time.time()
    P, info = site()
    js = write_info(info)
    print(len(P), "bagian, %.0f s" % (time.time() - t), "sawit", info["palms"])
    for k, v in js["routes"].items(): print("%-12s %6.0f m  USD %8.0f  %s" % (k, v["L_m"], v["cost"], v["label"]))
    print("kolam sebelum %.0f m2, sesudah %.0f m2, dibebaskan %.0f m2" % (js["pond_area_before_m2"], js["pond_area_after_m2"], js["land_freed_m2"]))
    for c in js["safety"]: print(c)
