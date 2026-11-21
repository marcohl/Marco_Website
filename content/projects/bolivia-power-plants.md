Project page: Where Bolivia makes its electricity.
How to edit: see content/README.md.

Placeholders available in the page text (filled from src/data/bolivia-power-plants/):
{plants} {capacity_mw} {generation_gwh}       grid totals, end of 2025
{top3_capacity_pct} {top3_generation_pct}     Cochabamba + Santa Cruz + Tarija share
{gas_mw} {gas_pct} {hydro_mw} {gas_cf}        gas fleet MW, % of capacity, hydro MW, gas capacity factor %
{gas_cc_mw} {gas_oc_mw} {gas_oc_cf} {engines_mw}
{carrasco_mw} {carrasco_gwh}
{zongo_n} {zongo_mw} {zongo_cf}
{santa_cruz_gwh} {cochabamba_gwh} {la_paz_mw} {la_paz_plants}
{approx_n} {approx_mw}                        plants with approximate location
{first_year} {first_gwh} {first_gas_pct}      history, first year
{peak_year} {peak_gas_pct}                    year with the highest gas share
{last_year} {last_gwh} {last_gas_pct} {growth}

[[page]]
title: Where Bolivia makes its electricity
description: Every power plant on Bolivia's national grid, how big it is, how much it produced in 2025, and how the mix changed since 1996.
eyebrow: Bolivia's national grid, end of 2025

[[intro]]
# *{top3_capacity_pct}%* of Bolivia's power capacity sits in three departments

At the end of 2025, Bolivia's national grid had {plants} power plants with {capacity_mw} MW of capacity. That year they produced {generation_gwh} GWh. Cochabamba, Santa Cruz and Tarija hold {top3_capacity_pct}% of the capacity and made {top3_generation_pct}% of the electricity.

Each circle on the map is one plant. Switch it from capacity to generation and some of the biggest gas plants shrink to a dot.

[[key-figures]]
- Capacity, end of 2025 | {capacity_mw} MW
- Generation 2025 | {generation_gwh} GWh
- Plants on the grid | {plants}
- Cochabamba, Santa Cruz, Tarija | {top3_capacity_pct}%

[[insights]]
1. **Gas turbines barely ran.** The open-cycle turbines add up to {gas_oc_mw} MW and ran at {gas_oc_cf}% of their capacity in 2025. Carrasco, with {carrasco_mw} MW, produced {carrasco_gwh} GWh. The combined cycles did the work.
2. **The Zongo valley**, north of La Paz, has {zongo_n} hydro plants and {zongo_mw} MW. They ran at {zongo_cf}% of their capacity, against {gas_cf}% for the gas fleet.
3. **Cochabamba has the most capacity, Santa Cruz makes the most electricity:** {santa_cruz_gwh} GWh against {cochabamba_gwh} GWh in 2025. Switch the bars to generation to see the swap.

[[after-chart]]
Most of that capacity burns natural gas: {gas_mw} MW, or {gas_pct}%. The large gas plants sit in the eastern lowlands. Guaracachi is in Santa Cruz city and Warnes just north of it. Entre Ríos, Bulo Bulo and Carrasco are in the tropical lowlands of Cochabamba, and Del Sur is near Yacuiba, in the Chaco of Tarija.

Hydro holds most of the rest, {hydro_mw} MW, in the Andean valleys of Cochabamba and La Paz. La Paz has the most plants, {la_paz_plants}, but they are small: together {la_paz_mw} MW.

[[history-intro]]
## Gas made {first_gas_pct}% of the electricity in {first_year}, {peak_gas_pct}% in {peak_year} and {last_gas_pct}% in {last_year}

The grid produced {last_gwh} GWh in {last_year}, {growth} times the {first_gwh} GWh of {first_year}. Gas plants covered most of that growth. Their share peaked in {peak_year}. It fell as Misicuni, the San José hydro plants and the large solar and wind farms came online between 2017 and 2021.

[[history-key-figures]]
- Gas share, {first_year} | {first_gas_pct}%
- Peak, {peak_year} | {peak_gas_pct}%
- {last_year} | {last_gas_pct}%

[[notes]]
## Notes and method

### What is counted

Only the national grid (Sistema Interconectado Nacional, SIN), which the CNDC dispatches. Isolated systems and self-producers are left out. **Capacity** is the CNDC figure for the end of 2025: effective capacity, with thermal units rated at the mean temperature of their site. It is not nameplate capacity. **Generation** is gross generation in 2025, before the plants' own consumption. The **capacity factor** is generation divided by capacity times 8,760 hours, using year-end capacity.

### Technologies

