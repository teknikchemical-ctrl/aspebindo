# Engineering Drawing Engine (kd.py + sym.py + vw.py)

A Python CAD-drafting engine that produces ASME Y14.5-style mechanical
engineering drawings as PDF (A3), from 3D CadQuery solid models. Originally
built for an R-01 Rotary Kiln drawing set (team "Lagi Pengen", UGM, MnMs
Week 2026, EF slag Route B SO2 sulfation) — included under `sheets/` as a
fully worked, verified example of real multi-sheet usage.

This engine is layered on top of the separate PFD Engine (`eng.py`, bundled
here as a dependency) — `eng.Doc` is the drawing canvas; `kd.py` adds 3D
projection (hidden-line removal, sections, isometrics via CadQuery/OCP),
ASME dimensioning, GD&T feature-control frames, title blocks/revision
blocks, balloons, and — the key feature — a strict zero-overlap "neatness"
checker with automatic collision-free placement for every dimension,
leader, balloon and FCF it draws.

Verified in this package: all 10 sheets rebuild clean (`ISU = 0` — zero
checker issues) from this exact packaged copy. See
`sample_output/R01_full_set_sample.pdf` (10-page A3 merged set) as proof.

## What it gives you

- `models.py` — CadQuery solid-model builders for each kiln component
  (shell, tyre, roller, girth gear, pinion, seal, station, main assembly).
  This file is project-specific; for a new project you'd write an
  equivalent module of your own solids.
- `eng.py` — base PFD/drafting canvas (see the separate `pfd_engine`
  package for its own documentation; it's duplicated here so this package
  is self-contained).
- `kd.py` — the core: 3D->2D view projection (`View` in `vw.py` wraps this),
  dimension primitives (`dim_h`, `dim_v`, `angdim`, `cl` centerlines),
  automatic collision-free placement (`auto_leader`, `auto_fcf`,
  `auto_balloon`, `auto_surf`, `auto_nz`), solid-body exclusion zones
  (`solid_profile`/`SOLIDS`) so text can't land inside a part's silhouette,
  `OPEN_VIEWS` for views where annotation legitimately belongs inside the
  view's own envelope, and the `check()` neatness checker (7 rule classes:
  text-text, text-line, forbidden-zone, leader/dimension crossings, balloon
  spacing, view/zone overlap, minimum letter height).
- `sym.py` — GD&T symbols: `fcf` (feature control frame), `fcf_under` /
  `auto_leader_fcf` (FCF attached directly beneath a size dimension, the
  ASME 6.4.1 pattern), `cutplane` / `cutplane_h` (ASME Y14.3 cutting
  planes), `vlabel`, `angdim`.
- `sh.py` — title block + two-row revision block (A3 sheet frame).
- `kt.py` — bill-of-materials / nozzle-list table renderer.
- `cadview.py`, `gearg.py` — supporting geometry helpers (gear tooth
  outline generation, CAD view utilities).
- `common.py` — the `finish(name)` entry point every sheet script calls at
  the end: runs the checker, writes `{name}.pdf`, and if any issues remain,
  also writes a red-highlighted `{name}_chk.pdf` overlay for debugging.

## Dependencies

- Python 3
- `reportlab`
- `cadquery` (pulls in OCP/OpenCASCADE — this is the heavy dependency;
  `pip install cadquery` can take a while and needs a working C++ toolchain
  on some platforms. On Linux, `pip install cadquery` from PyPI wheels
  usually just works.)
- `numpy`

```bash
pip install reportlab cadquery numpy
```

## Quick start — rebuild the example kiln sheets

```bash
cd kiln_drawing_engine/sheets
PYTHONPATH=.. python3 s01_rakitan.py   # writes s01.pdf in this folder; prints "s01 ISU = 0"
```

Run all ten and merge (requires `pdfunite` from poppler-utils, or substitute
any PDF merge tool):

```bash
cd kiln_drawing_engine/sheets
for f in s01_rakitan s02_stasiun s03_cangkang s04_ban s05_bar s06_rol s07_poros s08_gear s09_pinion s10_segel; do
  PYTHONPATH=.. python3 "$f.py"
done
pdfunite s01.pdf s02.pdf s03.pdf s04.pdf s05.pdf s06.pdf s07.pdf s08.pdf s09.pdf s10.pdf full_set.pdf
```

Each script prints `ISU = N` — the checker issue count. `0` means clean;
anything else means the script also wrote a `*_chk.pdf` with red overlays
marking exactly what overlaps or is out of place, for debugging.

## Starting a new project with this engine

1. Write your own `models.py`-equivalent: CadQuery solids for your parts,
   parametrized in mm.
2. Write a sheet script per drawing, following the pattern in `sheets/*.py`:
   call `sh.frame(...)` for the title block, build `View` objects for each
   projection you need (`View(direction, up, scale, x, y, name=...)`,
   `.draw()` / `.section()` / `.iso()`), add dimensions/leaders/balloons/FCFs
   using the `auto_*` placement functions so the checker keeps you honest,
   and end with `finish('sheet_name')`.
3. Re-run until every sheet prints `ISU = 0`.

## Known rough edges / things to know before extending it

- The `auto_*` placement functions work by scoring/rejecting candidate
  positions on a search ring — they are not a general constraint solver.
  Dense sheets sometimes need you to nudge `pref=`/`rmax=` arguments or add
  a sheet-specific `OPEN_VIEWS`/`solid_profile()` exclusion to get a clean
  placement; this is normal and was done throughout `sheets/*.py`.
- `models.py` and `sheets/*.py` as included are specific to the R-01 kiln —
  treat them as a worked reference example, not a generic template; the
  reusable part is everything *except* those two.
- This is an internal tool with terse, partly-Indonesian naming — read the
  function signatures directly for the full API surface rather than
  expecting exhaustive docstrings.
