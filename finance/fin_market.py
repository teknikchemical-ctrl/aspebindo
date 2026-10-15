# -*- coding: utf-8 -*-
"""Data analisis pasar: TAM-SAM-SOM, PESTLE (21 faktor), Lima Kekuatan Porter, matriks daya tarik segmen, pesaing.
Angka pasar dari finance/research/market_data.md (sumber + tahun). [UNVERIFIED] ditandai pada kolom sumber."""
import fin_core as F

# ------------------------------------------------------------------ ukuran pasar
MILLS = 1231                    # Universal Mill List (2023 data, publ. 2025)
POME_NAT = 125e6                # m3/th, PASPI/BRIN 2026 (rentang 125-170)
SH_SIZE = 0.70                  # porsi PKS 30-60 t/jam [UNVERIFIED, tidak ada dataset publik]
SH_NOCAP = 0.90                 # PKS tanpa penangkap metana (~10% sudah, T&E 2025)
SH_REGION = 0.85                # Sumatera + Kalimantan
PROV = [("Riau", 260), ("Sumut", 180), ("Kalteng", 130), ("Kalbar", 120), ("Sumsel", 110), ("Kaltim", 99), ("Jambi", 90), ("Kalsel", 46), ("Lainnya", 196)]

def market(o=None):
    o = o or F.run()
    rev_m3 = o["rev"][2] / F.TECH["pome_m3y"]                       # USD per m3 POME (th operasi penuh)
    tam = POME_NAT * rev_m3
    sam = tam * SH_SIZE * SH_NOCAP * SH_REGION
    sets_som = sum(n for y, n in F.ROLL.items())
    som = sets_som * o["rev"][2]
    return dict(rev_m3=rev_m3, TAM=tam, SAM=sam, SOM=som, sets_TAM=MILLS, sets_SAM=round(MILLS * SH_SIZE * SH_NOCAP * SH_REGION),
                sets_SOM=sets_som, capex_TAM=POME_NAT / F.TECH["pome_m3y"] * o["fci"], share=som / sam)

# ------------------------------------------------------------------ PESTLE: (kode, kategori, faktor, tanda, dampak 1-5, peluang terjadi 1-5, keterangan)
PESTLE = [
    ("P1", "Politik", "Target bauran EBT & NZE 2060 (RUEN, KEN)", +1, 4, 4, "Bioenergi di bawah target 5,5 GW; dorongan PLTBg"),
    ("P2", "Politik", "Harga patokan PLTBg Perpres 112/2022", +1, 4, 3, "11,47 USc/kWh x F untuk <= 1 MW (th 1-10)"),
    ("P3", "Politik", "Prioritas PLN & pengadaan lambat (RUPTL)", -1, 4, 3, "PPA skala kecil sering tertunda"),
    ("P4", "Politik", "ISPO wajib hilir & bioenergi (Perpres 16/2025)", +1, 3, 4, "Tenggat 19 Mar 2027 mendorong kepatuhan PKS"),
    ("E1", "Ekonomi", "Rupiah melemah (Rp17.855/USD, 2026)", -1, 3, 4, "Peralatan impor (genset, membran) dalam USD"),
    ("E2", "Ekonomi", "Suku bunga tinggi (BI rate 5,75%)", -1, 3, 4, "Biaya utang 8-11%"),
    ("E3", "Ekonomi", "Harga solar non-subsidi tinggi (Rp23.700/L)", +1, 3, 3, "Nilai listrik pengganti genset diesel PKS/kebun"),
    ("E4", "Ekonomi", "Harga karbon domestik rendah (IDXCarbon ~USD 2,2)", -1, 4, 4, "Ketergantungan pada pasar sukarela USD 10-25"),
    ("E5", "Ekonomi", "Produksi CPO naik (51,7 Mt 2025)", +1, 3, 4, "POME bertambah, pasokan umpan aman"),
    ("S1", "Sosial", "Keluhan bau & air dari kolam POME", +1, 3, 4, "Reaktor tertutup menghilangkan bau"),
    ("S2", "Sosial", "Lapangan kerja lokal (8 orang/set)", +1, 2, 4, "Operator dari desa sekitar PKS"),
    ("S3", "Sosial", "Kelangkaan teknisi biogas/membran", -1, 3, 3, "Butuh pelatihan & SCADA jarak jauh"),
    ("T1", "Teknologi", "AnMBR termofilik POME belum banyak skala penuh", -1, 4, 3, "Perlu pilot & garansi kinerja"),
    ("T2", "Teknologi", "Genset biogas kontainer sudah matang", +1, 3, 5, "Rantai pasok & layanan tersedia"),
    ("T3", "Teknologi", "Fouling membran & H2S tinggi", -1, 3, 3, "CIP, cross-flow 4 m/s, BTF + karbon aktif"),
    ("T4", "Teknologi", "Produksi seri bejana standar & kontainer", +1, 3, 4, "Kurva belajar biaya 10%/penggandaan"),
    ("H1", "Hukum", "Baku mutu efluen POME diperketat (revisi 2026)", +1, 4, 3, "BOD 100 mg/L mendorong pengolahan lanjut"),
    ("H2", "Hukum", "Perizinan PPA, IUPTL, SLO panjang", -1, 3, 4, "6-12 bulan sebelum COD"),
    ("H3", "Hukum", "Kepastian status Perpres 112/2022", -1, 4, 2, "Satu basis data mencatat 'dicabut' - perlu konfirmasi"),
    ("L1", "Lingkungan", "Metana POME ~ sumber GRK terbesar PKS; EUDR/RSPO", +1, 4, 4, "36.800 tCO2e/th terhindar per set"),
    ("L2", "Lingkungan", "Pengurangan lahan kolam 5-8 ha per PKS", +1, 3, 4, "Plot set hanya 0,29 ha"),
]
def pestle_scores():
    cats = ["Politik", "Ekonomi", "Sosial", "Teknologi", "Hukum", "Lingkungan"]
    return {c: sum(s * i * l for k, cc, f, s, i, l, d in PESTLE if cc == c) for c in cats}

