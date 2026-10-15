# -*- coding: utf-8 -*-
"""
Portable-module architecture of the biogas generator (reads outputs/results.json, writes outputs/portable_modules.json).

SELF-EVALUATION RESULT (drives this file)
  The digestion volume needed for a mill is V = Q x HRT (45 t FFB/h -> 14,000 m3).  No digester of that volume can be moved
  as one unit, so 'portable' is achieved as a KIT OF TRANSPORTABLE MODULES:
     PM-A  feed-preparation skid        (screen, shredder, conveyor)
     PM-B  POME cooling skid            (plate cooler + modular cooling-tower cells)
     PM-C  digester kit  x N            (bolted/glass-fused steel panels, membrane roof, mixers - ships flat-pack in ISO containers,
                                         re-locatable; only the floor slab is poured on site)
     PM-D  gas-treatment skid           (bio-trickling filter, chiller, blowers, carbon filter) + flare
     PM-E  CHP container  x 2           (1 MWe engine-generator in a 40 ft HC container + heat-recovery skid)
     PM-F  digestate & dosing skid      (screw press, polymer unit, NaOH / urea dosing)
  Masses and container counts are PLANNING ESTIMATES [ASSUME] - replace with vendor data.
"""
import json, math, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
eq, pdn = R["equipment"], R["process_decisions"]
N = eq["digester_module"]["count"]
ISO40 = dict(L=12.19, W=2.44, H=2.90, payload_t=26.0, vol_m3=67.0)          # 40 ft high-cube, dry
GFS_KG_M2 = 25.0                                                              # glass-fused-to-steel wall panel incl. bolts [ASSUME]
INSUL_M = 0.10                                                                # insulation thickness, m
dm = eq["digester_module"]

def containers(mass_t, vol_m3=0.0, fill=0.75):
    return max(math.ceil(mass_t / (ISO40["payload_t"] * fill)), math.ceil(vol_m3 / (ISO40["vol_m3"] * 0.8)) if vol_m3 else 0, 1)

A_wall = math.pi * dm["D_m"] * dm["H_wall_m"]
m_wall = A_wall * GFS_KG_M2 / 1000.0
m_roof = 2.5 + 1.2 + 0.0035 * math.pi * (dm["D_m"] / 2) ** 2 * 1.0           # truss + double membrane + hardware
m_mix = 2 * 0.8; m_ins = A_wall * 0.0035 + 0.5; m_misc = 2.0                    # mixers, rock-wool, ladders/manway/piping
m_dig = m_wall + m_roof + m_mix + m_ins + m_misc
v_dig = A_wall * INSUL_M * 1.1                                                  # insulation panels are the bulky item

mods = [
    dict(id="PM-A", name="Skid persiapan umpan", tags=["SC-101", "SH-101", "CV-101"], qty=1, mass_t_each=10.5,
         note="rotary screen, hammer mill %d mm, conveyor, MCC" % pdn["d_p_mm"]),
    dict(id="PM-B", name="Skid pendingin POME", tags=["E-101", "CT-601"], qty=1, mass_t_each=12.0,
         note="plate cooler %.0f kWth + 2 modular cooling-tower cells" % eq["pome_cooler"]["duty_kW"]),
    dict(id="PM-C", name="Kit modul digester", tags=["R-201 .. R-2%02d" % (N), "MX-201 .."], qty=N, mass_t_each=m_dig, vol_m3_each=v_dig,
         note="%d m3 liquid, D %.1f m, H %.1f m, bolted panels + membrane roof + 2 mixers; floor slab poured on site" % (dm["V_liq_m3"], dm["D_m"], dm["H_liq_m"])),
    dict(id="PM-D", name="Skid pengolahan gas", tags=["BTF-301", "K-301", "HX-301", "K-302", "AC-301"], qty=1, mass_t_each=14.5,
         note="%.0f Nm3/h; bio-trickling filter shipped as a separate vessel" % eq["bio_desulfurizer"]["gas_Nm3_h"], extra_units=1),
    dict(id="PM-D2", name="Flare tertutup", tags=["FL-301"], qty=1, mass_t_each=3.0, note="%.0f Nm3/h enclosed flare" % eq["flare"]["cap_Nm3_h"], extra_units=0),
    dict(id="PM-E", name="Kontainer CHP", tags=["GE-401", "GE-402", "HX-401"], qty=eq["chp"]["N"], mass_t_each=28.0,
         note="%.0f kWe gas engine-generator per 40 ft HC container; plus 5 t heat-recovery skid" % eq["chp"]["unit_kWe"], extra_mass_t=5.0),
    dict(id="PM-F", name="Skid dewatering dan dosing", tags=["PR-501", "TK-201", "TK-202"], qty=1, mass_t_each=11.0,
         note="screw press %.1f m3/h, polymer unit, NaOH and urea-N dosing" % eq["screw_press"]["feed_m3_h"]),
]
tot_units = 0; tot_mass = 0.0
for m in mods:
    per = containers(m["mass_t_each"], m.get("vol_m3_each", 0.0)) + m.get("extra_units", 0)
    if m["id"] == "PM-E": per = 1
    m["iso_units_each"] = per
    m["iso_units_total"] = per * m["qty"] + (1 if m["id"] == "PM-E" else 0)          # +1 for the heat-recovery skid
    m["mass_t_total"] = m["mass_t_each"] * m["qty"] + m.get("extra_mass_t", 0.0)
    tot_units += m["iso_units_total"]; tot_mass += m["mass_t_total"]
area_dig = N * (dm["D_m"] + 3.0) ** 2
out = dict(modules=mods, iso_units_total=tot_units, mass_t_total=tot_mass, iso=ISO40,
           plot_area_m2_estimate=dict(digesters=area_dig, skids_and_roads=1200.0, total=area_dig + 1200.0),
           scaling={k: dict(digester_kits=v["N_modules"], chp_units=v["chp"]["N_gen"], chp_kWe=v["chp"]["P_unit"]) for k, v in R["tiers"].items()},
           assumptions="masses, shipping units and footprint are planning estimates [ASSUME]")
json.dump(out, open(os.path.join(D, "outputs", "portable_modules.json"), "w"), indent=1)
print("%-6s %-30s %4s %9s %8s" % ("id", "module", "qty", "t total", "ISO units"))
for m in mods: print("%-6s %-30s %4d %9.1f %8d" % (m["id"], m["name"], m["qty"], m["mass_t_total"], m["iso_units_total"]))
print("TOTAL: %d ISO-sized units, %.0f t shipped; plot ~ %.0f m2 (%.2f ha)" % (tot_units, tot_mass, out["plot_area_m2_estimate"]["total"], out["plot_area_m2_estimate"]["total"] / 1e4))
