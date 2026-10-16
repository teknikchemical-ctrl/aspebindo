# Gambar gaya laporan konsultan untuk slide 1, 7-10 (dibaca dari deck_data.json). Jalankan dari akar repo.
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
D = json.load(open("deck/deck_data.json")); K = D["keu"]; TG = D["tgt"]; OUT = "deck/img/"
NAVY, ROYAL, TEAL, GREEN, RED, AMB, MID, INK, SL = "#0C2464", "#1F4E9E", "#2B9FC8", "#3E8E41", "#C8452F", "#E0A526", "#6898C8", "#14213D", "#5B6B7F"
plt.rcParams.update({"font.family": "Carlito", "font.size": 8, "axes.edgecolor": "#9AA9BA", "axes.linewidth": 0.6, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "xtick.major.width": .5, "ytick.major.width": .5, "xtick.major.size": 2.5, "ytick.major.size": 2.5})
def idn(x, d=0): s = f"{abs(x):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."); return ("−" if x < 0 and round(abs(x), d) != 0 else "") + s
def clean(ax, left=True):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
def save(fig, name): fig.savefig(OUT + name, dpi=260, facecolor="white"); plt.close(fig)

# ---------- F1 CAPEX: batang + cincin
cc = TG["capex_cat"]; FCI26 = TG["FCI26"]
g = {"Tangki GFS": cc["Tangki reaktor GFS"] + cc["Tangki umpan, efluen, ekualisasi"],
     "Genset 2 × 800 kWe": cc["Genset biogas"],
     "Skid proses": sum(cc[k] for k in ["Praolah (PM-1)", "Skid kontak (degasser + lamella)", "Dosing dan pompa", "Screw press dan lumpur", "Pemulih panas dan menara"]),
     "Pemurnian, penampung gas": cc["Pemurnian biogas (PM-6)"] + cc["Penampung gas dan flare"],
     "Sipil, angkut, ereksi": cc["Sipil, angkut, ereksi"], "Perpipaan, listrik": cc["Perpipaan, listrik, SCADA"],
     "Interkoneksi PLN": cc["Pipa lokasi dan interkoneksi PLN"], "Rekayasa dan start-up": cc["Rekayasa, izin, start-up"], "Kontingensi 20%": cc["Kontingensi 20%"]}
tot = sum(g.values()); items = sorted(g.items(), key=lambda x: -x[1])
colr = {"Tangki GFS": TEAL, "Genset": NAVY, "Skid": ROYAL, "Pemurnian": ROYAL, "Sipil": AMB, "Perpipaan": AMB, "Interkoneksi": AMB, "Rekayasa": RED, "Kontingensi": RED}
def cof(n): return next(v for k, v in colr.items() if n.startswith(k))
fig = plt.figure(figsize=(4.65, 2.0)); ax = fig.add_axes([0.40, 0.19, 0.30, 0.79])
nm = [i[0] for i in items]; vs = [i[1] / 1000 for i in items]
ax.barh(range(len(nm)), vs, color=[cof(n) for n in nm], height=0.68); ax.set_yticks(range(len(nm))); ax.set_yticklabels(nm, fontsize=7.2); ax.invert_yaxis(); clean(ax)
for i, v in enumerate(vs): ax.text(v + 12, i, f"{idn(v)} ({idn(v*1000/tot*100,1)}%)", va="center", fontsize=7)
ax.set_xlim(0, 1900); ax.set_xticks([0, 500, 1000]); ax.set_xlabel("USD ribu (2026)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
ax2 = fig.add_axes([0.74, 0.32, 0.24, 0.66]); grp = {"Peralatan": [TEAL, g["Tangki GFS"] + g["Skid proses"] + g["Pemurnian, penampung gas"]], "Genset": [NAVY, g["Genset 2 × 800 kWe"]],
       "Instalasi dan sipil": [AMB, g["Sipil, angkut, ereksi"] + g["Perpipaan, listrik"] + g["Interkoneksi PLN"]], "Rekayasa dan kontingensi": [RED, g["Rekayasa dan start-up"] + g["Kontingensi 20%"]]}
ax2.pie([v[1] for v in grp.values()], colors=[v[0] for v in grp.values()], startangle=90, counterclock=False, wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.5), radius=1.0)
ax2.text(0, 0.1, "USD " + idn(tot / 1e6, 2), ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY); ax2.text(0, -0.2, "juta", ha="center", va="center", fontsize=7.5, color=SL)
ax2.legend([plt.Rectangle((0, 0), 1, 1, color=v[0]) for v in grp.values()], [f"{k} {idn(v[1]/tot*100,0)}%" for k, v in grp.items()], loc="upper center", bbox_to_anchor=(0.5, 0.02), fontsize=6.4, frameon=False, ncol=1, handlelength=.8, labelspacing=.2)
save(fig, "f_capex.png")

