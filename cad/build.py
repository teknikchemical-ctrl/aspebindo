# -*- coding: utf-8 -*-
"""
Bangun semua model 3D produk: STEP (berwarna, untuk Inventor/SolidWorks/Fusion), STL per warna, dan render multi-sudut (PNG).
Jalankan: python3 build.py [nama_modul ...]     (tanpa argumen = semua + susunan pabrik)
Keluaran: cad/out/step/*.step, cad/out/stl/<modul>/*.stl, cad/out/render/<modul>_<sudut>.png
"""
import os, sys, json, subprocess, time
import cadquery as cq
import bgmodels as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); STEP = os.path.join(OUT, "step"); STL = os.path.join(OUT, "stl"); IMG = os.path.join(OUT, "render")
for p in (STEP, STL, IMG): os.makedirs(p, exist_ok=True)

TITLE = {"R-201": "Reaktor AnMBR standar R-201..R-214", "TK-101": "Bejana standar TK-101 / TK-301", "PM-1": "PM-1 skid praolah",
         "PM-4": "PM-4 kontainer membran", "PM-5": "PM-5 skid dosing + pompa umpan", "PM-6": "PM-6 skid pengolahan gas",
         "PM-7": "PM-7 penampung gas + flare", "PM-8": "PM-8 kontainer CHP + PM-9 HX-401", "PM-9": "PM-9 menara pendingin",
         "PM-10": "PM-10 skid lumpur", "PLANT": "Susunan pabrik 45 t TBS/jam"}
VIEWS = {"iso-depan": ((1, -1.25, .85), (0, 0, 1)), "iso-belakang": ((-1.2, 1, .75), (0, 0, 1)),
         "tampak-depan": ((0, -1, .0001), (0, 0, 1)), "tampak-atas": ((0.0001, -0.0001, 1), (0, 1, 0))}

def export(name, parts, views=VIEWS, size=(1600, 1100), step=True):
    t0 = time.time()
    if step:
        asm = cq.Assembly(name=name.replace("/", "_"))
        for n, s, c in parts:
            asm.add(cq.Workplane().add(s), name=n.replace("/", "_"), color=cq.Color(c))
        asm.save(os.path.join(STEP, name + ".step"))
    # STL per warna
    d = os.path.join(STL, name); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    groups = {}
    for n, s, c in parts: groups.setdefault(c, []).append(s)
    job = {"w": size[0], "h": size[1], "parts": [], "views": []}
    for k, (c, ss) in enumerate(groups.items()):
        fn = os.path.join(d, "g%02d.stl" % k)
        cq.exporters.export(cq.Compound.makeCompound(ss), fn, tolerance=2.0, angularTolerance=0.2)
        job["parts"].append({"stl": fn, "color": c, "opacity": .55 if c == M.CLAD and name == "R-201-cut" else 1})
    for vn, (dr, up) in views.items():
        job["views"].append({"dir": dr, "up": up, "out": os.path.join(IMG, "%s_%s.png" % (name, vn))})
    jf = os.path.join(d, "job.json"); json.dump(job, open(jf, "w"))
    r = subprocess.run(["node", "render.mjs", jf], cwd=os.path.join(HERE, "render"), capture_output=True, text=True, timeout=900)
    print(name, len(parts), "bagian", "%.0f s" % (time.time() - t0), r.stdout.strip(), r.stderr.strip()[:300])

CUT = ("-atap", "-dinding-left", "-rib-left", "-pintu-samping", "-dinding-belakang")
def cutaway(name, parts):
    keep = [p for p in parts if not any(k in p[0] for k in CUT)]
    export(name + "-potong", keep, {"iso-potong": ((1, -1.25, .95), (0, 0, 1)), "atas-potong": ((0.0001, -0.0001, 1), (0, 1, 0))}, step=False)

if __name__ == "__main__":
    want = sys.argv[1:] or list(M.MODULES) + ["PLANT"]
    for k in want:
        if k == "PLANT":
            parts, tags, _ = M.plant(simple=False)
            export("PLANT", parts, {"iso-depan": ((1, -1.1, .7), (0, 0, 1)), "iso-belakang": ((-1, 1.2, .8), (0, 0, 1)),
                                    "tampak-atas": ((0.0001, -0.0001, 1), (0, 1, 0)), "iso-selatan": ((0.3, -1, .45), (0, 0, 1))}, (2200, 1400))
        else:
            P = M.MODULES[k]()
            export(k, P)
            if k in ("PM-4", "PM-6", "PM-8"): cutaway(k, P)
