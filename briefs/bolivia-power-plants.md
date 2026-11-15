# Brief: Where Bolivia makes its electricity (working title)

- **Slug:** `bolivia-power-plants`
- **Code:** MHL-004
- **Revision:** A
- **Status:** published 2026-11-15 (text approved, QA passed, OG images done)
- **Started:** 2026-11-15

## The one sentence
"Bolivia's grid runs on two regions: gas turbines in the eastern lowlands and hydro plants in the Andean
valleys. [X] % of SIN capacity sits in Santa Cruz, Tarija and Cochabamba."

[X] and the exact department grouping are set in the data phase. If the data shows a sharper split (for
example lowland gas vs highland/valley hydro by MW or by GWh), the sentence is rewritten around that number.

## Question and reader
- Question the chart answers: where are the power plants of Bolivia's national grid (SIN), what does each one
  use, how big is it, how much does it produce, and how has production changed over the years?
- Main reader: curious general public. Second reader: recruiter or peer who opens the method and code.
- They know Bolivia has gas and mountains. They do not know where the plants are, that most capacity is gas
  fired, that a large share of it sits in a few eastern sites, or that installed capacity and energy produced
  tell different stories (a hydro plant can produce more GWh per MW than a gas peaker).

## Scope
- In the MVP:
  - Map of Bolivia with department borders. One circle per SIN power plant (central), color by technology
    (hydro, gas open cycle, gas combined cycle, solar, wind, biomass; final grouping set from the data).
  - Toggle for circle area: **installed capacity (MW)** or **annual gross generation (GWh)** for the latest
    complete year. Same plants, same positions; the switch shows which plants are built big and which ones
    actually produce.
  - Tooltip / tap panel per plant: operator, department, technology and fuel, number of units, installed and
    effective MW, GWh in the year, capacity factor (computed), commissioning year where the source gives it.
  - Historical chart: annual gross generation of the SIN by technology from the first year with plant-level
    CNDC data (target 1992) to the latest complete year. Colors match the map.
  - Bar of installed MW by department (supports the thesis).
  - Plant table in `<details>` (sortable) as text alternative.
- Explicitly out (maybe a v2):
  - Isolated systems (Sistemas Aislados) and self-producers (autoproductores).
  - Plants announced or under construction; retired plants as map marks (they may still appear in the
    historical totals).
  - Transmission lines (STI) as a map layer.
  - Prices, costs, dispatch, hourly or monthly profiles.
  - Year slider on the map (plant positions over time).

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| Capacity per plant and unit, end of 2025; capacity and gross production per plant 1996-2025 | CNDC, Memoria y Resultados 2025, https://www.cndc.bo/wp-content/uploads/memorias/memyres_2025.pdf (p. 49 "Capacidad de generación en el SIN a fines del 2025"; tables "Capacidad de generación por central" and "Producción bruta" 1996-2025) | 2026-11-15 | MW (effective, thermal at site mean temperature), GWh | `raw/memyres_2025.pdf`, 10,327,105 bytes. Read in Chrome, downloaded via Chrome to Marco's Mac |
| Gross generation per unit, monthly, 2005-2026 | CNDC, Estadísticas anuales, `https://www.cndc.bo/wp-content/uploads/mem/estadisticas/anual/<year>/genbruta_<year>.<ext>` | 2026-11-15 | MWh | `raw/genbruta_2005..2026` (.xls/.xlsx/.zip). 2026 is partial. 2025 file also has a "MWh - DEPAR" sheet (production by department) |
| Annual SIN generation by source 2016-2025 | CNDC, https://www.cndc.bo/historico-generacion/ | 2026-11-15 | GWh | Reference values only (2025: 11,795.7 GWh) |
| Plant coordinates (36 of 47 plants exact) | Global Energy Monitor, Global Integrated Power Tracker, September 2026 release, https://globalenergymonitor.org/projects/global-integrated-power-tracker/download-data/ | 2026-11-15 (file from Marco) | WGS84 | CC BY 4.0. Source xlsx is 34 MB, not committed (sha256 34749042...ee27); `raw/gem_gipt_2026-09_bolivia.csv` keeps the 108 Bolivia rows (`extract_sources.py`) |
| Plant coordinates GEM lacks; locality points | OpenStreetMap via Overpass API and Nominatim, read in Chrome | 2026-11-15 | WGS84 | ODbL. `raw/osm_power_plants_bo_2026-11-15.csv` (all `power=plant`), `raw/osm_named_power_bo_2026-11-15.csv`; other OSM ids are cited per plant in `plant_locations.csv` |
| Department borders | Natural Earth 10m admin-1, https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_1_states_provinces.geojson | 2026-11-15 | WGS84 | Public domain. Bolivia only, `raw/ne_10m_admin_1_bolivia.geojson` |

