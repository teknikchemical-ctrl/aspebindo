// Slide 7: Model keuangan
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, m = D.meta, cf = k.cf, i3 = 3;
  const img = (f, x, y, w, h, n) => pres.slides[pres.slides.length - 1].addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  const s = H.slide(7, "Hitungannya lolos, tetapi tipis: {{NPV USD " + fmt(k.NPV / 1e6, 2) + " juta, IRR " + fmt(k.IRR * 100, 1) + "%}}, dan baru impas bila PKS memakai " + fmt(k.bep_util_npv * 100, 0) + "% kapasitasnya",
    "Keuangan. Konfigurasi 60 t TBS/jam + PM-12. Semua angka berasal dari model Excel berumus hidup (BG_Model_Keuangan.xlsx) yang cocok dengan model Python sampai sen. Asumsi: umur 20 tahun (2028-2047), USD nominal, inflasi 2%, pajak 22%, beban PKS 75%, ketersediaan 93%, fee USD 1,25 per t TBS, listrik ke PKS USD 0,20/kWh, ekspor PLN 9,81 USc/kWh, karbon USD 5/t.");
  const rv = cf.rev[i3], eb = cf.ebitda[i3];
  const kp = [["USD " + fmt(k.FCI / 1e6, 2) + " juta", "Investasi (FCI 2027)\nUSD " + fmt(k.FCI26 / k.chp, 0) + "/kWe terpasang"], ["USD " + fmt(rv / 1e6, 2) + " juta", "Pendapatan tahun penuh\nbeban PKS 75%"], ["USD " + fmt(eb / 1e6, 2) + " juta", "EBITDA tahun penuh\nmargin " + fmt(eb / rv * 100, 0) + "%"],
    ["USD " + fmt(k.NPV / 1e6, 2) + " juta", "NPV proyek, 20 tahun\nWACC " + fmt(k.WACC * 100, 1) + "%"], [fmt(k.IRR * 100, 1) + "%", "IRR proyek\nekuitas " + fmt(k.IRR_eq * 100, 1) + "% (< biaya ekuitas 15%)"], [fmt(k.PBP, 1) + " tahun", "Payback sejak operasi\nDSCR minimum " + fmt(k.DSCR, 2)]];
  kp.forEach(([b, l], i) => { const x = 0.45 + i * 2.085, w = 2.0, red = i === 4; H.rect(s, x, 1.25, w, 0.66, { fill: C.white, line: red ? C.red : C.teal, radius: 0.05, lw: 1 });
    H.t(s, b, x + 0.05, 1.27, w - 0.1, 0.3, { fontFace: FONT_H, fontSize: 14, bold: true, color: red ? C.red : C.navy, align: "center", valign: "middle" });
    H.t(s, l, x + 0.05, 1.57, w - 0.1, 0.32, { fontSize: 7.4, color: C.slate, align: "center" }); });
  // baris A
  H.hdr(s, "(a) Rincian CAPEX bottom-up: USD " + fmt(k.FCI26 / 1e6, 2) + " juta (harga 2026, kelas estimasi 4)", 0.45, 2.0, 6.15, { h: 0.22, fs: 9 });
  img("f_capex.png", 0.45, 2.24, 6.15, 2.0, "grafik-capex");
  H.hdr(s, "(b) Rincian 8 pos OPEX tunai: USD " + fmt(k.opF / 1000 + k.opV / 1000 + 12, 0) + " ribu per tahun", 6.75, 2.0, 6.15, { fill: C.teal, h: 0.22, fs: 9 });
  img("f_opex.png", 6.75, 2.24, 6.15, 2.0, "grafik-opex");
  // baris B
  H.hdr(s, "(c) Titik impas terhadap beban PKS", 0.45, 4.3, 4.0, { h: 0.22, fs: 9 });
  img("f_bep.png", 0.45, 4.54, 4.0, 1.88, "grafik-bep");
  H.hdr(s, "(d) Kurva payback: arus kas kumulatif", 4.55, 4.3, 4.6, { fill: C.teal, h: 0.22, fs: 9 });
  img("f_payback.png", 4.55, 4.54, 4.6, 1.88, "grafik-payback");
  H.hdr(s, "(e) Ringkasan ekonometrik", 9.25, 4.3, 3.65, { h: 0.22, fs: 9 });
  const eq = [["WACC · biaya utang", fmt(k.WACC * 100, 1) + "% · " + fmt(m.r_debt * 100, 0) + "%"], ["Struktur modal", fmt(m.debt * 100, 0) + "% utang · " + (100 - Math.round(m.debt * 100)) + "% ekuitas"], ["DSCR minimum · rata-rata", fmt(k.DSCR, 2) + " · " + fmt(k.DSCR_avg, 2)], ["Indeks profitabilitas", fmt(k.PI, 2)], ["Payback terdiskonto", fmt(k.DPBP, 1) + " tahun"], ["LCOE kotor · bersih*", "USD " + fmt(k.LCOE, 3) + " · " + fmt(k.LCOE_net, 3)],
    ["Impas tunai · akuntansi · NPV", fmt(k.bep_util_cash * 100, 0) + " · " + fmt(k.bep_util_acc * 100, 0) + " · " + fmt(k.bep_util_npv * 100, 0) + "%"], ["Peluang NPV > 0 (Monte Carlo)", fmt(k.mc.p_pos * 100, 0) + "% (P50 USD " + fmt(k.mc.P50 / 1e6, 2) + " juta)"]];
  H.table(s, eq.map((r, i) => [{ text: r[0], options: { bold: true, color: C.navy } }, { text: r[1], options: { align: "right", bold: i === 7, color: i === 7 ? C.red : C.ink } }]), 9.25, 4.54, [1.75, 1.9], { fs: 7.6, rh: 0.222, head: 0 });
  H.t(s, "*Bersih: setelah dikurangi pendapatan fee dan karbon.", 9.25, 6.31, 3.65, 0.14, { fontSize: 6.3, color: C.slate });
  H.concl(s, "Satu set 60 t TBS/jam hanya layak jika PKS memakai ≥ " + fmt(k.bep_util_npv * 100, 0) + "% kapasitas, fee ≥ USD " + fmt(k.bep.fee_be, 2) + "/t, dan CAPEX tidak naik lebih dari 2%; peluang NPV positif baru 25%, dan gerbang G0–G3 yang menaikkannya.", "Kesimpulan");
  H.src(s, "BG_Model_Keuangan.xlsx; finance/fin_core.py v4 (60 t TBS/jam + tangki ekualisasi PM-12, USD nominal); Monte Carlo 4.000 iterasi; research/R2 dan R6.", "FCI biaya modal tetap; WACC biaya modal rata-rata tertimbang; DSCR rasio cakupan layanan utang; LCOE biaya listrik terlevelisasi; MRV pemantauan, pelaporan, verifikasi; O&M operasi dan pemeliharaan.");
};
