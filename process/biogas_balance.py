# -*- coding: utf-8 -*-
"""
===============================================================================
 MODULAR POME + EFB CO-DIGESTION BIOGAS GENERATOR
 Mass & energy balance, kinetic digestion model, feedstock uncertainty
 (EIC 2026 - technical package, Phase 1)
===============================================================================
 Run in Spyder (F5).  Ends with plt.show().  Results are written to
 ./outputs/results.json  (single source of truth for PFD / 3D / drawings).

 MODEL STRUCTURE
   1. Species & stoichiometry : every reaction is built from chemical formulas;
                                CO2 / H2O / NH3 / sulfate terms come from element
                                balances (no hard-coded yield tables for them).
   2. Feedstock model         : mill throughput, POME (8 COD fractions), EFB
                                (7 dry-basis fractions), shredding, uncertainty.
   3. Biology                 : reduced ADM1 (30 states): hydrolysis, acidogenesis,
                                acetogenesis, aceto/hydrogenotrophic methanogenesis,
                                sulfate reduction, pH / NH3 / H2S / LCFA / H2
                                inhibition, charge-balance pH, gas-liquid transfer.
                                Reactor conversion = integration of the ODEs.
   4. Design                  : EFB-share sweep, HRT sweep, standard module sizing.
   5. Plant energy & mass     : gas train, CHP part-load, parasitic loads, heat,
                                dewatering, full stream table, closure checks.
   6. Uncertainty             : Latin-hypercube Monte Carlo + Spearman sensitivity,
                                one-year seasonal dynamic simulation.

 PARAMETER PROVENANCE (tag in PAR table):
   [LIT-S]  value found in literature search during this project (see header refs)
   [ADM1]   Batstone et al. (2002) IWA ADM1 default (textbook values)
   [ASSUME] engineering assumption - replace with site data / vendor data
   [CALIB]  fitted at run-time to literature targets (calibrate())

 SEARCHED LITERATURE ANCHORS (to be cited in APA in the proposal)
   - Raw POME: COD 15-100 g/L (typical 51), TSS 5-54 g/L (typical 18),
     oil 0.6-0.7 % (encyclopedia.pub/entry/10093, PMC8225864 Table 1)
   - BMP: POME 0.397 and EFB 0.264 L CH4/g VS (mesophilic; science.gov
     palm-EFB topic page);  EFB:POME synergy at 0.25-0.31 : 1
   - POME CSTR: CH4 yield 0.34 L/g COD removed, HRT 8-24 d (UMP IJETS 1105)
   - Mill power demand 18.7-25 kWh/t FFB (Mahidol; FEDEPALMA)
   - Biogas engine electrical efficiency 34-38.5 % (Thai mill assessment)
   - ADM1 + sulfate reduction: Fedorovich, Lens & Kalyuzhnyi (2003)
===============================================================================
"""
import os, re, json, math, time, warnings
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
from scipy.stats import norm, truncnorm, rankdata
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
t_script0 = time.time()

# ------------------------------------------------------------------ run control
QUICK   = os.environ.get("BIOGAS_QUICK", "0") == "1"      # fast smoke test
NO_MAIN = os.environ.get("BIOGAS_NO_MAIN", "0") == "1"    # import definitions only
N_MC    = 48 if QUICK else 400          # Monte Carlo samples
SEED    = 20261015
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:                        # Spyder "run selection"
    BASE_DIR = os.getcwd()
OUTDIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTDIR, exist_ok=True)
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ constants
R_J   = 8.314462618           # J/mol/K
P_ATM = 101325.0              # Pa
T0K   = 273.15
VN    = R_J * T0K / P_ATM * 1000.0      # m3/kmol at 0 degC, 1 atm  (22.414)
G     = 9.80665
RHO_W = 995.0                 # kg/m3 water at ~35 degC (used for slurry volumes)
CP_W  = 4.18                  # kJ/kg/K
H_VAP = 2400.0                # kJ/kg latent heat of water near 35-40 degC
AT_MASS = dict(C=12.011, H=1.008, O=15.999, N=14.007, S=32.06)
# lower heating values, kJ/mol (NIST/CRC thermochemistry)
LHV_KJMOL = dict(CH4=802.3, H2=241.8, H2S=518.0)
LHV_CH4_MJNM3 = LHV_KJMOL["CH4"] / (VN / 1000.0) / 1000.0   # MJ/Nm3  (35.8)

# ============================================================================
# 1. SPECIES AND STOICHIOMETRY (all derived from chemical formulas)
# ============================================================================
FORMULA = dict(
    su="C6H12O6", ch="C6H10O5", hem="C5H8O4", pr="C5H7NO2", aa="C5H9NO3",
    li="C18H34O2", fa="C18H34O2", pro="C3H6O2", ac="C2H4O2", h2="H2", ch4="CH4",
    bio="C5H7NO2", lig="C10H12O3", inert="C6H10O5", sI="C6H10O5",
    co2="CO2", h2o="H2O", nh3="NH3", h2s="H2S", so4="H2SO4",
)
ELS = ["C", "H", "O", "N", "S"]

def parse_formula(f):
    d = dict.fromkeys(ELS, 0.0)
    for el, n in re.findall(r"([CHONS])(\d*\.?\d*)", f):
        d[el] += float(n) if n else 1.0
    return np.array([d[e] for e in ELS])

class Sp:
    """Chemical species: element vector, molar mass, COD per kmol (ThOD, N->NH3, S->H2SO4)."""
    def __init__(s, f):
        s.f = f
        s.e = parse_formula(f)
        s.MW = float(sum(s.e[i] * AT_MASS[ELS[i]] for i in range(5)))
        C, H, O, N, S = s.e
        s.cod = 32.0 * (C + H / 4.0 - O / 2.0 - 3.0 * N / 4.0 + 1.5 * S)   # kg COD / kmol
        s.mass_per_cod = s.MW / s.cod if s.cod > 0 else float("nan")        # kg / kg COD

SPX = {k: Sp(v) for k, v in FORMULA.items()}

def build_rxn(sub, prods):
    """
    1 kg COD of substrate `sub` -> products {species: kg COD fraction}.
    Solves for CO2, H2O, NH3 (+ sulfate consumption) by element balance (C,H,O,N,S).
    Returns dict of kmol per kg COD of substrate (positive = produced).
    """
    n_sub = 1.0 / SPX[sub].cod
    E = SPX[sub].e * n_sub
    for p, fr in prods.items():
        E = E - SPX[p].e * (fr / SPX[p].cod)
    # sulfur: products' S (as H2S) must come from sulfate
    nS_need = -E[4]                    # kmol H2SO4 consumed
    extra = {}
    if abs(nS_need) > 1e-15:
        extra["so4"] = nS_need
        E = E + SPX["so4"].e * nS_need     # sulfate supplies the S (and its H,O)
        # E now = what CO2,H2O,NH3 must supply (C,H,O,N)
    A = np.array([SPX["co2"].e[:4], SPX["h2o"].e[:4], SPX["nh3"].e[:4]]).T   # 4x3
    sol, *_ = np.linalg.lstsq(A, E[:4], rcond=None)
    res = float(np.max(np.abs(A @ sol - E[:4])))
    return dict(co2=sol[0], h2o=sol[1], nh3=sol[2], so4=-extra.get("so4", 0.0), resid=res)

# yields and product splits (ADM1, Batstone 2002, lumped: pro = C3-C5 VFA)  [ADM1]
Y_ = dict(su=0.10, aa=0.08, fa=0.06, pro=0.05, ac=0.05, h2=0.06, sa=0.04, sh=0.05)
F_SU  = dict(ac=0.41, h2=0.19, pro=0.40)
F_AA  = dict(ac=0.40, h2=0.06, pro=0.54)
F_FA  = dict(ac=0.70, h2=0.30)
F_PRO = dict(ac=0.57, h2=0.43)
F_DEC = dict(ch=0.20, pr=0.20, li=0.25, inert=0.25, sI=0.10)      # BSM2 composite split

def _uptake(Y, split):
    d = {"bio": Y}
    for k, v in split.items():
        d[k] = (1.0 - Y) * v
    return d

PROC = {
    "hyd_ch":  ("ch",  {"su": 1.0}),
    "hyd_cel": ("ch",  {"su": 1.0}),
    "hyd_hem": ("hem", {"su": 1.0}),
    "hyd_pr":  ("pr",  {"aa": 1.0}),
    "hyd_li":  ("li",  {"fa": 1.0}),
    "up_su":   ("su",  _uptake(Y_["su"], F_SU)),
    "up_aa":   ("aa",  _uptake(Y_["aa"], F_AA)),
    "up_fa":   ("fa",  _uptake(Y_["fa"], F_FA)),
    "up_pro":  ("pro", _uptake(Y_["pro"], F_PRO)),
    "up_ac":   ("ac",  {"bio": Y_["ac"], "ch4": 1 - Y_["ac"]}),
    "up_h2":   ("h2",  {"bio": Y_["h2"], "ch4": 1 - Y_["h2"]}),
    "srb_ac":  ("ac",  {"bio": Y_["sa"], "h2s": 1 - Y_["sa"]}),
    "srb_h2":  ("h2",  {"bio": Y_["sh"], "h2s": 1 - Y_["sh"]}),
    "dec":     ("bio", F_DEC),
}
STO = {k: build_rxn(s, p) for k, (s, p) in PROC.items()}
STO_MAXRES = max(v["resid"] for v in STO.values())     # element-balance residual (should be ~1e-16)

# ============================================================================
# 2. PHYSICAL CHEMISTRY
# ============================================================================
def eq_consts(Tc):
    T = Tc + T0K
    pKw = 4470.99 / T + 0.01706 * T - 6.0875                       # Harned & Robinson form
    pK1 = 17052.0 / T + 215.21 * math.log10(T) - 0.12675 * T - 545.56   # Plummer & Busenberg (CO2)
    pKN = 0.09018 + 2729.92 / T                                    # Emerson et al. 1975 (NH4+)
    pKS = 7.05 - 0.0116 * (Tc - 25.0)                              # H2S pKa1  [ASSUME T-slope]
    return dict(Kw=10 ** -pKw, K1=10 ** -pK1, KN=10 ** -pKN, Kac=10 ** -4.76,
                Kpro=10 ** -4.88, KS=10 ** -pKS)

HENRY298 = dict(co2=(0.034, 2400.0), ch4=(0.0014, 1600.0), h2=(0.00078, 500.0), h2s=(0.10, 2100.0))  # Sander 2015
def henry(sp, Tc):
    k0, C = HENRY298[sp]
    return k0 * math.exp(C * (1.0 / (Tc + T0K) - 1.0 / 298.15)) / 1.01325   # kmol/m3/bar

def p_sat(Tc):                                                     # Pa, Magnus (Alduchov-Eskridge)
    return 610.94 * math.exp(17.625 * Tc / (Tc + 243.04))

# ============================================================================
# 3. PARAMETER TABLE  (median, distribution, provenance)
# ============================================================================
# dist: 'fix' | ('ln', cv) | ('un', lo, hi) | ('tn', sd, lo, hi)
PAR = {
 # ---- plant / feedstock
 "ffb_tph":    (45.0,  "fix", "[ASSUME] representative independent mill, t FFB/h nameplate"),
 "hrs_day":    (20.0,  "fix", "[ASSUME] processing hours per day"),
 "days_yr":    (300.0, "fix", "[ASSUME] operating days per year"),
 "util":       (0.92,  ("tn", 0.07, 0.70, 1.05), "[ASSUME] mill load factor vs nameplate"),
 "pome_yield": (0.65,  ("ln", 0.10), "[LIT] 0.6-0.7 m3 POME/t FFB (range 0.5-0.8)"),
 "cod_pome":   (51.0,  ("ln", 0.15), "[LIT-S] typical raw POME COD 51 kg/m3 (15-100)"),
 "ash_pome":   (3.5,   ("ln", 0.25), "[ASSUME] mineral solids in POME, kg/m3"),
 "tan_pome":   (0.0025, ("ln", 0.30), "[ASSUME] NH4-N in POME feed, kmol/m3 (35 mg N/L)"),
 "so4_pome":   (0.0031, ("ln", 0.40), "[ASSUME] sulfate, kmol/m3 (300 mg SO4/L; earlier deck value)"),
 "cat_pome":   (0.030, ("ln", 0.25), "[ASSUME] net strong cations in POME (K+ etc. minus Cl-), kmol eq/m3"),
 "T_pome_in":  (85.0,  ("tn", 3.0, 75.0, 95.0), "[LIT] POME leaves sterilizer/clarifier at 80-90 degC"),
 "T_amb":      (27.0,  "fix", "[ASSUME] ambient (Sumatra)"),
 "efb_ratio":  (0.22,  ("ln", 0.08), "[LIT] 21-23 % of FFB mass"),
 "efb_mc":     (0.65,  ("tn", 0.025, 0.58, 0.70), "[LIT] EFB moisture 60-67 % wb"),
 "d_p_mm":     (10.0,  ("ln", 0.20), "shredded EFB mean particle size, mm (hammer-mill product)"),
 "K_ash":      (0.0095, "fix", "[ASSUME] kmol K+/kg EFB ash"),
 "ash_sol":    (0.7,   "fix", "[ASSUME] soluble fraction of EFB-ash cations"),
 "beta_lig":   (0.45,  ("tn", 0.12, 0.2, 1.0), "[CALIB] lignin shielding of cellulose"),
 "efb_share":  (0.30,  "fix", "[DESIGN] fraction of EFB to AD (re-optimised in Section 8)"),
 "TS_max":     (0.08,  "fix", "[ASSUME] max blend TS (wet basis) for pumpable, mixable CSTR"),
 "e_scr":      (0.05,  "fix", "[ASSUME] particulate removal across fine screen"),
 # ---- hydrolysis (first order, 1/d at 35 degC)
 "k_ch":       (1.0,   ("ln", 0.40), "[CALIB/ASSUME] POME carbohydrate particulates"),
 "k_pr":       (0.6,   ("ln", 0.40), "[ASSUME] POME protein particulates"),
 "k_li":       (0.8,   ("ln", 0.40), "[CALIB/ASSUME] POME oil/lipid (emulsified)"),
 "k_cel_ref":  (0.12,  ("ln", 0.35), "[CALIB] EFB cellulose at d_ref=10 mm"),
 "k_hem_ref":  (0.30,  ("ln", 0.35), "[CALIB] EFB hemicellulose at d_ref=10 mm"),
 "d_ref_mm":   (10.0,  "fix", "reference particle size"),
 "gam_size":   (0.5,   "fix", "[ASSUME] size exponent of surface-limited hydrolysis"),
 # ---- uptake (ADM1 Batstone 2002)
 "km_su":  (30.0, ("ln", 0.20), "[ADM1]"), "Ks_su":  (0.5,  "fix", "[ADM1]"),
 "km_aa":  (50.0, ("ln", 0.20), "[ADM1]"), "Ks_aa":  (0.3,  "fix", "[ADM1]"),
 "km_fa":  (6.0,  ("ln", 0.30), "[ADM1]"), "Ks_fa":  (0.4,  "fix", "[ADM1]"),
 "km_pro": (16.0, ("ln", 0.25), "[ADM1] lumped C3-C5 VFA (avg of c4/pro)"), "Ks_pro": (0.15, "fix", "[ADM1]"),
 "km_ac":  (8.0,  ("ln", 0.25), "[ADM1]"), "Ks_ac":  (0.15, "fix", "[ADM1]"),
 "km_h2":  (35.0, ("ln", 0.25), "[ADM1]"), "Ks_h2":  (7e-6, "fix", "[ADM1]"),
 "km_sa":  (14.0, ("ln", 0.30), "[ASSUME] acetate-SRB (Fedorovich-type magnitude)"), "Ks_sa": (0.10, "fix", "[ASSUME]"),
 "km_sh":  (40.0, ("ln", 0.30), "[ASSUME] H2-SRB"), "Ks_sh": (5e-6, "fix", "[ASSUME]"),
 "Ks_so4": (1e-4, "fix", "[ASSUME] kmol/m3"),
 "k_dec":  (0.02, "fix", "[ADM1] 1/d"),
 "Ks_IN":  (1e-4, "fix", "[ADM1] kmol/m3"),
 # ---- inhibition
 "KI_nh3":    (0.0036, ("ln", 0.35), "[ADM1x2] free NH3 on acetoclasts, kmol/m3 (acclimated; ADM1 0.0018)"),
 "KI_h2s_ac": (0.008,  ("ln", 0.40), "[ASSUME] free H2S on acetoclasts, kmol/m3"),
 "KI_h2s_h2": (0.012,  ("ln", 0.40), "[ASSUME] free H2S on hydrogenotrophs"),
 "KI_h2s_sr": (0.025,  "fix",        "[ASSUME] free H2S on SRB"),
 "KI_fa_ac":  (2.0,    ("ln", 0.30), "[ASSUME] LCFA on acetoclasts, kg COD/m3"),
 "KI_fa_h2":  (3.0,    ("ln", 0.30), "[ASSUME] LCFA on hydrogenotrophs"),
 "KI_h2_fa":  (5e-6, "fix", "[ADM1]"), "KI_h2_pro": (5e-6, "fix", "[ADM1]"),
 "th_up":     (0.069, "fix", "[ASSUME] Q10~2 temperature coefficient, uptake"),
 "th_hyd":    (0.040, "fix", "[ASSUME] temperature coefficient, hydrolysis"),
 # ---- reactor / gas transfer
 "T_dig":    (38.0, "fix", "[DESIGN] mesophilic set-point, degC"),
 "kLa":      (200.0, ("ln", 0.30), "[ADM1] 1/d"),
 "dP_roof":  (0.005, "fix", "bar, membrane roof overpressure"),
 "pH_sp":    (7.0,  "fix", "[DESIGN] alkali dosing set-point"),
 "IN_sp":    (0.0071, "fix", "[DESIGN] N-dosing set-point, kmol N/m3 (100 mg N/L): keeps TAN above nutrient limitation"),
 "K_dosN":   (1.0,  "fix", "1/d, N-dosing controller gain"),
 "dosN_max": (0.012, "fix", "kmol N/m3/d, N-dosing capacity"),
 "K_dose":   (0.04, "fix", "kmol/m3/d per pH unit"),
 "dose_max": (0.03, "fix", "kmol/m3/d"),
}
def pmed(name): return PAR[name][0]

