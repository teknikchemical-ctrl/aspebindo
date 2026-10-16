# Gambar gaya laporan konsultan untuk slide 1, 7-10 (dibaca dari deck_data.json). Jalankan dari akar repo.
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
D = json.load(open("deck/deck_data.json")); K = D["keu"]; OUT = "deck/img/"
NAVY, ROYAL, TEAL, GREEN, RED, AMB, MID, INK, SL = "#0C2464", "#1F4E9E", "#2B9FC8", "#3E8E41", "#C8452F", "#E0A526", "#6898C8", "#14213D", "#5B6B7F"
plt.rcParams.update({"font.family": "Carlito", "font.size": 8, "axes.edgecolor": "#9AA9BA", "axes.linewidth": 0.6, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "xtick.major.width": .5, "ytick.major.width": .5, "xtick.major.size": 2.5, "ytick.major.size": 2.5})
def idn(x, d=0): s = f"{abs(x):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."); return ("−" if x < 0 and round(abs(x), d) != 0 else "") + s
def clean(ax, left=True):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
def save(fig, name): fig.savefig(OUT + name, dpi=260, facecolor="white"); plt.close(fig)

# ---------- F1 CAPEX: batang + cincin
cc = K["capex_cat"]; FCI26 = K["FCI26"]
g = {"Tangki GFS (reaktor, umpan, efluen, ekualisasi)": cc["Tangki reaktor GFS"] + cc["Tangki umpan, efluen, ekualisasi"],
     "Genset biogas 2 × 800 kWe": cc["Genset biogas"],
     "Skid proses (praolah, kontak, dosing, lumpur, panas)": sum(cc[k] for k in ["Praolah (PM-1)", "Skid kontak (degasser + lamella)", "Dosing dan pompa", "Screw press dan lumpur", "Pemulih panas dan menara"]),
     "Pemurnian biogas, penampung, flare": cc["Pemurnian biogas (PM-6)"] + cc["Penampung gas dan flare"],
     "Sipil, angkut, ereksi": cc["Sipil, angkut, ereksi"], "Perpipaan, listrik, SCADA": cc["Perpipaan, listrik, SCADA"],
     "Pipa lokasi dan interkoneksi PLN": cc["Pipa lokasi dan interkoneksi PLN"], "Rekayasa, izin, start-up": cc["Rekayasa, izin, start-up"], "Kontingensi 20%": cc["Kontingensi 20%"]}
tot = sum(g.values()); items = sorted(g.items(), key=lambda x: -x[1])
colr = {"Tangki GFS": TEAL, "Genset": NAVY, "Skid": ROYAL, "Pemurnian": ROYAL, "Sipil": AMB, "Perpipaan": AMB, "Pipa lokasi": AMB, "Rekayasa": RED, "Kontingensi": RED}
def cof(n): return next(v for k, v in colr.items() if n.startswith(k))
fig = plt.figure(figsize=(6.15, 2.0)); ax = fig.add_axes([0.40, 0.19, 0.30, 0.79])
nm = [i[0] for i in items]; vs = [i[1] / 1000 for i in items]
ax.barh(range(len(nm)), vs, color=[cof(n) for n in nm], height=0.68); ax.set_yticks(range(len(nm))); ax.set_yticklabels(nm, fontsize=7.2); ax.invert_yaxis(); clean(ax)
for i, v in enumerate(vs): ax.text(v + 12, i, f"{idn(v)} ({idn(v*1000/tot*100,1)}%)", va="center", fontsize=7)
ax.set_xlim(0, 1500); ax.set_xticks([0, 500, 1000]); ax.set_xlabel("USD ribu (2026)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
ax2 = fig.add_axes([0.745, 0.3, 0.25, 0.68]); grp = {"Peralatan": [TEAL, g["Tangki GFS (reaktor, umpan, efluen, ekualisasi)"] + g["Skid proses (praolah, kontak, dosing, lumpur, panas)"] + g["Pemurnian biogas, penampung, flare"]], "Genset": [NAVY, g["Genset biogas 2 × 800 kWe"]],
       "Instalasi dan sipil": [AMB, g["Sipil, angkut, ereksi"] + g["Perpipaan, listrik, SCADA"] + g["Pipa lokasi dan interkoneksi PLN"]], "Rekayasa dan kontingensi": [RED, g["Rekayasa, izin, start-up"] + g["Kontingensi 20%"]]}
ax2.pie([v[1] for v in grp.values()], colors=[v[0] for v in grp.values()], startangle=90, counterclock=False, wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.5), radius=1.0)
ax2.text(0, 0.1, "USD " + idn(tot / 1e6, 2), ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY); ax2.text(0, -0.2, "juta", ha="center", va="center", fontsize=7.5, color=SL)
ax2.legend([plt.Rectangle((0, 0), 1, 1, color=v[0]) for v in grp.values()], [f"{k} {idn(v[1]/tot*100,0)}%" for k, v in grp.items()], loc="upper center", bbox_to_anchor=(0.5, 0.02), fontsize=6.4, frameon=False, ncol=1, handlelength=.8, labelspacing=.2)
save(fig, "f_capex.png")

