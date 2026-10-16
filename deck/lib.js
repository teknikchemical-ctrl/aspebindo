// Pustaka desain v2: gaya dek konsultan (judul dua warna, bilah header, panel biru muda, navigasi bawah)
const path = require("path");
const fs = require("fs");
const ROOT = path.resolve(__dirname, "..");
const D = JSON.parse(fs.readFileSync(path.join(__dirname, "deck_data.json"), "utf8"));

const C = {
  navy: "0C2464", royal: "1F4E9E", teal: "2B9FC8", tealL: "D6ECF6", panel: "EAF4FB", green: "3E8E41", greenL: "E3F3DE", lime: "8CC63F",
  ink: "14213D", slate: "5B6B7F", line: "BFD6E8", red: "C8452F", redL: "FBE6E2", amber: "E0A526", amberL: "FFF3CF", white: "FFFFFF", mid: "6898C8", grey: "EEF2F6",
};
const FONT_H = "Arial", FONT_B = "Calibri";
const THEME = {
  name: "EIC 2026 Malataxtax", headFontFace: FONT_H, bodyFontFace: FONT_B,
  colors: { dk1: C.ink, lt1: C.white, dk2: C.navy, lt2: C.panel, accent1: C.royal, accent2: C.green, accent3: C.teal, accent4: C.lime, accent5: C.mid, accent6: C.slate, hlink: C.royal, folHlink: C.navy },
};
const fmt = (x, d = 0) => {
  if (x === null || x === undefined || Number.isNaN(x)) return "n/a";
  const s = Math.abs(x).toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
  return (x < 0 && Number(Math.abs(x).toFixed(d)) !== 0 ? "−" : "") + s;
};
const NF = "[$-421]#,##0", NF1 = "[$-421]#,##0.0", NF2 = "[$-421]#,##0.00";
let nid = 0; const oid = (p) => (p || "o") + "-" + (++nid);

const NAV = ["Latar belakang", "Solusi", "Pesaing", "Keuangan", "Implementasi", "Dampak", "Kesimpulan"];
const NAVIDX = { 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6 };

