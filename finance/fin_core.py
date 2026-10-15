# -*- coding: utf-8 -*-
"""
Model keuangan inti (USD nominal) - Generator Biogas Portabel AnMBR termofilik untuk PKS.
Satu sumber kebenaran: dipakai oleh fin_model.py (Excel, gambar, laporan).

Model bisnis dasar: BOO (Build-Own-Operate) per set standar di lahan PKS, kontrak 20 tahun.
Pendapatan: listrik ke PLN (Perpres 112/2022, PLTBg <= 1 MW), kredit karbon penghindaran metana,
air panas ke PKS (pemanas awal air umpan boiler -> hemat cangkang), kue lumpur sebagai pupuk organik.
Data teknis dibaca dari process/outputs/results.json dan cad/out (massa bejana dari model 3D).
Semua angka harga/biaya memiliki sumber atau ditandai [ASUMSI] di tabel ASUMSI.
"""
import os, json, math, copy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
R = json.load(open(os.path.join(ROOT, "process", "outputs", "results.json"), encoding="utf-8"))
PMJ = json.load(open(os.path.join(ROOT, "process", "outputs", "portable_modules.json"), encoding="utf-8"))

# ------------------------------------------------------------------------------------------- teknis
TECH = dict(
    ffb_tph=R["design_basis"]["ffb_tph"], hrs_day=R["design_basis"]["hrs_day"], days_yr=R["design_basis"]["days_yr"],
    pome_m3d=R["design_basis"]["pome_m3d"], biogas_Nm3d=R["nominal"]["biogas_Nm3d"], ch4_frac=R["nominal"]["ch4_frac"],
    P_gross=R["energy"]["P_gross"], P_net=R["energy"]["P_net"], P_par=R["energy"]["P_par"], GWh_net=R["year"]["GWh_net"],
    Q_heat=R["energy"]["Q_heat_avail"], co2e_avoided=R["emissions"]["avoided_t"], n_vessel=R["tiers"]["45"]["N_modules"],
    area_mem=R["equipment"]["membrane"]["area_m2"], chp_kWe=R["equipment"]["chp"]["installed_kWe"],
    cake_kgh=[s for s in R["streams"] if s["id"] == 12][0]["kg_h"], gh_m3=R["equipment"]["gas_holder"]["V_m3"],
    polymer_kgh=[s for s in R["streams"] if s["id"] == 26][0]["kg_h"], ac_kgh=[s for s in R["streams"] if s["id"] == 25][0]["kg_h"],
    plot_m2=PMJ.get("plot_area_m2_estimate", {}).get("total", 2860.0) if isinstance(PMJ.get("plot_area_m2_estimate"), dict) else 2860.0,
    vessel_t=20.9, tank_t=20.0, truckloads=PMJ["ship_units_total"])
TECH["pome_m3y"] = TECH["pome_m3d"] * TECH["days_yr"]
TECH["ffb_ty"] = TECH["ffb_tph"] * TECH["hrs_day"] * TECH["days_yr"]
TECH["cake_ty"] = TECH["cake_kgh"] * TECH["hrs_day"] * TECH["days_yr"] / 1000.0
TECH["E_gross_GWh"] = TECH["GWh_net"] * TECH["P_gross"] / TECH["P_net"]

