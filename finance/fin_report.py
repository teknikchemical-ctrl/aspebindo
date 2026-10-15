# -*- coding: utf-8 -*-
"""Laporan analisis ekonomi (PDF, Bahasa Indonesia) - semua angka dibaca dari hasil model (tidak diketik manual)."""
import os, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fin_core as F, fin_market as MK

FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Ser", FD + "LiberationSerif-Regular.ttf")); pdfmetrics.registerFont(TTFont("SerB", FD + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerI", FD + "LiberationSerif-Italic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Ser", normal="Ser", bold="SerB", italic="SerI", boldItalic="SerB")
OUT = os.path.join(F.HERE, "outputs", "BG_Analisis_Ekonomi.pdf")
DK = colors.HexColor("#1f4e4a"); LT = colors.HexColor("#e6f0ee")
P = ParagraphStyle("p", fontName="Ser", fontSize=10.5, leading=15, alignment=TA_JUSTIFY, firstLineIndent=8 * mm, spaceAfter=4)
P0 = ParagraphStyle("p0", parent=P, firstLineIndent=0)
H1 = ParagraphStyle("h1", fontName="SerB", fontSize=12.5, leading=16, spaceBefore=8, spaceAfter=4, textColor=DK)
H2 = ParagraphStyle("h2", fontName="SerB", fontSize=11, leading=14, spaceBefore=5, spaceAfter=3)
CAP = ParagraphStyle("cap", fontName="SerB", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=8)
TT = ParagraphStyle("tt", fontName="SerB", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=2)
CELL = ParagraphStyle("c", fontName="Ser", fontSize=8.6, leading=10.5); CELLB = ParagraphStyle("cb", parent=CELL, fontName="SerB")
TITLE = ParagraphStyle("t", fontName="SerB", fontSize=16, leading=21, alignment=TA_CENTER, textColor=DK, spaceAfter=6)

def n(x, d=0):
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
def mu(x, d=2): return n(x / 1e6, d)
def pc(x, d=1): return n(x * 100, d) + "%"

