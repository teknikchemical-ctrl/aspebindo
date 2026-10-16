// Slide 6: Analisis pesaing dan posisi pasar
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const P = D.pesaing, t = D.tgt;
  const s = H.slide(6, "Pesaing melayani klaster dan PKS bermodal; {{BOO termofilik}} mengisi ruang kosong: PKS independen tanpa modal",
    "Pesaing. Sumber: research/R3 (reNIKOLA, KIS, Pertamina NRE, Aiken Kakoki, TSE, AANE, program grup, Veolia/Kubota). Skor berbobot K1-K7 (biaya POME 25%, modal PKS 20%, risiko kinerja 15%, kematangan 15%, lahan dan waktu 10%, metana dan bau 10%, dapat dipindah 5%); K2-K7 adalah penilaian tim. Peringkat 1 pada " + fmt(P.rankD_p * 100, 0) + "% dari 20.000 variasi bobot Dirichlet dan 7/7 uji bobot +-50%. Lima kekuatan Porter (intensitas 1-5): daya tawar pembeli 3,8; persaingan 3,5; produk substitusi 3,2; pendatang baru 2,8; pemasok 2,5. Titik yang dikelola: kematangan (TRL 4, pilot G3) dan CAPEX per kWe lebih tinggi dari tangki CSTR (TSE USD 1,8 juta/MW), sehingga skala dan kurva belajar menjadi kunci.");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  // ---------- A. siapa yang sudah bermain
  H.hdr(s, "A. Siapa yang sudah bermain di pengolahan POME Indonesia", 0.45, 1.25, 12.45, { h: 0.25, fs: 10 });
  const cards = [["Pengembang biometana (BOOT)", C.royal, "reNIKOLA + PTPN IV; KIS + Toyota Tsusho", "Membangun dan mengoperasikan, lalu menjual gas ke jaringan pipa. Bukti: 8 PKS PTPN IV, USD 40–45 juta, kontrak gas 15 tahun (2026).", "Perlu klaster PKS dan pipa gas; PKS di luar klaster tidak terlayani."],
    ["BUMN dan produsen listrik", C.navy, "Pertamina NRE + PTPN III; Aiken Kakoki + PTPN IV; AANE", "Memiliki pembangkit lagun tertutup: Sei Mangkei 2,4 MW (±2 ha), Sei Garo (Nov 2025), AANE Belitung (jual ke PLN).", "Terbatas pada aset BUMN dan grup; waktu bangun ±24 bulan."],
    ["Program internal dan CSTR milik sendiri", C.slate, "Wilmar (25), Musim Mas (17), Asian Agri (±7–20); TSE Group", "Modal sendiri. TSE: 2 tangki 7.800 m³, 2 MW, USD 3,6 juta (USD 1,8 juta/MW).", "PKS menanggung modal dan risiko kinerja; tidak melayani PKS lain."],
    ["Teknologi alternatif", C.mid, "UASB/IC; AnMBR (Veolia Memthane, Kubota)", "Reaktor lumpur aliran ke atas dan reaktor membran; efisien di industri lain.", "Belum ada referensi POME skala penuh; CAPEX ±USD 5 juta."]];
  cards.forEach(([h, c, who, how, gap], i) => { const x = 0.45 + i * 3.14, w = 3.05;
    H.hdr(s, h, x, 1.55, w, { fill: c, h: 0.26, fs: 9 }); H.rect(s, x, 1.81, w, 1.15, { fill: C.white, line: c, radius: 0, lw: 1 });
    H.t(s, [{ text: "Pemain: ", options: { bold: true, color: c } }, { text: who, options: { breakLine: true } }, { text: "Cara kerja: ", options: { bold: true, color: c } }, { text: how, options: { breakLine: true } }, { text: "Batasan: ", options: { bold: true, color: C.red } }, { text: gap }], x + 0.08, 1.84, w - 0.16, 1.1, { fontSize: 8.3, paraSpaceAfter: 2 }); });
  // ---------- B. tiga peta
  const Y = 3.05;
  H.hdr(s, "B. Peta posisi: seberapa ringan bagi PKS vs seberapa teruji", 0.45, Y, 4.7, { fill: C.teal, h: 0.24, fs: 8.8 });
  img("f_posisi2.png", 0.45, Y + 0.26, 4.7, 4.7 * 2.1 / 4.6, "grafik-posisi");
  H.take(s, "Biometana BOOT paling dekat dengan kami: sama ringannya bagi PKS dan lebih teruji, tetapi hanya untuk klaster berpipa gas. Kami belum teruji (pilot G3).", 0.45, Y + 0.26 + 2.14 + 0.04, 4.7, 0.5);
  H.hdr(s, "C. Skor tujuh kriteria (1 = lemah, 5 = unggul)", 5.25, Y, 3.95, { h: 0.24, fs: 8.8 });
  img("f_heatskor.png", 5.25, Y + 0.26 + 0.1, 3.95, 3.95 * 1.9 / 3.9, "grafik-heatskor");
  H.take(s, "Kami mencetak 5,0 pada modal PKS, penangkapan metana, dan kemudahan dipindah; tertinggal pada referensi (2,0) dan biaya POME (3,1). Skor total tertinggi: " + fmt(P.rows[6].total, 2) + ".", 5.25, Y + 0.26 + 2.14 + 0.04, 3.95, 0.5);
  H.hdr(s, "D. Segmentasi: siapa melayani siapa", 9.3, Y, 3.6, { fill: C.teal, h: 0.24, fs: 8.8 });
  img("f_segmen.png", 9.3, Y + 0.26 + 0.1, 3.6, 3.6 * 1.95 / 3.9, "grafik-segmen");
  H.take(s, "Kami memilih kuadran kiri-bawah: PKS independen bermodal terbatas. Pesaing BOO hari ini menyasar klaster berpipa gas; di kuadran kami ada 57 PKS (USD " + fmt(D.pasar.rows[2].rev / 1e6, 0) + " juta per tahun).", 9.3, Y + 0.26 + 2.14 + 0.04, 3.6, 0.5);
  // ---------- E. mengapa kami menang
  const Y3 = 6.02; const ch = [["Modal PKS nol", "skema BOO"], ["Hemat " + fmt(t.pks.save_pct * 100, 0) + "% biaya POME", "dibanding kolam"], ["Portabel", "21 kontainer, ±6 bulan"], ["Risiko kinerja di operator", "PKS membayar per ton TBS"], ["Peringkat 1: " + fmt(P.rankD_p * 100, 0) + "%", "dari 20.000 variasi bobot"]];
  ch.forEach(([a, b], i) => H.box(s, [{ text: a, options: { bold: true, fontSize: 9, color: C.white, breakLine: true } }, { text: b, options: { fontSize: 7.6, color: "DCEAF5" } }], 0.45 + i * 2.52, Y3, 2.4, 0.42, { fill: C.green, line: null, radius: 0.05 }));
  H.concl(s, "Pesaing kuat di klaster bergas dan PKS bermodal; kami unggul di segmen yang mereka lewati, dengan modal PKS nol dan skor berbobot tertinggi.", "Kesimpulan");
  H.src(s, "research/R3 dan R6 (The Star 2026, KIS, Pertamina NRE, InfoSawit TSE 2025, Petromindo Sei Garo); Model Keputusan PKS (fin_mill.py, kasus target); bobot dan skor K2–K7 penilaian tim; 20.000 variasi bobot Dirichlet.", "BOO bangun-miliki-operasikan; BOOT bangun-miliki-operasikan-alihkan; PKS pabrik kelapa sawit; POME limbah cair pabrik sawit; IPP produsen listrik swasta; UASB/IC reaktor lumpur aktif aliran ke atas; AnMBR reaktor membran anaerob; CSTR reaktor tangki berpengaduk; TRL tingkat kesiapan teknologi.");
};