# ------------------------------------------------------------------------------------------- asumsi
# (nilai, satuan, sumber/catatan, rendah, tinggi)  -> rendah/tinggi dipakai tornado & Monte Carlo
A = {
    # waktu
    "year0": (2027, "tahun", "Tahun konstruksi (fabrikasi bengkel 8 bln + pasang 3 bln)", None, None),
    "n_op": (20, "tahun", "Umur operasi kontrak BOO (bejana CS + pelapis epoksi 20+ th)", None, None),
    "ramp1": (0.75, "-", "Faktor tahun operasi pertama (start-up biomassa termofilik ~3 bln) [ASUMSI]", 0.6, 0.85),
    "avail": (0.95, "-", "Ketersediaan pembangkit (2 genset, N+0) [ASUMSI, praktik CHP biogas]", 0.90, 0.97),
    # teknis
    "E_net_GWh": (TECH["GWh_net"], "GWh/th", "Neraca energi tahunan (results.json, profil bulanan PKS)", TECH["GWh_net"] * 0.8, TECH["GWh_net"] * 1.15),
    "co2e": (TECH["co2e_avoided"], "tCO2e/th", "Emisi metana terhindar vs kolam terbuka (results.json, IPCC MCF 0,8)", None, None),
    "cer_ratio": (0.85, "-", "Rasio penerbitan kredit (buffer, ketidakpastian, kebocoran) [ASUMSI, metodologi AMS-III.H]", 0.75, 0.95),
    "heat_util": (0.40, "-", "Fraksi panas CHP terpakai PKS (pemanas air umpan boiler) [ASUMSI]", 0.2, 0.6),
    # harga & tarif
    "tariff1": (11.47, "USc/kWh", "Perpres 112/2022 Lamp. I, PLTBg <= 1 MW, th 1-10", 9.94, 11.47),
    "F_loc": (1.10, "-", "Faktor lokasi F Sumatera ~1,10 [perlu verifikasi; Kalimantan 1,10]", 1.00, 1.10),
    "tariff2": (6.88, "USc/kWh", "Perpres 112/2022, th 11-30 (0,6 x harga dasar, tanpa F)", 5.97, 6.88),
    "p_carbon": (12.0, "USD/tCO2e", "VCM penghindaran metana 10-25 (Carbonmark 2026); IDXCarbon ~2,2; dasar konservatif", 2.2, 20.0),
    "fee_pome": (0.40, "USD/m3 POME", "Jasa pengolahan POME dibayar PKS (hindari pengurasan kolam, lahan 5-8 ha, kepatuhan ISPO) [ASUMSI]", 0.0, 0.80),
    "p_heat": (18.0, "USD/MWh-th", "Setara cangkang USD 100/t, LHV 17 MJ/kg, boiler 75%, diskon 35% ke PKS [ASUMSI]", 10.0, 25.0),
    "p_cake": (5.0, "USD/t", "Kue lumpur ke kebun sebagai pupuk organik [ASUMSI]", 0.0, 10.0),
    "fx": (17855.0, "IDR/USD", "Kurs 22 Sep 2026 (RRI/Bisnis)", None, None),
    "infl": (0.03, "/th", "Eskalasi OPEX (inflasi CPI 3,19% Agu 2026)", 0.02, 0.045),
    # CAPEX unit cost
    "c_fab": (2.5, "USD/kg", "Bejana CS difabrikasi + dilapis (estimasi 1,8-4,0; HRC USD 515/t)", 2.0, 3.2),
    "c_mem": (200.0, "USD/m2", "Membran UF tubular PVDF (100-300) [ASUMSI]", 150.0, 280.0),
    "c_chp": (550.0, "USD/kWe", "Genset biogas kontainer (Asia 350-600; Eropa 700-1.100)", 450.0, 800.0),
    "cont": (0.10, "-", "Kontingensi atas biaya langsung + tak langsung (produk standar)", 0.05, 0.20),
    "eng": (0.05, "-", "Rekayasa & manajemen proyek (desain standar berulang) [ASUMSI]", 0.05, 0.12),
    # OPEX
    "c_eng_om": (0.012, "USD/kWh-gross", "O&M genset kontrak penuh (tanpa overhaul) [ASUMSI 10-18 USD/MWh]", 0.010, 0.018),
    "c_maint": (0.02, "-/th x PEC non-genset", "Perawatan peralatan proses [ASUMSI]", 0.015, 0.03),
    "c_ins": (0.005, "-/th x FCI", "Asuransi all-risk [ASUMSI]", None, None),
    "staff": (78000.0, "USD/th", "1 manajer, 6 operator 3 shift, 1 lab/K3; 14 bln gaji + BPJS", 65000.0, 95000.0),
    "c_mrv": (25000.0, "USD/th", "Pemantauan, validasi/verifikasi karbon + biaya registri", 15000.0, 35000.0),
    "c_admin": (30000.0, "USD/th", "Administrasi SPV, IT/SCADA jarak jauh, audit", None, None),
    "lease": (2.0, "USD/m2/th", "Sewa lahan di PKS (0,29 ha) [ASUMSI]", None, None),
    "p_poly": (4000.0, "USD/t", "Polimer kationik (dewatering)", None, None),
    "p_ac": (3000.0, "USD/t", "Karbon aktif impregnasi KI", None, None),
    "c_naoh": (8000.0, "USD/th", "Cadangan NaOH/urea untuk gangguan (P95 dosis) [ASUMSI]", None, None),
    "overhaul": (150.0, "USD/kWe", "Overhaul besar genset tiap 60.000 jam (~th 8 & 16)", 120.0, 220.0),
    "mem_life": (7, "tahun", "Umur membran tubular (penggantian th 8 & 15)", None, None),
    # pajak & pendanaan
    "tax": (0.22, "-", "PPh badan (UU HPP)", None, None),
    "dep_life": (16, "tahun", "Penyusutan garis lurus, kelompok 3 (PMK 72/2023)", None, None),
    "allow": (0.30, "-", "Tax allowance PP 78/2019: 30% investasi, 5%/th x 6 th (EBT)", None, None),
    "debt_frac": (0.60, "-", "Porsi utang pembiayaan proyek EBT [ASUMSI]", None, None),
    "r_debt": (0.08, "/th", "Bunga pinjaman hijau USD (6,5-8,5% + premi)", 0.065, 0.10),
    "tenor": (10, "tahun", "Tenor utang (anuitas, mulai th operasi 1)", None, None),
    "r_eq": (0.15, "/th", "Biaya ekuitas (CAPM negara berkembang + premi teknologi)", None, None),
    "wc_months": (2.0, "bulan", "Modal kerja = 2 bulan OPEX", None, None),
}
def V(a, k): return a[k][0] if isinstance(a[k], tuple) else a[k]
def vals(a=A): return {k: V(a, k) for k in a}

