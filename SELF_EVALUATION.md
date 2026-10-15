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


---
# Rev 1 self-evaluation (portable thermophilic AnMBR + new PFD)

## What changed
| Finding (Rev 0) | Action (Rev 1) |
|---|---|
| Rev 0 was "a kit of modules", but 2,000 m3 field-built digesters are not a portable product | The process was changed to a **thermophilic (55 C) anaerobic membrane bioreactor (AnMBR) on POME**. Membrane solids retention (SRT 12 d, HRT 4.6 d) plus thermophilic kinetics give 2,632 m3 instead of 14,023 m3. **One standard road-transportable vessel (D 4.2 m x 15.2 m, 194 m3)** is used for every reactor and tank: 10 / 14 / 19 reactors for 30 / 45 / 60 t FFB/h. Everything else ships in containers or skids. The total is 28 truck loads and the plot is about 0.16 ha. |
| EFB (32 % lignin) set most of the Rev 0 reactor volume | EFB was dropped from the portable product; it stays with the mill as mulch or boiler fuel. |
| POME is hot (85 C) and Rev 0 cooled it to 38 C and then reheated | At 55 C the plant needs **no heating**; it only cools the feed, and the feed's residual heat covers reactor losses. |
| The Rev 0 PFD carried the stream table and had little instrumentation | PFD-BG-002 Rev 1 changes: no table; EPC callout strip; stream tags (No./T/P); 22 ISA-5.1 loops, including level control on every vessel; module boundaries PM-1..PM-10; scale table for 30/45/60 t/h. The automatic overlap checker reports 0 issues. |

## Remaining weaknesses
1. **Thermophilic AnMBR parameters are literature-typical, not measured.** These include the thermophilic ADM1 ratios, a membrane flux of 15 LMH, 1.5 kWh/m3 and the 35 g/L solids limit. **A pilot AnMBR on real POME is the key validation step.**
2. **Net power about equals the mill's own demand** (961 vs 945 kWe). The product displaces diesel or grid power and earns methane credits; it does not export.
3. **Waste-sludge flow is large** (226 m3/d at 2-3 % solids). A screw press handles it, but cake disposal needs a plan; land application to the estate is assumed.
4. **Membrane fouling and cleaning chemicals are not modelled**; CIP is drawn but not costed in detail.
5. **Economics are a placeholder screen** (6.1 MUSD, about 6 y payback).
