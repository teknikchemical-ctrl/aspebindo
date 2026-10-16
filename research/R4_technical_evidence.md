# R4 — Technical evidence and red-team review: thermophilic AnMBR for raw POME (45 t FFB/h)

Prepared 2026-10-16. Scope: literature and industry evidence checked against the design in `process/` (results.json, biogas_balance.py).
Confidence tags: [H] peer-reviewed or official text, value seen directly; [M] peer-reviewed or official source seen only via abstract or snippet, or several secondary sources agree; [L] vendor or marketing claim, a single secondary source, or an engineering estimate by this analyst.
Access note: the research sandbox could not open full texts on ncbi/mdpi/sciencedirect/bpk.go.id (DNS/proxy block). Values were taken from search-index abstracts and snippets. Confirm the figures marked [M] against the PDFs before the final submission.

---

## 0. Model cross-checks we ran ourselves (from `process/outputs/results.json`)

- **COD routing (kg/d):** CH4 19,723 (67.4%), biomass to sludge 2,158, residual particulate to sludge 4,491, soluble effluent 2,615, H2S 98, dissolved gas 54. Influent is ~29,140 kg COD/d.
  - Our "68% COD removal" is the *methanisation fraction*, not COD removal as the AnMBR literature reports it (permeate-based). Different denominators.
- **Implied permeate COD** = 2,615 kg/d ÷ 359 m3/d ≈ **7,300 mg/L**, while VFA is only 84 mg/L. That means ~7.2 g/L of non-VFA soluble COD (about 14% of the feed COD treated as soluble refractory). This is high compared with AnMBR-on-POME permeates of ~0.8–3.5 g/L (93–98% removal). **Internally inconsistent / pessimistic.**
- **Methane check:** 19,723 kg COD × 0.35 = 6,903 Nm3 CH4/d, which matches the output. Biogas per m3 POME = 11,815/585 = **20.2 Nm3/m3**. CH4 per kg COD fed = 0.236 Nm3/kg. Volumetric CH4 productivity = 2.54 Nm3/m3·d.
- **Membrane loop:** the model sets loop flow = 10 × permeate (149 m3/h) and energy = 1.5 kWh/m3. For 34 tubular modules of about 30 m2 with 8 mm tubes (~400 tubes each, ~0.020 m2 flow area), 149 m3/h gives a cross-flow velocity of **~0.06 m/s in parallel**. Tubular AnMBR needs 1–4 m/s. To reach 2.5–3.5 m/s you need ~180–250 m3/h per module string: **~1,500–2,500 m3/h total**. Pump power ≈ Σ(Q·ΔP)/η ≈ 34 × 0.06 m3/s × 0.8 bar / 0.75 ≈ **150–250 kW**, not 22 kW [L, analyst calculation; consistent with Pentair 1.5–4 kWh/m3 at 80–200 LMH, which is ≈0.12–0.8 kW per m2 of membrane, × 996 m2 = 120–800 kW].
- **Benefit of the membrane, according to the model itself:** mesophilic CSTR at 20 d HRT gives 6,862 Nm3 CH4/d. Thermophilic AnMBR gives 6,907 (+0.7%). Thermophilic CSTR at HRT 5 d gives 6,403 (−7%), and the model only marks it "not ok". So the membrane buys **volume** (2,633 vs 11,700 m3), not methane. Choorit & Wisarnwan (2007) ran a plain thermophilic CSTR stably at HRT 5 d with 70% COD removal. The red-team question "why a membrane?" therefore has to be answered on footprint and portability alone.
- **Nitrogen:** the model doses N (setpoint ~99 mgN/L, ~31 kg N/d at P95) and predicts TAN 153 mg/L. Literature POME TN is typically ~750 mg/L (range 180–1,400). That suggests the model's POME N content is too low. N dosing is probably unnecessary, and permeate TAN will be ~300–600 mg/L.
- **BMP label:** the code calibrates to **397 NmL CH4/g VS** (mesophilic). Writing it as "/g COD" anywhere is physically impossible: the theoretical maximum is 350 NmL CH4/g COD at STP. Fix the wording in the deck.
- **Cooling duty** 812–832 kWth (85 → 56 °C on 585 m3/d) is correct arithmetic. **Parasitic total 127 kW** excludes realistic cross-flow energy (see §2).
- **Waste sludge:** 226 m3/d at MLSS ~26 g/L gives ~5.9 t TSS/d. Cake is 22.8 t/d at 22% DS (85% capture, 4 kg polymer/t DS). That leaves ~203 m3/d of press filtrate (≈0.9 t SS/d plus ~7 g/L soluble COD) with **no stated destination**.

---

## 1. Thermophilic vs mesophilic AD of POME

