# -*- coding: utf-8 -*-
"""Jalankan seluruh analisis ekonomi v3: model pengembang, Model Keputusan PKS, pasar, gambar, Excel, laporan PDF.  python3 run_all.py"""
import json, os, time, numpy as np
import fin_core as F, fin_market as MK, fin_mill as MI, fin_figs as G
t0 = time.time()
v = F.vals()
o = F.run(v)
be = F.bep(v)
torn = F.tornado(v)
curve = F.npv_curve(v)
mc = F.monte_carlo(3000, v=v)
fl = F.fleet(v)
tiers = {t: F.tier(t) for t in ("30", "45", "60")}
mill = MI.compare(v); fw = MI.fee_window(v); seg = MI.segments(v); wf = MI.waterfall(v)
comp = MK.compet_matrix(mill); reloc = MK.relocation_value(); usp = MK.usp(o, mill, reloc)
v0 = dict(v); v0["fee_ffb"] = 0.0
vg = dict(v); vg["diesel_L_tffb"] = 0.53
vc = dict(v); vc["p_carbon"] = 8.3
SC = [("Dasar S3\n(fee USD %.2f/t)" % v["fee_ffb"], o), ("Tanpa fee\nPOME", F.run(v0)), ("PKS terhubung PLN\n(S1, solar 0,53 L/t)", F.run(vg)),
      ("Karbon USD 8,3/t\n(puncak 2024)", F.run(vc)), ("Relokasi\nth-11", F.run(v, relocate=True)),
      ("Unit ke-10\n(kurva belajar)", F.run(v, capex_mult=F.LEARN_SHARE * 10 ** np.log2(0.9) + 1 - F.LEARN_SHARE)),
      ("Set 30 t/jam", tiers["30"]), ("Set 60 t/jam", tiers["60"])]
figs = dict(pasar=G.fig_market(o), porter=G.fig_porter_pestle(), capex=G.fig_capex_opex(o), cf=G.fig_cashflow(o),
            npv=G.fig_npv_tornado(o, torn, curve), pb=G.fig_payback(o), bep=G.fig_bep(o, be), mc=G.fig_mc(o, mc), fleet=G.fig_fleet(fl),
            sc=G.fig_scenarios(SC), mill=G.fig_mill(mill, wf, fw), seg=G.fig_segments(seg, v["fee_ffb"]), comp=G.fig_compet(comp))
RES = dict(o=o, be=be, torn=torn, curve=curve, mc=mc, fl=fl, tiers=tiers, SC=SC, figs=figs, mk=MK.market(o), mill=mill, fw=fw, seg=seg, wf=wf,
           comp=comp, reloc=reloc, usp=usp)
_i = 3
ENERGY_SPLIT = dict(captive_GWh=float(o["Ecap"][_i]), export_GWh=float(o["Eexp"][_i]), total_GWh=float(o["E"][_i]))
if __name__ == "__main__":
    import fin_excel, fin_report
    fin_excel.build(RES)
    fin_report.build(RES)
    s = dict(FCI=o["fci"], FCI_2026=o["fci26"], NPV=o["NPV"], IRR=o["IRR"], IRR_eq=o["IRR_eq"], PBP=o["PBP"], DPBP=o["DPBP"], PI=o["PI"], DSCR_min=o["DSCR_min"],
             LCOE=o["LCOE"], WACC=o["wacc"], P_NPV_pos=float((mc["NPV"] > 0).mean()), fleet_NPV=fl["NPV"], fleet_IRR=fl["IRR"], fleet_peak=fl["peak"],
             share_fee=o["share_fee"], share_el=o["share_el"], share_c=o["share_c"], BEP=be, energy_split=ENERGY_SPLIT, ER_t=o["ER"],
             mill={k_: dict(annual=mill[k_]["annual"], per_t=mill[k_]["per_t"], capex=mill[k_]["capex"]) for k_ in "ABCD"},
             mill_saving_pct=mill["saving_D_vs_A_pct"], mill_saving_per_t=mill["saving_D_vs_A_per_t"], fee_window=fw,
             segments=[{k_: (float(x) if isinstance(x, (float, np.floating)) else x) for k_, x in sg.items()} for sg in seg], relocation=reloc,
             market={k_: mk_ for k_, mk_ in RES["mk"].items() if k_ != "rows"},
             scenarios={n.replace("\n", " "): dict(NPV=x["NPV"], IRR=x["IRR"]) for n, x in SC})
    json.dump(s, open(os.path.join(F.HERE, "outputs", "summary.json"), "w"), indent=1, default=float)
    print(json.dumps({k_: s[k_] for k_ in ("FCI", "NPV", "IRR", "IRR_eq", "PBP", "DSCR_min", "P_NPV_pos", "fleet_NPV", "fleet_IRR", "mill_saving_pct", "fee_window", "scenarios")}, indent=1, default=float))
    print("%.0f s" % (time.time() - t0))