Derived inputs (committed, reproducible):
- `cndc_capacity_2025.csv`: Memoria 2025 p. 49 transcribed by hand, unit level for thermal plants. Checked against
  every subtotal on the page.
- `memoria_production_by_source_1996_2025.csv`: Memoria pp. 103-106, subtotal and total rows, extracted with
  `pdftotext -layout` by `extract_sources.py`.
- `plant_locations.csv`: one row per plant with source, OSM/GEM reference and precision (exact / approximate).

Known reference values to check against (read from CNDC Memoria 2025, p. 14 and p. 49):
- SIN capacity at end of 2025, mean temperature: 3,530.90 MW = hydro 715.81 + wind 135.00 + solar 167.58 +
  thermal and biomass 2,512.51 (thermal gas 2,387.51; biomass 125.00).
- SIN gross production 2025: 11,795.7 GWh (genbruta_2025: 11,795,718.24 MWh).
- 2025 production by department (genbruta_2025, sheet "MWh - DEPAR"): Santa Cruz 4,204.0, Cochabamba 4,039.3,
  Tarija 1,702.1, La Paz 1,475.2, Oruro 202.2, Potosí 141.7, Chuquisaca 31.2, Beni 0.01 GWh.
- Sum of plant rows equals the published SIN totals for every year of the historical series.

Checks in `build_data.py` (all pass, run 2026-11-15):
- Capacity by CNDC type and total (3,530.90 MW), unit counts (hydro 54, wind 40, solar 62, thermal 82), plant
  subtotals on p. 49.
- genbruta 2025: every unit assigned to a plant; units sum to the file total; total 11,795.7 GWh; generation by
  type equals Memoria p. 16 (combined cycle 7,210.69; hydro 3,354.21; solar 355.48; biomass 345.06; wind 289.89;
  gas turbines 240.38 GWh).
- Department of each plant by point-in-polygon; 2025 generation by department equals the CNDC sheet
  "MWh - DEPAR" within 0.05 GWh for all departments.
- History: sources add up to the Memoria total (max gap 0.1 GWh); totals equal every complete genbruta file
  2005-2025. Six genbruta files are incomplete on the CNDC site (2006: 2 months, 2011: 4, 2013: 11, 2016: 9,
  2017: 4, 2019: 4) and are not used for the history.
- Known discrepancy: the CNDC web chart (historico-generacion) shows 9,999.8 GWh for 2021 and 10,604.9 GWh for
  2022; Memoria and genbruta give 9,966.2 and 10,599.5. We use the Memoria.

Result (end of 2025):
- 47 plants, 3,530.9 MW, 11,795.7 GWh. 11 plants (205.7 MW, 5.8 %) placed at their locality, flagged approximate.
- Capacity by department: Cochabamba 1,269.2 MW, Santa Cruz 1,186.5, Tarija 518.4, La Paz 353.3, Oruro 100.0,
  Potosí 62.6, Chuquisaca 35.2, Beni 5.7. Cochabamba + Santa Cruz + Tarija = 2,974.1 MW = 84.2 %.
- Generation 2025 by department: Santa Cruz 4,204.0 GWh, Cochabamba 4,039.3, Tarija 1,702.1, La Paz 1,475.2.
- GEM lists Umapalca (85 MW) and Palillada (118 MW) as operating; CNDC does not list them in the SIN at the end of
  2025. We follow CNDC and say so on the page.

## Form and interaction
- Chart form and why: proportional-symbol map, because the thesis is about where capacity sits. Area (not
  radius) proportional to MW or GWh. Historical generation as stacked area or stacked bars by technology
  (part-of-whole over time, about 30 years); department capacity as a sorted bar.
- Interaction: MW / GWh toggle on the map (reveals the gap between built and used capacity); tooltip per
  plant; legend highlight by technology shared between map and history chart.
- Phone layout: map full width, toggle above it, plant detail as a panel under the map on tap; history chart
  and bar stacked below.

## Open questions
- Reference year: latest complete year published by CNDC (2025 if available, otherwise 2024).
- Plant vs unit: one circle per central; units listed in the tooltip. Plants with mixed technology
  (e.g. open cycle units plus a steam unit in combined cycle) need a rule.
- History by technology (Marco, 2026-11-15).
- Effective vs installed MW: the map uses installed (Marco's choice); effective goes in the tooltip.
