Project page: More reactors, smaller slice (nuclear capacity vs share, DNV ETO 2026).
How to edit: see content/README.md.
Numbers typed by hand come from the DNV main report (sec. 4.5) and are listed in [[notes]]:
17.5% (1996 peak), 1,000 GW commissioned and 260 GW replacing retirements, 310 GW of SMRs in 2060.

Placeholders available in the page text (filled from src/data/nuclear-capacity-vs-share/):
{first} {last}                                 first and last forecast year (2025, 2060)
{cap_first} {cap_2040} {cap_last} {fold}      world nuclear capacity, GW, and growth multiple
{share_first} {share_2040} {share_last}       nuclear share of world electricity, %
{share_low} {low_year}                         lowest share and its year
{nuc_first} {nuc_last}                         world nuclear generation, TWh
{tot_first} {tot_last}                         world electricity generation, all sources, TWh
{nuc_growth} {tot_growth}                      growth 2025-2060, %
{lf_first} {lf_last}                           implied world load factor
{gen_fold}                                     nuclear generation growth multiple, 2025-2060
{eur_cap_first} {eur_cap_last} {eur_share_first} {eur_share_last}
{nam_cap_first} {nam_cap_last} {nam_share_first} {nam_share_last}
{chn_cap_first} {chn_cap_last} {chn_share_first} {chn_share_last}

[[page]]
title: More reactors, smaller slice
description: DNV expects the world's nuclear fleet to almost triple by 2060. Nuclear's share of the world's electricity ends that period lower than today.
eyebrow: Nuclear power to 2060

[[intro]]
# Nuclear capacity grows *{fold} times* by {last}. Its share of the world's electricity does not.

Every year DNV, a Norwegian quality assurance and risk management company, publishes a forecast of the world's energy system. Its 2026 edition expects the world's reactor fleet to grow from {cap_first} GW in {first} to {cap_last} GW in {last}.

Nuclear's share of global electricity falls until {low_year}, from {share_first}% to {share_low}%. It then climbs back to {share_last}% by {last}, still below today. The record was 17.5% in 1996.

The rest of the grid grows faster. DNV expects world electricity generation to rise {tot_growth}%, from {tot_first} to {tot_last} TWh. Nuclear generation rises {nuc_growth}%.

[[fleet-figure]]
# Isotype figure beside the headline. Placeholders: {unit} {first} {last} {cap_first} {cap_last} {share_first} {share_last}
description: Pictogram. Each cooling tower stands for {unit} GW of nuclear capacity: about {towers_first} towers in {first} and {towers_last} in {last}. Below, two grids of 100 squares show nuclear's share of world electricity: {share_first}% in {first} and {share_last}% in {last}.
unit_key: Each tower = {unit} GW of reactors
share_key: Each square = 1% of the world's electricity
share_label: {share}% from nuclear

[[after-trend]]
Two more things hold nuclear back. Part of the new building only replaces old reactors: of the 1,000 GW DNV expects to come online by {last}, 260 GW makes up for closures, almost all of it in North America and Europe. And reactors run fewer hours. When solar and wind produce at almost no cost, reactors turn down. The world fleet's load factor drops from {lf_first} to {lf_last}, so generation grows {gen_fold} times while capacity grows {fold} times.

The share recovers after {low_year} because DNV expects small modular reactors to be built in large numbers, reaching 310 GW by {last}. DNV says this rests on a fall in their cost that no Western market has shown yet. If the cost does not fall, the share stays close to 7%.

[[region-intro]]
## Europe and North America build reactors and still lose share

Europe adds reactors, from {eur_cap_first} to {eur_cap_last} GW. Its nuclear share falls from {eur_share_first}% to {eur_share_last}%. North America goes from {nam_cap_first} to {nam_cap_last} GW, and its share from {nam_share_first}% to {nam_share_last}%. Greater China builds the most, from {chn_cap_first} to {chn_cap_last} GW, and its share rises from {chn_share_first}% to {chn_share_last}%.

Red marks the regions that add capacity and lose share. Switch the chart to capacity: the red rows that fall on share rise on capacity.

[[notes]]
## Notes and method

### What is shown

