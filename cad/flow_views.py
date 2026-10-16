# -*- coding: utf-8 -*-
"""Gambar alir lokasi: model 3D lokasi + garis alir skematis berwarna + penanda bernomor + panel legenda (tanpa teks di atas adegan).
python3 flow_views.py [norender]  -> cad/out/render/ALIR_*.png"""
import os, sys, json, subprocess, time
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
import site3d as SI
from build_site import NOEDGE

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "out", "render"); STL = os.path.join(HERE, "out", "stl", "ALIR")
os.makedirs(STL, exist_ok=True)
m = 1000.0
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fade(c, k=.35):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * k) for v in (r, g, b))

def steps():
    R = SI.R; E = R["energy"]; N = R["nominal"]; EQ = R["equipment"]
    sj = json.load(open(os.path.join(HERE, "out", "site.json")))
    fs = {}
    fp = os.path.join(HERE, "..", "finance", "outputs", "summary.json")
    ER = R["emissions"]["avoided_t"]
    if os.path.exists(fp):
        sm = json.load(open(fp)); fs = sm.get("energy_split", {}); ER = sm.get("ER_t", ER)
    cake = [s for s in R["streams"] if s["id"] == 12][0]["kg_h"] * R["design_basis"]["hrs_day"] * R["design_basis"]["days_yr"] / 1000
    f = lambda v, d=0: ("{:,.%df}" % d).format(v).replace(",", "X").replace(".", ",").replace("X", ".")
    return [(1, "POME", "Fat pit PKS: POME panas 85 °C, %s m³/hari" % f(R["design_basis"]["pome_m3d"])),
            (2, "POME", "PM-1 praolah: saringan, desander, pendingin 85 -> 56 °C"),
            (3, "POME", "14 reaktor AnMBR termofilik 55 °C, HRT %s hari" % f(R["process_decisions"]["hrt_actual_d"], 1)),
            (4, "POME", "PM-4 membran UF %s m²: biomassa kembali ke reaktor" % f(EQ["membrane"]["area_m2"])),
            (5, "BIOGAS", "GH-301 penampung biogas %s m³ (%s Nm³/hari, CH4 %s%%)" % (f(EQ["gas_holder"]["V_m3"]), f(N["biogas_Nm3d"]), f(N["ch4_frac"] * 100, 1))),
            (6, "BIOGAS", "PM-6 pembersih biogas: H2S %s -> %s ppm" % (f(N["h2s_ppm_raw"]), f(N["h2s_ppm_fuel"]))),
            (7, "LISTRIK", "PM-8 genset 2 x 800 kWe: %s kWe kotor" % f(E["P_gross"])),
            (8, "LISTRIK", "Gardu 0,4/20 kV: %s kWe neto" % f(E["P_net"])),
            (9, "LISTRIK", "Listrik ke rumah mesin PKS" + (" (%s GWh/th)" % f(fs["captive_GWh"], 2) if fs else "")),
            (10, "LISTRIK", "Ekspor ke jaringan PLN 20 kV" + (" (%s GWh/th)" % f(fs["export_GWh"], 2) if fs else "")),
            (11, "EFLUEN", "Efluen %s m³/hari ke kolam polishing" % f(sum(s["kg_h"] for s in R["streams"] if s["id"] == 14) * 24 / 1000)),
            (12, "EFLUEN", "Aplikasi lahan ke kebun sawit (flatbed)"),
            (13, "LUMPUR", "Kue lumpur %s t/th ke kebun (bahan organik)" % f(cake)),
            (14, None, "Kolam anaerobik lama dibebaskan %s ha; emisi neto %s t CO2e/th dihindari" % (f(sj["land_freed_m2"] / 1e4, 1), f(ER)))]

