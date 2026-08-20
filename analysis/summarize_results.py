#!/usr/bin/env python3
"""Print the manuscript-facing three-seed mean +/- sample-SD table from public aggregates."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SYSTEMS = ["gen_only", "cls_only", "shared", "dual_fixed", "dual_learned", "hard_task", "tc_static", "tc_dldg", "shared_pcgrad"]
LABEL = {
    "gen_only":"gen-only", "cls_only":"cls-only", "shared":"shared", "dual_fixed":"dual-fixed",
    "dual_learned":"dual-learned", "hard_task":"hard-task", "tc_static":"TC-static",
    "tc_dldg":"TC-DLDG", "shared_pcgrad":"shared+PCGrad"
}

def load(name):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))

def fmt(values):
    vals = [float(x) for x in values if x is not None]
    if not vals:
        return "--"
    a = np.asarray(vals, dtype=float)
    return f"{a.mean():.3f} +/- {a.std(ddof=1):.3f}"

def table(title, agg):
    print(f"\n{title}")
    print("system\tPPL\tMacro-F1\tBalanced acc.\tAccuracy")
    for s in SYSTEMS:
        print("\t".join([
            LABEL[s], fmt(agg[f"ppl_{s}"]), fmt(agg[f"macro_f1_{s}"]),
            fmt(agg[f"balanced_acc_{s}"]), fmt(agg[f"acc_{s}"])
        ]))

if __name__ == "__main__":
    table("Correctness", load("aggregate_dldg_edu_corr_p1.json"))
    table("Pedagogical move", load("aggregate_dldg_edu_move_p2.json"))
