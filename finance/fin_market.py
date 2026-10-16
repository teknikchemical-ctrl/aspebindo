# -*- coding: utf-8 -*-
"""Analisis pasar v3: TAM-SAM-SOM bottom-up per segmen, matriks pesaing berbobot, USP terukur, PESTLE, Porter.
Sumber angka: research/R1-R4 (source_register.json) - tanda [H]/[M]/[L]/[EST] = keyakinan; [ASUMSI] = asumsi tim."""
import json, os
import numpy as np
import fin_core as F

RS = os.path.join(F.ROOT, "research")
# ------------------------------------------------------------------ data pasar (R3 kecuali disebut)
MILLS_ID = 1300            # PKS beroperasi (Trase/Universal Mill List 1.318 th 2022; UML 2023 1.231) [R3, H]
SH_CAPTURED = 0.115        # sudah menangkap metana (84 PLTBg POME ~165 MW; 10-15% PKS) [R3, M]
POME_NAT = 150e6           # m3/th (125-170) [R3, M]
SH_SIZE = 0.65             # PKS 30-60 t/jam (kelas 30-45: 30%, 45-60: 35%) [R3, L - unduh CSV Trase untuk memastikan]
SH_REGION = 0.85           # Sumatera + Kalimantan [R3, M]
SH_DIESEL = 0.20           # HIPOTESIS: PKS dengan solar terukur >= 2 L/t TBS (emplasmen/perumahan/KCP bergantung diesel); basis lemah (Kaltim 12/62 desa diesel-saja, bukan solar PKS) [EST, rentang 0,10-0,35] -> validasi survei 30 PKS pada gerbang G0
SH_GRID = 0.60             # HIPOTESIS: jaringan 20 kV PLN <= 2 km sehingga ekspor layak [EST, rentang 0,40-0,80]
SH_FREE = 0.75             # HIPOTESIS: tidak terikat program biogas in-house/kontrak grup besar (Wilmar, Musim Mas, Asian Agri) [EST, rentang 0,60-0,90]
SH_INDEP = 0.34            # 442 PKS tanpa kebun / 1.300 [R3, M]
MILLS_MY_UNCAP = 315       # Malaysia 453 PKS, ~30% menangkap metana [R3, M]
BUILD_RATE_MW = 9.0        # laju bangun PLTBg nasional historis MW/th [R3, M]
PROV = [("Riau", 260), ("Sumut", 180), ("Kalteng", 130), ("Kalbar", 120), ("Sumsel", 110), ("Kaltim", 99), ("Jambi", 90), ("Kalsel", 46), ("Lainnya", 196)]   # [R3, L]

def market(o=None):
    """TAM/SAM/SOM dalam setara-set (volume POME per set) dan pendapatan rata-rata umur proyek per set (USD/th)"""
    o = o or F.run()
    n = int(o["v"]["n_op"]); rev_avg = float(sum(o["rev"][1:])) / n
    pome_set = F.TECH["pome_m3y_nom"] * o["v"]["util"]
    uncapt = MILLS_ID * (1 - SH_CAPTURED)
    sets_TAM = POME_NAT * (1 - SH_CAPTURED) / pome_set
    mills_SAM = uncapt * SH_SIZE * SH_REGION * SH_DIESEL * SH_GRID * SH_FREE
    sets_SOM = sum(F.ROLL.values())
    L = [("TAM", "Semua PKS Indonesia tanpa penangkap metana (volume POME)", uncapt, sets_TAM),
         ("SAM-luas", "+ ukuran 30-60 t/jam + Sumatera/Kalimantan", uncapt * SH_SIZE * SH_REGION, uncapt * SH_SIZE * SH_REGION),
         ("SAM", "+ solar >= 2 L/t TBS + jaringan 20 kV <= 2 km + bebas program grup: jendela kesepakatan terbuka", mills_SAM, mills_SAM),
         ("SOM 2034", "Rencana armada (ROLL) - 1 set per PKS", sets_SOM, sets_SOM)]
    rows = [dict(level=a, rule=b, mills=c, sets=d, rev=d * rev_avg, MW=d * F.TECH["chp_kWe"] / 1000) for a, b, c, d in L]
    return dict(rev_avg=rev_avg, pome_set=pome_set, rows=rows, TAM=rows[0]["rev"], SAM=rows[2]["rev"], SOM=rows[3]["rev"], sets_TAM=sets_TAM, sets_SAM=mills_SAM,
                sets_SOM=sets_SOM, share=sets_SOM / mills_SAM, my_sets=MILLS_MY_UNCAP * SH_SIZE * SH_DIESEL * SH_GRID * SH_FREE,
                build_share=sets_SOM * F.TECH["chp_kWe"] / 1000 / 8 / BUILD_RATE_MW, mills=MILLS_ID)

