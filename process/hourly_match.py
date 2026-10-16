# -*- coding: utf-8 -*-
"""Kecocokan per jam antara keluaran set dan beban solar PKS (temuan audit #1; angka dipakai fin_core.py dan Excel).
Masukan: process/outputs/year_daily.json = keluaran year_sim() 365 hari (util 0,75; Minggu libur; henti 14 hari) pada konfigurasi desain utama.
Aturan:
  * solar PKS hanya dibakar pada jam PKS tidak mengolah (listrik jam olah dipasok turbin uap berbahan biomassa milik PKS);
  * jam olah setahun = util x 6.000 jam (300 hari x 20 jam); jam tidak olah = 8.760 - jam olah; hari olah dibagi sebanding util harian;
  * beban solar rata (kW) pada jam tidak olah; set menggantikan min(daya neto harian set, beban);
  * tanpa tangki ekualisasi (desain dasar): Minggu dan henti 14 hari praktis tanpa keluaran; dengan tangki 24 jam (opsi PM-12): umpan dan daya dirata-ratakan 7 hari,
    henti 14 hari tetap nol.
match = energi solar yang tergantikan / energi beban solar (ketersediaan genset 0,93 dikalikan terpisah di model keuangan)."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "outputs", "year_daily.json")))
GRID = [1.0] + [float(x) for x in range(50, 1501, 50)]       # kW; simpul interpolasi (identik di Excel)

def profile(buffer=False, util_mean=0.75):
    P = np.array(D["P_net"], float); u = np.array(D["util"], float)
    if buffer:
        Ps = P.copy(); n = len(P)
        for i in range(n):
            if u[i] <= 0 and not (6 <= i % 7 == 6): pass
        shut = (u == 0) & (np.arange(n) % 7 != 6)               # hari henti (bukan Minggu)
        for i in range(n):
            if shut[i]: continue
            idx = [j for j in range(max(0, i - 3), min(n, i + 4)) if not shut[j]]
            Ps[i] = P[idx].mean() if idx else P[i]
        P = Ps
    hp = np.where(u > 0, u / u.max(), 0.0)
    hp = np.minimum(hp * (util_mean * 6000.0 / hp.sum()), 20.0)
    hp *= util_mean * 6000.0 / hp.sum()
    return P, 24.0 - hp                                          # daya neto harian (kW), jam tidak olah per hari

def match_at(load_kW, buffer=False):
    P, h = profile(buffer)
    return float(np.sum(np.minimum(P, load_kW) * h) / (load_kW * h.sum()))

def curve(buffer=False):
    return GRID, [match_at(x, buffer) for x in GRID]

def match_f(load_kW, buffer=False, _c={}):
    k = bool(buffer)
    if k not in _c: _c[k] = curve(k)
    xs, ys = _c[k]
    return float(np.interp(load_kW, xs, ys))

if __name__ == "__main__":
    P, h = profile()
    print("jam tidak olah/th %.0f | daya neto rata %.0f kW | Minggu %.0f kW | henti %.1f kW" % (h.sum(), P.mean(), P[6::7].mean(), P[40:54].mean()))
    for L in (100, 150, 238, 300, 400, 475, 600):
        print("beban %4d kW -> match %.3f | dengan tangki 24 jam %.3f" % (L, match_at(L), match_at(L, True)))
