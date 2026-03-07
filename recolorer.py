# Recoloring engine. Generates CVD-accessible replacement palettes for each
# palette type while trying to stay perceptually close to the original.

import numpy as np
from color_science import (
    srgb_to_lab, lab_to_srgb, ciede2000, rgb_to_hex, parse_color,
    simulate_cvd, simulate_cvd_lab, pairwise_de_under_cvd,
    get_lightness_under_cvd
)
from invariant_tests import test_categorical_pairwise, CATEGORICAL_MIN_DE


# pre-built CVD-safe categorical palettes
SAFE_CATEGORICAL_PALETTES = {
    "okabe_ito": [
        (0, 114, 178),    # blue
        (230, 159, 0),    # orange
        (0, 158, 115),    # bluish green
        (204, 121, 167),  # reddish purple
        (86, 180, 233),   # sky blue
        (213, 94, 0),     # vermillion
        (240, 228, 66),   # yellow
        (0, 0, 0),        # black
    ],
    "ibm": [
        (100, 143, 255),  # ultramarine
        (120, 94, 240),   # indigo
        (220, 38, 127),   # magenta
        (254, 97, 0),     # orange
        (255, 176, 0),    # gold
    ],
    "wong": [
        (0, 0, 0),        # black
        (230, 159, 0),    # orange
        (86, 180, 233),   # sky blue
        (0, 158, 115),    # bluish green
        (240, 228, 66),   # yellow
        (0, 114, 178),    # blue
        (213, 94, 0),     # vermillion
        (204, 121, 167),  # reddish purple
    ],
}

# single-hue sequential ramps that stay monotonic under CVD
SAFE_SEQUENTIAL_ANCHORS = {
    "blue": [(247, 251, 255), (198, 219, 239), (158, 202, 225),
             (107, 174, 214), (66, 146, 198), (33, 113, 181),
             (8, 81, 156), (8, 48, 107)],
    "purple": [(252, 251, 253), (218, 218, 235), (188, 189, 220),
               (158, 154, 200), (128, 125, 186), (106, 81, 163),
               (84, 39, 143), (63, 0, 125)],
    "orange": [(255, 245, 235), (254, 230, 206), (253, 208, 162),
               (253, 174, 107), (253, 141, 60), (241, 105, 19),
               (217, 72, 1), (166, 54, 3)],
}

# safe diverging endpoint pairs
SAFE_DIVERGING_ENDPOINTS = [
    {"left": (8, 48, 107), "mid": (247, 247, 247), "right": (166, 54, 3)},    # blue / orange
    {"left": (63, 0, 125), "mid": (247, 247, 247), "right": (0, 68, 27)},     # purple / green
    {"left": (5, 48, 97), "mid": (247, 247, 247), "right": (103, 0, 31)},     # blue / red-brown
]


# Find the safe palette perceptually closest to the original.
def _find_closest_safe_palette(original_colors, safe_palettes, cvd_type):
    n = len(original_colors)
    best_palette = None
    best_distance = float('inf')

    for name, palette in safe_palettes.items():
        if len(palette) < n:
            continue

        # greedy match: pair each original color to the nearest unused safe color
        subset = palette[:n]
        orig_labs = [srgb_to_lab(c) for c in original_colors]
        safe_labs = [srgb_to_lab(c) for c in subset]

        used = set()
        total_dist = 0
        mapping = {}

        for i, orig_lab in enumerate(orig_labs):
            best_j = -1
            best_d = float('inf')
            for j, safe_lab in enumerate(safe_labs):
                if j in used:
                    continue
                d = ciede2000(orig_lab, safe_lab)
                if d < best_d:
                    best_d = d
                    best_j = j
            if best_j >= 0:
                used.add(best_j)
                total_dist += best_d
                mapping[i] = best_j

        if total_dist < best_distance:
            best_distance = total_dist
            best_palette = (name, subset, mapping)

    return best_palette