# ---------- F2 OPEX: batang + cincin luar (kelompok) dan dalam (variabel/tetap)
oi = K["opex_items"]
ox = [("Staf operasi (10 orang)", oi["Staf operasi (10 orang)"]["v"], "F", "Staf dan admin."), ("O&M genset (kontrak)", oi["O&M genset (kontrak)"]["v"], "V", "Pemeliharaan"), ("Perawatan proses", oi["Perawatan peralatan proses"]["v"], "F", "Pemeliharaan"),
      ("Bahan kimia", oi["Bahan kimia (polimer, karbon aktif, NaOH)"]["v"], "V", "Bahan"), ("Administrasi dan SCADA", oi["Administrasi & SCADA jarak jauh"]["v"], "F", "Staf dan admin."), ("Asuransi", oi["Asuransi"]["v"], "F", "Asuransi dan lahan"), ("MRV karbon", 12000.0, "F", "Staf dan admin."), ("Sewa lahan", oi["Sewa lahan plot di PKS"]["v"], "F", "Asuransi dan lahan")]
ox.sort(key=lambda x: -x[1]); T = sum(x[1] for x in ox); gc = {"Staf dan admin.": ROYAL, "Pemeliharaan": TEAL, "Bahan": GREEN, "Asuransi dan lahan": AMB}
fig = plt.figure(figsize=(4.65, 2.0)); ax = fig.add_axes([0.27, 0.19, 0.44, 0.79])
ax.barh(range(len(ox)), [x[1] / 1000 for x in ox], color=[gc[x[3]] for x in ox], height=0.68); ax.set_yticks(range(len(ox))); ax.set_yticklabels([x[0] for x in ox], fontsize=7.2); ax.invert_yaxis(); clean(ax)
for i, x in enumerate(ox): ax.text(x[1] / 1000 + 3, i, f"{idn(x[1]/1000,1)} ({idn(x[1]/T*100,1)}%)", va="center", fontsize=7)
ax.set_xlim(0, 200); ax.set_xticks([0, 50, 100]); ax.set_xlabel("USD ribu per tahun (2026)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
ax2 = fig.add_axes([0.74, 0.32, 0.24, 0.66]); og = {}
for n, v_, t, gk in ox: og[gk] = og.get(gk, 0) + v_
ax2.pie(list(og.values()), colors=[gc[k] for k in og], startangle=90, counterclock=False, wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.5))
ax2.text(0, 0.1, "USD " + idn(T / 1000), ha="center", va="center", fontsize=8.5, fontweight="bold", color=NAVY); ax2.text(0, -0.22, "ribu/tahun", ha="center", va="center", fontsize=6.8, color=SL)
fx = sum(x[1] for x in ox if x[2] == "F")
ax2.legend([plt.Rectangle((0, 0), 1, 1, color=gc[k]) for k in og], [f"{k} {idn(og[k]/T*100,0)}%" for k in og] + [], loc="upper center", bbox_to_anchor=(0.5, 0.02), fontsize=6.4, frameon=False, handlelength=.8, labelspacing=.2)
ax2.text(0.5, -0.78, f"Tetap {idn(fx/T*100,0)}% · variabel {idn((T-fx)/T*100,0)}%", transform=ax2.transAxes, ha="center", fontsize=6.4, color=SL)
save(fig, "f_opex.png")