DNV's single "most likely" forecast, not a scenario. {first} is DNV's base-year estimate; every later year is forecast. **Capacity** is installed nuclear capacity in GW, including behind-the-meter units. **Generation** is electricity generated in TWh a year, including off-grid and behind-the-meter output. **Share** is nuclear generation divided by generation from all sources, same boundary. The **load factor** is nuclear generation divided by capacity times 8,760 hours.

### Where the numbers differ

The world values are the sum of DNV's 10 regions and match the main report to the rounding it uses. One exception: the report text gives Europe's share in 2040 as 10%; the dataset gives 10.6%, used here.

These numbers come from the report text, not the dataset: the 17.5% share in 1996 (DNV citing Thunder Said Energy, 2025), the 1,000 GW commissioned and 260 GW replacing closures to 2060, the 310 GW of small modular reactors in 2060, and the "close to 7%" share if their cost does not fall (pp. 71-74).

### Sources

DNV, [Energy Transition Outlook 2026](https://eto.dnv.com), main report section 4.5 (pp. 70-74), and the [forecast data workbook](https://www.dnv.com/eto-data), sheet "Power supply", accessed 21 November 2026. This work is partially based on data developed by DNV AS, ©DNV AS. 2026, but the resulting work has been prepared by Marco Herbas Lopez and does not necessarily reflect the views of DNV AS.

Numbers computed in `analysis/nuclear-capacity-vs-share/build_data.py`.

[[regions]]
# Region names in the regional chart and table (DNV region codes).
NAM: North America
LAM: Latin America
EUR: Europe
SSA: Sub-Saharan Africa
MEA: Middle East, N. Africa
NEE: North East Eurasia
CHN: Greater China
IND: Indian Subcontinent
SEA: South East Asia
OPA: OECD Pacific

[[trend-chart]]
# Two stacked panels. Placeholders: {first} {last} {cap_first} {cap_last} {share_first} {share_low} {low_year} {share_last} {fold}
chart_description: Two charts on one time axis, {first} to {last}. Top: world nuclear capacity rises from {cap_first} to {cap_last} GW. Bottom: nuclear's share of world electricity goes from {share_first}% to a low of {share_low}% in {low_year} and {share_last}% in {last}. Use the arrow keys to read each year.
cap_title: Nuclear capacity, GW
share_title: Nuclear share of world electricity, %
ref_label: {first} level, {share_first}%
low_label: Low: {share_low}% in {low_year}
fold_label: ×{fold}
card_capacity: Capacity
card_nuclear: Nuclear generation
card_total: All electricity
card_share: Nuclear share
card_line: Of every 100 kWh generated, {kwh} kWh come from nuclear.
hint: Hover or tap the chart to read a year.
table_summary: Show the data: world, {first}-{last}
table_caption: DNV Energy Transition Outlook 2026, forecast data. Capacity incl. behind-the-meter; generation incl. off-grid and behind-the-meter.
col_year: Year
col_capacity: Capacity (GW)
col_nuclear: Nuclear (TWh)
col_total: All sources (TWh)
col_share: Nuclear share
col_lf: Load factor

[[region-chart]]
# The dumbbell chart. Placeholders: {first} {last} {cap0} {cap1} {s0} {s1} {pct}
mode_label: Show
mode_share: Share of electricity
mode_capacity: Capacity
description_share: Nuclear share of electricity in DNV's 10 regions, {first} and {last}. Use the arrow keys to read each region.
description_capacity: Installed nuclear capacity in DNV's 10 regions, {first} and {last}. Use the arrow keys to read each region.
axis_share: % of the region's electricity
axis_capacity: GW
key_first: {first}
key_last: {last}
key_story: Builds reactors, loses share
key_context: Gains share
line_story: Capacity grows {pct}%, but the share falls from {s0}% to {s1}%.
line_context: Capacity goes from {cap0} to {cap1} GW and the share from {s0}% to {s1}%.
table_summary: Show the data: 10 regions, {first} and {last}
table_caption: DNV Energy Transition Outlook 2026, forecast data. Share = nuclear generation / all generation in the region.
col_region: Region
col_cap0: GW {first}
col_cap1: GW {last}
col_s0: Share {first}
col_s1: Share {last}
