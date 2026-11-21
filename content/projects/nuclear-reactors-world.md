Project page: Where reactors are being built.
How to edit: see content/README.md.

Placeholders available on this page (filled from src/data/nuclear-reactors-world/):
{world_operating} {world_construction} {world_planned} {world_proposed}
{world_construction_active}  = under construction minus the 6 suspended units
{china_construction} {china_planned} {china_sites}  = Chinese sites with a unit under construction
{others_construction} {others_countries}  = units and countries outside China
{firsts_construction}  = units building in Egypt, Turkey and Bangladesh together
{big3_planned}  = planned units in China, Russia and India together
{india_construction} {russia_construction} {pakistan_construction}
{us_operating} {france_operating} {japan_operating}
{sites} {approx_sites}

[[page]]
title: Where reactors are being built
description: Nuclear power reactors operating, under construction and planned, site by site, and the country building half of the new ones.
eyebrow: Nuclear power reactors, November 2026

[[intro]]
# Half of the reactors under construction today are in China: *{china_construction}* of {world_construction}

The world has {world_operating} nuclear power reactors connected to the grid, and {world_construction} more are being built. A reactor counts as under construction once the first concrete for it has been poured.

The map shows every site. Blue dots are reactors in operation, red dots are reactors under construction, and rings are the {world_planned} planned ones, which have approval, funding or a firm commitment but no construction yet.

[[key-figures]]
- Operating | {world_operating}
- Under construction | {world_construction}
- Planned | {world_planned}
- Building in China | {china_construction} of {world_construction}

[[insights]]
1. Switch the map to **East Asia**. China's {china_construction} units sit at {china_sites} sites, and every one of them is in a coastal province.
2. **Egypt, Turkey and Bangladesh** have no reactor running yet. Together they are building {firsts_construction}, all of them Russian VVER designs.
3. **China, Russia and India** hold {big3_planned} of the {world_planned} planned units. China alone has {china_planned}.

[[after-chart]]
China is building {china_construction} of those {world_construction}, at {china_sites} sites, all of them in coastal provinces. The other {others_construction} are spread over {others_countries} countries. India is building {india_construction} and Russia {russia_construction}. The United States runs the largest fleet, {us_operating} reactors, and is building none.

[[notes]]
## Notes and method

### What is counted

Reactor units, not plant capacity. Counts come from the World Nuclear Association table dated 11 November 2026. **Operable** means connected to the grid. **Under construction** means the first concrete for the reactor has been poured. **Planned** means approvals, funding or a commitment are in place, with most units expected to operate within 15 years. The {world_proposed} proposed units, with very uncertain timing, are left out.

### Suspended construction

Six of the {world_construction} units under construction have their construction suspended: Carem25 in Argentina, Angra 3 in Brazil, Ohma 1 and Shimane 3 in Japan, and Khmelnitski 3 and 4 in Ukraine. All six are outside China. Without them, China would be building {china_construction} of {world_construction_active}.

### Sites on the map

Each unit is assigned to a site from the Global Energy Monitor tracker by plant name, and the dot sits at the median position of that site's units. {approx_sites} of the {sites} sites only have an approximate location in the tracker; the reading card says so. Three planned units are counted but not drawn: Reftinskaya 1 in Russia, which has no location in the tracker, and the two French units the World Nuclear Association counts without naming a site. Dot area is proportional to the number of units.

### Where the sources disagree

The World Nuclear Association country profiles do not list France's and the United States' operating units, or Pakistan's unit under construction. Those come from the tracker, whose counts match the table ({france_operating}, {us_operating} and {pakistan_construction}). The China profile lists San'ao 4 and Xuwei HTR-PM 600-1 as both planned and under construction; they are counted once, as under construction. Japan has {japan_operating} operable units in this count, while the tracker lists 15 as operating.

### Cross-check

The IAEA Power Reactor Information System, read on 11 November 2026, lists 418 reactors in operation and 21 in suspended operation, 439 in all, against {world_operating} operable here. It lists 77 under construction, against {world_construction}.

### Sources

[World Nuclear Association, World Nuclear Power Reactors & Uranium Requirements](https://world-nuclear.org/information-library/facts-and-figures/world-nuclear-power-reactors-and-uranium-requireme) and [country profiles](https://world-nuclear.org/information-library/country-profiles), accessed 11 November 2026. [Global Energy Monitor, Global Nuclear Power Tracker](https://globalenergymonitor.org/projects/global-nuclear-power-tracker/), August 2026 release, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [IAEA PRIS](https://pris-stats.iaea.org/), accessed 11 November 2026. Coastlines from Natural Earth via [world-atlas](https://github.com/topojson/world-atlas).

Numbers computed in `analysis/nuclear-reactors-world/build_data.py`.
