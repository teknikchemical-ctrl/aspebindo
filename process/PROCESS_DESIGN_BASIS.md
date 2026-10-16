# Process Design Basis - Rev 2: Relocatable Thermophilic Anaerobic Contact Biogas Set (POME)

*Generated from `outputs/results.json` (seed 20261015, N_MC = 400). Rev 2 follows the Stage 1 technical red-team against the literature (`research/R4_technical_evidence.md`).*

## 1. Product
A **relocatable biogas power set for palm oil mills of 30-60 t FFB/h**. Hot POME (85 C) is digested at **55 C in a thermophilic anaerobic contact process**: completely mixed reactors, a vacuum degasser and a lamella settler that returns the sludge, so solids stay 12 d while the liquid passes in 5.0 d (at the nameplate day). The reactors are **standard bolted glass-fused-to-steel (GFS) tanks (D 11.46 m, 980 m3)** that ship flat-packed in 40 ft containers and can be dismantled and re-erected at the next mill: **2 / 3 / 4 tanks** for 30 / 45 / 60 t FFB/h. Everything else ships in containers or container-size skids (21 loads, about 254 t for 45 t FFB/h).

## 2. Stage 1 red-team: what changed from Rev 1 and why

| # | Finding (research/R4) | Rev 1 | Rev 2 action | Result |
|---|---|---|---|---|
| 1 | Membrane cross-flow loop undersized; flux 15 LMH optimistic (lit. 3-14) | 996 m2, 22 kW | Re-sized option at 8 LMH, 3 kWh/m3 (gas-lift) | 2,026 m2, 49 kW for +91 Nm3 CH4/d (+15 kWe gross): membrane dropped from base case |
| 2 | Membrane adds little methane; no full-scale POME AnMBR exists | AnMBR | Thermophilic contact process (degasser + lamella + recycle) | SRT 12 d at 4 kW extra; FOS/TAC 0.04 |
| 3 | 4.2 m vessels on low-bed are ~5.1 m high > 4.2 m road limit | 14 shop vessels | Bolted GFS tanks shipped as panels | 3 tanks, 2 containers each, no oversize loads |
| 4 | Design flow 585 m3/d is the nameplate day; annual average lower | util 0.92, 300 d x 24 h | util 0.75 (annual), Sundays off, 14 d shutdown, seasonal +/-25 % | 5.27 GWh/y net (annual simulation) |
| 5 | CHP oversized (68 % mean load) | 2 x 800 kWe on P95 | Sized on nameplate-day fuel | 2 x 600 kWe |
| 6 | '68 % COD removal' is the methanised fraction, not treatment removal | one number | Report both | CH4 68 % of COD; COD load to ponds -84 % |
| 7 | Permeate COD 7.3 g/L inconsistent with VFA 85 mg/L | sI 4 % of COD | sI 2.5 % (AD effluent soluble COD 1.5-4 g/L) | soluble COD 3,525 mg/L |
| 8 | Effluent cannot meet PermenLH 5/2014 river limits | implied compliance | Effluent to existing polishing ponds -> land application | COD 8,391, BOD 1,543 mg/L (land application <= 5,000 BOD: yes) |
| 9 | Nitrogen dosing unnecessary (POME TKN ~750 mg/L) | urea to 100 mg N/L | Safety floor 50 mg N/L, raw TAN 70 mg/L | TAN 180 mg N/L, dosing P95 0 kg N/d |
| 10 | Grit removal 60 % too low; polymer 4 kg/t DS optimistic | 60 %, 4 kg/t | 85 %, 8 kg/t DS, cake 20 % DS | cake 18.9 t/d |
| 11 | Carbon: uncertainty factor missing | MCF 0.8, no UF | AMS-III.H UF 0.89, degasser recovers 70 % dissolved CH4 | 24,025 tCO2e/y (0.119 t/t FFB) |
| 12 | BMP '397 NmL CH4/g COD' impossible (> 350) | label | Label fixed: per g VS | - |

Residual risks not closed by modelling: thermophilic VFA may run 200-800 mg/L in practice (model 85 mg/L); oleate inhibition at 55 C; start-up 2-4 months (finance uses a 75 % first-year factor); settler capture 85 % assumed (pilot to confirm).

## 3. Technology comparison (model, same 45 t FFB/h nameplate feed)

