# Brief: Where the world's nuclear reactors run, and where new ones are coming (working title)

- **Slug:** `nuclear-reactors-world`
- **Code:** MHL-003
- **Revision:** A
- **Status:** published locally 2026-11-11 (text approved, QA passed, OG images done); not yet pushed
- **Started:** 2026-11-11

## The one sentence
"Half of the reactors under construction today are in China: 40 of 81."

Confirmed in the data phase: WNA table dated 2026-11-11, China 41 of 82 units under construction (50.0 %).
Proposed wording: "Half of the reactors under construction today are in China: 41 of 82."
Context: 443 operable, 119 planned; China 65 operable and 39 planned; USA 94 operable, 0 under construction.

## Question and reader
- Question the chart answers: where are the reactors that run today, and where are the next ones being built
  or planned?
- Main reader: curious general public. Second reader: recruiter or peer who opens the method and code.
- They know nuclear plants exist and that some countries have many. They do not know that most new
  construction sits in a few countries, that "planned" and "proposed" mean very different things, or that a
  plant (site) usually holds several reactors.

## Scope
- In the MVP:
  - One world map, one mark per site (plant), size = number of reactor units at that site in the selected
    state, position from the dataset coordinates.
  - States: operating, under construction, planned. Filter (toggle) by state; default view shows all three.
  - Counts in reactor units, not GW (see units below).
  - Country table (operating / under construction / planned) in `<details>`, sortable by column.
- Explicitly out (maybe a v2):
  - Proposed reactors (WNA: 336 units, no firm timing or funding).
  - Retired, shelved, cancelled and mothballed units.
  - Capacity in GW as the main measure; timelines and start dates; reactor technology (PWR, BWR, SMR...).
  - Research reactors, naval reactors.

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| Country counts by status (sets every count) | WNA, World Nuclear Power Reactors & Uranium Requirements, https://world-nuclear.org/information-library/facts-and-figures/world-nuclear-power-reactors-and-uranium-requireme | 2026-11-11 (page dated 2026-11-11) | units; MWe net (operable), MWe gross (others) | `raw/wna_reactor_table_2026-11-11.tsv`, cell text read in Chrome |
| Unit and site lists | WNA country profiles, https://world-nuclear.org/information-library/country-profiles (38 pages, dated 2026-02-17 to 2026-11-11) | 2026-11-11 | units | `raw/wna_profiles_2026-11-11_part1-5.txt`, reactor tables only, spaces collapsed; CRC32 per country in `raw/wna_profiles_2026-11-11_crc32.txt` |
| Site coordinates; unit lists WNA lacks | Global Energy Monitor, Global Nuclear Power Tracker, August 2026 release, https://globalenergymonitor.org/projects/global-nuclear-power-tracker/ | 2026-11-11 (file from Marco) | units, MW, WGS84 | CC BY 4.0. Fills France and USA operating units and Pakistan's unit under construction |
| Cross-check, world level | IAEA PRIS, https://pris-stats.iaea.org/ | 2026-11-11 | units, MWe net | `raw/pris_home_2026-11-11.txt`. Country panels are Power BI, not read |

Checks in `build_data.py` (all pass, run 2026-11-11):
- WNA table: country rows sum to the WORLD row in all four states; WORLD 443 / 82 / 119 (proposed 336).
- CRC32 of the 38 profile blocks.
- WNA profiles + GEM fills reproduce the WNA table count for every country and state.
- GEM fills: France 57 and USA 94 operating, Pakistan 1 under construction, each equal to the WNA table.
- Every unit is assigned to a GEM site (aliases listed in the script); one planned unit (Reftinskaya 1, Russia)
  has no site in GEM and is counted but not drawn.
- GEM units of each site lie within 25 km of each other.
- PRIS 2026-11-11: 418 in operation + 21 suspended = 439 (WNA 443); 77 under construction (WNA 82).

Result: China 41 of 82 units under construction = 50.0 %. 218 sites on the map.

Assumptions (stated in `sites.json` meta and to be stated on the page):
- China planned: San'ao 4 and Xuwei HTR-PM 600-1 sit in both the construction and the planned tables of the
  profile; counted once, as under construction. Profile 41 planned, table 39.
- France planned: the table counts 2 units, the profile does not name them. Counted, not drawn (Marco,
  2026-11-11; the earlier Penly placement was dropped).
- Japan planned: profile lists Higashidori 1 (Tepco), table has 0; table used.
- WNA "under construction" includes 6 suspended units (Carem25, Angra 3, Ohma 1, Shimane 3, Khmelnitski 3&4).
  Without them China would be 41 of 76 (54 %). The headline uses WNA's definition.
- WNA vs GEM unit counts differ by 133 summed over sites and states (Japan restarts, GEM "announced" vs WNA
  "planned", recent construction starts). GEM is used for location only.

Definitions (WNA):
- Operable: connected to the grid.
- Under construction: first concrete for the reactor poured (keel laid for floating plants).
- Planned: approvals, funding or commitment in place; mostly expected in operation within 15 years.
- Proposed: specific programme or site proposals, timing very uncertain.

Units: WNA gives operable capacity in MWe net and the other categories in MWe gross, so capacities cannot be
summed across states as published. The page counts units. If GW appear anywhere, they use one basis and say which.