# ---------- F2 OPEX: batang + cincin luar (kelompok) dan dalam (variabel/tetap)
oi = K["opex_items"]
ox = [("Staf operasi (10 orang)", oi["Staf operasi (10 orang)"]["v"], "F", "Staf dan admin."), ("O&M genset (kontrak)", oi["O&M genset (kontrak)"]["v"], "V", "Pemeliharaan"), ("Perawatan proses", oi["Perawatan peralatan proses"]["v"], "F", "Pemeliharaan"),
      ("Bahan kimia", oi["Bahan kimia (polimer, karbon aktif, NaOH)"]["v"], "V", "Bahan"), ("Administrasi dan SCADA", oi["Administrasi & SCADA jarak jauh"]["v"], "F", "Staf dan admin."), ("Asuransi", oi["Asuransi"]["v"], "F", "Asuransi dan lahan"), ("MRV karbon", 12000.0, "F", "Staf dan admin."), ("Sewa lahan", oi["Sewa lahan plot di PKS"]["v"], "F", "Asuransi dan lahan")]
ox.sort(key=lambda x: -x[1]); T = sum(x[1] for x in ox); gc = {"Staf dan admin.": ROYAL, "Pemeliharaan": TEAL, "Bahan": GREEN, "Asuransi dan lahan": AMB}
fig = plt.figure(figsize=(6.15, 2.0)); ax = fig.add_axes([0.22, 0.19, 0.34, 0.79])
ax.barh(range(len(ox)), [x[1] / 1000 for x in ox], color=[gc[x[3]] for x in ox], height=0.68); ax.set_yticks(range(len(ox))); ax.set_yticklabels([x[0] for x in ox], fontsize=7.2); ax.invert_yaxis(); clean(ax)
for i, x in enumerate(ox): ax.text(x[1] / 1000 + 3, i, f"{idn(x[1]/1000,1)} ({idn(x[1]/T*100,1)}%)", va="center", fontsize=7)
ax.set_xlim(0, 200); ax.set_xticks([0, 50, 100]); ax.set_xlabel("USD ribu per tahun (2026)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
ax2 = fig.add_axes([0.56, 0.04, 0.27, 0.94]); og = {}
for n, v, t, gk in ox: og[gk] = og.get(gk, 0) + v
fx = sum(x[1] for x in ox if x[2] == "F"); vr = T - fx
ax2.pie(list(og.values()), colors=[gc[k] for k in og], radius=1.0, startangle=90, counterclock=False, wedgeprops=dict(width=0.3, edgecolor="white", linewidth=1.5), autopct=lambda p: f"{p:.0f}%", pctdistance=0.85, textprops=dict(color="white", fontsize=6.8, fontweight="bold"))
ax2.pie([fx, vr], colors=["#9AA9BA", "#5B6B7F"], radius=0.68, startangle=90, counterclock=False, wedgeprops=dict(width=0.26, edgecolor="white", linewidth=1.5), autopct=lambda p: f"{p:.0f}%", pctdistance=0.77, textprops=dict(color="white", fontsize=6.8, fontweight="bold"))
ax2.text(0, 0.07, "USD " + idn(T / 1000), ha="center", va="center", fontsize=8.5, fontweight="bold", color=NAVY); ax2.text(0, -0.13, "ribu/tahun", ha="center", va="center", fontsize=6.8, color=SL)
hd = [plt.Rectangle((0, 0), 1, 1, color=v) for v in list(gc.values()) + ["#9AA9BA", "#5B6B7F"]]
fig.legend(hd, [f"{k}: {idn(og.get(k,0)/1000)}" for k in gc] + [f"Tetap: {idn(fx/1000)}", f"Variabel: {idn(vr/1000)}"], loc="center left", bbox_to_anchor=(0.815, 0.5), bbox_transform=fig.transFigure, fontsize=6.3, frameon=False, handlelength=.8, labelspacing=.3)
save(fig, "f_opex.png")

# ---------- F3 titik impas (BEP)
bs = K["bep_series"]; u = np.array([b["util"] for b in bs]) * 100; rev = np.array([b["rev"] for b in bs]) / 1e3; opx = np.array([b["opex"] for b in bs]) / 1e3; tc = np.array([b["tc"] for b in bs]) / 1e3
fig = plt.figure(figsize=(4.0, 1.88)); ax = fig.add_axes([0.12, 0.3, 0.85, 0.67]); clean(ax); ax.set_ylim(0, 1850)
ax.plot(u, rev, color=GREEN, lw=2, label="Pendapatan"); ax.plot(u, opx, color=SL, lw=1.6, label="Biaya tunai (OPEX)"); ax.plot(u, tc, color=RED, lw=2, label="Biaya total (+ penyusutan + bunga)")
ax.fill_between(u, rev, tc, where=rev >= tc, color=GREEN, alpha=.12, lw=0); ax.fill_between(u, rev, tc, where=rev < tc, color=RED, alpha=.07, lw=0)
for x, lab, dy in [(K["bep_util_acc"] * 100, "impas akuntansi", 1), (K["bep_util_npv"] * 100, "impas NPV", 2)]:
    y = np.interp(x, u, rev); ax.plot(x, y, "o", ms=6, color=AMB, mec="white", mew=.8, zorder=5); ax.annotate(f"{lab}\n{idn(x,0)}% beban", (x, y), xytext=((28, 1250) if dy == 1 else (46, 1560)), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=.7), ha="center")