# ---------- F3 titik impas (BEP)
bs = TG["bep_series"]; u = np.array([b["util"] for b in bs]) * 100; rev = np.array([b["rev"] for b in bs]) / 1e3; opx = np.array([b["opex"] for b in bs]) / 1e3; tc = np.array([b["tc"] for b in bs]) / 1e3
fig = plt.figure(figsize=(4.0, 1.88)); ax = fig.add_axes([0.12, 0.3, 0.85, 0.67]); clean(ax); ax.set_ylim(0, 1850)
ax.plot(u, rev, color=GREEN, lw=2, label="Pendapatan"); ax.plot(u, opx, color=SL, lw=1.6, label="Biaya tunai (OPEX)"); ax.plot(u, tc, color=RED, lw=2, label="Biaya total (+ penyusutan + bunga)")
ax.fill_between(u, rev, tc, where=rev >= tc, color=GREEN, alpha=.12, lw=0); ax.fill_between(u, rev, tc, where=rev < tc, color=RED, alpha=.07, lw=0)
for x, lab, dy in [(TG["bep_util_acc"] * 100, "impas akuntansi", 1), (TG["bep_util_npv"] * 100, "impas NPV", 2)]:
    y = np.interp(x, u, rev); ax.plot(x, y, "o", ms=6, color=AMB, mec="white", mew=.8, zorder=5); ax.annotate(f"{lab}\n{idn(x,0)}% beban", (x, y), xytext=((28, 1250) if dy == 1 else (46, 1560)), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=.7), ha="center")
ax.axvline(75, color=NAVY, ls=":", lw=1); ax.text(74.0, 60, "asumsi dasar 75%", fontsize=6.8, color=NAVY, rotation=90, va="bottom", ha="right")
ax.set_xlabel("Beban PKS (% kapasitas nameplate)", fontsize=7.2, labelpad=1); ax.set_ylabel("USD ribu per tahun", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7); ax.legend(fontsize=6.3, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=3, handlelength=1.2, borderpad=0, columnspacing=.9)
save(fig, "f_bep.png")

# ---------- F4 payback (gaya contoh)
yrs = TG["years"]; cf = TG["cf"]; cum = np.array(cf["cum"]) / 1e6; cumd = np.array(cf["cumd"]) / 1e6
fig = plt.figure(figsize=(4.6, 1.88)); ax = fig.add_axes([0.1, 0.2, 0.88, 0.74]); clean(ax)
ax.axvspan(2026.5, 2027.5, color="#EEF2F6"); ax.text(2027, 8.6, "Konstruksi", fontsize=6.8, color=SL, ha="center")
ax.plot(yrs, cum, "-o", color=TEAL, lw=2, ms=3, label="Kumulatif arus kas (tanpa diskonto)"); ax.plot(yrs, cumd, "-s", color=RED, lw=2, ms=3, label=f"Kumulatif arus kas terdiskonto ({idn(TG['WACC']*100,1)}%)"); ax.axhline(0, color="k", lw=.8)
def cross(a):
    for i in range(1, len(a)):
        if a[i - 1] < 0 <= a[i]: return yrs[i - 1] + (-a[i - 1]) / (a[i] - a[i - 1])
px, pd_ = cross(cum), cross(cumd)
ax.plot(px, 0, "o", ms=8, color=AMB, mec="white", zorder=6); ax.annotate(f"Payback {idn(TG['PBP'],1)} tahun\nsejak operasi 2028 (±{int(round(px))})", (px, 0), xytext=(2031.2, 1.2), fontsize=7, color=NAVY, ha="center", arrowprops=dict(arrowstyle="-|>", color="k", lw=.7))
if pd_: ax.plot(pd_, 0, "o", ms=8, color=AMB, mec="white", zorder=6); ax.annotate(f"Payback terdiskonto\n{idn(TG['DPBP'],1)} tahun", (pd_, 0), xytext=(pd_ - 1.0, -5.6), fontsize=7, color=NAVY, ha="center", arrowprops=dict(arrowstyle="-|>", color="k", lw=.7))
i0 = int(np.argmin(cum)); ax.annotate(f"Puncak dana\n−{idn(abs(cum[i0]),1)}", (yrs[i0], cum[i0]), xytext=(2029.0, cum[i0] - 0.2), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color="k", lw=.7), va="center")
ax.set_ylim(-8, 11); ax.set_xticks(yrs[::2]); ax.tick_params(labelsize=7); ax.set_ylabel("USD juta", fontsize=7.2, labelpad=1); ax.set_xlabel("Tahun kalender (operasi 2028–2047)", fontsize=7.2, labelpad=1); ax.legend(fontsize=6.8, frameon=False, loc="upper left", bbox_to_anchor=(0.12, 1.0), borderpad=0)
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
ax.set_xlim(0, 310); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.text(0.98, 0.3, f"Σ {idn(sum(p[1] for p in pv))} PKS (data provinsi)", transform=ax.transAxes, ha="right", fontsize=7.4, color=NAVY, fontweight="bold")
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