function mk(pres) {
  const H = {};
  H.t = (s, text, x, y, w, h, o = {}) => s.addText(text, Object.assign({ x, y, w, h, fontFace: FONT_B, fontSize: 9, color: C.ink, margin: 0, valign: "top", isTextBox: true, objectName: oid("teks"), fit: "none" }, o));
  H.rect = (s, x, y, w, h, o = {}) => {
    const op = { x, y, w, h, fill: { color: o.fill || C.white, transparency: o.tr || 0 }, line: o.line === null ? { color: o.fill || C.white, width: 0 } : { color: o.line || C.line, width: o.lw || 0.75, dashType: o.dash }, objectName: oid("kotak") };
    if (o.radius) op.rectRadius = o.radius;
    s.addShape(o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, op);
  };
  H.box = (s, text, x, y, w, h, o = {}) => {
    const op = { x, y, w, h, fontFace: o.font || FONT_B, fontSize: o.fs || 9, bold: !!o.bold, italic: !!o.italic, color: o.color || C.ink, align: o.align || "center", valign: o.valign || "middle",
      fill: { color: o.fill || C.white, transparency: o.tr || 0 }, line: o.line === null ? { color: o.fill || C.white, width: 0 } : { color: o.line || C.line, width: o.lw || 0.75, dashType: o.dash },
      margin: o.margin === undefined ? [2, 5, 2, 5] : o.margin, shape: o.radius === 0 ? pres.shapes.RECTANGLE : pres.shapes.ROUNDED_RECTANGLE, isTextBox: true, objectName: oid("kotak"), fit: "none", paraSpaceAfter: o.psa };
    if (o.radius !== 0) op.rectRadius = o.radius === undefined ? 0.06 : o.radius;
    s.addText(text, op);
  };
  H.ln = (s, x1, y1, x2, y2, o = {}) => {
    const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1), flipV = (x2 - x1) * (y2 - y1) < 0;
    const defEnd = flipV ? [x + w, y] : [x + w, y + h];
    const endIsDef = Math.abs(defEnd[0] - x2) < 1e-6 && Math.abs(defEnd[1] - y2) < 1e-6;
    const line = { color: o.color || C.navy, width: o.w || 1.25, dashType: o.dash };
    if (o.arrow !== false) { if (endIsDef) line.endArrowType = "triangle"; else line.beginArrowType = "triangle"; }
    const op = { x, y, w, h, line, objectName: oid("garis") }; if (flipV) op.flipV = true;
    s.addShape(pres.shapes.LINE, op);
  };
  H.path = (s, pts, o = {}) => { for (let i = 0; i < pts.length - 1; i++) H.ln(s, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], Object.assign({}, o, { arrow: i === pts.length - 2 ? o.arrow !== false : false })); };
  H.imgFit = (s, file, pxw, pxh, x, y, w, h, o = {}) => {
    const r = pxw / pxh; let ww = w, hh = w / r; if (hh > h) { hh = h; ww = h * r; }
    const xx = x + (w - ww) / 2, yy = y + (h - hh) / 2;
    s.addImage(Object.assign({ path: file.startsWith("/") ? file : path.join(ROOT, file), x: xx, y: yy, w: ww, h: hh, objectName: oid("gambar") }, o)); return { x: xx, y: yy, w: ww, h: hh };
  };
  // bilah header gaya referensi (biru tua / teal)
  H.hdr = (s, text, x, y, w, o = {}) => H.box(s, text, x, y, w, o.h || 0.27, { fs: o.fs || 10, bold: true, color: C.white, fill: o.fill || C.navy, line: null, radius: 0.04, font: FONT_H, align: o.align || "center" });
  H.panel = (s, x, y, w, h, o = {}) => H.rect(s, x, y, w, h, { fill: o.fill || C.panel, line: o.line || C.line, radius: 0.05, lw: 0.75 });
  H.kpi = (s, big, label, x, y, w, h, o = {}) => {
    H.rect(s, x, y, w, h, { fill: C.white, line: o.line || C.teal, radius: 0.05, lw: 1 });
    H.t(s, big, x + 0.08, y + 0.05, w - 0.16, h * 0.5, { fontFace: FONT_H, fontSize: o.bs || 17, bold: true, color: o.color || C.navy, valign: "middle", align: "center" });
    H.t(s, label, x + 0.08, y + h * 0.52, w - 0.16, h * 0.46, { fontSize: o.ls || 8.5, color: C.slate, align: "center", valign: "top" });
  };
  H.table = (s, rows, x, y, colW, o = {}) => {
    const fs = o.fs || 8.5, nh = o.head === undefined ? 1 : o.head;
    const body = rows.map((r, i) => r.map((c, j) => {
      const cell = (c !== null && typeof c === "object" && !Array.isArray(c) && c.text !== undefined) ? c : { text: String(c) };
      const hd = i < nh;
      const op = Object.assign({ fontFace: FONT_B, fontSize: fs, color: hd ? C.white : C.ink, bold: hd, align: (o.align && o.align[j]) || (hd ? "center" : "left"), valign: "middle",
        fill: { color: hd ? (o.headFill || C.navy) : (o.zebra !== false && (i - nh) % 2 === 1 ? C.panel : C.white) }, margin: (o.margin || [1, 4, 1, 4]).map((q) => Math.max(1, q)),
        border: [0, 1, 2, 3].map(() => ({ type: "solid", pt: 0.5, color: C.line })) }, cell.options || {});
      return { text: cell.text, options: op };
    }));
    s.addTable(body, { x, y, colW, rowH: rows.map((_, i) => (i < nh ? (o.hrh || o.rh || 0.24) : (Array.isArray(o.rh) ? o.rh[i - nh] : (o.rh || 0.24)))), autoPage: false, objectName: oid("tabel") });
  };
  H.concl = (s, text, label) => {
    H.box(s, label || "Kesimpulan", 0.45, 6.5, 1.5, 0.38, { fs: 10, bold: true, color: C.white, fill: C.navy, line: null, radius: 0.05, font: FONT_H });
    H.box(s, text, 2.0, 6.5, 10.9, 0.38, { fs: 9.5, align: "left", fill: C.tealL, line: C.teal, lw: 0.75, radius: 0.05, margin: [2, 8, 2, 8], bold: false });
  };
  H.src = (s, text, abbr) => H.t(s, abbr ? [{ text: "Singkatan: " + abbr, options: { breakLine: true } }, { text: "Sumber: " + text }] : "Sumber: " + text, 0.45, 6.93, 12.4, 0.28, { fontSize: 5.6, color: C.slate, valign: "top" });
  H.nav = (s, num) => {
    const a = NAVIDX[num]; if (a === undefined) return;
    NAV.forEach((t, i) => H.box(s, t, 0.45 + i * 1.62, 7.22, 1.56, 0.22, { fs: 8, bold: i === a, color: i === a ? C.white : C.navy, fill: i === a ? C.navy : C.white, line: C.navy, lw: 1, radius: 0.11, margin: 0, font: FONT_H }));
    H.box(s, String(num), 12.4, 7.2, 0.5, 0.25, { fs: 10, bold: true, color: C.white, fill: C.royal, line: null, radius: 0.03, margin: 0, font: FONT_H });
  };
  // judul dua warna: {{...}} = sorotan teal
  H.slide = (num, title, notes) => {
    const s = pres.addSlide({ masterName: "KONTEN", sectionTitle: H.SEC[num - 1] });
    const runs = []; title.split(/(\{\{.*?\}\})/).filter(Boolean).forEach((p) => { const hl = p.startsWith("{{"); runs.push({ text: hl ? p.slice(2, -2) : p, options: { color: hl ? C.teal : C.navy, bold: true } }); });
    s.addText(runs, { placeholder: "judul" });
    H.nav(s, num);
    if (notes) s.addNotes(notes);
    return s;
  };
  return H;
}
module.exports = { C, FONT_H, FONT_B, THEME, D, fmt, NF, NF1, NF2, mk, ROOT, oid };
