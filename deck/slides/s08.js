// Slide 8: Rencana implementasi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const ch = D.tgt.chain;
  const s = H.slide(8, "Kami membangun bertahap: empat {{gerbang}} adalah titik keputusan lanjut atau berhenti, sehingga dana besar baru keluar setelah risiko utama terjawab",
    "Implementasi. Gantt, peta risiko (peluang x dampak, penilaian tim), KPI, gerbang tahap, dan anggaran usulan USD 1,3 juta (G0 150, G1 340, G2 400, G3 410 ribu). NPV dan IRR per gerbang dihitung kumulatif: kasus awal -> G0 solar 3,0 L/t -> G1 CAPEX -15% -> G2 fee 1,35 -> karbon 8,3. RACI: tim A untuk data, FEED, konstruksi; PKS A untuk izin lahan; EPC R untuk FEED dan konstruksi; laboratorium R untuk uji. Perizinan: PBG/SLF (pemda, bulan 18); UKL-UPL dan persetujuan teknis air limbah (KLH/DLH, bulan 18); IUPTLS/IUPTLU, PJBL, SLO (ESDM, PLN, LIT, bulan 24); K3 bejana tekan (Kemnaker, bulan 27).");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  // (a) Gantt
  H.hdr(s, "A. Apa dikerjakan kapan (K4/2026 – K2/2029)", 0.45, 1.25, 6.5, { h: 0.24, fs: 9.2 });
  const q = ["K4 '26", "K1 '27", "K2", "K3", "K4", "K1 '28", "K2", "K3", "K4", "K1 '29", "K2"]; const X0 = 3.15, QW = 0.335, Y0 = 1.52;
  q.forEach((t, i) => H.box(s, t, X0 + i * QW, Y0, QW - 0.02, 0.2, { fs: 6, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.02, margin: 0 }));
  const ph = [["1", "Data PKS dan uji laboratorium 55 °C", 0, 3, C.mid, "9 bln"], ["2.1", "Kuotasi harga tangki dan genset", 1, 3, C.royal, "6"], ["2.2", "Desain rinci dan kajian bahaya", 2, 5, C.royal, "9"], ["2.3", "Perizinan (bangunan, lingkungan, listrik)", 1, 7, C.royal, "18 bln"], ["2.4", "Kontrak jasa 20 tahun dan pinjaman", 4, 8, C.royal, "12"], ["3", "Pilot 10–20 m³ di PKS mitra", 3, 8, C.green, "15 bln"], ["4", "Pengadaan, konstruksi, komisioning", 5, 10, C.teal, "15 bln"], ["5", "Demonstrasi, lalu replikasi set 2–10", 9, 11, C.green, "→"]];
  const RH = 0.215, gy0 = Y0 + 0.23;
  ph.forEach(([w, t, a, b, c, d], i) => { const y = gy0 + i * RH; if (i % 2 === 0) H.rect(s, 0.45, y, 6.5, RH, { fill: C.panel, line: null });
    H.t(s, [{ text: w + "  ", options: { bold: true, color: C.royal } }, { text: t }], 0.5, y, 2.65, RH, { fontSize: 7.4, valign: "middle" });
    H.box(s, d, X0 + a * QW, y + 0.03, (b - a) * QW - 0.02, RH - 0.06, { fs: 6.6, bold: true, color: C.white, fill: c, line: null, radius: 0.03, margin: 0 }); });
  const gb = gy0 + ph.length * RH;
  [[2, "G0"], [5, "G1"], [8, "G2"], [10.5, "G3"]].forEach(([x, t]) => { H.ln(s, X0 + x * QW, Y0 + 0.22, X0 + x * QW, gb + 0.02, { color: C.red, w: 1, dash: "dash", arrow: false }); H.box(s, t, X0 + x * QW - 0.16, gb + 0.02, 0.32, 0.2, { fs: 7.5, bold: true, color: C.white, fill: C.red, line: null, radius: 0.1, margin: 0, font: FONT_H }); });
  H.t(s, [{ text: "Jalur kritis: ", options: { bold: true, color: C.red } }, { text: "kuotasi → desain → izin → genset → konstruksi" }], 0.5, gb + 0.02, 2.65, 0.2, { fontSize: 7.2, valign: "middle" });
  H.take(s, "Batang = lama kegiatan. Garis merah putus-putus = gerbang. Pembangunan baru dimulai setelah G1 (harga pasti), dan modal besar baru keluar setelah G2–G3.", 0.45, gb + 0.27, 6.5, 0.38, "Cara membaca: ");
  // (b) risiko
  H.hdr(s, "B. Risiko utama: sebelum dan sesudah mitigasi", 7.1, 1.25, 5.8, { fill: C.red, h: 0.24, fs: 9.2 });
  img("f_risiko.png", 7.3, 1.52, 5.3, 5.3 * 2.3 / 5.55, "grafik-risiko");
  H.take(s, "Semua risiko turun ke zona hijau atau kuning setelah mitigasi. Yang paling lama dikelola adalah kinerja reaktor (R2), yang baru terjawab oleh pilot di G3.", 7.1, gb + 0.27, 5.8, 0.38, "Artinya: ");
  // (c) KPI dan (d) mitigasi
  const Y2 = 4.14;
  H.hdr(s, "C. Ukuran keberhasilan (KPI)", 0.45, Y2, 6.5, { fill: C.teal, h: 0.22, fs: 9 });
  H.table(s, [["Bidang", "Yang diukur", "Target", "Cara mengukur"], ["Teknis", "Beban pencemar (COD) yang tersisih", "≥ 65% (di G3)", "analisis laboratorium mingguan"], ["Energi", "Listrik neto per m³ POME", "≥ 40 kWh", "meter genset"], ["Operasi", "Waktu set beroperasi", "≥ 93%", "pemantauan jarak jauh"], ["Dampak", "Emisi metana dihindari per set", "≥ 30 ribu tCO₂e/tahun", "verifikasi MRV"]].map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, r[1], { text: r[2], options: { bold: true, color: C.green } }, r[3]]), 0.45, Y2 + 0.24, [0.75, 2.25, 1.5, 2.0], { fs: 7.6, rh: 0.205, hrh: 0.2, margin: [1, 3, 1, 3] });
  H.hdr(s, "D. Cara kami menangani risiko", 7.1, Y2, 5.8, { fill: C.red, h: 0.22, fs: 9 });
  H.table(s, [["ID", "Risiko", "Penanganan", "Pemilik"], ["R1", "Tarif dan izin jual listrik", "konfirmasi ESDM/PLN; kontrak jasa energi", "hukum"], ["R2", "Kinerja reaktor termofilik", "pilot G3; jaminan kinerja bertahap", "teknis"], ["R3", "Biaya melampaui rencana", "tiga kuotasi di G1; pesan genset dini", "pengadaan"], ["R4", "Solar PKS di bawah target", "pilih PKS dengan solar ≥ 3,0 L/t", "komersial"], ["R5", "Beban TBS PKS rendah", "klausul beban minimum; fee dasar", "komersial"]].map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.red, align: "center" } }, r[1], r[2], r[3]]), 7.1, Y2 + 0.24, [0.35, 1.7, 2.7, 1.05], { fs: 7.4, rh: 0.2, hrh: 0.2, margin: [1, 3, 1, 3] });
  // (e) gerbang
  const g = [["G0 · bulan 6 · USD 150 ribu", "Apakah PKS mitra cocok?", "Lolos: solar ≥ 3,0 L/t, jaringan ≤ 2 km", 1], ["G1 · bulan 15 · USD 340 ribu", "Berapa harga sebenarnya?", "Lolos: tiga kuotasi, investasi ≤ USD 5,0 juta", 2], ["G2 · bulan 24 · USD 400 ribu", "Apakah kontrak dan izin aman?", "Lolos: fee ≥ USD 1,35/t, kajian bahaya bersih", 3], ["G3 · bulan 30 · USD 410 ribu", "Apakah reaktor terbukti?", "Lolos: pilot ≥ 65% COD tersisih → keputusan investasi", 4]];
  g.forEach(([h, qn, tx, ix], i) => { const x = 0.45 + i * 3.14, w = 3.05, c = ch[ix];
    H.hdr(s, h, x, 5.64, w, { fill: C.red, h: 0.2, fs: 8 }); H.rect(s, x, 5.84, w, 0.62, { fill: C.white, line: C.red, radius: 0, lw: 1 });
    H.t(s, [{ text: qn, options: { bold: true, color: C.navy, breakLine: true } }, { text: tx }], x + 0.07, 5.85, w - 0.14, 0.36, { fontSize: 7.6 });
    H.box(s, "Membuka NPV USD " + fmt(c.NPV / 1e6, 2) + " juta · IRR " + fmt(c.IRR * 100, 1) + "%", x + 0.07, 6.22, w - 0.14, 0.2, { fs: 8, bold: true, color: C.green, fill: C.greenL, line: null, radius: 0.04 }); });
  H.concl(s, "Dana USD 1,3 juta (usulan) dibelanjakan bertahap; modal utama (± USD 4,9 juta) baru keluar setelah kontrak, harga, dan pilot terbukti.", "Kesimpulan");
  H.src(s, "usulan tim; peluang × dampak risiko adalah penilaian tim; durasi izin dari research/R4 dan R6 (SLO ≤ 4 hari kerja setelah inspeksi: FAQ Ditjen Gatrik 2024; lama izin lain perkiraan tim); NPV dan IRR per gerbang dari fin_core.py.", "FEED desain rekayasa awal; HAZOP kajian bahaya dan operabilitas; MRV pemantauan, pelaporan, verifikasi; FID keputusan investasi akhir; OLR laju beban organik; PBG persetujuan bangunan gedung; SLO sertifikat laik operasi; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri; K3 keselamatan dan kesehatan kerja.");
};
