// Pustaka bantu deck (tema guidebook ASPEBINDO EIC 2026: biru tua, hijau, langit muda)
const path = require("path");
const fs = require("fs");
const ROOT = path.resolve(__dirname, "..");
const D = JSON.parse(fs.readFileSync(path.join(__dirname, "deck_data.json"), "utf8"));

const C = {
  navy: "0C2464", royal: "244C9C", sky: "D8E8F8", sky2: "ECF3FA", mid: "6898C8", green: "64BC54", lime: "D4DC54", teal: "54B4CC",
  slate: "587888", ink: "14213D", white: "FFFFFF", line: "C3D3E8", amber: "E0A526", red: "C8452F", grey: "8A97A8", greenD: "3E8E41", paper: "F7FAFD",
};
const FONT_H = "Arial", FONT_B = "Calibri";
const THEME = {
  name: "EIC 2026 Malataxtax", headFontFace: FONT_H, bodyFontFace: FONT_B,
  colors: { dk1: C.ink, lt1: C.white, dk2: C.navy, lt2: C.sky2, accent1: C.royal, accent2: C.green, accent3: C.teal, accent4: C.lime, accent5: C.mid, accent6: C.slate, hlink: C.royal, folHlink: C.navy },
};

// ---------- format angka Indonesia
const fmt = (x, d = 0) => {
  if (x === null || x === undefined || Number.isNaN(x)) return "n/a";
  const s = Math.abs(x).toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
  return (x < 0 ? "−" : "") + s;
};
const pct = (x, d = 0) => fmt(x * 100, d) + "%";
const usdM = (x, d = 2) => "USD " + fmt(x / 1e6, d) + " juta";
const num = fmt;
const NF = "[$-421]#,##0"; const NF1 = "[$-421]#,##0.0"; const NF2 = "[$-421]#,##0.00";

let nid = 0;
const oid = (p) => (p || "o") + "-" + (++nid);

