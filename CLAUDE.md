# Marco's Website

Personal site of Marco, an electrical and nuclear engineer. It publishes small
data-analysis and science-outreach projects, each built around one interactive
d3.js infographic. Over time the site becomes his data-analysis portfolio.

Topics are open: energy and nuclear are the starting point, but a project can be
about anything Marco finds interesting (science, technology, startups, economics,
sport, food...). The method below does not depend on the topic.

## How to work with Marco

- Talk to Marco in Spanish unless he writes in another language. Everything
  published on the site is in **English**.
- Answer first, then context only if it adds value. No filler, no closing
  summaries, no disclaimers.
- He is technically advanced. Do not explain basics of engineering, physics or
  programming unless asked.
- If the brief is unclear, ask with `AskUserQuestion` (2-4 short questions with
  options). Never fill gaps with invented content.
- Never invent data, numbers or sources. If something is uncertain, say so.
- Be proactive: if you see a better chart form, a stronger story, or a data
  problem, say it before building.
- Show work early: a rough working chart beats a long plan.

## Audience and voice of the site

- Default reader: **curious general public**, no technical background. A second
  reader is a recruiter or peer checking Marco's data skills; they will open the
  methodology and the code.
- One idea per project. If you need two headlines, it is two projects.
- Write like a knowledgeable person talking plainly. Short sentences, active
  voice, concrete numbers with units.
- Banned (Marco hates default AI prose): "delve", "tapestry", "landscape",
  "in today's world", "it's worth noting", "crucial", "pivotal", "game-changer",
  "not X, but Y" constructions, rhetorical questions as openers, em-dash asides,
  groups of three adjectives, emoji, exclamation marks, closing morals.
- Every number on the page must be traceable to the data file or a cited source.

## Stack

- **Astro 7** static site, MDX pages, deployed as static files.
- **d3 v7** from npm, imported inside a component `<script>` (bundled by Vite).
  No CDN script tags.
- **Python 3** for data work (`analysis/`), pandas/numpy when needed. Python
  writes clean JSON/CSV to `src/data/<slug>/`; the browser only draws.
- No UI framework (React etc.) unless a project truly needs one. Plain Astro +
  vanilla TS/JS + d3.

```
npm run dev              # local site at localhost:4321
npm run build            # static build to dist/
npm run check:palette -- "#hex,#hex" --surface "#F4F6F7"
python3 analysis/<slug>/build_data.py
```

## Repository layout

```
briefs/<slug>.md                      # one brief per project (from docs/brief-template.md)
analysis/<slug>/raw/                  # original downloads, never edited by hand
analysis/<slug>/build_data.py         # raw -> processed; prints checks
src/data/<slug>/*.json                # processed data the chart imports
src/components/viz/<slug>/*.astro     # the d3 component(s) for this project
src/pages/projects/<slug>.mdx         # the published page (text + components)
src/styles/tokens.css                 # site-wide design tokens (colors, type)
src/layouts/                          # Base and Project layouts
docs/                                 # brief template, design notes
scripts/check_palette.py              # color validator (CVD, contrast)
```

`<slug>` is short kebab-case, e.g. `uranium-enrichment`. Use the same slug in
every folder.

## The method: one mini-project, seven phases

Work through the phases in order. Each has a gate: do not start the next phase
until the gate is met. Tell Marco which phase you are in when you start one.

### 1. Brief
Create `briefs/<slug>.md` from `docs/brief-template.md`. It must state:
- **The one sentence** the reader should remember (the thesis).
- The question the chart answers, and who is reading.
- Scope: what is in the MVP and what is explicitly out.
- Candidate data sources.

Gate: Marco approves the thesis and the scope.

### 2. Data
- Save originals in `analysis/<slug>/raw/` with the source URL and the download
  date in the brief. Never edit raw files.
- `build_data.py` does all cleaning and calculation and writes to
  `src/data/<slug>/`. It must run from a clean checkout in one command.
- The script prints sanity checks against known reference values (totals,
  published figures). A mismatch stops the work.
