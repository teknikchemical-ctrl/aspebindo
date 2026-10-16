# -*- coding: utf-8 -*-
"""Simbol peralatan detail (gaya EPC, ISO 10628-2) untuk PFD Rev 2. Didaftarkan ke eng.Sym / eng.Surf saat diimpor.
Setiap simbol menggambar di kotak (x, y, w, h); garis luar 0,5 mm, detail 0,18-0,3 mm."""
import math
import eng
from eng import Sym, Surf

WF = '#ffffff'; BK = '#000000'
OL = .5          # garis luar alat
DT = .22         # detail


def _shell(d, x, y, w, h, r, lw=OL, fill=WF):
    """badan bejana tegak dengan kepala elipsoidal 2:1 (r = tinggi kepala)"""
    pts = d.arcpts(x + w / 2, y + r, w / 2, r, 180, 0) + d.arcpts(x + w / 2, y + h - r, w / 2, r, 360, 180)
    d.poly(pts, lw, fill)


def _tl(d, x, y, w, r, h):
    """garis tangen (seam kepala-badan)"""
    d.line([(x, y + r), (x + w, y + r)], .12)
    d.line([(x, y + h - r), (x + w, y + h - r)], .12)


def _level(d, x, y, w):
    """muka cairan + segitiga level ISO"""
    d.line([(x + .6, y), (x + w - .6, y)], .15, [1.0, .5])
    cx = x + w * .78
    d.poly([(cx - .9, y - 1.3), (cx + .9, y - 1.3), (cx, y - .1)], .15, WF)
    d.line([(cx - .6, y + .5), (cx + .6, y + .5)], .12); d.line([(cx - .35, y + .9), (cx + .35, y + .9)], .12)


def _skirt(d, x, y, w, h, r, hs):
    """rok penyangga + garis pondasi"""
    y0 = y + h - r * .35
    d.line([(x + w * .1, y0), (x + w * .1, y + h + hs)], .35)
    d.line([(x + w * .9, y0), (x + w * .9, y + h + hs)], .35)
    d.line([(x - 1.5, y + h + hs), (x + w + 1.5, y + h + hs)], .6)
    for i in range(6):
        xx = x - 1.0 + (w + 2.0) * i / 5
        d.line([(xx, y + h + hs), (xx - 1.0, y + h + hs + 1.0)], .12)


def _manhole(d, x, y, r=1.1):
    d.circ(x, y, r, .2, WF); d.circ(x, y, r * .55, .12, None)


def reactor(d, e):
    """reaktor AnMBR: bejana standar berinsulasi, kepala 2:1, rok, cincin jet, PVRV, manhole"""
    x, y, w, h = e.x, e.y, e.w, e.h; r = min(w / 4, h * .1)
    hs = e.__dict__.get('skirt', 3.0)
    # insulasi
    pts = d.arcpts(x + w / 2, y + r, w / 2 + 1.0, r + 1.0, 180, 0) + d.arcpts(x + w / 2, y + h - r, w / 2 + 1.0, r + 1.0, 360, 180)
    d.poly(pts, .15, None, BK, 'equip', [.8, .5])
    _skirt(d, x, y, w, h, r, hs)
    _shell(d, x, y, w, h, r); _tl(d, x, y, w, r, h)
    _level(d, x, y + h * .22, w)
    # cincin nosel jet
    yy = y + h - r - 2.2
    d.line([(x + w * .12, yy), (x + w * .88, yy)], .3)
    for f in (.2, .4, .6, .8):
        cx = x + w * f; d.poly([(cx - .65, yy), (cx + .65, yy), (cx, yy + 1.3)], .15, BK)
    _manhole(d, x + w * .22, y + h * .55)
    # PVRV di atas
    cx = x + w * .78; ty = y + r - r * math.sqrt(max(0, 1 - ((cx - x - w / 2) / (w / 2)) ** 2))
    d.line([(cx, ty), (cx, ty - 1.8)], .3); d.rect(cx - 1.2, ty - 3.6, 2.4, 1.8, .25, WF)
    d.line([(cx - .7, ty - 2.2), (cx + .7, ty - 3.2)], .12)