Natural gas groups combined cycles ({gas_cc_mw} MW), open-cycle gas turbines ({gas_oc_mw} MW), and the diesel and dual-fuel engines at Moxos and Aranjuez ({engines_mw} MW). Biomass plants are at sugar mills. A plant that mixes technologies, such as Guaracachi or Warnes, takes the color of its largest part; the reading card gives the split. Santa Rosa BC and AC, and Uyuni phases I and II, are shown as one plant each.

### Locations

Coordinates come from the Global Energy Monitor tracker and from OpenStreetMap. {approx_n} small plants ({approx_mw} MW) have no published position; they are placed at the village or town they belong to and drawn with a dashed outline. Each plant's department is found from its coordinates. The result matches the CNDC's 2025 generation by department to within 0.05 GWh.

### Where the sources disagree

The Global Energy Monitor tracker lists the Umapalca (85 MW) and Palillada (118 MW) hydro plants in La Paz as operating. The CNDC does not include them in the grid at the end of 2025, and this map follows the CNDC. The CNDC's [online chart](https://www.cndc.bo/historico-generacion/) gives 9,999.8 GWh for 2021 and 10,604.9 GWh for 2022; its annual report and data files give 9,966.2 and 10,599.5, used here. Six of the CNDC's yearly generation files (2006, 2011, 2013, 2016, 2017, 2019) stop before December, so the history comes from the annual report.

### Sources

CNDC, [Memoria y Resultados 2025](https://www.cndc.bo/wp-content/uploads/memorias/memyres_2025.pdf) (capacity by unit, p. 49; generation by source 1996-2025, pp. 103-106) and [yearly gross generation files](https://www.cndc.bo/estadisticas/), accessed 15 November 2026. [Global Energy Monitor, Global Integrated Power Tracker](https://globalenergymonitor.org/projects/global-integrated-power-tracker/), September 2026 release, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, ODbL. Department borders from [Natural Earth](https://www.naturalearthdata.com/).

Numbers computed in `analysis/bolivia-power-plants/build_data.py`.

[[technologies]]
# Names used in the legends, the reading card and the data tables of both charts.
gas: Natural gas
hydro: Hydro
solar: Solar
wind: Wind
biomass: Biomass
gas_cc: Gas, combined cycle
gas_oc: Gas turbines
diesel: Diesel engines
dual_fuel: Dual-fuel engines

[[map-chart]]
# The plant map. Placeholders filled while you use the chart:
# {plants} {dep} {n} {pct} {unit} {a} {b} {top3} {techs} {units} {operator} {note}
circle_size: Circle size
mode_mw: Capacity (MW)
mode_gwh: Generation 2025 (GWh)
department: Department
all_bolivia: All of Bolivia
legend_label: Technology. Select one to highlight it.
approximate: Approximate location
back: Show all of Bolivia
map_description: Map of Bolivia with {plants} power plants of the national grid. Select a department to zoom in. Use the arrow keys to step through plants.
hint: Tap a department to zoom in. Hover or tap a plant to read it.
hint_department: {dep}: {n} plants. Tap one on the map or in the list below.
bars_description: Capacity or 2025 generation by department, split by technology.
bars_title_mw: Capacity by department: {top3} hold {pct}%
bars_title_gwh: Generation 2025 by department: {top3} made {pct}%
list_title_mw: Plants in {dep}, by capacity
list_title_gwh: Plants in {dep}, by 2025 generation
size_key: {a} and {b} {unit}
zongo: Zongo valley
zongo_plants: {n} hydro plants
card_capacity: Capacity
card_generation: Generation 2025
card_factor: Capacity factor
line_barely: Barely ran in 2025.
line_high: Ran at {pct}% of its capacity over the year.
line_mid: Produced {pct}% of what it could at full power all year.
plant_details: {techs}. {units}. Operator: {operator}.
unit_one: 1 unit
unit_many: {n} units
approx_note: Location approximate: {note}
table_summary: Show the data: the {plants} plants
table_caption: CNDC, Memoria y Resultados 2025 (capacity at the end of 2025) and generación bruta 2025. Capacity factor = generation / (capacity x 8,760 h). * Location approximate.
col_plant: Plant
col_technology: Technology
col_department: Department
col_mw: MW
col_gwh: GWh 2025
col_factor: Capacity factor
total_row: SIN

[[history-chart]]
# The 1996-2025 columns. Placeholders: {first} {last} {first_gwh} {last_gwh} {pct}
legend_label: Source. Select one to highlight it.
chart_description: Stacked columns of yearly gross generation by source, {first} to {last}. Total grew from {first_gwh} to {last_gwh} GWh. Use the arrow keys to read each year.
y_axis: GWh a year
card_line: Natural gas made {pct}% of the electricity this year.
table_summary: Show the data: generation by source, {first}-{last}
table_caption: GWh. CNDC, Memoria y Resultados 2025, "Producción bruta (GWh) periodo 1996-2025". Natural gas includes small diesel and dual-fuel output.
col_year: Year
col_total: Total
