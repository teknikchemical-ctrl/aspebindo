# Self-evaluation (Phase 1 balance + Phase 2 PFD)

Written by the assistant after reviewing its own work. Dates: 2026-10-15.

## What was wrong or missing, and what was done
| Finding | Severity | Action |
|---|---|---|
| **The Phase-1 digester (2,000 m3, D 16.7 m, field-erected) was not a *portable module*.** A mill needs 14,000 m3 of digestion; no single unit of that size can be moved. | High (misses the product requirement) | Redefined the product as a **kit of ISO-transportable modules** PM-A..PM-F (`process/portable_modules.py`): 23 ISO-sized units, ~274 t for a 45 t FFB/h plant. Digesters ship as flat-pack bolted panels. The PFD draws the module boundaries. |
| Nitrogen starvation in 3 % of Monte-Carlo draws (EFB is N-poor) | Medium | Urea-N dosing loop added (set-point 100 mg N/L); upsets 3.2 % -> 0 %. |
| Dead variables, one broken reference found by static analysis | Low | Removed; `pyflakes` clean. |
| Results depend on the random seed? | Check | Three seeds: net power P50 1,281-1,288 kWe, upset probability 0 % each. Stable. |
| DXF with white fills hid line work on a dark CAD background | Low | Fills dropped from the DXF (PDF keeps them). |

## Known weaknesses (not fixed - need data or a decision)
1. **Not literally portable digestion.** If a single-container digester is required, only micro-scale (<~10 m3/d feed) works, or a different technology (high-rate UASB/EGSB for POME only; dry garage digesters for EFB). That is a separate product.
2. **Washout HRT of ~4 d is optimistic.** ADM1 defaults give Methanosarcina-like rates; real POME digesters acidify sooner. The 4x safety factor (design HRT 20 d) is a judgment, not a measured value.
3. **EFB hydrolysis is constrained by one literature BMP.** k_cel_ref and lignin shielding are only identifiable together; either could be wrong in continuous operation.
4. **Sulfide inhibition, SRB kinetics, part-load engine curve, cooling and heat-exchanger figures are assumptions** (tagged `[ASSUME]` in `results.json`).
5. **Economics use placeholder unit costs.** Payback ~7.8 y and 0.155 USD/kWh are not decision-grade.
6. **Heat is abundant and mostly unused**: 2.1 MWth hot water against a mill that has little use for it, plus 1.3 MWth of POME cooling load rejected.
7. **Full EFB co-digestion in CSTRs at this scale has pilot, not commercial, precedent.** POME-only CHP is the proven reference.
8. PFD: team name, university and date in the title block are placeholders (`TEAM`, `UNIV` in `pfd/pfd_biogas.py`). Instrument loops (10) are representative, not a full control philosophy. The DXF carries no fills, so it looks cleaner on screen than the PDF.
