// Slide 7: Model keuangan (kasus target setelah gerbang G0-G2)
module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H } = L; const k = D.keu, t = D.tgt, cf = t.cf, i3 = 3;
  const s = H.slide(7, "Satu set menghasilkan {{USD " + fmt(cf.ebitda[i3] / 1e6, 2) + " juta laba operasi per tahun}} dari investasi USD " + fmt(t.FCI26 / 1e6, 2) + " juta: {{IRR " + fmt(t.IRR * 100, 1) + "%}} dan balik modal dalam {{" + fmt(t.PBP, 1) + " tahun}}",
    "Keuangan. Konfigurasi 60 t TBS/jam + PM-12, USD nominal, 20 tahun (2028-2047). Kasus target = kasus awal + solar tergantikan 3,0 L/t (G0) + CAPEX -15% (G1, hasil kuotasi) + fee USD 1,35/t (G2, dalam jendela 0,67-1,84) + karbon USD 8,3/t; selebihnya identik. Kasus awal (solar 2,0 L/t, fee 1,25, karbon 5,0, tanpa potongan CAPEX): NPV USD 0,13 juta, IRR 10,3%, payback 7,1 tahun. Batas aman kasus target: NPV tetap positif sampai beban PKS 54%, fee USD 0,26/t, CAPEX +47%. Semua angka dari model Excel berumus hidup dan Python (fin_core.py, deck/export_target.py).");
  const img = (f, x, y, w, h, n) => s.addImage({ path: L.ROOT + "/deck/img/" + f, x, y, w, h, objectName: n });
  const fit = (f, x, y, w, h, n) => H.imgFit(s, L.ROOT + "/deck/img/" + f, 4.05, 1.65, x, y, w, h, { objectName: n });
  const rv = cf.rev[i3], eb = cf.ebitda[i3];
  const kp = [["USD " + fmt(t.FCI26 / 1e6, 2) + " juta", "Investasi awal (CAPEX): tangki, genset, instalasi"], ["USD " + fmt(rv / 1e6, 2) + " juta", "Pendapatan per tahun (beban PKS 75%)"], ["USD " + fmt(eb / 1e6, 2) + " juta", "Laba operasi (EBITDA) per tahun; margin " + fmt(eb / rv * 100, 0) + "%"],
    ["USD " + fmt(t.NPV / 1e6, 2) + " juta", "NPV: kelebihan nilai setelah modal kembali dan imbal hasil " + fmt(t.WACC * 100, 1) + "%"], [fmt(t.IRR * 100, 1) + "%", "IRR: imbal hasil tahunan proyek; untuk ekuitas " + fmt(t.IRR_eq * 100, 1) + "%"], [fmt(t.PBP, 1) + " tahun", "Payback: uang investasi kembali, dihitung dari operasi 2028"]];
  kp.forEach(([v, l], i) => { const x = 0.45 + i * 2.085, w = 2.0, hl = i >= 3; H.rect(s, x, 1.25, w, 0.66, { fill: hl ? C.navy : C.white, line: hl ? C.navy : C.teal, radius: 0.05, lw: 1 });
    H.t(s, v, x + 0.05, 1.26, w - 0.1, 0.3, { fontFace: FONT_H, fontSize: 14.5, bold: true, color: hl ? C.white : C.navy, align: "center", valign: "middle" });
    H.t(s, l, x + 0.07, 1.56, w - 0.14, 0.34, { fontSize: 7.4, color: hl ? "DCEAF5" : C.slate, align: "center" }); });
  const cols = [0.45, 4.6, 8.75], W = 4.15;
  const R1 = 1.98, R2 = 4.2;
  const sh = (a) => fmt(a[i3] / rv * 100, 0) + "%";
  // baris 1: uang masuk, investasi, biaya
  H.hdr(s, "1. Dari mana uang masuk (USD juta per tahun)", cols[0], R1, W, { h: 0.22, fs: 8.8 }); fit("f_pendapatan.png", cols[0], R1 + 0.24, W, 1.56, "grafik-pendapatan");
  H.take(s, "Pendapatan datang dari empat sumber: ekspor PLN " + sh(cf.rev_exp) + ", jasa POME " + sh(cf.rev_fee) + ", listrik ke PKS " + sh(cf.rev_cap) + ", karbon " + sh(cf.rev_c) + ". Tidak bergantung pada satu pembeli.", cols[0], R1 + 1.82, W, 0.4);
  const cc = t.capex_cat, top3 = (cc["Tangki reaktor GFS"] + cc["Tangki umpan, efluen, ekualisasi"] + 960000 * t.capex_ratio + cc["Kontingensi 20%"]) / t.FCI26;
  H.hdr(s, "2. Ke mana investasi dipakai: USD " + fmt(t.FCI26 / 1e6, 2) + " juta", cols[1], R1, W, { fill: C.teal, h: 0.22, fs: 8.8 }); fit("f_capex.png", cols[1], R1 + 0.24, W, 1.56, "grafik-capex");
  H.take(s, "Tangki GFS, genset, dan cadangan kontingensi 20% menyerap " + fmt(top3 * 100, 0) + "% investasi. Harga tangki (USD 200/m³) dikunci lewat kuotasi di G1.", cols[1], R1 + 1.82, W, 0.4);
  H.hdr(s, "3. Ke mana biaya operasi: USD " + fmt(k.opF / 1000 + k.opV / 1000 + 12, 0) + " ribu per tahun", cols[2], R1, W, { h: 0.22, fs: 8.8 }); fit("f_opex.png", cols[2], R1 + 0.24, W, 1.56, "grafik-opex");
  H.take(s, "Biaya operasi hanya " + fmt((k.opF + k.opV + 12000) / rv * 100, 0) + "% dari pendapatan; pos terbesar adalah perawatan genset kontrak dan 10 staf operasi.", cols[2], R1 + 1.82, W, 0.4);
  // baris 2: impas, payback, ringkasan
  H.hdr(s, "4. Mulai untung pada beban PKS berapa", cols[0], R2, W, { fill: C.teal, h: 0.22, fs: 8.8 }); fit("f_bep.png", cols[0], R2 + 0.24, W, 1.56, "grafik-bep");
  H.take(s, "Pendapatan menutup biaya tunai di beban " + fmt(t.bep_util_cash * 100, 0) + "%, seluruh biaya di " + fmt(t.bep_util_acc * 100, 0) + "%, dan NPV positif di " + fmt(t.bep_util_npv * 100, 0) + "%; asumsi dasar 75%.", cols[0], R2 + 1.82, W, 0.4);
  H.hdr(s, "5. Kapan modal kembali (USD juta, kumulatif)", cols[1], R2, W, { h: 0.22, fs: 8.8 }); fit("f_payback.png", cols[1], R2 + 0.24, W, 1.56, "grafik-payback");
  H.take(s, "Kas kumulatif melewati nol setelah " + fmt(t.PBP, 1) + " tahun operasi; dengan memperhitungkan nilai waktu uang, setelah " + fmt(t.DPBP, 1) + " tahun dari 20 tahun umur proyek.", cols[1], R2 + 1.82, W, 0.4);
  H.hdr(s, "6. Ringkasan kelayakan", cols[2], R2, W, { fill: C.teal, h: 0.22, fs: 8.8 });
  const rows = [["Indikator", "Nilai", "Ukuran kelayakan"], ["NPV", "USD " + fmt(t.NPV / 1e6, 2) + " juta", "> 0 layak"], ["IRR proyek", fmt(t.IRR * 100, 1) + "%", "> WACC " + fmt(t.WACC * 100, 1) + "%"], ["IRR ekuitas", fmt(t.IRR_eq * 100, 1) + "%", "> biaya ekuitas 15%"], ["DSCR minimum", fmt(t.DSCR, 2), "≥ 1,30 (syarat bank)"], ["Indeks profitabilitas", fmt(t.PI, 2), "> 1,0 layak"], ["LCOE bersih", "USD " + fmt(t.LCOE_net, 3) + "/kWh", "setelah fee dan karbon"], ["Dana puncak", "USD " + fmt(t.peak / 1e6, 1) + " juta", "utang 58%, ekuitas 42%"]];
  H.table(s, rows.map((r, i) => i === 0 ? r : [{ text: r[0], options: { bold: true, color: C.navy } }, { text: r[1], options: { align: "center", bold: true, fill: { color: C.greenL } } }, { text: r[2], options: { color: C.slate } }]), cols[2], R2 + 0.24, [1.3, 1.05, 1.8], { fs: 7.6, rh: 0.195, hrh: 0.2, margin: [1, 3, 1, 3] });
  H.take(s, "Semua ukuran melewati ambangnya: IRR " + fmt((t.IRR - t.WACC) * 100, 1) + " poin di atas WACC dan DSCR " + fmt(t.DSCR, 2) + " terhadap syarat bank 1,30.", cols[2], R2 + 1.82, W, 0.4);
  H.concl(s, "Investasi USD " + fmt(t.FCI26 / 1e6, 2) + " juta kembali dalam " + fmt(t.PBP, 1) + " tahun dan masih memberi NPV USD " + fmt(t.NPV / 1e6, 2) + " juta; proyek tetap layak sampai beban PKS turun ke " + fmt(t.be.util * 100, 0) + "% atau CAPEX naik " + fmt((t.be.capex / t.capex_mult - 1) * 100, 0) + "%.", "Kesimpulan");
  H.src(s, "BG_Model_Keuangan.xlsx; finance/fin_core.py v4 (60 t TBS/jam + PM-12, USD nominal, 20 tahun). Kasus target = solar tergantikan 3,0 L/t (G0) + CAPEX −15% (G1) + fee USD 1,35/t (G2; jendela 0,67–1,84) + karbon USD 8,3/t; asumsi lain identik.", "CAPEX belanja modal; OPEX biaya operasi; EBITDA laba sebelum bunga, pajak, penyusutan, amortisasi; NPV nilai kini bersih; IRR tingkat imbal hasil internal; WACC biaya modal rata-rata tertimbang; DSCR rasio cakupan layanan utang; LCOE biaya listrik terlevelisasi; GFS baja berlapis kaca.");
};