- State units explicitly everywhere (e.g. atom % vs mass %, MW vs MWh, nominal vs
  real money). Unit confusion is the most common error in popular infographics.
- Prefer primary sources (agencies, standards bodies, papers, official
  statistics) over aggregators.

Gate: processed data exists, checks pass, every field has a unit and a source.

### 3. Form (before any color)
Decide what job the data does and pick the form:
- part-of-whole with small counts -> waffle / unit chart
- comparison across categories -> bar (sorted, zero baseline)
- change over time -> line (or bars for few periods)
- relationship -> scatter
- distribution -> histogram / strip / box
- flow or mass balance -> Sankey
- one headline number -> big number, not a chart
Sketch in words (or ASCII) the layout, the interaction, and the phone layout.

Gate: Marco agrees on form and interaction.

### 4. Build
- One component per visualization in `src/components/viz/<slug>/`. It imports
  its JSON, draws in an SVG with a `viewBox` (responsive), and has no global
  state beyond its own root element.
- Interaction is the default: tooltip on hover/tap, highlight via legend. Add a
  control only if it reveals something new (a toggle, a slider, a scenario).
- Use `src/styles/tokens.css` tokens for every color and font. No literal colors
  in components.
- New categorical colors must pass `scripts/check_palette.py` in light and dark.
- Build the first working version fast; refine after Marco sees it.

Gate: renders with real data, desktop and 360 px wide, light and dark.

### 5. Words
Write the page in `src/pages/projects/<slug>.mdx`:
- Headline that states the finding (a sentence with a number), not a topic label.
- 2-4 short paragraphs of context, then the chart, then what to look at.
- A "Notes and method" section: data sources with links and access dates,
  units, rounding, assumptions, and a link to the analysis script.
Then audit the text against the banned list above and fix every hit.

Gate: Marco approves the text.

### 6. QA (definition of done)
- [ ] Every number on the page matches `src/data/<slug>/` or a cited source.
- [ ] `build_data.py` runs clean and its checks pass.
- [ ] `npm run build` passes with no warnings from the new code.
- [ ] Works at 360 px, 768 px and 1280 px; no horizontal page scroll.
- [ ] Light and dark themes both readable.
- [ ] Identity is never color-only: legend or direct labels are present.
- [ ] Keyboard focus visible; `prefers-reduced-motion` respected.
- [ ] A table view or text alternative (`aria-label`, `<details>` table).
- [ ] Frontmatter complete (title, description, date, tags, status).
- [ ] Text audited against the banned list.

### 7. Publish
- Set `status: published` in the frontmatter; the home page lists it.
- Export a static PNG (1200x1200 and 1200x630) of the key view for LinkedIn and
  link previews, saved to `public/og/<slug>.png`.
- Commit with a message like `feat(uranium-enrichment): waffle comparison`.

## Visualization rules (always)

- Form first, color last.
- One accent color carries the story; everything else is context.
- Sequential data: one hue, light to dark. Diverging: two hues with a neutral
  midpoint. Never a rainbow.
- Never two y-axes. Two measures means two charts or an index.
- Bars start at zero. Sort bars unless the order carries meaning.
- Label directly where possible; keep grids and axes quiet.
- Text uses ink tokens, never the series color.
- Tooltips show the value with unit and a short plain-language line.
- Animation only to show a change of state, 300-900 ms, disabled with reduced
  motion.
- Keep the page readable with JavaScript disabled: the headline, text and table
  still carry the story.

## Code conventions

- TypeScript or modern JS in component `<script>` tags; no inline `onclick`.
- Components find their root with a `data-viz="<slug>"` attribute so several can
  live on one page.
- Keep d3 code readable: scales, then axes, then marks, then interaction.
- Python: one `build_data.py` per project, standard library + pandas/numpy only
  unless justified; add new packages to `analysis/requirements.txt`.
- Do not commit `node_modules/`, `dist/` or large raw files (>20 MB); for those,
  store the download URL and a fetch step in `build_data.py`.

## Slash commands

- `/new-project <topic>`: start phase 1 for a new project.
- `/qa <slug>`: run the phase 6 checklist on a project.
