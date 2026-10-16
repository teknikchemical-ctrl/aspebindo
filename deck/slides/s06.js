// Slide 6: Analisis pesaing dan posisi pasar
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const P = D.pesaing, t = D.tgt;
  const s = H.slide(6, "Pesaing kuat di klaster besar dan modal sendiri; {{BOO termofilik}} menempati ruang kosong, yaitu PKS independen tanpa modal, dengan skor berbobot tertinggi (" + fmt(P.rows[6].total, 2) + ")",
    "Pesaing. Sumber: research/R3 (reNIKOLA, KIS, Pertamina NRE, Aiken Kakoki, TSE, AANE, program grup Wilmar/Musim Mas/Asian Agri, Veolia/Kubota). Skor berbobot K1-K7 (bobot: biaya POME 25%, modal PKS 20%, risiko kinerja 15%, kematangan 15%, lahan dan waktu 10%, metana dan bau 10%, dapat dipindah 5%); K2-K7 adalah penilaian tim. Peringkat 1 pada " + fmt(P.rankD_p * 100, 0) + "% dari 20.000 variasi bobot Dirichlet dan 7/7 uji bobot +-50%. Kelemahan yang dikelola: kematangan (TRL 4, pilot G3), CAPEX per kWe lebih tinggi dari tangki CSTR (TSE USD 1,8 juta/MW) sehingga skala dan kurva belajar menjadi kunci.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  H.hdr(s, "(a) Profil pesaing utama di Indonesia", 0.45, 1.25, 7.45, { h: 0.24, fs: 9.5 });
  const k = { fill: { color: C.greenL }, bold: true };
  const rows = [["Pesaing", "Model dan skala", "Kekuatan", "Celah yang kami isi"],
    ["reNIKOLA + PTPN IV", "BOO(T) biometana; 8 PKS, USD 40–45 juta, kontrak gas 15 tahun (2026)", "modal besar, offtake pasti", "PKS di luar klaster dan pipa gas"],
    ["KIS Group + Toyota Tsusho", "teknologi → BOOT; biometana ke PGN, 150 ribu MMBtu/th (2027)", "rekam jejak sejak 2013", "fokus gas; skala klaster"],
    ["Pertamina NRE + PTPN III", "IPP PLTBg Sei Mangkei 2,4 MW, lagun tertutup ±2 ha", "dukungan BUMN", "lahan ±2 ha; hanya aset BUMN"],
    ["Aiken Kakoki + PTPN IV", "EPC dan teknologi; Sei Garo, beroperasi Nov 2025 (±24 bulan)", "teknologi Jepang", "waktu bangun; modal di PKS"],
    ["TSE Group", "milik sendiri; 2 tangki 7.800 m³, 2 MW, USD 3,6 juta", "CAPEX per MW rendah", "modal dan risiko di PKS"],
    ["AANE (Austindo)", "IPP POME komersial pertama, Belitung, jual ke PLN", "pengalaman PPA PLN", "lagun; satu lokasi"],
    ["Wilmar, Musim Mas, Asian Agri", "program internal: 25, 17, dan ±7–20 fasilitas", "modal dan skala", "tidak melayani PKS lain"],
    ["Veolia Memthane, Kubota", "AnMBR; belum ada referensi POME", "teknologi membran", "CAPEX ±USD 5 juta"],
    [{ text: "KAMI: kontak termofilik BOO", options: k }, { text: "modal PKS nol; HRT 5 hari; modul 21 kontainer; fee USD " + fmt(t.fee, 2) + "/t", options: k }, { text: "portabel, tanpa pipa gas", options: k }, { text: "pilot 2027–28: TRL 4 → 7", options: k }]];
  H.table(s, rows.map((r, i) => i === 0 || i === 9 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, r[1], r[2], r[3]]), 0.45, 1.5, [1.55, 2.75, 1.5, 1.65], { fs: 7.2, rh: 0.262, hrh: 0.24, margin: [1, 3, 1, 3] });
  H.hdr(s, "(b) Peta posisi pesaing (dari skor)", 7.95, 1.25, 4.95, { fill: C.teal, h: 0.24, fs: 9.5 });
  img("f_posisi2.png", 7.95, 1.5, 4.95, 2.33 * 4.95 / 5.0 * 1.0, "grafik-posisi");
  H.box(s, "Peringkat 1 pada " + fmt(P.rankD_p * 100, 0) + "% dari 20.000 variasi bobot dan pada 7/7 uji ±50%", 7.95, 3.85, 4.95, 0.28, { fs: 8.2, bold: true, color: C.navy, fill: C.greenL, line: C.green, radius: 0.05 });
  const Y = 4.2;
  H.hdr(s, "(c) Peta panas skor (1–5)", 0.45, Y, 4.0, { h: 0.23, fs: 9 });
  img("f_heatskor.png", 0.45, Y + 0.25, 4.0, 4.0 * 2.05 / 4.3, "grafik-heatskor");
  H.hdr(s, "(d) Segmentasi pasar: siapa melayani siapa", 4.55, Y, 4.3, { fill: C.teal, h: 0.23, fs: 9 });
  img("f_segmen.png", 4.55, Y + 0.25, 4.3, 4.3 * 2.05 / 4.1, "grafik-segmen");
  H.hdr(s, "(e) Lima kekuatan Porter", 8.95, Y, 3.95, { h: 0.23, fs: 9 });
  img("f_porter.png", 8.95, Y + 0.25, 3.95, 3.95 * 2.05 / 3.8, "grafik-porter");
  H.concl(s, "Pesaing melayani klaster bergas atau PKS bermodal; kami melayani 57 PKS independen yang tidak tersentuh keduanya, tanpa modal PKS dan dengan skor tertinggi.", "Kesimpulan");
  H.src(s, "research/R3 dan R6 (reNIKOLA/The Star 2026, KIS, Pertamina NRE, InfoSawit TSE 2025, Petromindo Sei Garo); Model Keputusan PKS (fin_mill.py); bobot dan skor K2–K7 penilaian tim; 20.000 variasi bobot Dirichlet.", "BOO bangun-miliki-operasikan; BOOT bangun-miliki-operasikan-alihkan; IPP produsen listrik swasta; PLTBg pembangkit listrik tenaga biogas; AnMBR reaktor membran anaerob; HRT waktu tinggal hidraulik; TRL tingkat kesiapan teknologi; PPA perjanjian jual beli listrik.");
};
