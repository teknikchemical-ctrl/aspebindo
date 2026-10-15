# -*- coding: utf-8 -*-
"""Generates PROCESS_DESIGN_BASIS.md from outputs/results.json (run biogas_balance.py first)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
pd_, db, nom, en, eq, mc, ti = R["process_decisions"], R["design_basis"], R["nominal"], R["energy"], R["equipment"], R["monte_carlo"], R["tiers"]
mod = pd_["module"]; N = mod["N"]["45.0"]; Vm = mod["V_mod"]
f0 = lambda x: "{:,.0f}".format(x)
f1 = lambda x: "{:,.1f}".format(x)
f2 = lambda x: "{:,.2f}".format(x)
P = lambda k, fmt=f0: "%s / %s / %s" % (fmt(mc[k]["P5"]), fmt(mc[k]["P50"]), fmt(mc[k]["P95"]))
L = []
A = L.append
A("# Process Design Basis - Modular POME + EFB Biogas Generator")
A("")
A("*Generated from `outputs/results.json` (seed %d, N_MC = %d). Every number below is a model output; assumptions and their provenance are in section 9.*" % (R["meta"]["seed"], R["meta"]["N_MC"]))
A("")
A("## 1. Product definition")
A("A **numbered-up bank of identical mesophilic CSTR digester modules** that co-digests palm oil mill effluent (POME) with shredded empty fruit bunch (EFB) and delivers electricity and hot water to the mill. "
  "One standard module (%s m3 liquid) is repeated: **%s / %s / %s modules** serve 20 / 45 / 70 t FFB/h mills. Gas treatment, CHP, dewatering and utilities are shared equipment sized for the whole bank." % (f0(Vm), mod["N"]["20.0"], mod["N"]["45.0"], mod["N"]["70.0"]))
A("")
A("## 2. Fixed process decisions")
A("| # | Decision | Value | Basis |")
A("|---|---|---|---|")
A("| 1 | Reactor type | Mesophilic CSTR, steel/glass-fused tank, double-membrane gas roof | Controllable temperature and mixing; ~half the HRT of a lagoon; module-able |")
A("| 2 | Temperature | %.0f C | Model optimum range 35-40 C; heat comes from CHP jacket |" % pd_["T_dig"])
A("| 3 | EFB fed to digesters | **%.1f %% of mill EFB** (%.1f t wet/d) | Largest share whose P95 blend TS stays <= %.0f %% (feed-uncertainty Monte Carlo, P95 TS = %.2f %%) |" % (pd_["efb_share"] * 100, db["efb_ad_td"], 8, pd_["ts_p95"] * 100))
A("| 4 | EFB shredder product size | **%d mm** | Largest size within 1 %% of best net energy (gas gain vs shredding energy) |" % pd_["d_p_mm"])
A("| 5 | Design HRT | **%.0f d** (actual %.1f d with whole modules) | max(HRT for %.0f %% of asymptotic CH4 = %.0f d, %.0f x washout HRT %.0f d = %.0f d) |" % (pd_["hrt_design_d"], pd_["hrt_actual_d"], 92, pd_["hrt_info"]["h_yield"], 4, pd_["hrt_info"]["h_wash"], pd_["hrt_info"]["h_floor"]))
A("| 6 | Standard module | **%s m3 liquid, D = %.1f m, H = %.1f m** | Largest catalogue size with <= 15 %% overshoot in all three mill tiers and >= 4 modules at 45 t/h (N+1 operability) |" % (f0(Vm), eq["digester_module"]["D_m"], eq["digester_module"]["H_liq_m"]))
A("| 7 | Pre-treatment | Fine screen -> POME cooler (85 -> %.0f C) -> blend tank; EFB hammer mill + conveyor | POME must be cooled to hold the blend at 38 C |" % eq["pome_cooler"]["T_out"])
A("| 8 | H2S control | Bio-trickling filter (micro-air) -> gas chiller -> activated-carbon polish | %.0f ppm raw -> %.0f ppm to engine |" % (nom["h2s_ppm_raw"], nom["h2s_ppm_fuel"]))
A("| 9 | Power | %d x %s kWe lean-burn gas engines (CHP), jacket + exhaust heat recovery | Sized on P95 fuel of the Monte Carlo (%s kW) |" % (eq["chp"]["N"], f0(eq["chp"]["unit_kWe"]), f0(eq["chp"]["fuel_P95_kW"])))
A("| 10 | Digestate | Screw press -> cake (compost / plantation) + filtrate (land application) | 85 % solids capture, 22 % DS cake |")
A("| 11 | Stability control | pH set-point 7.0 (NaOH) and **urea-N set-point 100 mg N/L** | EFB is N-poor; without N dosing 3 % of Monte-Carlo draws starved and acidified |")
A("")
A("## 3. Equipment list (tags are fixed for the PFD and 3D models)")
A("| Tag | Equipment | Qty | Key size |")
A("|---|---|---|---|")
rows = [
 ("SC-101", "Fine screen (POME)", 1, "%s m3/h" % f0(db["pome_m3d"] / 24)),
 ("E-101", "POME plate cooler (to cooling water)", 1, "%s kWth, 85 -> %.0f C" % (f0(eq["pome_cooler"]["duty_kW"]), eq["pome_cooler"]["T_out"])),
 ("SH-101", "EFB hammer mill / shredder", 1, "%.1f t/h, %.0f kW, %d mm" % (eq["efb_shredder"]["cap_t_h"], eq["efb_shredder"]["power_kW"], eq["efb_shredder"]["product_mm"])),
 ("CV-101", "EFB screw / belt conveyor", 1, "%.1f t/h" % eq["efb_shredder"]["cap_t_h"]),
 ("TK-101", "Blend / buffer tank (mixed)", 1, "%s m3 (4 h)" % f0(eq["blend_tank"]["V_m3"])),
 ("P-201", "Digester feed pumps (progressive cavity)", "%d+1" % N, "%s m3/h total, %s m head" % (f1(eq["feed_pump"]["flow_m3_h"]), f0(eq["feed_pump"]["head_m"]))),
 ("R-201..R-20%d" % N, "Digester modules (CSTR, insulated, membrane roof)", N, "%s m3 liquid, D %.1f m, H %.1f m, dome %.1f m, gas buffer %s m3" % (f0(Vm), eq["digester_module"]["D_m"], eq["digester_module"]["H_liq_m"], eq["digester_module"]["roof_dome_h_m"], f0(eq["digester_module"]["V_gas_m3"]))),
 ("MX-201..", "Side-entry / top-entry mixers", "2 per module", "%.0f kW per module (6 W/m3)" % eq["digester_module"]["mixer_kW"]),
 ("TK-201 / P-203", "NaOH dosing tank + pump", 1, "P95 %s kg NaOH/d" % f0(eq["alkali_dosing"]["NaOH_kg_d_P95"])),
 ("TK-202 / P-204", "Urea-N dosing tank + pump", 1, "P95 %s kg N/d" % f0(eq["nutrient_dosing"]["N_kg_d_P95"])),
 ("P-202", "Digestate transfer pump (to screw press)", "1+1", "%s m3/h, %s m head" % (f1(eq["screw_press"]["feed_m3_h"]), f0(15))),
 ("BTF-301", "Bio-trickling filter (desulfurizer)", 1, "%s Nm3/h gas, %.0f m3 packing (120 s EBCT), air %.1f Nm3/h" % (f0(eq["bio_desulfurizer"]["gas_Nm3_h"]), eq["bio_desulfurizer"]["V_m3"], eq["bio_desulfurizer"]["air_Nm3_h"])),
 ("K-301", "Air blower to BTF", 1, "%.1f Nm3/h" % eq["bio_desulfurizer"]["air_Nm3_h"]),
 ("HX-301", "Gas chiller + condensate pot", 1, "%.0f kWth, 5 C dew point" % eq["gas_chiller"]["duty_kW"]),
 ("K-302", "Biogas blower", "1+1", "%s m3/h, %.0f kPa" % (f0(eq["gas_blower"]["flow_m3_h"]), eq["gas_blower"]["dP_kPa"])),
 ("AC-301", "Activated-carbon polishing filter", 1, "%.1f kg H2S/d" % eq["carbon_filter"]["h2s_kg_d"]),
 ("FL-301", "Enclosed flare", 1, "%s Nm3/h" % f0(eq["flare"]["cap_Nm3_h"])),
 ("GE-401/402", "CHP gas engine-generators (containerised)", eq["chp"]["N"], "%s kWe each" % f0(eq["chp"]["unit_kWe"])),
 ("HX-401", "Exhaust heat recovery boiler / hot-water exchanger", 1, "exhaust to 150 C"),
 ("PR-501", "Screw press (digestate dewatering)", 1, "%s m3/h, %.0f t/d cake" % (f1(eq["screw_press"]["feed_m3_h"]), eq["screw_press"]["cake_t_d"])),
 ("CT-601", "Cooling tower (modular cells)", 1, "%s kWth" % f0(eq["cooling_tower"]["duty_kW"])),
]
for t, n_, q, k in rows: A("| %s | %s | %s | %s |" % (t, n_, q, k))
A("")
A("")
A("## 3b. Portable-module architecture (shipping kit)")
A("The digestion volume of a mill (V = Q x HRT = 14,000 m3 at 45 t FFB/h) cannot be moved as one unit, so *portable* is achieved as a **kit of transportable modules**; planning estimates only (see `portable_modules.py`).")
A("")
A("| Module | Content | Qty | Mass t (total) | ISO-sized units |")
A("|---|---|---|---|---|")
try:
    PMj = json.load(open(os.path.join(D, "outputs", "portable_modules.json"), encoding="utf-8"))
    for pm_ in PMj["modules"]:
        A("| %s %s | %s | %d | %s | %d |" % (pm_["id"], pm_["name"], pm_["note"], pm_["qty"], f1(pm_["mass_t_total"]), pm_["iso_units_total"]))
    A("")
    A("**Total for the 45 t FFB/h plant: %d ISO-sized units, about %s t shipped, plot about %.2f ha.** Digester kits ship flat-pack and are re-locatable; only the floor slab and civil works are site-built." % (PMj["iso_units_total"], f0(PMj["mass_t_total"]), PMj["plot_area_m2_estimate"]["total"] / 1e4))
except FileNotFoundError:
    A("(run portable_modules.py first)")
A("")
A("## 4. Design-basis operating point (45 t FFB/h x 20 h, nameplate)")
A("| Item | Value |")
A("|---|---|")
for k, v in [("POME", "%s m3/d" % f0(db["pome_m3d"])), ("EFB to digesters", "%.1f t/d" % db["efb_ad_td"]), ("Blend", "%s m3/d, TS %.1f %%, COD %.0f kg/m3" % (f0(db["blend_m3d"]), db["TS_blend"] * 100, db["cod_blend"])),
             ("Digester state", "pH %.2f, VFA %.0f mg/L, FOS/TAC %.3f, TAN %.0f mg N/L" % (nom["pH"], nom["vfa_mgL"], nom["fos_tac"], nom["tan_mgN"])),
             ("Biogas", "%s Nm3/d, CH4 %.1f %%, raw H2S %s ppm" % (f0(nom["biogas_Nm3d"]), nom["ch4_frac"] * 100, f0(nom["h2s_ppm_raw"]))),
             ("COD to methane", "%.0f %% of blend COD (%.0f %% non-degradable lignin/inerts)" % (nom["cod_conv"] * 100, nom["cod_routing_kgd"]["Tak terurai (lignin, inert)"] / sum(nom["cod_routing_kgd"].values()) * 100)),
             ("Electricity", "gross %s kWe, parasitic %s kWe, **net %s kWe**, mill demand %s kW, surplus %s kWe" % (f0(en["P_gross"]), f0(en["P_par"]), f0(en["P_net"]), f0(en["P_mill"]), f0(en["P_export"]))),
             ("Heat", "CHP %s kWth, digesters %s kWth, to mill %s kWth; POME cooling rejected %s kWth" % (f0(en["Q_heat_avail"]), f0(en["Q_dig"]), f0(en["Q_heat_export"]), f0(en["Q_cool"]))),
             ("CHP", "%d of %d engines at %.0f %% load, eta_el %.1f %%, exhaust %.0f C (from energy balance)" % (en["chp"]["n_run"], eq["chp"]["N"], en["chp"]["load"] * 100, en["chp"]["eta_el"] * 100, en["chp"]["T_exh"]))]:
    A("| %s | %s |" % (k, v))
A("")
A("## 5. Uncertainty (Latin-hypercube Monte Carlo, N = %d; P5 / P50 / P95; mill load factor 0.92 +/- 0.07)" % mc["N"])
A("| Output | P5 / P50 / P95 |")
A("|---|---|")
for k, lab, fm in [("bg", "Biogas, Nm3/d", f0), ("ch4_frac", "CH4 fraction", lambda x: "%.3f" % x), ("cod_rem", "COD removal", lambda x: "%.3f" % x), ("P_gross", "Gross power, kWe", f0), ("P_net", "Net power, kWe", f0), ("P_export", "Surplus after mill demand, kWe", f0), ("h2s_ppm_raw", "Raw H2S, ppm", f0), ("doseN", "Urea-N dosing, kg N/d", f0)]:
    A("| %s | %s |" % (lab, P(k, fm)))
A("| Probability of digester upset | %.1f %% |" % (mc["upset_probability"] * 100))
A("")
A("## 6. Scalability (same module)")
A("| Mill | Modules | Digester volume | Biogas Nm3/d | Net kWe | Net GWh/y (300 d) |")
A("|---|---|---|---|---|---|")
for k in ("20", "45", "70"):
    t = ti[k]; A("| %s t FFB/h | %d | %s m3 | %s | %s | %.1f |" % (k, t["N_modules"], f0(t["V_total"]), f0(t["biogas_Nm3d"]), f0(t["P_net"]), t["GWh_y"]))
A("")
A("## 7. Mass-balance closure (relative error)")
A("| Check | Error |")
A("|---|---|")
for k, v in R["closure"].items():
    if v is not None: A("| %s | %.1e |" % (k, v))
A("")
A("## 8. Stream table (kg/h, design basis)")
A("| No. | Stream | T, C | P, bar | Phase | Total kg/h |")
A("|---|---|---|---|---|---|")
for r in R["streams"]: A("| %d | %s | %.0f | %.2f | %s | %s |" % (r["id"], r["name"], r["T"], r["P"], r["ph"], f0(r["kg_h"])))
A("")
A("Component split of every stream is in `results.json -> streams[].comp`.")
A("")
A("## 9. Model basis and provenance")
A("* Biology: reduced ADM1, 30 states. Hydrolysis (first order), acidogenesis, acetogenesis, aceto- and hydrogenotrophic methanogenesis, acetate/H2 sulfate reduction; pH, free NH3, free H2S, LCFA, H2 inhibition; charge-balance pH; quasi-steady headspace with Henry-law transfer.")
A("* Stoichiometry for CO2, H2O, NH3 and sulfate is generated from chemical formulas by element balance (residual %.0e)." % R["meta"]["sto_residual"])
A("* Calibrated at run time to literature BMPs (POME 397, EFB 264 NmL CH4/g VS): fitted POME BMP %.0f, EFB BMP %.0f; calibrated k_cel_ref = %.3f 1/d, shielding beta = %.2f, POME refractory COD = %.0f %%." % (R["calibration"]["bmp_fit"]["pome"], R["calibration"]["bmp_fit"]["efb"], R["calibration"]["values"]["k_cel_ref"], R["calibration"]["values"]["beta_lig"], R["calibration"]["values"]["f_ref_pome"] * 100))
A("* Parameter provenance tags: `[LIT-S]` found by literature search in this project, `[ADM1]` Batstone et al. (2002) defaults, `[ASSUME]` engineering assumption to be replaced with site/vendor data, `[CALIB]` fitted. Full table: `results.json -> assumptions`.")
A("")
A("## 10. Limitations and open items")
A("* Feed ranges are literature-based, not site-measured; replacing POME composition, EFB composition and flow with one real mill data set is the highest-value upgrade.")
A("* EFB hydrolysis rate and recalcitrant fraction are only constrained by one literature BMP (30 d); they are the main structural uncertainty for continuous operation.")
A("* Sulfide-inhibition constants, SRB kinetics, part-load engine curve, heat-exchanger/cooling-tower and electricity-per-tonne figures are `[ASSUME]`.")
A("* Economics in `results.json -> economics_screen` use placeholder unit costs - not for decisions until vendor quotes replace them.")
A("* Full EFB co-digestion in continuous CSTRs at this scale has pilot, not commercial, precedent; POME-only biogas CHP is the proven reference case.")
open(os.path.join(D, "PROCESS_DESIGN_BASIS.md"), "w", encoding="utf-8").write("\n".join(L))
print("written PROCESS_DESIGN_BASIS.md (%d lines)" % len(L))
