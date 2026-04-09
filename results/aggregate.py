#!/usr/bin/env python3
"""Aggregate per-file JSON reports into Ch5 statistics."""
import json, os, sys
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path("/Users/ayannath/Desktop/Senior Thesis/results")

def load_reports(cvd):
    d = ROOT / cvd / "reports"
    out = {}
    for f in sorted(d.glob("*.json")):
        with open(f) as fh:
            out[f.stem.replace("_report","")] = json.load(fh)
    return out

def per_file_invariants(rep):
    """Return (pre_tests, post_tests) lists of (name, passed) or None."""
    p5 = rep.get("phases", {}).get("phase5", {}).get("tests_run", [])
    pre = [(t["name"], t["passed"]) for t in p5]
    p6 = rep.get("phases", {}).get("phase6", {})
    post = None
    if p6 and "verification_tests" in p6:
        post = [(t["name"], t["passed"]) for t in p6["verification_tests"]]
    return pre, post

def summarize(cvd):
    reps = load_reports(cvd)
    n = len(reps)
    by_status = Counter()
    by_type = Counter()
    by_type_status = defaultdict(Counter)
    cat_ge8 = []
    cat_ge8_passed_pre = 0
    cat_ge8_repaired = 0
    invariants_relevant = Counter()
    invariants_violated_pre = Counter()
    invariants_repaired = Counter()
    invariants_still_failing = Counter()
    tier1_files = []  # all pre-pass
    tier2_files = []  # some fail
    tier3_files = []  # catastrophic (>=3 invariants fail or >=50%)
    error_files = []
    skipped_files = []
    repair_success = 0
    repair_attempted = 0
    fp_tier1 = 0  # tool recolored an already-accessible file
    for name, rep in reps.items():
        status = rep.get("status")
        by_status[status] += 1
        if status == "error":
            error_files.append(name); continue
        if status == "skipped":
            skipped_files.append(name); continue
        ptype = (rep.get("phases", {}).get("phase4", {}).get("reconciled_type")
                 or rep.get("phases", {}).get("phase2", {}).get("palette_type"))
        by_type[ptype] += 1
        by_type_status[ptype][status] += 1
        n_colors = rep.get("phases", {}).get("phase1", {}).get("n_data_colors", 0)
        pre, post = per_file_invariants(rep)
        n_pre_fail = sum(1 for _, p in pre if not p)
        n_pre_total = len(pre)
        for tname, passed in pre:
            invariants_relevant[tname] += 1
            if not passed:
                invariants_violated_pre[tname] += 1
        if post:
            for tname, passed in post:
                # only count if was failing pre
                pre_map = dict(pre)
                if tname in pre_map and not pre_map[tname]:
                    if passed:
                        invariants_repaired[tname] += 1
                    else:
                        invariants_still_failing[tname] += 1
        # tier classification
        if n_pre_fail == 0:
            tier1_files.append(name)
            if status in ("recolored", "recolored_with_warnings"):
                fp_tier1 += 1
        elif n_pre_total > 0 and (n_pre_fail >= 3 or n_pre_fail / n_pre_total >= 0.5):
            tier3_files.append(name)
        else:
            tier2_files.append(name)
        # repair attempts
        if status in ("recolored", "recolored_with_warnings", "failed_to_recolor"):
            repair_attempted += 1
            if status == "recolored":
                p6 = rep.get("phases", {}).get("phase6", {})
                if p6.get("verification_passed"):
                    repair_success += 1
        # categorical >=8
        if ptype == "categorical" and n_colors >= 8:
            cat_ge8.append((name, n_colors, status))
            if n_pre_fail == 0:
                cat_ge8_passed_pre += 1
            elif status == "recolored" and rep.get("phases", {}).get("phase6", {}).get("verification_passed"):
                cat_ge8_repaired += 1
    return {
        "n": n,
        "by_status": dict(by_status),
        "by_type": dict(by_type),
        "by_type_status": {k: dict(v) for k, v in by_type_status.items()},
        "invariants_relevant": dict(invariants_relevant),
        "invariants_violated_pre": dict(invariants_violated_pre),
        "invariants_repaired": dict(invariants_repaired),
        "invariants_still_failing": dict(invariants_still_failing),
        "tier1": tier1_files,
        "tier2": tier2_files,
        "tier3": tier3_files,
        "error_files": error_files,
        "skipped_files": skipped_files,
        "repair_attempted": repair_attempted,
        "repair_success": repair_success,
        "fp_tier1": fp_tier1,
        "cat_ge8": cat_ge8,
        "cat_ge8_passed_pre": cat_ge8_passed_pre,
        "cat_ge8_repaired": cat_ge8_repaired,
    }

protan = summarize("protan")
deutan = summarize("deutan")

# combined: per-file union of failures across both CVDs
def combined_tiers():
    pr = load_reports("protan")
    de = load_reports("deutan")
    files = sorted(set(pr) | set(de))
    t1 = t2 = t3 = 0
    t1_files = []; t2_files = []; t3_files = []
    err = 0
    for f in files:
        n_fail_max = 0
        n_total = 0
        any_error = False
        for src in (pr.get(f), de.get(f)):
            if not src: continue
            if src.get("status") in ("error","skipped"):
                any_error = True; continue
            pre = src.get("phases", {}).get("phase5", {}).get("tests_run", [])
            n_fail = sum(1 for t in pre if not t["passed"])
            n_total = max(n_total, len(pre))
            n_fail_max = max(n_fail_max, n_fail)
        if any_error and n_total == 0:
            err += 1; continue
        if n_fail_max == 0:
            t1 += 1; t1_files.append(f)
        elif n_total and (n_fail_max >= 3 or n_fail_max / n_total >= 0.5):
            t3 += 1; t3_files.append(f)
        else:
            t2 += 1; t2_files.append(f)
    return {"tier1": t1, "tier2": t2, "tier3": t3, "errors": err,
            "tier1_files": t1_files, "tier2_files": t2_files, "tier3_files": t3_files}

combined = combined_tiers()

out = {"protan": protan, "deutan": deutan, "combined": combined}
with open(ROOT / "aggregate.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
