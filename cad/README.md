# Phase 3 - 3D model dan gambar teknik (set biogas portabel 45 t TBS/jam)

## Deliverables
| File | Isi |
|---|---|
| `drawings/out/BG_drawing_set_A3.pdf` | Set gambar teknik A3, 9 lembar (PDF) |
| `drawings/out/BG-*.dxf` | Lembar yang sama dalam DXF (AutoCAD), audit 0 error |
| `out/step/*.step` | Model 3D STEP (mm, berwarna): R-201, TK-101, PM-1, PM-4 ... PM-10 |
| `out/step/PLANT_step.zip` | Susunan pabrik lengkap (PLANT.step 66 MB, di-zip) |
| `out/BG_3D_renders.pdf` | Buku render 11 halaman (isometri depan/belakang, potong) |
| `out/render/*.png` | Render per modul |
| `out/ga.json` | Ukuran plot dari model 3D (dipakai `process/portable_modules.py`) |

## Daftar lembar
| No | Doc no | Isi | Skala |
|---|---|---|---|
| 1 | BG-GA-001 | Tata letak umum + tabel modul + skala set | 1:300 |
| 2 | BG-V-201 | Reaktor AnMBR R-201 (bejana standar, 14 unit) | 1:80 / 1:60 |
| 3 | BG-M-004 | PM-4 kontainer membran UF | 1:60 |
| 4 | BG-M-001 | PM-1 praolah | 1:60 |
| 5 | BG-M-006 | PM-6 pengolahan biogas + BTF-301 | 1:100 / 1:60 |
| 6 | BG-M-008 | PM-8 kontainer CHP + HX-401/ST-401 | 1:75 |
| 7 | BG-M-007 | PM-7 penampung gas GH-301 + flare FL-301 | 1:150 / 1:60 |
| 8 | BG-M-005 | Skid PM-5, PM-9 (CT-601), PM-10 | 1:60 |

## Regenerasi
```
cd cad/render && npm install three@0.160.0 playwright-core   # sekali
cd cad && python3 build.py            # semua modul + PLANT -> STEP, STL, render
cd cad/drawings && for f in d0*.py; do python3 $f; done
```
Renderer: three.js di Chromium headless (Playwright), karena VTK tidak punya OpenGL di container.

## Catatan
- Ukuran proses (volume reaktor, luas membran, debit, duty) diambil dari model proses `process/`.
  Ukuran mekanis lain (tebal pelat, nosel, rangka, tata letak di dalam kontainer, pondasi) adalah
  asumsi desain konseptual, bukan hasil desain detail ASME / struktur. Perlu verifikasi engineer berlisensi.
- Nama di blok judul (Universitas, Nama Tim, Checked/Approved) masih placeholder - isi sebelum dikirim.
- Luas plot dari GA = 89,8 x 31,9 m = 0,29 ha (termasuk jalan 3 m), menggantikan estimasi rumus 0,16 ha.

## Rev B (detail)
Lembar tetap 8, detail ditambah: DETAIL A/B reaktor, potongan C-C modul UF, DETAIL C cincin jepit GH, daftar material + massa di setiap lembar, tabel nosel BTF, data kinerja genset, tampak ujung.
Buku render dibuat ulang dengan `python3 make_renderbook.py`. GA memakai model pabrik dengan pipe rack + perpipaan antar reaktor.

## Rev C - model 3D lokasi + alir
- `site3d.py`: PKS proksi 45 t TBS/jam (loading ramp, rebusan, pabrik utama, boiler + cerobong, rumah mesin, pengolahan air, tangki CPO, fat pit), sistem kolam POME yang diukur dari debit dan HRT, kebun sawit, produk, rute pipa/kabel nyata (panjang -> CAPEX via `out/site.json`), pemeriksaan jarak aman.
- `build_site.py`: STEP lokasi (`out/step/SITE_step.zip`).
- `diorama.py`: render diorama lokasi `DIORAMA_lokasi.png`, `DIORAMA_lokasi-barat.png`, `DIORAMA_atas.png`, `DIORAMA_produk.png` - platform rumput, atap biru, panah alir kecil berwarna (POME, biogas, listrik, efluen, lumpur), label pil singkat + legenda alir.
- Lembar ke-9 `BG-GA-002` denah lokasi dengan tabel interkoneksi, luas lahan, jarak aman.
- Perbaikan tata letak produk: flare 16 m dari tepi GH (sebelumnya 7 m), kontainer CHP digeser (sebelumnya menumpang pondasi GH), jalur gas sesuai PFD (reaktor -> GH -> BTF/PM-6 -> CHP, cabang flare). Plot 0,34 ha.
