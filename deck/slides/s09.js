// Slide 9: Peluang bisnis dan dampak
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, ps = D.pasar, lc = D.lca, fl = k.fleet, sc = k.scen;
  const s = H.slide(9, "Pasarnya sempit tetapi nyata: {{±" + fmt(ps.rows[2].sets, 0) + " PKS bernilai USD " + fmt(ps.rows[2].rev / 1e6, 0) + " juta per tahun}}, dan 10 set menghindari {{±" + fmt(10 * lc.net_total / 1000, 0) + " ribu tCO₂e}} setiap tahun",
    "Peluang bisnis dan dampak. Pasar bottom-up per filter (filter solar, jaringan, dan program grup adalah hipotesis yang divalidasi di G0); ekonomi per set menurut skenario; armada 10 set; dampak terukur.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  H.hdr(s, "(a) Corong pasar: set setara 60 t TBS/jam", 0.45, 1.25, 4.1, { h: 0.24, fs: 9.5 });
  img("f_pasar.png", 0.45, 1.52, 4.1, 2.35, "grafik-pasar");
  H.hdr(s, "(b) Sebaran PKS menurut provinsi (± pabrik)", 4.7, 1.25, 4.0, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_prov.png", 4.7, 1.52, 4.0, 2.35, "grafik-provinsi");
  // dampak: kartu
  H.hdr(s, "(c) Dampak terukur per set 60 t TBS/jam", 8.85, 1.25, 4.05, { h: 0.24, fs: 9.5 });
  const im = [["" + fmt(lc.net_total / 1000, 0) + " ribu", "tCO₂e per tahun dihindari (−" + fmt(lc.net_total / lc.base * 100, 0) + "%) · SDG 13"], [fmt(k.E_net, 1) + " GWh", "listrik neto per tahun, " + fmt(k.E_cap, 1) + " GWh ke PKS · SDG 7"], ["±" + fmt(k.E_cap * 0.3 * 1000, 0) + " ribu L", "solar tergantikan per tahun (perkiraan)"], ["10 orang", "pekerja lokal tetap; fabrikasi skid dalam negeri · SDG 8"]];
  im.forEach(([b, t], i) => { const x = 8.85 + (i % 2) * 2.05, y = 1.55 + Math.floor(i / 2) * 1.14; H.rect(s, x, y, 2.0, 1.08, { fill: C.panel, line: C.line, radius: 0.05 });
    H.t(s, b, x + 0.06, y + 0.08, 1.88, 0.4, { fontFace: FONT_H, fontSize: 15, bold: true, color: C.navy, align: "center", valign: "middle" }); H.t(s, t, x + 0.1, y + 0.52, 1.8, 0.52, { fontSize: 8, color: C.ink, align: "center" }); });
  H.t(s, "Efluen BOD 1.543 mg/L tidak dibuang ke sungai (SDG 6); HAZOP, SOP, dan detektor gas sebelum operasi (K3).", 8.85, 3.83, 4.05, 0.3, { fontSize: 7.6, color: C.slate });
  // baris 2
  H.hdr(s, "(d) NPV per set menurut skenario (USD juta)", 0.45, 4.15, 4.65, { h: 0.24, fs: 9.5 });
  img("f_skenario.png", 0.45, 4.41, 4.65, 2.0, "grafik-skenario");
  H.hdr(s, "(e) Armada 10 set: operasi dan emisi dihindari", 5.25, 4.15, 3.9, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_armada.png", 5.25, 4.41, 3.9, 1.95, "grafik-armada");
  H.hdr(s, "(f) Tawaran kepada pemodal", 9.3, 4.15, 3.6, { h: 0.24, fs: 9.5 });
  H.table(s, [["Unit pertama", "dana puncak USD " + fmt(k.peak / 1e6, 1) + " juta"], ["Imbal hasil set 1", "IRR " + fmt(k.IRR * 100, 1) + "% · ekuitas " + fmt(k.IRR_eq * 100, 1) + "%"], ["Set ke-10", "IRR " + fmt(sc[11].IRR * 100, 1) + "% · NPV USD " + fmt(sc[11].NPV / 1e6, 2) + " juta"], ["Armada 10 set", "puncak USD " + fmt(fl.peak / 1e6, 0) + " juta · NPV USD " + fmt(fl.NPV / 1e6, 1) + " juta"], ["Impas korporasi", "±" + fmt(fl.sets_breakeven, 0) + " set"], ["Hemat PKS", fmt(sc[0].save * 100, 1) + "% (3,0 L/t: " + fmt(sc[1].save * 100, 1) + "%)"]], 9.3, 4.41, [1.2, 2.4], { fs: 8, rh: 0.33, head: 0 });
  H.concl(s, "Hanya ±57 dari ±1.150 PKS lolos filter solar, jaringan, dan program grup; karena itu pasar dibuktikan dulu di G0, dan armada baru menutup biaya korporasi pada set ke-11.", "Kesimpulan");
  H.src(s, "fin_market.py (Trase/SEI-PCS, GAPKI 2026, PASPI/BRIN); fin_core.py (skenario, armada); neraca proses Rev 2; LCA AMS-III.H (UF 0,89; GWP 28); research/R1 dan R3.", "TAM total pasar; SAM pasar yang dapat dilayani; SOM pasar yang dapat dicapai; SDG tujuan pembangunan berkelanjutan; K3 keselamatan dan kesehatan kerja.");
};