| Case | Reactor volume m3 | HRT / SRT d | OLR kg COD/m3.d | CH4 Nm3/d | Nm3 CH4 per m3.d | MLSS g/L | FOS/TAC |
|---|---|---|---|---|---|---|---|
| A  Mesofilik CSTR + TKKS 29% (Rev0) | 14,023 | 22.0 / 22.0 | 4.0 | 10,359 | 0.74 | 29.3 | 0.01 |
| B  Mesofilik CSTR, POME | 11,700 | 20.0 / 20.0 | 2.5 | 6,873 | 0.59 | 10.3 | 0.02 |
| C  Termofilik CSTR, POME | 2,925 | 5.0 / 5.0 | 9.9 | 6,413 | 2.19 | 11.3 | 0.14 |
| D  Termofilik kontak, POME (dipilih) | 2,925 | 5.0 / 12.0 | 9.9 | 6,919 | 2.37 | 24.1 | 0.04 |
| E  Termofilik AnMBR (opsi) | 2,925 | 5.0 / 15.0 | 9.9 | 7,010 | 2.40 | 29.3 | 0.03 |

* POME arrives at 75-95 C, so 55 C operation needs **no heating**: the feed is only cooled, and its residual heat covers the reactor losses.
* The contact process gets most of the membrane's benefit (biomass retention, stability margin) for a lamella settler and two pumps; the AnMBR remains an option (PM-11) for water-reuse sites.
* Literature anchors: thermophilic CSTR on POME stable at HRT 5 d, OLR 17 (Choorit & Wisarnwan, 2007); thermophilic AnMBR on POME flux ~3 LMH (Membranes, 2019); full-scale ADI-MBR 2.5-4.2 LMH.

## 4. Fixed design decisions
| # | Decision | Value | Basis |
|---|---|---|---|
| 1 | Reactor | Thermophilic anaerobic contact: CSTR (jet mixing) + vacuum degasser + lamella settler + sludge recycle | Stage 1 red-team; no membrane in base case |
| 2 | Temperature | 55 C | Hot POME; ADM1 thermophilic set |
| 3 | HRT / SRT | 5.0 d at nameplate (6.7 d annual mean) / 12 d | Longest SRT with MLSS <= 25 g/L (settler), OLR <= 15, FOS/TAC <= 0.3 |
| 4 | Reactor tank | Bolted GFS, D 11.46 m, liquid 9.5 m, 980 m3, 140 panels | Standard size: 2/3/4 tanks for 30/45/60 t FFB/h within +-15 % |
| 5 | Settler | Lamella 81 m2 projected at 0.6 m3/m2.h; recycle 585 m3/d; capture 85 % | [ASSUME] pilot to confirm |
| 6 | Pre-treatment | Rotary screen + grit chamber/hydrocyclone (85 %) + plate cooler (85 -> 56 C) | Sand accumulates SRT/HRT times |
| 7 | Biogas cleaning | Bio-trickling filter (95 %) -> chiller 5 C -> blower -> carbon guard bed | 2,868 ppm raw -> 21 ppm H2S (engine limit 100-200) |
| 8 | Gas storage | Double-membrane gas holder 986 m3 (2 h) | Smooths the 20 h/d mill feed |
| 9 | Power | 2 x 600 kWe containerised gas engines | Nameplate-day fuel 2,867 kW |
| 10 | Effluent | Settler overflow + press filtrate -> existing polishing ponds -> land application | PermenLH 5/2014 river limits not met by AD alone |
| 11 | Stability control | pH 7.0 (NaOH), level, temperature, FOS/TAC titration daily | Monte Carlo upset probability 0.0 % |

## 5. Relocatable module set (45 t FFB/h)

| Module | Content | Qty | Shipping | Mass t |
|---|---|---|---|---|
| PM-1 Skid praolah POME | rotary screen, grit chamber + hydrocyclone (85 % grit), plate cooler 827 kWth | 1 | kontainer 40 ft (skid) | 12.0 |
| PM-2 Tangki GFS penyangga umpan | D 5.73 m, 116 m3, 35 panel | 1 | panel GFS dalam kontainer 40 ft | 10.8 |
| PM-3 Reaktor kontak termofilik (tangki GFS dibaut) | D 11.46 m x H 10.8 m, 980 m3, 55 C, jet mixing, atap membran ganda; 140 panel/tangki, 2 kontainer/tangki | 3 | panel GFS dalam kontainer 40 ft | 113.8 |
| PM-4 Skid kontak: degasser vakum + settler lamella + pompa resirkulasi | lamella 81 m2 proyeksi pada 0.6 m3/m2.jam, resirkulasi 585 m3/d, underflow x1.58 | 1 | 2 skid 40 ft | 18.0 |
| PM-5 Skid dosing dan pompa umpan | feed pumps, NaOH dosing (urea-N standby only) | 1 | skid 20 ft | 8.0 |
| PM-6 Skid pengolahan biogas | 493 Nm3/h; BTF 16 m3 packing ships as its own vessel | 1 | kontainer 40 ft + bejana BTF | 14.0 |
| PM-7 Penampung gas + flare | double-membrane gas holder 986 m3 (2 h), flare 542 Nm3/h | 1 | kontainer 20 ft (membran terlipat) + skid flare | 7.0 |
| PM-8 Kontainer CHP | 600 kWe biogas engine-generator per container | 2 | kontainer 40 ft HC | 40.0 |
| PM-9 Skid pemulih panas + menara pendingin | hot-water recovery 1405 kWth; cooling 847 kWth | 1 | skid 20 ft + sel CT modular | 9.0 |
| PM-10 Tangki GFS efluen + skid lumpur | effluent tank D 6.88 m; screw press 110 m3/d waste underflow -> 18.9 t/d cake | 1 | panel GFS + skid 20 ft | 21.3 |
| PM-11 (opsi) Kontainer membran AnMBR (opsional, reuse air) | tidak termasuk kasus dasar: +91 Nm3 CH4/d (+15 kWe kotor) vs 49 kW cross-flow | 2 | kontainer 40 ft | - |

