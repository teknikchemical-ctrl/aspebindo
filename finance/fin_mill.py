# -*- coding: utf-8 -*-
"""
Model Keputusan PKS (Mill Decision Model) - apakah layanan BOO ini LEBIH MURAH bagi PKS daripada status quo kolam POME?

Sudut pandang PKS 45 t TBS/jam, 20 tahun operasi (2028-2047), USD nominal, didiskonto pada biaya modal PKS.
Opsi:
  A  Status quo: kolam anaerobik terbuka + aplikasi lahan; listrik di luar jam olah / emplasmen dari genset diesel.
  B  PKS membangun kolam tertutup (covered lagoon) sendiri: CAPEX ditanggung PKS, operasi sendiri, ekspor PLN + karbon milik PKS.
  C  PKS membeli digester tangki (CSTR) dari EPC: CAPEX ditanggung PKS.
  D  Layanan BOO ini: PKS bayar jasa (USD/t TBS) + beli listrik set dengan harga di bawah diesel; tanpa CAPEX; risiko kinerja di pengembang.
Hubungan ke listrik & karbon: listrik set menggantikan solar PKS (penghematan terbesar); ekspor PLN dan kredit karbon
milik pengembang memungkinkan jasa (fee) di bawah biaya yang dihindari PKS. Jendela kesepakatan = [fee minimum pengembang (NPV=0),
fee maksimum PKS (biaya D = biaya A)]. Semua angka bersumber dari research/R1-R4 (source_register.json) atau ditandai [ASUMSI].
Excel (fin_excel.py, lembar 'Keputusan PKS') menghitung ulang semua ini dengan rumus hidup; verify() mencocokkan.
"""
import numpy as np
import fin_core as F

T = F.TECH
# (nilai, satuan, sumber, rendah, tinggi)
M = {
    "r_mill": (0.12, "/th", "Biaya modal PKS (WACC proyek nominal Indonesia 9,4-14%) [R2]", 0.10, 0.18),
    "p_diesel": (21000.0, "Rp/L", "Solar industri diantar (HSD/B40 non-subsidi) 18.200-25.850 [R2]", 18200.0, 25850.0),
    "genset_om": (0.02, "USD/kWh", "O&M genset diesel PKS (pelumas, filter, overhaul) [ASUMSI]", 0.01, 0.04),
    "desludge": (400.0, "juta Rp/th", "Pengurasan lumpur kolam anaerobik ~1 kali/th, Rp 0,2-0,6 M/kejadian [R2, keyakinan rendah]", 200.0, 600.0),
    "pond_om": (22.0, "juta Rp/th", "Pompa, tanggul, perawatan kolam (tanpa pengurasan) [R2]", 20.0, 100.0),
    "la_cost": (10000.0, "Rp/m3", "Aplikasi lahan flatbed/furrow per m3 limbah [R2]", 7000.0, 19000.0),
    "monitor": (250.0, "juta Rp/th", "Pemantauan RKL-RPL/Persetujuan Teknis (sama untuk semua opsi) [R2]", 150.0, 400.0),
    "margin": (15.0, "USD/t TBS", "Margin olah PKS per t TBS untuk menilai hari henti (penyegelan) [ASUMSI]", 10.0, 25.0),
    "p_enf_A": (0.03, "/th", "Peluang penegakan/penyegelan per th untuk kolam terbuka (kasus PT BMB 2023, PT SIPP 2024) [ASUMSI dari R1]", 0.01, 0.06),
    "p_enf_D": (0.005, "/th", "Peluang yang sama dengan reaktor tertutup + kolam polishing [ASUMSI]", 0.0, 0.01),
    "closure_d": (30.0, "hari", "Lama henti bila disegel [ASUMSI dari R1]", 14.0, 90.0),
    "land_margin": (32.0, "juta Rp/ha/th", "Margin bersih sawit per ha (TBS Rp 3.763/kg Riau Okt 2026) [R2]", 20.0, 45.0),
    "cake_val": (6.0, "USD/t basah", "Nilai pupuk kue lumpur 20% DS untuk kebun (N, P, K) [ASUMSI]", 0.0, 12.0),
    "c_share": (0.0, "-", "Bagian pendapatan karbon pengembang yang dibagi ke PKS (tuas komersial)", 0.0, 0.5),
    # opsi B / C (pesaing yang dibeli PKS)
    "capex_B": (2.2, "juta USD/MWe", "Kolam tertutup (covered lagoon) di Indonesia 1,8-3,7 [R3]", 1.8, 3.7),
    "capex_C": (2.5, "juta USD/MWe", "Digester tangki CSTR (TSE 2 MW USD 3,6 jt) 1,8-3,5 [R3]", 1.8, 3.5),
    "om_BC": (3.3, "miliar Rp/MW/th", "O&M PLTBg POME 2,3-4,3 [R2]", 2.3, 4.3),
    "perf_B": (0.75, "-", "Kinerja relatif kolam tertutup (buih, lumpur, faktor kapasitas 57-85%) [R2]", 0.57, 0.85),
    "perf_C": (0.85, "-", "Kinerja relatif tangki milik PKS (tanpa jaminan kinerja) [R2]", 0.70, 0.90),
    "desl_B": (0.5, "-", "Porsi pengurasan yang tetap ada pada kolam tertutup", 0.3, 0.8),
}
def mvals(m=M): return {k: (x[0] if isinstance(x, tuple) else x) for k, x in m.items()}

