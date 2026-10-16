// Deck pitch EIC 2026 (10 slide, Bahasa Indonesia). Semua angka dibaca dari keluaran model di repo ini.
// Jalankan: NODE_PATH=<node_modules> node deck/build_deck.js   (dari akar repo)
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL || "/root/.claude/skills/synced/1447d632-3db4-4ffa-8639-0456923eecc3_b47be9f3-76fa-4276-9bf3-c539adcfb469/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const ROOT = path.resolve(__dirname, "..");
const S = JSON.parse(fs.readFileSync(path.join(ROOT, "finance/outputs/summary.json"), "utf8"));
const R = JSON.parse(fs.readFileSync(path.join(ROOT, "process/outputs/results.json"), "utf8"));
const OUT = path.join(__dirname, "BG_Pitch_Deck_EIC2026.pptx");

// ---------- angka (format Indonesia)
const id = (v, d = 0) => v.toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
const M = (v, d = 2) => id(v / 1e6, d);
const P = (v, d = 1) => id(v * 100, d);
const seg = Object.fromEntries(S.segments.map(g => [g.name.slice(0, 2), g]));
const sc = S.scenarios;
const N = {
  fci: M(S.FCI, 1), npv: M(S.NPV), irr: P(S.IRR), irrEq: P(S.IRR_eq), pbp: id(S.PBP, 1), dscr: id(S.DSCR_min, 2),
  pnpv: P(S.P_NPV_pos, 0), wacc: P(S.WACC, 1), lcoe: id(S.LCOE, 3),
  A: id(S.mill.A.per_t, 2), D: id(S.mill.D.per_t, 2), B: id(S.mill.B.per_t, 2), C: id(S.mill.C.per_t, 2),
  save: P(S.mill_saving_pct, 0), saveYr: id((S.mill.A.annual - S.mill.D.annual) / 1e3, 0),
  fmin: id(S.fee_window.fee_min, 2), fmax: id(S.fee_window.fee_max, 2),
  er: id(S.ER_t, 0), cap: id(S.energy_split.captive_GWh, 2), exp: id(S.energy_split.export_GWh, 2),
  net: id(R.year.GWh_net, 2), dieselL: id(S.energy_split.captive_GWh * 0.30 * 1e6, 0), dieselK: id(S.energy_split.captive_GWh * 0.30 * 1e3, 0),
  tam: id(S.market.sets_TAM, 0), tamUSD: id(S.market.TAM / 1e9, 2), sam: id(S.market.sets_SAM, 0), samUSD: id(S.market.SAM / 1e6, 0),
  som: id(S.market.sets_SOM, 0), somUSD: id(S.market.SOM / 1e6, 1),
  fleetNPV: M(S.fleet_NPV), fleetIRR: P(S.fleet_IRR), fleetPeak: M(S.fleet_peak, 1),
  reloc: M(S.relocation.reloc), strand: M(S.relocation.stranded),
  shF: P(S.share_fee, 0), shE: P(S.share_el, 0), shC: P(S.share_c, 0),
  biogas: id(R.nominal.biogas_Nm3d, 0), ch4: P(R.nominal.ch4_frac, 0), pnet: id(R.energy.P_net, 0),
};

// ---------- tema
const THEME = {
  name: "EIC Sawit Biogas", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "1A2B26", lt1: "FFFFFF", dk2: "1F4E3D", lt2: "F3F1EA", accent1: "2E7D6B", accent2: "D99A2B",
    accent3: "B5462F", accent4: "4E87A0", accent5: "8A9A5B", accent6: "6B6F6C", hlink: "2E7D6B", folHlink: "1F4E3D" },
};
const HEX = THEME.colors;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,33 x 7,5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Biogas-as-a-Service untuk PKS - EIC 2026";
pres.author = "Tim EIC 2026";
const C = pres.SchemeColor;
const W = 13.333;