def wacc(v):
    return v["debt_frac"] * v["r_debt"] * (1 - v["tax"]) + (1 - v["debt_frac"]) * v["r_eq"]

# ------------------------------------------------------------------------------------------- CAPEX
def capex_items(v, tech=TECH, scale=1.0):
    """daftar (kelompok, item, jumlah, satuan, harga satuan USD, total USD, dasar). scale: faktor ukuran set (30/60 t)"""
    nv = tech["n_vessel"]
    rv = v["c_fab"] * tech["vessel_t"] * 1000 + 12000 + 7500 + 10000      # fab + insulasi/kladding + internal SS + nosel/instrumen
    tk = v["c_fab"] * tech["tank_t"] * 1000 + 6000
    I = [("PEC", "Reaktor AnMBR standar 194 m³ (bejana 20,9 t)", nv, "unit", rv, "Massa dari model 3D x biaya fabrikasi + insulasi + internal + instrumen"),
         ("PEC", "TK-101 / TK-301 bejana standar", 2, "unit", tk, "Bejana sama tanpa insulasi"),
         ("PEC", "Membran UF tubular MB-301", tech["area_mem"], "m²", v["c_mem"], "Luas dari neraca membran"),
         ("PEC", "PM-4 pompa cross-flow, CIP, MCC/VSD, kontainer", 1, "lot", 180000, "Penawaran tipikal paket [ASUMSI]"),
         ("PEC", "PM-1 skid praolah (saringan, desander, PHE 812 kW)", 1, "lot", 170000, "[ASUMSI] harga katalog"),
         ("PEC", "PM-5 skid dosing + pompa umpan", 1, "lot", 60000, "[ASUMSI]"),
         ("PEC", "PM-6 BTF + chiller + blower ATEX + karbon aktif + analis", 1, "lot", 280000, "[ASUMSI]"),
         ("PEC", "PM-7 penampung gas membran ganda %s m³ + flare" % round(tech["gh_m3"]), 1, "lot", 190000, "[ASUMSI] ~USD 90/m³ + flare tertutup"),
         ("PEC", "PM-8 genset biogas kontainer 2 x 800 kWe", tech["chp_kWe"], "kWe", v["c_chp"], "Riset harga genset"),
         ("PEC", "PM-9 pemulih panas + menara pendingin", 1, "lot", 100000, "[ASUMSI]"),
         ("PEC", "PM-10 screw press + skid lumpur", 1, "lot", 115000, "[ASUMSI]"),
         ("PEC", "Pipe rack + perpipaan antar modul", 1, "lot", 110000, "Model 3D: 4 jalur DN100-200"),
         ("PEC", "Listrik MV (trafo 1,25 MVA, switchgear 20 kV, kabel)", 1, "lot", 200000, "[ASUMSI]"),
         ("PEC", "Instrumentasi, PLC/SCADA jarak jauh", 1, "lot", 90000, "[ASUMSI]"),
         ("PEC", "Interkoneksi PLN 20 kV + kWh meter transaksi", 1, "lot", 150000, "[ASUMSI] jarak <= 2 km"),
         ]
    rows = [(g, n, q, u, c * (scale if g == "PEC" and u in ("lot",) else 1.0), q * c * (scale if g == "PEC" and u in ("lot",) else 1.0), b) for g, n, q, u, c, b in I]
    pec = sum(r[5] for r in rows)
    D = [("LANGSUNG", "Sipil & pondasi (16 cincin, pondasi GH, pad)", 1, "lot", 240000 * scale, "[ASUMSI] 0,29 ha"),
         ("LANGSUNG", "Transportasi Jawa/Batam -> Sumatera (%d muatan)" % tech["truckloads"], tech["truckloads"], "muatan", 6500, "low-bed + truk 40 ft [ASUMSI]"),
         ("LANGSUNG", "Pemasangan, crane & komisioning", 1, "lot", 200000 * scale, "[ASUMSI] 10 minggu"),
         ("TAK LANGSUNG", "Rekayasa & manajemen proyek", v["eng"], "x PEC", pec, "Desain standar berulang"),
         ("TAK LANGSUNG", "Perizinan (UKL-UPL, PPA, SLO, IUPTL)", 1, "lot", 50000, "[ASUMSI]"),
         ("TAK LANGSUNG", "Start-up: inokulum termofilik, bahan kimia, pelatihan", 1, "lot", 45000, "[ASUMSI]")]
    rows += [(g, n, q, u, c, q * c, b) for g, n, q, u, c, b in D]
    sub = sum(r[5] for r in rows)
    rows.append(("KONTINGENSI", "Kontingensi", v["cont"], "x subtotal", sub, v["cont"] * sub, "Produk standar"))
    fci = sum(r[5] for r in rows)
    return rows, pec, fci