- **Lab CSTR, 55 °C: max stable OLR 17.0 kgCOD/m3·d at HRT 5 d, COD removal 70.3%.** At 37 °C: 12.25 kgCOD/m3·d at HRT 7 d, 71.1%. Biogas 4.66 vs 3.73 L/L·d. CH4 slightly lower at 55 °C (~69.5% vs ~71%). Methane yield reported as 0.44–0.49 L/g COD (not normalised). — Choorit W., Wisarnwan P., *Electronic J. Biotechnology* 10(3), 2007, DOI 10.2225/vol10-issue3-fulltext-7, https://www.ejbiotechnology.info/index.php/ejbiotechnology/article/view/v10n3-7 [H for OLR/HRT/removal; M for yield basis]
- **Acidified POME, OLR 2.4–4.0 g COD/L·d: thermophilic yield 0.31 L CH4/g COD, higher than mesophilic at every OLR tested.** — "Performance of AD of acidified POME under various OLRs and temperatures", 2020, https://www.researchgate.net/publication/343979030 [M]
- **Mesophilic vs thermophilic reactors for POME (Bioresource Technology 2014): thermophilic tolerated higher loading.** — https://www.sciencedirect.com/science/article/abs/pii/S0960852414005021 [M, abstract only]
- **Thermophilic POME start-up:** 1-L digesters stabilised by day 44 (thermophilic) vs day 52 (mesophilic). One thermophilic UASB seeded directly with mesophilic granules failed at day 30. A UASB-HCPB thermophilic POME reactor started up in 36 d. Full-scale (sludge) thermophilic start-up took ~4 months with a direct start, vs ~1 yr when temperature is stepped up gradually. — IOP EES 268:012028 (2019) https://iopscience.iop.org/article/10.1088/1755-1315/268/1/012028/pdf ; UASB-HCPB, *Biomass & Bioenergy* 2014 https://www.sciencedirect.com/science/article/abs/pii/S0961953414002566 [M]
- **Full-scale mesophilic closed tank (FELDA Serting Hilir, 500 m3, UPM–Kyutech): HRT reduced to 17 d within <3 months, COD removal up to 97% (total), biogas rate fell at higher OLR. CH4 productivity 1.0–1.4 m3/m3·d.** — Yacob et al., *Process Biochemistry* 2006 (start-up of semi-commercial closed digester), https://www.sciencedirect.com/science/article/abs/pii/S1359511305004381 [M]
- **Industrial POME yield 28–34 m3 biogas/m3 POME, 54–65% CH4. Tank digesters reach 80–90% COD removal at 20–40 d HRT; lagoons reach 70–85% at 20–90 d.** — Amin et al., *Int. J. Chem. Eng.* 2022, DOI 10.1155/2022/2278211 ; MPOB POEB No.104 (theoretical 17.1 m3 CH4/m3 POME at 54 g/L COD, 80% removal) https://palmoilis.mpob.gov.my/publications/POEB/poeb104-tong.pdf [M]
- **Analysis of three commercial Malaysian POME biogas plants (historical data).** — *Processes* 11(6):1603, 2023, DOI 10.3390/pr11061603 [M, numbers not extracted]
- **Full-scale imbalanced POME digester recovered within 15 d by dilution with digester effluent.** — PMC7797170 (2021) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7797170/ [M]
- **LCFA/oleate: thermophilic acetoclastic methanogens are more sensitive. IC50 oleate 0.35–0.79 mM at 55 °C vs 2.35–4.30 mM at 30 °C. Flocculent sludge is more inhibited than granular. Thermophiles recover faster.** — Hwu C.S. & Lettinga G., *Enzyme Microb. Technol.* 21(4):297–301, 1997, DOI 10.1016/S0141-0229(97)00050-1 ; review in *IJERPH* 20(4):3423, 2023, DOI 10.3390/ijerph20043423 [H/M]
- **High-OLR POME failure signal: propionate/acetate ratio > 0.7. VFA rises above OLR 50 (two-stage AnMBR). Borja (1996) mesophilic UASB failed at 17.3 kgCOD/m3·d.** — Chaipetch et al., *BioResources* 17(2):3398, 2022, https://bioresources.cnr.ncsu.edu/resources/performance-of-a-high-rate-two-stage-anaerobic-membrane-bioreactor-anmbr-for-the-treatment-of-palm-oil-mill-effluent/ [M]
- **Thermophilic reactors usually carry more residual VFA (propionate) than mesophilic; failure-stage VFA in one thermophilic study reached 4.7 g/L.** — ResearchSquare rs-54152 (preprint) https://researchsquare.com/article/rs-54152/v1 [L]

**Verdict on our values**
- OLR 10.7 kgCOD/m3·d: **plausible but optimistic for full scale**. Lab thermophilic CSTR max is 17. Full-scale POME tanks usually run 3–8 (mesophilic). There is no full-scale thermophilic POME CSTR evidence at >10. Recommend **nominal 8 (range 6–11)**, with 10.7 as a peak-month check.
- HRT 4.6 d / SRT 12 d: **supported** (thermophilic CSTR stable at HRT 5 d). An SRT/HRT ratio of 2.6 is weak decoupling for an MBR.
- Methanisation 67–68%: **supported / slightly conservative** (thermophilic CSTR 67–72%). Recommend 65–75%.
- Biogas 20.2 Nm3/m3 POME: **conservative-to-supported** vs 20–34. Recommend 20–26 for thermophilic short HRT.
- CH4 58.5%: **supported** (54–65%; thermophilic lower). Range 56–62%.
- VFA 84 mg/L: **optimistic** for thermophilic at OLR ~11. Recommend designing for 200–800 mg/L (adds 0.3–1.2 g/L COD to the permeate).
- TAN 153 mgN/L: **too low** if POME TN ≈ 500–900. Recommend 250–600 mgN/L. Free NH3 at 55 °C and pH 7.3 is ≈7% of TAN (pKa ≈ 8.4), so 20–45 mg NH3-N/L: below inhibition, but drop N dosing.
- Start-up: not stated in our plan. Recommend **2–4 months** to reach full OLR using thermophilic inoculum (e.g., from the hot cooling pond / acidification pond). Allow 4–6 months if seeding with mesophilic lagoon sludge.