// ---------- layout
pres.defineSlideMaster({
  title: "COVER", background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.55, y: 1.35, w: 6.3, h: 1.5, fontSize: 38, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "KONTEN", background: { color: C.background1 },
  margin: [0.4, 0.45, 0.6, 0.45],
  objects: [
    { text: { text: "EIC 2026  |  Business Plan\nSubtema 3: Ekonomi Sirkular", options: { x: 10.35, y: 0.18, w: 2.55, h: 0.42, fontSize: 9, color: C.accent6, align: "right", margin: 0, isTextBox: true } } },
    { placeholder: { options: { name: "kicker", type: "body", x: 0.45, y: 0.2, w: 9.5, h: 0.26, fontSize: 11, bold: true, color: C.accent1, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.45, y: 0.46, w: 12.4, h: 0.86, fontSize: 21, bold: true, color: C.text2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.45, y: 7.08, w: 0.45, h: 0.28, fontSize: 10, color: C.background1, align: "center" },
});

// ---------- pembantu
const NAV = ["Masalah", "Solusi", "Inovasi", "Pasar", "Model bisnis", "Keuangan", "Dampak", "Skala", "Penutup"];
let nobj = 0;
const on = () => "o" + (++nobj);
function nav(s, idx) {
  const x0 = 0.45, w = 1.3, g = 0.04;
  NAV.forEach((t, i) => {
    const act = i === idx;
    s.addText(t, { x: x0 + i * (w + g), y: 7.08, w, h: 0.28, fontSize: 9.5, bold: act, align: "center", valign: "middle", margin: 0,
      color: act ? C.background1 : C.text2, fill: { color: act ? C.text2 : C.background2 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06,
      line: { color: act ? C.text2 : C.background2 }, isTextBox: true, objectName: on() });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 12.45, y: 7.08, w: 0.45, h: 0.28, rectRadius: 0.06, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: on() });
}
function concl(s, text, y = 6.2) {
  s.addText("Kesimpulan", { x: 0.45, y, w: 1.45, h: 0.5, fontSize: 12, bold: true, color: C.background1, fill: { color: C.text2 }, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: on() });
  s.addText(text, { x: 1.9, y, w: 11.0, h: 0.5, fontSize: 11.5, color: C.text1, fill: { color: C.background2 }, valign: "middle", margin: [0, 10, 0, 10], isTextBox: true, objectName: on() });
}
function src(s, text) {
  s.addText("Sumber: " + text, { x: 0.45, y: 6.74, w: 12.45, h: 0.28, fontSize: 7.5, color: C.accent6, valign: "middle", margin: 0, isTextBox: true, objectName: on() });
}
function img(s, rel, x, y, w, pxw, pxh, h) {
  const hh = h || w * pxh / pxw;
  const ww = h ? h * pxw / pxh : w;
  s.addImage({ path: path.join(ROOT, rel), x, y, w: ww, h: hh, objectName: on() });
  return hh;
}
function card(s, x, y, w, h, head, body, col, opt = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: opt.fill || C.background1 }, line: { color: col, width: 1.25 }, objectName: on() });
  s.addText(head, { x: x + 0.12, y: y + 0.07, w: w - 0.24, h: 0.3, fontSize: opt.hs || 12, bold: true, color: col, margin: 0, valign: "top", isTextBox: true, objectName: on() });
  s.addText(body, { x: x + 0.12, y: y + 0.38, w: w - 0.24, h: h - 0.45, fontSize: opt.bs || 10.5, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: on(), paraSpaceAfter: 2 });
}
function stat(s, x, y, w, h, big, label, col, opt = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: opt.fill || C.background2 }, line: { color: opt.fill || C.background2 }, objectName: on() });
  s.addText(big, { x: x + 0.1, y: y + 0.06, w: w - 0.2, h: h * 0.52, fontSize: opt.bigs || 24, bold: true, color: col, fontFace: THEME.headFontFace, margin: 0, valign: "bottom", isTextBox: true, objectName: on() });
  s.addText(label, { x: x + 0.1, y: y + h * 0.58, w: w - 0.2, h: h * 0.4, fontSize: opt.ls || 9.5, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: on() });
}
function head(s, x, y, w, t, col) {
  s.addText(t, { x, y, w, h: 0.3, fontSize: 12.5, bold: true, color: col || C.text2, margin: 0, valign: "middle", isTextBox: true, objectName: on() });
}
function slide(sec, kicker, title) {
  const s = pres.addSlide({ masterName: "KONTEN", sectionTitle: sec });
  s.addText(kicker, { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" });
  return s;
}
const T = (t, o = {}) => ({ text: t, options: o });
const tblHead = (arr) => arr.map(t => T(t, { bold: true, color: HEX.lt1, fill: { color: HEX.dk2 }, align: "center", valign: "middle" }));

// =====================================================================================
// 1  SAMPUL
pres.addSection({ title: "Pembuka" });
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: "Pembuka" });
  s.addText("EIC 2026  |  Business Plan  |  Subtema 3: Ekonomi Sirkular", { x: 0.55, y: 0.5, w: 6.4, h: 0.3, fontSize: 11, color: C.accent2, bold: true, margin: 0, isTextBox: true, objectName: on() });
  s.addText("Biogas-as-a-Service untuk Pabrik Kelapa Sawit", { placeholder: "title" });
  s.addText("Set biogas kontak termofilik yang dapat dipindah. Limbah cair POME diubah menjadi listrik pengganti solar, listrik PLN dan kredit karbon, dan PKS tidak mengeluarkan modal sepeser pun.",
    { x: 0.55, y: 2.95, w: 6.2, h: 1.05, fontSize: 13.5, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: on() });
  const k = [[N.save + "%", "lebih murah bagi PKS\ndibanding kolam terbuka"], ["USD 0", "capex PKS\n(model BOO)"],
             [N.er, "tCO2e/th metana\ndihindari per set"], [N.irr + "%", "IRR proyek\n(WACC " + N.wacc + "%)"]];
  k.forEach(([b, l], i) => {
    const x = 0.55 + (i % 2) * 3.12, y = 4.2 + Math.floor(i / 2) * 1.05;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.0, h: 0.92, rectRadius: 0.06, fill: { color: C.accent1, transparency: 25 }, line: { color: C.accent1 }, objectName: on() });
    s.addText(b, { x: x + 0.12, y: y + 0.08, w: 1.45, h: 0.76, fontSize: 21, bold: true, fontFace: THEME.headFontFace, color: C.accent2, valign: "middle", margin: 0, fit: "shrink", isTextBox: true, objectName: on() });
    s.addText(l, { x: x + 1.55, y: y + 0.08, w: 1.4, h: 0.76, fontSize: 9.5, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: on() });
  });
  s.addText("Tim: [Nama tim]    Universitas: [Universitas]    Dosen pembimbing: [Nama]", { x: 0.55, y: 6.55, w: 6.3, h: 0.3, fontSize: 10, color: C.background2, margin: 0, isTextBox: true, objectName: on() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.05, y: 0.55, w: 5.85, h: 6.35, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: C.background1 }, objectName: on() });
  img(s, "cad/out/render/DIORAMA_produk.png", 7.15, 0.65, 0, 3200, 1800, 3.0);
  img(s, "cad/out/render/DIORAMA_lokasi.png", 7.15, 3.75, 0, 3200, 1800, 3.0);
  s.addNotes("Pembuka. Kami menawarkan pengolahan POME sebagai layanan (BOO): kami membangun, memiliki dan mengoperasikan set biogas di PKS, PKS membayar jasa per ton TBS dan membeli listrik lebih murah dari solarnya. Empat angka kunci: PKS hemat " + N.save + "% tanpa capex, " + N.er + " tCO2e/th dihindari, IRR proyek " + N.irr + "%. Gambar adalah model 3D dari desain kami.");
}