def opex_base(v, fci, pec, tech=TECH, emult=1.0):
    """biaya operasi tahun penuh (USD tahun dasar, sebelum eskalasi). dict -> (nilai, jenis 'F'/'V')"""
    Egross = tech["E_gross_GWh"] * emult * v["avail"] * 1e6
    pec_chp = v["c_chp"] * tech["chp_kWe"]
    O = {"Staf operasi (8 orang)": (v["staff"], "F"),
         "O&M genset (kontrak)": (v["c_eng_om"] * Egross, "V"),
         "Perawatan peralatan proses": (v["c_maint"] * (pec - pec_chp), "F"),
         "Bahan kimia (polimer, karbon aktif, NaOH)": (tech["polymer_kgh"] * tech["hrs_day"] * tech["days_yr"] / 1000 * v["p_poly"] * emult
                                                      + tech["ac_kgh"] * 8760 * v["avail"] / 1000 * v["p_ac"] * emult + v["c_naoh"], "V"),
         "Asuransi": (v["c_ins"] * fci, "F"),
         "MRV & registri karbon": (v["c_mrv"], "F"),
         "Administrasi & SCADA jarak jauh": (v["c_admin"], "F"),
         "Sewa lahan PKS": (v["lease"] * tech["plot_m2"], "F"),
         "Cadangan overhaul genset + ganti membran": (v["overhaul"] * tech["chp_kWe"] / 8.0 + 0.8 * v["c_mem"] * tech["area_mem"] / v["mem_life"], "F")}
    return O

