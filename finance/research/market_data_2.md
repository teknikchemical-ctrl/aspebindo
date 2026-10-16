# Market data 2 – POME biogas power set (45 t FFB/h mill)

Researched 2026-10-15 using web search only. Direct PDF fetches of the official texts failed, so table values come from search-engine extracts of the regulation scans and press reports. Values marked [UNVERIFIED] need checking against the primary document.

## 1. Perpres 112/2022 PLTBg ceiling price (HPT)

| Item | Value | Source |
|---|---|---|
| PLTBg ≤1 MW, yr 1–10 | **10.18 × F** USc/kWh | Perpres 112/2022 Lampiran I scan; CNBC Indonesia, Katadata (2022) |
| PLTBg ≤1 MW, yr 11+ | **6.11** USc/kWh, no F | same |
| PLTBg >1–3 MW, yr 1–10 / 11+ | 9.81 × F / 5.89 (OCR) | Lampiran I scan; KESDM socialisation slides (2022) |
| PLTBg >3–5, >5–10, >10 MW | not extracted [UNVERIFIED] | – |
| **PLTBg excess power** (any capacity) | **7.44** USc/kWh flat, no F | Lampiran I "PLTBm dan PLTBg Excess Power"; Pasal 4 |
| F, Sumatera (Riau, Sumut, Jambi) | ~1.10 [UNVERIFIED] | Lampiran II (garbled extract); range is 1.0 (Jawa-Bali) to 1.5 (Papua) |
| F, Kalimantan | ~1.15 [UNVERIFIED] | same |
| Term of stage 2 | sources disagree (yr 11–20, 11–25 or 11–30) [UNVERIFIED] | – |