# Generate a CVD-accessible categorical palette. Tries known safe palettes
# first, falls back to perturbation-based optimization on failure.
def recolor_categorical(colors, cvd_type="deutan", attempt=0):
    n = len(colors)

    # rotate palette order on retries so we try different ones first
    palette_names = list(SAFE_CATEGORICAL_PALETTES.keys())
    if attempt > 0:
        palette_names = palette_names[attempt % len(palette_names):] + \
                        palette_names[:attempt % len(palette_names)]

    palettes_to_try = {name: SAFE_CATEGORICAL_PALETTES[name] for name in palette_names}

    # first try: use a known safe palette
    result = _find_closest_safe_palette(colors, palettes_to_try, cvd_type)
    if result:
        _, safe_subset, mapping = result
        ordered_safe = [None] * n
        for orig_idx, safe_idx in mapping.items():
            ordered_safe[orig_idx] = safe_subset[safe_idx]

        # verify it actually passes
        test_check = test_categorical_pairwise(ordered_safe, cvd_type)
        if test_check.passed:
            color_map = {}
            for i, orig in enumerate(colors):
                color_map[rgb_to_hex(orig)] = rgb_to_hex(ordered_safe[i])
            return color_map

    # fallback: perturbation-based optimization in Lab space
    step_scale = 3.0 + attempt * 2.0
    current = [srgb_to_lab(c) for c in colors]
    best_colors = list(colors)

    for _ in range(200):
        rgb_current = [lab_to_srgb(lab) for lab in current]
        de_mat = pairwise_de_under_cvd(rgb_current, cvd_type)

        min_de = float('inf')
        worst_i, worst_j = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if de_mat[i, j] < min_de:
                    min_de = de_mat[i, j]
                    worst_i, worst_j = i, j

        if min_de >= CATEGORICAL_MIN_DE:
            best_colors = rgb_current
            break

        # push the two closest colors apart in Lab
        lab_i = current[worst_i]
        lab_j = current[worst_j]

        direction = lab_i - lab_j
        norm = np.linalg.norm(direction[1:])  # a*, b* only
        if norm < 0.01:
            direction = np.array([0, 5, 5])  # arbitrary push
            norm = np.linalg.norm(direction[1:])

        step = step_scale * direction / (norm + 1e-6)
        current[worst_i] = current[worst_i] + step * 0.5
        current[worst_j] = current[worst_j] - step * 0.5

        # clamp L*
        for k in range(n):
            current[k][0] = np.clip(current[k][0], 10, 95)

        best_colors = [lab_to_srgb(lab) for lab in current]

    # build the color mapping
    color_map = {}
    for i, orig in enumerate(colors):
        new = best_colors[i]
        color_map[rgb_to_hex(orig)] = rgb_to_hex(new)
    return color_map


# Interpolate a Lab ramp to n evenly-spaced steps.
def _interpolate_ramp(ramp_labs, n):
    new_colors = []
    for i in range(n):
        t = i / max(n - 1, 1)  # 0.0 to 1.0
        pos = t * (len(ramp_labs) - 1)
        idx_lo = int(pos)
        idx_hi = min(idx_lo + 1, len(ramp_labs) - 1)
        frac = pos - idx_lo
        interp_lab = ramp_labs[idx_lo] * (1 - frac) + ramp_labs[idx_hi] * frac
        new_colors.append(lab_to_srgb(interp_lab))
    return new_colors


# Iteratively adjust L* until the palette passes all four sequential
# invariants under CVD. Returns adjusted sRGB colors, dark-to-light.
def _enforce_sequential_under_cvd(new_colors_sorted, cvd_type):
    from color_science import simulate_cvd, get_lightness_under_cvd

    n = len(new_colors_sorted)
    if n < 2:
        return new_colors_sorted

    current_labs = np.array([srgb_to_lab(c) for c in new_colors_sorted], dtype=np.float64)

    for _iteration in range(10):
        current_rgb = [lab_to_srgb(lab) for lab in current_labs]
        cvd_L = np.array(get_lightness_under_cvd(current_rgb, cvd_type))

        # test monotonicity
        diffs = np.diff(cvd_L)
        is_monotonic = np.all(diffs > -0.5)

        # test uniformity
        abs_diffs = np.abs(diffs)
        mean_step = np.mean(abs_diffs)
        cv = np.std(abs_diffs) / (mean_step + 1e-10)
        is_uniform = cv < 0.4

        # test direction
        direction_ok = cvd_L[-1] > cvd_L[0]

        # test min step size
        min_step = np.min(abs_diffs) if len(abs_diffs) > 0 else 0
        step_ok = min_step >= 3.0

        if is_monotonic and is_uniform and direction_ok and step_ok:
            return current_rgb

        # apply targeted repairs for whichever test failed
        if not direction_ok:
            current_labs = current_labs[::-1]
            continue

        if not is_monotonic:
            for i in range(1, n):
                if cvd_L[i] <= cvd_L[i-1] + 0.5:
                    current_labs[i][0] += (cvd_L[i-1] - cvd_L[i]) + 2.0
                    current_labs[i][0] = min(current_labs[i][0], 98)
            continue

        if not step_ok:
            for i in range(len(abs_diffs)):
                if abs_diffs[i] < 3.0:
                    adjust = (3.0 - abs_diffs[i]) / 2 + 0.5
                    current_labs[i][0] = max(current_labs[i][0] - adjust, 5)
                    current_labs[i+1][0] = min(current_labs[i+1][0] + adjust, 98)
            continue

        if not is_uniform:
            L_lo = current_labs[0][0]
            L_hi = current_labs[-1][0]
            for i in range(n):
                target_L = L_lo + (L_hi - L_lo) * i / max(n - 1, 1)
                current_labs[i][0] = target_L
            continue

    # best effort
    return [lab_to_srgb(lab) for lab in current_labs]