# --- logistic-normal COD / dry-mass composition groups
POME_KEYS = ["su", "aa", "vfa", "sI", "ch", "pr", "li", "inert"]
POME_MEAN = np.array([0.12, 0.04, 0.05, 0.04, 0.31, 0.08, 0.30, 0.06])    # [ASSUME] sums to 1
POME_SIG  = 0.22
EFB_KEYS  = ["cel", "hem", "lig", "ash", "oil", "prot", "ext"]
EFB_MEAN  = np.array([0.38, 0.24, 0.21, 0.06, 0.03, 0.04, 0.04])           # [ASSUME]/[LIT range] sums to 1
EFB_SIG   = 0.12
assert abs(POME_MEAN.sum() - 1) < 1e-12 and abs(EFB_MEAN.sum() - 1) < 1e-12

NAMES = ["su", "aa", "fa", "pro", "ac", "h2", "ch4", "sI",
         "ch", "pr", "li", "cel", "hem", "lig", "rc", "inert",
         "Xsu", "Xaa", "Xfa", "Xpro", "Xac", "Xh2", "Xsa", "Xsh",
         "IC", "IN", "SO4", "IS", "cat", "ash"]
IX = {k: i for i, k in enumerate(NAMES)}
NS = len(NAMES)
ATOL = np.full(NS, 1e-8); ATOL[IX["h2"]] = 1e-11; ATOL[IX["IS"]] = 1e-9
ATOL[[IX[k] for k in ("IC", "IN", "SO4", "cat")]] = 1e-9

# species -> state mass-per-COD helper
def m_per_cod(sp): return SPX[sp].mass_per_cod        # kg per kg COD
# state -> chemical species used for element/mass accounting of COD-type states
STATE_SP = dict(su="su", aa="aa", fa="fa", pro="pro", ac="ac", h2="h2", ch4="ch4", sI="sI",
                ch="ch", pr="pr", li="li", cel="ch", hem="hem", lig="lig", rc="ch", inert="inert",
                Xsu="bio", Xaa="bio", Xfa="bio", Xpro="bio", Xac="bio", Xh2="bio", Xsa="bio", Xsh="bio")

# ============================================================================
# 4. FEEDSTOCK MODEL
# ============================================================================
def cod_of(mass, sp):  return mass / SPX[sp].mass_per_cod       # kg COD from kg species
def mass_of(cod, sp):  return cod * SPX[sp].mass_per_cod        # kg species from kg COD

def nominal_theta():
    th = {k: v[0] for k, v in PAR.items()}
    th["fr_pome"] = POME_MEAN.copy()
    th["fr_efb"] = EFB_MEAN.copy()
    return th

def efb_frec(th):
    """fraction of EFB cellulose shielded by lignin (inert pool 'rc')."""
    w = th["fr_efb"]
    return float(np.clip(th["beta_lig"] * w[2] / w[0], 0.0, 0.8))

def build_feed(th, share=None, cap_ts=True, efb_on=True):
    """Daily blend entering the digester bank. Returns dict (concentrations per m3 of blend)."""
    ffb = th["ffb_tph"] * th["hrs_day"] * th["util"]                 # t FFB/d
    if ffb <= 1e-9:                                                  # mill shut down: no feed
        z = np.zeros(NS)
        return dict(c=z, Q=0.0, Qp=0.0, V_efb=0.0, M_efb=0.0, DM_efb=0.0, wat_efb=0.0, share=0.0, share_req=0.0, TS=0.0,
                    T_p_out=th["T_dig"], Qcool_kW=0.0, ffb_td=0.0, cP=z, tE=z, scr_mass=0.0, frc=efb_frec(th), raw={}, scr_cod={})
    Qp = ffb * th["pome_yield"]                                      # m3 POME/d
    fp, COD = th["fr_pome"], th["cod_pome"]
    raw = dict(su=fp[0] * COD, aa=fp[1] * COD, ac=fp[2] * COD, sI=fp[3] * COD,
               ch=fp[4] * COD, pr=fp[5] * COD, li=fp[6] * COD, inert=fp[7] * COD)
    es = th["e_scr"]
    scr_cod = {k: raw[k] * es for k in ("ch", "pr", "inert")}         # removed by screens
    cP = np.zeros(NS)
    for k in ("su", "aa", "ac", "sI", "li"):
        cP[IX[k]] = raw[k]
    for k in ("ch", "pr", "inert"):
        cP[IX[k]] = raw[k] - scr_cod[k]
    cP[IX["IN"]] = th["tan_pome"]; cP[IX["SO4"]] = th["so4_pome"]
    cP[IX["cat"]] = th["cat_pome"]; cP[IX["ash"]] = th["ash_pome"] * (1 - es)
    scr_mass = sum(mass_of(Qp * scr_cod[k], STATE_SP[k]) for k in scr_cod) + Qp * th["ash_pome"] * es
    # --- EFB (dry-basis composition -> COD states)
    M_all = ffb * th["efb_ratio"]                                    # t wet EFB/d (all)
    w = th["fr_efb"]; frc = efb_frec(th)

    def efb_totals(sh):
        M = M_all * sh; DM = M * 1000.0 * (1 - th["efb_mc"]); wat = M * 1000.0 * th["efb_mc"]
        t = np.zeros(NS)                                             # kg COD/d (or kmol/d, kg/d)
        t[IX["cel"]] = cod_of(DM * w[0] * (1 - frc), "ch")
        t[IX["rc"]] = cod_of(DM * w[0] * frc, "ch")
        t[IX["hem"]] = cod_of(DM * w[1], "hem")
        t[IX["lig"]] = cod_of(DM * w[2], "lig")
        t[IX["ash"]] = DM * w[3]
        t[IX["li"]] = cod_of(DM * w[4], "li")
        t[IX["pr"]] = cod_of(DM * w[5], "pr")
        t[IX["su"]] = cod_of(DM * w[6], "su")
        t[IX["cat"]] = DM * w[3] * th["K_ash"] * th["ash_sol"]
        return t, M, DM, wat

    def ts_frac(sh):
        t, M, DM, wat = efb_totals(sh)
        sol = Qp * sum(mass_of(cP[IX[k]], STATE_SP[k]) for k in ("su", "aa", "ac", "sI", "ch", "pr", "li", "inert"))
        sol += Qp * cP[IX["ash"]]
        sol += sum(mass_of(t[IX[k]], STATE_SP[k]) for k in ("su", "ch", "hem", "lig", "li", "pr", "cel", "rc") if k in STATE_SP) + t[IX["ash"]]
        tot = Qp * RHO_W + M * 1000.0
        return sol / tot
    sh_req = (th["efb_share"] if share is None else share) if efb_on else 0.0
    sh = sh_req
    if efb_on and cap_ts and ts_frac(sh_req) > th["TS_max"]:
        if ts_frac(0.0) < th["TS_max"]:
            sh = brentq(lambda x: ts_frac(x) - th["TS_max"], 0.0, sh_req)
        else:
            sh = 0.0
    tE, M, DM, wat = efb_totals(sh)
    V_efb = wat / RHO_W + DM / 1400.0
    Q = Qp + V_efb
    tot = Qp * cP + tE
    tot[IX["IN"]] += 0.0
    c = tot / Q
    # --- heat: POME must be cooled so that the blend sits at the digester temperature
    m_p = Qp * RHO_W
    cp_efb = (1 - th["efb_mc"]) * 1.5 + th["efb_mc"] * CP_W
    T_dig, T_amb = th["T_dig"], th["T_amb"]
    T_p_out = T_dig + (M * 1000.0 * cp_efb * (T_dig - T_amb)) / (m_p * CP_W) if m_p > 0 else T_dig
    Qcool = m_p * CP_W * (th["T_pome_in"] - T_p_out) / 86400.0        # kW_th
    return dict(c=c, Q=Q, Qp=Qp, V_efb=V_efb, M_efb=M, DM_efb=DM, wat_efb=wat, share=sh, share_req=sh_req,
                TS=ts_frac(sh), T_p_out=T_p_out, Qcool_kW=Qcool, ffb_td=ffb, cP=cP, tE=tE,
                scr_mass=scr_mass, frc=frc, raw=raw, scr_cod=scr_cod)

# ============================================================================
# 5. DIGESTER MODEL (reduced ADM1, quasi-steady gas phase)
# ============================================================================
def solve_h(cat, IN, IC, ac, pro, IS, SO4, c, h0):
    """charge balance -> [H+] (Newton in ln h; F(h) is monotonic increasing)."""
    a = ac / 64.0; p = pro / 112.0
    KN, K1, Ka, Kp, KS, Kw = c["KN"], c["K1"], c["Kac"], c["Kpro"], c["KS"], c["Kw"]
    x = math.log(h0)
    for _ in range(60):
        h = math.exp(x)
        F = (cat + IN * h / (h + KN) + h - IC * K1 / (h + K1) - a * Ka / (h + Ka)
             - p * Kp / (h + Kp) - IS * KS / (h + KS) - 2.0 * SO4 - Kw / h)
        dF = (IN * KN / (h + KN) ** 2 + 1.0 + IC * K1 / (h + K1) ** 2 + a * Ka / (h + Ka) ** 2
              + p * Kp / (h + Kp) ** 2 + IS * KS / (h + KS) ** 2 + Kw / h ** 2)
        dx = -F / (h * dF)
        dx = max(-1.5, min(1.5, dx))
        x += dx
        if abs(dx) < 1e-9:
            break
    return math.exp(x)

def ipH(pH, UL, LL):
    return 1.0 if pH >= UL else math.exp(-3.0 * ((pH - UL) / (UL - LL)) ** 2)

def gas_flux(a, b):
    """quasi-steady headspace: j_i = a_i*J/(J+b_i), J = sum j_i  (kmol/m3-liquid/d)."""
    J = sum(a)
    if J <= 1e-14:
        return [0.0] * len(a), 0.0
    for _ in range(40):
        g = sum(ai * J / (J + bi) for ai, bi in zip(a, b)) - J
        dg = sum(ai * bi / (J + bi) ** 2 for ai, bi in zip(a, b)) - 1.0
        Jn = J - g / dg
        if Jn <= 0:
            Jn = 0.5 * J
        if abs(Jn - J) < 1e-13 * max(1.0, J):
            J = Jn; break
        J = Jn
    return [ai * J / (J + bi) for ai, bi in zip(a, b)], J

