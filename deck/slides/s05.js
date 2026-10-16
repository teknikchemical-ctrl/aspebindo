// Slide 5: Desain produk (gambar rekayasa)
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const p = D.proses; const IM = (f) => L.ROOT + "/deck/img/" + f;
  const s = H.slide(5, "Desain produk: {{PFD, tata letak, model 3D, dan sembilan lembar gambar rekayasa}} menunjukkan set yang dirancang rinci, bukan sekadar konsep",
    "Desain produk. Semua gambar dihasilkan dari model parametrik yang sama dengan neraca proses (pfd/, cad/). Modul acuan 45 t TBS/jam: 3 reaktor GFS, 2 genset 600 kWe, plot 99,65 × 37,7 m.");
  // ---- kiri: PFD + dua gambar unit
  H.hdr(s, "① Diagram alir proses (PFD BG-002 Rev 3): dibaca dari kiri ke kanan", 0.45, 1.25, 6.25, { h: 0.25, fs: 9.5 });
  H.rect(s, 0.45, 1.5, 6.25, 3.4, { fill: C.white, line: C.line, radius: 0 });
  H.imgFit(s, IM("pfd_crop.png"), 3473, 1960, 0.47, 1.52, 6.21, 3.36);
  H.t(s, "A-100 praolah · A-200 reaktor kontak · A-300 degasser, settler, lumpur · A-400 pemurnian dan penampung gas · A-500 genset dan pemulih panas · A-600 menara pendingin. Tag, nomor aliran 1–26, suhu, tekanan, dan laju massa tertera pada lembar A2.", 0.45, 4.93, 6.25, 0.3, { fontSize: 7.5, color: C.slate });
  [["⑤ Reaktor GFS (BG-V-201): Ø11,5 × 10,8 m, 980 m³", "v201.png", [1488, 1088]], ["⑥ Skid kontak (BG-M-004): degasser + lamella", "m004.png", [1588, 1310]]].forEach(([t, f, px], i) => {
    const x = 0.45 + i * 3.15; H.hdr(s, t, x, 5.27, 3.1, { fill: C.teal, h: 0.22, fs: 7.5 }); H.rect(s, x, 5.49, 3.1, 0.99, { fill: C.white, line: C.line, radius: 0 }); H.imgFit(s, IM(f), px[0], px[1], x + 0.02, 5.5, 3.06, 0.97);
  });
  // ---- kanan: tata letak, 3D, lokasi, daftar peralatan
  const RX = 6.85, RW = 6.05;
  H.hdr(s, "② Tata letak plot 1:400 (BG-GA-001): 99,65 × 37,7 m = 0,38 ha", RX, 1.25, RW, { fill: C.teal, h: 0.25, fs: 9 });
  H.rect(s, RX, 1.5, RW, 2.05, { fill: C.white, line: C.line, radius: 0 }); H.imgFit(s, IM("plan_ga.png"), 2400, 830, RX + 0.02, 1.52, RW - 0.04, 2.01);
  [["③ Model 3D set lengkap", L.ROOT + "/cad/out/render/PLANT_iso-depan.png", [2200, 1400]], ["④ Lokasi di PKS 1:1750 (BG-GA-002)", IM("ga002.png"), [1800, 715]]].forEach(([t, f, px], i) => {
    const x = RX + i * 3.05; H.hdr(s, t, x, 3.62, 3.0, { fill: C.teal, h: 0.22, fs: 8 }); H.rect(s, x, 3.84, 3.0, 1.4, { fill: C.white, line: C.line, radius: 0 }); H.imgFit(s, f, px[0], px[1], x + 0.02, 3.86, 2.96, 1.36);
  });
  H.hdr(s, "Peralatan utama modul acuan 45 t TBS/jam (dari PFD dan daftar bagian)", RX, 5.3, RW, { fill: C.navy, h: 0.22, fs: 8 });
  H.table(s, [["Tag", "Uraian", "Ukuran / kapasitas"], ["R-201…203", "reaktor kontak GFS dibaut, 55 °C", "Ø11,46 × 10,8 m; 3 × 980 m³"], ["DG-301 · LS-301", "degasser vakum · settler lamella 60°", "8 m³ · 81 m² proyeksi"], ["GH-301 · FL-301", "penampung gas membran ganda · flare tertutup", "986 m³ (2 jam) · ≥ 15 m dari GH"], ["BTF-301 · AC-301", "bio-scrubber H₂S · karbon aktif penjaga", "2.868 → 21 ppm H₂S"], ["GE-401/402", "genset biogas kontainer 40 ft", "2 × 600 kWe; η 39,3%"]], RX, 5.53, [1.2, 2.85, 2.0], { fs: 7.3, rh: 0.158, head: 1, hrh: 0.17, margin: [0.5, 4, 0.5, 4] });
  H.concl(s, "Rancangan sudah mencakup PFD, tata letak dengan jarak aman terverifikasi, model 3D, dan gambar unit utama; skala komersial 60 t TBS/jam menambahkan satu reaktor identik dan tangki ekualisasi 24 jam pada desain yang sama.", "Kesimpulan");
  H.src(s, "pfd/outputs/PFD_BG-002_Rev3.pdf; cad/drawings/out/BG_drawing_set_A3.pdf (9 lembar, pemeriksa tabrakan teks: 0 temuan); model CadQuery tim.", "PFD diagram alir proses; GFS baja berlapis kaca; PM modul portabel; DG degasser; LS settler lamella; ISO/ISA standar simbol.");
};