def vtank(d, e):
    """bejana standar tanpa insulasi (TK-101, TK-301): kepala 2:1, rok, level, manhole"""
    x, y, w, h = e.x, e.y, e.w, e.h; r = min(w / 4, h * .1)
    _skirt(d, x, y, w, h, r, e.__dict__.get('skirt', 3.0))
    _shell(d, x, y, w, h, r); _tl(d, x, y, w, r, h)
    _level(d, x, y + h * .30, w)
    _manhole(d, x + w * .22, y + h * .6)


def pump(d, e):
    """pompa sentrifugal ISO: rumah lingkaran, segitiga, nosel buang tangensial, alas"""
    r = e.w / 2; cx, cy = e.x + r, e.y + e.h - r
    d.circ(cx, cy, r, OL, WF)
    d.poly([(cx - r * .62, cy + r * .45), (cx, cy - r * .80), (cx + r * .62, cy + r * .45)], .2, None)
    d.poly([(cx - r * .8, cy + r + .9), (cx + r * .8, cy + r + .9), (cx + r * .55, cy + r * .82), (cx - r * .55, cy + r * .82)], .3, WF)


def pd_pump(d, e):
    """pompa positive displacement / dosis: lingkaran + rotor"""
    r = e.w / 2; cx, cy = e.x + r, e.y + e.h - r
    d.circ(cx, cy, r, OL, WF)
    d.circ(cx, cy, r * .42, .2, None)
    d.line([(cx - r * .42, cy), (cx + r * .42, cy)], .2)
    d.poly([(cx - r * .8, cy + r + .9), (cx + r * .8, cy + r + .9), (cx + r * .55, cy + r * .82), (cx - r * .55, cy + r * .82)], .3, WF)


def membrane(d, e):
    """unit UF tubular cross-flow (ISO 10628 membran): rumah + kepala ujung + diagonal + tabung"""
    x, y, w, h = e.x, e.y, e.w, e.h; c = min(2.4, w * .1)
    d.rect(x, y, c, h, .4, WF); d.rect(x + w - c, y, c, h, .4, WF)
    d.rect(x + c, y + h * .08, w - 2 * c, h * .84, OL, WF)
    for f in (.3, .5, .7):
        yy = y + h * f
        d.line([(x + c, yy), (x + w - c, yy)], .12, [1.2, .6])
    d.line([(x + c, y + h * .92), (x + w - c, y + h * .08)], .3)
    d.text(x + w * .3, y + h * .38, "UF", 1.5, 'm', True, owner=e.tag, chk=False)


def gasholder(d, e):
    """penampung gas membran ganda di atas pondasi cincin: kubah luar, membran dalam, blower udara penyangga"""
    x, y, w, h = e.x, e.y, e.w, e.h; cx = x + w / 2; hb = h * .16
    yb = y + h - hb
    d.poly(d.arcpts(cx, yb, w / 2, h - hb, 180, 0), OL, WF)
    d.line(d.arcpts(cx, yb, w / 2 - 1.4, h - hb - 2.0, 180, 0), .22, [1.2, .6])
    d.line(d.arcpts(cx, yb, w / 2 - 3.0, (h - hb) * .45, 180, 0), .15, [.5, .5])          # muka gas (isi)
    d.rect(x - .8, yb, w + 1.6, hb, .4, WF)
    for i in range(1, 8):
        d.line([(x + w * i / 8, yb + .4), (x + w * i / 8 - 1.0, y + h - .4)], .1)
    # blower udara penyangga
    fx, fy = x + w + 3.2, yb - 3.0
    d.circ(fx, fy, 2.0, .3, WF); d.line([(fx - 2.0, fy), (x + w * .97, fy)], .25)
    d.line([(fx - 1.2, fy - 1.0), (fx + 1.2, fy + 1.0)], .15); d.line([(fx - 1.2, fy + 1.0), (fx + 1.2, fy - 1.0)], .15)


