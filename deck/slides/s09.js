// Slide 9: Peluang bisnis dan dampak
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, ps = D.pasar, lc = D.lca, t = D.tgt, fl = t.fleet, i35 = fl.years.indexOf(2035);
  const s = H.slide(9, "Peluang besar dan terukur: {{756 set setara (USD " + fmt(ps.rows[0].rev / 1e6, 0) + " juta per tahun)}}, dengan 57 PKS siap dilayani lebih dulu dan 10 set menghindari {{±" + fmt(10 * lc.net_total / 1000, 0) + " ribu tCO₂e}} per tahun",
    "Peluang bisnis dan dampak. Pasar bottom-up per filter (filter solar, jaringan, dan program grup adalah hipotesis yang divalidasi di G0). Tuas nilai dihitung satu per satu terhadap kasus awal; kasus target menggabungkan solar 3,0 L/t, CAPEX -15%, fee 1,35, karbon 8,3. Armada 10 set (2027-2034) pada asumsi kasus target; NPV korporasi setelah overhead holding. Skenario yang menurunkan NPV (tanpa ekspor PLN, tanpa jasa POME, modul 30-45 t/jam, tarif excess 7,44 USc) ada di BG_Model_Keuangan.xlsx.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  H.hdr(s, "(a) Corong pasar: set setara 60 t TBS/jam", 0.45, 1.25, 4.1, { h: 0.24, fs: 9.5 });
  img("f_pasar.png", 0.45, 1.52, 4.1, 2.35, "grafik-pasar");
  H.hdr(s, "(b) Sebaran PKS menurut provinsi", 4.7, 1.25, 4.0, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_prov.png", 4.7, 1.52, 4.0, 2.35, "grafik-provinsi");
  H.hdr(s, "(c) Dampak terukur per set 60 t TBS/jam", 8.85, 1.25, 4.05, { h: 0.24, fs: 9.5 });
  const im = [[fmt(lc.net_total / 1000, 0) + " ribu", "tCO₂e per tahun dihindari (−" + fmt(lc.net_total / lc.base * 100, 0) + "%) · SDG 13"], [fmt(t.E_net, 1) + " GWh", "listrik neto per tahun, " + fmt(t.E_cap, 1) + " GWh ke PKS · SDG 7"], ["±" + fmt(t.E_cap * 0.3 * 1000, 0) + " ribu L", "solar tergantikan per tahun (perkiraan)"], ["10 orang", "pekerja lokal tetap; fabrikasi skid dalam negeri · SDG 8"]];
  im.forEach(([b, tx], i) => { const x = 8.85 + (i % 2) * 2.05, y = 1.55 + Math.floor(i / 2) * 1.16; H.rect(s, x, y, 2.0, 1.1, { fill: C.panel, line: C.line, radius: 0.05 });
    H.t(s, b, x + 0.06, y + 0.08, 1.88, 0.4, { fontFace: FONT_H, fontSize: 15, bold: true, color: C.navy, align: "center", valign: "middle" }); H.t(s, tx, x + 0.1, y + 0.52, 1.8, 0.55, { fontSize: 8.2, align: "center" }); });
  H.t(s, "Efluen BOD 1.543 mg/L tidak dibuang ke sungai (SDG 6); HAZOP, SOP, dan detektor gas sebelum operasi (K3).", 8.85, 3.88, 4.05, 0.28, { fontSize: 7.6, color: C.slate });
  H.hdr(s, "(d) Tuas nilai: NPV per set (USD juta)", 0.45, 4.2, 4.65, { h: 0.24, fs: 9.5 });
  img("f_tuas.png", 0.45, 4.45, 4.65, 1.98, "grafik-tuas");
  H.hdr(s, "(e) Armada 10 set: operasi dan emisi dihindari", 5.25, 4.2, 3.9, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_armada.png", 5.25, 4.45, 3.9, 1.95, "grafik-armada");
  H.hdr(s, "(f) Tawaran kepada pemodal", 9.3, 4.2, 3.6, { h: 0.24, fs: 9.5 });
  const b = { bold: true, color: C.navy };
  H.table(s, [[{ text: "Set pertama", options: b }, "dana puncak USD " + fmt(t.peak / 1e6, 1) + " juta"], [{ text: "Imbal hasil", options: b }, "IRR " + fmt(t.IRR * 100, 1) + "% · ekuitas " + fmt(t.IRR_eq * 100, 1) + "%"], [{ text: "Payback", options: b }, fmt(t.PBP, 1) + " tahun · DSCR " + fmt(t.DSCR, 2)], [{ text: "Armada 10 set", options: b }, "pendapatan 2035 USD " + fmt(fl.rev[i35] / 1e6, 1) + " juta"], [{ text: "NPV armada", options: b }, "USD " + fmt(fl.NPV / 1e6, 1) + " juta (setelah overhead)"], [{ text: "Hemat PKS", options: b }, fmt(t.pks.save_pct * 100, 0) + "% biaya POME, modal nol"]], 9.3, 4.45, [1.1, 2.5], { fs: 8.2, rh: 0.32, head: 0 });
  H.concl(s, "Pasar siap dilayani: 57 PKS lolos filter pertama dengan potensi USD " + fmt(ps.rows[2].rev / 1e6, 0) + " juta per tahun; 10 set pertama menghasilkan pendapatan USD " + fmt(fl.rev[i35] / 1e6, 1) + " juta per tahun pada 2035 dan NPV armada USD " + fmt(fl.NPV / 1e6, 1) + " juta.", "Kesimpulan");
  H.src(s, "fin_market.py (Trase/SEI-PCS, GAPKI 2026, PASPI/BRIN); fin_core.py (tuas nilai, armada, kasus target); neraca proses Rev 2; LCA AMS-III.H (UF 0,89; GWP 28); research/R1 dan R3. Sebaran provinsi: data direktori PKS, jumlah berbeda dari TAM karena sumber berbeda.", "TAM total pasar; SAM pasar yang dapat dilayani; SOM pasar yang dapat dicapai; SDG tujuan pembangunan berkelanjutan; K3 keselamatan dan kesehatan kerja.");
};
