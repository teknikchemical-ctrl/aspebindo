// Deck pitch EIC 2026 (10 slide, Bahasa Indonesia). Semua angka dibaca dari deck_data.json (hasil model proses dan keuangan di repositori).
// Jalankan dari akar repositori:  python3 deck/export_data.py && NODE_PATH=<node_modules> node deck/build.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL || "/root/.claude/skills/synced/1447d632-3db4-4ffa-8639-0456923eecc3_b47be9f3-76fa-4276-9bf3-c539adcfb469/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const L = require("./lib.js");
const { C, THEME, FONT_H, FONT_B } = L;

const OUT = path.join(__dirname, process.env.DECK_OUT || "EIC2026_PITCHDECK_MALATAXTAX.pptx");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13,333 x 7,5 inci
pres.theme = { headFontFace: FONT_H, bodyFontFace: FONT_B };
pres.title = "Biogas sebagai Layanan: Pengolah POME Termofilik Modular untuk PKS";
pres.author = "Tim Malataxtax";
pres.subject = "EIC 2026 - Energy Business Plan Competition, Subtema 3";
pres.company = "Malataxtax";

pres.defineSlideMaster({
  title: "SAMPUL", background: { path: path.join(__dirname, "img/bg_sampul.png") }, objects: [],
});
pres.defineSlideMaster({
  title: "KONTEN", background: { path: path.join(__dirname, "img/bg_konten.png") },
  objects: [
    { placeholder: { options: { name: "judul", type: "title", x: 0.92, y: 0.45, w: 12.0, h: 0.62, fontFace: FONT_H, fontSize: 16, bold: true, color: C.navy, align: "left", valign: "top", margin: 0 }, text: "" } },
    { text: { text: "Malataxtax  |  Energy Business Plan Competition, EIC 2026  |  Subtema 3: Ekonomi Sirkular", options: { x: 0.4, y: 7.3, w: 9, h: 0.14, fontFace: FONT_B, fontSize: 6.5, color: C.slate, margin: 0, valign: "middle" } } },
  ],
  slideNumber: { x: 12.4, y: 7.3, w: 0.55, h: 0.14, fontFace: FONT_B, fontSize: 7, color: C.navy, align: "right" },
});

const H = L.mk(pres);
const SEC = ["Sampul", "Latar belakang dan masalah", "Solusi: konsep", "Solusi: validitas teknis", "Solusi: desain produk", "Analisis pesaing", "Model keuangan", "Rencana implementasi", "Peluang bisnis dan dampak", "Kesimpulan"];
H.SEC = SEC;
const only = (process.env.ONLY || "").split(",").filter(Boolean).map(Number);
for (let i = 1; i <= 10; i++) {
  if (only.length && !only.includes(i)) continue;
  const f = path.join(__dirname, "slides", "s" + String(i).padStart(2, "0") + ".js");
  pres.addSection({ title: SEC[i - 1] });
  require(f)(pres, H, L);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ditulis", OUT);
})();
