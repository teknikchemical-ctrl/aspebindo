# R1 — Regulatory & Carbon Evidence for a Thermophilic AnMBR POME Biogas BOO Project

**Project context:** 45 t FFB/h mill, ~585 m3/d POME, COD ~50 g/L, ~1.09 MWe gross, BOO structure, ~32,000 tCO2e/yr methane-avoidance credits claimed (10-yr crediting, USD 5/t base).
**Research date:** 2026-10-16.

**Method and limits:** All evidence comes from web searches run on 2026-10-16. Direct page fetches (WebFetch, curl) were blocked by the sandbox for most hosts (DNS/403), including rspo.org, kemenlh.go.id, bi.go.id and ecobiz.asia. Many claims therefore rest on search-engine extracts of the cited page, not a full read of the document. The search budget ran out before four checks could be done: the Malaysia MPOB rule, the ISPO GHG indicators, the ICVCM status of wastewater methodologies, and the exact RSPO 2024 GHG indicator text. These are marked **UNVERIFIED**. Items marked "[from primary text, not re-fetched]" are well-established values from the named primary document that I could not re-open this session.

**Confidence scale:**
- **High:** primary source, or several consistent sources.
- **Med:** a single reputable secondary source, or a primary source seen only as a snippet.
- **Low:** an unclear or conflicting source.

---

## 1. Indonesian POME effluent standards, land application, permits, sanctions, enforcement

### 1.1 Discharge standard: PermenLH 5/2014, Lampiran III (palm oil industry)