class Digester:
    """One CSTR module (all modules in the bank are identical -> 'numbering up')."""
    def __init__(s, th, F, N_mod, V_mod, Q_override=None):
        s.th = th; s.V = V_mod; s.N = N_mod
        s.Qm = (F["Q"] if Q_override is None else Q_override) / N_mod
        s.D = s.Qm / V_mod
        s.feed = F["c"].tolist()
        T = th["T_dig"]; s.T = T
        s.c = eq_consts(T)
        s.H = [henry(k, T) for k in ("co2", "ch4", "h2", "h2s")]
        s.Pdry = (P_ATM / 1e5 + th["dP_roof"]) - p_sat(T) / 1e5
        s.fu = math.exp(th["th_up"] * (T - 35.0)); s.fh = math.exp(th["th_hyd"] * (T - 35.0))
        s.kcel = th["k_cel_ref"] * (th["d_ref_mm"] / th["d_p_mm"]) ** th["gam_size"]
        s.khem = th["k_hem_ref"] * (th["d_ref_mm"] / th["d_p_mm"]) ** th["gam_size"]
        s.h_prev = 1e-7
        s.aux = {}
        s.dosed = 0.0

    def rhs(s, t, y):
        th = s.th; c = s.c; D = s.D; f = s.feed
        (su, aa, fa, pro, ac, h2, ch4, sI, ch, pr, li, cel, hem, lig, rc, inert,
         Xsu, Xaa, Xfa, Xpro, Xac, Xh2, Xsa, Xsh, IC, IN, SO4, IS, cat, ash) = y.tolist()
        h = solve_h(cat, max(IN, 0.0), max(IC, 0.0), max(ac, 0.0), max(pro, 0.0), max(IS, 0.0), max(SO4, 0.0), c, s.h_prev)
        s.h_prev = h
        pH = -math.log10(h)
        INp = max(IN, 0.0)
        co2 = max(IC, 0.0) * h / (h + c["K1"]); nh3 = INp * c["KN"] / (h + c["KN"]); h2s = max(IS, 0.0) * h / (h + c["KS"])
        # ---- gas-liquid transfer
        kLa = th["kLa"]; Pd = s.Pdry; H = s.H
        a = (kLa * co2, kLa * max(ch4, 0.0) / 64.0, kLa * max(h2, 0.0) / 16.0, kLa * h2s)
        b = (kLa * H[0] * Pd, kLa * H[1] * Pd, kLa * H[2] * Pd, kLa * H[3] * Pd)
        (j_co2, j_ch4, j_h2, j_h2s), Jt = gas_flux(a, b)
        # ---- inhibition
        Ia = ipH(pH, 5.5, 4.0); Iac = ipH(pH, 7.0, 6.0); Ih = ipH(pH, 6.0, 5.0); Isr = ipH(pH, 6.5, 5.0)
        Iin = 1.0 / (1.0 + th["Ks_IN"] / max(INp, 1e-12))
        h2p = max(h2, 0.0); fap = max(fa, 0.0)
        Ih2_fa = 1.0 / (1.0 + h2p / th["KI_h2_fa"]); Ih2_pro = 1.0 / (1.0 + h2p / th["KI_h2_pro"])
        Inh3 = 1.0 / (1.0 + nh3 / th["KI_nh3"])
        Ih2s_ac = 1.0 / (1.0 + h2s / th["KI_h2s_ac"]); Ih2s_h2 = 1.0 / (1.0 + h2s / th["KI_h2s_h2"]); Ih2s_sr = 1.0 / (1.0 + h2s / th["KI_h2s_sr"])
        Ifa_ac = 1.0 / (1.0 + fap / th["KI_fa_ac"]); Ifa_h2 = 1.0 / (1.0 + fap / th["KI_fa_h2"])
        fu, fh = s.fu, s.fh
        sup, aap, prop, acp, so4p = max(su, 0.0), max(aa, 0.0), max(pro, 0.0), max(ac, 0.0), max(SO4, 0.0)
        # ---- hydrolysis
        r_ch = th["k_ch"] * fh * max(ch, 0.0); r_pr = th["k_pr"] * fh * max(pr, 0.0); r_li = th["k_li"] * fh * max(li, 0.0)
        r_cel = s.kcel * fh * max(cel, 0.0); r_hem = s.khem * fh * max(hem, 0.0)
        # ---- uptake
        r_su = th["km_su"] * fu * sup / (th["Ks_su"] + sup) * max(Xsu, 0.0) * Ia * Iin
        r_aa = th["km_aa"] * fu * aap / (th["Ks_aa"] + aap) * max(Xaa, 0.0) * Ia * Iin
        r_fa = th["km_fa"] * fu * fap / (th["Ks_fa"] + fap) * max(Xfa, 0.0) * Ia * Iin * Ih2_fa
        r_pro = th["km_pro"] * fu * prop / (th["Ks_pro"] + prop) * max(Xpro, 0.0) * Ia * Iin * Ih2_pro
        r_ac = th["km_ac"] * fu * acp / (th["Ks_ac"] + acp) * max(Xac, 0.0) * Iac * Iin * Inh3 * Ih2s_ac * Ifa_ac
        r_h2 = th["km_h2"] * fu * h2p / (th["Ks_h2"] + h2p) * max(Xh2, 0.0) * Ih * Iin * Ih2s_h2 * Ifa_h2
        sulf = so4p / (th["Ks_so4"] + so4p)
        r_sa = th["km_sa"] * fu * acp / (th["Ks_sa"] + acp) * sulf * max(Xsa, 0.0) * Isr * Iin * Ih2s_sr
        r_sh = th["km_sh"] * fu * h2p / (th["Ks_sh"] + h2p) * sulf * max(Xsh, 0.0) * Isr * Iin * Ih2s_sr
        kd = th["k_dec"]
        dX = (kd * Xsu, kd * Xaa, kd * Xfa, kd * Xpro, kd * Xac, kd * Xh2, kd * Xsa, kd * Xsh)
        r_dec = sum(dX)
        # ---- pH control (alkali)
        dose = 0.0
        if pH < th["pH_sp"]:
            dose = min(th["dose_max"], th["K_dose"] * (th["pH_sp"] - pH))
        doseN = min(th["dosN_max"], th["K_dosN"] * (th["IN_sp"] - IN)) if IN < th["IN_sp"] else 0.0
        Ysu, Yaa, Yfa, Ypro, Yac, Yh2, Ysa, Ysh = (Y_[k] for k in ("su", "aa", "fa", "pro", "ac", "h2", "sa", "sh"))
        S = STO
        dy = [0.0] * NS
        dy[0] = D * (f[0] - su) + r_ch + r_cel + r_hem - r_su
        dy[1] = D * (f[1] - aa) + r_pr - r_aa
        dy[2] = D * (f[2] - fa) + r_li - r_fa
        dy[3] = D * (f[3] - pro) + (1 - Ysu) * F_SU["pro"] * r_su + (1 - Yaa) * F_AA["pro"] * r_aa - r_pro
        dy[4] = (D * (f[4] - ac) + (1 - Ysu) * F_SU["ac"] * r_su + (1 - Yaa) * F_AA["ac"] * r_aa
                 + (1 - Yfa) * F_FA["ac"] * r_fa + (1 - Ypro) * F_PRO["ac"] * r_pro - r_ac - r_sa)
        dy[5] = (D * (f[5] - h2) + (1 - Ysu) * F_SU["h2"] * r_su + (1 - Yaa) * F_AA["h2"] * r_aa
                 + (1 - Yfa) * F_FA["h2"] * r_fa + (1 - Ypro) * F_PRO["h2"] * r_pro - r_h2 - r_sh - 16.0 * j_h2)
        dy[6] = D * (f[6] - ch4) + (1 - Yac) * r_ac + (1 - Yh2) * r_h2 - 64.0 * j_ch4
        dy[7] = D * (f[7] - sI) + F_DEC["sI"] * r_dec
        dy[8] = D * (f[8] - ch) + F_DEC["ch"] * r_dec - r_ch
        dy[9] = D * (f[9] - pr) + F_DEC["pr"] * r_dec - r_pr
        dy[10] = D * (f[10] - li) + F_DEC["li"] * r_dec - r_li
        dy[11] = D * (f[11] - cel) - r_cel
        dy[12] = D * (f[12] - hem) - r_hem
        dy[13] = D * (f[13] - lig)
        dy[14] = D * (f[14] - rc)
        dy[15] = D * (f[15] - inert) + F_DEC["inert"] * r_dec
        dy[16] = D * (f[16] - Xsu) + Ysu * r_su - dX[0]
        dy[17] = D * (f[17] - Xaa) + Yaa * r_aa - dX[1]
        dy[18] = D * (f[18] - Xfa) + Yfa * r_fa - dX[2]
        dy[19] = D * (f[19] - Xpro) + Ypro * r_pro - dX[3]
        dy[20] = D * (f[20] - Xac) + Yac * r_ac - dX[4]
        dy[21] = D * (f[21] - Xh2) + Yh2 * r_h2 - dX[5]
        dy[22] = D * (f[22] - Xsa) + Ysa * r_sa - dX[6]
        dy[23] = D * (f[23] - Xsh) + Ysh * r_sh - dX[7]
        dy[24] = (D * (f[24] - IC) + S["up_su"]["co2"] * r_su + S["up_aa"]["co2"] * r_aa + S["up_fa"]["co2"] * r_fa
                  + S["up_pro"]["co2"] * r_pro + S["up_ac"]["co2"] * r_ac + S["up_h2"]["co2"] * r_h2
                  + S["srb_ac"]["co2"] * r_sa + S["srb_h2"]["co2"] * r_sh + S["dec"]["co2"] * r_dec - j_co2)
        dy[25] = (D * (f[25] - IN) + S["up_su"]["nh3"] * r_su + S["up_aa"]["nh3"] * r_aa + S["up_fa"]["nh3"] * r_fa
                  + S["up_pro"]["nh3"] * r_pro + S["up_ac"]["nh3"] * r_ac + S["up_h2"]["nh3"] * r_h2
                  + S["srb_ac"]["nh3"] * r_sa + S["srb_h2"]["nh3"] * r_sh + S["dec"]["nh3"] * r_dec + doseN)
        dy[26] = D * (f[26] - SO4) + S["srb_ac"]["so4"] * r_sa + S["srb_h2"]["so4"] * r_sh
        dy[27] = D * (f[27] - IS) - (S["srb_ac"]["so4"] * r_sa + S["srb_h2"]["so4"] * r_sh) - j_h2s
        dy[28] = D * (f[28] - cat) + dose
        dy[29] = D * (f[29] - ash)
        s.aux = dict(pH=pH, h=h, j_co2=j_co2, j_ch4=j_ch4, j_h2=j_h2, j_h2s=j_h2s, J=Jt, dose=dose, doseN=doseN,
                     co2=co2, nh3=nh3, h2s=h2s, Inh3=Inh3, Ih2s=Ih2s_ac, Ifa=Ifa_ac, Iac=Iac,
                     r=dict(hyd_ch=r_ch, hyd_cel=r_cel, hyd_hem=r_hem, hyd_pr=r_pr, hyd_li=r_li, up_su=r_su, up_aa=r_aa,
                            up_fa=r_fa, up_pro=r_pro, up_ac=r_ac, up_h2=r_h2, srb_ac=r_sa, srb_h2=r_sh, dec=r_dec))
        return np.array(dy)

    # ---------------------------------------------------------------- initial state / steady solver
    def y_init(s):
        f = np.array(s.feed)
        y = f * 0.15
        for k in ("lig", "rc", "inert", "ash", "cat", "IN", "SO4"):
            y[IX[k]] = f[IX[k]]
        y[IX["IC"]] = max(f[IX["cat"]], 0.03) + 0.02
        for k, v in dict(Xsu=1.0, Xaa=1.0, Xfa=0.7, Xpro=0.7, Xac=2.0, Xh2=1.0, Xsa=0.3, Xsh=0.3).items():
            y[IX[k]] = v
        y[IX["ac"]] = 0.3; y[IX["pro"]] = 0.1; y[IX["su"]] = 0.1
        return y

    def steady(s, y0=None, nhrt=3.0, tol=2e-4, max_ext=4):
        y = s.y_init() if y0 is None else np.array(y0, float)
        T = nhrt / s.D
        for k in range(max_ext + 1):
            sol = solve_ivp(s.rhs, (0.0, T), y, method="BDF", rtol=1e-6, atol=ATOL, first_step=1e-4)
            y = np.maximum(sol.y[:, -1], 0.0) if sol.success else y
            d = s.rhs(0.0, y)
            rel = np.max(np.abs(d) / (np.abs(y) + 1e-3 * (1 + np.abs(y).max())))
            if sol.success and rel < tol:
                return y, True, rel
            T = 1.5 / s.D
        return y, False, rel

    # ---------------------------------------------------------------- diagnostics at a state
    def diag(s, y):
        s.rhs(0.0, y)
        x = s.aux
        v = dict(zip(NAMES, y.tolist()))
        V, Qm = s.V, s.Qm
        f = np.array(s.feed)
        cod_idx = list(range(24))
        cod_in = f[cod_idx].sum() + 64.0 * f[IX["IS"]]
        cod_out = y[cod_idx].sum() + 64.0 * y[IX["IS"]]
        Jgas = dict(co2=x["j_co2"] * V, ch4=x["j_ch4"] * V, h2=x["j_h2"] * V, h2s=x["j_h2s"] * V)   # kmol/d per module
        cod_gas = 64 * Jgas["ch4"] + 16 * Jgas["h2"] + 64 * Jgas["h2s"]
        cod_bal_err = (Qm * cod_in - Qm * cod_out - cod_gas)
        vfa = v["ac"] + v["pro"]
        # bicarbonate alkalinity (kmol/m3) and FOS/TAC-type ratio (mg HAc-eq / mg CaCO3 style)
        hco3 = v["IC"] * s.c["K1"] / (x["h"] + s.c["K1"])
        alk_mgL = hco3 * 50000.0                                   # mg/L as CaCO3
        vfa_mgL = v["ac"] / 64.0 * 60.05 * 1000.0 + v["pro"] / 112.0 * 74.08 * 1000.0
        out = dict(pH=x["pH"], vfa_kgcod=vfa, vfa_mgL=vfa_mgL, alk_mgL=alk_mgL, fos_tac=vfa_mgL / max(alk_mgL, 1.0),
                   tan_mgN=v["IN"] * 14007.0, nh3_mgN=x["nh3"] * 14007.0, h2s_free_mgL=x["h2s"] * 34080.0,
                   Jgas=Jgas, cod_in=cod_in, cod_out=cod_out, cod_bal_err=cod_bal_err, dose=x["dose"], doseN=x["doseN"],
                   cod_removed_frac=1.0 - cod_out / cod_in if cod_in > 0 else 0.0, v=v, rates=x["r"], aux=x)
        return out

# ============================================================================
# 6. BATCH (BMP) SIMULATION  - used for validation / calibration of hydrolysis
# ============================================================================
def bmp_test(th, substrate, days=30.0, vs_loading=4.0, isr=2.0):
    """
    Mesophilic BMP at inoculum:substrate VS ratio `isr`. substrate in {'pome','efb'}.
    Returns cumulative CH4 yield (NmL/g VS added) vs time.  Same ODE as the digester (D = 0).
    """
    F = dict(c=np.zeros(NS), Q=1.0)
    thb = dict(th); thb["T_dig"] = 37.0
    d = Digester(thb, F, 1, 1.0)
    d.D = 0.0
    y = np.zeros(NS)
    # inoculum: digested sludge (VS in biomass + inert); buffered (large strong-cation reserve)
    vs_in = isr * vs_loading                                  # g VS/L inoculum
    y[IX["Xac"]] = 0.18 * vs_in * 1.42 * 0.5; y[IX["Xh2"]] = 0.08 * vs_in * 1.42 * 0.5
    y[IX["Xsu"]] = 0.04 * vs_in; y[IX["Xaa"]] = 0.04 * vs_in; y[IX["Xfa"]] = 0.03 * vs_in; y[IX["Xpro"]] = 0.03 * vs_in
    y[IX["Xsa"]] = 0.005 * vs_in; y[IX["Xsh"]] = 0.005 * vs_in
    y[IX["inert"]] = 0.4 * vs_in * 1.2
    y[IX["IN"]] = 0.02; y[IX["cat"]] = 0.09; y[IX["IC"]] = 0.075; y[IX["SO4"]] = 0.0
    if substrate == "pome":
        fp = th["fr_pome"]
        ccod = dict(su=fp[0], aa=fp[1], ac=fp[2], sI=fp[3], ch=fp[4], pr=fp[5], li=fp[6], inert=fp[7])
        for k, v in ccod.items(): y[IX[k]] += v * 1.0
        vs_g = sum(mass_of(ccod[k], STATE_SP[k]) for k in ccod)          # g VS per g COD-unit
        # scale substrate so that VS added = vs_loading g/L
        k_s = vs_loading / vs_g
        for k, v in ccod.items(): y[IX[k]] = y[IX[k]] - v + v * k_s
    else:
        w = th["fr_efb"]; frc = efb_frec(th)
        parts = dict(cel=cod_of(w[0] * (1 - frc), "ch"), rc=cod_of(w[0] * frc, "ch"), hem=cod_of(w[1], "hem"),
                     lig=cod_of(w[2], "lig"), li=cod_of(w[4], "li"), pr=cod_of(w[5], "pr"), su=cod_of(w[6], "su"))
        vs_g = sum(mass_of(parts[k], STATE_SP[k]) for k in parts)         # VS per g DM  (ash excluded)
        k_s = vs_loading / vs_g
        for k, v in parts.items(): y[IX[k]] += v * k_s
    vs_added = vs_loading
    # augmented system: cumulative CH4 (kmol/m3)
    def f_aug(t, ya):
        dy = d.rhs(t, ya[:NS])
        return np.concatenate([dy, [d.aux["j_ch4"]]])
    ya0 = np.concatenate([y, [0.0]])
    te = np.linspace(0, days, 61)
    sol = solve_ivp(f_aug, (0, days), ya0, method="BDF", t_eval=te, rtol=1e-6, atol=np.concatenate([ATOL, [1e-12]]))
    cum = sol.y[NS] * VN * 1000.0 / vs_added * 1000.0 / 1000.0            # kmol/m3 -> NmL/gVS  (m3/m3 -> L/L ; see below)
    # kmol/m3 * VN m3/kmol = Nm3 per m3 liquid = NL/L ; per g VS/L -> NL/gVS ; *1000 = NmL/gVS
    cum = sol.y[NS] * VN / vs_added * 1000.0
    return sol.t, cum

CAL_TARGETS = dict(pome=397.0, efb=264.0)    # NmL CH4 / g VS, mesophilic BMP [LIT-S]
# calibrated quantities: (name, prior mean, prior sd, lower, upper); sd in ln-units for rates, absolute otherwise
CAL_VARS = [("k_li", 0.8, 0.7, 0.05, 5.0, "ln"), ("k_ch", 1.0, 0.7, 0.1, 5.0, "ln"),
            ("k_cel_ref", 0.08, 0.5, 0.02, 0.5, "ln"), ("beta_lig", 0.45, 0.20, 0.2, 1.2, "lin"),
            ("f_ref_pome", 0.10, 0.04, 0.04, 0.35, "lin")]

def apply_cal(th, vals):
    """write calibrated values into a parameter dict (f_ref_pome rescales POME refractory COD)."""
    t2 = dict(th)
    for (n, m, sd, lo, hi, kind), v in zip(CAL_VARS, vals):
        if n == "f_ref_pome":
            fr = POME_MEAN.copy(); ref = fr[3] + fr[7]
            fr[3] *= v / ref; fr[7] *= v / ref
            rest = 1.0 - v; deg = np.delete(fr, [3, 7]).sum(); sc = rest / deg
            for i in range(len(fr)):
                if i not in (3, 7): fr[i] *= sc
            t2["fr_pome"] = fr; t2["f_ref_pome"] = v
        else:
            t2[n] = v
    return t2

def calibrate(th, verbose=True):
    """Fit k_li, k_ch, k_cel_ref, beta_lig and POME refractory fraction to the two literature BMPs."""
    def vals_from(x):
        return [float(math.exp(v)) if k == "ln" else float(v) for v, (_, _, _, _, _, k) in zip(x, CAL_VARS)]
    x0 = np.array([math.log(m) if k == "ln" else m for (_, m, _, _, _, k) in CAL_VARS])
    lo = np.array([math.log(l) if k == "ln" else l for (_, _, _, l, _, k) in CAL_VARS])
    hi = np.array([math.log(h) if k == "ln" else h for (_, _, _, _, h, k) in CAL_VARS])
    sd = np.array([s_ for (_, _, s_, _, _, _) in CAL_VARS])
    def resid(x):
        t2 = apply_cal(th, vals_from(x))
        r = []
        for sub, tgt in CAL_TARGETS.items():
            _, cum = bmp_test(t2, sub)
            r.append((cum[-1] - tgt) / (0.03 * tgt))
        r += list(0.7 * (x - x0) / sd)             # priors keep the 5-unknown / 2-target problem well-posed
        return r
    sol = least_squares(resid, x0, bounds=(lo, hi), diff_step=2e-2, max_nfev=30)
    vals = vals_from(sol.x)
    out = apply_cal(th, vals)
    res = {sub: float(bmp_test(out, sub)[1][-1]) for sub in CAL_TARGETS}
    if verbose:
        print("  calibrated:", {n: round(v, 3) for (n, *_), v in zip(CAL_VARS, vals)}, "| BMP30:", {k: round(v, 1) for k, v in res.items()})
    return out, res

# ============================================================================
# 7. UNCERTAINTY SAMPLER  (Latin hypercube + Gaussian copula + logistic-normal composition)
# ============================================================================
UNC = [k for k, v in PAR.items() if isinstance(v[1], tuple)]
CORR = {("pome_yield", "cod_pome"): -0.5,        # dilution: more wash-water -> lower COD
        ("k_cel_ref", "k_hem_ref"): 0.5,         # same biomass/particle structure
        ("km_ac", "km_h2"): 0.3}

def lhs(n, k, g):
    u = (np.arange(n)[:, None] + g.random((n, k))) / n
    for j in range(k):
        u[:, j] = u[g.permutation(n), j]
    return u

def _ppf(dist, med, z):
    kind = dist[0]
    if kind == "ln":
        cv = dist[1]; s2 = math.log(1 + cv ** 2); return med * np.exp(-0.5 * s2 + math.sqrt(s2) * z)
    if kind == "tn":
        sd, lo, hi = dist[1], dist[2], dist[3]
        a, b = (lo - med) / sd, (hi - med) / sd
        return truncnorm.ppf(norm.cdf(z), a, b, loc=med, scale=sd)
    if kind == "un":
        return dist[1] + (dist[2] - dist[1]) * norm.cdf(z)
    raise ValueError(kind)