# ------------------------------------------------------------------ PESTLE: (kode, kategori, faktor, tanda, dampak 1-5, peluang 1-5, keterangan)
PESTLE = [
    ("P1", "Politik", "Target EBT & NZE 2060; RUPTL 2025-34 bioenergi +0,9 GW", +1, 3, 4, "Bioenergi kecil di RUPTL; PLTBg terpasang ~164 MW [R1]"),
    ("P2", "Politik", "Harga patokan PLTBg Perpres 112/2022", +1, 4, 3, "10,18 USc x F (<= 1 MW, th 1-10), 6,11 th 11+ [R2]; tarif = plafon, bukan jaminan"),
    ("P3", "Politik", "PPA PLN lambat; power wheeling belum ada (RUU EBET)", -1, 4, 4, "Listrik ke PKS/emplasmen lebih kuat dari ekspor [R1/R2]"),
    ("P4", "Politik", "ISPO wajib hilir & bioenergi termasuk biogas (Perpres 16/2025, 19 Mar 2027)", +1, 3, 4, "SPV biogas juga perlu ISPO [R1]"),
    ("P5", "Politik", "Perpres 110/2025 nilai ekonomi karbon; SRUK; MRA Verra & GS", +1, 3, 3, "Jalur kredit internasional dibuka [R1]"),
    ("E1", "Ekonomi", "Solar non-subsidi mahal (Dexlite Rp 23.700/L; listrik diesel ~USD 0,37/kWh)", +1, 5, 4, "Inti nilai bagi PKS bergantung diesel [R2]"),
    ("E2", "Ekonomi", "Suku bunga tinggi (BI 5,75%; utang iklim 9-11%)", -1, 3, 4, "WACC USD 9,7% [R2]"),
    ("E3", "Ekonomi", "Harga kredit karbon rendah (USD 3,5-5; IDXCarbon tipis)", -1, 3, 4, "Karbon pendapatan sekunder [R1]"),
    ("E4", "Ekonomi", "Utilisasi PKS ~50-80% (kapasitas ~2x produksi)", -1, 4, 4, "Basis util 0,75 [R3]; seleksi PKS penting"),
    ("E5", "Ekonomi", "Produksi CPO naik (51,7 Mt 2025)", +1, 2, 4, "Pasokan POME aman [R3]"),
    ("S1", "Sosial", "Bau & air kolam POME; desa sekitar PKS tanpa listrik", +1, 3, 4, "Reaktor tertutup; listrik emplasmen [R2-tambahan]"),
    ("S2", "Sosial", "Lapangan kerja lokal (10 orang/set)", +1, 2, 4, "Operator dari desa sekitar"),
    ("S3", "Sosial", "Kelangkaan teknisi biogas termofilik", -1, 3, 3, "Pelatihan + SCADA jarak jauh"),
    ("T1", "Teknologi", "Proses kontak termofilik pada POME baru skala pilot", -1, 4, 3, "Choorit 2007 HRT 5 d stabil; perlu pilot + jaminan kinerja [R4]"),
    ("T2", "Teknologi", "Genset biogas & tangki GFS dibaut sudah matang", +1, 3, 5, "Rantai pasok global [R4]"),
    ("T3", "Teknologi", "H2S 1.000-4.000 ppm, pasir, minyak", -1, 3, 3, "BTF 95% + ruang pasir 85% [R4]"),
    ("T4", "Teknologi", "Produksi seri tangki & skid standar", +1, 3, 4, "Kurva belajar 10%/penggandaan pada 60% FCI"),
    ("H1", "Hukum", "Dasar hukum aplikasi lahan dicabut 2021; wacana larangan 2024", -1, 4, 3, "Efluen set tetap ke polishing + LA (BOD 1.500 < 5.000) [R1]"),
    ("H2", "Hukum", "Penjualan listrik pihak ketiga ke PKS butuh izin (IUPTLS/wilayah usaha)", -1, 4, 3, "Struktur: kontrak jasa energi/biogas; perlu nasihat hukum [R2]"),
    ("H3", "Hukum", "Penegakan pencemaran POME (penjara direksi, penyegelan)", +1, 3, 3, "PT SIPP 2024, PT BMB 2023 [R1]"),
    ("L1", "Lingkungan", "Metana POME 0,5-1,1 tCO2e/t CPO; RED II/ISCC", +1, 4, 4, "Penangkapan metana membuka default GHG biodiesel [R1]"),
    ("L2", "Lingkungan", "Kolam anaerobik 1,1 ha dibebaskan; kue lumpur jadi pupuk", +1, 2, 4, "Plot set 0,24 ha"),
]
def pestle_scores():
    cats = ["Politik", "Ekonomi", "Sosial", "Teknologi", "Hukum", "Lingkungan"]
    return {c: sum(s * i * l for k, cc, f, s, i, l, d in PESTLE if cc == c) for c in cats}