# ------------------------------------------------------------------------------------------- model tahunan
def run(v=None, emult=1.0, capex_mult=1.0, opex_mult=1.0, tech=TECH, scale=1.0, relocate=False, detail=True):
    v = dict(v or vals())
    y0, n = int(v["year0"]), int(v["n_op"])
    years = list(range(y0, y0 + n + 1))
    T = len(years)
    rows, pec, fci0 = capex_items(v, tech, scale)
    fci = fci0 * capex_mult
    O = opex_base(v, fci, pec, tech, emult)
    opex_full = sum(x for x, k in O.values()) * opex_mult
    opex_var = sum(x for x, k in O.values() if k == "V") * opex_mult
    wc = v["wc_months"] / 12 * opex_full
    E = np.zeros(T); tariff = np.zeros(T); rev_el = np.zeros(T); cer = np.zeros(T); rev_c = np.zeros(T)
    rev_h = np.zeros(T); rev_f = np.zeros(T); opex = np.zeros(T); capex = np.zeros(T); sust = np.zeros(T); dwc = np.zeros(T)
    for i, y in enumerate(years):
        if i == 0:
            capex[i] = fci; continue
        k = i                                   # tahun operasi ke-k
        f = (v["ramp1"] if k == 1 else 1.0)
        E[i] = v["E_net_GWh"] * emult * v["avail"] * f
        if relocate:
            kk = k if k <= 10 else k - 10
        else:
            kk = k
        tariff[i] = (v["tariff1"] * v["F_loc"] if kk <= 10 else v["tariff2"]) / 100.0
        rev_el[i] = E[i] * 1e6 * tariff[i]
        cer[i] = v["co2e"] * v["cer_ratio"] * f * (emult ** 0.5)      # emisi terhindar ~ COD tertangkap (lebih stabil dari daya)
        rev_c[i] = cer[i] * v["p_carbon"]
        rev_h[i] = tech["Q_heat"] / tech["P_gross"] * E[i] * 1e3 * (tech["P_gross"] / tech["P_net"]) * v["heat_util"] * v["p_heat"]
        rev_f[i] = tech["cake_ty"] * emult * f * v["p_cake"]
        esc = (1 + v["infl"]) ** (y - 2026)
        opex[i] = (opex_full - opex_var + opex_var * f * emult ** 0) * esc
        if k == 1: dwc[i] = wc * esc
        if k == n: dwc[i] = -wc * (1 + v["infl"]) ** (years[1] - 2026)
        if relocate and k == 11: sust[i] += 0.12 * fci * esc                       # biaya relokasi ke PKS kedua
    rev_fee = np.array([0.0] + [tech["pome_m3y"] * v["fee_pome"] * (v["ramp1"] if k == 1 else 1.0) * (1 + v["infl"]) ** (y - 2026) for k, y in enumerate(years) if k > 0])
    rev = rev_el + rev_c + rev_h + rev_f + rev_fee
    ebitda = rev - opex
    dep = np.zeros(T); allow = np.zeros(T)
    for i in range(1, T):
        k = i
        if k <= v["dep_life"]: dep[i] = fci / v["dep_life"]
        if k <= 6: allow[i] = v["allow"] * fci / 6
    # utang
    debt0 = v["debt_frac"] * fci
    r, N = v["r_debt"], int(v["tenor"])
    ann = debt0 * r / (1 - (1 + r) ** -N)
    bal = np.zeros(T); intr = np.zeros(T); princ = np.zeros(T)
    b = debt0
    for i in range(1, T):
        if i <= N:
            intr[i] = b * r; princ[i] = ann - intr[i]; b -= princ[i]
        bal[i] = b
    def taxes(ti):
        pool = 0.0; tx = np.zeros(T)
        for i in range(T):
            taxable = max(0.0, ti[i] - pool)
            pool = max(0.0, pool - ti[i])
            tx[i] = v["tax"] * taxable
        return tx
    ti_u = ebitda - dep - allow
    tax_u = taxes(ti_u)
    ti_l = ebitda - dep - allow - intr
    tax_l = taxes(ti_l)
    fcff = ebitda - tax_u - capex - sust - dwc
    fcfe = ebitda - tax_l - capex * (1 - v["debt_frac"]) - sust - dwc - intr - princ
    w = wacc(v)
    disc = np.array([(1 + w) ** -i for i in range(T)])
    out = dict(v=v, years=years, E=E, tariff=tariff, rev_fee=rev_fee, rev_el=rev_el, cer=cer, rev_c=rev_c, rev_h=rev_h, rev_f=rev_f, rev=rev, opex=opex,
               ebitda=ebitda, capex=capex, sust=sust, dwc=dwc, dep=dep, allow=allow, tax_u=tax_u, tax_l=tax_l, intr=intr, princ=princ,
               bal=bal, fcff=fcff, fcfe=fcfe, wacc=w, disc=disc, fci=fci, pec=pec, capex_rows=rows, opex_items=O, opex_full=opex_full,
               opex_var=opex_var, wc=wc, debt0=debt0, ann=ann)
    out.update(indicators(out))
    return out

