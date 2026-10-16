# -*- coding: utf-8 -*-
"""
Relocatable module set of the Rev 2 product (thermophilic anaerobic contact process).  Reads outputs/results.json, writes outputs/portable_modules.json.

Rev 2 (Stage 1 red-team, research/R4):
  * reactors, feed buffer and effluent tank are BOLTED glass-fused-to-steel (GFS) tanks: enamelled panels are flat-packed in 40 ft containers,
    erected on a ring-beam slab in ~3 weeks per tank and can be dismantled and re-erected when the contract ends (no oversize road loads;
    the Rev 1 4.2 m shop vessels were 5.1 m high on a low-bed against the 4.2 m road limit);
  * all rotating equipment, settler, gas treatment and CHP sit in 40 ft containers or container-size skids;
  * the AnMBR membrane is an OPTIONAL container (PM-11) for sites that need water reuse; not in the base case.
Masses and counts are PLANNING ESTIMATES [ASSUME] - confirm with fabricators.
"""
import json, math, os
D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "outputs", "results.json"), encoding="utf-8"))
eq = R["equipment"]; rv = eq["reactor_vessel"]
N = rv["count"]
STEEL = 7.85; T_PANEL = 0.007                                             # t/m3, 7 mm mean GFS panel (5-10 mm by course)  [ASSUME]
PANEL_A = 2.7 * 1.2

def gfs(D_, H_):
    """bolted GFS tank: panel count, steel + roof + insulation/cladding + internals (t), container loads (26 t / 40 ft)."""
    n_pan = math.ceil(math.pi * D_ / 2.7) * math.ceil(H_ / 1.2)
    m = n_pan * PANEL_A * T_PANEL * STEEL * 1.08 + 0.012 * math.pi / 4 * D_ ** 2 + 0.02 * math.pi * D_ * H_ + 2.0
    return dict(D=D_, H=H_, panels=n_pan, mass_t=m, containers=max(1, math.ceil(m / 22.0)))

rx = gfs(rv["D_m"], rv["H_shell_m"])
fb = gfs(5.73, 5.0)                                                       # feed buffer ~ 4 h at peak  [ASSUME standard size]
et = gfs(6.88, 5.0)                                                       # effluent / recycle balance tank ~ 6 h
ls = eq["lamella_settler"]
mods = [
    dict(id="PM-1", name="Skid praolah POME", tags=["SC-101", "HC-101", "E-101"], qty=1, mass_t_each=12.0, unit="kontainer 40 ft (skid)",
         note="rotary screen, grit chamber + hydrocyclone (%.0f %% grit), plate cooler %.0f kWth" % (eq["desander"]["grit_removal"] * 100, eq["pome_cooler"]["duty_kW"])),
    dict(id="PM-2", name="Tangki GFS penyangga umpan", tags=["TK-101"], qty=1, mass_t_each=fb["mass_t"], unit="panel GFS dalam kontainer 40 ft",
         note="D %.2f m, %.0f m3, %d panel" % (fb["D"], math.pi / 4 * fb["D"] ** 2 * (fb["H"] - 0.5), fb["panels"]), ship_units=fb["containers"]),
    dict(id="PM-3", name="Reaktor kontak termofilik (tangki GFS dibaut)", tags=["R-201..R-2%02d" % N, "P-202 (per reaktor)"], qty=N, mass_t_each=rx["mass_t"],
         unit="panel GFS dalam kontainer 40 ft", ship_units=N * rx["containers"],
         note="D %.2f m x H %.1f m, %.0f m3, 55 C, jet mixing, atap membran ganda; %d panel/tangki, %d kontainer/tangki"
              % (rv["D_m"], rv["H_shell_m"], rv["V_liq_m3"], rx["panels"], rx["containers"])),
    dict(id="PM-4", name="Skid kontak: degasser vakum + settler lamella + pompa resirkulasi", tags=["DG-301", "LS-301", "P-301", "P-302"], qty=1, mass_t_each=18.0,
         unit="2 skid 40 ft", ship_units=2,
         note="lamella %.0f m2 proyeksi pada %.1f m3/m2.jam, resirkulasi %.0f m3/d, underflow x%.2f" % (ls["A_proj_m2"], ls["rate_m3_m2h"], ls["recycle_m3d"], ls["underflow_factor"])),
    dict(id="PM-5", name="Skid dosing dan pompa umpan", tags=["P-201", "TK-201", "P-203"], qty=1, mass_t_each=8.0, unit="skid 20 ft",
         note="feed pumps, NaOH dosing (urea-N standby only)"),
    dict(id="PM-6", name="Skid pengolahan biogas", tags=["BTF-301", "K-301", "HX-301", "V-301", "K-302", "AC-301"], qty=1, mass_t_each=14.0, unit="kontainer 40 ft + bejana BTF",
         note="%.0f Nm3/h; BTF %.0f m3 packing ships as its own vessel" % (eq["bio_desulfurizer"]["gas_Nm3_h"], eq["bio_desulfurizer"]["V_m3"]), extra_units=1),
    dict(id="PM-7", name="Penampung gas + flare", tags=["GH-301", "FL-301"], qty=1, mass_t_each=7.0, unit="kontainer 20 ft (membran terlipat) + skid flare",
         note="double-membrane gas holder %.0f m3 (%.0f h), flare %.0f Nm3/h" % (eq["gas_holder"]["V_m3"], eq["gas_holder"]["hours"], eq["flare"]["cap_Nm3_h"]), extra_units=1),
    dict(id="PM-8", name="Kontainer CHP", tags=["GE-401", "GE-402", "ST-401"], qty=eq["chp"]["N"], mass_t_each=20.0, unit="kontainer 40 ft HC",
         note="%.0f kWe biogas engine-generator per container" % eq["chp"]["unit_kWe"]),
    dict(id="PM-9", name="Skid pemulih panas + menara pendingin", tags=["HX-401", "CT-601"], qty=1, mass_t_each=9.0, unit="skid 20 ft + sel CT modular",
         note="hot-water recovery %.0f kWth; cooling %.0f kWth" % (R["energy"]["Q_heat_avail"], eq["cooling_tower"]["duty_kW"]), extra_units=1),
    dict(id="PM-10", name="Tangki GFS efluen + skid lumpur", tags=["TK-301", "P-303", "PR-501", "P-501"], qty=1, mass_t_each=et["mass_t"] + 8.0, unit="panel GFS + skid 20 ft",
         note="effluent tank D %.2f m; screw press %.0f m3/d waste underflow -> %.1f t/d cake" % (et["D"], eq["waste_sludge"]["Qw_m3d"], eq["waste_sludge"]["cake_t_d"]),
         ship_units=et["containers"] + 1),
]
opt = R["membrane_option"]
option = dict(id="PM-11 (opsi)", name="Kontainer membran AnMBR (opsional, reuse air)", qty=opt["containers"], area_m2=opt["area_m2"], kW=opt["kW"], capex_USD=opt["capex_USD"],
              note="tidak termasuk kasus dasar: +%.0f Nm3 CH4/d (+%.0f kWe kotor) vs %.0f kW cross-flow" % (opt["ch4_gain_Nm3d"], opt["kWe_gain_gross"], opt["kW"]))
