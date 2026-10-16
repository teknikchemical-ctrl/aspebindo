# -*- coding: utf-8 -*-
"""Mengekspor SEMUA angka deck dari model proses dan keuangan ke deck/deck_data.json (satu sumber kebenaran untuk build_deck.js).
Jalankan dari akar repo:  python3 deck/export_data.py   (konfigurasi komersial = tier 60 t TBS/jam + PM-12; modul acuan = 45 t/jam)"""
import os, sys, json, math
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "finance")); os.chdir(os.path.join(ROOT, "finance"))
import fin_core as F, fin_mill as MI, fin_market as MK
R = F.R; v = F.vals(); o = F.run(v); T = F.TECH
f = lambda x: float(x)
D = {}
# ------------------------------------------------------------------ proses (modul acuan 45 t/jam dan tier 60)
t45, t60 = R["tiers"]["45"], R["tiers"]["60"]
nom = R["nominal"]; en = R["energy"]; eq = R["equipment"]; db = R["design_basis"]
D["proses"] = dict(
    ffb_tph=db["ffb_tph"], pome_m3d=db["pome_m3d"], cod_in=db["cod_blend"], T=55.0, hrt=eq["reactor_vessel"]["hrt_d"], srt=eq["reactor_vessel"]["srt_d"], olr=nom["olr"],
    V_tank=eq["reactor_vessel"]["V_liq_m3"], D_tank=eq["reactor_vessel"]["D_m"], H_liq=eq["reactor_vessel"]["H_liq_m"], n45=t45["N_modules"], n60=t60["N_modules"],
    biogas45=t45["biogas_Nm3d"], ch445=t45["ch4_Nm3d"], biogas60=t60["biogas_Nm3d"], ch460=t60["ch4_Nm3d"], ch4_frac=nom["ch4_frac"], cod_rem=nom["cod_rem"], h2s_raw=nom["h2s_ppm_raw"], h2s_fuel=nom["h2s_ppm_fuel"],
    pH=nom["pH"], vfa=nom["vfa_mgL"], fos=nom["fos_tac"], mlss=nom["mlss"],
    P_gross45=t45["P_gross"], P_net45=t45["P_net"], P_gross60=t60["P_gross"], P_net60=t60["P_net"], chp45=t45["chp"]["P_inst"], chp60=t60["chp"]["P_inst"],
    GWh45=t45["GWh_y"], GWh60=t60["GWh_y"], A_lam=eq["lamella_settler"]["A_proj_m2"], recycle=eq["lamella_settler"]["recycle_m3d"], capture=eq["lamella_settler"]["capture"],
    eta_el=en["chp"]["eta_el"], util_proc=R["year"]["util"], eff=R["effluent"], mc=R["monte_carlo"], year=dict(min_pH=R["year"]["min_pH"], max_fos=R["year"]["max_fos"]),
    parasitic={k: f(x) for k, x in en["parasitic"].items()}, P_par=en["P_par"], Q_jacket=en["chp"]["Q_jacket"], Q_exh=en["chp"]["Q_exh"], Q_dig=en["Q_dig"], Q_heat_avail=en["Q_heat_avail"],
    Q_cool=en["Q_cool"], fuel_kW=en["fuel_kW"], tiers={k: dict(ffb=x["ffb_tph"], N=x["N_modules"], V=x["V_total"], bg=x["biogas_Nm3d"], Pg=x["P_gross"], Pn=x["P_net"], chp=x["chp"]["P_inst"], GWh=x["GWh_y"]) for k, x in R["tiers"].items()},
    mc_sens=R["monte_carlo"].get("spearman", {}))