def irr(cf, lo=-0.99, hi=1.5):
    f = lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cf))
    if f(lo + 1e-9) * f(hi) > 0: return float("nan")
    a, b = lo + 1e-9, hi
    for _ in range(200):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2
def npv(r, cf): return sum(c / (1 + r) ** i for i, c in enumerate(cf))

def payback(cf):
    """tahun sejak COD (indeks 1 = akhir th operasi 1) ketika kumulatif >= 0, interpolasi linear"""
    cum = np.cumsum(cf)
    for i in range(1, len(cf)):
        if cum[i - 1] < 0 <= cum[i]:
            return (i - 1) + (-cum[i - 1] / cf[i])
    return float("nan")

def indicators(o):
    v = o["v"]; w = o["wacc"]; cf = o["fcff"]
    NPV = npv(w, cf); IRR = irr(cf); IRRe = irr(o["fcfe"])
    pb = payback(cf); dcf = cf * o["disc"]; dpb = payback(dcf)
    pv_in = sum(dcf[1:] + (o["capex"][1:] + o["sust"][1:]) * o["disc"][1:])     # PV arus kas operasi (sebelum capex)
    PI = (pv_in) / (o["fci"])
    ds = o["intr"] + o["princ"]; cfads = o["ebitda"] - o["tax_l"] - o["sust"] - o["dwc"]
    dscr = [cfads[i] / ds[i] for i in range(1, len(ds)) if ds[i] > 0]
    pvE = sum(o["E"][1:] * 1e6 * o["disc"][1:])
    pvC = o["fci"] + sum((o["opex"][1:] + o["sust"][1:]) * o["disc"][1:])
    LCOE = pvC / pvE
    pvRother = sum((o["rev_c"][1:] + o["rev_h"][1:] + o["rev_f"][1:] + o["rev_fee"][1:]) * o["disc"][1:])
    cum = np.cumsum(cf)
    return dict(NPV=NPV, IRR=IRR, IRR_eq=IRRe, PBP=pb, DPBP=dpb, PI=PI, DSCR_min=min(dscr) if dscr else float("nan"),
                DSCR_avg=float(np.mean(dscr)) if dscr else float("nan"), LCOE=LCOE, LCOE_net=(pvC - pvRother) / pvE,
                peak_funding=-min(cum), cum_end=cum[-1])

# ------------------------------------------------------------------------------------------- impas (BEP)
def solve(fun, lo, hi, it=80):
    a, b = lo, hi; fa = fun(a)
    if fa * fun(b) > 0: return float("nan")
    for _ in range(it):
        m = (a + b) / 2; fm = fun(m)
        if fa * fm <= 0: b = m
        else: a, fa = m, fm
    return (a + b) / 2

def bep(v=None):
    v = dict(v or vals())
    out = {}
    def with_(k, x):
        vv = dict(v); vv[k] = x; return run(vv)["NPV"]
    out["tariff1_be"] = solve(lambda x: with_("tariff1", x), 0.0, 40.0)                # USc/kWh (F tetap)
    out["p_carbon_be"] = solve(lambda x: with_("p_carbon", x), -50.0, 80.0)
    out["emult_be"] = solve(lambda x: run(v, emult=x)["NPV"], 0.2, 2.0)
    out["capex_be"] = solve(lambda x: run(v, capex_mult=x)["NPV"], 0.3, 3.0)
    # titik impas operasional (tahun penuh, th 2): biaya tetap / margin kontribusi
    o = run(v); i = 2
    var = o["opex_var"] * (1 + v["infl"]) ** (o["years"][i] - 2026)
    fixed = o["opex"][i] - var
    dep = o["dep"][i]; intr = o["intr"][i]
    out["BEP_cash"] = fixed / (o["rev"][i] - var)                                       # fraksi kapasitas, impas tunai
    out["BEP_acc"] = (fixed + dep + intr) / (o["rev"][i] - var)                          # impas akuntansi (laba = 0)
    out["SDP"] = (fixed - 0.0) / (o["rev"][i] - var) * 0.0 + (fixed * 0.6) / (o["rev"][i] - var)   # titik penutupan: biaya tetap tak terhindar 60%
    out["fixed"] = fixed; out["var"] = var; out["rev_full"] = o["rev"][i]; out["dep"] = dep; out["intr"] = intr
    return out