ax.axvline(75, color=NAVY, ls=":", lw=1); ax.text(74.0, 60, "asumsi dasar 75%", fontsize=6.8, color=NAVY, rotation=90, va="bottom", ha="right")
ax.set_xlabel("Beban PKS (% kapasitas nameplate)", fontsize=7.2, labelpad=1); ax.set_ylabel("USD ribu per tahun", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7); ax.legend(fontsize=6.3, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=3, handlelength=1.2, borderpad=0, columnspacing=.9)
save(fig, "f_bep.png")

# ---------- F4 payback (gaya contoh)
yrs = K["years"]; cf = K["cf"]; cum = np.array(cf["cum"]) / 1e6; cumd = np.array(cf["cumd"]) / 1e6
fig = plt.figure(figsize=(4.6, 1.88)); ax = fig.add_axes([0.1, 0.2, 0.88, 0.74]); clean(ax)
ax.axvspan(2026.5, 2027.5, color="#EEF2F6"); ax.text(2027, 6.3, "Konstruksi", fontsize=6.8, color=SL, ha="center")
ax.plot(yrs, cum, "-o", color=TEAL, lw=2, ms=3, label="Kumulatif arus kas (tanpa diskonto)"); ax.plot(yrs, cumd, "-s", color=RED, lw=2, ms=3, label=f"Kumulatif arus kas terdiskonto ({idn(K['WACC']*100,1)}%)"); ax.axhline(0, color="k", lw=.8)
def cross(a):
    for i in range(1, len(a)):
        if a[i - 1] < 0 <= a[i]: return yrs[i - 1] + (-a[i - 1]) / (a[i] - a[i - 1])