def btf(d, e):
    """filter bio-trickling: kolom, distributor semprot, 2 unggun packing, demister, sump bernosel"""
    x, y, w, h = e.x, e.y, e.w, e.h; r = min(w / 4, h * .06)
    _skirt(d, x, y, w, h, r, 2.5)
    _shell(d, x, y, w, h, r); _tl(d, x, y, w, r, h)
    # demister
    ym = y + h * .10; d.rect(x + .5, ym, w - 1, h * .035, .15, None)
    for i in range(6): d.line([(x + .8 + (w - 1.6) * i / 6, ym), (x + .8 + (w - 1.6) * (i + .6) / 6, ym + h * .035)], .1)
    # distributor
    yd = y + h * .19; d.line([(x + w * .12, yd), (x + w * .88, yd)], .28)
    for f in (.25, .5, .75):
        xx = x + w * f; d.line([(xx, yd), (xx - .9, yd + 1.5)], .12); d.line([(xx, yd), (xx + .9, yd + 1.5)], .12)
    for (a, b) in ((.25, .47), (.53, .75)):
        ya, yb = y + h * a, y + h * b
        d.rect(x, ya, w, yb - ya, .2, None)
        d.line([(x, ya), (x + w, yb)], .15); d.line([(x + w, ya), (x, yb)], .15)
    _level(d, x, y + h * .85, w)


def column_pk(d, e): btf(d, e)


def hcyc(d, e):
    """hidrosiklon: kepala silinder, inlet tangensial, vortex finder, kerucut, apex"""
    x, y, w, h = e.x, e.y, e.w, e.h; cx = x + w / 2
    d.poly([(x, y), (x + w, y), (x + w, y + h * .24), (cx + w * .1, y + h * .94), (cx - w * .1, y + h * .94), (x, y + h * .24)], OL, WF)
    d.rect(cx - w * .12, y + h * .94, w * .24, h * .06, .3, WF)
    d.line([(cx - w * .16, y - 1.4), (cx - w * .16, y + h * .30)], .25); d.line([(cx + w * .16, y - 1.4), (cx + w * .16, y + h * .30)], .25)
    d.line([(x, y + h * .24), (x + w, y + h * .24)], .12)


def rscreen(d, e):
    """saringan drum putar: rumah, drum perforasi, kotak inlet, motor"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.rect(x, y + h * .18, w, h * .64, OL, WF)
    d.poly([(x + w * .05, y + h * .82), (x + w * .95, y + h * .82), (x + w * .75, y + h), (x + w * .25, y + h)], .4, WF)
    cy = y + h * .5; rr = h * .25
    d.rect(x + w * .18, cy - rr, w * .64, 2 * rr, .3, None)
    for i in range(1, 8):
        xx = x + w * (.18 + .64 * i / 8); d.line([(xx, cy - rr), (xx, cy + rr)], .1, [.4, .4])
    d.rect(x - .1, y, w * .18, h * .18, .3, WF)                                           # kotak inlet
    d.rect(x + w * .80, y + h * .02, w * .16, h * .16, .3, WF); d.text(x + w * .88, y + h * .145, "M", 1.2, 'm', True, owner=e.tag, chk=False)


def phe(d, e):
    """penukar panas pelat: pelat tetap + tekan, tiang, paket pelat"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.rect(x, y, 1.8, h, .45, WF); d.rect(x + w - 1.8, y + h * .06, 1.8, h * .88, .45, WF)
    d.line([(x + 1.8, y + .8), (x + w + 1.2, y + .8)], .3); d.line([(x + 1.8, y + h - .8), (x + w + 1.2, y + h - .8)], .3)
    d.line([(x + w + 1.2, y), (x + w + 1.2, y + h)], .45)
    n = max(6, int((w - 4) / .9))
    for i in range(n):
        xx = x + 2.2 + (w - 4.4) * (i + .5) / n; d.line([(xx, y + 1.6), (xx, y + h - 1.6)], .2)


def shtx(d, e):
    """penukar shell-and-tube TEMA (BEM): kanal + shell + tutup, berkas tabung"""
    x, y, w, h = e.x, e.y, e.w, e.h; c = h * .55
    d.poly(d.arcpts(x + c, y + h / 2, c, h / 2, 90, 270) + [(x + c, y + h), (x + c, y)], .4, WF)
    d.rect(x + c, y, w - 2 * c, h, OL, WF)
    d.poly(d.arcpts(x + w - c, y + h / 2, c, h / 2, -90, 90) + [(x + w - c, y), (x + w - c, y + h)], .4, WF)
    d.line([(x + c, y), (x + c, y + h)], .45); d.line([(x + w - c, y), (x + w - c, y + h)], .45)
    for f in (.3, .5, .7): d.line([(x + c, y + h * f), (x + w - c, y + h * f)], .15)
    for f in (.3, .55, .8): d.line([(x + c + (w - 2 * c) * f, y), (x + c + (w - 2 * c) * f, y + h * (.6 if f != .55 else 1))], .12)


