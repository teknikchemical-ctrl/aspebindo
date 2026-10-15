# -*- coding: utf-8 -*-
"""
Slide pendamping PFD Rev 3: TABEL ALIRAN (16:9, 480 x 270 mm), dibaca dari ../process/outputs/results.json.
Kolom: No | Aliran | Dari -> Ke | Fasa | T | P | Laju | komposisi utama (gas: %-mol, cair/padat: %-massa).
Keluaran: outputs/PFD_BG-002_Rev3_streams.pdf / .png.  Jalankan: python3 pfd_streams.py
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eng
from eng import Doc

W, H = 480.0, 270.0
eng.W, eng.H = W, H
eng.DOC_TITLE = "Tabel Aliran PFD Generator Biogas Portabel"; eng.DOC_AUTHOR = "NAMA TIM"
R = json.load(open(os.path.join(HERE, "..", "process", "outputs", "results.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "outputs")
d = Doc()

def idn(x, dec=0):
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
def tc(x, y, t, size=2.2, anchor='l', bold=False): d.text(x, y, t, size, anchor, bold, layer='table', chk=False)

ROUTE = {1: ("PKS", "SC-101"), 2: ("SC/HC-101", "PKS (TKKS)"), 3: ("HC-101", "E-101"), 4: ("E-101", "TK-101"), 5: ("P-203", "header umpan"),
         6: ("P-204", "header umpan"), 7: ("P-201", "R-201..2%02d" % R["equipment"]["reactor_vessel"]["count"]), 8: ("Reaktor", "MB-301"),
         9: ("MB-301", "Reaktor"), 10: ("MB-301", "TK-301"), 11: ("Reaktor", "PR-501"), 12: ("PR-501", "Kebun"), 13: ("PR-501", "TK-301"),
         14: ("TK-301", "Kolam polishing"), 15: ("Reaktor", "GH-301"), 16: ("GH-301", "BTF-301"), 17: ("K-301", "BTF-301"),
         18: ("BTF-301", "HX-301"), 19: ("BTF-301", "IPAL"), 20: ("V-301", "IPAL"), 21: ("AC-301", "GE-401/402"), 22: ("Header gas", "FL-301"),
         23: ("Udara", "GE-401/402"), 24: ("HX-401", "ST-401"), 25: ("AC-301", "TPS limbah"), 26: ("Tangki polimer", "PR-501")}
SN = {1: "POME mentah", 2: "Residu saringan + pasir", 3: "POME bebas pasir", 4: "POME didinginkan", 5: "Larutan NaOH", 6: "Urea-N",
      7: "Umpan reaktor", 8: "Lumpur ke membran", 9: "Retentat", 10: "Permeat", 11: "Lumpur buangan", 12: "Kue lumpur", 13: "Filtrat",
      14: "Efluen akhir", 15: "Biogas mentah", 16: "Biogas ke BTF", 17: "Udara BTF", 18: "Biogas keluar BTF", 19: "Blowdown BTF",
      20: "Kondensat", 21: "Biogas bersih ke genset", 22: "Gas ke flare", 23: "Udara bakar", 24: "Gas buang", 25: "Karbon jenuh", 26: "Polimer"}
OVR = {5: "NaOH (sbg 100 %), dosis otomatis AIC-202; 0 pada titik rancangan, maks. = P95 MC", 6: "Urea, dosis otomatis AIC-203; 0 pada titik rancangan, maks. = P95 MC", 22: "Komposisi sama dengan aliran 21 (hanya saat GE berhenti)",
       25: "Karbon aktif jenuh belerang (diganti berkala)", 26: "Polimer kationik (flokulan)"}
FLW = {5: "0 \u2013 %s" % idn(R["equipment"]["alkali_dosing"]["NaOH_kg_d_P95"] / 24, 1),
       6: "0 \u2013 %s" % idn(R["equipment"]["nutrient_dosing"]["N_kg_d_P95"] * 60.06 / 28.01 / 24, 1)}
FASA = {'C': "Cair", 'G': "Gas", 'P': "Padat", 'PB': "Padat basah", 'CP': "Cair-padat", 'B': "Bubur"}
GL = dict(water="Air", carb="Karbohidrat", lignin="Lignin", protbio="Protein/biomassa", lipid="Minyak/LCFA", solorg="Organik terlarut",
          inertp="Inert partikulat", mineral="Mineral", tan="NH\u2083", sulf="Sulfat/sulfida", ic="CO\u2082 terlarut", dgas="CH\u2084 terlarut",
          g_ch4="CH\u2084", g_co2="CO\u2082", g_h2="H\u2082", g_h2s="H\u2082S", g_h2o="H\u2082O", g_n2="N\u2082", g_o2="O\u2082", g_so2="SO\u2082",
          sulfur="Belerang", chem="Bahan kimia")
MW = dict(g_ch4=16.04, g_co2=44.01, g_h2=2.016, g_h2s=34.08, g_h2o=18.015, g_n2=28.01, g_o2=32.0, g_so2=64.07)

def comp_text(s):
    c = {k: v for k, v in s["comp"].items() if v > 0}
    if not c: return "\u2013"
    if s["ph"] == 'G' and all(k in MW for k in c):
        n = {k: v / MW[k] for k, v in c.items()}; tot = sum(n.values()); unit = "%-mol"
        fr = {k: v / tot for k, v in n.items()}
    else:
        tot = sum(c.values()); unit = "%-massa"; fr = {k: v / tot for k, v in c.items()}
    top = sorted(fr.items(), key=lambda kv: -kv[1])[:4]
    parts = []
    for k, f in top:
        if k == 'g_h2s' and unit == "%-mol" and f < .01: parts.append("H\u2082S %s ppm" % idn(f * 1e6))
        elif f >= .001: parts.append("%s %s" % (GL[k], idn(f * 100, 1 if f < .995 else 1)))
    if unit == "%-mol" and 'g_h2s' in fr and 'g_h2s' not in dict(top):
        parts.append("H\u2082S %s ppm" % idn(fr['g_h2s'] * 1e6))
    return "; ".join(parts) + "  (" + unit + ")"

def main():
    d.rect(3, 3, W - 6, H - 6, .3, None, 'frame'); d.rect(5, 5, W - 10, H - 10, .7, None, 'frame')
    tc(12, 15.5, "TABEL ALIRAN \u2013 PFD-BG-002 Rev. 3", 4.6, 'l', True)
    tc(12, 21.5, "Generator biogas portabel AnMBR 55 \u00b0C, PKS 45 t TBS/jam \u00d7 20 jam/hari; laju rata-rata harian dari neraca massa kinetik (biogas_balance.py)", 2.4)
    cols = [(13, "No.", 'm'), (21, "Aliran", 'l'), (83, "Dari \u2192 Ke", 'l'), (152, "Fasa", 'l'), (196, "T, \u00b0C", 'r'), (220, "P, bar", 'r'),
            (253, "Laju, kg/jam", 'r'), (260, "Komposisi utama", 'l')]
    y0 = 27.5; hh = 7.5; ids = sorted(int(s["id"]) for s in R["streams"]); STR = {int(s["id"]): s for s in R["streams"]}
    rh = (H - 22 - y0 - hh) / len(ids)
    d.rect(8, y0, W - 16, hh, .0, '#e6e6e6', 'table')
    for x, t, a in cols: tc(x, y0 + 5.1, t, 3.1, a, True)
    d.line([(8, y0 + hh), (W - 8, y0 + hh)], .45, None, '#000000', 'table')
    for k, i in enumerate(ids):
        s = STR[i]; y = y0 + hh + rh * k
        if k % 2: d.rect(8, y, W - 16, rh, .0, '#f3f3f3', 'table')
        yy = y + rh * .68
        v = [str(i), SN[i], "%s \u2192 %s" % ROUTE[i], FASA.get(s["ph"], s["ph"]), idn(s["T"]), idn(s["P"], 2),
             FLW[i] if i in FLW else idn(s["kg_h"]) if s["kg_h"] >= 10 else (idn(s["kg_h"], 1) if s["kg_h"] >= .05 else "0"), OVR.get(i) or comp_text(s)]
        for (x, _, a), t in zip(cols, v): tc(x, yy, t, 3.0, a, a == 'm' or x == 21)
    yb = y0 + hh + rh * len(ids)
    d.rect(8, y0, W - 16, yb - y0, .5, None, 'table')
    for x in (18, 80, 149, 175, 200, 224, 257): d.line([(x, y0), (x, yb)], .15, None, '#000000', 'table')
    cl = R["closure"]
    tc(10, yb + 5.0, "Galat neraca massa pabrik %s; neraca unsur reaktor C/H/O/N/S < %s. Aliran 22 nol pada operasi normal; aliran 25 berkala. "
       "Komposisi gas dalam %%-mol, cair/padat dalam %%-massa." % ("%.1e" % abs(cl["plant_mass"]),
       "%.0e" % max(abs(cl["reactor_" + e]) for e in "CHONS")), 2.2)
    tc(10, yb + 10.2, "Ketidakpastian (Monte Carlo 400 sampel): biogas P5/P50/P95 = %s / %s / %s Nm³/hari; daya neto %s / %s / %s kWe." % (
        tuple(idn(R["monte_carlo"]["bg"][q]) for q in ("P5", "P50", "P95")) + tuple(idn(R["monte_carlo"]["P_net"][q]) for q in ("P5", "P50", "P95"))), 2.2)
    d.finalize()
    d.pdf(os.path.join(OUT, "PFD_BG-002_Rev3_streams.pdf"))

if __name__ == "__main__":
    main()
