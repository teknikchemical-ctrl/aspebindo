# -*- coding: utf-8 -*-
"""Jalankan seluruh analisis ekonomi: model, gambar, Excel, laporan PDF.  python3 run_all.py"""
import json, os, time, numpy as np
import fin_core as F, fin_market as MK, fin_figs as G
t0 = time.time()
v = F.vals()
o = F.run(v)
be = F.bep(v)
torn = F.tornado(v)
curve = F.npv_curve(v)
mc = F.monte_carlo(3000, v=v)
fl = F.fleet(v)
tiers = {t: F.tier(t) for t in ("30", "45", "60")}
v0 = dict(v); v0["fee_ffb"] = 0.0
vt = dict(v); vt["tariff1"], vt["tariff2"] = 9.81, 5.89
vc = dict(v); vc["p_carbon"] = 12.0
SC = [("Dasar\n(jasa USD 2,0/t)", o), ("Tanpa jasa\nPOME", F.run(v0)), ("Tier >1 MW\n(kap. terpasang)", F.run(vt)),
      ("Karbon USD 12/t\n(otorisasi)", F.run(vc)), ("Relokasi\nth-11", F.run(v, relocate=True)),
      ("Unit ke-10\n(kurva belajar)", F.run(v, capex_mult=F.LEARN_SHARE * 10 ** np.log2(0.9) + 1 - F.LEARN_SHARE)),
      ("Set 30 t/jam", tiers["30"]), ("Set 60 t/jam", tiers["60"])]
figs = dict(pasar=G.fig_market(o), porter=G.fig_porter_pestle(), capex=G.fig_capex_opex(o), cf=G.fig_cashflow(o),
            npv=G.fig_npv_tornado(o, torn, curve), pb=G.fig_payback(o), bep=G.fig_bep(o, be), mc=G.fig_mc(o, mc), fleet=G.fig_fleet(fl),
            sc=G.fig_scenarios(SC))
RES = dict(o=o, be=be, torn=torn, curve=curve, mc=mc, fl=fl, tiers=tiers, SC=SC, figs=figs, mk=MK.market(o))
_i = 3
ENERGY_SPLIT = dict(captive_GWh=float(o["Ecap"][_i]), export_GWh=float(o["Eexp"][_i]), total_GWh=float(o["E"][_i]))
if __name__ == "__main__":
    import fin_excel, fin_report
    fin_excel.build(RES)
    fin_report.build(RES)
    s = dict(FCI=o["fci"], FCI_2026=o["fci26"], NPV=o["NPV"], IRR=o["IRR"], IRR_eq=o["IRR_eq"], PBP=o["PBP"], DPBP=o["DPBP"], PI=o["PI"], DSCR_min=o["DSCR_min"],
             LCOE=o["LCOE"], WACC=o["wacc"], P_NPV_pos=float((mc["NPV"] > 0).mean()), fleet_NPV=fl["NPV"], fleet_IRR=fl["IRR"], fleet_peak=fl["peak"],
             share_fee=o["share_fee"], share_el=o["share_el"], share_c=o["share_c"], BEP=be, energy_split=ENERGY_SPLIT, ER_t=o["ER"],
             scenarios={n.replace("\n", " "): dict(NPV=x["NPV"], IRR=x["IRR"]) for n, x in SC})
    json.dump(s, open(os.path.join(F.HERE, "outputs", "summary.json"), "w"), indent=1, default=float)
    print(json.dumps(s, indent=1, default=float)); print("%.0f s" % (time.time() - t0))