def kopot(d, e):
    """KO pot dengan bantalan demister (silang) dan boot"""
    x, y, w, h = e.x, e.y, e.w, e.h; r = min(w / 4, h * .1)
    _shell(d, x, y, w, h, r); _tl(d, x, y, w, r, h)
    ym = y + h * .2; d.rect(x, ym, w, h * .1, .2, None)
    for i in range(5): d.line([(x + w * i / 5, ym), (x + w * (i + 1) / 5, ym + h * .1)], .12); d.line([(x + w * (i + 1) / 5, ym), (x + w * i / 5, ym + h * .1)], .12)
    _level(d, x, y + h * .75, w)


def blower(d, e):
    """blower / kompresor sentrifugal ISO: lingkaran + garis menyempit + alas"""
    r = min(e.w, e.h) / 2; cx, cy = e.x + e.w / 2, e.y + e.h / 2
    d.circ(cx, cy, r, OL, WF)
    a, b = math.radians(122), math.radians(32)
    d.line([(cx + r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(b), cy - r * math.sin(b))], .3)
    d.line([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + r * math.cos(b), cy + r * math.sin(b))], .3)


def acf(d, e):
    """adsorber karbon aktif: bejana, unggun karbon (titik), grid penyangga, distributor"""
    x, y, w, h = e.x, e.y, e.w, e.h; r = min(w / 4, h * .1)
    _skirt(d, x, y, w, h, r, 2.0)
    _shell(d, x, y, w, h, r); _tl(d, x, y, w, r, h)
    ya, yb = y + h * .30, y + h * .72
    d.line([(x, ya), (x + w, ya)], .2); d.line([(x, yb), (x + w, yb)], .35)
    for i in range(5):
        for j in range(4):
            d.circ(x + w * (.15 + .175 * i + (.08 if j % 2 else 0)), ya + (yb - ya) * (.15 + .23 * j), .32, .1, None)
    d.line([(x + w * .15, y + h * .18), (x + w * .85, y + h * .18)], .2)


def flare(d, e):
    """flare tertutup: badan berlapis refraktori, burner + pilot di dasar, nyala"""
    x, y, w, h = e.x, e.y, e.w, e.h; cx = x + w / 2
    d.rect(x, y + h * .14, w, h * .86, OL, WF)
    d.line([(x + .9, y + h * .14), (x + .9, y + h)], .12, [.6, .4]); d.line([(x + w - .9, y + h * .14), (x + w - .9, y + h)], .12, [.6, .4])
    d.line([(x + w * .2, y + h * .82), (x + w * .8, y + h * .82)], .3)
    for f in (.3, .5, .7): d.poly([(x + w * f - .5, y + h * .82), (x + w * f + .5, y + h * .82), (x + w * f, y + h * .78)], .1, BK)
    d.poly([(cx - w * .32, y + h * .14), (cx - w * .12, y - 1.0), (cx, y + h * .06), (cx + w * .14, y - 2.4), (cx + w * .32, y + h * .14)], .25, WF)
    for i in range(4):
        d.rect(x - 1.0, y + h * (.86 + .025 * i) - .2, 1.0, .4, .1, None)                 # louver udara


