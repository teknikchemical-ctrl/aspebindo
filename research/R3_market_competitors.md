# R3: Market sizing (TAM/SAM/SOM) and competitor analysis
Portable thermophilic AnMBR biogas power set for POME (14 x 194 m3 reactors, 45 t FFB/h mill, ~1.09 MWe gross / 0.96 MWe net, 0.34 ha plot, BOO with mill fee, relocatable)

Compiled 2026-10-16. Companion files: `R3_numbers.json` (model parameters) and `R3_competitors.json` (matrix).

**Method and limits (please read first).**
- In this sandbox, WebFetch and curl could not open any page (DNS/proxy refused gapki.id, trase.earth, wikipedia and others). Every figure here therefore comes from search-engine extracts of the cited pages, not from the full documents.
- Treat confidence as at most **M** unless the figure is a widely reported headline number.
- Confidence tags: **[H]** = official or primary statistic, consistent across sources. **[M]** = single credible source or a derived number. **[L]** = vendor or press claim, old data, or analyst estimate.
- **EST** = our own estimate, no source.
- Project-internal values come from `process/outputs/results.json` and `finance/` (FCI, P_gross, plot).

---

## 1. Market: Indonesia

### 1.1 Mill population and capacity
- **Mills in operation: 1,318 (2022)**. The series is 1,125 → 1,171 → 1,218 (2020) → 1,278 → 1,318. Source: Trase/SEI-PCS Indonesia palm oil methodology v1.2.2 (updated Universal Mill List, UCSB), Sep 2024, https://resources.trase.earth/documents/data_methods/SEI_PCS_Indonesia_palm_1.2.2_ENG.pdf **[H]**
  - Of these, 28 mills had no capacity value. The earlier version (v1.2, Sep 2022) used 1,218 mills for 2020, 65 of them without capacity.
- **Universal Mill List 2023: 1,231 mills.** Source: cited in EarthArXiv preprint 2025, https://eartharxiv.org/repository/object/7300/download/14614/ (taken from our earlier `finance/research/market_data.md`) **[M]**.
  - The gap against Trase's 1,318 reflects different inclusion rules.
  - **Model base: 1,300 mills (range 1,231–1,400).**
- **"Over 600 mills" / "~640 mills" is outdated** (2017–2019 figures still quoted in APEC 2017 and the IOP 2019 review). Do not use. Sources: APEC 2017, https://www.apec.org/docs/default-source/Publications/2017/3/Strategy-for-LargeScale-Implementation-of-Biogas-Capture-from-Palm-Oil-Mill-Effluent-and-Reuse-for-R/217_EWG_Biogas-from-Palm-Oil-Mill-Effluent_Final-Report-for-APEC-Secretariat.pdf ; IOP EES 293 (2019) 012004, https://iopscience.iop.org/article/10.1088/1755-1315/293/1/012004 **[H that it is outdated]**
- **Mills without their own estate (PKS tanpa kebun): ~442 units nationally**, quoted at a GAPKI forum. Source: GAPKI news, 10 Sep 2026, https://gapki.id/news/2026/09/10/pks-tanpa-kebun-dan-berondolan-ancam-ekosistem-rantai-pasok-sawit-yang-sudah-mapan/ **[M]**
  - That is about **34%** of 1,300 mills.
  - No base year is given, so growth cannot be computed from this source.
- **Growth signals for independent and new mills:**
  - Rokan Hulu (Riau) went from 36 to 74 mills in 2020–2024, a 105.6% increase. Source: Jerkin journal, https://jerkin.org/index.php/jerkin/article/download/3935/2872 **[M]**
  - Riau NGO cites 285 operating mills, not all with nucleus estates. Source: RiauPagi, Apr 2024, https://riaupagi.com/news/pabrik-kelapa-sawit-tanpa-kebun-kembali-dievaluasi-salamba-perlu-buka-data-terhadap-285-perusahaan-yang-menyalah-beri-sanksi-tegas-202404073991/ **[L]**
  - South Sumatra police chief: about 22 mills operating without a nucleus estate. Source: ANTARA, Dec 2025, https://www.antaranews.com/berita/5296279/kapolda-sumsel-soroti-puluhan-pabrik-sawit-beroperasi-tanpa-kebun-inti **[M]**
  - APKASINDO: 1,118 mills (2019), of which only 20–28% partner with smallholders. Source: Sawit Indonesia, https://sawitindonesia.com/apkasindo-pabrik-sawit-tanpa-kebun-harus-diwajibkan-bermitra/ **[L]**
- **Installed capacity versus throughput (overcapacity):** installed mill capacity is about 85 Mt CPO-eq/yr against 41 Mt CPO actually produced, roughly 2x. Source: Trase Infobrief 09 (about 2019 data), https://resources.trase.earth/documents/infobriefs/infobrief09EN.pdf **[M]**
  - This matters for us. Low utilisation and competition for FFB mean some mills close or idle, which supports the relocatability argument.
- **Provincial examples:**
  - Kaltim: **99 mills, 5,662 t FFB/h installed, 4,965 t/h used** (average 57 t/h per mill). Source: Disbun Kaltim, https://disbun.kaltimprov.go.id/artikel/kaltim-miliki-99-pabrik-pengolahan-kelapa-sawit **[H] (about 2022)**
  - Astra Agro Lestari: **32 mills, 1,570 t/h** (average 49 t/h). Source: Sawit Indonesia, https://sawitindonesia.com/5-emiten-sawit-dengan-jumlah-pabrik-sawit-terbanyak/ **[M]**
