"""Optional helper: export static PNG versions of the Task 2 experiments.

These are matplotlib renders of the same data and colour schemes, meant as a
fallback for the report. For the official screenshots, run the Streamlit app
and screenshot the Folium map itself.
"""
import os
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import map_population as mp

os.makedirs("screenshots", exist_ok=True)
gdf = gpd.read_file(mp.GEOJSON_PATH)

SCENARIOS = [
    ("01_baseline_population", "Population", 500_000, 5_000_000, "YlOrRd", False),
    ("02_population_1m_10m", "Population", 1_000_000, 10_000_000, "YlOrRd", False),
    ("03_gdp_yellow_orange_red", "GDP", 10_000, 100_000, "YlOrRd", False),
    ("04_gdp_bugn", "GDP", 10_000, 100_000, "BuGn", False),
    ("05_population_blues", "Population", 500_000, 5_000_000, "Blues", False),
    ("06_population_greens", "Population", 500_000, 5_000_000, "Greens", False),
    ("07_imaginary_states", "Population", 500_000, 5_000_000, "YlOrRd", True),
]

for name, metric, low, high, cmap, fake in SCENARIOS:
    data = mp.generate_data(metric, low, high, 42, mp.IMAGINARY_STATES if fake else None)
    if fake:
        data.loc[data.State == "Atlantis", metric] = 9_000_000
    merged = gdf.merge(data, left_on="state", right_on="GeoName", how="left")
    fig, ax = plt.subplots(figsize=(10, 5))
    merged.plot(column=metric, cmap=cmap, legend=True, ax=ax, edgecolor="grey",
                linewidth=0.3, vmin=data[metric].min(), vmax=data[metric].max(),
                legend_kwds={"label": metric, "shrink": 0.7})
    ax.set_title(f"{metric} | {cmap} | range {low:,} to {high:,}" + (" | + imaginary states" if fake else ""))
    ax.set_axis_off()
    fig.savefig(f"screenshots/{name}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(name, int(data[metric].min()), int(data[metric].max()))