# Generate a CVD-accessible sequential palette. Maps by lightness rank
# so the data ordering is preserved. Retries cycle through different ramps.
def recolor_sequential(colors, cvd_type="deutan", attempt=0):
    n = len(colors)
    labs = [srgb_to_lab(c) for c in colors]
    L_values = [lab[0] for lab in labs]

    # sort originals by lightness (darkest first)
    sorted_indices = sorted(range(n), key=lambda i: L_values[i])

    # pick a ramp: infer from original on first try, cycle on retries
    ramp_names = list(SAFE_SEQUENTIAL_ANCHORS.keys())

    if attempt == 0:
        # infer from average chromaticity
        avg_a = np.mean([lab[1] for lab in labs])
        avg_b = np.mean([lab[2] for lab in labs])

        best_ramp_name = "blue"
        if avg_b > 20 and avg_a > 0:
            best_ramp_name = "orange"
        elif avg_a < -10:
            best_ramp_name = "purple"
    else:
        best_ramp_name = ramp_names[attempt % len(ramp_names)]

    safe_ramp = SAFE_SEQUENTIAL_ANCHORS[best_ramp_name]

    # reverse so index 0 = darkest, matching our L*-ascending sort
    ramp_labs = [np.array(srgb_to_lab(c), dtype=np.float64) for c in reversed(safe_ramp)]

    # interpolate to get exactly n steps
    new_colors_sorted = _interpolate_ramp(ramp_labs, n)

    # verify and fix invariants under CVD
    new_colors_sorted = _enforce_sequential_under_cvd(new_colors_sorted, cvd_type)

    # map by lightness rank: darkest original gets darkest new, etc.
    color_map = {}
    for rank, orig_idx in enumerate(sorted_indices):
        color_map[rgb_to_hex(colors[orig_idx])] = rgb_to_hex(new_colors_sorted[rank])
    return color_map


# Generate a CVD-accessible diverging palette by interpolating through
# a neutral midpoint between two safe endpoint hues.
def recolor_diverging(colors, cvd_type="deutan", attempt=0):
    n = len(colors)
    mid_idx = n // 2

    if attempt == 0:
        # pick the closest safe scheme to the original
        orig_left_lab = srgb_to_lab(colors[0])
        orig_right_lab = srgb_to_lab(colors[-1])

        best_scheme = None
        best_dist = float('inf')

        for scheme in SAFE_DIVERGING_ENDPOINTS:
            left_lab = srgb_to_lab(scheme["left"])
            right_lab = srgb_to_lab(scheme["right"])
            dist = ciede2000(orig_left_lab, left_lab) + ciede2000(orig_right_lab, right_lab)
            dist2 = ciede2000(orig_left_lab, right_lab) + ciede2000(orig_right_lab, left_lab)
            if min(dist, dist2) < best_dist:
                best_dist = min(dist, dist2)
                if dist2 < dist:
                    best_scheme = {"left": scheme["right"], "mid": scheme["mid"], "right": scheme["left"]}
                else:
                    best_scheme = scheme

        if best_scheme is None:
            best_scheme = SAFE_DIVERGING_ENDPOINTS[0]
    else:
        # cycle through schemes on retries
        scheme = SAFE_DIVERGING_ENDPOINTS[attempt % len(SAFE_DIVERGING_ENDPOINTS)]
        best_scheme = scheme

    # interpolate both arms through the midpoint
    left_lab = srgb_to_lab(best_scheme["left"])
    mid_lab = srgb_to_lab(best_scheme["mid"])
    right_lab = srgb_to_lab(best_scheme["right"])

    n_left = mid_idx + 1   # including midpoint
    n_right = n - mid_idx  # including midpoint

    new_colors = []

    # left arm
    for i in range(n_left):
        t = i / max(n_left - 1, 1)
        lab = left_lab * (1 - t) + mid_lab * t
        new_colors.append(lab_to_srgb(lab))

    # right arm (skip midpoint, already included)
    for i in range(1, n_right):
        t = i / max(n_right - 1, 1)
        lab = mid_lab * (1 - t) + right_lab * t
        new_colors.append(lab_to_srgb(lab))

    # build mapping
    color_map = {}
    for i, orig in enumerate(colors):
        if i < len(new_colors):
            color_map[rgb_to_hex(orig)] = rgb_to_hex(new_colors[i])

    return color_map


# Dispatch to the right recoloring strategy for the palette type.
def recolor_palette(colors, palette_type, cvd_type="deutan", test_results=None, attempt=0):
    if palette_type == "categorical":
        return recolor_categorical(colors, cvd_type, attempt=attempt)
    elif palette_type == "sequential":
        return recolor_sequential(colors, cvd_type, attempt=attempt)
    elif palette_type == "diverging":
        return recolor_diverging(colors, cvd_type, attempt=attempt)
    else:
        raise ValueError(f"Unknown palette type: {palette_type}")
