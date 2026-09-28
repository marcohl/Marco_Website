# Brief: Seven in a Thousand

- **Slug:** `uranium-enrichment`
- **Status:** build
- **Started:** 2026-09-28

## The one sentence
Only 7 in every 1,000 uranium atoms are U-235; reactor fuel raises that to about
50, weapons-grade to about 900.

## Question and reader
- Question: what is the difference between natural and enriched uranium?
- Main reader: curious general public.
- They know "uranium" and "nuclear"; they do not know that uranium is a mix of
  isotopes or what the enrichment percentage refers to.

## Scope
- In the MVP: three waffle charts (natural 0.72%, 5% LEU, 90% HEU), 1,000 atoms
  each, with a sorted/mixed toggle, tooltips and legend highlight.
- Out (v2 ideas): fission cross-sections (ENDF/B-VIII.0), enrichment spectrum by
  reactor type, feed/SWU calculator, Oklo natural reactor time slider.

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| Natural isotopic abundance of U | IUPAC CIAAW, https://www.ciaaw.org/uranium.htm | 2026-09-28 | atom fraction | U-234 0.0054%, U-235 0.7204%, U-238 99.2742% |
| Atomic masses U-235, U-238 | AME2020 / NIST | 2026-09-28 | u | 235.0439299, 238.0507882 |
| LEU/HEU threshold (20%) | IAEA Safeguards Glossary | 2026-09-28 | mass % | |

Known reference values: 5 wt% U-235 is about 5.06 atom %; 90 wt% is about 90.1 atom %.

## Form and interaction
- Waffle (unit chart), 40 x 25 = 1,000 cells per panel: small counts (7) stay
  visible and countable.
- Toggle sorted/mixed; tooltip per cell; legend highlight across panels.
- Phone: panels stack in one column.

## Open questions
- Keep the naval-reactor mention in the 90% panel?
- Final source links to verify before publishing.