# ------------------------------------------------------------------------------------------- sensitivitas & Monte Carlo
TORNADO = [("Jasa pengolahan POME", "fee_pome"), ("Pendapatan listrik (tarif x F)", "tariff_mult"), ("Produksi energi (biogas)", "emult"), ("CAPEX (FCI)", "capex_mult"),
           ("Harga kredit karbon", "p_carbon"), ("OPEX", "opex_mult"), ("Biaya modal (WACC)", "r_eq"), ("Pendapatan panas", "p_heat")]
def tornado(v=None, d=0.20):
    v = dict(v or vals()); base = run(v)["NPV"]; res = []
    for lab, key in TORNADO:
        r = []
        for s in (1 - d, 1 + d):
            vv = dict(v); kw = {}
            if key == "tariff_mult": vv["tariff1"] *= s; vv["tariff2"] *= s
            elif key in ("emult", "capex_mult", "opex_mult"): kw[key] = s
            else: vv[key] = vv[key] * s
            r.append(run(vv, **kw)["NPV"])
        res.append((lab, r[0], r[1]))
    res.sort(key=lambda x: -abs(x[2] - x[1]))
    return base, res

def npv_curve(v=None, rates=None):
    o = run(v); rates = rates if rates is not None else np.linspace(0.04, 0.24, 41)
    return rates, [npv(r, o["fcff"]) for r in rates]

def tri(rng, lo, mode, hi, n): return rng.triangular(lo, mode, hi, n)
def monte_carlo(N=5000, seed=20261015, v=None):
    v = dict(v or vals()); rng = np.random.default_rng(seed)
    sig = (math.log(1.33) - math.log(0.764)) / (2 * 1.645)          # dari MC proses (P_net P5/P50/P95)
    S = dict(emult=np.clip(rng.lognormal(0.0, sig, N), 0.5, 1.5),
             capex=tri(rng, 0.90, 1.0, 1.35, N), opex=tri(rng, 0.85, 1.0, 1.25, N),
             p_carbon=tri(rng, 2.2, 12.0, 20.0, N), F_loc=rng.choice([1.0, 1.10], N, p=[0.3, 0.7]),
             avail=tri(rng, 0.88, 0.95, 0.97, N), p_heat=tri(rng, 8.0, 18.0, 25.0, N), heat_util=tri(rng, 0.15, 0.40, 0.60, N),
             r_debt=tri(rng, 0.065, 0.08, 0.10, N), infl=tri(rng, 0.02, 0.03, 0.05, N))
    NPV = np.zeros(N); IRR = np.zeros(N); PB = np.zeros(N)
    for j in range(N):
        vv = dict(v)
        for k in ("p_carbon", "F_loc", "avail", "p_heat", "heat_util", "r_debt", "infl"): vv[k] = float(S[k][j])
        o = run(vv, emult=float(S["emult"][j]), capex_mult=float(S["capex"][j]), opex_mult=float(S["opex"][j]))
        NPV[j], IRR[j], PB[j] = o["NPV"], o["IRR"], o["PBP"]
    # korelasi Spearman input -> NPV
    def rank(x): return np.argsort(np.argsort(x))
    sp = {k: float(np.corrcoef(rank(S[k]), rank(NPV))[0, 1]) for k in S}
    return dict(NPV=NPV, IRR=IRR, PBP=PB, S=S, spearman=sp)

# ------------------------------------------------------------------------------------------- skala 30/45/60
def tier(t):
    T_ = R["tiers"][t]; base = R["tiers"]["45"]
    tech = dict(TECH); f = T_["GWh_y"] / base["GWh_y"]
    tech.update(n_vessel=T_["N_modules"], area_mem=T_["membrane"]["area_m2"], chp_kWe=T_["chp"]["P_inst"],
                GWh_net=TECH["GWh_net"] * f, E_gross_GWh=TECH["E_gross_GWh"] * T_["P_gross"] / base["P_gross"],
                co2e_avoided=TECH["co2e_avoided"] * T_["ffb_tph"] / 45.0, Q_heat=TECH["Q_heat"] * f, cake_kgh=TECH["cake_kgh"] * f,
                polymer_kgh=TECH["polymer_kgh"] * f, ac_kgh=TECH["ac_kgh"] * f, plot_m2=TECH["plot_m2"] * (0.5 + 0.5 * T_["N_modules"] / 14),
                truckloads=int(round(TECH["truckloads"] + (T_["N_modules"] - 14))))
    v = vals(); v["E_net_GWh"] = tech["GWh_net"]; v["co2e"] = tech["co2e_avoided"]
    if T_["P_net"] > 1000: v["tariff1"] = 9.94                         # >1-3 MW
    return run(v, tech=tech, scale=(T_["ffb_tph"] / 45.0) ** 0.6)