PORTER = {
    "Pendatang baru": [("Modal per set ~USD 4 juta", 2.6, "Penghalang sedang"), ("Know-how proses kontak termofilik + data operasi", 2.4, "Hambatan teknologi & data"),
                       ("Kontraktor kolam tertutup mudah masuk", 3.4, "Teknologi lama, banyak EPC lokal")],
    "Pemasok": [("Genset biogas (Jenbacher, MWM, Weichai)", 3.4, "Sedikit merek, kirim 6-9 bln"), ("Tangki GFS dibaut (CST, ESP, Center Enamel, pabrikan Tiongkok)", 2.2, "Banyak pemasok"),
                ("Skid & fabrikasi lokal (Batam, Cilegon, Medan)", 2.0, "Banyak bengkel")],
    "Persaingan": [("Pengembang BOO/BOOT: reNIKOLA, KIS, Gree, AANE, Pertamina NRE", 3.8, "Mengambil POME gratis; fokus PKS besar/klaster [R3]"),
                   ("Program in-house grup besar (Wilmar 25, Musim Mas 17, Asian Agri)", 3.4, "Menutup segmen grup besar [R3]"),
                   ("EPC tangki/kolam tertutup untuk PKS yang punya modal", 3.2, "USD 1,8-3,7 jt/MWe [R3]")],
    "Pembeli": [("PKS: kuat menawar fee (preseden POME gratis)", 4.0, "Fee harus < biaya dihindari [Model Keputusan PKS]"),
                ("PLN pembeli tunggal listrik ekspor", 4.2, "Monopsoni, plafon tarif"), ("Pembeli kredit karbon", 3.3, "Harga volatil")],
    "Produk substitusi": [("Status quo kolam + aplikasi lahan", 3.8, "Murah tunai, masih legal (BOD <= 5.000)"), ("PLTS + baterai untuk emplasmen", 2.8, "Mengganti diesel juga, tanpa POME"),
                          ("Penyambungan ke PLN (Rp 1.115/kWh)", 3.0, "Mahal di lokasi terpencil [R2]")],
}
FORCE_ORDER = ["Pemasok", "Pembeli", "Pendatang baru", "Persaingan", "Produk substitusi"]
SEG_RADAR = {   # tekanan per kekuatan (urutan FORCE_ORDER)
    "S3 PKS bergantung diesel": [2.6, 3.4, 2.6, 2.8, 3.0],
    "S1 PKS terhubung PLN": [2.6, 4.4, 2.8, 3.6, 3.8],
    "Grup besar terintegrasi": [2.6, 4.6, 2.4, 4.0, 3.4],
    "PKS off-grid (S4)": [2.8, 3.0, 2.4, 2.4, 2.6],
}
# matriks daya tarik segmen: (nama, daya tarik 1-5, kemampuan menang 1-5, jumlah PKS perkiraan)
SEGMENTS = [("S3 PKS bergantung diesel 30-60 t/jam", 4.3, 3.9, 160), ("S4 PKS off-grid penuh", 4.5, 3.4, 60), ("S2 PKS terhubung PLN, util tinggi", 2.6, 3.0, 200),
            ("S1 PKS terhubung PLN, util rata-rata", 1.8, 2.8, 450), ("Grup besar (in-house)", 2.4, 1.8, 250), ("PKS < 30 t/jam", 1.9, 2.4, 280),
            ("Malaysia tanpa penangkap metana", 2.8, 2.0, 315)]

