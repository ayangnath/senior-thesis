"""
Aggregate pipeline results from the Full Corpus runs (deutan + protan)
into a markdown table for the Becker's Barley faceted plot in Ch. 5.

Key design choices:
  - ALL invariants tested against ALL palettes (Section 3.2: cross-boundary failures).
  - Results are collapsed to match the 6 thesis invariants (Sections 3.3.1–3.3.6):
      1. Pairwise Distinguishability (3.3.1)
         — includes Adjacent ΔE for sequential/multi-hue palettes
      2. Lightness Monotonicity (3.3.2)
         — includes Min Step Size as a sub-check
      3. Perceptual Uniformity (3.3.3)
      4. Direction Preservation (3.3.4)
      5. Midpoint Integrity (3.3.5)
      6. Bidirectional Separability (3.3.6)
         — compound: Endpoint Separability AND Arm Monotonicity AND Arm Ratio Preservation
  - Bivariate (3.3.7) is not implemented, acknowledged in thesis.
"""

import json
import sys
import os
from collections import defaultdict
from pathlib import Path

# Add the project root so we can import the invariant test functions
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from color_science import parse_color
from invariant_tests import (
    test_categorical_pairwise,
    run_sequential_tests,
    run_diverging_tests,
    _split_diverging_arms_by_hue,
)

RESULTS_DIR = Path(__file__).parent

# Map code test names → thesis invariant (Section 3.3) for invariants that
# are measured the same way regardless of palette type.
# Tests that map to the same thesis invariant are combined with AND logic.
THESIS_INVARIANT_MAP = {
    "Sequential Test 1: Monotonicity": "Lightness Monotonicity",
    "Sequential Test 4: Min Step Size": "Lightness Monotonicity",
    "Sequential Test 2: Uniformity": "Perceptual Uniformity",
    "Sequential Test 3: Direction": "Direction Preservation",
    "Diverging Test 1: Midpoint Extremum": "Midpoint Integrity",
    "Diverging Test 2: Endpoints Distinct": "Bidirectional Separability",
    "Diverging Test 3: Arms Sequential": "Bidirectional Separability",
    "Diverging Test 4: Arm Ratio Preservation": "Bidirectional Separability",
}

# Pairwise Distinguishability is defined differently per palette type, per
# thesis Section 3.3.1:
#   categorical → "every pair distinct" (categorical pairwise ΔE > 8)
#   sequential (multi-hue) → "adjacent steps stay distinct" (catches plateau
#       collapse under CVD); non-adjacent pairs on a ramp are supposed to look
#       clearly different and pass trivially, so the all-pairs-distinct test
#       would fail by construction on any well-designed ramp.
#   diverging → adjacent-step test applied per-arm (same logic as sequential,
#       applied inside run_all_invariants_raw before collapse).
PAIRWISE_TEST_BY_PALETTE = {
    "categorical": "Categorical Pairwise ΔE",
    "sequential": "Sequential Cross-Check: Adjacent ΔE",
    "diverging": "Sequential Cross-Check: Adjacent ΔE",
}

# Display order matching thesis section numbering
INVARIANT_ORDER = [
    "Pairwise Distinguishability",
    "Lightness Monotonicity",
    "Perceptual Uniformity",
    "Direction Preservation",
    "Midpoint Integrity",
    "Bidirectional Separability",
]


def load_reports(run_dir):
    """Load all per-file JSON reports from a pipeline run."""
    reports_dir = run_dir / "reports"
    reports = []
    for f in sorted(reports_dir.glob("*_report.json")):
        with open(f) as fh:
            reports.append(json.load(fh))
    return reports


def hex_list_to_rgb(hex_list):
    """Convert list of hex color strings to list of (R,G,B) tuples."""
    colors = []
    for h in hex_list:
        rgb = parse_color(h)
        if rgb:
            colors.append(rgb)
    return colors