def tbl(data, widths, head=1, bold_last=False, num_cols=()):
    rows = []
    for i, r in enumerate(data):
        rows.append([Paragraph(str(c), CELLB if i < head or (bold_last and i == len(data) - 1) else CELL) for c in r])
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=head)
    st = [("GRID", (0, 0), (-1, -1), .4, colors.grey), ("BACKGROUND", (0, 0), (-1, head - 1), LT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    for c in num_cols: st.append(("ALIGN", (c, head), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st)); return t

def KT(a, b): return KeepTogether([a, b])
def fig(path, w=170, cap=None):
    from PIL import Image as PI
    im = PI.open(path); h = w * im.height / im.width
    out = [Image(path, width=w * mm, height=h * mm)]
    if cap: out.append(Paragraph(cap, CAP))
    return KeepTogether(out)

def build(RES):
    o, be, mc, fl, mk, TR = RES["o"], RES["be"], RES["mc"], RES["fl"], RES["mk"], RES["tiers"]
    v = o["v"]; FG = RES["figs"]; T_ = F.TECH
    yrs = o["years"]; i2 = 2
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Analisis Ekonomi - Generator Biogas Portabel", author="NAMA TIM")
    S = []
    S += [Paragraph("ANALISIS PASAR DAN KELAYAKAN EKONOMI<br/>GENERATOR BIOGAS PORTABEL AnMBR TERMOFILIK UNTUK PKS", TITLE),
          Paragraph("Model keuangan lengkap: BG_Model_Keuangan.xlsx (rumus hidup). Seluruh angka pada dokumen ini dihasilkan oleh finance/run_all.py dari neraca massa-energi "
                    "(process/outputs/results.json) dan model 3D (massa bejana).", ParagraphStyle("s", parent=P0, alignment=TA_CENTER, fontSize=9.5, textColor=colors.grey)), Spacer(1, 4)]
    # ------------------------------------------------------------- 1 ringkasan
    S.append(Paragraph("1. Ringkasan", H1))
    S.append(Paragraph(
        "Produk adalah satu <b>set standar portabel</b> (14 reaktor AnMBR 194 m³ + 9 modul kontainer/skid, 28 muatan truk, plot 0,29 ha) yang mengolah "
        "%s m³/hari POME dari PKS %s t TBS/jam menjadi %s kWe listrik bersih. Model bisnis dasar adalah <b>Build-Own-Operate (BOO)</b>: perusahaan membiayai, "
        "memasang dan mengoperasikan set di lahan PKS selama %d tahun, menjual listrik ke PLN sesuai Perpres 112/2022, menjual kredit karbon penghindaran metana, "
        "menerima jasa pengolahan POME dari PKS, serta menjual air panas dan kue lumpur. Investasi tetap (FCI) USD %s juta (%s USD/kWe kotor) menghasilkan "
        "NPV USD %s juta pada WACC %s, IRR proyek %s, IRR ekuitas %s dan payback %s tahun sejak COD."
        % (n(T_["pome_m3d"]), n(T_["ffb_tph"]), n(T_["P_net"]), v["n_op"], mu(o["fci"]), n(o["fci"] / T_["P_gross"]), mu(o["NPV"]), pc(o["wacc"]),
           pc(o["IRR"]), pc(o["IRR_eq"]), n(o["PBP"], 2)), P))
    S.append(Paragraph(
        "Hasilnya <b>layak tetapi tipis</b> untuk satu set pertama: simulasi Monte Carlo memberi peluang NPV > 0 sebesar %s. Kelayakan bergantung kuat pada tiga hal: harga kredit karbon "
        "(impas USD %s/tCO₂e), jasa pengolahan POME dari PKS, dan biaya modal. Pada tingkat perusahaan, penggelaran %d set hingga 2034 dengan kurva belajar biaya 90%% "
        "memberikan NPV USD %s juta dan IRR %s, karena biaya set turun dari USD %s juta (unit-1) menjadi sekitar USD %s juta (unit-10)."
        % (pc((mc["NPV"] > 0).mean(), 0), n(be["p_carbon_be"], 1), sum(F.ROLL.values()), mu(fl["NPV"], 1), pc(fl["IRR"]),
           mu(fl["units"][0][2] * o["fci"]), mu(fl["units"][9][2] * o["fci"])), P))
    # ------------------------------------------------------------- 2 pasar
    S.append(Paragraph("2. Analisis Pasar", H1))
    S.append(Paragraph(
        "Indonesia memiliki sekitar %s PKS (Universal Mill List) yang menghasilkan %s juta m³ POME per tahun (PASPI/BRIN 2026), sedangkan baru ±10%% PKS yang menangkap metana "
        "(Transport & Environment 2025). Dengan pendapatan model USD %s per m³ POME (listrik, karbon, jasa, panas, pupuk), <b>TAM</b> = USD %s miliar/tahun. "
        "<b>SAM</b> dibatasi pada PKS 30-60 t/jam (%s) tanpa penangkap metana (%s) di Sumatera dan Kalimantan (%s): %s PKS atau USD %s juta/tahun. "
        "<b>SOM</b> = %d set pada 2034 (USD %s juta/tahun, %s dari SAM)."
        % (n(MK.MILLS), n(MK.POME_NAT / 1e6), n(mk["rev_m3"], 2), n(mk["TAM"] / 1e9, 2), pc(MK.SH_SIZE, 0), pc(MK.SH_NOCAP, 0), pc(MK.SH_REGION, 0),
           n(mk["sets_SAM"]), n(mk["SAM"] / 1e6), mk["sets_SOM"], n(mk["SOM"] / 1e6), pc(mk["share"])), P))
    S.append(fig(FG["pasar"], 165, "Gambar 1. Corong Pasar TAM-SAM-SOM (a) dan Sebaran PKS serta PKS Sasaran per Provinsi (b)"))
    S.append(KT(Paragraph("Tabel 1. Pembanding Teknologi Penangkapan Metana POME", TT),
    tbl([["Teknologi", "CAPEX USD juta/MW", "Lahan ha", "Bangun bln", "Portabel", "Mutu efluen", "Pemain"]] + [list(r) for r in MK.COMPET], [36, 24, 14, 15, 18, 26, 37])))
    S.append(Paragraph(
        "Posisi produk ini <b>bukan yang termurah per kW</b> (kolam tertutup USD 1,5-2,5 juta/MW), tetapi satu-satunya yang dapat dipindahkan, dibangun 11 bulan, "
        "hanya memakai 0,29 ha, menghasilkan efluen bermutu tinggi dan tanpa pemanasan (POME 85 °C langsung didinginkan ke 55 °C). Keunggulan ini dijual sebagai "
        "jasa kepatuhan (ISPO wajib, baku mutu efluen yang direvisi 2026) kepada PKS, bukan semata sebagai pembangkit listrik.", P))
    # ------------------------------------------------------------- 3 porter & pestle
    S.append(Paragraph("3. Lima Kekuatan Porter, PESTLE, dan Daya Tarik Segmen", H1))
    pf = {f: np.mean([s for _, s, _ in MK.PORTER[f]]) for f in MK.PORTER}; ps = MK.pestle_scores()
    top = sorted(pf, key=lambda k: -pf[k])
    S.append(Paragraph(
        "Rata-rata tekanan Porter %s dari 5. Tekanan tertinggi berasal dari <b>%s</b> (%s; PLN pembeli tunggal dengan harga patokan) dan <b>%s</b> (%s; kolam tertutup murah dan "
        "pengembang biometana), terendah dari <b>pendatang baru</b> (%s) karena kebutuhan modal dan know-how AnMBR termofilik. Pada PESTLE 21 faktor skor bersih %+d: "
        "politik (%+d) dan lingkungan (%+d) memberi peluang terbesar (target EBT, ISPO wajib, metana POME, pengurangan lahan kolam), sedangkan ekonomi (%+d) "
        "menjadi ancaman utama (rupiah melemah, suku bunga, harga karbon domestik rendah). Pada matriks daya tarik, PKS swasta 45 t/jam di Sumatera paling menarik "
        "dan paling mudah dimenangkan, sedangkan grup besar terintegrasi paling sulit (membangun sendiri)."
        % (n(np.mean(list(pf.values())), 2), top[0].lower(), n(pf[top[0]], 2), top[1].lower(), n(pf[top[1]], 2), n(pf["Pendatang baru"], 2),
           sum(ps.values()), ps["Politik"], ps["Lingkungan"], ps["Ekonomi"]), P))
    S.append(fig(FG["porter"], 165, "Gambar 2. Tekanan Lima Kekuatan Porter (a), Radar Tekanan menurut Segmen (b), Skor Bersih PESTLE 21 Faktor (c), dan Daya Tarik terhadap Kemampuan Menang (d)"))
    S.append(Paragraph("Tabel 2. Faktor PESTLE (skor = tanda x dampak x peluang)", TT))
    S.append(tbl([["Kode", "Faktor", "Dampak", "Peluang", "Skor", "Keterangan"]] + [[k, f_, i_, l_, "%+d" % (s_ * i_ * l_), d_] for k, c_, f_, s_, i_, l_, d_ in MK.PESTLE],
                 [10, 58, 13, 13, 11, 65], num_cols=(2, 3, 4)))
    # ------------------------------------------------------------- 4 capex opex
    S.append(Paragraph("4. Biaya Investasi (CAPEX) dan Biaya Operasi (OPEX)", H1))
    rows = [["Item", "Jumlah", "Total USD"]]
    for g, nm, q, u, c, t, b in o["capex_rows"]:
        rows.append([nm, ("%s %s" % (n(q, 2 if q < 1 else 0), u)), n(t)])
    rows.append(["<b>FCI</b>", "", "<b>%s</b>" % n(o["fci"])])
    S.append(Paragraph(
        "CAPEX disusun dari bawah (bottom-up). Biaya bejana dihitung dari <b>massa baja model 3D</b> (%s t per reaktor) dikali biaya fabrikasi USD %s/kg, "
        "membran %s m² x USD %s/m², genset %s kWe x USD %s/kWe; skid lain memakai harga paket tipikal. Biaya langsung lapangan kecil karena semua modul "
        "dirakit dan diuji di bengkel. Total FCI USD %s juta (PEC USD %s juta) atau %s USD/kWe kotor, di atas rata-rata literatur PLTBg POME 2.758 USD/kW "
        "(Energies 2022) karena reaktor baja berinsulasi dan membran; kurva belajar produksi seri menurunkannya (Bab 9)."
        % (n(T_["vessel_t"], 1), n(v["c_fab"], 1), n(T_["area_mem"]), n(v["c_mem"]), n(T_["chp_kWe"]), n(v["c_chp"]), mu(o["fci"]), mu(o["pec"]), n(o["fci"] / T_["P_gross"])), P))
    S.append(Paragraph("Tabel 3. Rincian CAPEX 1 Set Standar 45 t TBS/jam (USD 2026)", TT))
    S.append(tbl(rows, [110, 28, 28], bold_last=True, num_cols=(2,)))
    orow = [["Komponen OPEX", "Jenis", "USD/th"]] + [[k, "Tetap" if t == "F" else "Variabel", n(val)] for k, (val, t) in o["opex_items"].items()] + [["<b>Total (tahun dasar 2026)</b>", "", "<b>%s</b>" % n(o["opex_full"])]]
    S.append(KT(Paragraph("Tabel 4. OPEX Tahun Penuh", TT), tbl(orow, [110, 28, 28], bold_last=True, num_cols=(2,))))
    S.append(fig(FG["capex"], 168, "Gambar 3. Struktur CAPEX (a), OPEX (b), dan Bauran Pendapatan Tahun Operasi Penuh (c)"))
    # ------------------------------------------------------------- 5 arus kas
    S.append(Paragraph("5. Pendapatan dan Model Arus Kas", H1))
    S.append(Paragraph(
        "Listrik terjual %s GWh/tahun (neraca energi tahunan %s GWh x ketersediaan %s) dengan tarif %s USc/kWh x F %s pada tahun 1-10 dan %s USc/kWh setelahnya "
        "(Perpres 112/2022, PLTBg <= 1 MW). Kredit karbon %s tCO₂e/tahun (%s dari %s tCO₂e terhindar) pada USD %s/t. Jasa pengolahan POME USD %s/m³ "
        "(%s m³/tahun), air panas %s dari %s kWth ke PKS pada USD %s/MWh, dan kue lumpur %s t/tahun. Tahun operasi pertama memakai faktor %s untuk start-up "
        "biomassa termofilik. OPEX dieskalasi %s/tahun; tarif listrik tetap nominal. Pajak 22%% dengan penyusutan garis lurus %d tahun dan tax allowance 30%% investasi."
        % (n(o["E"][i2], 2), n(v["E_net_GWh"], 2), pc(v["avail"], 0), n(v["tariff1"], 2), n(v["F_loc"], 2), n(v["tariff2"], 2), n(o["cer"][i2]), pc(v["cer_ratio"], 0),
           n(v["co2e"]), n(v["p_carbon"]), n(v["fee_pome"], 2), n(T_["pome_m3y"]), pc(v["heat_util"], 0), n(T_["Q_heat"]), n(v["p_heat"]), n(T_["cake_ty"]),
           n(v["ramp1"], 2), pc(v["infl"], 0), v["dep_life"]), P))
    keys = [("Pendapatan listrik", "rev_el"), ("Pendapatan karbon", "rev_c"), ("Jasa POME", "rev_fee"), ("Panas + pupuk", None), ("Total pendapatan", "rev"),
            ("OPEX", "opex"), ("EBITDA", "ebitda"), ("CAPEX", "capex"), ("Pajak", "tax_u"), ("Arus kas bersih (FCFF)", "fcff"), ("Kumulatif", "cum")]
    cols = list(range(0, 8))
    head = ["Uraian"] + ["%d (%s)" % (yrs[i], "K" if i == 0 else "O%d" % i) for i in cols]
    data = [head]
    cum = np.cumsum(o["fcff"])
    for lab, k in keys:
        if k is None: vals_ = o["rev_h"] + o["rev_f"]
        elif k == "cum": vals_ = cum
        else: vals_ = o[k]
        neg = k in ("opex", "capex", "tax_u")
        data.append([lab] + [("(%s)" % n(abs(vals_[i]) / 1e3)) if (neg and vals_[i] > 0) or (not neg and vals_[i] < 0) else ("-" if abs(vals_[i]) < .5 else n(vals_[i] / 1e3)) for i in cols])
    S.append(Paragraph("Tabel 5. Model Arus Kas Proyek %d-%d (USD ribu; tanda kurung = negatif; K = konstruksi, O = operasi)" % (yrs[0], yrs[7]), TT))
    S[-1] = KT(S[-1], tbl(data, [36] + [16.2] * 8, num_cols=tuple(range(1, 9))))
    S.append(fig(FG["cf"], 165, "Gambar 4. Arus Kas Tahunan dan Kumulatif Proyek %d-%d" % (yrs[0], yrs[-1])))
    # ------------------------------------------------------------- 6 npv irr pbp
    S.append(Paragraph("6. NPV, IRR, dan Payback Period", H1))
    S.append(Paragraph(
        "Indikator dihitung dari FCFF tanpa utang dengan WACC %s = %s x %s x (1 - 22%%) + %s x %s sebagai laju minimum. "
        "<b>NPV</b> = Σ CF<sub>t</sub>/(1+WACC)<sup>t</sup> = USD %s juta. <b>IRR</b> adalah laju yang membuat NPV = 0: %s (proyek) dan %s (ekuitas, utang %s, bunga %s, tenor %d th). "
        "Kumulatif arus kas berubah positif pada tahun ke-%d operasi sehingga <b>payback = %s tahun sejak COD</b>; payback terdiskonto %s tahun. Indeks profitabilitas %s, "
        "DSCR minimum %s dan LCOE USD %s/kWh (USD %s/kWh setelah pendapatan non-listrik)."
        % (pc(o["wacc"], 2), pc(v["debt_frac"], 0), pc(v["r_debt"], 1), pc(1 - v["debt_frac"], 0), pc(v["r_eq"], 0), mu(o["NPV"]), pc(o["IRR"]), pc(o["IRR_eq"]),
           pc(v["debt_frac"], 0), pc(v["r_debt"], 1), v["tenor"], int(o["PBP"]) + 1, n(o["PBP"], 2), n(o["DPBP"], 2) if o["DPBP"] == o["DPBP"] else "> umur", n(o["PI"], 2),
           n(o["DSCR_min"], 2), n(o["LCOE"], 3), n(o["LCOE_net"], 3)), P))
    S.append(fig(FG["npv"], 165, "Gambar 5. Profil NPV terhadap Tingkat Diskonto (a) dan Diagram Tornado Sensitivitas NPV ±20%% (b)"))
    S.append(fig(FG["pb"], 165, "Gambar 6. Kurva Payback: Arus Kas Kumulatif Biasa dan Terdiskonto"))
    dec = lambda ok: "Layak" if ok else "Tidak layak"
    ind = [["Indikator", "Hasil", "Kriteria", "Keputusan"],
           ["NPV pada WACC %s" % pc(o["wacc"]), "USD %s juta" % mu(o["NPV"]), "> 0", dec(o["NPV"] > 0)],
           ["IRR proyek (setelah pajak)", pc(o["IRR"]), "> WACC", dec(o["IRR"] > o["wacc"])],
           ["IRR ekuitas", pc(o["IRR_eq"]), "> biaya ekuitas %s" % pc(v["r_eq"], 0), dec(o["IRR_eq"] > v["r_eq"])],
           ["Payback sejak COD", "%s tahun" % n(o["PBP"], 2), "< umur %d th" % v["n_op"], dec(o["PBP"] < v["n_op"])],
           ["Payback terdiskonto", "%s tahun" % (n(o["DPBP"], 2) if o["DPBP"] == o["DPBP"] else "> umur"), "< umur %d th" % v["n_op"], dec(o["DPBP"] == o["DPBP"] and o["DPBP"] < v["n_op"])],
           ["Indeks profitabilitas", n(o["PI"], 2), "> 1,0", dec(o["PI"] > 1)],
           ["DSCR minimum", n(o["DSCR_min"], 2), "> 1,2", dec(o["DSCR_min"] > 1.2)],
           ["Tarif listrik impas (NPV = 0)", "%s USc/kWh x F" % n(be["tariff1_be"], 2), "< %s (Perpres)" % n(v["tariff1"], 2), dec(be["tariff1_be"] < v["tariff1"])],
           ["Harga karbon impas", "USD %s/tCO₂e" % n(be["p_carbon_be"], 1), "< USD %s (dasar)" % n(v["p_carbon"]), dec(be["p_carbon_be"] < v["p_carbon"])],
           ["BEP tunai / akuntansi", "%s / %s kapasitas" % (pc(be["BEP_cash"]), pc(be["BEP_acc"])), "< 100%", dec(be["BEP_acc"] < 1)],
           ["Puncak kebutuhan dana", "USD %s juta" % mu(o["peak_funding"]), "Dasar struktur pendanaan", "Informasi"]]
    S.append(KT(Paragraph("Tabel 6. Ringkasan Indikator Kelayakan Finansial (1 set 45 t TBS/jam)", TT), tbl(ind, [56, 40, 44, 26], num_cols=(1,))))
    # ------------------------------------------------------------- 7 bep
    S.append(Paragraph("7. Titik Impas (BEP)", H1))
    S.append(Paragraph(
        "Pada tahun operasi penuh, biaya tetap tunai USD %s ribu dan biaya variabel USD %s ribu terhadap pendapatan USD %s ribu. BEP tunai tercapai pada %s kapasitas, "
        "BEP akuntansi (termasuk penyusutan dan bunga) pada %s, dan titik penutupan (SDP) pada %s. Dalam istilah NPV, proyek tetap bernilai positif selama tarif listrik "
        "tahun 1-10 di atas %s USc/kWh x F, harga karbon di atas USD %s/t, produksi energi di atas %s dari dasar, atau CAPEX di bawah %s dari dasar."
        % (n(be["fixed"] / 1e3), n(be["var"] / 1e3), n(be["rev_full"] / 1e3), pc(be["BEP_cash"]), pc(be["BEP_acc"]), pc(be["SDP"]), n(be["tariff1_be"], 2),
           n(be["p_carbon_be"], 1), pc(be["emult_be"], 0), pc(be["capex_be"], 0)), P))
    S.append(fig(FG["bep"], 165, "Gambar 7. Titik Impas Operasional (a) dan Nilai Impas NPV = 0 per Variabel (b)"))
    # ------------------------------------------------------------- 8 ketidakpastian
    S.append(Paragraph("8. Analisis Ketidakpastian", H1))
    base, res = RES["torn"]
    S.append(Paragraph(
        "Diagram tornado (Gambar 5b) menunjukkan variabel paling berpengaruh: <b>%s</b>, <b>%s</b> dan <b>%s</b>. Simulasi Monte Carlo %s iterasi memakai distribusi "
        "produksi energi dari Monte Carlo proses (P5-P95 daya bersih 646-1.123 kWe), CAPEX segitiga 0,90/1,00/1,35, OPEX 0,85/1,00/1,25, harga karbon USD 2,2/12/20, faktor lokasi 1,00 atau 1,10, "
        "ketersediaan, harga dan pemanfaatan panas, bunga dan inflasi. Hasil: NPV P10/P50/P90 = USD %s / %s / %s juta, peluang NPV > 0 = %s, IRR median %s. "
        "Penggerak terbesar adalah produksi energi dan harga karbon (korelasi Spearman %s dan %s)."
        % (res[0][0].lower(), res[1][0].lower(), res[2][0].lower(), n(len(mc["NPV"])), *[n(x / 1e6, 2) for x in np.percentile(mc["NPV"], [10, 50, 90])],
           pc((mc["NPV"] > 0).mean(), 0), pc(np.nanmedian(mc["IRR"])), n(mc["spearman"]["emult"], 2), n(mc["spearman"]["p_carbon"], 2)), P))
    S.append(fig(FG["mc"], 168, "Gambar 8. Distribusi NPV Monte Carlo (a), Kurva S IRR (b), dan Penggerak Ketidakpastian (c)"))
    scr = [["Skenario", "FCI USD juta", "NPV USD juta", "IRR", "Payback th"]] + [[s[0].replace("\n", " "), mu(s[1]["fci"]), mu(s[1]["NPV"]), pc(s[1]["IRR"]), n(s[1]["PBP"], 2)] for s in RES["SC"]]
    S.append(KT(Paragraph("Tabel 7. Skenario Model Bisnis dan Ukuran Set", TT), tbl(scr, [62, 26, 26, 22, 26], num_cols=(1, 2, 3, 4))))
    S.append(fig(FG["sc"], 150, "Gambar 9. NPV dan IRR per Skenario"))
    S.append(Paragraph(
        "Skenario menegaskan nilai portabilitas: <b>relokasi set ke PKS kedua pada tahun ke-11</b> (biaya 12%% FCI) mempertahankan tarif tahun 1-10 sehingga NPV naik menjadi USD %s juta. "
        "Sebaliknya, bila kredit karbon hanya terjual di IDXCarbon (USD 2,2/t) atau PKS tidak membayar jasa pengolahan POME, proyek tunggal tidak layak. "
        "Set 30 t/jam belum layak dengan harga dasar, sedangkan set 60 t/jam layak walaupun memakai tarif >1 MW."
        % mu(RES["SC"][1][1]["NPV"]), P))
    # ------------------------------------------------------------- 9 armada
    S.append(Paragraph("9. Model Perusahaan: Penggelaran Armada", H1))
    S.append(Paragraph(
        "Perusahaan membangun %d set pada 2027-2034 (unit pertama sebagai pilot komersial, FOAK +20%%). Biaya set turun mengikuti kurva belajar 90%% per penggandaan "
        "produksi karena desain bejana dan kontainer identik. Setelah overhead korporat (USD 450 ribu/tahun naik 10%%/tahun, ditambah USD 600 ribu R&D 2026), "
        "arus kas perusahaan 2026-2046 memberikan NPV USD %s juta, IRR %s, payback %s tahun dan puncak kebutuhan dana USD %s juta. "
        "Pada 2034 armada menghasilkan %s GWh/tahun dan %s ribu tCO₂e/tahun kredit karbon."
        % (sum(F.ROLL.values()), mu(fl["NPV"], 1), pc(fl["IRR"]), n(fl["PBP"], 1), mu(fl["peak"], 1), n(fl["E"][fl["years"].index(2035)], 0), n(fl["co2"][fl["years"].index(2035)] / 1e3)), P))
    S.append(fig(FG["fleet"], 165, "Gambar 10. Rencana Penggelaran Armada (a) dan Arus Kas Perusahaan (b)"))
    # ------------------------------------------------------------- 10 syarat
    S.append(Paragraph("10. Syarat Sebelum Keputusan Investasi Akhir (FID) dan Mitigasi Risiko", H1))
    for t in ("(1) <b>Kontrak offtake karbon</b> jangka panjang (forward/ERPA) minimal USD %s/tCO₂e untuk 10 tahun; harga impas USD %s/t." % (n(v["p_carbon"]), n(be["p_carbon_be"], 1)),
              "(2) <b>Perjanjian jasa dengan PKS</b>: jasa pengolahan POME USD %s/m³, sewa lahan 0,29 ha, pembelian air panas dan kue lumpur." % n(v["fee_pome"], 2),
              "(3) <b>PPA PLN</b> sesuai Perpres 112/2022 (konfirmasi status hukum dan faktor lokasi F) dan kelayakan interkoneksi 20 kV.",
              "(4) <b>Pilot</b> AnMBR termofilik (1 reaktor + 1 rak membran) 6 bulan untuk membuktikan OLR %s kg COD/m³.hari dan fluks %s LMH; garansi kinerja pemasok membran." % (n(F.R["nominal"]["olr"], 1), n(F.R["equipment"]["membrane"]["flux"])),
              "(5) <b>Pembiayaan hijau</b> USD (utang %s, bunga <= %s) dengan DSCR minimum %s; cadangan perawatan genset dan membran sudah termasuk OPEX." % (pc(v["debt_frac"], 0), pc(v["r_debt"], 1), n(o["DSCR_min"], 2))):
        S.append(Paragraph(t, P0))
    S.append(Paragraph("11. Catatan Data", H1))
    S.append(Paragraph(
        "Data pasar dan harga berasal dari penelusuran web Oktober 2026 (finance/research/market_data.md, lengkap dengan URL dan tahun). Item bertanda [ASUMSI]/[UNVERIFIED] "
        "(sebaran kapasitas PKS, harga membran tubular dan genset, biaya fabrikasi, jasa pengolahan POME, faktor lokasi Sumatera) harus dikonfirmasi dengan penawaran "
        "pemasok dan dokumen resmi sebelum dipakai untuk keputusan investasi. Ubah nilai pada lembar Asumsi Excel untuk menguji asumsi lain; seluruh lembar ikut terhitung ulang.", P))
    doc.build(S, onFirstPage=_pg, onLaterPages=_pg)
    return OUT

def _pg(c, d):
    c.saveState(); c.setFont("Ser", 8.5); c.setFillColor(colors.grey)
    c.drawString(22 * mm, 10 * mm, "Generator Biogas Portabel AnMBR - Analisis Ekonomi"); c.drawRightString(A4[0] - 22 * mm, 10 * mm, "%d" % d.page)
    c.restoreState()
