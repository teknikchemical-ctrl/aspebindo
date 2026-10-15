# -*- coding: utf-8 -*-
"""Gambar analisis ekonomi (gaya makalah: serif, label (a)-(d), palet hijau-teal/oranye/merah)."""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import fin_core as F, fin_market as MK

OUT = os.path.join(F.HERE, "outputs", "figs"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 220, "figure.dpi": 110})
DK, TE, LT, OR, RD, BL, GR = "#1f4e4a", "#3d8b7d", "#cfe3df", "#d4952b", "#b2472f", "#3f6d9a", "#8c8c8c"
M = 1e6
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight"); plt.close(fig); return os.path.join(OUT, name)

def fig_market(o):
    mk = MK.market(o)
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.0), gridspec_kw=dict(width_ratios=[1, 1.35]))
    a = ax[0]; a.set_aspect("equal"); a.axis("off")
    for r, c, lab, val, y in ((1.0, DK, "TAM", mk["TAM"], .62), (.68, TE, "SAM", mk["SAM"], .06), (.36, OR, "SOM (2034)", mk["SOM"], -.62)):
        a.add_patch(Circle((0, r - 1.0), r, color=c, ec="white", lw=1.5))
        a.text(0, y - .02, "%s\nUSD %s juta/th" % (lab, format(round(val / M), ",").replace(",", ".")) if val < 1e9 else
               "%s\nUSD %s miliar/th" % (lab, ("%.2f" % (val / 1e9)).replace(".", ",")), ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
    a.set_xlim(-1.05, 1.05); a.set_ylim(-1.05, 1.05)
    a.set_title("(a) Corong pasar (pendapatan energi + karbon + jasa)")
    a.text(0, -1.12, "TAM %d PKS | SAM %d PKS | SOM %d set" % (mk["sets_TAM"], mk["sets_SAM"], mk["sets_SOM"]), ha="center", fontsize=8)
    b = ax[1]
    names = [p for p, n in MK.PROV]; n_ = np.array([n for p, n in MK.PROV])
    sam = n_ * MK.SH_SIZE * MK.SH_NOCAP * np.array([1 if p != "Lainnya" else 0.25 for p in names])
    x = np.arange(len(names))
    b.bar(x - .2, n_, .4, color=LT, ec=TE, label="Jumlah PKS (estimasi)")
    b.bar(x + .2, sam, .4, color=TE, label="PKS sasaran (30-60 t/jam, tanpa penangkap metana)")
    b.set_xticks(x); b.set_xticklabels(names, rotation=30, ha="right"); b.set_ylabel("jumlah PKS")
    b.set_title("(b) Sebaran PKS & pasar sasaran per provinsi"); b.legend(frameon=False, fontsize=7.5)
    return save(fig, "g01_pasar.png")

def fig_porter_pestle():
    fig = plt.figure(figsize=(11, 8.2))
    a = fig.add_subplot(2, 2, 1)
    forces = list(MK.PORTER.keys()); sc = [np.mean([s for _, s, _ in MK.PORTER[f]]) for f in forces]
    cols = [TE if s < 3.0 else OR if s < 3.5 else RD for s in sc]
    a.barh(forces[::-1], sc[::-1], color=cols[::-1])
    for i, s in enumerate(sc[::-1]): a.text(s + .04, i, ("%.2f" % s).replace(".", ","), va="center", fontsize=8)
    m = np.mean(sc); a.axvline(m, ls=":", c=GR); a.set_xlim(0, 5)
    a.set_xlabel("Tekanan (1 rendah - 5 tinggi); rata-rata %s" % ("%.2f" % m).replace(".", ","))
    a.set_title("(a) Lima kekuatan Porter (tertimbang)")
    b = fig.add_subplot(2, 2, 2, projection="polar")
    ang = np.linspace(0, 2 * np.pi, 5, endpoint=False).tolist(); ang += ang[:1]
    for (seg, vals_), c in zip(MK.SEG_RADAR.items(), (DK, OR, TE, RD)):
        vv = vals_ + vals_[:1]; b.plot(ang, vv, c=c, lw=1.6, label=seg); b.fill(ang, vv, c=c, alpha=.06)
    b.set_xticks(ang[:-1]); b.set_xticklabels(MK.FORCE_ORDER, fontsize=8); b.set_ylim(0, 5); b.set_yticks([1, 3, 5])
    b.set_title("(b) Radar tekanan menurut segmen", pad=14); b.legend(loc="lower center", bbox_to_anchor=(.5, -.32), ncol=2, frameon=False, fontsize=7.5)
    c = fig.add_subplot(2, 2, 3)
    ps = MK.pestle_scores(); cats = list(ps.keys())
    vals_ = [ps[k] for k in cats]
    c.barh(cats[::-1], vals_[::-1], color=[TE if v >= 0 else RD for v in vals_[::-1]])
    for i, v in enumerate(vals_[::-1]): c.text(v + (1 if v >= 0 else -1), i, "%+d" % v, va="center", ha="left" if v >= 0 else "right", fontsize=8)
    c.axvline(0, c="k", lw=.8); c.set_xlim(-45, 50)
    c.set_xlabel("Skor bersih (peluang - ancaman); total %+d" % sum(vals_)); c.set_title("(c) Skor bersih PESTLE (21 faktor)")
    d = fig.add_subplot(2, 2, 4)
    for (n_, at, ab, sz), col in zip(MK.SEGMENTS, (DK, TE, OR, BL, "#7a5c9e", RD, GR)):
        d.scatter(ab, at, s=sz, color=col, zorder=3); d.annotate(n_, (ab, at), xytext=(6, 4), textcoords="offset points", fontsize=7.5)
    d.axhline(3, c=GR, lw=.6, ls=":"); d.axvline(3, c=GR, lw=.6, ls=":")
    d.set_xlim(1.5, 5); d.set_ylim(2, 4.5); d.set_xlabel("Kemampuan memenangkan pasar (1-5)"); d.set_ylabel("Daya tarik pasar (1-5)")
    d.set_title("(d) Daya tarik dan kemampuan menang"); d.grid(alpha=.2)
    fig.tight_layout(); return save(fig, "g02_porter_pestle.png")

def fig_capex_opex(o):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.2))
    rows = o["capex_rows"]
    grp = {}
    for g, n, q, u, c, t, b in rows:
        key = n.split(" ")[0] if g == "PEC" else g.title()
        if g == "PEC":
            key = ("Bejana standar" if ("Reaktor" in n or "TK-101" in n) else "Membran + PM-4" if ("Membran" in n or "PM-4" in n) else
                   "Genset PM-8" if "PM-8" in n else "Skid proses PM-1/5/6/7/9/10" if n.startswith("PM-") else "Listrik, I&C, pipa, PLN")
        grp[key] = grp.get(key, 0) + t
    ks = sorted(grp, key=lambda k: -grp[k])
    a = ax[0]; a.barh(ks[::-1], [grp[k] / M for k in ks[::-1]], color=TE)
    for i, k in enumerate(ks[::-1]): a.text(grp[k] / M + .02, i, "%.2f" % (grp[k] / M), va="center", fontsize=8)
    a.set_xlabel("USD juta"); a.set_title("(a) CAPEX (FCI USD %.2f juta)" % (o["fci"] / M))
    b = ax[1]; it = o["opex_items"]; ks2 = sorted(it, key=lambda k: -it[k][0])
    b.barh([k[:30] for k in ks2[::-1]], [it[k][0] / 1e3 for k in ks2[::-1]], color=[OR if it[k][1] == "V" else DK for k in ks2[::-1]])
    b.set_xlabel("USD ribu/th (oranye = variabel)"); b.set_title("(b) OPEX tahun penuh USD %.0f ribu" % (o["opex_full"] / 1e3))
    c = ax[2]; i = 2
    parts = [("Listrik PLN", o["rev_el"][i], DK), ("Kredit karbon", o["rev_c"][i], TE), ("Jasa POME", o["rev_fee"][i], OR), ("Panas", o["rev_h"][i], RD), ("Pupuk", o["rev_f"][i], GR)]
    c.pie([p[1] for p in parts], labels=["%s\n%.0f%%" % (p[0], 100 * p[1] / o["rev"][i]) for p in parts], colors=[p[2] for p in parts],
          startangle=90, wedgeprops=dict(width=.42, ec="white"), textprops=dict(fontsize=8))
    c.set_title("(c) Bauran pendapatan th %d: USD %.2f juta" % (o["years"][i], o["rev"][i] / M))
    fig.tight_layout(); return save(fig, "g03_capex_opex.png")

