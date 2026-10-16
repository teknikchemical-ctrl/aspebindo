// Slide 7: Model keuangan (kasus target setelah gerbang G0-G2; kasus awal sebagai pembanding)
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, t = D.tgt, cf = t.cf, i3 = 3, b = t.chain[0];
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  const s = H.slide(7, "Setelah gerbang G0–G2, satu set 60 t TBS/jam bernilai {{NPV USD " + fmt(t.NPV / 1e6, 2) + " juta, IRR " + fmt(t.IRR * 100, 1) + "%}}, dan {{balik modal dalam " + fmt(t.PBP, 1) + " tahun}}",
    "Keuangan. Konfigurasi 60 t TBS/jam + PM-12. Kasus target = kasus awal + solar tergantikan 3,0 L/t (G0) + CAPEX -15% (G1, hasil kuotasi) + fee USD 1,35/t (G2, di dalam jendela 0,67-1,84) + karbon USD 8,3/t; selebihnya identik. Kasus awal (solar 2,0 L/t, fee 1,25, karbon 5,0, tanpa potongan CAPEX): NPV USD 0,13 juta, IRR 10,3%, payback 7,1 tahun, peluang NPV positif Monte Carlo 25% (naik setelah tiap gerbang). Semua angka dari model Excel berumus hidup dan Python (fin_core.py, deck/export_target.py). Batas aman kasus target: NPV tetap positif sampai beban PKS 54%, fee USD 0,26/t, CAPEX +47%, produksi gas 23% dari desain.");
  const rv = cf.rev[i3], eb = cf.ebitda[i3];
  const kp = [["USD " + fmt(t.FCI26 / 1e6, 2) + " juta", "Investasi (FCI, harga 2026)\nUSD " + fmt(t.FCI26 / k.chp, 0) + "/kWe terpasang"], ["USD " + fmt(rv / 1e6, 2) + " juta", "Pendapatan tahun penuh\n" + fmt(t.E_net, 1) + " GWh neto per tahun"], ["USD " + fmt(eb / 1e6, 2) + " juta", "EBITDA tahun penuh\nmargin " + fmt(eb / rv * 100, 0) + "%"],
    ["USD " + fmt(t.NPV / 1e6, 2) + " juta", "NPV proyek, 20 tahun\nWACC " + fmt(t.WACC * 100, 1) + "%"], [fmt(t.IRR * 100, 1) + "%", "IRR proyek\nIRR ekuitas " + fmt(t.IRR_eq * 100, 1) + "%"], [fmt(t.PBP, 1) + " tahun", "Payback sejak operasi\nDSCR minimum " + fmt(t.DSCR, 2)]];
  kp.forEach(([v, l], i) => { const x = 0.45 + i * 2.085, w = 2.0, hl = i >= 3; H.rect(s, x, 1.25, w, 0.68, { fill: hl ? C.navy : C.white, line: hl ? C.navy : C.teal, radius: 0.05, lw: 1 });
    H.t(s, v, x + 0.05, 1.27, w - 0.1, 0.32, { fontFace: FONT_H, fontSize: 15, bold: true, color: hl ? C.white : C.navy, align: "center", valign: "middle" });
    H.t(s, l, x + 0.05, 1.59, w - 0.1, 0.32, { fontSize: 7.6, color: hl ? "DCEAF5" : C.slate, align: "center" }); });
  // baris A
  H.hdr(s, "(a) CAPEX bottom-up: USD " + fmt(t.FCI26 / 1e6, 2) + " juta (2026)", 0.45, 2.02, 4.65, { h: 0.22, fs: 9 });
  img("f_capex.png", 0.45, 2.26, 4.65, 2.0, "grafik-capex");
  H.hdr(s, "(b) OPEX tunai: USD " + fmt(k.opF / 1000 + k.opV / 1000 + 12, 0) + " ribu per tahun", 5.2, 2.02, 4.65, { fill: C.teal, h: 0.22, fs: 9 });
  img("f_opex.png", 5.2, 2.26, 4.65, 2.0, "grafik-opex");
  H.hdr(s, "(c) Ringkasan ekonometrik", 9.95, 2.02, 2.95, { h: 0.22, fs: 9 });
  const g = { fill: { color: C.greenL }, bold: true, align: "center" }, ce = { align: "center" };
  const rows = [["Indikator", "Awal", "Target"], ["NPV (USD juta)", fmt(b.NPV / 1e6, 2), fmt(t.NPV / 1e6, 2)], ["IRR proyek", fmt(b.IRR * 100, 1) + "%", fmt(t.IRR * 100, 1) + "%"], ["IRR ekuitas", fmt(b.IRR_eq * 100, 1) + "%", fmt(t.IRR_eq * 100, 1) + "%"], ["Payback (tahun)", fmt(b.PBP, 1), fmt(t.PBP, 1)], ["Payback terdiskonto", fmt(b.DPBP, 1), fmt(t.DPBP, 1)], ["DSCR minimum", fmt(b.DSCR, 2), fmt(t.DSCR, 2)], ["Indeks profitabilitas", fmt(b.PI, 2), fmt(t.PI, 2)], ["LCOE bersih (USD/kWh)", fmt(b.LCOE_net, 3), fmt(t.LCOE_net, 3)]];
  H.table(s, rows.map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, { text: r[1], options: ce }, { text: r[2], options: g }]), 9.95, 2.26, [1.35, 0.7, 0.9], { fs: 8, rh: 0.222, hrh: 0.24 });
  // baris B
  H.hdr(s, "(d) Titik impas terhadap beban PKS", 0.45, 4.33, 4.0, { h: 0.22, fs: 9 });
  img("f_bep.png", 0.45, 4.57, 4.0, 1.88, "grafik-bep");
  H.hdr(s, "(e) Kurva payback: arus kas kumulatif", 4.55, 4.33, 4.6, { fill: C.teal, h: 0.22, fs: 9 });
  img("f_payback.png", 4.55, 4.57, 4.6, 1.88, "grafik-payback");
  H.hdr(s, "(f) Jembatan NPV: nilai tiap gerbang", 9.25, 4.33, 3.65, { h: 0.22, fs: 9 });
  img("f_bridge.png", 9.25, 4.57, 3.65, 1.88, "grafik-jembatan");
  H.concl(s, "NPV tetap positif sampai beban PKS turun ke " + fmt(t.be.util * 100, 0) + "% dan CAPEX naik +" + fmt((t.be.capex / t.capex_mult - 1) * 100, 0) + "%; tiap gerbang G0–G2 membuka nilai tambah yang terukur, dari NPV USD " + fmt(b.NPV / 1e6, 2) + " juta menjadi USD " + fmt(t.NPV / 1e6, 2) + " juta.", "Kesimpulan");
  H.src(s, "BG_Model_Keuangan.xlsx; finance/fin_core.py v4 (60 t TBS/jam + PM-12, USD nominal, 20 tahun). Kasus target = kasus awal + solar tergantikan 3,0 L/t (G0) + CAPEX −15% (G1) + fee USD 1,35/t (G2; jendela 0,67–1,84) + karbon USD 8,3/t; asumsi lain identik.", "FCI biaya modal tetap; WACC biaya modal rata-rata tertimbang; DSCR rasio cakupan layanan utang; LCOE biaya listrik terlevelisasi; PI indeks profitabilitas; MRV pemantauan, pelaporan, verifikasi.");
};
