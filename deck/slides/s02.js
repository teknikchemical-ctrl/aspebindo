// Slide 2: Latar belakang dan masalah
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H, NF } = L; const P = D.pesaing, k = D.keu;
  const s = H.slide(2, "Metana POME dari ±1.150 PKS lepas ke udara karena {{modal dan risiko kinerja}}, bukan karena teknologinya belum ada",
    "Latar belakang. SCQA: situasi (1.300 PKS, hanya 11% menangkap metana), komplikasi (kolam terbuka ≈ 26 juta tCO2e/tahun; biogas milik sendiri mahal dan berisiko), pertanyaan, jawaban (layanan BOO).");
  // ---- SCQA
  const q = [["SITUASI", "±1.150 PKS", "dari ±1.300 PKS belum menangkap metana POME (±150 juta m³ POME per tahun)", C.navy], ["KOMPLIKASI", "≈ 26 juta tCO₂e", "per tahun lepas dari kolam; biogas milik sendiri USD 3,5–4,0 juta per set dan berisiko", C.royal],
             ["PERTANYAAN", "?", "Bagaimana PKS menangkap metana tanpa modal dan tanpa risiko kinerja, dengan biaya tidak melebihi kolam?", C.teal], ["JAWABAN", "USD 0 modal PKS", "Layanan BOO: set termofilik modular dibayar per t TBS dan per kWh (slide 3–7)", C.green]];
  q.forEach(([a, b, t, c], i) => {
    const x = 0.45 + i * 3.14, w = 3.04;
    H.hdr(s, a, x, 1.25, w, { fill: c, h: 0.22, fs: 9 });
    H.rect(s, x, 1.47, w, 0.78, { fill: C.white, line: c, radius: 0.04, lw: 1 });
    H.t(s, b, x + 0.1, 1.49, w - 0.2, 0.3, { fontFace: FONT_H, fontSize: 14, bold: true, color: c, valign: "middle" });
    H.t(s, t, x + 0.1, 1.8, w - 0.2, 0.44, { fontSize: 8.8 });
  });
  // ---- pohon masalah empat kolom
  const Y = 2.33, cw = [2.45, 2.2, 4.0, 3.45], gap = 0.1; const cx = [0.45]; for (let i = 0; i < 3; i++) cx.push(cx[i] + cw[i] + gap);
  ["Rumusan masalah", "Sub-masalah", "Akar masalah (terukur)", "Arah solusi"].forEach((t, i) => H.hdr(s, t, cx[i], Y, cw[i], { fill: i === 3 ? C.green : (i === 2 ? C.royal : C.navy), h: 0.26 }));
  H.box(s, "Bagaimana PKS independen dapat menangkap metana POME tanpa modal dan tanpa menanggung risiko kinerja, dengan biaya tidak melebihi kolam?", cx[0], Y + 0.3, cw[0], 1.84, { fs: 10, bold: true, color: C.navy, fill: C.white, line: C.navy, lw: 1.5, radius: 0.04 });
  const rows = [["Teknologi", ["Kolam terbuka: 100% CH₄ lepas, " + fmt(D.lca.base, 0) + " tCO₂e/tahun per PKS 60 t/jam", "Reaktor konvensional: HRT 25–40 hari, lahan luas"], "Reaktor kontak termofilik: HRT 5 hari, tangki GFS dibaut"],
                ["Ekonomi", ["Modal USD 3,5–4,0 juta per set; kinerja tidak dijamin", "Pendapatan kecil: tarif 9,81 USc/kWh, karbon USD 3–5/t"], "Layanan BOO: modal PKS nol; pendapatan jasa + listrik + karbon"],
                ["Regulasi dan pasar", ["Belum ada mandat penangkapan metana (ISPO bioenergi 2027)", "Izin jual listrik dan PJBL lambat"], "Kontrak jasa energi; gerbang izin sebelum modal"],
                ["Organisasi", ["PKS bukan operator biogas (±442 PKS tanpa kebun)", "Solar dan POME tidak terukur per PKS"], "Operator menjamin kinerja; data solar diukur pada gerbang G0"]];
  rows.forEach(([a, b, c], i) => {
    const y = Y + 0.3 + i * 0.47, h = 0.43;
    H.box(s, a, cx[1], y, cw[1], h, { fs: 10, bold: true, color: C.navy, fill: C.tealL, line: C.teal, radius: 0.04 });
    H.box(s, b.map((x, j) => ({ text: x, options: { bullet: { indent: 8 }, breakLine: j < b.length - 1 } })), cx[2], y, cw[2], h, { fs: 8.5, align: "left", fill: C.white, line: C.royal, radius: 0.04, margin: [1, 5, 1, 5] });
    H.box(s, c, cx[3], y, cw[3], h, { fs: 9, align: "left", fill: C.greenL, line: C.green, radius: 0.04, margin: [1, 6, 1, 6] });
    H.ln(s, cx[0] + cw[0], Y + 1.22, cx[1], y + h / 2, { color: C.slate, w: 1, arrow: false }); H.ln(s, cx[1] + cw[1], y + h / 2, cx[2], y + h / 2, { color: C.slate, w: 1 }); H.ln(s, cx[2] + cw[2], y + h / 2, cx[3], y + h / 2, { color: C.slate, w: 1 });
  });
  // ---- 5 mengapa
  const Y2 = 4.62;
  H.hdr(s, "5 Mengapa: dari gejala ke akar", 0.45, Y2, 5.55, { fill: C.navy, h: 0.26 });
  const wh = ["Metana POME tidak ditangkap → tidak ada reaktor biogas di PKS.", "Mengapa? Modal USD 3,5–4,0 juta per set tidak sepadan dengan imbal hasil.", "Mengapa? Pendapatan listrik dan karbon kecil, risiko kinerja ditanggung PKS.", "Mengapa? PKS bukan operator biogas; tidak ada penjamin kinerja.", "Akar: teknologi dijual sebagai proyek sekali jadi, bukan layanan modular yang dijamin operator."];
  wh.forEach((t, i) => { const y = Y2 + 0.28 + i * 0.27; H.box(s, i === 4 ? "A" : String(i + 1), 0.45, y, 0.28, 0.24, { fs: 9, bold: true, color: C.white, fill: i === 4 ? C.green : C.navy, line: null, radius: 0.04, margin: 0, font: FONT_H }); H.box(s, t, 0.78, y, 5.22, 0.24, { fs: 8.5, align: "left", fill: i === 4 ? C.greenL : C.white, line: i === 4 ? C.green : C.line, radius: 0.04, margin: [0, 5, 0, 5], bold: i === 4 }); });
  // ---- matriks keputusan
  H.hdr(s, "Pemilihan konsep: matriks keputusan berbobot (skor 1–5)", 6.15, Y2, 6.75, { fill: C.navy, h: 0.26 });
  const nm = ["A  Status quo kolam", "B  Lagun tertutup (milik PKS)", "C  CSTR mesofilik (milik PKS)", "D  Biometana BOOT klaster", "E  UASB/IC", "F  AnMBR", "G  Kontak termofilik BOO (usulan)"];
  const heat = ["F6CFC8", "FBE3BE", "FFF3C8", "DDF0CC", "BDE5AE"];
  const head = ["Alternatif"].concat(P.crit.map((c, i) => "K" + (i + 1) + " " + Math.round(c[1] * 100) + "%")).concat(["Skor", "% peringkat 1"]);
  const tb = [head]; P.rows.forEach((r, i) => { const g = i === 6; tb.push([{ text: nm[i], options: { bold: g, align: "left" } }].concat(r.scores.map((x) => ({ text: fmt(x, 1), options: { align: "center", fill: { color: heat[Math.max(0, Math.min(4, Math.round(x) - 1))] }, bold: g } }))).concat([{ text: fmt(r.total, 2), options: { bold: true, align: "center", color: g ? C.white : C.ink, fill: { color: g ? C.green : C.white } } }, { text: fmt(P.wins[i], 0) + "%", options: { align: "center", bold: g } }])); });
  H.table(s, tb, 6.15, Y2 + 0.28, [2.3, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.45, 0.66], { fs: 7.3, rh: 0.19, margin: [1, 3, 1, 3] });
  H.t(s, "K1 biaya POME bagi PKS · K2 modal PKS · K3 risiko kinerja ditanggung PKS · K4 referensi di Indonesia · K5 lahan dan waktu bangun · K6 penangkapan metana · K7 dapat dipindah · % peringkat 1: dari 20.000 variasi bobot (G tetap peringkat 1 pada uji ±50% tiap bobot).", 0.45, 6.37, 12.4, 0.12, { fontSize: 6.3, color: C.slate });
  H.concl(s, "Rumusan terukur: turunkan emisi metana ≥ 90% (≈ " + fmt(D.lca.net_total / 1000, 0) + " ribu tCO₂e/tahun per PKS 60 t TBS/jam) tanpa modal PKS, dengan biaya POME ≤ kolam (USD " + fmt(D.pks.per_t.A, 2) + "/t TBS) dan DSCR proyek ≥ 1,30.", "Rumusan masalah");
  H.src(s, "Trase/SEI-PCS 2024; IOP/ERL; GAPKI 2026; RTM Berita 2024; PASPI/BRIN; Perpres 16/2025 dan 112/2022; model tim (neraca proses Rev 2, Model Keputusan PKS); skor K2–K7 penilaian tim (research/R3, R6).", "PKS pabrik kelapa sawit; TBS tandan buah segar; BOO bangun-miliki-operasikan; BOOT bangun-miliki-operasikan-alihkan; HRT waktu tinggal hidraulik; PJBL perjanjian jual beli listrik; GFS baja berlapis kaca; DSCR rasio cakupan layanan utang.");
};
