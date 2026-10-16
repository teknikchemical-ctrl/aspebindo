# -*- coding: utf-8 -*-
"""
Diorama 3D lokasi: PKS proksi 45 t TBS/jam + set generator biogas portabel di atas platform, gaya maket (atap biru,
tangki putih, rumput hijau, jalan gelap bermarka), panah alir kecil, label pil pendek, kamera perspektif pas layar.
python3 diorama.py [norender]  ->  cad/out/render/DIORAMA_*.png  (+ _raw.png tanpa label)
Geometri fisik dari site3d.py (ukuran nyata); hanya warna dan dekorasi yang bergaya maket.
"""
import os, sys, json, math, subprocess, time
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
import site3d as SI
from bgmodels import box, cyl, cone, cyl_dir, mv

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "out", "render"); STL = os.path.join(HERE, "out", "stl", "DIORAMA")
os.makedirs(STL, exist_ok=True)
m = 1000.0
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ---------------------------------------------------------------- palet maket
GRASS = "#7cc46a"; RIM = "#8a5a3c"; ASPH = "#41464d"; PAVE = "#d9dad6"; MARK = "#f4f4f0"
PALETTE = {SI.WALL: "#eef1f4", SI.ROOF: "#2f6fd6", "#7f97a8": "#2f6fd6", "#b85c3a": "#2f6fd6", "#c9bfa8": "#c0573f", "#5d7486": "#9cc3e6",
           "#d9d5cc": "#f6f7f8", "#c7c3ba": "#e4e8ec", "#c9c4b5": "#f2f2f2", "#9fb3c0": "#e3edf3", "#77736d": "#e9eaec", "#8f8a83": "#b8bcc2",
           "#d8d0b0": "#f2f2f2", SI.YARD: PAVE, "#d3c9ae": "#8fd07c", SI.ROAD: ASPH, SI.CONCR: "#c9cac4", "#7f7f7f": "#9a9a9a",
           SI.WATER_C: "#9a7a52", SI.WATER_F: "#5fb5a5", SI.WATER_O: "#69c2d9", SI.WATER_R: "#5aa9e6", SI.GRASS: "#b6e09e", SI.BUND: "#c9a77c",
           "#c9cfd6": "#f4f6f8", "#9aa7b4": "#d3dae1", "#7c8b99": "#14a38b", "#3f6d9a": "#14a38b", "#c9c4b8": "#cdeee2", "#e7ecef": "#fbfbfb",
           "#cfd6dc": "#eaeef1", "#5d7a5d": "#a9b0b6", "#8a8a8a": "#b9bec4", "#555555": "#7a7f85", "#55595e": "#6b7076", "#7d7366": "#8a7f72",
           "#7d8c7d": "#a9b0b6", "#c8a23a": "#f2a516", "#7a5a3a": "#8b4513", "#5f8a6a": "#1aa3b8", "#9c6b4e": "#a0522d", "#4f4f4f": ASPH}
FLOW = {"POME": "#8b4513", "BIOGAS": "#ff8f00", "LISTRIK": "#fdd000", "EFLUEN": "#00a7c4", "LUMPUR": "#5e5e5e"}
FLOW_LAB = {"POME": "Air limbah POME", "BIOGAS": "Biogas", "LISTRIK": "Listrik", "EFLUEN": "Efluen terolah", "LUMPUR": "Kue lumpur"}

def tree(x, y, s=1.0, k=0):
    col = ("#3f9a45", "#4caf50", "#5bbd5a")[k % 3]
    return [("pohon-batang-%d-%d" % (x, y), cyl(220 * s, 3.0 * m * s, x * m, y * m, 0), "#7a5532"),
            ("pohon-tajuk-%d-%d" % (x, y), cq.Solid.makeSphere(2.4 * m * s).translate(cq.Vector(x * m, y * m, 4.6 * m * s)), col)]
def car(x, y, col, ang=0):
    b = [box(4.2 * m, 1.8 * m, 1.0 * m, x * m, y * m, 300), box(2.2 * m, 1.6 * m, .7 * m, (x + 1.0) * m, (y + .1) * m, 1300)]
    return [("mobil-%d-%d-%d" % (x, y, i), s.rotate(cq.Vector(x * m, y * m, 0), cq.Vector(x * m, y * m, 1), ang), col) for i, s in enumerate(b)]
def tanker(x, y):
    return [("tangki-truk-kabin-%d" % x, box(2.4 * m, 2.5 * m, 2.8 * m, x * m, y * m, 300), "#e53935"),
            ("tangki-truk-tabung-%d" % x, cyl(1.2 * m, 8 * m, (x + 2.6) * m, (y + 1.25) * m, 1.9 * m, "x"), "#eceff1"),
            ("tangki-truk-rangka-%d" % x, box(8.4 * m, 2.2 * m, .5 * m, (x + 2.5) * m, (y + .15) * m, .5 * m), "#37474f")]

