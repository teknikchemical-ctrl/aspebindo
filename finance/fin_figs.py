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
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.1), gridspec_kw=dict(width_ratios=[1.25, 1]))
    a = ax[0]; rows = mk["rows"]; cols = [DK, TE, OR, RD]
    mx = rows[0]["sets"]
    for i, (rw, c) in enumerate(zip(rows, cols)):
        w = max(rw["sets"] / mx, .06); y = len(rows) - 1 - i
        a.barh(y, w, left=(1 - w) / 2, color=c, height=.78)
        a.text(.5, y, "%s: %s set | %s MWe | USD %s jt/th" % (rw["level"], "{:,.0f}".format(rw["sets"]).replace(",", "."), "{:,.0f}".format(rw["MW"]).replace(",", "."),
                                                          "{:,.0f}".format(rw["rev"] / M).replace(",", ".")), ha="center", va="center", color="white" if w > .62 else "k", fontsize=8, fontweight="bold",
               bbox=None if w > .62 else dict(fc="white", ec="none", alpha=.85, pad=1.5))
    a.set_xlim(0, 1); a.axis("off"); a.set_title("(a) Corong pasar bottom-up (1 set per PKS; pendapatan rata-rata 20 th)")
    a.text(.5, -.75, "SOM = %.0f%% SAM; %.0f%% laju bangun PLTBg nasional (9 MW/th) [R3]" % (mk["share"] * 100, mk["build_share"] * 100), ha="center", fontsize=8)
    b = ax[1]
    names = [p for p, n in MK.PROV]; n_ = np.array([n for p, n in MK.PROV])
    sam = n_ * (1 - MK.SH_CAPTURED) * MK.SH_SIZE * MK.SH_DIESEL
    x = np.arange(len(names))
    b.bar(x - .2, n_, .4, color=LT, ec=TE, label="Jumlah PKS (estimasi [R3])")
    b.bar(x + .2, sam, .4, color=TE, label="SAM: 30-60 t/jam, tanpa metana, bergantung diesel")
    b.set_xticks(x); b.set_xticklabels(names, rotation=30, ha="right"); b.set_ylabel("jumlah PKS")
    b.set_title("(b) Sebaran PKS & pasar sasaran per provinsi"); b.legend(frameon=False, fontsize=7.5)
    return save(fig, "g01_pasar.png")

def fig_mill(c, wf, fw):
    """Model Keputusan PKS: biaya terlevelisasi A-D + langkah A -> D"""
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4), gridspec_kw=dict(width_ratios=[1, 1.35]))
    a = ax[0]; L = ["A Status quo\nkolam", "B Kolam tertutup\nmilik PKS", "C Tangki\nmilik PKS", "D Layanan BOO\n(produk ini)"]
    vals = [c[o]["per_t"] for o in "ABCD"]; cols = [RD, GR, GR, DK]
    a.bar(range(4), vals, color=cols, width=.62)
    for i, o in enumerate("ABCD"):
        a.text(i, vals[i] + .06, "%.2f" % vals[i], ha="center", fontsize=8.5, fontweight="bold")
        if c[o]["capex"] > 0: a.text(i, vals[i] / 2, "CAPEX PKS\nUSD %.1f jt" % (c[o]["capex"] / M), ha="center", color="white", fontsize=7.5)
    a.text(3, vals[3] / 2, "CAPEX PKS\n0", ha="center", color="white", fontsize=7.5)
    a.set_xticks(range(4)); a.set_xticklabels(L, fontsize=7.8); a.set_ylabel("Biaya POME bagi PKS (USD 2026 / t TBS, 20 th)")
    a.set_title("(a) D %.0f%% lebih murah dari kolam (segmen S3)" % (c["saving_D_vs_A_pct"] * 100))
    b = ax[1]; run_ = 0.0
    for i, (lab, v) in enumerate(wf):
        if i == 0 or i == len(wf) - 1:
            b.bar(i, v, color=RD if i == 0 else DK, width=.65); b.text(i, v + .06, "%.2f" % v, ha="center", fontsize=8); run_ = v
        else:
            b.bar(i, v, bottom=run_, color=TE if v < 0 else OR, width=.65)
            b.text(i, max(run_, run_ + v) + .06, "%+.2f" % v, ha="center", fontsize=7.5); run_ += v
    b.set_xticks(range(len(wf))); b.set_xticklabels([w[0] for w in wf], rotation=32, ha="right", fontsize=7.5)
    b.set_ylim(0, max(w[1] for w in wf) * 1.15); b.set_ylabel("USD 2026 / t TBS"); b.set_title("(b) Dari kolam ke layanan BOO; jendela fee USD %.2f-%.2f/t TBS" % (fw["fee_min"], fw["fee_max"]))
    fig.tight_layout(); return save(fig, "g11_keputusan_pks.png")

