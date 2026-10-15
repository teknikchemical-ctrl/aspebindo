# Process Design Basis - Rev 1: Portable Thermophilic AnMBR Biogas Generator (POME)

*Generated from `outputs/results.json` (seed 20261015, N_MC = 400). Rev 0 (mesophilic CSTR with EFB co-digestion) is kept as comparison case A.*

## 1. Product
A **portable, shop-built biogas power plant for palm oil mills of 30-60 t FFB/h** (the common sizes in Sumatra). Hot POME (85 C) is digested at **55 C in a thermophilic anaerobic membrane bioreactor (AnMBR)**: an external tubular ultrafiltration loop retains the biomass and solids (SRT 12 d) while the liquid passes in 4.5 d. This makes the reactor 5.2x smaller than the Rev 0 mesophilic design, so it fits in **one standard road-transportable vessel (D 4.2 m, 194 m3)** that is numbered up: **10 / 14 / 19 vessels** for 30 / 45 / 60 t FFB/h. Everything else ships in 40 ft containers or container-size skids.

## 2. Why this technology (model results, same 45 t FFB/h feed)

| Case | Reactor volume m3 | HRT / SRT d | OLR kg COD/m3.d | CH4 Nm3/d | Nm3 CH4 per m3.d | MLSS g/L |
|---|---|---|---|---|---|---|
| A  Mesofilik CSTR + TKKS 29% (Rev0) | 14,023 | 22.0 / 22.0 | 4.0 | 10,347 | 0.74 | 29.3 |
| B  Mesofilik CSTR, POME | 11,700 | 20.0 / 20.0 | 2.5 | 6,862 | 0.59 | 10.3 |
| C  Termofilik CSTR, POME | 2,925 | 5.0 / 5.0 | 10.0 | 6,403 | 2.19 | 11.3 |
| D  Termofilik AnMBR, POME (dipilih) | 2,632 | 4.5 / 12.0 | 11.1 | 6,907 | 2.62 | 26.8 |

* POME arrives at 75-95 C, so 55 C operation needs **no heating**: the feed is only cooled, and its residual heat covers the reactor losses.
* Thermophilic kinetics (ADM1 thermophilic parameter set) plus membrane solids retention raise volumetric productivity about 4x over Rev 0.
* EFB co-digestion is **dropped** from the portable product: in Rev 0, EFB (32 % non-degradable lignin, hydrolysis k ~0.03 1/d) set most of the reactor volume. EFB stays with the mill (mulch / boiler).
* Literature anchors: thermophilic CSTR on POME reached 17 kg COD/m3.d at HRT 5 d (Choorit & Wisarnwan, 2007); a 55 C AnMBR on palm oil wastewater held 93-98 % COD removal at 2-10 kg COD/m3.d (Membranes, 2019); Kubota markets a membrane-based compact POME biogas system; containerised 600 kW biogas gensets run at the Sei Pelakar mill in Sumatra (Guascor).

## 3. Fixed design decisions
| # | Decision | Value | Basis |
|---|---|---|---|
| 1 | Reactor | Thermophilic AnMBR, CSTR with jet mixing + external tubular UF | Volume, effluent quality, biomass retention |
| 2 | Temperature | 55 C | Hot POME; ADM1 thermophilic set |
| 3 | HRT / SRT | 4.5 d / 12 d (actual HRT 4.64 d) | Smallest volume with MLSS <= 85 % of 35 g/L, OLR <= 15 kg COD/m3.d, FOS/TAC <= 0.3, CH4 >= 95 % of best (HRT x SRT grid) |
| 4 | Standard vessel | D 4.2 m, liquid height 14.0 m, 194 m3; ships 17.3 m long | Largest road-transportable vessel with <= 15 % overshoot in all three mill sizes |
| 5 | Pre-treatment | Rotary screen + hydrocyclone desander + plate cooler (85 -> 56 C) | Grit would accumulate SRT/HRT times in the membrane loop |
| 6 | Membrane | 996 m2 tubular UF at 15 LMH, 34 modules, 22 kWe | External cross-flow handles 20-40 g/L solids |
| 7 | Biogas cleaning | Bio-trickling filter -> chiller 5 C -> blower -> activated carbon | 2,887 ppm raw -> 34 ppm H2S to engine |
| 8 | Gas storage | Double-membrane gas holder 1,135 m3 (2 h at P95) | Smooths the 20 h/d mill feed |
| 9 | Power | 2 x 800 kWe containerised gas engines | Sized on P95 fuel 3,252 kW |
| 10 | Stability control | pH 7.0 (NaOH), urea-N >= 100 mg N/L, level and temperature control on every vessel | Monte Carlo upset probability 0.0 % |

## 4. Portable module set (45 t FFB/h)