## 2. AnMBR on POME / high-strength, high-solids wastewater

- **Thermophilic (55 °C) AnMBR on POME, PTFE hollow fibre: COD removal 93–98% at OLR 2–10 kgCOD/m3·d, max yield 0.56 m3 CH4/kg COD_removed (sic, above theoretical: measurement basis), constant flux only 3 LMH, organic fouling 93% of total.** — *Membranes* 9(4):55, 2019, DOI 10.3390/membranes9040055 [M/H]
- **POME MBR review: AnMBR COD removal 94.8–98.4%. Main drawback is fouling.** — *Water* 10(9):1165, 2018, DOI 10.3390/w10091165 [M]
- **UMAS (ultrasonic membrane anaerobic system) on POME: 96.6–98.4% COD removal at HRT 7.5 d. CH4 0.24–0.59 L/g COD.** — Abdurahman & Azhari, LAPSE:2024.0022 https://psecommunity.org/LAPSE:2024.0022 ; economic viability, *J. Water Reuse Desal.* 2016, DOI 10.2166/wrd.2016.124 [M]
- **Two-stage AnMBR on POME: up to OLR 98 kgCOD/m3·d; COD removal falls to ~70%; membrane contributes 24–35% of removal.** — Chaipetch et al. 2022 (above) [M]
- **Full-scale ADI-MBR (Kens Foods, USA, food wastewater, external/tubular): COD removal 99.4%, flux only 2.5–4.2 LMH in the first two years.** — Christian et al., WEFTEC 2010, https://www.researchgate.net/publication/272549477 [M]
- **Sidestream helix-tubular AnMBR on vinasse: max attainable flux 10 LMH at 16–17 g VSS/L, COD removal 95±3%. Food-wastewater sidestream UF reached 14 LMH.** — Frontiers Bioeng. Biotechnol. 2024, DOI 10.3389/fbioe.2024.1491974 [M]
- **AnMBR typical MLSS 15–30 g/L; flux 5–10 LMH (full-scale AnMBR 5–12 LMH vs aerobic MBR 20–30).** — *Environ. Eng. Res.* review 2021, https://www.eeer.org/upload/eer-2021-575.pdf ; *Desal. Water Treat.* mini-review 2016, DOI 10.1080/19443994.2015.1100879 [M]
- **Thermophilic sidestream AnMBR "shear-rate dilemma": high cross-flow shear breaks flocs into fines and lowers the attainable flux. Cake layer is the limiting factor. Tested up to 1.5 m/s.** — Jeison D., Telkamp P., van Lier J.B., *Water Environ. Res.* 81(11):2372, 2009, PMID 19957769 https://pubmed.ncbi.nlm.nih.gov/19957769 [H, abstract]
- **Pentair X-Flow cross-flow MBR (aerobic reference): 80–200 LMH, MLSS 12–30+ g/L, 1.5–4 kWh/m3. Airlift: 40–60 LMH, <0.25 kWh/m3. AnMBR "favourable at COD >7,000 ppm".** — https://xflow.pentair.com/en/products/x-flow-crossflowmbr.html [L, vendor]
- **Temperature limits: X-Flow Compact 27 (8 mm) "do not exceed 60 °C". Compact 55G (8 mm, 55 m2) rated 0–40 °C. Berghof 8 mm PVDF tubes come in GFRP or PVC-U housing (PVC-U is limited to roughly 40–45 °C).** — Pentair datasheets via directindustry https://pdf.directindustry.com/pdf/pentair-x-flow/compact-27/71363-666138.html ; https://xflow.pentair.com/en/products/compact55g [L]. **At 55 °C we are 5 K from the module limit. Specify GFRP housings, and add a 60 °C trip on the loop.**
- **Fouling-control energy reported for AnMBR, 0.08–0.35 kWh/m3, applies to municipal, low-MLSS, gas-sparged systems. Not transferable to tubular cross-flow at 26 g/L.** — LAPSE-2023.31363 review https://psecommunity.org/wp-content/plugins/wpor/includes/file/2304/LAPSE-2023.31363-1v1.pdf [M]
- **Membrane capex:** no reliable public USD/m2 for tubular PVDF was found. Flat-sheet PVDF is ≤80 USD/m2 (lab-made). Industrial tubular modules are typically quoted at **~100–250 USD/m2 for the module alone** and **~400–800 USD/m2 installed with skid, pumps and CIP** [L, analyst estimate; obtain Pentair/Berghof quote].
- **CIP and life:** sidestream tubular AnMBR practice is a maintenance clean (NaOCl 200–500 ppm, alkaline) every 1–4 weeks and a recovery clean (NaOCl 1,000 ppm + citric/oxalic acid) every 1–3 months. Add a caustic/surfactant step for oil. Membrane life is typically **5–7 years**, shorter with oil/LCFA and 55 °C [L, synthesis of vendor practice; no POME full-scale data found].