def draw_thetas(n, th0, g, names=None):
    """n parameter sets around th0 (calibrated medians). names=None -> all uncertain inputs."""
    names = UNC if names is None else names
    k = len(names) + (len(POME_KEYS) - 1) + (len(EFB_KEYS) - 1)
    Z = norm.ppf(np.clip(lhs(n, k, g), 1e-6, 1 - 1e-6))
    for (a, b), rho in CORR.items():                       # impose correlation by 2-variable mixing
        if a in names and b in names:
            ia, ib = names.index(a), names.index(b)
            Z[:, ib] = rho * Z[:, ia] + math.sqrt(1 - rho ** 2) * Z[:, ib]
    ths = []
    for i in range(n):
        t = dict(th0)
        for j, nm in enumerate(names):
            t[nm] = float(_ppf(PAR[nm][1], th0[nm], Z[i, j]))
        o = len(names)
        for key, mean, sig, kk in (("fr_pome", th0["fr_pome"], POME_SIG, len(POME_KEYS)), ("fr_efb", th0["fr_efb"], EFB_SIG, len(EFB_KEYS))):
            lg = np.log(mean / mean[-1])[:-1] + sig * Z[i, o:o + kk - 1]
            e = np.exp(np.append(lg, 0.0)); t[key] = e / e.sum()
            o += kk - 1
        ths.append(t)
    return ths

# ============================================================================
# 8. EQUIPMENT / PLANT PARAMETERS (shared equipment is sized for the whole plant)
# ============================================================================
EQ = dict(
    rho_pome=1000.0,                 # kg/m3 bulk POME [ASSUME]
    # shredder (Rittinger-type): E = K*(1/d_p - 1/d_in)  [ASSUME]
    sh_E_at10=8.0, sh_d_in=150.0, conv_kWh_t=0.4,
    # digester geometry / thermal
    aspect=0.55, freeboard=0.6, mix_W_m3=6.0, U_wall=0.4, U_roof=1.1, U_floor=0.6, t_store_h=4.0,
    # pumps
    H_feed=25.0, H_dig=15.0, eta_pump=0.60,
    # gas train
    btf_eff=0.92, o2_per_h2s=0.9, ebct_s=120.0, ac_eff=0.85, chill_T=5.0, chill_cop=3.5,
    blower_dP_kPa=20.0, blower_eta=0.55, air_dP_kPa=12.0, air_eta=0.55, flare_margin=1.10,
    # CHP
    chp_cat=[500.0, 800.0, 1000.0, 1250.0, 1560.0], eta_el_nom=0.395, eta_jacket=0.25, eta_rad=0.02,
    min_load=0.50, lam=1.8, part_load_pts=[(0.50, 0.92), (0.75, 0.97), (1.00, 1.00)], chp_aux_frac=0.012,
    # dewatering / utilities
    press_capture=0.85, cake_DS=0.22, press_kWh_m3=1.0, polymer_kg_tDS=4.0, ct_kW_per_kWth=0.015,
    misc_frac=0.02, mill_kWh_tFFB=21.0,
    # catalogue of standard digester module volumes (m3 liquid)
    catalog=[1000.0, 1250.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0],
    SF_wash=4.0, yield_frac=0.92, N_min_base=4,
)
PL = np.polyfit([p[0] for p in EQ["part_load_pts"]], [p[1] for p in EQ["part_load_pts"]], 2)
def eta_rel(x): return float(np.polyval(PL, min(max(x, 0.3), 1.0)))

def shred_kWh_per_t_wet(d_p):
    K = EQ["sh_E_at10"] / (1.0 / 10.0 - 1.0 / EQ["sh_d_in"])
    return K * (1.0 / d_p - 1.0 / EQ["sh_d_in"])

def gas_summary(J):
    """J: dict kmol/d (co2,ch4,h2,h2s) -> composition and flows (dry, Nm3/d)."""
    tot = sum(J.values())
    return dict(tot_kmol=tot, Nm3d=tot * VN, y={k: v / tot for k, v in J.items()} if tot > 0 else {k: 0 for k in J},
                lhv_kW=(J["ch4"] * LHV_KJMOL["CH4"] + J["h2"] * LHV_KJMOL["H2"]) * 1e3 / 86400.0 / 1.0)

def run_steady(th, F, N, V, y0=None, nhrt=4.0):
    d = Digester(th, F, N, V)
    y, ok, rel = d.steady(y0=y0, nhrt=nhrt, tol=1e-3, max_ext=3)
    g = d.diag(y)
    return d, y, g, ok

# ============================================================================
# 9. PROCESS DESIGN  (EFB share, shredder size, HRT, standard module)
# ============================================================================
def design_share_from_feed_risk(th0, n=1500):
    """largest EFB share such that the P95 of blend TS (feed uncertainty only) stays <= TS_max."""
    g = np.random.default_rng(SEED + 1)
    names = ["util", "pome_yield", "cod_pome", "ash_pome", "efb_ratio", "efb_mc"]
    ths = draw_thetas(n, th0, g, names=names)
    def p95_ts(sh):
        v = [build_feed(t, share=sh, cap_ts=False)["TS"] for t in ths]
        return float(np.percentile(v, 95))
    if p95_ts(1.0) <= th0["TS_max"]:
        return 1.0, p95_ts(1.0)
    sh = brentq(lambda x: p95_ts(x) - th0["TS_max"], 0.0, 1.0, xtol=1e-3)
    return float(sh), p95_ts(sh)

def hrt_sweep(th, F, hrts, N=5):
    """descending continuation sweep (warm start) -> list of dict results."""
    out, y = [], None
    for hrt in sorted(hrts, reverse=True):
        V = F["Q"] * hrt / N
        d, y, g, ok = run_steady(th, F, N, V, y0=y, nhrt=6.0)
        J = g["Jgas"]; gs = gas_summary(J)
        out.append(dict(hrt=hrt, ok=ok, pH=g["pH"], fos=g["fos_tac"], vfa=g["vfa_mgL"], ch4=J["ch4"] * VN * N,
                        bg=gs["Nm3d"] * N, ch4_frac=gs["y"]["ch4"], cod_conv=64 * J["ch4"] / (d.Qm * g["cod_in"]),
                        cod_rem=g["cod_removed_frac"], ph_ok=(g["pH"] > 6.5 and g["fos_tac"] < 0.4 and J["ch4"] > 0)))
    return out

def design_hrt(sweep):
    ok = [r for r in sweep if r["ph_ok"]]
    wash = min([r["hrt"] for r in sweep if not r["ph_ok"]], default=0.0)
    wash = max([r["hrt"] for r in sweep if not r["ph_ok"]], default=0.0)      # largest failing HRT
    asym = max(r["ch4"] for r in sweep if r["ph_ok"])
    h_yield = min(r["hrt"] for r in ok if r["ch4"] >= EQ["yield_frac"] * asym)
    h_floor = EQ["SF_wash"] * wash
    return max(h_yield, h_floor), dict(h_wash=wash, h_yield=h_yield, h_floor=h_floor, ch4_asym=asym)

def tier_flows(th, ffb_tph, share):
    t = dict(th); t["ffb_tph"] = ffb_tph
    return build_feed(t, share=share)


def choose_module(th, share, hrt, tiers=(20.0, 45.0, 70.0), base=45.0, over_max=0.15):
    """one standard module for every tier ('numbering up'): largest catalogue size with overshoot <= over_max in all tiers."""
    Vreq = {f: tier_flows(th, f, share)["Q"] * hrt for f in tiers}
    cands = []
    for m in sorted(EQ["catalog"], reverse=True):
        N = {f: int(math.ceil(Vreq[f] / m)) for f in tiers}
        over = {f: N[f] * m / Vreq[f] - 1.0 for f in tiers}
        D = (4 * m / (math.pi * EQ["aspect"])) ** (1 / 3)
        cands.append((m, N, over, D))
        if N[base] >= EQ["N_min_base"] and D <= 26.0 and max(over.values()) <= over_max:
            return dict(V_mod=m, N=N, over=over, D=D, Vreq=Vreq,
                        rule="largest module with overshoot<=%.0f%% in all tiers, N_base>=%d" % (over_max * 100, EQ["N_min_base"]))
    pool = [c for c in cands if c[1][base] >= EQ["N_min_base"]] or cands
    m, N, over, D = min(pool, key=lambda c: max(c[2].values()))
    return dict(V_mod=m, N=N, over=over, D=D, Vreq=Vreq, rule="fallback: minimum overshoot")

# ============================================================================
# 10. DIGESTER GEOMETRY, GAS TRAIN, CHP, ENERGY AND MASS BALANCE
# ============================================================================
CP_G = dict(co2=45.5, h2o=35.6, n2=30.9, o2=32.7, so2=46.5)       # kJ/kmol/K mean 25-450 degC  [ASSUME Shomate mean]
MWG = dict(ch4=16.043, co2=44.009, h2=2.016, h2s=34.08, h2o=18.015, n2=28.014, o2=31.998, so2=64.06)
T_STACK = 150.0                                                    # degC exhaust after heat recovery  [ASSUME]
T_BTF = 30.0                                                       # degC gas leaving bio-desulfurizer
CP_BIOGAS = 38.0                                                   # kJ/kmol/K wet biogas  [ASSUME]

def tank_geometry(V, th, Q_gas_peak_m3d_per_module):
    a = EQ["aspect"]; D = (4 * V / (math.pi * a)) ** (1 / 3); H = a * D
    Hw = H + EQ["freeboard"]
    Vst = max(Q_gas_peak_m3d_per_module * EQ["t_store_h"] / 24.0, 1.0)
    hd = brentq(lambda hh: math.pi * hh * (3 * (D / 2) ** 2 + hh ** 2) / 6 - Vst, 1e-3, D)
    A_wall = math.pi * D * Hw; A_roof = math.pi * ((D / 2) ** 2 + hd ** 2); A_floor = math.pi * (D / 2) ** 2
    dT = th["T_dig"] - th["T_amb"]
    UA = EQ["U_wall"] * A_wall + EQ["U_roof"] * A_roof + EQ["U_floor"] * A_floor
    return dict(D=D, H_liq=H, H_wall=Hw, V_gas=Vst, dome_h=hd, A_wall=A_wall, A_roof=A_roof, A_floor=A_floor,
                UA_kWK=UA / 1000.0, Q_loss_kW=UA * dT / 1000.0, mixer_kW=EQ["mix_W_m3"] * V / 1000.0)

def combustion(fuel, lam):
    """fuel: kmol/d dict (ch4,co2,h2,h2s,n2,o2,h2o). Returns exhaust kmol/d and air kmol/d (lean burn, excess-air ratio lam)."""
    o2_st = 2.0 * fuel.get("ch4", 0) + 0.5 * fuel.get("h2", 0) + 1.5 * fuel.get("h2s", 0) - fuel.get("o2", 0)
    o2_st = max(o2_st, 0.0)
    o2_air = lam * o2_st
    n_air = o2_air / 0.2095
    ex = dict(co2=fuel.get("co2", 0) + fuel.get("ch4", 0) + n_air * 0.0004,
              h2o=fuel.get("h2o", 0) + 2 * fuel.get("ch4", 0) + fuel.get("h2", 0) + fuel.get("h2s", 0),
              n2=fuel.get("n2", 0) + n_air * (0.7808 + 0.0093),
              o2=(lam - 1.0) * o2_st, so2=fuel.get("h2s", 0))
    return ex, n_air

def gas_train(Jtot, th):
    """Jtot: dict kmol/d dry raw biogas (co2,ch4,h2,h2s) from ALL modules -> streams (kmol/d) and duties (kW)."""
    Pg = P_ATM + th["dP_roof"] * 1e5
    pv38 = p_sat(th["T_dig"]); n_dry = sum(Jtot.values())
    raw = dict(Jtot); raw["h2o"] = n_dry * pv38 / (Pg - pv38)
    # bio-desulfurizer: H2S + 1/2 O2 -> S + H2O ; air supplied o2_per_h2s * removed
    h2s_rem = EQ["btf_eff"] * Jtot["h2s"]
    o2_sup = EQ["o2_per_h2s"] * h2s_rem; o2_cons = 0.5 * h2s_rem
    n_air_btf = o2_sup / 0.2095
    btf = dict(ch4=Jtot["ch4"], co2=Jtot["co2"], h2=Jtot["h2"], h2s=Jtot["h2s"] - h2s_rem,
               n2=n_air_btf * (0.7808 + 0.0093), o2=o2_sup - o2_cons)
    btf["co2"] += n_air_btf * 0.0004
    nd = sum(btf.values()); pv_b = p_sat(T_BTF)
    btf_w = nd * pv_b / (Pg - pv_b)
    pv_c = p_sat(EQ["chill_T"]); chill_w = nd * pv_c / (Pg - pv_c)       # chiller: dew point = chill_T
    cond = max(btf_w - chill_w, 0.0)
    fuel = dict(btf); fuel["h2s"] = btf["h2s"] * (1 - EQ["ac_eff"]); fuel["h2o"] = chill_w
    ac_h2s = btf["h2s"] - fuel["h2s"]
    nfd = sum(v for k, v in fuel.items() if k != "h2o")
    lhv_kW = (fuel["ch4"] * LHV_KJMOL["CH4"] + fuel["h2"] * LHV_KJMOL["H2"]) * 1e3 / 86400.0
    Q_chill = (cond * MWG["h2o"] * H_VAP + (nd + btf_w) * CP_BIOGAS * (T_BTF - EQ["chill_T"])) / 86400.0
    V_air = n_air_btf * VN / 86400.0
    V_gas_s = (nd + chill_w) * VN / 86400.0 * (273.15 + 20.0) / 273.15
    P_air = V_air * EQ["air_dP_kPa"] / EQ["air_eta"]
    P_blow = V_gas_s * EQ["blower_dP_kPa"] / EQ["blower_eta"]
    return dict(raw=raw, btf=btf, btf_w=btf_w, fuel=fuel, cond=cond, h2s_rem=h2s_rem, ac_h2s=ac_h2s, o2_sup=o2_sup, n_air_btf=n_air_btf,
                lhv_kW=lhv_kW, Q_chill_kW=Q_chill, P_chill_kW=Q_chill / EQ["chill_cop"], P_air_kW=P_air, P_blow_kW=P_blow,
                h2s_ppm_raw=1e6 * Jtot["h2s"] / n_dry, h2s_ppm_fuel=1e6 * fuel["h2s"] / nfd,
                ch4_frac_dry=Jtot["ch4"] / n_dry, ch4_frac_fuel=fuel["ch4"] / nfd, nfd=nfd, V_gas_actual_m3s=V_gas_s)

def chp_select(P_fuel95_kW):
    P_el = P_fuel95_kW * EQ["eta_el_nom"]
    best = None
    for u in EQ["chp_cat"]:
        n = max(2, int(math.ceil(P_el / u)))
        inst = n * u
        if best is None or inst < best[0] - 1e-9 or (abs(inst - best[0]) < 1e-9 and n < best[2]):
            best = (inst, u, n)
    return dict(P_unit=best[1], N_gen=best[2], P_inst=best[0])

def chp_dispatch(fuel_kW, chp, gt, th):
    """equal load sharing over n_run units (min-load rule); gas above installed capacity goes to the flare."""
    unit_fuel = chp["P_unit"] / EQ["eta_el_nom"]
    n_run = int(math.floor(fuel_kW / (unit_fuel * EQ["min_load"])))
    n_run = min(chp["N_gen"], max(1, n_run))
    load = min(fuel_kW / (n_run * unit_fuel), 1.0)
    burned = load * n_run * unit_fuel
    flare = max(fuel_kW - burned, 0.0)
    eta = EQ["eta_el_nom"] * eta_rel(load)
    P_el = burned * eta
    fr = burned / fuel_kW if fuel_kW > 0 else 0.0
    fuel = {k: v * fr for k, v in gt["fuel"].items()}
    ex, n_air = combustion(fuel, EQ["lam"])
    Q_j = burned * EQ["eta_jacket"]; Q_r = burned * EQ["eta_rad"]
    H_ex = burned - P_el - Q_j - Q_r                                   # kW carried by hot exhaust (energy balance)
    ncp = sum(ex[k] * CP_G[k] for k in ex) / 86400.0                   # kW/K
    T_ex = 25.0 + H_ex / ncp if ncp > 0 else 25.0
    Q_exh = ncp * max(T_ex - T_STACK, 0.0)
    return dict(n_run=n_run, load=load, eta_el=eta, P_el=P_el, Q_jacket=Q_j, Q_rad=Q_r, Q_exh=Q_exh, T_exh=T_ex, flare_kW=flare,
                burned_kW=burned, exhaust=ex, n_air=n_air, fuel_burned=fuel, Q_stack=H_ex - Q_exh, fuel_frac=fr)