function mk(pres) {
  const H = {};
  H.pres = pres;
  // ---- teks
  H.t = (s, text, x, y, w, h, o = {}) => {
    s.addText(text, Object.assign({ x, y, w, h, fontFace: FONT_B, fontSize: 10, color: C.ink, margin: 0, valign: "top", isTextBox: true, objectName: oid("teks"), fit: "none" }, o));
  };
  H.rect = (s, x, y, w, h, o = {}) => {
    const shp = o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
    const op = { x, y, w, h, fill: { color: o.fill || C.white, transparency: o.tr || 0 }, line: o.line === null ? { color: o.fill || C.white, width: 0 } : { color: o.line || C.line, width: o.lw || 0.75 }, objectName: oid("kotak") };
    if (o.radius) op.rectRadius = o.radius;
    s.addShape(shp, op);
  };
  // kotak berteks
  H.box = (s, text, x, y, w, h, o = {}) => {
    const shp = o.radius === 0 ? pres.shapes.RECTANGLE : pres.shapes.ROUNDED_RECTANGLE;
    const op = {
      x, y, w, h, fontFace: o.font || FONT_B, fontSize: o.fs || 9, bold: !!o.bold, italic: !!o.italic, color: o.color || C.ink, align: o.align || "center", valign: o.valign || "middle",
      fill: { color: o.fill || C.white, transparency: o.tr || 0 }, line: o.line === null ? { color: o.fill || C.white, width: 0 } : { color: o.line || C.line, width: o.lw || 0.75, dashType: o.dash }, margin: o.margin === undefined ? [1, 3, 1, 3] : o.margin,
      shape: shp, isTextBox: true, objectName: oid("kotak"), fit: "none",
    };
    if (o.radius !== 0) op.rectRadius = o.radius || 0.05;
    s.addText(text, op);
  };
  // garis / panah dari (x1,y1) ke (x2,y2)
  H.ln = (s, x1, y1, x2, y2, o = {}) => {
    const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
    const flipV = (x2 - x1) * (y2 - y1) < 0;
    // ujung default: (maxx, maxy) bila tidak flip; (maxx, miny) bila flipV
    const defEnd = flipV ? [x + w, y] : [x + w, y + h];
    const endIsDef = Math.abs(defEnd[0] - x2) < 1e-6 && Math.abs(defEnd[1] - y2) < 1e-6;
    const line = { color: o.color || C.navy, width: o.w || 1.25, dashType: o.dash };
    if (o.arrow !== false && o.arrow !== "none") { if (endIsDef) line.endArrowType = "triangle"; else line.beginArrowType = "triangle"; }
    if (o.both) { line.endArrowType = "triangle"; line.beginArrowType = "triangle"; }
    const op = { x, y, w, h, line, objectName: oid("garis") };
    if (flipV) op.flipV = true;
    s.addShape(pres.shapes.LINE, op);
  };
  // jalur siku-siku: titik [[x,y],...], panah pada ujung terakhir
  H.path = (s, pts, o = {}) => {
    for (let i = 0; i < pts.length - 1; i++) {
      const last = i === pts.length - 2;
      H.ln(s, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], Object.assign({}, o, { arrow: last ? (o.arrow !== false) : false }));
    }
  };
  H.img = (s, rel, x, y, w, h, o = {}) => {
    s.addImage(Object.assign({ path: path.join(ROOT, rel), x, y, w, h, objectName: oid("gambar") }, o));
  };
  // gambar dengan rasio tetap di dalam kotak (x,y,w,h); kembalikan ukuran akhir
  H.imgFit = (s, file, pxw, pxh, x, y, w, h, o = {}) => {
    const r = pxw / pxh; let ww = w, hh = w / r; if (hh > h) { hh = h; ww = h * r; }
    const xx = x + (w - ww) / 2, yy = y + (h - hh) / 2;
    s.addImage(Object.assign({ path: file.startsWith("/") ? file : path.join(ROOT, file), x: xx, y: yy, w: ww, h: hh, objectName: oid("gambar") }, o));
    return { x: xx, y: yy, w: ww, h: hh };
  };
  // tabel
  H.table = (s, rows, x, y, w, colW, o = {}) => {
    const fs = o.fs || 8, rh = o.rh || 0.2;
    const body = rows.map((r, i) => r.map((c, j) => {
      const cell = (c !== null && typeof c === "object" && !Array.isArray(c) && c.text !== undefined) ? c : { text: String(c) };
      const hd = i < (o.head === undefined ? 1 : o.head);
      const op = Object.assign({
        fontFace: FONT_B, fontSize: fs, color: hd ? C.white : C.ink, bold: hd, align: (o.align && o.align[j]) || (hd ? "center" : "left"), valign: "middle",
        fill: { color: hd ? (o.headFill || C.navy) : (o.zebra && i % 2 === 0 ? C.sky2 : C.white) }, margin: (o.margin || [1, 3, 1, 3]).map((q) => Math.max(1, q)),
        border: [{ type: "solid", pt: 0.5, color: C.line }, { type: "solid", pt: 0.5, color: C.line }, { type: "solid", pt: 0.5, color: C.line }, { type: "solid", pt: 0.5, color: C.line }],
      }, cell.options || {});
      return { text: cell.text, options: op };
    }));
    s.addTable(body, { x, y, w, colW, rowH: Array.isArray(o.rowH) ? o.rowH : rows.map((_, i) => (i < (o.head === undefined ? 1 : o.head) ? (o.hrh || rh) : rh)), autoPage: false, objectName: oid("tabel") });
  };
  // kunci judul slide
  H.slide = (num, kicker, title, sec) => {
    const s = pres.addSlide({ masterName: "KONTEN", sectionTitle: H.SEC[num - 1] });
    // chip nomor gaya guidebook
    s.addText(String(num).padStart(2, "0"), { x: 0.4, y: 0.27, w: 0.42, h: 0.42, fontFace: FONT_H, fontSize: 13, bold: true, color: C.white, align: "center", valign: "middle", fill: { color: C.navy }, margin: 0, isTextBox: true, objectName: oid("nomor") });
    s.addText(kicker.toUpperCase(), { x: 0.92, y: 0.25, w: 9.5, h: 0.2, fontFace: FONT_H, fontSize: 8.5, bold: true, color: C.greenD, margin: 0, isTextBox: true, objectName: oid("kicker") });
    s.addText(title, { placeholder: "judul" });
    return s;
  };
  H.src = (s, text, abbr) => H.t(s, abbr ? [{ text: "Singkatan: " + abbr, options: { breakLine: true } }, { text: "Sumber: " + text }] : "Sumber: " + text, 0.4, 7.02, 12.15, 0.27, { fontSize: 5.9, color: C.slate, valign: "middle" });
  H.sec = (s, text, x, y, w, o = {}) => {
    H.t(s, text, x, y, w, 0.2, { fontFace: FONT_H, fontSize: o.fs || 8.5, bold: true, color: o.color || C.navy, valign: "middle" });
    H.ln(s, x, y + 0.21, x + w, y + 0.21, { color: o.lc || C.green, w: 1.25, arrow: false });
  };
  return H;
}
module.exports = { C, FONT_H, FONT_B, THEME, D, fmt, pct, usdM, num, NF, NF1, NF2, mk, ROOT, oid };