# neraca massa (kg/jam, hari nameplate 45 t/jam), dikelompokkan
S = {s["id"]: s for s in R["streams"]}
mass_in = [("POME mentah (S1)", S[1]["kg_h"]), ("Udara ke BTF (S17)", S[17]["kg_h"]), ("Udara pembakaran (S23)", S[23]["kg_h"]), ("Polimer flokulan (S26)", S[26]["kg_h"]), ("NaOH + urea (S5, S6)", S[5]["kg_h"] + S[6]["kg_h"])]
mass_out = [("Residu saringan dan pasir (S2)", S[2]["kg_h"]), ("Kue lumpur (S12)", S[12]["kg_h"]), ("Efluen ke kolam polishing (S14)", S[14]["kg_h"]), ("Blowdown BTF (S19)", S[19]["kg_h"]),
            ("Kondensat chiller (S20)", S[20]["kg_h"]), ("Gas buang genset (S24)", S[24]["kg_h"]), ("Gas ke flare (S22)", S[22]["kg_h"]), ("Karbon aktif jenuh (S25)", S[25]["kg_h"])]
D["massa"] = dict(inn=[(a, f(b)) for a, b in mass_in], out=[(a, f(b)) for a, b in mass_out], sum_in=f(sum(b for _, b in mass_in)), sum_out=f(sum(b for _, b in mass_out)),
                  closure=R["closure"], streams=[dict(id=s["id"], name=s["name"], T=s["T"], P=s["P"], kg_h=f(s["kg_h"])) for s in R["streams"]],
                  cod=nom["cod_routing_kgd"], cod_in_kgd=f(sum(nom["cod_routing_kgd"].values())))
# ------------------------------------------------------------------ keuangan: kasus dasar (60 t/jam + PM-12)
n = int(v["n_op"]); yrs = o["years"]
D["keu"] = dict(
    tier=F.BASE_TIER, ffb_tph=T["ffb_tph"], ffb_ty=T["ffb_ty_nom"] * v["util"], n_vessel=T["n_vessel"], chp=T["chp_kWe"], E_net=f(o["E"][3]), E_cap=f(o["Ecap"][3]), E_exp=f(o["Eexp"][3]),
    FCI=f(o["fci"]), FCI26=f(o["fci26"]), PEC=f(o["pec"]), IDC=f(o["idc"]), debt0=f(o["debt0"]), NPV=f(o["NPV"]), IRR=f(o["IRR"]), IRR_eq=f(o["IRR_eq"]), PBP=f(o["PBP"]), DPBP=f(o["DPBP"]), PI=f(o["PI"]),
    DSCR=f(o["DSCR_min"]), DSCR_avg=f(o["DSCR_avg"]), LCOE=f(o["LCOE"]), LCOE_net=f(o["LCOE_net"]), peak=f(o["peak_funding"]), WACC=f(o["wacc"]), ER=f(o["ER"]), fee=v["fee_ffb"],
    share=dict(fee=f(o["share_fee"]), el=f(o["share_el"]), c=f(o["share_c"])), years=yrs,
    cf=dict(rev=[f(x) for x in o["rev"]], opex=[f(x) for x in o["opex_tot"]], ebitda=[f(x) for x in o["ebitda"]], fcff=[f(x) for x in o["fcff"]], cum=[f(x) for x in np.cumsum(o["fcff"])],
            cumd=[f(x) for x in np.cumsum(o["fcff"] * o["disc"])], rev_fee=[f(x) for x in o["rev_fee"]], rev_cap=[f(x) for x in o["rev_cap"]], rev_exp=[f(x) for x in o["rev_exp"]],
            rev_c=[f(x) for x in o["rev_c"]], tax=[f(x) for x in o["tax_u"]], capex=[f(x) for x in o["capex"]], sust=[f(x) for x in o["sust"]], dwc=[f(x) for x in o["dwc"]],
            intr=[f(x) for x in o["intr"]], princ=[f(x) for x in o["princ"]], cfads=[f(x) for x in o["cfads"]], fcfe=[f(x) for x in o["fcfe"]], bal=[f(x) for x in o["bal"]], wc=[f(x) for x in o["wc"]]),
    capex_rows=[dict(g=g, n=nm, q=f(q), u=u, c=f(c), t=f(t), b=b) for g, nm, q, u, c, t, b in o["capex_rows"]],
    opex_items={k: dict(v=f(x), t=t_) for k, (x, t_) in o["opex_items"].items()}, opF=f(o["opF"]), opV=f(o["opV"]),
    assumptions={k: dict(v=(x[0] if not isinstance(x[0], (np.floating, np.integer)) else f(x[0])), u=x[1], src=x[2], lo=x[3], hi=x[4]) for k, x in F.A.items()},
    match=f(F.match_f(v)), load_kW=f(F.load_kW(v)), E_dsl_GWh=f(T["ffb_ty_nom"] * v["util"] * v["diesel_L_tffb"] / v["sfc"] / 1e6))