def fig_segments(seg, fee):
    fig, a = plt.subplots(figsize=(10.5, 3.8))
    for i, sg in enumerate(seg):
        lo, hi = sg["fee_min"], sg["fee_max"]; ok = hi > lo
        a.plot([lo, hi], [i, i], c=TE if ok else RD, lw=7 if ok else 2.5, solid_capstyle="butt", alpha=.9)
        a.scatter([lo], [i], marker="|", s=200, c="k"); a.scatter([hi], [i], marker="|", s=200, c="k")
        a.text(max(lo, hi) + .06, i, ("jendela %.2f-%.2f" % (lo, hi)) if ok else ("TANPA jendela: pengembang butuh %.2f, PKS maks %.2f" % (lo, hi)), va="center", fontsize=7.8)
    a.axvline(fee, c=OR, ls="--"); a.text(fee + .04, -.55, "fee dasar %.2f" % fee, color=OR, fontsize=8, ha="left")
    a.set_yticks(range(len(seg))); a.set_yticklabels([sg["name"] for sg in seg], fontsize=8); a.invert_yaxis()
    a.set_xlabel("Fee jasa POME (USD/t TBS): kiri = minimum pengembang (NPV = 0), kanan = maksimum PKS (biaya = kolam)")
    a.set_xlim(min(-0.5, min(sg["fee_min"] for sg in seg) - .2), max(sg["fee_max"] for sg in seg) + 2.2)
    a.set_title("Jendela kesepakatan per segmen PKS: pasar sasaran = PKS bergantung diesel")
    fig.tight_layout(); return save(fig, "g12_segmen.png")

def fig_compet(comp):
    fig, a = plt.subplots(figsize=(11, 4.6))
    crit = [c for c, _ in MK.CRIT]; Z = np.array([c["scores"] for c in comp])
    im = a.imshow(Z, cmap="RdYlGn", vmin=1, vmax=5, aspect="auto")
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]): a.text(j, i, "%.1f" % Z[i, j], ha="center", va="center", fontsize=7.5)
    import textwrap
    a.set_xticks(range(len(crit))); a.set_xticklabels(["%s\n(bobot %.0f%%)" % ("\n".join(textwrap.wrap(c.split(" (")[0], 16)), w * 100) for c, w in MK.CRIT], fontsize=7)
    a.set_yticks(range(len(comp))); a.set_yticklabels(["%s  [%.2f]" % (c["name"], c["total"]) for c in comp], fontsize=7.8)
    a.set_title("Matriks pesaing berbobot (5 = terbaik bagi PKS) - [skor tertimbang]")
    fig.colorbar(im, ax=a, fraction=.025); fig.tight_layout(); return save(fig, "g13_pesaing.png")

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
    c.set_xlabel("Skor bersih (peluang - ancaman); total %+d" % sum(vals_)); c.set_title("(c) Skor bersih PESTLE (%d faktor)" % len(MK.PESTLE))
    d = fig.add_subplot(2, 2, 4)
    for (n_, at, ab, sz), col in zip(MK.SEGMENTS, (DK, TE, OR, BL, "#7a5c9e", RD, GR, "#555555")):
        d.scatter(ab, at, s=sz, color=col, zorder=3); d.annotate(n_, (ab, at), xytext=(6, 4), textcoords="offset points", fontsize=7.5)
    d.axhline(3, c=GR, lw=.6, ls=":"); d.axvline(3, c=GR, lw=.6, ls=":")
    d.set_xlim(1.5, 5); d.set_ylim(1.5, 5); d.set_xlabel("Kemampuan memenangkan pasar (1-5)"); d.set_ylabel("Daya tarik pasar (1-5)")
    d.set_title("(d) Daya tarik dan kemampuan menang"); d.grid(alpha=.2)
    fig.tight_layout(); return save(fig, "g02_porter_pestle.png")

