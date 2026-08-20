# Cross-Objective Interference in Parameter-Efficient Educational Dialogue Adaptation

Reproducibility package for the manuscript:

**Cross-Objective Interference in Parameter-Efficient Educational Dialogue Adaptation: A Matched-Budget Study of Routing and Gradient Surgery**

Authors: Mohammed Kasbouya, Mohamed Akram Lamhour, Nawal Sael.

## Scope

This repository accompanies a matched-budget study of joint tutor-response generation and auxiliary educational-dialogue classification on MathDial. The study compares generation-only and classification-only adapters with shared LoRA, factorized adapters, task routing, context-dependent routing, and PCGrad under a fixed total LoRA rank budget.

The public repository is designed to make the manuscript-facing numbers and implementation auditable without redistributing MathDial or very large per-example artifacts.

## Repository contents

```text
analysis/                         scripts that regenerate summary tables and figures
protocols/                        Phase-2 pre-specified task-dependence protocol
results/
  aggregate_dldg_edu_corr_p1.json public three-seed correctness aggregate
  aggregate_dldg_edu_move_p2.json public three-seed move aggregate
  SHA256SUMS_AUDITED_FULL.txt      checksums for archived full per-seed audit JSONs
source/dldg_source_code.zip       exact audited training/evaluation + analysis source package
REPRODUCIBILITY.md                experimental freeze and integrity notes
requirements.txt                  environment dependencies
```

## Reproduce the manuscript-facing tables

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analysis/summarize_results.py
```

The public aggregate JSONs retain all three seed-level scalar metrics used to compute the paper's descriptive mean +/- sample SD values.

## Reproduce the four figures

```bash
python analysis/make_figures_from_aggregate.py
```

This regenerates the two PPL-vs-Macro-F1 plots, the cross-task generation-interference plot, and the method-effect-vs-shared plot from the public aggregate JSONs. Error bars are descriptive sample SD across the three seeds; they are not bootstrap confidence intervals.

## Exact experiment source

The complete audited source package is available as:

```text
source/dldg_source_code.zip
```

It contains the full training/evaluation engine, Phase-2 launcher, CPU integrity checks, original statistical/figure scripts, protocol, and requirements. The experiment code retrieves MathDial from its public source; the dataset is not redistributed here.

Key frozen settings:

- MathDial, same cohort for both auxiliary objectives
- 11,374 train / 1,173 validation / 3,069 test examples
- frozen Qwen2.5-1.5B-Instruct backbone
- total LoRA rank budget 32; two-branch systems use 16 + 16
- seeds 42, 123, 7
- response-only perplexity for generation
- Macro-F1 as the primary classification metric
- paired bootstrap within each seed (`n=2000`)
- three-seed mean +/- sample SD is descriptive only

See `REPRODUCIBILITY.md` and `protocols/DLDG_PHASE2_MOVE_PROTOCOL.md` for the experimental freeze and the Phase-2 task-dependence design.

## Full paired-bootstrap audit files

The six full per-seed JSON outputs contain the aligned per-example arrays used for paired-bootstrap verification (stable example IDs, response NLL/token counts, gold labels/predictions, and routing summaries). Because these files are substantially larger than the manuscript-facing aggregates, they are retained by the authors rather than duplicated in the public repository.

`results/SHA256SUMS_AUDITED_FULL.txt` records their exact SHA256 checksums. The full aligned files are available on reasonable request for independent verification.

## Data availability

MathDial is publicly available from its original source. This repository does not redistribute the dialogue dataset. Public result files contain aggregate metrics only and no dialogue text.

## Paper conclusions represented by this package

- Joint generation + classification causes reproducible generation interference across both tested auxiliary objectives.
- Classification transfer is asymmetric and task-dependent rather than symmetrically negative.
- Simple task-conditioned routing is the most consistent mitigation across the two tested objectives.
- Additional context-dependent routing does not provide a consistent incremental benefit in this controlled setting.

## Citation

The final bibliographic citation will be added after publication.