be = F.bep(v); D["keu"]["bep"] = {k: (f(x) if x == x else None) for k, x in be.items()}
# CAPEX per kelompok
grp = {}
for r in D["keu"]["capex_rows"]: grp[r["g"]] = grp.get(r["g"], 0) + r["t"]
D["keu"]["capex_grp"] = grp
# ------------------------------------------------------------------ tornado realistis, MC, gerbang
tb, tr = F.tornado_real(v); D["keu"]["tornado"] = dict(base=f(tb), rows=[dict(l=a, lo=f(b), hi=f(c), xlo=f(d), xhi=f(e)) for a, b, c, d, e in tr])
mc = F.monte_carlo(4000, v=v); N_ = mc["NPV"]; I_ = mc["IRR"]
h, ed = np.histogram(N_ / 1e6, bins=24)
D["keu"]["mc"] = dict(N=len(N_), p_pos=f((N_ > 0).mean()), P10=f(np.percentile(N_, 10)), P50=f(np.percentile(N_, 50)), P90=f(np.percentile(N_, 90)), mean=f(N_.mean()),
                      p_irr=f((np.nan_to_num(I_, nan=-1) > o["wacc"]).mean()), hist=[int(x) for x in h], edges=[f(x) for x in ed], spearman={k: f(x) for k, x in mc["spearman"].items()}, dist=F.MC_DIST, cfg=F.MC_CFG)
gates = []
for lab, cfg in (("Sekarang", {}), ("G0 log solar PKS mitra", dict(diesel=(1.8, 2.0, 2.2))), ("G1 + kuotasi vendor", dict(diesel=(1.8, 2.0, 2.2), capex=(0.95, 1.0, 1.12))),
                 ("G2 + kepastian tarif dan izin", dict(diesel=(1.8, 2.0, 2.2), capex=(0.95, 1.0, 1.12), regimeB=0.0)),
                 ("G3 + kontrak jasa dan TBS", dict(diesel=(1.8, 2.0, 2.2), capex=(0.95, 1.0, 1.12), regimeB=0.0, util=(0.70, 0.75, 0.80), fee=(0.95, 1.0, 1.05)))):
    m_ = F.monte_carlo(2000, v=v, cfg=cfg)["NPV"]; gates.append(dict(l=lab, p=f((m_ > 0).mean()), P50=f(np.percentile(m_, 50)), P10=f(np.percentile(m_, 10)), P90=f(np.percentile(m_, 90))))
D["keu"]["gates"] = gates
# kasus target (solar 3,0 L/t) dan skenario
def case(tag, **kw):
    vv = dict(v); vv.update(kw); oo = F.run(vv); c = MI.compare(vv)
    return dict(tag=tag, NPV=f(oo["NPV"]), IRR=f(oo["IRR"]) if oo["IRR"] == oo["IRR"] else None, IRR_eq=f(oo["IRR_eq"]) if oo["IRR_eq"] == oo["IRR_eq"] else None, DSCR=f(oo["DSCR_min"]), FCI=f(oo["fci"]),
                PBP=f(oo["PBP"]) if oo["PBP"] == oo["PBP"] else None, save=f(c["saving_D_vs_A_pct"]), save_t=f(c["saving_D_vs_A_per_t"]), E_cap=f(oo["Ecap"][3]), E_exp=f(oo["Eexp"][3]))