def genset(d, e):
    """kontainer genset biogas: mesin V (blok + kepala silinder), roda gila, generator, radiator di atap"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.rect(x, y, w, h, OL, WF); d.rect(x + .9, y + .9, w - 1.8, h - 1.8, .15, None, dash=[1.2, .7])
    ex, ey, ew, eh = x + w * .1, y + h * .35, w * .42, h * .42
    d.rect(ex, ey, ew, eh, .4, WF)
    for i in range(6):
        xx = ex + ew * (i + .5) / 6; d.rect(xx - ew * .05, ey - h * .1, ew * .1, h * .1, .2, WF)
    d.text(ex + ew / 2, ey + eh * .65, "MESIN GAS", 1.15, 'm', True, owner=e.tag, chk=False)
    d.rect(ex + ew, ey + eh * .25, w * .03, eh * .5, .3, WF)
    gx = x + w * .73; gy = ey + eh / 2; rg = eh * .48
    d.line([(ex + ew + w * .03, gy), (gx - rg, gy)], .45)
    d.circ(gx, gy, rg, .4, WF); d.text(gx, gy - .2, "G", 2.0, 'm', True, owner=e.tag, chk=False)
    d.text(gx, gy + 2.0, "3~", 1.2, 'm', False, owner=e.tag, chk=False)
    # radiator / dump cooler di atap
    d.rect(x + w * .62, y - 2.6, w * .3, 2.6, .3, WF)
    for i in range(1, 6): d.line([(x + w * (.62 + .3 * i / 6), y - 2.6), (x + w * (.62 + .3 * i / 6), y)], .1)


def wherb(d, e):
    """penukar panas gas buang (economizer bersirip) tegak dengan bypass"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.rect(x, y, w, h, OL, WF)
    for i in range(5):
        yy = y + h * (.18 + .16 * i)
        d.line([(x + w * .15, yy), (x + w * .85, yy)], .2)
        for k in range(6): d.line([(x + w * (.2 + .11 * k), yy - .7), (x + w * (.2 + .11 * k), yy + .7)], .1)
    d.line([(x + w * .85, y + h * .18), (x + w * .85, y + h * .82)], .2); d.line([(x + w * .15, y + h * .34), (x + w * .15, y + h * .66)], .2)


def stack(d, e):
    x, y, w, h = e.x, e.y, e.w, e.h
    d.poly([(x + w * .25, y), (x + w * .75, y), (x + w, y + h), (x, y + h)], OL, WF)
    d.line([(x + w * .18, y + h * .1), (x + w * .82, y + h * .1)], .25)
    d.line([(x + w * .2, y + h * .5), (x + w * .8, y + h * .5)], .12, [.6, .4])
    d.rect(x - 1, y + h, w + 2, 1.2, .3, WF)


