// Slide 6: Analisis pesaing
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const P = D.pesaing, tg = D.tgt, tp = tg.pks;
  const s = H.slide(6, "Pesaing unggul pada satu sisi saja; hanya {{BOO termofilik}} memberi modal PKS nol, biaya POME turun " + fmt(tp.save_pct * 100, 0) + "%, dan skor tertinggi (" + fmt(P.rows[6].total, 2) + ")",
    "Pesaing. Skor berbobot K1-K7 (bobot: biaya POME 25%, modal PKS 20%, risiko kinerja 15%, kematangan 15%, lahan dan waktu 10%, penangkapan metana 10%, dapat dipindah 5%). Opsi G peringkat 1 pada " + fmt(P.rankD_p * 100, 0) + "% dari 20.000 variasi bobot Dirichlet dan pada 7 dari 7 uji bobot ±50%. Skor K2-K7 adalah penilaian tim. Biaya POME PKS dari Model Keputusan PKS pada kasus target (solar tergantikan 3,0 L/t). Kelemahan yang dikelola: TRL 4 (pilot di G3), skala minimum 60 t/jam; ancaman: izin dan tarif PLN, program grup besar.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  H.hdr(s, "(a) Skor berbobot tujuh opsi (tujuh kriteria)", 0.45, 1.25, 5.3, { h: 0.24, fs: 9.5 });
  img("f_skor.png", 0.45, 1.52, 5.3, 2.55, "grafik-skor");
  H.hdr(s, "(b) Perbandingan opsi", 5.85, 1.25, 4.0, { fill: C.teal, h: 0.24, fs: 9.5 });
  const cp = (t, o = {}) => ({ text: t, options: Object.assign({ align: "center" }, o) }), gf = { fill: { color: C.greenL }, bold: true };
  const R = P.rows, sc = (i) => fmt(R[i].total, 2);
  H.table(s, [["Opsi", "Modal PKS (USD juta)", "Biaya POME (USD/t TBS)", "Referensi Indonesia"],
    ["A  Kolam terbuka", cp("0"), cp(fmt(tp.per_t.A, 2)), "±85–90% PKS"], ["B  Lagun tertutup", cp(fmt(tp.capex.B / 1e6, 1)), cp(fmt(tp.per_t.B, 2)), "Sei Mangkei"], ["C  CSTR mesofilik", cp(fmt(tp.capex.C / 1e6, 1)), cp(fmt(tp.per_t.C, 2)), "TSE 2 MW (2025)"],
    ["D  Biometana BOOT", cp("0"), cp("n/a"), "PTPN IV (2026)"], ["E  UASB / IC", cp("±4,4"), cp("n/a"), "belum ada"], ["F  AnMBR", cp("±8,0"), cp("n/a"), "belum ada"],
    [{ text: "G  Termofilik BOO (kami)", options: gf }, cp("0", gf), cp(fmt(tp.per_t.D, 2), gf), { text: "pilot 2027–28", options: gf }]], 5.85, 1.52, [1.4, 0.7, 0.8, 1.1], { fs: 8, rh: 0.27, hrh: 0.42 });
  H.t(s, "Biaya POME: biaya terlevelisasi 20 tahun yang ditanggung PKS (solar 3,0 L/t); D–F tanpa data biaya publik.", 5.85, 3.78, 4.0, 0.25, { fontSize: 7, color: C.slate });
  H.hdr(s, "(c) Posisi modal vs biaya", 9.95, 1.25, 2.95, { h: 0.24, fs: 9.5 });
  img("f_posisi.png", 9.95, 1.55, 2.95, 1.88, "grafik-posisi");
  H.box(s, "Peringkat 1 pada " + fmt(P.rankD_p * 100, 0) + "% dari 20.000 variasi bobot; 7/7 uji ±50%", 9.95, 3.5, 2.95, 0.55, { fs: 8.5, bold: true, color: C.navy, fill: C.greenL, line: C.green, radius: 0.05 });
  // baris 2
  const Y = 4.17;
  H.hdr(s, "(d) Lima kekuatan Porter", 0.45, Y, 3.6, { h: 0.24, fs: 9.5 });
  img("f_porter.png", 0.45, Y + 0.27, 3.6, 1.95, "grafik-porter");
  H.hdr(s, "(e) PESTLE: dampak terhadap keputusan", 4.15, Y, 4.5, { fill: C.teal, h: 0.24, fs: 9.5 });
  H.table(s, [["Faktor", "Kondisi", "Keputusan kami"], ["Politik", "Perpres 112/2022: tarif plafon", "tarif dasar 9,81 USc, tanpa F"], ["Ekonomi", "solar Rp 21.000/L", "layani PKS solar-berat"], ["Sosial", "bau POME; kerja lokal", "10 pekerja lokal; kontrak komunitas"], ["Teknologi", "TRL 4 termofilik", "pilot 10–20 m³ sebelum FID"], ["Hukum", "IUPTLS dan PJBL", "kontrak jasa energi 20 tahun"], ["Lingkungan", "ISPO 2027, RED II", "nilai penangkapan metana naik"]], 4.15, Y + 0.27, [0.8, 1.7, 2.0], { fs: 8, rh: 0.275, hrh: 0.25 });
  H.hdr(s, "(f) SWOT → strategi TOWS", 8.75, Y, 4.15, { h: 0.24, fs: 9.5 });
  const q = [["SO · Masuk lebih dulu", "kontrak percontohan sebelum ISPO 2027; modal nol sebagai pembuka", C.green], ["WO · Buktikan lebih cepat", "pilot menaikkan TRL 4 → 6; jaminan kinerja bertahap", C.royal], ["ST · Kunci pendapatan", "kontrak jasa energi 20 tahun; tarif dasar tanpa F", C.teal], ["WT · Kecilkan risiko", "mulai di 60 t/jam; tiga kuotasi sebelum FID", C.navy]];
  q.forEach(([a, b, c], i) => { const x = 8.75 + (i % 2) * 2.1, y = Y + 0.3 + Math.floor(i / 2) * 1.0; H.rect(s, x, y, 2.05, 0.95, { fill: C.white, line: c, radius: 0.04, lw: 1.25 }); H.rect(s, x, y, 0.07, 0.95, { fill: c, line: null });
    H.t(s, [{ text: a, options: { bold: true, color: c, fontSize: 8.8, breakLine: true } }, { text: b, options: { fontSize: 8 } }], x + 0.14, y + 0.06, 1.85, 0.85, { valign: "top" }); });
  H.concl(s, "Pesaing menang di satu kriteria (modal atau biaya); kami unggul di keseluruhan: PKS tidak mengeluarkan modal, hemat " + fmt(tp.save_pct * 100, 0) + "% biaya POME, dan risiko kinerja ada pada operator.", "Kesimpulan");
  H.src(s, "research/R3 (reNIKOLA, KIS, TSE, AANE), R2, R6; Model Keputusan PKS (finance/fin_mill.py, kasus target); bobot dan skor K2–K7 penilaian tim; 20.000 variasi bobot Dirichlet.", "TRL tingkat kesiapan teknologi; BOOT bangun-miliki-operasikan-alihkan; UASB/IC reaktor lumpur aktif aliran ke atas; AnMBR reaktor membran anaerob; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri; PJBL perjanjian jual beli listrik; FID keputusan investasi akhir.");
};