LRN = F.LEARN_SHARE * 10 ** np.log2(0.9) + 1 - F.LEARN_SHARE
sc = [case("Kasus dasar (60 t/jam + PM-12, solar 2,0 L/t)"), case("Kasus target (solar tergantikan 3,0 L/t)", diesel_L_tffb=3.0), case("Tanpa tangki ekualisasi", buffer=0),
      case("Solar tergantikan 1,0 L/t", diesel_L_tffb=1.0), case("Tarif excess power 7,44 USc", tariff1=7.44, tariff2=4.46), case("Faktor lokasi F 1,10", F_loc=1.10),
      case("Karbon USD 8,3/t", p_carbon=8.3), case("Tanpa jasa POME", fee_ffb=0.0), case("PKS terisolasi (tanpa ekspor)", export_on=0), case("CAPEX -15% (hasil kuotasi)", ),
      case("Biaya modal ekuitas 12%", r_eq=0.12)]
oo = F.run(v, capex_mult=0.85); sc[9].update(NPV=f(oo["NPV"]), IRR=f(oo["IRR"]), DSCR=f(oo["DSCR_min"]), FCI=f(oo["fci"]))
oo = F.run(v, capex_mult=LRN); sc.append(dict(tag="Unit ke-10 (kurva belajar)", NPV=f(oo["NPV"]), IRR=f(oo["IRR"]), IRR_eq=f(oo["IRR_eq"]), DSCR=f(oo["DSCR_min"]), FCI=f(oo["fci"]), PBP=f(oo["PBP"]), save=0, save_t=0, E_cap=0, E_exp=0))
for t_ in ("30", "45"):
    oo = F.tier(t_); sc.append(dict(tag="Modul %s t/jam" % t_, NPV=f(oo["NPV"]), IRR=f(oo["IRR"]), IRR_eq=f(oo["IRR_eq"]) if oo["IRR_eq"] == oo["IRR_eq"] else None, DSCR=f(oo["DSCR_min"]), FCI=f(oo["fci"]), PBP=f(oo["PBP"]) if oo["PBP"] == oo["PBP"] else None, save=0, save_t=0, E_cap=0, E_exp=0))
D["keu"]["scen"] = sc
# peta kelayakan: NPV skala x fee (solar 2,0) dan solar x fee (60 t/jam)
fees = [0.75, 1.0, 1.25, 1.5, 1.75]
D["keu"]["map_tier"] = dict(fees=fees, tiers=["30", "45", "60"], npv=[[f(F.tier(t, dict(v, fee_ffb=x))["NPV"] / 1e6) for x in fees] for t in ("30", "45", "60")],
                            dscr=[[f(F.tier(t, dict(v, fee_ffb=x))["DSCR_min"]) for x in fees] for t in ("30", "45", "60")])
dsl = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
D["keu"]["map_diesel"] = dict(diesel=dsl, fees=fees, npv=[[f(F.run(dict(v, diesel_L_tffb=d, fee_ffb=x))["NPV"] / 1e6) for x in fees] for d in dsl],
                              save=[[f(MI.compare(dict(v, diesel_L_tffb=d, fee_ffb=x))["saving_D_vs_A_pct"]) for x in fees] for d in dsl])
D["keu"]["fee_curve"] = dict(fee=[round(x, 2) for x in np.arange(0.5, 2.01, 0.1)], npv=[f(F.run(dict(v, fee_ffb=float(x)))["NPV"] / 1e6) for x in np.arange(0.5, 2.01, 0.1)],
                             save=[f(MI.compare(dict(v, fee_ffb=float(x)))["saving_D_vs_A_pct"]) for x in np.arange(0.5, 2.01, 0.1)])
# armada
fl = F.fleet(v); D["keu"]["fleet"] = dict(years=fl["years"], sets_op=[f(x) for x in fl["sets_op"]], sets_new=[f(x) for x in fl["sets_new"]], fcff_co=[f(x) for x in fl["fcff_co"]], NPV=f(fl["NPV"]),
        IRR=f(fl["IRR"]) if fl["IRR"] == fl["IRR"] else None, peak=f(fl["peak"]), units=[[int(a), int(b_), f(c), f(d), f(e), f(g)] for a, b_, c, d, e, g in fl["units"]], overhead=[f(x) for x in fl["overhead"]],
        E=[f(x) for x in fl["E"]], co2=[f(x) for x in fl["co2"]])