# ---------- jembatan NPV (kasus awal -> target)
ch = TG["chain"]; lab = ["Kasus\nawal", "G0 solar\n3,0 L/t", "G1 CAPEX\n−15%", "G2 fee\n1,35", "Karbon\n8,3", "Kasus\ntarget"]
vals_ = [c["NPV"] / 1e6 for c in ch]; steps = [vals_[0]] + [vals_[i] - vals_[i - 1] for i in range(1, len(vals_))]
fig = plt.figure(figsize=(3.65, 1.9)); ax = fig.add_axes([0.1, 0.24, 0.88, 0.7]); clean(ax); run = 0
for i, st in enumerate(steps):
    ax.bar(i, st, bottom=run if i else 0, color=NAVY if i == 0 else GREEN, width=.62); ax.text(i, (run + st) + 0.07, ("+" if i else "") + idn(st, 2), ha="center", fontsize=7.4, fontweight="bold", color=INK); run += st
ax.bar(5, vals_[-1], color=ROYAL, width=.62); ax.text(5, vals_[-1] + 0.07, idn(vals_[-1], 2), ha="center", fontsize=8, fontweight="bold", color=NAVY)
ax.set_xticks(range(6)); ax.set_xticklabels(lab, fontsize=6.4); ax.set_ylim(0, 2.9); ax.set_ylabel("NPV, USD juta", fontsize=7, labelpad=1); ax.tick_params(labelsize=6.8)
save(fig, "f_bridge.png")

# ---------- NPV dan IRR per gerbang
lab = ["Awal", "G0", "G1", "G2", "Karbon"]; fig = plt.figure(figsize=(4.4, 1.55)); ax = fig.add_axes([0.1, 0.2, 0.78, 0.68]); clean(ax)
ax.bar(lab, [c["NPV"] / 1e6 for c in ch[:5]], color=[SL, TEAL, ROYAL, NAVY, GREEN], width=.6)
for i, c in enumerate(ch[:5]): ax.text(i, c["NPV"] / 1e6 + 0.06, f"{idn(c['NPV']/1e6,2)}", ha="center", fontsize=7.6, fontweight="bold")
ax.set_ylim(0, 4.6); ax.set_yticks([0, 1, 2]); ax.set_ylabel("NPV, USD juta", fontsize=7, labelpad=1); ax.tick_params(labelsize=7.2)
ax2 = ax.twinx(); ax2.plot(range(5), [c["IRR"] * 100 for c in ch[:5]], color=AMB, marker="o", ms=4, lw=2); ax2.set_ylim(-14, 19); ax2.set_yticks([]); ax2.set_ylabel("IRR proyek (garis)", fontsize=7, labelpad=1, color="#9A6B00"); ax2.spines["top"].set_visible(False)
for i, c in enumerate(ch[:5]): ax2.text(i, c["IRR"] * 100 + 1.6, f"{idn(c['IRR']*100,1)}%", ha="center", fontsize=6.8, color="#9A6B00")
save(fig, "f_gerbang.png")

# ---------- dana per gerbang
gs = ["G0", "G1", "G2", "G3"]; cl = [("Uji lab dan pilot", [70, 160, 0, 250], GREEN), ("Tim dan manajemen", [60, 80, 80, 90], NAVY), ("FEED dan HAZOP", [0, 40, 180, 0], ROYAL), ("Kuotasi dan MRV", [20, 60, 40, 40], TEAL), ("Izin dan hukum", [0, 0, 100, 30], MID)]
fig = plt.figure(figsize=(4.4, 1.2)); ax = fig.add_axes([0.1, 0.2, 0.5, 0.72]); clean(ax); bt = np.zeros(4)
for n, v_, c in cl: ax.bar(gs, v_, bottom=bt, color=c, width=.62, label=n); bt += np.array(v_)
for i, t in enumerate(bt): ax.text(i, t + 8, str(int(t)), ha="center", fontsize=8, fontweight="bold")
ax.set_ylim(0, 520); ax.set_ylabel("USD ribu", fontsize=7, labelpad=1); ax.tick_params(labelsize=7.4)
h, l = ax.get_legend_handles_labels(); fig.legend(h[::-1], l[::-1], loc="center left", bbox_to_anchor=(0.62, 0.5), fontsize=7, frameon=False, handlelength=.9, labelspacing=.45)
fig.text(0.62, 0.04, "Total USD 1.300 ribu (usulan)", fontsize=7.4, fontweight="bold", color=NAVY)
save(fig, "f_dana.png")