px, pd_ = cross(cum), cross(cumd)
ax.plot(px, 0, "o", ms=8, color=AMB, mec="white", zorder=6); ax.annotate(f"Payback {idn(K['PBP'],1)} tahun\nsejak operasi 2028 (±{int(round(px))})", (px, 0), xytext=(2031.2, 1.2), fontsize=7, color=NAVY, ha="center", arrowprops=dict(arrowstyle="-|>", color="k", lw=.7))
if pd_: ax.plot(pd_, 0, "o", ms=8, color=AMB, mec="white", zorder=6); ax.annotate(f"Payback terdiskonto\n{idn(K['DPBP'],1)} tahun", (pd_, 0), xytext=(pd_ - 1.0, -5.6), fontsize=7, color=NAVY, ha="center", arrowprops=dict(arrowstyle="-|>", color="k", lw=.7))
i0 = int(np.argmin(cum)); ax.annotate(f"Puncak dana\n−{idn(abs(cum[i0]),1)}", (yrs[i0], cum[i0]), xytext=(2029.0, cum[i0] - 0.2), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color="k", lw=.7), va="center")
ax.set_ylim(-8, 8); ax.set_xticks(yrs[::2]); ax.tick_params(labelsize=7); ax.set_ylabel("USD juta", fontsize=7.2, labelpad=1); ax.set_xlabel("Tahun kalender (operasi 2028–2047)", fontsize=7.2, labelpad=1); ax.legend(fontsize=6.8, frameon=False, loc="upper left", bbox_to_anchor=(0.12, 1.0), borderpad=0)
save(fig, "f_payback.png")

# ---------- F5 pasar: lingkaran bersarang + provinsi
P = D["pasar"]; r = P["rows"]
fig = plt.figure(figsize=(4.1, 2.35)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 4.1); ax.set_ylim(0, 2.35); ax.axis("off"); ax.set_aspect("equal")
cx = 1.2
for rad, col, y in [(1.12, NAVY, 1.17), (0.8, ROYAL, 0.85), (0.5, TEAL, 0.55), (0.24, AMB, 0.29)]: ax.add_patch(Circle((cx, y), rad, fc=col, ec="white", lw=1.8))
lab = [("TAM", r[0], 2.0), ("SAM luas", r[1], 1.48), ("SAM", r[2], 0.9), ("SOM", r[3], 0.29)]
ax.text(cx, 1.97, f"TAM  {idn(r[0]['sets'])} set", color="white", ha="center", fontsize=8, fontweight="bold"); ax.text(cx, 1.78, f"USD {idn(r[0]['rev']/1e6)} juta/th", color="white", ha="center", fontsize=6.6)
ax.text(cx, 1.40, f"SAM luas  {idn(r[1]['sets'])}", color="white", ha="center", fontsize=7.6, fontweight="bold"); ax.text(cx, 1.24, f"USD {idn(r[1]['rev']/1e6)} juta/th", color="white", ha="center", fontsize=6.4)
ax.text(cx, 0.78, f"SAM  {idn(r[2]['sets'])}", color="white", ha="center", fontsize=7.6, fontweight="bold"); ax.text(cx, 0.62, f"USD {idn(r[2]['rev']/1e6)} jt/th", color="white", ha="center", fontsize=6.2)
ax.text(cx, 0.29, f"SOM\n{idn(r[3]['sets'])}", color=INK, ha="center", va="center", fontsize=7, fontweight="bold")
notes = [(2.35, 1.95, "Seluruh PKS tanpa penangkap metana\n(1.150 pabrik ≈ 756 set setara)"), (2.35, 1.38, "Ukuran 30–60 t/jam, Sumatera dan\nKalimantan: 636 set"), (2.35, 0.82, "Lolos filter solar ≥ 2 L/t, jaringan 20 kV\n≤ 2 km, bebas program grup (hipotesis)"), (2.35, 0.26, "Sasaran armada 2034: 10 set\n= 17% SAM")]
for (x, y, t), col in zip(notes, [NAVY, ROYAL, TEAL, AMB]):
    ax.text(x, y, t, fontsize=6.9, va="center", color=INK); ax.plot([x - .06, x - .06], [y - .13, y + .13], color=col, lw=2.5)
