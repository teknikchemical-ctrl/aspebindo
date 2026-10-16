module.exports = (pres, H, L) => {
  const { C, D, fmt, FONT_H, NF } = L; const p = D.proses, k = D.keu;
  const s = H.slide(4, "Solusi: validitas teknis", "Validitas teknis: neraca massa menutup (galat 0,0002%), swasembada energi 91%, tetapi TRL baru 4; lima uji terjadwal diperlukan sebelum keputusan investasi");
  H.sec(s, "Dasar desain (45 | 60 t TBS/jam) dan status data", 0.4, 1.18, 4.1);
  const T = p.tiers;
  H.table(s, [["Parameter", "45", "60", "Status"],
    ["POME (m³/hari)", fmt(p.pome_m3d, 0), fmt(p.pome_m3d * 60 / 45, 0), "L: 0,65 m³/t TBS"], ["COD umpan (g/L)", fmt(p.cod_in, 1), fmt(p.cod_in, 1), "L: 50–60"], ["Suhu · HRT · SRT", "55 °C · 5,0 · 12 hari", "sama", "L; S"],
    ["Tangki GFS 980 m³", T["45"].N, T["60"].N, "R"], ["OLR (kg COD/m³·hari)", fmt(p.olr, 1), fmt(p.olr, 1), "S (rekomendasi ≤ 8)"], ["Penyisihan COD", fmt(p.cod_rem * 100, 0) + "%", fmt(p.cod_rem * 100, 0) + "%", "S terkalibrasi"],
    ["Biogas (Nm³/hari)", fmt(T["45"].bg, 0), fmt(T["60"].bg, 0), "S"], ["CH₄ · H₂S ke genset", fmt(p.ch4_frac * 100, 0) + "% · " + fmt(p.h2s_fuel, 0) + " ppm", "sama", "S"],
    ["Daya kotor/neto (kW)", fmt(T["45"].Pg, 0) + "/" + fmt(T["45"].Pn, 0), fmt(T["60"].Pg, 0) + "/" + fmt(T["60"].Pn, 0), "S; η 39,3% (L)"], ["Energi neto (GWh/tahun)", fmt(T["45"].GWh, 2), fmt(T["60"].GWh, 2), "S 365 hari"], ["Ketersediaan · beban PKS", "93% · 75%", "sama", "A"]],
    0.4, 1.43, 4.1, [1.5, 0.95, 0.75, 0.9], { fs: 6.6, rh: 0.205, align: ["left", "center", "center", "left"] });
  H.t(s, "Status: L literatur; S simulasi (ADM1-lite terkalibrasi, 365 hari); R rancangan; A asumsi. Tidak ada data terukur di lokasi (belum).", 0.4, 3.95, 4.1, 0.25, { fontSize: 6, italic: true, color: C.slate });
  H.sec(s, "Neraca massa nameplate 45 t/jam (kg/jam)", 0.4, 4.25, 4.1);
  const ma = D.massa; const rows = [["Masuk", "kg/jam", "Keluar", "kg/jam"]];
  for (let i = 0; i < 5; i++) { const a = ma.inn[i], b = ma.out[i]; rows.push([a[0].replace(/ \(S\d+.*\)/, ""), fmt(a[1], 0), b[0].replace(/ \(S\d+\)/, ""), fmt(b[1], 0)]); }
  rows.push(["Jumlah masuk", fmt(ma.sum_in, 0), "Jumlah keluar", fmt(ma.sum_out, 0)]);
  H.table(s, rows, 0.4, 4.5, 4.1, [1.3, 0.65, 1.5, 0.65], { fs: 6.5, rh: 0.2, align: ["left", "right", "left", "right"] });
  H.t(s, "Penutupan: |masuk − keluar| = " + fmt(Math.abs(ma.sum_in - ma.sum_out), 2) + " kg/jam (" + fmt(Math.abs(ma.sum_in - ma.sum_out) / ma.sum_in * 100, 4) + "%); neraca unsur C, H, O, N, S < 10⁻⁴. Gas buang dan gas ke flare dihitung; kehilangan CH₄ lepas 1% + slip 0,5%.", 0.4, 6.0, 4.1, 0.4, { fontSize: 6.3 });
  // energi
  H.sec(s, "Neraca energi (kW, modul 45 t/jam)", 4.7, 1.18, 3.8);
  const pa = p.parasitic; const lab = { chp_aux_misc: "Bantu genset", jet_mixing: "Pencampur jet", cooling_tower: "Menara pendingin", sludge_press: "Screw press", gas_blower: "Blower gas", pretreatment: "Praolah", gas_chiller: "Pendingin gas", feed_pumps: "Pompa umpan", degasser: "Degasser" };
  const ks = Object.keys(lab);
  s.addChart(pres.charts.BAR, [{ name: "kW", labels: ks.map((x) => lab[x]), values: ks.map((x) => pa[x]) }], { x: 4.65, y: 1.4, w: 3.9, h: 2.0, barDir: "bar", chartColors: [C.royal], showValue: true, dataLabelFormatCode: L.NF1, dataLabelFontSize: 6.5, catAxisLabelFontSize: 6.5, catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" }, showLegend: false, catAxisLabelFontFace: "Calibri", dataLabelFontFace: "Calibri" });
  H.t(s, [{ text: "Daya kotor " + fmt(p.P_gross45, 0) + " kW − pemakaian sendiri " + fmt(p.P_par, 0) + " kW (" + fmt(p.P_par / p.P_gross45 * 100, 0) + "%) = neto " + fmt(p.P_net45, 0) + " kW. ", options: { bold: true } }, { text: "Panas: selubung " + fmt(p.Q_jacket, 0) + " kW + gas buang " + fmt(p.Q_exh, 0) + " kW; pemanasan reaktor hanya " + fmt(p.Q_dig, 0) + " kW, sisa untuk PKS (nilai tidak dihitung)." }], 4.7, 3.45, 3.8, 0.55, { fontSize: 6.8 });
  H.sec(s, "Ketidakpastian: korelasi peringkat terhadap daya neto", 4.7, 4.1, 3.8);
  const sp = p.mc_sens.P_net || {}; const top = Object.entries(sp).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 6);
  const nm = { util: "Beban PKS", cod_pome: "COD POME", pome_yield: "Volume POME", kLa: "kLa", km_pro: "km propionat", KI_h2s_ac: "Hambat H₂S", cat_pome: "Kation POME", km_fa: "km asam lemak" };
  s.addChart(pres.charts.BAR, [{ name: "ρ", labels: top.map((x) => nm[x[0]] || x[0]), values: top.map((x) => x[1]) }], { x: 4.65, y: 4.32, w: 3.9, h: 1.65, barDir: "bar", chartColors: [C.mid], invertedColors: [C.red], showValue: true, dataLabelFormatCode: L.NF2, dataLabelFontSize: 6.5, catAxisLabelFontSize: 6.5, catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" }, showLegend: false, catAxisLabelPos: "low", catAxisLabelFontFace: "Calibri", dataLabelFontFace: "Calibri" });
  H.t(s, "Monte Carlo proses (400 sampel): daya neto P5–P95 = " + fmt(p.mc.P_net.P5, 0) + "–" + fmt(p.mc.P_net.P95, 0) + " kW (hari rata-rata, beban 0,55–0,93). Ketersediaan 88–97% dan ukuran tangki diuji pada slide 7.", 4.7, 6.0, 3.8, 0.4, { fontSize: 6.3 });
  // TRL + validasi + HAZID
  H.sec(s, "Tingkat kesiapan teknologi (TRL)", 8.7, 1.18, 4.25);
  for (let i = 1; i <= 9; i++) H.box(s, String(i), 8.7 + (i - 1) * 0.47, 1.45, 0.43, 0.28, { fs: 8, bold: true, color: i <= 4 ? C.white : C.slate, fill: i <= 4 ? (i === 4 ? C.greenD : C.royal) : C.sky2, line: C.line, radius: 0.03, margin: 0 });
  H.t(s, "Sistem terintegrasi: TRL 4 (komponen dan kinetika tervalidasi pustaka; genset, tangki GFS, lamella sudah TRL 9). TRL 6 setelah pilot 10–20 m³ di PKS (6 bulan); TRL 7–8 setelah demonstrasi 12 bulan.", 8.7, 1.77, 4.25, 0.45, { fontSize: 6.6 });
  H.sec(s, "Matriks validasi klaim kritis", 8.7, 2.27, 4.25);
  const st = (t) => ({ text: t, options: { bold: true, align: "center", color: C.white, fill: { color: t === "Belum" ? C.red : t === "Sebagian" ? C.amber : C.greenD } } });
  H.table(s, [["Klaim", "Uji dan kriteria penerimaan", "Status"],
    ["COD tersisih ≥ 65% pada HRT 5 hari", "semikontinu 55 °C 90 hari; VFA < 500 mg/L", st("Sebagian")], ["Settler menahan ≥ 85% padatan", "uji kolom dan pilot; laju 0,6 m/jam", st("Belum")], ["H₂S ke genset ≤ 50 ppm", "pilot bio-scrubber 14 hari", st("Sebagian")],
    ["Ketersediaan genset ≥ 90%", "kontrak O&M dan data jam jalan", st("Belum")], ["Efluen BOD < 5.000 mg/L", "uji laboratorium efluen pilot", st("Sebagian")], ["Tata letak aman (flare ≥ 15 m)", "pemeriksaan jarak model 3D: lolos", st("Sebagian")]],
    8.7, 2.52, 4.25, [1.55, 2.05, 0.65], { fs: 6.2, rh: 0.25 });
  H.sec(s, "HAZID awal (L × S; belum HAZOP)", 8.7, 4.4, 4.25);
  const rk = (t) => ({ text: t, options: { align: "center", bold: true } });
  H.table(s, [["Bahaya", "L·S", "Mitigasi", "Sisa"], ["Biogas CH₄ 58% bocor, ledakan", "3·5", "zona ATEX, detektor, flare tertutup", rk("1·5")], ["H₂S 2.868 ppm mentah", "3·5", "bio-scrubber, detektor 10 ppm, SCBA", rk("2·4")], ["Tekanan lebih/vakum tangki", "2·4", "katup tekan-vakum, penampung gas", rk("1·4")],
    ["POME 85 °C (luka bakar)", "3·3", "isolasi, pelindung", rk("2·2")], ["Ruang terbatas tangki", "2·5", "izin kerja, SOP, SCBA", rk("1·5")], ["Luapan efluen", "3·3", "bund, sensor level", rk("2·3")]],
    8.7, 4.65, 4.25, [1.5, 0.4, 1.9, 0.45], { fs: 6.1, rh: 0.23 });
  H.t(s, "FMEA dan analisis pohon kegagalan dijadwalkan pada FEED (gerbang G2).", 8.7, 6.3, 4.25, 0.15, { fontSize: 6, italic: true, color: C.slate });
  H.src(s, "neraca proses Rev 2 (results.json), research/R4 (Choorit 2007; evidensi teknis), R6; HAZID awal tim (belum difasilitasi).", "OLR laju beban organik; VFA asam lemak volatil; ATEX zona atmosfer eksplosif; SCBA alat bantu napas; FEED desain rekayasa awal; L peluang 1–5; S keparahan 1–5.");
  s.addNotes("Validitas teknis. Klaim terkuat: neraca massa dan unsur menutup. Klaim terlemah: OLR 9,9 kg COD/m³·hari melebihi rekomendasi 8 dan belum ada operasi skala penuh termofilik POME di atas OLR 10; TRL 4.");
};
