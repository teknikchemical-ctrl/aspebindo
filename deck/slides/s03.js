// Slide 3: Konsep solusi
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, p = D.proses, pk = D.pks, sc = k.scen;
  const s = H.slide(3, "Set biogas termofilik 55 °C mengolah POME dalam 5 hari menjadi {{" + fmt(k.E_net, 1) + " GWh listrik per tahun}}, dibayar sebagai layanan, dan dapat dibongkar-pasang",
    "Konsep: urutan proses dari POME sampai listrik; modularitas 2/3/4 tangki identik; hanya skala 60 t TBS/jam yang layak pada asumsi dasar.");
  // ---- kiri
  H.hdr(s, "Wujud produk (modul acuan 45 t TBS/jam)", 0.45, 1.25, 5.75);
  const W0 = 5.75, H0 = W0 * 9 / 16;
  s.addImage({ path: L.ROOT + "/cad/out/render/DIORAMA_produk.png", x: 0.45, y: 1.57, w: W0, h: 2.6, sizing: { type: "cover", w: W0, h: 2.6 }, objectName: "render-produk" });
  const y1 = 1.57 + 2.6 + 0.08;
  H.hdr(s, "Modular dan portabel", 0.45, y1, 5.75, { fill: C.teal });
  [["21", "kontainer dan skid 40 ft per modul acuan"], ["980 m³", "tangki GFS dibaut identik; 2, 3, atau 4 per set"], ["±6 bulan", "bongkar-pasang antar-PKS, biaya 15% FCI"]].forEach(([b, t], i) => H.kpi(s, b, t, 0.45 + i * 1.95, y1 + 0.33, 1.85, 0.78, { bs: 15, ls: 8 }));
  const m30 = sc.find((x) => x.tag === "Modul 30 t/jam"), m45 = sc.find((x) => x.tag === "Modul 45 t/jam"), b60 = sc[0], T = p.tiers;
  const nv = (x) => ({ text: fmt(x / 1e6, 2), options: { align: "center", bold: true, color: x < 0 ? C.red : C.green } });
  H.table(s, [["PKS (t TBS/jam)", "Tangki", "Genset (kWe)", "Biogas (Nm³/hari)", "Neto (kW)", "FCI (USD juta)", "Peran"],
    ["30", "2", "2 × 400", fmt(T["30"].bg, 0), fmt(T["30"].Pn, 0), fmt(m30.FCI / 1e6, 2), "pilot"], ["45 (acuan)", "3", "2 × 600", fmt(T["45"].bg, 0), fmt(T["45"].Pn, 0), fmt(m45.FCI / 1e6, 2), "acuan gambar"], ["60 (komersial)", "4", "2 × 800", fmt(T["60"].bg, 0), fmt(T["60"].Pn, 0), fmt(b60.FCI / 1e6, 2), "komersial"]],
    0.45, y1 + 1.22, [1.0, 0.55, 0.8, 0.95, 0.65, 0.85, 0.95], { fs: 8, rh: 0.2, hrh: 0.3, align: ["left", "center", "center", "center", "center", "center", "center"] });
  // ---- kanan: alur proses
  const X0 = 6.4, XW = 6.5;
  H.hdr(s, "Cara kerja, dari POME sampai listrik (set 60 t TBS/jam)", X0, 1.25, XW);
  const bw = 1.52, bh = 0.86, gap = (XW - 4 * bw) / 3, xr = (i) => X0 + i * (bw + gap);
  const yA = 1.95;
  H.t(s, "A. Pengolahan POME", X0, 1.57, 2.5, 0.2, { fontFace: FONT_H, fontSize: 9, bold: true, color: C.royal });
  const r1 = [["1 Penerimaan", fmt(p.pome_m3d * 60 / 45, 0) + " m³ POME/hari, 85 °C, dari fat pit"], ["2 Praolah", "saringan, ruang pasir, pendingin ke 55 °C"], ["3 Reaktor kontak", p.n60 + " tangki GFS, 55 °C, HRT 5 hari"], ["4 Degasser + settler", "lumpur kembali ke reaktor (SRT 12 hari)"]];
  r1.forEach(([a, b], i) => {
    H.box(s, [{ text: a, options: { bold: true, fontSize: 10, color: C.white, breakLine: true } }, { text: b, options: { fontSize: 8.5, color: C.white } }], xr(i), yA, bw, bh, { fill: i === 2 ? C.royal : C.navy, line: null, radius: 0.06, margin: [3, 5, 3, 5] });
    if (i < 3) H.ln(s, xr(i) + bw, yA + bh / 2, xr(i + 1), yA + bh / 2, { color: C.navy, w: 1.75 });
  });
  const c3 = xr(2) + bw / 2, c4 = xr(3) + bw / 2, c2 = xr(1) + bw / 2;
  H.path(s, [[c4, yA], [c4, yA - 0.14], [c3, yA - 0.14], [c3, yA]], { color: C.green, w: 1.5 });
  H.t(s, "resirkulasi " + fmt(p.recycle * 60 / 45, 0) + " m³/hari", c3 + 0.1, yA - 0.32, 1.6, 0.16, { fontSize: 8, bold: true, color: C.green });
  H.path(s, [[c2, yA + bh], [c2, yA + bh + 0.22]], { color: C.slate, w: 1.25 }); H.t(s, "residu saringan dan pasir ke PKS", c2 - 0.8, yA + bh + 0.24, 1.6, 0.3, { fontSize: 8, align: "center", color: C.slate });
  H.path(s, [[c4, yA + bh], [c4, yA + bh + 0.22]], { color: C.teal, w: 1.5 }); H.t(s, "efluen " + fmt(p.eff.Q_m3d * 60 / 45, 0) + " m³/hari ke kolam polishing", c4 - 0.78, yA + bh + 0.24, 1.56, 0.3, { fontSize: 8, align: "center", color: C.slate });
  const yB = 3.62;
  H.t(s, "B. Biogas menjadi listrik", X0, yB - 0.34, 1.75, 0.16, { fontFace: FONT_H, fontSize: 9, bold: true, color: "9A6A00" });
  H.path(s, [[c3, yA + bh], [c3, yB - 0.16], [xr(0) + bw / 2, yB - 0.16], [xr(0) + bw / 2, yB]], { color: C.amber, w: 2.25 });
  H.t(s, fmt(p.biogas60, 0) + " Nm³ biogas/hari (CH₄ " + fmt(p.ch4_frac * 100, 0) + "%)", xr(1) + 0.3, yB - 0.34, 2.6, 0.16, { fontSize: 8, bold: true, color: "9A6A00" });
  const r2 = [["5 Pemurnian", "H₂S " + fmt(p.h2s_raw, 0) + " → " + fmt(p.h2s_fuel, 0) + " ppm (bio-scrubber, karbon aktif)"], ["6 Penampung gas", "membran ganda 2 jam; flare tertutup"], ["7 Genset", "2 × 800 kWe, efisiensi listrik " + fmt(p.eta_el * 100, 1) + "%"], ["8 Listrik dan panas", "20 kV ke PKS dan PLN; panas ke reaktor"]];
  r2.forEach(([a, b], i) => {
    H.box(s, [{ text: a, options: { bold: true, fontSize: 10, color: C.ink, breakLine: true } }, { text: b, options: { fontSize: 8.5 } }], xr(i), yB, bw, bh, { fill: C.amberL, line: C.amber, lw: 1.25, radius: 0.06, margin: [3, 5, 3, 5] });
    if (i < 3) H.ln(s, xr(i) + bw, yB + bh / 2, xr(i + 1), yB + bh / 2, { color: "9A6A00", w: 1.75 });
  });
  const yC = 4.85, ow = (XW - 0.3) / 4;
  H.path(s, [[xr(3) + bw / 2, yB + bh], [xr(3) + bw / 2, yC - 0.1], [X0 + ow / 2, yC - 0.1]], { color: C.navy, w: 1.25, arrow: false });
  [["Listrik ke PKS", fmt(k.E_cap, 2) + " GWh/tahun, menggantikan solar"], ["Ekspor ke PLN", fmt(k.E_exp, 2) + " GWh/tahun, 9,81 USc/kWh"], ["Kredit karbon", "≈ " + fmt(D.lca.credited / 1000, 0) + " ribu tCO₂e/tahun"], ["Jasa pengolahan", "USD " + fmt(D.meta.fee, 2) + " per t TBS"]].forEach(([a, b], i) => {
    const x = X0 + i * (ow + 0.1); H.ln(s, x + ow / 2, yC - 0.1, x + ow / 2, yC, { color: C.navy, w: 1.25 });
    H.box(s, [{ text: a, options: { bold: true, fontSize: 9.5, color: C.green, breakLine: true } }, { text: b, options: { fontSize: 8.5 } }], x, yC, ow, 0.55, { fill: C.greenL, line: C.green, radius: 0.05 });
  });
  // panel bawah
  const pw = (XW - 0.15) / 2;
  H.hdr(s, "Pengguna dan nilai", X0, 5.55, pw, { fill: C.teal, h: 0.25, fs: 9.5 }); H.hdr(s, "Pembeda dari praktik saat ini", X0 + pw + 0.15, 5.55, pw, { fill: C.teal, h: 0.25, fs: 9.5 });
  const bl = (a) => a.map((q, j) => ({ text: q, options: { bullet: { indent: 9 }, breakLine: j < a.length - 1, paraSpaceAfter: 2 } }));
  H.panel(s, X0, 5.8, pw, 0.72); H.panel(s, X0 + pw + 0.15, 5.8, pw, 0.72);
  H.t(s, bl(["PKS 45–60 t TBS/jam, solar tergantikan ≥ 2,0 L/t TBS", "PKS bayar USD " + fmt(pk.per_t.D, 2) + " vs " + fmt(pk.per_t.A, 2) + "/t TBS bila memakai kolam"]), X0 + 0.08, 5.84, pw - 0.16, 0.66, { fontSize: 9 });
  H.t(s, bl(["Layanan, bukan proyek: operator menjamin kinerja", "HRT 5 hari (kolam tertutup 25–40 hari), plot 0,38–0,5 ha"]), X0 + pw + 0.23, 5.84, pw - 0.16, 0.66, { fontSize: 9 });
  H.concl(s, "Konsep ini menukar proyek rekayasa sekali jadi dengan layanan modular: modal PKS nol, reaktor 5 hari, dan set yang dapat dipindah bila PKS berhenti beroperasi.", "Kesimpulan");
  H.src(s, "neraca proses Rev 2 (process/outputs/results.json; aliran 60 t/jam = modul acuan × 4/3); Model Keputusan PKS; model 3D tim; research/R3, R6.", "GFS baja berlapis kaca; HRT/SRT waktu tinggal hidraulik/lumpur; FCI biaya modal tetap; NPV nilai kini neto; PKS pabrik kelapa sawit.");
};
