# Lab 6: Visualizing Population Distribution with Streamlit

TFB3133/TEB3133 Data Visualization, Sept 2026.

An interactive choropleth map of Malaysia's states built with Streamlit, GeoPandas and Folium. All values are randomly generated for the lab; they are not real statistics.

## Features
- Switch between Population and GDP datasets
- Adjust the random value range with a slider
- Choose the colour scheme (YlOrRd, BuGn, Blues, Greens, and more)
- Add imaginary states to see how they affect the table and colour scale
- Hover over a state to see its value

## Run locally
```bash
pip install -r requirements.txt
streamlit run map_population.py
```

## Files
| File | Purpose |
|---|---|
| `map_population.py` | The Streamlit app |
| `malaysia_states.geojson` | State boundaries (DOSM open data, `administrative_1_state.geojson`) |
| `make_figures.py` | Optional: exports static PNGs of each experiment |
| `REPORT.md` | Reflection report (Task 3) |
| `screenshots/` | Map images used in the report |

## Notes
The GeoJSON stores state names under `properties.state` and spells Penang, Kuala Lumpur, Labuan and Putrajaya as "Pulau Pinang", "W.P. Kuala Lumpur", "W.P. Labuan" and "W.P. Putrajaya". The app maps the lab's names to these so every state is coloured.

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub (public, or private with access granted).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, select the repository, branch `main`, and main file `map_population.py`.
4. Under **Advanced settings**, choose Python 3.12 or newer, then deploy.
