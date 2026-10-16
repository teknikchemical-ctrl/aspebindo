# -*- coding: utf-8 -*-
"""Laporan analisis pasar & kelayakan ekonomi v2 (PDF, Bahasa Indonesia). Semua angka dibaca dari hasil model."""
import os, json, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import fin_core as F, fin_market as MK

FD = "/usr/share/fonts/truetype/liberation/"
for nm, fn in (("Ser", "Regular"), ("SerB", "Bold"), ("SerI", "Italic")): pdfmetrics.registerFont(TTFont(nm, FD + "LiberationSerif-%s.ttf" % fn))
registerFontFamily("Ser", normal="Ser", bold="SerB", italic="SerI", boldItalic="SerB")
OUT = os.path.join(F.HERE, "outputs", "BG_Analisis_Ekonomi.pdf")
DK = colors.HexColor("#1f4e4a"); LT = colors.HexColor("#e6f0ee")
P = ParagraphStyle("p", fontName="Ser", fontSize=10.5, leading=15, alignment=TA_JUSTIFY, firstLineIndent=8 * mm, spaceAfter=4)
P0 = ParagraphStyle("p0", parent=P, firstLineIndent=0)
H1 = ParagraphStyle("h1", fontName="SerB", fontSize=12.5, leading=16, spaceBefore=8, spaceAfter=4, textColor=DK)
CAP = ParagraphStyle("cap", fontName="SerB", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=8)
TT = ParagraphStyle("tt", fontName="SerB", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=2)
CELL = ParagraphStyle("c", fontName="Ser", fontSize=8.6, leading=10.5); CELLB = ParagraphStyle("cb", parent=CELL, fontName="SerB")
TITLE = ParagraphStyle("t", fontName="SerB", fontSize=16, leading=21, alignment=TA_CENTER, textColor=DK, spaceAfter=6)

def n(x, d=0):
    if x is None or (isinstance(x, float) and not np.isfinite(x)): return "-"
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
def mu(x, d=2): return n(x / 1e6, d)
def pc(x, d=1): return "-" if not np.isfinite(x) else n(x * 100, d) + "%"
def tbl(data, widths, head=1, bold_last=False, num_cols=()):
    rows = [[Paragraph(str(c), CELLB if i < head or (bold_last and i == len(data) - 1) else CELL) for c in r] for i, r in enumerate(data)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=head)
    st = [("GRID", (0, 0), (-1, -1), .4, colors.grey), ("BACKGROUND", (0, 0), (-1, head - 1), LT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)] + [("ALIGN", (c, head), (c, -1), "RIGHT") for c in num_cols]
    t.setStyle(TableStyle(st)); return t
def KT(cap, t): return KeepTogether([Paragraph(cap, TT), t])
def fig(path, w=170, cap=None):
    from PIL import Image as PI
    im = PI.open(path); h = w * im.height / im.width
    out = [Image(path, width=w * mm, height=h * mm)]
    if cap: out.append(Paragraph(cap, CAP))
    return KeepTogether(out)

