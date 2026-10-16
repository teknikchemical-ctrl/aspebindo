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
  const rows = [["Indikator", "Nilai", "Acuan"], ["NPV (USD juta)", fmt(t.NPV / 1e6, 2), "WACC " + fmt(t.WACC * 100, 1) + "%"], ["IRR proyek", fmt(t.IRR * 100, 1) + "%", "+" + fmt((t.IRR - t.WACC) * 100, 1) + " poin dari WACC"], ["IRR ekuitas", fmt(t.IRR_eq * 100, 1) + "%", "biaya ekuitas 15%"], ["Payback (tahun)", fmt(t.PBP, 1), "umur proyek 20 tahun"], ["Payback terdiskonto", fmt(t.DPBP, 1) + " th", "pada WACC"], ["DSCR minimum", fmt(t.DSCR, 2), "ambang bank 1,30"], ["Indeks profitabilitas", fmt(t.PI, 2), "> 1,0 layak"], ["LCOE bersih (USD/kWh)", fmt(t.LCOE_net, 3), "setelah fee dan karbon"], ["Impas beban PKS", fmt(t.be.util * 100, 0) + "%", "asumsi dasar 75%"]];
  H.table(s, rows.map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, { text: r[1], options: { align: "center", bold: true, fill: { color: C.greenL } } }, { text: r[2], options: { color: C.slate } }]), 9.95, 2.26, [1.2, 0.62, 1.13], { fs: 7.6, rh: 0.2, hrh: 0.22, margin: [1, 3, 1, 3] });
  // baris B
  H.hdr(s, "(d) Titik impas terhadap beban PKS", 0.45, 4.33, 4.0, { h: 0.22, fs: 9 });
  img("f_bep.png", 0.45, 4.57, 4.0, 1.88, "grafik-bep");
  H.hdr(s, "(e) Kurva payback: arus kas kumulatif", 4.55, 4.33, 4.6, { fill: C.teal, h: 0.22, fs: 9 });
  img("f_payback.png", 4.55, 4.57, 4.6, 1.88, "grafik-payback");
  H.hdr(s, "(f) Pendapatan per aliran dan EBITDA", 9.25, 4.33, 3.65, { h: 0.22, fs: 9 });
  img("f_pendapatan.png", 9.25, 4.57, 3.65, 1.88, "grafik-pendapatan");
  H.concl(s, "Selisih IRR terhadap WACC +" + fmt((t.IRR - t.WACC) * 100, 1) + " poin dan DSCR " + fmt(t.DSCR, 2) + " (ambang 1,30); NPV tetap positif sampai beban PKS turun ke " + fmt(t.be.util * 100, 0) + "% atau CAPEX naik +" + fmt((t.be.capex / t.capex_mult - 1) * 100, 0) + "%.", "Kesimpulan");
  H.src(s, "BG_Model_Keuangan.xlsx; finance/fin_core.py v4 (60 t TBS/jam + PM-12, USD nominal, 20 tahun). Kasus target = kasus awal + solar tergantikan 3,0 L/t (G0) + CAPEX −15% (G1) + fee USD 1,35/t (G2; jendela 0,67–1,84) + karbon USD 8,3/t; asumsi lain identik.", "FCI biaya modal tetap; WACC biaya modal rata-rata tertimbang; DSCR rasio cakupan layanan utang; LCOE biaya listrik terlevelisasi; PI indeks profitabilitas; MRV pemantauan, pelaporan, verifikasi.");
};