def plant_energy(F, th, des, Jtot, chp):
    """deterministic plant energy balance for one operating point."""
    gt = gas_train(Jtot, th)
    ch = chp_dispatch(gt["lhv_kW"], chp, gt, th)
    N = des["N"]; geo = des["geo"]; Qd = F["Q"]
    P = {}
    P["feed_pumps"] = RHO_W * G * EQ["H_feed"] * (Qd / 86400.0) / EQ["eta_pump"] / 1e3
    P["digestate_pumps"] = RHO_W * G * EQ["H_dig"] * (Qd / 86400.0) / EQ["eta_pump"] / 1e3
    P["mixers"] = geo["mixer_kW"] * N
    P["shredder"] = F["M_efb"] * shred_kWh_per_t_wet(th["d_p_mm"]) / 24.0
    P["conveyors"] = F["M_efb"] * EQ["conv_kWh_t"] / 24.0
    P["air_blower"] = gt["P_air_kW"]; P["gas_blower"] = gt["P_blow_kW"]; P["gas_chiller"] = gt["P_chill_kW"]
    P["screw_press"] = EQ["press_kWh_m3"] * Qd / 24.0
    Q_ct = F["Qcool_kW"] + gt["Q_chill_kW"] * (1 + 1.0 / EQ["chill_cop"])
    P["cooling_tower"] = EQ["ct_kW_per_kWth"] * Q_ct
    P["chp_aux_misc"] = (EQ["chp_aux_frac"] + EQ["misc_frac"]) * ch["P_el"]
    P_par = sum(P.values())
    Q_dig = geo["Q_loss_kW"] * N
    Q_heat_avail = ch["Q_jacket"] + ch["Q_exh"]
    P_mill = EQ["mill_kWh_tFFB"] * th["ffb_tph"] * th["util"]
    net = ch["P_el"] - P_par
    return dict(gt=gt, chp=ch, P=P, P_par=P_par, P_gross=ch["P_el"], P_net=net, Q_dig=Q_dig, Q_heat_avail=Q_heat_avail,
                Q_heat_export=max(Q_heat_avail - Q_dig, 0.0), Q_cool=Q_ct, P_mill=P_mill, P_export=net - P_mill,
                self_suff=min(net / P_mill, 9.99) if P_mill > 0 else 0.0)

# ---------------------------------------------------------------- mass balance (species level, kg/d)
GRP = [("water", "Air"), ("carb", "Karbohidrat partikulat (selulosa, hemiselulosa, pati)"), ("lignin", "Lignin dan residu sulit terurai"),
       ("protbio", "Protein dan biomassa mikroba"), ("lipid", "Minyak/lemak dan asam lemak"), ("solorg", "Organik terlarut (gula, VFA, asam amino)"),
       ("inertp", "Inert partikulat"), ("mineral", "Mineral dan garam (abu, K+)"), ("tan", "Amonium (sebagai NH3)"),
       ("sulf", "Sulfat dan sulfida"), ("ic", "Karbon anorganik (sebagai CO2)"), ("dgas", "CH4/H2 terlarut"),
       ("g_ch4", "CH4"), ("g_co2", "CO2"), ("g_h2", "H2"), ("g_h2s", "H2S"), ("g_h2o", "Uap air"), ("g_n2", "N2 (+Ar)"),
       ("g_o2", "O2"), ("g_so2", "SO2"), ("sulfur", "Belerang unsur (S0)"), ("chem", "Bahan kimia (NaOH/polimer/karbon aktif)")]
GRP_KEYS = [k for k, _ in GRP]
STATE_GRP = dict(su="solorg", aa="solorg", fa="lipid", pro="solorg", ac="solorg", h2="dgas", ch4="dgas", sI="solorg",
                 ch="carb", pr="protbio", li="lipid", cel="carb", hem="carb", lig="lignin", rc="lignin", inert="inertp",
                 Xsu="protbio", Xaa="protbio", Xfa="protbio", Xpro="protbio", Xac="protbio", Xh2="protbio", Xsa="protbio", Xsh="protbio")
PART_STATES = ("ch", "pr", "li", "cel", "hem", "lig", "rc", "inert", "Xsu", "Xaa", "Xfa", "Xpro", "Xac", "Xh2", "Xsa", "Xsh")
SPFORM = dict(ch4="CH4", co2="CO2", h2="H2", h2s="H2S", h2o="H2O", n2="N2", o2="O2", so2="SO2")
ELFORM = {k: parse_formula(v) if k != "n2" else np.zeros(5) for k, v in
          dict(ch4="CH4", co2="CO2", h2="H2", h2s="H2S", h2o="H2O", n2="N2", o2="O2", so2="SO2").items()}

def liq_species(vec, Q):
    """species (kg/d, fine-grained) of a liquid stream with state vector `vec` (per m3) and flow Q m3/d."""
    out = {}
    for k in NAMES:
        c = vec[IX[k]] * Q
        if k in STATE_SP: out[k] = c * SPX[STATE_SP[k]].mass_per_cod
        elif k == "IC": out[k] = c * SPX["co2"].MW
        elif k == "IN": out[k] = c * SPX["nh3"].MW
        elif k == "SO4": out[k] = c * SPX["so4"].MW
        elif k == "IS": out[k] = c * SPX["h2s"].MW
        elif k == "cat": out[k] = c * 39.098
        elif k == "ash": out[k] = c
    return out

def to_groups(sp, water=0.0):
    g = dict.fromkeys(GRP_KEYS, 0.0); g["water"] = water
    for k, v in sp.items():
        if k in STATE_GRP: g[STATE_GRP[k]] += v
        elif k == "IC": g["ic"] += v
        elif k == "IN": g["tan"] += v
        elif k in ("SO4", "IS"): g["sulf"] += v
        elif k in ("cat", "ash"): g["mineral"] += v
        elif k in g: g[k] += v
    return g

def elements(sp, water=0.0):
    """element kmol/d from fine-grained species dict (kg/d). Minerals/chemicals ignored (pass-through)."""
    E = np.zeros(5)
    for k, v in sp.items():
        if k in STATE_SP: E += SPX[STATE_SP[k]].e * v / SPX[STATE_SP[k]].MW
        elif k == "IC": E += SPX["co2"].e * v / SPX["co2"].MW
        elif k == "IN": E += SPX["nh3"].e * v / SPX["nh3"].MW
        elif k == "SO4": E += SPX["so4"].e * v / SPX["so4"].MW
        elif k == "IS": E += SPX["h2s"].e * v / SPX["h2s"].MW
        elif k.startswith('g_') and k[2:] in ELFORM: E += ELFORM[k[2:]] * v / MWG[k[2:]]
        elif k in ELFORM: E += ELFORM[k] * v / MWG[k]
        elif k == "sulfur": E += np.array([0, 0, 0, 0, 1.0]) * v / 32.06
    E += SPX["h2o"].e * water / SPX["h2o"].MW
    return E

def gas_kg(nd):                      # kmol/d dict -> kg/d dict with g_ prefix
    return {"g_" + k: v * MWG[k] for k, v in nd.items()}

def mass_balance(th, F, des, d, y, g, E):
    """full stream table (kg/d) and closure tests for the nominal operating point."""
    N, V = des["N"], des["V_mod"]; Q = F["Q"]; Qp = F["Qp"]
    gt, ch = E["gt"], E["chp"]
    S = {}                                     # id -> dict(name, sp, water, T, P, phase)
    # --- 1 raw POME, 3 screenings, 4 screened POME
    raw_vec = np.zeros(NS)
    for k, v in F["raw"].items(): raw_vec[IX[k]] = v
    raw_vec[IX["IN"]] = th["tan_pome"]; raw_vec[IX["SO4"]] = th["so4_pome"]; raw_vec[IX["cat"]] = th["cat_pome"]; raw_vec[IX["ash"]] = th["ash_pome"]
    sp1 = liq_species(raw_vec, Qp); m1 = Qp * EQ["rho_pome"]
    S[1] = dict(name="POME mentah dari pabrik", sp=sp1, water=m1 - sum(sp1.values()), T=th["T_pome_in"], P=1.3, ph="C")
    scr_dry = {k: Qp * F["scr_cod"][k] * SPX[STATE_SP[k]].mass_per_cod for k in ("ch", "pr", "inert")}
    scr_dry["ash"] = Qp * th["ash_pome"] * th["e_scr"]
    scr_w = sum(scr_dry.values()) * 0.6 / 0.4
    S[3] = dict(name="Residu saringan", sp=scr_dry, water=scr_w, T=th["T_pome_in"], P=1.01, ph="P")
    sp4 = {k: sp1[k] - scr_dry.get(k, 0.0) for k in sp1}
    S[4] = dict(name="POME tersaring", sp=sp4, water=S[1]["water"] - scr_w, T=th["T_pome_in"], P=1.3, ph="C")
    S[5] = dict(name="POME didinginkan", sp=dict(sp4), water=S[4]["water"], T=F["T_p_out"], P=1.2, ph="C")
    # --- 2 EFB to AD, 6 shredded
    tE = F["tE"]; spE = liq_species(tE, 1.0)             # tE is per day -> species kg/d
    S[2] = dict(name="TKKS mentah ke digester", sp=spE, water=F["wat_efb"], T=th["T_amb"], P=1.01, ph="PB")
    S[6] = dict(name="TKKS tercacah", sp=dict(spE), water=F["wat_efb"], T=th["T_amb"], P=1.01, ph="PB")
    # --- 7 blend (+ 8 alkali)
    sp7 = {k: S[5]["sp"].get(k, 0) + S[6]["sp"].get(k, 0) for k in set(S[5]["sp"]) | set(S[6]["sp"])}
    w7 = S[5]["water"] + S[6]["water"]
    # consistency with concentration vector c*Q (build_feed)
    sp7c = liq_species(F["c"], Q)
    blend_err = max(abs(sp7[k] - sp7c[k]) / (abs(sp7c[k]) + 1e-9) for k in sp7c if abs(sp7c[k]) > 1e-6)
    S[7] = dict(name="Umpan campuran POME+TKKS", sp=sp7, water=w7, T=th["T_dig"], P=2.0, ph="B")
    dose_kmol = g["dose"] * V * N
    S[8] = dict(name="Larutan alkali (NaOH)", sp={"chem": dose_kmol * 40.0}, water=0.0, T=th["T_amb"], P=2.0, ph="C")
    S[23] = dict(name="Nutrien nitrogen (urea, dihitung sbg N)", sp={"IN": g["doseN"] * V * N * SPX["nh3"].MW}, water=0.0, T=th["T_amb"], P=2.0, ph="C")
    # --- digester: 9 raw biogas, 10 digestate
    Jt = {k: v * N for k, v in g["Jgas"].items()}
    raw_gas = dict(Jt); raw_gas["h2o"] = gt["raw"]["h2o"]
    S[9] = dict(name="Biogas mentah (jenuh uap, 38 C)", sp=gas_kg(raw_gas), water=0.0, T=th["T_dig"], P=1.02, ph="G")
    w_rx = sum(STO[k]["h2o"] * g["rates"][k] for k in g["rates"]) * V * N * SPX["h2o"].MW      # kg/d water produced by reactions
    yv = y.copy()
    sp10 = liq_species(yv, Q)
    w10 = w7 + w_rx - raw_gas["h2o"] * MWG["h2o"]   # water balance (reaction water from stoichiometry)
    sp10["cat"] += 0.0
    S[10] = dict(name="Digestat dari digester", sp=sp10, water=w10, T=th["T_dig"], P=1.5, ph="CP")
    # --- dewatering: 19 cake, 20 filtrate, 21 polymer
    solid_keys = list(PART_STATES) + ["ash"]
    capt = {k: sp10[k] * EQ["press_capture"] for k in solid_keys}
    sol_cake = sum(capt.values())
    poly = EQ["polymer_kg_tDS"] * sol_cake / 1000.0
    cake_mass = sol_cake / EQ["cake_DS"]
    w_cake = max(cake_mass - sol_cake, 0.0)
    fw = w_cake / w10
    sp19 = {k: (capt[k] if k in capt else sp10[k] * fw) for k in sp10}
    sp19["chem"] = poly
    sp20 = {k: sp10[k] - sp19[k] for k in sp10}
    S[19] = dict(name="Kue digestat", sp=sp19, water=w_cake, T=th["T_dig"], P=1.01, ph="PB")
    S[20] = dict(name="Filtrat (efluen cair)", sp=sp20, water=w10 - w_cake, T=th["T_dig"], P=1.01, ph="C")
    S[21] = dict(name="Polimer flokulan", sp={"chem": poly}, water=0.0, T=th["T_amb"], P=1.01, ph="C")
    # --- gas train: 11 air, 12 gas after BTF, 13 sulfur sludge, 14 condensate, 15 clean fuel gas, 16 spent carbon
    air_btf = dict(o2=gt["o2_sup"], n2=gt["n_air_btf"] * (0.7808 + 0.0093), co2=gt["n_air_btf"] * 0.0004)
    S[11] = dict(name="Udara ke bio-desulfurisasi", sp=gas_kg(air_btf), water=0.0, T=th["T_amb"], P=1.2, ph="G")
    btf_out = dict(gt["btf"]); btf_out["h2o"] = gt["btf_w"]
    S[12] = dict(name="Biogas keluar BTF (30 C)", sp=gas_kg(btf_out), water=0.0, T=T_BTF, P=1.05, ph="G")
    sulfur = gt["h2s_rem"] * 32.06
    w13 = (raw_gas["h2o"] + gt["h2s_rem"] - gt["btf_w"]) * MWG["h2o"]
    S[13] = dict(name="Lumpur belerang / blowdown BTF", sp={"sulfur": sulfur}, water=w13, T=T_BTF, P=1.01, ph="CP")
    S[14] = dict(name="Kondensat chiller", sp={}, water=gt["cond"] * MWG["h2o"], T=EQ["chill_T"], P=1.01, ph="C")
    fuel_all = gt["fuel"]
    S[15] = dict(name="Biogas bersih ke CHP (5 C)", sp=gas_kg(fuel_all), water=0.0, T=EQ["chill_T"] + 15, P=1.15, ph="G")
    S[16] = dict(name="Karbon aktif jenuh (H2S)", sp={"chem": gt["ac_h2s"] * MWG["h2s"]}, water=0.0, T=th["T_amb"], P=1.01, ph="P")
    # --- CHP: split fuel between burned (17 air, 18 exhaust) and flare (22)
    ex, n_air = ch["exhaust"], ch["n_air"]
    air_ch = dict(o2=n_air * 0.2095, n2=n_air * (0.7808 + 0.0093), co2=n_air * 0.0004)
    S[17] = dict(name="Udara pembakaran CHP", sp=gas_kg(air_ch), water=0.0, T=th["T_amb"], P=1.1, ph="G")
    S[18] = dict(name="Gas buang CHP (setelah pemulihan panas)", sp=gas_kg(ex), water=0.0, T=T_STACK, P=1.01, ph="G")
    fl = {k: v - ch["fuel_burned"].get(k, 0.0) for k, v in fuel_all.items()}
    S[22] = dict(name="Gas ke flare (kelebihan/darurat)", sp=gas_kg(fl), water=0.0, T=EQ["chill_T"] + 15, P=1.1, ph="G")
    # --- unit-level closure (kg/d and elements)
    def tot(s): return sum(s["sp"].values()) + s["water"]
    chk = {}
    m_in = tot(S[7]) + tot(S[8]) + tot(S[23]); m_out = tot(S[9]) + tot(S[10])
    chk["digester_mass"] = (m_in - m_out) / m_in
    Ein = elements(S[7]["sp"], S[7]["water"]) + elements(S[23]["sp"]); Eout = elements(S[9]["sp"], 0.0) + elements(S[10]["sp"], S[10]["water"])
    for i, el in enumerate("CHONS"):
        chk["digester_" + el] = (Ein[i] - Eout[i]) / max(abs(Ein[i]), 1e-12)
    m_in = tot(S[10]) + tot(S[21]); m_out = tot(S[19]) + tot(S[20])
    chk["dewatering_mass"] = (m_in - m_out) / m_in
    m_in = tot(S[9]) + tot(S[11]); m_out = tot(S[12]) + tot(S[13])
    chk["btf_gas_mass_excl_water"] = None
    sp_in = elements(S[9]["sp"]) + elements(S[11]["sp"]); sp_out = elements(S[12]["sp"]) + elements(S[13]["sp"], S[13]["water"])
    chk["btf_S"] = (sp_in[4] - sp_out[4]) / max(sp_in[4], 1e-12)
    chk["btf_C"] = (sp_in[0] - sp_out[0]) / max(sp_in[0], 1e-12)
    m_in = tot(S[15]) - tot(S[22]) + tot(S[17]); m_out = tot(S[18])
    chk["chp_mass"] = (m_in - m_out) / m_in
    Ein = elements(S[15]["sp"]) - elements(S[22]["sp"]) + elements(S[17]["sp"]); Eout = elements(S[18]["sp"])
    for i, el in enumerate("CHONS"):
        chk["chp_" + el] = (Ein[i] - Eout[i]) / max(abs(Ein[i]), 1e-12)
    chk["blend_consistency"] = blend_err
    chk.pop("btf_gas_mass_excl_water")
    # --- overall plant boundary (feed in / products + wastes out), kg/d
    m_plant_in = tot(S[1]) + tot(S[2]) + tot(S[8]) + tot(S[23]) + tot(S[11]) + tot(S[17]) + tot(S[21])
    m_plant_out = (tot(S[3]) + tot(S[19]) + tot(S[20]) + tot(S[13]) + tot(S[14]) + tot(S[16]) + tot(S[18]) + tot(S[22]))
    chk["plant_mass"] = (m_plant_in - m_plant_out) / m_plant_in
    # COD / energy
    chk["COD_digester"] = g["cod_bal_err"] / (d.Qm * g["cod_in"])
    return S, chk, dict(m_in=m_plant_in, m_out=m_plant_out, w_rx=w_rx)

