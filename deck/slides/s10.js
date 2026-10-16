// Slide 10: Kesimpulan
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, pk = D.pks, gt = k.gates, lc = D.lca;
  const s = H.slide(10, "Kesimpulan: konsepnya {{kuat secara teknis dan lingkungan}}, ekonominya {{baru layak bersyarat}}; kami minta USD 1,3 juta untuk membuktikan sisanya",
    "Kesimpulan. Tiga pesan, kartu skor sebelum dan sesudah gerbang, syarat kelayakan terukur, langkah berikutnya dengan dana, dan titik terlemah yang masih terbuka (uji penentang).");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  const msg = [["−" + fmt(lc.net_total / lc.base * 100, 0) + "%", "Masalahnya nyata", "Kolam POME satu PKS 60 t/jam melepas ±" + fmt(lc.base / 1000, 0) + " ribu tCO₂e metana per tahun, sementara PKS bersolar berat membayar USD " + fmt(pk.diesel_cost / 1e6, 2) + " juta per tahun untuk listrik diesel.", C.navy],
    ["0,0002%", "Solusinya kredibel", "Neraca massa menutup dengan galat 0,0002%. Satu m³ POME menjadi " + fmt(D.yield.kwh_net_m3_year, 0) + " kWh neto. Tangki GFS dan genset adalah teknologi matang; TRL sistem baru 4.", C.royal],
    [fmt(k.IRR * 100, 1) + "%", "Ekonominya bersyarat", "NPV USD " + fmt(k.NPV / 1e6, 2) + " juta, DSCR " + fmt(k.DSCR, 2) + ", PKS hemat " + fmt(pk.save_pct * 100, 1) + "% tanpa modal. Peluang NPV positif baru " + fmt(k.mc.p_pos * 100, 0) + "%; itu sebabnya gerbang data dahulu.", C.green]];
  msg.forEach(([b, a, t, c], i) => { const x = 0.45 + i * 4.2; H.rect(s, x, 1.25, 4.05, 1.35, { fill: C.white, line: c, radius: 0.05, lw: 1.25 }); H.rect(s, x, 1.25, 1.25, 1.35, { fill: c, line: null, radius: 0.05 });
    H.t(s, b, x, 1.25, 1.25, 1.35, { fontFace: FONT_H, fontSize: 17, bold: true, color: C.white, align: "center", valign: "middle" });
    H.t(s, a, x + 1.35, 1.3, 2.6, 0.26, { fontFace: FONT_H, fontSize: 10.5, bold: true, color: c, valign: "middle" }); H.t(s, t, x + 1.35, 1.58, 2.62, 1.0, { fontSize: 8.4 }); });
  // radar
  H.hdr(s, "Kartu skor kesiapan (1–5)", 0.45, 2.72, 3.5, { h: 0.24, fs: 9.5 });
  img("f_radar.png", 0.5, 2.98, 3.4, 2.37, "grafik-radar");
  // syarat
  H.hdr(s, "Syarat kelayakan: di bawah ini NPV < 0", 4.1, 2.72, 4.5, { fill: C.red, h: 0.24, fs: 9.5 });
  H.table(s, [["Parameter", "Ambang", "Dasar"], ["Solar tergantikan (L/t TBS)", "≥ " + fmt(1.84, 2), "2,0"], ["Beban PKS (% nameplate)", "≥ " + fmt(k.bep_util_npv * 100, 0), "75"], ["Fee jasa (USD/t TBS)", "≥ " + fmt(k.bep.fee_be, 2), fmt(D.meta.fee, 2)], ["Tarif ekspor PLN (USc/kWh)", "≥ " + fmt(k.bep.tariff1_be, 2), "9,81"], ["CAPEX (FCI 2026)", "≤ USD 5,9 juta", "5,74"], ["Harga karbon (USD/t)", "≥ " + fmt(k.bep.p_carbon_be, 1), "5,0"], ["Produksi biogas (% desain)", "≥ " + fmt(k.bep.emult_be * 100, 0), "100"]], 4.1, 2.98, [2.3, 1.2, 1.0], { fs: 8.6, rh: 0.29, align: ["left", "center", "center"] });
  H.t(s, "Ambang = titik impas NPV, satu variabel per kali. Margin tipis: semua syarat harus dibuktikan di G0–G3.", 4.1, 5.32, 4.5, 0.3, { fontSize: 7.6, color: C.slate });
  // langkah
  H.hdr(s, "Langkah berikutnya dan dana (≤ 30 bulan)", 8.75, 2.72, 4.15, { fill: C.teal, h: 0.24, fs: 9.5 });
  H.table(s, [["Langkah", "Hasil terukur", "USD ribu"], ["Data PKS mitra", "solar ≥ 2,0 L/t", "60"], ["Uji lab dan pilot", "COD ≥ 65%; TRL 6", "480"], ["Kuotasi, FEED, HAZOP", "FCI ≤ USD 6,0 juta", "380"], ["Izin dan hukum", "PJBL, IUPTLS", "130"], ["Tim dan MRV", "set 1 siap FID", "250"], [{ text: "Total", options: { bold: true } }, "", { text: "1.300", options: { bold: true, align: "right" } }]], 8.75, 2.98, [1.55, 1.6, 1.0], { fs: 8.6, rh: 0.29, align: ["left", "left", "right"] });
  H.t(s, "Usulan tim, belum berkomitmen. Peluang NPV positif per gerbang: " + gt.map((g) => fmt(g.p * 100, 0) + "%").join(" → ") + ".", 8.75, 5.05, 4.15, 0.4, { fontSize: 7.6, color: C.slate });
  // uji penentang
  H.hdr(s, "Uji penentang: lima titik terlemah yang masih terbuka", 0.45, 5.68, 12.45, { fill: C.navy, h: 0.22, fs: 9 });
  const rt = [["Teknis", "OLR 9,9 di atas rekomendasi 8; belum skala penuh"], ["Keuangan", "harga tangki GFS USD 200/m³ belum dikuotasi"], ["Pesaing", "opsi B/C lebih murah bila PKS punya modal"], ["Eksekusi", "struktur jual listrik dan tarif belum pasti"], ["Lingkungan", "MCF efluen 0,3 belum diukur"]];
  rt.forEach(([a, b], i) => H.box(s, [{ text: a + "  ", options: { bold: true, color: C.red } }, { text: b }], 0.45 + i * 2.5, 5.93, 2.45, 0.5, { fs: 7.8, fill: C.redL, line: C.red, radius: 0.04, align: "left", margin: [1, 5, 1, 5] }));
  H.concl(s, "Metana POME sudah bisa ditangkap; yang belum ada adalah cara PKS membayarnya tanpa menanggung risiko. Kami hanya membangun setelah data, kuotasi, dan izin membuktikannya.", "Penutup");
  H.src(s, "ringkasan slide 2–9 (fin_core.py v4; BG_Model_Keuangan.xlsx). Skor kartu adalah penilaian tim atas bukti pada slide terkait; sasaran setelah G3 adalah target, bukan hasil.", "TRL tingkat kesiapan teknologi; OLR laju beban organik; FEED desain rekayasa awal; FID keputusan investasi akhir; MCF faktor koreksi metana; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri.");
};
