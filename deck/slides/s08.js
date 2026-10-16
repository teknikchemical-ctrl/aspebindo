// Slide 8: Rencana implementasi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H, NF } = L; const gt = D.keu.gates;
  const s = H.slide(8, "Empat gerbang go/no-go dalam ±30 bulan menaikkan {{TRL 4 menjadi 7}} dan peluang NPV positif dari " + fmt(gt[0].p * 100, 0) + "% menjadi " + fmt(gt[4].p * 100, 0) + "%, dengan anggaran USD 1,3 juta",
    "Implementasi. Gantt, WBS, gerbang tahap, RACI, risiko, perizinan, dan anggaran. Peluang NPV positif per gerbang dari Monte Carlo (menyempitkan distribusi solar, CAPEX, rezim tarif, beban, dan fee).");
  // ---- Gantt
  H.hdr(s, "Gantt dan jalur kritis (kuartal 4/2026 – kuartal 2/2029)", 0.45, 1.25, 8.3, { h: 0.25, fs: 9.5 });
  const q = ["K4 '26", "K1 '27", "K2", "K3", "K4", "K1 '28", "K2", "K3", "K4", "K1 '29", "K2"]; const X0 = 3.0, QW = 0.52, Y0 = 1.54;
  q.forEach((t, i) => H.box(s, t, X0 + i * QW, Y0, QW - 0.02, 0.2, { fs: 7, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.02, margin: 0 }));
  const ph = [["1.1", "Data solar dan POME PKS mitra", 0, 2, C.mid, "6 bln"], ["1.2", "Uji laboratorium semikontinu 55 °C", 0, 3, C.mid, "9 bln"], ["2.1", "Kuotasi vendor, FEED, HAZOP", 1, 5, C.royal, "12 bln"], ["2.2", "Perizinan (PBG, SLO, IUPTLS, PJBL, UKL-UPL)", 1, 7, C.royal, "18 bln"],
              ["3.1", "Pilot 10–20 m³ di PKS (TRL 6)", 3, 8, C.green, "15 bln"], ["4.1", "Pengadaan dan fabrikasi (genset 6–9 bln)", 5, 9, C.mid, "12 bln"], ["4.2", "Konstruksi set 1 dan komisioning", 7, 10, C.royal, "9 bln"], ["5.1", "Operasi demonstrasi (TRL 7) dan MRV", 9, 11, C.green, "6 bln"]];
  ph.forEach(([w, t, a, b, c, d], i) => { const y = Y0 + 0.25 + i * 0.24; H.t(s, [{ text: w + "  ", options: { bold: true, color: C.royal } }, { text: t }], 0.45, y, 2.55, 0.25, { fontSize: 7.8, valign: "middle" }); H.box(s, d, X0 + a * QW, y + 0.02, (b - a) * QW - 0.02, 0.19, { fs: 7.3, bold: true, color: C.white, fill: c, line: null, radius: 0.03, margin: 0 }); H.rect(s, X0, y + 0.23, 11 * QW - 0.02, 0.0, { fill: C.line, line: C.line, lw: 0.25 }); });
  const gy = Y0 + 0.25 + 8 * 0.24 + 0.03;
  H.t(s, "Gerbang tahap", 0.45, gy, 2.5, 0.22, { fontSize: 8, bold: true, color: C.red, valign: "middle" });
  [[2, "G0"], [5, "G1"], [8, "G2"], [10.5, "G3"]].forEach(([x, t]) => { H.ln(s, X0 + x * QW, Y0 + 0.22, X0 + x * QW, gy, { color: C.red, w: 0.9, dash: "dash", arrow: false }); H.box(s, t, X0 + x * QW - 0.17, gy, 0.34, 0.22, { fs: 8, bold: true, color: C.white, fill: C.red, line: null, radius: 0.11, margin: 0, font: FONT_H }); });
  H.t(s, "Jalur kritis: kuotasi/FEED → izin PLN dan IUPTLS → genset (6–9 bulan) → konstruksi. WBS: 1 data dan uji · 2 rekayasa dan izin · 3 pilot · 4 pengadaan dan konstruksi · 5 operasi dan MRV.", 0.45, gy + 0.25, 8.3, 0.26, { fontSize: 7.3, color: C.red });
  // ---- anggaran
  H.hdr(s, "Anggaran pengembangan: USD 1,3 juta (usulan)", 8.9, 1.25, 4.0, { fill: C.teal, h: 0.25, fs: 9.5 });
  const bd = [["Uji lab dan pilot", 480, C.green], ["Tim dan manajemen", 310, C.navy], ["FEED dan HAZOP", 220, C.royal], ["Kuotasi dan MRV karbon", 160, C.teal], ["Izin dan hukum", 130, C.mid]];
  s.addChart(pres.charts.DOUGHNUT, [{ name: "USD ribu", labels: bd.map((x) => x[0]), values: bd.map((x) => x[1]) }], { x: 8.85, y: 1.55, w: 1.75, h: 1.75, holeSize: 55, chartColors: bd.map((x) => x[2]), showLegend: false, showPercent: false, showValue: false, dataBorder: { pt: 1, color: "FFFFFF" } });
  H.t(s, "1.300", 9.2, 2.25, 1.05, 0.3, { fontFace: FONT_H, fontSize: 13, bold: true, color: C.navy, align: "center", valign: "middle" });
  bd.forEach(([a, v, c], i) => { const y = 1.68 + i * 0.3; H.rect(s, 10.65, y + 0.04, 0.14, 0.14, { fill: c, line: null }); H.t(s, a, 10.85, y, 1.4, 0.22, { fontSize: 8.2, valign: "middle" }); H.t(s, fmt(v, 0), 12.3, y, 0.55, 0.22, { fontSize: 8.5, bold: true, align: "right", valign: "middle" }); });
  H.t(s, "USD ribu. Status: usulan tim, belum ada komitmen. Sumber prospektif: hibah riset, kontribusi in-kind PKS mitra, investor tahap awal. Mitra yang belum terikat: PKS mitra, EPC, laboratorium universitas, vendor genset dan GFS.", 8.9, 3.32, 4.0, 0.55, { fontSize: 7.6, color: C.slate });
  // ---- kartu gerbang
  const g = [["G0 · Data PKS · bulan 6", ["Solar tergantikan terukur ≥ 2,0 L/t TBS (log 12 bulan)", "Jaringan 20 kV ≤ 2 km; beban TBS ≥ 70%", "Surat minat PKS mitra"]], ["G1 · Kuotasi · bulan 15", ["FCI ≤ USD 6,0 juta (±12%)", "Tiga kuotasi: tangki GFS dan genset", "Perjanjian pendahuluan PKS"]], ["G2 · FEED dan hukum · bulan 24", ["HAZOP tanpa risiko tinggi", "Struktur kontrak dan tarif dikonfirmasi ESDM/PLN", "Penawaran pembiayaan (DSCR ≥ 1,30)"]], ["G3 · Pilot · bulan 30", ["COD ≥ 65% pada OLR ≥ 8; settler ≥ 85%", "H₂S ke genset ≤ 50 ppm", "Kontrak 20 tahun ditandatangani → FID"]]];
  g.forEach(([h, ls], i) => { const x = 0.45 + i * 3.14, w = 3.05; H.hdr(s, h, x, 4.36, w, { fill: C.red, h: 0.22, fs: 8.3 }); H.rect(s, x, 4.58, w, 0.66, { fill: C.white, line: C.red, radius: 0, lw: 1 });
    H.t(s, ls.map((t, j) => ({ text: t, options: { bullet: { indent: 8 }, breakLine: j < 2, paraSpaceAfter: 1 } })), x + 0.07, 4.6, w - 0.14, 0.45, { fontSize: 7.4 });
    H.t(s, "P(NPV>0) setelah lolos: " + fmt(gt[i + 1].p * 100, 0) + "% · gagal: berhenti/ganti PKS", x + 0.07, 5.06, w - 0.14, 0.16, { fontSize: 7.2, bold: true, color: C.red }); });
  // ---- RACI, risiko, perizinan
  const Y3 = 5.3;
  H.hdr(s, "RACI (R pelaksana, A penanggung jawab, C konsultasi)", 0.45, Y3, 3.6, { h: 0.2, fs: 7.8 });
  H.table(s, [["Kegiatan", "Tim", "PKS", "EPC", "Lab"], ["Data dan uji", "A", "R", "I", "R"], ["FEED, HAZOP", "A", "C", "R", "I"], ["Izin ESDM/PLN/KLH", "R", "A", "C", "I"], ["Konstruksi dan operasi", "A", "C", "R", "I"]], 0.45, Y3 + 0.22, [1.6, 0.5, 0.5, 0.5, 0.5], { fs: 7.2, rh: 0.17, align: ["left", "center", "center", "center", "center"], margin: [0.5, 3, 0.5, 3] });
  H.hdr(s, "Risiko utama dan pemilik", 4.2, Y3, 4.4, { h: 0.2, fs: 7.8, fill: C.red });
  H.table(s, [["Risiko", "Peluang · dampak", "Mitigasi (pemilik)"], ["Tarif dan izin jual listrik", "4 · 4", "konfirmasi ESDM, kontrak jasa (hukum)"], ["CAPEX > USD 6 juta", "3 · 4", "tiga kuotasi, desain ke biaya (pengadaan)"], ["Kinerja termofilik", "3 · 5", "pilot dan jaminan bertahap (teknis)"], ["Solar < 1,5 L/t", "3 · 4", "gerbang G0 (komersial)"]], 4.2, Y3 + 0.22, [1.5, 0.85, 2.05], { fs: 7.2, rh: 0.17, align: ["left", "center", "left"], margin: [0.5, 3, 0.5, 3] });
  H.hdr(s, "Perizinan (otoritas)", 8.75, Y3, 4.15, { h: 0.2, fs: 7.8 });
  H.table(s, [["Izin", "Otoritas"], ["PBG/SLF", "pemerintah daerah"], ["UKL-UPL, persetujuan teknis air limbah", "KLH/DLH"], ["IUPTLS/IUPTLU, PJBL, SLO", "ESDM (Gatrik), PLN, LIT"], ["K3 bejana tekan dan listrik; ISPO 2027", "Kemnaker; Komite ISPO"]], 8.75, Y3 + 0.22, [2.5, 1.65], { fs: 7.2, rh: 0.17, margin: [0.5, 3, 0.5, 3] });
  H.concl(s, "Dana pengembangan USD 1,3 juta membeli informasi, bukan aset: tiap gerbang mengubah asumsi terlemah menjadi data, dan modal besar (± USD 5,9 juta) baru dikucurkan setelah G3.", "Kesimpulan");
  H.src(s, "usulan tim; durasi dan kendala dari research/R4 dan R6 (SLO ≤ 4 hari kerja setelah inspeksi, FAQ Ditjen Gatrik 2024; lama izin lain belum terverifikasi); Monte Carlo per gerbang (deck/export_data.py).", "FEED desain rekayasa awal; HAZOP kajian bahaya dan operabilitas; MRV pemantauan, pelaporan, verifikasi; FID keputusan investasi akhir; PBG persetujuan bangunan gedung; SLO sertifikat laik operasi; LIT lembaga inspeksi teknik.");
};
