# -*- coding: utf-8 -*-
"""Gerbang konsistensi (Tahap 4): angka kunci harus sama di neraca proses, modul, GA 3D, lokasi, keuangan, Excel, laporan dan gambar;
istilah Rev 1 yang usang (AnMBR sebagai kasus dasar, 14 reaktor, 800 kWe, 0,34 ha, 6,17 GWh) tidak boleh muncul di keluaran.
Jalankan: python3 consistency_check.py   -> kode keluar 0 bila lolos."""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
J = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
R = J("process/outputs/results.json"); PM = J("process/outputs/portable_modules.json"); GA = J("cad/out/ga.json")
SITE = J("cad/out/site.json"); SUM = J("finance/outputs/summary.json")
sys.path.insert(0, os.path.join(ROOT, "finance")); os.chdir(os.path.join(ROOT, "finance"))
import fin_core as F
fails, rows = [], []
def chk(name, a, b, tol=1e-6, rel=True):
    ok = abs(a - b) <= (tol * max(abs(a), abs(b), 1e-12) if rel else tol)
    rows.append((name, a, b, ok)); (None if ok else fails.append(name))
eq = R["equipment"]
chk("Jumlah reaktor: proses vs modul", eq["reactor_vessel"]["count"], [m for m in PM["modules"] if m["id"] == "PM-3"][0]["qty"])
chk("Jumlah reaktor: proses vs keuangan", eq["reactor_vessel"]["count"], F.TECH["n_vessel"])
chk("Volume tangki: proses vs keuangan", eq["reactor_vessel"]["V_liq_m3"], F.TECH["V_tank"])
chk("CHP terpasang: proses vs keuangan", eq["chp"]["installed_kWe"], F.TECH["chp_kWe"])
chk("Energi neto tahunan: proses vs keuangan", R["year"]["GWh_net"], F.TECH["E_year_GWh"])
chk("Plot: GA 3D vs modul", GA["plot_m2"], PM["plot_area_m2_estimate"]["total"])
chk("Plot: GA 3D vs keuangan (sewa lahan)", GA["plot_m2"], F.TECH["plot_m2"])
chk("Rute lokasi: site.json vs CAPEX", SITE["interconnect_cost"], sum(c for _, _, _, c in F.TECH["site_lines"]), 1e-3)
o = F.run()
chk("NPV: keuangan vs summary.json", o["NPV"], SUM["NPV"], 1e-9)
chk("ER karbon: keuangan vs summary", o["ER"], SUM["ER_t"], 1e-9)
chk("Energi th-3 = E_tahun x util/util_proses x avail", o["E"][3], R["year"]["GWh_net"] * o["v"]["util"] / R["year"]["util"] * o["v"]["avail"], 1e-9)
chk("Semua jarak aman lokasi OK", sum(1 for c in SITE["safety"] if c["ok"]), len(SITE["safety"]), 0, False)
# Excel cache = Python (nilai yang tersimpan di buku kerja)
import openpyxl
ws = openpyxl.load_workbook(os.path.join(ROOT, "finance/outputs/BG_Model_Keuangan.xlsx"), data_only=True)["Indikator"]
chk("Excel NPV (cache) = Python", ws["B4"].value, o["NPV"], 1e-6)
# istilah usang dalam teks keluaran
STALE = [(r"14 reaktor|R-214|14 x 194|x 14 ", "14 reaktor Rev 1"), (r"Kontainer CHP 800 kWe|Genset 2 x 800 kWe|kontainer 2 x 800", "CHP 800 kWe Rev 1 pada 45 t/jam"), (r"6[,.]17 GWh", "energi Rev 1"),
         (r"0[,.]34 ha", "plot Rev 1"), (r"Generator Biogas Portabel AnMBR|AnMBR termofilik portabel|Reaktor AnMBR", "AnMBR sebagai kasus dasar")]
def text_of(p):
    if p.endswith(".pdf"): return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    return open(p, encoding="utf-8").read()
FILES = ["finance/outputs/BG_Analisis_Ekonomi.pdf", "cad/drawings/out/BG_drawing_set_A3.pdf", "pfd/outputs/PFD_BG-002_Rev3.pdf", "process/PROCESS_DESIGN_BASIS.md",
         "cad/out/BG_3D_renders.pdf"]
for f in FILES:
    t = text_of(os.path.join(ROOT, f))
    for pat, why in STALE:
        hits = re.findall(pat, t)
        if hits: fails.append("%s: %s (%s)" % (f, why, hits[0]))
    rows.append(("Istilah usang di " + f, 0, 0, not any(re.search(p_, t) for p_, _ in STALE)))
w = max(len(r[0]) for r in rows)
for n, a, b, ok in rows: print("%-*s  %-14s %-14s %s" % (w, n, ("%.6g" % a) if isinstance(a, (int, float)) else a, ("%.6g" % b) if isinstance(b, (int, float)) else b, "OK" if ok else "GAGAL"))
print("\n%d pemeriksaan, %d gagal" % (len(rows), len(fails)))
for f in fails: print("  - " + f)
sys.exit(1 if fails else 0)