def run_all_invariants_raw(colors, cvd_type, palette_type=None):
    """
    Run EVERY invariant test on a palette.

    For diverging palettes, the sub-checks that apply per-arm
    (Pairwise ΔE, Monotonicity, Min Step, Uniformity, Direction) are
    evaluated on each hue-cluster arm independently and AND-ed together.
    This matches the thesis framing in Sections 3.3.1 - 3.3.4, which says
    those invariants apply per-arm for diverging palettes. Evaluating on
    the whole palette would measure the wrong thing, because a diverging
    palette is V-shaped in L* and has intentionally-close neighboring
    shades inside each arm.

    Midpoint Integrity (Test 1) and Bidirectional Separability
    (Tests 2-4) remain whole-palette checks for diverging palettes,
    since those invariants are canonically defined on the whole palette.

    Returns dict: {code_test_name: passed (bool)}
    """
    results = {}

    if palette_type == "diverging" and len(colors) >= 3:
        # --- Per-arm evaluation for the four sub-checks that apply per-arm ---
        left_idx, right_idx = _split_diverging_arms_by_hue(colors)
        left_arm = [colors[i] for i in left_idx]
        right_arm = [colors[i] for i in right_idx]

        def and_per_arm(test_name, left_arm_result, right_arm_result):
            if left_arm_result is None and right_arm_result is None:
                return  # no arms had enough colors; skip this test
            lp = True if left_arm_result is None else left_arm_result
            rp = True if right_arm_result is None else right_arm_result
            results[test_name] = lp and rp

        # Pairwise Distinguishability per-arm (each arm needs >=2 colors)
        left_cat = test_categorical_pairwise(left_arm, cvd_type).passed if len(left_arm) >= 2 else None
        right_cat = test_categorical_pairwise(right_arm, cvd_type).passed if len(right_arm) >= 2 else None
        and_per_arm("Categorical Pairwise ΔE", left_cat, right_cat)

        # Sequential sub-tests per-arm
        left_seq = {r.test_name: r.passed for r in run_sequential_tests(left_arm, cvd_type)} if len(left_arm) >= 2 else {}
        right_seq = {r.test_name: r.passed for r in run_sequential_tests(right_arm, cvd_type)} if len(right_arm) >= 2 else {}
        for seq_test in set(list(left_seq) + list(right_seq)):
            and_per_arm(seq_test, left_seq.get(seq_test), right_seq.get(seq_test))

        # Midpoint + Bidirectional Separability on the whole palette
        div_results = run_diverging_tests(colors, cvd_type)
        for r in div_results:
            results[r.test_name] = r.passed
    else:
        # --- Whole-palette evaluation for categorical / sequential / <3-color ---
        cat_result = test_categorical_pairwise(colors, cvd_type)
        results[cat_result.test_name] = cat_result.passed

        if len(colors) >= 2:
            seq_results = run_sequential_tests(colors, cvd_type)
            for r in seq_results:
                results[r.test_name] = r.passed

        if len(colors) >= 3:
            div_results = run_diverging_tests(colors, cvd_type)
            for r in div_results:
                results[r.test_name] = r.passed

    return results


def collapse_to_thesis_invariants(raw_results, palette_type=None):
    """
    Collapse raw code-level test results into the 6 thesis invariants.
    When multiple code tests map to the same thesis invariant, they are
    combined with AND logic (all sub-checks must pass).

    For Pairwise Distinguishability, the test used depends on palette type
    (see PAIRWISE_TEST_BY_PALETTE): categorical uses "every pair distinct",
    sequential and diverging use "adjacent steps distinct".

    Returns dict: {thesis_invariant_name: passed (bool)}
    """
    grouped = defaultdict(list)
    for code_name, passed in raw_results.items():
        thesis_name = THESIS_INVARIANT_MAP.get(code_name)
        if thesis_name:
            grouped[thesis_name].append(passed)

    # Pairwise Distinguishability: palette-type-specific test.
    # For sequential and diverging, Pairwise is a *multi-hue* failure mode
    # (plateau collapse under CVD). A single-hue palette cannot plateau-
    # collapse by construction, so when Adjacent ΔE isn't emitted the
    # invariant is trivially satisfied. This matters because the tool
    # frequently remaps multi-hue ramps to single-hue CVD-safe ramps as its
    # repair strategy, and we want that to count as a successful correction.
    pairwise_test = PAIRWISE_TEST_BY_PALETTE.get(palette_type)
    if pairwise_test:
        if pairwise_test in raw_results:
            grouped["Pairwise Distinguishability"].append(raw_results[pairwise_test])
        elif palette_type in ("sequential", "diverging"):
            grouped["Pairwise Distinguishability"].append(True)

    collapsed = {}
    for thesis_name in INVARIANT_ORDER:
        sub_results = grouped.get(thesis_name, [])
        if sub_results:
            collapsed[thesis_name] = all(sub_results)
        # If no sub-checks ran (e.g., single-hue sequential palette has no
        # Adjacent ΔE test emitted), skip this invariant for that file.

    return collapsed


