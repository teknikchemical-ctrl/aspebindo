# -*- coding: utf-8 -*-
"""Ekspor model 3D lokasi lengkap (PKS proksi + kolam + produk) ke STEP. python3 build_site.py
Keluaran: cad/out/step/SITE.step (+zip), cad/out/site.json. Render lokasi: diorama.py (DIORAMA_*.png)."""
import os, time, zipfile
import cadquery as cq
import site3d as SI

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, "out", "step"); os.makedirs(STEP, exist_ok=True)

def main():
    t0 = time.time()
    P, info = SI.site(); js = SI.write_info(info)
    print(len(P), "bagian", "%.0f s" % (time.time() - t0))
    asm = cq.Assembly(name="SITE")
    groups = {}
    for n, s, c in P: groups.setdefault((n.split("/")[0] if "/" in n else n.split("-")[0], c), []).append(s)
    for (k, c), ss in groups.items():
        asm.add(cq.Workplane().add(cq.Compound.makeCompound(ss)), name=("%s_%s" % (k, c[1:])).replace("/", "_"), color=cq.Color(c))
    fn = os.path.join(STEP, "SITE.step"); asm.save(fn)
    with zipfile.ZipFile(fn.replace(".step", "_step.zip"), "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z: z.write(fn, "SITE.step")
    print("STEP", os.path.getsize(fn) / 1e6, "MB", "%.0f s" % (time.time() - t0))
    return info, js

if __name__ == "__main__":
    main()