- **BOD5 100 mg/L (0.25 kg/t CPO); COD 350 mg/L (0.88 kg/t); TSS 250 mg/L (0.63 kg/t); oil & grease 25 mg/L (0.063 kg/t); total N (as N) 50 mg/L (0.125 kg/t); pH 6.0–9.0** — Permen LH No. 5/2014 Lampiran III (BPK JDIH, set 15-Oct-2014, effective 25-Nov-2014, https://peraturan.bpk.go.id/Download/384240/Permen%20LH%20No%205%20Tahun%202014.pdf ; record https://peraturan.bpk.go.id/Details/322442) [High]
- **Maximum wastewater volume: 2.5 m3 per tonne CPO.** The OCR of the official text prints "m2", but secondary tables give m3, which is the intended unit — same BPK PDF; karbonaktif.org table (Jul-2023, https://www.karbonaktif.org/2023/07/permen-baku-mutu-air-limbah-industri.html) [High on the value, Med on the unit text]
  - *Model check (my calculation):* 585 m3/d of POME from about 900 t FFB/d at about 21% OER gives about 189 t CPO/d, which is **about 3.1 m3 POME per t CPO**. That is already above the 2.5 m3/t discharge quota. A mill that discharges to a river must reuse or land-apply the excess, which in turn requires a technical approval (Persetujuan Teknis).
- **Status of the regulation:** PermenLH 5/2014 was amended by PermenLHK 16/2019. Its textile and domestic annexes were replaced in 2025: textile by Permen LH/BPLH 12/2025 and domestic by Permen LH/BPLH 11/2025 (effective 9-Sep-2025). Animal feed got a new standard in 2026 (Permen LH/BPLH 2/2026, effective 26-Feb-2026). **No palm-oil-specific replacement was found as of Oct-2026**, so Lampiran III is presumed still in force — BPK JDIH (https://peraturan.bpk.go.id/Details/345623/permen-lhbplh-no-12-tahun-2025 ; https://peraturan.bpk.go.id/Details/286527/permen-lhk-no-16-tahun-2019 ; https://peraturan.bpk.go.id/Details/347119/permen-lhbplh-no-2-tahun-2026) [Med]
  - **Risk:** KLH/BPLH is reissuing sector standards one by one under the new "baku mutu + standar teknologi" format. A palm-oil revision could tighten the limits, which would help our case, or prescribe a technology.

### 1.2 Land application ("aplikasi lahan") and permits

- **Land-applied POME must have BOD ≤ 5,000 mg/L and pH 6–9.** These limits come from KepMenLH 28/2003 (technical guidance) and KepMenLH 29/2003 (permit requirements and procedure) — Kepmen LH 29/2003 text (toolsfortransformation mirror, https://indonesia.toolsfortransformation.net/wp-content/uploads/2017/05/Kepmen-LH-No.-29-Tahun-2003-tentang-Pemanfaatan-Limbah-Kelapa-Sawit.pdf); Unpad Soilrens paper (https://journals.unpad.ac.id/soilrens/article/download/45267/19386) [High on the limits]
- **Peat and sandy soils** are not recommended for land application. This is cited as field practice, not confirmed as regulation text — same academic sources [Low]
- **PermenLHK 5/2021 (Persetujuan Teknis and SLO for wastewater and emissions)** requires any business that discharges *or uses* wastewater, land application included, to hold a technical approval (Persetujuan Teknis) and an operational fitness certificate (SLO) (Art. 3(1)). Industry press reports that the regulation **implicitly revoked KepMenLH 28 & 29/2003**. That left no explicit technical land-application standard, and experts (e.g., Prof. Yanto Santosa, IPB) have called for a revision — InfoSAWIT (30-Dec-2022, https://www.infosawit.com/2022/12/30/dampak-permen-lhk-nomor-5-tahun-2021-terhadap-perusahaan-sawit/); Antara Gorontalo (https://gorontalo.antaranews.com/berita/282977/pemerintah-diminta-revisi-permen-lhk-no-5-tahun-2021/) [Med]
  - In practice, permitting authorities still apply the 5,000 mg/L BOD benchmark [Med]
  - I could not confirm whether PermenLHK 5/2021 was revised in 2025–26 [**UNVERIFIED**]
- **PP 22/2021 (environmental protection and management)** is the umbrella regulation. It folds wastewater permits into the environmental approval (Persetujuan Lingkungan) via the technical approval, and it sets the administrative sanctions: written warning, government coercion (paksaan pemerintah), administrative fine, suspension, and revocation — BPK JDIH PP 22/2021 (https://peraturan.bpk.go.id/Details/161852/pp-no-22-tahun-2021) [High on the structure; from primary text, not re-fetched. I could not verify the exact article on fine amounts]

### 1.3 Sanctions under UU 32/2009 as amended by Cipta Kerja (UU 6/2023)

- **Art. 98 (intentionally causing water quality standards to be exceeded): 3–10 years in prison and Rp 3–10 billion fine.** Corporate penalties are aggravated, and additional penalties include confiscation of profits and remediation — UU 32/2009 (https://peraturan.bpk.go.id/Details/38771/uu-no-32-tahun-2009); cited in the BMB case by InfoSAWIT (4-Apr-2024, https://www.infosawit.com/2024/04/04/perusahaan-sawit-bmb-terancam-hukuman-denda-rp-10-miliar-diduga-cemari-lingkungan/) [High]
- **Art. 100 (violating wastewater quality standards): up to 3 years and Rp 3 billion**, but only as a last resort (*ultimum remedium*). Criminal penalties apply only if administrative sanctions are ignored or the violation is repeated — Warmadewa law journal (https://ejournal.warmadewa.ac.id/index.php/analogihukum/article/download/10284/5886) [Med]
- **Art. 104 (dumping without a permit): up to 3 years and Rp 3 billion** [Med]

### 1.4 Real enforcement cases (POME)

- **PT SIPP (Bengkalis, Riau).** Charged with dumping POME without a permit and running a non-compliant treatment plant (IPAL).
  - Prosecutors sought 7 years and a Rp 4 bn fine for the Director (Aug-2023).
  - PN Bengkalis (Oct-2023) gave 1 year, suspended, plus Rp 200 m.
  - PT Pekanbaru (Jan-2024) made it 1 year actual prison, Rp 200 m, and **Rp 250 m remediation**.
  - **Supreme Court cassation (28-Nov-2024): 3 years and Rp 100 m each for the Director and the GM.**
  - Sources: Sabang Merauke News (https://www.sabangmeraukenews.com/berita/15801/... ; https://www.sabangmeraukenews.com/berita/25432/...); GoRiau (https://www.goriau.com/berita/baca/sukses-kawal-kasus-limbah-pt-sipp-hingga-putusan-kasasi-ma-dr-marnalom-hutahaean-ini-kemenangan-masyarakat.html); Antara (https://www.antaranews.com/berita/3142541/klhk-rencanakan-pidana-tambahan-pt-sipp-untuk-pemulihan-lingkungan) [Med; the cassation fine amount differs between sources]
- **PT Berkala Maju Bersama (Gunung Mas, Central Kalimantan).** POME flowed into the Masien River and killed fish.
  - The regent sealed or halted the mill on 19-Jun-2023.
  - The Gakkum case file was declared complete (P-21) on 14-Mar-2024, with exposure of Rp 3–10 bn and 3–10 years.
  - **The PN Palangka Raya pretrial ruling 12/Pid.Pra/2024 (24-Apr-2024) annulled the corporate suspect status.** No trial verdict was found.
  - Sources: Betahita (https://www.betahita.id/berita/10075/berkas-kasus-pencemaran-limbah-sawit-gunung-mas-siap-disidangkan); Medius News (https://www.mediusnews.com/regional/13212513075/pn-palangka-raya-batalkan-penetapan-tersangka-korporasi-pt-bmb); Cyrustimes [Med]
- **Other cases:** Repeated complaints were filed with KLHK over POME pollution of the Krueng Trang river in Nagan Raya, Aceh (31-May-2024 and Aug-2023), with no outcome found — Antara Aceh (https://aceh.antaranews.com/berita/360624/...) [Med]. Further community complaints in Sekadau and Paser (2025–26) come from local media [Low].
- **Takeaway:** Enforcement is real but slow and inconsistent. Final fines are small (Rp 0.1–0.25 bn); the larger costs are **prison for directors, mill closure orders, and remediation**. The stronger selling point for compliance is avoiding a shutdown, not avoiding fines.

---

## 2. PROPER (company environmental performance rating)

- **Rating levels:**
  - Gold and Green: "beyond compliance", earned through energy efficiency, emission reduction, water efficiency, 3R, and community development.
  - Blue: compliant.
  - Red: effort made but not compliant.
  - Black: caused pollution or damage, or a serious violation.
  - Sources: KLH press release (Jun-2025, https://kemenlh.go.id/news/detail/proper-2024-2025-menteri-lh-tegaskan-lompatan-transformasi-industri-berkelas-dunia); environment-indonesia.com [High]
- **PROPER 2024–2025: 5,476 companies assessed (+22%), of which 39 Gold and 243 Green (282 beyond compliance).** Most were rated Blue; the Red and Black counts were not published in the extract — KLH (https://kemenlh.go.id/news/detail/5476-perusahaan-dipantau-lewat-proper-2025-...); Ecobiz Asia (https://ecobiz.asia/beyond-compliance-282-perusahaan-raih-peringkat-emas-dan-hijau-proper-2025/) [High]
- **PROPER 2023–2024: 85 Gold, 227 Green, 2,649 Blue, 1,313 Red, 16 Black** — Forest Insights (https://forestinsights.id/patuhi-pengelolaan-lingkungan-85-perusahaan-raih-proper-emas/) [Med]
- **Regulatory basis:** PROPER now runs under **PermenLH/BPLH 7/2025**, which appears to supersede PermenLHK 1/2021. Kepmen 1375/2025 contains palm-oil-specific wastewater monitoring rules: POME discharged to a water body is monitored against the strictest applicable standard — proper.menlhk.go.id; ecoverse.id copy of Kepmen 1375/2025 (https://ecoverse.id/wp-content/uploads/2025/07/Kepmen-1375-Tahun-2025-Tentang-PROPER.pdf) [Med]
- **How methane capture affects the rating:** Green and Gold require beyond-compliance performance in energy efficiency and emission reduction, among other areas. Recorded GHG reductions and renewable energy count toward this, and captured POME biogas that replaces diesel or grid power fits directly. However, I could not confirm the exact scoring weight of methane capture within the PROPER criteria [Med on direction, **UNVERIFIED** on weight]
- **Consequences of a Red or Black rating:**
  - Reputational damage (the ratings are published).
  - A trigger for Gakkum follow-up.
  - Bank credit: Bank Indonesia's asset-quality rule PBI 7/2/PBI/2005 (later PBI 14/15/2012) required banks to consider a debtor's environmental-management efforts when assessing business prospects, and PROPER was the usual reference. I could not re-open the text this session — BI/OJK regulation pages (https://ojk.go.id/id/regulasi/Pages/PBI-tentang-Penilaian-Kualitas-Aset-Bank-Umum.aspx) [Low–Med]
  - Since POJK 51/2017 (sustainable finance), banks also screen environmental, social and governance (ESG) risks [Med, not re-verified]

---

## 3. ISPO (Indonesian Sustainable Palm Oil certification)

- **Perpres 16/2025** was signed on 19-Mar-2025 and **replaces Perpres 44/2020**. It extends mandatory ISPO beyond plantations and mills to **downstream industries (cooking oil, oleochemicals, etc.) and bioenergy (biofuel, biomass, *biogas*)**. **Deadline for downstream and bioenergy: about 19/20-Mar-2027** (2 years after enactment). Smallholders get 4 years (about 2029). Plantation companies are mandatory immediately — InfoSAWIT (12-May-2025, https://www.infosawit.com/2025/05/12/ispo-kini-wajib-untuk-industri-hilir-dan-bioenergi-petani-swadaya-didorong-dapat-insentif/); Bisnis (22-Apr-2025, https://ekonomi.bisnis.com/read/20250422/12/1871013/prabowo-teken-perpres-sertifikasi-sawit-berkelanjutan-ini-isinya); InfoSAWIT EN (https://en.infosawit.com/news/16012/...) [High on scope, Med on the exact date: 19 vs 20 March]
- **Sanctions (Art. 5):** written warning, administrative fine, temporary suspension, and up to licence revocation. A sanction is lifted only once certification is obtained — elaeis.co (https://www.elaeis.co/berita/baca/perpres-16-2025-wajibkan-sertifikasi-ispo-untuk-semua-rantai-usaha-sawit); SIP Law Firm (https://siplawfirm.id/id/publikasi/sertifikasi-ispo-bioenergi-sawit) [Med]
- **Implementing ministries:** Kementan (lead); Kemenperin sets downstream criteria and ESDM sets bioenergy criteria; certifiers are accredited by KAN, the national accreditation body — Kontan (https://industri.kontan.co.id/news/perkuat-pengelolaan-kelapa-sawit-pemerintah-dorong-sertifikasi-ispo-hulu-hilir) [Med]
- **Permentan 38/2020** (set 16-Nov-2020, promulgated 24-Nov-2020) holds the ISPO principles and criteria. Kementan has said it will revise it to align with Perpres 16/2025 — BPK JDIH (https://peraturan.bpk.go.id/Details/201269/permentan-no-38-tahun-2020); Antara (https://www.antaranews.com/berita/3984402/kementan-siap-merevisi-permentan-38-2020-setelah-perpres-ispo-terbit) [High]
  - I could not confirm whether the revised Permentan has been issued as of Oct-2026 [**UNVERIFIED**]
- **GHG and methane in ISPO:** ISPO has a GHG mitigation principle. Mills must **identify, inventory and report** GHG sources, with reduction efforts. ISPO **does not mandate methane capture**; an earlier plan (around 2015–2017) to require capture at certain mills from 2020 was not adopted as a hard rule — APEC EWG report (Mar-2017, https://www.apec.org/docs/default-source/Publications/2017/3/...); Madani (2022, https://madaniberkelanjutan.id/wp-content/uploads/2022/07/Madani-Update-Permentan-ISPO-Final_compressed.pdf) [Med; the exact 2020 indicator text is **UNVERIFIED**]
- **No mandatory methane-capture regulation as of Oct-2026.** PASPI and GAPKI (Sep-2026) are still *proposing* mandatory capture, carbon credits for POME projects, and biogas blending. ESDM says the implementing framework "has yet to be issued" — GAPKI (16-Sep-2026, https://gapki.id/en/news/2026/09/16/ri-potential-to-become-global-leader-in-pome-based-biogas/); energynews.pro (Aug-2026, https://energynews.pro/en/indonesia-weighs-turning-palm-oil-mill-effluent-into-biogas) [Med–High]
- **Implication:** Because capture is voluntary, the project remains additional for carbon credits. If capture becomes mandatory, that additionality and the credit revenue could be lost.

---

## 4. RSPO, ISCC, CORSIA, price premiums, POME oil

### 4.1 RSPO

- **P&C 2018, Criterion 7.10:** "Plans to reduce pollution and emissions, including GHG, are developed, implemented and monitored." **Indicator 7.10.1 (Critical):** GHG emissions are identified and assessed using **PalmGHG** and reported publicly. New developments are designed to minimise GHG (Criterion 7.8 and the separate New Development GHG Assessment Procedure). Methane capture is **promoted as the main mill-level mitigation measure but is not an explicit mandatory indicator** — RSPO P&C 2018 (15-Nov-2018, https://rspo.org/wp-content/uploads/rspo-principles-and-criteria-2018-approved-15-november-2018-english.pdf); RSPO BMP compilation (https://rspo.org/wp-content/uploads/RSPO-Compilation-of-Best-Management-Practices-to-Reduce-Total-Emission-from-Palm-Oil-Production-English.pdf) [High]
- **P&C 2024 (v4.0) was adopted on 13-Nov-2024** (updated 19-Sep-2025 and Jul-2025 v4.1). It requires POME to be treated in line with national rules and discharge quantity and quality, especially BOD, to be monitored. The Indonesia National Interpretation of the 2024 P&C was endorsed on 17-Mar-2026 — RSPO (https://rspo.org/wp-content/uploads/Consolidated-PC-2024_Adopted_13112024.pdf ; https://rspo.org/wp-content/uploads/ENG-Indonesia-National-Interpretation-of-2024-RSPO-Principles-and-Criteria_17032026_s.pdf) [High on the dates; the exact 2024 GHG/methane indicator wording is **UNVERIFIED** (fetch blocked)]
- **PalmGHG pilot (2011, 9 companies): average 1.67 tCO2e/t CPO (range −0.02 to 8.32). POME methane = 15–35% of emissions; land clearing = 41–80%** — Bessou et al., PalmGHG paper (https://agritrop.cirad.fr/580308/1/Bessou.paper.ICOPE2016.pdf ; https://www.sciencedirect.com/science/article/abs/pii/S0959652613008627) [High, but the data are old]
- **RSPO credits (book & claim) have slumped to about USD 2/t**, down from about USD 40/t at their peak. Earlier studies (2019) put the book-and-claim premium at USD 2.5–3.5/t, and mass-balance or segregated premiums at 1–7% of the base price — Eco-Business (date uncertain, ~2024–25, https://www.eco-business.com/news/new-sustainable-palm-oil-rules-win-consensus-amid-rspo-credit-price-slump/); WWF business case (https://wwfint.awsassets.panda.org/downloads/full_report___business_case_for_certified_sustainable_palm_oil.pdf) [Med]

### 4.2 ISCC EU / RED II–III

- **EU RED II minimum GHG saving for biofuels: 50% (pre-Oct-2015 plants), 60%, and 65% for new plants. The default value for palm biodiesel with an *open effluent pond* gives only about 20% saving**, so it **cannot be used**. A mill must either use the "methane capture" default or calculate actual values. The capture default applies only if mill CH4 is **< 5.46 kg CH4/t CPO** — ISCC EU 205 GHG v4.1 (Jan-2024, https://www.iscc-system.org/wp-content/uploads/2024/01/ISCC_EU_205_Greenhouse-Gas-Emissions_v4.1_January2024.pdf); ISCC 205 v3.0 [High]
  - In effect, palm oil from mills **without methane capture cannot qualify as an EU-compliant biofuel feedstock** under default values. This is a real market lever for our product.
- **POME oil** (oil recovered from the effluent) is classed as a residue under RED Annex IX, carries **zero upstream emissions**, and has no RED default value. Since 2022, every mill supplying POME oil under ISCC must be individually certified and audited on site each year — ISCC guidance on palm-mill wastes and residues v3.1 (Dec-2023, https://www.iscc-system.org/wp-content/uploads/2023/12/ISCC_Guidance_WR_from_Palm_Oil_Mills_V3.1.pdf); ISCC news (https://www.iscc-system.org/news/understanding-pome-context-and-controversy/) [High]
- **POME oil price was close to CPO by mid/late 2024:** about 90% of the CPO price, and about USD 1,010/t CIF ARA (Rotterdam area) vs BMD CPO at USD 1,000–1,010. T&E estimates palm residues may have made up **about a quarter of EU HVO feedstock in 2023** and raises fraud concerns. Indonesia raised export levies on POME and UCO in Sep-2024 — Transport & Environment (Mar-2025, https://www.transportenvironment.org/uploads/files/202504_POME_fraud_Report.pdf); Vesper (Oct-2024, https://vespertool.com/news/pome-market-update/); QCIntel (https://www.qcintel.com/biofuels/article/indonesia-s-cpo-export-levy-hike-proposal-for-2026-to-hit-pome-uco-sources-51248.html) [Med]
  - Relevance: an AnMBR upstream oil trap or sludge-oil recovery could produce a small POME-oil co-product, but the policy and fraud-scrutiny risk is high.
- **"Low-GHG CPO" premium (USD/t):** **not found** in any 2025–26 source. No price-reporting agency figure was retrievable [**UNVERIFIED** — do not model a premium]
- **CPO reference price, Oct-2026: about USD 1,042/t** (Indonesian HRE reference); Rotterdam CPO about USD 1,570/t (15-Oct-2026) — IDN Financials (https://www.idnfinancials.com/news/69778/...); Palm Oil Magazine (16-Oct-2026, https://palmoilmagazine.com/cpo-price/2026/10/16/...) [Med]

### 4.3 CORSIA (international aviation offsetting)

- **First phase (2024–2026):** Verra VCS and Gold Standard are approved programmes, but units need a **host-country Letter of Authorization (LoA) and a corresponding adjustment**. Sources disagree on supply: about 10 countries supplying via LoA (IATA, Apr-2026) versus about 42 LoAs covering about 72 m units (Aug-2026). Phase-1 demand is estimated at 146–236 m units, and the retirement deadline is **31-Jan-2028** — Carbon Direct (https://www.carbon-direct.com/insights/corsia-phase-1-credits-compliance-and-what-comes-next); greenfueljournal (https://www.greenfueljournal.com/post/corsia-eligible-emissions-units-2026-2028); ICAO (https://www.icao.int/news/icao-expands-approved-emissions-unit-programmes-effective-corsia-implementation) [Med]
- **CORSIA unit price: no official price.** The ICAO 2025 periodic review estimated USD 10–40/t; a planning marker of about USD 20–25 is cited — theplanetbrief (https://theplanetbrief.com/carbon/corsia/credit-prices/) [Low–Med]
  - Indonesia's authorization pathway is set out under Perpres 110/2025 (see §5). Whether a POME project would get an LoA is uncertain.

---

## 5. Government biogas/methane policy and carbon pricing

### 5.1 Biogas and bioenergy targets and installed capacity

- **Installed biogas power (PLTBg), all feedstocks: 155.84 MW (Oct-2024); 164.10 MW (EBTKE homepage, status Apr-2026).** Total bioenergy power was about 3,138 MW (Sep-2025) — ESDM (https://www.esdm.go.id/id/media-center/arsip-berita/semester-i-2024-kapasitas-terpasang-ebt-bertambah-2177-mw); EBTKE (https://ebtke.esdm.go.id/); EBTKE Technopex slides (16-Oct-2025, https://semnas.iti.ac.id/wp-content/uploads/2025/10/251016-SDE-Technopex-R1-Potensi-ET-untuk-Ekonomi-Hijau_compressed.pdf) [Med–High]
- **The old national energy plan (RUEN) target of 5.5 GW of PLTBg by 2025 was badly missed** (about 1.3% achieved in 2020) — Kompas (6-Jul-2020, https://nasional.kompas.com/read/2020/07/06/18455311/...) [High]
- **POME potential:** about 125 Mt POME/yr could yield about 3.6 bn m3 biogas/yr (PASPI), with about 15% currently used — bioenergy-news / investortrust (Aug-2026, https://www.bioenergy-news.com/news/indonesias-palm-oil-waste-could-generate-3-6-billion-cubic-metres-of-biogas-annually/) [Med]
  - ESDM rule of thumb: a 30 t FFB/h mill supports about 1 MW of POME biogas power (https://www.esdm.go.id/id/berita-unit/direktorat-jenderal-ebtke/strategi-pengembangan-biogas-kejar-target-bauran-energi) [Med]
  - By that rule a 45 t/h mill supports about 1.5 MW, so our 1.09 MWe gross is plausible.
- **RUPTL 2025–2034 (PLN's 10-year power supply plan): 69.5 GW of additions, of which bioenergy is only about 0.9 GW** (solar 17.1, hydro 11.7, wind 7.2, geothermal 5.2). No separate biogas line was found; ESDM says POME biogas "will be reflected" in the RUPTL — RMOL (26-May-2025, https://rmol.id/amp/2025/05/26/667818/...); ESDM RUPTL slides (https://gatrik.esdm.go.id/assets/uploads/download_index/files/4ec39-materi-paparan-ruptl-2025-2034.pdf); CREA (Sep-2025) [High]
- **PLN ceiling tariff for biogas (Perpres 112/2022, Lampiran I).** For years 1–10 the price is multiplied by a location factor F, but the regulation states that F does not apply to biomass or biogas; years 11–30 have no F:
  - ≤1 MW: 11.47 ¢/kWh (years 1–10) and 6.88 ¢/kWh (years 11–30)
  - 1–3 MW: 9.94 ¢/kWh and 5.97 ¢/kWh
  - 3–5 MW: 8.77 ¢/kWh and 5.26 ¢/kWh
  - These figures come from an OCR of the official annex (Stockbit mirror, https://stream-asset.stockbit.com/666bead2-8e72-4e2a-8586-30f783dad49b_stream.pdf ; official https://jdih.kemenkeu.go.id/api/download/7332a343-0623-4d26-80f2-9d8f62a5c2ba/2022perpres112.pdf) [Med]
  - Media versions differ: Katadata gives 10.18, 9.81 and 8.99 ¢ [Low]
  - **Use the annex values, with sensitivity at about 9–10 ¢/kWh.**
- **Biomethane** for PGN's gas pipelines and Toyota Tsusho/KBI (target 2027) is emerging as a rival use of POME biogas — Palm Oil Magazine (13-Oct-2026, https://www.palmoilmagazine.com/energy/2026/10/13/pgn-to-integrate-palm-oil-waste-derived-biomethane-into-indonesias-gas-network/) [Med]
- **KLH plans a "super-pollutant" (methane and black carbon) unit, operating from 2027** — Ecobiz Asia (Oct-2026, https://ecobiz.asia/indonesia-plans-special-unit-to-tackle-methane-black-carbon-emissions-by-2027/) [Med]

### 5.2 NDC (national climate pledge) and methane

- **Enhanced NDC (23-Sep-2022): 31.89% unconditional and 43.20% conditional reduction vs BAU by 2030.** It includes a measure for **industrial wastewater methane capture (palm oil, pulp, food)**, raising its target from 3 Mt to **26 MtCO2e (about 1.2 Mt CH4 recovered)** — UNFCCC (https://unfccc.int/sites/default/files/NDC/2022-09/23.09.2022_Enhanced%20NDC%20Indonesia.pdf) [High]
- **Second NDC (2025):** a POME-specific target was **not confirmed** [**UNVERIFIED**]

### 5.3 Carbon pricing framework

- **Perpres 110/2025** (promulgated 10-Oct-2025) on the carbon-pricing instrument (Nilai Ekonomi Karbon) and national GHG control **revokes Perpres 98/2021**. It provides four instruments: carbon trading, results-based payment, carbon levy, and others. A steering committee is chaired by the Coordinating Minister for Food. It introduces carbon allocations and sets rules for authorised (corresponding-adjustment) and voluntary-use units — BPK JDIH (https://peraturan.bpk.go.id/Details/334733/perpres-no-110-tahun-2025); SSEK (https://ssek.com/blog/indonesia-introduces-new-carbon-trading-framework-under-presidential-regulation-no-110-of-2025/) [High]
- **SRUK (carbon unit registry):** **PermenLH 10/2026** (signed 2-Jul-2026) sets up the carbon-unit registry, which launched about 9-Jul-2026. SRUK records unit issuance, transfer and retirement, while the older SRN-PPI keeps recording mitigation and adaptation actions in parallel — SRUK portal (https://srukindonesia.kemenlh.go.id/about); TruCarbon (https://www.trucarbon.co/sruk-carbon-unit-registry-explained) [Med–High]
- **POJK 14/2023** (carbon exchange rules) was **amended by POJK 10/2026** (set 2-Jul-2026, promulgated 6-Jul-2026) to align with Perpres 110. Units traded must be recorded in SRUK, with a 3-month transition allowing units held in ministry systems. Foreign units need validation and verification by an internationally recognised body — OJK abstract (https://www.ojk.go.id/id/regulasi/Documents/Pages/POJK-10-Tahun-2026-...); Kompas (21-May-2026) [High]
- **Mutual recognition agreements (MRAs):** with Gold Standard (May-2025, excludes REDD+; projects must register in the national registry first) and with **Verra (3-Oct-2025)**, allowing dual registration and Article 6 authorization. Units for voluntary use may still need Ministry of Environment approval. Verra's first issuances under the new rules were forestry projects (Jul-2026, ≥20 MtCO2e expected) — Verra (https://verra.org/verra-and-indonesia-sign-milestone-agreement-to-advance-carbon-markets/ ; https://verra.org/verra-to-issue-first-credits-under-indonesias-new-carbon-market-regulations/); SSEK [High]
- **Carbon tax** (UU 7/2021, about Rp 30,000 ≈ USD 2/tCO2e, coal power first) is **still not in force**. It has been deferred repeatedly, and the Ministry of Finance has signalled it is not a 2026 budget priority — IISD policy brief (Mar-2026, https://www.iisd.org/system/files/2026-03/carbon-pricing-southeast-asia.pdf); baliaccountants (2026) [Med–High]

### 5.4 IDXCarbon prices and volumes (2023–2026)

- **Cumulative since launch (26-Sep-2023): about 1.6 MtCO2e and Rp 80.75 bn (to 24-Dec-2025); 1.98 MtCO2e and Rp 93.97 bn (to 30-Sep-2026); 160 users.** Implied average about Rp 47,000/t ≈ USD 2.9/t — OJK via periskop.id (13-Oct-2026, https://periskop.id/pasar-modal/20261013/pasar-karbon-ri-baru-rp94-miliar-...); Investortrust [High]
- **2025 volume about 0.90 MtCO2e and Rp 36.4 bn across 213 trades** (implied about Rp 40,200/t ≈ USD 2.5) — DJPb Kemenkeu (https://djpb.kemenkeu.go.id/kppn/bengkulu/id/data-publikasi/artikel/2931-carbon-trading.html) [Med]
  - Q1-2025 alone was 690,675 t — Antara (https://www.antaranews.com/berita/4783493/...) [High]
- **2026 volumes are thin:** Jan-2026 was 117,455 t and Rp 4.7 bn (≈ Rp 40,000/t); Feb-2026 was only 2,218 t — KabarBursa (https://www.kabarbursa.com/carbon-trading/perdagangan-karbon-indonesia-januari-2026-turun-nilai-transaksi-rp47-miliar); IDXCarbon monthly report Feb-2026 (https://www.idxcarbon.co.id/document/share/161/caf49365-34e4-4582-8cd3-bb660ebb126c) [Med]
- **Unit prices:**
  - International launch (20-Jan-2025): IDTBS Rp 96,000 and IDTBS-RE Rp 144,000/t.
  - Jul-2025 (OJK): IDTBS **Rp 58,800 (≈ USD 3.6)** and IDTBS-RE **Rp 61,000 (≈ USD 3.7)**.
  - Sources: Tempo (https://www.tempo.co/ekonomi/ri-resmi-luncurkan-perdagangan-karbon-internasional-harga-rp-96-ribu-dan-rp-144-ribu-per-ton-1196430); Mongabay ID (23-Mar-2025) [High]

---

## 6. Carbon methodology for POME methane avoidance

### 6.1 Methodologies

- **CDM AMS-III.H "Methane recovery in wastewater treatment" v19.0** (valid from 14-Jun-2019; clarification 2023) covers small-scale projects. Projects above about 60 ktCO2e/yr use **ACM0014 "Treatment of wastewater" v8.0** — UNFCCC CDM (https://cdm.unfccc.int/methodologies/DB/0VAXUEJCAFN54BBE98CARMZU2TPMPJ/) [High]
  - Both can be used under Verra VCS. Under the Verra–Indonesia MRA, a CDM-transition or new VCS route via SRUK is possible.
- **ICVCM CCP (core carbon principles) status:** AMS-III.H was "under assessment" (Project Developer Forum letter, May-2024). The ICVCM has approved landfill-gas methodologies (ACM0001, AMS-III.G, Verra VMR0016) but **no CCP approval for wastewater methane (AMS-III.H or ACM0014) was found** — ICVCM (https://icvcm.org/wp-content/uploads/2025/09/240522-PD-Forum-letter-to-IC-VCM-re-CCP-eligible-meths-1.pdf); Verra (https://verra.org/verras-rice-cultivation-and-landfill-gas-methodologies-receive-icvcm-approval/) [Med; current status **UNVERIFIED**]

### 6.2 Key parameters

- **Baseline methane conversion factor (MCF) for a deep anaerobic lagoon (>2 m): 0.8 (range 0.8–1.0); for a shallow lagoon (<2 m): 0.2 (range 0–0.3)** — IPCC 2006 GL Vol.5 Ch.6 Table 6.3 (https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_6_Ch6_Wastewater.pdf); unchanged in 2019 Refinement Table 6.3 (https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_6_Ch06_Wastewater.pdf). AMS-III.H Table III.H.1 uses the 0.8 lower value (CDM SSC WG doc, https://cdm.unfccc.int/sunsetcms/storage/contents/stored-file-20160525193002357/SSCWG48_A11_AMS-III%20H.pdf) [High; IPCC values from primary text, not re-fetched]
- **Maximum methane capacity (Bo): 0.25 kg CH4/kg COD** — IPCC 2006 Vol.5 Ch.6 (default, same URL) [High; from primary text, not re-fetched]
- **Model uncertainty (conservativeness) factor in AMS-III.H: 0.89** for baseline lagoon emissions [Med; from methodology text, not re-fetched]
- **GWP for CH4:**
  - CDM 2008–12 used 21 (AR2); CDM 2013–20 used 25 (AR4).
  - **Paris Agreement transparency and Article 6 use AR5 = 28** (Decision 18/CMA.1, https://unfccc.int/sites/default/files/resource/cma2018_3_add2_new_advance.pdf).
  - AR6 = 27.9 (non-fossil CH4 27.0).
  - Verra moved to AR5 values in VCS v4.x — Verra (https://verra.org/verra-releases-version-4-5-of-the-vcs-standard/) [High on 28/27.9; Med on the Verra effective date]
  - **Use 28 in the model**, and note that credits from older CDM projects were computed at 21, which understates them by about 25% versus today.

### 6.3 Registered Indonesian CDM POME projects (annual emission reductions in the PDD, mostly GWP 21)

| Project | Methodology | ER (tCO2e/yr) | Source |
|---|---|---|---|
| PT Musim Mas, Pangkalan Lesung, Riau (reg. 2013) | AMS-III.H v16 | 52,397 | https://cdm.unfccc.int/Projects/DB/DNV-CUK1297330109.8/view [High] |
| PT Unggul Lestari, Central Kalimantan | AMS-III.H | 52,781 | https://cdm.unfccc.int/Projects/DB/DNV-CUK1342676421.56/view [High] |
| PT Umbul Mas Wisesa | AMS-III.H | 57,640 | https://cdm.unfccc.int/Projects/DB/SIRIM1356491158.66/view [High] |
| PT Golden Blossom Sumatra | AMS-III.H | 21,675 | https://cdm.unfccc.int/Projects/DB/TUEV-RHEIN1348556880.63/view [High] |
| PT Pinago Utama Sugihwaras (validation) | AMS-III.H v10 | 52,584 | https://cdm.unfccc.int/Projects/Validation/DB/8T2Z67AXN0AHD64XJZ999VXSNHPCN3/view.html [Med] |
| PT Agrowiratama, West Sumatra (validation) | AMS-III.H | 34,573 | https://cdm.unfccc.int/Projects/Validation/DB/Y0ZNS59146F9KK9T12K0PELLHV06GJ/view.html [Med] |
| Sei Silau, North Sumatra (GEC feasibility study 2009) | AMS-III.H | 17,738 | https://gec.jp/en-cdm/2009cdmfs01-1/ [Med] |
| Ulu Kanchong POM, Malaysia | AMS-III.H | (see page) | https://cdm.unfccc.int/Projects/DB/RWTUV1257518413.1/view [—] |

- Mill capacities (t FFB/h) were **not in the extracts** [**UNVERIFIED**]. Typical CDM-era Indonesian mills were 30–60 t FFB/h.
- **Range for the bulk of projects: about 35–58 ktCO2e/yr at GWP 21**, equivalent to about 47–77 kt at GWP 28.

### 6.4 Our project vs the methodology (my calculation, transparent)

- **COD load:** 585 m3/d × 50 kg COD/m3 × 365 = **10,676 t COD/yr**
- **Baseline CH4:**
  - Formula: COD × removal efficiency in the lagoon (assume 0.90) × Bo 0.25 × MCF 0.8 × uncertainty factor 0.89
  - Result: **≈ 1,710 t CH4/yr ≈ 47,900 tCO2e at GWP 28** (≈ 35,900 at GWP 21)
- **Project emissions and leakage** (biogas leakage, flare inefficiency, permeate dissolved CH4, aux power): typically 5–15%, giving **≈ 41,000–45,000 tCO2e/yr methane avoidance** at GWP 28.
- **Grid electricity displacement:** a separate component, not included in this methane figure.
- **Our 32,000 tCO2e/yr claim is therefore conservative**, about 70% of the methodology value. It corresponds to about 0.097 tCO2e/t FFB (assuming about 328,500 t FFB/yr) or about 55 kgCO2e/m3 POME.
  - Note: dissolved CH4 in a thermophilic AnMBR permeate escapes unless it is degassed (the fraction was not sourced here), so a conservative project-emission allowance is prudent.

### 6.5 Voluntary-market prices, issuance costs

- **MSCI Global Carbon Credit Price Index annual average: USD 3.5/t in 2025** (USD 4.3 in 2024) — MSCI (https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025) [High]
- **Methane-destruction credits: spot peaked at about USD 8.3/t (Jul-2024, Climate Action Reserve) and settled at about USD 5/t through 2025** (AlliedOffsets) — EcoEngineers (https://www.ecoengineers.us/insights/unlocking-value-from-landfill-methane-destruction/) [Med]
  - Vendor quotes of USD 18–30/t for livestock methane are premium or US-specific [Low]
- **Ecosystem Marketplace SOVCM 2025:** 2024 transaction volume fell 25% and the average price fell 5.5%. Waste-disposal volume tripled, driven by CCP-labelled landfill gas — Ecosystem Marketplace (https://3298623.fs1.hubspotusercontent-na1.net/hubfs/3298623/SOVCM%202025/Ecosystem%20Marketplace%20State%20of%20the%20Voluntary%20Carbon%20Market%202025.pdf) [Med; methane-specific price not extracted]
- **Verra fees:**
  - **VCU issuance levy USD 0.23/t** (on reductions *claimed*), effective 1-Jan-2025, up from USD 0.20.
  - Registry transaction fee USD 0.02/VCU; registration review fee USD 3,750; pipeline listing fee USD 1,500.
  - Source: Verra (https://verra.org/new-verra-program-fee-schedule-faqs/ ; https://verra.org/verra-releases-updated-fee-schedule/) [High]
  - No 2026 schedule was found [**UNVERIFIED**]
- **Validation and verification (VVB) costs:** typically USD 15–40k for validation plus USD 10–25k per verification. **No source was retrieved; this is an industry estimate** [Low]

---

## 7. Baseline GHG of POME open ponds per t CPO and share of mill-level GHG

- **PalmGHG pilot: POME methane = 15–35% of total product emissions** (average total 1.67 tCO2e/t CPO, including land use) — Bessou et al. (ICOPE 2016 / J. Cleaner Prod. 2014, https://agritrop.cirad.fr/580308/1/Bessou.paper.ICOPE2016.pdf) [High]
- **Mill-level POME emissions:**
  - **About 1,100 kgCO2e/t CPO reducible to about 200 with biogas capture** — J. Air & Waste Mgmt. Assoc. (2014, https://www.tandfonline.com/doi/pdf/10.1080/10962247.2013.873092) [Med]
  - Another figure from the same paper covers a different scope: 225 → 25 kgCO2e/t CPO from covering the ponds [Low]
  - **Over 90% of *mill-gate* (mill-only) GHG comes from POME** (same source) [Med]
- **Per tonne of FFB: 6.54 kg CH4 ≈ 137 kgCO2e/t FFB (GWP 21)** ≈ 183 kgCO2e/t FFB at GWP 28 — cited in an MDPI review (https://www.mdpi.com/2673-8783/6/5/77) [Med]
- **Per m3 of POME: about 12.36 kg CH4/t POME** treated in commercial Malaysian ponds ≈ **346 kgCO2e/m3 at GWP 28** (pond measurements; higher than the methodology value) — MDPI review (same URL) [Med]
  - A lower value of about 18 kgCO2e/m3 appears in a blog source [Low; inconsistent]
- **Total plantation-to-CPO emissions of 5–25 tCO2e/t CPO (with land-use change), of which POME is 9–18%** — IOP Conf. Ser. EES 293 (2019, https://iopscience.iop.org/article/10.1088/1755-1315/293/1/012004/pdf) [Low–Med]
- **Our mill (my calculation):** about 47,900 tCO2e baseline over about 69,000 t CPO/yr gives **≈ 0.69 tCO2e/t CPO**, inside the 0.5–1.1 t literature band.
- **Adoption:** under 10% of about 640 surveyed Indonesian mills used biogas (older study); PASPI (2026) says about 15% of POME potential is used — GMI presentation (https://www.globalmethane.org/expo-docs/canada13/ag_11Franco_Miguel_Presentation%20v4.pdf); bioenergy-news (2026) [Med]

---

## KEY NUMBERS FOR MODEL

| Parameter | Value | Unit | Low | High | Source |
|---|---|---|---|---|---|
| BOD discharge limit | 100 | mg/L | 100 | 100 | PermenLH 5/2014 Lamp. III (BPK) |
| COD discharge limit | 350 | mg/L | 350 | 350 | PermenLH 5/2014 Lamp. III |
| TSS discharge limit | 250 | mg/L | 250 | 250 | PermenLH 5/2014 Lamp. III |
| Oil & grease limit | 25 | mg/L | 25 | 25 | PermenLH 5/2014 Lamp. III |
| Total N limit | 50 | mg/L | 50 | 50 | PermenLH 5/2014 Lamp. III |
| pH range | 6–9 | – | 6 | 9 | PermenLH 5/2014 Lamp. III |
| Max discharge volume | 2.5 | m3/t CPO | 2.5 | 2.5 | PermenLH 5/2014 Lamp. III |
| Land application BOD max | 5,000 | mg/L | 3,500 | 5,000 | KepMenLH 28/29-2003 (status contested) |
| Max criminal fine, intentional pollution (Art. 98) | 10 | bn IDR | 3 | 10 | UU 32/2009 |
| Real POME case fine (SIPP, MA 2024) | 0.1 | bn IDR | 0.1 | 0.45 | Sabang Merauke / GoRiau |
| ISPO bioenergy/downstream deadline | 2027-03-19 | date | 2027-03-19 | 2027-03-20 | Perpres 16/2025 (InfoSAWIT) |
| Bo | 0.25 | kg CH4/kg COD | 0.25 | 0.25 | IPCC 2006 V5 Ch6 |
| MCF deep anaerobic lagoon | 0.8 | – | 0.8 | 1.0 | IPCC 2006/2019 Table 6.3 |
| AMS-III.H uncertainty factor | 0.89 | – | 0.89 | 1.0 | AMS-III.H |
| GWP CH4 | 28 | tCO2e/tCH4 | 21 | 28 | Decision 18/CMA.1 (AR5) |
| Our baseline CH4 avoidance (calc.) | 43,000 | tCO2e/yr | 32,000 | 47,900 | Own calc. from IPCC/AMS-III.H |
| Indonesian CDM POME project ER | 52,000 | tCO2e/yr | 21,675 | 57,640 | UNFCCC CDM registry |
| Baseline mill GHG from POME | 0.69 | tCO2e/t CPO | 0.5 | 1.1 | Own calc.; JAWMA 2014 |
| POME share of product GHG (PalmGHG) | 25 | % | 15 | 35 | Bessou et al. |
| Methane-avoidance VCM price | 5 | USD/tCO2e | 3 | 8.3 | AlliedOffsets via EcoEngineers; MSCI |
| MSCI carbon credit index 2025 | 3.5 | USD/tCO2e | 3.5 | 4.3 | MSCI |
| IDXCarbon IDTBS price | 3.6 | USD/tCO2e | 2.5 | 5.9 | OJK Jul-2025; Tempo Jan-2025 |
| CORSIA eligible unit (planning) | 20 | USD/tCO2e | 10 | 40 | ICAO periodic review via theplanetbrief |
| Verra issuance levy | 0.23 | USD/VCU | 0.20 | 0.25 | Verra fee schedule 2025 |
| Verra registration review fee | 3,750 | USD | 3,750 | 3,750 | Verra |
| VVB validation + verification (est.) | 50,000 | USD per 10 yr (excl. validation) | 25,000 | 100,000 | Industry estimate, unsourced |
| PLN biogas ceiling tariff 1–3 MW, yr 1–10 | 9.94 | USc/kWh | 9.81 | 11.47 | Perpres 112/2022 Lamp. I |
| PLN biogas ceiling tariff 1–3 MW, yr 11–30 | 5.97 | USc/kWh | 5.89 | 6.88 | Perpres 112/2022 Lamp. I |
| RUPTL 2025–34 bioenergy additions | 0.9 | GW | 0.5 | 0.9 | ESDM/RUPTL |
| Installed PLTBg Indonesia | 164 | MW | 156 | 164 | EBTKE (Apr-2026) |
| EU RED palm biodiesel default saving with open pond | 20 | % | 19 | 20 | ISCC EU 205 |
| Methane-capture default eligibility threshold | 5.46 | kg CH4/t CPO | – | 5.46 | ISCC 205 v3.0 |
| RSPO book & claim credit price | 2 | USD/t oil | 2 | 3.5 | Eco-Business; WWF |
| Enhanced NDC industrial wastewater CH4 target | 26 | MtCO2e (2030) | 3 | 26 | Enhanced NDC 2022 |
| Carbon tax (planned, not in force) | 2 | USD/tCO2e | 0 | 2 | IISD 2026 |

(The same data is in `/home/user/aspebindo/research/R1_numbers.json`.)

---

## Implications for the business case

1. **The 32,000 tCO2e/yr credit claim is defensible and conservative.** An AMS-III.H-style calculation (Bo 0.25 × MCF 0.8 × 0.89 × GWP 28) gives about 41–48 ktCO2e/yr for 10.7 kt COD/yr, which matches registered Indonesian CDM projects at about 50 kt/yr. The pitch should say "conservative (≈70% of the methodology maximum)" and show the calculation. The deck should also use GWP 28, not 21.
2. **The carbon price is the weak leg.** Real 2025–26 prices are about USD 3.5 (MSCI average), about USD 5 (methane avoidance), and **about USD 2.5–3.6 on IDXCarbon with very thin volume** (Feb-2026: 2,218 t). After the Verra levy (USD 0.23), registry fees and verifier costs (about USD 5–10k/yr amortised), net revenue at USD 5 is about USD 4.4/t ≈ **USD 140k/yr, under 10% of revenue**. Treat carbon as upside and stress-test at USD 3. A CORSIA price of USD 10–40 is possible only with a host-country Letter of Authorization and corresponding adjustment under Perpres 110/2025, plus SRUK registration, which is uncertain for a single small project.
3. **Additionality is both a strength and a risk.** Methane capture is not mandatory in Indonesia (no ISPO, ESDM or KLH mandate as of Oct-2026), so the project is additional. But PASPI and GAPKI are lobbying for mandatory capture, and KLH plans a methane unit from 2027. If capture becomes mandatory within the 10-year crediting period, credits could stop at renewal. The same mandate would, however, create forced demand for our BOO service. Present this as a hedge: carbon income falls, but the market grows.
4. **The compliance driver is real but the "fine avoidance" argument is weak.** Court fines are small (Rp 0.1–0.25 bn). The real costs are mill closure orders (PT BMB was sealed by its regent), director imprisonment (PT SIPP, 3 years at the Supreme Court in 2024), a Red or Black PROPER rating, and RSPO, ISPO or buyer delisting. **Sell "licence-to-operate and continuity" rather than fines.**
5. **The AnMBR permeate will still not meet river-discharge limits on its own.** About 95–98% COD removal of 50 g/L leaves roughly 1,000–2,500 mg/L COD, versus the 350 mg/L limit. It does comfortably meet the 5,000 mg/L BOD land-application benchmark. The mill also generates about 3.1 m3 of POME per t CPO, above the 2.5 m3/t discharge quota. The offer must therefore include either polishing (aerobic treatment or membrane bioreactor) or a land-application technical approval (Persetujuan Teknis + SLO under PermenLHK 5/2021). That permit path is currently ambiguous because the 2003 land-application decrees were superseded without a replacement standard. Budget for the permit work.
6. **EU market lever (ISCC/RED):** palm biodiesel from mills with open ponds fails the RED saving threshold on default values (about 20% saving), while methane capture (<5.46 kg CH4/t CPO) unlocks the default. This is a genuine selling point for mills that supply ISCC chains. No quantified "low-GHG CPO" premium was found for 2025–26, so **do not model a CPO premium**; mention it only qualitatively.
7. **New ISPO obligation on us (Perpres 16/2025):** bioenergy businesses, explicitly including biogas, must be ISPO-certified by about 19-Mar-2027. As a BOO biogas operator we will probably need our own ISPO certificate, or must sit under the mill's. Add certification cost and timeline to the plan, and check the ESDM implementing criteria, which were not found.
8. **The power-export price is capped and PLN demand is small.** The Perpres 112/2022 ceiling for 1–3 MW biogas is 9.94 ¢/kWh in years 1–10 and **drops to 5.97 ¢/kWh in years 11–30**, subject to negotiation. RUPTL 2025–34 allocates only about 0.9 GW to all bioenergy. Captive supply to the mill (replacing diesel at more than 20 ¢/kWh) is economically stronger than PLN export. Model PLN export at 9–10 ¢ with an access risk, and treat biomethane (PGN/Toyota Tsusho) as an alternative offtake.
9. **Track record of the market:** Indonesian PLTBg is only about 164 MW after more than 10 years of targets (the RUEN goal was 5.5 GW by 2025), and about 15% of POME potential is used. This shows that financing, PLN access and policy are the real barriers, not technology. Judges will expect the business model (BOO, service fee per t FFB) to tackle these barriers. That is our differentiator, but also evidence of how hard execution is.
10. **Credibility risks to disclose:**
    - The ICVCM CCP label has **not been confirmed** for wastewater methodologies, so premium buyers may discount the credits.
    - Under the Indonesian rules (Perpres 110/2025 and PermenLH 10/2026), the government may take a share of credits or require authorization.
    - The project must register in SRUK before issuance, and there is no track record yet for non-forestry projects.
    - Several numbers in this report are marked UNVERIFIED because of tool limits. Re-check them before final submission: the PermenLH 5/2014 palm annex status, the RSPO 2024 GHG indicator, the PROPER methane scoring weight, the Malaysian MPOB biogas mandate, and the Verra 2026 fees.
