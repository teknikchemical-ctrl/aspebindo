// Slide 1: Sampul
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H, FONT_B } = L;
  const s = pres.addSlide({ masterName: "SAMPUL", sectionTitle: "Sampul" });
  const k = D.keu, lc = D.lca, red = lc.net_total / lc.base;
  s.addImage({ path: L.ROOT + "/deck/img/cover_bg.png", x: 0, y: 0, w: 13.333, h: 7.5, objectName: "latar-sampul" });
  // marka
  H.box(s, "M", 0.55, 0.45, 0.5, 0.5, { fs: 20, bold: true, color: C.navy, fill: C.white, line: null, radius: 0.08, font: FONT_H, margin: 0 });
  H.t(s, "MALATAXTAX", 1.15, 0.45, 3, 0.26, { fontFace: FONT_H, fontSize: 12, bold: true, color: C.white, valign: "middle" });
  H.t(s, "Energy Business Plan Competition · EIC 2026", 1.15, 0.71, 4.5, 0.22, { fontSize: 9, color: "BFD6E8", valign: "middle" });
  H.box(s, "SUBTEMA 3 · EKONOMI SIRKULAR DAN SOLUSI LINGKUNGAN", 0.55, 1.3, 4.65, 0.28, { fs: 8.5, bold: true, color: C.navy, fill: C.lime, line: null, radius: 0.14, font: FONT_H, margin: 0 });
  // judul
  H.t(s, [{ text: "Dari kolam limbah", options: { color: C.white, breakLine: true } }, { text: "menjadi pembangkit listrik", options: { color: "7FD3F2" } }], 0.55, 1.75, 6.6, 1.5, { fontFace: FONT_H, fontSize: 30, bold: true, valign: "top" });
  H.t(s, "Biogas sebagai Layanan: pengolah POME termofilik modular untuk pabrik kelapa sawit", 0.55, 3.2, 5.6, 0.62, { fontFace: FONT_H, fontSize: 13, color: C.white });
  H.t(s, "Setiap tahun, satu pabrik sawit besar melepas ±" + fmt(lc.base / 1000, 0) + " ribu ton CO₂e metana dari kolam limbahnya. Kami menangkap gas itu, mengubahnya menjadi listrik, dan membiarkan pabrik membayar per ton buah yang diolah, tanpa mengeluarkan modal.", 0.55, 3.95, 5.5, 1.0, { fontSize: 11.5, color: "DCEAF5" });
  // KPI
  const kp = [["−" + fmt(red * 100, 0) + "%", "emisi metana kolam POME dihindari"], ["USD 0", "modal dari pabrik (skema BOO)"], [fmt(k.E_net, 1) + " GWh", "listrik neto per tahun per set"]];
  kp.forEach(([b, t], i) => { const x = 0.55 + i * 1.95; H.rect(s, x, 5.2, 1.85, 1.1, { fill: C.white, line: null, radius: 0.06, tr: 8 });
    H.t(s, b, x + 0.05, 5.26, 1.75, 0.5, { fontFace: FONT_H, fontSize: 20, bold: true, color: C.navy, align: "center", valign: "middle" }); H.t(s, t, x + 0.1, 5.8, 1.65, 0.45, { fontSize: 8.5, color: C.slate, align: "center" }); });
  // tim
  H.t(s, [{ text: "Tim Malataxtax", options: { bold: true, color: C.white, fontSize: 11, breakLine: true } }, { text: "[Nama lengkap 1] · [Nama lengkap 2] · [Nama lengkap 3]  |  [Nama perguruan tinggi]", options: { color: "BFD6E8" } }], 0.55, 6.55, 7.2, 0.5, { fontSize: 9 });
  // penanda pada gambar (pergeseran gambar +420/2667 lebar)
  const mx = (px) => ((px / 1280 * 2667 + 900) / 2667) * 13.333, my = (py) => py / 720 * 7.5;
  [[1, 640, 203], [2, 612, 340], [3, 553, 190], [4, 965, 287], [5, 835, 342]].forEach(([n, px, py]) => H.box(s, String(n), mx(px) - 0.12, my(py) - 0.12, 0.24, 0.24, { fs: 9, bold: true, color: C.white, fill: C.royal, line: C.white, lw: 1.25, radius: 0.12, margin: 0, font: FONT_H }));
  // legenda integrasi
  H.rect(s, 8.15, 0.25, 4.75, 1.65, { fill: C.white, line: null, radius: 0.05, tr: 10 });
  H.t(s, "Titik integrasi dengan PKS", 8.3, 0.3, 4.4, 0.24, { fontFace: FONT_H, fontSize: 9.5, bold: true, color: C.navy });
  ["POME 85 °C dari fat pit ke praolah", "Set biogas di bekas kolam, 0,38 ha", "Listrik ke rumah mesin PKS dan jaringan PLN", "Efluen ke kolam polishing", "Kolam anaerobik lama (±1,1 ha) dibebaskan"].forEach((t, i) => {
    const y = 0.6 + i * 0.25; H.box(s, String(i + 1), 8.3, y + 0.02, 0.2, 0.2, { fs: 8, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.1, margin: 0, font: FONT_H }); H.t(s, t, 8.6, y, 4.2, 0.24, { fontSize: 9, valign: "middle" }); });
  // inset produk
  const IW = 3.6, IH = IW * 9 / 16, IX = 12.9 - IW, IY = 7.1 - IH;
  H.rect(s, IX - 0.05, IY - 0.05, IW + 0.1, IH + 0.1, { fill: C.white, line: null, radius: 0.04 });
  s.addImage({ path: L.ROOT + "/cad/out/render/DIORAMA_produk_raw.png", x: IX, y: IY, w: IW, h: IH, objectName: "render-produk" });
  H.box(s, "Set biogas modular, dapat dipindahkan", IX, IY + IH - 0.28, IW, 0.28, { fs: 8.5, bold: true, color: C.white, fill: C.navy, line: null, radius: 0, tr: 15 });
  s.addNotes("Sampul. Satu set 60 t TBS/jam menghindari ≈ " + fmt(lc.net_total, 0) + " tCO2e per tahun (−" + fmt(red * 100, 0) + "% dari kolam terbuka; AMS-III.H, UF 0,89, GWP 28) tanpa modal pabrik. Model 3D (CadQuery) dari neraca proses; modul acuan 45 t TBS/jam, konfigurasi komersial 60 t TBS/jam.");
};
