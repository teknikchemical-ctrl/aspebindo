# R6 - Verifikasi atas Audit Juri (solar, hukum, CAPEX, perizinan)

**Tanggal:** 2026-10-16. **Kurs:** Rp 17.948/USD (JISDOR 15 Okt 2026, dari R2). **Referensi:** PKS 45 t TBS/jam, 270.000 t TBS/tahun.

**Keterbatasan metode.** WebFetch dan curl diblokir di sandbox (DNS/proxy 403). Semua angka berasal dari kutipan hasil WebSearch, bukan dari PDF primer. Teks pasal PP 25/2021, Permen ESDM 5/2025 dan Lampiran I-II Perpres 112/2022 TIDAK sempat dibuka utuh. Tingkat keyakinan: **T** = tinggi (beberapa sumber sepakat atau teks resmi dikutip), **S** = sedang (satu sumber kredibel atau sumber sekunder), **R** = rendah (blog/agregator/OCR/turunan analis). Nilai bertanda *[turunan]* adalah hitungan saya.

---

## 1. Konsumsi solar PKS dan penghematan PLTBg

**Kesimpulan.** Angka 3,0 L/t TBS tidak punya sumber terukur. Solar pabrik terukur berkisar 0,4-1,5 L/t TBS. Solar yang benar-benar tergantikan biogas pada kasus nyata adalah 1,9 L/t (PalmCo, turunan) sampai 4,8-5,5 L/t (DSNG, turunan, mencakup beban non-pabrik). **Basis rekomendasi 2,0 L/t TBS (rentang 0,5-4,8)**; 3,0 hanya sah bila PKS tuan rumah membuktikan beban emplasmen/perumahan/bengkel lewat log solar.