// 2  MASALAH
pres.addSection({ title: "Masalah" });
{
  const s = slide("Masalah", "Identifikasi masalah", "Masalah: PKS membuang POME ke kolam terbuka, sehingga metana terlepas, solar tetap dibakar dan biaya POME USD " + N.A + "/t TBS tidak terlihat");
  head(s, 0.45, 1.42, 4.1, "Akar masalah");
  const rc = [["Kolam terbuka melepas metana", "Hanya ~10% PKS di Indonesia menangkap metana (Malaysia 38%). ~1.150 PKS masih memakai kolam terbuka."],
              ["Listrik masih dari solar", "PKS jauh dari jaringan memakai ~3 L solar/t TBS untuk emplasmen, bengkel dan KCP; listrik solar USD 0,37-0,39/kWh."],
              ["PLTBg sendiri mahal dan berisiko", "Kolam tertutup atau tangki milik PKS butuh capex USD 2,6-3,0 juta dan menanggung risiko kinerja; aset terkunci di satu lokasi."],
              ["Tekanan regulasi dan pasar", "ISPO wajib bagi bioenergi per Maret 2027; nilai default EU RED untuk kolam terbuka hanya hemat 20% GRK; kasus pidana POME (PT SIPP)."]];
  rc.forEach(([h, b], i) => card(s, 0.45, 1.78 + i * 1.08, 4.1, 0.98, h, b, i < 2 ? C.accent3 : C.accent6, { bs: 10 }));
  // inti masalah
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.75, y: 2.35, w: 3.0, h: 2.6, rectRadius: 0.08, fill: { color: C.accent3 }, line: { color: C.accent3 }, objectName: on() });
  s.addText([T("Inti masalah", { fontSize: 12, bold: true, color: HEX.lt2, breakLine: true }), T("Limbah POME menjadi biaya dan emisi, bukan sumber energi", { fontSize: 17, bold: true, color: HEX.lt1, fontFace: "Cambria", breakLine: true }),
             T(" ", { fontSize: 6, breakLine: true }), T("PKS bergantung solar membayar USD " + N.A + "/t TBS untuk solar, kolam dan risiko lingkungan (USD " + id(S.mill.A.annual / 1e3, 0) + " rb/th per PKS 45 t/jam).", { fontSize: 10.5, color: HEX.lt1 })],
    { x: 4.9, y: 2.45, w: 2.7, h: 2.4, margin: 0, valign: "top", isTextBox: true, objectName: on() });
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 4.52, y: 3.48, w: 0.22, h: 0.34, fill: { color: C.accent6 }, line: { color: C.accent6 }, objectName: on() });
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 7.8, y: 3.48, w: 0.22, h: 0.34, fill: { color: C.accent6 }, line: { color: C.accent6 }, objectName: on() });
  // dampak
  head(s, 8.1, 1.42, 4.8, "Dampak per PKS 45 t TBS/jam (model kami)");
  stat(s, 8.1, 1.78, 2.35, 1.0, id(R.emissions.base_t, 0), "tCO2e/th dari kolam terbuka (AMS-III.H, GWP 28)", C.accent3, { bigs: 22 });
  stat(s, 10.55, 1.78, 2.35, 1.0, id(R.year.pome_m3, 0), "m³ POME/th (0,65 m³/t TBS)", C.accent3, { bigs: 22 });
  stat(s, 8.1, 2.88, 2.35, 1.0, "≤ 15%", "potensi biogas POME nasional yang dimanfaatkan", C.accent3, { bigs: 22 });
  stat(s, 10.55, 2.88, 2.35, 1.0, "165 MW", "PLTBg POME terpasang (84 unit) dari ~1.300 PKS", C.accent3, { bigs: 22 });
  s.addChart(pres.charts.BAR, [{ name: "PKS dengan penangkapan metana", labels: ["Indonesia", "Malaysia"], values: [10, 38] }], {
    x: 8.1, y: 4.0, w: 4.8, h: 2.05, barDir: "bar", chartColors: [HEX.accent3, HEX.accent1], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0\"%\"",
    dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt", showTitle: true, title: "Porsi PKS yang menangkap metana", titleFontSize: 11, titleFontFace: "+mn-lt", titleColor: HEX.dk2,
    catAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt", catAxisLabelColor: HEX.dk1, valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    showLegend: false, valAxisMaxVal: 45, varyColors: true, objectName: on() });
  concl(s, "Masalah POME bukan teknologi, tetapi modal dan risiko: PKS tahu metana bisa jadi listrik, tetapi tidak mau menanam USD 2,6-3,0 juta di aset yang terkunci. Kesenjangan ini terbesar di PKS yang masih membakar solar.");
  src(s, "Model neraca proses dan Keputusan PKS (repo ini); IOP Environ. Res. Lett. (<10% PKS ID); RTM Berita 2024 (170/446 PKS MY); PASPI/BRIN; GAPKI-EBTKE 2026; Perpres 16/2025; ISCC EU 205; Trase/SEI-PCS.");
  nav(s, 0);
  s.addNotes("Masalah. Empat akar masalah: kolam terbuka, ketergantungan solar, capex dan risiko PLTBg milik PKS, serta regulasi yang mengetat. Inti masalah: POME menjadi biaya dan emisi. Untuk PKS 45 t/jam yang bergantung solar, biaya status quo USD " + N.A + "/t TBS atau USD " + id(S.mill.A.annual / 1e3, 0) + " ribu per tahun, dan kolam melepas " + id(R.emissions.base_t, 0) + " tCO2e/th.");
}

// 3  SOLUSI
pres.addSection({ title: "Solusi" });
{
  const s = slide("Solusi", "Solusi yang diusulkan", "Solusi: reaktor kontak termofilik 55 °C dalam 3 tangki baut GFS mengubah POME menjadi " + N.net + " GWh/th listrik neto bagi PKS dan PLN");
  head(s, 0.45, 1.42, 7.95, "Alur proses: jalur cairan (atas) dan jalur gas (bawah)");
  const flow = (row, items, col) => items.forEach((t, i) => {
    const x = 0.45 + i * 1.62, y = 1.8 + row * 0.62;
    s.addText(t, { x, y, w: 1.42, h: 0.5, fontSize: 9.5, bold: true, align: "center", valign: "middle", margin: 2, color: C.background1, fill: { color: col },
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, isTextBox: true, objectName: on() });
    if (i < items.length - 1) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 1.44, y: y + 0.15, w: 0.16, h: 0.2, fill: { color: C.accent6 }, line: { color: C.accent6 }, objectName: on() });
  });
  flow(0, ["POME fat pit\n585 m³/hari", "Praolah PM-1\nsaring + pasir", "3 reaktor kontak\n55 °C, 980 m³", "Degasser vakum\nDG-301", "Settler lamella\nLS-301 → kolam"], C.accent4);
  flow(1, ["Biogas\nCH4 58%", "Pembersih H2S\nbio + karbon aktif", "Penampung gas\n2 jam", "Genset\n2 x 600 kWe", "Listrik PKS\n+ PLN 20 kV"], C.accent2);
  s.addText("Lumpur settler 585 m³/hari dikembalikan ke reaktor (SRT 12 hari); lumpur lebih → screw press → pupuk kebun.", { x: 0.45, y: 3.0, w: 7.95, h: 0.26, fontSize: 9.5, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: on() });
  img(s, "cad/out/render/PLANT_iso-depan.png", 0.45, 3.3, 0, 2200, 1400, 2.75);
  const cr = R.nominal.cod_routing_kgd;
  const ck = Object.keys(cr), cv = ck.map(k2 => cr[k2]);
  const cl = ["Metana", "H2S", "Biomassa", "Partikulat", "Efluen terlarut", "Gas terlarut"];
  s.addChart(pres.charts.DOUGHNUT, [{ name: "COD", labels: [cl[0], cl[2] + " + " + cl[3], cl[4], "Lain-lain"], values: [cv[0], cv[2] + cv[3], cv[4], cv[1] + cv[5]] }], {
    x: 4.85, y: 3.25, w: 3.55, h: 2.85, holeSize: 50, chartColors: [HEX.accent1, HEX.accent6, HEX.accent4, HEX.accent2], showPercent: true, showValue: false, dataLabelColor: HEX.lt1,
    dataLabelFontSize: 9, dataLabelFontFace: "+mn-lt", showTitle: true, title: "Neraca COD (kg/hari)", titleFontSize: 10.5, titleFontFace: "+mn-lt", titleColor: HEX.dk2,
    showLegend: true, legendPos: "r", legendFontSize: 8.5, legendFontFace: "+mn-lt", objectName: on() });
  head(s, 8.6, 1.42, 4.3, "Spesifikasi set 45 t TBS/jam (neraca proses Rev 2)");
  const rows = [["Umpan POME", "585 m³/hari, COD ~50 g/L"], ["Reaktor", "3 x 980 m³ tangki baut GFS, 55 °C"], ["HRT / SRT", "5 hari / 12 hari (resirkulasi lumpur)"],
    ["Pemisah", "Degasser vakum + settler lamella 81 m²"], ["Biogas", N.biogas + " Nm³/hari, CH4 " + N.ch4 + "%"], ["H2S", "2.868 → 21 ppm (bio-scrubber + karbon aktif)"],
    ["Pembangkit", "Genset 2 x 600 kWe, neto " + N.pnet + " kW"], ["Energi neto", N.net + " GWh/th (beban 75%, musiman ±25%)"], ["Lahan / angkut", "0,38 ha / 21 muatan kontainer"]];
  s.addTable(rows.map((r, i) => [T(r[0], { bold: true, color: HEX.dk2 }), T(r[1])]), { x: 8.6, y: 1.78, w: 4.3, colW: [1.35, 2.95], fontSize: 10, fontFace: "Calibri", color: HEX.dk1,
    border: { type: "solid", pt: 0.5, color: "D9D6CC" }, fill: { color: HEX.lt1 }, rowH: 0.31, margin: [2, 4, 2, 4], objectName: on() });
  card(s, 8.6, 4.72, 4.3, 1.17, "Efluen tetap ke kolam polishing", "Efluen settler (BOD ~1.540 mg/L) masuk kolam fakultatif lama lalu aplikasi lahan (batas 5.000 mg/L), sesuai Persetujuan Teknis PKS; tidak dibuang ke sungai.", C.accent4, { bs: 10 });
  concl(s, "Proses kontak menahan biomassa (SRT 12 hari) dalam reaktor kecil (HRT 5 hari), sehingga seluruh set muat di 0,38 ha, dapat dibaut dan dibongkar, dan metana terlarut ditangkap kembali oleh degasser.");
  src(s, "PFD BG-002 Rev 3, process/biogas_balance.py (model ADM1-lite kalibrasi), PermenLH 5/2014; desain dasar process/PROCESS_DESIGN_BASIS.md.");
  nav(s, 1);
  s.addNotes("Solusi. Alur: POME dari fat pit diolah awal, masuk 3 reaktor kontak termofilik, lalu degasser vakum dan settler lamella; lumpur dikembalikan ke reaktor. Biogas dibersihkan dari H2S, ditampung, lalu dibakar di 2 genset 600 kWe. Listrik dipakai PKS menggantikan solar, sisanya diekspor ke PLN.");
}