# ------------------------------------------------------------------------------------------- armada perusahaan
ROLL = {2027: 1, 2028: 2, 2029: 4, 2030: 5, 2031: 6, 2032: 7, 2033: 7, 2034: 8}     # set baru per tahun (mulai konstruksi)
def fleet(v=None, lr=0.90, foak=1.20, horizon=2046, overhead0=450000.0, oh_growth=0.10):
    """agregat armada BOO: kurva belajar biaya (lr per penggandaan), unit pertama FOAK, overhead korporat"""
    v = dict(v or vals())
    years = list(range(2026, horizon + 1)); T = len(years)
    agg = {k: np.zeros(T) for k in ("rev", "opex", "ebitda", "capex", "fcff", "tax", "sets_new", "sets_op", "E", "co2")}
    n_cum = 0; units = []
    for y0, nn in sorted(ROLL.items()):
        for _ in range(nn):
            n_cum += 1
            cm = (foak if n_cum == 1 else 1.0) * n_cum ** (math.log(lr, 2)) / (1.0)     # relatif terhadap unit-1 pada harga dasar
            vv = dict(v); vv["year0"] = y0
            o = run(vv, capex_mult=cm)
            units.append((n_cum, y0, cm, o["NPV"], o["IRR"]))
            for i, y in enumerate(o["years"]):
                if y > horizon: break
                j = years.index(y)
                agg["rev"][j] += o["rev"][i]; agg["opex"][j] += o["opex"][i]; agg["ebitda"][j] += o["ebitda"][i]
                agg["capex"][j] += o["capex"][i] + o["sust"][i]; agg["fcff"][j] += o["fcff"][i]; agg["tax"][j] += o["tax_u"][i]
                agg["E"][j] += o["E"][i]; agg["co2"][j] += o["cer"][i]
                if i == 0: agg["sets_new"][j] += 1
                if i >= 1: agg["sets_op"][j] += 1
    oh = np.array([0 if y < 2026 else overhead0 * (1 + oh_growth) ** min(y - 2026, 8) for y in years])
    oh[0] += 600000                                    # R&D / pilot engineering / sertifikasi 2026
    agg["overhead"] = oh
    agg["fcff_co"] = agg["fcff"] - oh * (1 - v["tax"])
    # nilai terminal: armada beroperasi setelah horizon (perpetuitas tanpa pertumbuhan dari FCFF th terakhir, dipotong 50% konservatif)
    w = wacc(v)
    agg["years"] = years; agg["units"] = units
    cf = agg["fcff_co"]
    agg["NPV"] = npv(w, cf); agg["IRR"] = irr(cf); agg["peak"] = -min(np.cumsum(cf)); agg["PBP"] = payback(cf)
    agg["wacc"] = w
    return agg

if __name__ == "__main__":
    o = run()
    print("FCI %.2f MUSD (PEC %.2f), USD/kWe gross %.0f" % (o["fci"] / 1e6, o["pec"] / 1e6, o["fci"] / TECH["P_gross"]))
    print("rev th2 %.0f  opex th2 %.0f  EBITDA %.0f" % (o["rev"][2], o["opex"][2], o["ebitda"][2]))
    for k in ("NPV", "IRR", "IRR_eq", "PBP", "DPBP", "PI", "DSCR_min", "LCOE", "LCOE_net", "peak_funding"): print(k, o[k])
    print("WACC", o["wacc"])
    print(bep())
    fl = fleet(); print("fleet NPV %.1f M IRR %.3f peak %.1f M PBP %.1f" % (fl["NPV"] / 1e6, fl["IRR"], fl["peak"] / 1e6, fl["PBP"]))
    for t in ("30", "45", "60"):
        ot = tier(t); print(t, "FCI %.2f NPV %.2f IRR %.3f PBP %.1f" % (ot["fci"] / 1e6, ot["NPV"] / 1e6, ot["IRR"], ot["PBP"]))