def fig_cashflow(o):
    fig, a = plt.subplots(figsize=(10.5, 4.3))
    y = np.array(o["years"])
    a.bar(y, o["ebitda"] / M, color=LT, ec=TE, lw=.5, label="EBITDA", width=.7)
    a.bar(y, o["fcff"] / M, color=[RD if v < 0 else TE for v in o["fcff"]], width=.45)
    a.bar([y[0]], [0], color=TE, label="Arus kas bersih proyek (FCFF; merah = negatif)")
    a.axhline(0, c="k", lw=.7); a.set_ylabel("Arus kas tahunan (USD juta)")
    b = a.twinx(); cum = np.cumsum(o["fcff"]) / M
    b.plot(y, cum, c=OR, marker="o", ms=3, label="Kumulatif (sumbu kanan)"); b.set_ylabel("Kumulatif (USD juta)")
    b.spines["right"].set_visible(True)
    lo = min(a.get_ylim()[0], b.get_ylim()[0]); hi = max(a.get_ylim()[1], b.get_ylim()[1]); a.set_ylim(lo, hi); b.set_ylim(lo, hi)
    b.annotate("Puncak pendanaan\nUSD %.2f juta" % (o["peak_funding"] / M), (y[0], cum[0]), xytext=(y[0] + 1.5, cum[0] + .3), arrowprops=dict(arrowstyle="->"), fontsize=8)
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=8)
    a.set_xticks(y[::2]); a.set_title("Arus kas tahunan dan kumulatif proyek %d-%d (1 set 45 t TBS/jam)" % (y[0], y[-1]))
    return save(fig, "g04_arus_kas.png")