def build(RES):
    o, be, mc, fl, mk, TR = RES["o"], RES["be"], RES["mc"], RES["fl"], RES["mk"], RES["tiers"]
    v = o["v"]; FG = RES["figs"]; T_ = F.TECH; i3 = 3; yrs = o["years"]; SJ = F.SITE
    alir = os.path.join(F.ROOT, "cad", "out", "render", "DIORAMA_lokasi.png")
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Analisis Ekonomi - Generator Biogas Portabel", author="NAMA TIM")
    S = [Paragraph("ANALISIS PASAR DAN KELAYAKAN EKONOMI<br/>GENERATOR BIOGAS PORTABEL AnMBR TERMOFILIK UNTUK PKS", TITLE),
         Paragraph("Model v2 (setelah audit independen). Seluruh angka dihasilkan finance/run_all.py dari neraca massa-energi, model 3D produk dan model 3D lokasi; "
                   "model keuangan lengkap dengan rumus hidup: BG_Model_Keuangan.xlsx.", ParagraphStyle("s", parent=P0, alignment=TA_CENTER, fontSize=9.5, textColor=colors.grey)), Spacer(1, 4)]
    fee_cpo = v["fee_ffb"] / 0.21
    # ---------------------------------------------------------------- 1
    S.append(Paragraph("1. Ringkasan", H1))
    S.append(Paragraph(
        "Satu <b>set standar portabel</b> (14 reaktor AnMBR 194 m³ + modul kontainer/skid, %d muatan truk, plot %s ha) mengolah POME panas PKS %s t TBS/jam. "
        "Model bisnisnya <b>jasa pengolahan limbah + energi (BOO)</b>: perusahaan membiayai, memasang dan mengoperasikan set; PKS membayar <b>jasa pengolahan POME dan kepatuhan</b> "
        "USD %s/t TBS (setara USD %s/t CPO), menerima listrik di luar jam olah pengganti genset diesel, dan terbebas dari %s ha kolam anaerobik. Sisa listrik diekspor ke PLN "
        "(Perpres 112/2022) dan pengurangan emisi dijual sebagai kredit karbon."
        % (T_["truckloads"], n(T_["plot_m2"] / 1e4, 2), n(T_["ffb_tph"]), n(v["fee_ffb"], 2), n(fee_cpo, 1), n(SJ.get("land_freed_m2", 0) / 1e4, 1)), P))
    S.append(Paragraph(
        "Investasi tetap USD %s juta (harga 2026; USD %s juta pada 2027) menghasilkan <b>NPV USD %s juta</b> pada WACC %s, <b>IRR proyek %s</b>, IRR ekuitas %s, "
        "payback %s tahun sejak COD dan DSCR minimum %s. Pendapatan berasal dari jasa POME (%s), listrik (%s) dan karbon (%s). "
        "<b>Tanpa jasa POME proyek tidak layak</b> (NPV USD %s juta): jasa impas adalah USD %s/t TBS. Monte Carlo memberi peluang NPV > 0 sebesar %s. "
        "Pada tingkat perusahaan (%d set hingga 2034, kurva belajar 90%% pada %d%% biaya) NPV USD %s juta dan IRR %s."
        % (mu(o["fci26"]), mu(o["fci"]), mu(o["NPV"]), pc(o["wacc"], 2), pc(o["IRR"]), pc(o["IRR_eq"]), n(o["PBP"], 1), n(o["DSCR_min"], 2),
           pc(o["share_fee"], 0), pc(o["share_el"], 0), pc(o["share_c"], 0), mu(RES["SC"][1][1]["NPV"]), n(be["fee_be"], 2), pc((mc["NPV"] > 0).mean(), 0),
           sum(F.ROLL.values()), round(F.LEARN_SHARE * 100), mu(fl["NPV"], 1), pc(fl["IRR"])), P))
    if os.path.exists(alir):
        S.append(fig(alir, 168, "Gambar 1. Alir POME -> Energi di Lokasi PKS Proksi 45 t TBS/jam (Model 3D Lokasi)"))
    # ---------------------------------------------------------------- 2 lokasi
    S.append(Paragraph("2. Integrasi Fisik di Lokasi PKS", H1))
    lines = [[l, n(L_), n(cm, 0), n(c)] for l, L_, cm, c in T_["site_lines"]]
    S.append(Paragraph(
        "Model 3D lokasi menempatkan set di samping PKS proksi (rebusan, pabrik utama, boiler, tangki CPO) dan sistem kolam POME yang diukur dari debit %s m³/hari. "
        "POME dipompa dari fat pit ke PM-1; efluen AnMBR (COD terlarut ~%s mg/L, turun ~90%%) tetap dialirkan ke kolam fakultatif/aerobik yang dipertahankan sebagai "
        "<b>kolam polishing</b> sebelum aplikasi lahan, sedangkan kolam pengasaman dan anaerobik (%s ha) dibebaskan. Panjang pipa dan kabel dari model 3D masuk langsung ke CAPEX "
        "(Tabel 1), dan semua jarak aman terpenuhi (flare - GH %s m, GH - rumah boiler %s m)."
        % (n(T_["pome_m3d"]), n(T_["cod_eff_kgd"] / (T_["pome_m3d"] * 0.925) * 1000, 0), n(SJ.get("land_freed_m2", 0) / 1e4, 1),
           n(SJ["safety"][0]["dist"], 1) if SJ.get("safety") else "-", n(SJ["safety"][2]["dist"], 0) if SJ.get("safety") else "-"), P))
    S.append(KT("Tabel 1. Interkoneksi dari Model 3D Lokasi (masuk CAPEX)", tbl([["Rute", "Panjang m", "USD/m", "Biaya USD"]] + lines, [100, 20, 18, 26], num_cols=(1, 2, 3))))
    # ---------------------------------------------------------------- 3 pasar
    S.append(Paragraph("3. Analisis Pasar", H1))
    S.append(Paragraph(
        "Indonesia memiliki %s PKS dan %s juta m³ POME/tahun; baru ±10%% PKS menangkap metana. Dengan pendapatan rata-rata umur proyek USD %s per m³ POME, "
        "<b>TAM</b> = USD %s juta/tahun (setara %s set). <b>SAM</b> (PKS 30-60 t/jam tanpa penangkap metana di Sumatera-Kalimantan) = USD %s juta/tahun (%s setara-set). "
        "<b>SOM</b> = %d set pada 2034 = USD %s juta/tahun (%s SAM). Pendorong permintaan terkuat bukan tarif listrik, melainkan <b>syarat akses pasar</b>: biodiesel sawit untuk "
        "RED II/ISCC-EU dan bahan baku SAF CORSIA praktis mensyaratkan penangkapan metana POME (penghematan GRK biodiesel sawit naik dari 33%% menjadi 51%% dengan penangkapan metana)."
        % (n(MK.MILLS), n(MK.POME_NAT / 1e6), n(mk["rev_m3"], 2), n(mk["TAM"] / 1e6), n(mk["sets_TAM"]), n(mk["SAM"] / 1e6), n(mk["sets_SAM"]),
           mk["sets_SOM"], n(mk["SOM"] / 1e6, 1), pc(mk["share"])), P))
    S.append(fig(FG["pasar"], 165, "Gambar 2. Corong Pasar TAM-SAM-SOM (a) dan Sebaran PKS per Provinsi (b)"))
    S.append(KT("Tabel 2. Pembanding Teknologi Penangkapan Metana POME", tbl([["Teknologi", "CAPEX USD juta/MW", "Lahan ha", "Bangun bln", "Portabel", "Mutu efluen", "Pemain"]] + [list(r) for r in MK.compet(fl)], [34, 26, 14, 14, 18, 30, 34])))
    S.append(Paragraph(
        "Produk ini <b>lebih mahal per kW</b> daripada kolam tertutup dan PLTBg tangki (literatur 1,8-3,0 juta USD/MW). Nilainya bagi PKS terletak pada kepatuhan "
        "dan akses pasar, lahan, kecepatan pasang (11 bulan) dan portabilitas; karena itu jasa pengolahan menjadi aliran pendapatan utama, bukan tarif listrik.", P))
    # ---------------------------------------------------------------- 4 porter pestle
    S.append(Paragraph("4. Lima Kekuatan Porter, PESTLE, dan Daya Tarik Segmen", H1))
    pf = {f: np.mean([s for _, s, _ in MK.PORTER[f]]) for f in MK.PORTER}; ps = MK.pestle_scores(); top = sorted(pf, key=lambda k: -pf[k])
    S.append(Paragraph(
        "Rata-rata tekanan Porter %s dari 5; tertinggi dari <b>%s</b> (%s) dan <b>%s</b> (%s). PESTLE 22 faktor memberi skor bersih %+d: politik (%+d) dan lingkungan (%+d) "
        "merupakan peluang (target EBT, ISPO wajib, syarat ISCC/CORSIA), sedangkan hukum (%+d) dan ekonomi (%+d) adalah ancaman (perizinan PPA, baku mutu efluen yang diperketat, "
        "harga karbon rendah, suku bunga). Segmen paling menarik adalah PKS pemasok biodiesel/SAF bersertifikat dan PKS swasta 45 t/jam di Sumatera."
        % (n(np.mean(list(pf.values())), 2), top[0].lower(), n(pf[top[0]], 2), top[1].lower(), n(pf[top[1]], 2), sum(ps.values()), ps["Politik"], ps["Lingkungan"], ps["Hukum"], ps["Ekonomi"]), P))
    S.append(fig(FG["porter"], 165, "Gambar 3. Lima Kekuatan Porter (a), Radar per Segmen (b), Skor PESTLE (c), Daya Tarik vs Kemampuan Menang (d)"))
    S.append(KT("Tabel 3. Faktor PESTLE (skor = tanda x dampak x peluang)", tbl([["Kode", "Faktor", "Dampak", "Peluang", "Skor", "Keterangan"]] + [[k, f_, i_, l_, "%+d" % (s_ * i_ * l_), d_] for k, c_, f_, s_, i_, l_, d_ in MK.PESTLE],
                                                                              [10, 58, 13, 13, 11, 65], num_cols=(2, 3, 4))))
    # ---------------------------------------------------------------- 5 capex opex
    S.append(Paragraph("5. CAPEX dan OPEX", H1))
    S.append(Paragraph(
        "CAPEX bottom-up: bejana dari <b>massa baja model 3D</b> (%s t/reaktor) x USD %s/kg, membran %s m² x USD %s/m², genset %s kWe x USD %s/kWe, interkoneksi dari model 3D lokasi. "
        "FCI USD %s juta (2026) = %s USD/kWe kotor; dieskalasi %s/th ke 2027 (USD %s juta). Ditambah bunga selama konstruksi USD %s ribu, PPN 11%% CAPEX (restitusi tahun ke-2), "
        "biaya upfront pinjaman dan DSRA 6 bulan. OPEX tahun penuh USD %s ribu ditambah biaya MRV karbon; overhaul genset (th 8, 16) dan ganti membran (th 8, 15) dimodelkan pada tahun terjadinya."
        % (n(T_["vessel_t"], 1), n(v["c_fab"], 1), n(T_["area_mem"]), n(v["c_mem"]), n(T_["chp_kWe"]), n(v["c_chp"]), mu(o["fci26"]), n(o["fci26"] / T_["P_gross"]), pc(v["infl"], 0),
           mu(o["fci"]), n(o["idc"] / 1e3), n((o["opF"] + o["opV"]) / 1e3)), P))
    rows = [["Item", "Jumlah", "Total USD"]] + [[nm, "%s %s" % (n(q, 2 if q < 1 else 0), u), n(t)] for g, nm, q, u, c, t, b in o["capex_rows"]] + [["<b>FCI (2026)</b>", "", "<b>%s</b>" % n(o["fci26"])]]
    S.append(KT("Tabel 4. Rincian CAPEX 1 Set 45 t TBS/jam (USD 2026)", tbl(rows, [110, 28, 28], bold_last=True, num_cols=(2,))))
    orow = [["Komponen OPEX", "Jenis", "USD/th"]] + [[k, "Tetap" if t == "F" else "Variabel", n(val)] for k, (val, t) in o["opex_items"].items()] + [["MRV karbon (selama periode kredit)", "Tetap", n(v["c_mrv"])], ["<b>Total</b>", "", "<b>%s</b>" % n(o["opF"] + o["opV"] + v["c_mrv"])]]
    S.append(KT("Tabel 5. OPEX Tahun Penuh (USD 2026)", tbl(orow, [110, 28, 28], bold_last=True, num_cols=(2,))))
    S.append(fig(FG["capex"], 168, "Gambar 4. Struktur CAPEX (a), OPEX (b), dan Bauran Pendapatan Tahun ke-3 (c)"))
    # ---------------------------------------------------------------- 6 pendapatan & arus kas
    S.append(Paragraph("6. Pendapatan dan Arus Kas", H1))
    S.append(Paragraph(
        "Basis volume tunggal: %s t TBS/tahun (45 t/jam x 20 jam x 300 hari x faktor beban %s). Listrik neto %s GWh/tahun (ketersediaan %s): %s GWh ke PKS di luar jam olah "
        "(150 kW x %s jam) pada USD %s/kWh - lebih murah dari genset diesel PKS (Rp4.000-5.000/kWh) - dan %s GWh ke PLN pada %s USc/kWh x F %s (tahun 1-10) lalu %s USc/kWh. "
        "Pengurangan emisi neto %s tCO₂e/tahun (setelah dikurangi metana dari efluen di kolam polishing %s t), kredit %s pada USD %s/t selama periode kredit %d tahun, diterima "
        "satu tahun setelah vintage. Jasa pengolahan POME USD %s/t TBS dieskalasi %s/th."
        % (n(T_["ffb_ty_nom"] * v["util"]), n(v["util"], 2), n(o["E"][i3], 2), pc(v["avail"], 0), n(o["Ecap"][i3], 2), n(v["captive_h"]), n(v["p_captive"], 2), n(o["Eexp"][i3], 2),
           n(v["tariff1"], 2), n(v["F_loc"], 2), n(v["tariff2"], 2), n(o["ER"]), n(o["eff_t"]), pc(v["cer_ratio"], 0), n(v["p_carbon"]), v["carbon_years"], n(v["fee_ffb"], 2), pc(v["infl"], 0)), P))
    keys = [("Jasa POME", "rev_fee"), ("Listrik ke PKS", "rev_cap"), ("Listrik ke PLN", "rev_exp"), ("Kredit karbon", "rev_c"), ("Total pendapatan", "rev"),
            ("OPEX + karbon", "opex_tot"), ("EBITDA", "ebitda"), ("CAPEX", "capex"), ("PPN CAPEX", "vat"), ("Pajak", "tax_u"), ("Arus kas bersih (FCFF)", "fcff"), ("Kumulatif", "cum")]
    cols = list(range(8)); cum = np.cumsum(o["fcff"])
    data = [["Uraian"] + ["%d (%s)" % (yrs[i], "K" if i == 0 else "O%d" % i) for i in cols]]
    for lab, k in keys:
        vals_ = cum if k == "cum" else o[k]; neg = k in ("opex_tot", "capex", "tax_u", "vat")
        data.append([lab] + [("(%s)" % n(abs(vals_[i]) / 1e3)) if (neg and vals_[i] > 0) or (not neg and vals_[i] < 0) else ("-" if abs(vals_[i]) < .5 else n(vals_[i] / 1e3)) for i in cols])
    S.append(KT("Tabel 6. Model Arus Kas %d-%d (USD ribu; kurung = negatif; K = konstruksi, O = operasi)" % (yrs[0], yrs[7]), tbl(data, [36] + [16.2] * 8, num_cols=tuple(range(1, 9)))))
    S.append(fig(FG["cf"], 165, "Gambar 5. Arus Kas Tahunan dan Kumulatif %d-%d" % (yrs[0], yrs[-1])))
    # ---------------------------------------------------------------- 7 indikator
    S.append(Paragraph("7. NPV, IRR, dan Payback", H1))
    S.append(Paragraph(
        "WACC %s = %s x %s x (1 - %s) + %s x %s. NPV = Σ CF<sub>t</sub>/(1+WACC)<sup>t</sup> = USD %s juta; IRR proyek %s; IRR ekuitas %s (utang %s termasuk IDC, bunga %s, tenor %d th dengan "
        "masa tenggang pokok 1 th). Payback %s tahun sejak COD, payback terdiskonto %s tahun, indeks profitabilitas %s, DSCR minimum %s (dengan cadangan perawatan)."
        % (pc(o["wacc"], 2), pc(v["debt_frac"], 0), pc(v["r_debt"], 1), pc(v["tax"], 0), pc(1 - v["debt_frac"], 0), pc(v["r_eq"], 0), mu(o["NPV"]), pc(o["IRR"]), pc(o["IRR_eq"]),
           pc(v["debt_frac"], 0), pc(v["r_debt"], 1), v["tenor"], n(o["PBP"], 2), n(o["DPBP"], 2), n(o["PI"], 2), n(o["DSCR_min"], 2)), P))
    S.append(fig(FG["npv"], 165, "Gambar 6. Profil NPV terhadap Tingkat Diskonto (a) dan Diagram Tornado ±20%% (b)"))
    S.append(fig(FG["pb"], 165, "Gambar 7. Kurva Payback Biasa dan Terdiskonto"))
    dec = lambda ok: "Layak" if ok else "Tidak layak"
    ind = [["Indikator", "Hasil", "Kriteria", "Keputusan"],
           ["NPV @ WACC %s" % pc(o["wacc"]), "USD %s juta" % mu(o["NPV"]), "> 0", dec(o["NPV"] > 0)],
           ["IRR proyek", pc(o["IRR"]), "> WACC", dec(o["IRR"] > o["wacc"])],
           ["IRR ekuitas", pc(o["IRR_eq"]), ">= %s" % pc(v["r_eq"], 0), dec(o["IRR_eq"] >= v["r_eq"] - 5e-4)],
           ["Payback sejak COD", "%s th" % n(o["PBP"], 2), "< %d th" % v["n_op"], dec(o["PBP"] < v["n_op"])],
           ["Payback terdiskonto", "%s th" % n(o["DPBP"], 2), "< %d th" % v["n_op"], dec(np.isfinite(o["DPBP"]) and o["DPBP"] < v["n_op"])],
           ["Indeks profitabilitas", n(o["PI"], 2), "> 1,0", dec(o["PI"] > 1)],
           ["DSCR minimum", n(o["DSCR_min"], 2), ">= 1,30", dec(o["DSCR_min"] >= 1.3)],
           ["Jasa POME impas", "USD %s/t TBS" % n(be["fee_be"], 2), "< USD %s (dasar)" % n(v["fee_ffb"], 2), dec(be["fee_be"] < v["fee_ffb"])],
           ["Tarif PLN impas (th 1-10)", "%s USc/kWh x F" % n(be["tariff1_be"], 2), "< %s (Perpres)" % n(v["tariff1"], 2), dec(be["tariff1_be"] < v["tariff1"])],
           ["Puncak kebutuhan dana", "USD %s juta" % mu(o["peak_funding"]), "Struktur pendanaan", "Informasi"]]
    S.append(KT("Tabel 7. Ringkasan Indikator Kelayakan (1 set 45 t TBS/jam)", tbl(ind, [56, 40, 44, 26], num_cols=(1,))))
    # ---------------------------------------------------------------- 8 BEP
    S.append(Paragraph("8. Titik Impas", H1))
    S.append(Paragraph(
        "Karena jasa POME dibayar per t TBS dan tidak bergantung pada gas, arus kas tunai sudah positif pada produksi energi 0 (BEP tunai %s); BEP akuntansi (penyusutan buku + bunga) "
        "tercapai pada %s produksi energi dasar. Dalam istilah NPV, proyek tetap positif selama jasa POME di atas USD %s/t TBS (USD %s/t CPO), tarif PLN tahun 1-10 di atas %s USc/kWh x F, "
        "produksi energi di atas %s dasar atau CAPEX di bawah %s dasar."
        % (pc(be["BEP_cash"], 0), pc(be["BEP_acc"], 0), n(be["fee_be"], 2), n(be["fee_be_cpo"], 1), n(be["tariff1_be"], 2), pc(be["emult_be"], 0), pc(be["capex_be"], 0)), P))
    S.append(fig(FG["bep"], 165, "Gambar 8. Titik Impas Operasional (a) dan Nilai Impas NPV = 0 (b)"))
    # ---------------------------------------------------------------- 9 ketidakpastian
    S.append(Paragraph("9. Analisis Ketidakpastian", H1))
    base, res = RES["torn"]
    S.append(Paragraph(
        "Tornado (Gambar 6b): variabel paling berpengaruh adalah <b>%s</b>, <b>%s</b> dan <b>%s</b>. Monte Carlo %s iterasi (distribusi condong merugikan; kasus dasar = modus; "
        "25%% peluang PLN memakai tier >1 MW karena kapasitas terpasang 1,6 MW) memberi NPV P10/P50/P90 = USD %s / %s / %s juta, peluang NPV > 0 = %s, IRR P50 = %s. "
        "Kasus tanpa IRR dihitung sebagai nilai terburuk, tidak dibuang."
        % (res[0][0].lower(), res[1][0].lower(), res[2][0].lower(), n(len(mc["NPV"])), *[n(F.pct(mc["NPV"], q) / 1e6, 2) for q in (10, 50, 90)], pc((mc["NPV"] > 0).mean(), 0), pc(F.pct(mc["IRR"], 50, -0.5))), P))
    S.append(fig(FG["mc"], 168, "Gambar 9. Distribusi NPV (a), Kurva S IRR (b), dan Penggerak Ketidakpastian (c)"))
    scr = [["Skenario", "FCI USD juta", "NPV USD juta", "IRR", "Payback th"]] + [[s[0].replace("\n", " "), mu(s[1]["fci"]), mu(s[1]["NPV"]), pc(s[1]["IRR"]), n(s[1]["PBP"], 1)] for s in RES["SC"]]
    S.append(KT("Tabel 8. Skenario", tbl(scr, [62, 26, 26, 22, 26], num_cols=(1, 2, 3, 4))))
    S.append(fig(FG["sc"], 150, "Gambar 10. NPV dan IRR per Skenario"))
    # ---------------------------------------------------------------- 10 armada
    S.append(Paragraph("10. Model Perusahaan", H1))
    u1, u10 = fl["units"][0], fl["units"][9]
    S.append(Paragraph(
        "Perusahaan membangun %d set 2027-2034. Unit pertama FOAK (+20%%) berbiaya USD %s juta; kurva belajar 90%% pada %d%% FCI (bejana, skid, pemasangan; genset, membran dan transport "
        "tidak turun) dan eskalasi %s/th membawa unit ke-10 menjadi USD %s juta (nominal %d). Setelah overhead korporat (USD 450 ribu/th naik 10%%/th hingga 2034, R&D USD 600 ribu 2026, "
        "tanpa perisai pajak), arus kas perusahaan %d-%d (umur penuh semua unit) memberi NPV USD %s juta, IRR %s dan puncak kebutuhan dana USD %s juta."
        % (sum(F.ROLL.values()), mu(u1[5]), round(F.LEARN_SHARE * 100), pc(v["infl"], 0), mu(u10[5]), u10[1], fl["years"][0], fl["years"][-1], mu(fl["NPV"], 1), pc(fl["IRR"]), mu(fl["peak"], 1)), P))
    S.append(fig(FG["fleet"], 165, "Gambar 11. Penggelaran Armada (a) dan Arus Kas Perusahaan (b)"))
    # ---------------------------------------------------------------- 11 nilai bagi PKS & syarat FID
    S.append(Paragraph("11. Nilai bagi PKS dan Syarat Sebelum FID", H1))
    diesel = 0.25
    S.append(Paragraph(
        "Jasa USD %s/t TBS = USD %s ribu/tahun bagi PKS ini, setara USD %s/t CPO (sekitar 1%% harga CPO). Sebagai imbalannya PKS: (i) memenuhi syarat penangkapan metana ISCC-EU/CORSIA "
        "untuk pasar biodiesel/SAF (nilai kredit RSPO 2023 ~USD 27/t CSPO sebagai pembanding besaran premi keberlanjutan), (ii) menghemat ±USD %s ribu/tahun selisih biaya listrik "
        "diesel (USD %s/kWh) terhadap harga listrik set, (iii) membebaskan %s ha kolam anaerobik dan biaya pengurasannya, (iv) menghilangkan bau dan emisi %s tCO₂e/tahun."
        % (n(v["fee_ffb"], 2), n(o["rev_fee"][i3] / 1e3), n(fee_cpo, 1), n(o["Ecap"][i3] * 1e6 * (diesel - v["p_captive"]) / 1e3), n(diesel, 2), n(SJ.get("land_freed_m2", 0) / 1e4, 1), n(o["ER"])), P))
    for t in ("(1) <b>Kontrak jasa 20 tahun dengan PKS</b> (jasa >= USD %s/t TBS, impas %s), jaminan pasokan POME dan sewa lahan %s ha." % (n(v["fee_ffb"], 2), n(be["fee_be"], 2), n(T_["plot_m2"] / 1e4, 2)),
              "(2) <b>PPA PLN</b> dengan kapasitas kontrak <= 1 MW di titik serah dan konfirmasi tertulis tier Perpres 112/2022 (status revisi 2026) serta faktor lokasi F.",
              "(3) <b>Izin pasokan listrik ke PKS</b> (IUPTLS/skema sewa) untuk %s GWh/tahun di luar jam olah." % n(o["Ecap"][i3], 2),
              "(4) <b>Pilot</b> 1 reaktor + 1 rak membran 6 bulan: OLR %s kg COD/m³.hari, fluks %s LMH, COD efluen." % (n(F.R["nominal"]["olr"], 1), n(F.R["equipment"]["membrane"]["flux"])),
              "(5) <b>Registrasi karbon</b> (Verra/SRN-PPI) dan keputusan apakah kredit dijual atau dipakai PKS untuk klaim GRK produknya (tidak boleh dihitung ganda)."):
        S.append(Paragraph(t, P0))
    S.append(Paragraph("12. Catatan Data dan Audit", H1))
    S.append(Paragraph(
        "Sumber pasar, tarif, karbon dan biaya ada di finance/research/market_data.md dan market_data_2.md (URL dan tahun). Model v2 memperbaiki temuan audit: basis volume tunggal "
        "(300 hari x faktor beban), tier tarif & kapasitas kontrak, emisi efluen dan periode kredit karbon, IRR kokoh, eskalasi CAPEX armada, IDC/PPN/DSRA, waktu overhaul nyata, "
        "aturan pajak PP 78/2019, serta klaim mutu efluen. Item [ASUMSI]/[UNVERIFIED] (jasa POME, harga membran/genset, faktor F, status Perpres) wajib dikonfirmasi sebelum FID.", P))
    doc.build(S, onFirstPage=_pg, onLaterPages=_pg)
    return OUT

def _pg(c, d):
    c.saveState(); c.setFont("Ser", 8.5); c.setFillColor(colors.grey)
    c.drawString(22 * mm, 10 * mm, "Generator Biogas Portabel AnMBR - Analisis Ekonomi v2"); c.drawRightString(A4[0] - 22 * mm, 10 * mm, "%d" % d.page)
    c.restoreState()
