"""
Becker's Barley-style faceted dot plot for Chapter 5 results.
Each facet is a palette type, Y-axis is the 6 thesis invariants,
X-axis is % passing, with Before/After as the two color marks.
"""

import altair as alt
import pandas as pd

# Data from ch5_results.md (collapsed to 6 thesis invariants)
rows = [
    # Categorical
    {"Palette Type": "Categorical", "Invariant": "Pairwise Distinguishability", "% Passing": 35.0, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Pairwise Distinguishability", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Categorical", "Invariant": "Lightness Monotonicity", "% Passing": 20.0, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Lightness Monotonicity", "% Passing": 15.0, "Condition": "After"},
    {"Palette Type": "Categorical", "Invariant": "Perceptual Uniformity", "% Passing": 25.0, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Perceptual Uniformity", "% Passing": 20.0, "Condition": "After"},
    {"Palette Type": "Categorical", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Categorical", "Invariant": "Midpoint Integrity", "% Passing": 72.2, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Midpoint Integrity", "% Passing": 83.3, "Condition": "After"},
    {"Palette Type": "Categorical", "Invariant": "Bidirectional Separability", "% Passing": 11.1, "Condition": "Before"},
    {"Palette Type": "Categorical", "Invariant": "Bidirectional Separability", "% Passing": 0.0, "Condition": "After"},
    # Sequential
    {"Palette Type": "Sequential", "Invariant": "Pairwise Distinguishability", "% Passing": 16.7, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Pairwise Distinguishability", "% Passing": 21.4, "Condition": "After"},
    {"Palette Type": "Sequential", "Invariant": "Lightness Monotonicity", "% Passing": 22.6, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Lightness Monotonicity", "% Passing": 97.6, "Condition": "After"},
    {"Palette Type": "Sequential", "Invariant": "Perceptual Uniformity", "% Passing": 25.0, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Perceptual Uniformity", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Sequential", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Sequential", "Invariant": "Midpoint Integrity", "% Passing": 80.0, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Midpoint Integrity", "% Passing": 86.2, "Condition": "After"},
    {"Palette Type": "Sequential", "Invariant": "Bidirectional Separability", "% Passing": 12.5, "Condition": "Before"},
    {"Palette Type": "Sequential", "Invariant": "Bidirectional Separability", "% Passing": 27.5, "Condition": "After"},
    # Diverging
    {"Palette Type": "Diverging", "Invariant": "Pairwise Distinguishability", "% Passing": 27.3, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Pairwise Distinguishability", "% Passing": 50.0, "Condition": "After"},
    {"Palette Type": "Diverging", "Invariant": "Lightness Monotonicity", "% Passing": 13.6, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Lightness Monotonicity", "% Passing": 36.4, "Condition": "After"},
    {"Palette Type": "Diverging", "Invariant": "Perceptual Uniformity", "% Passing": 4.5, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Perceptual Uniformity", "% Passing": 36.4, "Condition": "After"},
    {"Palette Type": "Diverging", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Direction Preservation", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Diverging", "Invariant": "Midpoint Integrity", "% Passing": 86.4, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Midpoint Integrity", "% Passing": 100.0, "Condition": "After"},
    {"Palette Type": "Diverging", "Invariant": "Bidirectional Separability", "% Passing": 9.1, "Condition": "Before"},
    {"Palette Type": "Diverging", "Invariant": "Bidirectional Separability", "% Passing": 77.3, "Condition": "After"},
]

df = pd.DataFrame(rows)

# Invariant display order (top to bottom on Y-axis)
invariant_order = [
    "Bidirectional Separability",
    "Midpoint Integrity",
    "Direction Preservation",
    "Perceptual Uniformity",
    "Lightness Monotonicity",
    "Pairwise Distinguishability",
]

# Facet order
palette_order = ["Categorical", "Sequential", "Diverging"]

chart = alt.Chart(df, title="Invariant Pass Rates Before and After Correction").mark_point(
    size=80, filled=True
).encode(
    alt.X(
        "% Passing:Q",
        title="% of Test Cases Passing",
        scale=alt.Scale(domain=[0, 100]),
        axis=alt.Axis(grid=False),
    ),
    alt.Y(
        "Invariant:N",
        title="",
        sort=invariant_order,
        axis=alt.Axis(grid=True),
    ),
    alt.Color(
        "Condition:N",
        title="",
        scale=alt.Scale(
            domain=["Before", "After"],
            range=["#d62728", "#1f77b4"],
        ),
        legend=alt.Legend(orient="bottom"),
    ),
    alt.Row(
        "Palette Type:N",
        title="",
        sort=palette_order,
    ),
).properties(
    width=400,
    height=alt.Step(28),
).configure_view(
    stroke="transparent",
).configure_axis(
    labelFontSize=12,
    titleFontSize=13,
).configure_title(
    fontSize=15,
    anchor="start",
)

chart.save("results/ch5_barley_plot.svg")
chart.save("results/ch5_barley_plot.png", ppi=300)
print("Saved to results/ch5_barley_plot.svg and .png")