def af(r, g, n):
    """sum_{t=1..n} (1+g)^(t+1) / (1+r)^t : faktor anuitas biaya 2026 yang dieskalasi (tahun = 2027 + t)"""
    q = (1 + g) / (1 + r)
    return (1 + g) * q * (1 - q ** n) / (1 - q)

def dfs(r, n): return (1 - (1 + r) ** -n) / r

def annual(v=None, m=None):
    """biaya/manfaat tahunan (USD 2026, tahun penuh) untuk opsi A-D; positif = biaya PKS"""
    v = dict(v or F.vals()); m = dict(m or mvals())
    fx = v["fx"]; ffb = T["ffb_ty_nom"] * v["util"]; pome = ffb * T["pome_m3d"] / 900.0
    eff_m3 = pome * F.R["effluent"]["Q_m3d"] / T["pome_m3d"]
    k = F.kfac(v)
    E_net = T["E_year_GWh"] * k * v["avail"] * 1e6                     # kWh/th netto set D
    E_dsl = ffb * v["diesel_L_tffb"] / v["sfc"]                          # kWh/th diesel PKS
    c_dsl = v["sfc"] * m["p_diesel"] / fx + m["genset_om"]               # USD/kWh listrik diesel PKS
    cap = min(E_dsl * v["avail"], E_net)                                 # listrik set ke PKS (saat set tidak tersedia, genset diesel jalan)
    risk = lambda p: p * m["closure_d"] * ffb / T["days_yr"] * m["margin"]
    land = F.SITE.get("land_freed_m2", 11081.0) / 1e4 * m["land_margin"] * 1e6 / fx
    cake = ffb * T["cake_kg_tffb"] / 1000 * m["cake_val"]
    ER, _ = F.carbon_t(v); cnet = ER * v["cer_ratio"] * (v["p_carbon"] - v["c_levy"])
    A = {"Listrik diesel PKS (solar + O&M genset)": E_dsl * c_dsl,
         "Pengurasan lumpur kolam": m["desludge"] * 1e6 / fx,
         "Perawatan kolam & pompa": m["pond_om"] * 1e6 / fx,
         "Aplikasi lahan": pome * m["la_cost"] / fx,
         "Pemantauan lingkungan": m["monitor"] * 1e6 / fx,
         "Risiko penyegelan (nilai harapan)": risk(m["p_enf_A"])}
    D = {"Jasa pengolahan POME (fee)": ffb * v["fee_ffb"],
         "Listrik dari set": cap * v["p_captive"],
         "Listrik diesel sisa (set tidak tersedia)": (E_dsl - cap) * c_dsl,
         "Aplikasi lahan (efluen)": eff_m3 * m["la_cost"] / fx,
         "Pemantauan lingkungan": m["monitor"] * 1e6 / fx,
         "Risiko penyegelan (nilai harapan)": risk(m["p_enf_D"]),
         "Lahan kolam dibebaskan (margin sawit)": -land,
         "Kue lumpur sebagai pupuk": -cake,
         "Bagi hasil karbon": -m["c_share"] * cnet}
    out = {"A": A, "D": D}
    for o_, cpx, perf, desl, frees in (("B", m["capex_B"], m["perf_B"], m["desl_B"], 0.0), ("C", m["capex_C"], m["perf_C"], 0.0, 1.0)):
        E_o = T["E_year_GWh"] * k * perf * 1e6
        cap_o = min(E_dsl * perf, E_o)
        exp_o = E_o - cap_o
        tar = v["tariff1"] * v["F_loc"] / 100.0
        X = {"Listrik diesel sisa": (E_dsl - cap_o) * c_dsl,
             "O&M pembangkit biogas milik PKS": m["om_BC"] * 1e9 / fx * T["chp_kWe"] / 1000.0,
             "Pengurasan lumpur": desl * m["desludge"] * 1e6 / fx,
             "Aplikasi lahan": pome * m["la_cost"] / fx,
             "Pemantauan lingkungan": m["monitor"] * 1e6 / fx,
             "Risiko penyegelan (nilai harapan)": risk(m["p_enf_D"]),
             "Ekspor listrik ke PLN (th 1-10)": -exp_o * tar,
             "Kredit karbon (PKS daftar sendiri)": -cnet * perf + (v["c_mrv"]),
             "Lahan kolam dibebaskan": -land * frees}
        out[o_] = X
        out[o_ + "_capex"] = cpx * 1e6 * T["chp_kWe"] / 1000.0
    out.update(ffb=ffb, E_dsl=E_dsl, cap=cap, c_dsl=c_dsl, E_net=E_net, cnet=cnet, land=land, cake=cake)
    return out