**Verdict**
- Flux 15 LMH: **optimistic**. Evidence is 3 LMH (thermophilic POME), 2.5–4.2 (full-scale ADI-MBR) and 5–14 (sidestream high-strength). Recommend **design 8 LMH (range 5–12)**, giving area **~1,900 m2 (1,250–3,000)**.
- Cross-flow loop 149 m3/h and energy 22 kW (1.5 kWh/m3): **severely underestimated (~5–10×)**. Recommend **4–12 kWh/m3 → 60–180 kW** at 8 LMH with optimised velocity (~2 m/s), or ~150–250 kW at the current design. Alternatively use gas-lift tubular (X-Flow Airlift-type with biogas) at 0.5–1.5 kWh/m3, but flux drops to ~5–10 LMH.
- Membrane replacement years 8 and 15: **optimistic**. Recommend a 5-year life (replace years 6, 11, 16), at 15–20% of membrane capex per year in sinking-fund terms.
- "Total COD removal 68%": **inconsistent wording, not pessimism.** Report two numbers:
  - (a) methanisation 65–72%;
  - (b) permeate-based COD removal 92–97% (permeate COD 1.5–4 g/L).
  Our implied permeate COD of 7.3 g/L is **too high**: re-check the soluble-inert fraction (literature points to ≤5% of feed COD).

## 3. Effluent compliance (PermenLH 5/2014, Lampiran III – palm oil industry)

- **Limits: BOD 100, COD 350, TSS 250, oil & grease 25, total N 50 mg/L, pH 6–9, max 2.5 m3 per t CPO.** — Permen LH No.5/2014, https://peraturan.bpk.go.id/Download/384240/Permen%20LH%20No%205%20Tahun%202014.pdf [M: values match multiple Indonesian theses; one secondary source cites COD 300. Verify against Lampiran III.]
- **Land application route: Kepmen LH 28/2003 & 29/2003 (BOD ≤5,000 mg/L, pH 6–9) was historically the dominant compliance path for Indonesian mills.** Kontan reports both were revoked by Permen LHK 5/2021, which takes land application into the Persetujuan Teknis regime. — Soilrens/UNPAD https://journals.unpad.ac.id/soilrens/article/download/45267/19386 ; Kontan https://industri.kontan.co.id/news/pemerintah-disarankan-revisi-aturan-pemanfaatan-limbah-cair-kelapa-sawit [M]
- **Typical AnMBR-on-POME permeate:** COD 0.8–3.5 g/L (93–98% removal of 50 g/L). BOD ~200–1,000 mg/L. TSS <10–50 mg/L (UF). O&G <25 mg/L (mostly retained). NH4-N 250–600 mg/L. Colour/humics high. [M, derived from the removal %s above]

