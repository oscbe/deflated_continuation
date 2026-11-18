# FEM Carrier Problem Solver

A 1D Finite Element Method (FEM) implementation for solving the nonlinear Carrier problem using Newton-Kantorovich iteration and deflated continuation.

---

## Structure

FEM components:
- `mesh.py` – 1D mesh generation
- `basis.py` – Linear (CG1) basis functions
- `quadrature.py` – Gaussian quadrature
- `interpolant.py` – FEM function representation

Solver:
- `carrier.py` – Newton solver and deflated solver

Scripts:
- `def_cont_carrier.py` – Main continuation run (generates solutions + checkpoints)
- `load_checkpoint.py` – Restart continuation from a checkpoint

---

## Dependencies

- Python 3.8+
- numpy
- scipy
- matplotlib

## Usage

### Run deflated continuation
```
python def_cont_carrier.py
```

Outputs:
- Solutions saved in `checkpoints/run_1/`
- Plots saved in `figs/`

---

### Restart from checkpoint
```
python load_checkpoint.py
```

---

## Notes

- Domain: [-1, 1]
- Linear finite elements (CG1)
- Dirichlet boundary conditions enforced
- Deflation used to compute multiple solutions


## Next Steps
- Optimise
    - Sparse solvers - might need to think about construction
    - Look into GMRES with deflation preconditioner
    - See if Function, Deflator, and TotalDeflator objects can be optimised. I'm sure I've missed some obvious stuff - there's a lot of recalculation
- Implement and test other bases
- Try cranking epsilon even lower
- Produce a full bifurcation diagram - I'm not sure how to identify solutions as epsilon is varied, as sometimes we get convergence to multiple from one.