def compare(v=None, m=None):
    """NPV biaya 20 th (USD nominal, 2027 = t0) dan biaya terlevelisasi USD 2026/t TBS per opsi"""
    v = dict(v or F.vals()); m = dict(m or mvals())
    a = annual(v, m); r, g, n = m["r_mill"], v["infl"], int(v["n_op"])
    f_ = af(r, g, n); ffb_pv = a["ffb"] * f_                            # levelisasi dalam USD 2026 (biaya dibagi TBS yang 'dieskalasi' sama)
    res = {}
    for o_ in ("A", "B", "C", "D"):
        ann = sum(a[o_].values())
        npv_ = ann * f_ + a.get(o_ + "_capex", 0.0) * (1 + g)
        res[o_] = dict(annual=ann, NPV=npv_, per_t=npv_ / ffb_pv, capex=a.get(o_ + "_capex", 0.0))
    res["saving_D_vs_A_per_t"] = res["A"]["per_t"] - res["D"]["per_t"]
    res["saving_D_vs_A_pct"] = res["saving_D_vs_A_per_t"] / res["A"]["per_t"]
    res["af"] = f_; res["ffb_pv"] = ffb_pv; res["detail"] = a
    return res

def fee_window(v=None, m=None):
    """fee minimum (pengembang NPV=0 pada WACC) dan fee maksimum (biaya PKS opsi D = opsi A); juga fee yang membuat D = B"""
    v = dict(v or F.vals()); m = dict(m or mvals())
    def dev(x): vv = dict(v); vv["fee_ffb"] = x; return F.run(vv)["NPV"]
    def mill(x, o="A"): vv = dict(v); vv["fee_ffb"] = x; c = compare(vv, m); return c[o]["NPV"] - c["D"]["NPV"]
    lo = F.solve(dev, -2.0, 8.0); hi = F.solve(lambda x: mill(x, "A"), -2.0, 12.0); hB = F.solve(lambda x: mill(x, "B"), -6.0, 12.0)
    return dict(fee_min=lo, fee_max=hi, fee_max_vs_B=hB, width=hi - lo if (lo == lo and hi == hi) else float("nan"))

