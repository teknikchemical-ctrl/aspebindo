# -*- coding: utf-8 -*-
"""Generates PROCESS_DESIGN_BASIS.md (Rev 1) from outputs/results.json and outputs/portable_modules.json."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(D, "outputs", "portable_modules.json"), encoding="utf-8"))
pdn, db, nom, en, eq, mc, ti = R["process_decisions"], R["design_basis"], R["nominal"], R["energy"], R["equipment"], R["monte_carlo"], R["tiers"]
rv = eq["reactor_vessel"]; ves = pdn["vessel"]
f0 = lambda x: "{:,.0f}".format(x); f1 = lambda x: "{:,.1f}".format(x)
P = lambda k, fmt=f0: "%s / %s / %s" % (fmt(mc[k]["P5"]), fmt(mc[k]["P50"]), fmt(mc[k]["P95"]))
L = []; A = L.append
A("# Process Design Basis - Rev 1: Portable Thermophilic AnMBR Biogas Generator (POME)")
A("")
A("*Generated from `outputs/results.json` (seed %d, N_MC = %d). Rev 0 (mesophilic CSTR with EFB co-digestion) is kept as comparison case A.*" % (R["meta"]["seed"], R["meta"]["N_MC"]))
A("")
A("## 1. Product")
A("A **portable, shop-built biogas power plant for palm oil mills of 30-60 t FFB/h** (the common sizes in Sumatra). Hot POME (85 C) is digested at **55 C in a thermophilic "
  "anaerobic membrane bioreactor (AnMBR)**: an external tubular ultrafiltration loop retains the biomass and solids (SRT %.0f d) while the liquid passes in %.1f d. "
  "This makes the reactor %.1fx smaller than the Rev 0 mesophilic design, so it fits in **one standard road-transportable vessel (D %.1f m, %.0f m3)** that is numbered up: "
  "**%d / %d / %d vessels** for 30 / 45 / 60 t FFB/h. Everything else ships in 40 ft containers or container-size skids."
  % (pdn["srt_d"], pdn["hrt_design_d"], PM["rev0_comparison"]["rev0_digester_m3"] / PM["rev0_comparison"]["rev1_reactor_m3"], ves["D"], ves["V_mod"],
     ves["N"]["30.0"], ves["N"]["45.0"], ves["N"]["60.0"]))
A("")
A("## 2. Why this technology (model results, same 45 t FFB/h feed)")
A("")
A("| Case | Reactor volume m3 | HRT / SRT d | OLR kg COD/m3.d | CH4 Nm3/d | Nm3 CH4 per m3.d | MLSS g/L |")
A("|---|---|---|---|---|---|---|")
for t in pdn["tech_compare"]:
    A("| %s | %s | %.1f / %.1f | %.1f | %s | %.2f | %.1f |" % (t["name"], f0(t["V"]), t["hrt"], t["srt"], t["olr"], f0(t["ch4"]), t["prod"], t["mlss"]))
A("")
A("* POME arrives at 75-95 C, so 55 C operation needs **no heating**: the feed is only cooled, and its residual heat covers the reactor losses.")
A("* Thermophilic kinetics (ADM1 thermophilic parameter set) plus membrane solids retention raise volumetric productivity about 4x over Rev 0.")
A("* EFB co-digestion is **dropped** from the portable product: in Rev 0, EFB (32 % non-degradable lignin, hydrolysis k ~0.03 1/d) set most of the reactor volume. EFB stays with the mill (mulch / boiler).")
A("* Literature anchors: thermophilic CSTR on POME reached 17 kg COD/m3.d at HRT 5 d (Choorit & Wisarnwan, 2007); a 55 C AnMBR on palm oil wastewater held 93-98 % COD removal at 2-10 kg COD/m3.d (Membranes, 2019); "
  "Kubota markets a membrane-based compact POME biogas system; containerised 600 kW biogas gensets run at the Sei Pelakar mill in Sumatra (Guascor).")
A("")
A("## 3. Fixed design decisions")
A("| # | Decision | Value | Basis |")
A("|---|---|---|---|")
rows = [("Reactor", "Thermophilic AnMBR, CSTR with jet mixing + external tubular UF", "Volume, effluent quality, biomass retention"),
        ("Temperature", "55 C", "Hot POME; ADM1 thermophilic set"),
        ("HRT / SRT", "%.1f d / %.0f d (actual HRT %.2f d)" % (pdn["hrt_design_d"], pdn["srt_d"], pdn["hrt_actual_d"]),
         "Smallest volume with MLSS <= 85 %% of %.0f g/L, OLR <= %.0f kg COD/m3.d, FOS/TAC <= 0.3, CH4 >= 95 %% of best (HRT x SRT grid)" % (R["EQ"]["mlss_max"], R["EQ"]["olr_max"])),
        ("Standard vessel", "D %.1f m, liquid height %.1f m, %.0f m3; ships %.1f m long" % (ves["D"], ves["H_liq"], ves["V_mod"], PM["vessel"]["ship_length_m"]),
         "Largest road-transportable vessel with <= 15 % overshoot in all three mill sizes"),
        ("Pre-treatment", "Rotary screen + hydrocyclone desander + plate cooler (85 -> %.0f C)" % eq["pome_cooler"]["T_out"], "Grit would accumulate SRT/HRT times in the membrane loop"),
        ("Membrane", "%.0f m2 tubular UF at %.0f LMH, %d modules, %.0f kWe" % (eq["membrane"]["area_m2"], eq["membrane"]["flux"], eq["membrane"]["modules"], eq["membrane"]["kW"]), "External cross-flow handles 20-40 g/L solids"),
        ("Biogas cleaning", "Bio-trickling filter -> chiller 5 C -> blower -> activated carbon", "%s ppm raw -> %s ppm H2S to engine" % (f0(nom["h2s_ppm_raw"]), f0(nom["h2s_ppm_fuel"]))),
        ("Gas storage", "Double-membrane gas holder %s m3 (%.0f h at P95)" % (f0(eq["gas_holder"]["V_m3"]), eq["gas_holder"]["hours"]), "Smooths the 20 h/d mill feed"),
        ("Power", "%d x %s kWe containerised gas engines" % (eq["chp"]["N"], f0(eq["chp"]["unit_kWe"])), "Sized on P95 fuel %s kW" % f0(eq["chp"]["fuel_P95_kW"])),
        ("Stability control", "pH 7.0 (NaOH), urea-N >= 100 mg N/L, level and temperature control on every vessel", "Monte Carlo upset probability %.1f %%" % (mc["upset_probability"] * 100))]
for i, (a, b, c) in enumerate(rows, 1): A("| %d | %s | %s | %s |" % (i, a, b, c))
A("")
A("## 4. Portable module set (45 t FFB/h)")
A("")
A("| Module | Content | Qty | Shipping | Mass t |")
A("|---|---|---|---|---|")
for m in PM["modules"]:
    A("| %s %s | %s | %d | %s | %s |" % (m["id"], m["name"], m["note"], m["qty"], m["unit"], f1(m["mass_t_total"])))
A("")
A("**Total: %d truck loads, about %s t; plot about %.2f ha** (Rev 0: 0.39 ha). Planning estimates." % (PM["ship_units_total"], f0(PM["mass_t_total"]), PM["plot_area_m2_estimate"]["total"] / 1e4))
A("")
A("## 5. Design-basis operating point (45 t FFB/h x 20 h)")
A("| Item | Value |")
A("|---|---|")
for k, v in [("POME", "%s m3/d at 85 C, COD %.0f kg/m3" % (f0(db["pome_m3d"]), db["cod_blend"])),
             ("Reactor state", "pH %.2f, VFA %.0f mg/L, FOS/TAC %.3f, TAN %.0f mg N/L, MLSS %.1f g/L, OLR %.1f kg COD/m3.d" % (nom["pH"], nom["vfa_mgL"], nom["fos_tac"], nom["tan_mgN"], nom["mlss"], nom["olr"])),
             ("Biogas", "%s Nm3/d, CH4 %.1f %% (%s Nm3 CH4/d)" % (f0(nom["biogas_Nm3d"]), nom["ch4_frac"] * 100, f0(nom["ch4_Nm3d"]))),
             ("Electricity", "gross %s kWe, parasitic %s, **net %s kWe**, mill demand %s kW" % (f0(en["P_gross"]), f0(en["P_par"]), f0(en["P_net"]), f0(en["P_mill"]))),
             ("Heat", "POME cooling %s kWth rejected; CHP hot water %s kWth available" % (f0(en["Q_pome_cool"]), f0(en["Q_heat_avail"]))),
             ("Effluent", "permeate + filtrate; waste sludge %s m3/d -> %s t/d cake" % (f1(eq["waste_sludge"]["Qw_m3d"]), f1(eq["waste_sludge"]["cake_t_d"]))),
             ("Methane avoided", "%s tCO2e/y vs open ponds (IPCC defaults)" % f0(R["emissions"]["avoided_t"]))]:
    A("| %s | %s |" % (k, v))
A("")
A("## 6. Uncertainty (Monte Carlo N = %d, mill load 0.92 +/- 0.07; P5 / P50 / P95)" % mc["N"])
A("| Output | P5 / P50 / P95 |")
A("|---|---|")
for k, lab, fm in [("bg", "Biogas, Nm3/d", f0), ("P_net", "Net power, kWe", f0), ("P_export", "Surplus over mill demand, kWe", f0), ("mlss", "Reactor MLSS, g/L", f1), ("olr", "OLR, kg COD/m3.d", f1), ("doseN", "Urea-N, kg N/d", f0)]:
    A("| %s | %s |" % (lab, P(k, fm)))
A("")
A("## 7. Scalability")
A("| Mill | Reactor vessels | Net kWe | Net GWh/y | CHP |")
A("|---|---|---|---|---|")
for k in ("30", "45", "60"):
    t = ti[k]; A("| %s t FFB/h | %d | %s | %.1f | %d x %s kWe |" % (k, t["N_modules"], f0(t["P_net"]), t["GWh_y"], t["chp"]["N_gen"], f0(t["chp"]["P_unit"])))
A("")
A("## 8. Closure (relative error)")
A("| Check | Error |")
A("|---|---|")
for k, v in R["closure"].items(): A("| %s | %.1e |" % (k, v))
A("")
A("## 9. Limitations")
A("* Thermophilic ADM1 parameter ratios and membrane flux / energy / solids limit are literature-typical values, not pilot data; a pilot AnMBR on real POME is the single most important validation step.")
A("* POME composition is literature-based; one real mill data set would tighten every number.")
A("* With POME only, net power about equals the mill's own demand, but the mill keeps its fibre/shell steam turbine. The business case (finance/) is a BOO treatment + energy service: the mill pays a POME treatment/compliance fee per t FFB, takes ~0.37 GWh/yr off-shift power in place of diesel, and the rest (~5.7 GWh/yr) is exported to PLN under Perpres 112/2022; methane credits are a minor stream.")
A("* Economics (`economics_screen`) use placeholder costs.")
open(os.path.join(D, "PROCESS_DESIGN_BASIS.md"), "w", encoding="utf-8").write("\n".join(L))
print("written PROCESS_DESIGN_BASIS.md (%d lines)" % len(L))
