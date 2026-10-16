// Slide 6: Analisis pesaing
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const P = D.pesaing, pk = D.pks, k = D.keu;
  const s = H.slide(6, "Pesaing lebih murah dalam modal, tetapi hanya layanan BOO kami yang memberi {{modal PKS nol dan risiko di operator}}",
    "Pesaing. Peta posisi memakai dua sumbu terukur dari Model Keputusan PKS: modal yang ditanggung PKS dan biaya POME terlevelisasi per t TBS. Porter, PESTLE, SWOT dan TOWS ditutup dengan strategi masuk.");
  // ---------- tabel pembanding
  H.hdr(s, "Pembanding teknologi dan model penyampaian (per PKS 60 t TBS/jam)", 0.45, 1.25, 7.6, { h: 0.25, fs: 9.5 });
  const sc = P.rows.map((r) => fmt(r.total, 2)); const g = (t, bold) => ({ text: t, options: { bold: !!bold, align: "center" } });
  const cap = (t) => ({ text: t, options: { align: "center" } });
  const rows = [["Opsi", "Modal PKS (USD juta)", "Biaya POME PKS (USD/t TBS)", "Risiko kinerja", "TRL", "Referensi di Indonesia", "Skor"],
    ["A  Status quo kolam", cap("0"), cap(fmt(pk.per_t.A, 2)), cap("—"), cap("9"), "±85–90% PKS", g(sc[0])],
    ["B  Lagun tertutup (milik PKS)", cap(fmt(pk.capex.B / 1e6, 1)), cap(fmt(pk.per_t.B, 2)), cap("PKS"), cap("9"), "Sei Mangkei 2,4 MW", g(sc[1])],
    ["C  CSTR mesofilik (milik PKS)", cap(fmt(pk.capex.C / 1e6, 1)), cap(fmt(pk.per_t.C, 2)), cap("PKS"), cap("9"), "TSE 2 MW (2025)", g(sc[2])],
    ["D  Biometana BOOT (klaster)", cap("0"), cap("n/a"), cap("pengembang"), cap("8"), "PTPN IV, 8 PKS (2026)", g(sc[3])],
    ["E  UASB/IC", cap("±4,4"), cap("n/a"), cap("PKS"), cap("6"), "belum ada untuk POME", g(sc[4])],
    ["F  AnMBR", cap("±8,0"), cap("n/a"), cap("PKS"), cap("5"), "belum ada untuk POME", g(sc[5])],
    [{ text: "G  Kontak termofilik BOO (usulan)", options: { bold: true, fill: { color: C.greenL } } }, { text: "0", options: { bold: true, align: "center", fill: { color: C.greenL } } }, { text: fmt(pk.per_t.D, 2), options: { bold: true, align: "center", fill: { color: C.greenL } } }, { text: "operator", options: { bold: true, align: "center", fill: { color: C.greenL } } }, { text: "4", options: { bold: true, align: "center", fill: { color: C.greenL } } }, { text: "belum (perlu pilot)", options: { bold: true, fill: { color: C.greenL } } }, { text: sc[6], options: { bold: true, align: "center", color: C.white, fill: { color: C.green } } }]];
  H.table(s, rows, 0.45, 1.52, [2.2, 0.8, 1.0, 0.85, 0.4, 1.8, 0.55], { fs: 8.2, rh: 0.22, hrh: 0.36 });
  H.t(s, "Biaya POME PKS = biaya terlevelisasi 20 tahun (Model Keputusan PKS, solar tergantikan 2,0 L/t TBS); opsi D–F tanpa data biaya publik. Skor 1–5 berbobot (K1–K7, slide 2).", 0.45, 3.43, 7.6, 0.2, { fontSize: 7.3, color: C.slate });
  // ---------- peta posisi (bentuk manual, sumbu terukur)
  const X0 = 8.2, W0 = 4.7;
  H.hdr(s, "Peta posisi: modal PKS vs biaya POME PKS (model)", X0, 1.25, W0, { fill: C.teal, h: 0.25, fs: 9.5 });
  const px0 = X0 + 0.55, py0 = 3.2, pw = 3.95, ph = 1.45, xr = [0, 4.5], yr = [1.4, 3.4];
  H.rect(s, px0, py0 - ph, pw, ph, { fill: C.white, line: C.line, radius: 0 });
  const X = (v) => px0 + (v - xr[0]) / (xr[1] - xr[0]) * pw, Y = (v) => py0 - (v - yr[0]) / (yr[1] - yr[0]) * ph;
  [1.5, 2.0, 2.5, 3.0].forEach((v) => { H.ln(s, px0, Y(v), px0 + pw, Y(v), { color: "E3ECF4", w: 0.5, arrow: false }); H.t(s, fmt(v, 1), px0 - 0.35, Y(v) - 0.07, 0.3, 0.14, { fontSize: 7.5, align: "right", color: C.slate }); });
  [0, 1, 2, 3, 4].forEach((v) => H.t(s, String(v), X(v) - 0.15, py0 + 0.02, 0.3, 0.14, { fontSize: 7.5, align: "center", color: C.slate }));
  H.t(s, "Modal yang dikeluarkan PKS (USD juta)", px0, py0 + 0.17, pw, 0.15, { fontSize: 7.8, align: "center", bold: true, color: C.navy });
  H.t(s, "USD/t TBS", X0 - 0.02, py0 - ph - 0.0, 0.55, 0.14, { fontSize: 7.5, bold: true, color: C.navy });
  [["A", 0, pk.per_t.A, C.slate], ["B", pk.capex.B / 1e6, pk.per_t.B, C.mid], ["C", pk.capex.C / 1e6, pk.per_t.C, C.mid], ["G", 0, pk.per_t.D, C.green]].forEach(([l, x, y, c]) => {
    H.box(s, l, X(x) - 0.12 + (l === "G" ? 0.32 : (x === 0 ? 0.05 : 0)), Y(y) - 0.12, 0.24, 0.24, { fs: 9, bold: true, color: C.white, fill: c, line: C.white, lw: 1, radius: 0.14, margin: 0, font: FONT_H });
  });
  H.t(s, "G: modal nol, biaya setara kolam (A). B dan C lebih murah tetapi menuntut USD 3,5–4,0 juta dan risiko kinerja di PKS.", px0 - 0.4, py0 + 0.36, pw + 0.4, 0.3, { fontSize: 7.5, color: C.ink });
  // ---------- Porter, PESTLE, SWOT/TOWS
  const Y2 = 3.7;
  H.hdr(s, "Lima kekuatan Porter (1–5)", 0.45, Y2, 3.55, { h: 0.24, fs: 9 });
  const fo = [["Pembeli (PKS, PLN)", "Pembeli", "fee harus < biaya yang dihindari PKS"], ["Persaingan", "Persaingan", "BOOT reNIKOLA, EPC lagun, program grup"], ["Produk substitusi", "Produk substitusi", "kolam murah; PLTS + baterai"], ["Pendatang baru", "Pendatang baru", "izin PLN, modal USD 5,9 juta"], ["Pemasok", "Pemasok", "genset 6–9 bulan; GFS banyak"]];
  fo.forEach(([a, key, n], i) => { const v = D.porter[key].reduce((q, b) => q + b.s, 0) / D.porter[key].length, y = Y2 + 0.28 + i * 0.32; H.t(s, a, 0.45, y, 1.3, 0.16, { fontSize: 8, bold: true, color: C.navy }); H.rect(s, 1.78, y + 0.01, 1.4, 0.14, { fill: C.grey, line: null }); H.rect(s, 1.78, y + 0.01, 1.4 * v / 5, 0.14, { fill: v >= 3.5 ? C.red : v >= 3 ? C.amber : C.green, line: null }); H.t(s, fmt(v, 1), 3.22, y, 0.3, 0.16, { fontSize: 8, bold: true }); H.t(s, n, 0.45, y + 0.15, 3.5, 0.14, { fontSize: 7.2, color: C.slate }); });
  H.hdr(s, "PESTLE → keputusan", 4.15, Y2, 4.0, { h: 0.24, fs: 9 });
  H.table(s, [["Faktor", "Kondisi", "Keputusan"], ["Politik", "Perpres 112/2022: tarif plafon", "dasar tarif 9,81 USc, tanpa F"], ["Ekonomi", "solar Rp 21.000/L; suku bunga tinggi", "target PKS solar-berat; utang 58%"], ["Sosial", "bau POME; kerja lokal", "kontrak komunitas; 10 pekerja"], ["Teknologi", "TRL 4 termofilik", "pilot wajib sebelum FID"], ["Hukum", "IUPTLS/PJBL belum pasti", "kontrak jasa energi"], ["Lingkungan", "ISPO 2027, RED II", "nilai penangkapan metana naik"]], 4.15, Y2 + 0.28, [0.7, 1.7, 1.6], { fs: 7.4, rh: 0.25, hrh: 0.2 });
  H.hdr(s, "SWOT → TOWS", 8.3, Y2, 4.6, { h: 0.24, fs: 9 });
  const sw = [["KEKUATAN", "modal PKS nol; portabel; HRT 5 hari", C.green], ["KELEMAHAN", "TRL 4; CAPEX/kWe tinggi; skala min. 60 t/jam", C.red], ["PELUANG", "ISPO 2027; ±1.150 PKS tanpa penangkap", C.royal], ["ANCAMAN", "izin/tarif PLN; karbon rendah; program grup", C.amber]];
  sw.forEach(([a, b, c], i) => { const x = 8.3 + (i % 2) * 2.32, y = Y2 + 0.28 + Math.floor(i / 2) * 0.45; H.box(s, [{ text: a, options: { bold: true, fontSize: 8, color: c, breakLine: true } }, { text: b, options: { fontSize: 7.6 } }], x, y, 2.28, 0.42, { fill: C.white, line: c, lw: 1.25, radius: 0.04, align: "left", margin: [1, 5, 1, 5] }); });
  H.table(s, [["Strategi TOWS", "Tindakan"], ["SO", "kontrak percontohan sebelum ISPO 2027"], ["WO", "pilot untuk TRL 6; jaminan kinerja bertahap"], ["ST", "kontrak jasa energi; tarif dasar konservatif"], ["WT", "mulai 60 t/jam; kuotasi vendor sebelum FID"]], 8.3, Y2 + 1.2, [1.1, 3.5], { fs: 7.4, rh: 0.19 });
  // ---------- strategi masuk
  const st = [["Segmen awal", "PKS independen 60 t TBS/jam, solar tergantikan ≥ 2 L/t, jaringan 20 kV ≤ 2 km: ±" + fmt(D.pasar.rows[2].sets, 0) + " PKS"], ["Kemitraan", "PKS mitra pilot, kontraktor EPC lokal, laboratorium universitas, vendor genset/GFS"], ["Harga", "fee USD " + fmt(D.meta.fee, 2) + "/t TBS + USD 0,20/kWh: di dalam jendela USD 1,19–1,39"], ["Pembeda dijaga", "jaminan kinerja, portabilitas, data operasi; hambatan: izin PLN, kontrak 20 tahun"]];
  st.forEach(([a, b], i) => { const x = 0.45 + i * 3.14; H.box(s, [{ text: a, options: { bold: true, fontSize: 8.5, color: C.navy, breakLine: true } }, { text: b, options: { fontSize: 7.6 } }], x, 5.9, 3.05, 0.55, { fill: C.panel, line: C.line, radius: 0.04, align: "left", margin: [2, 6, 2, 6] }); });
  H.concl(s, "Kami tidak menang pada biaya modal atau kematangan; kami menang pada siapa yang menanggung modal dan risiko. Karena itu pasar awal hanya PKS tanpa modal dengan solar berat, dan klaim harus dibuktikan pilot.", "Kesimpulan");
  H.src(s, "research/R3 (pesaing: reNIKOLA, KIS, TSE, AANE), R2, R6; Model Keputusan PKS (finance/fin_mill.py); skor K2–K7 penilaian tim.", "TRL tingkat kesiapan teknologi; BOOT bangun-miliki-operasikan-alihkan; UASB/IC reaktor lumpur aktif aliran ke atas; AnMBR reaktor membran anaerob; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri; PJBL perjanjian jual beli listrik; FID keputusan investasi akhir.");
};