# ------------------------------------------------------------------ pesaing: matriks berbobot (skor 1-5, 5 = terbaik bagi PKS)
CRIT = [("Biaya POME bagi PKS (USD/t TBS, Model Keputusan PKS)", 0.25), ("Modal yang harus dikeluarkan PKS", 0.20), ("Risiko kinerja ditanggung PKS", 0.15),
        ("Kematangan / referensi di Indonesia", 0.15), ("Lahan & waktu bangun", 0.10), ("Penangkapan metana & bau", 0.10), ("Dapat dipindah (nilai sisa aset)", 0.05)]
def compet_matrix(mill=None):
    """opsi: (nama, CAPEX USD jt/MWe, lahan ha, bangun bln, PKS bayar CAPEX?, referensi ID, skor per kriteria, sumber)"""
    import fin_mill as MI
    c = mill or MI.compare()
    fl_fci = F.run()["fci26"] / (F.TECH["chp_kWe"] / 1000) / 1e6
    def s_cost(x): return float(np.clip(5 - (x - 1.5) / 0.8, 1, 5))         # 1,5 USD/t -> 5; 4,7 -> 1
    R = [("A Status quo kolam terbuka", "0 (tertanam)", "2,2 (GA 3D); 1-5 lit.", "0", "Tidak", "~85-90% PKS",
          [s_cost(c["A"]["per_t"]), 5, 3, 5, 2, 1, 1], "Model; R3"),
         ("B Kolam tertutup milik PKS", "1,8-3,7 (2,2)", "1,5", "9-15", "Ya", "Sei Mangkei 2,4 MW; AANE Belitung",
          [s_cost(c["B"]["per_t"]), 2, 2, 4, 3, 3, 1], "R2/R3"),
         ("C Tangki CSTR milik PKS (EPC)", "1,8-3,5 (2,5)", "0,75", "12-24", "Ya", "TSE 2 MW 2025; KIS PT Maya",
          [s_cost(c["C"]["per_t"]), 1, 2, 4, 3, 4, 1], "R3"),
         ("Biometana BOOT (reNIKOLA, KIS)", "~4 (5,3 jt/PKS)", "1,5", "14", "Tidak", "PTPN IV 8 PKS 2026",
          [3.5, 5, 4, 3, 3, 4, 1], "R3: hanya klaster PKS besar dengan pipa/offtake gas"),
         ("UASB/EGSB/IC", "~2,75", "0,35", "12-18", "Ya", "tidak ada di ID", [2.5, 1, 2, 1, 4, 4, 1], "R3"),
         ("AnMBR konvensional (Veolia, Kubota)", "~5,0", "0,3", "12-18", "Ya", "tidak ada referensi POME", [1.5, 1, 2, 1, 4, 5, 1], "R3/R4"),
         ("D Set kontak termofilik BOO (produk ini)", "%.1f (FCI/kWe terpasang)" % fl_fci, "%.2f" % (F.TECH["plot_m2"] / 1e4), "10", "Tidak", "belum (pilot diperlukan)",
          [s_cost(c["D"]["per_t"]), 5, 4, 2, 4, 5, 5], "Model; R3/R4")]
    out = []
    for nm, cx, la, bm, pay, ref, sc, src in R:
        out.append(dict(name=nm, capex=cx, land=la, build=bm, mill_pays=pay, ref=ref, scores=sc, total=sum(w * s for (_, w), s in zip(CRIT, sc)), src=src))
    return out

