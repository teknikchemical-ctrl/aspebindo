# Process engineering - modular POME + EFB biogas generator

| File | Purpose |
|---|---|
| `biogas_balance.py` | Mass & energy balance (kinetic model, Monte Carlo). Run in Spyder (F5); ends with `plt.show()`. Set `BIOGAS_QUICK=1` for a 40 s smoke test. ~60 s for the full run (N_MC = 400). |
| `make_design_basis.py` | Builds `PROCESS_DESIGN_BASIS.md` from `outputs/results.json` |
| `outputs/results.json` | Single source of truth for PFD, 3D and drawings (streams, equipment sizes, energy, MC) |
| `outputs/figs/*.png` | The nine figures shown by the script |

Needs: numpy, scipy, matplotlib.