def compose(png, marks_px, out, title, sub):
    sc = Image.open(png).convert("RGB"); W, H = sc.size; PW = 980
    im = Image.new("RGB", (W + PW, H), "white"); im.paste(sc, (0, 0)); d = ImageDraw.Draw(im)
    fn = ImageFont.truetype(FB, 30); placed = []
    for n, (x, y) in marks_px:
        if not (0 <= x < W and 0 <= y < H): continue
        for k in range(12):
            if all((x - a) ** 2 + (y - b) ** 2 > 62 ** 2 for a, b in placed): break
            y -= 22
        placed.append((x, y)); r = 27
        d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(20, 20, 20)); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
        d.text((x, y), str(n), font=fn, fill=(15, 15, 15), anchor="mm")
    x0 = W + 40; y = 50
    d.rectangle([W, 0, W + PW, H], fill=(247, 247, 245)); d.line([(W, 0), (W, H)], fill=(180, 180, 180), width=3)
    d.text((x0, y), title, font=ImageFont.truetype(FB, 40), fill=(20, 40, 38)); y += 58
    d.text((x0, y), sub, font=ImageFont.truetype(FR, 25), fill=(80, 80, 80)); y += 60
    fl = ImageFont.truetype(FB, 26)
    for k, (nm, lab) in enumerate((("POME", "Air limbah POME"), ("BIOGAS", "Biogas"), ("LISTRIK", "Listrik"), ("EFLUEN", "Efluen terolah"), ("LUMPUR", "Kue lumpur"))):
        xx = x0 + (k % 2) * 440; yy = y + (k // 2) * 44
        d.rounded_rectangle([xx, yy, xx + 70, yy + 22], 8, fill=SI.FLOW[nm]); d.text((xx + 85, yy + 11), lab, font=fl, fill=(30, 30, 30), anchor="lm")
    y += 150
    ft = ImageFont.truetype(FR, 25); fnb = ImageFont.truetype(FB, 25)
    for n, kind, txt in steps():
        col = SI.FLOW[kind] if kind else "#8fb46a"
        d.ellipse([x0, y, x0 + 46, y + 46], fill=col); d.text((x0 + 23, y + 23), str(n), font=fnb, fill="white", anchor="mm")
        # bungkus teks
        words = txt.split(" "); line = ""; lines = []
        for w_ in words:
            if d.textlength(line + " " + w_, font=ft) > PW - 130: lines.append(line); line = w_
            else: line = (line + " " + w_).strip()
        lines.append(line)
        for i, l_ in enumerate(lines): d.text((x0 + 62, y + 10 + i * 31), l_, font=ft, fill=(25, 25, 25))
        y += max(58, 31 * len(lines) + 22)
    d.text((x0, H - 60), "Garis alir skematis (diperbesar), bukan diameter pipa nyata.", font=ImageFont.truetype(FR, 22), fill=(110, 110, 110))
    im.save(out)

def main(render=True):
    t0 = time.time()
    P, info = SI.site(); F, marks = SI.flows(info)
    bb = info["pts"]["prod_bb"]
    VIEWS = {"ALIR_lokasi": dict(dir=(1, -1.15, 1.05), zoom=[-5 * m, -15 * m, 0, 480 * m, 232 * m, 30 * m]),
             "ALIR_produk": dict(dir=(.75, -1.25, .95), zoom=[(bb[0] - 8) * m, (bb[1] - 42) * m, 0, (bb[2] + 4) * m, (bb[3] + 6) * m, 24 * m]),
             "ALIR_atas": dict(dir=(0.0001, -0.0001, 1), up=(0, 1, 0), zoom=[-5 * m, -15 * m, 0, 480 * m, 232 * m, 0])}
    if render:
        for f_ in os.listdir(STL): os.remove(os.path.join(STL, f_))
        groups = {}
        for n, s, c in P: groups.setdefault(fade(c), []).append(s)
        job = {"w": 2600, "h": 1700, "parts": [], "views": [], "labels": [list(p) for n, p in marks]}
        BLD = {fade(c) for c in (SI.WALL, SI.ROOF, "#c9bfa8", "#7f97a8")}
        NOE = {fade(c) for c in NOEDGE}
        for k, (c, ss) in enumerate(groups.items()):
            fn = os.path.join(STL, "s%02d.stl" % k)
            cq.exporters.export(cq.Compound.makeCompound(ss), fn, tolerance=20.0 if c in NOE else 4.0, angularTolerance=0.35)
            job["parts"].append({"stl": fn, "color": c, "edges": c in BLD, "rough": .9})
        fg = {}
        for n, s, c in F: fg.setdefault(c, []).append(s)
        for k, (c, ss) in enumerate(fg.items()):
            fn = os.path.join(STL, "f%02d.stl" % k)
            cq.exporters.export(cq.Compound.makeCompound(ss), fn, tolerance=30.0, angularTolerance=0.3)
            job["parts"].append({"stl": fn, "color": c, "edges": False, "rough": .35, "metal": 0.0})
        for vn, vv in VIEWS.items():
            job["views"].append({"dir": vv["dir"], "up": vv.get("up", (0, 0, 1)), "zoom": vv["zoom"], "out": os.path.join(IMG, vn + "_raw.png"), "pad": .02})
        jf = os.path.join(STL, "job.json"); json.dump(job, open(jf, "w"))
        r = subprocess.run(["node", "render.mjs", jf], cwd=os.path.join(HERE, "render"), capture_output=True, text=True, timeout=1800)
        print(r.stdout.strip(), r.stderr.strip()[:300], "%.0f s" % (time.time() - t0))
    T = {"ALIR_lokasi": ("ALIR: POME -> ENERGI PKS", "PKS proksi 45 t TBS/jam + set generator biogas portabel"),
         "ALIR_produk": ("ALIR DI DALAM SET PORTABEL", "Dari POME panas ke listrik untuk PKS dan PLN"),
         "ALIR_atas": ("DENAH ALIR LOKASI", "Tampak atas, skala tidak tercantum")}
    for vn in VIEWS:
        raw = os.path.join(IMG, vn + "_raw.png"); lp = json.load(open(raw.replace(".png", ".labels.json")))
        compose(raw, [(n, tuple(xy)) for (n, _), xy in zip(marks, lp)], os.path.join(IMG, vn + ".png"), *T[vn])
    print("selesai %.0f s" % (time.time() - t0))

if __name__ == "__main__":
    main(render="norender" not in sys.argv)
