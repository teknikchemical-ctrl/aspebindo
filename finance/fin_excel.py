# -*- coding: utf-8 -*-
"""Buku kerja Excel model keuangan dengan RUMUS HIDUP (xlsxwriter). Lembar Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator.
Nilai hasil Python disimpan sebagai nilai cache rumus; diverifikasi ulang dengan LibreOffice (verify())."""
import os, math, subprocess, shutil
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell as rc, xl_col_to_name as coln
import fin_core as F, fin_market as MK

OUT = os.path.join(F.HERE, "outputs", "BG_Model_Keuangan.xlsx")

def build(RES):
    o, be, mc, fl = RES["o"], RES["be"], RES["mc"], RES["fl"]
    v = o["v"]
    wb = xlsxwriter.Workbook(OUT)
    H = wb.add_format(dict(bold=True, bg_color="#1f4e4a", font_color="white", border=1, text_wrap=True, valign="vcenter"))
    T = wb.add_format(dict(bold=True, font_size=14, font_color="#1f4e4a"))
    B = wb.add_format(dict(bold=True))
    INP = wb.add_format(dict(bg_color="#fff2cc", border=1, num_format="#,##0.00##"))
    NUM = wb.add_format(dict(num_format="#,##0", border=1)); NUM2 = wb.add_format(dict(num_format="#,##0.00", border=1))
    NUM4 = wb.add_format(dict(num_format="0.0000", border=1)); PCT = wb.add_format(dict(num_format="0.0%", border=1))
    TXT = wb.add_format(dict(border=1, text_wrap=True, valign="top")); BNUM = wb.add_format(dict(bold=True, num_format="#,##0", border=1, bg_color="#e2efda"))
    BPCT = wb.add_format(dict(bold=True, num_format="0.0%", border=1, bg_color="#e2efda")); BN2 = wb.add_format(dict(bold=True, num_format="#,##0.00", border=1, bg_color="#e2efda"))
    NEG = wb.add_format(dict(num_format="#,##0;[Red]-#,##0", border=1)); BNEG = wb.add_format(dict(bold=True, num_format="#,##0;[Red]-#,##0", border=1, bg_color="#e2efda"))
    NOTE = wb.add_format(dict(italic=True, font_color="#555555", text_wrap=True))

    # ============================================================== Ringkasan (diisi di akhir)
    ws0 = wb.add_worksheet("Ringkasan")
    # ============================================================== Asumsi
    wa = wb.add_worksheet("Asumsi"); wa.set_column(0, 0, 14); wa.set_column(1, 1, 12); wa.set_column(2, 2, 14); wa.set_column(3, 3, 14); wa.set_column(4, 4, 90)
    wa.write(0, 0, "ASUMSI MODEL (sel kuning = input; ubah di sini, seluruh model ikut berubah)", T)
    wa.write_row(2, 0, ["Nama", "Nilai", "Satuan", "Rendah / Tinggi", "Sumber / catatan"], H)
    r = 3; NAME = {}
    for k, (val, unit, src, lo, hi) in F.A.items():
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), INP); wa.write(r, 2, unit, TXT)
        wa.write(r, 3, "" if lo is None else "%s / %s" % (lo, hi), TXT); wa.write(r, 4, src, TXT)
        nm = "a_" + k; wb.define_name(nm, "=Asumsi!$B$%d" % (r + 1)); NAME[k] = nm; r += 1
    # turunan teknis
    r += 1; wa.write(r, 0, "DATA TEKNIS (dari process/outputs/results.json, tidak diubah manual)", B); r += 1
    TK = [("P_gross", F.TECH["P_gross"], "kWe", "Daya kotor genset"), ("P_net", F.TECH["P_net"], "kWe", "Daya bersih ekspor"),
          ("E_gross", F.TECH["E_gross_GWh"], "GWh/th", "Energi kotor tahunan"), ("Q_heat", F.TECH["Q_heat"], "kWth", "Panas CHP terpulihkan"),
          ("chp_kWe", F.TECH["chp_kWe"], "kWe", "Kapasitas genset terpasang"), ("area_mem", F.TECH["area_mem"], "m2", "Luas membran"),
          ("pome_m3y", F.TECH["pome_m3y"], "m3/th", "POME diolah"), ("cake_ty", F.TECH["cake_ty"], "t/th", "Kue lumpur"),
          ("ffb_ty", F.TECH["ffb_ty"], "t TBS/th", "TBS diolah PKS"), ("plot_m2", F.TECH["plot_m2"], "m2", "Luas plot dari GA 3D")]
    for k, val, unit, src in TK:
        wa.write(r, 0, k); wa.write_number(r, 1, float(val), NUM2); wa.write(r, 2, unit); wa.write(r, 4, src)
        wb.define_name("t_" + k, "=Asumsi!$B$%d" % (r + 1)); r += 1
    r += 1
    wa.write(r, 0, "WACC"); wa.write_formula(r, 1, "=a_debt_frac*a_r_debt*(1-a_tax)+(1-a_debt_frac)*a_r_eq", BPCT, o["wacc"]); wa.write(r, 4, "Biaya modal rata-rata tertimbang")
    wb.define_name("WACC", "=Asumsi!$B$%d" % (r + 1))

    # ============================================================== CAPEX
    wc = wb.add_worksheet("CAPEX"); wc.set_column(0, 0, 14); wc.set_column(1, 1, 56); wc.set_column(2, 5, 14); wc.set_column(6, 6, 60)
    wc.write(0, 0, "CAPEX - Biaya Investasi Tetap (FCI) 1 set standar 45 t TBS/jam (USD 2026)", T)
    wc.write_row(2, 0, ["Kelompok", "Item", "Jumlah", "Satuan", "Harga satuan USD", "Total USD", "Dasar"], H)
    r = 3; first = r; pec_rows = []; sub_rows = []
    unit_f = {0: "=a_c_fab*%s*1000+12000+7500+10000" % F.TECH["vessel_t"], 1: "=a_c_fab*%s*1000+6000" % F.TECH["tank_t"], 2: "=a_c_mem", 8: "=a_c_chp"}
    for i, (g, n, q, u, c, t, b) in enumerate(o["capex_rows"]):
        wc.write(r, 0, g, TXT); wc.write(r, 1, n, TXT); wc.write(r, 3, u, TXT); wc.write(r, 6, b, TXT)
        if g == "PEC":
            wc.write_number(r, 2, q, NUM2)
            if i in unit_f: wc.write_formula(r, 4, unit_f[i], NUM, c)
            else: wc.write_number(r, 4, c, INP)
            wc.write_formula(r, 5, "=C%d*E%d" % (r + 1, r + 1), NUM, t); pec_rows.append(r)
        elif n.startswith("Rekayasa"):
            wc.write_formula(r, 2, "=a_eng", NUM4, q); wc.write_formula(r, 4, "=PEC", NUM, c); wc.write_formula(r, 5, "=C%d*E%d" % (r + 1, r + 1), NUM, t)
        elif g == "KONTINGENSI":
            wc.write_formula(r, 2, "=a_cont", NUM4, q); wc.write_formula(r, 4, "=SUM(F%d:F%d)" % (first + 1, r), NUM, c)
            wc.write_formula(r, 5, "=C%d*E%d" % (r + 1, r + 1), NUM, t)
        else:
            wc.write_number(r, 2, q, NUM2); wc.write_number(r, 4, c, INP); wc.write_formula(r, 5, "=C%d*E%d" % (r + 1, r + 1), NUM, t)
        if i == len([x for x in o["capex_rows"] if x[0] == "PEC"]) - 1:
            pass
        r += 1
    last = r - 1
    wb.define_name("PEC", "=CAPEX!$F$%d" % (r + 2)); wb.define_name("FCI", "=CAPEX!$F$%d" % (r + 3))
    wc.write(r + 1, 1, "PEC (biaya peralatan terbeli)", B); wc.write_formula(r + 1, 5, "=SUM(F%d:F%d)" % (pec_rows[0] + 1, pec_rows[-1] + 1), BNUM, o["pec"])
    wc.write(r + 2, 1, "FCI (biaya investasi tetap)", B); wc.write_formula(r + 2, 5, "=SUM(F%d:F%d)" % (first + 1, last + 1), BNUM, o["fci"])
    wc.write(r + 3, 1, "USD per kWe kotor"); wc.write_formula(r + 3, 5, "=FCI/t_P_gross", BNUM, o["fci"] / F.TECH["P_gross"])
    wc.write(r + 4, 1, "Modal kerja (2 bln OPEX)"); wc.write_formula(r + 4, 5, "=a_wc_months/12*(OPEX_F+OPEX_V)", BNUM, o["wc"])
    wc.write(r + 5, 1, "Total kebutuhan investasi (TCI)", B); wc.write_formula(r + 5, 5, "=F%d+F%d" % (r + 3, r + 5), BNUM, o["fci"] + o["wc"])
    wc.write(r + 7, 1, "Pembanding literatur: PLTBg POME 1-10 MW rata-rata 2.758 USD/kW (2.256-3.669), Energies 15:7265 (2022).", NOTE)
    wb.define_name("WC", "=CAPEX!$F$%d" % (r + 5))

    # ============================================================== OPEX
    wo = wb.add_worksheet("OPEX"); wo.set_column(0, 0, 46); wo.set_column(1, 2, 16); wo.set_column(3, 3, 70)
    wo.write(0, 0, "OPEX tahun penuh (USD 2026, dieskalasi a_infl di Arus Kas)", T)
    wo.write_row(2, 0, ["Komponen", "USD/th", "Jenis (F/V)", "Rumus / dasar"], H)
    FORM = {"Staf operasi (8 orang)": "=a_staff", "O&M genset (kontrak)": "=a_c_eng_om*t_E_gross*a_avail*1000000",
            "Perawatan peralatan proses": "=a_c_maint*(PEC-a_c_chp*t_chp_kWe)", "Asuransi": "=a_c_ins*FCI", "MRV & registri karbon": "=a_c_mrv",
            "Administrasi & SCADA jarak jauh": "=a_c_admin", "Sewa lahan PKS": "=a_lease*t_plot_m2",
            "Cadangan overhaul genset + ganti membran": "=a_overhaul*t_chp_kWe/8+0.8*a_c_mem*t_area_mem/a_mem_life"}
    r = 3; fr = []; vr = []
    for k, (val, typ) in o["opex_items"].items():
        wo.write(r, 0, k, TXT)
        if k in FORM: wo.write_formula(r, 1, FORM[k], NUM, val); wo.write(r, 3, FORM[k][1:], TXT)
        else: wo.write_number(r, 1, val, INP); wo.write(r, 3, "polimer %.2f kg/jam, karbon aktif %.3f kg/jam (neraca massa) + cadangan NaOH" % (F.TECH["polymer_kgh"], F.TECH["ac_kgh"]), TXT)
        wo.write(r, 2, typ, TXT); (fr if typ == "F" else vr).append(r); r += 1
    wo.write(r + 1, 0, "Biaya tetap (F)", B); wo.write_formula(r + 1, 1, "=" + "+".join("B%d" % (x + 1) for x in fr), BNUM, o["opex_full"] - o["opex_var"])
    wo.write(r + 2, 0, "Biaya variabel (V)", B); wo.write_formula(r + 2, 1, "=" + "+".join("B%d" % (x + 1) for x in vr), BNUM, o["opex_var"])
    wo.write(r + 3, 0, "Total OPEX", B); wo.write_formula(r + 3, 1, "=B%d+B%d" % (r + 2, r + 3), BNUM, o["opex_full"])
    wb.define_name("OPEX_F", "=OPEX!$B$%d" % (r + 2)); wb.define_name("OPEX_V", "=OPEX!$B$%d" % (r + 3))

    # ============================================================== Arus Kas
    wf = wb.add_worksheet("Arus Kas"); wf.set_column(0, 0, 40); wf.set_column(1, 1, 3); wf.freeze_panes(3, 2)
    wf.write(0, 0, "MODEL ARUS KAS PROYEK (USD nominal; tanda negatif = keluar). 1 set 45 t TBS/jam, BOO", T)
    yrs = o["years"]; nY = len(yrs); C0 = 2
    wf.set_column(C0, C0 + nY - 1, 11.5)
    rows = {}
    def col(i): return coln(C0 + i)
    def row(key, label, fn_, py=None, fmt=NEG, bold=False):
        rr = len(rows) + 3; rows[key] = rr
        wf.write(rr, 0, label, B if bold else None)
        for i in range(nY):
            f = fn_(i); val = float(py[i]) if py is not None else None
            if isinstance(f, (int, float)): wf.write_number(rr, C0 + i, f, fmt)
            else: wf.write_formula(rr, C0 + i, f, BNEG if bold else fmt, val if val is not None and np.isfinite(val) else 0)
        return rr
    R_ = lambda key, i: "%s%d" % (col(i), rows[key] + 1)
    wf.write(2, 0, "Tahun", H); wf.write(2, 1, "", H)
    for i, y in enumerate(yrs): wf.write(2, C0 + i, y, H)
    row("k", "Tahun operasi ke-", lambda i: i, fmt=NUM)
    row("yr", "Tahun kalender", lambda i: yrs[i], fmt=NUM)
    row("f", "Faktor operasi (ramp-up)", lambda i: "=IF(%s=0,0,IF(%s=1,a_ramp1,1))" % (R_("k", i), R_("k", i)), [0] + [v["ramp1"]] + [1] * (nY - 2), NUM2)
    row("E", "Listrik terjual ke PLN (GWh)", lambda i: "=a_E_net_GWh*a_avail*%s" % R_("f", i), o["E"], NUM2)
    row("tar", "Tarif (USD/kWh)", lambda i: "=IF(%s=0,0,IF(%s<=10,a_tariff1*a_F_loc,a_tariff2)/100)" % (R_("k", i), R_("k", i)), o["tariff"], NUM4)
    row("rel", "Pendapatan listrik", lambda i: "=%s*1000000*%s" % (R_("E", i), R_("tar", i)), o["rev_el"])
    row("cer", "Kredit karbon terbit (tCO2e)", lambda i: "=a_co2e*a_cer_ratio*%s" % R_("f", i), o["cer"], NUM)
    row("rc", "Pendapatan karbon", lambda i: "=%s*a_p_carbon" % R_("cer", i), o["rev_c"])
    row("rfee", "Jasa pengolahan POME (dari PKS)", lambda i: "=t_pome_m3y*a_fee_pome*%s*(1+a_infl)^(%s-2026)" % (R_("f", i), R_("yr", i)), o["rev_fee"])
    row("rh", "Penjualan air panas ke PKS", lambda i: "=t_Q_heat/t_P_net*%s*1000*a_heat_util*a_p_heat" % R_("E", i), o["rev_h"])
    row("rf", "Kue lumpur (pupuk organik)", lambda i: "=t_cake_ty*%s*a_p_cake" % R_("f", i), o["rev_f"])
    row("rev", "TOTAL PENDAPATAN", lambda i: "=%s+%s+%s+%s+%s" % (R_("rel", i), R_("rc", i), R_("rfee", i), R_("rh", i), R_("rf", i)), o["rev"], bold=True)
    row("opex", "OPEX (dieskalasi)", lambda i: "=IF(%s=0,0,-(OPEX_F+OPEX_V*%s)*(1+a_infl)^(%s-2026))" % (R_("k", i), R_("f", i), R_("yr", i)), -o["opex"])
    row("ebitda", "EBITDA", lambda i: "=%s+%s" % (R_("rev", i), R_("opex", i)), o["ebitda"], bold=True)
    row("capex", "CAPEX (FCI)", lambda i: "=IF(%s=0,-FCI,0)" % R_("k", i), -o["capex"])
    row("dwc", "Perubahan modal kerja", lambda i: "=IF(%s=1,-WC*(1+a_infl)^(%s-2026),IF(%s=a_n_op,WC*(1+a_infl)^(%d-2026),0))" % (R_("k", i), R_("yr", i), R_("k", i), yrs[1]), -o["dwc"])
    row("dep", "Penyusutan (garis lurus)", lambda i: "=IF(AND(%s>=1,%s<=a_dep_life),FCI/a_dep_life,0)" % (R_("k", i), R_("k", i)), o["dep"])
    row("alw", "Tax allowance (30% / 6 th)", lambda i: "=IF(AND(%s>=1,%s<=6),a_allow*FCI/6,0)" % (R_("k", i), R_("k", i)), o["allow"])
    row("tiu", "Laba kena pajak (tanpa utang)", lambda i: "=%s-%s-%s" % (R_("ebitda", i), R_("dep", i), R_("alw", i)), o["ebitda"] - o["dep"] - o["allow"])
    row("poolu", "Akumulasi rugi fiskal", lambda i: ("=MAX(0,-%s)" % R_("tiu", 0)) if i == 0 else "=MAX(0,%s-%s)" % (R_("poolu", i - 1), R_("tiu", i)), None)
    row("taxu", "Pajak (tanpa utang)", lambda i: ("=-a_tax*MAX(0,%s)" % R_("tiu", 0)) if i == 0 else "=-a_tax*MAX(0,%s-%s)" % (R_("tiu", i), R_("poolu", i - 1)), -o["tax_u"])
    row("fcff", "ARUS KAS BERSIH PROYEK (FCFF)", lambda i: "=%s+%s+%s+%s" % (R_("ebitda", i), R_("taxu", i), R_("capex", i), R_("dwc", i)), o["fcff"], bold=True)
    row("cum", "Kumulatif FCFF", lambda i: ("=%s" % R_("fcff", 0)) if i == 0 else "=%s+%s" % (R_("cum", i - 1), R_("fcff", i)), np.cumsum(o["fcff"]))
    row("disc", "Faktor diskonto (WACC)", lambda i: "=1/(1+WACC)^%d" % i, o["disc"], NUM4)
    row("dcf", "FCFF terdiskonto", lambda i: "=%s*%s" % (R_("fcff", i), R_("disc", i)), o["fcff"] * o["disc"])
    row("dcum", "Kumulatif terdiskonto", lambda i: ("=%s" % R_("dcf", 0)) if i == 0 else "=%s+%s" % (R_("dcum", i - 1), R_("dcf", i)), np.cumsum(o["fcff"] * o["disc"]))
    row("pbh", "Bantu payback (th sejak COD)", lambda i: '=""' if i == 0 else '=IF(AND(%s<0,%s>=0),%d+(-%s/%s),"")' % (R_("cum", i - 1), R_("cum", i), i - 1, R_("cum", i - 1), R_("fcff", i)), None, NUM2)
    row("dpbh", "Bantu payback terdiskonto", lambda i: '=""' if i == 0 else '=IF(AND(%s<0,%s>=0),%d+(-%s/%s),"")' % (R_("dcum", i - 1), R_("dcum", i), i - 1, R_("dcum", i - 1), R_("dcf", i)), None, NUM2)
    # pendanaan
    row("bal", "Saldo utang akhir tahun", lambda i: ("=a_debt_frac*FCI") if i == 0 else "=%s-%s" % (R_("bal", i - 1), "%s%d" % (col(i), len(rows) + 3 + 2)), o["bal"] if False else None)
    rb = rows["bal"]
    row("int", "Bunga", lambda i: 0 if i == 0 else "=IF(%s<=a_tenor,%s*a_r_debt,0)" % (R_("k", i), R_("bal", i - 1)), -o["intr"] * 0 + o["intr"])
    row("pri", "Pokok (anuitas)", lambda i: 0 if i == 0 else "=IF(%s<=a_tenor,a_debt_frac*FCI*a_r_debt/(1-(1+a_r_debt)^-a_tenor)-%s,0)" % (R_("k", i), R_("int", i)), o["princ"])
    # perbaiki rumus saldo utang (butuh baris pokok)
    for i in range(nY):
        wf.write_formula(rb, C0 + i, "=a_debt_frac*FCI" if i == 0 else "=%s-%s" % (R_("bal", i - 1), R_("pri", i)), NEG, float(o["bal"][i]) if i else o["debt0"])
    row("til", "Laba kena pajak (dengan utang)", lambda i: "=%s-%s" % (R_("tiu", i), R_("int", i)), o["ebitda"] - o["dep"] - o["allow"] - o["intr"])
    row("pooll", "Akumulasi rugi fiskal (dengan utang)", lambda i: ("=MAX(0,-%s)" % R_("til", 0)) if i == 0 else "=MAX(0,%s-%s)" % (R_("pooll", i - 1), R_("til", i)), None)
    row("taxl", "Pajak (dengan utang)", lambda i: ("=-a_tax*MAX(0,%s)" % R_("til", 0)) if i == 0 else "=-a_tax*MAX(0,%s-%s)" % (R_("til", i), R_("pooll", i - 1)), -o["tax_l"])
    row("dscr", "DSCR", lambda i: '=""' if i == 0 else '=IF(%s+%s>0,(%s+%s+%s)/(%s+%s),"")' % (R_("int", i), R_("pri", i), R_("ebitda", i), R_("taxl", i), R_("dwc", i), R_("int", i), R_("pri", i)), None, NUM2)
    row("fcfe", "ARUS KAS EKUITAS (FCFE)", lambda i: "=%s+%s+%s*(1-a_debt_frac)+%s-%s-%s" % (R_("ebitda", i), R_("taxl", i), R_("capex", i), R_("dwc", i), R_("int", i), R_("pri", i)), o["fcfe"], bold=True)
    lastc = col(nY - 1)
    rng = lambda key: "'Arus Kas'!$C$%d:$%s$%d" % (rows[key] + 1, lastc, rows[key] + 1)

    # ============================================================== Indikator
    wi = wb.add_worksheet("Indikator"); wi.set_column(0, 0, 48); wi.set_column(1, 1, 16); wi.set_column(2, 2, 22); wi.set_column(3, 3, 14)
    wi.write(0, 0, "INDIKATOR KELAYAKAN FINANSIAL (rumus hidup)", T)
    wi.write_row(2, 0, ["Indikator", "Hasil", "Kriteria", "Keputusan"], H)
    IND = [("NPV pada WACC (USD)", "=SUMPRODUCT(%s,%s)" % (rng("fcff"), rng("disc")), o["NPV"], "> 0", '=IF(B4>0,"Layak","Tidak layak")', BNUM),
           ("IRR proyek (setelah pajak)", "=IRR(%s)" % rng("fcff"), o["IRR"], "> WACC", '=IF(B5>WACC,"Layak","Tidak layak")', BPCT),
           ("IRR ekuitas (%d%% utang)" % round(v["debt_frac"] * 100), "=IRR(%s)" % rng("fcfe"), o["IRR_eq"], "> biaya ekuitas", '=IF(B6>a_r_eq,"Layak","Tidak layak")', BPCT),
           ("WACC", "=WACC", o["wacc"], "-", '="Informasi"', BPCT),
           ("Payback period sejak COD (th)", "=SUM(%s)" % rng("pbh"), o["PBP"], "< umur proyek", '=IF(B8<a_n_op,"Layak","Tidak layak")', BN2),
           ("Payback terdiskonto sejak COD (th)", '=IF(SUM(%s)=0,"> umur",SUM(%s))' % (rng("dpbh"), rng("dpbh")), o["DPBP"], "< umur proyek", '=IF(ISNUMBER(B9),IF(B9<a_n_op,"Layak","Tidak layak"),"Tidak layak")', BN2),
           ("Indeks profitabilitas", "=SUMPRODUCT('Arus Kas'!$D$%d:$%s$%d,'Arus Kas'!$D$%d:$%s$%d)/FCI" % (rows["fcff"] + 1, lastc, rows["fcff"] + 1, rows["disc"] + 1, lastc, rows["disc"] + 1), o["PI"], "> 1,0", '=IF(B10>1,"Layak","Tidak layak")', BN2),
           ("DSCR minimum", "=MIN(%s)" % rng("dscr"), o["DSCR_min"], "> 1,2", '=IF(B11>1.2,"Layak","Tidak layak")', BN2),
           ("LCOE (USD/kWh)", "=(FCI-SUMPRODUCT(%s,%s))/(SUMPRODUCT(%s,%s)*1000000)" % (rng("opex"), rng("disc"), rng("E"), rng("disc")), o["LCOE"], "vs tarif", '="Informasi"', NUM4),
           ("Puncak kebutuhan dana (USD)", "=-MIN(%s)" % rng("cum"), o["peak_funding"], "Struktur pendanaan", '="Informasi"', BNUM),
           ("Total FCFF umur proyek (USD)", "=SUM(%s)" % rng("fcff"), o["cum_end"], "-", '="Informasi"', BNUM)]
    for j, (lab, f, val, kr, dec, fm) in enumerate(IND):
        rr = 3 + j; wi.write(rr, 0, lab, TXT); wi.write_formula(rr, 1, f, fm, float(val) if np.isfinite(val) else 0); wi.write(rr, 2, kr, TXT)
        wi.write_formula(rr, 3, dec, TXT)
    rr = 3 + len(IND) + 1
    wi.write(rr, 0, "TITIK IMPAS (BEP)", B); rr += 1
    BE = [("BEP tunai (fraksi kapasitas, th penuh)", be["BEP_cash"], PCT), ("BEP akuntansi (laba = 0)", be["BEP_acc"], PCT), ("Titik penutupan (SDP)", be["SDP"], PCT),
          ("Tarif impas th 1-10, USc/kWh sebelum F (NPV=0)", be["tariff1_be"], NUM2), ("Harga karbon impas USD/tCO2e (NPV=0)", be["p_carbon_be"], NUM2),
          ("Produksi energi impas (x dasar)", be["emult_be"], NUM2), ("CAPEX impas (x dasar)", be["capex_be"], NUM2)]
    for lab, val, fm in BE:
        wi.write(rr, 0, lab, TXT); wi.write_number(rr, 1, float(val), fm); rr += 1
    wi.write(rr + 1, 0, "BEP tunai = biaya tetap tunai / (pendapatan - biaya variabel); nilai impas NPV=0 diselesaikan dengan bisection di fin_core.bep().", NOTE)
    # grafik payback (native)
    ch = wb.add_chart(dict(type="line"))
    ch.add_series(dict(name="Kumulatif FCFF", categories=rng("yr"), values=rng("cum"), line=dict(color="#3d8b7d", width=2.25)))
    ch.add_series(dict(name="Kumulatif terdiskonto", categories=rng("yr"), values=rng("dcum"), line=dict(color="#b2472f", width=2.25)))
    ch.set_title(dict(name="Kurva payback (USD)")); ch.set_size(dict(width=720, height=340)); ch.set_legend(dict(position="bottom"))
    wi.insert_chart("F3", ch)
    ch2 = wb.add_chart(dict(type="column")); ch2.add_series(dict(name="FCFF", categories=rng("yr"), values=rng("fcff"), fill=dict(color="#3d8b7d")))
    ch2.add_series(dict(name="EBITDA", categories=rng("yr"), values=rng("ebitda"), fill=dict(color="#cfe3df")))
    ch2.set_title(dict(name="Arus kas tahunan (USD)")); ch2.set_size(dict(width=720, height=320)); ch2.set_legend(dict(position="bottom"))
    wi.insert_chart("F21", ch2)

    # ============================================================== Sensitivitas
    wsn = wb.add_worksheet("Sensitivitas"); wsn.set_column(0, 0, 36); wsn.set_column(1, 4, 15)
    base, res = RES["torn"]
    wsn.write(0, 0, "SENSITIVITAS NPV (+/-20%) - dihitung fin_core.tornado()", T)
    wsn.write_row(2, 0, ["Variabel", "NPV -20%", "NPV +20%", "Rentang", "NPV dasar"], H)
    for j, (lab, lo, hi) in enumerate(res):
        wsn.write(3 + j, 0, lab, TXT); wsn.write_number(3 + j, 1, lo, NEG); wsn.write_number(3 + j, 2, hi, NEG)
        wsn.write_formula(3 + j, 3, "=ABS(C%d-B%d)" % (4 + j, 4 + j), NUM, abs(hi - lo)); wsn.write_number(3 + j, 4, base, NUM)
    rr = 5 + len(res); wsn.write(rr, 0, "PROFIL NPV vs TINGKAT DISKONTO", B); wsn.write_row(rr + 1, 0, ["Tingkat diskonto", "NPV (USD, rumus NPV Excel)"], H)
    rates, nv = RES["curve"]
    for j, (rt, n_) in enumerate(zip(rates, nv)):
        wsn.write_number(rr + 2 + j, 0, float(rt), PCT)
        wsn.write_formula(rr + 2 + j, 1, "=%s+NPV(A%d,'Arus Kas'!$D$%d:$%s$%d)" % ("'Arus Kas'!$C$%d" % (rows["fcff"] + 1), rr + 3 + j, rows["fcff"] + 1, lastc, rows["fcff"] + 1), NEG, float(n_))
    c3 = wb.add_chart(dict(type="scatter", subtype="smooth"))
    c3.add_series(dict(name="NPV", categories="=Sensitivitas!$A$%d:$A$%d" % (rr + 3, rr + 2 + len(rates)), values="=Sensitivitas!$B$%d:$B$%d" % (rr + 3, rr + 2 + len(rates)), line=dict(color="#1f4e4a")))
    c3.set_title(dict(name="NPV vs tingkat diskonto")); c3.set_x_axis(dict(name="tingkat diskonto", num_format="0%")); c3.set_size(dict(width=620, height=320)); c3.set_legend(dict(none=True))
    wsn.insert_chart("G3", c3)
    rr2 = rr + 4 + len(rates); wsn.write(rr2, 0, "SKENARIO", B); wsn.write_row(rr2 + 1, 0, ["Skenario", "FCI USD", "NPV USD", "IRR", "Payback th"], H)
    for j, (n_, s) in enumerate(RES["SC"]):
        wsn.write(rr2 + 2 + j, 0, n_.replace("\n", " "), TXT); wsn.write_number(rr2 + 2 + j, 1, s["fci"], NUM); wsn.write_number(rr2 + 2 + j, 2, s["NPV"], NEG)
        wsn.write_number(rr2 + 2 + j, 3, s["IRR"], PCT); wsn.write_number(rr2 + 2 + j, 4, s["PBP"], NUM2)

    # ============================================================== Monte Carlo
    wm = wb.add_worksheet("Monte Carlo"); wm.set_column(0, 0, 34); wm.set_column(1, 6, 14)
    wm.write(0, 0, "MONTE CARLO (N = %d) - fin_core.monte_carlo()" % len(mc["NPV"]), T)
    wm.write_row(2, 0, ["Statistik", "NPV USD", "IRR", "Payback th"], H)
    I = mc["IRR"][np.isfinite(mc["IRR"])]; PBv = mc["PBP"][np.isfinite(mc["PBP"])]
    for j, (lab, fnc) in enumerate((("Rata-rata", np.mean), ("P10", lambda x: np.percentile(x, 10)), ("P50", lambda x: np.percentile(x, 50)), ("P90", lambda x: np.percentile(x, 90)), ("Simpangan baku", np.std))):
        wm.write(3 + j, 0, lab); wm.write_number(3 + j, 1, float(fnc(mc["NPV"])), NEG); wm.write_number(3 + j, 2, float(fnc(I)), PCT); wm.write_number(3 + j, 3, float(fnc(PBv)), NUM2)
    wm.write(9, 0, "Peluang NPV > 0", B); wm.write_number(9, 1, float((mc["NPV"] > 0).mean()), BPCT)
    wm.write(10, 0, "Peluang IRR > WACC", B); wm.write_number(10, 1, float((I > o["wacc"]).mean()), BPCT)
    wm.write(12, 0, "DISTRIBUSI INPUT", B); wm.write_row(13, 0, ["Input", "Distribusi", "Korelasi Spearman ke NPV"], H)
    DIST = dict(emult="Lognormal median 1, P5-P95 0,76-1,33 (dari MC proses P_net)", capex="Segitiga 0,90 / 1,00 / 1,35", opex="Segitiga 0,85 / 1,00 / 1,25",
                p_carbon="Segitiga 2,2 / 12 / 20 USD/t", F_loc="Diskrit 1,00 (30%) / 1,10 (70%)", avail="Segitiga 0,88 / 0,95 / 0,97",
                p_heat="Segitiga 8 / 18 / 25 USD/MWh", heat_util="Segitiga 0,15 / 0,40 / 0,60", r_debt="Segitiga 6,5 / 8 / 10%", infl="Segitiga 2 / 3 / 5%")
    for j, (k, sp) in enumerate(sorted(mc["spearman"].items(), key=lambda kv: -abs(kv[1]))):
        wm.write(14 + j, 0, k); wm.write(14 + j, 1, DIST[k], TXT); wm.write_number(14 + j, 2, sp, NUM2)
    h, edges = np.histogram(mc["NPV"], bins=30)
    wm.write_row(26, 0, ["Bin NPV (tengah)", "Frekuensi"], H)
    for j in range(len(h)):
        wm.write_number(27 + j, 0, float((edges[j] + edges[j + 1]) / 2), NUM); wm.write_number(27 + j, 1, int(h[j]), NUM)
    c4 = wb.add_chart(dict(type="column")); c4.add_series(dict(name="Frekuensi", categories="='Monte Carlo'!$A$28:$A$%d" % (27 + len(h)), values="='Monte Carlo'!$B$28:$B$%d" % (27 + len(h)), fill=dict(color="#3d8b7d"), gap=10))
    c4.set_title(dict(name="Histogram NPV")); c4.set_size(dict(width=620, height=320)); c4.set_legend(dict(none=True)); wm.insert_chart("F3", c4)

    # ============================================================== Skala & Armada
    wsk = wb.add_worksheet("Skala Set"); wsk.set_column(0, 0, 30); wsk.set_column(1, 3, 16)
    wsk.write(0, 0, "EKONOMI PER UKURAN PKS (desain bejana sama)", T); wsk.write_row(2, 0, ["Indikator", "30 t/jam", "45 t/jam", "60 t/jam"], H)
    TR = RES["tiers"]
    for j, (lab, key, fm) in enumerate((("Jumlah reaktor", None, NUM), ("FCI USD", "fci", NUM), ("Listrik GWh/th (th penuh)", "E2", NUM2), ("Pendapatan th penuh USD", "rev2", NUM),
                                        ("NPV USD", "NPV", NEG), ("IRR", "IRR", PCT), ("Payback th", "PBP", NUM2), ("LCOE USD/kWh", "LCOE", NUM4))):
        wsk.write(3 + j, 0, lab)
        for c_, t in enumerate(("30", "45", "60")):
            ot = TR[t]
            val = F.R["tiers"][t]["N_modules"] if key is None else ot["E"][2] if key == "E2" else ot["rev"][2] if key == "rev2" else ot[key]
            wsk.write_number(3 + j, 1 + c_, float(val), fm)
    wsk.write(12, 0, "Set > 1 MW (60 t/jam) memakai tarif Perpres 112 >1-3 MW (9,94 USc/kWh x F).", NOTE)
    wfl = wb.add_worksheet("Armada"); wfl.set_column(0, 0, 30); wfl.set_column(1, len(fl["years"]), 11)
    wfl.write(0, 0, "MODEL PERUSAHAAN: penggelaran armada BOO, kurva belajar 90%%, unit-1 FOAK +20%%, overhead korporat", T)
    wfl.write(2, 0, "Tahun", H); wfl.write_row(2, 1, fl["years"], H)
    for j, (lab, key, fm) in enumerate((("Set baru", "sets_new", NUM), ("Set beroperasi", "sets_op", NUM), ("Listrik GWh", "E", NUM2), ("Kredit karbon tCO2e", "co2", NUM),
                                        ("Pendapatan USD", "rev", NUM), ("OPEX USD", "opex", NUM), ("EBITDA USD", "ebitda", NUM), ("CAPEX + sustaining USD", "capex", NUM),
                                        ("Overhead korporat USD", "overhead", NUM), ("FCFF perusahaan USD", "fcff_co", NEG))):
        wfl.write(3 + j, 0, lab, B if key == "fcff_co" else None)
        for c_, val in enumerate(fl[key]): wfl.write_number(3 + j, 1 + c_, float(val), fm)
    rF = 3 + 9 + 1; lc = coln(len(fl["years"]))
    wfl.write(rF + 1, 0, "Kumulatif FCFF", B)
    for c_ in range(len(fl["years"])):
        wfl.write_formula(rF, 1 + c_, "=%s%d" % (coln(1 + c_), rF) if c_ == 0 else "=%s%d+%s%d" % (coln(c_), rF + 1, coln(1 + c_), rF), NEG)
    wfl.write(rF, 0, "Kumulatif FCFF", B)
    wfl.write(rF + 2, 0, "NPV perusahaan @WACC", B); wfl.write_formula(rF + 2, 1, "=B%d+NPV(WACC,C%d:%s%d)" % (rF, rF, lc, rF), BNUM, fl["NPV"])
    wfl.write(rF + 3, 0, "IRR perusahaan", B); wfl.write_formula(rF + 3, 1, "=IRR(B%d:%s%d)" % (rF, lc, rF), BPCT, fl["IRR"])
    wfl.write(rF + 4, 0, "Puncak kebutuhan dana", B); wfl.write_formula(rF + 4, 1, "=-MIN(B%d:%s%d)" % (rF + 1, lc, rF + 1), BNUM, fl["peak"])
    wfl.write(rF + 6, 0, "Biaya CAPEX per unit (relatif unit-1 harga dasar)", B); wfl.write_row(rF + 7, 0, ["Unit ke-", "Tahun", "Faktor CAPEX", "NPV unit USD", "IRR unit"], H)
    for j, (n_, y0, cm, nv_, ir) in enumerate(fl["units"]):
        wfl.write_row(rF + 8 + j, 0, [n_, y0]); wfl.write_number(rF + 8 + j, 2, cm, NUM2); wfl.write_number(rF + 8 + j, 3, nv_, NEG); wfl.write_number(rF + 8 + j, 4, ir, PCT)

    # ============================================================== Pasar, PESTLE, Porter
    mk = RES["mk"]
    wp = wb.add_worksheet("Pasar"); wp.set_column(0, 0, 44); wp.set_column(1, 2, 18); wp.set_column(3, 3, 70)
    wp.write(0, 0, "UKURAN PASAR (TAM-SAM-SOM)", T); wp.write_row(2, 0, ["Parameter", "Nilai", "Satuan", "Sumber"], H)
    MR = [("Jumlah PKS Indonesia", MK.MILLS, "PKS", "Universal Mill List (2023 data, publ. 2025)"), ("POME nasional", MK.POME_NAT, "m3/th", "PASPI/BRIN 2026 (125-170 juta)"),
          ("Pendapatan per m3 POME (model)", mk["rev_m3"], "USD/m3", "Arus Kas th penuh / POME diolah"), ("Porsi PKS 30-60 t/jam", MK.SH_SIZE, "-", "[UNVERIFIED] estimasi"),
          ("Porsi tanpa penangkap metana", MK.SH_NOCAP, "-", "T&E 2025: ~10% sudah menangkap"), ("Porsi Sumatera + Kalimantan", MK.SH_REGION, "-", "Sebaran PKS"),
          ("Set SOM s/d 2034", mk["sets_SOM"], "set", "Rencana penggelaran (Armada)")]
    for j, (lab, val, u, src) in enumerate(MR):
        wp.write(3 + j, 0, lab); wp.write_number(3 + j, 1, float(val), INP); wp.write(3 + j, 2, u); wp.write(3 + j, 3, src)
    wp.write(11, 0, "TAM (USD/th)", B); wp.write_formula(11, 1, "=B5*B6", BNUM, mk["TAM"])
    wp.write(12, 0, "SAM (USD/th)", B); wp.write_formula(12, 1, "=B12*B7*B8*B9", BNUM, mk["SAM"])
    wp.write(13, 0, "SOM (USD/th, 2034)", B); wp.write_formula(13, 1, "=B10*'Arus Kas'!E%d" % (rows["rev"] + 1), BNUM, mk["SOM"])
    wp.write(14, 0, "Pangsa SOM / SAM", B); wp.write_formula(14, 1, "=B14/B13", BPCT, mk["share"])
    wp.write(15, 0, "PKS sasaran (SAM)", B); wp.write_formula(15, 1, "=ROUND(B4*B7*B8*B9,0)", BNUM, mk["sets_SAM"])
    wp.write(17, 0, "PEMBANDING TEKNOLOGI", B); wp.write_row(18, 0, ["Teknologi", "CAPEX USD juta/MW", "Lahan ha", "Waktu bangun bln", "Portabel", "Mutu efluen", "Pemain"], H)
    for j, row_ in enumerate(MK.COMPET): wp.write_row(19 + j, 0, row_, TXT)
    wpe = wb.add_worksheet("PESTLE"); wpe.set_column(0, 0, 6); wpe.set_column(1, 1, 12); wpe.set_column(2, 2, 52); wpe.set_column(3, 6, 10); wpe.set_column(7, 7, 60)
    wpe.write(0, 0, "ANALISIS PESTLE (skor = tanda x dampak x peluang)", T)
    wpe.write_row(2, 0, ["Kode", "Kategori", "Faktor", "Tanda", "Dampak 1-5", "Peluang 1-5", "Skor", "Keterangan"], H)
    for j, (k, c_, f_, s_, i_, l_, d_) in enumerate(MK.PESTLE):
        rr = 3 + j; wpe.write_row(rr, 0, [k, c_, f_], TXT); wpe.write_number(rr, 3, s_, INP); wpe.write_number(rr, 4, i_, INP); wpe.write_number(rr, 5, l_, INP)
        wpe.write_formula(rr, 6, "=D%d*E%d*F%d" % (rr + 1, rr + 1, rr + 1), NEG, s_ * i_ * l_); wpe.write(rr, 7, d_, TXT)
    rr = 4 + len(MK.PESTLE); wpe.write_row(rr, 1, ["Kategori", "Skor bersih"], H)
    ps = MK.pestle_scores()
    for j, c_ in enumerate(ps):
        wpe.write(rr + 1 + j, 1, c_); wpe.write_formula(rr + 1 + j, 2, '=SUMIF($B$4:$B$%d,B%d,$G$4:$G$%d)' % (3 + len(MK.PESTLE), rr + 2 + j, 3 + len(MK.PESTLE)), NEG, ps[c_])
    wpe.write(rr + 7, 1, "Total", B); wpe.write_formula(rr + 7, 2, "=SUM(C%d:C%d)" % (rr + 2, rr + 7), BNEG, sum(ps.values()))
    wpt = wb.add_worksheet("Porter"); wpt.set_column(0, 0, 20); wpt.set_column(1, 1, 46); wpt.set_column(2, 2, 12); wpt.set_column(3, 3, 50)
    wpt.write(0, 0, "LIMA KEKUATAN PORTER (tekanan 1 rendah - 5 tinggi)", T); wpt.write_row(2, 0, ["Kekuatan", "Sub-faktor", "Skor", "Alasan"], H)
    rr = 3; summ = []
    for f_, subs in MK.PORTER.items():
        r0 = rr
        for s_, sc, why in subs:
            wpt.write(rr, 0, f_, TXT); wpt.write(rr, 1, s_, TXT); wpt.write_number(rr, 2, sc, INP); wpt.write(rr, 3, why, TXT); rr += 1
        summ.append((f_, r0, rr - 1))
    rr += 1; wpt.write_row(rr, 0, ["Kekuatan", "Skor rata-rata"], H)
    for j, (f_, a_, b_) in enumerate(summ):
        wpt.write(rr + 1 + j, 0, f_); wpt.write_formula(rr + 1 + j, 1, "=AVERAGE(C%d:C%d)" % (a_ + 1, b_ + 1), NUM2, float(np.mean([s for _, s, _ in MK.PORTER[f_]])))
    # ============================================================== Sumber
    wsr = wb.add_worksheet("Sumber"); wsr.set_column(0, 0, 150)
    wsr.write(0, 0, "SUMBER DATA (lihat finance/research/market_data.md untuk tabel lengkap + URL)", T)
    for j, l_ in enumerate(open(os.path.join(F.HERE, "research", "market_data.md"), encoding="utf-8").read().splitlines()):
        wsr.write(2 + j, 0, l_)

    # ============================================================== Ringkasan
    ws0.set_column(0, 0, 44); ws0.set_column(1, 1, 18); ws0.set_column(2, 2, 4)
    ws0.write(0, 0, "MODEL KEUANGAN - GENERATOR BIOGAS PORTABEL AnMBR TERMOFILIK (1 set PKS 45 t TBS/jam, BOO)", T)
    ws0.write(1, 0, "Semua angka mengalir dari lembar Asumsi -> CAPEX/OPEX -> Arus Kas -> Indikator. Sel kuning = input.", NOTE)
    KP = [("FCI (USD)", "=FCI", o["fci"], BNUM), ("USD per kWe kotor", "=FCI/t_P_gross", o["fci"] / F.TECH["P_gross"], BNUM),
          ("Pendapatan th penuh (USD)", "='Arus Kas'!E%d" % (rows["rev"] + 1), o["rev"][2], BNUM), ("EBITDA th penuh (USD)", "='Arus Kas'!E%d" % (rows["ebitda"] + 1), o["ebitda"][2], BNUM),
          ("NPV @WACC (USD)", "=Indikator!B4", o["NPV"], BNUM), ("IRR proyek", "=Indikator!B5", o["IRR"], BPCT), ("IRR ekuitas", "=Indikator!B6", o["IRR_eq"], BPCT),
          ("WACC", "=WACC", o["wacc"], BPCT), ("Payback sejak COD (th)", "=Indikator!B8", o["PBP"], BN2), ("Payback terdiskonto (th)", "=Indikator!B9", o["DPBP"], BN2),
          ("DSCR minimum", "=Indikator!B11", o["DSCR_min"], BN2), ("LCOE (USD/kWh)", "=Indikator!B12", o["LCOE"], BN2),
          ("Peluang NPV > 0 (Monte Carlo)", "='Monte Carlo'!B10", float((mc["NPV"] > 0).mean()), BPCT),
          ("NPV perusahaan (armada %d set)" % sum(F.ROLL.values()), "=Armada!B%d" % (rF + 3), fl["NPV"], BNUM), ("IRR perusahaan", "=Armada!B%d" % (rF + 4), fl["IRR"], BPCT)]
    for j, (lab, f, val, fm) in enumerate(KP):
        ws0.write(3 + j, 0, lab); ws0.write_formula(3 + j, 1, f, fm, float(val) if np.isfinite(val) else 0)
    figs = RES["figs"]
    ws0.insert_image("D3", figs["cf"], dict(x_scale=.42, y_scale=.42)); ws0.insert_image("D22", figs["pb"], dict(x_scale=.42, y_scale=.42))
    ws0.insert_image("D41", figs["npv"], dict(x_scale=.40, y_scale=.40)); ws0.insert_image("A22", figs["capex"], dict(x_scale=.24, y_scale=.24))
    wg = wb.add_worksheet("Gambar")
    yy = 0
    for k in ("pasar", "porter", "capex", "cf", "npv", "pb", "bep", "mc", "fleet", "sc"):
        wg.insert_image(yy, 0, figs[k], dict(x_scale=.45, y_scale=.45)); yy += 48 if k == "porter" else 26
    wb.close()
    return OUT

def verify(path=OUT):
    """hitung ulang dengan LibreOffice headless dan bandingkan indikator dengan Python"""
    import openpyxl, tempfile
    tmp = tempfile.mkdtemp()
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", tmp, path], capture_output=True, timeout=180)
    wb = openpyxl.load_workbook(os.path.join(tmp, os.path.basename(path)), data_only=True)
    ws = wb["Indikator"]
    return {ws.cell(r, 1).value: ws.cell(r, 2).value for r in range(4, 15)}
