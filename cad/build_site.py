# -*- coding: utf-8 -*-
"""Render + ekspor model 3D lokasi lengkap (PKS proksi + kolam + produk). python3 build_site.py [nostep]
Keluaran: cad/out/step/SITE.step (+zip), cad/out/render/SITE_*.png, SITE_*_label.png (berlabel), cad/out/site.json"""
import os, sys, json, subprocess, time, zipfile
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
import site3d as SI

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); STL = os.path.join(OUT, "stl", "SITE"); IMG = os.path.join(OUT, "render"); STEP = os.path.join(OUT, "step")
for p in (STL, IMG, STEP): os.makedirs(p, exist_ok=True)
m = 1000.0
NOEDGE = {SI.GROUND, SI.YARD, SI.ROAD, SI.GRASS, SI.CROWN, SI.TRUNK, SI.WATER_A, SI.WATER_F, SI.WATER_O, SI.WATER_C, SI.WATER_R, "#d3c9ae", "#4f4f4f", "#c9c4b8", SI.BUND, "#5d7a5d", "#222222", "#dcd8cf"}

def labels(info):
    p = info["pts"]; A = info["ponds"]
    L = [("Loading ramp TBS", (90, 65, 10)), ("Rebusan (sterilizer)", (85, 84, 3)), ("Pabrik utama PKS 45 t TBS/jam", (95, 110, 22)),
         ("Rumah boiler + cerobong", (175, 106, 30)), ("Tangki timbun CPO 2 x 2.000 t", (126, 169, 13)), ("Pengolahan air", (82, 170, 23)),
         ("Fat pit (sumber POME)", (203, 146, 1)), ("Kolam pendingin (bypass darurat)", (A["CP2"]["x"] + 13, A["CP2"]["y"] + 5, 1)),
         ("Kolam pengasaman + anaerobik: DIBEBASKAN (%.1f ha)" % (sum(v["area_m2"] for k, v in A.items() if not k.startswith("_") and v["status"] == "dibebaskan") / 1e4), (A["AN1"]["x"] + 40, A["AN1"]["y"] + 27, 1)),
         ("Kolam fakultatif + aerobik (polishing efluen)", (A["AE1"]["x"] + 35, A["AE1"]["y"] + 16, 1)), ("Aplikasi lahan ke kebun", (330, 220, 0.5)),
         ("PRODUK: 14 reaktor AnMBR", ((p["prod_bb"][0] + 35), (p["prod_bb"][1] + 18), 19)), ("Penampung gas GH-301", (p["GH"][0], p["GH"][1], 11)),
         ("Genset CHP 2 x 800 kWe", (p["CHP"][0], p["CHP"][1], 4)), ("Flare FL-301", (p["FL"][0], p["FL"][1], 7)),
         ("Gardu 20 kV -> jaringan PLN", (p["CHP"][0] + 2, p["CHP"][1] - 6, 3)), ("Pipa POME DN150 (%d m)" % info["routes"]["POME"]["L_m"], (236, 100, 1)),
         ("Pipa efluen ke kolam polishing (%d m)" % info["routes"]["EFLUEN"]["L_m"], (240, 120, 1))]
    return [(t, (x * m, y * m, z * m)) for t, (x, y, z) in L]

def annotate(png, labs, texts, out, scale=1.0):
    im = Image.open(png).convert("RGB"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(26 * scale))
    W, H = im.size; placed = []
    for (x, y), t in sorted(zip(labs, texts), key=lambda a: a[0][1]):
        if not (0 <= x < W and 0 <= y < H): continue
        tw = d.textlength(t, font=f); th = int(34 * scale)
        best = None
        for dy in (-110, -160, -70, 90, 140, -210, 190, -260):
            for dx in (0, -tw / 2, -tw + 40, 40, -tw - 40):
                bx, by = x + dx, y + dy * scale
                bb = (bx - 8, by - 6, bx + tw + 8, by + th)
                if bb[0] < 5 or bb[2] > W - 5 or bb[1] < 5 or bb[3] > H - 5: continue
                if any(not (bb[2] < q[0] or bb[0] > q[2] or bb[3] < q[1] or bb[1] > q[3]) for q in placed): continue
                best = bb; break
            if best: break
        if not best: continue
        placed.append(best)
        cx = min(max(x, best[0]), best[2]); cy = best[3] if best[1] > y else best[1]
        d.line([(x, y), (cx, cy)], fill=(20, 20, 20), width=3); d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(200, 40, 30))
        d.rectangle(best, fill=(255, 255, 255), outline=(30, 30, 30), width=2)
        d.text((best[0] + 8, best[1] + 4), t, font=f, fill=(15, 15, 15))
    im.save(out)

