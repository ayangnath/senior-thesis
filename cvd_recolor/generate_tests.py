# Generate test SVGs that cover common CVD failure modes across all palette types.

import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_svgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_svg(filename, content):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Created: {path}")


# stacked bar with red/green/orange - collapses under deuteranopia
CATEGORICAL_FAIL = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <text x="200" y="25" text-anchor="middle" font-size="14" fill="#333">
    Sales by Region (Stacked Bar)
  </text>

  <!-- Y-axis -->
  <line x1="60" y1="40" x2="60" y2="260" stroke="#666" stroke-width="1"/>
  <!-- X-axis -->
  <line x1="60" y1="260" x2="380" y2="260" stroke="#666" stroke-width="1"/>

  <!-- Axis labels -->
  <text x="55" y="265" text-anchor="end" font-size="10" fill="#666">0</text>
  <text x="55" y="205" text-anchor="end" font-size="10" fill="#666">25</text>
  <text x="55" y="145" text-anchor="end" font-size="10" fill="#666">50</text>
  <text x="55" y="85" text-anchor="end" font-size="10" fill="#666">75</text>

  <!-- Gridlines -->
  <line x1="60" y1="200" x2="380" y2="200" stroke="#eee" stroke-width="0.5"/>
  <line x1="60" y1="140" x2="380" y2="140" stroke="#eee" stroke-width="0.5"/>
  <line x1="60" y1="80" x2="380" y2="80" stroke="#eee" stroke-width="0.5"/>

  <!-- Bar group 1: Q1 -->
  <text x="120" y="278" text-anchor="middle" font-size="10" fill="#666">Q1</text>
  <rect x="85" y="180" width="70" height="80" fill="#d62728"/>  <!-- Red: North -->
  <rect x="85" y="120" width="70" height="60" fill="#2ca02c"/>  <!-- Green: South -->
  <rect x="85" y="80"  width="70" height="40" fill="#ff7f0e"/>  <!-- Orange: West -->

  <!-- Bar group 2: Q2 -->
  <text x="230" y="278" text-anchor="middle" font-size="10" fill="#666">Q2</text>
  <rect x="195" y="160" width="70" height="100" fill="#d62728"/>
  <rect x="195" y="100" width="70" height="60"  fill="#2ca02c"/>
  <rect x="195" y="60"  width="70" height="40"  fill="#ff7f0e"/>

  <!-- Bar group 3: Q3 -->
  <text x="340" y="278" text-anchor="middle" font-size="10" fill="#666">Q3</text>
  <rect x="305" y="170" width="70" height="90" fill="#d62728"/>
  <rect x="305" y="110" width="70" height="60" fill="#2ca02c"/>
  <rect x="305" y="70"  width="70" height="40" fill="#ff7f0e"/>

  <!-- Legend -->
  <g class="legend" transform="translate(60, 290)">
    <rect x="0" y="-5" width="12" height="12" fill="#d62728"/>
    <text x="16" y="5" font-size="10" fill="#333">North</text>
    <rect x="70" y="-5" width="12" height="12" fill="#2ca02c"/>
    <text x="86" y="5" font-size="10" fill="#333">South</text>
    <rect x="140" y="-5" width="12" height="12" fill="#ff7f0e"/>
    <text x="156" y="5" font-size="10" fill="#333">West</text>
  </g>