Expected mismatches to explain or resolve in `build_data.py`:
- GEM status names (operating, construction, pre-construction, announced, ...) do not map one-to-one to WNA
  (operable, under construction, planned, proposed). The mapping is a decision for the data phase, stated on the page.
- "Operable" in WNA includes Japanese units connected to the grid but not restarted; GEM and PRIS may classify
  them differently. Count per source and report the difference.
- Taiwan: listed separately by WNA; the map shows it as its own entry, with the source's naming.

## Form and interaction, proposal 2026-11-11 (phase 3, for Marco's OK)

Density measured on `sites.json`: the East China coast box (105-125 E, 18-42 N) holds 32 sites and all 41
Chinese units under construction; Europe 63 sites; north-east USA 38. Largest site: 8 units (Bruce). At 360 px
the Chinese coast is about 30 px wide, so a world view alone cannot show the thesis on a phone.

```
 [h1 headline + 2-3 paragraphs]                 | [title block: 443 operating | 82 under construction |
                                                |  119 planned | China 41 of 82]
 ----------------------------------------------------------------------------------------------
 STAGE  82 squares = 82 units under construction, grouped by country, China block first (41),
        direct labels under each group: China 41, India 8, Russia 7, Egypt 4, Korea 4, Turkey 4, ...
 ----------------------------------------------------------------------------------------------
 [ All | Operating | Under construction | Planned ]      [ World | East Asia | Europe | Americas ]
 +--------------------------------------------------------------------------------------------+
 |  Equal Earth map, land as flat --grid fill, --rule coastline, dashed graticule              |
 |  one circle per site and state, area ~ units:                                               |
 |    operating = filled --cat-1 (.55)   under construction = filled --cat-2   planned = ring  |
 +--------------------------------------------------------------------------------------------+
 reading card: Tianwan, China | 7 operating, 1 under construction | unit names
 [what to look at: 2-3 numbered insights]       [Show the data: country table, sortable]
```

- Colour: red (`--cat-2`) = under construction, on the map and in the squares; operating = `--cat-1`;
  planned = hollow ring in `--cat-1`. State also shown by fill vs ring and by the legend/toggle; China in the
  squares is identified by position and label, not colour. No new colour token.
- Map: d3 `geoEqualEarth`, Natural Earth land 110 m from the `world-atlas` npm package (public domain) read
  with `topojson-client` (two new dependencies). Region buttons refit the projection (600 ms, reduced motion
  jumps). Circles drawn largest first; a site with several states shows concentric marks.
- Interaction: state toggle, region presets, hover/tap card under the map, arrow keys step through the
  sites of the current view; squares highlight their sites on the map on hover.
- Phone (360 px): squares wrap to 10 per row; toggles become two rows of segmented controls; default region
  East Asia on phones, World on desktop.
- No JavaScript: headline, title block, text and country table.

## Form and interaction (first sketch, superseded by the proposal above)
- Form: proportional-symbol map (one circle per site), Equal Earth projection, land in a quiet ink tone.
  Symbol area proportional to unit count. Operating in a neutral context tone; under construction carries the
  accent colour (the thesis); planned in a lighter or hollow variant of the accent. Identity never by colour
  alone: legend with shape (filled vs hollow) and direct labels for the largest countries.
- Interaction: state toggle; hover/tap card with site name, country, units per state and the source status;
  keyboard steps through sites in the current view. Above the map, a single line of counts that updates with
  the toggle ("81 under construction, 40 in China").
- Phone (360 px): map full width, toggle as a segmented control above it, card pinned below the map instead
  of a floating tooltip. Dense regions (East Asia, Europe) need a check for overlap; fall back to a zoom
  inset or a country list if circles merge.
- No JavaScript: headline, text and the country table carry the story.

## Decisions (Marco)
- 2026-11-11: thesis "China: half of what is under construction" (wording follows the verified number);
  map by site with state toggle; states = operating, under construction, planned (proposed out).
- 2026-11-11: source priority. WNA sets the counts and status of every unit. GEM fills what WNA lacks
  (coordinates, and units WNA does not list, flagged). IAEA PRIS only as a cross-check of operating and
  under-construction counts; differences reported in the notes.
- 2026-11-11: reconcile WNA and GEM unit by unit, using the WNA country profiles (unit lists). Every map mark
  is a unit WNA recognises, so the map and the headline count the same thing.
- 2026-11-11: raw WNA and PRIS tables read as page text in Marco's Chrome, saved with read date and CRC32.

## First look at GEM (August 2026 release, read 2026-11-11)
- 1825 units, no duplicate unit ids, last researched 2024-05-06 to 2026-07-08.
- operating 424, construction 85, pre-construction 137, announced 328.
- China construction 36 of 85 (42 %). Six GEM "construction" units are not first-concrete power reactors in
  WNA terms: Hermes (test reactor), Project Pele (military microreactor), Palisades repower; Kashiwazaki-Kariwa 7,
  Tokai 2 and Tomari 3 (operable in WNA). Without them: 36 of 79 (46 %).
- Japan operating: GEM 15 (restarted) vs WNA 33 (operable).
- pre-construction: 70 of 137 units have approximate locations.

## Open questions
- France planned: 2 units counted, not drawn (Marco, 2026-11-11).
- Basemap source (Natural Earth 110 m or 50 m, public domain) and its size in the bundle.