// 4  INOVASI
pres.addSection({ title: "Inovasi" });
{
  const s = slide("Inovasi", "Inovasi dan keunggulan unik", "Inovasi: satu-satunya opsi yang menggabungkan nol capex PKS, kinerja yang dijamin operator dan aset yang dapat dipindah");
  const u = [["1  Reaktor kecil, kinerja tinggi", "Kontak termofilik 55 °C: HRT 5 hari, bukan ~40 hari seperti kolam tertutup. Volume reaktor 2.940 m³ cukup untuk PKS 45 t/jam.", C.accent1],
             ["2  Dapat dipindah", "Tangki GFS dibaut dan peralatan di skid kontainer (21 muatan). Bila PKS tutup di tahun 8, set dipindah: NPV USD " + N.reloc + " juta, bukan USD " + N.strand + " juta terdampar.", C.accent1],
             ["3  Layanan, bukan penjualan alat", "BOO: PKS membayar USD 1,00/t TBS dan listrik USD 0,20/kWh (solar USD 0,37-0,39). Operator menanggung risiko biologis dan teknis.", C.accent2],
             ["4  Tiga aliran nilai dari satu limbah", "Listrik pengganti solar, ekspor PLN (Perpres 112/2022) dan kredit penghindaran metana; karbon hanya " + N.shC + "% pendapatan, jadi proyek tidak bergantung harga karbon.", C.accent2]];
  u.forEach(([h, b, c], i) => card(s, 0.45 + (i % 2) * 3.1, 1.42 + Math.floor(i / 2) * 1.62, 3.0, 1.52, h, b, c, { bs: 10, hs: 11.5 }));
  s.addChart(pres.charts.BAR, [{ name: "NPV pengembang", labels: ["Tetap 20 th", "PKS tutup th 8, set dipindah", "PKS tutup th 8, aset terdampar"], values: [S.NPV / 1e6, S.relocation.reloc / 1e6, S.relocation.stranded / 1e6] }], {
    x: 0.45, y: 4.72, w: 6.1, h: 1.38, barDir: "bar", chartColors: [HEX.accent1, HEX.accent2, HEX.accent3], varyColors: true, showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00",
    dataLabelFontSize: 9, dataLabelFontFace: "+mn-lt", showTitle: true, title: "Nilai relokasi bagi pemberi pinjaman: NPV (USD juta)", titleFontSize: 10, titleFontFace: "+mn-lt", titleColor: HEX.dk2,
    catAxisLabelFontSize: 9, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, valAxisMinVal: -1.2, valAxisMaxVal: 1.2, catAxisLabelPos: "low", objectName: on() });
  head(s, 6.75, 1.42, 6.15, "Matriks pesaing berbobot (5 = terbaik bagi PKS)");
  img(s, "finance/outputs/figs/g13_pesaing.png", 6.75, 1.78, 6.15, 2409, 996);
  stat(s, 6.75, 4.4, 1.95, 1.7, "3,71", "skor kami, tertinggi dari 7 opsi", C.accent1, { bigs: 26 });
  stat(s, 8.85, 4.4, 1.95, 1.7, "3,67", "biometana BOOT (reNIKOLA): butuh USD 5,3 jt/PKS", C.accent6, { bigs: 26 });
  stat(s, 10.95, 4.4, 1.95, 1.7, "5,0", "satu-satunya skor penuh untuk modal PKS dan relokasi", C.accent2, { bigs: 26 });
  concl(s, "Teknologi biogas POME sudah matang; inovasi kami adalah mengemasnya menjadi produk standar yang dapat dipindah dan dijual sebagai layanan, sehingga risiko modal dan kinerja pindah dari PKS ke operator.");
  src(s, "fin_market.py (matriks 7 kriteria berbobot), fin_core.py (skenario relokasi), R3_competitors.json; reNIKOLA/PTPN IV/Pertagas (USD 40-45 jt untuk 8 PKS).");
  nav(s, 2);
  s.addNotes("Inovasi. Empat keunggulan: reaktor kecil, dapat dipindah, model layanan, tiga aliran nilai. Matriks pesaing menilai 7 opsi pada 7 kriteria berbobot; kami 3,71 dan biometana BOOT 3,67, tetapi biometana butuh investasi jauh lebih besar per PKS. Grafik kiri bawah menunjukkan mengapa relokasi penting bagi pemberi pinjaman.");
}