| Parameter | Nilai | Rentang | Sumber (URL) | Tanggal | Yakin | Catatan |
|---|---|---|---|---|---|---|
| Solar seluruh pabrik (Jamaludin 2018) | 0,53 L/t TBS | 0,3-1,0 | https://www.sciencedirect.com/science/article/pii/S2666789425000698 | 2025 | S | Dikutip studi simulasi (dari R2) |
| Solar pemulihan minyak (LCA PFAD) | 0,37 L/t TBS | - | https://www.sciencedirect.com/science/article/pii/S1364032120304354 | 2020 | S | Sumber primer tak disebut |
| Solar PKS Malaysia 2015 | 1,51 L/t TBS *[turunan]* | - | https://www.matec-conferences.org/articles/matecconf/pdf/2018/18/matecconf_ijcaet-isampe2018_01028.pdf | 2018 | S | 154.452 L / 102.537 t TBS |
| LCI MPOB 12 PKS (Vijaya 2008) | 0-4,51 L/t CPO (~0-0,95 L/t TBS *[turunan, OER 21%]*) | 0-4,51 | https://palmoilis.mpob.gov.my/publications/joprv20june-vijaya.pdf | 2008 | S | Satuan per t CPO; variasi antarpabrik besar |
| PKS Tri Bakti Sarimas (Riau) sebelum PLN | 150 L/hari (ada buah), 400 L/hari (tanpa buah) | - | https://www.idxchannel.com/economics/pakai-jaringan-listrik-pln-perusahaan-sawit-ini-bisa-berhemat-hingga-rp7-juta/all | 2022-04 | S | Kapasitas olah tak dilaporkan, tak bisa dijadikan L/t. Harga solar saat itu Rp 17.500/L |
| Genset diesel SFC | 0,42 L/kWh | 0,28-0,42 | https://palmoilis.mpob.gov.my/publications/POEB/poeb115-ravi.pdf | - | S | dari R2 |
| PalmCo: solar dihemat 2023-2025 | >2,6 juta L; ~Rp 39,5 miliar | - | https://en.infosawit.com/news/17709/palmco-converts-palm-oil-waste-into-clean-energy--saving-millions-of-liters-of-diesel ; https://industri.kontan.co.id/news/manfaatkan-limbah-sawit-palmco-hemat-biaya-energi-hingga-rp-395-miliar ; https://economy.okezone.com/read/2026/04/15/320/3212712/2-pltbg-jadi-andalan-tekan-biaya-energi-di-tengah-gejolak-global | 2026-04-15 | **T** (4+ media) | **Terverifikasi** angka 2,6 juta L, 3 tahun, Rp 39,5 miliar. Data perusahaan, tanpa audit independen. Implisit Rp ~15.200/L |
| PalmCo: POME diolah | 293.000 m3 (tahun lalu, dua PLTBg) | - | Okezone (di atas) | 2026-04-15 | S | Setara ~451.000 t TBS/tahun pada 0,65 m3/t |
| PalmCo: solar tergantikan per t TBS | 1,9 L/t *[turunan]* | 1,7-2,1 | turunan dari dua baris di atas | 2026-10-16 | R | 0,867 juta L/th / 451 ribu t. Asumsi 0,6-0,7 m3 POME/t |
| Kapasitas PLTBg | Tandun 1,2 MW; Terantam 0,7 MW (covered lagoon) | - | https://industri.kontan.co.id/news/ptpn-v-resmikan-plt-biogas-dengan-kapasitas-700kw | 2016-17 | S | Daya terverifikasi. Listrik Terantam dipakai juga pabrik kernel Tandun. Evaluasi BRIN: Terantam tidak optimal (lumpur menumpuk) |
| Kapasitas olah PKS Tandun / Terantam | Tandun 45 t/jam (jurnal Unilak 2016-17) | - | https://journal.unilak.ac.id/index.php/agr/article/download/5716/4535/44749 | 2017 | R | **Tidak terverifikasi** sebagai data PalmCo terbaru. Terantam: tidak ditemukan. Kontan menyebut '575 t TBS/jam' tanpa konteks jelas (jangan dipakai) |
| DSNG Muara Wahau: solar dihemat 2023 | 1,99 juta L; Rp 30,94 miliar (Rp 15.548/L) | - | https://www.idnfinancials.com/id/news/51470/tempo-dan-idn-financials-nobatkan-andrianto-oetomo-ceo-terbaik | 2024 | S | Pabrik 1 melayani 1 PKS 60 t TBS/jam, 'hingga 2 juta L/tahun' (detik/Bisnis 2020): https://finance.detik.com/energi/d-5507709/pakai-limbah-sawit-pabrik-ini-hemat-jutaan-liter-solar-tiap-tahun . Kapasitas CNG total: 820 atau 850 m3/jam, sumber berbeda |
| DSNG: solar tergantikan per t TBS | 4,8-5,5 L/t *[turunan]* | - | turunan: 1,99 juta L / ~360.000 t TBS (60 t/jam x 20 jam x 300 hari, asumsi) | 2026-10-16 | R | Batas atas, lokasi terpencil (Kaltim), listrik non-pabrik ikut tergantikan |
| **Basis rekomendasi** | **2,0 L/t TBS** | **0,5-4,8** | gabungan | 2026-10-16 | R | Ganti dengan log solar 12 bulan PKS tuan rumah |

### Harga solar industri, Oktober 2026

