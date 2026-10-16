# -*- coding: utf-8 -*-
"""Menambahkan 'kasus target' (setelah gerbang G0-G2 + harga karbon) ke deck/deck_data.json.
Kasus target = kasus dasar + solar tergantikan 3,0 L/t (G0), CAPEX -15% (G1), fee USD 1,35/t (G2), karbon USD 8,3/t. Semua dari fin_core.run()."""
import os, sys, json
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "finance")); os.chdir(os.path.join(ROOT, "finance"))
import fin_core as F, fin_mill as MI
f = float
D = json.load(open(os.path.join(ROOT, "deck", "deck_data.json")))
v = F.vals(); ob = F.run(v)
STEPS = [("G0 · solar tergantikan 3,0 L/t", dict(diesel_L_tffb=3.0), 1.0), ("G1 · CAPEX −15% (kuotasi)", {}, 0.85), ("G2 · fee USD 1,35/t", dict(fee_ffb=1.35), 0.85), ("Karbon USD 8,3/t", dict(p_carbon=8.3), 0.85)]
vt = dict(v); cm = 1.0; chain = [("Kasus awal", ob)]
for lab, kw, c in STEPS:
    vt.update(kw); cm = c; chain.append((lab, F.run(dict(vt), capex_mult=cm)))
o = chain[-1][1]; yrs = o["years"]
ind = lambda o_: dict(NPV=f(o_["NPV"]), IRR=f(o_["IRR"]), IRR_eq=f(o_["IRR_eq"]), PBP=f(o_["PBP"]), DPBP=f(o_["DPBP"]), DSCR=f(o_["DSCR_min"]), DSCR_avg=f(o_["DSCR_avg"]), PI=f(o_["PI"]), LCOE=f(o_["LCOE"]), LCOE_net=f(o_["LCOE_net"]), peak=f(o_["peak_funding"]), FCI=f(o_["fci"]), FCI26=f(o_["fci26"]))
T = dict(ind(o), years=yrs, WACC=f(o["wacc"]), fee=vt["fee_ffb"], diesel=vt["diesel_L_tffb"], carbon=vt["p_carbon"], capex_mult=cm,
    cf=dict(rev=[f(x) for x in o["rev"]], opex=[f(x) for x in o["opex_tot"]], ebitda=[f(x) for x in o["ebitda"]], fcff=[f(x) for x in o["fcff"]], cum=[f(x) for x in np.cumsum(o["fcff"])], cumd=[f(x) for x in np.cumsum(o["fcff"] * o["disc"])],
            rev_fee=[f(x) for x in o["rev_fee"]], rev_cap=[f(x) for x in o["rev_cap"]], rev_exp=[f(x) for x in o["rev_exp"]], rev_c=[f(x) for x in o["rev_c"]]),
    E_net=f(o["E"][3]), E_cap=f(o["Ecap"][3]), E_exp=f(o["Eexp"][3]), opF=f(o["opF"]), opV=f(o["opV"]),
    chain=[dict(l=l, **ind(o_)) for l, o_ in chain])
# CAPEX per kategori: skala dengan rasio FCI
D["tgt"] = T; r = o["fci26"] / ob["fci26"]; T["capex_cat"] = {k: x * r for k, x in D["keu"]["capex_cat"].items()}; T["capex_ratio"] = f(r)
# BEP terhadap beban PKS
bs = []
for u in np.arange(0.10, 1.001, 0.05):
    oo = F.run(dict(vt, util=float(u)), capex_mult=cm); i = 3
    bs.append(dict(util=float(u), rev=f(oo["rev"][i]), opex=f(oo["opex_tot"][i]), dep=f(oo["fci"] / vt["n_op"]), intr=f(oo["intr"][i]), npv=f(oo["NPV"])))
for b in bs: b["tc"] = b["opex"] + b["dep"] + b["intr"]
def cross(a, b_):
    xs = [(b["util"], b[a] - b[b_]) for b in bs]
    for (u0, d0), (u1, d1) in zip(xs[:-1], xs[1:]):
        if d0 <= 0 <= d1: return u0 + (u1 - u0) * (-d0) / (d1 - d0)
    return None
T["bep_series"] = bs; T["bep_util_cash"] = cross("rev", "opex"); T["bep_util_acc"] = cross("rev", "tc")
xs = [(b["util"], b["npv"]) for b in bs]; T["bep_util_npv"] = None
for (u0, d0), (u1, d1) in zip(xs[:-1], xs[1:]):
    if d0 <= 0 <= d1: T["bep_util_npv"] = u0 + (u1 - u0) * (-d0) / (d1 - d0)
# ambang impas NPV kasus target (ruang aman)
def sv(fun, lo, hi): return F.solve(fun, lo, hi)
T["be"] = dict(
    diesel=f(sv(lambda x: F.run(dict(vt, diesel_L_tffb=x), capex_mult=cm)["NPV"], 0.0, 3.0)), fee=f(sv(lambda x: F.run(dict(vt, fee_ffb=x), capex_mult=cm)["NPV"], 0.0, 3.0)),
    util=f(sv(lambda x: F.run(dict(vt, util=x), capex_mult=cm)["NPV"], 0.2, 1.0)), carbon=f(sv(lambda x: F.run(dict(vt, p_carbon=x), capex_mult=cm)["NPV"], -20.0, 20.0)),
    capex=f(sv(lambda x: F.run(dict(vt), capex_mult=x)["NPV"], 0.5, 3.0)), tariff1=f(sv(lambda x: F.run(dict(vt, tariff1=x), capex_mult=cm)["NPV"], 0.0, 30.0)),
    emult=f(sv(lambda x: F.run(dict(vt), emult=x, capex_mult=cm)["NPV"], 0.2, 1.2)))