def ctower(d, e):
    """menara pendingin induced-draft sel modular: badan, fill, eliminator, fan, bak"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.poly([(x + w * .1, y + h * .16), (x + w * .9, y + h * .16), (x + w, y + h * .84), (x, y + h * .84)], OL, WF)
    d.rect(x - .8, y + h * .84, w + 1.6, h * .16, .45, WF)
    _level(d, x, y + h * .92, w)
    d.poly([(x + w * .3, y + h * .16), (x + w * .34, y), (x + w * .66, y), (x + w * .7, y + h * .16)], .4, WF)
    d.line([(x + w * .36, y + h * .08), (x + w * .64, y + h * .08)], .5); d.circ(x + w * .5, y + h * .08, .5, .1, BK)
    d.line([(x + w * .14, y + h * .26), (x + w * .86, y + h * .26)], .15)                  # eliminator
    for i in range(7):
        xx = x + w * (.14 + .1 * i); d.line([(xx, y + h * .45), (xx + w * .06, y + h * .7)], .12)   # fill
    d.line([(x + w * .1, y + h * .45), (x + w * .9, y + h * .45)], .12); d.line([(x + w * .06, y + h * .7), (x + w * .94, y + h * .7)], .12)
    d.line([(x + w * .14, y + h * .36), (x + w * .86, y + h * .36)], .25)                  # spray header
    for f in (.25, .45, .65, .8): d.poly([(x + w * f - .5, y + h * .36), (x + w * f + .5, y + h * .36), (x + w * f, y + h * .40)], .1, BK)


def dtank(d, e):
    """tangki dosis atap datar + pengaduk + motor"""
    x, y, w, h = e.x, e.y, e.w, e.h; cx = x + w / 2
    d.rect(x, y, w, h, OL, WF)
    d.rect(cx - 1.2, y - 2.4, 2.4, 2.4, .3, WF); d.text(cx, y - .6, "M", 1.0, 'm', True, owner=e.tag, chk=False)
    d.line([(cx, y), (cx, y + h * .78)], .3)
    d.poly([(cx - w * .24, y + h * .74), (cx - w * .04, y + h * .78), (cx - w * .24, y + h * .82)], .15, BK)
    d.poly([(cx + w * .24, y + h * .74), (cx + w * .04, y + h * .78), (cx + w * .24, y + h * .82)], .15, BK)
    _level(d, x, y + h * .25, w)


def ftank(d, e):
    """tangki CIP atap kerucut + pemanas listrik"""
    x, y, w, h = e.x, e.y, e.w, e.h; rf = min(h * .12, w * .2)
    d.poly([(x, y + rf), (x + w / 2, y), (x + w, y + rf), (x + w, y + h), (x, y + h)], OL, WF)
    _level(d, x, y + rf + (h - rf) * .25, w)
    yy = y + h * .82
    d.line([(x + w, yy - 1), (x + w * .3, yy - 1), (x + w * .3, yy + 1), (x + w, yy + 1)], .25)


def spress(d, e):
    """screw press: badan saringan miring, ulir, corong umpan, motor-gearbox, chute kue"""
    x, y, w, h = e.x, e.y, e.w, e.h
    d.poly([(x, y + h * .2), (x + w * .82, y), (x + w * .82, y + h * .72), (x, y + h * .92)], OL, WF)
    for i in range(1, 10):
        xx = x + w * .82 * i / 10; d.line([(xx, y + h * .2 - h * .2 * i / 10 + .4), (xx + w * .035, y + h * .92 - h * .2 * i / 10 - .4)], .2)
    d.line([(x, y + h * .56), (x + w * .82, y + h * .36)], .15, [.6, .4])
    d.rect(x + w * .82, y + h * .1, w * .09, h * .52, .35, WF); d.rect(x + w * .91, y + h * .18, w * .09, h * .36, .35, WF)
    d.text(x + w * .955, y + h * .42, "M", 1.1, 'm', True, owner=e.tag, chk=False)
    d.poly([(x + w * .1, y - 2.4), (x + w * .36, y - 2.4), (x + w * .30, y + h * .15), (x + w * .16, y + h * .17)], .3, WF)
    d.poly([(x + w * .5, y + h * .8), (x + w * .66, y + h * .74), (x + w * .64, y + h + 1.8), (x + w * .56, y + h + 1.8)], .3, WF)


def lamella(d, e):
    """settler lamella: badan persegi + paket pelat miring + 2 corong lumpur di bawah"""
    x, y, w, h = e.x, e.y, e.w, e.h; hb = h * .66
    d.rect(x, y, w, hb, OL, WF)
    for i in range(9):
        xx = x + w * (.18 + .07 * i)
        d.line([(xx, y + hb * .78), (xx + w * .1, y + hb * .22)], .2)
    d.line([(x + w * .05, y + hb * .12), (x + w * .95, y + hb * .12)], .15, [1.0, .6])
    for k in range(2):
        x0 = x + w * k / 2
        d.poly([(x0, y + hb), (x0 + w / 2, y + hb), (x0 + w * .29, y + h), (x0 + w * .21, y + h)], OL, WF)


for _n in ('reactor', 'vtank', 'pump', 'pd_pump', 'membrane', 'lamella', 'gasholder', 'btf', 'hcyc', 'rscreen', 'phe', 'shtx', 'kopot', 'blower',
           'acf', 'flare', 'genset', 'wherb', 'stack', 'ctower', 'dtank', 'ftank', 'spress'):
    setattr(Sym, _n + '2', staticmethod(globals()[_n]))


# ------------------------------------------------------------ titik permukaan
def _vhead(e, side, f, rr):
    if side in 'tb': return Surf._head(e, side, f, rr)
def _pumpsurf(e, side, f): return Surf.pump(e, side, f)
def _blowsurf(e, side, f):
    r = min(e.w, e.h) / 2; cx, cy = e.x + e.w / 2, e.y + e.h / 2
    if side == 'l': return (cx - r, cy, 'L')
    if side == 'r': return (cx + r, cy, 'R')
    xx = e.x + f * e.w; u = min(1, abs(xx - cx) / r); dy = r * math.sqrt(max(0, 1 - u * u))
    return (xx, cy - dy, 'U') if side == 't' else (xx, cy + dy, 'D')
for _n in ('reactor', 'vtank', 'acf', 'kopot'):
    setattr(Surf, _n + '2', staticmethod(lambda e, side, f: _vhead(e, side, f, min(e.w / 4, e.h * .1))))
Surf.btf2 = staticmethod(lambda e, side, f: _vhead(e, side, f, min(e.w / 4, e.h * .06)))
Surf.pump2 = staticmethod(_pumpsurf); Surf.pd_pump2 = staticmethod(_pumpsurf); Surf.blower2 = staticmethod(_blowsurf)
