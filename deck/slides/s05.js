// Slide 5: Desain produk (gambar rekayasa)
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const p = D.proses; const IM = (f) => L.ROOT + "/deck/img/" + f;
  const s = H.slide(5, "Desain produk: {{PFD, tata letak, model 3D, dan sembilan lembar gambar rekayasa}} menunjukkan set yang dirancang rinci, bukan sekadar konsep",
    "Desain produk. Semua gambar dihasilkan dari model parametrik yang sama dengan neraca proses (pfd/, cad/). Modul acuan 45 t TBS/jam: 3 reaktor GFS, 2 genset 600 kWe, plot 99,65 × 37,7 m.");
  // ---- kiri: PFD besar
  H.hdr(s, "① Diagram alir proses (PFD BG-002 Rev 3): dibaca dari kiri ke kanan", 0.45, 1.25, 7.4, { h: 0.25, fs: 9.5 });
  H.rect(s, 0.45, 1.5, 7.4, 4.22, { fill: C.white, line: C.line, radius: 0 });
  H.imgFit(s, IM("pfd_crop.png"), 3473, 1960, 0.47, 1.52, 7.36, 4.18);
  H.t(s, "A-100 praolah · A-200 reaktor kontak · A-300 degasser, settler, lumpur · A-400 pemurnian dan penampung gas · A-500 genset dan pemulih panas · A-600 menara pendingin. Tag, nomor aliran 1–26, suhu, tekanan, dan laju massa tertera pada lembar A2 (PDF dapat diperbesar).", 0.45, 5.76, 7.4, 0.4, { fontSize: 7.8, color: C.slate });
  H.box(s, "Sembilan lembar gambar rekayasa A3 (tata letak, elevasi, skid, lokasi) menyertai PFD", 0.45, 6.12, 7.4, 0.3, { fs: 8.4, bold: true, color: C.navy, fill: C.tealL, line: C.teal, radius: 0.04 });
  // ---- kanan
  const RX = 8.0, RW = 4.9;
  H.hdr(s, "② Tata letak plot 1:400: 99,65 × 37,7 m = 0,38 ha", RX, 1.25, RW, { fill: C.teal, h: 0.25, fs: 9 });
  H.rect(s, RX, 1.5, RW, 1.72, { fill: C.white, line: C.line, radius: 0 }); H.imgFit(s, IM("plan_ga.png"), 2400, 830, RX + 0.02, 1.52, RW - 0.04, 1.68);
  [["③ Model 3D set lengkap", L.ROOT + "/cad/out/render/PLANT_iso-depan.png", [2200, 1400]], ["④ Reaktor GFS: Ø11,5 × 10,8 m", IM("v201.png"), [1488, 1088]]].forEach(([t, f, px], i) => {
    const x = RX + i * 2.5; H.hdr(s, t, x, 3.29, 2.4, { fill: C.teal, h: 0.22, fs: 8 }); H.rect(s, x, 3.51, 2.4, 1.5, { fill: C.white, line: C.line, radius: 0 }); H.imgFit(s, f, px[0], px[1], x + 0.02, 3.53, 2.36, 1.46);
  });
  H.hdr(s, "Peralatan utama modul acuan 45 t TBS/jam", RX, 5.08, RW, { fill: C.navy, h: 0.22, fs: 8.4 });
  H.table(s, [["Tag", "Uraian", "Kapasitas"], ["R-201…203", "reaktor kontak GFS, 55 °C", "3 × 980 m³"], ["DG-301 · LS-301", "degasser vakum · settler lamella", "8 m³ · 81 m²"], ["GH-301 · FL-301", "penampung gas · flare tertutup", "986 m³ (2 jam)"], ["GE-401/402", "genset biogas kontainer 40 ft", "2 × 600 kWe"]], RX, 5.3, [1.2, 2.3, 1.4], { fs: 7.6, rh: 0.2, hrh: 0.2, margin: [1, 3, 1, 3] });
  H.concl(s, "Rancangan lengkap: PFD, tata letak dengan jarak aman terverifikasi, model 3D, dan gambar unit; skala 60 t TBS/jam menambah satu reaktor identik dan tangki ekualisasi.", "Kesimpulan");
  H.src(s, "pfd/outputs/PFD_BG-002_Rev3.pdf; cad/drawings/out/BG_drawing_set_A3.pdf (9 lembar, pemeriksa tabrakan teks: 0 temuan); model CadQuery tim.", "PFD diagram alir proses; GFS baja berlapis kaca; PM modul portabel; DG degasser; LS settler lamella; ISO/ISA standar simbol.");
};