- **Capacity basis.** None of the sources defines the tier as installed or contracted capacity [UNVERIFIED]. In PLN practice PPAs are written on contracted net capacity at the delivery point. For a ~0.96 MWe net export, the 2 × 500 kWe set clearly sits in the ≤1 MW tier. With 2 × 800 kWe (1.6 MW installed), the tier is unclear unless contracted capacity is capped at ≤1 MW. The case should treat that as a legal risk.
- **Excess power.** If the plant mainly supplies the mill and sells only its surplus, it falls under the "excess power" price of 7.44 USc/kWh, not 10.18 × F.
- **Status.** Perpres 112/2022 is still in force as of 2026. Permen ESDM 5/2025 (EBET PPA rules) implements it and does not replace it. In February 2026 ESDM confirmed that an izin prakarsa had been issued to revise the Perpres (new floor/ceiling price scheme, hybrids). As of the latest results found, no revised Perpres had been issued [verify on JDIH Setneg]. The ceiling prices can be evaluated every year.
- Sources: [listrikindonesia.com](https://listrikindonesia.com/detail/19147/harga-listrik-ebt-akan-diatur-tidak-ada-lagi-diskusi-alot-ipp-dan-pln) (2026); [CNBC Indonesia, Energy Outlook 2026](https://www.cnbcindonesia.com/news/20260205161013-4-708547/siap-siap-pemerintah-mau-tetapkan-batas-atas-bawah-tarif-listrik-ebt/amp); [CNBC 2022](https://www.cnbcindonesia.com/news/20220915083310-4-372210/jokowi-teken-aturan-harga-murah-listrik-ebt-begini-isinya); [Katadata 2022](https://katadata.co.id/ekonomi-hijau/energi-baru/6322b0d0c80d2/diatur-perpres-ebt-ini-rincian-harga-listrik-dari-energi-terbarukan); [JDIH Kemenkeu PDF](https://jdih.kemenkeu.go.id/api/download/7332a343-0623-4d26-80f2-9d8f62a5c2ba/2022perpres112.pdf); [LPEM UI 2023](https://www.lpem.org/wp-content/uploads/2023/06/Environmental_Policy_Update_V1_No1_ID.pdf); [Kontan (annual review)](https://industri.kontan.co.id/news/tarif-listrik-ebt-di-perpres-1122022-bisa-dievaluasi-tiap-tahun).

**Takeaway:** For the base case, use 10.18 × 1.10 ≈ **11.2 USc/kWh** in years 1–10 and 6.11 after that, provided the full-export PPA is ≤1 MW. Use **7.44 USc/kWh** if the plant is treated as excess power from a captive plant. Size the set at 2 × 500 kWe, or cap contracted capacity, so it stays in the ≤1 MW tier.

## 2. Carbon credits (POME methane avoidance)

| Item | Value | Source / note |
|---|---|---|
| Methodology | AMS-III.H (CDM small-scale, usable under VCS); GS uses equivalent | – |
| Crediting period, Verra non-AFOLU | 7 yr renewable twice (21 yr max) or 10 yr fixed | VCS Standard [UNVERIFIED in this search] |
| Crediting period, Gold Standard | 5 yr renewable twice (15 yr) or 10 yr fixed | [UNVERIFIED] |
| Verra fees (2025 schedule) | pipeline listing US$1,000–1,500; registration US$2,000 (one methodology); verification review US$1,250–5,000; issuance levy **US$0.23/VCU**; account US$750/yr | [Verra 2025 fee update](https://verra.org/verra-releases-updated-fee-schedule/), [FAQ](https://verra.org/new-verra-program-fee-schedule-faqs/) (figures conflict, so check the PDF) |
| VVB validation / verification | ~US$15–40k / ~US$10–25k per event | industry rule of thumb [UNVERIFIED] |
| Time to first issuance | ~12–24 months after start | [UNVERIFIED] |
| Prices | Platts "Methane Collection" US$3.80/t (Dec 2024); renewable-energy avoidance US$1.10/t; MSCI all-credit index US$3.5/t (2025), BBB+ US$6.8/t | [S&P Global](https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/122024-commodities-2025-demand-for-avoidance-carbon-credits-set-to-remain-muted); [MSCI](https://www.msci.com/research-and-insights/blog-post/carbon-credits-come-of-age-in-2025) |
| POME-specific price | no published series; assume **US$2–6/t**, Article 6 authorised (CA) units **US$8–15/t** | [UNVERIFIED] |
| Indonesia framework | Perpres 110/2025 replaced Perpres 98/2021. International transfers under Art 6.2/6.4 need KLH authorisation and a corresponding adjustment; non-CA voluntary trades are recognised. Registration in SRN-PPI (moving to the SRUK platform). Levy rate is left to MoF regulations, so no % found [UNVERIFIED]. Verra–Indonesia MRA signed Oct 2025. | [SSEK](https://ssek.com/blog/indonesia-introduces-new-carbon-trading-framework-under-presidential-regulation-no-110-of-2025/), [Ashurst](https://www.ashurstperkinscoie.com/en/insights/major-overhaul-of-indonesias-carbon-regulatory-framework/), [Verra](https://verra.org/verra-and-indonesia-sign-milestone-agreement-to-advance-carbon-markets/) |
| IDXCarbon | thin market: about IDR 47k/t implied (~US$3); 8 t traded in June 2025; cumulative 1.6 Mt / IDR 78 bn by Jul 2025 (~IDR 49k/t) | [IDN Financials](https://www.idnfinancials.com/news/55927/carbon-trading-plunges-98-5-in-june-2025-idx-chief-responds); [IEEFA](https://ieefa.org/resources/two-years-after-launch-indonesias-carbon-market-struggles-find-momentum) |

**Takeaway:** 33 kt/yr × US$3 is about **US$100k/yr gross**, against roughly US$40–60k/yr of MRV and fees. Carbon is upside, not the base case. Note also that the same methane reduction cannot be both sold as a credit and claimed in the CPO/biofuel GHG value (double claiming).

## 3. CPO market value from methane capture

| Scheme | Savings without capture | Savings with capture | Source |
|---|---|---|---|
| RED II Annex V, palm biodiesel (typical / default) | 33% / **20%** | 51% / **45%** | [RED II Annex V (SEAI consolidated)](https://www.seai.ie/sites/default/files/publications/RED-II-directive-ANNEX-V-RULES-FOR-CALCULATING-THE-GREENHOUSE-GAS-IMPACT-OF-BIOFUELS-BIOLIQUIDS-AND-THEIR-FOSSIL-FUEL-COMPARATORS.pdf) |
| RED II, palm HVO | 34% / 22% | 53% / 49% | same |
| CORSIA palm FFB HEFA core LCA | open pond ~60 g/MJ | **37.4 g/MJ** (requires ≥85% POME biogas capture) | [ICAO Doc 06, Nov 2025](https://www.icao.int/sites/default/files/environmental-protection/CORSIA/Documents/CORSIA%20Eligible%20Fuels/ICAO-document-06-Default-Life-Cycle-Emissions-November-2025.pdf); [ICCT 2021](https://theicct.org/wp-content/uploads/2021/06/Alt-aviation-fuel-sustainability-mar2021.pdf) |

- The RED II threshold is 50–65% depending on plant start date. Palm biofuel can essentially only pass on actual values with methane capture. Even then, palm counts as high-ILUC-risk (Del. Reg. 2019/807), its RED counting is being phased out by 2030, and CORSIA adds palm ILUC, which limits SAF eligibility. Methane capture is a **market-access precondition** for ISCC EU/CORSIA buyers, not a guaranteed premium.
- RSPO credits: about US$27 per t CSPO implied in 2023 (US$7m for 261,792 credits). Prices fell in 2024–25. 16.2 Mt CSPO was sold in 2025 ([Eco-Business](https://eco-business.com/news/new-sustainable-palm-oil-rules-win-consensus-amid-rspo-credit-price-slump)). RSPO P&C 2018 requires GHG reporting and favours methane capture for new mills, but there is no separate premium.
- No published "methane capture premium" in US$/t CPO was found [UNVERIFIED]. Treat an ISCC/low-GHG premium as roughly US$5–20/t only where a buyer contract exists.
- **EUDR**: Reg. (EU) 2025/2650 applies from **30 Dec 2026** for large and medium operators and from 30 Jun 2027 for micro and small ones ([Vinciworks](https://vinciworks.com/blog/eudr-delayed-again-what-changed-what-is-now-fixed-and-what-businesses-should-do-in-2026/), [Andersen](https://pl.andersen.com/en/newsletter/amendment-to-the-eudr-published-changes-to-deadlines-and-simplification-of-obligations-now-official/)). EUDR is about deforestation and traceability, not GHG, so methane capture has no direct EUDR value.

**Takeaway:** Value the market-access benefit qualitatively, or as an optional sensitivity of US$5–20/t × 52 kt = US$0.26–1.0m/yr. Do not put it in the base case.

## 4. CAPEX benchmarks

| Data point | CAPEX per MWe | Source |
|---|---|---|
| Malaysia closed digester, 60 t/h mill, ~1.8 MW: RM18–20m | ~RM10–11m/MW (~US$2.3–2.5m) | [MDPI review 2025](https://www.mdpi.com/2673-8783/6/5/77) |
| PLTBg Suka Damai, 2.4 MW: Rp109.1bn | ~Rp45bn/MW (~US$2.8m) | [ITS case study](https://iptek.its.ac.id/index.php/jsh/article/view/6775) |
| Indonesia biogas cost-recovery basis | US$1.82m/MW | [ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2666188825010172) |
| Malaysia older plants | RM9–18m/MW | MDPI (citing 2014) |

- Typical range is **US$1.8–3.0m per MWe**. Covered lagoons sit at the low end and tanks/CSTR at the high end [split UNVERIFIED].
- Tipping or treatment fees paid by mills: none found [UNVERIFIED]. The usual Indonesian and Malaysian BOO model is the reverse. The developer gets POME free, and the mill gets avoided effluent treatment, sometimes a revenue share, plus credits or power (Cenergi in Malaysia, [UEM Lestra](https://www.uemlestra.com/press-cenergi-and-ypj-plantations-enter-MoU-on-Biogas-Power-Plant.html); Malaysia FiT 2.0 at RM0.45/kWh for 10 years).

**Takeaway:** At US$1.9–2.9m for 0.96–1.6 MWe, a portable set should beat about US$2m/MW to be competitive. Do not assume a tipping fee.

## 5. Diesel use and captive power

- Start-up genset: about **0.53 L diesel/t FFB** ([ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2666789425000698)). At 250 kt FFB that is ~130 kL/yr, or about 1.5–2 kWh/t FFB at ~3.5 kWh/L.
- DSNG's 60 t/h Bio-CNG plant saves ≥2.0m L/yr of diesel previously used in mill and kernel-plant gensets ([GAPKI 2021](https://gapki.id/en/news/2021/04/03/palm-oil-mills-save-millions-liters-of-fuel-by-using-wastes/)). This indicates higher diesel use at mills with KCP or off-grid housing.
- Estate housing loads: no data found [UNVERIFIED]. A typical assumption is 0.3–1 kW per household on diesel at night.
- Diesel generation cost was Rp2,700–4,000/kWh in 2013 vs Rp700–900/kWh for POME biogas ([Jakarta Post](https://www.thejakartapost.com/news/2013/09/19/capturing-methane-electricity-generation)). At current industrial diesel prices (~Rp13–15k/L [UNVERIFIED]) it is about **Rp4,000–5,000/kWh**.
- Captive PPAs: a third-party IPP selling power on-site to a mill generally needs an IUPTL or wilayah usaha, so such arrangements are uncommon. Most mill biogas is owned by the mill, or structured as a lease/O&M or BOT [UNVERIFIED]. Historical PLN excess-power purchase was Rp1,150/kWh (Berau, 2013), capped at 85% of BPP ([IJE](https://ije-pyc.org/IJE/article/download/11/3/22)). A UI Bangka study used Rp1,575/kWh ([UI 2022](https://doi.org/10.3390/en15197265)).

**Takeaway:** Diesel displacement is worth far more per kWh (~US$0.25–0.30) than PLN export (~US$0.07–0.11). It is limited to roughly 0.4–0.6 GWh/yr of start-up and housing load, so model it as a separate revenue line. A captive PPA to a third-party mill is legally awkward. A lease or O&M service fee is the safer structure.
