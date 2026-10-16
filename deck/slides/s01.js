// Slide 1: Sampul
module.exports = (pres, H, L) => {
  const { C, D, fmt, pct, FONT_H, FONT_B } = L;
  const s = pres.addSlide({ masterName: "SAMPUL", sectionTitle: "Sampul" });
  const k = D.keu, m = D.meta;
  H.t(s, "ENERGY INNOVATION STRATEGY COMPETITION 2026", 0.55, 0.42, 4.9, 0.2, { fontFace: FONT_H, fontSize: 9, bold: true, color: C.greenD, valign: "middle" });
  H.t(s, "Energy Business Plan Competition  ·  Subtema 3: Ekonomi Sirkular dan Solusi Lingkungan untuk Transisi Energi", 0.55, 0.64, 4.75, 0.34, { fontSize: 8.5, color: C.slate });
  H.t(s, "Biogas sebagai Layanan: Pengolah POME Termofilik Modular untuk Pabrik Kelapa Sawit", 0.55, 1.05, 4.75, 2.05, { fontFace: FONT_H, fontSize: 26, bold: true, color: C.navy });
  H.t(s, "Mengubah air limbah pabrik kelapa sawit (palm oil mill effluent, POME) menjadi listrik pengganti solar, listrik jaringan, dan kredit karbon. Pabrik membayar per ton tandan buah segar (TBS) dan tidak mengeluarkan modal: set dibangun, dimiliki, dan dioperasikan oleh kami (BOO) serta dapat dipindahkan.",
    0.55, 3.2, 4.75, 1.15, { fontSize: 10.5, color: C.ink });
  // KPI
  H.rect(s, 0.55, 4.5, 4.75, 1.55, { fill: C.white, line: C.line, radius: 0.06 });
  H.t(s, "−" + fmt((1 - (D.lca.net_total ? (D.lca.base - D.lca.net_total) / D.lca.base : 0)) * 0 + (D.lca.net_total / D.lca.base) * 100, 0) + "%", 0.7, 4.55, 1.9, 0.8, { fontFace: FONT_H, fontSize: 38, bold: true, color: C.greenD, valign: "middle" });
  H.t(s, "emisi metana kolam POME dihindari: ≈ " + fmt(D.lca.net_total / 1000, 0) + " ribu tCO₂e per tahun untuk satu set 60 t TBS/jam", 2.65, 4.6, 2.55, 0.75, { fontSize: 9.5, bold: true, color: C.navy, valign: "middle" });
  H.ln(s, 0.7, 5.42, 5.15, 5.42, { color: C.line, arrow: false, w: 0.75 });
  H.t(s, [{ text: "USD 0", options: { bold: true, color: C.royal, fontSize: 13, fontFace: FONT_H, breakLine: true } }, { text: "modal dari pabrik (skema BOO)", options: { fontSize: 8, color: C.slate } }], 0.7, 5.5, 2.1, 0.5, {});
  H.t(s, [{ text: fmt(k.E_net, 1) + " GWh", options: { bold: true, color: C.royal, fontSize: 13, fontFace: FONT_H, breakLine: true } }, { text: "listrik neto per tahun per set", options: { fontSize: 8, color: C.slate } }], 2.85, 5.5, 2.4, 0.5, {});
  // tim
  H.t(s, "TIM MALATAXTAX", 0.55, 6.3, 4.75, 0.3, { fontFace: FONT_H, fontSize: 15, bold: true, color: C.navy, valign: "middle" });
  H.t(s, "Anggota: [Nama lengkap 1]  ·  [Nama lengkap 2]  ·  [Nama lengkap 3]", 0.55, 6.62, 4.75, 0.2, { fontSize: 8.5, color: C.ink, valign: "middle" });
  H.t(s, "Perguruan tinggi: [Nama perguruan tinggi]", 0.55, 6.82, 4.75, 0.2, { fontSize: 8.5, color: C.ink, valign: "middle" });
  H.t(s, "Identitas dalam tanda kurung siku wajib diisi sesuai buku panduan sebelum pengumpulan.", 0.55, 7.04, 4.75, 0.18, { fontSize: 6.5, italic: true, color: C.slate, valign: "middle" });
  // render 3D utama: PKS lengkap + set biogas
  const X0 = 5.55, Y0 = 0.45, W0 = 7.4, H0 = W0 * 9 / 16;
  H.rect(s, X0 - 0.04, Y0 - 0.04, W0 + 0.08, H0 + 0.08, { fill: C.white, line: C.line, radius: 0.04 });
  H.img(s, "cad/out/render/DIORAMA_lokasi.png", X0, Y0, W0, H0);
  const mark = (n, px, py) => {
    const x = X0 + px * W0 / 1280 - 0.12, y = Y0 + py * H0 / 720 - 0.12;
    H.box(s, String(n), x, y, 0.24, 0.24, { fs: 8.5, bold: true, color: C.white, fill: C.royal, line: C.white, lw: 1.25, radius: 0.12, margin: 0, font: FONT_H });
  };
  mark(1, 640, 203); mark(2, 612, 340); mark(3, 553, 190); mark(4, 965, 287); mark(5, 835, 342);
  // inset produk
  const IX = 9.0, IY = Y0 + H0 + 0.2, IW = 3.95, IH = IW * 9 / 16;
  H.rect(s, IX - 0.04, IY - 0.04, IW + 0.08, IH + 0.08, { fill: C.white, line: C.line, radius: 0.04 });
  H.img(s, "cad/out/render/DIORAMA_produk.png", IX, IY, IW, IH);
  H.t(s, "Set biogas dari dekat: 3 tangki GFS, degasser + settler, genset, penampung gas, flare", IX, IY + IH + 0.08, IW, 0.2, { fontSize: 6.5, color: C.slate, italic: true });
  // titik integrasi
  H.t(s, "Titik integrasi dengan PKS (angka pada gambar)", 5.55, IY - 0.03, 3.35, 0.2, { fontFace: FONT_H, fontSize: 8.5, bold: true, color: C.navy, valign: "middle" });
  const items = ["POME panas 85 °C dari fat pit masuk praolah (pipa DN150)", "Set biogas di lahan bekas kolam, 0,38 ha (modul acuan 45 t TBS/jam)", "Listrik 400 V/20 kV ke rumah mesin PKS (menggantikan solar) dan ke jaringan PLN",
    "Efluen settler ke kolam polishing yang sudah ada, lalu aplikasi lahan", "Kolam anaerobik lama (±1,1 ha) dibebaskan; kue lumpur ke kebun"];
  items.forEach((t, i) => {
    const yy = IY + 0.25 + i * 0.37;
    H.box(s, String(i + 1), 5.55, yy + 0.02, 0.2, 0.2, { fs: 7.5, bold: true, color: C.white, fill: C.royal, line: C.royal, radius: 0.1, margin: 0, font: FONT_H });
    H.t(s, t, 5.85, yy, 3.05, 0.36, { fontSize: 7.5, color: C.ink });
  });
  H.t(s, "Model 3D (CadQuery, three.js) dibangun dari neraca proses dan model lokasi tim. Modul acuan 45 t TBS/jam; konfigurasi komersial 60 t TBS/jam menambah satu modul identik.", 5.55, 7.08, 3.35, 0.3, { fontSize: 6.3, color: C.slate });
  s.addNotes("Sampul. Satu klaim terukur: satu set 60 t TBS/jam menghindari ≈ " + fmt(D.lca.net_total, 0) + " tCO2e per tahun (−96% dari kolam terbuka, AMS-III.H, UF 0,89, GWP 28) tanpa modal dari pabrik. Gambar 3D adalah modul acuan 45 t TBS/jam; angka keuangan memakai 60 t TBS/jam dengan tangki ekualisasi (lihat slide 7).");
};