| Module | Content | Qty | Shipping | Mass t |
|---|---|---|---|---|
| PM-1 Skid praolah POME | rotary screen, hydrocyclone desander, plate cooler 812 kWth | 1 | kontainer 40 ft (skid) | 12.0 |
| PM-2 Bejana standar: tangki penyangga umpan | same 194 m3 vessel as the reactors, 8.0 h hold-up | 1 | bejana di trailer low-bed | 19.0 |
| PM-3 Bejana standar: reaktor AnMBR termofilik | D 4.2 m x H 15.2 m, 194 m3, 55 C, jet mixing; ships 17.3 m long | 14 | bejana di trailer low-bed | 266.0 |
| PM-4 Kontainer membran + CIP | 996 m2 tubular UF, 34 modules, cross-flow 149 m3/h | 1 | kontainer 40 ft HC | 16.0 |
| PM-5 Skid dosing dan pompa umpan | feed pumps, NaOH and urea-N dosing | 1 | skid 20 ft | 8.0 |
| PM-6 Skid pengolahan biogas | 492 Nm3/h; BTF 16 m3 packing ships as its own vessel | 1 | kontainer 40 ft + bejana BTF | 14.0 |
| PM-7 Penampung gas + flare | double-membrane gas holder 1135 m3 (2 h), flare 624 Nm3/h | 1 | kontainer 20 ft (membran terlipat) + skid flare | 7.0 |
| PM-8 Kontainer CHP | 800 kWe biogas engine-generator per container | 2 | kontainer 40 ft HC | 48.0 |
| PM-9 Skid pemulih panas + menara pendingin | hot-water recovery 1439 kWth; cooling 832 kWth | 1 | skid 20 ft + sel CT modular | 9.0 |
| PM-10 Bejana standar: tangki permeat + skid lumpur | permeate tank (same vessel), screw press 226.3 m3/d waste sludge | 1 | bejana + skid 20 ft | 27.0 |

**Total: 28 truck loads, about 426 t; plot about 0.29 ha** (Rev 0: 0.39 ha). Planning estimates.

## 5. Design-basis operating point (45 t FFB/h x 20 h)
| Item | Value |
|---|---|
| POME | 585 m3/d at 85 C, COD 50 kg/m3 |
| Reactor state | pH 7.10, VFA 84 mg/L, FOS/TAC 0.043, TAN 153 mg N/L, MLSS 25.9 g/L, OLR 10.7 kg COD/m3.d |
| Biogas | 11,815 Nm3/d, CH4 58.5 % (6,907 Nm3 CH4/d) |
| Electricity | gross 1,088 kWe, parasitic 127, **net 961 kWe**, mill demand 945 kW |
| Heat | POME cooling 812 kWth rejected; CHP hot water 1,439 kWth available |
| Effluent | permeate + filtrate; waste sludge 226.3 m3/d -> 22.8 t/d cake |
| Methane avoided | 36,777 tCO2e/y vs open ponds (IPCC defaults) |

## 6. Uncertainty (Monte Carlo N = 400, mill load 0.92 +/- 0.07; P5 / P50 / P95)
| Output | P5 / P50 / P95 |
|---|---|
| Biogas, Nm3/d | 8,001 / 10,527 / 13,615 |
| Net power, kWe | 646 / 845 / 1,123 |
| Surplus over mill demand, kWe | -215 / -20 / 225 |
| Reactor MLSS, g/L | 18.5 / 23.5 / 29.6 |
| OLR, kg COD/m3.d | 7.5 / 9.6 / 12.2 |
| Urea-N, kg N/d | 0 / 0 / 31 |

## 7. Scalability
| Mill | Reactor vessels | Net kWe | Net GWh/y | CHP |
|---|---|---|---|---|
| 30 t FFB/h | 10 | 627 | 4.5 | 2 x 600 kWe |
| 45 t FFB/h | 14 | 961 | 6.9 | 2 x 800 kWe |
| 60 t FFB/h | 19 | 1,311 | 9.4 | 3 x 600 kWe |

## 8. Closure (relative error)
| Check | Error |
|---|---|
| reactor_mass | 2.5e-06 |
| reactor_C | 5.2e-05 |
| reactor_H | 1.1e-06 |
| reactor_O | 1.1e-06 |
| reactor_N | 7.0e-06 |
| reactor_S | -1.5e-05 |
| membrane_loop_mass | -3.0e-17 |
| dewatering_mass | 0.0e+00 |
| chp_mass | 2.2e-10 |
| chp_C | 0.0e+00 |
| chp_H | 0.0e+00 |
| chp_O | -1.7e-16 |
| chp_N | 0.0e+00 |
| chp_S | 0.0e+00 |
| plant_mass | 1.9e-06 |
| COD_reactor | 4.7e-05 |

## 9. Limitations
* Thermophilic ADM1 parameter ratios and membrane flux / energy / solids limit are literature-typical values, not pilot data; a pilot AnMBR on real POME is the single most important validation step.
* POME composition is literature-based; one real mill data set would tighten every number.
* With POME only, net power about equals the mill's own demand; the business case is diesel/grid displacement plus methane credits, not export.
* Economics (`economics_screen`) use placeholder costs.