def fig_npv_tornado(o, torn, curve):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    rates, nv = curve; a = ax[0]
    a.plot(rates * 100, np.array(nv) / M, c=DK, marker="o", ms=2.5); a.axhline(0, c="k", lw=.7)
    a.scatter([o["wacc"] * 100], [o["NPV"] / M], c=RD, zorder=4); a.scatter([o["IRR"] * 100], [0], c=OR, zorder=4)
    a.annotate("WACC %s%%:\nNPV = %s" % (("%.1f" % (o["wacc"] * 100)).replace(".", ","), ("%.2f" % (o["NPV"] / M)).replace(".", ",")), (o["wacc"] * 100, o["NPV"] / M), xytext=(25, 25), textcoords="offset points", arrowprops=dict(arrowstyle="->"), fontsize=8, color=RD)
    a.annotate("IRR = %s%%" % ("%.1f" % (o["IRR"] * 100)).replace(".", ","), (o["IRR"] * 100, 0), xytext=(10, -30), textcoords="offset points", arrowprops=dict(arrowstyle="->"), fontsize=8)
    a.set_xlabel("Tingkat diskonto (%)"); a.set_ylabel("NPV (USD juta)"); a.set_title("(a) Profil NPV terhadap tingkat diskonto")
    base, res = torn; b = ax[1]
    for i, (lab, lo, hi) in enumerate(res[::-1]):
        b.barh(i, (lo - base) / M, left=base / M, color=RD); b.barh(i, (hi - base) / M, left=base / M, color=TE)
        b.text(min(lo, hi) / M - .05, i, "%.2f" % (min(lo, hi) / M), ha="right", va="center", fontsize=7.5)
        b.text(max(lo, hi) / M + .05, i, "%.2f" % (max(lo, hi) / M), ha="left", va="center", fontsize=7.5)
    b.set_yticks(range(len(res))); b.set_yticklabels([r[0] for r in res[::-1]], fontsize=8); b.axvline(base / M, c="k", lw=.8); b.axvline(0, c=GR, ls=":")
    b.set_xlabel("NPV (USD juta); variasi -20% (merah) / +20% (hijau)"); b.set_title("(b) Diagram tornado, NPV dasar %.2f" % (base / M))
    fig.tight_layout(); return save(fig, "g05_npv_tornado.png")