</svg>"""

# green-yellow-red heatmap - U-shaped lightness under deuteranopia
SEQUENTIAL_FAIL = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <text x="200" y="25" text-anchor="middle" font-size="14" fill="#333">
    Temperature Heatmap (Sequential)
  </text>

  <!-- row labels -->
  <text x="55" y="65" text-anchor="end" font-size="10" fill="#666">Mon</text>
  <text x="55" y="105" text-anchor="end" font-size="10" fill="#666">Tue</text>
  <text x="55" y="145" text-anchor="end" font-size="10" fill="#666">Wed</text>
  <text x="55" y="185" text-anchor="end" font-size="10" fill="#666">Thu</text>
  <text x="55" y="225" text-anchor="end" font-size="10" fill="#666">Fri</text>

  <!-- column labels -->
  <text x="95"  y="48" text-anchor="middle" font-size="10" fill="#666">6am</text>
  <text x="155" y="48" text-anchor="middle" font-size="10" fill="#666">9am</text>
  <text x="215" y="48" text-anchor="middle" font-size="10" fill="#666">12pm</text>
  <text x="275" y="48" text-anchor="middle" font-size="10" fill="#666">3pm</text>
  <text x="335" y="48" text-anchor="middle" font-size="10" fill="#666">6pm</text>

  <!-- data cells: green to yellow to red ramp, classic CVD problem -->
  <!-- Row 1 -->
  <rect x="65" y="52" width="55" height="35" fill="#1a9641"/>
  <rect x="125" y="52" width="55" height="35" fill="#66bd63"/>
  <rect x="185" y="52" width="55" height="35" fill="#a6d96a"/>
  <rect x="245" y="52" width="55" height="35" fill="#d9ef8b"/>
  <rect x="305" y="52" width="55" height="35" fill="#fee08b"/>
  <!-- Row 2 -->
  <rect x="65" y="92" width="55" height="35" fill="#66bd63"/>
  <rect x="125" y="92" width="55" height="35" fill="#a6d96a"/>
  <rect x="185" y="92" width="55" height="35" fill="#fee08b"/>
  <rect x="245" y="92" width="55" height="35" fill="#fdae61"/>
  <rect x="305" y="92" width="55" height="35" fill="#f46d43"/>
  <!-- Row 3 -->
  <rect x="65" y="132" width="55" height="35" fill="#a6d96a"/>
  <rect x="125" y="132" width="55" height="35" fill="#fee08b"/>
  <rect x="185" y="132" width="55" height="35" fill="#fdae61"/>
  <rect x="245" y="132" width="55" height="35" fill="#f46d43"/>
  <rect x="305" y="132" width="55" height="35" fill="#d73027"/>
  <!-- Row 4 -->
  <rect x="65" y="172" width="55" height="35" fill="#d9ef8b"/>
  <rect x="125" y="172" width="55" height="35" fill="#fdae61"/>
  <rect x="185" y="172" width="55" height="35" fill="#f46d43"/>
  <rect x="245" y="172" width="55" height="35" fill="#d73027"/>
  <rect x="305" y="172" width="55" height="35" fill="#a50026"/>
  <!-- Row 5 -->
  <rect x="65" y="212" width="55" height="35" fill="#fee08b"/>
  <rect x="125" y="212" width="55" height="35" fill="#f46d43"/>
  <rect x="185" y="212" width="55" height="35" fill="#d73027"/>
  <rect x="245" y="212" width="55" height="35" fill="#a50026"/>
  <rect x="305" y="212" width="55" height="35" fill="#67001f"/>

  <!-- Legend: sequential ramp -->
  <g class="legend" transform="translate(65, 260)">
    <text x="0" y="0" font-size="9" fill="#666">Low</text>
    <rect x="25" y="-9" width="20" height="12" fill="#1a9641"/>
    <rect x="47" y="-9" width="20" height="12" fill="#66bd63"/>
    <rect x="69" y="-9" width="20" height="12" fill="#a6d96a"/>
    <rect x="91" y="-9" width="20" height="12" fill="#d9ef8b"/>
    <rect x="113" y="-9" width="20" height="12" fill="#fee08b"/>
    <rect x="135" y="-9" width="20" height="12" fill="#fdae61"/>
    <rect x="157" y="-9" width="20" height="12" fill="#f46d43"/>
    <rect x="179" y="-9" width="20" height="12" fill="#d73027"/>
    <rect x="201" y="-9" width="20" height="12" fill="#a50026"/>
    <rect x="223" y="-9" width="20" height="12" fill="#67001f"/>
    <text x="250" y="0" font-size="9" fill="#666">High</text>
  </g>
</svg>"""

