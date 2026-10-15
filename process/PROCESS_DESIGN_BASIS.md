# Process Design Basis - Modular POME + EFB Biogas Generator

*Generated from `outputs/results.json` (seed 20261015, N_MC = 400). Every number below is a model output; assumptions and their provenance are in section 9.*

## 1. Product definition
A **numbered-up bank of identical mesophilic CSTR digester modules** that co-digests palm oil mill effluent (POME) with shredded empty fruit bunch (EFB) and delivers electricity and hot water to the mill. One standard module (2,000 m3 liquid) is repeated: **3 / 7 / 10 modules** serve 20 / 45 / 70 t FFB/h mills. Gas treatment, CHP, dewatering and utilities are shared equipment sized for the whole bank.

## 2. Fixed process decisions
| # | Decision | Value | Basis |
|---|---|---|---|
| 1 | Reactor type | Mesophilic CSTR, steel/glass-fused tank, double-membrane gas roof | Controllable temperature and mixing; ~half the HRT of a lagoon; module-able |
| 2 | Temperature | 38 C | Model optimum range 35-40 C; heat comes from CHP jacket |
| 3 | EFB fed to digesters | **29.3 % of mill EFB** (58.1 t wet/d) | Largest share whose P95 blend TS stays <= 8 % (feed-uncertainty Monte Carlo, P95 TS = 8.00 %) |
| 4 | EFB shredder product size | **10 mm** | Largest size within 1 % of best net energy (gas gain vs shredding energy) |
| 5 | Design HRT | **20 d** (actual 22.0 d with whole modules) | max(HRT for 92 % of asymptotic CH4 = 20 d, 4 x washout HRT 4 d = 16 d) |
| 6 | Standard module | **2,000 m3 liquid, D = 16.7 m, H = 9.2 m** | Largest catalogue size with <= 15 % overshoot in all three mill tiers and >= 4 modules at 45 t/h (N+1 operability) |
| 7 | Pre-treatment | Fine screen -> POME cooler (85 -> 39 C) -> blend tank; EFB hammer mill + conveyor | POME must be cooled to hold the blend at 38 C |
| 8 | H2S control | Bio-trickling filter (micro-air) -> gas chiller -> activated-carbon polish | 1928 ppm raw -> 23 ppm to engine |
| 9 | Power | 2 x 1,000 kWe lean-burn gas engines (CHP), jacket + exhaust heat recovery | Sized on P95 fuel of the Monte Carlo (4,648 kW) |
| 10 | Digestate | Screw press -> cake (compost / plantation) + filtrate (land application) | 85 % solids capture, 22 % DS cake |
| 11 | Stability control | pH set-point 7.0 (NaOH) and **urea-N set-point 100 mg N/L** | EFB is N-poor; without N dosing 3 % of Monte-Carlo draws starved and acidified |

## 3. Equipment list (tags are fixed for the PFD and 3D models)
| Tag | Equipment | Qty | Key size |
|---|---|---|---|
| SC-101 | Fine screen (POME) | 1 | 24 m3/h |
| E-101 | POME plate cooler (to cooling water) | 1 | 1,300 kWth, 85 -> 39 C |
| SH-101 | EFB hammer mill / shredder | 1 | 2.9 t/h, 19 kW, 10 mm |
| CV-101 | EFB screw / belt conveyor | 1 | 2.9 t/h |
| TK-101 | Blend / buffer tank (mixed) | 1 | 106 m3 (4 h) |
| P-201 | Digester feed pumps (progressive cavity) | 7+1 | 26.6 m3/h total, 25 m head |
| R-201..R-207 | Digester modules (CSTR, insulated, membrane roof) | 7 | 2,000 m3 liquid, D 16.7 m, H 9.2 m, dome 4.0 m, gas buffer 467 m3 |
| MX-201.. | Side-entry / top-entry mixers | 2 per module | 12 kW per module (6 W/m3) |
| TK-201 | NaOH dosing tank + pump | 1 | P95 207 kg NaOH/d |
| TK-202 | Urea-N dosing tank + pump | 1 | P95 57 kg N/d |
| BTF-301 | Bio-trickling filter (desulfurizer) | 1 | 755 Nm3/h gas, 25 m3 packing (120 s EBCT), air 5.8 Nm3/h |
| K-301 | Air blower to BTF | 1 | 5.8 Nm3/h |
| HX-301 | Gas chiller + condensate pot | 1 | 23 kWth, 5 C dew point |
| K-302 | Biogas blower | 1+1 | 822 m3/h, 20 kPa |
| AC-301 | Activated-carbon polishing filter | 1 | 3.6 kg H2S/d |
| FL-301 | Enclosed flare | 1 | 900 Nm3/h |
| GE-401/402 | CHP gas engine-generators (containerised) | 2 | 1,000 kWe each |
| HX-401 | Exhaust heat recovery boiler / hot-water exchanger | 1 | exhaust to 150 C |
| PR-501 | Screw press (digestate dewatering) | 1 | 26.6 m3/h, 77 t/d cake |
| CT-601 | Cooling tower | 1 | 1,330 kWth |

