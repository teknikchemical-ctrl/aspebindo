// Slide 1: Sampul
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H, FONT_B } = L;
  const s = pres.addSlide({ masterName: "SAMPUL", sectionTitle: "Sampul" });
  const k = D.keu, red = D.lca.net_total / D.lca.base;
  H.box(s, "M", 0.55, 0.45, 0.5, 0.5, { fs: 20, bold: true, color: C.white, fill: C.navy, line: null, radius: 0.08, font: FONT_H, margin: 0 });
  H.t(s, "MALATAXTAX", 1.15, 0.45, 3, 0.26, { fontFace: FONT_H, fontSize: 12, bold: true, color: C.navy, valign: "middle" });
  H.t(s, "Energy Business Plan Competition  ·  EIC 2026", 1.15, 0.71, 4.5, 0.22, { fontSize: 9, color: C.slate, valign: "middle" });
  H.t(s, "Subtema 3: Ekonomi Sirkular dan Solusi Lingkungan untuk Transisi Energi", 0.55, 1.2, 5.6, 0.22, { fontSize: 9.5, bold: true, color: C.green, valign: "middle" });
  H.t(s, [{ text: "Biogas sebagai Layanan: ", options: { color: C.navy } }, { text: "pengolah POME termofilik modular untuk pabrik kelapa sawit", options: { color: C.teal } }], 0.55, 1.5, 5.6, 1.95, { fontFace: FONT_H, fontSize: 25, bold: true });
  H.t(s, "Air limbah pabrik kelapa sawit (palm oil mill effluent, POME) diubah menjadi listrik pengganti solar, listrik jaringan, dan kredit karbon. Pabrik membayar per ton tandan buah segar (TBS) tanpa modal: set biogas dibangun, dimiliki, dan dioperasikan oleh kami (BOO), dan dapat dipindahkan.", 0.55, 3.55, 5.6, 1.05, { fontSize: 11, color: C.ink });
  const kp = [["−" + fmt(red * 100, 0) + "%", "emisi metana kolam POME dihindari: ≈ " + fmt(D.lca.net_total / 1000, 0) + " ribu tCO₂e per tahun per set 60 t TBS/jam"], ["USD 0", "modal yang dikeluarkan pabrik (skema BOO)"], [fmt(k.E_net, 1) + " GWh", "listrik neto per tahun per set"]];
  kp.forEach(([b, t], i) => H.kpi(s, b, t, 0.55 + i * 1.93, 4.75, 1.83, 1.2, { bs: 18, ls: 8 }));
  H.t(s, [{ text: "Tim Malataxtax", options: { bold: true, color: C.navy, fontSize: 11, breakLine: true } }, { text: "Anggota: [Nama lengkap 1] · [Nama lengkap 2] · [Nama lengkap 3]", options: { breakLine: true } }, { text: "Perguruan tinggi: [Nama perguruan tinggi]" }], 0.55, 6.15, 5.6, 0.7, { fontSize: 9 });
  H.t(s, "Identitas dalam kurung siku diisi sesuai buku panduan sebelum pengumpulan.", 0.55, 6.95, 5.6, 0.2, { fontSize: 7, italic: true, color: C.slate });
  // gambar utama
  const X0 = 6.45, Y0 = 0.45, W0 = 6.5, H0 = W0 * 9 / 16;
  H.rect(s, X0 - 0.05, Y0 - 0.05, W0 + 0.1, H0 + 0.1, { fill: C.white, line: C.teal, radius: 0.04, lw: 1.5 });
  s.addImage({ path: L.ROOT + "/cad/out/render/DIORAMA_lokasi.png", x: X0, y: Y0, w: W0, h: H0, objectName: "render-lokasi" });
  const mk = (n, px, py) => H.box(s, String(n), X0 + px * W0 / 1280 - 0.12, Y0 + py * H0 / 720 - 0.12, 0.24, 0.24, { fs: 9, bold: true, color: C.white, fill: C.royal, line: C.white, lw: 1.25, radius: 0.12, margin: 0, font: FONT_H });
  mk(1, 640, 203); mk(2, 612, 340); mk(3, 553, 190); mk(4, 965, 287); mk(5, 835, 342);
  const IY = Y0 + H0 + 0.25, IW = 3.4, IH = IW * 9 / 16;
  H.hdr(s, "Titik integrasi dengan PKS", X0, IY, 3.0, { h: 0.25, fs: 9 });
  ["POME 85 °C dari fat pit ke praolah", "Set biogas di bekas kolam, 0,38 ha", "Listrik ke rumah mesin PKS dan jaringan PLN", "Efluen ke kolam polishing, lalu aplikasi lahan", "Kolam anaerobik lama (±1,1 ha) dibebaskan"].forEach((t, i) => {
    const y = IY + 0.33 + i * 0.36;
    H.box(s, String(i + 1), X0, y + 0.02, 0.22, 0.22, { fs: 8.5, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.11, margin: 0, font: FONT_H });
    H.t(s, t, X0 + 0.3, y, 2.7, 0.3, { fontSize: 9, valign: "middle" });
  });
  H.rect(s, X0 + W0 - IW - 0.05, IY - 0.05, IW + 0.1, IH + 0.1, { fill: C.white, line: C.teal, radius: 0.04, lw: 1.25 });
  s.addImage({ path: L.ROOT + "/cad/out/render/DIORAMA_produk.png", x: X0 + W0 - IW, y: IY, w: IW, h: IH, objectName: "render-produk" });
  H.t(s, "Model 3D (CadQuery) dari neraca proses dan model lokasi tim. Modul acuan 45 t TBS/jam; konfigurasi komersial 60 t TBS/jam menambah satu modul identik.", X0, 7.1, W0, 0.3, { fontSize: 7, italic: true, color: C.slate });
  s.addNotes("Sampul. Satu klaim terukur: satu set 60 t TBS/jam menghindari ≈ " + fmt(D.lca.net_total, 0) + " tCO2e per tahun (−" + fmt(red * 100, 0) + "% dari kolam terbuka; AMS-III.H, UF 0,89, GWP 28) tanpa modal pabrik.");
};