// 5  PASAR
pres.addSection({ title: "Pasar" });
{
  const s = slide("Pasar", "Peluang pasar", "Pasar: ~1.150 PKS belum menangkap metana; target awal " + N.sam + " PKS bergantung solar dengan nilai layanan USD " + N.samUSD + " juta/th");
  img(s, "finance/outputs/figs/g01_pasar.png", 0.45, 1.42, 7.0, 2033, 879);
  const st = [[N.tam + " set", "TAM: USD " + N.tamUSD + " miliar/th, semua POME tanpa penangkapan"], [N.sam + " PKS", "SAM: 30-60 t/jam, tanpa metana, bergantung solar"], [N.som + " set", "SOM 2034: USD " + N.somUSD + " juta/th (" + P(S.market.share, 0) + "% SAM)"]];
  st.forEach(([b, l], i) => stat(s, 0.45 + i * 2.37, 4.6, 2.25, 1.45, b, l, [C.text2, C.accent1, C.accent2][i], { bigs: 22, ls: 9.5 }));
  head(s, 7.7, 1.42, 5.2, "Jendela kesepakatan per segmen (USD/t TBS)");
  const rows = [tblHead(["Segmen", "Fee min\npengembang", "Fee maks\nPKS", "Hemat\nPKS", "IRR"])];
  [["S1", "Terhubung PLN"], ["S2", "PLN, beban tinggi"], ["S3", "Bergantung solar"], ["S4", "Off-grid penuh"]].forEach(([k, n]) => {
    const g = seg[k], ok = g.fee_max > g.fee_min, tgt = k === "S3";
    const o = { fill: { color: tgt ? "E3EFE9" : HEX.lt1 }, bold: tgt, align: "center" };
    rows.push([T(k + " " + n, { ...o, align: "left" }), T(id(g.fee_min, 2), o), T(id(g.fee_max, 2), o), T(P(g.saving_pct, 0) + "%", { ...o, color: g.saving_pct > 0 ? HEX.accent1 : HEX.accent3 }), T(P(g.IRR_dev) + "%", o)]);
  });
  s.addTable(rows, { x: 7.7, y: 1.78, w: 5.2, colW: [1.8, 0.9, 0.85, 0.85, 0.8], fontSize: 10, fontFace: "Calibri", color: HEX.dk1, border: { type: "solid", pt: 0.5, color: "D9D6CC" }, rowH: 0.36, margin: [2, 4, 2, 4], objectName: on() });
  card(s, 7.7, 3.72, 5.2, 2.33, "Mengapa mulai dari S3", [
    T("S1/S2 tidak punya jendela: biaya minimum kami melebihi yang mau dibayar PKS. Kami tidak menjual ke sana dulu.", { bullet: true, breakLine: true }),
    T("S3 punya jendela USD " + N.fmin + "-" + N.fmax + "/t TBS; fee dasar USD 1,00 di tengahnya.", { bullet: true, breakLine: true }),
    T("442 PKS tanpa kebun (GAPKI 2026) adalah pembeli layanan alami: modal terbatas, risiko pasokan TBS tinggi.", { bullet: true, breakLine: true }),
    T("Riau, Sumut, Kalteng, Kalbar dan Sumsel memuat >60% SAM.", { bullet: true })], C.accent1, { bs: 10 });
  concl(s, "Kami sengaja menyempitkan pasar ke PKS yang benar-benar diuntungkan. Merebut " + N.som + " set pada 2034 sama dengan ~" + P(S.market.share, 0) + "% SAM dan seperempat laju bangun PLTBg nasional (9 MW/th), target yang dapat dicapai.");
  src(s, "fin_market.py (pasar bottom-up), fin_mill.py (segmen); Trase/SEI-PCS (~1.300 PKS); GAPKI 2026 (442 PKS tanpa kebun); EBTKE (laju bangun PLTBg); Disbun Kaltim.");
  nav(s, 3);
  s.addNotes("Pasar. Corong bottom-up: 1 set per PKS, pendapatan rata-rata 20 tahun. TAM " + N.tam + " set, SAM " + N.sam + " PKS bergantung solar, SOM " + N.som + " set pada 2034. Tabel segmen membuktikan secara jujur bahwa PKS yang sudah terhubung PLN bukan pasar pertama kami.");
}

