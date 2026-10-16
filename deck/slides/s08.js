// Slide 8: Rencana implementasi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const ch = D.tgt.chain;
  const s = H.slide(8, "Rencana 30 bulan dengan empat gerbang, enam risiko yang dipetakan dan dimitigasi, serta lima KPI terukur: {{NPV set pertama naik ke USD " + fmt(ch[4].NPV / 1e6, 2) + " juta}}",
    "Implementasi. Gantt, peta risiko (peluang x dampak, penilaian tim), KPI, gerbang tahap, dan anggaran usulan USD 1,3 juta (G0 150, G1 340, G2 400, G3 410 ribu). NPV dan IRR per gerbang dihitung kumulatif: kasus awal -> G0 solar 3,0 L/t -> G1 CAPEX -15% -> G2 fee 1,35 -> karbon 8,3. RACI: tim A untuk data, FEED, konstruksi; PKS A untuk izin lahan; EPC R untuk FEED dan konstruksi; laboratorium R untuk uji. Perizinan: PBG/SLF (pemda, bulan 18); UKL-UPL dan persetujuan teknis air limbah (KLH/DLH, bulan 18); IUPTLS/IUPTLU, PJBL, SLO (ESDM, PLN, LIT, bulan 24); K3 bejana tekan (Kemnaker, bulan 27).");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  // (a) Gantt
  H.hdr(s, "(a) Jadwal dan jalur kritis (K4/2026 – K2/2029)", 0.45, 1.25, 6.5, { h: 0.24, fs: 9.5 });
  const q = ["K4 '26", "K1 '27", "K2", "K3", "K4", "K1 '28", "K2", "K3", "K4", "K1 '29", "K2"]; const X0 = 3.15, QW = 0.335, Y0 = 1.52;
  q.forEach((t, i) => H.box(s, t, X0 + i * QW, Y0, QW - 0.02, 0.2, { fs: 6, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.02, margin: 0 }));
  const ph = [["1", "Data PKS dan uji lab 55 °C", 0, 3, C.mid, "9 bln"], ["2.1", "Kuotasi GFS dan genset", 1, 3, C.royal, "6"], ["2.2", "FEED dan HAZOP", 2, 5, C.royal, "9"], ["2.3", "Perizinan (PBG, IUPTLS, PJBL, SLO)", 1, 7, C.royal, "18 bln"], ["2.4", "Kontrak jasa 20 tahun dan utang", 4, 8, C.royal, "12"], ["3", "Pilot 10–20 m³ di PKS (TRL 6)", 3, 8, C.green, "15 bln"], ["4", "Pengadaan, konstruksi, komisioning", 5, 10, C.teal, "15 bln"], ["5", "Demonstrasi TRL 7 lalu replikasi 2–10", 9, 11, C.green, "→"]];
  const RH = 0.215, gy0 = Y0 + 0.23;
  ph.forEach(([w, t, a, b, c, d], i) => { const y = gy0 + i * RH; if (i % 2 === 0) H.rect(s, 0.45, y, 6.5, RH, { fill: C.panel, line: null });
    H.t(s, [{ text: w + "  ", options: { bold: true, color: C.royal } }, { text: t }], 0.5, y, 2.65, RH, { fontSize: 7.4, valign: "middle" });
    H.box(s, d, X0 + a * QW, y + 0.03, (b - a) * QW - 0.02, RH - 0.06, { fs: 6.6, bold: true, color: C.white, fill: c, line: null, radius: 0.03, margin: 0 }); });
  const gb = gy0 + ph.length * RH;
  [[2, "G0"], [5, "G1"], [8, "G2"], [10.5, "G3"]].forEach(([x, t]) => { H.ln(s, X0 + x * QW, Y0 + 0.22, X0 + x * QW, gb + 0.02, { color: C.red, w: 1, dash: "dash", arrow: false }); H.box(s, t, X0 + x * QW - 0.16, gb + 0.02, 0.32, 0.2, { fs: 7.5, bold: true, color: C.white, fill: C.red, line: null, radius: 0.1, margin: 0, font: FONT_H }); });
  H.t(s, [{ text: "Jalur kritis: ", options: { bold: true, color: C.red } }, { text: "kuotasi → FEED → izin → genset → konstruksi" }], 0.5, gb + 0.02, 2.65, 0.2, { fontSize: 7.2, valign: "middle" });
  // (b) risiko
  H.hdr(s, "(b) Peta risiko: sebelum dan sesudah mitigasi", 7.1, 1.25, 5.8, { fill: C.red, h: 0.24, fs: 9.5 });
  img("f_risiko.png", 7.3, 1.52, 5.3, 5.3 * 2.3 / 5.55, "grafik-risiko");
  // (c) KPI dan (d) mitigasi
  const Y2 = 3.76;
  H.hdr(s, "(c) KPI proyek dan target", 0.45, Y2, 6.5, { fill: C.teal, h: 0.22, fs: 9 });
  H.table(s, [["Bidang", "KPI", "Target", "Pengukuran"], ["Teknis", "COD tersisih pada OLR ≥ 8", "≥ 65% (G3)", "analisis lab mingguan"], ["Energi", "Listrik neto per m³ POME", "≥ 40 kWh", "meter genset"], ["Operasi", "Ketersediaan set", "≥ 93%", "SCADA jarak jauh"], ["Komersial", "Fee jasa terkontrak", "≥ USD 1,35/t TBS", "kontrak 20 tahun"], ["Dampak", "tCO₂e dihindari per set", "≥ 30 ribu/tahun", "MRV terverifikasi"]].map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, r[1], { text: r[2], options: { bold: true, color: C.green } }, r[3]]), 0.45, Y2 + 0.24, [0.9, 2.2, 1.4, 2.0], { fs: 7.6, rh: 0.222, hrh: 0.21, margin: [1, 3, 1, 3] });
  H.hdr(s, "(d) Mitigasi risiko dan pemilik", 7.1, Y2, 5.8, { fill: C.red, h: 0.22, fs: 9 });
  H.table(s, [["ID", "Risiko", "Mitigasi", "Pemilik"], ["R1", "Tarif dan izin jual listrik", "konfirmasi ESDM/PLN; kontrak jasa energi", "hukum"], ["R2", "Kinerja termofilik", "pilot G3; jaminan kinerja bertahap", "teknis"], ["R3", "CAPEX melampaui rencana", "tiga kuotasi G1; pesan genset dini", "pengadaan"], ["R4", "Solar PKS di bawah target", "pilih PKS solar ≥ 3,0 L/t di G0", "komersial"], ["R5", "Beban TBS PKS rendah", "klausul beban minimum, fee dasar", "komersial"], ["R6", "Keselamatan gas dan bejana", "HAZOP, SOP, detektor gas, SLO", "K3"]].map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.red, align: "center" } }, r[1], r[2], r[3]]), 7.1, Y2 + 0.24, [0.35, 1.7, 2.7, 1.05], { fs: 7.3, rh: 0.19, hrh: 0.2, margin: [1, 3, 1, 3] });
  // (e) gerbang
  const g = [["G0 · bulan 6 · USD 150 ribu", "Lolos bila PKS mitra solar ≥ 3,0 L/t dan jaringan ≤ 2 km", 1], ["G1 · bulan 15 · USD 340 ribu", "Lolos bila tiga kuotasi mendukung FCI ≤ USD 5,0 juta", 2], ["G2 · bulan 24 · USD 400 ribu", "Lolos bila kontrak fee ≥ USD 1,35/t dan HAZOP bersih", 3], ["G3 · bulan 30 · USD 410 ribu", "Lolos bila pilot COD ≥ 65%, MRV siap → FID", 4]];
  g.forEach(([h, tx, ix], i) => { const x = 0.45 + i * 3.14, w = 3.05, c = ch[ix];
    H.hdr(s, h, x, 5.56, w, { fill: C.red, h: 0.21, fs: 8.2 }); H.rect(s, x, 5.77, w, 0.68, { fill: C.white, line: C.red, radius: 0, lw: 1 });
    H.t(s, tx, x + 0.07, 5.79, w - 0.14, 0.3, { fontSize: 7.8 });
    H.box(s, "Membuka NPV USD " + fmt(c.NPV / 1e6, 2) + " juta · IRR " + fmt(c.IRR * 100, 1) + "%", x + 0.07, 6.14, w - 0.14, 0.25, { fs: 8.3, bold: true, color: C.green, fill: C.greenL, line: null, radius: 0.04 }); });
  H.concl(s, "Dana USD 1,3 juta (usulan) dibelanjakan bertahap per gerbang; modal utama (± USD 4,9 juta) baru keluar setelah kontrak, kuotasi, dan pilot terkunci.", "Kesimpulan");
  H.src(s, "usulan tim; peluang × dampak risiko adalah penilaian tim; durasi izin dari research/R4 dan R6 (SLO ≤ 4 hari kerja setelah inspeksi: FAQ Ditjen Gatrik 2024; lama izin lain perkiraan tim); NPV dan IRR per gerbang dari fin_core.py.", "FEED desain rekayasa awal; HAZOP kajian bahaya dan operabilitas; MRV pemantauan, pelaporan, verifikasi; FID keputusan investasi akhir; OLR laju beban organik; PBG persetujuan bangunan gedung; SLO sertifikat laik operasi; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri; K3 keselamatan dan kesehatan kerja.");
};