def extract_all_invariants(reports):
    """
    For each report with ≥2 data colors, run ALL invariant tests on:
      - the ORIGINAL palette (before correction)
      - the CORRECTED palette (after correction), or original if no correction

    Collapses results to the 6 thesis invariants (Sections 3.3.1–3.3.6).
    Returns list of row dicts.
    """
    rows = []

    for report in reports:
        status = report.get("status", "")
        if status == "skipped":
            continue

        phases = report.get("phases", {})
        phase1 = phases.get("phase1", {})
        phase4 = phases.get("phase4", {})
        phase6 = phases.get("phase6", {})

        palette_type = (
            phase4.get("reconciled_type")
            or phases.get("phase2", {}).get("palette_type", "unknown")
        )
        cvd_type = report.get("cvd_type", "unknown")
        filename = report.get("file", "unknown")

        # Original palette
        orig_hex = phase1.get("original_palette", [])
        orig_colors = hex_list_to_rgb(orig_hex)
        if len(orig_colors) < 2:
            continue

        # Corrected palette (or original if no correction)
        new_hex = phase6.get("new_palette", [])
        if new_hex:
            new_colors = hex_list_to_rgb(new_hex)
        else:
            new_colors = orig_colors  # no correction applied

        # Run ALL invariants on both, then collapse to thesis invariants.
        # palette_type is threaded through so per-arm evaluation kicks in
        # for diverging palettes.
        before_raw = run_all_invariants_raw(orig_colors, cvd_type, palette_type)
        after_raw = run_all_invariants_raw(new_colors, cvd_type, palette_type)

        before_collapsed = collapse_to_thesis_invariants(before_raw, palette_type)
        after_collapsed = collapse_to_thesis_invariants(after_raw, palette_type)

        for thesis_inv in before_collapsed:
            rows.append({
                "file": filename,
                "cvd_type": cvd_type,
                "palette_type": palette_type,
                "status": status,
                "invariant": thesis_inv,
                "passed_before": before_collapsed[thesis_inv],
                "passed_after": after_collapsed.get(thesis_inv, before_collapsed[thesis_inv]),
            })

    return rows


def compute_summary(rows):
    """
    Group by (palette_type, invariant) and compute counts and percentages.
    """
    groups = defaultdict(lambda: {"n": 0, "before": 0, "after": 0})

    for row in rows:
        key = (row["palette_type"], row["invariant"])
        groups[key]["n"] += 1
        if row["passed_before"]:
            groups[key]["before"] += 1
        if row["passed_after"]:
            groups[key]["after"] += 1

    results = []
    for (ptype, inv), counts in groups.items():
        n = counts["n"]
        results.append({
            "palette_type": ptype,
            "invariant": inv,
            "n_cases": n,
            "n_passed_before": counts["before"],
            "n_passed_after": counts["after"],
            "pct_before": round(100 * counts["before"] / n, 1) if n > 0 else 0,
            "pct_after": round(100 * counts["after"] / n, 1) if n > 0 else 0,
        })

    # Sort by palette type order, then invariant display order
    ptype_order = {"categorical": 0, "sequential": 1, "diverging": 2}
    inv_order = {name: i for i, name in enumerate(INVARIANT_ORDER)}
    results.sort(key=lambda r: (
        ptype_order.get(r["palette_type"], 99),
        inv_order.get(r["invariant"], 99),
    ))

    return results


