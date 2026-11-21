# Brief: More reactors, smaller slice

- **Slug:** `nuclear-capacity-vs-share`
- **Status:** published (2026-11-21)
- **Started:** 2026-11-21

## The one sentence
DNV forecasts world nuclear capacity growing 2.9-fold, from 415 GW in 2025 to
1,200 GW in 2060, yet nuclear's share of world electricity falls from 8.7% to
7.0% in the mid-2040s and is still below today's level in 2060 (8.3%).

Draft headline: "Nuclear capacity nearly triples by 2060. Its share of the
world's electricity does not grow."

## Question and reader
- Question the chart answers: if the world builds so many reactors, why does
  nuclear not take a bigger share of the electricity mix?
- Main reader: curious general public. Second reader: recruiter or peer who
  checks the method and the units (GW vs TWh vs %).
- What they already know: headlines about a "nuclear renaissance", SMRs, big
  tech signing nuclear deals.
- What they do not know: capacity, generation and share are three different
  things. Total electricity grows faster than nuclear output (33,000 to
  84,200 TWh, +155%, against +144% for nuclear). Part of the new build only
  replaces retiring reactors, and reactors run fewer hours (load factor 0.79
  to 0.67) as solar and wind push them down the merit order.

## Scope
- In the MVP:
  - Global series 2025-2060: nuclear capacity (GW), nuclear generation (TWh),
    total generation (TWh), nuclear share (%).
  - Regional share 2025 vs 2060 for DNV's 10 regions (Europe 20% to 8%,
    North America 17% to 7%, China 4% to 11%, Indian Subcontinent 3% to 10%).
  - One annotation on the mechanism: replacement (260 of the 1,000 GW
    commissioned to 2060 replaces retirements) and lower load factor.
- Explicitly out (maybe v2):
  - SMR costs and learning curves (USD/kW): a separate story.
  - Hyperscaler deals and behind-the-meter nuclear.
  - IEA WEO scenarios. Mixing a DNV forecast with IEA scenarios breaks the
    one-source series rule. IEA may appear only as context in the notes
    (about 90 GW under construction in mid-2026).
  - Historical series before 2025, except the 1996 peak (17.5%) as a single
    cited reference in the text, if we use it.

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| DNV ETO 2026 forecast data (xlsx, released 2026-10-07) | https://www.dnv.com/eto-data (redirects to a brandcentral.dnv.com .xlsx) | 2026-11-21 | GW, GWh/yr | Sheet "Power supply", annual 2025-2060, 10 regions. Use the "incl behind-the-meter" variables: they reproduce the report (see checks). Saved to `raw/dnv_eto_2026_data.xlsx`, gitignored. |
| DNV ETO 2026 main report, sec. 4.5 | `DNV_ETO_Main_Report_2026_r3-2.pdf`, pp. 70-74 | 2026-11-21 | GW, TWh, %, USD/kW | Cited reference values. Local copy in `Data analysis sources/`, not committed (43 MB). |

Known reference values to check against (DNV report, pp. 70-73):
- Capacity: 415 GW (2025), 600 GW (2040), 1,200 GW (2060).
- Nuclear generation: 2,900 TWh (2025), 7,000 TWh (2060).
- Total generation: 33,000 TWh (2025), 84,200 TWh (2060).
- World share: 8.7% (2025), 7.6% (2040), 7.0% low (mid-2040s), 8.3% (2060).
- Net additions 2025-2040: 180 GW, of which Greater China 140 GW.
- Commissioned to 2060: 1,000 GW, of which 260 GW replaces retirements.
- Implied load factor: 0.79 (2025) to 0.67 (2060); North America 0.50,
  Europe 0.47 in 2060.
- Regional share 2025 / 2040 / 2060: Europe 20 / 10 / 8%; North America
  17 / 10 / 7%; China 4% to 11%; Indian Subcontinent 3% to 10%; OECD Pacific
  14% (2025), peak 20% (2030), 16% (2060).
- SMR capacity: 13 GW (2040), 88 GW (2050), 310 GW (2060). The text says
  310 GW; the annotation on Fig. 4.12 says "300 GW". Use the dataset value.

Check: 7,000 / 2,900 = 2.41 (report says generation 2.4-fold) and
1,200 / 415 = 2.89 (report says 2.9-fold).

## Form and interaction
To be decided in phase 3. Candidates:
- A two-panel view: capacity (GW) rising steeply on top, share (%) dipping
  and recovering below, shared x-axis 2025-2060. Two charts, never two y-axes.
- Or an index chart (2025 = 100) of nuclear capacity, nuclear generation and
  total generation, so the gap between the lines is the story.
- Regional slope chart of share 2025 to 2060, sorted, with Europe and North
  America falling and China and India rising.
- Phone layout: panels stack vertically; slope chart keeps labels on both
  sides.

Dataset vs report (world sums of the 10 regions, checked 2026-11-21):
- "Installed Capacity including behind-the-meter...", nuclear: 415 / 600 /
  1,203 GW (2025 / 2040 / 2060). Report: 415 / 600 / 1,200.
- "Electricity Generation incl off-grid and behind-the-meter": nuclear
  2,872 -> 7,017 TWh; all sources 33,007 -> 84,154 TWh. Report: 2,900 ->
  7,000 and 33,000 -> 84,200.
- Share: 8.70% (2025), 7.60% (2040), 8.34% (2060). Report: 8.7 / 7.6 / 8.3.
- Known discrepancy: Europe 2040 share is 10.6% in the dataset vs "10%" in
  the report text. Treated as rounding in the prose; the page uses 10.6%.
- The "Utility-scale" variables are lower (1,163 GW, 63,437 TWh in 2060) and
  must not be used for the headline.

Licence (sheet "Disclaimer and copyright"): derived work may be published
with the notice "This work is partially based on data developed by DNV AS,
©DNV AS. 2026, but the resulting work has been prepared by [entity] and does
not necessarily reflect the views of DNV AS." Commercial use and
redistribution of the report are not allowed. So: raw xlsx is not committed;
build_data.py downloads it; the site ships only the small derived JSON.

## Open questions
- Is a derived JSON of 4 series x 10 regions x 36 years acceptable under the
  licence, or should the JSON keep only the years the chart draws? Low risk,
  but decide before publishing.
- Headline wording: "does not grow" vs "ends below today" (8.3% vs 8.7%).
