"""TFB3133/TEB3133 Data Visualization - Lab 6
Visualizing Population Distribution using Streamlit, GeoPandas and Folium.

Run locally:
    streamlit run map_population.py
"""

import geopandas as gpd
import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

GEOJSON_PATH = "malaysia_states.geojson"

STATES = [
    "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
    "Pahang", "Penang", "Perak", "Perlis", "Sabah", "Sarawak",
    "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya",
]

# The GeoJSON used here (DOSM open data) stores state names under the
# property "state" and spells some of them differently from the lab's list.
# Without this mapping, Penang, Kuala Lumpur, Labuan and Putrajaya would
# silently stay grey on the map.
NAME_TO_GEOJSON = {
    "Penang": "Pulau Pinang",
    "Kuala Lumpur": "W.P. Kuala Lumpur",
    "Labuan": "W.P. Labuan",
    "Putrajaya": "W.P. Putrajaya",
}

IMAGINARY_STATES = ["Atlantis", "Narnia", "Wakanda"]

SEED_OFFSET = {"Population": 0, "GDP": 1000}

COLOR_SCHEMES = ["YlOrRd", "BuGn", "Blues", "Greens", "Purples", "RdPu", "YlGnBu"]

DATASETS = {
    "Population": {"low": 500_000, "high": 5_000_000, "unit": "people"},
    "GDP": {"low": 10_000, "high": 100_000, "unit": "RM million"},
}


def generate_data(metric, low, high, seed, extra_states=None):
    """Generate random values for each state.

    A fixed seed keeps the numbers stable between Streamlit reruns, so the
    map only changes when the user actually changes a setting.
    """
    # Each dataset gets its own offset. With the same seed, numpy would
    # otherwise return the same random pattern for Population and GDP (just
    # rescaled), and the two maps would look identical.
    rng = np.random.default_rng(seed + SEED_OFFSET[metric])
    states = STATES + list(extra_states or [])
    values = rng.integers(low, high, size=len(states))
    data = pd.DataFrame({"State": states, metric: values})
    data["GeoName"] = data["State"].replace(NAME_TO_GEOJSON)
    return data


@st.cache_data
def load_map():
    return gpd.read_file(GEOJSON_PATH)


def plot_map(malaysia_map, data, metric, color):
    m = folium.Map(location=[4.2105, 108.0], zoom_start=6)

    folium.Choropleth(
        geo_data=malaysia_map,
        name=f"{metric} Distribution",
        data=data,
        columns=["GeoName", metric],
        key_on="feature.properties.state",
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{metric} Distribution",
        nan_fill_color="lightgrey",
    ).add_to(m)

    # Hover tooltip with the generated value for each state.
    lookup = data.set_index("GeoName")[metric].to_dict()
    geo = malaysia_map.copy()
    geo[metric] = geo["state"].map(lookup)
    folium.GeoJson(
        geo[["state", metric, "geometry"]],
        style_function=lambda _: {"fillOpacity": 0, "weight": 0},
        tooltip=folium.GeoJsonTooltip(
            fields=["state", metric], aliases=["State:", f"{metric}:"], localize=True
        ),
    ).add_to(m)
    return m


def main():
    st.set_page_config(page_title="Malaysia Distribution Map", layout="wide")
    st.title("Malaysia Population Distribution Map")
    st.caption("TFB3133/TEB3133 Data Visualization, Lab 6. All values are randomly generated.")

    # ---- Sidebar controls (Task 2) ----
    st.sidebar.header("Experiment settings")
    metric = st.sidebar.radio("Dataset", list(DATASETS.keys()))
    cfg = DATASETS[metric]

    low, high = st.sidebar.slider(
        f"{metric} range ({cfg['unit']})",
        min_value=0,
        max_value=cfg["high"] * 2,
        value=(cfg["low"], cfg["high"]),
        step=max(cfg["low"] // 10, 1),
    )
    color = st.sidebar.selectbox("Color scheme", COLOR_SCHEMES)
    seed = st.sidebar.number_input("Random seed", value=42, step=1)
    add_fake = st.sidebar.checkbox("Add imaginary states (Atlantis, Narnia, Wakanda)")

    if low >= high:
        st.error("The minimum must be smaller than the maximum.")
        return

    data = generate_data(metric, low, high, int(seed), IMAGINARY_STATES if add_fake else None)

    left, right = st.columns([1, 2])
    with left:
        st.write(f"Sample {metric} data for states:")
        st.dataframe(data[["State", metric]], hide_index=True, height=520)
        if add_fake:
            st.info(
                "Imaginary states have no polygon in the GeoJSON, so they appear "
                "in the table but cannot be drawn. They still affect the colour "
                "scale, because the legend is built from every row in the data."
            )
    with right:
        malaysia_map = load_map()
        st_folium(
            plot_map(malaysia_map, data, metric, color),
            height=520,
            use_container_width=True,
            returned_objects=[],
        )


if __name__ == "__main__":
    main()
