# -*- coding: utf-8 -*-
"""Buku kerja Excel model keuangan v2 dengan RUMUS HIDUP (xlsxwriter): Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator.
Nilai Python disimpan sebagai cache rumus; verify() menghitung ulang dengan LibreOffice dan membandingkan."""
import os, subprocess, tempfile
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name as coln
import json
import fin_core as F, fin_market as MK, fin_mill as MI

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
    wa.write(0, 0, "ASUMSI MODEL v3 (sel kuning = input; seluruh model ikut berubah). Sumber [R1]-[R4] = research/*.md", TT)
    wa.write_row(2, 0, ["Nama", "Nilai", "Satuan", "Rendah / Tinggi", "Sumber / catatan"], H)
    r = 3
    for k, (val, unit, src, lo, hi) in F.A.items():
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), INP); wa.write(r, 2, unit, TXT)
        wa.write(r, 3, "" if lo is None else "%s / %s" % (lo, hi), TXT); wa.write(r, 4, src, TXT)
        wb.define_name("a_" + k, "=Asumsi!$B$%d" % (r + 1)); r += 1
    r += 1; wa.write(r, 0, "DATA TEKNIS & LOKASI (dihitung dari results.json, ga.json, site.json - bukan input)", B); r += 1
    ef = F.R["effluent"]
    TK = [("P_gross", T_["P_gross"], "kWe", "Daya kotor genset pada hari nameplate"), ("P_net", T_["P_net"], "kWe", "Daya neto pada hari nameplate"),
          ("E_year", T_["E_year_GWh"], "GWh/th", "Energi neto tahunan, simulasi 365 hari proses (util proses, Minggu libur, 14 hari henti)"),
          ("Eg_year", T_["Eg_year_GWh"], "GWh/th", "Energi kotor tahunan, simulasi yang sama"), ("up", T_["util_proc"], "-", "Util pada simulasi tahunan proses"),
          ("ffb", T_["ffb_ty_nom"], "t TBS/th", "45 t/jam x 20 jam x 300 hari (dikali util)"), ("days", T_["days_yr"], "hari/th", "Hari olah"),
          ("poly", T_["polymer_kg_tffb"], "kg/t TBS", "Polimer (neraca massa, 8 kg/t DS)"), ("ac", T_["ac_kg_tffb"], "kg/t TBS", "Karbon aktif penjaga (neraca massa)"),
          ("naoh", T_["naoh_kgd"], "kg/hari", "NaOH P95 (MC proses)"),
          ("base", T_["base_t"], "tCO2e/th", "Baseline kolam terbuka (AMS-III.H, UF 0,89) pada util proses"), ("proj", T_["proj_t"], "tCO2e/th", "Emisi proyek (bocor, CH4 terlarut, slip, flare, efluen MCF proses)"),
          ("effCOD", T_["eff_t_nom"], "t COD/th", "COD terurai efluen ke kolam polishing pada util 1,0"), ("B0", T_["B0"], "kg CH4/kg COD", "IPCC"), ("GWP", T_["GWP"], "-", "GWP CH4 (AR5)"),
          ("MCFp", T_["MCF_proc"], "-", "MCF efluen yang dipakai di results.json"),
          ("chp_kWe", T_["chp_kWe"], "kWe", "Genset terpasang"), ("V_tank", T_["V_tank"], "m3", "Volume cair 1 tangki GFS"), ("n_vessel", T_["n_vessel"], "tangki", "Jumlah tangki reaktor"),
          ("A_lam", T_["A_lam"], "m2", "Luas proyeksi settler lamella"), ("gh_m3", T_["gh_m3"], "m3", "Penampung gas"), ("plot_m2", T_["plot_m2"], "m2", "Luas plot"),
          ("pome_tffb", T_["pome_m3d"] / 900.0, "m3/t TBS", "POME per t TBS"), ("effratio", ef["Q_m3d"] / T_["pome_m3d"], "-", "Efluen / POME (m3/m3)"),
          ("cake", T_["cake_kg_tffb"], "kg/t TBS", "Kue lumpur 20% DS"), ("land_m2", F.SITE.get("land_freed_m2", 11081.0), "m2", "Kolam anaerobik dibebaskan (site.json)")]
    for k, val, unit, src in TK:
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), NUM4 if val < 10 else NUM2); wa.write(r, 2, unit); wa.write(r, 4, src)
        wb.define_name("t_" + k, "=Asumsi!$B$%d" % (r + 1)); r += 1
    wa.write(r, 0, "ER"); wa.write_formula(r, 1, "=(t_base-(t_proj-t_effCOD*t_up*t_B0*t_MCFp*t_GWP))*a_util/t_up-t_effCOD*a_util*t_B0*a_MCF_eff*t_GWP", NUM, o["ER"])
    wa.write(r, 4, "Pengurangan emisi neto tCO2e/th (baseline - proyek - efluen ke kolam polishing pada MCF_eff)"); wb.define_name("t_ER", "=Asumsi!$B$%d" % (r + 1)); r += 1
    # faktor ekspor di bawah kapasitas kontrak: profil musiman bulanan (simulasi tahunan proses)
    r += 1; wa.write(r, 0, "Profil musiman (faktor bulan)", B); wa.write(r + 1, 0, "Daya neto bulan (kW)", B); wa.write(r + 2, 0, "Terekspor <= kontrak (kW)", B)
    for j, fm in enumerate(T_["month_f"]):
        cc = coln(1 + j)
        wa.write_number(r, 1 + j, fm, NUM4)
        pk = T_["E_year_GWh"] * 1e6 / 8760 * F.kfac(v) * fm
        wa.write_formula(r + 1, 1 + j, "=t_E_year*1000000/8760*a_util/t_up*%s%d" % (cc, r + 1), NUM, pk)
        wa.write_formula(r + 2, 1 + j, "=MIN(%s%d,a_cap_kW)" % (cc, r + 2), NUM, min(pk, v["cap_kW"]))
    wa.write(r + 3, 0, "capf"); wa.write_formula(r + 3, 1, "=SUM(B%d:M%d)/SUM(B%d:M%d)" % (r + 3, r + 3, r + 2, r + 2), NUM4, o["capf"])
    wa.write(r + 3, 4, "Fraksi energi yang dapat diekspor di bawah kapasitas kontrak PLN")
    wb.define_name("t_capf", "=Asumsi!$B$%d" % (r + 4)); r += 5
    wa.write(r, 0, "WACC"); wa.write_formula(r, 1, "=a_debt_frac*a_r_debt*(1-a_tax)+(1-a_debt_frac)*a_r_eq", BPCT, o["wacc"]); wb.define_name("WACC", "=Asumsi!$B$%d" % (r + 1))

    # ====================================================== CAPEX
    wc = wb.add_worksheet("CAPEX"); wc.set_column(0, 0, 14); wc.set_column(1, 1, 66); wc.set_column(2, 5, 14); wc.set_column(6, 6, 56)
    wc.write(0, 0, "CAPEX 1 set standar 45 t TBS/jam (USD 2026; dieskalasi ke tahun konstruksi)", TT)
    wc.write_row(2, 0, ["Kelompok", "Item", "Jumlah", "Satuan", "Harga satuan USD", "Total USD", "Dasar"], H)
    r = 3; first = r; pec_r = []; tang_r = []
    def unit_f(n):
        if "tangki GFS dibaut" in n: return "=a_c_gfs"
        if n.startswith("TK-101"): return "=a_c_gfs*1.3"
        if n.startswith("PM-8"): return "=a_c_chp"
        if n.startswith("PM-7"): return "=90*t_gh_m3+50000"
        return None
    for i, (g, n, q, u, c, t, b) in enumerate(o["capex_rows"]):
        wc.write(r, 0, g, TXT); wc.write(r, 1, n, TXT); wc.write(r, 3, u, TXT); wc.write(r, 6, b, TXT)
        if n.startswith("Rekayasa"):
            wc.write_formula(r, 2, "=a_eng", NUM4, q); wc.write_formula(r, 4, "=PEC", NUM, c)
        elif g == "KONTINGENSI":
            wc.write_formula(r, 2, "=a_cont", NUM4, q); wc.write_formula(r, 4, "=SUM(F%d:F%d)" % (first + 1, r), NUM, c)
        else:
            wc.write_number(r, 2, q, NUM2)
            if g == "PEC" and unit_f(n): wc.write_formula(r, 4, unit_f(n), NUM, c)
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
    wc.write(r + 2 + len(names), 1, "Pembanding [R3]: kolam tertutup 1,8-3,7 juta USD/MWe; tangki CSTR 1,8-3,5 (TSE 2 MW USD 3,6 juta, 2025); biometana ~USD 5,3 juta/PKS.", NOTE)

    # ====================================================== OPEX
    wo = wb.add_worksheet("OPEX"); wo.set_column(0, 0, 46); wo.set_column(1, 2, 16); wo.set_column(3, 3, 80)
    wo.write(0, 0, "OPEX tahun penuh (USD 2026, pada beban util x avail) - dieskalasi di Arus Kas", TT)
    wo.write_row(2, 0, ["Komponen", "USD/th", "Jenis", "Rumus"], H)
    FORM = {"Staf operasi (10 orang)": "=a_staff", "O&M genset (kontrak)": "=a_c_eng_om*t_Eg_year*a_util/t_up*a_avail*1000000",
            "Perawatan peralatan proses": "=a_c_maint*(PEC-a_c_chp*t_chp_kWe)", "Asuransi": "=a_c_ins*FCI26",
            "Administrasi & SCADA jarak jauh": "=a_c_admin", "Sewa lahan plot di PKS": "=a_lease*t_plot_m2"}
    r = 3; fr = []; vr = []
    for k, (val, typ) in o["opex_items"].items():
        wo.write(r, 0, k, TXT)
        if k in FORM: wo.write_formula(r, 1, FORM[k], NUM, val); wo.write(r, 3, FORM[k][1:], TXT)
        else:
            fchem = "=t_ffb*a_util*(t_poly*a_p_poly+t_ac*a_p_ac)/1000+t_naoh*t_days/1000*a_p_naoh"
            wo.write_formula(r, 1, fchem, NUM, val); wo.write(r, 3, fchem[1:], TXT)
        wo.write(r, 2, typ, TXT); (fr if typ == "F" else vr).append(r); r += 1
    wo.write(r + 1, 0, "Biaya tetap (F)", B); wo.write_formula(r + 1, 1, "=" + "+".join("B%d" % (x + 1) for x in fr), BNUM, o["opF"])
    wo.write(r + 2, 0, "Biaya variabel (V)", B); wo.write_formula(r + 2, 1, "=" + "+".join("B%d" % (x + 1) for x in vr), BNUM, o["opV"])
    wb.define_name("OPEX_F", "=OPEX!$B$%d" % (r + 2)); wb.define_name("OPEX_V", "=OPEX!$B$%d" % (r + 3))
    wo.write(r + 4, 0, "Biaya karbon (MRV tahunan + validasi sekali) dan sustaining capex dihitung per tahun di Arus Kas.", NOTE)

    # ====================================================== Arus Kas
    wf = wb.add_worksheet("Arus Kas"); wf.set_column(0, 0, 44); wf.set_column(1, 1, 3); wf.freeze_panes(3, 2)
    wf.write(0, 0, "MODEL ARUS KAS PROYEK v3 (USD nominal; negatif = keluar). 1 set 45 t TBS/jam, BOO, segmen S3", TT)
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
    row("E", "Listrik neto (GWh)", lambda i: "=t_E_year*a_util/t_up*a_avail*%s" % R_("f", i), o["E"], NUM2)
    row("Ecap", "  ke PKS menggantikan solar (GWh)", lambda i: "=MIN(t_ffb*a_util*a_diesel_L_tffb/a_sfc/1000000*a_avail*IF(%s>=1,1,%s),%s)" % (R_("f", i), R_("f", i), R_("E", i)), o["Ecap"], NUM2)
    row("Eexp", "  ekspor ke PLN (GWh)", lambda i: "=(%s-%s)*t_capf" % (R_("E", i), R_("Ecap", i)), o["Eexp"], NUM2)
    row("tar", "Tarif PLN (USD/kWh)", lambda i: "=IF(%s=0,0,IF(%s<=10,a_tariff1*a_F_loc,a_tariff2)/100)" % (k_(i), k_(i)), o["tariff"], NUM4)
    row("tarc", "Harga listrik ke PKS (USD/kWh)", lambda i: "=IF(%s=0,0,a_p_captive*%s)" % (k_(i), esc(i)), o["tar_c"], NUM4)
    row("rfee", "Jasa pengolahan POME & kepatuhan", lambda i: "=IF(%s=0,0,t_ffb*a_util*a_fee_ffb*%s)" % (k_(i), esc(i)), o["rev_fee"])
    row("rcap", "Penjualan listrik ke PKS", lambda i: "=%s*1000000*%s" % (R_("Ecap", i), R_("tarc", i)), o["rev_cap"])
    row("rexp", "Penjualan listrik ke PLN", lambda i: "=%s*1000000*%s" % (R_("Eexp", i), R_("tar", i)), o["rev_exp"])
    row("cer", "Vintage kredit karbon (tCO2e)", lambda i: "=IF(AND(%s>=1,%s<=a_carbon_years),t_ER*a_cer_ratio*%s,0)" % (k_(i), k_(i), R_("f", i)), o["cer"], NUM)
    row("rc", "Kredit karbon terjual (lag 1 th, neto pungutan)", lambda i: 0 if i < 2 else "=%s*(a_p_carbon-a_c_levy)" % R_("cer", i - 1), o["rev_c"])
    row("rev", "TOTAL PENDAPATAN", lambda i: "=%s+%s+%s+%s" % (R_("rfee", i), R_("rcap", i), R_("rexp", i), R_("rc", i)), o["rev"], bold=True)
    row("opex", "OPEX operasi (dieskalasi)", lambda i: "=IF(%s=0,0,-(OPEX_F+OPEX_V*%s/(t_E_year*a_util/t_up*a_avail))*%s)" % (k_(i), R_("E", i), esc(i)), -o["opex"])
    row("ccarb", "Biaya karbon (MRV + validasi)", lambda i: "=IF(%s=0,0,-(IF(%s<=a_carbon_years+1,a_c_mrv,0)+IF(%s=1,a_c_val,0))*%s)" % (k_(i), k_(i), k_(i), esc(i)), -o["c_carb"])
    row("ebitda", "EBITDA", lambda i: "=%s+%s+%s" % (R_("rev", i), R_("opex", i), R_("ccarb", i)), o["ebitda"], bold=True)
    row("capex", "CAPEX (FCI)", lambda i: "=IF(%s=0,-FCI,0)" % k_(i), -o["capex"])
    row("sust", "Sustaining: overhaul genset (8,16) + atap membran tangki (12)", lambda i: "=-(IF(OR(%s=8,%s=16),a_overhaul*t_chp_kWe,0)+IF(%s=12,a_roof_repl*t_n_vessel,0))*%s" % (k_(i), k_(i), k_(i), esc(i)), -o["sust"])
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
    wi.write(0, 0, "INDIKATOR KELAYAKAN FINANSIAL v3 (rumus hidup)", TT); wi.write_row(2, 0, ["Indikator", "Hasil", "Kriteria", "Keputusan"], H)
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
    wsk.write(0, 0, "EKONOMI PER UKURAN PKS (tangki GFS standar sama: 2 / 3 / 4 tangki)", TT); wsk.write_row(2, 0, ["Indikator", "30 t/jam", "45 t/jam", "60 t/jam"], H)
    TR = RES["tiers"]
    for j, (lab, key, fm) in enumerate((("Jumlah tangki reaktor", None, NUM), ("FCI USD", "fci", NUM), ("Listrik GWh/th (th 2)", "E2", NUM2), ("Pendapatan th 2 USD", "rev2", NUM),
                                        ("NPV USD", "NPV", NEG), ("IRR", "IRR", PCT), ("Payback th", "PBP", NUM2))):
        wsk.write(3 + j, 0, lab)
        for c_, t in enumerate(("30", "45", "60")):
            ot = TR[t]; val = F.R["tiers"][t]["N_modules"] if key is None else ot["E"][2] if key == "E2" else ot["rev"][2] if key == "rev2" else ot[key]
            wsk.write_number(3 + j, 1 + c_, float(val) if np.isfinite(val) else -1, fm)
    wsk.write(11, 0, "Set 60 t/jam (> 1 MW neto pada hari nameplate) memakai tier Perpres 112 >1-3 MW (9,81 / 5,89 USc).", NOTE)
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
    wp = wb.add_worksheet("Pasar"); wp.set_column(0, 0, 52); wp.set_column(1, 1, 16); wp.set_column(2, 2, 14); wp.set_column(3, 6, 18); wp.set_column(4, 4, 60)
    wp.write(0, 0, "UKURAN PASAR BOTTOM-UP (sel kuning = input; setara-set = 1 set per PKS / volume POME 1 set)", TT)
    wp.write_row(2, 0, ["Parameter", "Nilai", "Satuan", "Keyakinan", "Sumber"], H)
    MR = [("PKS beroperasi di Indonesia", MK.MILLS_ID, "PKS", "H", "Trase/Universal Mill List 1.318 (2022) [R3]"),
          ("Porsi sudah menangkap metana", MK.SH_CAPTURED, "-", "M", "84 PLTBg POME ~165 MW (GAPKI 2026) [R3]"),
          ("POME nasional", MK.POME_NAT, "m3/th", "M", "125-170 juta m3 [R3]"),
          ("Porsi PKS 30-60 t/jam", MK.SH_SIZE, "-", "L", "Estimasi kelas kapasitas [R3]; perlu CSV Trase"),
          ("Porsi Sumatera + Kalimantan", MK.SH_REGION, "-", "M", "Sebaran PKS [R3]"),
          ("Porsi PKS bergantung diesel (S3/S4)", MK.SH_DIESEL, "-", "EST", "Kaltim 12/62 PKS dekat desa diesel-saja (Jakarta Post 2015) + emplasmen/KCP; rentang 0,15-0,35"),
          ("POME per set (m3/th)", mk["pome_set"], "m3/th", "Model", "45 t/jam x 20 x 300 x util x 0,65"),
          ("Pendapatan rata-rata per set (USD/th)", mk["rev_avg"], "USD/th", "Model", "Arus Kas, rata-rata 20 th"),
          ("Set SOM s/d 2034 (rencana armada)", mk["sets_SOM"], "set", "Rencana", "ROLL di fin_core"),
          ("MWe terpasang per set", F.TECH["chp_kWe"] / 1000, "MWe", "Model", "2 x 600 kWe")]
    for j, (lab, val, u, cf_, src) in enumerate(MR):
        wp.write(3 + j, 0, lab); wp.write_number(3 + j, 1, float(val), INP); wp.write(3 + j, 2, u); wp.write(3 + j, 3, cf_); wp.write(3 + j, 4, src, TXT)
    r0 = 15; wp.write_row(r0, 0, ["Tingkat", "PKS / set", "MWe", "Pendapatan USD/th", "Aturan"], H)
    FUN = [("TAM (volume POME semua PKS tanpa penangkap metana)", "=B6*(1-B5)/B10", mk["rows"][0]),
           ("SAM-luas (+30-60 t/jam, Sumatera/Kalimantan)", "=B4*(1-B5)*B7*B8", mk["rows"][1]),
           ("SAM (+bergantung diesel: jendela kesepakatan terbuka)", "=B%d*B9" % (r0 + 3), mk["rows"][2]),
           ("SOM 2034", "=B12", mk["rows"][3])]
    for j, (lab, f, rw) in enumerate(FUN):
        rr = r0 + 1 + j; wp.write(rr, 0, lab, B); wp.write_formula(rr, 1, f, BNUM, rw["sets"])
        wp.write_formula(rr, 2, "=B%d*B13" % (rr + 1), NUM, rw["MW"]); wp.write_formula(rr, 3, "=B%d*B11" % (rr + 1), BNUM, rw["rev"]); wp.write(rr, 4, rw["rule"], TXT)
    wp.write(r0 + 6, 0, "Pangsa SOM / SAM", B); wp.write_formula(r0 + 6, 1, "=B%d/B%d" % (r0 + 5, r0 + 4), BPCT, mk["share"])
    wp.write(r0 + 7, 0, "SOM vs laju bangun PLTBg nasional (9 MW/th) [R3]", B); wp.write_formula(r0 + 7, 1, "=C%d/8/9" % (r0 + 5), BPCT, mk["build_share"])
    wp.write(r0 + 8, 0, "Ekspansi: Malaysia ~315 PKS tanpa penangkap metana [R3] -> setara-set segmen diesel", B); wp.write_number(r0 + 8, 1, mk["my_sets"], NUM)
    wp.write(r0 + 10, 0, "PKS per provinsi (estimasi [R3, L])", B); wp.write_row(r0 + 11, 0, ["Provinsi", "PKS", "SAM (estimasi)"], H)
    for j, (pv, nn) in enumerate(MK.PROV):
        wp.write(r0 + 12 + j, 0, pv); wp.write_number(r0 + 12 + j, 1, nn, NUM)
        wp.write_formula(r0 + 12 + j, 2, "=B%d*(1-$B$5)*$B$7*$B$9%s" % (r0 + 13 + j, "" if pv == "Lainnya" else ""), NUM, nn * (1 - MK.SH_CAPTURED) * MK.SH_SIZE * MK.SH_DIESEL)

    # ====================================================== Keputusan PKS (rumus hidup)
    mv = MI.mvals(); cm = RES["mill"]; ad = cm["detail"]
    wk = wb.add_worksheet("Keputusan PKS"); wk.set_column(0, 0, 50); wk.set_column(1, 4, 15); wk.set_column(5, 5, 70)
    wk.write(0, 0, "MODEL KEPUTUSAN PKS: apakah layanan BOO lebih murah bagi PKS daripada kolam POME? (rumus hidup)", TT)
    wk.write(1, 0, "Sudut pandang PKS 45 t TBS/jam, 20 th, USD 2026 dieskalasi a_infl, diskonto biaya modal PKS. Ubah sel kuning di sini atau di Asumsi (fee, util, solar, harga listrik).", NOTE)
    wk.write_row(3, 0, ["Input sisi PKS", "Nilai", "Satuan", "Rendah / Tinggi", "", "Sumber"], H)
    r = 4
    for k, (val, unit, src, lo, hi) in MI.M.items():
        wk.write(r, 0, k); wk.write_number(r, 1, float(val), INP); wk.write(r, 2, unit, TXT); wk.write(r, 3, "%s / %s" % (lo, hi), TXT); wk.write(r, 5, src, TXT)
        wb.define_name("m_" + k, "='Keputusan PKS'!$B$%d" % (r + 1)); r += 1
    r += 1; wk.write(r, 0, "BESARAN ANTARA", B); r += 1
    MID = [("ffb", "TBS diolah (t/th)", "=t_ffb*a_util", ad["ffb"]), ("pome", "POME (m3/th)", "=K_ffb*t_pome_tffb", ad["ffb"] * T_["pome_m3d"] / 900),
           ("effm3", "Efluen set ke kolam polishing (m3/th)", "=K_pome*t_effratio", ad["ffb"] * T_["pome_m3d"] / 900 * F.R["effluent"]["Q_m3d"] / T_["pome_m3d"]),
           ("Enet", "Listrik neto set (kWh/th)", "=t_E_year*a_util/t_up*a_avail*1000000", ad["E_net"]),
           ("Edsl", "Listrik diesel PKS saat ini (kWh/th)", "=K_ffb*a_diesel_L_tffb/a_sfc", ad["E_dsl"]),
           ("cdsl", "Biaya listrik diesel PKS (USD/kWh)", "=a_sfc*m_p_diesel/a_fx+m_genset_om", ad["c_dsl"]),
           ("cap", "Listrik set ke PKS (kWh/th)", "=MIN(K_Edsl*a_avail,K_Enet)", ad["cap"]),
           ("land", "Nilai lahan kolam dibebaskan (USD/th)", "=t_land_m2/10000*m_land_margin*1000000/a_fx", ad["land"]),
           ("cake", "Nilai pupuk kue lumpur (USD/th)", "=K_ffb*t_cake/1000*m_cake_val", ad["cake"]),
           ("cnet", "Pendapatan karbon neto pengembang (USD/th)", "=t_ER*a_cer_ratio*(a_p_carbon-a_c_levy)", ad["cnet"]),
           ("riskA", "Risiko penyegelan A (USD/th)", "=m_p_enf_A*m_closure_d*K_ffb/t_days*m_margin", ad["A"]["Risiko penyegelan (nilai harapan)"]),
           ("riskD", "Risiko penyegelan B/C/D (USD/th)", "=m_p_enf_D*m_closure_d*K_ffb/t_days*m_margin", ad["D"]["Risiko penyegelan (nilai harapan)"])]
    for key, lab, f, val in MID:
        wk.write(r, 0, lab); wk.write_formula(r, 1, f, NUM2 if key == "cdsl" else NUM, float(val) if val is not None else 0.0)
        wb.define_name("K_" + key, "='Keputusan PKS'!$B$%d" % (r + 1)); r += 1
    # opsi B/C turunan
    for o_, perf in (("B", "m_perf_B"), ("C", "m_perf_C")):
        wk.write(r, 0, "Listrik pembangkit milik PKS opsi %s (kWh/th)" % o_); wk.write_formula(r, 1, "=t_E_year*a_util/t_up*%s*1000000" % perf, NUM); wb.define_name("K_E" + o_, "='Keputusan PKS'!$B$%d" % (r + 1)); r += 1
        wk.write(r, 0, "  dipakai PKS menggantikan solar (kWh/th)"); wk.write_formula(r, 1, "=MIN(K_Edsl*%s,K_E%s)" % (perf, o_), NUM); wb.define_name("K_cap" + o_, "='Keputusan PKS'!$B$%d" % (r + 1)); r += 1
    r += 1; wk.write_row(r, 0, ["BIAYA TAHUNAN PKS (USD 2026; negatif = manfaat)", "A Status quo", "B Kolam tertutup", "C Tangki milik PKS", "D Layanan BOO", "Rumus / keterangan"], H); r += 1
    oth = "m_monitor*1000000/a_fx"
    LINES = [("Listrik diesel PKS", "=K_Edsl*K_cdsl", "=(K_Edsl-K_capB)*K_cdsl", "=(K_Edsl-K_capC)*K_cdsl", "=(K_Edsl-K_cap)*K_cdsl", "Solar + O&M genset untuk listrik yang tidak dipasok biogas"),
             ("Jasa pengolahan POME (fee)", 0, 0, 0, "=K_ffb*a_fee_ffb", "Hanya D"),
             ("Beli listrik dari set", 0, 0, 0, "=K_cap*a_p_captive", "Hanya D, harga di bawah diesel"),
             ("O&M pembangkit biogas milik PKS", 0, "=m_om_BC*1000000000/a_fx*t_chp_kWe/1000", "=m_om_BC*1000000000/a_fx*t_chp_kWe/1000", 0, "Rp 3,3 miliar/MW/th [R2]"),
             ("Pengurasan lumpur & perawatan kolam", "=(m_desludge+m_pond_om)*1000000/a_fx", "=m_desl_B*m_desludge*1000000/a_fx", 0, 0, "Kolam anaerobik hilang pada C/D"),
             ("Aplikasi lahan", "=K_pome*m_la_cost/a_fx", "=K_pome*m_la_cost/a_fx", "=K_pome*m_la_cost/a_fx", "=K_effm3*m_la_cost/a_fx", "Efluen tetap ke LA pada semua opsi"),
             ("Pemantauan lingkungan", "=" + oth, "=" + oth, "=" + oth, "=" + oth, "Sama"),
             ("Risiko penyegelan (nilai harapan)", "=K_riskA", "=K_riskD", "=K_riskD", "=K_riskD", "Peluang x hari henti x margin"),
             ("Ekspor listrik ke PLN (th 1-10)", 0, "=-(K_EB-K_capB)*a_tariff1*a_F_loc/100", "=-(K_EC-K_capC)*a_tariff1*a_F_loc/100", 0, "Pada D ekspor milik pengembang"),
             ("Kredit karbon (PKS daftar sendiri)", 0, "=-K_cnet*m_perf_B+a_c_mrv", "=-K_cnet*m_perf_C+a_c_mrv", "=-m_c_share*K_cnet", "D: bagi hasil opsional"),
             ("Lahan kolam dibebaskan", 0, 0, "=-K_land", "=-K_land", "Margin sawit pada lahan kolam anaerobik"),
             ("Kue lumpur sebagai pupuk", 0, 0, 0, "=-K_cake", "Hanya D (screw press)")]
    py = {"A": [ad["A"]["Listrik diesel PKS (solar + O&M genset)"], 0, 0, 0, ad["A"]["Pengurasan lumpur kolam"] + ad["A"]["Perawatan kolam & pompa"], ad["A"]["Aplikasi lahan"], ad["A"]["Pemantauan lingkungan"], ad["A"]["Risiko penyegelan (nilai harapan)"], 0, 0, 0, 0]}
    for o_ in ("B", "C"):
        X = ad[o_]; py[o_] = [X["Listrik diesel sisa"], 0, 0, X["O&M pembangkit biogas milik PKS"], X["Pengurasan lumpur"], X["Aplikasi lahan"], X["Pemantauan lingkungan"], X["Risiko penyegelan (nilai harapan)"],
                             X["Ekspor listrik ke PLN (th 1-10)"], X["Kredit karbon (PKS daftar sendiri)"], X["Lahan kolam dibebaskan"], 0]
    X = ad["D"]; py["D"] = [X["Listrik diesel sisa (set tidak tersedia)"], X["Jasa pengolahan POME (fee)"], X["Listrik dari set"], 0, 0, X["Aplikasi lahan (efluen)"], X["Pemantauan lingkungan"],
                            X["Risiko penyegelan (nilai harapan)"], 0, X["Bagi hasil karbon"], X["Lahan kolam dibebaskan (margin sawit)"], X["Kue lumpur sebagai pupuk"]]
    r1 = r
    for j, (lab, *fs, note) in enumerate(LINES):
        wk.write(r, 0, lab)
        for c_, (f, o_) in enumerate(zip(fs, "ABCD")):
            if isinstance(f, str): wk.write_formula(r, 1 + c_, f, NEG, float(py[o_][j]))
            else: wk.write_number(r, 1 + c_, f, NEG)
        wk.write(r, 5, note, TXT); r += 1
    rT = r; wk.write(r, 0, "Total biaya tahunan (USD 2026)", B)
    for c_, o_ in enumerate("ABCD"): wk.write_formula(r, 1 + c_, "=SUM(%s%d:%s%d)" % (coln(1 + c_), r1 + 1, coln(1 + c_), r), BNEG, cm[o_]["annual"])
    r += 1; wk.write(r, 0, "CAPEX dibayar PKS (th 2027)", B)
    for c_, (o_, f) in enumerate((("A", "=0"), ("B", "=m_capex_B*1000000*t_chp_kWe/1000"), ("C", "=m_capex_C*1000000*t_chp_kWe/1000"), ("D", "=0"))):
        wk.write_formula(r, 1 + c_, f, BNEG, cm[o_]["capex"])
    rC = r; r += 1
    wk.write(r, 0, "Faktor anuitas biaya dieskalasi (20 th)"); wk.write_formula(r, 1, "=(1+a_infl)*((1+a_infl)/(1+m_r_mill))*(1-((1+a_infl)/(1+m_r_mill))^a_n_op)/(1-(1+a_infl)/(1+m_r_mill))", NUM4, cm["af"])
    wb.define_name("K_af", "='Keputusan PKS'!$B$%d" % (r + 1)); r += 1
    wk.write(r, 0, "NPV biaya 20 th (USD)", B)
    for c_, o_ in enumerate("ABCD"): wk.write_formula(r, 1 + c_, "=%s%d*K_af+%s%d*(1+a_infl)" % (coln(1 + c_), rT + 1, coln(1 + c_), rC + 1), BNEG, cm[o_]["NPV"])
    rN = r; r += 1
    wk.write(r, 0, "BIAYA POME TERLEVELISASI (USD 2026 / t TBS)", B)
    for c_, o_ in enumerate("ABCD"): wk.write_formula(r, 1 + c_, "=%s%d/(K_ffb*K_af)" % (coln(1 + c_), rN + 1), BN2, cm[o_]["per_t"])
    rP = r; r += 1
    wk.write(r, 0, "PKS hemat dengan D vs A (USD/t TBS)", B); wk.write_formula(r, 4, "=B%d-E%d" % (rP + 1, rP + 1), BN2, cm["saving_D_vs_A_per_t"]); r += 1
    wk.write(r, 0, "PKS hemat dengan D vs A (%)", B); wk.write_formula(r, 4, "=(B%d-E%d)/B%d" % (rP + 1, rP + 1, rP + 1), BPCT, cm["saving_D_vs_A_pct"]); rS = r; r += 1
    wk.write(r, 0, "PKS hemat dengan D vs A (USD/th)", B); wk.write_formula(r, 4, "=B%d-E%d" % (rT + 1, rT + 1), BNEG, cm["A"]["annual"] - cm["D"]["annual"]); r += 1
    wk.write(r, 0, "Pengembang: NPV proyek pada fee yang sama (USD)", B); wk.write_formula(r, 4, "=Indikator!B4", BNUM, o["NPV"]); r += 1
    wk.write(r, 0, "Pengembang: IRR proyek", B); wk.write_formula(r, 4, "=Indikator!B5", BPCT, o["IRR"]); r += 1
    wk.write(r, 0, "Keputusan PKS", B); wk.write_formula(r, 4, '=IF(E%d>0,"D lebih murah dari kolam","Kolam lebih murah")' % (rS + 1), TXT, "D lebih murah dari kolam" if cm["saving_D_vs_A_pct"] > 0 else "Kolam lebih murah"); r += 2
    fw = RES["fw"]
    wk.write(r, 0, "JENDELA KESEPAKATAN (fin_mill.fee_window, bisection; di Excel: Goal Seek a_fee_ffb)", B); r += 1
    for lab, val in (("Fee minimum pengembang (NPV = 0 pada WACC), USD/t TBS", fw["fee_min"]), ("Fee maksimum PKS (biaya D = biaya A), USD/t TBS", fw["fee_max"]),
                     ("Lebar jendela, USD/t TBS", fw["width"]), ("Fee dasar dipakai", v["fee_ffb"])):
        wk.write(r, 0, lab); wk.write_number(r, 1, float(val), BN2); r += 1
    wk.write(r, 0, "Catatan jujur: B/C (PKS membangun sendiri) memberi biaya terlevelisasi lebih rendah BILA PKS punya modal USD 2,6-3,0 juta dan tim operasi; D untuk PKS tanpa modal / tanpa selera risiko teknis.", NOTE); r += 2
    # langkah waterfall (USD/t TBS) dengan rumus = item / TBS
    wk.write(r, 0, "LANGKAH DARI A KE D (USD 2026 / t TBS)", B); wk.write_row(r + 1, 0, ["Langkah", "USD/t TBS"], H); r += 2; rw0 = r
    WF = [("Status quo (A)", "=B%d" % (rP + 1)), ("Solar dihindari", "=-(B%d-E%d)/K_ffb" % (r1 + 1, r1 + 1)), ("Beli listrik set", "=E%d/K_ffb" % (r1 + 3)),
          ("Pengurasan & kolam dihindari", "=-B%d/K_ffb" % (r1 + 5)), ("Aplikasi lahan", "=(E%d-B%d)/K_ffb" % (r1 + 6, r1 + 6)), ("Risiko penyegelan turun", "=(E%d-B%d)/K_ffb" % (r1 + 8, r1 + 8)),
          ("Lahan + pupuk + karbon", "=(E%d+E%d+E%d)/K_ffb" % (r1 + 10, r1 + 11, r1 + 12)), ("Jasa pengolahan (fee)", "=E%d/K_ffb" % (r1 + 2)), ("Layanan BOO (D)", "=E%d" % (rP + 1))]
    wfp = MI.waterfall()
    for j, ((lab, f), (_, pv)) in enumerate(zip(WF, wfp)): wk.write(r, 0, lab); wk.write_formula(r, 1, f, NUM2, pv); r += 1
    chm = wb.add_chart(dict(type="column"))
    chm.add_series(dict(name="Biaya POME PKS (USD/t TBS)", categories="='Keputusan PKS'!$B$%d:$E$%d" % (r1, r1), values="='Keputusan PKS'!$B$%d:$E$%d" % (rP + 1, rP + 1),
                        points=[dict(fill=dict(color=c_)) for c_ in ("#b2472f", "#8c8c8c", "#8c8c8c", "#1f4e4a")], data_labels=dict(value=True, num_format="0.00")))
    chm.set_title(dict(name="Biaya POME terlevelisasi bagi PKS")); chm.set_legend(dict(none=True)); chm.set_size(dict(width=560, height=300)); wk.insert_chart("H4", chm)

    # ====================================================== Segmen
    wsg = wb.add_worksheet("Segmen"); wsg.set_column(0, 0, 46); wsg.set_column(1, 8, 14); wsg.set_column(9, 9, 60)
    wsg.write(0, 0, "SEGMEN PKS: di mana jendela kesepakatan terbuka (fin_mill.segments)", TT)
    wsg.write_row(2, 0, ["Segmen", "Util", "Solar L/t TBS", "Fee min USD/t", "Fee maks USD/t", "Jendela?", "NPV pengembang @fee dasar", "IRR pengembang", "PKS hemat (%)", "Catatan"], H)
    for j, sg in enumerate(RES["seg"]):
        rr = 3 + j; wsg.write(rr, 0, sg["name"], TXT); wsg.write_number(rr, 1, sg["util"], NUM2); wsg.write_number(rr, 2, sg["diesel"], NUM2)
        wsg.write_number(rr, 3, sg["fee_min"], NUM2); wsg.write_number(rr, 4, sg["fee_max"], NUM2); wsg.write_formula(rr, 5, '=IF(E%d>D%d,"Ya","Tidak")' % (rr + 1, rr + 1), TXT, "Ya" if sg["fee_max"] > sg["fee_min"] else "Tidak")
        wsg.write_number(rr, 6, sg["NPV_dev"], NEG); wsg.write_number(rr, 7, float(sg["IRR_dev"]) if np.isfinite(sg["IRR_dev"]) else -1, PCT); wsg.write_number(rr, 8, sg["saving_pct"], PCT); wsg.write(rr, 9, sg["note"], TXT)
    wsg.write(4 + len(RES["seg"]), 0, "Kesimpulan: pasar sasaran = PKS bergantung diesel (S3/S4). PKS terhubung PLN (S1/S2) tidak dilayani kecuali harga karbon / CAPEX berubah.", NOTE)

    # ====================================================== Pesaing
    wcp = wb.add_worksheet("Pesaing"); wcp.set_column(0, 0, 40); wcp.set_column(1, 5, 15); wcp.set_column(6, 6, 30); wcp.set_column(7, 14, 11)
    wcp.write(0, 0, "MATRIKS PESAING BERBOBOT (skor 1-5, 5 = terbaik bagi PKS; bobot dapat diubah)", TT)
    hdr = ["Opsi", "CAPEX USD jt/MWe", "Lahan ha", "Bangun bln", "PKS bayar CAPEX", "Referensi ID", "Sumber"] + [c for c, _ in MK.CRIT] + ["Skor tertimbang"]
    wcp.write_row(3, 0, hdr, H); wcp.write(2, 6, "Bobot ->", B)
    for j, (_, w) in enumerate(MK.CRIT): wcp.write_number(2, 7 + j, w, INP)
    for j, c in enumerate(RES["comp"]):
        rr = 4 + j; wcp.write_row(rr, 0, [c["name"], c["capex"], c["land"], c["build"], c["mill_pays"], c["ref"], c["src"]], TXT)
        for k_, sc in enumerate(c["scores"]): wcp.write_number(rr, 7 + k_, round(sc, 2), INP)
        last = coln(7 + len(MK.CRIT) - 1)
        wcp.write_formula(rr, 7 + len(MK.CRIT), "=SUMPRODUCT($H$3:$%s$3,H%d:%s%d)" % (last, rr + 1, last, rr + 1), BN2, c["total"])
    wcp.write(5 + len(RES["comp"]), 0, "Skor biaya: dari Model Keputusan PKS (USD/t TBS terlevelisasi). Kelemahan kami: kematangan (belum ada referensi) - ditutup oleh pilot + jaminan kinerja.", NOTE)

    # ====================================================== USP
    wu = wb.add_worksheet("USP"); wu.set_column(0, 0, 28); wu.set_column(1, 1, 70); wu.set_column(2, 2, 30); wu.set_column(3, 3, 55)
    wu.write(0, 0, "KEUNGGULAN UNIK (USP) - DIUKUR, BUKAN DIKLAIM", TT); wu.write_row(2, 0, ["USP", "Metrik dari model", "Bukti", "Penilaian jujur"], H)
    for j, u_ in enumerate(RES["usp"]): wu.write_row(3 + j, 0, list(u_), TXT)

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
    wsr = wb.add_worksheet("Sumber"); wsr.set_column(0, 0, 22); wsr.set_column(1, 1, 46); wsr.set_column(2, 5, 13); wsr.set_column(6, 6, 30); wsr.set_column(7, 7, 60); wsr.set_column(8, 9, 12); wsr.set_column(10, 10, 50)
    wsr.write(0, 0, "REGISTER SUMBER (research/source_register.json; laporan lengkap research/R1-R4*.md)", TT)
    wsr.write_row(2, 0, ["Berkas", "Parameter", "Nilai", "Satuan", "Rendah", "Tinggi", "Sumber", "URL", "Tanggal", "Keyakinan", "Catatan"], H)
    reg = json.load(open(os.path.join(F.ROOT, "research", "source_register.json"), encoding="utf-8"))
    for j, d in enumerate(reg):
        vals_ = [d.get(k) for k in ("file", "param", "value", "unit", "low", "high", "source_name", "source_url", "date", "confidence", "note")]
        wsr.write_row(3 + j, 0, [x if isinstance(x, (int, float)) and not isinstance(x, bool) else ("" if x is None else str(x)) for x in vals_])
    # ====================================================== Ringkasan
    ws0.set_column(0, 0, 46); ws0.set_column(1, 1, 18)
    ws0.write(0, 0, "MODEL KEUANGAN v3 - SET BIOGAS KONTAK TERMOFILIK YANG DAPAT DIPINDAH (1 set PKS 45 t TBS/jam, BOO, segmen bergantung diesel)", TT)
    ws0.write(1, 0, "Alur: Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator; Keputusan PKS (PKS vs kolam); Segmen; Pasar; Pesaing; USP; Sumber. Sel kuning = input.", NOTE)
    KP = [("FCI 2027 (USD)", "=FCI", o["fci"], BNUM), ("USD per kWe kotor (2026)", "=FCI26/t_P_gross", o["fci26"] / T_["P_gross"], BNUM),
          ("Pendapatan th 3 (USD)", "='Arus Kas'!F%d" % (rows["rev"] + 1), o["rev"][3], BNUM), ("EBITDA th 3 (USD)", "='Arus Kas'!F%d" % (rows["ebitda"] + 1), o["ebitda"][3], BNUM),
          ("NPV @WACC (USD)", "=Indikator!B4", o["NPV"], BNUM), ("IRR proyek", "=Indikator!B5", o["IRR"], BPCT), ("IRR ekuitas", "=Indikator!B6", o["IRR_eq"], BPCT),
          ("WACC", "=WACC", o["wacc"], BPCT), ("Payback sejak COD (th)", "=Indikator!B8", o["PBP"], BN2), ("Payback terdiskonto (th)", "=Indikator!B9", o["DPBP"], BN2),
          ("DSCR minimum", "=Indikator!B11", o["DSCR_min"], BN2), ("Porsi pendapatan dari jasa POME", "=Indikator!B14", o["share_fee"], BPCT),
          ("Jasa POME impas (USD/t TBS)", "=Indikator!B17", be["fee_be"], BN2), ("Peluang NPV > 0 (Monte Carlo)", "='Monte Carlo'!B9", float((mc["NPV"] > 0).mean()), BPCT),
          ("NPV perusahaan (armada)", "=Armada!B%d" % (rC + 3), fl["NPV"], BNUM), ("IRR perusahaan", "=Armada!B%d" % (rC + 4), fl["IRR"], BPCT),
          ("PKS: biaya POME status quo (USD/t TBS)", "='Keputusan PKS'!B%d" % (rP + 1), RES["mill"]["A"]["per_t"], BN2),
          ("PKS: biaya POME dengan layanan BOO (USD/t TBS)", "='Keputusan PKS'!E%d" % (rP + 1), RES["mill"]["D"]["per_t"], BN2),
          ("PKS hemat vs kolam (%)", "='Keputusan PKS'!E%d" % (rS + 1), RES["mill"]["saving_D_vs_A_pct"], BPCT),
          ("Jendela fee (min - maks USD/t TBS)", None, 0, None)]
    for j, (lab, f, val, fm) in enumerate(KP):
        ws0.write(3 + j, 0, lab)
        if f is None: ws0.write(3 + j, 1, "%.2f - %.2f" % (RES["fw"]["fee_min"], RES["fw"]["fee_max"]), TXT)
        else: ws0.write_formula(3 + j, 1, f, fm, float(val) if np.isfinite(val) else 0)
    figs = RES["figs"]
    ws0.insert_image("D3", figs["mill"], dict(x_scale=.40, y_scale=.40)); ws0.insert_image("D24", figs["cf"], dict(x_scale=.42, y_scale=.42))
    ws0.insert_image("D43", figs["pb"], dict(x_scale=.42, y_scale=.42)); ws0.insert_image("A26", figs["capex"], dict(x_scale=.24, y_scale=.24))
    wg = wb.add_worksheet("Gambar"); yy = 0
    for k in ("mill", "seg", "comp", "pasar", "porter", "capex", "cf", "npv", "pb", "bep", "mc", "fleet", "sc"):
        wg.insert_image(yy, 0, figs[k], dict(x_scale=.45, y_scale=.45)); yy += 48 if k in ("porter", "mill") else 28
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
    wbk = openpyxl.load_workbook(os.path.join(t2, os.path.basename(src)), data_only=True)
    ws = wbk["Indikator"]; out = {ws.cell(r, 1).value: ws.cell(r, 2).value for r in range(4, 15)}
    wk = wbk["Keputusan PKS"]
    for r in range(1, 200):
        lab = wk.cell(r, 1).value
        if lab and (lab.startswith("BIAYA POME TERLEVELISASI") or lab.startswith("NPV biaya 20")): out[lab] = [wk.cell(r, c).value for c in range(2, 6)]
        if lab and lab.startswith("PKS hemat dengan D vs A (%)"): out[lab] = wk.cell(r, 5).value
    return out