# tuas nilai satu per satu terhadap kasus awal
lev = [("Kasus awal", {}, 1.0), ("Solar tergantikan 3,0 L/t", dict(diesel_L_tffb=3.0), 1.0), ("CAPEX −15% (kuotasi)", {}, 0.85), ("Unit ke-10 (kurva belajar)", {}, None), ("Fee USD 1,35/t", dict(fee_ffb=1.35), 1.0), ("Karbon USD 8,3/t", dict(p_carbon=8.3), 1.0), ("Beban PKS 85%", dict(util=0.85), 1.0), ("Faktor lokasi F 1,10", dict(F_loc=1.10), 1.0), ("Kasus target", None, None)]
LRN = F.LEARN_SHARE * 10 ** np.log2(0.9) + 1 - F.LEARN_SHARE; out = []
for l, kw, c in lev:
    if l == "Kasus target": oo = o
    else: oo = F.run(dict(v, **(kw or {})), capex_mult=(LRN if c is None else c))
    out.append(dict(l=l, NPV=f(oo["NPV"]), IRR=f(oo["IRR"]), PBP=f(oo["PBP"])))
T["levers"] = out
rob = []
for l, kw in [("Kasus target", {}), ("Tanpa pendapatan karbon", dict(p_carbon=0.0)), ("Solar tergantikan turun ke 1,0 L/t", dict(diesel_L_tffb=1.0)), ("Tarif ekspor PLN 7,44 USc/kWh", dict(tariff1=7.44, tariff2=4.46)), ("Fee turun ke USD 1,00/t", dict(fee_ffb=1.0)), ("Beban PKS turun ke 60%", dict(util=0.60))]:
    oo = F.run(dict(vt, **kw), capex_mult=cm); rob.append(dict(l=l, NPV=f(oo["NPV"]), IRR=f(oo["IRR"]), PBP=f(oo["PBP"])))
T["robust"] = rob
# PKS: biaya POME dan jendela fee pada kasus target
c = MI.compare(vt); fw = MI.fee_window(vt)
T["pks"] = dict(per_t={k: f(c[k]["per_t"]) for k in "ABCD"}, capex={k: f(c[k]["capex"]) for k in "ABCD"}, save_pct=f(c["saving_D_vs_A_pct"]), save_t=f(c["saving_D_vs_A_per_t"]), fw={k: f(x) for k, x in fw.items()})
# armada pada kasus target
fl = F.fleet(vt); i0 = fl["years"].index(2035)
T["fleet"] = dict(NPV=f(fl["NPV"]), IRR=f(fl["IRR"]) if fl["IRR"] == fl["IRR"] else None, peak=f(fl["peak"]), years=fl["years"], sets_op=[f(x) for x in fl["sets_op"]], rev=[f(x) for x in fl["rev"]], ebitda=[f(x) for x in fl["ebitda"]], co2=[f(x) for x in fl["co2"]], E=[f(x) for x in fl["E"]])
T["be"] = {k: (x if x == x else None) for k, x in T["be"].items()}
fees = [0.8, 1.0, 1.2, 1.35, 1.5, 1.7]; dsl = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
T["heat"] = dict(fees=fees, diesel=dsl, npv=[[f(F.run(dict(vt, diesel_L_tffb=d, fee_ffb=x), capex_mult=cm)["NPV"] / 1e6) for x in fees] for d in dsl])
T["segsave"] = [dict(d=d, save=f(MI.compare(dict(vt, diesel_L_tffb=d))["saving_D_vs_A_pct"]), npv=f(F.run(dict(vt, diesel_L_tffb=d), capex_mult=cm)["NPV"] / 1e6), per_t_A=f(MI.compare(dict(vt, diesel_L_tffb=d))["A"]["per_t"])) for d in dsl]
T["fleet"]["rev_fee"] = [f(x) for x in fl["rev_fee"]]; T["fleet"]["rev_el"] = [f(x) for x in fl["rev_el"]]; T["fleet"]["rev_c"] = [f(x) for x in fl["rev_c"]]
json.dump(D, open(os.path.join(ROOT, "deck", "deck_data.json"), "w"), indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))
print({k: (round(T[k], 3) if isinstance(T[k], float) else None) for k in ("NPV", "IRR", "IRR_eq", "PBP", "DPBP", "DSCR", "FCI", "peak")}); print(T["be"]); print([(x["l"], round(x["NPV"] / 1e6, 2)) for x in T["levers"]]); print("flt", T["fleet"]["NPV"], T["fleet"]["peak"], T["fleet"]["IRR"], T["pks"]["per_t"], T["pks"]["save_pct"], T["bep_util_acc"], T["bep_util_npv"])
