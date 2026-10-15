# -*- coding: utf-8 -*-
"""
Portable-module set of the Rev 1 product (thermophilic AnMBR).  Reads outputs/results.json, writes outputs/portable_modules.json.

Every piece is shop-built and road-transportable to a Sumatra mill:
  * ONE standard vessel design (D 4.2 m, 194 m3 working) is used for every reactor, the feed buffer and the permeate tank;
    it ships lying down on a low-bed trailer (oversize load, escort) and is set on a plain slab.
  * all rotating equipment, membranes, gas treatment and CHP sit in 40 ft high-cube containers or container-size skids.
Masses and counts are PLANNING ESTIMATES [ASSUME] - confirm with fabricators.
"""
import json, math, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
eq = R["equipment"]; rv = eq["reactor_vessel"]
N = rv["count"]
STEEL = 7.85; T_SHELL = 0.008                                             # t/m3, 8 mm carbon-steel shell  [ASSUME]
A_shell = math.pi * rv["D_m"] * rv["H_shell_m"] + 2 * 1.084 * rv["D_m"] ** 2
m_vessel = A_shell * T_SHELL * STEEL + 2.0 + 2.0                           # shell + insulation/cladding + nozzles/internals
L_ship = rv["H_shell_m"] + 0.5 * rv["D_m"]
n_buffer = 1; n_perm = 1

mods = [
    dict(id="PM-1", name="Skid praolah POME", tags=["SC-101", "HC-101", "E-101"], qty=1, mass_t_each=12.0, unit="kontainer 40 ft (skid)",
         note="rotary screen, hydrocyclone desander, plate cooler %.0f kWth" % eq["pome_cooler"]["duty_kW"]),
    dict(id="PM-2", name="Bejana standar: tangki penyangga umpan", tags=["TK-101"], qty=n_buffer, mass_t_each=m_vessel, unit="bejana di trailer low-bed",
         note="same 194 m3 vessel as the reactors, %.1f h hold-up" % (194.0 / (eq["feed_pump"]["flow_m3_h"]))),
    dict(id="PM-3", name="Bejana standar: reaktor AnMBR termofilik", tags=["R-201..R-2%02d" % N, "P-202 (per reaktor)"], qty=N, mass_t_each=m_vessel, unit="bejana di trailer low-bed",
         note="D %.1f m x H %.1f m, %.0f m3, 55 C, jet mixing; ships %.1f m long" % (rv["D_m"], rv["H_shell_m"], rv["V_liq_m3"], L_ship)),
    dict(id="PM-4", name="Kontainer membran + CIP", tags=["MB-301", "P-301", "P-302", "TK-302"], qty=eq["membrane"]["containers"], mass_t_each=16.0, unit="kontainer 40 ft HC",
         note="%.0f m2 tubular UF, %d modules, cross-flow %.0f m3/h" % (eq["membrane"]["area_m2"], eq["membrane"]["modules"], eq["membrane"]["loop_m3h"])),
    dict(id="PM-5", name="Skid dosing dan pompa umpan", tags=["P-201", "TK-201", "P-203", "TK-202", "P-204"], qty=1, mass_t_each=8.0, unit="skid 20 ft",
         note="feed pumps, NaOH and urea-N dosing"),
    dict(id="PM-6", name="Skid pengolahan biogas", tags=["BTF-301", "K-301", "HX-301", "V-301", "K-302", "AC-301"], qty=1, mass_t_each=14.0, unit="kontainer 40 ft + bejana BTF",
         note="%.0f Nm3/h; BTF %.0f m3 packing ships as its own vessel" % (eq["bio_desulfurizer"]["gas_Nm3_h"], eq["bio_desulfurizer"]["V_m3"]), extra_units=1),
    dict(id="PM-7", name="Penampung gas + flare", tags=["GH-301", "FL-301"], qty=1, mass_t_each=7.0, unit="kontainer 20 ft (membran terlipat) + skid flare",
         note="double-membrane gas holder %.0f m3 (%.0f h), flare %.0f Nm3/h" % (eq["gas_holder"]["V_m3"], eq["gas_holder"]["hours"], eq["flare"]["cap_Nm3_h"]), extra_units=1),
    dict(id="PM-8", name="Kontainer CHP", tags=["GE-401", "GE-402", "ST-401"], qty=eq["chp"]["N"], mass_t_each=24.0, unit="kontainer 40 ft HC",
         note="%.0f kWe biogas engine-generator per container" % eq["chp"]["unit_kWe"]),
    dict(id="PM-9", name="Skid pemulih panas + menara pendingin", tags=["HX-401", "CT-601"], qty=1, mass_t_each=9.0, unit="skid 20 ft + sel CT modular",
         note="hot-water recovery %.0f kWth; cooling %.0f kWth" % (R["energy"]["Q_heat_avail"], eq["cooling_tower"]["duty_kW"]), extra_units=1),
    dict(id="PM-10", name="Bejana standar: tangki permeat + skid lumpur", tags=["TK-301", "P-303", "PR-501", "P-501"], qty=1, mass_t_each=m_vessel + 8.0, unit="bejana + skid 20 ft",
         note="permeate tank (same vessel), screw press %.1f m3/d waste sludge" % eq["waste_sludge"]["Qw_m3d"], extra_units=1),
]
tot_u = 0; tot_m = 0.0
for m in mods:
    m["ship_units"] = m["qty"] + m.get("extra_units", 0)
    m["mass_t_total"] = m["mass_t_each"] * m["qty"]
    tot_u += m["ship_units"]; tot_m += m["mass_t_total"]
pitch = rv["D_m"] + 1.5
rows = 2; cols = math.ceil((N + n_buffer + n_perm) / rows)
area_v = (cols * pitch) * (rows * pitch + 4.0)
out = dict(modules=mods, ship_units_total=tot_u, mass_t_total=tot_m, vessel=dict(D=rv["D_m"], H_shell=rv["H_shell_m"], V=rv["V_liq_m3"], mass_t=m_vessel, ship_length_m=L_ship),
           plot_area_m2_estimate=dict(vessels=area_v, skids_and_roads=900.0, total=area_v + 900.0),
           scaling={k: dict(vessels=v["N_modules"] + 2, chp_units=v["chp"]["N_gen"], chp_kWe=v["chp"]["P_unit"], membrane_m2=v["membrane"]["area_m2"]) for k, v in R["tiers"].items()},
           rev0_comparison=dict(rev0_digester_m3=14000, rev1_reactor_m3=N * rv["V_liq_m3"]),
           assumptions="masses, shipping units and footprint are planning estimates [ASSUME]")
json.dump(out, open(os.path.join(D, "outputs", "portable_modules.json"), "w"), indent=1)
print("%-6s %-44s %4s %8s %6s" % ("id", "module", "qty", "t total", "loads"))
for m in mods: print("%-6s %-44s %4d %8.1f %6d" % (m["id"], m["name"], m["qty"], m["mass_t_total"], m["ship_units"]))
print("TOTAL %d truck loads, %.0f t; standard vessel %.1f t, ships %.1f m long; plot ~%.0f m2 (%.2f ha)" % (tot_u, tot_m, m_vessel, L_ship, out["plot_area_m2_estimate"]["total"], out["plot_area_m2_estimate"]["total"] / 1e4))