save(fig, "f_pasar.png")
pv = P["prov"]; fig = plt.figure(figsize=(4.0, 2.35)); ax = fig.add_axes([0.2, 0.14, 0.72, 0.8]); clean(ax)
ax.barh(range(len(pv)), [p[1] for p in pv], color=[NAVY if i < 3 else (TEAL if i < 7 else MID) for i in range(len(pv))], height=0.68); ax.set_yticks(range(len(pv))); ax.set_yticklabels([p[0] for p in pv], fontsize=7.4); ax.invert_yaxis()
for i, p in enumerate(pv): ax.text(p[1] + 4, i, str(p[1]), va="center", fontsize=7.2)
ax.set_xlim(0, 310); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.text(0.98, 0.05, f"Σ {idn(sum(p[1] for p in pv))} PKS (data provinsi)", transform=ax.transAxes, ha="right", fontsize=7.4, color=NAVY, fontweight="bold")
save(fig, "f_prov.png")

# ---------- F6 NPV per skenario
sc = K["scen"]; pick = [("Kasus dasar", 0), ("Solar tergantikan 3,0 L/t", 1), ("CAPEX −15% (hasil kuotasi)", 9), ("Unit ke-10 (kurva belajar)", 11), ("Karbon USD 8,3/t", 6), ("Solar tergantikan 1,0 L/t", 3), ("Tarif excess power 7,44 USc", 4), ("Modul 45 t/jam", 13), ("Modul 30 t/jam", 12), ("Tanpa jasa POME", 7), ("PKS terisolasi (tanpa ekspor)", 8)]
pick.sort(key=lambda x: -sc[x[1]]["NPV"]); vals = [sc[i]["NPV"] / 1e6 for _, i in pick]
fig = plt.figure(figsize=(4.6, 2.35)); ax = fig.add_axes([0.40, 0.16, 0.55, 0.82]); clean(ax)
ax.barh(range(len(pick)), vals, color=[NAVY if i == 0 and False else (GREEN if v >= 0 else RED) for i, v in enumerate(vals)], height=0.66)
for i, (n, j) in enumerate(pick):
    if j == 0: ax.get_children()[i].set_color(NAVY)
ax.set_yticks(range(len(pick))); ax.set_yticklabels([p[0] for p in pick], fontsize=7.2); ax.invert_yaxis(); ax.axvline(0, color="k", lw=.7)
for i, v in enumerate(vals): ax.text(v + (0.06 if v >= 0 else -0.06), i, idn(v, 2), va="center", ha="left" if v >= 0 else "right", fontsize=7)
ax.set_xlim(-3.9, 2.0); ax.set_xticks([-3, -2, -1, 0, 1, 2]); ax.tick_params(labelsize=7); ax.set_xlabel("NPV per set, USD juta", fontsize=7.2, labelpad=1)
save(fig, "f_skenario.png")

# ---------- F7 armada: set beroperasi + tCO2e dihindari
fl = K["fleet"]; ys = fl["years"]; n = 14; sets = fl["sets_op"][:n]; lc = D["lca"]
fig = plt.figure(figsize=(3.9, 1.95)); ax = fig.add_axes([0.1, 0.18, 0.78, 0.74]); clean(ax)
ax.bar(ys[:n], sets, color=TEAL, width=.7); ax.set_xticks(ys[1:n:2]); ax.tick_params(labelsize=7); ax.set_ylabel("Set beroperasi", fontsize=7.2, labelpad=1)
ax2 = ax.twinx(); ax2.plot(ys[:n], [s * lc["net_total"] / 1000 for s in sets], color=NAVY, lw=2, marker="o", ms=3); ax2.set_ylabel("ribu tCO₂e dihindari/tahun", fontsize=7.2, labelpad=1); ax2.tick_params(labelsize=7)
for s in ("top",): ax2.spines[s].set_visible(False)
ax.annotate(f"10 set pada 2035:\n±{idn(10*lc['net_total']/1000)} ribu tCO₂e/tahun", (2035, 10), xytext=(2029.6, 10.3), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=.7)); ax.set_ylim(0, 12.5)
save(fig, "f_armada.png")