SEGMENTS = [  # (nama, util, L solar/t TBS, catatan)
    ("S1 PKS terhubung PLN, diesel hanya PKS", 0.75, 0.53, "Konsumsi solar PKS rata-rata [R2]"),
    ("S2 PKS terhubung PLN, util tinggi", 0.85, 0.53, "PKS dengan pasokan TBS terjamin"),
    ("S3 PKS bergantung diesel (emplasmen, bengkel, KCP)", 0.75, 3.0, "Kasus dasar; DSNG hemat 2-2,75 jt L/th [R2-tambahan]"),
    ("S4 PKS off-grid penuh", 0.75, 5.0, "Kaltim: 12 dari 62 PKS dekat desa tanpa listrik/diesel [Jakarta Post 2015]"),
]
def segments(v=None, m=None):
    v = dict(v or F.vals()); out = []
    for nm, u, dl, note in SEGMENTS:
        vv = dict(v); vv["util"] = u; vv["diesel_L_tffb"] = dl
        fw = fee_window(vv, m); o = F.run(vv); c = compare(vv, m)
        out.append(dict(name=nm, util=u, diesel=dl, note=note, fee_min=fw["fee_min"], fee_max=fw["fee_max"], NPV_dev=o["NPV"], IRR_dev=o["IRR"],
                        saving_pct=c["saving_D_vs_A_pct"], A_per_t=c["A"]["per_t"], D_per_t=c["D"]["per_t"]))
    return out

def waterfall(v=None, m=None):
    """langkah dari biaya status quo ke biaya opsi D, USD/t TBS terlevelisasi"""
    c = compare(v, m); a = c["detail"]; s = c["af"] / c["ffb_pv"]
    A = a["A"]; D = a["D"]
    steps = [("Status quo (A)", c["A"]["per_t"])]
    steps.append(("Solar dihindari", -(A["Listrik diesel PKS (solar + O&M genset)"] - D["Listrik diesel sisa (set tidak tersedia)"]) * s))
    steps.append(("Beli listrik set", D["Listrik dari set"] * s))
    steps.append(("Pengurasan & kolam dihindari", -(A["Pengurasan lumpur kolam"] + A["Perawatan kolam & pompa"]) * s))
    steps.append(("Aplikasi lahan (efluen lebih sedikit)", (D["Aplikasi lahan (efluen)"] - A["Aplikasi lahan"]) * s))
    steps.append(("Risiko penyegelan turun", (D["Risiko penyegelan (nilai harapan)"] - A["Risiko penyegelan (nilai harapan)"]) * s))
    steps.append(("Lahan + pupuk + karbon", (D["Lahan kolam dibebaskan (margin sawit)"] + D["Kue lumpur sebagai pupuk"] + D["Bagi hasil karbon"]) * s))
    steps.append(("Jasa pengolahan (fee)", D["Jasa pengolahan POME (fee)"] * s))
    steps.append(("Layanan BOO (D)", c["D"]["per_t"]))
    return steps

if __name__ == "__main__":
    c = compare()
    for o_ in "ABCD": print(o_, "annual %.0f  NPV %.0f  USD/t %.2f  capex %.0f" % (c[o_]["annual"], c[o_]["NPV"], c[o_]["per_t"], c[o_]["capex"]))
    print("D saves vs A: %.2f USD/t (%.0f%%)" % (c["saving_D_vs_A_per_t"], c["saving_D_vs_A_pct"] * 100))
    print(fee_window())
    for s in segments(): print(s)
    for s in waterfall(): print("%-40s %7.2f" % s)