// 6  MODEL BISNIS
pres.addSection({ title: "Model bisnis" });
{
  const s = slide("Model bisnis", "Model bisnis", "Model bisnis: PKS membayar USD " + N.D + "/t TBS, bukan " + N.A + ", sehingga hemat " + N.save + "% (USD " + N.saveYr + " rb/th) tanpa capex, dan operator tetap untung");
  head(s, 0.45, 1.42, 8.0, "Biaya POME bagi PKS bergantung solar (USD 2026/t TBS, 20 th): opsi A-D dan jembatan A → D");
  img(s, "finance/outputs/figs/g11_keputusan_pks.png", 0.45, 1.75, 8.0, 2514, 952);
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Pendapatan", labels: ["Listrik (PKS + PLN)", "Jasa POME", "Karbon"], values: [S.share_el * 100, S.share_fee * 100, S.share_c * 100] }], {
    x: 8.7, y: 1.42, w: 4.2, h: 3.1, holeSize: 55, chartColors: [HEX.accent1, HEX.accent2, HEX.accent4], showPercent: true, showValue: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 10,
    dataLabelFontFace: "+mn-lt", showTitle: true, title: "Porsi pendapatan 20 th", titleFontSize: 11, titleFontFace: "+mn-lt", titleColor: HEX.dk2, showLegend: true, legendPos: "b",
    legendFontSize: 9.5, legendFontFace: "+mn-lt", objectName: on() });
  const rv = [["Listrik ke PKS", N.cap + " GWh/th × USD 0,20/kWh, menggantikan " + N.dieselL + " L solar/th", C.accent1],
              ["Ekspor ke PLN", N.exp + " GWh/th × 10,18 USc × F 1,10 (th 1-10), lalu 6,11 USc", C.accent1],
              ["Jasa POME", "USD 1,00/t TBS × 202.500 t/th; jendela USD " + N.fmin + "-" + N.fmax, C.accent2],
              ["Kredit karbon", N.er + " tCO2e/th × USD 5 (Verra, 10 th)", C.accent4]];
  rv.forEach(([h, b, c], i) => card(s, 0.45 + i * 3.13, 4.88, 3.02, 1.2, h, b, c, { bs: 10 }));
  concl(s, "Fee ditetapkan di dalam jendela kesepakatan: di atas titik impas pengembang (USD " + N.fmin + ") dan jauh di bawah titik PKS lebih baik memakai kolam (USD " + N.fmax + "). Kedua pihak untung, tanpa subsidi.");
  src(s, "fin_mill.py dan lembar Keputusan PKS di BG_Model_Keuangan.xlsx (rumus hidup); Perpres 112/2022; harga karbon EcoEngineers/AlliedOffsets 2025; biaya solar R2.");
  nav(s, 4);
  s.addNotes("Model bisnis. Kiri: biaya POME bagi PKS untuk empat opsi. Kolam tertutup dan tangki milik PKS lebih murah di atas kertas, tetapi butuh capex USD 2,6-3,0 juta dan PKS menanggung risiko kinerja. Layanan kami USD " + N.D + "/t, " + N.save + "% di bawah status quo. Jembatan menunjukkan dari mana penghematan berasal: solar yang dihindari.");
}

// 7  KEUANGAN
pres.addSection({ title: "Keuangan" });
{
  const s = slide("Keuangan", "Kelayakan finansial", "Keuangan: investasi USD " + N.fci + " juta per set memberi NPV USD " + N.npv + " juta, IRR " + N.irr + "% dan payback " + N.pbp + " tahun");
  const k = [["USD " + N.fci + " jt", "FCI per set (60% utang hijau 8%)"], ["USD " + N.npv + " jt", "NPV proyek @ WACC " + N.wacc + "%"], [N.irr + "%", "IRR proyek"], [N.irrEq + "%", "IRR ekuitas"],
             [N.pbp + " th", "payback sejak COD 2028"], [N.dscr, "DSCR minimum (≥ 1,30)"], ["USD " + N.lcoe, "LCOE per kWh"], [N.pnpv + "%", "P(NPV > 0), Monte Carlo 3.000"]];
  k.forEach(([b, l], i) => stat(s, 0.45 + (i % 4) * 1.47, 1.42 + Math.floor(i / 4) * 1.02, 1.39, 0.94, b, l, i < 4 ? C.text2 : C.accent1, { bigs: 16, ls: 8.5 }));
  img(s, "finance/outputs/figs/g04_arus_kas.png", 0.45, 3.52, 5.82, 2037, 861);
  const keys = Object.keys(sc);
  s.addChart(pres.charts.BAR, [{ name: "NPV", labels: keys.map(k2 => k2.replace(" (S1, solar 0,53 L/t)", " (S1)").replace(" (fee USD 1.00/t)", "").replace(" (puncak 2024)", "").replace(" (kurva belajar)", "")), values: keys.map(k2 => sc[k2].NPV / 1e6) }], {
    x: 6.5, y: 1.42, w: 6.4, h: 3.1, barDir: "bar", chartColors: [HEX.accent1], invertedColors: [HEX.accent3], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00",
    dataLabelFontSize: 9, dataLabelFontFace: "+mn-lt", showTitle: true, title: "NPV per skenario (USD juta)", titleFontSize: 11, titleFontFace: "+mn-lt", titleColor: HEX.dk2,
    catAxisLabelFontSize: 9, catAxisLabelFontFace: "+mn-lt", catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, valAxisMinVal: -1.5, valAxisMaxVal: 2.2, catAxisLabelPos: "low", objectName: on() });
  card(s, 6.5, 4.65, 3.1, 1.4, "Yang membuat proyek layak", "Fee POME dan penggantian solar. Tanpa fee, NPV USD " + M(sc["Tanpa fee POME"].NPV) + " juta; di PKS terhubung PLN, USD " + M(sc["PKS terhubung PLN (S1, solar 0,53 L/t)"].NPV) + " juta.", C.accent3, { bs: 9.5 });
  card(s, 9.8, 4.65, 3.1, 1.4, "Yang memperbaikinya", "Kurva belajar: unit ke-10 IRR " + P(sc["Unit ke-10 (kurva belajar)"].IRR) + "%. Tier 60 t/jam IRR " + P(sc["Set 60 t/jam"].IRR) + "%. Penggerak utama ketidakpastian: faktor beban TBS dan capex.", C.accent1, { bs: 9.5 });
  concl(s, "Satu set layak dengan margin wajar (IRR " + N.irr + "% vs WACC " + N.wacc + "%, DSCR " + N.dscr + "). Risikonya kami ungkap: P(NPV > 0) " + N.pnpv + "%, sehingga set pertama dipilih di PKS dengan beban TBS terjamin.");
  src(s, "BG_Model_Keuangan.xlsx (rumus hidup, diverifikasi ulang LibreOffice = Python), fin_core.py v3; WACC dari IEA, CPI, BI Rate 5,75%; PP 78/2019 (tax allowance).");
  nav(s, 5);
  s.addNotes("Keuangan. Delapan indikator kunci dari model Excel dengan rumus hidup. Arus kas kumulatif kembali positif tahun ke-" + N.pbp + ". Grafik skenario menunjukkan proyek bergantung pada fee POME dan penggantian solar, dan membaik dengan kurva belajar serta tier 60 t/jam.");
}