def stream_table(S, order=None):
    rows = []
    for i in sorted(S):
        s = S[i]; gp = to_groups(s["sp"], s["water"])
        tot = sum(gp.values())
        rows.append(dict(id=i, name=s["name"], T=s["T"], P=s["P"], ph=s["ph"], kg_h=tot / 24.0, comp={k: v / 24.0 for k, v in gp.items() if abs(v) > 1e-9}))
    return rows

# ============================================================================
# 11. MONTE CARLO, SENSITIVITY, ANNUAL DYNAMIC SIMULATION
# ============================================================================
MC_IN = ["util", "pome_yield", "cod_pome", "efb_ratio", "efb_mc", "d_p_mm", "beta_lig", "k_li", "k_ch", "k_cel_ref", "k_hem_ref",
         "km_ac", "km_h2", "KI_nh3", "KI_h2s_ac", "kLa", "cat_pome", "so4_pome", "T_pome_in"]

def mc_run(th_mc, des, y_base, n, g, verbose=True):
    ths = draw_thetas(n, th_mc, g)
    rec = []; t0 = time.time()
    for i, t in enumerate(ths):
        F = build_feed(t, share=des["share"])
        d, y, gg, ok = run_steady(t, F, des["N"], des["V_mod"], y0=y_base, nhrt=4.0)
        if not ok:
            d, y, gg, ok = run_steady(t, F, des["N"], des["V_mod"], y0=None, nhrt=6.0)
        J = {k: v * des["N"] for k, v in gg["Jgas"].items()}
        gs = gas_summary(J)
        rec.append(dict(t=t, F=F, J=J, gs=gs, g=gg, ok=ok, y=y))
        if verbose and (i + 1) % max(1, n // 5) == 0:
            print("   MC %d/%d  (%.0f s)" % (i + 1, n, time.time() - t0))
    return rec

def mc_arrays(rec, des, chp):
    A = {k: [] for k in ("bg", "ch4", "ch4_frac", "h2s_ppm_raw", "pH", "fos", "tan", "nh3", "cod_rem", "cod_conv", "share", "TS", "Q", "HRT",
                          "lhv_kW", "P_gross", "P_net", "P_export", "P_par", "Q_heat_export", "Q_cool", "flare_kW", "load", "eta_el", "self_suff",
                          "upset", "ok", "ch4_yield_pome", "T_exh", "h2s_ppm_fuel", "P_mill", "cake_td", "dose", "doseN")}
    X = {k: [] for k in MC_IN}
    for r in rec:
        t, F, J, gs, g = r["t"], r["F"], r["J"], r["gs"], r["g"]
        E = plant_energy(F, t, des, J, chp)
        A["bg"].append(gs["Nm3d"]); A["ch4"].append(J["ch4"] * VN); A["ch4_frac"].append(gs["y"]["ch4"]); A["h2s_ppm_raw"].append(E["gt"]["h2s_ppm_raw"])
        A["pH"].append(g["pH"]); A["fos"].append(g["fos_tac"]); A["tan"].append(g["tan_mgN"]); A["nh3"].append(g["nh3_mgN"])
        A["cod_rem"].append(g["cod_removed_frac"]); A["cod_conv"].append(64 * J["ch4"] / (F["Q"] * g["cod_in"]))
        A["share"].append(F["share"]); A["TS"].append(F["TS"]); A["Q"].append(F["Q"]); A["HRT"].append(des["N"] * des["V_mod"] / F["Q"])
        A["lhv_kW"].append(E["gt"]["lhv_kW"]); A["P_gross"].append(E["P_gross"]); A["P_net"].append(E["P_net"]); A["P_export"].append(E["P_export"])
        A["P_par"].append(E["P_par"]); A["Q_heat_export"].append(E["Q_heat_export"]); A["Q_cool"].append(E["Q_cool"])
        A["flare_kW"].append(E["chp"]["flare_kW"]); A["load"].append(E["chp"]["load"]); A["eta_el"].append(E["chp"]["eta_el"])
        A["self_suff"].append(E["self_suff"]); A["T_exh"].append(E["chp"]["T_exh"]); A["h2s_ppm_fuel"].append(E["gt"]["h2s_ppm_fuel"])
        A["P_mill"].append(E["P_mill"])
        A["upset"].append(float((g["pH"] < 6.5) or (g["fos_tac"] > 0.4) or (J["ch4"] <= 0)))
        A["ok"].append(float(r["ok"]))
        A["ch4_yield_pome"].append(J["ch4"] * VN / F["Qp"])
        A["cake_td"].append(0.0); A["dose"].append(g["dose"] * des["V_mod"] * des["N"]); A["doseN"].append(g["doseN"] * des["V_mod"] * des["N"] * 14.007)
        for k in MC_IN: X[k].append(t[k])
    return {k: np.array(v) for k, v in A.items()}, {k: np.array(v) for k, v in X.items()}

def spearman_table(X, A, outs):
    tab = {}
    for o in outs:
        y = rankdata(A[o]); tab[o] = {}
        for k, x in X.items():
            if np.std(x) < 1e-12: tab[o][k] = 0.0; continue
            r = np.corrcoef(rankdata(x), y)[0, 1]; tab[o][k] = float(r)
    return tab

def pct(a, q=(5, 50, 95)): return [float(np.percentile(a, p)) for p in q]

def year_sim(th, des, chp, y0, g, A_seas=0.15, m_pk=9.5, phi=0.7, sig=0.06, shut_days=(40, 54)):
    days = 365
    doy = np.arange(days)
    f = 1.0 + A_seas * np.cos(2 * np.pi * (doy / 365.0 - m_pk / 12.0)); f /= f.mean()
    e = np.zeros(days)
    for i in range(1, days):
        e[i] = phi * e[i - 1] + math.sqrt(1 - phi ** 2) * sig * g.standard_normal()
    util = np.clip(th["util"] * f * (1 + e), 0.35, 1.05)
    util[shut_days[0]:shut_days[1]] = 0.0                               # annual maintenance shutdown (low season)
    y = y0.copy(); rows = []
    for dd in range(days):
        t = dict(th); t["util"] = float(util[dd])
        F = build_feed(t, share=des["share"])
        dig = Digester(t, F, des["N"], des["V_mod"], Q_override=F["Q"])
        sol = solve_ivp(dig.rhs, (0.0, 1.0), y, method="BDF", rtol=1e-6, atol=ATOL, first_step=1e-4)
        y = np.maximum(sol.y[:, -1], 0.0)
        gg = dig.diag(y); J = {k: v * des["N"] for k, v in gg["Jgas"].items()}; gs = gas_summary(J)
        E = plant_energy(F, t, des, J, chp)
        rows.append(dict(day=dd, util=util[dd], Q=F["Q"], bg=gs["Nm3d"], ch4=J["ch4"] * VN, ch4_frac=gs["y"]["ch4"], pH=gg["pH"],
                         vfa=gg["vfa_mgL"], fos=gg["fos_tac"], P_gross=E["P_gross"], P_net=E["P_net"], P_mill=E["P_mill"],
                         P_export=E["P_export"], flare=E["chp"]["flare_kW"], TS=F["TS"], share=F["share"]))
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def startup_sim(th, des, days=120.0):
    """cold start from inoculated digester -> time series of states (used for dynamic validation plot)."""
    F = build_feed(th, share=des["share"])
    dig = Digester(th, F, des["N"], des["V_mod"])
    y0 = dig.y_init(); te = np.linspace(0, days, 121)
    sol = solve_ivp(dig.rhs, (0, days), y0, method="BDF", t_eval=te, rtol=1e-6, atol=ATOL, first_step=1e-4)
    out = dict(t=sol.t, bg=[], ch4=[], pH=[], vfa=[], Xac=[], tan=[])
    for i in range(len(sol.t)):
        g = dig.diag(sol.y[:, i]); J = {k: v * des["N"] for k, v in g["Jgas"].items()}
        out["bg"].append(sum(J.values()) * VN); out["ch4"].append(J["ch4"] * VN); out["pH"].append(g["pH"]); out["vfa"].append(g["vfa_mgL"])
        out["Xac"].append(sol.y[IX["Xac"], i]); out["tan"].append(g["tan_mgN"])
    return {k: np.array(v) for k, v in out.items()}

# ============================================================================
# 12. EMISSIONS AND PRELIMINARY ECONOMICS (screening only)
# ============================================================================
EMIS = dict(B0=0.25, MCF_base=0.80, remov_base=0.75, leak=0.01, slip=0.005, flare_destr=0.98, MCF_filtrate=0.2, GWP_CH4=28.0,
            ef_grid=0.80, ef_diesel=0.75)           # IPCC 2006 Vol.5 Ch.6 defaults / AR5 GWP100; EF kgCO2/kWh [ASSUME]
def emissions(th, F, des, g, E, S_dig_cod_biodeg):
    """tCO2e/yr for the nominal operating point (kg CH4/d first)."""
    cod_pome_d = F["Qp"] * th["cod_pome"] * (1 - th["e_scr"] * (th["fr_pome"][4] + th["fr_pome"][5] + th["fr_pome"][7]))
    base_ch4 = cod_pome_d * EMIS["remov_base"] * EMIS["B0"] * EMIS["MCF_base"]                        # open pond, kg CH4/d
    Jt = {k: v * des["N"] for k, v in g["Jgas"].items()}
    ch4_prod = Jt["ch4"] * MWG["ch4"]
    dissolved = g["v"]["ch4"] * F["Q"] * SPX["ch4"].mass_per_cod                                         # kg CH4/d leaves with digestate
    proj = (EMIS["leak"] * ch4_prod + dissolved + EMIS["slip"] * ch4_prod * E["chp"]["fuel_frac"]
            + (1 - EMIS["flare_destr"]) * E["chp"]["flare_kW"] / max(E["gt"]["lhv_kW"], 1e-9) * ch4_prod
            + EMIS["B0"] * EMIS["MCF_filtrate"] * S_dig_cod_biodeg)
    days = th["days_yr"]
    return dict(base_t=base_ch4 * EMIS["GWP_CH4"] * days / 1000.0, proj_t=proj * EMIS["GWP_CH4"] * days / 1000.0,
                avoided_t=(base_ch4 - proj) * EMIS["GWP_CH4"] * days / 1000.0, base_kgd=base_ch4, proj_kgd=proj,
                elec_t=E["P_net"] * 24 * days / 1000.0 * EMIS["ef_diesel"] / 1000.0)

ECON = dict(capex_dig=250.0, capex_chp=1050.0, capex_gas=420.0, capex_efb_per_tph=90e3, capex_press=180e3, bop=0.20, cont=0.15,
            opex_frac=0.045, labour=96e3, p_el_export=0.08, p_el_self=0.15, p_carbon=8.0, discount=0.10, life=15)
# USD; ALL unit costs are screening placeholders [ASSUME] -> replace with vendor quotations.
def econ_screen(th, des, chp, E, em, g):
    capex = (ECON["capex_dig"] * des["V_mod"] * des["N"] + ECON["capex_chp"] * chp["P_inst"]
             + ECON["capex_gas"] * E["gt"]["fuel"]["ch4"] * VN / 24.0 * 1.0 + ECON["capex_efb_per_tph"] * (E["P"]["shredder"] > 0) * th["ffb_tph"] * th["efb_ratio"] * des["share"]
             + ECON["capex_press"])
    capex *= (1 + ECON["bop"]) * (1 + ECON["cont"])
    days = th["days_yr"]
    self_kW = min(E["P_net"], E["P_mill"]); exp_kW = max(E["P_net"] - E["P_mill"], 0.0)
    rev = (self_kW * ECON["p_el_self"] + exp_kW * ECON["p_el_export"]) * 24 * days + em["avoided_t"] * ECON["p_carbon"]
    opex = ECON["opex_frac"] * capex + ECON["labour"]
    cf = rev - opex
    r, n = ECON["discount"], ECON["life"]
    ann = (1 - (1 + r) ** -n) / r
    return dict(capex=capex, revenue=rev, opex=opex, cashflow=cf, payback=capex / cf if cf > 0 else float("inf"), npv=-capex + cf * ann,
                rev_el=(self_kW * ECON["p_el_self"] + exp_kW * ECON["p_el_export"]) * 24 * days, rev_c=em["avoided_t"] * ECON["p_carbon"],
                lcoe=(capex / ann + opex) / max(E["P_net"] * 24 * days, 1.0))

# ============================================================================
# 13. PLOT STYLE (fixed categorical order, one axis per chart, thin marks, recessive grid)
# ============================================================================
CC = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": "#b8b7b1", "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left", "lines.linewidth": 2.0,
                     "legend.frameon": False, "legend.fontsize": 8, "figure.dpi": 100, "savefig.dpi": 150})
FIGDIR = os.path.join(OUTDIR, "figs"); os.makedirs(FIGDIR, exist_ok=True)
def logx_ticks(ax, ticks):
    ax.set_xscale("log"); ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks]); ax.minorticks_off()
def savefig(fig, name):
    fig.savefig(os.path.join(FIGDIR, name + ".png"), facecolor=SURF, bbox_inches="tight")
def pband(ax, a, color, label=None):
    p5, p50, p95 = pct(a)
    ax.axvline(p50, color=color, lw=1.6); ax.axvspan(p5, p95, color=color, alpha=0.10, lw=0)
    return p5, p50, p95
def hist(ax, a, color, xlabel, bins=24):
    ax.hist(a, bins=bins, color=color, alpha=0.85, edgecolor=SURF, linewidth=1.0)
    p5, p50, p95 = pband(ax, a, INK)
    ax.set_xlabel(xlabel); ax.set_yticks([])
    ax.text(0.98, 0.95, "P5 %.3g\nP50 %.3g\nP95 %.3g" % (p5, p50, p95), transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color=INK2)

def cod_routing(F, des, g, y):
    N = des["N"]; Q = F["Q"]; v = g["v"]; J = {k: x * N for k, x in g["Jgas"].items()}
    nondeg = sum(v[k] for k in ("lig", "rc", "inert", "sI")) * Q
    degr = sum(v[k] for k in ("su", "aa", "fa", "pro", "ac", "ch", "pr", "li", "cel", "hem")) * Q
    bio = sum(v[k] for k in ("Xsu", "Xaa", "Xfa", "Xpro", "Xac", "Xh2", "Xsa", "Xsh")) * Q
    diss = (v["ch4"] + v["h2"] + 64 * v["IS"]) * Q
    return {"Metana (biogas)": 64 * J["ch4"], "H2S (reduksi sulfat)": 64 * J["h2s"] + 16 * J["h2"],
            "Biomassa mikroba": bio, "Terurai sebagian (belum habis)": degr, "Tak terurai (lignin, inert)": nondeg, "CH4/H2S terlarut": diss}

