# Design system: Isotype

The visual rules for every page and every project on the site. `CLAUDE.md` says
how to work; this file says how things must look. Read it before phase 3 (Form)
of any new project and check against it in phase 6 (QA). `DESIGN.md` at the repo
root is the full record of the system; this file is the working checklist.

The values below are copied from the `body.iso` block in
`src/styles/tokens.css`. If the two ever disagree, the CSS wins and this file
must be updated in the same commit. (The `:root` block above it is the old
Blueline set, kept only as a fallback; do not design against it.)

## 1. The idea

The site counts things with you, in the spirit of Isotype picture statistics
(Neurath, Arntz): rows of identical little symbols, one group coloured
differently. Flat cut-paper shapes in saturated poster colours on a cool
off-white ground, black text, one friendly humanist sans. The tone is relaxed
but credible: no blueprint jargon, no drawing numbers, no revisions, no title
blocks.

Every page uses `<Base world="iso">` (project pages get it from
`Project.astro`).

Three consequences for anything new:

- **Flat colour, no shadows.** Structure comes from colour fields, soft panels
  and 1px `--rule` lines. No drop shadows, no gradients (except the
  highlighter band), no glassmorphism, no textures.
- **Soft corners.** `--radius` (6px) on panels, tiles and buttons (buttons and
  segmented pills are fully round). Data marks stay geometric.
- **Count, don't decorate.** Where a number can be shown as countable units,
  show the units (the 1,000-atom grid on the home, the language row in About).
  Never invent numbers to fill a pictogram row.

## 2. Color

Components never use literal colors. Use these tokens only.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#EDF0F1` | `#11151B` | Page ground |
| `--panel` | `#FFFFFF` | `#1A2029` | Chart boxes, key-figure panels |
| `--ink` | `#15181C` | `#EDF0F1` | Headings, strong text, focus rings |
| `--ink-2` | `#3C424A` | `#C4CAD2` | Body text |
| `--ink-3` | `#565D67` | `#9CA5B0` | Secondary labels, ticks, captions |
| `--rule` | `#C5CCD2` | `#2E3743` | Separators, control borders |
| `--grid` | `#DDE2E6` | `#222A34` | Chart gridlines only |
| `--marker` | `#F0B429` | `#F5C04A` | Highlighter, text selection |
| `--cat-1` | `#2F5D9E` | `#7EA2DA` | Data: context (Neurath blue) |
| `--cat-2` | `#D63B26` | `#FF6A50` | Data: the story (signal red) |
| `--cat-3` | `#286B4A` | `#5FBF8F` | Data: a second group that is not the story (e.g. women vs men) |
| `--field-blue / -red / -green / -ochre` | `#2F5D9E` / `#B8321F` / `#286B4A` / `#F0B429` | same | Colour fields: gallery tiles, home closing band, Next project tile |
| `--on-field` / `--on-ochre` | `#FFFFFF` / `#15181C` | same | Text on a colour field |

Rules:

- **Red means the story, on every page.** `--cat-2` is the one thing the
  reader must notice. Not for decoration, links, warnings or a neutral group.
  The primary button is ink, never red, because it shares the screen with red
  marks. `--field-red` (a darker field shade) fills the red tile and the home
  closing band.
- **Blue is context, green is a second group.** When two groups are compared
  and neither is the story, use `--cat-1` and `--cat-3`.
- **Fields carry text only in their `--on-*` colour.** White on blue, red and
  green; dark ink on ochre.
- **Technology palette (exception, `bolivia-power-plants`).** `--tech-*`
  tokens, approved 2026-11-15, with an ink outline, a text label and a table
  for every series. Do not mix them with `--cat-*` in the same chart.
- A new data colour needs a token pair validated with `npm run check:palette`
  on `--bg` and `--panel`, light and dark, and a row in this table.

## 3. Typography

One family: **Atkinson Hyperlegible Next** (variable, self-hosted), mapped to
`--f-display`, `--f-body` and `--f-data` under `body.iso`. Chunky weights for
headings, regular for reading.

| Element | Spec |
|---|---|
| Home hero `h1` | 800, `clamp(44px, 9vw, 80px)`, line-height 1.02, -.025em |
| Project `h1` | 800, `clamp(40px, 6vw, 72px)`, line-height 1, -.02em |
| Section `h2` | 800, 28-32px, line-height 1.1 |
| Tile / Next project title | 800, 26px (36px for the newest tile on desktop) |
| Body | 400, 17px, line-height 1.6; lead 19px (17px under 560px) |
| Meta line (date, subject) | 600, 15-16px, `--ink-2` |
| Chart text | 12px ticks, 13px direct labels, 13-14px legends and cards |

