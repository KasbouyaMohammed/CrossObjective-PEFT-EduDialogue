# Source archive manifest

This archive contains the audited source used for the manuscript's correctness and pedagogical-move experiments.

## Core experiment engine
- `code/dldg_edu_run.py`
- `code/dldg_edu_phase2_move.py`
- `code/dynapersona_full_run.py`
- `code/dynapersona_moe_run.py`

## Integrity checks
- `code/dldg_phase1_cpu_checks.py`
- `code/dldg_phase2_move_cpu_checks.py`

## Analysis / regeneration
- `analysis/verify_results.py`
- `analysis/reproduce_tables.py`
- `analysis/make_figures.py`

## Protocol / environment
- `protocols/DLDG_PHASE2_MOVE_PROTOCOL.md`
- `requirements.txt`
- `REPRODUCIBILITY.md`

The two `dynapersona_*` modules are included because the audited DLDG engine imports the common model/LoRA utilities from them.
