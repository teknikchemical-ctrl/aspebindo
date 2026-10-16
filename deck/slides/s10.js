// Slide 10: Kesimpulan
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, pk = D.pks, gt = k.gates;
  const s = H.slide(10, "Kesimpulan: konsep {{layak teknis dan berdampak besar}}, tetapi {{layak komersial hanya bersyarat}}; langkah berikutnya adalah pilot dan kuotasi senilai USD 1,3 juta",
    "Kesimpulan. Tiga pesan, kartu skor, syarat kelayakan terukur, langkah berikutnya dengan dana, dan penutup berbasis bukti.");
  // ---- tiga pesan
  const msg = [["1  Masalah nyata", "±1.150 PKS melepas ≈ 26 juta tCO₂e per tahun metana; PKS bersolar berat membayar USD " + fmt(pk.diesel_cost / 1e6, 2) + " juta per tahun untuk listrik diesel.", C.navy],
               ["2  Solusi kredibel", "Neraca massa menutup 0,0002%; reaktor 5 hari; " + fmt(D.yield.kwh_net_m3_year, 0) + " kWh neto per m³ POME; genset dan tangki GFS teknologi matang. TRL sistem 4.", C.royal],
               ["3  Ekonomi bersyarat", "Set 60 t TBS/jam: NPV USD " + fmt(k.NPV / 1e6, 2) + " juta, IRR " + fmt(k.IRR * 100, 1) + "%, DSCR " + fmt(k.DSCR, 2) + "; PKS hemat " + fmt(pk.save_pct * 100, 1) + "% tanpa modal. Peluang NPV positif " + fmt(k.mc.p_pos * 100, 0) + "% kini.", C.green]];
  msg.forEach(([a, b, c], i) => { const x = 0.45 + i * 4.2; H.hdr(s, a, x, 1.25, 4.1, { fill: c, h: 0.27, fs: 10 }); H.rect(s, x, 1.52, 4.1, 0.78, { fill: C.white, line: c, radius: 0, lw: 1 }); H.t(s, b, x + 0.1, 1.58, 3.9, 0.7, { fontSize: 9.5 }); });
  // ---- kartu skor
  H.hdr(s, "Kartu skor kesiapan (1–5)", 0.45, 2.45, 4.1, { h: 0.25, fs: 9.5 });
  const sc = [["Kelayakan teknis", 3, "TRL 4; neraca menutup"], ["Daya tarik ekonomi", 2.5, "IRR ≈ WACC; median Monte Carlo negatif"], ["Kesiapan pasar", 2.5, "SAM ±57 PKS; filter hipotesis"], ["Keberlanjutan", 4.5, "−96% metana; titik panas efluen"], ["Risiko implementasi", 2, "tarif/izin PLN; kinerja termofilik"]];
  sc.forEach(([a, v, t], i) => { const y = 2.78 + i * 0.5; H.t(s, a, 0.45, y, 1.4, 0.2, { fontSize: 9, bold: true, color: C.navy, valign: "middle" }); H.rect(s, 1.9, y + 0.02, 2.6, 0.17, { fill: C.grey, line: null }); H.box(s, fmt(v, 1), 1.9, y + 0.02, 2.6 * v / 5, 0.17, { fs: 7.8, bold: true, color: C.white, fill: v >= 4 ? C.green : v >= 3 ? C.royal : C.amber, line: null, radius: 0, margin: 0 }); H.t(s, t, 0.45, y + 0.2, 4.1, 0.18, { fontSize: 7.5, color: C.slate }); });
  // ---- syarat kelayakan
  H.hdr(s, "Syarat kelayakan terukur (di bawahnya NPV < 0)", 4.7, 2.45, 4.25, { fill: C.red, h: 0.25, fs: 9.5 });
  H.table(s, [["Parameter", "Ambang", "Dasar"], ["Solar tergantikan (L/t TBS)", "≥ 1,84", "2,0"], ["Beban PKS (% nameplate)", "≥ " + fmt(k.bep_util_npv * 100, 0), "75"], ["Fee jasa (USD/t TBS)", "≥ " + fmt(k.bep.fee_be, 2), fmt(D.meta.fee, 2)], ["Tarif ekspor PLN (USc/kWh)", "≥ " + fmt(k.bep.tariff1_be, 2), "9,81"], ["CAPEX (FCI)", "≤ USD 5,9 juta", "5,74 (2026)"], ["Harga karbon (USD/t)", "≥ " + fmt(k.bep.p_carbon_be, 1), "5,0"], ["Produksi biogas (% desain)", "≥ " + fmt(k.bep.emult_be * 100, 0), "100"]], 4.7, 2.75, [2.05, 1.15, 1.05], { fs: 8.2, rh: 0.26, align: ["left", "center", "center"] });
  H.t(s, "Ambang diperoleh dari titik impas model (NPV = 0 satu variabel per kali); margin pengaman tipis, sehingga semua syarat harus dibuktikan di gerbang G0–G3.", 4.7, 4.88, 4.25, 0.3, { fontSize: 7.5, color: C.slate });
  // ---- langkah berikutnya
  H.hdr(s, "Langkah berikutnya dan dana (≤ 30 bulan)", 9.1, 2.45, 3.8, { fill: C.teal, h: 0.25, fs: 9.5 });
  H.table(s, [["Langkah", "Hasil terukur", "USD ribu"], ["Data PKS mitra", "solar ≥ 2,0 L/t", "60"], ["Uji lab + pilot", "COD ≥ 65%; TRL 6", "480"], ["Kuotasi + FEED + HAZOP", "FCI ≤ USD 6,0 juta", "380"], ["Izin dan hukum", "PJBL, IUPTLS", "130"], ["Tim dan MRV", "set 1 siap FID", "250"], [{ text: "Total", options: { bold: true } }, "", { text: "1.300", options: { bold: true, align: "right" } }]], 9.1, 2.75, [1.5, 1.5, 0.8], { fs: 7.8, rh: 0.26, align: ["left", "left", "right"] });
  H.t(s, "Usulan, belum berkomitmen. Peluang NPV positif: " + gt.map((g) => fmt(g.p * 100, 0) + "%").slice(0, 5).join(" → ") + " setelah tiap gerbang.", 9.1, 4.88, 3.8, 0.3, { fontSize: 7.5, color: C.slate });
  // ---- uji penentang
  H.hdr(s, "Uji penentang: titik terlemah yang masih terbuka", 0.45, 5.25, 12.45, { fill: C.navy, h: 0.24, fs: 9 });
  const rt = [["Teknis", "OLR 9,9 > 8 rekomendasi; belum skala penuh"], ["Keuangan", "GFS USD 200/m³ belum dikuotasi"], ["Pesaing", "B/C lebih murah bila PKS punya modal"], ["Eksekusi", "struktur jual listrik dan tarif belum pasti"], ["Keberlanjutan", "MCF efluen 0,3 belum diukur"]];
  rt.forEach(([a, b], i) => { const x = 0.45 + i * 2.5; H.box(s, [{ text: a, options: { bold: true, fontSize: 8.5, color: C.red, breakLine: true } }, { text: b, options: { fontSize: 7.8 } }], x, 5.52, 2.43, 0.52, { fill: C.redL, line: C.red, radius: 0.04, align: "left", margin: [1, 5, 1, 5] }); });
  H.box(s, [{ text: "Penutup  ", options: { bold: true, color: C.teal } }, { text: "Metana POME sudah dapat ditangkap; yang belum ada adalah cara PKS membayarnya tanpa menanggung risiko. Satu set 60 t TBS/jam menghindari ≈ " + fmt(D.lca.net_total / 1000, 0) + " ribu tCO₂e per tahun. Kami hanya membangun setelah data PKS, kuotasi, dan izin membuktikannya." }], 0.45, 6.1, 12.45, 0.5, { fs: 9.5, align: "left", fill: C.white, line: C.navy, lw: 1.25, radius: 0.04, margin: [1, 8, 1, 8], color: C.ink });
  H.src(s, "ringkasan slide 2–9 (fin_core.py v4; BG_Model_Keuangan.xlsx); skor kartu adalah penilaian tim atas bukti pada slide terkait.", "TRL tingkat kesiapan teknologi; OLR laju beban organik; FEED desain rekayasa awal; FID keputusan investasi akhir; MCF faktor koreksi metana; PJBL perjanjian jual beli listrik; IUPTLS izin usaha penyediaan tenaga listrik untuk kepentingan sendiri.");
};