pv_oh = float(sum(fl["overhead"][i] / (1 + fl["wacc"]) ** i for i in range(len(fl["years"])))); avg_u = float(np.mean([u[3] for u in fl["units"][1:]]))
D["keu"]["fleet"]["pv_overhead"] = pv_oh; D["keu"]["fleet"]["avg_unit_npv"] = avg_u; D["keu"]["fleet"]["sets_breakeven"] = pv_oh / avg_u if avg_u > 0 else None
# ------------------------------------------------------------------ PKS: keputusan
c = MI.compare(v); fw = MI.fee_window(v); seg = MI.segments(v); wf = MI.waterfall(v); a_ = c["detail"]
D["pks"] = dict(per_t={k: f(c[k]["per_t"]) for k in "ABCD"}, annual={k: f(c[k]["annual"]) for k in "ABCD"}, capex={k: f(c[k]["capex"]) for k in "ABCD"}, save_pct=f(c["saving_D_vs_A_pct"]), save_t=f(c["saving_D_vs_A_per_t"]),
                fw={k: f(x) for k, x in fw.items()}, seg=[{k: (f(x) if isinstance(x, (float, np.floating)) else x) for k, x in s.items()} for s in seg], wf=[(a, f(b)) for a, b in wf],
                A_items={k: f(x) for k, x in a_["A"].items()}, D_items={k: f(x) for k, x in a_["D"].items()}, c_dsl=f(a_["c_dsl"]), E_dsl=f(a_["E_dsl"]), cap=f(a_["cap"]), match=f(a_["match"]),
                diesel_L=f(a_["ffb"] * v["diesel_L_tffb"]), diesel_cost=f(a_["E_dsl"] * a_["c_dsl"]))
vb = dict(v); vb["buffer"] = 0; D["pks"]["match_nobuf"] = f(F.match_f(vb))
# ------------------------------------------------------------------ pasar, pesaing, PESTLE
mk = MK.market(o); D["pasar"] = dict(rows=[dict(level=r["level"], rule=r["rule"], mills=f(r["mills"]), sets=f(r["sets"]), rev=f(r["rev"]), MW=f(r["MW"])) for r in mk["rows"]],
        rev_avg=f(mk["rev_avg"]), share=f(mk["share"]), build_share=f(mk["build_share"]), my_sets=f(mk["my_sets"]), params=dict(mills=MK.MILLS_ID, captured=MK.SH_CAPTURED, size=MK.SH_SIZE, region=MK.SH_REGION, diesel=MK.SH_DIESEL, grid=MK.SH_GRID, free=MK.SH_FREE),
        prov=MK.PROV)
comp = MK.compet_matrix(c); D["pesaing"] = dict(crit=MK.CRIT, rows=[dict(name=r["name"], capex=r["capex"], land=r["land"], build=r["build"], pays=r["mill_pays"], ref=r["ref"], scores=[f(x) for x in r["scores"]], total=f(r["total"]), src=r["src"]) for r in comp])
Sm = np.array([r["scores"] for r in comp]); w0 = np.array([x[1] for x in MK.CRIT]); rng = np.random.default_rng(7); wins = np.zeros(len(comp)); rankD = []
for _ in range(20000):
    ww = rng.dirichlet(w0 * 30); tot = Sm @ ww; wins[np.argmax(tot)] += 1; rankD.append(int((tot > tot[-1]).sum()) + 1)
D["pesaing"]["wins"] = [f(x / 200) for x in wins]; D["pesaing"]["rankD_p"] = f(np.mean(np.array(rankD) == 1)); D["pesaing"]["rankD_top2"] = f(np.mean(np.array(rankD) <= 2))
oat = []
for j, (nm, w_) in enumerate(MK.CRIT):
    row = []
    for fac in (0.5, 1.5):
        ww = w0.copy(); ww[j] *= fac; ww /= ww.sum(); tot = Sm @ ww; row.append(int(np.argmax(tot) == len(comp) - 1))
    oat.append(row)