def ribbon(name, pts, col, r=260, every=14.0, arrow_r=1050, arrow_L=3000):
    out = []
    P3 = [(x * m, y * m, z * m) for x, y, z in pts]
    for i, (a, b) in enumerate(zip(P3[:-1], P3[1:])):
        L = math.dist(a, b)
        if L < 1: continue
        d = tuple((b[k] - a[k]) / L for k in range(3))
        out.append(("ALIR/%s-%d" % (name, i), cyl_dir(r, L, a, d), col))
        if i: out.append(("ALIR/%s-s-%d" % (name, i), cq.Solid.makeSphere(r).translate(cq.Vector(*a)), col))
        n = max(1, int(L / (every * m)))
        for j in range(n):
            t = (j + .55) / n
            c = [a[k] + (b[k] - a[k]) * t - d[k] * arrow_L / 2 for k in range(3)]
            out.append(("ALIR/%s-p-%d-%d" % (name, i, j), cq.Solid.makeCone(arrow_r, 0, arrow_L, cq.Vector(*c), cq.Vector(*d)), col))
    return out

def flows(info):
    p = info["pts"]; A = info["ponds"]
    MD = {nm: (x, y, l, w) for nm, x, y, l, w in p["mods"]}
    cen = lambda nm: (MD[nm][0] + MD[nm][2] / 2, MD[nm][1] + MD[nm][3] / 2)
    PM1 = cen("PM-1"); PM10 = cen("PM-10"); PM6 = p["PM6"]; BTF = p["BTF"]; GH = p["GH"]; CHP = p["CHP"]
    TK1 = p["TK101"]; TK3 = p["TK301"]; RX = p["reactors"]; dx, dy = SI.PRODUCT_ORIGIN
    yrack = 9.5 + dy; yhead = 27.2 + dy
    gx, gy = p["mill_power"][0]; ER = p["mill_power"][-1]
    fa, ae1, ae2 = A["FA"], A["AE1"], A["AE2"]
    F = []
    F += ribbon("POME", [(208, 146, 2.5), (230, 146, 2.5), (230, PM1[1], 2.5), (PM1[0], PM1[1], 2.5), (PM1[0], TK1[1], 3.0), (TK1[0] + 3.5, TK1[1], 3.0)], FLOW["POME"])
    F += ribbon("POME2", [(TK1[0] + 3.5, TK1[1] - 2, 6.0), (TK1[0] + 3.5, yrack, 6.0), (RX[-1][0], yrack, 6.0)], FLOW["POME"])
    F += ribbon("BIOGAS", [(RX[0][0], yhead, 7.5), (GH[0] - 9.5, yhead, 7.5), (GH[0] - 9.5, GH[1], 7.5), (GH[0] - 6.5, GH[1], 7.5)], FLOW["BIOGAS"])
    F += ribbon("BIOGAS2", [(GH[0], GH[1] + 7.5, 5), (GH[0], BTF[1], 5), (BTF[0] + 2.5, BTF[1], 5), (PM6[0] + 12.6, BTF[1], 4.5), (PM6[0] + 12.6, PM6[1] + .6, 4.5),
                            (58.3 + dx, PM6[1] + .6, 4.5), (58.3 + dx, CHP[1] + 3.4, 4.5), (CHP[0] - 5, CHP[1] + 3.4, 4.5)], FLOW["BIOGAS"])
    F += ribbon("LISTRIK-PKS", [(CHP[0] - 4, CHP[1] - 1, 4), (gx, gy, 4), (gx, 2, 4), (228, 2, 4), (228, ER[1], 4), (ER[0], ER[1], 4)], FLOW["LISTRIK"])
    F += ribbon("LISTRIK-PLN", [(gx + 2, gy, 4), (gx + 2, -24, 4)], FLOW["LISTRIK"])
    F += ribbon("EFLUEN", [(TK3[0], TK3[1], 2.5), (232, TK3[1], 2.5), (232, fa["y"] + fa["W"] / 2, 2.5), (fa["x"] + fa["L"] / 2, fa["y"] + fa["W"] / 2, 2.5),
                           (ae1["x"] + ae1["L"] / 2, ae1["y"] + ae1["W"] / 2, 2.5), (ae2["x"] + ae2["L"] / 2, ae2["y"] + ae2["W"] / 2, 2.5), (ae2["x"] + ae2["L"] / 2, 186, 2.5), (300, 186, 2.5)], FLOW["EFLUEN"])
    F += ribbon("LUMPUR", [(PM10[0], PM10[1], 2.5), (PM10[0], -1, 2.5), (470, -1, 2.5), (486, -1, 2.5)], FLOW["LUMPUR"])
    return F

