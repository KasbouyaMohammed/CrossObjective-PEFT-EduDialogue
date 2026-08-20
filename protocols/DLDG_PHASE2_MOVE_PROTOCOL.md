# DLDG Phase 2 (pedagogical move) - pre-registered protocol

> STATUS: pre-registered BEFORE running. Phase 2 is a controlled TASK-DEPENDENCE test, not a search
> for better numbers. Categories M1-M5 and the comparison set below are fixed and must not be changed
> after seeing results. Code + CPU checks are done; the GPU run is a separate authorization.

## Question
Does the Phase-1 interference/mitigation pattern (measured on 3-class student self-correctness)
generalise to a different educational-dialogue objective - 4-class pedagogical move - or is it
task-dependent? If Phase 2 disagrees with Phase 1, the disagreement is the scientific result.

## What changes vs Phase 1
Only the classification target: `CLS_TASK = "move"` (4 classes: focus / probing / telling / generic).
Everything else is inherited unchanged by reusing the audited Phase-1 engine (`dldg_edu_run.py`):
MathDial source and split rules, frozen Qwen2.5-1.5B-Instruct, rank-32 total / 16+16 dual budget,
LoRA targets, lr 5e-4, 3 epochs, batch 8, grad_accum 4, seeds 42/123/7, optimiser/scheduler, best-val
rule, CLS_LAMBDA=1, class weighting, PCGrad, routing architectures, dropout, evaluation code,
bootstrap n=2000. No HPO, no extra seeds, no router redesign, no capacity change, no loss-weight tuning.

## Isolation and execution
- Executable: `colab_run/dldg_edu_phase2_move.py`; `RESULTS_TAG=_dldg_edu_move_p2`. Never reads or
  writes `*_dldg_edu_corr_p1.json`. Outputs: `results_seed{42,123,7}_dldg_edu_move_p2.json`,
  `aggregate_dldg_edu_move_p2.json` (smoke: `*_move_p2_smoke.json`).
- All nine systems (gen_only, cls_only, shared, dual_fixed, dual_learned, hard_task, tc_static,
  tc_dldg, shared_pcgrad) re-run from scratch on all three seeds. gen_only is re-run in the same
  environment so generation-interference comparisons are internally paired and contemporaneous.
- No historical reproduction gate. Old move experiments predate the audited evaluation/routing
  protocol; the launcher records them as informational only and never uses them as a stop condition.
  Phase-2 scientific comparisons use only the newly generated Phase-2 runs.

## Metrics
- Generation primary: response-only perplexity (down).
- Classification primary: 4-class Macro-F1 (up). Ordinary accuracy is NOT the main metric.
- Secondary: balanced accuracy, ordinary accuracy, majority-class baseline (context only).
- Same per-example arrays and stable example IDs as Phase 1; exact alignment (ex_id + gold) asserted
  before every paired bootstrap.

## Required paired comparisons (within each seed; 3-seed mean +/- SD is descriptive only; no t-tests)
Convention: for a pair (X vs Y), positive => X better (lower ppl for generation, higher Macro-F1).

Generation (perplexity):
1. shared vs gen_only  (generation interference)
2. tc_static vs shared
3. tc_dldg vs shared
4. tc_dldg vs tc_static
5. hard_task vs shared
6. shared_pcgrad vs shared
7. tc_static vs shared_pcgrad

Classification (Macro-F1):
1. shared vs cls_only  (classification interference)
2. tc_static vs shared
3. tc_dldg vs shared
4. tc_dldg vs tc_static
5. hard_task vs shared
6. shared_pcgrad vs shared
7. tc_static vs shared_pcgrad

## Pre-registered outcomes (fixed; do not edit after seeing results)
- **M1 - Cross-task confirmation.** Move reproduces the correctness pattern: shared causes significant
  generation interference vs gen_only; simple task conditioning mitigates it without systematic
  Macro-F1 sacrifice; contextual routing adds no robust advantage over task-only routing.
- **M2 - Context becomes useful.** TC-DLDG robustly beats TC-static on at least one primary axis
  without sacrificing the other, with paired evidence in the majority of seeds. Implies context
  utility is classification-task dependent.
- **M3 - Optimization dominates.** PCGrad consistently dominates the routing approaches on the 2D
  Pareto view with paired support.
- **M4 - No mitigation.** Shared interference exists, but neither routing nor PCGrad consistently
  improves the two-axis trade-off.
- **M5 - No generation interference.** The move objective does not reproduce the generation
  interference seen on correctness. This itself is evidence that cross-objective interference depends
  on the auxiliary task.

## Phase-1 vs Phase-2 comparison to prepare (report side by side; never pool the two tasks)
Correctness vs pedagogical move, for each:
- shared generation penalty relative to gen_only;
- shared classification change relative to cls_only;
- TC-static improvement relative to shared;
- TC-DLDG incremental value over TC-static;
- PCGrad improvement relative to shared;
- seed stability;
- Pareto frontier.
Correctness and move are separate tasks; they are never combined into one statistical test.

## Phase-1 result (frozen context, for reference only)
Phase-1 correctness outcome = **B**: task conditioning helps, contextual routing does not provide
robust additional value; strong asymmetric generation interference; PCGrad competitive but
seed-sensitive; tc_static more defensible than TC-DLDG. No correctness re-tuning is permitted.

## Historical (pre-audit) move values - INFORMATIONAL ONLY, not a gate
ppl means: gen_only 4.919, shared 5.125, dual_fixed 5.104, dual_learned 5.088.
acc means: cls_only 0.333, shared 0.463, dual_fixed 0.440, dual_learned 0.461.
Different implementation semantics; not comparable to the audited protocol; never an execution stop.

## Status of verification (done, no GPU)
- `py_compile` + import: OK. Guards assert CLS_TASK=move, 4 classes, tag isolation, nine systems.
- CPU checks (`dldg_phase2_move_cpu_checks.py`): move config, 4-class Macro-F1 vs sklearn, launcher
  isolation, comparison-set sizes - ALL PASS. GPU integrity (dual_learned gate liveness incl. the
  zero-B warm-up-aware check, hard/tc_static/tc_dldg routing, deterministic eval routes) runs inside
  the smoke via the reused Phase-1 integrity checks.
- FINAL CLASSIFICATION (M1-M5): emitted only after the move_p2 JSONs are audited; not before.