# red-white-green temperature map - red arm collapses under CVD
DIVERGING_FAIL = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="450" height="300" viewBox="0 0 450 300">
  <text x="225" y="25" text-anchor="middle" font-size="14" fill="#333">
    Temperature Anomaly by Region (Diverging)
  </text>

  <!-- regions -->
  <!-- red/white/green diverging scheme, collapses under protan/deutan -->
  <rect x="20"  y="40" width="80" height="60" fill="#1b7837"/>  <!-- Strong green (cold) -->
  <rect x="105" y="40" width="80" height="60" fill="#5aae61"/>  <!-- Medium green -->
  <rect x="190" y="40" width="80" height="60" fill="#a6dba0"/>  <!-- Light green -->
  <rect x="275" y="40" width="80" height="60" fill="#d9f0d3"/>  <!-- Very light green -->
  <rect x="360" y="40" width="80" height="60" fill="#f7f7f7"/>  <!-- White/neutral -->

  <rect x="20"  y="105" width="80" height="60" fill="#f7f7f7"/> <!-- White/neutral -->
  <rect x="105" y="105" width="80" height="60" fill="#fddbc7"/> <!-- Very light red -->
  <rect x="190" y="105" width="80" height="60" fill="#f4a582"/> <!-- Light red -->
  <rect x="275" y="105" width="80" height="60" fill="#d6604d"/> <!-- Medium red -->
  <rect x="360" y="105" width="80" height="60" fill="#b2182b"/> <!-- Strong red -->

  <!-- Mixed rows -->
  <rect x="20"  y="170" width="80" height="60" fill="#5aae61"/>
  <rect x="105" y="170" width="80" height="60" fill="#f4a582"/>
  <rect x="190" y="170" width="80" height="60" fill="#f7f7f7"/>
  <rect x="275" y="170" width="80" height="60" fill="#a6dba0"/>
  <rect x="360" y="170" width="80" height="60" fill="#d6604d"/>

  <!-- Legend -->
  <g class="legend" transform="translate(30, 250)">
    <text x="0" y="12" font-size="10" fill="#333">Cold</text>
    <rect x="40"  y="2" width="25" height="15" fill="#1b7837"/>
    <rect x="68"  y="2" width="25" height="15" fill="#5aae61"/>
    <rect x="96"  y="2" width="25" height="15" fill="#a6dba0"/>
    <rect x="124" y="2" width="25" height="15" fill="#d9f0d3"/>
    <rect x="152" y="2" width="25" height="15" fill="#f7f7f7" stroke="#ccc" stroke-width="0.5"/>
    <rect x="180" y="2" width="25" height="15" fill="#fddbc7"/>
    <rect x="208" y="2" width="25" height="15" fill="#f4a582"/>
    <rect x="236" y="2" width="25" height="15" fill="#d6604d"/>
    <rect x="264" y="2" width="25" height="15" fill="#b2182b"/>
    <text x="295" y="12" font-size="10" fill="#333">Hot</text>
  </g>
</svg>"""

# blue+orange bar chart - already CVD-safe
CATEGORICAL_PASS = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="350" height="250" viewBox="0 0 350 250">
  <text x="175" y="22" text-anchor="middle" font-size="14" fill="#333">
    Revenue: Online vs In-Store
  </text>

  <line x1="50" y1="35" x2="50" y2="210" stroke="#666" stroke-width="1"/>
  <line x1="50" y1="210" x2="330" y2="210" stroke="#666" stroke-width="1"/>

  <!-- Blue bars (online) -->
  <rect x="70"  y="80"  width="35" height="130" fill="#0072B2"/>
  <rect x="155" y="60"  width="35" height="150" fill="#0072B2"/>
  <rect x="240" y="100" width="35" height="110" fill="#0072B2"/>

  <!-- Orange bars (in-store) -->
  <rect x="110" y="110" width="35" height="100" fill="#E69F00"/>
  <rect x="195" y="90"  width="35" height="120" fill="#E69F00"/>
  <rect x="280" y="130" width="35" height="80"  fill="#E69F00"/>

  <text x="110" y="225" text-anchor="middle" font-size="10" fill="#666">Q1</text>
  <text x="195" y="225" text-anchor="middle" font-size="10" fill="#666">Q2</text>
  <text x="280" y="225" text-anchor="middle" font-size="10" fill="#666">Q3</text>

  <g class="legend" transform="translate(70, 240)">
    <rect x="0" y="-5" width="12" height="12" fill="#0072B2"/>
    <text x="16" y="5" font-size="10" fill="#333">Online</text>
    <rect x="80" y="-5" width="12" height="12" fill="#E69F00"/>
    <text x="96" y="5" font-size="10" fill="#333">In-Store</text>
  </g>
</svg>"""

# single-hue blue ramp - monotonic lightness under any CVD type
SEQUENTIAL_PASS = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <text x="200" y="22" text-anchor="middle" font-size="14" fill="#333">
    Population Density (Blue Sequential)
  </text>

  <!-- blue ramp regions -->
  <rect x="20"  y="40" width="70" height="100" fill="#eff3ff"/>
  <rect x="95"  y="40" width="70" height="100" fill="#bdd7e7"/>
  <rect x="170" y="40" width="70" height="100" fill="#6baed6"/>
  <rect x="245" y="40" width="70" height="100" fill="#3182bd"/>
  <rect x="320" y="40" width="70" height="100" fill="#08519c"/>

  <!-- Legend -->
  <g class="legend" transform="translate(20, 160)">
    <text x="0" y="10" font-size="9" fill="#666">Low</text>
    <rect x="30"  y="0" width="50" height="14" fill="#eff3ff"/>
    <rect x="82"  y="0" width="50" height="14" fill="#bdd7e7"/>
    <rect x="134" y="0" width="50" height="14" fill="#6baed6"/>
    <rect x="186" y="0" width="50" height="14" fill="#3182bd"/>
    <rect x="238" y="0" width="50" height="14" fill="#08519c"/>
    <text x="295" y="10" font-size="9" fill="#666">High</text>
  </g>