def decorate(P, info):
    """buang dekorasi kebun lama, tambah platform, jalan bermarka, pohon tertata, kendaraan"""
    out = [(n, s, PALETTE.get(c, c)) for n, s, c in P if not n.startswith(("sawit-", "tanah-kebun", "jalan-umum", "PLN-"))]
    X0, Y0, X1, Y1 = -26, -46, 500, 222
    out += [("platform-rumput", box((X1 - X0) * m, (Y1 - Y0) * m, 200, X0 * m, Y0 * m, -200), GRASS),
            ("platform-badan", box((X1 - X0) * m + 400, (Y1 - Y0) * m + 400, 7.5 * m, X0 * m - 200, Y0 * m - 200, -7.7 * m), RIM)]
    out += [("jalan-umum", box((X1 - X0) * m, 11 * m, 80, X0 * m, -30 * m, 0), ASPH)]
    for k in range(int((X1 - X0) // 10)):
        out.append(("marka-%d" % k, box(5 * m, 250, 60, (X0 + 2 + k * 10) * m, -24.6 * m, 80), MARK))
    for xx in (36, 232):                                         # gerbang/jalan masuk
        out.append(("jalan-masuk-%d" % xx, box(8 * m, 14 * m, 70, xx * m, -19 * m, 0), ASPH))
    # tiang PLN tertata di sisi jalan
    for k in range(10):
        x = X0 + 8 + 52 * k
        out.append(("PLN-tiang-%d" % k, cyl(170, 10 * m, x * m, -36 * m, 0), "#b9bec4"))
    out.append(("PLN-kabel", cyl_dir(40, (X1 - X0 - 16) * m, ((X0 + 8) * m, -36 * m, 9.8 * m), (1, 0, 0)), "#5a5f66"))
    # pohon: deret tepi platform + penyangga hijau antar zona
    k = 0
    for x in range(X0 + 6, X1 - 4, 11):
        out += tree(x, Y1 - 6, 1.0, k); k += 1
        out += tree(x, -40, .9, k); k += 1
    for y in range(Y0 + 16, Y1 - 10, 11):
        out += tree(X0 + 5, y, 1.0, k); out += tree(X1 - 5, y, 1.0, k + 1); k += 2
    for x in range(-2, 225, 13): out += tree(x, 207, .8, k); k += 1
    for y in range(10, 195, 13): out += tree(-12, y, .8, k); k += 1
    # kelompok pohon di halaman hijau timur/selatan kolam
    for (cx, cy) in ((360, 10), (395, 30), (430, 12), (455, 38), (348, 40), (465, 105), (300, 205)):
        for j in range(5):
            out += tree(cx + 4.5 * math.cos(j * 1.3) * (j % 3), cy + 4.5 * math.sin(j * 1.3) * (j % 3), .9, j)
    # parkir + mobil di kantor, truk TBS sudah ada; tangki CPO keluar
    out.append(("parkir", box(24 * m, 12 * m, 60, 3 * m, -2 * m, 0), "#9aa0a6"))
    for i, col in enumerate(("#e53935", "#fafafa", "#1e88e5", "#43a047", "#fdd835")):
        out += car(4 + i * 4.6, 2, col, 90)
    out += tanker(166, 166); out += tanker(150, 186)
    return out

def labels(info):
    p = info["pts"]; A = info["ponds"]; dx, dy = SI.PRODUCT_ORIGIN
    L = lambda x, y, z: ((x / m + dx) * m, (y / m + dy) * m, z)
    bb = p["prod_bb"]
    over = [("SET BIOGAS", ((bb[0] + bb[2]) / 2 * m - 10 * m, (bb[1] + bb[3]) / 2 * m, 20 * m)), ("Fat pit (POME)", (203, 146, 1.5)),
            ("Pabrik utama", (95, 110, 22)), ("Boiler", (170, 106, 22)), ("Rumah mesin", (169, 130, 11)), ("Tangki CPO", (126, 169, 13)),
            ("Loading ramp TBS", (90, 65, 11)), ("Rebusan", (85, 87, 4)), ("Pengolahan air", (82, 170, 23)), ("Kantor", (16, 19, 9)), ("Jembatan timbang", (55, 16, 1)),
            ("Kolam pendingin", (A["CP2"]["x"] + 13, A["CP2"]["y"] + 5, 1)), ("Kolam lama dibebaskan", (A["AN1"]["x"] + 33, A["AN1"]["y"] + 27, 1)),
            ("Kolam polishing", (A["AE1"]["x"] + 35, A["AE1"]["y"] + 17, 1)), ("Aplikasi lahan", (330, 186, 1))]
    over = [(t, (x * m, y * m, z * m)) if t != "SET BIOGAS" else (t, (x, y, z)) for t, (x, y, z) in over]
    MD = {nm: (x, y, l, w) for nm, x, y, l, w in p["mods"]}
    c3 = lambda nm, z: ((MD[nm][0] + MD[nm][2] / 2) * m, (MD[nm][1] + MD[nm][3] / 2) * m, z * m)
    q3 = lambda q, z: (q[0] * m, q[1] * m, z * m)
    RX = p["reactors"]
    prod = [("Praolah PM-1", c3("PM-1", 3.0)), ("Tangki umpan", q3(p["TK101"], 6.0)), ("3 reaktor kontak (GFS)", q3(RX[1], 14.0)),
            ("Degasser + settler lamella", c3("PM-4B", 5.2)), ("Penampung gas", q3(p["GH"], 11)), ("Pembersih biogas", q3(p["BTF"], 9.5)),
            ("Genset 2 x 600 kWe", c3("PM-8B", 3.5)), ("Flare", q3(p["FL"], 7)), ("Gardu 20 kV", (p["mill_power"][0][0] * m, p["mill_power"][0][1] * m, 3 * m)),
            ("Skid lumpur", c3("PM-10", 2.5)), ("Menara pendingin", c3("PM-9", 4.5)), ("Tangki efluen", q3(p["TK301"], 6.0))]
    return over, prod

def seg_hits(a, b, q, n=20):
    for i in range(n + 1):
        t = i / n; x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
        if q[0] - 4 < x < q[2] + 4 and q[1] - 4 < y < q[3] + 4: return True
    return False

def pill(d, x, y, text, f, placed, W, H, stem=(60, 100, 140, 40, 180)):
    tw = d.textlength(text, font=f); th = f.size + 14; pw = tw + 30
    for s in stem:
        for dxp in (0, -pw * .35, pw * .35, -pw * .7, pw * .7):
            bx0, by1 = x - pw / 2 + dxp, y - s
            bb = (bx0, by1 - th, bx0 + pw, by1)
            if bb[0] < 6 or bb[2] > W - 6 or bb[1] < 6: continue
            if any(not (bb[2] + 8 < q[0] or bb[0] - 8 > q[2] or bb[3] + 6 < q[1] or bb[1] - 6 > q[3]) for q in placed): continue
            sx = min(max(x, bb[0] + 14), bb[2] - 14)
            if any(seg_hits((x, y), (sx, bb[3]), q) for q in placed): continue
            placed.append(bb)
            d.line([(x, y), (min(max(x, bb[0] + 14), bb[2] - 14), bb[3])], fill=(255, 255, 255), width=5)
            d.line([(x, y), (min(max(x, bb[0] + 14), bb[2] - 14), bb[3])], fill=(30, 38, 46), width=2)
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(255, 255, 255), outline=(30, 38, 46), width=2)
            d.rounded_rectangle(bb, radius=th / 2, fill=(28, 36, 44), outline=(255, 255, 255), width=2)
            d.text(((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2), text, font=f, fill=(255, 255, 255), anchor="mm")
            return True
    return False

def legend(d, W, H, title, sub):
    ft = ImageFont.truetype(FB, 40); fs = ImageFont.truetype(FR, 27); fl = ImageFont.truetype(FB, 26)
    d.rounded_rectangle([30, 26, 30 + max(d.textlength(title, font=ft), d.textlength(sub, font=fs)) + 50, 140], 22, fill=(255, 255, 255), outline=(200, 205, 210), width=2)
    d.text((55, 42), title, font=ft, fill=(25, 40, 50)); d.text((55, 96), sub, font=fs, fill=(80, 90, 100))
    x0, y0 = 30, H - 92; w = 40 + sum(d.textlength(FLOW_LAB[k], font=fl) + 110 for k in FLOW)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + 64], 20, fill=(255, 255, 255), outline=(200, 205, 210), width=2)
    x = x0 + 26
    for k in FLOW:
        y = y0 + 32
        d.line([(x, y), (x + 46, y)], fill=FLOW[k], width=9); d.polygon([(x + 46, y - 12), (x + 66, y), (x + 46, y + 12)], fill=FLOW[k])
        d.text((x + 76, y), FLOW_LAB[k], font=fl, fill=(30, 30, 30), anchor="lm"); x += d.textlength(FLOW_LAB[k], font=fl) + 110

