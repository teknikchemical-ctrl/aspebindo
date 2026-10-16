// Slide 9: Peluang bisnis dan dampak
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const ps = D.pasar, lc = D.lca, t = D.tgt, fl = t.fleet, i35 = fl.years.indexOf(2035), i28 = fl.years.indexOf(2028), r = ps.rows;
  const s = H.slide(9, "Pasar siap dilayani: {{756 set setara bernilai USD " + fmt(r[0].rev / 1e6, 0) + " juta per tahun}}; 57 PKS lolos saringan pertama, dan 10 set menghasilkan {{USD " + fmt(fl.rev[i35] / 1e6, 0) + " juta}} per tahun pada 2035",
    "Peluang bisnis dan dampak. Pasar bottom-up per saringan (saringan solar, jaringan, dan program grup adalah hipotesis yang divalidasi di G0). Peta NPV dihitung pada kasus target (CAPEX -15%, karbon 8,3). Armada 10 set (2027-2034); NPV armada USD " + fmt(fl.NPV / 1e6, 1) + " juta setelah overhead holding. Skenario yang menurunkan NPV (tanpa ekspor PLN, tanpa jasa POME, modul 30-45 t/jam) ada di BG_Model_Keuangan.xlsx.");
  const fit = (f, x, y, w, h, n) => H.imgFit(s, L.ROOT + "/deck/img/" + f, 4.05, 1.88, x, y, w, h, { objectName: n });
  const cols = [0.45, 4.6, 8.75], W = 4.15, R1 = 1.25, R2 = 3.84, IH = 1.8, SY = 0.26 + IH + 0.03;
  // 1. corong pasar (native)
  H.hdr(s, "1. Seberapa besar pasarnya (set setara 60 t TBS/jam)", cols[0], R1, W, { h: 0.24, fs: 8.8 });
  const fn = [[fmt(r[0].sets, 0), 1.5, C.navy, "TAM", "seluruh PKS tanpa penangkap metana · USD " + fmt(r[0].rev / 1e6, 0) + " juta/tahun"], [fmt(r[1].sets, 0), 1.25, C.royal, "SAM luas", "ukuran 30–60 t/jam di Sumatera dan Kalimantan · USD " + fmt(r[1].rev / 1e6, 0) + " juta"], [fmt(r[2].sets, 0), 0.9, C.teal, "SAM", "lolos saringan solar ≥ 2 L/t, jaringan ≤ 2 km, bebas program grup · USD " + fmt(r[2].rev / 1e6, 0) + " juta"], ["10", 0.55, C.amber, "SOM 2034", "sasaran armada kami = 17% SAM"]];
  fn.forEach(([v, w, c, lab, d], i) => { const y = R1 + 0.3 + i * 0.4; H.box(s, [{ text: v, options: { bold: true, fontSize: 12, color: i === 3 ? C.ink : C.white, breakLine: true } }], cols[0], y, w, 0.36, { fill: c, line: null, radius: 0.04, margin: 0, font: FONT_H });
    H.t(s, [{ text: lab + "  ", options: { bold: true, color: i === 3 ? C.amber : c } }, { text: d }], cols[0] + 1.58, y - 0.01, W - 1.58, 0.38, { fontSize: 7.7, valign: "middle" }); });
  H.take(s, "Hanya " + fmt(r[2].sets, 0) + " dari " + fmt(r[0].sets, 0) + " set lolos saringan awal, tetapi nilainya sudah USD " + fmt(r[2].rev / 1e6, 0) + " juta per tahun, cukup untuk 10 set pertama.", cols[0], R1 + SY, W, 0.4);
  // 2. provinsi
  const pv = ps.prov, tot = pv.reduce((q, x) => q + x[1], 0), top3 = (pv[0][1] + pv[1][1] + pv[2][1]) / tot;
  H.hdr(s, "2. Di mana PKS berada (jumlah pabrik)", cols[1], R1, W, { fill: C.teal, h: 0.24, fs: 8.8 }); fit("f_prov.png", cols[1], R1 + 0.26, W, IH, "grafik-provinsi");
  H.take(s, "Riau, Sumatera Utara, dan Kalimantan Tengah memegang " + fmt(top3 * 100, 0) + "% PKS; tiga provinsi ini menjadi sasaran awal.", cols[1], R1 + SY, W, 0.4);
  // 3. peta NPV
  H.hdr(s, "3. Seberapa menarik per set: NPV (USD juta)", cols[2], R1, W, { h: 0.24, fs: 8.8 }); fit("f_heatnpv.png", cols[2], R1 + 0.26, W, IH, "grafik-heatnpv");
  H.take(s, "Makin banyak solar tergantikan dan makin tinggi fee, makin besar NPV. Kotak biru = kasus target: USD " + fmt(t.NPV / 1e6, 1) + " juta. Hanya pojok kiri-bawah yang di bawah nol.", cols[2], R1 + SY, W, 0.4);
  // 4. armada
  H.hdr(s, "4. Pertumbuhan armada 10 set (USD juta per tahun)", cols[0], R2, W, { fill: C.teal, h: 0.24, fs: 8.8 }); fit("f_armada.png", cols[0], R2 + 0.26, W, IH, "grafik-armada");
  H.take(s, "Pendapatan armada naik dari USD " + fmt(fl.rev[i28] / 1e6, 1) + " juta (2028) menjadi USD " + fmt(fl.rev[i35] / 1e6, 1) + " juta (2035), dengan EBITDA USD " + fmt(fl.ebitda[i35] / 1e6, 1) + " juta.", cols[0], R2 + SY, W, 0.4);
  // 5. dampak
  H.hdr(s, "5. Dampak per set 60 t TBS/jam", cols[1], R2, W, { h: 0.24, fs: 8.8 });
  const im = [[fmt(lc.net_total / 1000, 0) + " ribu tCO₂e", "metana dihindari per tahun (−" + fmt(lc.net_total / lc.base * 100, 0) + "%) · SDG 13"], [fmt(t.E_net, 1) + " GWh", "listrik neto per tahun · SDG 7"], ["±" + fmt(t.E_cap * 0.3 * 1000, 0) + " ribu L", "solar tergantikan per tahun"], ["10 pekerja", "tenaga lokal tetap · SDG 8; efluen terolah · SDG 6"]];
  im.forEach(([b, tx], i) => { const x = cols[1] + (i % 2) * 2.1, y = R2 + 0.3 + Math.floor(i / 2) * 0.88; H.rect(s, x, y, 2.05, 0.82, { fill: C.panel, line: C.line, radius: 0.05 });
    H.t(s, b, x + 0.04, y + 0.06, 1.97, 0.34, { fontFace: FONT_H, fontSize: 12.5, bold: true, color: C.navy, align: "center", valign: "middle" }); H.t(s, tx, x + 0.08, y + 0.42, 1.89, 0.38, { fontSize: 7.6, align: "center" }); });
  H.take(s, "Armada 10 set menghindari ±" + fmt(10 * lc.net_total / 1000, 0) + " ribu tCO₂e per tahun, sambil menggantikan solar PKS dan membuka lapangan kerja.", cols[1], R2 + SY, W, 0.4);
  // 6. tawaran
  H.hdr(s, "6. Tawaran kepada pemodal", cols[2], R2, W, { fill: C.teal, h: 0.24, fs: 8.8 });
  const b = { bold: true, color: C.navy };
  H.table(s, [[{ text: "Dana set pertama", options: b }, "USD " + fmt(t.peak / 1e6, 1) + " juta (utang 58%)"], [{ text: "Imbal hasil", options: b }, "IRR " + fmt(t.IRR * 100, 1) + "% · ekuitas " + fmt(t.IRR_eq * 100, 1) + "%"], [{ text: "Balik modal", options: b }, fmt(t.PBP, 1) + " tahun · DSCR " + fmt(t.DSCR, 2)], [{ text: "Armada 10 set", options: b }, "EBITDA 2035 USD " + fmt(fl.ebitda[i35] / 1e6, 1) + " juta"], [{ text: "NPV armada", options: b }, "USD " + fmt(fl.NPV / 1e6, 1) + " juta (setelah overhead)"], [{ text: "Hemat bagi PKS", options: b }, fmt(t.pks.save_pct * 100, 0) + "% biaya POME, modal nol"]], cols[2], R2 + 0.28, [1.35, 2.8], { fs: 7.9, rh: 0.255, head: 0 });
  H.take(s, "Pemodal masuk setelah gerbang G3, ketika kinerja reaktor, harga, dan kontrak sudah terbukti.", cols[2], R2 + SY, W, 0.4);
  H.concl(s, "Pasar nyata dan terukur: 57 PKS siap dilayani lebih dulu, 10 set menghasilkan USD " + fmt(fl.rev[i35] / 1e6, 1) + " juta pendapatan per tahun, dan tiap set menghindari 32 ribu tCO₂e.", "Kesimpulan");
  H.src(s, "fin_market.py (Trase/SEI-PCS, GAPKI 2026, PASPI/BRIN); fin_core.py (kasus target, armada); neraca proses Rev 2; LCA AMS-III.H (UF 0,89; GWP 28); research/R1 dan R3. Sebaran provinsi dari direktori PKS (jumlah berbeda dari TAM karena sumber berbeda).", "TAM total pasar; SAM pasar yang dapat dilayani; SOM pasar yang dapat dicapai; SDG tujuan pembangunan berkelanjutan; EBITDA laba sebelum bunga, pajak, penyusutan, amortisasi; NPV nilai kini bersih; DSCR rasio cakupan layanan utang.");
};
