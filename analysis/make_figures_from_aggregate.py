#!/usr/bin/env python3
"""Regenerate the four paper figures from the public three-seed aggregate JSON files.

The aggregate files retain the three per-seed scalar values for every method, so the
published mean, descriptive SD, and faint per-seed points can be reconstructed without
the large aligned per-example audit files.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
SYSTEMS = ["shared","dual_fixed","dual_learned","hard_task","tc_static","tc_dldg","shared_pcgrad"]
LABEL = {"shared":"shared","dual_fixed":"dual-fixed","dual_learned":"dual-learned","hard_task":"hard-task","tc_static":"TC-static","tc_dldg":"TC-DLDG","shared_pcgrad":"PCGrad"}
COLORS = dict(zip(SYSTEMS, plt.rcParams["axes.prop_cycle"].by_key()["color"][:len(SYSTEMS)]))

def load(name): return json.loads((RESULTS/name).read_text(encoding="utf-8"))
def arr(a,k): return np.asarray([x for x in a[k] if x is not None], dtype=float)
def ms(a,k):
    x=arr(a,k); return float(x.mean()), float(x.std(ddof=1))

def pareto(agg):
    pts=[(s,ms(agg,f"ppl_{s}")[0],ms(agg,f"macro_f1_{s}")[0]) for s in SYSTEMS]
    return {s for s,x,y in pts if not any(x2<=x and y2>=y and (x2<x or y2>y) for s2,x2,y2 in pts if s2!=s)}

def pareto_plot(agg,title,out):
    fig,ax=plt.subplots(figsize=(8,6)); nd=pareto(agg)
    for s in SYSTEMS:
        x,sx=ms(agg,f"ppl_{s}"); y,sy=ms(agg,f"macro_f1_{s}")
        ax.errorbar(x,y,xerr=sx,yerr=sy,fmt='o',ms=10 if s in nd else 8.5,capsize=4,label=LABEL[s])
        ax.scatter(arr(agg,f"ppl_{s}"),arr(agg,f"macro_f1_{s}"),s=22,alpha=.28)
    gx,_=ms(agg,"ppl_gen_only"); cy,_=ms(agg,"macro_f1_cls_only")
    ax.axvline(gx,ls='--',lw=1,color='.35'); ax.axhline(cy,ls=':',lw=1,color='.35')
    ax.set(xlabel="Response perplexity (lower is better)",ylabel="Classification Macro-F1 (higher is better)",title=title)
    ax.grid(alpha=.22); ax.legend(title="System (mean of 3 seeds)",ncol=2,loc="lower left")
    fig.tight_layout(); fig.savefig(out,dpi=300); plt.close(fig)

def interference(corr,move,out):
    fig,ax=plt.subplots(figsize=(9,5.4)); x=np.arange(len(SYSTEMS)); w=.38
    for agg,name,off in [(corr,"correctness",-w/2),(move,"move",w/2)]:
        g=arr(agg,"ppl_gen_only"); ds=[arr(agg,f"ppl_{s}")-g for s in SYSTEMS]
        ax.bar(x+off,[d.mean() for d in ds],w,yerr=[d.std(ddof=1) for d in ds],capsize=4,label=name)
    ax.axhline(0,color='.2',lw=.9); ax.set_xticks(x,[LABEL[s] for s in SYSTEMS],rotation=20,ha='right')
    ax.set_ylabel("PPL relative to gen-only (positive = interference)"); ax.set_title("Generation interference vs gen-only, both auxiliary tasks")
    ax.legend(); ax.grid(alpha=.22,axis='y'); fig.tight_layout(); fig.savefig(out,dpi=300); plt.close(fig)

def effects(corr,move,out):
    methods=[s for s in SYSTEMS if s!="shared"]; x=np.arange(len(methods)); w=.38
    fig,axs=plt.subplots(1,2,figsize=(11.5,5))
    for agg,name,off in [(corr,"correctness",-w/2),(move,"move",w/2)]:
        p=arr(agg,"ppl_shared"); f=arr(agg,"macro_f1_shared")
        dp=[p-arr(agg,f"ppl_{s}") for s in methods]; df=[arr(agg,f"macro_f1_{s}")-f for s in methods]
        axs[0].bar(x+off,[d.mean() for d in dp],w,yerr=[d.std(ddof=1) for d in dp],capsize=4,label=name)
        axs[1].bar(x+off,[d.mean() for d in df],w,yerr=[d.std(ddof=1) for d in df],capsize=4,label=name)
    for ax in axs:
        ax.axhline(0,color='.2',lw=.9); ax.set_xticks(x,[LABEL[s] for s in methods],rotation=20,ha='right'); ax.grid(alpha=.22,axis='y'); ax.legend()
    axs[0].set_title("Generation recovery vs shared"); axs[0].set_ylabel("PPL improvement over shared (positive = better)")
    axs[1].set_title("Classification change vs shared"); axs[1].set_ylabel("Macro-F1 change vs shared (positive = better)")
    fig.suptitle("Method effect relative to the shared joint baseline (descriptive SD across 3 seeds)")
    fig.tight_layout(); fig.savefig(out,dpi=300); plt.close(fig)

if __name__ == "__main__":
    corr=load("aggregate_dldg_edu_corr_p1.json"); move=load("aggregate_dldg_edu_move_p2.json")
    pareto_plot(corr,"Correctness: PPL vs Macro-F1 (matched adapter budget)",OUT/"fig1_pareto_correctness.png")
    pareto_plot(move,"Pedagogical move: PPL vs Macro-F1 (matched adapter budget)",OUT/"fig2_pareto_move.png")
    interference(corr,move,OUT/"fig3_generation_interference.png")
    effects(corr,move,OUT/"fig4_improvement_vs_shared.png")
    print(f"Wrote figures to {OUT}")
