// Slide 8: Rencana implementasi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const ch = D.tgt.chain;
  const s = H.slide(8, "Empat gerbang dalam 30 bulan mengubah asumsi menjadi kontrak: {{NPV naik dari USD " + fmt(ch[0].NPV / 1e6, 2) + " menjadi " + fmt(ch[4].NPV / 1e6, 2) + " juta}} dengan dana pengembangan USD 1,3 juta",
    "Implementasi. Gantt, gerbang tahap, anggaran, risiko, dan perizinan. NPV dan IRR per gerbang dihitung kumulatif dengan model keuangan (kasus awal -> G0 solar 3,0 L/t -> G1 CAPEX -15% -> G2 fee USD 1,35/t -> karbon USD 8,3/t). Peluang NPV positif Monte Carlo per gerbang: 25%, 24%, 35%, 46%, 45%. RACI: tim A untuk data, FEED, konstruksi; PKS A untuk izin lahan; EPC R untuk FEED dan konstruksi; laboratorium R untuk uji. Anggaran adalah usulan tim.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  H.hdr(s, "(a) Jadwal 11 kegiatan dan jalur kritis (K4/2026 – K2/2029)", 0.45, 1.25, 8.0, { h: 0.24, fs: 9.5 });
  const q = ["K4 '26", "K1 '27", "K2", "K3", "K4", "K1 '28", "K2", "K3", "K4", "K1 '29", "K2"]; const X0 = 3.55, QW = 0.44, Y0 = 1.52;
  q.forEach((t, i) => H.box(s, t, X0 + i * QW, Y0, QW - 0.02, 0.2, { fs: 6.8, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.02, margin: 0 }));
  const ph = [["1.1", "Log solar dan POME PKS mitra", 0, 2, C.mid, "6 bln"], ["1.2", "Uji lab semikontinu 55 °C", 0, 3, C.mid, "9 bln"], ["2.1", "Kuotasi tangki GFS dan genset", 1, 3, C.royal, "6 bln"], ["2.2", "FEED dan HAZOP", 2, 5, C.royal, "9 bln"], ["2.3", "Izin: PBG, SLO, IUPTLS, PJBL", 1, 7, C.royal, "18 bln"], ["2.4", "Kontrak jasa 20 tahun dan pendanaan", 4, 8, C.royal, "12 bln"],
    ["3.1", "Pilot 10–20 m³ di PKS (TRL 6)", 3, 8, C.green, "15 bln"], ["4.1", "Pengadaan genset dan tangki", 5, 9, C.teal, "12 bln"], ["4.2", "Konstruksi dan komisioning set 1", 7, 10, C.teal, "9 bln"], ["5.1", "Operasi demonstrasi (TRL 7) + MRV", 9, 11, C.green, "6 bln"], ["5.2", "Replikasi set 2–10 (2029–2034)", 10, 11, C.navy, "→"]];
  const RH = 0.215, gy0 = Y0 + 0.23;
  ph.forEach(([w, t, a, b, c, d], i) => { const y = gy0 + i * RH; if (i % 2 === 0) H.rect(s, 0.45, y, 8.0, RH, { fill: C.panel, line: null });
    H.t(s, [{ text: w + "  ", options: { bold: true, color: C.royal } }, { text: t }], 0.52, y, 3.0, RH, { fontSize: 8, valign: "middle" });
    H.box(s, d, X0 + a * QW, y + 0.035, (b - a) * QW - 0.02, RH - 0.07, { fs: 7, bold: true, color: C.white, fill: c, line: null, radius: 0.03, margin: 0 }); });
  const gb = gy0 + ph.length * RH;
  [[2, "G0"], [5, "G1"], [8, "G2"], [10.5, "G3"]].forEach(([x, t]) => { H.ln(s, X0 + x * QW, Y0 + 0.22, X0 + x * QW, gb + 0.02, { color: C.red, w: 1, dash: "dash", arrow: false }); H.box(s, t, X0 + x * QW - 0.17, gb + 0.02, 0.34, 0.21, { fs: 8, bold: true, color: C.white, fill: C.red, line: null, radius: 0.1, margin: 0, font: FONT_H }); });
  H.t(s, [{ text: "Jalur kritis: ", options: { bold: true, color: C.red } }, { text: "kuotasi → FEED → izin PLN dan IUPTLS → genset (6–9 bulan) → konstruksi" }], 0.52, gb + 0.02, 2.95, 0.22, { fontSize: 7.4, valign: "middle" });
  // kanan
  H.hdr(s, "(b) Nilai yang dibuka tiap gerbang", 8.6, 1.25, 4.3, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_gerbang.png", 8.55, 1.52, 4.4, 1.55, "grafik-gerbang");
  H.hdr(s, "(c) Dana pengembangan per gerbang", 8.6, 3.1, 4.3, { h: 0.24, fs: 9.5 });
  img("f_dana.png", 8.55, 3.37, 4.4, 1.2, "grafik-dana");
  // kartu gerbang
  const g = [["G0 · Data PKS · bulan 6", ["PKS mitra dengan solar ≥ 3,0 L/t TBS (log 12 bulan)", "Jaringan 20 kV ≤ 2 km; beban TBS ≥ 70%", "Surat minat PKS mitra"], 1], ["G1 · Kuotasi · bulan 15", ["FCI ≤ USD 5,0 juta (−15%)", "Tiga kuotasi tangki GFS dan genset", "Perjanjian pendahuluan PKS"], 2], ["G2 · FEED dan hukum · bulan 24", ["HAZOP tanpa risiko tinggi", "Kontrak jasa 20 tahun, fee ≥ USD 1,35/t", "Penawaran utang dengan DSCR ≥ 1,30"], 3], ["G3 · Pilot · bulan 30", ["COD ≥ 65% pada OLR ≥ 8; H₂S ≤ 50 ppm", "Sertifikasi MRV karbon (USD 8,3/t)", "Kontrak ditandatangani → FID"], 4]];
  g.forEach(([h, ls, ix], i) => { const x = 0.45 + i * 3.14, w = 3.05, c = ch[ix];
    H.hdr(s, h, x, 4.6, w, { fill: C.red, h: 0.23, fs: 8.8 }); H.rect(s, x, 4.83, w, 0.82, { fill: C.white, line: C.red, radius: 0, lw: 1 });
    H.t(s, ls.map((t, j) => ({ text: t, options: { bullet: { indent: 9 }, breakLine: j < 2, paraSpaceAfter: 1 } })), x + 0.08, 4.86, w - 0.16, 0.5, { fontSize: 8 });
    H.box(s, "Membuka: NPV USD " + fmt(c.NPV / 1e6, 2) + " juta · IRR " + fmt(c.IRR * 100, 1) + "%", x + 0.08, 5.38, w - 0.16, 0.24, { fs: 8.2, bold: true, color: C.green, fill: C.greenL, line: null, radius: 0.04 }); });
  // tabel
  H.hdr(s, "Pengelolaan risiko: fokus · pengendali · pemilik", 0.45, 5.7, 6.1, { fill: C.navy, h: 0.2, fs: 8.2 });
  H.table(s, [["Tarif dan izin jual listrik", "konfirmasi ESDM; kontrak jasa energi", "hukum"], ["Kinerja termofilik", "pilot G3; jaminan bertahap", "teknis"], ["Harga dan waktu peralatan", "tiga kuotasi G1; pesan genset dini", "pengadaan"]], 0.45, 5.9, [1.8, 3.2, 1.1], { fs: 7.8, rh: 0.2, head: 0 });
  H.hdr(s, "Izin utama: izin · otoritas · selesai", 6.7, 5.7, 6.2, { fill: C.navy, h: 0.2, fs: 8.2 });
  H.table(s, [["PBG/SLF; UKL-UPL dan persetujuan teknis air limbah", "pemda; KLH/DLH", "bulan 18"], ["IUPTLS/IUPTLU, PJBL, SLO", "ESDM (Gatrik), PLN, LIT", "bulan 24"], ["K3 bejana tekan dan listrik", "Kemnaker", "bulan 27"]], 6.7, 5.9, [3.5, 1.8, 0.9], { fs: 7.8, rh: 0.2, head: 0 });
  H.concl(s, "Dana USD 1,3 juta menaikkan NPV set pertama di setiap gerbang; modal utama (± USD 4,9 juta) baru keluar setelah kontrak dan kuotasi terkunci.", "Kesimpulan");
  H.src(s, "usulan tim; durasi izin dari research/R4 dan R6 (SLO ≤ 4 hari kerja setelah inspeksi: FAQ Ditjen Gatrik 2024; lama izin lain perkiraan tim); NPV dan IRR per gerbang dari fin_core.py. Anggaran belum berkomitmen.", "FEED desain rekayasa awal; HAZOP kajian bahaya dan operabilitas; MRV pemantauan, pelaporan, verifikasi; FID keputusan investasi akhir; PBG persetujuan bangunan gedung; SLO sertifikat laik operasi; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri; LIT lembaga inspeksi teknik.");
};
