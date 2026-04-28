"""
Shorter version of the Barley faceted dot plot.

Each facet shows only a subset of invariants (rows for filtered invariants are
removed entirely, not blank). Built as a vconcat of three independent charts
that share the bottom X-axis title via the last row.
"""

import re
from pathlib import Path

import altair as alt
import pandas as pd


MD_PATH = Path(__file__).with_name("ch5_results.md")
OUT_SVG = Path(__file__).with_name("shorter_barley_plot_for_vis.svg")
OUT_PNG = Path(__file__).with_name("shorter_barley_plot_for_vis.png")


def parse_markdown(md_text: str):
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


df = pd.DataFrame(parse_markdown(MD_PATH.read_text()))

invariant_order = [
    "Bidirectional Separability",
    "Midpoint Integrity",
    "Direction Preservation",
    "Perceptual Uniformity",
    "Lightness Monotonicity",
    "Pairwise Distinguishability",
]

facets = [
    ("Categorical", {"Pairwise Distinguishability"}),
    ("Sequential", {
        "Direction Preservation",
        "Perceptual Uniformity",
        "Lightness Monotonicity",
        "Pairwise Distinguishability",
    }),
    ("Diverging", set(invariant_order)),
]

color_scale = alt.Scale(domain=["Before", "After"], range=["#d62728", "#1f77b4"])


def facet_chart(palette_type: str, keep: set[str], is_last: bool):
    sub = df[(df["Palette Type"] == palette_type) & (df["Invariant"].isin(keep))]
    sort_order = [inv for inv in invariant_order if inv in keep]
    return alt.Chart(sub, title=alt.TitleParams(palette_type, orient="left", anchor="middle", angle=270, fontSize=10, fontWeight="normal")).mark_point(
        size=80, filled=True
    ).encode(
        alt.X(
            "% Passing:Q",
            title="% of Test Cases Passing" if is_last else None,
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(grid=False, labels=is_last, ticks=is_last, domain=is_last),
        ),
        alt.Y(
            "Invariant:N",
            title=None,
            sort=sort_order,
            axis=alt.Axis(grid=True),
        ),
        alt.Color(
            "Condition:N",
            title=None,
            scale=color_scale,
            legend=alt.Legend(orient="bottom"),
        ),
    ).properties(width=400, height=alt.Step(28))


charts = [facet_chart(name, keep, i == len(facets) - 1) for i, (name, keep) in enumerate(facets)]

combined = alt.vconcat(*charts, spacing=22, title=alt.TitleParams(
    "Invariant Pass Rates Before and After Correction", anchor="start", fontSize=15
)).configure_view(stroke="transparent").configure_axis(
    labelFontSize=12,
    titleFontSize=13,
)

combined.save(str(OUT_SVG))
combined.save(str(OUT_PNG), ppi=300)
print(f"Saved {OUT_SVG} and {OUT_PNG}")