- **Provincial split (model input, mostly EST):**

  | Province | Mills (EST) |
  |---|---|
  | Riau | ~260 |
  | Sumut | ~180 |
  | Kalteng | ~130 |
  | Kalbar | ~120 |
  | Sumsel | ~110 |
  | Kaltim | 99 (sourced) |
  | Jambi | ~90 |
  | Kalsel | 46 (GAPKI Kalsel) |
  | Others | ~196 |

  - Source: `finance/research/market_data.md`. **[L]**
  - Papua holds about 1% of national mill capacity (11 mills in 2020). Source: Trase insight, https://trase.earth/insights/indonesia-makes-progress-towards-zero-palm-oil-deforestation **[M]**
  - **Gap:** no public province x capacity-class table was found. The Trase 2023 mill CSV (https://trase.earth/open-data/datasets/indonesia-palm-oil-mills) has a capacity field per mill and should be downloaded outside this sandbox to replace these estimates.
- **Capacity-class split (EST)** **[L]**:

  | Capacity class | Share of mills (EST) |
  |---|---|
  | <30 t/h | ~25% |
  | 30–45 t/h | ~30% |
  | 45–60 t/h | ~35% |
  | >60 t/h | ~10% |

  - Anchors:
    - Kaltim average is 57 t/h. Astra average is 49 t/h.
    - "Large mills 10–60 t/h", and an East Kalimantan sample range of 30–90 t/h.
    - APEC: mills below 30 t/h (~1 MW) are less viable; 60–90 t/h mills give about 2 MW.
  - **Implied national installed capacity: about 1,300 x ~50 t/h ≈ 65,000 t FFB/h** **[L/EST]**. At 6,000 h/yr that is about 390 Mt FFB/yr capacity, against roughly 250 Mt processed. Utilisation is therefore about 64%, consistent with Trase's overcapacity finding.

### 1.2 Production, FFB and POME
- **CPO production:**
  - 2024: **48.16 Mt**
  - 2025: **51.66 Mt** (+7.2%). CPO+PKO 2025 was 56.55 Mt, against 52.76 Mt in 2024.
  - Source: GAPKI via Kontan, Mar 2026, https://industri.kontan.co.id/news/gapki-catat-produksi-cpo-nasional-naik-72-di-tahun-2025 **[H]**
  - Ministry of Agriculture's 2024 figure is 47.47 Mt (provisional), and BPS gives 45.44 Mt. Sources: satudata.pertanian.go.id, https://satudata.pertanian.go.id/details/publikasi/696 ; Kompas data **[H]**
- **CPO 2026 forecast:** GAPKI says +1–5%. The chairman cites total oil of about 57 Mt, which implies CPO of about 52–54 Mt. A Reuters analyst median is 51.2 Mt. Sources: Bisnis, 13 Mar 2026, https://ekonomi.bisnis.com/read/20260313/12/1960184/gapki-cemas-pasokan-cpo-makin-ketat-produksi-2026-diproyeksi-hanya-naik-2 ; Kontan https://industri.kontan.co.id/news/gapki-prediksi-produksi-sawit-2026-naik-4-5-fokus-produktivitas **[M]**
  - **Model: 52.5 Mt (range 51–54).**
- **FFB processed: about 250 Mt/yr.** Basis: BRIN/PASPI ("16.8 Mha produce ~250 Mt FFB/yr"). Source: RRI, Aug 2026, https://rri.co.id/en/technology/2661068/indonesia-has-potential-to-use-pome-as-clean-energy-source **[M]**
  - Cross-check: 51.66 Mt CPO / OER 20.5% = 252 Mt.
  - OER is not published nationally. Malaysia's 2024 OER was 19.67% (MPOB, https://bepi.mpob.gov.my/images/overview/Overview2024.pdf) **[H for MY]**.
- **POME generation: 125 Mt/yr (PASPI, 0.5 t/t FFB) to 164 Mm3/yr (0.65 m3/t FFB x 252 Mt).** Source: Bioenergy Insight, 2026, https://www.bioenergy-news.com/news/indonesias-palm-oil-waste-could-generate-3-6-billion-cubic-metres-of-biogas-annually/ **[M]**
  - Our design basis uses 0.65 m3/t (585 m3/d for 45 t/h x 20 h).
  - **Model: 150 Mm3/yr (125–170).**
- **Biogas potential: 3.6 bn m3/yr (28.8 m3 biogas per t POME). Utilisation is ≤15%.** Source: PASPI/BRIN via Bioenergy Insight (same URL) **[M]**
- **Technical power potential:**
  - **~1.1 GWe.** Source: World Biogas Association Indonesia Market Report, Dec 2022, https://www.worldbiogasassociation.org/wp-content/uploads/2022/12/WBA-Market-Report-indonesia.pdf **[M]**
  - **1,113.39 MW across 22 provinces** (ESDM figure cited by Gree Energy), https://gree-energy.com/unlocking-the-power-of-biogas-from-palm-oil-mill-effluent/ **[M]**
  - APEC 2017: ">1,000 MW". **[M]**
  - Cross-check with our design (1.088 MWe gross per 270 kt FFB/yr): 252 Mt → **~1,015 MWe gross**. This is consistent.

### 1.3 Methane-capture penetration
- **Installed POME biogas: 84 PLTBg, 165 MW, of which 53.7 MW is grid-connected** (≈ 111 MW captive or own use). Source: GAPKI, 30 May 2026, https://gapki.id/en/news/2026/05/30/pome-to-electricity-expands-sustainability-of-palm-industry/ **[M]** (reference year unclear; cites EBTKE)
  - Five CBG (compressed biomethane) plants were under construction.
- **EBTKE dashboard: PLTBg (all feedstocks) 164.10 MW, April 2026.** Source: https://ebtke.esdm.go.id/ **[H]**
- **WBA (2022):** 78 industrial AD plants with 161.6 MWe in total, of which about 130 MWe is POME. Source: WBA report above **[M]**
- **Share of mills with capture:** historically "<10% of ~640 mills" (IOP 2019 review) and "<10% of POME used for electricity" (APEC 2017). **[M, dated]**
  - PASPI 2026: ≤15% of the biogas potential is used **[M]**.
  - Bottom-up check: 84 PLTBg, plus captive flaring or boiler-only plants (for example KIS's PT Maya plant, 20,056 m3/d to boiler, 2013, https://kisgroup.net/client8.html), plus CBG sites.
  - Company counts: Wilmar has 25 methane-capture facilities across ID+MY at end-2023 (https://www.wilmar-international.com/sustainability/responsible-operations/reducing-greenhouse-gas-emissions). Musim Mas: 17 by 2024 (https://www.musimmas.com/resources/blogs/musim-mas-circular-waste-mills-driving-solutions-to-sustainability-challenges/). Asian Agri: 7 in 2018, target 20 (https://riau.antaranews.com/berita/60120/asian-agri-to-build-20-units-of-pltb-until-2020).
  - **Model: ~150 mills (11.5%; range 120–200) have capture. About 1,150 mills (88%) do not** **[M/EST]**.
- **No binding methane-capture mandate (as of Aug 2026).** PASPI and BRIN are calling for one, plus carbon trading and a biogas blending mandate. Sources: energynews.pro, https://energynews.pro/en/indonesia-weighs-turning-palm-oil-mill-effluent-into-biogas ; Palm Oil Magazine, Aug 2026, https://www.palmoilmagazine.com/sustainability/2026/08/19/brin-indonesia-has-potential-to-become-a-major-global-palm-oil-biogas-producer/ **[M]**
- **Effluent rules:**
  - Discharge to water: BOD ≤100, COD ≤350, TSS ≤250 mg/L (PermenLH 5/2014).
  - Land application: BOD ≤5,000 mg/L under KepMenLH 28/29/2003. These decrees were reportedly revoked by PermenLHK 5/2021, which leaves a regulatory gap. Source: Kontan, https://industri.kontan.co.id/news/pemerintah-disarankan-revisi-aturan-pemanfaatan-limbah-cair-kelapa-sawit **[M]**
- **Tariff:**
  - Perpres 112/2022 PLTBg ceiling for ≤1 MW is about 10.18–11.47 x F USc/kWh in years 1–10 (sources conflict; see `finance/research/market_data_2.md`).
  - **Excess power: 7.43–7.44 USc/kWh.** Source: Katadata, https://katadata.co.id/ekonomi-hijau/energi-baru/6322b0d0c80d2/diatur-perpres-ebt-ini-rincian-harga-listrik-dari-energi-terbarukan **[M]**

### 1.4 Malaysia (regional expansion)
- **453 mills, 123.46 Mt FFB/yr processing capacity (2024).** Source: MPOB JOPR "Oil palm economic performance in Malaysia and R&D progress in 2024", Jun 2025, https://jopr.mpob.gov.my/wp-content/uploads/2025/06/OIL-PALM-ECONOMIC-PERFORMANCE-IN-MALAYSIA-AND-RD-PROGRESS-IN-2024.pdf **[H]**
  - Heliyon 2024 cites 447 operating mills.
- **Biogas capture: about 30% of mills (December 2024).** Source: MPOB Palm Oil Engineering Bulletin 148, https://palmoilis.mpob.gov.my/publications/POEB/poeb148-soh.pdf **[M]**
  - Earlier points:
    - 135 mills in 2021 (MPOB JOPR, https://jopr.mpob.gov.my/renewable-energy-and-greenhouse-gases-emission-reduction-potential-of-biogas-from-palm-oil-mill-effluent/).
    - 125 of 452 in 2020 (USDA FAS Biofuels Annual MY2024, https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Biofuels+Annual_Kuala+Lumpur_Malaysia_MY2024-0010.pdf).
    - 94 in Sep 2017, of which **56 were tanks and 38 covered lagoons** (MPOB POEB 126).
  - Capture has been mandatory for new and expanding mills since 2014. Existing mills have "no requirement or incentive" (USDA FAS). **[H]**
- **Malaysia potential: 508 MWe from all mills (2021).** Source: MPOB JOPR (above) **[M]**
- **Implied Malaysian SAM: about 300–320 mills without capture** **[M/EST]**. Note that the Malaysian market is consolidating around centralised biomethane hubs (Kluang injection station, 2025, https://www.qcintel.com/biofuels/article/malaysia-eyes-first-pome-based-centralised-biogas-hub-in-q2-reports-41463.html).

### 1.5 TAM / SAM / SOM (bottom-up, Indonesia)

Unit: one "set-equivalent" = 45 t/h x 20 h x 300 d = 270 kt FFB/yr = ~160–175 k m3 POME/yr = 1.09 MWe gross. Revenue per set averages about USD 1.26 M/yr over the project life (finance model `fin_market.market()`). That is about USD 8 per m3 POME.

| Layer | Definition | Mills | Set-equivalents | MWe gross | Revenue USD/yr | Capex pool USD |
|---|---|---|---|---|---|---|
| **TAM** | All Indonesian POME (125–164 Mm3/yr) | ~1,300 | 774–1,015 | 0.85–1.1 GW | 0.98–1.28 bn | 4.3–5.6 bn |
| **SAM** | No capture (88%) x 30–60+ t/h class (~70–75%) x Sumatra+Kalimantan (85%) x road-accessible (~95%) | ~720 | 405–530 | 0.45–0.58 GW | 0.51–0.67 bn | 2.2–2.9 bn |
| **SAM-beachhead** | Independent mills without estates (442), no capture (~95%), ≥30 t/h (~75%) | ~315 | ~250 | ~0.27 GW | ~0.32 bn | ~1.4 bn |
| **SOM (2034)** | Finance fleet plan (1→8 sets/yr, 40 sets cumulative) | 40 | 40 | 44 MW | ~0.05 bn | ~0.22 bn |

- **SOM as a share of SAM is about 8–10% of sets in 8 years.** This is aggressive for a new entrant. Benchmarks:
  - reNIKOLA signed 8 PTPN IV mills in about 3 years (2023 MoU to 2026 offtake).
  - Asian Agri built about 7 in-house plants in about 5 years.
  - Installed PLTBg nationally grew from about 120 MW (2021) to about 164 MW (2026), roughly **+9 MW/yr for the whole country** (EBTKE).
  - **Our plan adds up to ~8.7 MW/yr by 2034, close to the entire historical national build rate.** A conservative SOM of 15–20 sets by 2034 (2–4% of SAM) is more defensible. **[EST]**

---

## 2. Competing technologies and alternatives

Project-internal reference: FCI 2026 USD 5.42 M, P_gross 1.088 MWe, P_net 0.961 MWe, giving **USD ~4.98 M/MWe gross (5.64 M/MWe net)**. The 0.34 ha plot comes from the 3D GA, the 11-month build from `fin_market.COMPET`, and effluent COD of about 4,800 mg/L (≈90% removal) from the process model.

### (h) Do nothing: open anaerobic ponds
- **Land:**
  - 1–5 ha in a peer-reviewed Malaysian comparison (≈85% of MY mills use ponds). Source: J. Cleaner Prod. 2020, https://www.sciencedirect.com/science/article/abs/pii/S0959652620314086 **[M]**
  - 30–45 acres (12–18 ha) in an older review. Source: Processes 9(5):739 (2021), https://www.mdpi.com/2227-9717/9/5/739 **[M]**
  - Our site baseline is 2.2 ha of ponds, about 1.1 ha of which is acid/anaerobic (project GA).
- **HRT:** anaerobic series 54–60 d; full train 100–160 d (same review) **[M]**
- **Methane:**
  - Ponds emit most of the removed carbon as CH4 and CO2. Source: ScienceDirect 2026, https://www.sciencedirect.com/science/article/pii/S004565352600007X **[M]**
  - 137–163 kg CO2e/t FFB (earlier R1 research) **[M]**
- **Business model:** none (sunk cost). The mill carries methane, odour and compliance risk, and gets no energy.

### (a) Covered lagoon (HDPE cover over an existing or new pond)
- **Capex:**
  - APEC 2017 assumes USD 2–4 M/MW with a typical 1.8 MW per mill. Its Jambi 2.4 MW feasibility case is USD 5.49 M total (≈ USD 2.3 M/MW). URL as in §1.1. **[M]**
  - Energies 15(19):7265 (2022, Indonesian POME): 2,256–3,669 USD/kW, mean 2,758. https://doi.org/10.3390/EN15197265 **[M]**
  - West Kalimantan 60 t/h mill: USD 3.1 M investment (2.9 M capex) (APEC/WBA extract) **[L]**
  - Bangka 2 MW: IDR 63.5 bn ≈ USD 4.0 M at 15.9k (Energies 2022) **[M]**
  - **Model: USD 1.8–2.5 M/MWe.**
- **Why Indonesia uses lagoons:** "covered lagoon is prevalent in Indonesia mainly because investment costs are low and it does not require highly skilled HR" (search extract of the Energies/IOP reviews) **[M]**
- **Footprint:** PLTBg Sei Mangkei (2.4 MW, Pertamina NRE + PTPN III) sits on **about 2 ha**. Source: zonaebt, https://zonaebt.com/pltbg-sei-mangkei-24-mw-olah-limbah-pome-jadi-energi-hijau/ **[M]**
  - Scaled to 45 t/h (~1.1 MW): **~1.0–2.0 ha** (EST; the lagoon often reuses existing pond area).
- **COD removal:** up to 91%, with 55% CH4, at a 30 t/h Bangka mill. Source: e3s-conferences 2024 / Energies 2022 **[M]**
- **Operating issues:**
  - Scum under the cover degrades the cover, blocks gas off-takes and reduces working volume.
  - Desludging is hard without removing the cover. Source: MLA covered anaerobic lagoon info sheet, https://www.mla.com.au/contentassets/71c5008960fe4b709543799e4b903431/info-sheet-for-cal.pdf **[M]**
  - Non-UV-stabilised HDPE cracks after a few years (vendor). Source: beta.co.id, https://beta.co.id/blog/pome-jadi-daya-menutup-kolam-menghidupkan-jaringan **[L]**
  - Scum, sludge washout and low TSS removal in Indonesian systems; "performance data for covered lagoons in Indonesia is scarce". Source: J. Cleaner Prod. 2020 (above) **[M]**
- **Build time:** livestock-sector vendors claim 2–4 months **[L]**. A POME covered lagoon with genset, grid interconnection and permits typically takes **9–15 months** **[EST]**.
- **Life-cycle cost (Malaysia):** lagoon LCC USD 0.55 M/yr versus CSTR USD 0.63 M/yr. Source: RSER 2021 LCCBA, https://www.sciencedirect.com/science/article/abs/pii/S1364032121012533 **[M]**
- **References:**
  - Sei Mangkei 2.4 MW (Pertamina NRE/PTPN III).
  - AANE Belitung, the first commercial POME IPP (ESDM, https://www.esdm.go.id/en/media-center/news-archives/melihat-lebih-dekat-pembangkit-listrik-biogas-komersil-pertama-di-indonesia).
  - PLTBg Jangkang, Bangka: 1.2 → 1.8 MW in 2016.
  - Asian Agri: about 2 MW per plant; PT Indo Sepadan Jaya adds 1 MW excess to PLN on a 3-year PPA (Aug 2025). Source: Malay Mail, https://www.malaymail.com/news/money/mediaoutreach/2025/08/26/asian-agri-signs-agreement-to-supply-renewable-energy-to-pln-in-north-sumatra/404658 **[M]**
- **Suppliers:** HDPE geomembrane installers (Solmax/GSE, local "geosintetik" firms such as Petrane), KIS Group, local EPCs. **Asia Biogas, Novaenergi and CDM Smith had no Indonesian POME evidence in our search.** We do not claim them.

### (b) CSTR / tank digesters (steel, enamelled-bolted or concrete)
- **Capex:**
  - **TSE Group (Berkat Cipta Abadi), South Papua:** 2 tanks of 7,800 m3, 1,000 m3/d POME, **2 MW, USD 3.6 M (≈ USD 1.8 M/MW)**. Operating since May 2025, inaugurated 1 Aug 2025. Sources: InfoSawit, https://en.infosawit.com/news/15379/tse-group-invests-us--3-6-million-to-build-biogas-plant--a-bold-step-towards-net-zero-emissions ; Petromindo, https://www.petromindo.com/news/article/first-biogas-power-plant-in-papua-inaugurated **[M]**. This is a strong, low benchmark, and it uses a tank.
  - Malaysia closed digester, 60 t/h, ~1.8 MW: RM 18–20 M (≈ USD 2.3–2.5 M/MW). Source: MDPI review 2025, https://www.mdpi.com/2673-8783/6/5/77 **[M]**
  - MPOB (2011): biogas trapping RM 4–6 M per mill (capture only). https://tot.mpob.gov.my/wp-content/uploads/2020/02/TT-491.pdf **[M, dated]**
  - **Model: USD 2.0–3.5 M/MWe.**
- **Footprint:** **~0.5–1.0 ha** for 45 t/h **[EST]** (two 7,000–8,000 m3 tanks of ~30 m diameter, plus genset, gas holder and buffer).
- **Build time:** 12–18 months (generic tank AD) **[L]**. PTPN IV Sei Garo (with Aiken Kakoki, Japan) took about 2 years from late-2023 start to commissioning in Nov 2025. Sources: Petromindo, https://www.petromindo.com/news/article/ptpn-iv-japan-s-aiken-kakoki-accelerate-construction-of-palm-biogas-plant ; QCIntel, https://www.qcintel.com/biofuels/article/ptpn-iv-launches-pome-based-biogas-plant-in-riau-province-report-52994.html **[M]**
- **COD removal:** 80–95% **[M]**
- **Operating issues:**
  - Full-scale POME digesters see low pH and VFA accumulation (Thai full-scale). Source: PMC7797170, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7797170/ **[M]**
  - Mixer energy and maintenance. Roof/foam design matters; see "Seleksi desain roof tank CSTR untuk plant biogas POME setara 700 kW", https://www.researchgate.net/publication/352517946 **[M]**
- **Players:**
  - KIS Group: PT Maya (Poliplant), 6,975 m3 digester, 2013.
  - GWE (RAPTOR/ANAMIX; no POME reference found).
  - Weltec, Biotec, Center Enamel (bolted tanks, Thai POME EPC, https://www.wateronline.com/doc/center-enamel-epc-contractor-for-palm-oil-wastewater-treatment-project-in-thailand-0001), Aqualimpia, Aiken Kakoki.

### (c) UASB / EGSB / IC high-rate reactors
- **Fit to POME:** POME has high suspended solids and oil (raw COD ~50 g/L, of which a large share is particulate), so granular-sludge reactors need solids and oil removal first. Clogging is "the major problem in anaerobic biofilm systems". Source: J. Env. Mgmt 2022 review, https://www.sciencedirect.com/science/article/abs/pii/S0301479722013238 **[M]**
- **Full-scale references:** MPOB co-developed UASB-hybrid plug-flow and EGSB systems in Malaysia **[M]**. **No Paques or Veolia Biothane full-scale POME plant was found** **[L for absence]**.
- **Capex:** USD 2–3.5 M/MWe including pre-treatment **[EST]**. **Footprint** 0.2–0.5 ha **[EST]**. **COD removal** 80–90% of soluble COD **[M]**.

### (d) AnMBR vendors (our technology class)
- **Veolia Memthane (ex ADI-MBR with Kubota):**
  - References in ethanol, dairy, confectionery and food.
  - Jack Link's: permeate BOD <100 ppm, >98% BOD removal.
  - Sources: Veolia, https://www.veoliawatertechnologies.com/en/solutions/technologies/memthane ; https://www.veoliawatertech.com/en/case-studies/jack-links-wastewater-treatment **[M]**
  - Ken's Foods (USA) ADI-AnMBR, 100,000 gpd (≈380 m3/d), 2009. Source: pollutionsolutions-online **[M]**
  - **No full-scale POME AnMBR found anywhere** **[M]**.
- **Capex versus a covered lagoon:**
  - AMPC (Australian meat, 3.3 ML/d): AnMBR about 9.7 M versus covered anaerobic lagoon about 4.05 M, i.e. **2.4x**; payback 8.8 yr. Source: https://ampc.com.au/media/vbqmc2bg/ampc_anaerobicmembranebioreactors_snapshot.pdf **[M]**
  - AnMBR capex is "comparable to CAL only at idealised 10 kgCOD/m3·d and 15 LMH; high at demonstrated parameters". Source: https://ampc.com.au/media/vdtf2ibm/ampc_anaerobicmembranebioreactors_factsheet.pdf **[M]**
- **Performance on POME (lab or pilot):**
  - Thermophilic (55 °C) PTFE hollow-fibre AnMBR: **COD removal 93–98%** at OLR 2–10 kg COD/m3·d; 0.56 m3 CH4/kg COD removed; **organic fouling 93% of total fouling**. Source: Membranes (PMC6523901), https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6523901/ **[M]**
  - Two-stage AnMBR at OLR 98 kg COD/m3·d: 70% COD removal. Source: BioResources, https://bioresources.cnr.ncsu.edu/resources/performance-of-a-high-rate-two-stage-anaerobic-membrane-bioreactor-anmbr-for-the-treatment-of-palm-oil-mill-effluent/ **[M]**
  - Malaysian 1-yr pilot (pretreatment + AD + membrane): COD down to about 3,587 mg/L; biogas 27.65x the POME volume. Source: PMC4317585, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4317585/ **[M]**
- **Evoqua:** no POME AnMBR evidence found.

### (e) Composting with POME (EFB + POME co-composting, "zero discharge")
- **Mass balance:** a pilot used 40 t EFB with 120 t partially treated POME (≈3 m3 POME per t EFB); the C/N ratio fell from 51 to 15 in 60 d. Source: scialert IJAR 2009, https://scialert.net/fulltext/?doi=ijar.2009.69.78 **[M]**
  - A 45 t/h mill produces about 0.22 t EFB/t FFB, ≈ 59 kt EFB/yr, which could absorb about 60–100% of POME by evaporation in windrows **[EST]**.
- **Combining with biogas:** coupling a POME digester with anaerobic co-composting of EFB adds about 0.93 MW for a 45 t/h mill. Source: PubMed 26398023, https://pubmed.ncbi.nlm.nih.gov/26398023/ **[M]**. This is complementary to biogas, not purely a competitor.
- **Indonesia reference:** Winrock/WIPO GREEN EFB composting pilot, May 2025–Jul 2026. Source: https://winrock.org/projects/the-empty-fruit-bunch-composting-project/ **[M]**
- **Capex:** **not found**. EST USD 1–2.5 M per 45–60 t/h mill (turners, roofed pad, leachate pond). **Land** 2–4 ha **[EST]**.

### (f) POME to bio-CNG / biomethane / bio-methanol
- **reNIKOLA + PTPN IV PalmCo + Pertagas Niaga:**
  - 8 PTPN IV mills; **US$40–45 M (~Rp790 bn)**; >830,000 MMBtu/yr; **15-year gas sales agreement (Aug–Sep 2026)**; BOO/BOOT.
  - First plant: Tinjowan (Simalungun), 162,000 MMBtu/yr, **14-month build**, full operation by Q4 2026.
  - Sources: The Star, 19 Aug 2026, https://www.thestar.com.my/business/business-news/2026/08/19/renikola-secures-long-term-gas-sales-agreement-in-indonesia ; Mitrapol, 10 Sep 2026, http://mitrapol.com/2026/09/10/cbg-palmco-renikola-pertagas-niaga/ ; Petromindo, https://www.petromindo.com/news/article/perkebunan-nusantara-iv-palmco-breaks-ground-on-indonesia-s-first-palm-waste-based-cbg-plant **[M]**
  - Earlier ambition: 50 CBG projects, >US$300 M (RM1.4 bn) over 5 years (MIDA/BusinessToday 2023) **[M]**.
  - **Implied ≈ US$5.3 M per mill.** 104k MMBtu/yr per mill ≈ 30 GWh_th, ≈ 1.3 MWe-equivalent at 38% efficiency, so **≈ US$4 M per MWe-eq** **[EST]**.
- **KIS Biofuels + Toyota Tsusho (JV KTBI, KIS 51%):** South Sumatra biomethane, groundbreaking 5 Oct 2026, ~150,000 MMBtu/yr from 2027, gas into PGN pipeline to Java industry. Source: Sirkularium, https://sirkularium.com/en/insight/pgn-south-sumatra-biomethane-plant-toyota-industry **[M]**
  - PGN/Gagas–KIS offtake: 36,500 MMBtu in year 1. Source: GAPKI Jan 2024, https://gapki.id/en/news/2024/01/19/pgn-to-distribute-palm-waste-based-biogas/ **[M]**
  - KIS is moving to BOOT. Source: responsAbility, https://www.responsability.com/en/magazine/kis-group-turning-waste-into-cleaner-fuel-in-indonesia **[M]**
- **Pertamina NRE:**
  - Operates PLTBg Sei Mangkei 2.4 MW.
  - MoU with CRecTech (Apr 2026) for a 50 t/yr biogas-to-biomethanol pilot at Sei Mangkei (target Dec 2026); commercial plant about 2028.
  - Sources: Hydrocarbon Processing, https://www.hydrocarbonprocessing.com/news/2026/04/pertamina-and-crectech-sign-mou-to-explore-pilot-biogas-to-biomethanol-facility-in-sez-indonesia/ ; Bioenergy International, https://bioenergyinternational.com/pertamina-nre-and-crectech-eye-biogas-to-methanol/ **[M]**
  - Joint POME biomethane study with Osaka Gas, JGC and INPEX (Bioenergy Insight) **[M]**.
- **Implication:** biomethane is the fastest-moving, best-capitalised competitor for **large state and group mills near gas infrastructure**. It needs scale and long offtake contracts, so it targets clusters, not isolated independent mills.

### (g) Evaporation / ZLD / membrane polishing
- **Cost barrier:** "the payback period for the high capital investment remains a significant hurdle", and long-term operating data is lacking. Source: Sustainability 17(23):10665 (2025), https://doi.org/10.3390/su172310665 **[M]**
- **Polishing performance:** MPOB BioAX polishing pilot (5 m3/h): BOD <20 mg/L in 80.8% of readings. Membrane/RO pilots reach BOD <20 with boiler-feed reuse (PMC4317585) **[M]**
- **Role:** this is a **post-treatment complement** after anaerobic treatment (required in sensitive Malaysian areas, 20 ppm), not a methane-capture alternative. It could pair with our AnMBR permeate (low TSS) as an upsell.

---

## 3. Business-model competitors (IPP / ESCO / BOO)

| Player | Model | Offer to the mill | Scale / evidence | Conf. |
|---|---|---|---|---|
| reNIKOLA (MY) / PT reNIKOLA Primer Energi | BOO(T) CBG, 15-yr offtake to Pertagas Niaga | Mill supplies POME; developer funds US$5 M/mill; mill gets methane compliance plus a likely revenue share (terms not public) | 8 PTPN IV mills, US$40–45 M; target 50 projects | M |
| KIS Group / KIS Biofuels (+ Toyota Tsusho) | Technology provider moving to BOOT; bio-CNG to PGN/Gagas | Turnkey, or BOOT with gas sale | PT Maya 2013; S. Sumatra JV 150k MMBtu/yr (2027) | M |
| Pertamina NRE (+PTPN III) | State JV IPP / energy hub | Co-development on PTPN land | Sei Mangkei 2.4 MW on ~2 ha; biomethanol pilot | M |
| Gree Energy (Jakarta) | IPP and on-site BioLNG co-location | Three-party MoU with PLN and mills; mills supply POME | MoU only (https://gree-energy.com/gree-energy-signs-3-parties-mou-with-pln-and-palm-oil-mills-for-biogas-development/); Third Derivative portfolio | L |
| PT Austindo Aufwind New Energy (AANE) | First commercial POME IPP (Belitung) | IPP selling to PLN | ESDM news (capacity not in extract) | M |
| Aiken Kakoki (JP) + PTPN IV | EPC / tech partner | PTPN IV-owned | Sei Garo, Riau, commissioned Nov 2025 | M |
| In-house group programmes (Wilmar 25, Musim Mas 17, Asian Agri ~7–20, GAR ≥6, PTPN) | Own capex | n/a: they capture their own mills | Company reports | M |
| TSE Group (Berkat Cipta Abadi) | Own capex, captive plus CBG | n/a | 2 MW, US$3.6 M, South Papua 2025 | M |
| PLN Nusantara Power, Indonesia Power, Medco, Clean Power Indonesia, Blue Sphere | **No POME-biogas activity found in our searches** | – | Not verified; do not cite as competitors without checking | L |

- **Typical offer:** the developer takes POME **free of charge**, and the mill gets compliance, odour reduction, sometimes a revenue share or power.
- **We found no evidence of mills paying a treatment or tipping fee** (see also `finance/research/market_data_2.md` §4). **Our "mill fee" is about 50% of project revenue (`summary.json share_fee = 0.497`). That is the biggest commercial risk against these competitors.**

---

## 4. Buyer behaviour: why mills have not adopted biogas

No national survey with percentages was found. The evidence comes from case studies and reports:

- **Economics and payback:**
  - IRR 6.75%, NPV negative, **payback 10.8 yr**. The main problem was insufficient POME. Source: Riau small-scale study, MATEC 2019, https://www.matec-conferences.org/articles/matecconf/abs/2019/09/matecconf_icpse2018_03004/matecconf_icpse2018_03004.html **[M]**
  - A 30 t/h mill: IRR 12.5%, payback 6.6 yr, investment US$1.98 M (ResearchGate techno-economic) **[M]**
  - Malaysian FiT cases: payback 9–10 yr for a 60 t/h mill (Khor Reports) **[L]**
- **PLN and the grid:**
  - PLN is reluctant to sign PPAs at feed-in tariffs that cause it losses (APEC 2017) **[M]**
  - Mills are remote; grid extension costs **USD 28–42k/km**; on-site use is recommended (WBA 2022) **[M]**
  - The excess-power tariff is only 7.44 USc/kWh.
- **Finance:** AD plants are perceived as high risk by lenders (WBA 2022) **[M]**. High upfront cost deters smaller firms (Gree Energy blog) **[L]**
- **Regulation:** no binding mandate, so capture remains voluntary. Existing Malaysian mills likewise had "no requirement or incentive" (USDA FAS) **[M]**
- **Skills and complexity:** "capital requirements and technical complexity" (MDPI 2025 MY review) **[M]**. Lagoons are chosen because they need little skilled HR (Indonesian reviews) **[M]**
- **Feedstock risk:** low or uncertain throughput (above), which is acute for independent mills competing for FFB, at a national utilisation of about 64% **[EST]**.
- **Pull factors (counter-evidence):**
  - EU RED II/ISCC and CORSIA: palm biofuel essentially needs methane capture to pass GHG thresholds (see `market_data_2.md` §3).
  - ISPO becomes mandatory for downstream and bioenergy by Mar 2027.
  - Diesel displacement: ~Rp4,000–5,000/kWh versus <half that for biogas (Jakarta Post 2013/2015) **[M]**

---

## 5. Portable / modular AD units elsewhere (USP support or attack)

- **SEaB Energy Flexibuster/Muckbuster (UK):** containerised AD for 0.2–20 t/d of organic waste (sources inconsistent: 0.5–5 t/d, 0.5–2.5 t/d). Price from about US$181.5k (LA County 2020 survey).
  - Sources: https://seabenergy.com/products/anaerobic-digesters/ ; http://dpw.lacounty.gov/epd/socalconversion/PDFS/2020_Small_Scale_Food_Waste_Technology.pdf **[M]**
  - Our set handles about 585 m3/d, roughly **30–100x larger**.
- **Qube Renewables (bioQUBE / quickQUBE, now owned by Blue Planet):** 20/40-ft container and flat-pack bladder digesters; "rapidly deployable". Sources: power-technology, https://www.power-technology.com/features/qube-ikea-renewable-energy/ ; Energy Catalyst case (Kenya dry AD) **[L/M]**
- **HomeBiogas:** household scale. Its commercial unit handled 200 kg/d food waste (beta, Israel). Source: BioCycle, https://www.biocycle.net/on-site-commercial-food-waste-digester/ **[M]**
- **Impact Bioenergy:** US$133–383k base systems, 1–9 kW generators (LA County 2020) **[M]**
- **Industry trend:** "modular approaches (containers), mobile units and plug & play" (BiogasWorld) **[L]**
- **Methanogen (Uganda), BioHiTech, ScanTech, and Malaysian skid-mounted POME units:** **no evidence found**.
- **Reading:**
  - Containerised AD exists only at **small food-waste or farm scale (≤20 t/d, ≤~100 kW)**. We found **no MW-scale relocatable POME digester anywhere**.
  - That supports novelty, but it also means **no market proof that buyers value relocation**, and no reliability record at our scale.
  - Bolted-steel/enamel tank vendors (Center Enamel and similar) are the nearest "partly demountable" incumbents.

---

## KEY NUMBERS FOR MODEL

| Parameter | Base | Low | High | Unit | Source (short) | Conf. |
|---|---|---|---|---|---|---|
| Mills operating, Indonesia | 1,300 | 1,231 | 1,400 | mills | Trase 2024 (1,318 for 2022); UML 2023 (1,231) | H/M |
| Independent mills (no estate) | 442 | 350 | 500 | mills | GAPKI Sep 2026 | M |
| Average mill capacity | 50 | 45 | 57 | t FFB/h | Kaltim 57; Astra 49 | M/EST |
| Installed capacity | 65,000 | 55,000 | 75,000 | t FFB/h | EST = mills x average | L |
| CPO 2024 / 2025 / 2026F | 48.16 / 51.66 / 52.5 | 45.4 / – / 51.2 | – / – / 54 | Mt | GAPKI; Kementan; Reuters poll | H/M |
| FFB processed | 250 | 240 | 260 | Mt/yr | BRIN/PASPI 2026; CPO/OER | M |
| POME factor | 0.65 | 0.50 | 0.70 | m3/t FFB | design basis; PASPI 0.5 | M |
| National POME | 150 | 125 | 170 | Mm3/yr | PASPI; derived | M |
| Biogas potential | 3.6 | 3.3 | 4.0 | bn m3/yr | PASPI 2026 | M |
| Technical power potential | 1,050 | 1,000 | 1,113 | MWe | ESDM via Gree; WBA; our check | M |
| Installed POME biogas | 165 | 130 | 165 | MW | GAPKI May 2026; WBA 2022 | M |
| PLTBg count (POME) | 84 | 78 | 90 | plants | GAPKI 2026; WBA | M |
| Grid-connected share | 53.7 | – | – | MW | GAPKI 2026 | M |
| Mills with capture | 11.5 | 9 | 15 | % | APEC; IOP; PASPI | M |
| Uncaptured mills | 1,150 | 1,050 | 1,250 | mills | derived | M |
| TAM (sets) | 900 | 774 | 1,015 | set-eq | derived | M |
| SAM (sets) | 470 | 405 | 530 | set-eq | derived | M/EST |
| SOM 2034 | 40 (plan) / 15–20 (cons.) | 15 | 40 | sets | finance ROLL; EST | EST |
| Revenue per set | 1.26 | – | – | USD M/yr | finance model | internal |
| Covered lagoon capex | 2.2 | 1.8 | 3.7 | USD M/MWe | APEC 2017; Energies 2022 | M |
| Tank/CSTR capex | 2.5 | 1.8 | 3.5 | USD M/MWe | TSE 2025; MDPI 2025 | M |
| Biomethane capex | 5.3 | 5.0 | 5.6 | USD M/mill | reNIKOLA 2026 | M |
| AnMBR/CAL capex ratio | 2.4 | 1.0 | 2.4 | x | AMPC | M |
| Our FCI per MWe gross | 4.98 | – | – | USD M/MWe | finance summary | internal |
| PLTBg excess-power tariff | 7.44 | 7.43 | 7.44 | USc/kWh | Perpres 112/2022 | M |
| Grid extension cost | 35 | 28 | 42 | kUSD/km | WBA 2022 | M |
| Malaysia mills | 453 | 447 | 453 | mills | MPOB 2025 | H |
| Malaysia capture share | 30 | 28 | 33 | % | MPOB POEB 148 (Dec 2024) | M |
| Malaysia POME potential | 508 | – | – | MWe | MPOB JOPR 2021 | M |

## COMPETITOR SCORING MATRIX (45 t FFB/h mill, ~1.1 MWe)

Values are sourced unless marked **EST**. Scores use 1 = poor and 5 = best for the mill.

| Option | Capex USD M/MWe | Land ha | Build months | COD removal % | Uptime % | Mill capex burden | Relocatable | Effluent quality | Odour / CH4 leak | Score /45 |
|---|---|---|---|---|---|---|---|---|---|---|
| Open ponds (do nothing) | 0 (sunk) [5] | 2.2 site; 1–5 lit. (up to 12–18) [1] | 0 [5] | 90–95 over 100+ d (CH4 released) [3] | n/a [3] | none [5] | N [1] | often fails BOD 100; land application [2] | high CH4 (137–163 kg CO2e/t FFB), odour [1] | 26 |
| Covered lagoon | 1.8–3.7 (base 2.2) [4] | 1.0–2.0 EST (Sei Mangkei 2 ha / 2.4 MW) [2] | 9–15 EST [3] | up to 91 [4] | 85–92 EST (scum, desludging, liner) [3] | high if owned; 0 under BOO [3] | N [1] | COD 3–5 g/L, needs polishing [2] | low; leaks at cover/edges [3] | 25 |
| CSTR / tank | 1.8–3.5 (TSE 1.8) [4] | 0.5–1.0 EST [3] | 12–24 (Sei Garo ~24) [2] | 80–95 [4] | 90–95 EST [4] | high [2] | N (bolted tanks partly) [2] | COD 2.5–5 g/L, needs polishing [3] | low [4] | 28 |
| UASB/EGSB/IC (+ pre-treatment) | 2–3.5 EST [3] | 0.2–0.5 EST [4] | 12–18 EST [3] | 80–90 soluble; clogging [3] | 85–90 EST [3] | high [2] | N [1] | moderate [3] | low [4] | 26 |
| Conventional AnMBR (Memthane/Kubota) | ~2.4x lagoon ≈ 5 EST [2] | 0.2–0.4 EST [4] | 12–18 EST [3] | 93–98 lab (POME) [5] | fouling risk; no POME ref, 90 EST [3] | high [2] | N [1] | TSS-free permeate, BOD <100 (non-POME) [5] | very low [5] | 30 |
| Biomethane / CBG (BOOT) | ≈4 per MWe-eq; US$5.3 M/mill [2] | 1–2 EST (digester + upgrading) [2] | 14 (Tinjowan) [3] | as digester, 80–91 [4] | 90–95 EST [4] | 0 (developer-funded) [5] | N [1] | as digester [2] | low; venting at upgrading [4] | 27 |
| EFB+POME co-composting | 1–2.5 per mill EST (no MWe) [3] | 2–4 EST [1] | 6–12 EST [4] | ~100 of absorbed fraction (no discharge) [4] | weather-dependent, 80 EST [3] | medium [3] | N [1] | zero discharge if fully absorbed [5] | ponds still emit unless upstream AD [2] | 26 |
| ZLD / evaporation / polishing | high; payback hurdle (no figure) [1] | 0.2–0.5 EST [4] | 12+ EST [3] | >99 (BOD <20) [5] | 85–90 EST [3] | very high [1] | N [1] | best [5] | no CH4 capture unless AD upstream [2] | 25 |
| **Ours: portable thermophilic AnMBR, BOO** | **4.98 gross / 5.64 net (internal) [2]** | **0.34 (3D GA) [5]** | **11 (plan) [4]** | **~90 (effluent ~4.8 g/L COD) [4]** | **97 CHP availability, assumption only [4]** | **0 capex, but pays a mill fee (~50% of revenue) [3]** | **Y (truckloads) [5]** | **TSS-free permeate, COD ~4.8 g/L, still needs polishing [3]** | **very low (closed vessels) [5]** | **35** |

- **Scoring caveat.** Our row uses design targets, not field data. If uptime is cut to 85–90% and the mill fee is scored as a burden [2], we drop to about 33, still first but only narrowly ahead of conventional AnMBR and CSTR.
- Our capex per MWe is the weakest cell: about 2x lagoon/tank benchmarks, and 2.8x the TSE Papua tank plant.

## USP EVIDENCE: which claims hold, which are weak (honest)

| Claimed USP | Verdict | Evidence / gap |
|---|---|---|
| **Small footprint (0.34 ha vs ~2.2 ha ponds)** | **Supported, but low buyer value at most mills** | 0.34 ha vs Sei Mangkei 2 ha for 2.4 MW, and 1–5 ha (lit.) for ponds. However, mills already own pond land, so land is rarely the binding constraint. It matters for land-locked, flood- or peat-prone sites, mills expanding throughput, and HGU/permit-constrained independents. Present it as "frees ~1–2 ha and removes pond liability", not as a primary reason to buy. |
| **Relocatable / portable** | **Novel but unproven demand (weak to moderate)** | No MW-scale relocatable POME digester exists, so there is no direct competitor. Containerised AD tops out at ~20 t/d (SEaB). Indirect support: 2x overcapacity (Trase), 442 independent mills with insecure FFB, mill churn (Rokan Hulu +105%). No source shows mills or lenders pricing relocation. The real value is **financier residual-value / collateral risk reduction** (WBA: lenders see AD as high risk). Quantify that in the finance model rather than asserting it. |
| **No mill capex (BOO)** | **Supported as a need, not unique** | Capex and payback (6.6–10.8 yr) are the top barriers. But reNIKOLA, KIS, Gree, AANE and Pertamina NRE all already offer developer-funded BOO/BOOT. Differentiate on target segment: independents and mid-size mills that biomethane players skip. |
| **Mill pays a fee** | **Weak / contrary to market norm** | Competitors take POME free and often share revenue. No tipping-fee precedent found in ID or MY. The fee is about 50% of our revenue, so this is the most attackable assumption. Mitigate by bundling (compliance + odour + ISCC/RED II market access + diesel displacement), or switch to revenue share plus power-at-discount. |
| **High COD removal / better effluent (thermophilic AnMBR)** | **Supported at lab scale; no full-scale POME proof** | Lab thermophilic AnMBR 93–98% COD; Memthane >98% BOD on food wastewater. Our design is ~90% with COD ~4.8 g/L, so a polishing pond is still needed. Do not claim "replaces all ponds". Fouling (organic 93% of fouling) is a known risk. |
| **Fast deployment (11 months)** | **Moderately supported** | Benchmarks: biomethane Tinjowan 14 months; PTPN IV Sei Garo ~24 months. Lagoon vendors claim faster for simple covers. Shop-fabricated modules plausibly shorten site work, but no field record. |
| **High uptime (97%)** | **Weak (assumption)** | No field data. Membranes add a failure mode; lagoons and tanks have documented scum, sludge and VFA upsets. Present 93–97% as a range with a membrane-cleaning schedule. |
| **Lower methane leakage / odour** | **Supported vs ponds; partial vs covered lagoon** | Closed steel vessels avoid cover-edge leaks and scum-related damage (MLA). Quantified leak rates for Indonesian lagoons not found. |
| **Cost-competitive** | **Not supported** | USD ~5.0 M/MWe gross vs 1.8–3.7 for lagoon/tank (TSE 1.8). Learning-curve and fleet economics (finance model) must close the gap, or the pitch must rest on fee-free alternatives being unavailable to the target segment. |

**Bottom line.**
- **Strongest defensible positioning:** a developer-funded, redeployable methane-capture asset for **independent and mid-size (30–60 t/h) mills that biomethane clusters and group in-house programmes do not serve**. Its value is that the financier's asset is not stranded if the mill closes.
- **Weakest points:** capex per MWe (about 2x incumbents) and the mill-fee assumption. Address both in the pitch.