**Total: 21 truck/container loads, about 254 t; plot about 0.24 ha** (perkiraan rumus). Planning estimates.

## 6. Operating points
| Item | Nameplate day (equipment sizing) | Annual average (finance) |
|---|---|---|
| FFB | 45 t/h x 20 h = 900 t/d | 202,500 t/y (util 0.75, ~300 d) |
| POME | 585 m3/d, COD 50 kg/m3 | 131,625 m3/y |
| Reactor | pH 7.12, VFA 85 mg/L, FOS/TAC 0.042, TAN 180 mg N/L, MLSS 24.0 g/L, OLR 9.9 | MC P50 MLSS 17.7 g/L |
| Biogas | 11,836 Nm3/d, CH4 58.5 % | MC P50 8,627 Nm3/d |
| Electricity | gross 1,127, parasitic 102, **net 1,025 kWe** | **5.27 GWh/y net** (gross 5.92) |
| Heat | POME cooling 827 kWth rejected; CHP hot water 1,405 kWth | - |
| Effluent to ponds | 544 m3/d: COD 8,391 (soluble 3,525), BOD 1,543, TSS 3,903, TN 342 mg/L | - |
| Sludge cake | 18.9 t/d (20 % DS) | - |
| Methane avoided | - | **24,025 tCO2e/y** (AMS-III.H, GWP 28, UF 0.89) |

## 7. Uncertainty (Monte Carlo N = 400 at annual-average util; P5 / P50 / P95)
| Output | P5 / P50 / P95 |
|---|---|
| Biogas, Nm3/d | 6,485 / 8,627 / 11,518 |
| Net power, kWe | 507 / 708 / 979 |
| Reactor MLSS, g/L | 13.4 / 17.7 / 22.6 |
| OLR, kg COD/m3.d | 5.5 / 7.3 / 9.5 |
| FOS/TAC | 0.028 / 0.046 / 0.076 |

## 8. Scalability
| Mill | GFS tanks | Net kWe (nameplate) | Net GWh/y (annual) | CHP |
|---|---|---|---|---|
| 30 t FFB/h | 2 | 681 | 3.50 | 2 x 400 kWe |
| 45 t FFB/h | 3 | 1,025 | 5.27 | 2 x 600 kWe |
| 60 t FFB/h | 4 | 1,369 | 7.04 | 2 x 800 kWe |

## 9. Closure (relative error)
| Check | Error |
|---|---|
| reactor_mass | 2.3e-06 |
| reactor_C | 5.5e-05 |
| reactor_H | 1.2e-06 |
| reactor_O | 1.2e-06 |
| reactor_N | 5.3e-06 |
| reactor_S | -1.6e-05 |
| settler_mass | -8.9e-17 |
| dewatering_mass | 1.3e-16 |
| chp_mass | 1.4e-10 |
| chp_C | 0.0e+00 |
| chp_H | 0.0e+00 |
| chp_O | 0.0e+00 |
| chp_N | 0.0e+00 |
| chp_S | 0.0e+00 |
| plant_mass | 1.8e-06 |
| COD_reactor | 5.1e-05 |

## 10. Limitations
* Thermophilic ADM1 ratios, settler capture and the solids limit are literature-typical, not pilot data; a pilot on real POME is the key validation step.
* POME composition is literature-based; one real mill data set would tighten every number.
* Net power during processing hours is about the mill's own demand, but the mill keeps its fibre/shell turbine, so the power is sold (diesel displacement at the mill, PLN export). The business case is in `finance/` (Mill Decision Model: status-quo ponds vs alternatives vs this BOO service).