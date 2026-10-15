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
mc = F.monte_carlo(4000, v=v)
fl = F.fleet(v)
tiers = {t: F.tier(t) for t in ("30", "45", "60")}
vr = dict(v); vr["fee_pome"] = 0.0
vc = dict(v); vc["p_carbon"] = 2.2
SC = [("Dasar\n(45 t/jam)", o), ("Relokasi th-11\n(tarif th 1-10)", F.run(v, relocate=True)), ("Tanpa jasa\nPOME", F.run(vr)),
      ("Karbon IDX\nUSD 2,2/t", F.run(vc)), ("Unit ke-10\n(kurva belajar)", F.run(v, capex_mult=10 ** np.log2(0.9))),
      ("Set 30 t/jam", tiers["30"]), ("Set 60 t/jam", tiers["60"])]
figs = dict(pasar=G.fig_market(o), porter=G.fig_porter_pestle(), capex=G.fig_capex_opex(o), cf=G.fig_cashflow(o),
            npv=G.fig_npv_tornado(o, torn, curve), pb=G.fig_payback(o), bep=G.fig_bep(o, be), mc=G.fig_mc(o, mc), fleet=G.fig_fleet(fl),
            sc=G.fig_scenarios(SC))
RES = dict(o=o, be=be, torn=torn, curve=curve, mc=mc, fl=fl, tiers=tiers, SC=SC, figs=figs, mk=MK.market(o))
if __name__ == "__main__":
    import fin_excel, fin_report
    fin_excel.build(RES)
    fin_report.build(RES)
    s = dict(FCI=o["fci"], NPV=o["NPV"], IRR=o["IRR"], IRR_eq=o["IRR_eq"], PBP=o["PBP"], DPBP=o["DPBP"], PI=o["PI"], DSCR_min=o["DSCR_min"],
             LCOE=o["LCOE"], WACC=o["wacc"], P_NPV_pos=float((mc["NPV"] > 0).mean()), fleet_NPV=fl["NPV"], fleet_IRR=fl["IRR"], fleet_peak=fl["peak"],
             BEP=be)
    json.dump(s, open(os.path.join(F.HERE, "outputs", "summary.json"), "w"), indent=1, default=float)
    print(json.dumps(s, indent=1, default=float)); print("%.0f s" % (time.time() - t0))
