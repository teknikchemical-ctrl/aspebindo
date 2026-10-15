# -*- coding: utf-8 -*-
"""Susun buku render 3D (PDF A4 lanskap, 1 halaman per modul, 4 sudut) dari cad/out/render/*.png"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from build import TITLE
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "out", "render")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 3508, 2480
pages = []
for k in ["PLANT", "R-201", "TK-101", "PM-1", "PM-4", "PM-5", "PM-6", "PM-7", "PM-8", "PM-9", "PM-10"]:
    views = [f for f in sorted(os.listdir(IMG)) if f.startswith(k + "_")]
    if k in ("PM-4", "PM-6", "PM-8"): views = [k + "_iso-depan.png", k + "_iso-belakang.png", k + "-potong_iso-potong.png", k + "-potong_atas-potong.png"]
    else: views = [v for v in (k + "_iso-depan.png", k + "_iso-belakang.png", k + "_tampak-depan.png", k + "_tampak-atas.png", k + "_iso-selatan.png") if v in views][:4]
    pg = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(pg)
    d.text((120, 70), TITLE[k], font=ImageFont.truetype(FB, 80), fill="black"); d.line([(120, 175), (W - 120, 175)], fill="black", width=4)
    for i, v in enumerate(views):
        im = Image.open(os.path.join(IMG, v)).convert("RGB"); bb = ImageOps.invert(im).getbbox(); im = im.crop(bb) if bb else im
        cw, ch = (W - 360) // 2, (H - 420) // 2; im.thumbnail((cw, ch - 70))
        x0 = 120 + (i % 2) * (cw + 120) + (cw - im.width) // 2; y0 = 220 + (i // 2) * ch + (ch - 70 - im.height) // 2
        pg.paste(im, (x0, y0))
        lab = v.split("_")[1][:-4].replace("-", " ").replace("iso", "isometri").replace("potong", "(potong)")
        d.text((120 + (i % 2) * (cw + 120) + cw // 2, 220 + (i // 2) * ch + ch - 55), lab, font=ImageFont.truetype(F, 46), fill="black", anchor="mm")
    d.text((120, H - 80), "Generator Biogas Portabel - model 3D CadQuery (mm), STEP di cad/out/step/%s.step" % k, font=ImageFont.truetype(F, 40), fill="#555555")
    pages.append(pg)
out = os.path.join(HERE, "out", "BG_3D_renders.pdf")
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=300)
print(out, len(pages))