# ---------- F8 gerbang: peluang NPV>0
gt = K["gates"]; fig = plt.figure(figsize=(4.4, 1.5)); ax = fig.add_axes([0.1, 0.17, 0.88, 0.74]); clean(ax)
lb = ["Sekarang", "G0", "G1", "G2", "G3"]; pp = [g["p"] * 100 for g in gt]
ax.bar(lb, pp, color=[SL, TEAL, ROYAL, NAVY, GREEN], width=.62)
for i, p in enumerate(pp): ax.text(i, p + 1.5, f"{idn(p)}%", ha="center", fontsize=8, fontweight="bold", color=INK)
ax.set_ylim(0, 60); ax.set_yticks([0, 25, 50]); ax.tick_params(labelsize=7.4); ax.set_ylabel("Peluang NPV > 0 (%)", fontsize=7.2, labelpad=1)
save(fig, "f_gerbang.png")

# ---------- F9 anggaran: cincin
bd = [("Uji lab dan pilot", 480, GREEN), ("Tim dan manajemen", 310, NAVY), ("FEED dan HAZOP", 220, ROYAL), ("Kuotasi dan MRV", 160, TEAL), ("Izin dan hukum", 130, MID)]
fig = plt.figure(figsize=(4.4, 1.5)); ax = fig.add_axes([0, 0, 0.4, 1]); ax.pie([b[1] for b in bd], colors=[b[2] for b in bd], startangle=90, counterclock=False, wedgeprops=dict(width=0.36, edgecolor="white", linewidth=1.5))
ax.text(0, 0.1, "1.300", ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY); ax.text(0, -0.25, "USD ribu", ha="center", va="center", fontsize=7, color=SL)
ax3 = fig.add_axes([0.42, 0.05, 0.58, 0.9]); ax3.axis("off")
for i, (a, v, c) in enumerate(bd):
    y = 0.88 - i * 0.19; ax3.add_patch(plt.Rectangle((0, y - .05), .06, .1, color=c, transform=ax3.transAxes)); ax3.text(.1, y, a, fontsize=7.8, va="center", transform=ax3.transAxes); ax3.text(1.0, y, f"{idn(v)} ({idn(v/13,0)}%)", fontsize=7.8, va="center", ha="right", fontweight="bold", transform=ax3.transAxes)
save(fig, "f_anggaran.png")

# ---------- F10 radar kesiapan
cats = ["Kelayakan\nteknis", "Daya tarik\nekonomi", "Kesiapan\npasar", "Keberlanjutan", "Risiko\nimplementasi\n(5 = aman)"]; now = [3, 2.5, 2.5, 4.5, 2]; tgt = [4.5, 3.5, 3.5, 4.5, 4]
an = np.linspace(0, 2 * np.pi, 5, endpoint=False); an = np.r_[an, an[0]]
fig = plt.figure(figsize=(3.3, 2.3)); ax = fig.add_axes([0.2, 0.17, 0.6, 0.7], polar=True); ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
for v, c, l, f in [(tgt, GREEN, "Sasaran setelah G3", .08), (now, NAVY, "Kondisi sekarang", .22)]:
    ax.plot(an, v + [v[0]], color=c, lw=1.8, label=l); ax.fill(an, v + [v[0]], color=c, alpha=f)
ax.set_xticks(an[:-1]); ax.set_xticklabels(cats, fontsize=7); ax.set_ylim(0, 5); ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=6, color=SL); ax.spines["polar"].set_color("#9AA9BA"); ax.grid(color="#C9D6E3", lw=.5)
fig.legend(*ax.get_legend_handles_labels(), loc="lower center", fontsize=7, frameon=False, ncol=2, handlelength=1.2)
save(fig, "f_radar.png")

# ---------- sampul: latar render + gradasi navy
im = Image.open("cad/out/render/DIORAMA_lokasi_raw.png").convert("RGB"); W, Hh = 2667, 1500; sh = 900
bg = Image.new("RGB", (W, Hh), (12, 36, 100)); r_ = im.resize((W, Hh), Image.LANCZOS); bg.paste(r_.crop((0, 0, W - sh, Hh)), (sh, 0))
a = np.zeros((Hh, W)); x = np.arange(W); ramp = np.clip((1750 - x) / (1750 - 1150), 0, 1) ** 1.2; a[:] = ramp
base = np.asarray(bg).astype(float); nav = np.array([9, 28, 84], float); out = base * (1 - a[..., None]) + nav * a[..., None]
Image.fromarray(out.astype("uint8")).save(OUT + "cover_bg.png"); print("ok")
