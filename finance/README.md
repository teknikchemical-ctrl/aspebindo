# Phase 4 - Model keuangan & analisis pasar

| File | Isi |
|---|---|
| `outputs/BG_Model_Keuangan.xlsx` | Model keuangan dengan **rumus hidup**: Asumsi (sel kuning) -> CAPEX -> OPEX -> Arus Kas 2027-2047 -> Indikator (NPV, IRR, payback, PI, DSCR, LCOE, BEP). Ditambah Sensitivitas, Monte Carlo, Skala Set, Armada, Pasar (TAM-SAM-SOM), PESTLE, Porter, Sumber, Gambar |
| `outputs/BG_Analisis_Ekonomi.pdf` | Laporan 9 halaman (gaya makalah): pasar, Porter/PESTLE, CAPEX/OPEX, arus kas, NPV/IRR/PBP, BEP, ketidakpastian, armada, syarat FID |
| `outputs/figs/g01..g10*.png` | Gambar untuk deck/makalah |
| `outputs/summary.json` | Indikator utama |
| `research/market_data.md` | Data pasar & harga dengan sumber + URL + tahun |

Jalankan: `cd finance && python3 run_all.py` (~25 s). Semua angka dibaca dari `process/outputs/results.json` dan massa bejana model 3D.
Excel diverifikasi: dihitung ulang dengan LibreOffice dan cocok dengan Python sampai digit terakhir, termasuk setelah input diubah.

Hasil dasar (1 set 45 t TBS/jam, BOO): FCI USD 5,39 juta; NPV USD 0,61 juta @ WACC 9,74%; IRR 11,7%; IRR ekuitas 16,5%; payback 6,5 th sejak COD;
P(NPV>0) Monte Carlo ~40%. Perusahaan (40 set s/d 2034, kurva belajar 90%): NPV USD 28,7 juta, IRR 15,2%.
Item [ASUMSI]/[UNVERIFIED] (jasa pengolahan POME, harga membran/genset, faktor lokasi F Sumatera, status Perpres 112/2022) harus dikonfirmasi sebelum FID.