# ------------------------------------------------------------------ Porter: kekuatan -> [(sub-faktor, skor 1-5, alasan)]
PORTER = {
    "Pendatang baru": [("Kebutuhan modal per set USD 5,4 juta", 2.5, "Penghalang sedang"), ("Know-how AnMBR termofilik", 2.2, "Hambatan teknologi & data operasi"),
                       ("Kontraktor kolam tertutup mudah masuk", 3.4, "Teknologi lama, banyak EPC lokal")],
    "Pemasok": [("Genset biogas (Jenbacher, MWM, Weichai)", 3.4, "Sedikit merek, waktu kirim 6-9 bln"), ("Membran UF tubular", 3.6, "Pemasok global terbatas"),
                ("Fabrikasi bejana CS (Batam, Cilegon)", 2.0, "Banyak bengkel lokal")],
    "Persaingan": [("Kolam tertutup (Asian Agri, grup besar)", 3.8, "Capex/kW lebih murah"), ("Biometana/CNG (reNIKOLA-Pertagas, KIS)", 3.4, "Kontrak 15 th, skala besar"),
                   ("CSTR tangki Eropa (Weltec, Biotec)", 3.0, "Tidak portabel, mahal")],
    "Pembeli": [("PLN pembeli tunggal listrik", 4.3, "Monopsoni, harga patokan"), ("PKS pemilik lahan & POME", 3.6, "Menegosiasi jasa & sewa"),
                ("Pembeli kredit karbon", 3.3, "Harga volatil, preferensi metodologi")],
    "Produk substitusi": [("Penutupan kolam + flare saja", 3.6, "Murah, cukup untuk ISPO"), ("Land application & kompos", 3.0, "Tanpa pendapatan energi"),
                          ("Co-firing biogas di boiler PKS", 3.0, "Mengurangi kebutuhan listrik ekspor")],
}
SEG_RADAR = {   # tekanan per kekuatan untuk 4 segmen (urutan: Pemasok, Pembeli, Pendatang baru, Persaingan, Substitusi)
    "PKS swasta 45 t/jam": [3.0, 3.4, 2.6, 3.2, 3.0],
    "Grup besar terintegrasi": [2.8, 4.4, 2.4, 3.9, 3.6],
    "PTPN (BUMN)": [3.0, 4.0, 2.8, 3.4, 3.4],
    "PKS Kalimantan (F 1,1)": [3.3, 3.2, 2.5, 2.9, 3.1],
}
FORCE_ORDER = ["Pemasok", "Pembeli", "Pendatang baru", "Persaingan", "Produk substitusi"]

# ------------------------------------------------------------------ matriks daya tarik (daya tarik pasar, kemampuan menang) 1-5
SEGMENTS = [("PKS swasta 45 t/jam Sumatera", 3.9, 4.0, 160), ("PKS 60 t/jam", 3.7, 3.4, 120), ("PKS 30 t/jam", 2.8, 3.6, 150),
            ("PKS Kalimantan (F 1,1)", 3.5, 3.2, 130), ("PTPN (BUMN)", 3.3, 2.6, 110), ("Grup besar (in-house)", 3.0, 2.2, 140),
            ("Ekspor Malaysia/Thailand", 2.6, 2.0, 90)]

# ------------------------------------------------------------------ pesaing / teknologi alternatif
COMPET = [("Kolam tertutup (covered lagoon)", "1,5-2,5", "5-8", "12-18", "Tidak", "Rendah-sedang", "Asian Agri, grup besar"),
          ("CSTR tangki beton/baja", "2,5-4,0", "1-2", "18-24", "Tidak", "Sedang", "Weltec, Biotec, EPC lokal"),
          ("Biometana / CNG", "> 4", "1-2", "24", "Tidak", "Tinggi", "reNIKOLA-Pertagas, KIS-Toyota Tsusho"),
          ("AnMBR termofilik portabel (produk ini)", "4,9 (unit-1) -> 3,5 (unit-10)", "0,29", "11", "Ya (28 muatan truk)", "Tinggi (BOD efluen rendah)", "-")]