**Verdict:** the permeate is **not compliant** with PermenLH 5/2014 on COD, BOD and TN (our own model's permeate at 7.3 g/L COD and TAN 153 also fails). Options:
- (i) land application under Persetujuan Teknis: BOD easily <5,000. This is the cheapest route. Recommended as the base case.
- (ii) aerobic polishing (activated sludge/SBR with nitrification-denitrification), ~360 m3/d, ~1.5–2.5 t COD/d. Adds ~60–120 kW aeration and capex.
- The press filtrate (~200 m3/d) must also be included. It should be returned to the reactor feed or to polishing, not discharged.

## 4. Sludge

- **Anaerobic biomass yield 0.03–0.1 g VSS/g COD. Model: 2.16 t COD/d biomass ≈ 7% of feed COD (≈0.05 gVSS/gCOD), which is supported.** — standard ADM1 range; USM thesis 0.174 gVSS/gCOD for UASB/UASFF on POME https://erepo.usm.my/items/dd7a1458-dd62-49e3-8fe0-394604b7ec22 [M]
- **POME AD generates sludge ~35% of treated volume (lagoon practice).** — *Current World Environment* 9(2):321, 2014 https://mail.cwejournal.org/pdf/vol9no2/vol9_no2_321-330.pdf [L]
- **Thermophilic dewaterability evidence is mixed.** ATAD/thermophilic sludges show higher polymer demand and shear sensitivity. Some anaerobic studies show TAD dewaterability 14–22% better than MAD. — *Bioengineering* 3(2):15, 2016, DOI 10.3390/bioengineering3020015 ; *Water* 13(20):2839, 2021, DOI 10.3390/w13202839 [M]
- **Screw-press cake for digested sludges: typically 15–25% DS. Polymer 6–12 kg/t DS. Capture 90–95%** [L, industry practice; no POME screw-press dataset found].
- **Use as fertiliser:** POME digestate and decanter cake are routinely applied in Indonesian/Malaysian estates (N, K, Mg rich). Classified as non-B3 when from a non-hazardous process; check KLHK Persetujuan Teknis [L].

**Verdict:**
- Cake 22% DS: **supported** (range 15–25%). Recommend 18% as the conservative case, giving 28 t/d cake.
- Polymer 4 kg/t DS: **optimistic**. Recommend 8 (5–12).
- Capture 85%: conservative (90–95% possible).
- **Missing:** the filtrate stream and the cake handling/disposal route.

## 5. H2S, desulfurisation and gas engines

- **Raw POME biogas H2S 1,000–3,000 ppm (Malaysia), 2,700–3,000 ppm (Indonesia), up to 4,000 (vendors).** — Johor bioscrubber study, 2025, PMC12272170 https://pmc.ncbi.nlm.nih.gov/articles/PMC12272170/ ; Polije thesis (PT Inti Indosawit) https://sipora.polije.ac.id/11230/ [M]
- **Full-scale biotrickling filter: complete removal at 2,923–4,400 ppmv inlet. EC ~53 g H2S/m3·h. Aerobic BTF needs controlled O2 (~stoichiometric). Explosion-limit control is mandatory.** — Samsun Univ. study https://avesis.samsun.edu.tr/yayin/2fd1c075-2e94-4410-bf20-41f60378d5b8 ; UPC thesis https://upcommons.upc.edu/entities/publication/026ea93e-ce12-411f-9c63-66143bf01eb1/full [M]
- **Engine fuel limits.** Jenbacher TI 1000-0300 / MWM TR 0199-99-3017 set the limits, and they depend on whether a catalyst is fitted. Secondary values: Jenbacher H2S <200 mg/Nm3 (~130 ppm). "Most ICE OEMs limit H2S to ~100 ppm" (WEF). Practical target ≤100–200 ppm. — Lucideon https://www.lucideon.com/testing-characterisation/test-methods/test-method-page-jenbacher ; Duzynski (PL) https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-article-BWAW-0016-0016/c/Duzynski.pdf ; WEF 2017 ICE report https://www.wef.org/globalassets/assets-wef/direct-download-library/public/03---resources/wsec-2017-tr-002-rbc-internal-combustion-engines---9.2017.pdf [M/L]
- **MWM TCG 3016 V16 (800 kWe): η_el up to 43.4% (natural-gas rating; biogas ~40–42%). Availability 97% claimed for a German biogas plant.** — https://zorg-biogas.com/equipment/generators/MWM-TCG3016-V16-800-kw-el-biogas-generator-building ; MWM Langenau https://www.mwm.net/en/news/news-releases/97-percent-availability-biogas-fueled-mwm-tcg-3016-engines-supply-energy-to-alb-danube-district/ [L]
- **Biogas genset O&M ≈ USD 0.012–0.025/kWh including overhaul reserve. Availability 90–95% realistic for remote tropical sites** [L, analyst synthesis].

**Verdict:**
- H2S raw 2,900 ppm: **supported**.
- BDS 92%: **supported** (90–99%).
- 34 ppm after activated carbon: **conservative / over-engineered**. With 232 ppm after BDS, AC would consume ~4 kg H2S/d, i.e. ~7–15 t AC/yr (~USD 30–70k/yr). Better: size the BDS for ≥95% and use AC only as guard (target <150 ppm).
- η_el 38%: **conservative at full load**. But two 800 kWe units carrying a 1,088 kW average sit at ~68% load. That rises to ~45% in low-crop months, when one engine runs at partial load. Consider 3 × 400–500 kWe or 2 × 600 kWe.
- Availability: specify 92%.

## 6. Mixing and heat balance

- **Gas mixing 1.5–3.5 W/m3. Pumped-jet systems need 3–5 turnovers per HRT and >90% of volume at >0.1 m/s. Heating-loop recirculation alone rarely mixes well.** — Stellenbosch thesis https://scholar.sun.ac.za/handle/10019.1/104798 ; KLA jet mixing https://klasystems.com/jet-mixing/ ; WWD https://www.wwdmag.com/mixers-mixing-equipment-agitators/jet-mixing-matters [M/L]
- **Malaysian full-scale POME plant had to install an induced-draft cross-flow cooling tower to hold POME <40 °C (mesophilic). CH4 yield rose >40% after the cooling tower plus co-digestion.** — Univ. Nottingham eprint 80045 https://eprints.nottingham.ac.uk/80045 ; Indonesian direct-contact cooling-tower design https://ejournal.brin.go.id/MIPI/article/download/1441/1023/5241 [M]
- **Sidestream thermophilic AnMBR (sewage sludge): heating penalty exceeded the extra gas, so mesophilic gave 3× the net energy.** This does **not** apply to POME, because the feed arrives hot: here thermophilic operation is a genuine advantage. — Bioresource Technology 2024 https://www.sciencedirect.com/science/article/abs/pii/S0960852424015268 [M]

**Verdict:**
- Jet mixing 27 kW (~10 W/m3): **supported / slightly generous** (5–10 W/m3 for 26 g/L MLSS in H/D = 3.3 vessels). The tall, slim geometry needs a multi-level nozzle design. Grit settles at the bottom, so use a conical bottom.
- Cooling 812 kWth: **supported**. Thermophilic halves the cooling duty versus mesophilic (85 → 38 °C ≈ 1.33 MW).
- Weekend and holiday mill stops: insulated vessels (~33 kW total loss) can be kept warm with engine jacket heat, but only if gas is stored. Size gas storage for ≥24–36 h of mill downtime.

## 7. Transport and installation

- **PP 55/2012 (amended by PP 30/2021): vehicle width ≤2,500 mm; height ≤4,200 mm and ≤1.7 × width.** Loads exceeding these need special permits (dispensasi/izin angkutan barang khusus/alat berat), route survey and police escort (PM 60/2019 on goods transport). — https://pasal.id/peraturan/pp/pp-no-55-tahun-2012 ; https://peraturan.bpk.go.id/Download/141279/PM_60_TAHUN_2019_rev.pdf [M]
- **Precedent:** an 82-t pressure vessel moved 70 km in Malaysia over 2 days with escort, detours around overhead bridges, and ~100 overhead cables lifted. In Indonesia, oversized cargo needed a police escort and power-line management. A Sumatra excavator move used ferry plus local roads with escort. — AJOT https://ajot.com/news/three-days-for-82-ton-oil-gas-pressure-vessel-to-arrive-at-its-foundation ; Röhlig https://www.rohlig.com/about-us/news-press/detail/transporting-oversized-cargo-antennae-from-china-to-indonesia/ ; Breakbulk https://breakbulk.com/articles/fls-moves-sumatran-excavator [M]
- **Our shell is 4.2 m Ø × 17.3 m.** On a lowbed (deck ~0.8–1.0 m) the travel height is ~5.0–5.2 m, which is **+0.8–1.0 m over the legal height** and **1.7 m over the legal width**. Estimated shell mass ≈ 266 m2 × 10 mm × 7.85 ≈ 21 t, ~25–30 t with nozzles and internals. Gross combination ~55–65 t needs multi-axle lowbeds. Class III provincial and estate roads (MST 8 t) need dispensasi and bridge checks [L, analyst calculation].
- **Modular / bolted digester installation:** typically 3–6 months from site handover to mechanical completion, plus 2–4 months of biological start-up [L].

**Verdict:** shipping 14 vessels horizontally is **feasible but optimistic** on cost and permitting. Every move is an oversize convoy (14 trips per relocation) with PLN line lifting. Recommend either:
- ≤3.5 m Ø vessels, or
- split shells / bolted glass-fused-steel tanks erected on site, keeping only the membrane, CHP and gas-cleaning units containerised (true "portable" elements).

Also budget **USD 5–15k per vessel trip** in Sumatra [L], plus permits.

## 8. Grit, fibre, oil and pretreatment

- **POME TSS 5–54 g/L (range); 16.6–94 g/L in one Indonesian dataset. O&G 130–18,000 mg/L (typ. 2,000–8,300).** — *Processes* 9(5):739, 2021, DOI 10.3390/pr9050739 ; IntechOpen ch. 60482 https://www.intechopen.com/chapters/60482 ; Setiadi 1996 in https://www.researchgate.net/publication/279868673 [M]
- **Oil-removal pretreatment raises oil separation: DAF +68%, coalescer +53%, ultrasonication +50% (Mahidol).** Effective pretreatment "radically reduces load on digesters". — https://repository.li.mahidol.ac.th/entities/publication/d538c958-d5d8-4191-a47c-766653f67886/full ; Abertay review https://rke.abertay.ac.uk/en/publications/recent-advances-on-palm-oil-mill-effluent-pome-pretreatment-and-a/ [M]
- **Practice:** sand and fruit dirt from FFB settle in digesters and need periodic desludging. Fibre causes ragging on jet nozzles and blocks 5–8 mm tubes. Tubular membranes need ≤1–2 mm pre-screening (vendor rule ~1/3 of the tube ID) [L].

**Verdict:**
- Desander 60% removal: **optimistic in its consequences**. Use a hydrocyclone or aerated grit chamber with ≥85–90% removal of >100 µm grit.
- Add a 1 mm rotary or drum screen on the membrane loop (not only on the feed).
- Keep the mill's oil-recovery pit and limit feed FOG to ~1–2 g/L before the AnMBR.
- Use hardened or rubber-lined cross-flow pumps.

## 9. POME characteristics and seasonality

- **COD 15–100 g/L (typ. ~50), BOD 10–44 g/L (typ. ~25), TSS 5–54 g/L, O&G 0.13–18 g/L, pH 4–5, T 80–90 °C, TN 180–1,400 mg/L (typ. 750), NH4-N 4–80 mg/L raw.** — *Processes* 2021 DOI 10.3390/pr9050739 ; encyclopedia.pub entry 10093 (Malaysian DOE table) ; IntechOpen 60482 [M]
- **POME generation 0.55–0.67 m3/t FFB.** Our 585 m3/d over 900 t FFB/d (20 h × 45 t/h) = 0.65: **supported**. — https://www.researchgate.net/publication/279868673 [M]
- **Seasonality:** February is consistently the lowest month (First Resources, Indonesia: 218 kt vs 258 Jan, 306 Jun, 2023). Annual yield cycles persist even without climatic seasonality. Industry pattern: low crop Feb–Apr, peak Aug–Nov, **peak:trough ≈ 1.5–1.8**. — First Resources 1H2023 https://links.sgx.com/1.0.0/corporate-announcements/TOI4KBRYUFP6AQ6Y/768567_First_Resources_1H2023_Production_Highlights.pdf ; Henson & Mohd Tayeb, JOPR (MPOB) https://jopr.mpob.gov.my/seasonal-variation-in-yield-and-developmental-processes-in-an-oil-palm-density-trial-on-a-peat-soil-1-yield-and-bunch-number-components/ [M for Feb low; L for the ratio]
- **Mill utilisation:** Indonesian mills often average 60–80% of rated throughput over the year [L]. The design 585 m3/d is a **peak-day** figure. The annual average is likely ~420–470 m3/d.

**Verdict:**
- COD 50 g/L: **supported**.
- Volume: **supported for the design day, optimistic for annual energy**. Use annual average POME ≈ 0.75–0.8 × design for revenue.
- Size membranes and CHP for peak, and finance on the average.

---

## DESIGN CHECK TABLE

| Parameter | Our value | Literature range | Verdict | Recommended | Source |
|---|---|---|---|---|---|
| Inlet COD | 50 g/L | 40–80 (15–100) | Supported | 50 (40–65) | Processes 2021, 10.3390/pr9050739 |
| POME generation | 0.65 m3/t FFB | 0.55–0.70 | Supported | 0.65 | Setiadi in RG 279868673 |
| Annual avg POME | 585 m3/d (design) | 0.6–0.8 × design | Optimistic for revenue | 440 (410–470) m3/d avg | First Resources; analyst |
| Temperature | 55 °C | 50–57 thermophilic | Supported | 52–55 | Choorit 2007 |
| OLR | 10.7 kgCOD/m3·d | 4–17 (lab thermo); 3–8 full-scale | Optimistic (full scale) | 8 (6–11) | Choorit 2007; Amin 2022 |
| HRT | 4.6 d | 5–7 (thermo CSTR) | Supported | 5 (4.5–7) | Choorit 2007 |
| SRT | 12 d | 10–30 | Supported (weak decoupling) | 15–20 | Jeison 2009; ADM1 |
| Methanisation | 68% | 65–72 (thermo CSTR) | Supported | 70 (65–75) | Choorit 2007 |
| AnMBR permeate COD removal | ~85% implied | 93–98% | Pessimistic/inconsistent | 94 (92–97)% | Membranes 2019; Water 2018 |
| Permeate COD | ~7,300 mg/L | 800–3,500 | Too high | 2,500 (1,500–4,000) | Membranes 2019; UMAS 2024 |
| Biogas yield | 20.2 Nm3/m3 POME | 20–34 | Conservative | 22 (20–26) | Amin 2022 |
| CH4 content | 58.5% | 54–65 | Supported | 60 (56–62) | Amin 2022 |
| CH4 per kg COD fed | 0.236 Nm3/kg | 0.20–0.31 | Supported | 0.24 (0.21–0.27) | Acidified POME 2020 |
| BMP POME | 397 NmL/g (VS) | ≤350 /g COD theor. | Label error if "/gCOD" | Keep /gVS | Stoichiometry |
| VFA | 84 mg/L | 100–1,000 thermophilic | Optimistic | 400 (200–800) | Chaipetch 2022; Hwu 1997 |
| TAN | 153 mgN/L | 250–600 (TN 750 typical) | Underestimated | 400 (250–600) | encyclopedia.pub/DOE |
| N dosing | ~31 kg N/d | not needed for POME | Likely unnecessary | 0 | POME TN data |
| Membrane flux | 15 LMH | 3–14 (2.5–4.2 full-scale) | Optimistic | 8 (5–12) | Kens Foods; Membranes 2019 |
| Membrane area | 996 m2 | – | Undersized | 1,900 (1,250–3,000) m2 | derived |
| Cross-flow loop | 149 m3/h | 1,500–2,500 needed (2.5–3.5 m/s) | Severely low | ~1,800 m3/h or gas-lift | analyst hydraulic calc |
| Cross-flow energy | 22 kW (1.5 kWh/m3) | 4–12+ kWh/m3 | Severely optimistic | 120 (60–250) kW | Pentair; analyst calc |
| Membrane life | ~7 yr (yr 8, 15) | 5–7 | Optimistic | 5 yr | vendor practice |
| Module temp limit | 55 °C op | 40–60 °C limits | Marginal | GFRP, ≤55 °C trip 58–60 | Pentair datasheets |
| Membrane capex | – | 100–250 USD/m2 module; 400–800 installed | Need quote | 600 USD/m2 installed | analyst [L] |
| MLSS | 26 g/L | 15–30 | Supported (upper) | 20–25 | EER review 2021 |
| Raw H2S | 2,900 ppm | 1,000–4,000 | Supported | 2,900 (2,000–4,000) | PMC12272170 |
| BDS removal | 92% | 90–99 | Supported | 95 | Samsun BTF study |
| H2S to engine | 34 ppm | ≤100–200 | Conservative | ≤150 | Jenbacher via Lucideon/WEF |
| η_el | 38% | 39–43 (full load) | Conservative full load / optimistic part load | 39% at ≥75% load | MWM spec |
| CHP configuration | 2 × 800 kWe | – | Oversized (68% avg load) | 2 × 600 or 3 × 400 kWe | analyst |
| Availability | (implicit ~100%) | 90–97 | Optimistic | 92% | MWM 97% claim |
| O&M genset | – | 0.012–0.025 USD/kWh | – | 0.018 | analyst [L] |
| Parasitic load | 127 kW (11.7%) | 20–35% with AnMBR | Optimistic | 230 (180–350) kW | derived |
| Net power | 961 kW | – | Optimistic | 740 (650–850) kW design; ~600 annual avg | derived |
| Mixing | 27 kW (~10 W/m3) | 5–10 W/m3 | Supported | 20–27 kW | KLA; Stellenbosch |
| POME cooling | 812 kWth | – | Supported | 812 (650–900) | heat balance |
| Cake DS | 22% | 15–25 | Supported | 18–22% | Water 2021; practice |
| Polymer | 4 kg/t DS | 6–12 | Optimistic | 8 | practice [L] |
| Desander removal | 60% | ≥85–90% needed | Insufficient | ≥85% hydrocyclone | practice [L] |
| Thermo start-up | not stated | 36–120 d | Missing | 90 (60–120) d | IOP 2019; UASB-HCPB |
| Effluent compliance | – | COD 350, BOD 100, TN 50 | Non-compliant | land application or aerobic polish | PermenLH 5/2014 |
| Transport envelope | 4.2 × 17.3 m | 2.5 W × 4.2 H legal | Oversize (permit) | ≤3.5 m Ø or site-erected | PP 55/2012 |
| Seasonality peak:trough | – | 1.5–1.8 | Missing | model monthly | First Resources |

## Top 10 technical risks and mitigations

1. **Cross-flow energy and hydraulics are underestimated ~5–10×** (149 m3/h, 22 kW vs ~1,800 m3/h and 120–250 kW). Net power could fall 15–25%.
   - Mitigation: re-size with the vendor at 2–2.5 m/s and 8 LMH. Evaluate biogas-lift tubular or intermittent cross-flow. Report sensitivity.
2. **Flux of 15 LMH is unproven for thermophilic, oily, 26 g/L POME** (evidence 3–10 LMH).
   - Mitigation: design at 8 LMH (≈1,900 m2) with 30% spare module space. Run a pilot (1 module) at a mill before the final competition claim.
3. **The membrane adds almost no methane** (model +0.7% vs mesophilic CSTR; a plain thermophilic CSTR works at HRT 5 d).
   - Mitigation: justify the membrane on footprint/portability and effluent TSS only. Compare against a thermophilic CSTR plus a decanter/lamella settler with solids recycle (lower capex and opex).
4. **Effluent non-compliance** (permeate COD 1.5–7 g/L, TN 250–600 vs 350/50 limits). The press filtrate (~200 m3/d) has no destination.
   - Mitigation: land application under Persetujuan Teknis (BOD <5,000) as base case. Optional SBR polishing. Recycle filtrate to the feed tank.
5. **LCFA/oil inhibition and membrane oil fouling at 55 °C** (thermophilic IC50 for oleate is ~5× lower).
   - Mitigation: keep the mill oil-recovery pit; target feed FOG ≤1–2 g/L; continuous feeding; online CH4/VFA/alkalinity (FOS/TAC) monitoring; caustic-surfactant CIP.
6. **Thermophilic instability / VFA (propionate) excursions at OLR ~11 and during mill stops/restarts.**
   - Mitigation: design nominal OLR 8; feed equalisation ≥24 h; ramp protocol after weekends; P/A ratio <0.7 alarm; effluent recycle for dilution (proven full-scale recovery in 15 d).
7. **Oversize transport and relocation** (5.1 m travel height, 4.2 m width, 14 convoys, PLN lines, estate roads).
   - Mitigation: ≤3.5 m Ø shells or bolted/site-welded tanks; containerise only the membrane/CHP/gas skids; route survey and dispensasi budget.
8. **Grit and fibre**: abrasion of high-velocity pumps, blocked 5–8 mm tubes and jet nozzles, sand accumulation in slim vessels.
   - Mitigation: hydrocyclone ≥85%; 1 mm screen on the membrane loop; conical bottoms with sludge draw-off; hardened pumps; 8 mm (not 5.2 mm) tubes.
9. **Membrane temperature and life** (55 °C vs 40–60 °C module limits; life 5 yr, not 7).
   - Mitigation: GFRP-housed PVDF rated ≥60 °C; high-temperature interlock; replacement every 5 yr in the financial model.
10. **Energy-yield overstatement from seasonality, part-load CHP and availability** (design-day POME, 2 × 800 kWe at 45–68% load, 100% availability).
    - Mitigation: model monthly FFB (Feb–Apr trough ~60–65% of peak); 92% availability; right-size CHP (2 × 600 or 3 × 400 kWe); gas storage ≥24 h. Present net power as an annual-average ~600–750 kW, not 961 kW.

Also fix the units on the "BMP 397 NmL CH4/gCOD" wording (it is /gVS), and drop the N dosing (POME TN ~750 mg/L).