# ---------- skor pesaing: kontribusi kriteria berbobot
P = D["pesaing"]; crit = P["crit"]; w = np.array([c[1] for c in crit]); nm = ["Status quo: kolam terbuka", "Lagun tertutup (milik PKS)", "CSTR mesofilik (milik PKS)", "Biometana BOOT (klaster)", "UASB / IC", "AnMBR konvensional", "Kontak termofilik BOO (usulan)"]
rows = [(nm[i], np.array(r["scores"]) * w, r["total"]) for i, r in enumerate(P["rows"])]; rows.sort(key=lambda x: x[2])
ck = ["Biaya POME bagi PKS", "Modal yang dikeluarkan PKS", "Risiko kinerja di PKS", "Kematangan dan referensi", "Lahan dan waktu bangun", "Penangkapan metana dan bau", "Dapat dipindah"]; cc_ = [NAVY, TEAL, ROYAL, MID, AMB, GREEN, "#8CC63F"]
fig = plt.figure(figsize=(5.3, 2.55)); ax = fig.add_axes([0.33, 0.3, 0.64, 0.68]); clean(ax)
for yi, (n, ct, tot_) in enumerate(rows):
    lft = 0
    for j, c_ in enumerate(ct): ax.barh(yi, c_, left=lft, color=cc_[j], height=.66, edgecolor="white", lw=.5, label=ck[j] if yi == 0 else None); lft += c_
    ax.text(tot_ + .04, yi, idn(tot_, 2), va="center", fontsize=8, fontweight="bold", color=GREEN if yi == len(rows) - 1 else INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7.6); ax.get_yticklabels()[-1].set_fontweight("bold"); ax.set_xlim(0, 4.6); ax.set_xlabel("Skor berbobot (maks. 5)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
fig.legend(*ax.get_legend_handles_labels(), loc="lower center", ncol=3, fontsize=6.4, frameon=False, handlelength=.8, columnspacing=.8, bbox_to_anchor=(0.55, -0.02))
save(fig, "f_skor.png")

# ---------- posisi: modal PKS vs biaya POME (kasus target)
tp = TG["pks"]; fig = plt.figure(figsize=(3.3, 2.1)); ax = fig.add_axes([0.14, 0.2, 0.82, 0.74]); clean(ax)
pts = [("A Kolam terbuka", 0, tp["per_t"]["A"], SL), ("B Lagun tertutup", tp["capex"]["B"] / 1e6, tp["per_t"]["B"], MID), ("C CSTR milik PKS", tp["capex"]["C"] / 1e6, tp["per_t"]["C"], ROYAL), ("G BOO termofilik", 0, tp["per_t"]["D"], GREEN)]
for n, x, y, c in pts: ax.scatter(x, y, s=130 if n[0] == "G" else 80, color=c, edgecolor="white", zorder=5); ax.text(x + 0.25, y + (-0.34 if n[0] == "G" else (0.0 if n[0] == "A" else 0.12)), n, fontsize=7.2, fontweight="bold" if n[0] == "G" else None, color=INK)
ax.annotate("", (0, tp["per_t"]["D"] + .02), (0, tp["per_t"]["A"] - .02), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4))
ax.text(1.6, 4.2, f"hemat {idn(tp['save_pct']*100,0)}%\nmodal PKS nol", fontsize=7, color=GREEN, fontweight="bold", va="center")
ax.set_xlim(-0.35, 5.8); ax.set_ylim(1.4, 5.0); ax.set_xlabel("Modal yang dikeluarkan PKS (USD juta)", fontsize=7.2, labelpad=1); ax.set_ylabel("Biaya POME PKS (USD/t TBS)", fontsize=7.2, labelpad=1); ax.tick_params(labelsize=7)
save(fig, "f_posisi.png")