</svg>"""

# scatter plot with 6 confusable colors
CATEGORICAL_MULTI_FAIL = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="320" viewBox="0 0 400 320">
  <text x="200" y="20" text-anchor="middle" font-size="14" fill="#333">
    Species Distribution (Scatter)
  </text>

  <line x1="50" y1="30" x2="50" y2="250" stroke="#666" stroke-width="1"/>
  <line x1="50" y1="250" x2="380" y2="250" stroke="#666" stroke-width="1"/>

  <!-- Species A: Red -->
  <circle cx="100" cy="80"  r="6" fill="#e41a1c"/>
  <circle cx="130" cy="100" r="6" fill="#e41a1c"/>
  <circle cx="110" cy="120" r="6" fill="#e41a1c"/>
  <circle cx="150" cy="90"  r="6" fill="#e41a1c"/>

  <!-- Species B: Green -->
  <circle cx="180" cy="150" r="6" fill="#4daf4a"/>
  <circle cx="200" cy="130" r="6" fill="#4daf4a"/>
  <circle cx="170" cy="170" r="6" fill="#4daf4a"/>
  <circle cx="210" cy="160" r="6" fill="#4daf4a"/>

  <!-- Species C: Brown -->
  <circle cx="250" cy="70"  r="6" fill="#a65628"/>
  <circle cx="270" cy="90"  r="6" fill="#a65628"/>
  <circle cx="260" cy="110" r="6" fill="#a65628"/>

  <!-- Species D: Orange -->
  <circle cx="300" cy="180" r="6" fill="#ff7f00"/>
  <circle cx="320" cy="200" r="6" fill="#ff7f00"/>
  <circle cx="280" cy="190" r="6" fill="#ff7f00"/>

  <!-- Species E: Dark green -->
  <circle cx="140" cy="200" r="6" fill="#006d2c"/>
  <circle cx="160" cy="220" r="6" fill="#006d2c"/>
  <circle cx="120" cy="210" r="6" fill="#006d2c"/>

  <!-- Species F: Olive -->
  <circle cx="340" cy="100" r="6" fill="#808000"/>
  <circle cx="350" cy="120" r="6" fill="#808000"/>
  <circle cx="360" cy="80"  r="6" fill="#808000"/>

  <g class="legend" transform="translate(50, 270)">
    <rect x="0" y="-5" width="10" height="10" fill="#e41a1c"/>
    <text x="14" y="4" font-size="9" fill="#333">Sp. A</text>
    <rect x="55" y="-5" width="10" height="10" fill="#4daf4a"/>
    <text x="69" y="4" font-size="9" fill="#333">Sp. B</text>
    <rect x="110" y="-5" width="10" height="10" fill="#a65628"/>
    <text x="124" y="4" font-size="9" fill="#333">Sp. C</text>
    <rect x="165" y="-5" width="10" height="10" fill="#ff7f00"/>
    <text x="179" y="4" font-size="9" fill="#333">Sp. D</text>
    <rect x="220" y="-5" width="10" height="10" fill="#006d2c"/>
    <text x="234" y="4" font-size="9" fill="#333">Sp. E</text>
    <rect x="275" y="-5" width="10" height="10" fill="#808000"/>
    <text x="289" y="4" font-size="9" fill="#333">Sp. F</text>
  </g>
</svg>"""

