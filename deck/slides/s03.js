// Slide 3: Solusi - konsep utama
module.exports = (pres, H, L) => {
  const { C, D, fmt, pct, FONT_H, FONT_B } = L;
  const k = D.keu, p = D.proses, m = D.meta, pk = D.pks;
  const s = H.slide(3, "Solusi: konsep utama", "Solusi: set biogas termofilik 55 °C mengolah POME dalam lima hari, menjual ≈ " + fmt(k.E_net, 1) + " GWh listrik neto per tahun, dan dapat dibongkar-pasang antar-PKS");
  // ---------------- kiri: render 3D + modularitas
  const W0 = 5.6, H0 = W0 * 9 / 16;
  H.rect(s, 0.36, 1.16, W0 + 0.08, H0 + 0.08, { fill: C.white, line: C.line, radius: 0.04 });
  H.img(s, "cad/out/render/DIORAMA_produk.png", 0.4, 1.2, W0, H0);
  H.t(s, "Model 3D set biogas (modul acuan 45 t TBS/jam; konfigurasi 60 t/jam menambah satu tangki)", 0.4, 1.2 + H0 + 0.06, W0, 0.18, { fontSize: 6.5, italic: true, color: C.slate });
  const yT = 1.2 + H0 + 0.3;
  H.sec(s, "Modular dan portabel: bukti terukur", 0.4, yT, W0);
  const tl = [[fmt(p.tiers["45"].N * 7) , "muatan kontainer/skid 40 ft per modul acuan (21)"], ["980 m³", "tangki GFS dibaut identik; 2, 3, atau 4 tangki"], ["±6 bulan", "bongkar-pasang; biaya 15% FCI"], ["USD " + fmt((D.reloc.reloc - D.reloc.stranded) / 1e6, 2) + " jt", "kerugian dihindari bila PKS tutup tahun 8 dan set dipindah (NPV " + fmt(D.reloc.reloc / 1e6, 2) + " vs " + fmt(D.reloc.stranded / 1e6, 2) + " juta bila terdampar)"]];
  tl[0][0] = "21";
  tl.forEach(([b, t], i) => {
    const x = 0.4 + i * 1.4;
    H.rect(s, x, yT + 0.27, 1.35, 0.62, { fill: C.white, line: C.line, radius: 0.04 });
    H.t(s, b, x + 0.06, yT + 0.29, 1.25, 0.22, { fontFace: FONT_H, fontSize: 11, bold: true, color: C.royal, valign: "middle" });
    H.t(s, t, x + 0.06, yT + 0.51, 1.25, 0.38, { fontSize: 5.8 });
  });
  const T3 = D.proses.tiers, sc = k.scen;
  const modul = sc.find((x) => x.tag === "Modul 30 t/jam"), m45 = sc.find((x) => x.tag === "Modul 45 t/jam"), base = sc[0];
  H.sec(s, "Skala dengan penambahan modul identik (numbering up)", 0.4, yT + 0.98, W0);
  const col = (v) => ({ text: v, options: { align: "center" } });
  const neg = (x, d = 2) => ({ text: fmt(x, d), options: { align: "center", bold: true, color: x < 0 ? C.red : C.greenD } });
  H.table(s, [["Ukuran PKS (t TBS/jam)", "30", "45 (acuan)", "60 (komersial)"],
    ["Tangki GFS 980 m³ · genset", "2 · 2×400", "3 · 2×600", "4 · 2×800 kWe"],
    ["Biogas (Nm³/hari) · neto (kW)", fmt(T3["30"].bg, 0) + " · " + fmt(T3["30"].Pn, 0), fmt(T3["45"].bg, 0) + " · " + fmt(T3["45"].Pn, 0), fmt(T3["60"].bg, 0) + " · " + fmt(T3["60"].Pn, 0)],
    ["Investasi (FCI, USD juta)", fmt(modul.FCI / 1e6, 2), fmt(m45.FCI / 1e6, 2), fmt(base.FCI / 1e6, 2)],
    ["NPV proyek (USD juta) · IRR", [neg(modul.NPV / 1e6)][0], neg(m45.NPV / 1e6), neg(base.NPV / 1e6)],
  ].map((r, i) => i === 4 ? [r[0], { text: fmt(modul.NPV / 1e6, 2) + " · " + fmt(modul.IRR * 100, 1) + "%", options: { align: "center", bold: true, color: C.red } }, { text: fmt(m45.NPV / 1e6, 2) + " · " + fmt(m45.IRR * 100, 1) + "%", options: { align: "center", bold: true, color: C.red } }, { text: fmt(base.NPV / 1e6, 2) + " · " + fmt(base.IRR * 100, 1) + "%", options: { align: "center", bold: true, color: C.greenD } }] : r.map((c, j) => j ? col(c) : c)),
    0.4, yT + 1.24, W0, [1.85, 1.0, 1.25, 1.5], { fs: 6.8, rh: 0.2, hrh: 0.2 });
  H.t(s, "NPV pada fee USD " + fmt(m.fee, 2) + "/t TBS, solar tergantikan 2,0 L/t TBS: skala minimum layak 60 t/jam (slide 7).", 0.4, yT + 2.27, W0, 0.15, { fontSize: 6, italic: true, color: C.slate });
  // ---------------- kanan: diagram alir proses
  const X0 = 6.85, XW = 6.1;
  H.sec(s, "Cara kerja, dari penerimaan POME sampai listrik (set 60 t TBS/jam)", X0, 1.18, XW);
  const bw = 1.4, bh = 0.74, gap = (XW - 4 * bw) / 3;
  const row1 = [["1  Penerimaan POME", "85 °C, " + fmt(p.pome_m3d * 60 / 45, 0) + " m³/hari dari fat pit"], ["2  Praolah", "saringan putar, ruang pasir (85%), pendingin ke 55 °C"],
                ["3  Reaktor kontak 55 °C", p.n60 + " tangki GFS 980 m³; HRT 5 hari, SRT 12 hari"], ["4  Degasser + settler lamella", "vakum −0,3 bar; 85% biomassa kembali ke reaktor"]];
  const xr = (i) => X0 + i * (bw + gap), y1 = 1.9;
  row1.forEach(([a, b], i) => {
    H.box(s, [{ text: a, options: { bold: true, color: C.white, fontSize: 7.5, breakLine: true } }, { text: b, options: { color: C.white, fontSize: 6.5 } }], xr(i), y1, bw, bh, { fill: i === 2 ? C.royal : C.navy, line: null, radius: 0.05, margin: [2, 4, 2, 4] });
    if (i < 3) H.ln(s, xr(i) + bw, y1 + bh / 2, xr(i + 1), y1 + bh / 2, { color: C.navy, w: 1.5 });
  });
  H.t(s, "POME tak diolah, masuk dari fat pit", X0, y1 - 0.17, 1.4, 0.14, { fontSize: 5.8, color: C.slate });
  // lumpur resirkulasi (loop di atas)
  const cx3 = xr(2) + bw / 2, cx4 = xr(3) + bw / 2;
  H.path(s, [[cx4, y1], [cx4, y1 - 0.2], [cx3, y1 - 0.2], [cx3, y1]], { color: C.greenD, w: 1.25 });
  H.t(s, "lumpur resirkulasi " + fmt(p.recycle * 60 / 45, 0) + " m³/hari", cx3 - 0.2, y1 - 0.37, 1.9, 0.15, { fontSize: 6, bold: true, color: C.greenD });
  // keluaran sisi baris 1
  const cx2 = xr(1) + bw / 2;
  H.path(s, [[cx2, y1 + bh], [cx2, y1 + bh + 0.2]], { color: C.slate, w: 1 });
  H.t(s, "residu saringan dan pasir ke PKS", cx2 - 0.55, y1 + bh + 0.21, 1.1, 0.25, { fontSize: 5.8, color: C.slate, align: "center" });
  H.path(s, [[cx4, y1 + bh], [cx4, y1 + bh + 0.2]], { color: C.teal, w: 1.25 });
  H.t(s, "efluen " + fmt(p.eff.Q_m3d * 60 / 45, 0) + " m³/hari (BOD ≈ " + fmt(p.eff.BOD5, 0) + " mg/L) ke kolam polishing; lumpur lebih ke screw press", cx4 - 0.7, y1 + bh + 0.21, 1.38, 0.4, { fontSize: 5.8, color: C.slate, align: "center" });
  // biogas dari reaktor
  const y2 = 3.42;
  H.path(s, [[cx3, y1 + bh], [cx3, 3.18], [xr(0) + bw / 2, 3.18], [xr(0) + bw / 2, y2]], { color: C.amber, w: 2 });
  H.t(s, "biogas " + fmt(p.biogas60, 0) + " Nm³/hari, CH₄ " + fmt(p.ch4_frac * 100, 0) + "%", xr(0) + bw / 2 + 0.1, 3.2, 2.3, 0.15, { fontSize: 6.3, bold: true, color: "9A6A00" });
  const row2 = [["5  Pemurnian biogas", "bio-scrubber, pendingin 5 °C, karbon aktif: H₂S " + fmt(p.h2s_raw, 0) + " → " + fmt(p.h2s_fuel, 0) + " ppm"], ["6  Penampung gas", "membran ganda 2 jam; kendali tekanan; flare tertutup"], ["7  Genset biogas", "2 × 800 kWe, η listrik " + fmt(p.eta_el * 100, 1) + "%"], ["8  Panas dan listrik", "air panas 90 °C memanasi reaktor; sisa panas ke PKS"]];
  row2.forEach(([a, b], i) => {
    H.box(s, [{ text: a, options: { bold: true, color: C.ink, fontSize: 7.5, breakLine: true } }, { text: b, options: { color: C.ink, fontSize: 6.5 } }], xr(i), y2, bw, bh, { fill: "FFF3CF", line: C.amber, radius: 0.05, margin: [2, 4, 2, 4] });
    if (i < 3) H.ln(s, xr(i) + bw, y2 + bh / 2, xr(i + 1), y2 + bh / 2, { color: "9A6A00", w: 1.5 });
  });
  // keluaran bernilai
  const y3 = 4.55, ow = (XW - 3 * 0.1) / 4;
  const outs = [["Listrik ke PKS", fmt(k.E_cap, 2) + " GWh/tahun menggantikan solar (USD 0,20/kWh)"], ["Ekspor ke PLN", fmt(k.E_exp, 2) + " GWh/tahun pada 9,81 USc/kWh"], ["Kredit karbon", "≈ " + fmt(D.lca.credited / 1000, 0) + " ribu tCO₂e/tahun (USD 5/t)"], ["Jasa pengolahan POME", "USD " + fmt(m.fee, 2) + "/t TBS dari PKS"]];
  H.path(s, [[xr(3) + bw / 2, y2 + bh], [xr(3) + bw / 2, y3 - 0.1], [X0 + ow / 2, y3 - 0.1]], { color: C.navy, w: 1.25, arrow: false });
  outs.forEach(([a, b], i) => {
    const x = X0 + i * (ow + 0.1);
    H.ln(s, x + ow / 2, y3 - 0.1, x + ow / 2, y3, { color: C.navy, w: 1.25 });
    H.box(s, [{ text: a, options: { bold: true, color: C.greenD, fontSize: 7.2, breakLine: true } }, { text: b, options: { fontSize: 6.3 } }], x, y3, ow, 0.52, { fill: "E7F4E2", line: C.greenD, radius: 0.05, margin: [2, 3, 2, 3] });
  });
  H.t(s, "Batas sistem: dari fat pit PKS sampai titik serah 20 kV; efluen terolah memakai kolam polishing PKS yang sudah ada.", X0, 5.1, XW, 0.15, { fontSize: 6.2, italic: true, color: C.slate });
  // kartu bawah
  const cw = (XW - 0.2) / 3, cy = 5.3, ch = 1.65;
  const cards = [["Pengguna sasaran", ["PKS independen 45–60 t TBS/jam yang membakar solar di luar jam olah (terukur ≥ 2,0 L/t TBS), dengan jaringan 20 kV ≤ 2 km.", "±" + fmt(D.pasar.rows[2].sets, 0) + " PKS di Sumatera dan Kalimantan (SAM); pembeli: PKS, PLN, pembeli karbon."]],
                 ["Proposisi nilai (PKS 60 t/jam)", ["Modal PKS USD 0; kontrak 20 tahun; operator menjamin kinerja.", "Biaya POME USD " + fmt(pk.per_t.D, 2) + " vs " + fmt(pk.per_t.A, 2) + "/t TBS bila memakai kolam (−" + fmt(pk.save_pct * 100, 1) + "%); emisi metana −96%.", "Efluen tetap memenuhi syarat aplikasi lahan."]],
                 ["Pembeda dari praktik saat ini", ["Layanan, bukan proyek rekayasa sekali jadi.", "Reaktor kecil: HRT 5 hari (kolam tertutup 25–40 hari), plot 0,38–0,5 ha.", "Tangki baut dan skid kontainer: dapat dipindah; pasang ±10 bulan."]]];
  cards.forEach(([h, ls], i) => {
    const x = X0 + i * (cw + 0.1);
    H.rect(s, x, cy, cw, ch, { fill: C.white, line: C.line, radius: 0.05 });
    H.t(s, h, x + 0.08, cy + 0.06, cw - 0.16, 0.2, { fontFace: FONT_H, fontSize: 8.2, bold: true, color: C.navy, valign: "middle" });
    H.t(s, ls.map((q, j) => ({ text: q, options: { bullet: { indent: 8 }, breakLine: j < ls.length - 1, paraSpaceAfter: 2 } })), x + 0.08, cy + 0.3, cw - 0.16, ch - 0.34, { fontSize: 6.9 });
  });
  H.src(s, "neraca proses Rev 2 (process/outputs/results.json; tier 60 t/jam), model 3D tim, Model Keputusan PKS, research/R3 dan R6. Angka aliran 60 t/jam diskalakan linier dari modul acuan 45 t/jam (HRT dan SRT identik).", "GFS baja berlapis kaca; HRT/SRT waktu tinggal hidraulik/lumpur; SAM pasar yang dapat dilayani; FCI biaya modal tetap; IRR laju pengembalian internal; η efisiensi.");
  s.addNotes("Konsep. Urutan: POME 85 °C dari fat pit → praolah → reaktor kontak 55 °C → degasser dan settler (lumpur kembali) → pemurnian biogas → penampung → genset → listrik ke PKS dan PLN. Tabel skala menunjukkan bahwa modul 30 dan 45 t/jam belum layak pada asumsi dasar; 60 t/jam layak tipis.");
};
