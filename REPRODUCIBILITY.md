# Reproducibility notes

## Fixed experimental design

- Dataset: MathDial (`eth-nlped/mathdial`), with the same example cohort for correctness and pedagogical-move experiments.
- Full cohort: 11,374 train / 1,173 validation / 3,069 test examples.
- Backbone: `Qwen2.5-1.5B-Instruct`, frozen.
- Total LoRA budget: rank 32. Two-branch systems use rank 16 + rank 16.
- Seeds: 42, 123, 7.
- Primary generation metric: response-only perplexity.
- Primary classification metric: Macro-F1.
- Statistical inference: paired bootstrap within seed (`n=2000`). Mean +/- sample SD across three seeds is descriptive only.

## Why two phases exist

Phase 1 uses 3-class student self-correctness. Phase 2 changes the auxiliary classification target to the 4-class pedagogical-move task while preserving the Phase-1 cohort and all frozen training settings. The Phase-2 decision criteria were fixed before running Phase 2; later gap-filling contrasts are explicitly post-hoc/exploratory in the manuscript. The preserved protocol file uses the historical label “pre-registered”; this denotes internal pre-specification before Phase 2, not a public registry deposit.

## Integrity checks

The runnable code includes checks for:

- gate gradient liveness;
- per-instance routing without detach/item/batch-collapse;
- deterministic hard task routing;
- task-dependent and context-dependent routing;
- whole-model train/eval state;
- stable example alignment for paired bootstrap;
- crash-safe atomic result persistence.

## Compute

The published full runs were executed on an NVIDIA RTX PRO 6000 Blackwell Server Edition. A smoke run should be performed before any full reproduction to verify the environment and routing integrity.