// 8  DAMPAK
pres.addSection({ title: "Dampak" });
{
  const s = slide("Dampak", "Dampak lingkungan, energi dan sosial", "Dampak: setiap set menghindari " + N.er + " tCO2e/th dan menggantikan ~" + N.dieselK + " rb L solar/th; " + N.som + " set pada 2034 menghindari ~" + id(S.ER_t * S.market.sets_SOM / 1e3, 0) + " rb tCO2e/th");
  img(s, "cad/out/render/DIORAMA_lokasi.png", 0.45, 1.42, 6.4, 3200, 1800);
  s.addText("Set biogas dipasang di samping kolam POME lama; kolam lama dikosongkan, kolam polishing tetap dipakai.", { x: 0.45, y: 5.04, w: 6.4, h: 0.28, fontSize: 9, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: on() });
  const sd = [["SDG 6", "Air bersih"], ["SDG 7", "Energi bersih"], ["SDG 8", "Pekerjaan layak"], ["SDG 12", "Konsumsi bertanggung jawab"], ["SDG 13", "Aksi iklim"]];
  sd.forEach(([a, b], i) => s.addText([T(a, { bold: true, fontSize: 10, breakLine: true }), T(b, { fontSize: 8.5 })], { x: 0.45 + i * 1.29, y: 5.4, w: 1.22, h: 0.65, align: "center", valign: "middle", margin: 2,
    color: C.background1, fill: { color: [C.accent4, C.accent2, C.accent3, C.accent5, C.text2][i] }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, isTextBox: true, objectName: on() }));
  const im = [[N.er, "tCO2e/th metana dihindari (96% dari baseline kolam)", C.accent1], [N.dieselL + " L", "solar/th digantikan listrik biogas di PKS", C.accent2],
              [N.net + " GWh", "listrik neto/th; " + N.exp + " GWh ke jaringan PLN", C.accent1], ["USD " + N.saveYr + " rb", "hemat biaya PKS per tahun, tanpa capex", C.accent2],
              ["10 orang", "lapangan kerja lokal per set (operator, lab/K3, manajer)", C.text2], ["0,1186", "tCO2e/t TBS dihindari: membantu PKS lolos ISPO dan EU RED", C.text2]];
  im.forEach(([b, l, c], i) => stat(s, 7.05 + (i % 2) * 2.95, 1.42 + Math.floor(i / 2) * 1.23, 2.85, 1.13, b, l, c, { bigs: 22, ls: 9.5 }));
  card(s, 7.05, 5.12, 5.85, 0.93, "Ekonomi sirkular", "Limbah POME → listrik dan kredit karbon; lumpur terolah → pupuk kebun; kolam lama dibebaskan untuk polishing. Tidak ada limbah baru.", C.accent5, { bs: 10 });
  concl(s, "Dampak paling besar ada pada metana: satu set menghindari emisi setara " + N.er + " t CO2, dan karena set dapat dipindah, dampak ini tetap berjalan meskipun satu PKS tutup.");
  src(s, "process/biogas_balance.py (emisi AMS-III.H, UF 0,89, GWP 28 sesuai Decision 18/CMA.1); solar 0,30 L/kWh (R2); staf dari fin_core.py; ISCC EU 205.");
  nav(s, 6);
  s.addNotes("Dampak. Lingkungan: " + N.er + " tCO2e/th per set dengan metodologi AMS-III.H dan faktor ketidakpastian 0,89. Energi: " + N.net + " GWh neto. Ekonomi: PKS hemat USD " + N.saveYr + " ribu per tahun. Sosial: 10 pekerjaan lokal per set.");
}

// 9  SKALABILITAS
pres.addSection({ title: "Skala" });
{
  const s = slide("Skala", "Skalabilitas dan peta jalan", "Skala: modul standar 2/3/4 tangki untuk PKS 30/45/60 t/jam; " + N.som + " set pada 2034 memberi NPV perusahaan USD " + N.fleetNPV + " juta");
  img(s, "finance/outputs/figs/g09_armada.png", 0.45, 1.42, 7.6, 2404, 864);
  head(s, 8.3, 1.42, 4.6, "Tier produk (desain berulang, tangki standar 980 m³)");
  const rows = [tblHead(["Tier PKS", "Tangki", "Genset", "NPV", "IRR"])];
  [["30 t/jam", "2", "2 x 400", sc["Set 30 t/jam"]], ["45 t/jam", "3", "2 x 600", { NPV: S.NPV, IRR: S.IRR }], ["60 t/jam", "4", "2 x 800", sc["Set 60 t/jam"]]].forEach(([a, b, c, v], i) => {
    const o = { align: "center", fill: { color: i === 1 ? "E3EFE9" : HEX.lt1 }, bold: i === 1 };
    rows.push([T(a, o), T(b, o), T(c + " kWe", o), T(id(v.NPV / 1e6, 2), { ...o, color: v.NPV < 0 ? HEX.accent3 : HEX.dk1 }), T(P(v.IRR) + "%", o)]);
  });
  s.addTable(rows, { x: 8.3, y: 1.78, w: 4.6, colW: [1.0, 0.75, 1.15, 0.85, 0.85], fontSize: 10, fontFace: "Calibri", color: HEX.dk1, border: { type: "solid", pt: 0.5, color: "D9D6CC" }, rowH: 0.34, margin: [2, 4, 2, 4], objectName: on() });
  s.addText("NPV dalam USD juta. Tier 30 t/jam baru layak setelah kurva belajar; unit ke-10 tier 45 mencapai IRR " + P(sc["Unit ke-10 (kurva belajar)"].IRR) + "%.", { x: 8.3, y: 3.22, w: 4.6, h: 0.5, fontSize: 9, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: on() });
  // peta jalan
  head(s, 0.45, 4.3, 12.45, "Peta jalan");
  const rm = [["2026-27", "Pilot & FID", "MoU PKS S3 pertama, uji batch termofilik, PDD Verra, FID set 1"], ["2027", "Konstruksi set 1", "Panel GFS dan skid dibuat 6 bln, pasang 4 bln"],
              ["2028", "COD set 1", "Ramp-up 2-4 bln; data kinerja untuk pemberi pinjaman"], ["2029-31", "Replikasi", "2 set/th di Riau, Sumut, Kalteng; kontrak standar"],
              ["2032-34", "Armada " + N.som + " set", "3 set/th; relokasi set pertama bila diperlukan"], ["2035+", "Fase 2", "Opsi membran PM-11, bio-CNG, pasar Malaysia (315 PKS)"]];
  rm.forEach(([t, h, b], i) => {
    const x = 0.45 + i * 2.09;
    s.addShape(pres.shapes.CHEVRON, { x, y: 4.7, w: 2.02, h: 0.46, fill: { color: i < 3 ? C.text2 : C.accent1 }, line: { color: C.background1 }, objectName: on() });
    s.addText(t, { x: x + 0.18, y: 4.7, w: 1.66, h: 0.46, fontSize: 11, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: on() });
    s.addText([T(h, { bold: true, color: HEX.dk2, breakLine: true, fontSize: 11.5 }), T(b, { fontSize: 10.5 })], { x: x + 0.04, y: 5.24, w: 1.96, h: 1.0, valign: "top", margin: 2, color: C.text1, isTextBox: true, objectName: on() });
  });
  concl(s, "Satu desain dipakai berulang: tambah atau kurangi tangki untuk ukuran PKS, pindahkan set bila PKS tutup. Puncak kebutuhan dana armada USD " + N.fleetPeak + " juta (2034), IRR perusahaan " + N.fleetIRR + "%.");
  src(s, "fin_core.py (ROLL 1-1-2-2-2-2-2-3 set/th, kurva belajar), process tiers (2/3/4 tangki), MPOB/RTM (PKS Malaysia tanpa penangkapan).");
  nav(s, 7);
  s.addNotes("Skalabilitas. Desain modular: satu ukuran tangki dipakai untuk tiga tier PKS. Rencana armada " + N.som + " set pada 2034 dengan puncak pendanaan USD " + N.fleetPeak + " juta. Peta jalan dimulai dengan pilot dan FID di PKS bergantung solar.");
}

