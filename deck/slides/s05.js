module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L;
  const s = H.slide(5, "Solusi: desain produk", "Desain produk: PFD, tata letak 0,38 ha, model 3D, dan sembilan lembar gambar rekayasa konsisten satu sama lain pada modul acuan 45 t TBS/jam");
  H.sec(s, "Diagram alir proses (PFD BG-002 Rev 3): aliran, kendali, dan batas modul portabel", 0.4, 1.18, 7.6);
  H.imgFit(s, "deck/img/pfd_crop.png", 3473, 1960, 0.4, 1.45, 7.6, 4.3);
  H.t(s, "Nomor aliran, suhu, tekanan, dan laju massa tercantum pada tabel kondisi aliran di lembar PFD; simbol ISO 10628-2/ISA-5.1; setiap bejana punya kendali level; tiap modul diberi batas portabel (PM-1 … PM-10).", 0.4, 5.78, 7.6, 0.3, { fontSize: 6.8 });
  H.sec(s, "Model 3D set lengkap", 8.2, 1.18, 4.75);
  H.imgFit(s, "cad/out/render/PLANT_iso-depan.png", 2200, 1400, 8.2, 1.45, 2.4, 1.55);
  H.imgFit(s, "cad/out/render/DIORAMA_atas.png", 3200, 1800, 10.65, 1.45, 2.3, 1.55);
  H.sec(s, "Tata letak plot (1:400) dan aliran material", 8.2, 3.05, 4.75);
  H.imgFit(s, "deck/img/plan_ga.png", 2600, 899, 8.2, 3.3, 4.75, 1.65);
  H.t(s, "Aliran: POME → rak pipa selatan → reaktor R-201…203 → degasser/settler → gas utara → penampung gas → genset (timur). Jarak aman terpenuhi: flare ≥ 15 m dari penampung gas dan kontainer genset.", 8.2, 5.0, 4.75, 0.4, { fontSize: 6.6 });
  H.sec(s, "Gambar rekayasa (9 lembar A3, 0 tabrakan teks)", 0.4, 6.1, 7.6);
  H.t(s, "GA-001 tata letak · GA-002 lokasi PKS · V-201 tangki GFS · M-004 skid kontak · M-001 praolah · M-006 pemurnian gas · M-008 genset · M-007 penampung gas · M-005 skid dosing dan lumpur", 0.4, 6.35, 7.6, 0.3, { fontSize: 6.8 });
  H.imgFit(s, "deck/img/dwg3.png", 1400, 990, 8.2, 5.45, 1.6, 1.5); H.imgFit(s, "deck/img/dwg4.png", 1400, 990, 9.9, 5.45, 1.6, 1.5);
  H.t(s, "Lembar V-201 dan M-004", 11.6, 5.6, 1.35, 0.4, { fontSize: 6.5, italic: true, color: C.slate });
  H.src(s, "pfd/outputs/PFD_BG-002_Rev3.pdf; cad/drawings/out/BG_drawing_set_A3.pdf; model CadQuery tim (cad/bgmodels.py).", "PFD diagram alir proses; GFS baja berlapis kaca; PM modul portabel.");
};