## 4. Design-basis operating point (45 t FFB/h x 20 h, nameplate)
| Item | Value |
|---|---|
| POME | 585 m3/d |
| EFB to digesters | 58.1 t/d |
| Blend | 637 m3/d, TS 6.7 %, COD 89 kg/m3 |
| Digester state | pH 7.00, VFA 32 mg/L, FOS/TAC 0.013, TAN 106 mg N/L |
| Biogas | 18,125 Nm3/d, CH4 57.1 %, raw H2S 1,928 ppm |
| COD to methane | 52 % of blend COD (32 % non-degradable lignin/inerts) |
| Electricity | gross 1,667 kWe, parasitic 224 kWe, **net 1,443 kWe**, mill demand 945 kW, surplus 498 kWe |
| Heat | CHP 2,119 kWth, digesters 49 kWth, to mill 2,071 kWth; POME cooling rejected 1,330 kWth |
| CHP | 2 of 2 engines at 85 % load, eta_el 38.9 %, exhaust 464 C (from energy balance) |

## 5. Uncertainty (Latin-hypercube Monte Carlo, N = 400; P5 / P50 / P95; mill load factor 0.92 +/- 0.07)
| Output | P5 / P50 / P95 |
|---|---|
| Biogas, Nm3/d | 13,250 / 16,422 / 19,632 |
| CH4 fraction | 0.560 / 0.572 / 0.588 |
| COD removal | 0.484 / 0.524 / 0.564 |
| Gross power, kWe | 1,177 / 1,498 / 1,822 |
| Net power, kWe | 988 / 1,286 / 1,590 |
| Surplus after mill demand, kWe | 182 / 423 / 683 |
| Raw H2S, ppm | 803 / 1,749 / 3,358 |
| Urea-N dosing, kg N/d | 0 / 0 / 57 |
| Probability of digester upset | 0.0 % |

## 6. Scalability (same module)
| Mill | Modules | Digester volume | Biogas Nm3/d | Net kWe | Net GWh/y (300 d) |
|---|---|---|---|---|---|
| 20 t FFB/h | 3 | 6,000 m3 | 8,020 | 629 | 4.5 |
| 45 t FFB/h | 7 | 14,000 m3 | 18,125 | 1,443 | 10.4 |
| 70 t FFB/h | 10 | 20,000 m3 | 27,901 | 2,238 | 16.1 |

## 7. Mass-balance closure (relative error)
| Check | Error |
|---|---|
| digester_mass | 3.1e-06 |
| digester_C | 3.8e-05 |
| digester_H | 1.2e-06 |
| digester_O | 1.4e-06 |
| digester_N | -2.4e-04 |
| digester_S | -5.3e-04 |
| dewatering_mass | 0.0e+00 |
| btf_S | 0.0e+00 |
| btf_C | 1.4e-16 |
| chp_mass | 1.5e-10 |
| chp_C | 0.0e+00 |
| chp_H | -1.2e-16 |
| chp_O | 1.1e-16 |
| chp_N | 0.0e+00 |
| chp_S | 0.0e+00 |
| blend_consistency | 1.8e-16 |
| plant_mass | 2.3e-06 |
| COD_digester | 3.5e-05 |