def fig_capex_opex(o):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.2))
    rows = o["capex_rows"]
    grp = {}
    for g, n, q, u, c, t, b in rows:
        key = n.split(" ")[0] if g == "PEC" else g.title()
        if g == "PEC":
            key = ("Tangki GFS" if ("Reaktor" in n or "TK-101" in n) else "Skid kontak PM-4" if "PM-4" in n else
                   "Genset PM-8" if "PM-8" in n else "Skid proses PM-1/5/6/7/9/10" if n.startswith("PM-") else "Listrik, I&C, pipa, PLN")
        grp[key] = grp.get(key, 0) + t
    ks = sorted(grp, key=lambda k: -grp[k])
    a = ax[0]; a.barh(ks[::-1], [grp[k] / M for k in ks[::-1]], color=TE)
    for i, k in enumerate(ks[::-1]): a.text(grp[k] / M + .02, i, "%.2f" % (grp[k] / M), va="center", fontsize=8)
    a.set_xlabel("USD juta (harga 2026)"); a.set_title("(a) CAPEX (FCI USD %.2f juta, 2026)" % (o["fci26"] / M))
    b = ax[1]; it = o["opex_items"]; ks2 = sorted(it, key=lambda k: -it[k][0])
    b.barh([k[:30] for k in ks2[::-1]], [it[k][0] / 1e3 for k in ks2[::-1]], color=[OR if it[k][1] == "V" else DK for k in ks2[::-1]])
    b.set_xlabel("USD ribu/th (oranye = variabel)"); b.set_title("(b) OPEX tahun penuh USD %.0f ribu (+ MRV karbon)" % ((o["opF"] + o["opV"]) / 1e3))
    c = ax[2]; i = 2
    i = 3
    parts = [("Jasa pengolahan POME", o["rev_fee"][i], OR), ("Listrik ke PLN", o["rev_exp"][i], DK), ("Listrik ke PKS (ganti solar)", o["rev_cap"][i], BL), ("Kredit karbon", o["rev_c"][i], TE)]
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
    a.set_xticks(y[::2]); a.set_title("Arus kas tahunan dan kumulatif proyek %d-%d (1 set 60 t TBS/jam)" % (y[0], y[-1]))
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
    rev = be["fee"] + be["vol"] * u; cost = be["fixed"] + be["var"] * u; cost2 = cost + be["dep"] + be["intr"]
    a.plot(u * 100, rev / M, c=TE, lw=2, label="Pendapatan (jasa tetap + energi/karbon)"); a.plot(u * 100, cost / M, c=OR, label="Biaya tunai (tetap + variabel)")
    a.plot(u * 100, cost2 / M, c=RD, ls="--", label="Biaya total (+ penyusutan + bunga)")
    for x, lab in ((be["BEP_cash"], "BEP tunai"), (be["BEP_acc"], "BEP akuntansi")):
        a.axvline(x * 100, c=GR, ls=":"); a.text(x * 100 + 1, rev.max() / M * .9 if lab == "BEP tunai" else rev.max() / M * .75, "%s\n%.1f%%" % (lab, x * 100), fontsize=8)
    a.set_xlabel("Produksi biogas/energi terhadap dasar (%)"); a.set_ylabel("USD juta/th"); a.legend(frameon=False, fontsize=8, loc="lower right"); a.set_title("(a) Titik impas operasional (th penuh)")
    b = ax[1]
    items = [("Jasa POME\n(USD/t TBS x10)", be["fee_be"] * 10, o["v"]["fee_ffb"] * 10), ("Tarif PLN th 1-10\n(USc/kWh, sebelum F)", be["tariff1_be"], o["v"]["tariff1"]),
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
    a.text(.02, .95, "P(NPV>0) = %.0f%%\nP10 %.2f | P50 %.2f | P90 %.2f" % (p * 100, *np.percentile(N, [10, 50, 90])), transform=a.transAxes, va="top", fontsize=8, bbox=dict(fc="white", ec="none", alpha=.85))
    b = ax[1]; I = np.sort(np.where(np.isfinite(mc["IRR"]), mc["IRR"], -0.5)) * 100
    b.plot(I, np.linspace(0, 1, len(I)), c=DK); b.axvline(o["wacc"] * 100, c=RD, ls=":"); b.text(o["wacc"] * 100 + .3, .1, "WACC", color=RD, fontsize=8)
    b.set_xlim(max(-5, I.min() if len(I) else -5), I.max() + 1); b.set_xlabel("IRR proyek (%%); P(IRR > WACC) = %.0f%%" % (100 * (I > o["wacc"] * 100).mean())); b.set_ylabel("Peluang kumulatif"); b.set_title("(b) Kurva S IRR"); b.grid(alpha=.2)
    c = ax[2]; sp = sorted(mc["spearman"].items(), key=lambda kv: abs(kv[1]))
    LAB = dict(emult="Produksi energi", capex="CAPEX", opex="OPEX", p_carbon="Harga karbon", F_loc="Faktor lokasi F", avail="Ketersediaan",
               tier="Tier tarif >1 MW", fee="Jasa POME", ramp1="Ramp-up th 1", cer_ratio="Rasio kredit", r_debt="Bunga utang", infl="Inflasi", util="Faktor beban PKS")
    c.barh([LAB[k] for k, v in sp], [v for k, v in sp], color=[TE if v > 0 else RD for k, v in sp]); c.axvline(0, c="k", lw=.7)
    c.set_xlabel("Korelasi Spearman terhadap NPV"); c.set_title("(c) Penggerak ketidakpastian")
    fig.tight_layout(); return save(fig, "g08_monte_carlo.png")

def fig_fleet(fl):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.0)); y = np.array(fl["years"])
    a = ax[0]; a.bar(y, fl["sets_op"], color=TE, label="Set beroperasi"); a.bar(y, fl["sets_new"], bottom=fl["sets_op"], color=OR, label="Set baru (konstruksi)")
    a.set_ylabel("jumlah set"); b = a.twinx(); b.plot(y, fl["E"], c=DK, marker="o", ms=3, label="Listrik (GWh/th)"); b.set_ylabel("GWh/th"); b.spines["right"].set_visible(True)
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left")
    a.set_ylim(0, sum(F.ROLL.values()) * 1.25); a.set_title("(a) Rencana penggelaran armada (SOM %d set)" % sum(F.ROLL.values()))
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
    for i, (n_, ir) in enumerate(zip(npv_, irr_)): a.text(i, n_ + (.08 if n_ >= 0 else -.25), ("IRR %.1f%%" % ir) if np.isfinite(ir) else "tanpa IRR", ha="center", fontsize=8)
    a.set_xticks(x); a.set_xticklabels(names, fontsize=8); a.set_ylabel("NPV (USD juta)"); a.set_title("Skenario model bisnis & skala set")
    return save(fig, "g10_skenario.png")