def fig_payback(o):
    fig, a = plt.subplots(figsize=(10.5, 4.2)); y = np.array(o["years"])
    c1 = np.cumsum(o["fcff"]) / M; c2 = np.cumsum(o["fcff"] * o["disc"]) / M
    a.axvspan(y[0] - .5, y[0] + .5, color="#eeeeee"); a.text(y[0], c1.max() * .55, "Konstruksi", ha="center", color=GR, fontsize=8)
    a.plot(y, c1, c=TE, marker="o", ms=3, label="Kumulatif arus kas (tanpa diskonto)")
    a.plot(y, c2, c=RD, marker="s", ms=3, label="Kumulatif arus kas terdiskonto (WACC %.1f%%)" % (o["wacc"] * 100))
    a.axhline(0, c="k", lw=.7)
    for pb, c, lab in ((o["PBP"], TE, "Payback %.2f th sejak COD"), (o["DPBP"], RD, "Payback terdiskonto %.2f th sejak COD")):
        if pb == pb:
            x = y[0] + pb; a.scatter([x], [0], c=OR, zorder=5, s=40)
            a.annotate(lab % pb, (x, 0), xytext=(x + .5, -1.6 if c == TE else -2.6), arrowprops=dict(arrowstyle="->"), fontsize=8)
    a.set_xlabel("Tahun kalender (COD %d)" % (y[0] + 1)); a.set_ylabel("USD juta"); a.legend(frameon=False, fontsize=8, loc="upper left")
    a.set_xticks(y[::2]); a.set_title("Kurva payback: arus kas kumulatif biasa dan terdiskonto")
    return save(fig, "g06_payback.png")

def fig_bep(o, be):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    a = ax[0]; u = np.linspace(0, 1.1, 50)
    rev = be["rev_full"] * u; cost = be["fixed"] + be["var"] * u; cost2 = cost + be["dep"] + be["intr"]
    a.plot(u * 100, rev / M, c=TE, lw=2, label="Pendapatan"); a.plot(u * 100, cost / M, c=OR, label="Biaya tunai (tetap + variabel)")
    a.plot(u * 100, cost2 / M, c=RD, ls="--", label="Biaya total (+ penyusutan + bunga)")
    for x, lab in ((be["BEP_cash"], "BEP tunai"), (be["BEP_acc"], "BEP akuntansi")):
        a.axvline(x * 100, c=GR, ls=":"); a.text(x * 100 + 1, rev.max() / M * .9 if lab == "BEP tunai" else rev.max() / M * .75, "%s\n%.1f%%" % (lab, x * 100), fontsize=8)
    a.set_xlabel("Kapasitas terpakai (%)"); a.set_ylabel("USD juta/th"); a.legend(frameon=False, fontsize=8, loc="lower right"); a.set_title("(a) Titik impas operasional (th penuh)")
    b = ax[1]
    items = [("Tarif listrik th 1-10\n(USc/kWh, sebelum F)", be["tariff1_be"], o["v"]["tariff1"]), ("Harga karbon\n(USD/tCO2e)", be["p_carbon_be"], o["v"]["p_carbon"]),
             ("Produksi energi\n(% dasar)", be["emult_be"] * 100, 100.0), ("CAPEX\n(% dasar)", be["capex_be"] * 100, 100.0)]
    x = np.arange(len(items))
    b.bar(x - .18, [i[2] for i in items], .36, color=LT, ec=TE, label="Nilai dasar"); b.bar(x + .18, [i[1] for i in items], .36, color=OR, label="Nilai impas (NPV = 0)")
    for k, (n_, be_, bs) in enumerate(items): b.text(k + .18, be_ + 1, "%.1f" % be_, ha="center", fontsize=8)
    b.set_xticks(x); b.set_xticklabels([i[0] for i in items], fontsize=8); b.legend(frameon=False, fontsize=8); b.set_title("(b) Nilai impas NPV = 0 per variabel")
    fig.tight_layout(); return save(fig, "g07_bep.png")

