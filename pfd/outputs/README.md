# PFD deliverables - Portable thermophilic AnMBR biogas generator (EIC 2026)

| File | Use |
|---|---|
| `PFD_BG-002_Rev3_slides.pptx` | 2 slides (16:9) ready for the deck: slide 1 PFD, slide 2 stream table |
| `PFD_BG-002_Rev3_deck.png` / `.pdf` / `.svg` | PFD, deck edition (480 x 270 mm, 16:9), 300 dpi PNG for PowerPoint, vector PDF/SVG |
| `PFD_BG-002_Rev3_deck.dxf` | Same drawing for AutoCAD (layers PFD-PROSES, PFD-UTILITAS, PFD-SINYAL, PFD-PERALATAN, PFD-INSTRUMEN, PFD-TEKS, ...) |
| `PFD_BG-002_Rev3_streams.png` / `.pdf` | Stream table: no., route, phase, T, P, flow, main composition (from results.json) |
| `PFD_BG-002_Rev2.pdf` / `.dxf` / `.svg` | Full A2 engineering sheet (larger instrument set, stream conditions, loop table) |
| Rev 0 / Rev 1 files | Archive only (superseded) |

Content of Rev 3: 35 equipment tags (about 65 physical units), 26 numbered streams, 20 ISA-5.1 loops with level control on every vessel
(TK-101, reactors, TK-301, TK-302, dosing tanks, gas holder, BTF sump, KO pot, cooling-tower basin), utility lines (CWS/CWR, CHWS/CHWR, HWS/HWR, PW, power),
portable-module boundaries PM-1..PM-10, symbols per ISO 10628-2. Blowers K-301/K-302: suction enters vertically at top-left, discharge leaves vertically at bottom-right.

Regenerate: `python3 pfd_deck.py`, `python3 pfd_streams.py` (team name: edit `TEAM`/`UNIV` at the top of `pfd_deck.py`).
