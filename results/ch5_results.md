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
| Bidirectional Separability   | 18  | 2      | 0     | 11.1     | 0.0     |

---

## Sequential Palettes (N = 84 test cases)

Tier 1 (already accessible): 14 | Tier 2/3 (needed correction): 70 | Successfully corrected: 70

| Invariant                    | N   | Before | After | % Before | % After |
|------------------------------|-----|--------|-------|----------|---------|
| Pairwise Distinguishability  | 84  | 14     | 18    | 16.7     | 21.4    |
| Lightness Monotonicity       | 84  | 19     | 82    | 22.6     | 97.6    |
| Perceptual Uniformity        | 84  | 21     | 84    | 25.0     | 100.0   |
| Direction Preservation       | 84  | 84     | 84    | 100.0    | 100.0   |
| Midpoint Integrity           | 80  | 64     | 69    | 80.0     | 86.2    |
| Bidirectional Separability   | 80  | 10     | 22    | 12.5     | 27.5    |

---

## Diverging Palettes (N = 22 test cases)

Tier 1 (already accessible): 2 | Tier 2/3 (needed correction): 20 | Successfully corrected: 20

| Invariant                    | N   | Before | After | % Before | % After |
|------------------------------|-----|--------|-------|----------|---------|
| Pairwise Distinguishability  | 22  | 6      | 11    | 27.3     | 50.0    |
| Lightness Monotonicity       | 22  | 3      | 8     | 13.6     | 36.4    |
| Perceptual Uniformity        | 22  | 1      | 8     | 4.5      | 36.4    |
| Direction Preservation       | 22  | 22     | 22    | 100.0    | 100.0   |
| Midpoint Integrity           | 22  | 19     | 22    | 86.4     | 100.0   |
| Bidirectional Separability   | 22  | 2      | 17    | 9.1      | 77.3    |