def main(step=True):
    t0 = time.time()
    P, info = SI.site(); js = SI.write_info(info)
    print(len(P), "bagian", "%.0f s" % (time.time() - t0))
    if step:
        asm = cq.Assembly(name="SITE")
        groups = {}
        for n, s, c in P: groups.setdefault((n.split("/")[0] if "/" in n else n.split("-")[0], c), []).append(s)
        for (k, c), ss in groups.items():
            asm.add(cq.Workplane().add(cq.Compound.makeCompound(ss)), name=("%s_%s" % (k, c[1:])).replace("/", "_"), color=cq.Color(c))
        fn = os.path.join(STEP, "SITE.step"); asm.save(fn)
        with zipfile.ZipFile(fn.replace(".step", "_step.zip"), "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z: z.write(fn, "SITE.step")
        print("STEP", os.path.getsize(fn) / 1e6, "MB", "%.0f s" % (time.time() - t0))
    for f in os.listdir(STL): os.remove(os.path.join(STL, f))
    groups = {}
    for n, s, c in P: groups.setdefault(c, []).append(s)
    LB = labels(info)
    job = {"w": 2600, "h": 1600, "parts": [], "views": [], "labels": [list(p) for t, p in LB]}
    for k, (c, ss) in enumerate(groups.items()):
        fn = os.path.join(STL, "g%02d.stl" % k)
        cq.exporters.export(cq.Compound.makeCompound(ss), fn, tolerance=20.0 if c in NOEDGE else 4.0, angularTolerance=0.35)
        job["parts"].append({"stl": fn, "color": c, "edges": c not in NOEDGE, "edgeAngle": 35, "rough": .85 if c in NOEDGE else .55})
    bb = info["pts"]["prod_bb"]
    OVER = {"udara-tenggara": dict(dir=(1, -1.15, .95)), "udara-baratdaya": dict(dir=(-1, -1.0, .9)), "tampak-atas": dict(dir=(0.0001, -0.0001, 1), up=(0, 1, 0))}
    CLOSE = {"dekat-produk": dict(dir=(1, -1.3, .75), zoom=[(bb[0] - 10) * m, (bb[1] - 25) * m, 0, (bb[2] + 5) * m, (bb[3] + 8) * m, 20 * m]),
             "produk-PKS": dict(dir=(.55, -1.2, .6), zoom=[50 * m, -10 * m, 0, (bb[2] + 5) * m, 200 * m, 25 * m]),
             "produk-kolam": dict(dir=(-.6, -1.0, .7), zoom=[(bb[0] - 20) * m, (bb[1] - 15) * m, 0, 470 * m, 200 * m, 20 * m])}
    BLD = {SI.WALL, SI.ROOF, "#c9bfa8", "#7f97a8", "#b85c3a"}
    for tag, VV, edge_fn in (("over", OVER, lambda c: c in BLD), ("close", CLOSE, lambda c: c not in NOEDGE)):
        j2 = dict(job); j2["parts"] = [dict(p, edges=edge_fn(p["color"])) for p in job["parts"]]
        j2["views"] = [{"dir": vv["dir"], "up": vv.get("up", (0, 0, 1)), "zoom": vv.get("zoom"), "out": os.path.join(IMG, "SITE_%s.png" % vn), "pad": .02} for vn, vv in VV.items()]
        jf = os.path.join(STL, "job_%s.json" % tag); json.dump(j2, open(jf, "w"))
        r = subprocess.run(["node", "render.mjs", jf], cwd=os.path.join(HERE, "render"), capture_output=True, text=True, timeout=1800)
        print(tag, r.stdout.strip(), r.stderr.strip()[:400], "%.0f s" % (time.time() - t0))
    for vn in list(OVER) + list(CLOSE):
        png = os.path.join(IMG, "SITE_%s.png" % vn); lj = png.replace(".png", ".labels.json")
        if os.path.exists(lj) and vn in ("udara-tenggara", "udara-baratdaya", "tampak-atas", "produk-PKS"):
            annotate(png, json.load(open(lj)), [t for t, p in LB], png.replace(".png", "_label.png"))
    return info, js

if __name__ == "__main__":
    main(step="nostep" not in sys.argv)
