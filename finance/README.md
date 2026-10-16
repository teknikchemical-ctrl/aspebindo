# Phase 4 - Model keuangan & analisis pasar (v2, setelah audit)

| File | Isi |
|---|---|
| `outputs/BG_Model_Keuangan.xlsx` | Model dengan **rumus hidup**: Asumsi -> CAPEX -> OPEX -> Arus Kas 2027-2047 -> Indikator; + Sensitivitas, Monte Carlo, Skala Set, Armada, Lokasi (dari model 3D), Pasar, PESTLE, Porter, Sumber, Gambar |
| `outputs/BG_Analisis_Ekonomi.pdf` | Laporan 10 halaman: integrasi lokasi, pasar, Porter/PESTLE, CAPEX/OPEX, arus kas, NPV/IRR/PBP, BEP, ketidakpastian, armada, nilai bagi PKS, syarat FID |
| `outputs/figs/g01..g10*.png` | Gambar untuk deck/makalah |
| `outputs/summary.json` | Indikator utama |
| `research/market_data.md`, `research/market_data_2.md` | Data pasar, tarif, karbon, biaya (sumber + URL + tahun) |

Jalankan: `cd finance && python3 run_all.py` (~10 s). Input teknis: `process/outputs/results.json`; luas plot: `cad/out/ga.json`; panjang pipa/kabel lokasi: `cad/out/site.json`.
Excel diverifikasi: dihitung ulang LibreOffice = Python sampai digit terakhir, juga setelah 3-4 input diubah (`fin_excel.verify(mods=...)`).

## Model bisnis
BOO jasa pengolahan + energi. PKS membayar **jasa pengolahan POME & kepatuhan USD 2,0/t TBS** (impas USD 1,51/t TBS); listrik 0,37 GWh/th ke PKS di luar jam olah (USD 0,18/kWh, menggantikan diesel) dan 5,69 GWh/th ke PLN (Perpres 112/2022: 10,18 USc x F 1,10 th 1-10, 6,11 sesudahnya); kredit karbon USD 5/t selama 10 th.

## Hasil dasar (1 set 45 t TBS/jam)
FCI USD 5,42 juta (2026); NPV USD 1,02 juta @ WACC 9,74%; IRR 12,5%; IRR ekuitas 14,8%; payback 6,0 th; DSCR min 1,55; P(NPV>0) 64%.
Tanpa jasa POME NPV -3,47 juta -> produk adalah jasa pengolahan limbah, bukan pembangkit murni. Armada 40 set: NPV USD 35,6 juta, IRR 13,9%.

## Perbaikan v2 (dari audit independen)
1. Basis volume tunggal 300 hari x faktor beban 0,92 (energi turun dari 7,32 ke 6,17 GWh/th).
2. Tarif Perpres 112 dikoreksi (10,18/6,11 USc) + kapasitas kontrak 1 MW (profil musiman); skenario tier >1 MW.
3. Klaim mutu efluen dikoreksi (COD ~4.800 mg/L -> kolam polishing tetap dipakai).
4. Karbon: emisi efluen dikurangkan, periode kredit 10 th, lag penerbitan 1 th, biaya validasi; harga USD 5/t.
5. IRR kokoh (akar polinom), kasus gagal tidak dibuang di Monte Carlo.
6. Armada: CAPEX dieskalasi, kurva belajar hanya 60% FCI, horizon penuh tanpa pemotongan, overhead tanpa perisai pajak.
7. IDC, PPN CAPEX (restitusi), biaya upfront, DSRA, masa tenggang pokok, overhaul & ganti membran pada tahun nyata, MRA untuk DSCR.
8. Pajak PP 78/2019: allowance atas aset berwujud, penyusutan 8 th, rugi fiskal maks 10 th; modal kerja piutang/utang.
9. Teks laporan & tabel membaca variabel model (tidak ada angka ketik manual).
10. Pendapatan panas & pupuk dihapus dari kasus dasar (tidak terbukti); diganti listrik ke PKS (pengganti diesel).