// 10  PENUTUP
pres.addSection({ title: "Penutup" });
{
  const s = slide("Penutup", "Risiko, kesimpulan dan kebutuhan", "Kesimpulan: layanan biogas yang dapat dipindah membuat penangkapan metana lebih murah bagi PKS daripada membuang POME ke kolam");
  head(s, 0.45, 1.42, 6.9, "Risiko utama dan mitigasi");
  const rk = [["Beban TBS rendah", "Fee per t TBS + kontrak minimum; pilih PKS dengan pasokan terjamin; set dapat dipindah"],
              ["Kinerja biologis termofilik", "Kontrol FOS/TAC online, resirkulasi lumpur, uji batch sebelum FID; operator menanggung risiko"],
              ["PKS tutup atau putus kontrak", "Relokasi: NPV tetap USD " + N.reloc + " juta, bukan USD " + N.strand + " juta"],
              ["Tarif PLN dan izin ekspor", "Prioritas listrik captive (USD 0,20/kWh); ekspor hanya kelebihan ≤ 1 MW"],
              ["Harga karbon jatuh", "Karbon hanya " + N.shC + "% pendapatan; titik impas karbon < USD 0"],
              ["Capex tangki GFS (asumsi)", "Penawaran 3 pabrikan sebelum FID; capex impas +" + P(S.BEP.capex_be - 1, 0) + "%"]];
  const rows = [tblHead(["Risiko", "Mitigasi"])].concat(rk.map(([a, b], i) => [T(a, { bold: true, color: HEX.dk2, fill: { color: i % 2 ? HEX.lt2 : HEX.lt1 } }), T(b, { fill: { color: i % 2 ? HEX.lt2 : HEX.lt1 } })]));
  s.addTable(rows, { x: 0.45, y: 1.78, w: 6.9, colW: [2.0, 4.9], fontSize: 10, fontFace: "Calibri", color: HEX.dk1, border: { type: "solid", pt: 0.5, color: "D9D6CC" }, rowH: 0.52, margin: [2, 5, 2, 5], objectName: on() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.6, y: 1.42, w: 5.3, h: 4.63, rectRadius: 0.08, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: on() });
  const ans = [["Inovasi", "Kontak termofilik dalam tangki baut yang dapat dipindah, dijual sebagai layanan"], ["Bisnis", "PKS hemat " + N.save + "% tanpa capex; IRR proyek " + N.irr + "%, DSCR " + N.dscr],
               ["Dampak", N.er + " tCO2e/th dan " + N.dieselL + " L solar/th per set"], ["Skala", N.som + " set pada 2034; tier 30/45/60 t/jam; relokasi"]];
  s.addText("Jawaban atas kriteria penilaian", { x: 7.8, y: 1.55, w: 4.9, h: 0.3, fontSize: 12.5, bold: true, color: C.accent2, margin: 0, isTextBox: true, objectName: on() });
  ans.forEach(([a, b], i) => s.addText([T(a, { bold: true, color: HEX.accent2, fontSize: 11, breakLine: true }), T(b, { color: HEX.lt1, fontSize: 10.5 })],
    { x: 7.8, y: 1.92 + i * 0.66, w: 4.9, h: 0.62, margin: 0, valign: "top", isTextBox: true, objectName: on() }));
  s.addText("Yang kami butuhkan", { x: 7.8, y: 4.62, w: 4.9, h: 0.3, fontSize: 12.5, bold: true, color: C.accent2, margin: 0, isTextBox: true, objectName: on() });
  s.addText([T("Satu PKS mitra pilot di segmen S3 (data POME dan solar 12 bulan)", { bullet: true, breakLine: true }), T("Ekuitas USD " + M(S.FCI * 0.4, 2) + " juta + pinjaman hijau USD " + M(S.FCI * 0.6, 2) + " juta untuk set 1", { bullet: true, breakLine: true }),
             T("Pendampingan izin PLN (IUPTLS) dan PDD Verra", { bullet: true })], { x: 7.8, y: 4.94, w: 4.9, h: 1.05, fontSize: 10.5, color: C.background1, margin: 0, valign: "top", paraSpaceAfter: 2, isTextBox: true, objectName: on() });
  concl(s, "POME tidak perlu lagi menjadi biaya. Dengan model layanan, PKS bergantung solar membayar " + N.save + "% lebih sedikit, operator memperoleh IRR " + N.irr + "%, dan Indonesia menangkap metana yang selama ini terlepas dari kolam.");
  src(s, "Seluruh angka dari model di repositori ini (neraca proses Rev 2, BG_Model_Keuangan.xlsx v3, register 177 sumber di research/source_register.json).");
  nav(s, 8);
  s.addNotes("Penutup. Enam risiko utama dan mitigasinya, jawaban atas empat kriteria penilaian, dan kebutuhan kami: PKS mitra pilot, pendanaan set pertama dan pendampingan izin.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ditulis", OUT);
})();
