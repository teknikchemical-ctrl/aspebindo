# PFD Engine (eng.py)

A standalone 2D drafting engine, in Python, for Process Flow Diagrams (PFD) /
process schematics — built around the ReportLab PDF canvas. This is the base
layer that the separate "Kiln Drawing Engine" (ASME mechanical drafting) was
built on top of; it also works entirely on its own for drawing PFDs.

Verified working in this package (standalone smoke test, see `example/`).

## What it gives you

- `eng.Doc` — a drawing canvas object. All drawing happens on an instance of it.
- ~50 pre-built equipment symbols via `Doc.eq(kind, tag, x, y, w, h, ...)`:
  vessel, agit, tank, ctank, column, thick, cyclone, hydrocyclone, bag, esp,
  mill, kiln, drum, dryer, boiler, fboiler, hx, hxc, reboiler, pump, fan,
  comp, bfilter, press, centr, evap, cryst, stack, silo, hopper, feeder,
  wfeeder, conv, elev, stock, screw, pugmill, hims, vrm, hgg, pulv,
  classifier, mixsettle, ct, deaer, box, wtp, prv, n2pk, kcomp, manifold,
  diverter, granul, splitter, storage, quench, valve.
- Orthogonal stream routing between equipment nozzles: `Doc.conn(key, a, b, ...)`,
  with automatic line-crossing gaps, arrows, and flow-number diamonds.
- Boundary flags (feed/product in/out of battery limits): `Doc.flag(...)`.
- Primitives: `line`, `poly`, `rect`, `circ`, `arc`, `text` (with automatic
  chemical-formula subscripting, e.g. "SO2" -> "SO₂").
- `Doc.finalize()` — must be called once, after all `conn()` calls and before
  `Doc.pdf()`, to compute line-crossing breaks and draw arrowheads.
- `Doc.pdf(path)` — writes the finished page to a PDF file (A2 by default,
  `W,H` module constants control page size in the same units as coordinates).

## Dependencies

- Python 3
- `reportlab` (`pip install reportlab`)
- Nothing else — no CAD kernel needed for this layer (that's only required
  by the separate Kiln Drawing Engine, for 3D-derived mechanical views).

## Quick start

```bash
cd pfd_engine
python3 example/contoh_pfd_minimal.py
```

This regenerates `example/contoh_pfd_minimal.pdf` — a two-equipment PFD
(a vessel feeding a pump) with a routed, numbered stream and a boundary flag,
confirmed to render correctly.

```python
import eng

d = eng.Doc()
d.eq('vessel', 'V-101', 20, 30, 20, 40)
d.eq('pump',   'P-101', 60, 20, 8, 8)
d.conn('1', 'V-101.b', 'P-101.l', num=1)   # nozzle refs: 'TAG.side' (l/r/t/b)
d.flag('UMPAN', 5, 50, d='r', kind='in')
d.text(10, 80, 'CONTOH PFD MINIMAL', 4, 'l', True)
d.finalize()
d.pdf('out.pdf')
```

## Known rough edges

- API is terse/unlabeled (Indonesian internal naming in places) — it was
  written as an internal tool, not a published library. Read the symbol
  list and `Doc` method signatures directly in `eng.py` for the full surface
  area; the methods above are the ones exercised in this package's example.
- No built-in overlap/neatness checker in this layer (that logic — the
  zero-overlap "kerapihan" checker, auto-placement, GD&T, etc. — lives in
  the separate Kiln Drawing Engine package, `kd.py`, which wraps this one).
- This engine was tested here with a minimal 2-equipment example only; it
  was exercised more heavily (dozens of symbols, many streams) inside the
  kiln project historically, but that usage went through the ASME wrapper
  layer, not through this engine directly.
