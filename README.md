# Cross-Objective Interference in Parameter-Efficient Educational Dialogue Adaptation

Reproducibility package for the manuscript:

**Cross-Objective Interference in Parameter-Efficient Educational Dialogue Adaptation: A Matched-Budget Study of Routing and Gradient Surgery**

Authors: Mohammed Kasbouya, Mohamed Akram Lamhour, Nawal Sael.

## What this repository contains

This repository reproduces the matched-budget study of joint tutor-response generation and auxiliary educational-dialogue classification on MathDial. It includes the exact audited experiment code, the Phase-2 pre-specified protocol, source-of-truth result files used by the manuscript, integrity checks, and scripts that regenerate the reported summary tables and figures.

The paper compares nine systems under the same total LoRA rank budget: generation-only, classification-only, shared joint LoRA, dual-fixed factorization, task-agnostic learned routing, hard task routing, static task-conditioned routing, task+context routing, and shared LoRA with PCGrad.

## Main reproducibility claim

The repository is intended to make the reported numbers independently auditable. No training is needed to regenerate the manuscript's summary tables and figures: decompress the saved per-seed JSON files and run the analysis scripts.

## Repository layout

```text
code/                  exact audited training/evaluation code
analysis/              table, statistics, and figure regeneration
results/               audited aggregate + per-seed JSON outputs
protocols/             Phase-2 pre-specified protocol
figures/               regenerated publication figures
requirements.txt       Python dependencies
REPRODUCIBILITY.md      experimental freeze and integrity notes
```

## 1. Environment

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

For a Colab reproduction, use a GPU runtime and set the project root to the cloned repository:

```bash
export PROJECT_ROOT="$PWD"
```

The experiment code downloads MathDial from Hugging Face (`eth-nlped/mathdial`) and falls back to the public raw CSV files if needed. The dataset itself is not redistributed here.

## 2. Verify the saved results without training

```bash
gzip -dk results/results_seed*_dldg_edu_*.json.gz
python analysis/verify_results.py
python analysis/reproduce_tables.py
python analysis/make_figures.py --results-dir results --out-dir figures
```

`verify_results.py` checks the eight audited JSONs, seeds, cohorts, metric finiteness, example alignment, and expected system set before any table/figure regeneration.

## 3. CPU integrity tests

```bash
export PROJECT_ROOT="$PWD"
python code/dldg_phase1_cpu_checks.py
python code/dldg_phase2_move_cpu_checks.py
```

## 4. Smoke run

Run a smoke test before a full experiment:

```bash
export PROJECT_ROOT="$PWD"
export PYTHONPATH="$PWD/code"
export SMOKE=1
export CLS_TASK=correctness
export RESULTS_TAG=_dldg_edu_corr_p1_smoke
python code/dldg_edu_run.py
```

For pedagogical move:

```bash
export PROJECT_ROOT="$PWD"
export PYTHONPATH="$PWD/code"
export SMOKE=1
python code/dldg_edu_phase2_move.py
```

A valid environment should reach both `INTEGRITY PASS` and `INTEGRITY 2 PASS` before completing the nine-system smoke exercise.

## 5. Full reproduction

Full correctness and move runs are computationally expensive. Keep the audited hyperparameters unchanged and run only after the smoke tests pass. See the module-level documentation in `code/dldg_edu_run.py`, `code/dldg_edu_phase2_move.py`, and `protocols/DLDG_PHASE2_MOVE_PROTOCOL.md`.

## Results used by the paper

The manuscript's source of truth is restricted to:

- `aggregate_dldg_edu_corr_p1.json`
- `results_seed{42,123,7}_dldg_edu_corr_p1.json`
- `aggregate_dldg_edu_move_p2.json`
- `results_seed{42,123,7}_dldg_edu_move_p2.json`

The per-seed files are stored as `.json.gz` in GitHub and decompress byte-for-byte to the audited JSONs.

## Data and code availability

MathDial is publicly available from its original repository/Hugging Face dataset card. This repository contains preprocessing logic and does not redistribute the dataset. The saved result artifacts contain metrics, example identifiers, token-level loss aggregates, labels/predictions, and routing summaries; they do not contain the dialogue text.

## Citation

If the manuscript is accepted, the final bibliographic citation will be added here.
