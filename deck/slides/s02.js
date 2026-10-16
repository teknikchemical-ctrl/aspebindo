// Slide 2: Latar belakang dan masalah
module.exports = (pres, H, L) => {
  const { C, D, fmt, pct, FONT_H, FONT_B, NF, NF1 } = L;
  const s = H.slide(2, "Latar belakang dan masalah", "Masalah: ±1.150 PKS melepas metana POME karena modal dan risiko kinerja, bukan karena teknologinya belum ada; layanan BOO modular menjadi alternatif terpilih dari tujuh opsi");
  const base = D.lca.base, dsl = D.pks.diesel_cost;
  // ---------------- kolom kiri: SCQA
  H.sec(s, "SCQA: dari situasi ke jawaban", 0.4, 1.18, 3.3);
  const q = [["S", "Situasi", "±1.300 PKS menghasilkan ±150 juta m³ POME per tahun; hanya ±11% PKS yang menangkap metana (Malaysia ±38%)."],
             ["K", "Komplikasi", "Kolam terbuka melepas ±26 juta tCO₂e/tahun. Biogas milik sendiri butuh USD 3,5–4,0 juta per set, berisiko, dan terkunci pada satu lokasi."],
             ["P", "Pertanyaan", "Bagaimana PKS menangkap metana tanpa modal dan tanpa menanggung risiko kinerja, dengan biaya tidak melebihi kolam?"],
             ["J", "Jawaban", "Layanan BOO: set biogas termofilik modular, dipasang dengan baut, dapat dipindah, dibayar per t TBS dan per kWh."]];
  q.forEach(([a, b, t], i) => {
    const y = 1.45 + i * 0.43;
    H.box(s, a, 0.4, y, 0.22, 0.38, { fs: 9, bold: true, color: C.white, fill: i === 3 ? C.greenD : C.navy, line: null, radius: 0.04, margin: 0, font: FONT_H });
    H.t(s, [{ text: b + ": ", options: { bold: true, color: C.navy } }, { text: t }], 0.67, y - 0.01, 3.03, 0.42, { fontSize: 7.3 });
  });
  // besaran masalah
  H.sec(s, "Besaran masalah", 0.4, 3.2, 3.3);
  const tiles = [["±1.150", "PKS tanpa penangkapan metana (±88,5% dari ±1.300)"], ["≈ 26 juta", "tCO₂e/tahun metana kolam nasional (0,119 tCO₂e/t TBS × ±250 juta t TBS)"],
                 [fmt(base, 0), "tCO₂e/tahun per PKS 60 t TBS/jam (AMS-III.H, UF 0,89)"], ["USD " + fmt(dsl / 1e6, 2) + " juta", "per tahun untuk listrik solar yang dapat digantikan (2,0 L/t TBS)"]];
  tiles.forEach(([b, t], i) => {
    const x = 0.4 + (i % 2) * 1.67, y = 3.45 + Math.floor(i / 2) * 0.57;
    H.rect(s, x, y, 1.63, 0.53, { fill: C.white, line: C.line, radius: 0.04 });
    H.t(s, b, x + 0.06, y + 0.02, 1.52, 0.2, { fontFace: FONT_H, fontSize: 10.5, bold: true, color: C.royal, valign: "middle" });
    H.t(s, t, x + 0.06, y + 0.22, 1.52, 0.3, { fontSize: 6.3, color: C.ink });
  });
  // pemangku kepentingan
  H.sec(s, "Pemangku kepentingan dan insentif", 0.4, 4.62, 3.3);
  H.table(s, [["Pihak", "Insentif", "Kekhawatiran"],
    ["Operator PKS", "biaya ≤ kolam, izin aman", "kinerja, kontrak 20 tahun"], ["Pemodal dan bank", "DSCR ≥ 1,30, agunan", "teknologi baru, nilai sisa"], ["PLN (pembeli)", "listrik EBT ≤ 3 MW", "plafon harga, PJBL"],
    ["Regulator", "emisi NDC, efluen patuh", "izin, pemantauan"], ["Pemasok teknologi", "volume proyek, referensi", "garansi kinerja"], ["Masyarakat sekitar", "bau, air, kerja lokal", "gas, kebocoran efluen"]],
    0.4, 4.87, 3.3, [0.9, 1.25, 1.15], { fs: 6.5, rh: 0.2, hrh: 0.2 });
  // ---------------- kolom tengah: pohon isu
  H.sec(s, "Pohon isu (MECE): mengapa metana tidak ditangkap?", 3.85, 1.18, 5.25);
  const rootY = 1.5, rootH = 2.2;
  H.box(s, "Metana POME terlepas dan solar tetap dibakar di ±1.150 PKS", 3.85, rootY + 0.55, 1.05, 1.1, { fs: 7.5, bold: true, color: C.white, fill: C.navy, line: null, radius: 0.05 });
  const br = [["Teknologi", [["Kolam terbuka: " + fmt(base, 0) + " tCO₂e/tahun per PKS 60 t/jam lepas ke udara", "g"], ["Reaktor konvensional: HRT 25–40 hari, lahan luas, H₂S 2.900 ppm", "a"]]],
              ["Ekonomi", [["Modal USD 3,5–4,0 juta per set milik sendiri; kinerja tak dijamin", "a"], ["Pendapatan kecil: tarif PLN 9,81 USc/kWh; karbon USD 3–5/t", "a"]]],
              ["Regulasi", [["Belum ada mandat penangkapan metana (ISPO bioenergi 2027)", "a"], ["Izin jual listrik dan PJBL lambat; struktur BOO belum pasti", "k"]]],
              ["Perilaku dan organisasi", [["POME dianggap limbah; solar dan POME tidak terukur per PKS", "g"], ["Keahlian biogas terbatas di ±442 PKS tanpa kebun", "a"]]]];
  const LH = 0.262, LP = 0.275;
  br.forEach(([nm, lv], i) => {
    const y0 = rootY + i * 2 * LP + 0.0;
    const by = y0 + LP - 0.17;
    H.box(s, nm, 5.1, by, 1.05, 0.34, { fs: 7.5, bold: true, color: C.navy, fill: C.sky, line: C.mid, radius: 0.05 });
    H.path(s, [[4.9, rootY + 1.1], [5.0, rootY + 1.1], [5.0, by + 0.17], [5.1, by + 0.17]], { color: C.slate, w: 1, arrow: false });
    lv.forEach(([t, k], j) => {
      const ly = y0 + j * LP;
      const st = k === "a" ? { fill: C.navy, color: C.white, line: C.navy } : k === "k" ? { fill: C.sky, color: C.ink, line: C.mid } : { fill: C.white, color: C.ink, line: C.mid };
      H.box(s, t, 6.35, ly, 2.75, LH, Object.assign({ fs: 6.6, align: "left", radius: 0.04, margin: [0, 4, 0, 4] }, st));
      H.path(s, [[6.15, by + 0.17], [6.25, by + 0.17], [6.25, ly + LH / 2], [6.35, ly + LH / 2]], { color: C.slate, w: 1, arrow: false });
    });
  });
  // legenda
  [["Akar masalah", C.navy, C.white], ["Kendala", C.sky, C.ink], ["Gejala / akibat", C.white, C.ink]].forEach(([t, f, c], i) => {
    H.box(s, t, 6.35 + i * 0.93, rootY + 8 * 0.275 + 0.0, 0.88, 0.16, { fs: 6.2, color: c, fill: f, line: C.mid, radius: 0.03, margin: 0 });
  });
  // 5 Mengapa
  H.sec(s, "5 Mengapa (akar masalah)", 3.85, 3.97, 2.3);
  const wh = [["Masalah", "Metana POME PKS independen tidak ditangkap"], ["1", "Tidak ada reaktor biogas di PKS."], ["2", "Modal USD 3,5–4,0 juta per set tidak sepadan dengan imbal hasil."],
              ["3", "Pendapatan listrik dan karbon kecil; risiko kinerja ada di PKS."], ["4", "PKS bukan operator biogas dan tidak ada penjamin kinerja."], ["5", "Teknologi dijual sebagai proyek sekali jadi, bukan layanan modular yang dijamin operator."]];
  wh.forEach(([n, t], i) => {
    const y = 4.22 + i * 0.335;
    const last = i === wh.length - 1;
    H.box(s, n === "Masalah" ? "M" : n, 3.85, y, 0.24, 0.3, { fs: 7.5, bold: true, color: C.white, fill: last ? C.greenD : (i === 0 ? C.red : C.navy), line: null, radius: 0.04, margin: 0, font: FONT_H });
    H.box(s, t, 4.12, y, 2.03, 0.3, { fs: 6.6, align: "left", fill: last ? "E7F4E2" : C.white, line: last ? C.greenD : C.line, radius: 0.04, margin: [0, 4, 0, 4], bold: last });
    if (i < wh.length - 1) H.ln(s, 3.97, y + 0.3, 3.97, y + 0.335, { color: C.slate, w: 0.75 });
  });
  // Ishikawa
  H.sec(s, "Diagram Ishikawa", 6.3, 3.97, 2.8);
  const sy = 5.28;
  H.ln(s, 6.35, sy, 8.55, sy, { color: C.navy, w: 2 });
  H.box(s, "Metana POME tidak tertangkap", 8.55, sy - 0.32, 0.55, 0.64, { fs: 6.3, bold: true, color: C.white, fill: C.red, line: null, radius: 0.04, margin: 1 });
  const bones = [["Teknologi", ["HRT panjang", "H₂S, pasir, minyak"], 6.8, -1], ["Ekonomi", ["CAPEX tinggi", "tarif, karbon rendah"], 7.4, -1], ["Regulasi", ["tanpa mandat", "izin jual listrik"], 8.0, -1],
                 ["Infrastruktur", ["jaringan 20 kV jauh", "lahan terbatas"], 6.8, 1], ["Operasional", ["beban TBS 50–80%", "musiman ±25%"], 7.4, 1], ["Perilaku", ["POME = limbah", "tanpa data terukur"], 8.0, 1]];
  bones.forEach(([nm, cs, x, dir]) => {
    const xs = x - 0.3, yEnd = dir < 0 ? 4.5 : 6.05;
    H.ln(s, xs, yEnd, x, sy, { color: C.mid, w: 1.25, arrow: false });
    H.box(s, nm, xs - 0.31, dir < 0 ? 4.22 : 6.07, 0.62, 0.17, { fs: 6.2, bold: true, color: C.navy, fill: C.sky, line: C.mid, radius: 0.03, margin: 0 });
    cs.forEach((c, k) => {
      const yy = dir < 0 ? 4.55 + k * 0.28 : 5.5 + k * 0.28; const frac = dir < 0 ? (yy - 4.5) / 0.78 : (6.05 - yy) / 0.77;
      H.t(s, c, xs + 0.3 * frac + 0.05, yy, 0.58, 0.26, { fontSize: 5.6, color: C.ink });
    });
  });
  // ---------------- kolom kanan: pohon solusi
  H.sec(s, "Pohon solusi dan alternatif (A–G)", 9.25, 1.18, 3.7);
  H.box(s, "Tangkap metana POME", 9.25, 1.55, 0.78, 0.5, { fs: 6.8, bold: true, color: C.white, fill: C.navy, line: null, radius: 0.04 });
  H.box(s, "Teknologi", 10.2, 1.45, 0.62, 0.22, { fs: 6.8, bold: true, color: C.navy, fill: C.sky, line: C.mid, radius: 0.03, margin: 0 });
  H.box(s, "Penyampaian", 10.2, 1.95, 0.62, 0.22, { fs: 6.5, bold: true, color: C.navy, fill: C.sky, line: C.mid, radius: 0.03, margin: 0 });
  H.path(s, [[10.03, 1.8], [10.11, 1.8], [10.11, 1.56], [10.2, 1.56]], { color: C.slate, w: 1, arrow: false });
  H.path(s, [[10.03, 1.8], [10.11, 1.8], [10.11, 2.06], [10.2, 2.06]], { color: C.slate, w: 1, arrow: false });
  const lt = [["A Status quo", 0], ["B Lagun tertutup", 0], ["C CSTR mesofilik", 0], ["E UASB/IC", 0], ["F AnMBR", 0], ["G Kontak termofilik", 1]];
  lt.forEach(([t, g], i) => H.box(s, t, 10.95 + (i % 3) * 0.67, 1.36 + Math.floor(i / 3) * 0.24, 0.65, 0.22, { fs: 5.7, color: g ? C.white : C.ink, bold: !!g, fill: g ? C.greenD : C.white, line: g ? C.greenD : C.mid, radius: 0.03, margin: 0 }));
  [["Milik PKS (EPC): B, C, E, F", 0], ["Layanan BOO: G", 1], ["BOOT biometana klaster: D", 0]].forEach(([t, g], i) => H.box(s, t, 10.95 + i * 0.67, 1.9, 0.65, 0.3, { fs: 5.7, color: g ? C.white : C.ink, bold: !!g, fill: g ? C.greenD : C.white, line: g ? C.greenD : C.mid, radius: 0.03, margin: 0 }));
  H.path(s, [[10.82, 1.56], [10.95, 1.56]], { color: C.slate, w: 1, arrow: false }); H.path(s, [[10.82, 2.06], [10.95, 2.06]], { color: C.slate, w: 1, arrow: false });
  // matriks keputusan
  H.sec(s, "Matriks keputusan berbobot (skor 1–5)", 9.25, 2.27, 3.7);
  const nm = ["A Status quo kolam", "B Lagun tertutup (PKS)", "C CSTR mesofilik (PKS)", "D Biometana BOOT klaster", "E UASB/IC", "F AnMBR", "G Kontak termofilik BOO"];
  const heat = ["F2C4BC", "F8DDB8", "FFF1C2", "DCEEC6", "B9E2AA"];
  const head = ["Alternatif"].concat(D.pesaing.crit.map((c, i) => "K" + (i + 1) + "\n" + Math.round(c[1] * 100) + "%")).concat(["Skor"]);
  const rows = [head];
  D.pesaing.rows.forEach((r, i) => {
    const g = i === D.pesaing.rows.length - 1;
    rows.push([{ text: nm[i], options: { bold: g, align: "left" } }].concat(r.scores.map((x) => ({ text: fmt(x, 1), options: { align: "center", fill: { color: heat[Math.max(0, Math.min(4, Math.round(x) - 1))] }, bold: g } }))).concat([{ text: fmt(r.total, 2), options: { bold: true, align: "center", color: g ? C.white : C.ink, fill: { color: g ? C.greenD : C.white } } }]));
  });
  H.table(s, rows, 9.25, 2.52, 3.7, [1.17, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.36], { fs: 6.2, rh: 0.205, hrh: 0.3, margin: [0, 2, 0, 2] });
  H.t(s, "K1 biaya POME bagi PKS (USD/t TBS; dari model, 3,14 untuk A dan 3,00 untuk G) · K2 modal PKS · K3 risiko kinerja ditanggung PKS · K4 kematangan dan referensi di Indonesia · K5 lahan dan waktu bangun · K6 penangkapan metana dan bau · K7 dapat dipindah. Skor K2–K7: penilaian tim dari R3/R6 (subjektif).",
    9.25, 4.52, 3.7, 0.5, { fontSize: 5.8, color: C.slate });
  // sensitivitas bobot
  H.sec(s, "Uji sensitivitas bobot (20.000 variasi)", 9.25, 5.02, 3.7);
  const wins = D.pesaing.wins;
  s.addChart(pres.charts.BAR, [{ name: "Peringkat 1 (%)", labels: ["A", "B", "C", "D", "E", "F", "G"], values: wins }], {
    x: 9.2, y: 5.25, w: 2.2, h: 1.1, barDir: "col", chartColors: [C.mid, C.mid, C.mid, C.mid, C.mid, C.mid, C.greenD], showValue: true, dataLabelFormatCode: NF, dataLabelFontSize: 7, dataLabelFontFace: FONT_B, dataLabelPosition: "outEnd",
    catAxisLabelFontSize: 7, valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, valAxisMaxVal: 100, valAxisMinVal: 0, catAxisLabelFontFace: FONT_B, varyColors: true, objectName: "grafik-bobot" });
  H.t(s, [{ text: "G peringkat 1 pada " + fmt(D.pesaing.rankD_p * 100, 0) + "% variasi bobot", options: { bold: true, color: C.greenD, breakLine: true } },
          { text: "dan pada 7 dari 7 uji ±50% satu bobot. Pesaing terdekat: D biometana (" + fmt(wins[3], 0) + "%), yang menuntut klaster PKS dan offtake gas." }], 11.4, 5.3, 1.55, 1.05, { fontSize: 6.6 });
  // rumusan masalah
  H.box(s, "RUMUSAN MASALAH TERUKUR", 0.4, 6.42, 1.55, 0.58, { fs: 8, bold: true, color: C.white, fill: C.navy, line: null, radius: 0.04, font: FONT_H });
  H.box(s, [{ text: "Menurunkan emisi metana POME ≥ 90% (≈ " + fmt(D.lca.net_total / 1000, 0) + " ribu tCO₂e/tahun per PKS 60 t TBS/jam), tanpa modal PKS dan dengan biaya POME PKS tidak lebih tinggi daripada kolam (USD " + fmt(D.pks.per_t.A, 2) + "/t TBS), pada DSCR proyek ≥ 1,30. ", options: {} }, { text: "Jawaban: slide 3–7.", options: { bold: true, color: C.greenD } }],
    1.95, 6.42, 11.0, 0.58, { fs: 9, align: "left", fill: C.white, line: C.navy, lw: 1, radius: 0.04, margin: [2, 8, 2, 8] });
  H.src(s, "Trase/SEI-PCS 2024 (±1.300 PKS); IOP/Environ. Res. Lett. dan GAPKI 2026 (penangkapan metana); RTM Berita 2024 (Malaysia); PASPI/BRIN (POME); Perpres 16/2025 (ISPO); Perpres 112/2022 (tarif); model tim: neraca proses Rev 2, Model Keputusan PKS (research/R1–R6).", "PKS pabrik kelapa sawit; POME air limbah PKS; TBS tandan buah segar; BOO bangun-miliki-operasikan; BOOT bangun-miliki-operasikan-alihkan; HRT waktu tinggal hidraulik; PJBL perjanjian jual beli listrik; DSCR rasio cakupan layanan utang; MECE saling lepas dan menyeluruh; UASB/IC reaktor lumpur aktif aliran ke atas; AnMBR reaktor membran anaerob; CSTR tangki berpengaduk.");
  s.addNotes("Masalah. Akar masalah (5 Mengapa) adalah cara teknologi dijual: proyek rekayasa sekali jadi dengan modal dan risiko kinerja di PKS. Matriks keputusan: skor K1 dari model; K2–K7 penilaian tim, jadi diuji dengan 20.000 variasi bobot (Dirichlet di sekitar bobot dasar) dan uji ±50% satu bobot. Skor G tertinggi karena modal PKS nol, risiko dibawa operator, dan dapat dipindah; titik lemahnya kematangan (belum ada referensi di Indonesia).");
};
