# -*- coding: utf-8 -*-
"""Laporan analisis pasar, Model Keputusan PKS & kelayakan ekonomi v3 (PDF, Bahasa Indonesia). Semua angka dibaca dari hasil model."""
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
    cm, fw, seg, comp, usp_, rl = RES["mill"], RES["fw"], RES["seg"], RES["comp"], RES["usp"], RES["reloc"]
    v = o["v"]; FG = RES["figs"]; T_ = F.TECH; i3 = 3; yrs = o["years"]; SJ = F.SITE; ad = cm["detail"]
    PR = F.R; ef = PR["effluent"]; yr = PR["year"]; mo = PR["membrane_option"]
    alir = os.path.join(F.ROOT, "cad", "out", "render", "DIORAMA_lokasi.png")
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Analisis Ekonomi - Set Biogas Kontak Termofilik", author="NAMA TIM")
    S = [Paragraph("ANALISIS PASAR, KEPUTUSAN PKS DAN KELAYAKAN EKONOMI<br/>SET BIOGAS KONTAK TERMOFILIK YANG DAPAT DIPINDAH UNTUK PKS", TITLE),
         Paragraph("Model v3 setelah iterasi riset (research/R1-R4: regulasi & karbon, energi & ekonomi PKS, pasar & pesaing, bukti teknis). Semua angka dihasilkan finance/run_all.py; "
                   "model lengkap dengan rumus hidup: BG_Model_Keuangan.xlsx.", ParagraphStyle("s", parent=P0, alignment=TA_CENTER, fontSize=9.5, textColor=colors.grey)), Spacer(1, 4)]
    # ---------------------------------------------------------------- 1
    S.append(Paragraph("1. Ringkasan", H1))
    S.append(Paragraph(
        "<b>Pertanyaan PKS: apakah lebih murah menyerahkan POME kepada kami daripada mempertahankan kolam?</b> Untuk PKS 45 t TBS/jam yang bergantung pada solar "
        "(emplasmen, bengkel, kernel plant), jawabannya <b>ya</b>: biaya pengelolaan POME + listrik turun dari USD %s menjadi USD %s per t TBS (<b>hemat %s</b>, USD %s ribu/tahun) "
        "tanpa CAPEX PKS. Penghematan berasal dari listrik biogas yang menggantikan solar (USD %s/kWh vs diesel USD %s/kWh), kolam anaerobik yang tidak perlu dikuras, "
        "risiko penyegelan yang turun, lahan dan pupuk. Ekspor listrik ke PLN dan kredit karbon milik pengembang membuat jasa pengolahan cukup USD %s/t TBS "
        "(jendela kesepakatan USD %s-%s)."
        % (n(cm["A"]["per_t"], 2), n(cm["D"]["per_t"], 2), pc(cm["saving_D_vs_A_pct"], 0), n((cm["A"]["annual"] - cm["D"]["annual"]) / 1e3), n(v["p_captive"], 2), n(ad["c_dsl"], 2),
           n(v["fee_ffb"], 2), n(fw["fee_min"], 2), n(fw["fee_max"], 2)), P))
    S.append(Paragraph(
        "Bagi pengembang, satu set (FCI USD %s juta, harga 2026) memberi <b>NPV USD %s juta</b> pada WACC %s, IRR proyek %s, IRR ekuitas %s, payback %s tahun dan DSCR minimum %s; "
        "peluang NPV > 0 (Monte Carlo) %s. Model juga menunjukkan batasnya secara jujur: untuk PKS yang terhubung PLN dan memakai solar sedikit (0,53 L/t TBS) "
        "<b>tidak ada jendela kesepakatan</b>, dan PKS yang mempunyai modal USD 2,6-3,0 juta serta tim operasi akan lebih untung membangun digester sendiri. "
        "Karena itu pasar sasaran adalah PKS bergantung diesel tanpa modal atau selera risiko teknis (SAM %s PKS; SOM %d set hingga 2034)."
        % (mu(o["fci26"]), mu(o["NPV"]), pc(o["wacc"], 2), pc(o["IRR"]), pc(o["IRR_eq"]), n(o["PBP"], 1), n(o["DSCR_min"], 2), pc((mc["NPV"] > 0).mean(), 0), n(mk["sets_SAM"]), mk["sets_SOM"]), P))
    S.append(fig(FG["mill"], 168, "Gambar 1. Model Keputusan PKS: Biaya POME Terlevelisasi Opsi A-D (a) dan Langkah dari Kolam ke Layanan BOO (b)"))
    # ---------------------------------------------------------------- 2 iterasi teknis
    S.append(Paragraph("2. Iterasi Riset -> Teknis -> Neraca Massa -> Keuangan", H1))
    S.append(Paragraph(
        "Desain Rev 1 (AnMBR termofilik dalam 14 bejana 4,2 m) diuji terhadap literatur. Membran hanya menambah %s Nm³ CH₄/hari (+%s kWe kotor) tetapi butuh %s m² pada fluks realistis 8 LMH dan "
        "%s kW energi cross-flow; tidak ada AnMBR POME skala penuh di dunia. Bejana 4,2 m di atas low-bed setinggi ~5,1 m melebihi batas jalan 4,2 m. "
        "Rev 2 memakai <b>proses kontak termofilik</b> (CSTR + degasser vakum + settler lamella + resirkulasi lumpur, SRT %s hari) dalam <b>%d tangki GFS dibaut</b> %s m³ "
        "yang dikirim sebagai panel dalam kontainer dan dapat dibongkar-pasang. Utilisasi PKS realistis %s (kapasitas PKS Indonesia ~2x produksi) menurunkan energi neto menjadi "
        "<b>%s GWh/tahun</b> (simulasi 365 hari). Efluen (COD %s mg/L, BOD %s mg/L) tetap ke kolam polishing lalu aplikasi lahan; tidak diklaim memenuhi baku mutu sungai."
        % (n(mo["ch4_gain_Nm3d"]), n(mo["kWe_gain_gross"]), n(mo["area_m2"]), n(mo["kW"]), n(PR["process_decisions"]["srt_d"]), T_["n_vessel"], n(T_["V_tank"]),
           n(yr["util"], 2), n(yr["GWh_net"], 2), n(ef["COD"]), n(ef["BOD5"])), P))
    # ---------------------------------------------------------------- 3 keputusan PKS
    S.append(Paragraph("3. Model Keputusan PKS: Listrik, Karbon dan Biaya POME", H1))
    S.append(Paragraph(
        "Empat opsi dibandingkan dari sudut pandang PKS selama 20 tahun (biaya modal PKS %s, eskalasi %s): <b>A</b> kolam terbuka + genset diesel (status quo), <b>B</b> kolam tertutup "
        "milik PKS, <b>C</b> digester tangki milik PKS, <b>D</b> layanan BOO ini. Listrik adalah penghubung utama: PKS memakai %s L solar/t TBS (%s GWh/tahun listrik diesel pada USD %s/kWh); "
        "set memasok %s GWh/tahun dengan harga USD %s/kWh. Karbon adalah penghubung kedua: %s tCO₂e/tahun (AMS-III.H) dijual pengembang dan menyubsidi fee; opsi bagi hasil karbon ke PKS "
        "tersedia di model (sel m_c_share)."
        % (pc(MI_r(), 0), pc(v["infl"], 0), n(v["diesel_L_tffb"], 2), n(ad["E_dsl"] / 1e6, 2), n(ad["c_dsl"], 2), n(ad["cap"] / 1e6, 2), n(v["p_captive"], 2), n(o["ER"])), P))
    rows = [["Biaya tahunan PKS (USD 2026)", "A Kolam", "B Kolam tertutup", "C Tangki PKS", "D Layanan BOO"]]
    lab_map = [("Listrik diesel", ("Listrik diesel PKS (solar + O&M genset)", "Listrik diesel sisa", "Listrik diesel sisa", "Listrik diesel sisa (set tidak tersedia)")),
               ("Jasa POME (fee)", (None, None, None, "Jasa pengolahan POME (fee)")), ("Beli listrik set", (None, None, None, "Listrik dari set")),
               ("O&M pembangkit milik PKS", (None, "O&M pembangkit biogas milik PKS", "O&M pembangkit biogas milik PKS", None)),
               ("Pengurasan & kolam", (("Pengurasan lumpur kolam", "Perawatan kolam & pompa"), "Pengurasan lumpur", "Pengurasan lumpur", None)),
               ("Aplikasi lahan + pemantauan", (("Aplikasi lahan", "Pemantauan lingkungan"), ("Aplikasi lahan", "Pemantauan lingkungan"), ("Aplikasi lahan", "Pemantauan lingkungan"), ("Aplikasi lahan (efluen)", "Pemantauan lingkungan"))),
               ("Ekspor PLN + karbon milik PKS", (None, ("Ekspor listrik ke PLN (th 1-10)", "Kredit karbon (PKS daftar sendiri)"), ("Ekspor listrik ke PLN (th 1-10)", "Kredit karbon (PKS daftar sendiri)"), "Bagi hasil karbon")),
               ("Risiko, lahan, pupuk", (("Risiko penyegelan (nilai harapan)",), ("Risiko penyegelan (nilai harapan)", "Lahan kolam dibebaskan"), ("Risiko penyegelan (nilai harapan)", "Lahan kolam dibebaskan"),
                                         ("Risiko penyegelan (nilai harapan)", "Lahan kolam dibebaskan (margin sawit)", "Kue lumpur sebagai pupuk")))]
    for lab, keys in lab_map:
        r_ = [lab]
        for o_, k in zip("ABCD", keys):
            ks = () if k is None else (k if isinstance(k, tuple) else (k,))
            r_.append(n(sum(ad[o_].get(x, 0.0) for x in ks)))
        rows.append(r_)
    rows.append(["<b>Total tahunan</b>"] + ["<b>%s</b>" % n(cm[o_]["annual"]) for o_ in "ABCD"])
    rows.append(["CAPEX dibayar PKS"] + [n(cm[o_]["capex"]) for o_ in "ABCD"])
    rows.append(["<b>Biaya terlevelisasi USD/t TBS</b>"] + ["<b>%s</b>" % n(cm[o_]["per_t"], 2) for o_ in "ABCD"])
    S.append(KT("Tabel 1. Model Keputusan PKS 45 t TBS/jam, Segmen Bergantung Diesel (negatif = manfaat)", tbl(rows, [52, 28, 30, 28, 28], num_cols=(1, 2, 3, 4))))
    S.append(Paragraph(
        "Opsi D <b>%s lebih murah</b> daripada status quo. Opsi B dan C bahkan lebih murah lagi di atas kertas, tetapi menuntut CAPEX PKS USD %s-%s juta, operasi oleh PKS sendiri, "
        "dan menanggung risiko kinerja (faktor kapasitas PLTBg POME nyata 57-85%%; kasus Bangka IRR 6,75%% karena POME kurang [R2]). Inilah alasan <10-15%% PKS Indonesia sudah "
        "menangkap metana meskipun manfaatnya jelas: penghalangnya modal dan risiko, bukan ekonomi. Layanan D menghapus keduanya; untuk PKS yang ingin memiliki aset, kontrak dapat "
        "menyertakan opsi beli pada tahun ke-8."
        % (pc(cm["saving_D_vs_A_pct"], 0), mu(cm["B"]["capex"], 1), mu(cm["C"]["capex"], 1)), P))
    # ---------------------------------------------------------------- 4 segmen
    S.append(Paragraph("4. Segmen dan Jendela Kesepakatan", H1))
    srows = [["Segmen", "Util", "Solar L/t", "Fee min", "Fee maks", "IRR pengembang", "PKS hemat"]] + [[sg["name"], n(sg["util"], 2), n(sg["diesel"], 2), n(sg["fee_min"], 2), n(sg["fee_max"], 2), pc(sg["IRR_dev"]), pc(sg["saving_pct"], 0)] for sg in seg]
    S.append(KT("Tabel 2. Jendela Kesepakatan per Segmen (fee USD/t TBS; IRR dan penghematan pada fee dasar USD %s)" % n(v["fee_ffb"], 2), tbl(srows, [62, 14, 16, 16, 16, 22, 20], num_cols=(1, 2, 3, 4, 5, 6))))
    S.append(fig(FG["seg"], 160, "Gambar 2. Jendela Kesepakatan: Fee Minimum Pengembang vs Fee Maksimum PKS"))
    S.append(Paragraph(
        "Pada PKS terhubung PLN, listrik biogas hanya bernilai tarif PLN (%s USc/kWh x F) sehingga pengembang membutuhkan fee > USD %s/t TBS, padahal PKS hanya menghemat < USD %s. "
        "Pada PKS bergantung diesel, setiap kWh bernilai ~USD %s bagi PKS, cukup untuk membayar fee, memberi PKS penghematan dan memberi pengembang IRR di atas WACC."
        % (n(v["tariff1"], 2), n(seg[0]["fee_min"], 2), n(seg[0]["fee_max"], 2), n(ad["c_dsl"], 2)), P))
    # ---------------------------------------------------------------- 5 pasar
    S.append(Paragraph("5. Analisis Pasar Bottom-up", H1))
    mr = mk["rows"]
    S.append(Paragraph(
        "Indonesia mempunyai ±%s PKS; %s sudah menangkap metana (84 PLTBg POME ±165 MW). <b>TAM</b> = %s setara-set (USD %s juta/tahun, %s MWe). <b>SAM-luas</b> (30-60 t/jam, "
        "Sumatera/Kalimantan) = %s PKS. <b>SAM</b> = PKS yang bergantung diesel, tempat jendela kesepakatan terbuka = %s PKS (USD %s juta/tahun). <b>SOM</b> = %d set pada 2034 "
        "(%s SAM; %s laju pembangunan PLTBg nasional historis 9 MW/tahun). Ekspansi ke Malaysia (±315 PKS tanpa penangkap metana) tidak dihitung."
        % (n(MK.MILLS_ID), pc(MK.SH_CAPTURED, 1), n(mr[0]["sets"]), n(mr[0]["rev"] / 1e6), n(mr[0]["MW"]), n(mr[1]["mills"]), n(mr[2]["mills"]), n(mr[2]["rev"] / 1e6), mk["sets_SOM"],
           pc(mk["share"], 0), pc(mk["build_share"], 0)), P))
    S.append(fig(FG["pasar"], 165, "Gambar 3. Corong Pasar Bottom-up (a) dan Sebaran PKS per Provinsi (b)"))
    # ---------------------------------------------------------------- 6 pesaing & USP
    S.append(Paragraph("6. Pesaing dan Keunggulan Unik (USP)", H1))
    S.append(fig(FG["comp"], 168, "Gambar 4. Matriks Pesaing Berbobot (skor 1-5; biaya dari Model Keputusan PKS)"))
    S.append(Paragraph(
        "Produk ini mendapat skor tertimbang %s, setara dengan biometana BOOT (%s) yang hanya melayani klaster PKS besar dengan offtake gas, dan di atas digester milik PKS (%s-%s). "
        "Kelemahan kami nyata: belum ada referensi (skor kematangan 2) dan CAPEX/MWe di atas kolam tertutup. Tabel 3 merangkum USP yang diukur model, bukan sekadar diklaim."
        % (n([c["total"] for c in comp if c["name"].startswith("D ")][0], 2), n([c["total"] for c in comp if c["name"].startswith("Biometana")][0], 2),
           n(min(c["total"] for c in comp if c["name"][:2] in ("B ", "C ")), 2), n(max(c["total"] for c in comp if c["name"][:2] in ("B ", "C ")), 2)), P))
    S.append(KT("Tabel 3. USP Terukur dan Penilaian Jujur", tbl([["USP", "Metrik model", "Penilaian"]] + [[u_[0], u_[1], u_[3]] for u_ in usp_], [34, 82, 52])))
    S.append(Paragraph(
        "Nilai dapat dipindah: bila PKS tutup pada tahun ke-%d, set dipindah ke PKS lain (biaya 15%% FCI, 6 bulan henti) sehingga NPV pengembang tetap USD %s juta, "
        "sedangkan digester tetap akan terdampar (NPV USD %s juta). Ini menurunkan risiko pemberi pinjaman - dasar pembiayaan murah untuk armada."
        % (rl["close_year"], mu(rl["reloc"]), mu(rl["stranded"])), P))
    # ---------------------------------------------------------------- 7 porter pestle
    S.append(Paragraph("7. Lima Kekuatan Porter dan PESTLE", H1))
    pf = {f: np.mean([s for _, s, _ in MK.PORTER[f]]) for f in MK.PORTER}; ps = MK.pestle_scores(); top = sorted(pf, key=lambda k: -pf[k])
    S.append(Paragraph(
        "Rata-rata tekanan Porter %s dari 5; tertinggi dari <b>%s</b> (%s) dan <b>%s</b> (%s): PKS terbiasa dengan pengembang yang mengambil POME gratis, sehingga fee hanya diterima "
        "bila lebih kecil dari biaya yang dihindari (Bab 3). PESTLE %d faktor memberi skor bersih %+d; ekonomi (%+d) didorong harga solar tinggi, hukum (%+d) dibebani izin penjualan "
        "listrik pihak ketiga dan status aplikasi lahan."
        % (n(np.mean(list(pf.values())), 2), top[0].lower(), n(pf[top[0]], 2), top[1].lower(), n(pf[top[1]], 2), len(MK.PESTLE), sum(ps.values()), ps["Ekonomi"], ps["Hukum"]), P))
    S.append(fig(FG["porter"], 165, "Gambar 5. Porter (a), Radar per Segmen (b), Skor PESTLE (c), Daya Tarik vs Kemampuan Menang (d)"))
    S.append(KT("Tabel 4. Faktor PESTLE (skor = tanda x dampak x peluang)", tbl([["Kode", "Faktor", "Dampak", "Peluang", "Skor", "Keterangan"]] + [[k, f_, i_, l_, "%+d" % (s_ * i_ * l_), d_] for k, c_, f_, s_, i_, l_, d_ in MK.PESTLE],
                                                                              [10, 58, 13, 13, 11, 65], num_cols=(2, 3, 4))))
    # ---------------------------------------------------------------- 8 lokasi
    S.append(Paragraph("8. Integrasi Fisik di Lokasi PKS", H1))
    if os.path.exists(alir): S.append(fig(alir, 160, "Gambar 6. Diorama Lokasi PKS 45 t TBS/jam dengan Set Biogas"))
    lines = [[l, n(L_), n(cm_, 0), n(c)] for l, L_, cm_, c in T_["site_lines"]]
    S.append(KT("Tabel 5. Interkoneksi dari Model 3D Lokasi (masuk CAPEX)", tbl([["Rute", "Panjang m", "USD/m", "Biaya USD"]] + lines, [100, 20, 18, 26], num_cols=(1, 2, 3))))
    # ---------------------------------------------------------------- 9 capex opex
    S.append(Paragraph("9. CAPEX dan OPEX", H1))
    S.append(Paragraph(
        "CAPEX bottom-up: %d tangki GFS %s m³ x USD %s/m³ terpasang [ASUMSI, perlu penawaran], genset %s kWe x USD %s/kWe, skid kontak (settler %s m²), interkoneksi dari model 3D lokasi. "
        "FCI USD %s juta (2026) = USD %s/kWe terpasang (pembanding: kolam tertutup 1.800-3.700, tangki 1.800-3.500 [R3]). OPEX tahun penuh USD %s ribu ditambah MRV karbon; "
        "overhaul genset (th 8, 16) dan atap membran tangki (th 12) dimodelkan pada tahun terjadinya."
        % (T_["n_vessel"], n(T_["V_tank"]), n(v["c_gfs"]), n(T_["chp_kWe"]), n(v["c_chp"]), n(T_["A_lam"]), mu(o["fci26"]), n(o["fci26"] / T_["chp_kWe"] * 1000), n((o["opF"] + o["opV"]) / 1e3)), P))
    rows = [["Item", "Jumlah", "Total USD"]] + [[nm, "%s %s" % (n(q, 2 if q < 1 else 0), u), n(t)] for g, nm, q, u, c, t, b in o["capex_rows"]] + [["<b>FCI (2026)</b>", "", "<b>%s</b>" % n(o["fci26"])]]
    S.append(KT("Tabel 6. Rincian CAPEX 1 Set 45 t TBS/jam (USD 2026)", tbl(rows, [110, 28, 28], bold_last=True, num_cols=(2,))))
    orow = [["Komponen OPEX", "Jenis", "USD/th"]] + [[k, "Tetap" if t == "F" else "Variabel", n(val)] for k, (val, t) in o["opex_items"].items()] + [["MRV karbon (selama periode kredit)", "Tetap", n(v["c_mrv"])], ["<b>Total</b>", "", "<b>%s</b>" % n(o["opF"] + o["opV"] + v["c_mrv"])]]
    S.append(KT("Tabel 7. OPEX Tahun Penuh (USD 2026)", tbl(orow, [110, 28, 28], bold_last=True, num_cols=(2,))))
    S.append(fig(FG["capex"], 168, "Gambar 7. Struktur CAPEX (a), OPEX (b), dan Bauran Pendapatan Tahun ke-3 (c)"))
    # ---------------------------------------------------------------- 10 arus kas
    S.append(Paragraph("10. Pendapatan dan Arus Kas Pengembang", H1))
    S.append(Paragraph(
        "%s t TBS/tahun (util %s). Listrik neto %s GWh/tahun (ketersediaan %s): %s GWh ke PKS menggantikan solar pada USD %s/kWh dan %s GWh ke PLN pada %s USc/kWh x F %s "
        "(tahun 1-10) lalu %s USc/kWh. Pengurangan emisi %s tCO₂e/tahun, kredit %s pada USD %s/t selama %d tahun (diterima 1 tahun setelah vintage). Fee USD %s/t TBS dieskalasi %s/th. "
        "Bauran pendapatan: listrik %s, fee %s, karbon %s."
        % (n(T_["ffb_ty_nom"] * v["util"]), n(v["util"], 2), n(o["E"][i3], 2), pc(v["avail"], 0), n(o["Ecap"][i3], 2), n(v["p_captive"], 2), n(o["Eexp"][i3], 2),
           n(v["tariff1"], 2), n(v["F_loc"], 2), n(v["tariff2"], 2), n(o["ER"]), pc(v["cer_ratio"], 0), n(v["p_carbon"]), v["carbon_years"], n(v["fee_ffb"], 2), pc(v["infl"], 0),
           pc(o["share_el"], 0), pc(o["share_fee"], 0), pc(o["share_c"], 0)), P))
    keys = [("Jasa POME", "rev_fee"), ("Listrik ke PKS", "rev_cap"), ("Listrik ke PLN", "rev_exp"), ("Kredit karbon", "rev_c"), ("Total pendapatan", "rev"),
            ("OPEX + karbon", "opex_tot"), ("EBITDA", "ebitda"), ("CAPEX", "capex"), ("PPN CAPEX", "vat"), ("Pajak", "tax_u"), ("Arus kas bersih (FCFF)", "fcff"), ("Kumulatif", "cum")]
    cols = list(range(8)); cum = np.cumsum(o["fcff"])
    data = [["Uraian"] + ["%d (%s)" % (yrs[i], "K" if i == 0 else "O%d" % i) for i in cols]]
    for lab, k in keys:
        vals_ = cum if k == "cum" else o[k]; neg = k in ("opex_tot", "capex", "tax_u", "vat")
        data.append([lab] + [("(%s)" % n(abs(vals_[i]) / 1e3)) if (neg and vals_[i] > 0) or (not neg and vals_[i] < 0) else ("-" if abs(vals_[i]) < .5 else n(vals_[i] / 1e3)) for i in cols])
    S.append(KT("Tabel 8. Model Arus Kas %d-%d (USD ribu; kurung = negatif; K = konstruksi, O = operasi)" % (yrs[0], yrs[7]), tbl(data, [36] + [16.2] * 8, num_cols=tuple(range(1, 9)))))
    S.append(fig(FG["cf"], 165, "Gambar 8. Arus Kas Tahunan dan Kumulatif %d-%d" % (yrs[0], yrs[-1])))
    # ---------------------------------------------------------------- 11 indikator
    S.append(Paragraph("11. NPV, IRR, dan Payback", H1))
    S.append(Paragraph(
        "WACC %s = %s x %s x (1 - %s) + %s x %s. NPV USD %s juta; IRR proyek %s; IRR ekuitas %s (utang %s termasuk IDC, bunga %s, tenor %d th, tenggang pokok 1 th). "
        "Payback %s tahun sejak COD, payback terdiskonto %s tahun, indeks profitabilitas %s, DSCR minimum %s."
        % (pc(o["wacc"], 2), pc(v["debt_frac"], 0), pc(v["r_debt"], 1), pc(v["tax"], 0), pc(1 - v["debt_frac"], 0), pc(v["r_eq"], 0), mu(o["NPV"]), pc(o["IRR"]), pc(o["IRR_eq"]),
           pc(v["debt_frac"], 0), pc(v["r_debt"], 1), v["tenor"], n(o["PBP"], 2), n(o["DPBP"], 2), n(o["PI"], 2), n(o["DSCR_min"], 2)), P))
    S.append(fig(FG["npv"], 165, "Gambar 9. Profil NPV terhadap Tingkat Diskonto (a) dan Diagram Tornado ±20%% (b)"))
    S.append(fig(FG["pb"], 165, "Gambar 10. Kurva Payback Biasa dan Terdiskonto"))
    dec = lambda ok: "Layak" if ok else "Tidak layak"
    ind = [["Indikator", "Hasil", "Kriteria", "Keputusan"],
           ["NPV @ WACC %s" % pc(o["wacc"]), "USD %s juta" % mu(o["NPV"]), "> 0", dec(o["NPV"] > 0)],
           ["IRR proyek", pc(o["IRR"]), "> WACC", dec(o["IRR"] > o["wacc"])],
           ["IRR ekuitas", pc(o["IRR_eq"]), ">= %s" % pc(v["r_eq"], 0), dec(o["IRR_eq"] >= v["r_eq"] - 5e-4)],
           ["Payback sejak COD", "%s th" % n(o["PBP"], 2), "< %d th" % v["n_op"], dec(o["PBP"] < v["n_op"])],
           ["Payback terdiskonto", "%s th" % n(o["DPBP"], 2), "< %d th" % v["n_op"], dec(np.isfinite(o["DPBP"]) and o["DPBP"] < v["n_op"])],
           ["Indeks profitabilitas", n(o["PI"], 2), "> 1,0", dec(o["PI"] > 1)],
           ["DSCR minimum", n(o["DSCR_min"], 2), ">= 1,30", dec(o["DSCR_min"] >= 1.3)],
           ["PKS hemat vs kolam", pc(cm["saving_D_vs_A_pct"], 0), "> 0", dec(cm["saving_D_vs_A_pct"] > 0)],
           ["Fee di dalam jendela", "USD %s/t TBS" % n(v["fee_ffb"], 2), "%s-%s" % (n(fw["fee_min"], 2), n(fw["fee_max"], 2)), dec(fw["fee_min"] < v["fee_ffb"] < fw["fee_max"])],
           ["Puncak kebutuhan dana", "USD %s juta" % mu(o["peak_funding"]), "Struktur pendanaan", "Informasi"]]
    S.append(KT("Tabel 9. Ringkasan Indikator Kelayakan (1 set 45 t TBS/jam, segmen S3)", tbl(ind, [56, 40, 44, 26], num_cols=(1,))))
    # ---------------------------------------------------------------- 12 BEP
    S.append(Paragraph("12. Titik Impas", H1))
    S.append(Paragraph(
        "BEP tunai tercapai pada %s produksi energi dasar dan BEP akuntansi (penyusutan buku + bunga) pada %s. Proyek tetap ber-NPV positif selama fee di atas USD %s/t TBS, "
        "tarif PLN tahun 1-10 di atas %s USc/kWh x F, harga karbon di atas USD %s/t, atau CAPEX di bawah %s dasar."
        % (pc(be["BEP_cash"], 0), pc(be["BEP_acc"], 0), n(be["fee_be"], 2), n(be["tariff1_be"], 2), n(be["p_carbon_be"], 1), pc(be["capex_be"], 0)), P))
    S.append(fig(FG["bep"], 165, "Gambar 11. Titik Impas Operasional (a) dan Nilai Impas NPV = 0 (b)"))
    # ---------------------------------------------------------------- 13 ketidakpastian
    S.append(Paragraph("13. Analisis Ketidakpastian", H1))
    base, res = RES["torn"]
    S.append(Paragraph(
        "Tornado: variabel paling berpengaruh adalah <b>%s</b>, <b>%s</b> dan <b>%s</b>. Monte Carlo %s iterasi (util 0,60-0,90, CAPEX +35%%, harga karbon 3-8,3, tarif tawar 90%% plafon "
        "dengan peluang 25%%) memberi NPV P10/P50/P90 = USD %s / %s / %s juta, peluang NPV > 0 = %s, IRR P50 = %s."
        % (res[0][0].lower(), res[1][0].lower(), res[2][0].lower(), n(len(mc["NPV"])), *[n(F.pct(mc["NPV"], q) / 1e6, 2) for q in (10, 50, 90)], pc((mc["NPV"] > 0).mean(), 0), pc(F.pct(mc["IRR"], 50, -0.5))), P))
    S.append(fig(FG["mc"], 168, "Gambar 12. Distribusi NPV (a), Kurva S IRR (b), dan Penggerak Ketidakpastian (c)"))
    scr = [["Skenario", "FCI USD juta", "NPV USD juta", "IRR", "Payback th"]] + [[s[0].replace("\n", " "), mu(s[1]["fci"]), mu(s[1]["NPV"]), pc(s[1]["IRR"]), n(s[1]["PBP"], 1)] for s in RES["SC"]]
    S.append(KT("Tabel 10. Skenario", tbl(scr, [62, 26, 26, 22, 26], num_cols=(1, 2, 3, 4))))
    S.append(fig(FG["sc"], 150, "Gambar 13. NPV dan IRR per Skenario"))
    # ---------------------------------------------------------------- 14 armada
    S.append(Paragraph("14. Model Perusahaan", H1))
    u1 = fl["units"][0]; u10 = fl["units"][min(9, len(fl["units"]) - 1)]
    S.append(Paragraph(
        "Perusahaan membangun %d set 2027-2034. Unit pertama FOAK (+20%%) USD %s juta; kurva belajar 90%% pada %d%% FCI dan eskalasi %s/th membawa unit ke-%d menjadi USD %s juta (nominal %d). "
        "Setelah overhead korporat tanpa perisai pajak, perusahaan memberi NPV USD %s juta, IRR %s dan puncak kebutuhan dana USD %s juta."
        % (sum(F.ROLL.values()), mu(u1[5]), round(F.LEARN_SHARE * 100), pc(v["infl"], 0), u10[0], mu(u10[5]), u10[1], mu(fl["NPV"], 1), pc(fl["IRR"]), mu(fl["peak"], 1)), P))
    S.append(fig(FG["fleet"], 165, "Gambar 14. Penggelaran Armada (a) dan Arus Kas Perusahaan (b)"))
    # ---------------------------------------------------------------- 15 syarat
    S.append(Paragraph("15. Syarat Sebelum FID dan Catatan Data", H1))
    for t in ("(1) <b>Seleksi PKS</b>: konsumsi solar terukur >= 2 L/t TBS (meter genset 12 bulan), util >= 0,7, kontrak POME 20 tahun.",
              "(2) <b>Struktur hukum penjualan listrik ke PKS</b> (IUPTLS milik PKS + kontrak jasa energi/biogas) - nasihat hukum [R2].",
              "(3) <b>Pilot</b> 1 tangki 6 bulan: OLR, VFA, tangkapan settler %s, COD efluen; jaminan kinerja vendor." % pc(PR["EQ"]["e_set"], 0),
              "(4) <b>Penawaran vendor</b> tangki GFS (USD/m³), genset, skid kontak; harga saat ini [ASUMSI].",
              "(5) <b>PPA PLN</b> <= 1 MW dan konfirmasi faktor F; <b>registrasi karbon</b> Verra/SRUK tanpa penghitungan ganda dengan klaim GRK PKS."):
        S.append(Paragraph(t, P0))
    S.append(Paragraph(
        "Semua angka bersumber dari research/R1-R4 (register 177 parameter di lembar Sumber Excel) atau ditandai [ASUMSI]. Keterbatasan riset: banyak sumber hanya terbaca sebagai "
        "cuplikan mesin pencari (akses halaman penuh terblokir) - item berkeyakinan rendah (faktor F, biaya pengurasan, porsi PKS bergantung diesel) harus dikonfirmasi dengan data PKS nyata.", P))
    doc.build(S, onFirstPage=_pg, onLaterPages=_pg)
    return OUT

def MI_r():
    import fin_mill as MI
    return MI.mvals()["r_mill"]

def _pg(c, d):
    c.saveState(); c.setFont("Ser", 8.5); c.setFillColor(colors.grey)
    c.drawString(22 * mm, 10 * mm, "Set Biogas Kontak Termofilik - Analisis Ekonomi v3"); c.drawRightString(A4[0] - 22 * mm, 10 * mm, "%d" % d.page)
    c.restoreState()
