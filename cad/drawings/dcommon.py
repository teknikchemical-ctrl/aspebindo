# -*- coding: utf-8 -*-
"""
Infrastruktur lembar gambar teknik produk (A3 lanskap, proyeksi sudut pertama) di atas drawing_engine (kd/vw).
Blok judul mengikuti format contoh (University | Checked by | Design Lab. | Document type | Rev ...).
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "drawing_engine")); sys.path.insert(0, os.path.join(ROOT, "cad"))
os.chdir(os.path.join(ROOT, "drawing_engine"))
from kd import *            # noqa
import kd, eng
from vw import View, cl     # noqa
from PIL import Image

# ---- identitas (isi sesuai tim) ------------------------------------------------------------
UNIV = "UNIVERSITAS"
TEAM = "NAMA TIM"
CHECKED = "-"
APPROVED = "-"
DATE = "15/10/2026"
NSHEET = 9
eng.DOC_AUTHOR = TEAM
OUT = os.path.join(ROOT, "cad", "drawings", "out"); os.makedirs(OUT, exist_ok=True)
REND = os.path.join(ROOT, "cad", "out", "render")

FX0, FY0, FX1, FY1 = 10.0, 10.0, 410.0, 287.0
TBW, TBH = 236.0, 33.0
TBX, TBY = FX1 - TBW, FY1 - TBH

def frame(sheet, title, docno, scale, dtype="Part Engineering Drawing", rev="0"):
    """bingkai A3 + tanda pusat (segitiga) + blok judul gaya contoh"""
    eng.DOC_TITLE = "%s - %s" % (docno, title)
    d.rect(5, 5, 410, 287, .3, None, 'frame'); d.rect(FX0, FY0, FX1 - FX0, FY1 - FY0, .8, None, 'frame')
    # tanda pusat + segitiga penunjuk (seperti contoh)
    for (x, y, dx, dy) in ((210, 5, 0, 1), (210, 292, 0, -1), (5, 148.5, 1, 0), (415, 148.5, -1, 0)):
        x2, y2 = x + dx * 9, y + dy * 9
        d.line([(x, y), (x2, y2)], .5, None, K, 'frame')
        if dx == 0:
            d.poly([(x - 2.2, y + dy * 2.5), (x + 2.2, y + dy * 2.5), (x, y + dy * 6.5)], .4, '#ffffff', K, 'frame')
        else:
            d.poly([(x + dx * 2.5, y - 2.2), (x + dx * 2.5, y + 2.2), (x + dx * 6.5, y)], .4, '#ffffff', K, 'frame')
    x0, y0 = TBX, TBY
    d.rect(x0, y0, TBW, TBH, 0, '#ffffff', 'frame'); d.rect(x0, y0, TBW, TBH, .7, None, 'frame')
    cw = [44, 52, 58, 82]; xs = [x0]
    for w in cw: xs.append(xs[-1] + w)
    rh = TBH / 3; ys = [y0, y0 + rh, y0 + 2 * rh, y0 + TBH]
    ln = lambda p, q, w=.3: d.line([p, q], w, None, K, 'frame')
    for x in xs[1:-1]: ln((x, y0), (x, y0 + TBH))
    ln((xs[0], ys[1]), (xs[2], ys[1])); ln((xs[1], ys[2]), (xs[2], ys[2])); ln((xs[2], ys[1]), (xs[3], ys[1]))
    ln((xs[3], ys[1]), (xs[4], ys[1])); ln((xs[3], ys[2]), (xs[4], ys[2]))
    def lab(x, y, t): T(x + 1.2, y + 2.6, t, 2.0, 'l', layer='frame')
    def val(x, y, t, s=3.0, a='l', w=None):
        if a == 'm': TC(x + w / 2, y + rh * .58, t, s, 'm', layer='frame')
        else: T(x + 2.0, y + rh - 1.6, t, s, 'l', layer='frame')
    lab(xs[0], ys[0], "University"); val(xs[0], ys[0], UNIV, 2.8)
    lab(xs[1], ys[0], "Checked by :"); val(xs[1], ys[0], CHECKED, 2.8)
    lab(xs[1], ys[1], "Author :"); val(xs[1], ys[1], TEAM, 2.8)
    lab(xs[1], ys[2], "Eng. Approved by :"); val(xs[1], ys[2], APPROVED, 2.8)
    TC(xs[2] + cw[2] / 2, ys[0] + rh * .55, "Design Lab.", 4.2, 'm', layer='frame')
    # judul bagian (baris 2-3)
    ls = title.split("\n")
    for i, l_ in enumerate(ls):
        TC(xs[2] + cw[2] / 2, ys[1] + rh + (i - (len(ls) - 1) / 2) * 5.6, l_, 3.2, 'm', layer='frame')
    # kolom kanan: jenis dokumen + rev / unit-skala-tanggal-ukuran / no dok + lembar
    xr = xs[3]; wr = cw[3]; wrev = 12
    ln((xr + wr - wrev, ys[0]), (xr + wr - wrev, ys[2]))
    lab(xr, ys[0], "Document type"); val(xr, ys[0], dtype, 2.8)
    lab(xr + wr - wrev, ys[0], "Rev"); TC(xr + wr - wrev / 2, ys[0] + rh * .62, rev, 3.0, 'm', layer='frame')
    sub = [12, 30, 28]; xx = xr
    for (w, l_, v) in zip(sub, ("Unit", "Scale", "Creation date"), ("mm", scale, DATE)):
        ln((xx + w, ys[1]), (xx + w, ys[2])); lab(xx, ys[1], l_); TC(xx + w / 2, ys[1] + rh * .66, v, 2.8 if len(v) < 10 else 2.5, 'm', layer='frame'); xx += w
    lab(xr + wr - wrev, ys[1], "Size"); TC(xr + wr - wrev / 2, ys[1] + rh * .66, "A3", 2.8, 'm', layer='frame')
    ln((xr + 56, ys[2]), (xr + 56, ys[3]))
    TC(xr + 28, ys[2] + rh * .55, docno, 3.0, 'm', layer='frame')
    lab(xr + 56, ys[2], "Sheet number"); TC(xr + 69, ys[2] + rh * .66, "%d / %d" % (sheet, NSHEET), 3.0, 'm', layer='frame')
    # simbol proyeksi sudut pertama
    cx, cy = xs[0] + 22, ys[1] + rh
    d.circ(cx - 9, cy, 4.2, .35, None, 'frame'); d.circ(cx - 9, cy, 2.0, .35, None, 'frame')
    d.poly([(cx + 1, cy - 2.6), (cx + 12, cy - 4.6), (cx + 12, cy + 4.6), (cx + 1, cy + 2.6)], .35, None, K, 'frame')
    d.line([(cx - 15, cy), (cx + 15, cy)], .2, [3, .8, .8, .8], K, 'frame'); d.line([(cx - 9, cy - 6), (cx - 9, cy + 6)], .2, [3, .8, .8, .8], K, 'frame')
    zone('BLOK JUDUL', (x0, y0, x0 + TBW, y0 + TBH))

def image(fn, x, y, w, h, trim=True, name=None):
    """sisipkan render PNG (dipangkas putihnya) di dalam kotak (x,y,w,h), proporsional, terpusat. Didaftarkan sebagai zona."""
    src = os.path.join(REND, fn)
    im = Image.open(src).convert("RGB")
    if trim:
        import PIL.ImageOps as IO
        bb = IO.invert(im).getbbox()
        if bb: im = im.crop((max(0, bb[0] - 6), max(0, bb[1] - 6), min(im.width, bb[2] + 6), min(im.height, bb[3] + 6)))
    out = os.path.join(OUT, "_img_" + fn)
    im.save(out)
    k = min(w / im.width, h / im.height); ww, hh = im.width * k, im.height * k
    xx, yy = x + (w - ww) / 2, y + (h - hh) / 2
    d.items['util'].append(('image', out, xx, yy, ww, hh))
    zone(name or fn, (xx, yy, xx + ww, yy + hh))
    return (xx, yy, xx + ww, yy + hh)

def table(x, y, cols, rows, title=None, rh=5.2, size=2.6, hsize=2.7, zname=None):
    """tabel sederhana; cols = [(judul, lebar, align)], rows = [[...]]"""
    W_ = sum(c[1] for c in cols); y0 = y
    if title:
        d.rect(x, y, W_, 6.0, .0, '#e9e9e9', 'table'); d.rect(x, y, W_, 6.0, .5, None, 'table')
        TC(x + W_ / 2, y + 3.0, title, 3.0, 'm', layer='table'); y += 6.0
    d.rect(x, y, W_, rh, 0, '#f3f3f3', 'table')
    xx = x
    for (h_, w, a) in cols:
        TC(xx + (w / 2 if a == 'm' else 1.2 if a == 'l' else w - 1.2), y + rh / 2, h_, hsize, a, layer='table'); xx += w
    y += rh
    d.line([(x, y), (x + W_, y)], .4, None, K, 'table')
    for r in rows:
        xx = x
        for (h_, w, a), v in zip(cols, r):
            TC(xx + (w / 2 if a == 'm' else 1.2 if a == 'l' else w - 1.2), y + rh / 2, str(v), size, a, layer='table'); xx += w
        y += rh
        d.line([(x, y), (x + W_, y)], .15, None, K, 'table')
    d.rect(x, y0, W_, y - y0, .5, None, 'table')
    xx = x
    for (h_, w, a) in cols[:-1]:
        xx += w; d.line([(xx, y0 + (6.0 if title else 0)), (xx, y)], .15, None, K, 'table')
    zone(zname or ("TABEL", x), (x, y0, x + W_, y))
    return y

def note(x, y, lines, size=3.0, title="CATATAN :"):
    T(x, y, title, size, 'l', owner=('note', x, y))
    for i, l_ in enumerate(lines): T(x, y + (i + 1) * size * 1.65, l_, size, 'l', owner=('note', x, y))
    return y + (len(lines) + 1) * size * 1.65

def finish(name):
    iss = check(verbose=True)
    d.pdf(os.path.join(OUT, name + ".pdf"))
    try: d.dxf(os.path.join(OUT, name + ".dxf"))
    except Exception as e: print("dxf gagal", e)
    if iss:
        check(verbose=False, overlay=True); d.pdf(os.path.join(OUT, name + "_chk.pdf"))
    print(name, "ISU =", len(iss))
    return len(iss)

# ---------------------------------------------------------------- tampilan detail (diperbesar)
import cadquery as cq
def crop(shapes, ang, r0, r1, z0, z1, w, cx=0, cy=0):
    """potong kumpulan bentuk dengan kotak lokal: arah radial sudut ang (deg) dari r0..r1, lebar w, tinggi z0..z1"""
    bx = cq.Solid.makeBox(r1 - r0, w, z1 - z0, cq.Vector(r0, -w / 2, z0)).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), ang).translate(cq.Vector(cx, cy, 0))
    out = []
    for s in shapes:
        try:
            r = s.intersect(bx)
            if r.Volume() > 1: out.append(r)
        except Exception:
            pass
    return out

def detail_view(shapes, ang, origin, scale, ox, oy, name, cx=0, cy=0):
    """potongan vertikal melalui bidang radial sudut ang; sumbu-x kertas = arah radial keluar"""
    a = math.radians(ang)
    V = View((math.sin(a), -math.cos(a), 0), (math.cos(a), math.sin(a), 0), scale, ox, oy, origin=(cx, cy, 0), name=name)
    V.section(shapes, origin, hatch_sp=1.2, ang=45, draw_rest=True)
    kd.OPEN_VIEWS.add(name)
    return V

def callout(p, r, letter, size=3.5, ang=45):
    """lingkaran rujukan detail pada tampilan induk"""
    d.circ(p[0], p[1], r, .35, None, 'util', K)
    a = math.radians(ang)
    tx, ty = p[0] + (r + 3.2) * math.cos(a), p[1] - (r + 3.2) * math.sin(a)
    TC(tx, ty, letter, size, 'm', owner=('callout', letter))

def mass_of(parts, pred):
    return sum(s.Volume() for n, s, c in parts if pred(n)) * 7.85e-9 * 1000   # kg