def main(render=True):
    t0 = time.time()
    P, info = SI.site(); js = SI.write_info(info)
    P = decorate(P, info); F = flows(info)
    over, prod = labels(info); LB = over + prod
    bb = info["pts"]["prod_bb"]
    V = {"DIORAMA_lokasi": dict(dir=(.62, -1.0, .78), persp=28, fit=[-26 * m, -46 * m, -7.7 * m, 500 * m, 222 * m, 8 * m], pad=.015),
         "DIORAMA_lokasi-barat": dict(dir=(-.7, -1.0, .8), persp=28, fit=[-26 * m, -46 * m, -7.7 * m, 500 * m, 222 * m, 8 * m], pad=.015),
         "DIORAMA_produk": dict(dir=(.5, -1.0, .8), persp=26, fit=[(bb[0] - 2) * m, (bb[1] - 2) * m, 0, (bb[2] + 2) * m, (bb[3] + 2) * m, 20 * m], pad=.03),
         "DIORAMA_atas": dict(dir=(0.0001, -0.12, 1), persp=20, fit=[-26 * m, -46 * m, -7.7 * m, 500 * m, 222 * m, 0], pad=.01)}
    W, H = 3200, 1800
    if render:
        for f_ in os.listdir(STL): os.remove(os.path.join(STL, f_))
        groups = {}
        for n, s, c in P + F: groups.setdefault(c, []).append(s)
        job = {"w": W, "h": H, "parts": [], "views": [], "labels": [list(p) for t, p in LB], "shadows": True, "shadowMap": 4096, "bg": "#eef2f5", "light": [1.15, 1.9, .45]}
        for k, (c, ss) in enumerate(groups.items()):
            fn = os.path.join(STL, "g%03d.stl" % k)
            fine = c in FLOW.values() or c in ("#f4f6f8", "#fbfbfb", "#14a38b")
            cq.exporters.export(cq.Compound.makeCompound(ss), fn, tolerance=3.0 if fine else 12.0, angularTolerance=0.3)
            job["parts"].append({"stl": fn, "color": c, "edges": False, "rough": .8, "metal": 0.0, "cast": c not in (GRASS, PAVE, ASPH, "#dedfdb")})
        for vn, vv in V.items():
            job["views"].append({"dir": vv["dir"], "up": (0, 0, 1), "persp": vv["persp"], "fit": vv["fit"], "pad": vv["pad"], "sun": (.55, -.75, 1.25), "out": os.path.join(IMG, vn + "_raw.png")})
        jf = os.path.join(STL, "job.json"); json.dump(job, open(jf, "w"))
        r = subprocess.run(["node", "render.mjs", jf], cwd=os.path.join(HERE, "render"), capture_output=True, text=True, timeout=3000)
        print(r.stdout.strip(), r.stderr.strip()[:400], "%.0f s" % (time.time() - t0))
    T = {"DIORAMA_lokasi": ("PKS 45 t TBS/jam + Set Biogas yang Dapat Dipindah", "POME -> biogas -> listrik pengganti solar PKS + PLN; efluen ke kolam polishing"),
         "DIORAMA_lokasi-barat": ("PKS 45 t TBS/jam + Set Biogas yang Dapat Dipindah", "Tampak dari barat daya"),
         "DIORAMA_produk": ("Set Biogas Kontak Termofilik", "3 reaktor GFS, degasser + settler, gas holder, pembersih gas, genset 2 x 600 kWe, flare"),
         "DIORAMA_atas": ("Denah lokasi", "Tampak atas")}
    for vn in V:
        raw = os.path.join(IMG, vn + "_raw.png"); lp = json.load(open(raw.replace(".png", ".labels.json")))
        im = Image.open(raw).convert("RGB"); d = ImageDraw.Draw(im); f = ImageFont.truetype(FB, 30 if vn != "DIORAMA_produk" else 32)
        placed = [(20, 20, 1300, 150), (20, H - 110, 1500, H)]
        sel = range(len(over)) if vn != "DIORAMA_produk" else range(len(over), len(LB))
        if vn == "DIORAMA_produk": sel = list(sel)
        for i in sel:
            x, y = lp[i]
            if 0 < x < W and 0 < y < H: pill(d, x, y, LB[i][0], f, placed, W, H)
        legend(d, W, H, *T[vn])
        im.save(os.path.join(IMG, vn + ".png"))
    print("selesai %.0f s" % (time.time() - t0))
    return info

if __name__ == "__main__":
    main(render="norender" not in sys.argv)