# ============================================================================
# 14. MAIN
# ============================================================================
def main():
    print("=" * 78); print(" POME + EFB CO-DIGESTION BIOGAS GENERATOR - MASS & ENERGY BALANCE"); print("=" * 78)
    print("stoichiometry element-balance residual (max over %d reactions): %.1e" % (len(STO), STO_MAXRES))
    print("molar volume %.3f Nm3/kmol | LHV(CH4) %.2f MJ/Nm3 (from dH_c) | N_MC=%d" % (VN, LHV_CH4_MJNM3, N_MC))
    TH0 = nominal_theta(); TH0["util"] = 1.0                                  # design basis = nameplate
    R = {}                                                                    # results container
    # ---------------------------------------------------------------- A. calibration
    print("\n[A] calibration to literature BMPs (POME 397, EFB 264 NmL CH4/gVS) ...")
    TH, bmp_fit = calibrate(TH0)
    tP, cP_ = bmp_test(TH, "pome"); tE_, cE_ = bmp_test(TH, "efb")
    R["calibration"] = dict(values={n: float(TH[n]) for n in ("k_li", "k_ch", "k_cel_ref", "beta_lig", "f_ref_pome")},
                            bmp_fit=bmp_fit, bmp_target=CAL_TARGETS)
    # ---------------------------------------------------------------- B. process decisions
    print("\n[B] process design decisions")
    share, ts95 = design_share_from_feed_risk(TH)
    TH["efb_share"] = share
    print("   EFB share to AD: %.1f %% of EFB (P95 blend TS = %.2f %%, limit %.1f %%)" % (share * 100, ts95 * 100, TH["TS_max"] * 100))
    sw_share = []
    for sh in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        F_ = build_feed(TH, share=sh, cap_ts=False); V_ = F_["Q"] * 20.0 / 5
        d_, y_, g_, ok_ = run_steady(TH, F_, 5, V_); J_ = g_["Jgas"]
        sw_share.append(dict(share=sh, TS=F_["TS"], ch4=J_["ch4"] * VN * 5, prod=J_["ch4"] * VN * 5 / (V_ * 5), efb_td=F_["M_efb"]))
    sw_dp = []
    for dp in (3, 5, 10, 15, 20, 30):
        t_ = dict(TH); t_["d_p_mm"] = dp; F_ = build_feed(t_, share=share); V_ = F_["Q"] * 20.0 / 5
        d_, y_, g_, ok_ = run_steady(t_, F_, 5, V_); ch4_ = g_["Jgas"]["ch4"] * VN * 5
        e_gain = ch4_ * LHV_KJMOL["CH4"] / (VN) / 3.6 * EQ["eta_el_nom"]            # kWh_e/d (LHV: kJ/kmol -> kWh)
        e_sh = F_["M_efb"] * shred_kWh_per_t_wet(dp)
        sw_dp.append(dict(dp=dp, ch4=ch4_, net=e_gain - e_sh, shred=e_sh))
    best = max(r["net"] for r in sw_dp)
    dp_sel = max(r["dp"] for r in sw_dp if r["net"] >= 0.99 * best)
    TH["d_p_mm"] = float(dp_sel)
    print("   shredder product size: %d mm (largest size within 1 %% of best net energy)" % dp_sel)
    F_nom = build_feed(TH, share=share)
    hrts = [40, 30, 24, 20, 18, 16, 14, 12, 10, 8, 6, 5, 4, 3]
    sw_hrt = hrt_sweep(TH, F_nom, hrts)
    HRT, hinfo = design_hrt(sw_hrt)
    print("   HRT sweep: washout HRT ~ %.0f d; %.0f %% of asymptotic CH4 reached at %.0f d; floor %.0f x washout = %.0f d -> design HRT %.0f d"
          % (hinfo["h_wash"], EQ["yield_frac"] * 100, hinfo["h_yield"], EQ["SF_wash"], hinfo["h_floor"], HRT))
    mod = choose_module(TH, share, HRT)
    N, Vm = mod["N"][45.0], mod["V_mod"]
    HRT_act = N * Vm / F_nom["Q"]
    print("   standard module: %.0f m3 liquid (D %.1f m) -> %s modules for 20/45/70 t FFB/h; base case N=%d, actual HRT %.1f d"
          % (Vm, mod["D"], "/".join(str(mod["N"][k]) for k in (20.0, 45.0, 70.0)), N, HRT_act))
    R["process_decisions"] = dict(efb_share=share, ts_p95=ts95, d_p_mm=dp_sel, hrt_design_d=HRT, hrt_info=hinfo, hrt_actual_d=HRT_act,
                                  module=mod, T_dig=TH["T_dig"], reactor="mesophilic CSTR, steel/GFS tank, double-membrane roof",
                                  sweeps=dict(share=sw_share, d_p=sw_dp, hrt=sw_hrt))
    # ---------------------------------------------------------------- C. nominal (design-basis) run
    print("\n[C] design-basis balance (45 t FFB/h x 20 h, EFB share %.0f %%)" % (share * 100))
    d_nom, y_nom, g_nom, ok_nom = run_steady(TH, F_nom, N, Vm)
    J_nom = {k: v * N for k, v in g_nom["Jgas"].items()}; gs_nom = gas_summary(J_nom)
    print("   steady state converged: %s | pH %.2f | VFA %.0f mg/L | FOS/TAC %.3f | TAN %.0f mg N/L | NH3 %.1f mg N/L"
          % (ok_nom, g_nom["pH"], g_nom["vfa_mgL"], g_nom["fos_tac"], g_nom["tan_mgN"], g_nom["nh3_mgN"]))
    print("   biogas %.0f Nm3/d (CH4 %.1f %%, raw H2S %.0f ppm) | CH4 %.0f Nm3/d | %.1f Nm3 biogas per m3 POME-equivalent"
          % (gs_nom["Nm3d"], gs_nom["y"]["ch4"] * 100, 1e6 * gs_nom["y"]["h2s"], J_nom["ch4"] * VN, gs_nom["Nm3d"] / F_nom["Qp"]))
    # ---------------------------------------------------------------- D. Monte Carlo (reactor level)
    print("\n[D] Monte Carlo (Latin hypercube, %d samples) ..." % N_MC)
    TH_mc = dict(TH); TH_mc["util"] = pmed("util")
    y_mc0 = run_steady(TH_mc, build_feed(TH_mc, share=share), N, Vm)[1]
    rec = mc_run(TH_mc, dict(N=N, V_mod=Vm, share=share), y_mc0, N_MC, rng)
    lhv95 = float(np.percentile([gas_train(r["J"], r["t"])["lhv_kW"] for r in rec], 95))
    bg95 = float(np.percentile([r["gs"]["Nm3d"] for r in rec], 95))
    chp = chp_select(lhv95)
    geo = tank_geometry(Vm, TH, bg95 / N)
    des = dict(N=N, V_mod=Vm, geo=geo, share=share, chp=chp)
    print("   P95 fuel %.0f kW -> CHP: %d x %.0f kWe (installed %.0f kWe) | P95 biogas %.0f Nm3/d -> flare %.0f Nm3/h"
          % (lhv95, chp["N_gen"], chp["P_unit"], chp["P_inst"], bg95, EQ["flare_margin"] * bg95 / 24.0))
    A, X = mc_arrays(rec, des, chp)
    upset_p = float(A["upset"].mean())
    print("   urea-N dosing needed (kg N/d): P50 %.0f | P95 %.0f ; NaOH P95 %.0f kg/d" % (np.percentile(A["doseN"], 50), np.percentile(A["doseN"], 95), np.percentile(A["dose"], 95) * 40.0))
    print("   probability of digester upset (pH<6.5 or FOS/TAC>0.4): %.1f %% | steady-state not reached in %.1f %% of runs"
          % (upset_p * 100, (1 - A["ok"].mean()) * 100))
    for k, lab in (("bg", "biogas Nm3/d"), ("ch4_frac", "CH4 fraction"), ("cod_rem", "COD removal"), ("P_gross", "gross kWe"), ("P_net", "net kWe"),
                   ("P_export", "export kWe"), ("share", "EFB share actually fed")):
        print("   %-24s P5 %9.3f  P50 %9.3f  P95 %9.3f" % (lab, *pct(A[k])))
    outs = ["bg", "P_net", "cod_conv", "fos", "tan"]
    sens = spearman_table(X, A, outs)
    # ---------------------------------------------------------------- E. final nominal balance with final equipment
    E_nom = plant_energy(F_nom, TH, des, J_nom, chp)
    S, chk, mtot = mass_balance(TH, F_nom, des, d_nom, y_nom, g_nom, E_nom)
    rows = stream_table(S)
    c = E_nom["chp"]; gt = E_nom["gt"]
    print("\n[E] plant energy balance (design basis)")
    print("   fuel %.0f kW(LHV) | CHP %d of %d units at %.0f %% load, eta_el %.1f %% | gross %.0f kWe | parasitic %.0f kWe (%.1f %%) | net %.0f kWe"
          % (gt["lhv_kW"], c["n_run"], chp["N_gen"], c["load"] * 100, c["eta_el"] * 100, E_nom["P_gross"], E_nom["P_par"], E_nom["P_par"] / E_nom["P_gross"] * 100, E_nom["P_net"]))
    print("   mill demand %.0f kW -> self-sufficiency %.0f %%, surplus %.0f kWe | heat: CHP %.0f kWth, digester %.0f kWth, export %.0f kWth | POME cooling %.0f kWth"
          % (E_nom["P_mill"], E_nom["self_suff"] * 100, E_nom["P_export"], E_nom["Q_heat_avail"], E_nom["Q_dig"], E_nom["Q_heat_export"], F_nom["Qcool_kW"]))
    print("   engine exhaust T from energy balance: %.0f C | fuel H2S %.0f ppm | CH4 in fuel %.1f %%" % (c["T_exh"], gt["h2s_ppm_fuel"], gt["ch4_frac_fuel"] * 100))
    print("   closure checks (relative error):  " + "  ".join("%s %.1e" % (k, v) for k, v in chk.items() if v is not None and k in
          ("digester_mass", "digester_C", "digester_H", "digester_O", "digester_N", "digester_S", "plant_mass", "chp_mass", "COD_digester")))
    # ---------------------------------------------------------------- F. emissions and economics
    v = g_nom["v"]; Qn = F_nom["Q"]
    bio_deg = Qn * ((1 - EQ["press_capture"]) * sum(v[k] for k in ("ch", "pr", "li", "cel", "hem")) + sum(v[k] for k in ("su", "aa", "fa", "pro", "ac")))
    em = emissions(TH, F_nom, des, g_nom, E_nom, bio_deg)
    ec = econ_screen(TH, des, chp, E_nom, em, g_nom)
    print("\n[F] methane avoidance (IPCC defaults): baseline %.0f tCO2e/y -> project %.0f -> avoided %.0f tCO2e/y" % (em["base_t"], em["proj_t"], em["avoided_t"]))
    print("    screening economics (placeholder unit costs): CAPEX %.2f MUSD | revenue %.2f MUSD/y | payback %.1f y | LCOE %.3f USD/kWh"
          % (ec["capex"] / 1e6, ec["revenue"] / 1e6, ec["payback"], ec["lcoe"]))
    # ---------------------------------------------------------------- G. tiers (scalability)
    tiers = {}
    for f in (20.0, 45.0, 70.0):
        t_ = dict(TH); t_["ffb_tph"] = f
        F_ = build_feed(t_, share=share); n_ = mod["N"][f]
        d_, y_, g_, ok_ = run_steady(t_, F_, n_, Vm); J_ = {k: x * n_ for k, x in g_["Jgas"].items()}
        gt_ = gas_train(J_, t_); chp_ = chp_select(gt_["lhv_kW"] * (lhv95 / gas_train(J_nom, TH)["lhv_kW"]))
        geo_ = tank_geometry(Vm, t_, gas_summary(J_)["Nm3d"] * (bg95 / gs_nom["Nm3d"]) / n_)
        E_ = plant_energy(F_, t_, dict(N=n_, V_mod=Vm, geo=geo_), J_, chp_)
        tiers[str(int(f))] = dict(ffb_tph=f, N_modules=n_, V_total=n_ * Vm, HRT=n_ * Vm / F_["Q"], biogas_Nm3d=gas_summary(J_)["Nm3d"], ch4_Nm3d=J_["ch4"] * VN,
                                  P_gross=E_["P_gross"], P_net=E_["P_net"], P_mill=E_["P_mill"], GWh_y=E_["P_net"] * 24 * t_["days_yr"] / 1e6,
                                  chp=chp_, EFB_td=F_["M_efb"], POME_m3d=F_["Qp"], Q_blend=F_["Q"])
    print("\n[G] tiers (same %.0f m3 module): " % Vm + " | ".join("%d t/h: %d mod, %.0f kWe net, %.1f GWh/y" % (k_, v_["N_modules"], v_["P_net"], v_["GWh_y"]) for k_, v_ in ((int(float(a)), b_) for a, b_ in tiers.items())))
    # ---------------------------------------------------------------- H. dynamics
    print("\n[H] start-up and annual dynamic simulation ...")
    TH_y = dict(TH); TH_y["util"] = pmed("util")
    su = startup_sim(TH, dict(N=N, V_mod=Vm, share=share), days=150.0)
    yr = year_sim(TH_y, des, chp, y_mc0, np.random.default_rng(SEED + 7))
    yr_GWh = float(np.sum(yr["P_net"]) * 24 / 1e6)
    print("   one-year simulation (seasonal + noise + 14 d shutdown): net %.2f GWh/y | min pH %.2f | max FOS/TAC %.2f | flared energy %.1f MWh"
          % (yr_GWh, yr["pH"].min(), yr["fos"].max(), yr["flare"].sum() * 24 / 1e3))
    # ---------------------------------------------------------------- I. export JSON
    cod_r = cod_routing(F_nom, des, g_nom, y_nom)
    equip = dict(
        digester_module=dict(count=N, V_liq_m3=Vm, D_m=geo["D"], H_liq_m=geo["H_liq"], H_wall_m=geo["H_wall"], roof_dome_h_m=geo["dome_h"],
                             V_gas_m3=geo["V_gas"], mixer_kW=geo["mixer_kW"], heat_loss_kW=geo["Q_loss_kW"], T_C=TH["T_dig"], material="baja / GFS, insulasi 100 mm, atap membran ganda"),
        blend_tank=dict(V_m3=F_nom["Q"] * 4.0 / 24.0, hold_h=4.0), efb_shredder=dict(cap_t_h=F_nom["M_efb"] / 20.0, power_kW=E_nom["P"]["shredder"], product_mm=dp_sel),
        pome_cooler=dict(duty_kW=F_nom["Qcool_kW"], T_in=TH["T_pome_in"], T_out=F_nom["T_p_out"]),
        feed_pump=dict(flow_m3_h=F_nom["Q"] / 24.0, head_m=EQ["H_feed"], kW=E_nom["P"]["feed_pumps"]),
        bio_desulfurizer=dict(gas_Nm3_h=gs_nom["Nm3d"] / 24.0, V_m3=gs_nom["Nm3d"] / 24.0 * EQ["ebct_s"] / 3600.0 * 1.0, eff=EQ["btf_eff"], air_Nm3_h=gt["n_air_btf"] * VN / 24.0),
        gas_chiller=dict(duty_kW=gt["Q_chill_kW"], T_C=EQ["chill_T"]), gas_blower=dict(flow_m3_h=gt["V_gas_actual_m3s"] * 3600.0, dP_kPa=EQ["blower_dP_kPa"], kW=gt["P_blow_kW"]),
        carbon_filter=dict(h2s_kg_d=gt["ac_h2s"] * MWG["h2s"], eff=EQ["ac_eff"]),
        flare=dict(cap_Nm3_h=EQ["flare_margin"] * bg95 / 24.0), chp=dict(N=chp["N_gen"], unit_kWe=chp["P_unit"], installed_kWe=chp["P_inst"], eta_el_nom=EQ["eta_el_nom"], fuel_P95_kW=lhv95),
        screw_press=dict(feed_m3_h=F_nom["Q"] / 24.0, cake_t_d=sum(S[19]["sp"].values()) / 1000.0 + S[19]["water"] / 1000.0, kW=E_nom["P"]["screw_press"]),
        cooling_tower=dict(duty_kW=E_nom["Q_cool"], kW=E_nom["P"]["cooling_tower"]),
        nutrient_dosing=dict(N_kg_d_nominal=g_nom["doseN"] * Vm * N * 14.007, N_kg_d_P95=float(np.percentile(A["doseN"], 95)), setpoint_mgN_L=TH["IN_sp"] * 14007.0),
        alkali_dosing=dict(NaOH_kg_d_P95=float(np.percentile(A["dose"], 95)) * 40.0))
    R.update(dict(
        meta=dict(title="Modular POME+EFB biogas generator - mass & energy balance", seed=SEED, N_MC=N_MC, quick=QUICK, runtime_s=time.time() - t_script0, sto_residual=STO_MAXRES),
        design_basis=dict(ffb_tph=TH["ffb_tph"], hrs_day=TH["hrs_day"], days_yr=TH["days_yr"], pome_m3d=F_nom["Qp"], efb_ad_td=F_nom["M_efb"], blend_m3d=F_nom["Q"], TS_blend=F_nom["TS"],
                          T_dig=TH["T_dig"], cod_blend=g_nom["cod_in"]),
        nominal=dict(pH=g_nom["pH"], vfa_mgL=g_nom["vfa_mgL"], fos_tac=g_nom["fos_tac"], tan_mgN=g_nom["tan_mgN"], biogas_Nm3d=gs_nom["Nm3d"], ch4_Nm3d=J_nom["ch4"] * VN,
                     ch4_frac=gs_nom["y"]["ch4"], h2s_ppm_raw=gt["h2s_ppm_raw"], h2s_ppm_fuel=gt["h2s_ppm_fuel"], cod_conv=64 * J_nom["ch4"] / (Qn * g_nom["cod_in"]), cod_routing_kgd=cod_r,
                     states={k: float(val) for k, val in zip(NAMES, y_nom)}),
        energy=dict(P_gross=E_nom["P_gross"], P_net=E_nom["P_net"], P_par=E_nom["P_par"], parasitic=E_nom["P"], P_mill=E_nom["P_mill"], P_export=E_nom["P_export"],
                    chp={k: (float(vv) if not isinstance(vv, dict) else vv) for k, vv in c.items()}, Q_heat_avail=E_nom["Q_heat_avail"], Q_dig=E_nom["Q_dig"],
                    Q_heat_export=E_nom["Q_heat_export"], Q_cool=E_nom["Q_cool"], fuel_kW=gt["lhv_kW"]),
        equipment=equip, streams=rows, closure=chk, tiers=tiers, emissions=em, economics_screen=ec,
        monte_carlo=dict(N=N_MC, upset_probability=upset_p, **{k: dict(zip(("P5", "P50", "P95"), pct(A[k]))) for k in
                         ("bg", "ch4", "ch4_frac", "cod_rem", "cod_conv", "P_gross", "P_net", "P_export", "pH", "fos", "tan", "nh3", "share", "TS", "h2s_ppm_raw", "load", "eta_el", "doseN")},
                         spearman=sens),
        year=dict(GWh_net=yr_GWh, min_pH=float(yr["pH"].min()), max_fos=float(yr["fos"].max()), monthly_net_MWh=[float(yr["P_net"][i:i + 30].sum() * 24 / 1e3) for i in range(0, 360, 30)]),
        assumptions={k: dict(value=(v_[0] if not isinstance(v_[0], np.ndarray) else v_[0].tolist()), dist=str(v_[1]), source=v_[2]) for k, v_ in PAR.items()},
        EQ={k: v_ for k, v_ in EQ.items() if not isinstance(v_, np.ndarray)}, EMIS=EMIS, ECON=ECON))
    with open(os.path.join(OUTDIR, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(R, fh, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else (o.tolist() if isinstance(o, np.ndarray) else str(o)))
    print("\nresults -> %s   (runtime %.0f s)" % (os.path.join(OUTDIR, "results.json"), time.time() - t_script0))
    make_figures(locals())
    return R

def make_figures(L):
    TH, F_nom, des, A, X, sens, sw_share, sw_dp, sw_hrt, hinfo, HRT = (L[k] for k in ("TH", "F_nom", "des", "A", "X", "sens", "sw_share", "sw_dp", "sw_hrt", "hinfo", "HRT"))
    E_nom, gt, c, chp, em, ec, tiers, su, yr, cod_r, mod, share = (L[k] for k in ("E_nom", "gt", "c", "chp", "em", "ec", "tiers", "su", "yr", "cod_r", "mod", "share"))
    # ---- Fig 1 feedstock model + uncertainty
    g0 = np.random.default_rng(SEED + 3); ths = draw_thetas(1500, dict(TH, util=pmed("util")), g0)
    Fs = [build_feed(t, share=share) for t in ths]
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.4)); ax = ax.ravel()
    hist(ax[0], np.array([f["Qp"] for f in Fs]), CC[0], "POME, m3/d"); ax[0].set_title("POME flow")
    hist(ax[1], np.array([t["cod_pome"] for t in ths]), CC[1], "POME COD, kg/m3"); ax[1].set_title("POME COD (lognormal, [LIT-S] 51)")
    hist(ax[2], np.array([f["TS"] for f in Fs]) * 100, CC[2], "blend TS, % wet"); ax[2].axvline(TH["TS_max"] * 100, color=CC[7], lw=1.6)
    ax[2].set_title("Blend TS at fixed EFB share"); ax[2].text(TH["TS_max"] * 100 - 0.05, ax[2].get_ylim()[1] * 0.55, "limit 8 %", color=CC[7], fontsize=8, ha="right")
    fp = np.array([t["fr_pome"] for t in ths]); fe = np.array([t["fr_efb"] for t in ths])
    bp = ax[3].boxplot(fp, patch_artist=True, showfliers=False, medianprops=dict(color=INK, lw=1.4)); ax[3].set_xticks(range(1, len(POME_KEYS) + 1)); ax[3].set_xticklabels(POME_KEYS)
    for b_ in bp["boxes"]: b_.set(facecolor=CC[0], alpha=0.5, edgecolor=CC[0])
    ax[3].set_title("POME COD fractions (logistic-normal)"); ax[3].set_ylabel("fraction of COD")
    bp = ax[4].boxplot(fe, patch_artist=True, showfliers=False, medianprops=dict(color=INK, lw=1.4)); ax[4].set_xticks(range(1, len(EFB_KEYS) + 1)); ax[4].set_xticklabels(EFB_KEYS)
    for b_ in bp["boxes"]: b_.set(facecolor=CC[1], alpha=0.5, edgecolor=CC[1])
    ax[4].set_title("EFB dry-basis composition"); ax[4].set_ylabel("mass fraction (dry)")
    hist(ax[5], np.array([f["M_efb"] for f in Fs]), CC[4], "EFB to AD, t/d"); ax[5].set_title("EFB fed (TS-capped)")
    fig.suptitle("Fig 1  Feedstock model and input uncertainty (n=1500, Latin hypercube)", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig1_feedstock")
    # ---- Fig 2 calibration / validation
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    for a_, sub, col, tg in ((ax[0], "pome", CC[0], CAL_TARGETS["pome"]), (ax[1], "efb", CC[1], CAL_TARGETS["efb"])):
        t_, cu = bmp_test(TH, sub); a_.plot(t_, cu, color=col); a_.scatter([30], [tg], color=INK, zorder=5, s=28); a_.text(30, tg, "  literature\n  %d" % tg, fontsize=8, va="top")
        a_.set_title("BMP, %s (model vs literature 30 d)" % sub.upper()); a_.set_xlabel("day"); a_.set_ylabel("NmL CH4 / g VS")
    ok_ = [r for r in sw_hrt if r["ph_ok"]]; ax[2].plot([r["hrt"] for r in ok_], [r["cod_conv"] * EQ_CH4_PER_COD() / r["cod_rem"] for r in ok_], color=CC[2], marker="o", ms=4)
    ax[2].axhline(0.34, color=INK, lw=1.0, ls="--"); ax[2].text(max(r["hrt"] for r in sw_hrt), 0.34, "literature POME CSTR 0.34 L/g COD removed ", ha="right", va="bottom", fontsize=7.5)
    logx_ticks(ax[2], [3, 5, 10, 20, 40]); ax[2].set_xlabel("HRT, d"); ax[2].set_ylabel("Nm3 CH4 / kg COD removed"); ax[2].set_ylim(0, 0.45); ax[2].set_title("CSTR methane yield vs HRT")
    fig.suptitle("Fig 2  Calibration targets and continuous-reactor check", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig2_calibration")
    # ---- Fig 3 process decisions
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.6)); ax = ax.ravel()
    ax[0].plot([r["share"] * 100 for r in sw_share], [r["ch4"] for r in sw_share], color=CC[0], marker="o", ms=4)
    ax[0].axvline(share * 100, color=INK, ls="--", lw=1); ax[0].set_title("Methane vs EFB share (HRT 20 d)"); ax[0].set_xlabel("EFB to AD, % of EFB"); ax[0].set_ylabel("Nm3 CH4/d")
    ax[1].plot([r["share"] * 100 for r in sw_share], [r["TS"] * 100 for r in sw_share], color=CC[1], marker="o", ms=4)
    ax[1].axhline(TH["TS_max"] * 100, color=CC[7], lw=1.4); ax[1].axvline(share * 100, color=INK, ls="--", lw=1); ax[1].set_title("Blend TS vs EFB share"); ax[1].set_xlabel("EFB to AD, % of EFB"); ax[1].set_ylabel("TS, % wet")
    ax[2].bar([str(r["dp"]) for r in sw_dp], [r["net"] / 1000 for r in sw_dp], color=CC[2], width=0.6); ax[2].set_title("Net energy vs shredder size"); ax[2].set_xlabel("product size, mm"); ax[2].set_ylabel("MWh_e/d (gas - shredding)")
    ax[2].set_ylim(min(r["net"] for r in sw_dp) / 1000 * 0.98, max(r["net"] for r in sw_dp) / 1000 * 1.01)
    sw = sorted(sw_hrt, key=lambda r: r["hrt"])
    ax[3].plot([r["hrt"] for r in sw], [r["ch4"] for r in sw], color=CC[0], marker="o", ms=4); ax[3].axvline(HRT, color=INK, ls="--", lw=1)
    ax[3].axvspan(0, hinfo["h_wash"], color=CC[7], alpha=0.12, lw=0); ax[3].text(hinfo["h_wash"] * 0.97, ax[3].get_ylim()[1] * 0.45, "washout ", rotation=90, color=CC[7], ha="right", fontsize=8)
    logx_ticks(ax[3], [3, 5, 10, 20, 40]); ax[3].set_title("Methane vs HRT"); ax[3].set_xlabel("HRT, d"); ax[3].set_ylabel("Nm3 CH4/d")
    ax[4].plot([r["hrt"] for r in sw], [max(r["fos"], 1e-3) for r in sw], color=CC[1], marker="o", ms=4); ax[4].axhline(0.4, color=CC[7], lw=1.2)
    ax[4].set_yscale("log"); logx_ticks(ax[4], [3, 5, 10, 20, 40]); ax[4].set_title("FOS/TAC vs HRT (limit 0.4)"); ax[4].set_xlabel("HRT, d"); ax[4].set_ylabel("VFA / alkalinity")
    ax[5].bar(["N=%d" % mod["N"][k] for k in (20.0, 45.0, 70.0)], [mod["N"][k] * mod["V_mod"] / 1000 for k in (20.0, 45.0, 70.0)], color=[CC[0], CC[1], CC[2]], width=0.55)
    for i, k in enumerate((20.0, 45.0, 70.0)): ax[5].text(i, mod["N"][k] * mod["V_mod"] / 1000, "%d t/h\n+%.0f%%" % (k, mod["over"][k] * 100), ha="center", va="bottom", fontsize=8)
    ax[5].set_title("Numbering up: one %.0f m3 module" % mod["V_mod"]); ax[5].set_ylabel("installed digester volume, 1000 m3"); ax[5].set_ylim(0, ax[5].get_ylim()[1] * 1.15)
    fig.suptitle("Fig 3  Process decisions: EFB share, shredder size, HRT, standard module", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig3_process_decisions")
    # ---- Fig 4 COD routing + start-up
    fig, ax = plt.subplots(2, 2, figsize=(12, 6.6)); ax = ax.ravel()
    tot = sum(cod_r.values()); ks = list(cod_r.keys())[::-1]
    ax[0].barh(ks, [cod_r[k] / 1000 for k in ks], color=[CC[3], CC[1], CC[4], CC[6], CC[7], CC[0]][::-1][: len(ks)] if False else CC[0], height=0.55)
    for i, k in enumerate(ks): ax[0].text(cod_r[k] / 1000, i, "  %.1f t/d (%.0f%%)" % (cod_r[k] / 1000, cod_r[k] / tot * 100), va="center", fontsize=8)
    ax[0].set_xlim(0, max(cod_r.values()) / 1000 * 1.35); ax[0].set_title("Where the COD goes (design basis, t COD/d)"); ax[0].set_xlabel("t COD/d")
    m_ = su["t"] >= 2; ax[1].plot(su["t"][m_], su["ch4"][m_], color=CC[0], label="CH4"); ax[1].plot(su["t"][m_], su["bg"][m_], color=CC[1], label="biogas"); ax[1].legend(); ax[1].set_title("Cold start-up from inoculum"); ax[1].set_xlabel("day"); ax[1].set_ylabel("Nm3/d")
    ax[2].plot(su["t"][m_], su["pH"][m_], color=CC[2]); ax[2].set_title("pH during start-up"); ax[2].set_xlabel("day"); ax[2].set_ylabel("pH")
    ax[3].plot(su["t"][m_], su["vfa"][m_], color=CC[7], label="VFA mg/L"); ax[3].plot(su["t"][m_], su["tan"][m_], color=CC[6], label="TAN mg N/L"); ax[3].legend(); ax[3].set_title("VFA and TAN during start-up"); ax[3].set_xlabel("day"); ax[3].set_ylabel("mg/L")
    fig.suptitle("Fig 4  Conversion pathways and dynamics", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig4_cod_dynamics")
    # ---- Fig 5 energy
    fig, ax = plt.subplots(2, 2, figsize=(12, 6.6)); ax = ax.ravel()
    fu = gt["lhv_kW"]; parts = [("electricity", c["P_el"]), ("jacket+oil heat", c["Q_jacket"]), ("exhaust heat recovered", c["Q_exh"]), ("stack loss", c["Q_stack"]), ("radiation", c["Q_rad"])]
    left = 0.0
    for i, (n_, v_) in enumerate(parts):
        ax[0].barh([0], [v_ / fu * 100], left=left, color=CC[i], height=0.5, edgecolor=SURF, linewidth=2, label="%s %.0f%%" % (n_, v_ / fu * 100)); left += v_ / fu * 100
    ax[0].set_yticks([]); ax[0].set_xlabel("%% of fuel LHV (%.0f kW)" % fu); ax[0].set_title("CHP energy split (load %.0f%%)" % (c["load"] * 100)); ax[0].legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.25))
    P = sorted(E_nom["P"].items(), key=lambda kv: kv[1]); ax[1].barh([k.replace("_", " ") for k, _ in P], [v for _, v in P], color=CC[0], height=0.55)
    for i, (k, v) in enumerate(P): ax[1].text(v, i, " %.0f" % v, va="center", fontsize=8)
    ax[1].set_title("Parasitic load, kWe (total %.0f)" % E_nom["P_par"]); ax[1].set_xlim(0, max(v for _, v in P) * 1.2)
    names = ["gross", "parasitic", "net", "mill demand", "surplus"]; vals = [E_nom["P_gross"], E_nom["P_par"], E_nom["P_net"], E_nom["P_mill"], E_nom["P_export"]]
    ax[2].bar(names, vals, color=[CC[0], CC[7], CC[2], CC[3], CC[4]], width=0.6)
    for i, v in enumerate(vals): ax[2].text(i, v, "%.0f" % v, ha="center", va="bottom", fontsize=8)
    ax[2].set_title("Electricity balance, kWe"); ax[2].set_ylim(0, max(vals) * 1.15)
    names = ["POME cooling\n(rejected)", "CHP heat\navailable", "digester\nheating", "heat to mill\n(export)"]; vals = [F_nom["Qcool_kW"], E_nom["Q_heat_avail"], E_nom["Q_dig"], E_nom["Q_heat_export"]]
    ax[3].bar(names, vals, color=[CC[6], CC[1], CC[7], CC[2]], width=0.6)
    for i, v in enumerate(vals): ax[3].text(i, v, "%.0f" % v, ha="center", va="bottom", fontsize=8)
    ax[3].set_title("Heat balance, kWth"); ax[3].set_ylim(0, max(vals) * 1.15)
    fig.suptitle("Fig 5  Plant energy balance (design basis)", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig5_energy")
    # ---- Fig 6 Monte Carlo
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.2)); ax = ax.ravel()
    for a_, k, col, lab, f_ in ((ax[0], "bg", CC[0], "biogas, Nm3/d", 1), (ax[1], "ch4_frac", CC[1], "CH4 in raw biogas, %", 100), (ax[2], "P_net", CC[2], "net electricity, kWe", 1),
                                (ax[3], "cod_rem", CC[3], "COD removal, fraction", 1), (ax[4], "fos", CC[7], "log10 FOS/TAC (stability limit: -0.4)", 1), (ax[5], "P_export", CC[6], "surplus after mill demand, kWe", 1)):
        hist(a_, (np.log10(np.maximum(A[k], 1e-4)) if k == "fos" else A[k] * f_), col, lab); a_.set_title(lab)
    fig.suptitle("Fig 6  Monte Carlo outputs (n=%d)  band = P5-P95, line = median;  upset probability %.1f %%" % (len(A["bg"]), A["upset"].mean() * 100), x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig6_montecarlo")
    # ---- Fig 7 sensitivity
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    for a_, o, ttl in ((ax[0], "bg", "Biogas flow"), (ax[1], "P_net", "Net electricity")):
        items = sorted(sens[o].items(), key=lambda kv: abs(kv[1]))[-10:]
        a_.barh([k for k, _ in items], [v for _, v in items], color=[CC[0] if v >= 0 else CC[1] for _, v in items], height=0.6); a_.axvline(0, color=INK, lw=0.8)
        a_.set_title("Spearman rank correlation: " + ttl); a_.set_xlabel("rho")
    fig.suptitle("Fig 7  Sensitivity (inputs ranked by |rho|)", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig7_sensitivity")
    # ---- Fig 8 year
    fig, ax = plt.subplots(3, 1, figsize=(12, 7.4), sharex=True)
    ax[0].plot(yr["day"], yr["bg"], color=CC[0]); ax[0].set_ylabel("biogas, Nm3/d"); ax[0].set_title("Annual dynamic simulation: seasonal FFB, daily noise, 14 d shutdown")
    ax[1].plot(yr["day"], yr["P_net"], color=CC[2], label="net electricity"); ax[1].plot(yr["day"], yr["P_mill"], color=CC[3], label="mill demand"); ax[1].legend(ncol=2, loc="lower right"); ax[1].set_ylabel("kW")
    ax[2].plot(yr["day"], yr["pH"], color=CC[1], label="pH"); ax[2].set_ylabel("pH"); ax[2].set_xlabel("day of year")
    fig.suptitle("Fig 8  One-year behaviour of the digester bank", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig8_year")
    # ---- Fig 9 tiers
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8)); kk = ["20", "45", "70"]
    ax[0].bar(kk, [tiers[k]["N_modules"] for k in kk], color=CC[0], width=0.55); ax[0].set_title("Modules (one standard size)"); ax[0].set_xlabel("mill size, t FFB/h")
    ax[1].bar(kk, [tiers[k]["P_net"] for k in kk], color=CC[2], width=0.55); ax[1].plot(kk, [tiers[k]["P_mill"] for k in kk], color=CC[3], marker="o", label="mill demand"); ax[1].legend(); ax[1].set_title("Net electricity, kWe")
    ax[2].bar(kk, [tiers[k]["GWh_y"] for k in kk], color=CC[1], width=0.55); ax[2].set_title("Net energy, GWh/y (300 d)")
    for a_ in ax: a_.set_xlabel("mill size, t FFB/h")
    fig.suptitle("Fig 9  Scalability: numbering up", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); savefig(fig, "fig9_tiers")
    plt.show()

def EQ_CH4_PER_COD():                    # Nm3 CH4 per kg COD (stoichiometric, from ideal-gas molar volume and CH4 COD)
    return VN / SPX["ch4"].cod

if not NO_MAIN:
    RESULTS = main()
