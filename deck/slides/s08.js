// Slide 8: Rencana implementasi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const gt = D.keu.gates;
  const s = H.slide(8, "Kami tidak langsung membangun: {{empat gerbang go/no-go}} dalam 30 bulan menaikkan peluang NPV positif dari " + fmt(gt[0].p * 100, 0) + "% menjadi " + fmt(gt[4].p * 100, 0) + "%, dengan dana USD 1,3 juta",
    "Implementasi. Gantt, gerbang tahap, anggaran, dan peluang NPV positif per gerbang (Monte Carlo menyempitkan distribusi solar, CAPEX, rezim tarif, beban, dan fee). Jalur kritis: kuotasi/FEED, izin PLN dan IUPTLS, genset (6-9 bulan), konstruksi. Perizinan: PBG/SLF (pemda); UKL-UPL dan persetujuan teknis air limbah (KLH/DLH); IUPTLS/IUPTLU, PJBL, SLO (ESDM, PLN, LIT); K3 bejana tekan (Kemnaker). Risiko utama: tarif dan izin jual listrik (hukum), CAPEX di atas USD 6 juta (pengadaan), kinerja termofilik (teknis), solar di bawah 1,5 L/t (komersial). RACI: tim A untuk data, FEED, konstruksi; PKS A untuk izin lahan; EPC R untuk FEED dan konstruksi; laboratorium R untuk uji.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  // ---- Gantt
  H.hdr(s, "Jadwal dan jalur kritis (kuartal 4/2026 – kuartal 2/2029)", 0.45, 1.25, 7.95, { h: 0.24, fs: 9.5 });
  const q = ["K4 '26", "K1 '27", "K2", "K3", "K4", "K1 '28", "K2", "K3", "K4", "K1 '29", "K2"]; const X0 = 3.45, QW = 0.45, Y0 = 1.54;
  q.forEach((t, i) => H.box(s, t, X0 + i * QW, Y0, QW - 0.02, 0.2, { fs: 6.8, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.02, margin: 0 }));
  const ph = [["Data solar dan POME PKS mitra", 0, 2, C.mid, "6 bln"], ["Uji lab semikontinu 55 °C", 0, 3, C.mid, "9 bln"], ["Kuotasi vendor, FEED, HAZOP", 1, 5, C.royal, "12 bln"], ["Perizinan: PBG, SLO, IUPTLS, PJBL", 1, 7, C.royal, "18 bln"], ["Pilot 10–20 m³ di PKS (TRL 6)", 3, 8, C.green, "15 bln"], ["Pengadaan dan fabrikasi", 5, 9, C.mid, "12 bln"], ["Konstruksi set 1 dan komisioning", 7, 10, C.royal, "9 bln"], ["Operasi demonstrasi (TRL 7) + MRV", 9, 11, C.green, "6 bln"]];
  const RH = 0.3, gy0 = Y0 + 0.26;
  ph.forEach(([t, a, b, c, d], i) => { const y = gy0 + i * RH; if (i % 2 === 0) H.rect(s, 0.45, y, 7.95, RH, { fill: C.panel, line: null });
    H.t(s, [{ text: (Math.floor(i / 2) + 1) + "." + (i % 2 + 1) + "  ", options: { bold: true, color: C.royal } }, { text: t }], 0.52, y, 2.9, RH, { fontSize: 8.3, valign: "middle" });
    H.box(s, d, X0 + a * QW, y + 0.05, (b - a) * QW - 0.02, RH - 0.1, { fs: 7.6, bold: true, color: C.white, fill: c, line: null, radius: 0.03, margin: 0 }); });
  const gb = gy0 + ph.length * RH;
  [[2, "G0"], [5, "G1"], [8, "G2"], [10.5, "G3"]].forEach(([x, t]) => { H.ln(s, X0 + x * QW, Y0 + 0.22, X0 + x * QW, gb + 0.02, { color: C.red, w: 1, dash: "dash", arrow: false }); H.box(s, t, X0 + x * QW - 0.17, gb + 0.02, 0.34, 0.22, { fs: 8, bold: true, color: C.white, fill: C.red, line: null, radius: 0.11, margin: 0, font: FONT_H }); });
  H.t(s, [{ text: "Jalur kritis: ", options: { bold: true, color: C.red } }, { text: "kuotasi dan FEED → izin PLN dan IUPTLS → genset (6–9 bulan) → konstruksi. Gerbang merah = titik berhenti atau lanjut." }], 0.5, gb + 0.3, 7.9, 0.22, { fontSize: 8, valign: "middle" });
  // ---- kanan
  H.hdr(s, "Peluang NPV positif naik di setiap gerbang", 8.55, 1.25, 4.35, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_gerbang.png", 8.5, 1.52, 4.4, 1.5, "grafik-gerbang");
  H.hdr(s, "Anggaran pengembangan USD 1,3 juta (usulan)", 8.55, 3.1, 4.35, { h: 0.24, fs: 9.5 });
  img("f_anggaran.png", 8.5, 3.37, 4.4, 1.5, "grafik-anggaran");
  // ---- kartu gerbang
  const g = [["G0 · Data PKS · bulan 6", ["Solar tergantikan terukur ≥ 2,0 L/t TBS (log 12 bulan)", "Jaringan 20 kV ≤ 2 km, beban TBS ≥ 70%", "Surat minat PKS mitra"]], ["G1 · Kuotasi · bulan 15", ["FCI ≤ USD 6,0 juta (±12%)", "Tiga kuotasi: tangki GFS dan genset", "Perjanjian pendahuluan dengan PKS"]], ["G2 · FEED dan hukum · bulan 24", ["HAZOP tanpa risiko tinggi", "Struktur kontrak dan tarif dikonfirmasi ESDM/PLN", "Penawaran pembiayaan dengan DSCR ≥ 1,30"]], ["G3 · Pilot · bulan 30", ["COD ≥ 65% pada OLR ≥ 8; settler ≥ 85%", "H₂S ke genset ≤ 50 ppm", "Kontrak 20 tahun ditandatangani → FID"]]];
  g.forEach(([h, ls], i) => { const x = 0.45 + i * 3.14, w = 3.05;
    H.hdr(s, h, x, 4.97, w, { fill: C.red, h: 0.25, fs: 8.8 }); H.rect(s, x, 5.22, w, 1.2, { fill: C.white, line: C.red, radius: 0, lw: 1 });
    H.t(s, ls.map((t, j) => ({ text: t, options: { bullet: { indent: 9 }, breakLine: j < 2, paraSpaceAfter: 2 } })), x + 0.08, 5.27, w - 0.16, 0.78, { fontSize: 8.4 });
    H.box(s, "Lolos → peluang NPV > 0: " + fmt(gt[i + 1].p * 100, 0) + "%", x + 0.08, 6.1, w - 0.16, 0.26, { fs: 8.4, bold: true, color: C.red, fill: C.redL, line: null, radius: 0.04 }); });
  H.concl(s, "Dana USD 1,3 juta membeli kepastian, bukan aset: tiap gerbang mengubah asumsi terlemah menjadi data, dan modal besar (± USD 5,9 juta) baru keluar setelah G3.", "Kesimpulan");
  H.src(s, "usulan tim; durasi izin dari research/R4 dan R6 (SLO ≤ 4 hari kerja setelah inspeksi: FAQ Ditjen Gatrik 2024; lama izin lain belum terverifikasi); Monte Carlo per gerbang (deck/export_data.py). Anggaran belum berkomitmen.", "FEED desain rekayasa awal; HAZOP kajian bahaya dan operabilitas; MRV pemantauan, pelaporan, verifikasi; FID keputusan investasi akhir; PBG persetujuan bangunan gedung; SLO sertifikat laik operasi; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri.");
};