D["pesaing"]["oat"] = oat
D["pestle"] = [dict(k=k, cat=cc, fac=fa, sign=sg, imp=im, opp=op, note=nt) for k, cc, fa, sg, im, op, nt in MK.PESTLE]
D["porter"] = {k: [dict(f=a, s=f(b), n=cn) for a, b, cn in x] for k, x in MK.PORTER.items()}
D["reloc"] = {k: f(x) for k, x in MK.relocation_value().items()}
# ------------------------------------------------------------------ emisi (LCA awal, per tahun pada skala dasar, tCO2e)
k_ = F.TECH["ffb_ty_nom"] / F.TECH45["ffb_ty_nom"]; E_ = R["EMIS"]; GW = E_["GWP_CH4"]
ch4_prod_kgd = R["tiers"]["45"]["ch4_Nm3d"] * 0.7157; days = T["days_yr"] * (v["util"])
pm = json.load(open(os.path.join(ROOT, "process/outputs/portable_modules.json"))); steel_t = pm["mass_t_total"] * k_
eff_pond = T["eff_t_nom"] * v["util"] * T["B0"] * v["MCF_eff"] * GW
leak = E_["leak"] * ch4_prod_kgd * k_ * days * GW / 1000; slip = E_["slip"] * ch4_prod_kgd * k_ * days * GW / 1000
proj_nom = T["proj_t"] * v["util"] / T["util_proc"]; dissolved = max(proj_nom - leak - slip - T["eff_t_nom"] * T["util_proc"] * T["B0"] * T["MCF_proc"] * GW * v["util"] / T["util_proc"], 0.0)
embod = steel_t * 1000 * 1.9 / 1000 / v["n_op"]; transp = pm["ship_units_total"] * k_ * 2 * 2000 * 0.1 * 1.0 / 1000 / v["n_op"] * 0.0 + 21 * k_ * 0.9 * 2.0 / v["n_op"] * 0.0
chem = (T["polymer_kg_tffb"] * 2.5 + T["ac_kg_tffb"] * 6.0) * T["ffb_ty_nom"] * v["util"] / 1000 / 1000 + T["naoh_kgd"] * T["days_yr"] * 1.1 / 1000 / 1000
base_t = T["base_t"] * v["util"] / T["util_proc"]; grid_exp = float(o["Eexp"][3]) * 1e6 * E_["ef_grid"] / 1000; dsl_t = float(o["Ecap"][3]) * 1e6 * 0.30 * 2.68 / 1000
D["lca"] = dict(base=f(base_t), leak=f(leak), slip=f(slip), dissolved=f(dissolved), eff_pond=f(eff_pond), embodied=f(embod), chem=f(chem), net_credit=f(o["ER"]), credited=f(o["ER"] * v["cer_ratio"]),
                grid_cobenefit=f(grid_exp), diesel_cobenefit=f(dsl_t), steel_t=f(steel_t), assumptions="faktor baja 1,9 kgCO2e/kg (ICE v3, asumsi), solar 2,68 kgCO2/L, jaringan 0,80 kg/kWh (EMIS), polimer 2,5 dan karbon aktif 6,0 kgCO2e/kg (asumsi)")
D["lca"]["net_total"] = f(base_t - (leak + slip + dissolved + eff_pond + embod + chem))
# ------------------------------------------------------------------ lain-lain
D["meta"] = dict(base_tier=F.BASE_TIER, util=v["util"], wacc=f(o["wacc"]), inflasi=v["infl"], fx=v["fx"], year0=v["year0"], n_op=n, tax=v["tax"], diesel_L=v["diesel_L_tffb"], p_captive=v["p_captive"],
                 tariff1=v["tariff1"], tariff2=v["tariff2"], p_carbon=v["p_carbon"], fee=v["fee_ffb"], cont=v["cont"], debt=v["debt_frac"], r_debt=v["r_debt"], r_eq=v["r_eq"], tenor=v["tenor"], dep=v["dep_life"],
                 p_diesel=MI.M["p_diesel"][0], avail=v["avail"], c_gfs=v["c_gfs"], c_chp=v["c_chp"], match=f(F.match_f(v)), roll=F.ROLL)
json.dump(D, open(os.path.join(ROOT, "deck", "deck_data.json"), "w"), indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else (x.tolist() if isinstance(x, np.ndarray) else str(x)))
print("ok", os.path.getsize(os.path.join(ROOT, "deck", "deck_data.json")))
