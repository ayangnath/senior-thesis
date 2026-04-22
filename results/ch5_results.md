# Chapter 5 Results: Invariant Pass Rates Before and After Correction

Data for Becker's Barley faceted plot. Three facets (one per palette type),
each showing the same 6 thesis invariants (Sections 3.3.1–3.3.6).
X-axis: % of test cases passing. Y-axis: invariant.
Two marks per row: Before (red) and After (blue).

**All 6 invariants tested against all palettes** (Section 3.2: cross-boundary failures).
Compound invariants collapsed with AND logic:
  - Pairwise Distinguishability = Categorical Pairwise ΔE AND Adjacent ΔE (when multi-hue)
  - Lightness Monotonicity = Monotonicity AND Min Step Size
  - Bidirectional Separability = Endpoint Separability AND Arm Monotonicity AND Arm Ratio

Aggregated across protanopia + deuteranopia at full severity (Machado et al. 2009).
Full Corpus: 75 SVGs, 63 with ≥2 data colors (12 skipped).

---

## Categorical Palettes (N = 20 test cases)

Tier 1 (already accessible): 7 | Tier 2/3 (needed correction): 13 | Successfully corrected: 13

| Invariant                    | N   | Before | After | % Before | % After |
|------------------------------|-----|--------|-------|----------|---------|
| Pairwise Distinguishability  | 20  | 7      | 20    | 35.0     | 100.0   |
| Lightness Monotonicity       | 20  | 4      | 3     | 20.0     | 15.0    |
| Perceptual Uniformity        | 20  | 5      | 4     | 25.0     | 20.0    |
| Direction Preservation       | 20  | 20     | 20    | 100.0    | 100.0   |
| Midpoint Integrity           | 18  | 13     | 15    | 72.2     | 83.3    |
| Bidirectional Separability   | 18  | 0      | 0     | 0.0      | 0.0     |

---

## Sequential Palettes (N = 76 test cases)

Tier 1 (already accessible): 14 | Tier 2/3 (needed correction): 62 | Successfully corrected: 62

| Invariant                    | N   | Before | After | % Before | % After |
|------------------------------|-----|--------|-------|----------|---------|
| Pairwise Distinguishability  | 76  | 52     | 76    | 68.4     | 100.0   |
| Lightness Monotonicity       | 76  | 19     | 74    | 25.0     | 97.4    |
| Perceptual Uniformity        | 76  | 21     | 76    | 27.6     | 100.0   |
| Direction Preservation       | 76  | 76     | 76    | 100.0    | 100.0   |
| Midpoint Integrity           | 72  | 56     | 61    | 77.8     | 84.7    |
| Bidirectional Separability   | 72  | 8      | 13    | 11.1     | 18.1    |

---

## Diverging Palettes (N = 30 test cases)

Tier 1 (already accessible): 1 | Tier 2/3 (needed correction): 29 | Successfully corrected: 29

| Invariant                    | N   | Before | After | % Before | % After |
|------------------------------|-----|--------|-------|----------|---------|
| Pairwise Distinguishability  | 30  | 27     | 30    | 90.0     | 100.0   |
| Lightness Monotonicity       | 30  | 6      | 24    | 20.0     | 80.0    |
| Perceptual Uniformity        | 30  | 7      | 25    | 23.3     | 83.3    |
| Direction Preservation       | 30  | 29     | 30    | 96.7     | 100.0   |
| Midpoint Integrity           | 30  | 27     | 29    | 90.0     | 96.7    |
| Bidirectional Separability   | 30  | 1      | 23    | 3.3      | 76.7    |