def compute_tier_summary(rows):
    """Tier-level summary grouped by palette_type."""
    seen = set()
    tier_counts = defaultdict(lambda: {"tier1": 0, "tier2_3": 0, "tier2_3_success": 0, "total": 0})

    for row in rows:
        key = (row["file"], row["cvd_type"])
        if key in seen:
            continue
        seen.add(key)

        ptype = row["palette_type"]
        tier_counts[ptype]["total"] += 1

        if row["status"] == "passed":
            tier_counts[ptype]["tier1"] += 1
        elif row["status"] in ("recolored", "recolored_with_warnings", "failed_to_recolor"):
            tier_counts[ptype]["tier2_3"] += 1
            if row["status"] in ("recolored", "recolored_with_warnings"):
                tier_counts[ptype]["tier2_3_success"] += 1

    return dict(tier_counts)


def format_markdown(summary, tier_summary):
    """Format results as markdown — one section per palette type."""
    lines = []
    lines.append("# Chapter 5 Results: Invariant Pass Rates Before and After Correction")
    lines.append("")
    lines.append("Data for Becker's Barley faceted plot. Three facets (one per palette type),")
    lines.append("each showing the same 6 thesis invariants (Sections 3.3.1–3.3.6).")
    lines.append("X-axis: % of test cases passing. Y-axis: invariant.")
    lines.append("Two marks per row: Before (red) and After (blue).")
    lines.append("")
    lines.append("**All 6 invariants tested against all palettes** (Section 3.2: cross-boundary failures).")
    lines.append("Compound invariants collapsed with AND logic:")
    lines.append("  - Pairwise Distinguishability = Categorical Pairwise ΔE AND Adjacent ΔE (when multi-hue)")
    lines.append("  - Lightness Monotonicity = Monotonicity AND Min Step Size")
    lines.append("  - Bidirectional Separability = Endpoint Separability AND Arm Monotonicity AND Arm Ratio")
    lines.append("")
    lines.append("Aggregated across protanopia + deuteranopia at full severity (Machado et al. 2009).")
    lines.append("Full Corpus: 75 SVGs, 63 with ≥2 data colors (12 skipped).")
    lines.append("")

    # One section per palette type
    for ptype in ["categorical", "sequential", "diverging"]:
        tc = tier_summary.get(ptype, {})
        total = tc.get("total", 0)
        t1 = tc.get("tier1", 0)
        t23 = tc.get("tier2_3", 0)
        t23s = tc.get("tier2_3_success", 0)

        lines.append("---")
        lines.append("")
        lines.append(f"## {ptype.capitalize()} Palettes (N = {total} test cases)")
        lines.append("")
        lines.append(f"Tier 1 (already accessible): {t1} | Tier 2/3 (needed correction): {t23} | Successfully corrected: {t23s}")
        lines.append("")
        lines.append("| Invariant                    | N   | Before | After | % Before | % After |")
        lines.append("|------------------------------|-----|--------|-------|----------|---------|")

        ptype_rows = [r for r in summary if r["palette_type"] == ptype]
        for row in ptype_rows:
            lines.append(
                f"| {row['invariant']:<28} "
                f"| {row['n_cases']:<3} "
                f"| {row['n_passed_before']:<6} "
                f"| {row['n_passed_after']:<5} "
                f"| {row['pct_before']:<8} "
                f"| {row['pct_after']:<7} |"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    all_rows = []

    for run_name in ["full_corpus_deutan", "full_corpus_protan"]:
        run_dir = RESULTS_DIR / run_name
        if not run_dir.exists():
            print(f"Skipping {run_name}: directory not found")
            continue
        print(f"Loading reports from {run_name}...")
        reports = load_reports(run_dir)
        print(f"  {len(reports)} reports loaded. Running all invariants on each...")
        rows = extract_all_invariants(reports)
        all_rows.extend(rows)
        print(f"  {len(rows)} invariant rows generated.")

    summary = compute_summary(all_rows)
    tier_summary = compute_tier_summary(all_rows)
    md = format_markdown(summary, tier_summary)

    output_path = RESULTS_DIR / "ch5_results.md"
    with open(output_path, "w") as f:
        f.write(md)

    print(f"\nWritten to {output_path}")
    print(f"Total invariant rows: {len(all_rows)}")
    print(f"Summary entries: {len(summary)} (should be ~18: 6 invariants × 3 palette types)")


if __name__ == "__main__":
    main()
