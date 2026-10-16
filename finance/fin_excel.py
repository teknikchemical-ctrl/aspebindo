# -*- coding: utf-8 -*-
"""Buku kerja Excel model keuangan v2 dengan RUMUS HIDUP (xlsxwriter): Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator.
Nilai Python disimpan sebagai cache rumus; verify() menghitung ulang dengan LibreOffice dan membandingkan."""
import os, subprocess, tempfile
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name as coln
import fin_core as F, fin_market as MK

OUT = os.path.join(F.HERE, "outputs", "BG_Model_Keuangan.xlsx")

def build(RES):
    o, be, mc, fl = RES["o"], RES["be"], RES["mc"], RES["fl"]
    v = o["v"]; T_ = F.TECH
    wb = xlsxwriter.Workbook(OUT)
    H = wb.add_format(dict(bold=True, bg_color="#1f4e4a", font_color="white", border=1, text_wrap=True, valign="vcenter"))
    TT = wb.add_format(dict(bold=True, font_size=14, font_color="#1f4e4a")); B = wb.add_format(dict(bold=True))
    INP = wb.add_format(dict(bg_color="#fff2cc", border=1, num_format="#,##0.00##"))
    NUM = wb.add_format(dict(num_format="#,##0", border=1)); NUM2 = wb.add_format(dict(num_format="#,##0.00", border=1)); NUM4 = wb.add_format(dict(num_format="0.0000", border=1))
    PCT = wb.add_format(dict(num_format="0.0%", border=1)); TXT = wb.add_format(dict(border=1, text_wrap=True, valign="top"))
    BNUM = wb.add_format(dict(bold=True, num_format="#,##0", border=1, bg_color="#e2efda")); BPCT = wb.add_format(dict(bold=True, num_format="0.0%", border=1, bg_color="#e2efda"))
    BN2 = wb.add_format(dict(bold=True, num_format="#,##0.00", border=1, bg_color="#e2efda"))
    NEG = wb.add_format(dict(num_format="#,##0;[Red]-#,##0", border=1)); BNEG = wb.add_format(dict(bold=True, num_format="#,##0;[Red]-#,##0", border=1, bg_color="#e2efda"))
    NOTE = wb.add_format(dict(italic=True, font_color="#555555", text_wrap=True))
    ws0 = wb.add_worksheet("Ringkasan")

    # ====================================================== Asumsi
    wa = wb.add_worksheet("Asumsi"); wa.set_column(0, 0, 14); wa.set_column(1, 1, 13); wa.set_column(2, 3, 15); wa.set_column(4, 4, 96)
    wa.write(0, 0, "ASUMSI MODEL v2 (sel kuning = input; seluruh model ikut berubah)", TT)
    wa.write_row(2, 0, ["Nama", "Nilai", "Satuan", "Rendah / Tinggi", "Sumber / catatan"], H)
    r = 3
    for k, (val, unit, src, lo, hi) in F.A.items():
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), INP); wa.write(r, 2, unit, TXT)
        wa.write(r, 3, "" if lo is None else "%s / %s" % (lo, hi), TXT); wa.write(r, 4, src, TXT)
        wb.define_name("a_" + k, "=Asumsi!$B$%d" % (r + 1)); r += 1
    r += 1; wa.write(r, 0, "DATA TEKNIS & LOKASI (dihitung dari results.json, ga.json, site.json - bukan input)", B); r += 1
    TK = [("P_gross", T_["P_gross"], "kWe", "Daya kotor genset"), ("P_net", T_["P_net"], "kWe", "Daya neto pada 100% beban PKS"),
          ("E_nom", T_["E_nom_GWh"], "GWh/th", "P_net x 24 jam x 300 hari"),
          ("poly", T_["polymer_kgh"], "kg/jam", "Polimer (neraca massa)"), ("ac", T_["ac_kgh"], "kg/jam", "Karbon aktif (neraca massa)"),
          ("base", T_["base_t"], "tCO2e/th", "Baseline kolam terbuka pada 100% beban (results.json)"), ("proj", T_["proj_t"], "tCO2e/th", "Emisi proyek: slip CHP, flare, bocor"),
          ("effCOD", T_["eff_t_nom"], "t COD/th", "COD efluen ke kolam polishing pada 100% beban"), ("B0", T_["B0"], "kg CH4/kg COD", "IPCC"), ("GWP", T_["GWP"], "-", "GWP CH4"),
          ("ffb", T_["ffb_ty_nom"], "t TBS/th", "45 t/jam x 20 jam x 300 hari (dikali util)"), ("chp_kWe", T_["chp_kWe"], "kWe", "Genset terpasang"),
          ("area_mem", T_["area_mem"], "m2", "Luas membran"), ("plot_m2", T_["plot_m2"], "m2", "Luas plot dari GA 3D")]
    for k, val, unit, src in TK:
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), NUM4 if val < 10 else NUM2); wa.write(r, 2, unit); wa.write(r, 4, src)
        wb.define_name("t_" + k, "=Asumsi!$B$%d" % (r + 1)); r += 1
    r += 0; wa.write(r, 0, "ER"); wa.write_formula(r, 1, "=(t_base-t_proj)*a_util-t_effCOD*a_util*t_B0*a_MCF_eff*t_GWP", NUM, o["ER"])
    wa.write(r, 4, "Pengurangan emisi neto tCO2e/th (baseline - proyek - efluen ke kolam polishing)"); wb.define_name("t_ER", "=Asumsi!$B$%d" % (r + 1)); r += 1
    # faktor ekspor di bawah kapasitas kontrak: profil musiman bulanan (simulasi tahunan proses)
    r += 1; wa.write(r, 0, "Profil musiman (faktor bulan)", B); wa.write(r + 1, 0, "Daya neto bulan (kW)", B); wa.write(r + 2, 0, "Terekspor <= kontrak (kW)", B)
    for j, fm in enumerate(T_["month_f"]):
        cc = coln(1 + j)
        wa.write_number(r, 1 + j, fm, NUM4)
        wa.write_formula(r + 1, 1 + j, "=t_P_net*a_util*%s%d" % (cc, r + 1), NUM, T_["P_net"] * v["util"] * fm)
        wa.write_formula(r + 2, 1 + j, "=MIN(%s%d,a_cap_kW)" % (cc, r + 2), NUM, min(T_["P_net"] * v["util"] * fm, v["cap_kW"]))
    wa.write(r + 3, 0, "capf"); wa.write_formula(r + 3, 1, "=SUM(B%d:M%d)/SUM(B%d:M%d)" % (r + 3, r + 3, r + 2, r + 2), NUM4, o["capf"])
    wa.write(r + 3, 4, "Fraksi energi yang dapat diekspor di bawah kapasitas kontrak PLN")
    wb.define_name("t_capf", "=Asumsi!$B$%d" % (r + 4)); r += 5
    wa.write(r, 0, "WACC"); wa.write_formula(r, 1, "=a_debt_frac*a_r_debt*(1-a_tax)+(1-a_debt_frac)*a_r_eq", BPCT, o["wacc"]); wb.define_name("WACC", "=Asumsi!$B$%d" % (r + 1))

    # ====================================================== CAPEX
    wc = wb.add_worksheet("CAPEX"); wc.set_column(0, 0, 14); wc.set_column(1, 1, 66); wc.set_column(2, 5, 14); wc.set_column(6, 6, 56)
    wc.write(0, 0, "CAPEX 1 set standar 45 t TBS/jam (USD 2026; dieskalasi ke tahun konstruksi)", TT)
    wc.write_row(2, 0, ["Kelompok", "Item", "Jumlah", "Satuan", "Harga satuan USD", "Total USD", "Dasar"], H)
    r = 3; first = r; pec_r = []; tang_r = []
    unit_f = {0: "=a_c_fab*%s*1000+29500" % T_["vessel_t"], 1: "=a_c_fab*%s*1000+6000" % T_["tank_t"], 2: "=a_c_mem", 8: "=a_c_chp"}
    for i, (g, n, q, u, c, t, b) in enumerate(o["capex_rows"]):
        wc.write(r, 0, g, TXT); wc.write(r, 1, n, TXT); wc.write(r, 3, u, TXT); wc.write(r, 6, b, TXT)
        if n.startswith("Rekayasa"):
            wc.write_formula(r, 2, "=a_eng", NUM4, q); wc.write_formula(r, 4, "=PEC", NUM, c)
        elif g == "KONTINGENSI":
            wc.write_formula(r, 2, "=a_cont", NUM4, q); wc.write_formula(r, 4, "=SUM(F%d:F%d)" % (first + 1, r), NUM, c)
        else:
            wc.write_number(r, 2, q, NUM2)
            if g == "PEC" and i in unit_f: wc.write_formula(r, 4, unit_f[i], NUM, c)
            elif n.startswith("Interkoneksi PLN"): wc.write_formula(r, 4, "=a_c_grid", NUM, c)
            else: wc.write_number(r, 4, c, INP)
        wc.write_formula(r, 5, "=C%d*E%d" % (r + 1, r + 1), NUM, t)
        if g == "PEC": pec_r.append(r)
        if g in ("PEC", "LANGSUNG"): tang_r.append(r)
        r += 1
    last = r - 1
    names = [("PEC (peralatan terbeli)", "=SUM(F%d:F%d)" % (pec_r[0] + 1, pec_r[-1] + 1), o["pec"], "PEC"),
             ("FCI 2026", "=SUM(F%d:F%d)" % (first + 1, last + 1), o["fci26"], "FCI26"),
             ("FCI tahun konstruksi (eskalasi)", "=FCI26*(1+a_infl)^(a_year0-2026)", o["fci"], "FCI"),
             ("Aset berwujud (basis tax allowance)", "=SUM(F%d:F%d)*(1+a_cont)*(1+a_infl)^(a_year0-2026)" % (tang_r[0] + 1, tang_r[-1] + 1), o["tang"], "TANG"),
             ("USD per kWe kotor (2026)", "=FCI26/t_P_gross", o["fci26"] / T_["P_gross"], None),
             ("Bunga selama konstruksi (IDC)", "=a_debt_frac*FCI*a_r_debt*0.5", o["idc"], "IDC"),
             ("Pinjaman (termasuk IDC)", "=a_debt_frac*FCI+IDC", o["debt0"], "DEBT"),
             ("Anuitas th 2-10", "=DEBT*a_r_debt/(1-(1+a_r_debt)^-(a_tenor-1))", o["ann"], "ANN")]
    for j, (lab, f, val, nm) in enumerate(names):
        rr = r + 1 + j; wc.write(rr, 1, lab, B); wc.write_formula(rr, 5, f, BNUM, val)
        if nm: wb.define_name(nm, "=CAPEX!$F$%d" % (rr + 1))
    wc.write(r + 2 + len(names), 1, "Pembanding: PLTBg POME 1,8-3,0 juta USD/MW (MDPI 2025; Suka Damai 2,4 MW; Energies 2022 rata-rata 2.758 USD/kW).", NOTE)

    # ====================================================== OPEX
    wo = wb.add_worksheet("OPEX"); wo.set_column(0, 0, 46); wo.set_column(1, 2, 16); wo.set_column(3, 3, 80)
    wo.write(0, 0, "OPEX tahun penuh (USD 2026, pada beban util x avail) - dieskalasi di Arus Kas", TT)
    wo.write_row(2, 0, ["Komponen", "USD/th", "Jenis", "Rumus"], H)
    FORM = {"Staf operasi (10 orang)": "=a_staff", "O&M genset (kontrak)": "=a_c_eng_om*t_E_nom*a_util*a_avail*t_P_gross/t_P_net*1000000",
            "Perawatan peralatan proses": "=a_c_maint*(PEC-a_c_chp*t_chp_kWe)", "Asuransi": "=a_c_ins*FCI26",
            "Administrasi & SCADA jarak jauh": "=a_c_admin", "Sewa lahan plot di PKS": "=a_lease*t_plot_m2"}
    r = 3; fr = []; vr = []
    for k, (val, typ) in o["opex_items"].items():
        wo.write(r, 0, k, TXT)
        if k in FORM: wo.write_formula(r, 1, FORM[k], NUM, val); wo.write(r, 3, FORM[k][1:], TXT)
        else:
            fchem = "=t_poly*%d*%d*a_util/1000*a_p_poly+t_ac*24*%d*a_util/1000*a_p_ac+a_c_naoh" % (T_["hrs_day"], T_["days_yr"], T_["days_yr"])
            wo.write_formula(r, 1, fchem, NUM, val); wo.write(r, 3, fchem[1:], TXT)
        wo.write(r, 2, typ, TXT); (fr if typ == "F" else vr).append(r); r += 1
    wo.write(r + 1, 0, "Biaya tetap (F)", B); wo.write_formula(r + 1, 1, "=" + "+".join("B%d" % (x + 1) for x in fr), BNUM, o["opF"])
    wo.write(r + 2, 0, "Biaya variabel (V)", B); wo.write_formula(r + 2, 1, "=" + "+".join("B%d" % (x + 1) for x in vr), BNUM, o["opV"])
    wb.define_name("OPEX_F", "=OPEX!$B$%d" % (r + 2)); wb.define_name("OPEX_V", "=OPEX!$B$%d" % (r + 3))
    wo.write(r + 4, 0, "Biaya karbon (MRV tahunan + validasi sekali) dan sustaining capex dihitung per tahun di Arus Kas.", NOTE)

    # ====================================================== Arus Kas
    wf = wb.add_worksheet("Arus Kas"); wf.set_column(0, 0, 44); wf.set_column(1, 1, 3); wf.freeze_panes(3, 2)
    wf.write(0, 0, "MODEL ARUS KAS PROYEK v2 (USD nominal; negatif = keluar). 1 set 45 t TBS/jam, BOO", TT)
    yrs = o["years"]; nY = len(yrs); C0 = 2; wf.set_column(C0, C0 + nY - 1, 11.5)
    rows = {}
    col = lambda i: coln(C0 + i)
    def row(key, label, fn_, py=None, fmt=NEG, bold=False):
        rr = len(rows) + 3; rows[key] = rr; wf.write(rr, 0, label, B if bold else None)
        for i in range(nY):
            f = fn_(i); val = float(py[i]) if py is not None and np.isfinite(py[i]) else 0.0
            if isinstance(f, (int, float)): wf.write_number(rr, C0 + i, f, fmt)
            else: wf.write_formula(rr, C0 + i, f, BNEG if bold else fmt, val)
    R_ = lambda key, i: "%s%d" % (col(i), rows[key] + 1)
    wf.write(2, 0, "Tahun", H); wf.write(2, 1, "", H)
    for i, y in enumerate(yrs): wf.write(2, C0 + i, y, H)
    k_ = lambda i: R_("k", i); esc = lambda i: "(1+a_infl)^(%s-2026)" % R_("yr", i)
    row("k", "Tahun operasi ke-", lambda i: i, fmt=NUM)
    row("yr", "Tahun kalender", lambda i: yrs[i], fmt=NUM)
    row("f", "Faktor operasi (ramp-up)", lambda i: "=IF(%s=0,0,IF(%s=1,a_ramp1,1))" % (k_(i), k_(i)), o["f"], NUM2)
    row("E", "Listrik neto (GWh)", lambda i: "=t_E_nom*a_util*a_avail*%s" % R_("f", i), o["E"], NUM2)
    row("Ecap", "  ke PKS di luar jam olah (GWh)", lambda i: "=MIN(a_captive_kW*a_captive_h/1000000*IF(%s>=1,1,%s),%s)" % (R_("f", i), R_("f", i), R_("E", i)), o["Ecap"], NUM2)
    row("Eexp", "  ekspor ke PLN (GWh)", lambda i: "=(%s-%s)*t_capf" % (R_("E", i), R_("Ecap", i)), o["Eexp"], NUM2)
    row("tar", "Tarif PLN (USD/kWh)", lambda i: "=IF(%s=0,0,IF(%s<=10,a_tariff1*a_F_loc,a_tariff2)/100)" % (k_(i), k_(i)), o["tariff"], NUM4)
    row("tarc", "Harga listrik ke PKS (USD/kWh)", lambda i: "=IF(%s=0,0,a_p_captive*%s)" % (k_(i), esc(i)), o["tar_c"], NUM4)
    row("rfee", "Jasa pengolahan POME & kepatuhan", lambda i: "=IF(%s=0,0,t_ffb*a_util*a_fee_ffb*%s)" % (k_(i), esc(i)), o["rev_fee"])
    row("rcap", "Penjualan listrik ke PKS", lambda i: "=%s*1000000*%s" % (R_("Ecap", i), R_("tarc", i)), o["rev_cap"])
    row("rexp", "Penjualan listrik ke PLN", lambda i: "=%s*1000000*%s" % (R_("Eexp", i), R_("tar", i)), o["rev_exp"])
    row("cer", "Vintage kredit karbon (tCO2e)", lambda i: "=IF(AND(%s>=1,%s<=a_carbon_years),t_ER*a_cer_ratio*%s,0)" % (k_(i), k_(i), R_("f", i)), o["cer"], NUM)
    row("rc", "Kredit karbon terjual (lag 1 th, neto pungutan)", lambda i: 0 if i < 2 else "=%s*(a_p_carbon-a_c_levy)" % R_("cer", i - 1), o["rev_c"])
    row("rev", "TOTAL PENDAPATAN", lambda i: "=%s+%s+%s+%s" % (R_("rfee", i), R_("rcap", i), R_("rexp", i), R_("rc", i)), o["rev"], bold=True)
    row("opex", "OPEX operasi (dieskalasi)", lambda i: "=IF(%s=0,0,-(OPEX_F+OPEX_V*%s/(t_E_nom*a_util*a_avail))*%s)" % (k_(i), R_("E", i), esc(i)), -o["opex"])
    row("ccarb", "Biaya karbon (MRV + validasi)", lambda i: "=IF(%s=0,0,-(IF(%s<=a_carbon_years+1,a_c_mrv,0)+IF(%s=1,a_c_val,0))*%s)" % (k_(i), k_(i), k_(i), esc(i)), -o["c_carb"])
    row("ebitda", "EBITDA", lambda i: "=%s+%s+%s" % (R_("rev", i), R_("opex", i), R_("ccarb", i)), o["ebitda"], bold=True)
    row("capex", "CAPEX (FCI)", lambda i: "=IF(%s=0,-FCI,0)" % k_(i), -o["capex"])
    row("sust", "Sustaining: overhaul genset (8,16) + ganti membran (8,15)", lambda i: "=-(IF(OR(%s=8,%s=16),a_overhaul*t_chp_kWe,0)+IF(OR(%s=8,%s=15),a_mem_repl*a_c_mem*t_area_mem,0))*%s" % (k_(i), k_(i), k_(i), k_(i), esc(i)), -o["sust"])
    row("vat", "PPN CAPEX (bayar th 0, restitusi th 2)", lambda i: "=IF(%s=0,-a_vat*FCI,IF(%s=2,a_vat*FCI,0))" % (k_(i), k_(i)), -o["vat"])
    row("wc", "Modal kerja (piutang - utang usaha)", lambda i: 0 if i == nY - 1 else "=%s*a_rec_days/365+(%s+%s)*a_pay_days/365" % (R_("rev", i), R_("opex", i), R_("ccarb", i)), o["wc"])
    row("dwc", "Perubahan modal kerja", lambda i: ("=-%s" % R_("wc", 0)) if i == 0 else "=-(%s-%s)" % (R_("wc", i), R_("wc", i - 1)), -o["dwc"])
    row("dep", "Penyusutan fiskal (FCI+IDC 8 th; sustaining 8 th)", lambda i: 0 if i == 0 else "=IF(%s<=a_dep_life,(FCI+IDC)/a_dep_life,0)-SUM(%s:%s)/8" % (k_(i), R_("sust", max(1, i - 7)), R_("sust", i)), o["dep"])
    row("alw", "Tax allowance (30% aset berwujud / 6 th)", lambda i: "=IF(AND(%s>=1,%s<=6),a_allow*TANG/6,0)" % (k_(i), k_(i)), o["allow"])
    row("tiu", "Laba kena pajak (tanpa utang)", lambda i: "=%s-%s-%s" % (R_("ebitda", i), R_("dep", i), R_("alw", i)), o["ebitda"] - o["dep"] - o["allow"])
    row("poolu", "Akumulasi rugi fiskal", lambda i: ("=MAX(0,-%s)" % R_("tiu", 0)) if i == 0 else "=MAX(0,%s-%s)" % (R_("poolu", i - 1), R_("tiu", i)), None)
    row("taxu", "Pajak (tanpa utang)", lambda i: ("=-a_tax*MAX(0,%s)" % R_("tiu", 0)) if i == 0 else "=-a_tax*MAX(0,%s-%s)" % (R_("tiu", i), R_("poolu", i - 1)), -o["tax_u"])
    row("fcff", "ARUS KAS BERSIH PROYEK (FCFF)", lambda i: "=%s+%s+%s+%s+%s+%s" % (R_("ebitda", i), R_("taxu", i), R_("capex", i), R_("sust", i), R_("vat", i), R_("dwc", i)), o["fcff"], bold=True)
    row("cum", "Kumulatif FCFF", lambda i: ("=%s" % R_("fcff", 0)) if i == 0 else "=%s+%s" % (R_("cum", i - 1), R_("fcff", i)), np.cumsum(o["fcff"]))
    row("disc", "Faktor diskonto (WACC)", lambda i: "=1/(1+WACC)^%d" % i, o["disc"], NUM4)
    row("dcf", "FCFF terdiskonto", lambda i: "=%s*%s" % (R_("fcff", i), R_("disc", i)), o["fcff"] * o["disc"])
    row("dcum", "Kumulatif terdiskonto", lambda i: ("=%s" % R_("dcf", 0)) if i == 0 else "=%s+%s" % (R_("dcum", i - 1), R_("dcf", i)), np.cumsum(o["fcff"] * o["disc"]))
    row("pbh", "Bantu payback (th sejak COD)", lambda i: '=""' if i == 0 else '=IF(AND(%s<0,%s>=0),%d+(-%s/%s),"")' % (R_("cum", i - 1), R_("cum", i), i - 1, R_("cum", i - 1), R_("fcff", i)), None, NUM2)
    row("dpbh", "Bantu payback terdiskonto", lambda i: '=""' if i == 0 else '=IF(AND(%s<0,%s>=0),%d+(-%s/%s),"")' % (R_("dcum", i - 1), R_("dcum", i), i - 1, R_("dcum", i - 1), R_("dcf", i)), None, NUM2)
    row("int", "Bunga", lambda i: 0 if i == 0 else "=IF(%s<=a_tenor,%s*a_r_debt,0)" % (k_(i), "%s%d" % (col(i - 1), len(rows) + 3 + 2)), o["intr"])
    row("pri", "Pokok (tenggang th 1, anuitas th 2-10)", lambda i: 0 if i == 0 else "=IF(AND(%s>=2,%s<=a_tenor),ANN-%s,0)" % (k_(i), k_(i), R_("int", i)), o["princ"])
    row("bal", "Saldo utang akhir tahun", lambda i: "=DEBT" if i == 0 else "=%s-%s" % (R_("bal", i - 1), R_("pri", i)), o["bal"])
    for i in range(1, nY):    # perbaiki referensi bunga -> saldo tahun sebelumnya
        wf.write_formula(rows["int"], C0 + i, "=IF(%s<=a_tenor,%s*a_r_debt,0)" % (k_(i), R_("bal", i - 1)), NEG, float(o["intr"][i]))
    row("upf", "Biaya upfront pinjaman", lambda i: "=-a_fee_debt*DEBT" if i == 0 else 0, -o["upfront"])
    row("dsra", "DSRA (isi th 1, lepas akhir tenor)", lambda i: "=IF(%s=1,-ANN*a_dsra_m/12,IF(%s=a_tenor,ANN*a_dsra_m/12,0))" % (k_(i), k_(i)), -o["dsra"])
    row("til", "Laba kena pajak (dengan utang)", lambda i: "=%s-%s+IF(%s=1,%s,0)" % (R_("tiu", i), R_("int", i), k_(i), R_("upf", 0)), o["ebitda"] - o["dep"] - o["allow"] - o["intr"] - np.where(np.arange(nY) == 1, o["upfront"][0], 0))
    row("pooll", "Akumulasi rugi fiskal (dengan utang)", lambda i: ("=MAX(0,-%s)" % R_("til", 0)) if i == 0 else "=MAX(0,%s-%s)" % (R_("pooll", i - 1), R_("til", i)), None)
    row("taxl", "Pajak (dengan utang)", lambda i: ("=-a_tax*MAX(0,%s)" % R_("til", 0)) if i == 0 else "=-a_tax*MAX(0,%s-%s)" % (R_("til", i), R_("pooll", i - 1)), -o["tax_l"])
    row("mra", "Cadangan perawatan (MRA, rata)", lambda i: 0 if i == 0 else "=SUM(%s:%s)/a_n_op" % (R_("sust", 1), R_("sust", nY - 1)), -o["mra"])
    row("dscr", "DSCR = (EBITDA - pajak - dWC - MRA) / layanan utang", lambda i: '=""' if i == 0 else '=IF(%s+%s>0,(%s+%s+%s+%s)/(%s+%s),"")' % (R_("int", i), R_("pri", i), R_("ebitda", i), R_("taxl", i), R_("dwc", i), R_("mra", i), R_("int", i), R_("pri", i)), None, NUM2)
    row("fcfe", "ARUS KAS EKUITAS (FCFE)", lambda i: "=%s+%s+%s*(1-a_debt_frac)+%s+%s+%s-%s-%s+%s+%s" % (R_("ebitda", i), R_("taxl", i), R_("capex", i), R_("sust", i), R_("vat", i), R_("dwc", i), R_("int", i), R_("pri", i), R_("upf", i), R_("dsra", i)), o["fcfe"], bold=True)
    lastc = col(nY - 1)
    rng = lambda key, a="C": "'Arus Kas'!$%s$%d:$%s$%d" % (a, rows[key] + 1, lastc, rows[key] + 1)
    wf.write(len(rows) + 4, 0, "Catatan: kompensasi rugi fiskal di Excel tanpa batas umur (Python: maks 10 th, PP 78/2019) - pada kasus dasar hasil identik.", NOTE)

    # ====================================================== Indikator
    wi = wb.add_worksheet("Indikator"); wi.set_column(0, 0, 50); wi.set_column(1, 1, 16); wi.set_column(2, 2, 24); wi.set_column(3, 3, 14)
    wi.write(0, 0, "INDIKATOR KELAYAKAN FINANSIAL v2 (rumus hidup)", TT); wi.write_row(2, 0, ["Indikator", "Hasil", "Kriteria", "Keputusan"], H)
    IND = [("NPV pada WACC (USD)", "=SUMPRODUCT(%s,%s)" % (rng("fcff"), rng("disc")), o["NPV"], "> 0", '=IF(B4>0,"Layak","Tidak layak")', BNUM),
           ("IRR proyek (setelah pajak)", "=IRR(%s)" % rng("fcff"), o["IRR"], "> WACC", '=IF(B5>WACC,"Layak","Tidak layak")', BPCT),
           ("IRR ekuitas", "=IRR(%s)" % rng("fcfe"), o["IRR_eq"], "> biaya ekuitas", '=IF(B6>=a_r_eq-0.0005,"Layak","Tidak layak")', BPCT),
           ("WACC", "=WACC", o["wacc"], "-", '="Informasi"', BPCT),
           ("Payback sejak COD (th)", "=SUM(%s)" % rng("pbh"), o["PBP"], "< umur", '=IF(B8<a_n_op,"Layak","Tidak layak")', BN2),
           ("Payback terdiskonto sejak COD (th)", '=IF(SUM(%s)=0,"> umur",SUM(%s))' % (rng("dpbh"), rng("dpbh")), o["DPBP"], "< umur", '=IF(ISNUMBER(B9),IF(B9<a_n_op,"Layak","Tidak layak"),"Tidak layak")', BN2),
           ("Indeks profitabilitas", "=SUMPRODUCT(%s,%s)/FCI" % (rng("fcff", "D"), rng("disc", "D")), o["PI"], "> 1,0", '=IF(B10>1,"Layak","Tidak layak")', BN2),
           ("DSCR minimum", "=MIN(%s)" % rng("dscr"), o["DSCR_min"], ">= 1,3", '=IF(B11>=1.3,"Layak","Tidak layak")', BN2),
           ("LCOE kotor (USD/kWh; seluruh biaya ke listrik)", "=(FCI-SUMPRODUCT(%s,%s)-SUMPRODUCT(%s,%s)-SUMPRODUCT(%s,%s))/(SUMPRODUCT(%s,%s)*1000000)" % (rng("opex"), rng("disc"), rng("ccarb"), rng("disc"), rng("sust"), rng("disc"), rng("E"), rng("disc")), o["LCOE"], "Informasi", '="Informasi"', NUM4),
           ("Puncak kebutuhan dana (USD)", "=-MIN(%s)" % rng("cum"), o["peak_funding"], "Struktur pendanaan", '="Informasi"', BNUM),
           ("Porsi jasa POME dalam pendapatan", "=SUM(%s)/SUM(%s)" % (rng("rfee"), rng("rev")), o["share_fee"], "Informasi", '="Informasi"', BPCT)]
    for j, (lab, f, val, kr, dec, fm) in enumerate(IND):
        rr = 3 + j; wi.write(rr, 0, lab, TXT); wi.write_formula(rr, 1, f, fm, float(val) if np.isfinite(val) else 0); wi.write(rr, 2, kr, TXT); wi.write_formula(rr, 3, dec, TXT)
    rr = 4 + len(IND); wi.write(rr, 0, "TITIK IMPAS (dihitung fin_core.bep, bisection NPV = 0)", B); rr += 1
    for lab, val, fm in (("Jasa POME impas (USD/t TBS)", be["fee_be"], NUM2), ("  setara USD/t CPO (OER 21%)", be["fee_be_cpo"], NUM2),
                         ("Tarif PLN th 1-10 impas (USc/kWh, sebelum F)", be["tariff1_be"], NUM2), ("Harga karbon impas (USD/t)", be["p_carbon_be"], NUM2),
                         ("Produksi energi impas (x dasar)", be["emult_be"], NUM2), ("CAPEX impas (x dasar)", be["capex_be"], NUM2),
                         ("BEP tunai (fraksi produksi energi)", be["BEP_cash"], PCT), ("BEP akuntansi (penyusutan buku)", be["BEP_acc"], PCT)):
        wi.write(rr, 0, lab, TXT); wi.write_number(rr, 1, float(val) if np.isfinite(val) else 0, fm); rr += 1
    ch = wb.add_chart(dict(type="line"))
    ch.add_series(dict(name="Kumulatif FCFF", categories=rng("yr"), values=rng("cum"), line=dict(color="#3d8b7d", width=2.25)))
    ch.add_series(dict(name="Kumulatif terdiskonto", categories=rng("yr"), values=rng("dcum"), line=dict(color="#b2472f", width=2.25)))
    ch.set_title(dict(name="Kurva payback (USD)")); ch.set_size(dict(width=720, height=340)); ch.set_legend(dict(position="bottom")); wi.insert_chart("F3", ch)
    ch2 = wb.add_chart(dict(type="column"))
    for key, nm_, c_ in (("rfee", "Jasa POME", "#d4952b"), ("rexp", "Listrik PLN", "#1f4e4a"), ("rcap", "Listrik PKS", "#3f6d9a"), ("rc", "Karbon", "#3d8b7d")):
        ch2.add_series(dict(name=nm_, categories=rng("yr"), values=rng(key), fill=dict(color=c_)))
    ch2.set_title(dict(name="Pendapatan per aliran (USD)")); ch2.set_size(dict(width=720, height=320)); ch2.set_legend(dict(position="bottom")); wi.insert_chart("F21", ch2)
    ch2.set_y_axis(dict(num_format="#,##0"));

    # ====================================================== Sensitivitas
    wsn = wb.add_worksheet("Sensitivitas"); wsn.set_column(0, 0, 36); wsn.set_column(1, 4, 15)
    base, res = RES["torn"]
    wsn.write(0, 0, "SENSITIVITAS NPV (+/-20%)", TT); wsn.write_row(2, 0, ["Variabel", "NPV -20%", "NPV +20%", "Rentang", "NPV dasar"], H)
    for j, (lab, lo, hi) in enumerate(res):
        wsn.write(3 + j, 0, lab, TXT); wsn.write_number(3 + j, 1, lo, NEG); wsn.write_number(3 + j, 2, hi, NEG)
        wsn.write_formula(3 + j, 3, "=ABS(C%d-B%d)" % (4 + j, 4 + j), NUM, abs(hi - lo)); wsn.write_number(3 + j, 4, base, NUM)
    rr = 5 + len(res); wsn.write(rr, 0, "PROFIL NPV vs TINGKAT DISKONTO (rumus NPV Excel)", B); wsn.write_row(rr + 1, 0, ["Tingkat diskonto", "NPV (USD)"], H)
    rates, nv = RES["curve"]
    for j, (rt, n_) in enumerate(zip(rates, nv)):
        wsn.write_number(rr + 2 + j, 0, float(rt), PCT)
        wsn.write_formula(rr + 2 + j, 1, "='Arus Kas'!$C$%d+NPV(A%d,%s)" % (rows["fcff"] + 1, rr + 3 + j, rng("fcff", "D")), NEG, float(n_))
    c3 = wb.add_chart(dict(type="scatter", subtype="smooth"))
    c3.add_series(dict(name="NPV", categories="=Sensitivitas!$A$%d:$A$%d" % (rr + 3, rr + 2 + len(rates)), values="=Sensitivitas!$B$%d:$B$%d" % (rr + 3, rr + 2 + len(rates)), line=dict(color="#1f4e4a")))
    c3.set_title(dict(name="NPV vs tingkat diskonto")); c3.set_x_axis(dict(num_format="0%")); c3.set_size(dict(width=620, height=320)); c3.set_legend(dict(none=True)); wsn.insert_chart("G3", c3)
    rr2 = rr + 4 + len(rates); wsn.write(rr2, 0, "SKENARIO", B); wsn.write_row(rr2 + 1, 0, ["Skenario", "FCI USD", "NPV USD", "IRR", "Payback th"], H)
    for j, (n_, s) in enumerate(RES["SC"]):
        wsn.write(rr2 + 2 + j, 0, n_.replace("\n", " "), TXT); wsn.write_number(rr2 + 2 + j, 1, s["fci"], NUM); wsn.write_number(rr2 + 2 + j, 2, s["NPV"], NEG)
        wsn.write_number(rr2 + 2 + j, 3, s["IRR"] if np.isfinite(s["IRR"]) else -1, PCT); wsn.write_number(rr2 + 2 + j, 4, s["PBP"] if np.isfinite(s["PBP"]) else 99, NUM2)

    # ====================================================== Monte Carlo
    wm = wb.add_worksheet("Monte Carlo"); wm.set_column(0, 0, 34); wm.set_column(1, 2, 14); wm.set_column(3, 3, 60)
    wm.write(0, 0, "MONTE CARLO (N = %d). Kasus gagal (tanpa IRR / tidak balik modal) dihitung sebagai nilai terburuk, tidak dibuang." % len(mc["NPV"]), TT)
    wm.write_row(2, 0, ["Statistik", "NPV USD", "IRR", "Payback th"], H)
    for j, (lab, q) in enumerate((("P10", 10), ("P50", 50), ("P90", 90))):
        wm.write(3 + j, 0, lab); wm.write_number(3 + j, 1, F.pct(mc["NPV"], q), NEG); wm.write_number(3 + j, 2, F.pct(mc["IRR"], q, -0.5), PCT); wm.write_number(3 + j, 3, F.pct(mc["PBP"], q, 99), NUM2)
    wm.write(6, 0, "Rata-rata NPV"); wm.write_number(6, 1, float(mc["NPV"].mean()), NEG)
    wm.write(8, 0, "Peluang NPV > 0", B); wm.write_number(8, 1, float((mc["NPV"] > 0).mean()), BPCT)
    wm.write(9, 0, "Peluang IRR > WACC", B); wm.write_number(9, 1, float((np.nan_to_num(mc["IRR"], nan=-1) > o["wacc"]).mean()), BPCT)
    wm.write(10, 0, "Kasus tanpa IRR / tidak balik modal"); wm.write_number(10, 1, int((~np.isfinite(mc["IRR"])).sum())); wm.write_number(10, 2, int((~np.isfinite(mc["PBP"])).sum()))
    wm.write(12, 0, "DISTRIBUSI INPUT (kasus dasar = modus; distribusi condong merugikan)", B); wm.write_row(13, 0, ["Input", "Spearman ke NPV", "", "Distribusi"], H)
    for j, (k, sp) in enumerate(sorted(mc["spearman"].items(), key=lambda kv: -abs(kv[1]))):
        wm.write(14 + j, 0, k); wm.write_number(14 + j, 1, sp, NUM2); wm.write(14 + j, 3, F.MC_DIST[k], TXT)
    h, edges = np.histogram(mc["NPV"], bins=30); r0 = 30
    wm.write_row(r0 - 1, 0, ["Bin NPV (tengah)", "Frekuensi"], H)
    for j in range(len(h)): wm.write_number(r0 + j, 0, float((edges[j] + edges[j + 1]) / 2), NUM); wm.write_number(r0 + j, 1, int(h[j]), NUM)
    c4 = wb.add_chart(dict(type="column")); c4.add_series(dict(name="Frekuensi", categories="='Monte Carlo'!$A$%d:$A$%d" % (r0 + 1, r0 + len(h)), values="='Monte Carlo'!$B$%d:$B$%d" % (r0 + 1, r0 + len(h)), fill=dict(color="#3d8b7d"), gap=10))
    c4.set_title(dict(name="Histogram NPV")); c4.set_size(dict(width=620, height=320)); c4.set_legend(dict(none=True)); wm.insert_chart("F3", c4)

    # ====================================================== Skala, Armada
    wsk = wb.add_worksheet("Skala Set"); wsk.set_column(0, 0, 32); wsk.set_column(1, 3, 16)
    wsk.write(0, 0, "EKONOMI PER UKURAN PKS (desain bejana sama)", TT); wsk.write_row(2, 0, ["Indikator", "30 t/jam", "45 t/jam", "60 t/jam"], H)
    TR = RES["tiers"]
    for j, (lab, key, fm) in enumerate((("Jumlah reaktor", None, NUM), ("FCI USD", "fci", NUM), ("Listrik GWh/th (th 2)", "E2", NUM2), ("Pendapatan th 2 USD", "rev2", NUM),
                                        ("NPV USD", "NPV", NEG), ("IRR", "IRR", PCT), ("Payback th", "PBP", NUM2))):
        wsk.write(3 + j, 0, lab)
        for c_, t in enumerate(("30", "45", "60")):
            ot = TR[t]; val = F.R["tiers"][t]["N_modules"] if key is None else ot["E"][2] if key == "E2" else ot["rev"][2] if key == "rev2" else ot[key]
            wsk.write_number(3 + j, 1 + c_, float(val) if np.isfinite(val) else -1, fm)
    wsk.write(11, 0, "Set 60 t/jam (> 1 MW neto) memakai tier Perpres 112 >1-3 MW (9,81 / 5,89 USc).", NOTE)
    wfl = wb.add_worksheet("Armada"); wfl.set_column(0, 0, 32); wfl.set_column(1, len(fl["years"]), 11)
    wfl.write(0, 0, "MODEL PERUSAHAAN: %d set BOO 2027-2034, kurva belajar 90%% pada %d%% FCI, unit-1 FOAK +20%%, CAPEX dieskalasi, overhead tanpa perisai pajak" % (sum(F.ROLL.values()), round(F.LEARN_SHARE * 100)), TT)
    wfl.write(2, 0, "Tahun", H); wfl.write_row(2, 1, fl["years"], H)
    keys = (("Set baru", "sets_new", NUM), ("Set beroperasi", "sets_op", NUM), ("Listrik GWh", "E", NUM2), ("Kredit karbon tCO2e", "co2", NUM),
            ("Pendapatan USD", "rev", NUM), ("  jasa POME", "rev_fee", NUM), ("  listrik", "rev_el", NUM), ("  karbon", "rev_c", NUM), ("OPEX USD", "opex", NUM),
            ("EBITDA USD", "ebitda", NUM), ("CAPEX + sustaining USD", "capex", NUM), ("Overhead korporat USD", "overhead", NUM), ("FCFF perusahaan USD", "fcff_co", NEG))
    for j, (lab, key, fm) in enumerate(keys):
        wfl.write(3 + j, 0, lab, B if key == "fcff_co" else None)
        for c_, val in enumerate(fl[key]): wfl.write_number(3 + j, 1 + c_, float(val), fm)
    rF = 3 + len(keys) - 1; lc = coln(len(fl["years"])); rC = rF + 1
    wfl.write(rC, 0, "Kumulatif FCFF", B)
    for c_ in range(len(fl["years"])):
        wfl.write_formula(rC, 1 + c_, "=%s%d" % (coln(1 + c_), rF + 1) if c_ == 0 else "=%s%d+%s%d" % (coln(c_), rC + 1, coln(1 + c_), rF + 1), NEG)
    wfl.write(rC + 2, 0, "NPV perusahaan @WACC", B); wfl.write_formula(rC + 2, 1, "=B%d+NPV(WACC,C%d:%s%d)" % (rF + 1, rF + 1, lc, rF + 1), BNUM, fl["NPV"])
    wfl.write(rC + 3, 0, "IRR perusahaan", B); wfl.write_formula(rC + 3, 1, "=IRR(B%d:%s%d)" % (rF + 1, lc, rF + 1), BPCT, fl["IRR"])
    wfl.write(rC + 4, 0, "Puncak kebutuhan dana", B); wfl.write_formula(rC + 4, 1, "=-MIN(B%d:%s%d)" % (rC + 1, lc, rC + 1), BNUM, fl["peak"])
    wfl.write_row(rC + 6, 0, ["Unit ke-", "Tahun", "Faktor CAPEX", "FCI USD", "NPV unit USD", "IRR unit"], H)
    for j, (n_, y0, cm, nv_, ir, fci_) in enumerate(fl["units"]):
        wfl.write_row(rC + 7 + j, 0, [n_, y0]); wfl.write_number(rC + 7 + j, 2, cm, NUM2); wfl.write_number(rC + 7 + j, 3, fci_, NUM)
        wfl.write_number(rC + 7 + j, 4, nv_, NEG); wfl.write_number(rC + 7 + j, 5, ir if np.isfinite(ir) else -1, PCT)

    # ====================================================== Lokasi, Pasar, PESTLE, Porter, Sumber
    wl = wb.add_worksheet("Lokasi"); wl.set_column(0, 0, 70); wl.set_column(1, 3, 14)
    wl.write(0, 0, "INTERKONEKSI & LAHAN DARI MODEL 3D LOKASI (cad/out/site.json)", TT); wl.write_row(2, 0, ["Rute", "Panjang m", "USD/m", "Biaya USD"], H)
    for j, (lab, L_, cm, c) in enumerate(T_["site_lines"]):
        wl.write(3 + j, 0, lab, TXT); wl.write_number(3 + j, 1, L_, NUM); wl.write_number(3 + j, 2, cm, NUM2); wl.write_number(3 + j, 3, c, NUM)
    rr = 5 + len(T_["site_lines"]); SJ = F.SITE
    for j, (lab, val) in enumerate((("Luas kolam POME sebelum (m2)", SJ.get("pond_area_before_m2", 0)), ("Luas kolam setelah - tetap untuk polishing (m2)", SJ.get("pond_area_after_m2", 0)),
                                    ("Lahan kolam dibebaskan (m2)", SJ.get("land_freed_m2", 0)), ("Luas plot produk (m2)", T_["plot_m2"]))):
        wl.write(rr + j, 0, lab); wl.write_number(rr + j, 1, float(val), NUM)
    rr += 6; wl.write(rr, 0, "PEMERIKSAAN JARAK AMAN", B); wl.write_row(rr + 1, 0, ["Item", "Jarak m", "Minimum m", "OK"], H)
    for j, c in enumerate(SJ.get("safety", [])):
        wl.write(rr + 2 + j, 0, "%s (%s)" % (c["item"], c["basis"]), TXT); wl.write_number(rr + 2 + j, 1, c["dist"], NUM2); wl.write_number(rr + 2 + j, 2, c["min"], NUM); wl.write(rr + 2 + j, 3, "Ya" if c["ok"] else "TIDAK")
    mk = RES["mk"]
    wp = wb.add_worksheet("Pasar"); wp.set_column(0, 0, 46); wp.set_column(1, 2, 18); wp.set_column(3, 6, 22)
    wp.write(0, 0, "UKURAN PASAR (pendapatan rata-rata umur proyek, setara-set berbasis volume POME)", TT); wp.write_row(2, 0, ["Parameter", "Nilai", "Satuan", "Sumber"], H)
    MR = [("Jumlah PKS Indonesia", MK.MILLS, "PKS", "Universal Mill List"), ("POME nasional", MK.POME_NAT, "m3/th", "PASPI/BRIN 2026"),
          ("Pendapatan rata-rata per set", mk["rev_avg"], "USD/th", "Arus Kas (umur 20 th)"), ("POME per set", F.TECH["pome_m3y_nom"] * v["util"], "m3/th", "Basis volume model"),
          ("Porsi PKS 30-60 t/jam", MK.SH_SIZE, "-", "[UNVERIFIED]"), ("Porsi tanpa penangkap metana", MK.SH_NOCAP, "-", "T&E 2025"), ("Porsi Sumatera + Kalimantan", MK.SH_REGION, "-", "Sebaran PKS"),
          ("Set SOM s/d 2034", mk["sets_SOM"], "set", "Rencana armada")]
    for j, (lab, val, u, src) in enumerate(MR):
        wp.write(3 + j, 0, lab); wp.write_number(3 + j, 1, float(val), INP); wp.write(3 + j, 2, u); wp.write(3 + j, 3, src)
    wp.write(12, 0, "Pendapatan per m3 POME", B); wp.write_formula(12, 1, "=B6/B7", BN2, mk["rev_m3"])
    wp.write(13, 0, "TAM (USD/th)", B); wp.write_formula(13, 1, "=B5*B13", BNUM, mk["TAM"])
    wp.write(14, 0, "SAM (USD/th)", B); wp.write_formula(14, 1, "=B14*B8*B9*B10", BNUM, mk["SAM"])
    wp.write(15, 0, "SOM (USD/th)", B); wp.write_formula(15, 1, "=B11*B6", BNUM, mk["SOM"])
    wp.write(16, 0, "Setara-set TAM / SAM", B); wp.write_formula(16, 1, "=ROUND(B5/B7,0)", BNUM, mk["sets_TAM"]); wp.write_formula(16, 2, "=ROUND(B5*B8*B9*B10/B7,0)", BNUM, mk["sets_SAM"])
    wp.write(17, 0, "Pangsa SOM / SAM", B); wp.write_formula(17, 1, "=B16/B15", BPCT, mk["share"])
    wp.write(19, 0, "PEMBANDING TEKNOLOGI", B); wp.write_row(20, 0, ["Teknologi", "CAPEX USD juta/MW", "Lahan ha", "Bangun bln", "Portabel", "Mutu efluen", "Pemain"], H)
    for j, row_ in enumerate(MK.compet(fl)): wp.write_row(21 + j, 0, row_, TXT)
    wpe = wb.add_worksheet("PESTLE"); wpe.set_column(0, 0, 6); wpe.set_column(1, 1, 12); wpe.set_column(2, 2, 54); wpe.set_column(3, 6, 10); wpe.set_column(7, 7, 66)
    wpe.write(0, 0, "PESTLE (skor = tanda x dampak x peluang)", TT)
    wpe.write_row(2, 0, ["Kode", "Kategori", "Faktor", "Tanda", "Dampak 1-5", "Peluang 1-5", "Skor", "Keterangan"], H)
    for j, (k, c_, f_, s_, i_, l_, d_) in enumerate(MK.PESTLE):
        rr = 3 + j; wpe.write_row(rr, 0, [k, c_, f_], TXT); wpe.write_number(rr, 3, s_, INP); wpe.write_number(rr, 4, i_, INP); wpe.write_number(rr, 5, l_, INP)
        wpe.write_formula(rr, 6, "=D%d*E%d*F%d" % (rr + 1, rr + 1, rr + 1), NEG, s_ * i_ * l_); wpe.write(rr, 7, d_, TXT)
    rr = 4 + len(MK.PESTLE); wpe.write_row(rr, 1, ["Kategori", "Skor bersih"], H); ps = MK.pestle_scores()
    for j, c_ in enumerate(ps):
        wpe.write(rr + 1 + j, 1, c_); wpe.write_formula(rr + 1 + j, 2, '=SUMIF($B$4:$B$%d,B%d,$G$4:$G$%d)' % (3 + len(MK.PESTLE), rr + 2 + j, 3 + len(MK.PESTLE)), NEG, ps[c_])
    wpe.write(rr + 7, 1, "Total", B); wpe.write_formula(rr + 7, 2, "=SUM(C%d:C%d)" % (rr + 2, rr + 7), BNEG, sum(ps.values()))
    wpt = wb.add_worksheet("Porter"); wpt.set_column(0, 0, 20); wpt.set_column(1, 1, 46); wpt.set_column(2, 2, 12); wpt.set_column(3, 3, 50)
    wpt.write(0, 0, "LIMA KEKUATAN PORTER (tekanan 1-5)", TT); wpt.write_row(2, 0, ["Kekuatan", "Sub-faktor", "Skor", "Alasan"], H)
    rr = 3; summ = []
    for f_, subs in MK.PORTER.items():
        r0 = rr
        for s_, sc, why in subs: wpt.write(rr, 0, f_, TXT); wpt.write(rr, 1, s_, TXT); wpt.write_number(rr, 2, sc, INP); wpt.write(rr, 3, why, TXT); rr += 1
        summ.append((f_, r0, rr - 1))
    rr += 1; wpt.write_row(rr, 0, ["Kekuatan", "Skor rata-rata"], H)
    for j, (f_, a_, b_) in enumerate(summ): wpt.write(rr + 1 + j, 0, f_); wpt.write_formula(rr + 1 + j, 1, "=AVERAGE(C%d:C%d)" % (a_ + 1, b_ + 1), NUM2, float(np.mean([s for _, s, _ in MK.PORTER[f_]])))
    wsr = wb.add_worksheet("Sumber"); wsr.set_column(0, 0, 160); wsr.write(0, 0, "SUMBER DATA (finance/research/*.md)", TT); rr = 2
    for fn in ("market_data.md", "market_data_2.md"):
        p = os.path.join(F.HERE, "research", fn)
        if os.path.exists(p):
            for l_ in open(p, encoding="utf-8").read().splitlines(): wsr.write(rr, 0, l_); rr += 1
            rr += 1

    # ====================================================== Ringkasan
    ws0.set_column(0, 0, 46); ws0.set_column(1, 1, 18)
    ws0.write(0, 0, "MODEL KEUANGAN v2 - GENERATOR BIOGAS PORTABEL (1 set PKS 45 t TBS/jam, BOO)", TT)
    ws0.write(1, 0, "Alur: Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator. Sel kuning di lembar Asumsi = input.", NOTE)
    KP = [("FCI 2027 (USD)", "=FCI", o["fci"], BNUM), ("USD per kWe kotor (2026)", "=FCI26/t_P_gross", o["fci26"] / T_["P_gross"], BNUM),
          ("Pendapatan th 3 (USD)", "='Arus Kas'!F%d" % (rows["rev"] + 1), o["rev"][3], BNUM), ("EBITDA th 3 (USD)", "='Arus Kas'!F%d" % (rows["ebitda"] + 1), o["ebitda"][3], BNUM),
          ("NPV @WACC (USD)", "=Indikator!B4", o["NPV"], BNUM), ("IRR proyek", "=Indikator!B5", o["IRR"], BPCT), ("IRR ekuitas", "=Indikator!B6", o["IRR_eq"], BPCT),
          ("WACC", "=WACC", o["wacc"], BPCT), ("Payback sejak COD (th)", "=Indikator!B8", o["PBP"], BN2), ("Payback terdiskonto (th)", "=Indikator!B9", o["DPBP"], BN2),
          ("DSCR minimum", "=Indikator!B11", o["DSCR_min"], BN2), ("Porsi pendapatan dari jasa POME", "=Indikator!B14", o["share_fee"], BPCT),
          ("Jasa POME impas (USD/t TBS)", "=Indikator!B17", be["fee_be"], BN2), ("Peluang NPV > 0 (Monte Carlo)", "='Monte Carlo'!B9", float((mc["NPV"] > 0).mean()), BPCT),
          ("NPV perusahaan (armada)", "=Armada!B%d" % (rC + 3), fl["NPV"], BNUM), ("IRR perusahaan", "=Armada!B%d" % (rC + 4), fl["IRR"], BPCT)]
    for j, (lab, f, val, fm) in enumerate(KP): ws0.write(3 + j, 0, lab); ws0.write_formula(3 + j, 1, f, fm, float(val) if np.isfinite(val) else 0)
    figs = RES["figs"]
    ws0.insert_image("D3", figs["cf"], dict(x_scale=.42, y_scale=.42)); ws0.insert_image("D22", figs["pb"], dict(x_scale=.42, y_scale=.42))
    ws0.insert_image("D41", figs["npv"], dict(x_scale=.40, y_scale=.40)); ws0.insert_image("A22", figs["capex"], dict(x_scale=.24, y_scale=.24))
    wg = wb.add_worksheet("Gambar"); yy = 0
    for k in ("pasar", "porter", "capex", "cf", "npv", "pb", "bep", "mc", "fleet", "sc"):
        wg.insert_image(yy, 0, figs[k], dict(x_scale=.45, y_scale=.45)); yy += 48 if k == "porter" else 26
    wb.close()
    return OUT

def verify(path=OUT, mods=None):
    """hitung ulang dengan LibreOffice; mods = {nama_asumsi: nilai} untuk uji rumus hidup"""
    import openpyxl
    t = tempfile.mkdtemp(); src = path
    if mods:
        wb = openpyxl.load_workbook(path); ws = wb["Asumsi"]
        for r in range(1, 120):
            if ws.cell(r, 1).value in mods: ws.cell(r, 2).value = mods[ws.cell(r, 1).value]
        src = os.path.join(t, "in.xlsx"); wb.save(src)
    t2 = tempfile.mkdtemp()
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", t2, src], capture_output=True, timeout=240)
    ws = openpyxl.load_workbook(os.path.join(t2, os.path.basename(src)), data_only=True)["Indikator"]
    return {ws.cell(r, 1).value: ws.cell(r, 2).value for r in range(4, 15)}
