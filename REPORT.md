# Lab 6 Reflection: Visualizing Distribution Data on a Map

All maps use random seed 42, so changes between maps come from the settings I changed and not from new random draws.

**Changing the population range.** I first widened the range from 500,000 to 5,000,000 to 1,000,000 to 10,000,000. The colour pattern across the states stayed the same, because the same seed produces the same relative ordering and the values simply scaled up (Penang stayed the lowest and Selangor the highest). Only the legend and table numbers changed, from about 0.89 to 4.89 million up to about 1.77 to 9.78 million. This shows that a choropleth encodes relative position within the range, not absolute size.

**Switching to GDP.** GDP used a different random draw, so the pattern changed completely. Kelantan became the lowest (RM 10,628 million) and Johor the highest (RM 77,808 million). Because both datasets are random, they are unrelated to each other, which is unrealistic. Real GDP would likely follow population and industrial activity.

**Changing the colour scheme.** I compared YlOrRd with BuGn, Blues and Greens on the same data. The ordering of states did not change, but the feel of the map did. YlOrRd makes high values look intense or alarming, while Blues and Greens look calmer and suit neutral or environmental topics. Light shades also separated less clearly on some palettes, so adjacent states with similar values were harder to tell apart.

**Adding imaginary states.** Atlantis, Narnia and Wakanda appeared in the table but not on the map, since the GeoJSON has no polygons for them. They still affected the map indirectly. After I gave one of them a value of 9 million, the legend stretched to that maximum, and the real states were pushed into the paler colours. A single outlier can therefore distort how all other regions are read.

**Other observation.** The GeoJSON I used names states differently from the lab's list (for example "Pulau Pinang" and "W.P. Kuala Lumpur"). Without a name mapping, four states would stay grey, so I added one.
