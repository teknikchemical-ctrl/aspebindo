# -*- coding: utf-8 -*-
"""
Model keuangan inti v2 (USD nominal) - Generator Biogas Portabel AnMBR termofilik untuk PKS.
Satu sumber kebenaran untuk Excel (fin_excel.py), gambar (fin_figs.py) dan laporan (fin_report.py).

Model bisnis: BOO per set standar di lahan PKS (kontrak 20 th). Aliran pendapatan:
  (1) jasa pengolahan POME & kepatuhan (USD/t TBS) dibayar PKS - penangkapan metana adalah syarat akses pasar
      ISCC-EU/RED II dan CORSIA (SAF) bagi minyak sawit; PKS juga terbebas dari 1,1 ha kolam anaerobik,
  (2) listrik ke jaringan internal PKS di luar jam olah (menggantikan genset diesel),
  (3) sisa listrik diekspor ke PLN (Perpres 112/2022, kontrak <= 1 MW),
  (4) kredit karbon penghindaran metana (periode kredit 10 th, harga pasar sukarela rendah).
Basis volume tunggal: 45 t/jam x 20 jam x 300 hari x faktor beban PKS (util). Data teknis dari
process/outputs/results.json, luas plot dari cad/out/ga.json, panjang pipa/kabel dari cad/out/site.json.
Perbaikan v2 mengikuti audit (lihat finance/README.md).
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
R = json.load(open(os.path.join(ROOT, "process", "outputs", "results.json"), encoding="utf-8"))
def _js(p, d):
    try: return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
    except Exception: return d
GA = _js("cad/out/ga.json", {"plot_m2": 3387.0})
SITE = _js("cad/out/site.json", {"routes": {}, "land_freed_m2": 11081.0})

# ------------------------------------------------------------------------------------------- teknis
_mon = np.array(R["year"]["monthly_net_MWh"]); _f = _mon / _mon.mean()
TECH = dict(
    ffb_tph=R["design_basis"]["ffb_tph"], hrs_day=R["design_basis"]["hrs_day"], days_yr=R["design_basis"]["days_yr"],
    pome_m3d=R["design_basis"]["pome_m3d"], P_gross=R["energy"]["P_gross"], P_net=R["energy"]["P_net"], P_par=R["energy"]["P_par"],
    Q_heat=R["energy"]["Q_heat_avail"], n_vessel=R["tiers"]["45"]["N_modules"], area_mem=R["equipment"]["membrane"]["area_m2"],
    chp_kWe=R["equipment"]["chp"]["installed_kWe"], gh_m3=R["equipment"]["gas_holder"]["V_m3"],
    base_t=R["emissions"]["base_t"], proj_t=R["emissions"]["proj_t"], B0=R["EMIS"]["B0"], GWP=R["EMIS"]["GWP_CH4"],
    cod_eff_kgd=R["nominal"]["cod_routing_kgd"]["Organik terlarut (efluen)"] + R["nominal"]["cod_routing_kgd"]["CH4/H2S terlarut"],
    cake_kgh=[s for s in R["streams"] if s["id"] == 12][0]["kg_h"], polymer_kgh=[s for s in R["streams"] if s["id"] == 26][0]["kg_h"],
    ac_kgh=[s for s in R["streams"] if s["id"] == 25][0]["kg_h"], plot_m2=GA.get("plot_m2", 3387.0),
    vessel_t=20.9, tank_t=20.0, truckloads=json.load(open(os.path.join(ROOT, "process", "outputs", "portable_modules.json")))["ship_units_total"],
    month_f=_f.tolist())
TECH["E_nom_GWh"] = TECH["P_net"] * 24 * TECH["days_yr"] / 1e6           # energi neto pada 100% beban PKS (gas hanya dari POME hari olah)
TECH["pome_m3y_nom"] = TECH["pome_m3d"] * TECH["days_yr"]
TECH["ffb_ty_nom"] = TECH["ffb_tph"] * TECH["hrs_day"] * TECH["days_yr"]
TECH["cake_ty_nom"] = TECH["cake_kgh"] * TECH["hrs_day"] * TECH["days_yr"] / 1000.0
TECH["eff_t_nom"] = TECH["cod_eff_kgd"] * TECH["days_yr"] / 1000.0      # t COD/th efluen ke kolam polishing
SR = SITE.get("routes", {})
TECH["site_lines"] = [(v["label"], round(v["L_m"]), v["cost_m"], v["cost"]) for k, v in SR.items()]

# ------------------------------------------------------------------------------------------- asumsi
# (nilai, satuan, sumber/catatan, rendah, tinggi)
A = {
    "year0": (2027, "tahun", "Tahun konstruksi (fabrikasi bengkel 8 bln + pasang 3 bln); COD awal 2028", None, None),
    "n_op": (20, "tahun", "Umur operasi kontrak BOO", None, None),
    "util": (0.92, "-", "Faktor beban PKS thd kapasitas 45 t/jam (results.json, asumsi 'util')", 0.80, 1.0),
    "avail": (0.97, "-", "Ketersediaan CHP: 2 x 800 kWe, satu unit memikul 73% beban rata-rata + GH 2 jam", 0.93, 0.985),
    "ramp1": (0.75, "-", "Faktor produksi tahun operasi 1 (start-up biomassa termofilik ~3 bln)", 0.60, 0.90),
    "cap_kW": (1000.0, "kW", "Kapasitas kontrak ekspor PLN di titik serah (tier Perpres 112 <= 1 MW)", None, None),
    # offtake listrik
    "captive_kW": (150.0, "kW", "Beban PKS di luar jam olah (perumahan, kantor, pompa air, bengkel) [ASUMSI]", 100.0, 250.0),
    "captive_h": (2448.0, "jam/th", "4 jam/hari x 300 hari + 52 Minggu x 24 jam", None, None),
    "p_captive": (0.18, "USD/kWh", "Diskon thd biaya listrik genset diesel PKS Rp4.000-5.000/kWh (Dexlite Rp23.700/L)", 0.12, 0.24),
    "tariff1": (10.18, "USc/kWh", "Perpres 112/2022 Lamp. I PLTBg <= 1 MW, th 1-10 (CNBC/Katadata 2022)", 9.81, 10.18),
    "F_loc": (1.10, "-", "Faktor lokasi F Sumatera ~1,10 [perlu verifikasi]", 1.00, 1.10),
    "tariff2": (6.11, "USc/kWh", "Perpres 112/2022 PLTBg <= 1 MW, th 11 dst (tanpa F)", 5.89, 6.11),
    # jasa pengolahan & kepatuhan
    "fee_ffb": (2.00, "USD/t TBS", "Jasa pengolahan POME + kepatuhan (ISCC/CORSIA butuh penangkapan metana) [ASUMSI kontrak]", 0.0, 2.5),
    # karbon
    "p_carbon": (5.0, "USD/tCO2e", "Penghindaran metana: Platts 3,8 / MSCI BBB+ 6,8 USD (2024-25); IDXCarbon ~3", 2.0, 12.0),
    "cer_ratio": (0.90, "-", "Rasio penerbitan (ketidakpastian, kebocoran)", 0.80, 0.95),
    "MCF_eff": (0.30, "-", "MCF kolam polishing penerima efluen (fakultatif 3 m) [IPCC 0,2-0,8]", 0.2, 0.8),
    "carbon_years": (10, "tahun", "Periode kredit tetap 10 th (Verra/GS)", None, None),
    "c_val": (60000.0, "USD", "Validasi + registrasi + PDD (sekali, th operasi 1)", 40000.0, 90000.0),
    "c_levy": (0.23, "USD/t", "Pungutan penerbitan Verra 2025", None, None),
    # makro
    "infl": (0.02, "/th", "Eskalasi biaya & harga dalam USD", 0.015, 0.035),
    "fx": (17855.0, "IDR/USD", "Kurs 22 Sep 2026", None, None),
    # CAPEX
    "c_fab": (2.5, "USD/kg", "Bejana CS difabrikasi + dilapis (1,8-4,0)", 2.0, 3.2),
    "c_mem": (200.0, "USD/m2", "Membran UF tubular PVDF (100-300) [ASUMSI]", 150.0, 280.0),
    "c_chp": (550.0, "USD/kWe", "Genset biogas kontainer (Asia 350-600; Eropa 700-1.100)", 450.0, 800.0),
    "cont": (0.10, "-", "Kontingensi produk standar", 0.05, 0.20),
    "eng": (0.05, "-", "Rekayasa & manajemen proyek (desain berulang)", 0.05, 0.12),
    "c_grid": (120000.0, "USD", "Switchgear 20 kV + kWh meter transaksi + saluran ke jaringan PLN <= 2 km", 80000.0, 250000.0),
    "vat": (0.11, "-", "PPN efektif atas CAPEX (restitusi th operasi 2)", None, None),
    # OPEX
    "c_eng_om": (0.012, "USD/kWh-kotor", "O&M genset kontrak (tanpa overhaul)", 0.010, 0.018),
    "c_maint": (0.02, "-/th x PEC non-genset", "Perawatan peralatan proses", 0.015, 0.03),
    "c_ins": (0.005, "-/th x FCI", "Asuransi all-risk", None, None),
    "staff": (82000.0, "USD/th", "10 orang: manajer, lab/K3, 8 operator (4 regu x 2) - 14 bln gaji + BPJS", 70000.0, 100000.0),
    "c_mrv": (25000.0, "USD/th", "Pemantauan + verifikasi karbon (selama periode kredit)", 15000.0, 35000.0),
    "c_admin": (30000.0, "USD/th", "Administrasi SPV, SCADA jarak jauh, audit", None, None),
    "lease": (2.0, "USD/m2/th", "Sewa lahan plot di PKS (dari GA 3D)", None, None),
    "p_poly": (4000.0, "USD/t", "Polimer kationik", None, None),
    "p_ac": (3000.0, "USD/t", "Karbon aktif impregnasi KI", None, None),
    "c_naoh": (8000.0, "USD/th", "Cadangan NaOH/urea (dosis P95)", None, None),
    "overhaul": (150.0, "USD/kWe", "Overhaul besar genset th operasi 8 & 16 (60.000 jam)", 120.0, 220.0),
    "mem_repl": (0.80, "x biaya membran", "Ganti elemen membran th 8 & 15 (rumah dipakai ulang)", None, None),
    # pajak & pendanaan
    "tax": (0.22, "-", "PPh badan", None, None),
    "dep_life": (8, "tahun", "Penyusutan dipercepat PP 78/2019 (1/2 umur kelompok 3)", None, None),
    "allow": (0.30, "-", "Tax allowance PP 78/2019: 30% aset berwujud, 5%/th x 6 th", None, None),
    "loss_cf": (10, "tahun", "Kompensasi rugi fiskal PP 78/2019 (maks 10 th)", None, None),
    "debt_frac": (0.60, "-", "Porsi utang proyek", None, None),
    "r_debt": (0.08, "/th", "Bunga pinjaman hijau USD", 0.065, 0.10),
    "tenor": (10, "tahun", "Tenor (th operasi 1 bunga saja, anuitas th 2-10)", None, None),
    "fee_debt": (0.015, "-", "Biaya upfront pinjaman", None, None),
    "dsra_m": (6.0, "bulan", "Rekening cadangan layanan utang (DSRA)", None, None),
    "r_eq": (0.15, "/th", "Biaya ekuitas", None, None),
    "rec_days": (60.0, "hari", "Piutang PLN/PKS", None, None),
    "pay_days": (30.0, "hari", "Utang usaha", None, None),
}
def V(a, k): return a[k][0] if isinstance(a[k], tuple) else a[k]
def vals(a=A): return {k: V(a, k) for k in a}
def wacc(v): return v["debt_frac"] * v["r_debt"] * (1 - v["tax"]) + (1 - v["debt_frac"]) * v["r_eq"]

def cap_factor(v, tech=TECH, emult=1.0):
    """fraksi energi yang dapat diekspor di bawah kapasitas kontrak (profil musiman bulanan dari simulasi tahunan)"""
    P = tech["P_net"] * v["util"] * emult * np.array(tech["month_f"])
    return float(np.minimum(P, v["cap_kW"]).mean() / P.mean())

def carbon_t(v, tech=TECH, emult=1.0):
    """pengurangan emisi tahunan (tCO2e): baseline kolam - emisi proyek (CHP/flare/bocor) - efluen ke kolam polishing"""
    eff = tech["eff_t_nom"] * v["util"] * emult * tech["B0"] * v["MCF_eff"] * tech["GWP"]
    return (tech["base_t"] - tech["proj_t"]) * v["util"] * emult - eff, eff

# ------------------------------------------------------------------------------------------- CAPEX
def capex_items(v, tech=TECH, scale=1.0):
    nv = tech["n_vessel"]
    rv = v["c_fab"] * tech["vessel_t"] * 1000 + 12000 + 7500 + 10000
    tk = v["c_fab"] * tech["tank_t"] * 1000 + 6000
    s = lambda c: c * scale
    I = [("PEC", "Reaktor AnMBR standar 194 m³ (bejana 20,9 t dari model 3D)", nv, "unit", rv, "Massa 3D x biaya fabrikasi + insulasi + internal + instrumen"),
         ("PEC", "TK-101 / TK-301 bejana standar", 2, "unit", tk, "Bejana sama tanpa insulasi"),
         ("PEC", "Membran UF tubular MB-301", tech["area_mem"], "m²", v["c_mem"], "Luas dari neraca membran"),
         ("PEC", "PM-4 pompa cross-flow, CIP, MCC/VSD, kontainer", 1, "lot", s(180000), "Paket tipikal [ASUMSI]"),
         ("PEC", "PM-1 skid praolah (saringan, desander, PHE 812 kW)", 1, "lot", s(170000), "[ASUMSI]"),
         ("PEC", "PM-5 skid dosing + pompa umpan", 1, "lot", s(60000), "[ASUMSI]"),
         ("PEC", "PM-6 BTF + chiller + blower ATEX + karbon aktif + analis", 1, "lot", s(280000), "[ASUMSI]"),
         ("PEC", "PM-7 penampung gas membran ganda %s m³ + flare" % round(tech["gh_m3"]), 1, "lot", s(190000), "~USD 90/m³ + flare tertutup"),
         ("PEC", "PM-8 genset biogas kontainer 2 x %d kWe" % round(tech["chp_kWe"] / 2), tech["chp_kWe"], "kWe", v["c_chp"], "Riset harga genset"),
         ("PEC", "PM-9 pemulih panas + menara pendingin", 1, "lot", s(100000), "[ASUMSI]"),
         ("PEC", "PM-10 screw press + skid lumpur", 1, "lot", s(115000), "[ASUMSI]"),
         ("PEC", "Pipe rack + perpipaan antar modul", 1, "lot", s(110000), "Model 3D: 4 jalur DN100-200"),
         ("PEC", "Listrik (trafo 1,25 MVA 0,4/20 kV, switchgear, kabel)", 1, "lot", s(200000), "[ASUMSI]"),
         ("PEC", "Instrumentasi, PLC/SCADA jarak jauh", 1, "lot", s(90000), "[ASUMSI]")]
    rows = [(g, n, q, u, c, q * c, b) for g, n, q, u, c, b in I]
    pec = sum(r[5] for r in rows)
    D = [("LANGSUNG", "Sipil & pondasi (16 cincin, pondasi GH, pad)", 1, "lot", s(240000), "Plot %s m² (GA 3D)" % round(tech["plot_m2"])),
         ("LANGSUNG", "Transportasi bengkel -> Sumatera (%d muatan)" % tech["truckloads"], tech["truckloads"], "muatan", 6500, "low-bed + truk 40 ft"),
         ("LANGSUNG", "Pemasangan, crane & komisioning", 1, "lot", s(200000), "10 minggu")]
    for lab, L_, cm, c in tech["site_lines"]:
        D.append(("LANGSUNG", "Lokasi: " + lab, L_, "m", c / max(L_, 1), "Panjang dari model 3D lokasi (site.json)"))
    D.append(("LANGSUNG", "Interkoneksi PLN: switchgear 20 kV, meter transaksi, jaringan <= 2 km", 1, "lot", v["c_grid"], "[ASUMSI]"))
    D += [("TAK LANGSUNG", "Rekayasa & manajemen proyek", v["eng"], "x PEC", pec, "Desain standar berulang"),
          ("TAK LANGSUNG", "Perizinan (UKL-UPL, PPA, SLO, IUPTL)", 1, "lot", 50000, "[ASUMSI]"),
          ("TAK LANGSUNG", "Start-up: inokulum termofilik, bahan kimia, pelatihan", 1, "lot", 45000, "[ASUMSI]")]
    rows += [(g, n, q, u, c, q * c, b) for g, n, q, u, c, b in D]
    sub = sum(r[5] for r in rows)
    rows.append(("KONTINGENSI", "Kontingensi", v["cont"], "x subtotal", sub, v["cont"] * sub, "Produk standar"))
    fci = sum(r[5] for r in rows)
    tangible = (sum(r[5] for r in rows if r[0] in ("PEC", "LANGSUNG"))) * (1 + v["cont"])
    return rows, pec, fci, tangible

def opex_base(v, fci, pec, tech=TECH, emult=1.0):
    """biaya operasi tahun penuh, USD 2026. -> {nama: (nilai, 'F'/'V')}"""
    Eg = tech["E_nom_GWh"] * v["util"] * emult * v["avail"] * tech["P_gross"] / tech["P_net"] * 1e6
    return {"Staf operasi (10 orang)": (v["staff"], "F"),
            "O&M genset (kontrak)": (v["c_eng_om"] * Eg, "V"),
            "Perawatan peralatan proses": (v["c_maint"] * (pec - v["c_chp"] * tech["chp_kWe"]), "F"),
            "Bahan kimia (polimer, karbon aktif, NaOH)": (tech["polymer_kgh"] * tech["hrs_day"] * tech["days_yr"] * v["util"] * emult / 1000 * v["p_poly"]
                                                         + tech["ac_kgh"] * 24 * tech["days_yr"] * v["util"] * emult / 1000 * v["p_ac"] + v["c_naoh"], "V"),
            "Asuransi": (v["c_ins"] * fci, "F"),
            "Administrasi & SCADA jarak jauh": (v["c_admin"], "F"),
            "Sewa lahan plot di PKS": (v["lease"] * tech["plot_m2"], "F")}

# ------------------------------------------------------------------------------------------- model tahunan
def run(v=None, emult=1.0, capex_mult=1.0, opex_mult=1.0, tech=TECH, scale=1.0, relocate=False):
    v = dict(v or vals())
    y0, n = int(v["year0"]), int(v["n_op"])
    years = list(range(y0, y0 + n + 1)); T = len(years)
    rows, pec, fci26, tang26 = capex_items(v, tech, scale)
    cesc = (1 + v["infl"]) ** (y0 - 2026)
    fci = fci26 * capex_mult * cesc; tang = tang26 * capex_mult * cesc
    O = opex_base(v, fci26 * capex_mult, pec * capex_mult, tech, emult)
    opF = sum(x for x, k in O.values() if k == "F") * opex_mult
    opV = sum(x for x, k in O.values() if k == "V") * opex_mult
    capf = cap_factor(v, tech, emult)
    ER, eff_t = carbon_t(v, tech, emult)
    Z = lambda: np.zeros(T)
    f_ = Z(); E = Z(); Ecap = Z(); Eexp = Z(); tar = Z(); rev_cap = Z(); rev_exp = Z(); rev_fee = Z(); cer = Z(); rev_c = Z()
    opex = Z(); c_carb = Z(); capex = Z(); sust = Z(); vat = Z(); tar_c = Z()
    capex[0] = fci; vat[0] = v["vat"] * fci
    if T > 2: vat[2] = -v["vat"] * fci
    for i in range(1, T):
        y = years[i]; k = i; esc = (1 + v["infl"]) ** (y - 2026)
        kk = (k - 10 if (relocate and k > 10) else k)
        f = v["ramp1"] if kk == 1 else 1.0
        if relocate and k == 11: f = 0.5 * v["ramp1"]                 # 6 bln bongkar-angkut-pasang + start-up ulang
        f_[i] = f
        E[i] = tech["E_nom_GWh"] * v["util"] * emult * v["avail"] * f
        Ecap[i] = min(v["captive_kW"] * v["captive_h"] / 1e6 * (1 if f >= 1 else f), E[i])
        Eexp[i] = (E[i] - Ecap[i]) * capf
        tar[i] = (v["tariff1"] * v["F_loc"] if kk <= 10 else v["tariff2"]) / 100.0
        tar_c[i] = v["p_captive"] * esc
        rev_cap[i] = Ecap[i] * 1e6 * tar_c[i]; rev_exp[i] = Eexp[i] * 1e6 * tar[i]
        rev_fee[i] = tech["ffb_ty_nom"] * v["util"] * emult ** 0 * v["fee_ffb"] * esc * (0.5 if (relocate and k == 11) else 1.0)
        vint = ER * v["cer_ratio"] * f if kk <= v["carbon_years"] else 0.0   # vintage tahun ini
        cer[i] = vint
        c_carb[i] = (v["c_mrv"] * esc if kk <= v["carbon_years"] + 1 else 0.0) + (v["c_val"] * esc if kk == 1 else 0.0)
        opex[i] = (opF + opV * (E[i] / (tech["E_nom_GWh"] * v["util"] * v["avail"]))) * esc
        if k in (8, 16): sust[i] += v["overhaul"] * tech["chp_kWe"] * esc
        if k in (8, 15): sust[i] += v["mem_repl"] * v["c_mem"] * tech["area_mem"] * esc
        if relocate and k == 11: sust[i] += 0.12 * fci26 * esc
    # kredit karbon diterima 1 tahun setelah vintage, dikurangi pungutan penerbitan
    for i in range(1, T):
        iss = cer[i - 1] if i >= 2 else 0.0
        rev_c[i] = iss * (v["p_carbon"] - v["c_levy"]) * (1 + v["infl"]) ** (years[i] - 2026) * 0 + iss * (v["p_carbon"] - v["c_levy"])
    rev = rev_cap + rev_exp + rev_fee + rev_c
    opex_tot = opex + c_carb
    ebitda = rev - opex_tot
    # modal kerja
    wc = rev * v["rec_days"] / 365 - opex_tot * v["pay_days"] / 365
    wc[-1] = 0.0
    dwc = np.diff(np.concatenate([[0.0], wc]))
    # pendanaan
    debt_c = v["debt_frac"] * fci; idc = debt_c * v["r_debt"] * 0.5
    debt0 = debt_c + idc
    r, N = v["r_debt"], int(v["tenor"])
    ann = debt0 * r / (1 - (1 + r) ** -(N - 1))                       # masa tenggang pokok 1 th
    bal = Z(); intr = Z(); princ = Z(); b = debt0; bal[0] = b
    for i in range(1, T):
        if i <= N:
            intr[i] = b * r; princ[i] = (ann - intr[i]) if i >= 2 else 0.0; b -= princ[i]
        bal[i] = b
    dsra = Z(); dsra[1] = ann * v["dsra_m"] / 12; dsra[min(N, T - 1)] -= ann * v["dsra_m"] / 12
    upfront = Z(); upfront[0] = v["fee_debt"] * debt0
    # pajak (penyusutan dipercepat 8 th; sustaining capex disusutkan 8 th; tax allowance; kompensasi rugi maks loss_cf th)
    dep = Z(); allow = Z()
    base_dep = fci + idc
    for i in range(1, T):
        if i <= v["dep_life"]: dep[i] += base_dep / v["dep_life"]
        if i <= 6: allow[i] = v["allow"] * tang / 6
        for j in range(1, i + 1):
            if sust[j] and i - j < 8: dep[i] += sust[j] / 8
    def taxes(ti):
        pools = []; tx = Z()
        for i in range(T):
            pools = [(age + 1, amt) for age, amt in pools if age + 1 <= v["loss_cf"]]
            x = ti[i]
            if x < 0: pools.append((0, -x)); continue
            for kq in range(len(pools)):
                use = min(pools[kq][1], x); pools[kq] = (pools[kq][0], pools[kq][1] - use); x -= use
            pools = [p for p in pools if p[1] > 1e-6]
            tx[i] = v["tax"] * x
        return tx
    ti_u = ebitda - dep - allow; tax_u = taxes(ti_u)
    ti_l = ti_u - intr - np.where(np.arange(T) == 1, upfront[0], 0.0); tax_l = taxes(ti_l)
    fcff = ebitda - tax_u - capex - sust - vat - dwc
    fcfe = ebitda - tax_l - capex * (1 - v["debt_frac"]) - sust - vat - dwc - intr - princ - upfront - dsra
    # cadangan perawatan (MRA) untuk DSCR: biaya sustaining disebar rata selama umur proyek
    mra = np.where(np.arange(T) >= 1, sust.sum() / n, 0.0)
    cfads = ebitda - tax_l - dwc - mra
    w = wacc(v); disc = np.array([(1 + w) ** -i for i in range(T)])
    out = dict(v=v, years=years, f=f_, E=E, Ecap=Ecap, Eexp=Eexp, tariff=tar, tar_c=tar_c, rev_cap=rev_cap, rev_exp=rev_exp, rev_el=rev_cap + rev_exp,
               rev_fee=rev_fee, cer=cer, rev_c=rev_c, rev=rev, opex=opex, c_carb=c_carb, opex_tot=opex_tot, ebitda=ebitda, capex=capex, sust=sust, vat=vat,
               wc=wc, dwc=dwc, dep=dep, allow=allow, tax_u=tax_u, tax_l=tax_l, intr=intr, princ=princ, bal=bal, dsra=dsra, upfront=upfront, mra=mra,
               cfads=cfads, fcff=fcff, fcfe=fcfe, wacc=w, disc=disc, fci=fci, fci26=fci26 * capex_mult, pec=pec, tang=tang, idc=idc, debt0=debt0, ann=ann,
               capex_rows=rows, opex_items=O, opF=opF, opV=opV, capf=capf, ER=ER, eff_t=eff_t)
    out.update(indicators(out))
    return out

# ------------------------------------------------------------------------------------------- indikator
def irr(cf):
    """IRR kokoh: akar riil polinom NPV(x=1/(1+r)) dengan r dalam [-0,5; 1,5]; NaN bila tidak ada"""
    cf = np.asarray(cf, float)
    if not (cf.min() < 0 < cf.max()): return float("nan")
    roots = np.roots(cf[::-1])                # sum c_i x^i -> koefisien derajat tertinggi dulu
    rs = []
    for z in roots:
        if abs(z.imag) < 1e-9 and z.real > 0:
            r = 1 / z.real - 1
            if -0.5 <= r <= 1.5: rs.append(r)
    if not rs: return float("nan")
    return min(rs, key=lambda r: abs(r - 0.1))
def npv(r, cf): return float(sum(c / (1 + r) ** i for i, c in enumerate(cf)))
def payback(cf):
    cum = np.cumsum(cf); last = float("nan")
    for i in range(1, len(cf)):
        if cum[i - 1] < 0 <= cum[i]: last = (i - 1) + (-cum[i - 1] / cf[i])
    return last if (cum[-1] >= 0) else float("nan")
def indicators(o):
    w = o["wacc"]; cf = o["fcff"]; d = o["disc"]
    ds = o["intr"] + o["princ"]
    dscr = [o["cfads"][i] / ds[i] for i in range(1, len(ds)) if ds[i] > 0]
    pvE = float(sum(o["E"] * 1e6 * d)); pvC = o["fci"] + float(sum((o["opex_tot"] + o["sust"]) * d))
    pv_nonel = float(sum((o["rev_fee"] + o["rev_c"]) * d))
    cum = np.cumsum(cf)
    return dict(NPV=npv(w, cf), IRR=irr(cf), IRR_eq=irr(o["fcfe"]), PBP=payback(cf), DPBP=payback(cf * d),
                PI=float(sum(cf[1:] * d[1:])) / o["fci"], DSCR_min=min(dscr) if dscr else float("nan"), DSCR_avg=float(np.mean(dscr)) if dscr else float("nan"),
                LCOE=pvC / pvE, LCOE_net=(pvC - pv_nonel) / pvE, peak_funding=float(-cum.min()), cum_end=float(cum[-1]),
                share_fee=float(sum(o["rev_fee"])) / float(sum(o["rev"])), share_el=float(sum(o["rev_el"])) / float(sum(o["rev"])),
                share_c=float(sum(o["rev_c"])) / float(sum(o["rev"])))

# ------------------------------------------------------------------------------------------- impas
def solve(fun, lo, hi, it=70):
    a, b = lo, hi; fa = fun(a)
    if fa * fun(b) > 0: return float("nan")
    for _ in range(it):
        m = (a + b) / 2; fm = fun(m)
        if fa * fm <= 0: b = m
        else: a, fa = m, fm
    return (a + b) / 2
def bep(v=None):
    v = dict(v or vals()); out = {}
    def w_(k, x): vv = dict(v); vv[k] = x; return run(vv)["NPV"]
    out["fee_be"] = solve(lambda x: w_("fee_ffb", x), 0.0, 6.0)
    out["tariff1_be"] = solve(lambda x: w_("tariff1", x), 0.0, 40.0)
    out["p_carbon_be"] = solve(lambda x: w_("p_carbon", x), -40.0, 100.0)
    out["emult_be"] = solve(lambda x: run(v, emult=x)["NPV"], 0.05, 1.2)
    out["capex_be"] = solve(lambda x: run(v, capex_mult=x)["NPV"], 0.3, 3.0)
    o = run(v); i = 2
    var = o["opV"] * (1 + v["infl"]) ** (o["years"][i] - 2026)
    fixed = o["opex_tot"][i] - var
    vol = o["rev_el"][i] + o["rev_c"][i]                    # pendapatan yang berskala dengan produksi gas
    fee = o["rev_fee"][i]
    out["BEP_cash"] = max(0.0, (fixed - fee) / (vol - var))
    dep_book = o["fci"] / v["n_op"]                           # penyusutan buku garis lurus (bukan penyusutan fiskal dipercepat)
    out["BEP_acc"] = max(0.0, (fixed + dep_book + o["intr"][i] - fee) / (vol - var))
    out.update(fixed=fixed, var=var, vol=vol, fee=fee, rev_full=o["rev"][i], dep=dep_book, intr=o["intr"][i])
    out["fee_be_cpo"] = out["fee_be"] / 0.21                 # USD/t CPO (OER 21%)
    return out

# ------------------------------------------------------------------------------------------- sensitivitas & Monte Carlo
TORNADO = [("Jasa pengolahan POME (USD/t TBS)", "fee_ffb"), ("Tarif PLN (x F)", "tariff_mult"), ("Produksi biogas/energi", "emult"),
           ("CAPEX", "capex_mult"), ("OPEX", "opex_mult"), ("Harga karbon", "p_carbon"), ("Biaya ekuitas", "r_eq"), ("Harga listrik ke PKS", "p_captive"),
           ("Faktor beban PKS", "util")]
def tornado(v=None, d=0.20):
    v = dict(v or vals()); base = run(v)["NPV"]; res = []
    for lab, key in TORNADO:
        r = []
        for s in (1 - d, 1 + d):
            vv = dict(v); kw = {}
            if key == "tariff_mult": vv["tariff1"] *= s; vv["tariff2"] *= s
            elif key in ("emult", "capex_mult", "opex_mult"): kw[key] = s
            elif key == "util": vv[key] = min(1.0, vv[key] * s)
            else: vv[key] = vv[key] * s
            r.append(run(vv, **kw)["NPV"])
        res.append((lab, r[0], r[1]))
    res.sort(key=lambda x: -abs(x[2] - x[1]))
    return base, res
def npv_curve(v=None, rates=None):
    o = run(v); rates = rates if rates is not None else np.linspace(0.04, 0.24, 41)
    return rates, [npv(r, o["fcff"]) for r in rates]
def tri(rng, lo, mode, hi, n): return rng.triangular(lo, mode, hi, n)
MC_DIST = dict(emult="Lognormal median 1, P5-P95 0,76-1,33 (MC proses daya neto)", capex="Segitiga 0,90 / 1,00 / 1,30", opex="Segitiga 0,90 / 1,00 / 1,20",
               p_carbon="Segitiga 2 / 5 / 12 USD/t", F_loc="Diskrit 1,00 (30%) / 1,10 (70%)", tier="25%: tier >1 MW (9,81 / 5,89 USc)",
               fee="Segitiga 0,75 / 1,00 / 1,25 x dasar", avail="Segitiga 0,93 / 0,97 / 0,985", ramp1="Segitiga 0,60 / 0,75 / 0,90",
               cer_ratio="Segitiga 0,80 / 0,90 / 0,95", r_debt="Segitiga 6,5 / 8 / 10%", infl="Segitiga 1,5 / 2 / 3,5%", util="Segitiga 0,82 / 0,92 / 0,98")
def monte_carlo(N=4000, seed=20261015, v=None):
    v = dict(v or vals()); rng = np.random.default_rng(seed)
    sig = (math.log(1.33) - math.log(0.764)) / (2 * 1.645)
    S = dict(emult=np.clip(rng.lognormal(0.0, sig, N), 0.5, 1.6), capex=tri(rng, 0.90, 1.0, 1.30, N), opex=tri(rng, 0.90, 1.0, 1.20, N),
             p_carbon=tri(rng, 2.0, 5.0, 12.0, N), F_loc=rng.choice([1.0, 1.10], N, p=[0.3, 0.7]), tier=(rng.random(N) < 0.25).astype(float),
             fee=tri(rng, 0.75, 1.0, 1.25, N), avail=tri(rng, 0.93, 0.97, 0.985, N), ramp1=tri(rng, 0.6, 0.75, 0.9, N),
             cer_ratio=tri(rng, 0.8, 0.9, 0.95, N), r_debt=tri(rng, 0.065, 0.08, 0.10, N), infl=tri(rng, 0.015, 0.02, 0.035, N), util=tri(rng, 0.82, 0.92, 0.98, N))
    NPV = np.zeros(N); IRR = np.zeros(N); PB = np.zeros(N)
    for j in range(N):
        vv = dict(v)
        for k in ("p_carbon", "F_loc", "avail", "ramp1", "cer_ratio", "r_debt", "infl", "util"): vv[k] = float(S[k][j])
        vv["fee_ffb"] = v["fee_ffb"] * float(S["fee"][j])
        if S["tier"][j]: vv["tariff1"], vv["tariff2"] = 9.81, 5.89
        o = run(vv, emult=float(S["emult"][j]), capex_mult=float(S["capex"][j]), opex_mult=float(S["opex"][j]))
        NPV[j], IRR[j], PB[j] = o["NPV"], o["IRR"], o["PBP"]
    rank = lambda x: np.argsort(np.argsort(x))
    sp = {k: float(np.corrcoef(rank(S[k]), rank(NPV))[0, 1]) for k in S}
    return dict(NPV=NPV, IRR=IRR, PBP=PB, S=S, spearman=sp)
def pct(x, q, fill=-1.0):
    """persentil dengan kasus gagal (NaN = tidak ada IRR / tidak balik modal) dihitung sebagai nilai terburuk"""
    x = np.where(np.isfinite(x), x, fill); return float(np.percentile(x, q))

# ------------------------------------------------------------------------------------------- skala 30/45/60
def tier(t):
    T_ = R["tiers"][t]; b = R["tiers"]["45"]; f = T_["ffb_tph"] / 45.0
    tech = dict(TECH)
    tech.update(n_vessel=T_["N_modules"], area_mem=T_["membrane"]["area_m2"], chp_kWe=T_["chp"]["P_inst"], P_net=T_["P_net"], P_gross=T_["P_gross"],
                E_nom_GWh=T_["P_net"] * 24 * TECH["days_yr"] / 1e6, ffb_tph=T_["ffb_tph"], ffb_ty_nom=TECH["ffb_ty_nom"] * f, base_t=TECH["base_t"] * f,
                proj_t=TECH["proj_t"] * f, eff_t_nom=TECH["eff_t_nom"] * f, cake_kgh=TECH["cake_kgh"] * f, polymer_kgh=TECH["polymer_kgh"] * f,
                ac_kgh=TECH["ac_kgh"] * f, plot_m2=TECH["plot_m2"] * (0.5 + 0.5 * T_["N_modules"] / 14), truckloads=int(round(TECH["truckloads"] + (T_["N_modules"] - 14))))
    v = vals()
    if T_["P_net"] * v["util"] > 1000: v["tariff1"], v["tariff2"], v["cap_kW"] = 9.81, 5.89, 3000.0
    return run(v, tech=tech, scale=f ** 0.6)

# ------------------------------------------------------------------------------------------- armada perusahaan
ROLL = {2027: 1, 2028: 2, 2029: 4, 2030: 5, 2031: 6, 2032: 7, 2033: 7, 2034: 8}
LEARN_SHARE = 0.60          # porsi FCI yang turun dengan kurva belajar (bejana, skid, rekayasa, pemasangan); genset/membran/tranpor tidak
def fleet(v=None, lr=0.90, foak=1.20, overhead0=450000.0, oh_growth=0.10):
    v = dict(v or vals())
    last = max(ROLL) + int(v["n_op"]); years = list(range(2026, last + 1)); T = len(years)
    agg = {k: np.zeros(T) for k in ("rev", "opex", "ebitda", "capex", "fcff", "tax", "sets_new", "sets_op", "E", "co2", "rev_fee", "rev_el", "rev_c")}
    n_cum = 0; units = []
    for y0, nn in sorted(ROLL.items()):
        for _ in range(nn):
            n_cum += 1
            cm = (foak if n_cum == 1 else 1.0) * (LEARN_SHARE * n_cum ** math.log(lr, 2) + 1 - LEARN_SHARE)
            vv = dict(v); vv["year0"] = y0
            o = run(vv, capex_mult=cm)
            units.append((n_cum, y0, cm, o["NPV"], o["IRR"], o["fci"]))
            for i, y in enumerate(o["years"]):
                j = years.index(y)
                for k_, src in (("rev", "rev"), ("opex", "opex_tot"), ("ebitda", "ebitda"), ("fcff", "fcff"), ("tax", "tax_u"), ("E", "E"), ("co2", "cer"),
                                ("rev_fee", "rev_fee"), ("rev_el", "rev_el"), ("rev_c", "rev_c")):
                    agg[k_][j] += o[src][i]
                agg["capex"][j] += o["capex"][i] + o["sust"][i]
                if i == 0: agg["sets_new"][j] += 1
                else: agg["sets_op"][j] += 1
    oh = np.array([overhead0 * (1 + oh_growth) ** min(y - 2026, 8) * (1 + v["infl"]) ** max(0, y - 2034) for y in years])
    oh[0] += 600000.0                                       # R&D, pilot, sertifikasi 2026
    agg["overhead"] = oh
    agg["fcff_co"] = agg["fcff"] - oh                       # overhead HoldCo tanpa perisai pajak (tidak ada konsolidasi fiskal)
    w = wacc(v); cf = agg["fcff_co"]
    agg.update(years=years, units=units, NPV=npv(w, cf), IRR=irr(cf), peak=float(-np.cumsum(cf).min()), PBP=payback(cf), wacc=w)
    return agg

if __name__ == "__main__":
    o = run()
    print("FCI 2027 %.2f M (2026 %.2f; PEC %.2f) | USD/kWe kotor %.0f | capf %.3f | ER %.0f t (efluen %.0f)" % (o["fci"] / 1e6, o["fci26"] / 1e6, o["pec"] / 1e6, o["fci26"] / TECH["P_gross"], o["capf"], o["ER"], o["eff_t"]))
    i = 2
    print("th2: E %.2f GWh (PKS %.2f, PLN %.2f) | fee %.0f el %.0f karbon %.0f | rev %.0f opex %.0f EBITDA %.0f" % (o["E"][i], o["Ecap"][i], o["Eexp"][i], o["rev_fee"][i], o["rev_el"][i], o["rev_c"][i], o["rev"][i], o["opex_tot"][i], o["ebitda"][i]))
    for k in ("NPV", "IRR", "IRR_eq", "PBP", "DPBP", "PI", "DSCR_min", "LCOE", "LCOE_net", "peak_funding", "share_fee", "share_el", "share_c"): print(k, round(o[k], 4) if o[k] == o[k] else o[k])
    print("WACC", o["wacc"]); print({k: round(x, 3) for k, x in bep().items()})
    vv = vals(); vv["fee_ffb"] = 0; o0 = run(vv); print("tanpa jasa: NPV %.2f IRR %s" % (o0["NPV"] / 1e6, o0["IRR"]))
    fl = fleet(); print("armada NPV %.1f M IRR %.3f puncak %.1f M PBP %.1f" % (fl["NPV"] / 1e6, fl["IRR"], fl["peak"] / 1e6, fl["PBP"]))
    for t in ("30", "45", "60"):
        ot = tier(t); print(t, "FCI %.2f NPV %.2f IRR %.3f PBP %.1f" % (ot["fci"] / 1e6, ot["NPV"] / 1e6, ot["IRR"], ot["PBP"]))