# ---------- Porter
po = D["porter"]; fo = [("Daya tawar pembeli", "Pembeli"), ("Persaingan", "Persaingan"), ("Produk substitusi", "Produk substitusi"), ("Ancaman pendatang baru", "Pendatang baru"), ("Daya tawar pemasok", "Pemasok")]
mean = [(a, float(np.mean([x["s"] for x in po[k]]))) for a, k in fo]
fig = plt.figure(figsize=(3.6, 1.95)); ax = fig.add_axes([0.42, 0.14, 0.52, 0.8]); clean(ax)
ax.barh(range(5), [m[1] for m in mean], color=[GREEN if m[1] < 3 else (AMB if m[1] < 3.5 else RED) for m in mean], height=.6); ax.set_yticks(range(5)); ax.set_yticklabels([m[0] for m in mean], fontsize=7.6); ax.invert_yaxis(); ax.set_xlim(0, 5)
for i, m in enumerate(mean): ax.text(m[1] + .06, i, idn(m[1], 1), va="center", fontsize=7.6, fontweight="bold")
ax.axvline(3, color=SL, ls=":", lw=.8); ax.set_xlabel("Intensitas (1 = lemah, 5 = kuat)", fontsize=7, labelpad=1); ax.tick_params(labelsize=7)
save(fig, "f_porter.png")

# ---------- tuas nilai
lv = TG["levers"]; fig = plt.figure(figsize=(4.65, 2.0)); ax = fig.add_axes([0.36, 0.17, 0.6, 0.78]); clean(ax)
nmv = [l["l"] for l in lv]; vv_ = [l["NPV"] / 1e6 for l in lv]
ax.barh(range(len(lv)), vv_, color=[SL] + [TEAL] * (len(lv) - 2) + [GREEN], height=.64); ax.set_yticks(range(len(lv))); ax.set_yticklabels(nmv, fontsize=7.4); ax.invert_yaxis(); ax.get_yticklabels()[-1].set_fontweight("bold")
for i, (a, l) in enumerate(zip(vv_, lv)): ax.text(a + .04, i, f"{idn(a,2)}  ·  IRR {idn(l['IRR']*100,1)}%", va="center", fontsize=7)
ax.set_xlim(0, 3.7); ax.set_xlabel("NPV per set, USD juta (tiap tuas berdiri sendiri; target = gabungan)", fontsize=6.8, labelpad=1); ax.tick_params(labelsize=7)
save(fig, "f_tuas.png")

# ---------- armada (kasus target)
fl = TG["fleet"]; ys = fl["years"]; n = 14; sets = fl["sets_op"][:n]; lc = D["lca"]
fig = plt.figure(figsize=(3.9, 1.95)); ax = fig.add_axes([0.1, 0.18, 0.78, 0.74]); clean(ax)
ax.bar(ys[:n], sets, color=TEAL, width=.7); ax.set_xticks(ys[1:n:2]); ax.tick_params(labelsize=7); ax.set_ylabel("Set beroperasi", fontsize=7.2, labelpad=1); ax.set_ylim(0, 12.5)
ax2 = ax.twinx(); ax2.plot(ys[:n], [x * lc["net_total"] / 1000 for x in sets], color=NAVY, lw=2, marker="o", ms=3); ax2.set_ylabel("ribu tCO₂e dihindari/tahun", fontsize=7.2, labelpad=1); ax2.tick_params(labelsize=7); ax2.spines["top"].set_visible(False)
ax.annotate(f"10 set pada 2035:\n±{idn(10*lc['net_total']/1000)} ribu tCO₂e/tahun", (2035, 10), xytext=(2029.6, 10.3), fontsize=7, color=NAVY, arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=.7))
save(fig, "f_armada.png")

# ---------- sampul: latar render + gradasi navy
im = Image.open("cad/out/render/DIORAMA_lokasi_raw.png").convert("RGB"); W, Hh = 2667, 1500; sh = 900
bg = Image.new("RGB", (W, Hh), (12, 36, 100)); r_ = im.resize((W, Hh), Image.LANCZOS); bg.paste(r_.crop((0, 0, W - sh, Hh)), (sh, 0))
a = np.zeros((Hh, W)); x = np.arange(W); ramp = np.clip((1750 - x) / (1750 - 1150), 0, 1) ** 1.2; a[:] = ramp
base = np.asarray(bg).astype(float); nav = np.array([9, 28, 84], float); out = base * (1 - a[..., None]) + nav * a[..., None]
Image.fromarray(out.astype("uint8")).save(OUT + "cover_bg.png"); print("ok")
