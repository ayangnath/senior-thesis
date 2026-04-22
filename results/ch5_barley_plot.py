"""
Becker's Barley-style faceted dot plot for Chapter 5 results.
Each facet is a palette type, Y-axis is the 6 thesis invariants,
X-axis is % passing, with Before/After as the two color marks.

Numbers auto-parsed from ch5_results.md so they stay in sync with the
latest aggregate run.
"""

import re
from pathlib import Path

import altair as alt
import pandas as pd


MD_PATH = Path(__file__).with_name("ch5_results.md")
OUT_SVG = Path(__file__).with_name("ch5_barley_plot.svg")
OUT_PNG = Path(__file__).with_name("ch5_barley_plot.png")


def parse_markdown(md_text: str):
    """Return list of {Palette Type, Invariant, % Passing, Condition} rows."""
    rows = []
    sections = re.split(r"^## (Categorical|Sequential|Diverging) Palettes.*$", md_text, flags=re.M)
    for i in range(1, len(sections), 2):
        ptype = sections[i]
        body = sections[i + 1]
        for line in body.splitlines():
            m = re.match(
                r"\|\s*([A-Za-z ]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|",
                line,
            )
            if not m:
                continue
            inv = m.group(1).strip()
            pct_before = float(m.group(5))
            pct_after = float(m.group(6))
            rows.append({"Palette Type": ptype, "Invariant": inv, "% Passing": pct_before, "Condition": "Before"})
            rows.append({"Palette Type": ptype, "Invariant": inv, "% Passing": pct_after, "Condition": "After"})
    return rows


rows = parse_markdown(MD_PATH.read_text())
df = pd.DataFrame(rows)

invariant_order = [
    "Bidirectional Separability",
    "Midpoint Integrity",
    "Direction Preservation",
    "Perceptual Uniformity",
    "Lightness Monotonicity",
    "Pairwise Distinguishability",
]
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

chart.save(str(OUT_SVG))
chart.save(str(OUT_PNG), ppi=300)
print(f"Saved to {OUT_SVG} and {OUT_PNG}")
