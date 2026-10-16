# -*- coding: utf-8 -*-
"""Generates PROCESS_DESIGN_BASIS.md (Rev 2) from outputs/results.json and outputs/portable_modules.json."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
PM = json.load(open(os.path.join(D, "outputs", "portable_modules.json"), encoding="utf-8"))
pdn, db, nom, en, eq, mc, ti = R["process_decisions"], R["design_basis"], R["nominal"], R["energy"], R["equipment"], R["monte_carlo"], R["tiers"]
rv = eq["reactor_vessel"]; ves = pdn["vessel"]; yr = R["year"]; ef = R["effluent"]; mo = R["membrane_option"]; em = R["emissions"]; ls = eq["lamella_settler"]
f0 = lambda x: "{:,.0f}".format(x); f1 = lambda x: "{:,.1f}".format(x)
P = lambda k, fmt=f0: "%s / %s / %s" % (fmt(mc[k]["P5"]), fmt(mc[k]["P50"]), fmt(mc[k]["P95"]))
L = []; A = L.append
A("# Process Design Basis - Rev 2: Relocatable Thermophilic Anaerobic Contact Biogas Set (POME)")
A("")
A("*Generated from `outputs/results.json` (seed %d, N_MC = %d). Rev 2 follows the Stage 1 technical red-team against the literature (`research/R4_technical_evidence.md`).*"
  % (R["meta"]["seed"], R["meta"]["N_MC"]))
A("")
A("## 1. Product")
A("A **relocatable biogas power set for palm oil mills of 30-60 t FFB/h**. Hot POME (85 C) is digested at **55 C in a thermophilic anaerobic contact process**: "
  "completely mixed reactors, a vacuum degasser and a lamella settler that returns the sludge, so solids stay %.0f d while the liquid passes in %.1f d (at the nameplate day). "
  "The reactors are **standard bolted glass-fused-to-steel (GFS) tanks (D %.2f m, %.0f m3)** that ship flat-packed in 40 ft containers and can be dismantled and re-erected at the next mill: "
  "**%d / %d / %d tanks** for 30 / 45 / 60 t FFB/h. Everything else ships in containers or container-size skids (%d loads, about %s t for 45 t FFB/h)."
  % (pdn["srt_d"], pdn["hrt_design_d"], ves["D"], ves["V_mod"], ves["N"]["30.0"], ves["N"]["45.0"], ves["N"]["60.0"], PM["ship_units_total"], f0(PM["mass_t_total"])))
A("")
A("## 2. Stage 1 red-team: what changed from Rev 1 and why")
A("")
A("| # | Finding (research/R4) | Rev 1 | Rev 2 action | Result |")
A("|---|---|---|---|---|")
rows = [
 ("Membrane cross-flow loop undersized; flux 15 LMH optimistic (lit. 3-14)", "996 m2, 22 kW", "Re-sized option at 8 LMH, 3 kWh/m3 (gas-lift)",
  "%s m2, %s kW for +%s Nm3 CH4/d (+%s kWe gross): membrane dropped from base case" % (f0(mo["area_m2"]), f0(mo["kW"]), f0(mo["ch4_gain_Nm3d"]), f0(mo["kWe_gain_gross"]))),
 ("Membrane adds little methane; no full-scale POME AnMBR exists", "AnMBR", "Thermophilic contact process (degasser + lamella + recycle)",
  "SRT %.0f d at %.0f kW extra; FOS/TAC %.2f" % (pdn["srt_d"], en["parasitic"]["degasser"] + en["parasitic"]["sludge_recycle"], nom["fos_tac"])),
 ("4.2 m vessels on low-bed are ~5.1 m high > 4.2 m road limit", "14 shop vessels", "Bolted GFS tanks shipped as panels",
  "%d tanks, %d containers each, no oversize loads" % (rv["count"], PM["vessel"]["containers"])),
 ("Design flow 585 m3/d is the nameplate day; annual average lower", "util 0.92, 300 d x 24 h", "util 0.75 (annual), Sundays off, 14 d shutdown, seasonal +/-25 %",
  "%.2f GWh/y net (annual simulation)" % yr["GWh_net"]),
 ("CHP oversized (68 % mean load)", "2 x 800 kWe on P95", "Sized on nameplate-day fuel", "%d x %s kWe" % (eq["chp"]["N"], f0(eq["chp"]["unit_kWe"]))),
 ("'68 % COD removal' is the methanised fraction, not treatment removal", "one number", "Report both",
  "CH4 %.0f %% of COD; COD load to ponds -%.0f %%" % (nom["cod_rem"] * 100, (1 - ef["COD"] * ef["Q_m3d"] / (db["pome_m3d"] * db["cod_blend"] * 1000)) * 100)),
 ("Permeate COD 7.3 g/L inconsistent with VFA 85 mg/L", "sI 4 % of COD", "sI 2.5 % (AD effluent soluble COD 1.5-4 g/L)", "soluble COD %s mg/L" % f0(ef["COD_soluble"])),
 ("Effluent cannot meet PermenLH 5/2014 river limits", "implied compliance", "Effluent to existing polishing ponds -> land application",
  "COD %s, BOD %s mg/L (land application <= 5,000 BOD: %s)" % (f0(ef["COD"]), f0(ef["BOD5"]), "yes" if ef["meets_land_application_BOD5000"] else "no")),
 ("Nitrogen dosing unnecessary (POME TKN ~750 mg/L)", "urea to 100 mg N/L", "Safety floor 50 mg N/L, raw TAN 70 mg/L", "TAN %s mg N/L, dosing P95 %s kg N/d" % (f0(nom["tan_mgN"]), f0(mc["doseN"]["P95"]))),
 ("Grit removal 60 % too low; polymer 4 kg/t DS optimistic", "60 %, 4 kg/t", "85 %, 8 kg/t DS, cake 20 % DS", "cake %s t/d" % f1(eq["waste_sludge"]["cake_t_d"])),
 ("Carbon: uncertainty factor missing", "MCF 0.8, no UF", "AMS-III.H UF 0.89, degasser recovers 70 % dissolved CH4", "%s tCO2e/y (%.3f t/t FFB)" % (f0(em["avoided_t"]), em["per_t_ffb"])),
 ("BMP '397 NmL CH4/g COD' impossible (> 350)", "label", "Label fixed: per g VS", "-"),
]
for i, r in enumerate(rows, 1): A("| %d | %s |" % (i, " | ".join(r)))
A("")
A("Residual risks not closed by modelling: thermophilic VFA may run 200-800 mg/L in practice (model 85 mg/L); oleate inhibition at 55 C; start-up 2-4 months "
  "(finance uses a 75 %% first-year factor); settler capture %.0f %% assumed (pilot to confirm)." % (R["EQ"]["e_set"] * 100))
A("")
A("## 3. Technology comparison (model, same 45 t FFB/h nameplate feed)")
A("")
A("| Case | Reactor volume m3 | HRT / SRT d | OLR kg COD/m3.d | CH4 Nm3/d | Nm3 CH4 per m3.d | MLSS g/L | FOS/TAC |")
A("|---|---|---|---|---|---|---|---|")
for t in pdn["tech_compare"]:
    A("| %s | %s | %.1f / %.1f | %.1f | %s | %.2f | %.1f | %.2f |" % (t["name"], f0(t["V"]), t["hrt"], t["srt"], t["olr"], f0(t["ch4"]), t["prod"], t["mlss"], t["fos"]))
A("")
A("* POME arrives at 75-95 C, so 55 C operation needs **no heating**: the feed is only cooled, and its residual heat covers the reactor losses.")
A("* The contact process gets most of the membrane's benefit (biomass retention, stability margin) for a lamella settler and two pumps; the AnMBR remains an option (PM-11) for water-reuse sites.")
A("* Literature anchors: thermophilic CSTR on POME stable at HRT 5 d, OLR 17 (Choorit & Wisarnwan, 2007); thermophilic AnMBR on POME flux ~3 LMH (Membranes, 2019); "
  "full-scale ADI-MBR 2.5-4.2 LMH.")
A("")
A("## 4. Fixed design decisions")
A("| # | Decision | Value | Basis |")
A("|---|---|---|---|")
rows = [("Reactor", "Thermophilic anaerobic contact: CSTR (jet mixing) + vacuum degasser + lamella settler + sludge recycle", "Stage 1 red-team; no membrane in base case"),
        ("Temperature", "55 C", "Hot POME; ADM1 thermophilic set"),
        ("HRT / SRT", "%.1f d at nameplate (%.1f d annual mean) / %.0f d" % (pdn["hrt_actual_d"], pdn["hrt_actual_d"] / yr["util"] * 1.0, pdn["srt_d"]),
         "Longest SRT with MLSS <= %.0f g/L (settler), OLR <= %.0f, FOS/TAC <= 0.3" % (R["EQ"]["mlss_max"], R["EQ"]["olr_max"])),
        ("Reactor tank", "Bolted GFS, D %.2f m, liquid %.1f m, %.0f m3, %d panels" % (ves["D"], ves["H_liq"], ves["V_mod"], PM["vessel"]["panels"]),
         "Standard size: 2/3/4 tanks for 30/45/60 t FFB/h within +-15 %"),
        ("Settler", "Lamella %.0f m2 projected at %.1f m3/m2.h; recycle %.0f m3/d; capture %.0f %%" % (ls["A_proj_m2"], ls["rate_m3_m2h"], ls["recycle_m3d"], ls["capture"] * 100), "[ASSUME] pilot to confirm"),
        ("Pre-treatment", "Rotary screen + grit chamber/hydrocyclone (%.0f %%) + plate cooler (85 -> %.0f C)" % (eq["desander"]["grit_removal"] * 100, eq["pome_cooler"]["T_out"]), "Sand accumulates SRT/HRT times"),
        ("Biogas cleaning", "Bio-trickling filter (95 %) -> chiller 5 C -> blower -> carbon guard bed", "%s ppm raw -> %s ppm H2S (engine limit 100-200)" % (f0(nom["h2s_ppm_raw"]), f0(nom["h2s_ppm_fuel"]))),
        ("Gas storage", "Double-membrane gas holder %s m3 (%.0f h)" % (f0(eq["gas_holder"]["V_m3"]), eq["gas_holder"]["hours"]), "Smooths the 20 h/d mill feed"),
        ("Power", "%d x %s kWe containerised gas engines" % (eq["chp"]["N"], f0(eq["chp"]["unit_kWe"])), "Nameplate-day fuel %s kW" % f0(eq["chp"]["fuel_design_kW"])),
        ("Effluent", "Settler overflow + press filtrate -> existing polishing ponds -> land application", "PermenLH 5/2014 river limits not met by AD alone"),
        ("Stability control", "pH 7.0 (NaOH), level, temperature, FOS/TAC titration daily", "Monte Carlo upset probability %.1f %%" % (mc["upset_probability"] * 100))]
for i, (a, b, c) in enumerate(rows, 1): A("| %d | %s | %s | %s |" % (i, a, b, c))
A("")
A("## 5. Relocatable module set (45 t FFB/h)")
A("")
A("| Module | Content | Qty | Shipping | Mass t |")
A("|---|---|---|---|---|")
for m in PM["modules"]:
    A("| %s %s | %s | %d | %s | %s |" % (m["id"], m["name"], m["note"], m["qty"], m["unit"], f1(m["mass_t_total"])))
o = PM["option"]
A("| %s %s | %s | %d | kontainer 40 ft | - |" % (o["id"], o["name"], o["note"], o["qty"]))
A("")
A("**Total: %d truck/container loads, about %s t; plot about %.2f ha** (%s). Planning estimates." % (PM["ship_units_total"], f0(PM["mass_t_total"]), PM["plot_area_m2_estimate"]["total"] / 1e4, PM["plot_area_m2_estimate"]["source"]))
A("")
A("## 6. Operating points")
A("| Item | Nameplate day (equipment sizing) | Annual average (finance) |")
A("|---|---|---|")
A("| FFB | 45 t/h x 20 h = 900 t/d | %s t/y (util %.2f, ~300 d) |" % (f0(yr["ffb_t"]), yr["util"]))
A("| POME | %s m3/d, COD %.0f kg/m3 | %s m3/y |" % (f0(db["pome_m3d"]), db["cod_blend"], f0(yr["pome_m3"])))
A("| Reactor | pH %.2f, VFA %.0f mg/L, FOS/TAC %.3f, TAN %.0f mg N/L, MLSS %.1f g/L, OLR %.1f | MC P50 MLSS %.1f g/L |" % (nom["pH"], nom["vfa_mgL"], nom["fos_tac"], nom["tan_mgN"], nom["mlss"], nom["olr"], mc["mlss"]["P50"]))
A("| Biogas | %s Nm3/d, CH4 %.1f %% | MC P50 %s Nm3/d |" % (f0(nom["biogas_Nm3d"]), nom["ch4_frac"] * 100, f0(mc["bg"]["P50"])))
A("| Electricity | gross %s, parasitic %s, **net %s kWe** | **%.2f GWh/y net** (gross %.2f) |" % (f0(en["P_gross"]), f0(en["P_par"]), f0(en["P_net"]), yr["GWh_net"], yr["GWh_gross"]))
A("| Heat | POME cooling %s kWth rejected; CHP hot water %s kWth | - |" % (f0(en["Q_pome_cool"]), f0(en["Q_heat_avail"])))
A("| Effluent to ponds | %s m3/d: COD %s (soluble %s), BOD %s, TSS %s, TN %s mg/L | - |" % (f0(ef["Q_m3d"]), f0(ef["COD"]), f0(ef["COD_soluble"]), f0(ef["BOD5"]), f0(ef["TSS"]), f0(ef["TN"])))
A("| Sludge cake | %s t/d (20 %% DS) | - |" % f1(eq["waste_sludge"]["cake_t_d"]))
A("| Methane avoided | - | **%s tCO2e/y** (AMS-III.H, GWP 28, UF 0.89) |" % f0(em["avoided_t"]))
A("")
A("## 7. Uncertainty (Monte Carlo N = %d at annual-average util; P5 / P50 / P95)" % mc["N"])
A("| Output | P5 / P50 / P95 |")
A("|---|---|")
for k, lab, fm in [("bg", "Biogas, Nm3/d", f0), ("P_net", "Net power, kWe", f0), ("mlss", "Reactor MLSS, g/L", f1), ("olr", "OLR, kg COD/m3.d", f1), ("fos", "FOS/TAC", lambda x: "%.3f" % x)]:
    A("| %s | %s |" % (lab, P(k, fm)))
A("")
A("## 8. Scalability")
A("| Mill | GFS tanks | Net kWe (nameplate) | Net GWh/y (annual) | CHP |")
A("|---|---|---|---|---|")
for k in ("30", "45", "60"):
    t = ti[k]; A("| %s t FFB/h | %d | %s | %.2f | %d x %s kWe |" % (k, t["N_modules"], f0(t["P_net"]), t["GWh_y"], t["chp"]["N_gen"], f0(t["chp"]["P_unit"])))
A("")
A("## 9. Closure (relative error)")
A("| Check | Error |")
A("|---|---|")
for k, v in R["closure"].items(): A("| %s | %.1e |" % (k, v))
A("")
A("## 10. Limitations")
A("* Thermophilic ADM1 ratios, settler capture and the solids limit are literature-typical, not pilot data; a pilot on real POME is the key validation step.")
A("* POME composition is literature-based; one real mill data set would tighten every number.")
A("* Net power during processing hours is about the mill's own demand, but the mill keeps its fibre/shell turbine, so the power is sold (diesel displacement at the mill, PLN export). "
  "The business case is in `finance/` (Mill Decision Model: status-quo ponds vs alternatives vs this BOO service).")
open(os.path.join(D, "PROCESS_DESIGN_BASIS.md"), "w", encoding="utf-8").write("\n".join(L))
print("written PROCESS_DESIGN_BASIS.md (%d lines)" % len(L))