tot_u = 0; tot_m = 0.0
for m in mods:
    m["ship_units"] = m.get("ship_units", m["qty"]) + m.get("extra_units", 0)
    m["mass_t_total"] = m["mass_t_each"] * m["qty"]
    tot_u += m["ship_units"]; tot_m += m["mass_t_total"]
pitch = rv["D_m"] + 3.0
area_v = (N * pitch + 6.0) * (pitch + 6.0)
GA = os.path.join(D, "..", "cad", "out", "ga.json")          # tata letak umum dari model 3D (cad/drawings/d01_ga.py)
plot = dict(vessels=area_v, skids_and_roads=1400.0, total=area_v + 1400.0, source="perkiraan rumus")
if os.path.exists(GA):
    g = json.load(open(GA))
    if g.get("rev", 1) >= 2:
        plot = dict(total=g["plot_m2"], x_m=g["plot_x_m"], y_m=g["plot_y_m"], source="GA 3D BG-GA-001 (termasuk jalan 3 m)")
out = dict(modules=mods, option=option, ship_units_total=tot_u, mass_t_total=tot_m,
           vessel=dict(D=rv["D_m"], H_shell=rv["H_shell_m"], V=rv["V_liq_m3"], mass_t=rx["mass_t"], panels=rx["panels"], containers=rx["containers"], type="bolted GFS"),
           small_tanks=dict(feed=fb, effluent=et),
           plot_area_m2_estimate=plot,
           scaling={k: dict(vessels=v["N_modules"], chp_units=v["chp"]["N_gen"], chp_kWe=v["chp"]["P_unit"], lamella_m2=v["settler"]["A_lam"]) for k, v in R["tiers"].items()},
           rev_comparison=dict(rev0_digester_m3=14000, rev1_reactor_m3=14 * 193.96, rev2_reactor_m3=N * rv["V_liq_m3"], rev1_vessels=14, rev2_tanks=N),
           assumptions="masses, shipping units and footprint are planning estimates [ASSUME]")
json.dump(out, open(os.path.join(D, "outputs", "portable_modules.json"), "w"), indent=1)
print("%-6s %-60s %4s %8s %6s" % ("id", "module", "qty", "t total", "loads"))
for m in mods: print("%-6s %-60s %4d %8.1f %6d" % (m["id"], m["name"], m["qty"], m["mass_t_total"], m["ship_units"]))
print("TOTAL %d truck loads, %.0f t; GFS reactor %.1f t (%d panels, %d containers); plot ~%.0f m2 (%.2f ha)" % (tot_u, tot_m, rx["mass_t"], rx["panels"], rx["containers"],
      out["plot_area_m2_estimate"]["total"], out["plot_area_m2_estimate"]["total"] / 1e4))