# ------------------------------------------------------------------ USP terukur
def usp(o=None, mill=None, reloc=None):
    import fin_mill as MI
    o = o or F.run(); c = mill or MI.compare(); a = c["detail"]
    sv = c["saving_D_vs_A_per_t"]; pct = c["saving_D_vs_A_pct"]
    rl = reloc or relocation_value()
    return [
        ("1 PKS hemat tanpa modal", "Biaya POME PKS turun %.2f USD/t TBS (%.0f%%) vs kolam, CAPEX PKS = 0" % (sv, pct * 100), "Model Keputusan PKS (segmen S3)", "Kuat (S3/S4); tidak berlaku untuk PKS terhubung PLN (S1)"),
        ("2 Listrik menggantikan solar", "%.1f GWh/th ke PKS pada USD %.2f/kWh vs diesel USD %.2f/kWh" % (a["cap"] / 1e6, o["v"]["p_captive"], a["c_dsl"]), "R2 (harga solar), DSNG", "Kuat; inti proposisi"),
        ("3 Aset dapat dipindah", "Bila PKS tutup th 8: NPV pengembang %s vs tangki tetap %s (USD)" % ("{:,.0f}".format(rl["reloc"]), "{:,.0f}".format(rl["stranded"])), "Model skenario relokasi", "Sedang: nilai bagi pemberi pinjaman (agunan), belum ada preseden"),
        ("4 Lahan & bau", "Membebaskan 1,1 ha kolam anaerobik; plot %.2f ha; reaktor tertutup" % (F.TECH["plot_m2"] / 1e4), "Model 3D lokasi", "Sedang: nilai tunai kecil, nilai sosial/regulasi"),
        ("5 Karbon & pasar ekspor", "%s tCO2e/th (AMS-III.H); membuka default GHG RED II/ISCC" % "{:,.0f}".format(o["ER"]), "R1", "Sedang: harga karbon rendah, akses pasar nyata"),
        ("6 Cepat dibangun", "Panel GFS + skid kontainer: ~10 bulan vs 12-24 bln tangki EPC", "R3", "Sedang: belum ada rekam jejak"),
        ("Bukan USP", "CAPEX/MWe lebih tinggi dari kolam tertutup (1,8-3,7)", "R3", "Kelemahan: ditutup oleh kurva belajar + segmen diesel")]

def relocation_value(close_year=8):
    """PKS tutup di tahun ke-close_year: set dipindah (relokasi 0,15 FCI, 6 bln henti) vs digester tetap yang terdampar (arus kas berhenti)"""
    v = F.vals()
    base = F.run(v)
    rel = F.run(v, relocate=True)                          # relokasi th 11 di model inti; di sini geser ke close_year
    w = base["wacc"]; cf = base["fcff"].copy()
    stranded = cf.copy(); stranded[close_year + 1:] = 0.0
    reloc = cf.copy(); d = close_year + 1
    reloc[d] = cf[d] * 0.5 * v["ramp1"] - 0.15 * base["fci26"] * (1 + v["infl"]) ** (base["years"][d] - 2026)
    return dict(base=F.npv(w, cf), stranded=F.npv(w, stranded), reloc=F.npv(w, reloc), close_year=close_year)