def fig_mc(o, mc):
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.9))
    N = mc["NPV"] / M; a = ax[0]
    a.hist(N, bins=50, color=TE, alpha=.85); a.axvline(0, c="k"); a.axvline(np.median(N), c=OR, ls="--")
    p = (N > 0).mean()
    a.set_title("(a) Distribusi NPV (N = %d)" % len(N)); a.set_xlabel("NPV (USD juta)")
    a.text(.02, .95, "P(NPV>0) = %.0f%%\nP10 %.2f | P50 %.2f | P90 %.2f" % (p * 100, *np.percentile(N, [10, 50, 90])), transform=a.transAxes, va="top", fontsize=8)
    b = ax[1]; I = np.sort(mc["IRR"][np.isfinite(mc["IRR"])]) * 100
    b.plot(I, np.linspace(0, 1, len(I)), c=DK); b.axvline(o["wacc"] * 100, c=RD, ls=":"); b.text(o["wacc"] * 100 + .3, .1, "WACC", color=RD, fontsize=8)
    b.set_xlim(max(-5, I.min() if len(I) else -5), I.max() + 1); b.set_xlabel("IRR proyek (%%); P(IRR > WACC) = %.0f%%" % (100 * (I > o["wacc"] * 100).mean())); b.set_ylabel("Peluang kumulatif"); b.set_title("(b) Kurva S IRR"); b.grid(alpha=.2)
    c = ax[2]; sp = sorted(mc["spearman"].items(), key=lambda kv: abs(kv[1]))
    LAB = dict(emult="Produksi energi", capex="CAPEX", opex="OPEX", p_carbon="Harga karbon", F_loc="Faktor lokasi F", avail="Ketersediaan",
               p_heat="Harga panas", heat_util="Pemanfaatan panas", r_debt="Bunga utang", infl="Inflasi")
    c.barh([LAB[k] for k, v in sp], [v for k, v in sp], color=[TE if v > 0 else RD for k, v in sp]); c.axvline(0, c="k", lw=.7)
    c.set_xlabel("Korelasi Spearman terhadap NPV"); c.set_title("(c) Penggerak ketidakpastian")
    fig.tight_layout(); return save(fig, "g08_monte_carlo.png")

def fig_fleet(fl):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.0)); y = np.array(fl["years"])
    a = ax[0]; a.bar(y, fl["sets_op"], color=TE, label="Set beroperasi"); a.bar(y, fl["sets_new"], bottom=fl["sets_op"], color=OR, label="Set baru (konstruksi)")
    a.set_ylabel("jumlah set"); b = a.twinx(); b.plot(y, fl["E"], c=DK, marker="o", ms=3, label="Listrik ke PLN (GWh/th)"); b.set_ylabel("GWh/th"); b.spines["right"].set_visible(True)
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left")
    a.set_title("(a) Rencana penggelaran armada (SOM %d set)" % sum(F.ROLL.values()))
    c = ax[1]; c.bar(y, fl["rev"] / M, color=LT, ec=TE, label="Pendapatan"); c.bar(y, fl["fcff_co"] / M, color=[RD if v < 0 else TE for v in fl["fcff_co"]], width=.5, label="FCFF perusahaan")
    d = c.twinx(); d.plot(y, np.cumsum(fl["fcff_co"]) / M, c=OR, marker="o", ms=3, label="Kumulatif"); d.spines["right"].set_visible(True); d.set_ylabel("Kumulatif (USD juta)")
    lo = min(c.get_ylim()[0], d.get_ylim()[0]); hi = max(c.get_ylim()[1], d.get_ylim()[1]); c.set_ylim(lo, hi); d.set_ylim(lo, hi)
    h1, l1 = c.get_legend_handles_labels(); h2, l2 = d.get_legend_handles_labels(); c.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left")
    c.set_ylabel("USD juta/th"); c.set_title("(b) Perusahaan: NPV %.1f juta, IRR %.1f%%, puncak dana %.1f juta" % (fl["NPV"] / M, fl["IRR"] * 100, fl["peak"] / M))
    fig.tight_layout(); return save(fig, "g09_armada.png")

def fig_scenarios(sc):
    fig, a = plt.subplots(figsize=(9, 3.6))
    names = [s[0] for s in sc]; npv_ = [s[1]["NPV"] / M for s in sc]; irr_ = [s[1]["IRR"] * 100 for s in sc]
    x = np.arange(len(sc)); a.bar(x, npv_, color=[TE if v > 0 else RD for v in npv_]); a.axhline(0, c="k", lw=.7)
    for i, (n_, ir) in enumerate(zip(npv_, irr_)): a.text(i, n_ + (.08 if n_ >= 0 else -.25), "IRR %.1f%%" % ir, ha="center", fontsize=8)
    a.set_xticks(x); a.set_xticklabels(names, fontsize=8); a.set_ylabel("NPV (USD juta)"); a.set_title("Skenario model bisnis & skala set")
    return save(fig, "g10_skenario.png")