## 8. Stream table (kg/h, design basis)
| No. | Stream | T, C | P, bar | Phase | Total kg/h |
|---|---|---|---|---|---|
| 1 | POME mentah dari pabrik | 85 | 1.30 | C | 24,375 |
| 2 | TKKS mentah ke digester | 27 | 1.01 | PB | 2,434 |
| 3 | Residu saringan | 85 | 1.01 | P | 70 |
| 4 | POME tersaring | 85 | 1.30 | C | 24,305 |
| 5 | POME didinginkan | 39 | 1.20 | C | 24,305 |
| 6 | TKKS tercacah | 27 | 1.01 | PB | 2,434 |
| 7 | Umpan campuran POME+TKKS | 38 | 2.00 | B | 26,739 |
| 8 | Larutan alkali (NaOH) | 27 | 2.00 | C | 1 |
| 9 | Biogas mentah (jenuh uap, 38 C) | 38 | 1.02 | G | 986 |
| 10 | Digestat dari digester | 38 | 1.50 | CP | 25,753 |
| 11 | Udara ke bio-desulfurisasi | 27 | 1.20 | G | 7 |
| 12 | Biogas keluar BTF (30 C) | 30 | 1.05 | G | 975 |
| 13 | Lumpur belerang / blowdown BTF | 30 | 1.01 | CP | 19 |
| 14 | Kondensat chiller | 5 | 1.01 | C | 21 |
| 15 | Biogas bersih ke CHP (5 C) | 20 | 1.15 | G | 954 |
| 16 | Karbon aktif jenuh (H2S) | 27 | 1.01 | P | 0 |
| 17 | Udara pembakaran CHP | 27 | 1.10 | G | 9,535 |
| 18 | Gas buang CHP (setelah pemulihan panas) | 150 | 1.01 | G | 10,489 |
| 19 | Kue digestat | 38 | 1.01 | PB | 3,224 |
| 20 | Filtrat (efluen cair) | 38 | 1.01 | C | 22,532 |
| 21 | Polimer flokulan | 27 | 1.01 | C | 3 |
| 22 | Gas ke flare (kelebihan/darurat) | 20 | 1.10 | G | 0 |
| 23 | Nutrien nitrogen (urea, dihitung sbg N) | 27 | 2.00 | C | 0 |

Component split of every stream is in `results.json -> streams[].comp`.

## 9. Model basis and provenance
* Biology: reduced ADM1, 30 states. Hydrolysis (first order), acidogenesis, acetogenesis, aceto- and hydrogenotrophic methanogenesis, acetate/H2 sulfate reduction; pH, free NH3, free H2S, LCFA, H2 inhibition; charge-balance pH; quasi-steady headspace with Henry-law transfer.
* Stoichiometry for CO2, H2O, NH3 and sulfate is generated from chemical formulas by element balance (residual 3e-17).
* Calibrated at run time to literature BMPs (POME 397, EFB 264 NmL CH4/g VS): fitted POME BMP 405, EFB BMP 267; calibrated k_cel_ref = 0.031 1/d, shielding beta = 0.68, POME refractory COD = 20 %.
* Parameter provenance tags: `[LIT-S]` found by literature search in this project, `[ADM1]` Batstone et al. (2002) defaults, `[ASSUME]` engineering assumption to be replaced with site/vendor data, `[CALIB]` fitted. Full table: `results.json -> assumptions`.

## 10. Limitations and open items
* Feed ranges are literature-based, not site-measured; replacing POME composition, EFB composition and flow with one real mill data set is the highest-value upgrade.
* EFB hydrolysis rate and recalcitrant fraction are only constrained by one literature BMP (30 d); they are the main structural uncertainty for continuous operation.
* Sulfide-inhibition constants, SRB kinetics, part-load engine curve, heat-exchanger/cooling-tower and electricity-per-tonne figures are `[ASSUME]`.
* Economics in `results.json -> economics_screen` use placeholder unit costs - not for decisions until vendor quotes replace them.
* Full EFB co-digestion in continuous CSTRs at this scale has pilot, not commercial, precedent; POME-only biogas CHP is the proven reference case.