# red-white-green correlation heatmap
CORRELATION_HEATMAP = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="350" height="350" viewBox="0 0 350 350">
  <text x="175" y="22" text-anchor="middle" font-size="14" fill="#333">
    Correlation Matrix
  </text>

  <!-- labels -->
  <text x="95"  y="48" text-anchor="middle" font-size="10" fill="#666">A</text>
  <text x="155" y="48" text-anchor="middle" font-size="10" fill="#666">B</text>
  <text x="215" y="48" text-anchor="middle" font-size="10" fill="#666">C</text>
  <text x="275" y="48" text-anchor="middle" font-size="10" fill="#666">D</text>

  <text x="55" y="95"  text-anchor="end" font-size="10" fill="#666">A</text>
  <text x="55" y="155" text-anchor="end" font-size="10" fill="#666">B</text>
  <text x="55" y="215" text-anchor="end" font-size="10" fill="#666">C</text>
  <text x="55" y="275" text-anchor="end" font-size="10" fill="#666">D</text>

  <!-- red-green diverging scheme, collapses under CVD -->
  <!-- Row A -->
  <rect x="65"  y="55"  width="55" height="55" fill="#1b7837"/>  <!-- A-A: +1.0 -->
  <rect x="125" y="55"  width="55" height="55" fill="#a6dba0"/>  <!-- A-B: +0.5 -->
  <rect x="185" y="55"  width="55" height="55" fill="#d6604d"/>  <!-- A-C: -0.6 -->
  <rect x="245" y="55"  width="55" height="55" fill="#f7f7f7"/>  <!-- A-D: 0.0 -->

  <!-- Row B -->
  <rect x="65"  y="115" width="55" height="55" fill="#a6dba0"/>  <!-- B-A: +0.5 -->
  <rect x="125" y="115" width="55" height="55" fill="#1b7837"/>  <!-- B-B: +1.0 -->
  <rect x="185" y="115" width="55" height="55" fill="#b2182b"/>  <!-- B-C: -0.9 -->
  <rect x="245" y="115" width="55" height="55" fill="#fddbc7"/>  <!-- B-D: -0.2 -->

  <!-- Row C -->
  <rect x="65"  y="175" width="55" height="55" fill="#d6604d"/>  <!-- C-A: -0.6 -->
  <rect x="125" y="175" width="55" height="55" fill="#b2182b"/>  <!-- C-B: -0.9 -->
  <rect x="185" y="175" width="55" height="55" fill="#1b7837"/>  <!-- C-C: +1.0 -->
  <rect x="245" y="175" width="55" height="55" fill="#d9f0d3"/>  <!-- C-D: +0.3 -->

  <!-- Row D -->
  <rect x="65"  y="235" width="55" height="55" fill="#f7f7f7"/>  <!-- D-A: 0.0 -->
  <rect x="125" y="235" width="55" height="55" fill="#fddbc7"/>  <!-- D-B: -0.2 -->
  <rect x="185" y="235" width="55" height="55" fill="#d9f0d3"/>  <!-- D-C: +0.3 -->
  <rect x="245" y="235" width="55" height="55" fill="#1b7837"/>  <!-- D-D: +1.0 -->

  <!-- Legend -->
  <g class="legend" transform="translate(60, 310)">
    <text x="0" y="10" font-size="9" fill="#666">-1</text>
    <rect x="18"  y="0" width="40" height="14" fill="#b2182b"/>
    <rect x="60"  y="0" width="40" height="14" fill="#d6604d"/>
    <rect x="102" y="0" width="40" height="14" fill="#fddbc7"/>
    <rect x="144" y="0" width="40" height="14" fill="#f7f7f7" stroke="#ccc" stroke-width="0.5"/>
    <rect x="186" y="0" width="40" height="14" fill="#d9f0d3"/>
    <rect x="228" y="0" width="40" height="14" fill="#a6dba0"/>
    <rect x="270" y="0" width="40" height="14" fill="#1b7837"/>
    <text x="315" y="10" font-size="9" fill="#666">+1</text>
  </g>
</svg>"""


if __name__ == "__main__":
    print("Generating test SVGs...\n")

    write_svg("01_categorical_fail_stacked_bar.svg", CATEGORICAL_FAIL)
    write_svg("02_sequential_fail_heatmap.svg", SEQUENTIAL_FAIL)
    write_svg("03_diverging_fail_election.svg", DIVERGING_FAIL)
    write_svg("04_categorical_pass_bar.svg", CATEGORICAL_PASS)
    write_svg("05_sequential_pass_blue.svg", SEQUENTIAL_PASS)
    write_svg("06_categorical_fail_scatter.svg", CATEGORICAL_MULTI_FAIL)
    write_svg("07_diverging_fail_correlation.svg", CORRELATION_HEATMAP)

    print(f"\nGenerated 7 test SVGs in {OUTPUT_DIR}/")
    print("  - 01: Categorical FAIL (red/green/orange stacked bar)")
    print("  - 02: Sequential FAIL (green-yellow-red heatmap, lightness reversal)")
    print("  - 03: Diverging FAIL (red-white-green temperature anomaly)")
    print("  - 04: Categorical PASS (blue+orange bar chart)")
    print("  - 05: Sequential PASS (single-hue blue ramp)")
    print("  - 06: Categorical FAIL (6 confusable species in scatter)")
    print("  - 07: Diverging FAIL (red-white-green correlation heatmap)")