Tidak ada daftar harga resmi untuk solar industri (B2B). Pertamina Patra Niaga tidak mengumumkan harga B2B umum (pernyataan 2021, via Kontan, https://industri.kontan.co.id/news/pertamina-patra-niaga-solar-industri-dijual-dengan-skema-b2b), sehingga angka berikut dari agregator.

| Parameter | Nilai Rp/L | Rentang | Sumber | Tanggal | Yakin | Catatan |
|---|---|---|---|---|---|---|
| Solar Industri B50 harga dasar Wil. I-II | 18.950 | 18.950-19.200 (Wil. III 19.050; IV 19.200) | https://www.hargasolarindustri.com/ | 1-14 Okt 2026 | R | Tanpa PPN, PBBKB, ongkos angkut; loco depot |
| Referensi MyPertamina industri | 24.886 | - | https://solardistro.com/artikel/harga-solar-industri-periode-15-31-september-2026/ | 1-14 Okt 2026 | R | Termasuk PPN |
| Pertamina Dex (SPBU, non-subsidi) | 25.200 (Jawa); 25.750 (Sumut, Aceh, Jambi, Sumsel dll); 26.300 (Riau, Kepri) | - | https://www.rctiplus.com/news/detail/inews/5490554/daftar-harga-bbm-pertamina-10-oktober-2026-di-spbu-seluruh-indonesia | 10 Okt 2026 | S | Berlaku sejak 2 Sep 2026, tidak naik Oktober. Termasuk pajak, harga eceran |
| Dexlite | 23.700 | - | R2 | 2026 | S | |
| Biosolar subsidi | 6.800 | - | rctiplus (di atas) | Okt 2026 | T | Bukan untuk industri/PKS |
| Riwayat B40 industri | 30.550 (15-30 Apr 2026); 25.850 (1-14 Jun 2026) | - | https://industri.kontan.co.id/news/harga-solar-industri-b40-naik-jadi-rp-30550-per-liter-ini-penjelasan-pertamina | 2026 | S | Volatilitas tinggi (periode krisis harga minyak) |
| Realisasi PKS | PalmCo ~15.200; DSNG 2023 15.548; Tri Bakti 2022 17.500 | - | sumber di atas | 2022-26 | S | Harga rata-rata historis, bukan harga Okt 2026 |
| **Basis rekomendasi** | **21.000 terkirim, tanpa PPN** | 18.950-25.850 | R2 + R6 | 2026-10-16 | R | Gunakan faktur solar PKS aktual |

---

## 2. Struktur hukum penjualan listrik

**Yang berhasil diverifikasi (dari kutipan, bukan teks utuh):**
- Perizinan usaha ketenagalistrikan dibedakan IUPTLU (kepentingan umum, dapat berwilayah usaha) dan IUPTLS (kepentingan sendiri). Definisi: Permen ESDM 12/2021 https://jdih.esdm.go.id/common/dokumen-external/Permen%20ESDM%20No.%2012%20Tahun%202021.pdf ; pelaksanaan: Permen ESDM 11/2021 https://gatrik.esdm.go.id/assets/uploads/download_index/files/a7726-permen-esdm-no.-11-tahun-2021.pdf [S]
- IUPTLS untuk total pembangkit > 500 kW (PP 25/2021, disebut Pasal 40(1), https://perpajakan.ddtc.co.id/sumber-hukum/peraturan-pusat/peraturan-pemerintah-25-tahun-2021) [R, teks pasal tidak terbuka]. Izin diberikan Menteri atau Gubernur sesuai kewenangan (slide Gatrik) [S]
- Penjualan tenaga listrik secara umum hanya oleh pemegang IUPTLU (Permen ESDM 11/2021 Pasal 36, kutipan terpotong) [R]. Pemegang IUPTLS yang hendak menjual kelebihan listrik ke pemegang IUPTLU atau masyarakat harus memenuhi: wilayah belum terjangkau IUPTLU dan persetujuan pemberi izin (Corruption Risk Assessment TI Indonesia, https://ti.or.id/wp-content/uploads/2024/12/LAPORAN-CRA-Pembangkitan-Listrik.pdf) [S]
- Pembelian excess power oleh IUPTLU terintegrasi berwilayah usaha dari IUPTLS: Permen ESDM 11/2021 Pasal 59; harga wajib persetujuan Menteri [S]
- Permen ESDM 5/2025 (ditetapkan 27 Feb, diundangkan 4 Mar 2025; https://www.peraturan.go.id/id/permen-esdm-no-5-tahun-2025): Pasal 47, PJBL standar tidak menjadi acuan excess power PLN-IUPTLS, perjanjian atas kesepakatan; Pasal 16, kelebihan di atas CE/AF dibeli maksimal 80% harga PJBL (hanya pembangkit ber-PJBL) [S]
- Perpres 112/2022 Pasal 5(1): harga beli PLN = HPT (Lampiran I) atau harga kesepakatan, dengan atau tanpa faktor lokasi F; F dalam Lampiran II [T, dikutip dari pasal.id]
- Penentuan SPV BOO jual kWh ke PKS tuan rumah: **tidak ada sumber yang secara eksplisit menjawab**. Pencarian skema sewa/BOO captive tidak menemukan teks. Ini penalaran saya.

**Analisis struktur (keyakinan R, wajib konfirmasi).**

| Struktur | Sah? | Dasar/alasan | Risiko |
|---|---|---|---|
| A. SPV memiliki genset dan menjual kWh langsung ke PKS tanpa izin | **Tidak aman** | Menjual listrik ke pihak lain = penyediaan listrik; umumnya perlu IUPTLU (Permen 11/2021 Psl 36, R) | Sanksi perizinan, ditolak LIT saat SLO |
| B. SPV pegang **IUPTLU**, jual ke PLN (PJBL Permen 5/2025 + HPT Perpres 112) dan/atau ke PKS | Sah di jalur PLN. Jual langsung ke PKS dalam wilayah usaha PLN bergantung wilayah usaha dan kerja sama dengan PLN (Pasal 45/59 Permen 11/2021: pemanfaatan jaringan bersama, operasi paralel) | S/R | Proses lama; PKS tetap pembeli PLN bila tak ada skema |
| C. **PKS pegang IUPTLS**, SPV menyewakan aset dan/atau memberi jasa O&M/pengolahan POME (SPV pegang izin jasa penunjang, IUJPTL), bayar sewa/tarif jasa, bukan per kWh | **Struktur paling aman menurut penalaran** (listrik dikonsumsi sendiri oleh pemegang IUPTLS) | Praktik sewa genset lazim, tapi dasar teks tidak ditemukan (R) | Substansi 'sewa' vs 'jual kWh' bila tarif dihitung per kWh; PKS menanggung kewajiban SLO/laporan; hak kepemilikan BOO terpisah |
| D. SPV menjual **biogas** (bukan listrik) ke PKS atau menjual jasa pengolahan POME | Tidak termasuk usaha ketenagalistrikan jika SPV tidak menghasilkan listrik | R, belum dicek ke Migas/biogas | Genset tetap dimiliki PKS |
| E. Ekspor excess power ke PLN oleh PKS (IUPTLS), SPV sebagai penyedia aset | Sah, harga kesepakatan (Permen 5/2025 Psl 47), HPT sebagai acuan | S | Harga tidak otomatis HPT |

**Rekomendasi struktur kontrak:** C (PKS pemegang IUPTLS, SPV pemilik aset dan operator berizin jasa, bayar sewa kapasitas + tarif jasa/biogas) untuk pasokan captive; ekspor ke PLN lewat E atau B tergantung siapa pemegang izin. Hindari A.

**Tarif PLTBg (Perpres 112/2022 Lampiran I).**

| Parameter | Nilai | Rentang | Sumber | Yakin | Catatan |
|---|---|---|---|---|---|
| HPT PLTBg <=1 MW, tahun 1-10 | 10,18 USc/kWh (x F) | 10,18-11,47 | Tesis Undip https://eprints2.undip.ac.id/id/eprint/16233/3/BAB%20II.pdf ; Scribd sosialisasi ESDM https://id.scribd.com/document/609079033 ; OCR annex https://stream-asset.stockbit.com/666bead2-8e72-4e2a-8586-30f783dad49b_stream.pdf | S | **Konflik 10,18 vs 11,47 belum selesai**. Header kapasitas tabel OCR rusak |
| HPT PLTBg <=1 MW, tahun 11-30 | 6,11 USc/kWh | 6,11-6,88 | idem | S | Tanpa F. Tabel Scribd menyebut tahun 11-20; periode 30 tahun dari R1/R2 |
| Tier lain (Undip) | >1-3 MW 9,81 xF (5,89); >3-5 MW 8,99 xF; >5-10 MW 8,51 xF | - | Undip | S | |
| Faktor F berlaku untuk biogas? | Ya menurut tabel Undip/Scribd/catatan Lampiran ('HPT setelah dikalikan F', hanya tahap 1); **tidak** menurut LPEM 2023 (https://lpem.org/wp-content/uploads/2023/06/Environmental_Policy_Update_V1_No1_ID.pdf) dan R1 | F 1,00-1,50; Sumatera/Kalimantan 1,10 (R2, R) | Pasal 5 dan Lampiran II | **R** | **Tidak terselesaikan**. Basis: tanpa F (10,18); F=1,10 sebagai peluang |
| Excess power PLTBg (IUPTLS) | 7,44 USc/kWh, tahun 11+: 4,46 | 4,46-7,44 | Stockbit OCR; Scribd | **R** | Angka 7,44/4,46 juga muncul sebagai ujung seri kapasitas Scribd (10,18; 9,81; 8,99; 8,51; 7,44; rasio 0,60 sama dengan 6,11/10,18), jadi mungkin bukan baris 'excess power'. Permen 5/2025 Psl 47: harga atas kesepakatan |

**Harus dikonfirmasi ke Ditjen Gatrik/ESDM (Dit. Pembinaan Pengusahaan Ketenagalistrikan):**
1. Apakah SPV pemilik genset yang menyewakan aset ke pemegang IUPTLS memerlukan IUPTLU, IUJPTL, atau cukup perjanjian sewa/O&M; apakah tarif berbasis kWh dalam sewa dipandang penjualan listrik.
2. Teks Pasal 40-41 PP 25/2021 dan Pasal 36 Permen 11/2021 tentang jual listrik oleh IUPTLS ke pihak lain di luar excess power; status PP 28/2025 (perizinan berbasis risiko) terhadap rezim ini.
3. Nilai pasti Lampiran I baris PLTBg (<=1 MW dan excess power) dan apakah F berlaku (Lampiran II).
4. Apakah harga 'kesepakatan' excess power IUPTLS-PLN dibatasi HPT dan perlu persetujuan Menteri.

---

## 3. Benchmark CAPEX

**Kesimpulan.** Tidak ditemukan benchmark USD/kWe 2022-2026 yang memisahkan lagun tertutup dan tangki CSTR, dan tidak ditemukan harga terpasang tangki GFS dari CST/Center Enamel/ESP/Lipp maupun harga genset biogas China. Yang ada hanya proyek Indonesia 2018-2021 (Rp) dan studi kelayakan.

| Parameter | Nilai | Rentang | Sumber | Tanggal | Yakin | Catatan |
|---|---|---|---|---|---|---|
| PLTBg Sawit Graha Manunggal 1 MW | Rp 36,9 miliar/MW | - | https://www.esdm.go.id/id/berita-unit/direktorat-jenderal-ketenagalistrikan/hemat-penggunaan-bbm-untuk-pembangkit-pln-teken-perjanjian-jual-beli-tenaga-listrik-pjbl-dengan-plta-sita-dan-pltbg-sawit-graha-manunggal | ~2018 | S | USD 2.056/kW (kurs kini) atau ~2.540 (kurs 2018). Teknologi tak disebut |
| PLTBg Pasir Mandoge 2x1 MW | Rp 21 miliar/MW | - | https://konstruksimedia.com/investasi-biogas-hingga-rp42-miliar-pln-perkuat-listrik-di-sumut-dengan-pltbg/ | ~2021 | S | USD 1.170/kW; cakupan biaya tak jelas |
| CSTR 700 kW Sei Pagar (studi kelayakan) | Rp 37,6 miliar/MW | - | https://ejournal.brin.go.id/MIPI/article/view/1630 | n.d. | S | USD 2.094/kW; bukan proyek terbangun |
| Studi KSI 1,2 MW | Rp 35,9 miliar/MW | - | https://digilib.itp.ac.id/index.php?id=159&keywords=&p=show_detail | n.d. | R | USD 2.000/kW |
| Suka Damai 2,4 MW | Rp 45,5 miliar/MW | - | R2 (ResearchGate) | ~2019 | S | |
| Review 2025, Indonesia 1,2 MW | USD 3.200/kW; kisaran USD 2,24-2,80 juta/MW | - | https://www.sciencedirect.com/org/science/article/pii/S019985952500137X | 2025 | R | Tahun dan cakupan tak jelas |
| MPOB 2013: tangki tertutup vs lagun tertutup | RM 10-12 juta vs ~RM 4 juta | - | https://palmoilis.mpob.gov.my/publications/OPIEJ/opiejv13n1-roslan.pdf | 2013 | R | Tangki sekitar 2,5-3x lagun; cakupan tak jelas |
| Blog 2026 lagun tertutup | USD 1.500-3.000 per m3/hari POME | - | https://hydropurewater.com/blog/6651-palm-oil-mill-wastewater-treatment-system-2026-engineering-guide.html | 2026 | R | Tanpa sumber, jangan dipakai |
| Harga tangki GFS terpasang (CST, Center Enamel, ESP, Lipp) | **tidak ditemukan** | placeholder analis USD 100-250/m3 | model biaya forum ~EUR 100/m3 baja (https://www.researchgate.net/post/how_to_assess_anaerobic_digester_investment_cost) ; pabrik Jerman 2.500 m3 EUR 750 ribu total 2002 (https://www.kriegfischer.de/fileadmin/public/docs/datenblaetter/101Boeckermanenglisch040222.pdf) | - | R | Alasan: vendor tidak mempublikasikan harga; wajib kuotasi. Angka 150 = asumsi |
| Genset biogas Eropa (dealer) | Jenbacher J320 1,06 MW baru (gas alam): USD 291/kW; J420 1,4 MW: 268/kW; J320 bekas 2008: ~150/kW; CAT G3516 (3 unit): ~362/kW | 150-362 | https://uspeglobal.com/inventory/jenbacher-j320-gs-c105-natural-gas-generator/ ; https://uspeglobal.com/inventory/jenbacher-j420-gs-b25-biogas-generator-set/ ; https://uspeglobal.com/inventory/used-caterpillar-g3516-biogas-generator-set/ | 2026 | R | Harga tawaran dealer, hanya mesin; tanpa gas train/H2S/instalasi |
| Genset biogas China 500-1000 kW | **tidak ditemukan** | - | listing Made-in-China tidak dapat dipakai (USD 25-150 ribu per 1.000 kW, USD 9) | - | R | Perlu kuotasi Weichai/Jichai/Guangzhou Cummins |
| **Basis CAPEX tangki/CSTR (rekomendasi)** | **USD 2.600/kWe** | 2.100-3.500 | sintesis; cocok dengan R2 (2,1-3,5 juta USD/MW) | 2026-10-16 | R | AnMBR termofilik belum terbukti, tambah premi |
| Basis lagun tertutup | USD 1.700/kWe | 1.170-2.100 | Pasir Mandoge dan Sawit Graha dikonversi | 2026-10-16 | R | Dua titik saja |
| Basis GFS | USD 150/m3 (placeholder) | 100-250 | di atas | 2026-10-16 | R | Bukan temuan |

---

## 4. Perizinan PLTBg POME 1 MW

| Izin/persetujuan | Dasar | Penerbit | Lama proses | Status verifikasi |
|---|---|---|---|---|
| PBG dan SLF | PP 16/2021; SIMBG | Pemda kab./kota (DPMPTSP/PUPR), TPA untuk non-hunian | Tidak ditemukan untuk bangunan industri/pembangkit (SOP Demak: menit per tahap, bukan total) | S untuk dasar; waktu **belum terverifikasi**. Retribusi mengikuti perda; sumber: https://dpmptspp.belitung.go.id/wp-content/uploads/2022/04/MEKANISMES-Penerbitan-PBG-SLF-dan-SBKBG.pdf |
| IUPTLS (izin operasi pembangkit sendiri, >500 kW) via OSS | PP 25/2021; Permen ESDM 11/2021 (menggantikan Izin Operasi Permen 35/2013) | Menteri ESDM (Ditjen Gatrik) atau Gubernur, via OSS | Tidak ditemukan | S untuk rezim; ambang 500 kW R; waktu **belum terverifikasi** |
| IUPTLU (bila SPV jual ke PLN/pihak lain) | idem | Menteri atau Gubernur, via OSS | Tidak ditemukan | R |
| PJBL dengan PLN dan interkoneksi (bila ekspor) | Permen ESDM 5/2025; Perpres 112/2022 | PLN (harga: Menteri/Gubernur untuk persetujuan harga tertentu) | Tidak ditemukan; WUR: negosiasi sering panjang (R2) | S |
| SLO instalasi pembangkit | UU 30/2009 jo. UU 6/2023 Pasal 44; Permen ESDM 12/2021 | Lembaga Inspeksi Teknik terakreditasi | SLO non-TR terbit paling lambat 4 hari kerja setelah pemeriksaan/pengujian selesai; masa berlaku pembangkit 5 tahun. Sumber: https://gatrik.esdm.go.id/assets/uploads/download_index/files/81afd-faq-slo-07082024.pdf | **S** (FAQ 2024) |
| Persetujuan lingkungan (AMDAL/UKL-UPL/SPPL) | PP 22/2021 | DLH kab./prov. atau KLH; PKS tuan rumah sudah punya dokumen, kemungkinan perubahan/adendum | Tidak ditemukan | Ambang PLTBg 1 MW **belum terverifikasi** |
| Persetujuan Teknis air limbah + SLO air limbah (termasuk aplikasi lahan) | Permen LHK 5/2021 (Pasal 3: wajib bagi usaha ber-AMDAL/UKL-UPL yang membuang/memanfaatkan air limbah) | KLH atau DLH | Tidak ditemukan; pedoman lama KepmenLH 28/2003: persetujuan bupati/walikota 30 hari kerja (mungkin sudah tidak berlaku) | S untuk dasar. https://pasal.id/peraturan/permen/permen-lhk-no-5-tahun-2021 |
| K3 bejana tekan dan tangki timbun | Permenaker 37/2016 (sebagian pasal pengawasan dicabut Permenaker 11/2026, per BPK) | Kemnaker/Disnaker provinsi; pemeriksaan oleh PJK3/ahli K3 | Tidak ditemukan | S untuk dasar. https://peraturan.bpk.go.id/Details/146211/permenaker-no-37-tahun-2016 |
| K3 ketel uap/pesawat uap, instalasi listrik, penyalur petir | Aturan uap 1930, Permenaker 02/1982 dan 01/1988 dikutip bahan pelatihan; lainnya tidak terverifikasi | Disnaker provinsi | Tidak ditemukan | **Belum terverifikasi**; Permenaker instalasi listrik dan penyalur petir tidak ditemukan dalam pencarian |
| ISPO | Perpres 44/2020 diperbarui Perpres 16/2025 (cakupan diperluas ke industri olahan dan bioenergi, Kontan Jun 2025: https://industri.kontan.co.id/news/perkuat-pengelolaan-kelapa-sawit-pemerintah-dorong-sertifikasi-ispo-hulu-hilir) | Lembaga sertifikasi terakreditasi KAN, Kementan | Tidak ditemukan | R. Tidak ada syarat khusus penangkapan metana ditemukan. PLTBg bukan objek ISPO sendiri |
| Registrasi SRN-PPI dan SPE-GRK (SPEI) | Permen LHK 21/2022; skema SPEI 2023 (https://srn.menlhk.go.id/static/srn/PDF/skema_SPEI_2023.pdf); Hukumonline menyebut Permen LHK 12/2024 mengatur registrasi (perlu cek mana yang berlaku) | Dirjen PPI KLH; verifikator independen | Tidak ditemukan. 1 SPE-GRK = 1 tCO2e; tidak boleh ganda dengan skema lain | S untuk alur; waktu **belum terverifikasi** |
| Verra VCS/ AMS-III.H | R1 | Verra | Tidak dicari ulang di R6 | Lihat R1 |

---

## 5. Hal yang belum terverifikasi (daftar ringkas)
1. Kapasitas olah PKS Tandun (45 t/jam hanya jurnal 2016-17) dan Terantam.
2. Solar PKS terukur 3,0 L/t: tidak ada; pembenaran hanya lewat beban non-pabrik.
3. Harga resmi solar industri Okt 2026: hanya agregator.
4. Teks utuh PP 25/2021, Permen 11/2021, Permen 5/2025, Perpres 112 Lampiran I-II.
5. Berlaku/tidaknya F pada PLTBg; 10,18 vs 11,47; baris excess power 7,44.
6. Struktur sewa/BOO captive tanpa IUPTLU: tidak ada teks eksplisit.
7. CAPEX 2022-2026 per teknologi, harga GFS terpasang, harga genset China.
8. Waktu proses PBG/SLF, IUPTLS, persetujuan lingkungan, persetujuan teknis, SPEI.
9. Peraturan K3 ketel/listrik/petir yang berlaku.