Rules:

- **Sentence case everywhere**, including project titles. No tracked
  uppercase. No kicker or eyebrow above a heading: dates and topics go in a
  meta line after the text or above the page as a breadcrumb.
- **Numbers are tabular** (`tabular-nums` on `svg text`, `table`, `.num`).
- **Percent without a space:** `84%`, never `84 %`.
- `text-wrap: balance` on headings, `pretty` on prose.
- Prose is capped at `--measure` (64ch).

## 4. Layout and structure

- **Container:** `.wrap`, max 1180px, 20px side gutter.
- **Mobile first**; breakpoints in use 560, 640, 700, 900, 960, 1000px. Check
  360/375, 768 and 1280px. No horizontal page scroll.
- **First viewport shows the work.** On the home, the live chart starts in the
  first phone screen.
- **No empty bands on desktop.** A text column gets an illustration or a
  key-figure panel beside it, top-aligned with the headline.
- **Lines:** 1px `--rule` only. No ink rules under the header or above the
  method section.
- **Touch targets** at least 44px.

## 5. Components

- **Primary button** (`.btn`): `--ink`, paper text, 700 18px, 48px high,
  pill. Hover turns to `--ink-2`.
- **Gallery tile** (home): a colour field (blue, red, green, ochre in turn)
  holding a white panel with the project thumbnail, then title, description
  and the meta line. Newest tile spans full width. One gallery, never a
  thumbnail strip plus a list.
- **Atom count** (`AtomCount.astro`): 1,000 atom pictograms (`<symbol>` plus
  one `<use>` each), three pill buttons, a big count and an `sr-only` live
  sentence announcing the full reading.
- **Key-figure panel** (`.tblock`): white panel with `--radius`, cells split by
  `--rule` lines, `small` label over a bold value.
- **Project meta line** (`Project.astro`): "Projects / subject · Mon YYYY",
  from frontmatter. Do not rebuild it by hand.
- **Next project tile** (`Project.astro`): blue field linking to the next
  older project, wrapping to the newest.
- **Segmented control / select, legend, tooltip, reading card, numbered
  insights, data table in `<details>`, Notes and method section:** unchanged
  in structure; they take their colours from the tokens above.
- **Theme toggle:** the label names the theme it switches to ("Dark theme" /
  "Light theme"). The default follows `prefers-color-scheme`.
- **Skip link** to `#main` on every page.

## 6. Charts

These complement the visualization rules in `CLAUDE.md`.

- **Marks:** lines 2px round; context lines 1.5px at .55 opacity; bands at
  .17. Hollow marks for a different state.
- **Axes:** no domain line, horizontal `--grid` lines, ticks in `--ink-3`.
- **Direct labels** at line ends: 600 `--ink` for the story, 400 `--ink-3`
  for context.
- **Annotations:** at most two or three per view.
- **Dimming:** unselected series .18-.3; inactive scroll steps no lower than
  .6 opacity so the text stays readable.
- **Motion:** only to show a change of state, 300-900 ms; everything respects
  `prefers-reduced-motion`.
- **No JavaScript:** headline, text and data table still tell the story.

## 7. A new project page, step by step

1. Frontmatter: `layout`, `title` (sentence case), `description` (one
   sentence, used in the gallery and link previews), `date`, `tags` (first tag
   shows on the gallery tile), `eyebrow` (subject in the meta line), `status`.
   Add `src/components/viz/<slug>/Thumb.astro` (small SVG from the project
   data, tokens only, `aria-label` stating the finding) so the gallery tile
   has a picture. `code` and `rev` are no longer shown.
2. Intro block: `h1` stating the finding with a number, 2-4 short paragraphs
   in `.prose`, and an illustration or key-figure panel beside it on desktop.
3. The chart component(s), tokens only.
4. Optional numbered insights.
5. Data table in `<details>`.
6. Notes and method section; last card "Sources" ends with the analysis
   script path.
7. Open Graph images: `public/og/<slug>.png` (1200x630) and
   `public/og/<slug>-square.png` (1200x1200).

## 8. Design checklist (add to phase 6 QA)

- [ ] `world="iso"`; no literal colours or font names; only tokens.
- [ ] Red (`--cat-2`) marks the story and nothing else.
- [ ] Sentence case; no kicker above headings; `84%` without a space.
- [ ] Soft corners, flat colour, no shadows or gradients.
- [ ] No empty half-width bands on desktop; the chart is reachable in the
      first phone screen.
- [ ] Heading levels do not skip.
- [ ] Light and dark both checked; new data colours validated with
      `check:palette`.
- [ ] Touch targets 44px; focus outline visible in both themes.
