# Design system: Blueline

The visual rules for every page and every project on the site. `CLAUDE.md` says
how to work; this file says how things must look. Read it before phase 3 (Form)
of any new project and check against it in phase 6 (QA).

The values below are copied from `src/styles/tokens.css`. If the two ever
disagree, the CSS wins and this file must be updated in the same commit.

## 1. The idea

The site looks like a set of engineering drawings. Blue ink on white paper, as
in a diazo (blueline) print; the dark theme is the cyanotype, white lines on
deep blue. Each project is a **drawing sheet** with a number (`MHL-00N`), a
revision letter and a title block. The home page is the **register of
drawings**.

Three consequences for anything new:

- **Lines, not shadows.** Structure comes from 1-2 px ink rules and boxes. No
  drop shadows, no gradients (except the highlighter band), no glassmorphism.
- **Square corners.** `border-radius: 0` everywhere. The only round shapes are
  data marks (dots, rings) and numbered markers.
- **It must not look generated.** No rounded cards with soft shadows, no
  pastel gradient blobs, no emoji, no centered hero with a big blurred
  illustration. If a layout looks like a SaaS landing page template, redo it.

## 2. Color

Components never use literal colors. Use these tokens only.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#F2F3F0` | `#0E1740` | Page background (the paper) |
| `--panel` | `#FAFAF8` | `#162257` | Boxes that hold a chart, title blocks, sheets |
| `--ink` | `#1B2A6B` | `#EAF0FF` | Headings, strong text, rules, borders of boxes |
| `--ink-2` | `#4B5688` | `#B9C4F2` | Body text, axis labels on the category axis |
| `--ink-3` | `#5F6993` | `#98A5DC` | Secondary labels, metadata, tick labels, captions |
| `--rule` | `#C9CDE0` | `#2C3A7A` | Light separators inside a figure, control borders |
| `--grid` | `#DDE0EE` | `#1B2766` | Chart gridlines only |
| `--marker` | `#FFE14D` | `#FFD84D` | Highlighter (see below) |
| `--on-marker` | `#1B2A6B` | `#0E1740` | Text on top of the highlighter |
| `--cat-1` | `#5A68B0` | `#8FA2F0` | Data: context series |
| `--cat-2` | `#C8372D` | `#FF7A66` | Data: the story (accent) |

Rules:

- **Two data colors, fixed roles.** `--cat-2` (red) is the one thing the
  reader must notice; `--cat-1` (blue) is everything it is compared with.
  Additional series that are not the story use `--ink-3` at reduced opacity
  (see the grey context lines in `SprintChart`).
- **Red means the story, on every page.** Do not use `--cat-2` for decoration,
  links, warnings or UI state.
- **The highlighter is yellow and rare.** `--marker` is used in two ways only:
  1. the `.mk` band behind one key figure in text, or the big number in a
     chart's stage (`UraniumWaffles .n`): at most one per screen;
  2. hover state of interactive blocks: links in the register, sheets, the
     primary button, the theme toggle.
  Never as a data series color, never as text color.
- **Text is never in a series color.** Labels and numbers use ink tokens; the
  series is identified by a swatch or by position.
- **A third data color** needs a new token pair in `tokens.css`, validated in
  both themes on `--bg` and `--panel`:
  `npm run check:palette -- "#cat1,#cat2,#new" --surface "#F2F3F0"` (and
  `#FAFAF8`, then the dark values on `#0E1740` and `#162257`). Add it here
  when it lands. The current pair passes: contrast 4.7-5.0:1 light,
  5.9-7.1:1 dark; worst colour-blind distance 19.7 (protan).
- **Sequential and diverging scales** are not defined yet. The first project
  that needs one defines `--seq-*` or `--div-*` tokens (one hue light to dark;
  two hues with a neutral midpoint), validates them, and documents them here.

## 3. Typography

Three families, three jobs. Do not add a fourth.

| Role | Token | Family | Where |
|---|---|---|---|
| Display | `--f-display` | Barlow Semi Condensed 400/600/700 | Headings, nav, buttons, title blocks, register, big numbers |
| Body | `--f-body` | Literata (variable, serif) | Running text, paragraphs, lists |
| Data | `--f-data` | Atkinson Hyperlegible Next (variable) | Everything inside a chart: axis and tick labels, direct labels, legends, tooltips, controls, tables, numbers in stats |

Scale in use:

| Element | Spec |
|---|---|
| Page `h1` (project headline) | 700, `clamp(40px, 6vw, 72px)`, line-height 1, letter-spacing -.01em |
| Home hero `h1` | 700, `clamp(42px, 10.5vw, 88px)` |
| Section `h2` | 600, 28px (project) / 30px (home), line-height 1.1 |
| `h3` in method / steps | 600, 18px (method) / 30-34px (scrolly step titles) |
| Eyebrow | 600, 16px, `--ink-2`, sentence case |
| Body | 400, 17px, line-height 1.6; `--ink-2` in `.prose` |
| Lead (home) | as body, max 60ch |
| Method notes | 15px, `--ink-2` |
| Chart text | `--f-data` 12px ticks, 13px direct labels (600 for the story series), 13-14px legends and cards |
| Title-block label / value | `small` 13px `--f-data` `--ink-3` / `b` 600 17px `--f-display` `--ink` |

Rules:

- **Sentence case everywhere.** No uppercase with letter-spacing (the old
  monospace eyebrows are gone; do not bring them back).
- **Numbers are tabular.** `font-variant-numeric: tabular-nums` is set
  globally on `svg text`, `table` and `.num`. Right-align numeric table cells.
- **Bold in prose** (`strong`) is 700, `--ink`, no wrapping. Use it for the
  terms the reader needs to carry, not for emphasis of whole sentences.
- `h1 em` is upright: it marks the key number in the headline. To make that
  number stand out, wrap it in `.mk` (highlighter) only if no other highlighter
  is on the first screen.
- Line length: prose is capped at `--measure` (64ch).
- Code (method section only): system monospace, `.88em`.

## 4. Layout and structure

- **Container:** `.wrap`, max 1180px, 20px side gutter, 40px top / 64px bottom.
- **Mobile first.** Base CSS is the phone layout; desktop is added with
  `min-width` queries. Breakpoints in use: 560, 640, 700, 900, 1000px.
- **Three widths must work:** 360, 768, 1280px. No horizontal page scroll;
  wide tables scroll inside their own `overflow-x: auto` box.
- **No empty bands.** Every horizontal band of the page is filled across its
  width on desktop. If the text column leaves the right half empty, put an
  illustration, a key-figure block or a title block there (the atom next to
  the uranium headline, the pool next to the swimming one). On phones the
  side illustration may be dropped if it pushes the chart down.
- **Rules:**
  - 2px `--ink`: major section breaks (header bar, footer, method section,
    top of the register).
  - 1px `--ink`: borders of title blocks, sheets, register rows.
  - 1px `--rule`: separators inside a figure (legend top, card, controls).
- **Spacing:** sections 48-64px apart; inside a figure 8-12px (phone) to
  12-20px (desktop). Charts get `margin-block: 24px` (32px from 900-1000px).
- **Touch targets** at least 44px high (40px allowed on desktop controls).

## 5. Components

Reuse these before inventing new ones.

- **Title block** (`.tblock`, global in `tokens.css`): grid of cells, 1px ink
  border, `--panel` fill, each cell a `small` label over a `b` value. Collapses
  to 2 columns under 560px. Used for the project cartouche (automatic, from
  frontmatter), the home sheets and the About facts. Use it for any set of
  3-6 key facts or figures on a project page.
- **Cartouche:** rendered by `Project.astro` from frontmatter (Drawing no.,
  Subject = `eyebrow` or tags, Revision, Date). Do not rebuild it by hand.
- **Primary button** (`.btn`, home): `--ink` fill, `--bg` text, display 600
  19px, 48px high, square; hover turns to the highlighter.
- **Segmented control** (`.seg` / `.sp-seg`): 1px `--rule` box on `--bg`,
  buttons in `--f-data` 600 13-14px; the pressed one is `--ink` fill with
  `--bg` text and `aria-pressed="true"`.
- **Select** (`.sp-sel`): same box, small label in `--ink-3` before it; label
  visually hidden under 700px.
- **Figure box:** the chart sits on `--panel` with a 1px `--rule` border,
  padding 12px (18-20px desktop).
- **Legend:** swatch + label, `--f-data` 13-14px. Swatches are squares
  (14px) for areas/cells, short bars (10x3px) for lines. Clicking a legend
  item may highlight its series (dim the rest to ~.18 opacity).
- **Tooltip:** `--ink` fill, `--bg` text, `--f-data` 13px, square, max 220px.
  Shows value with unit and one plain-language line. On charts where a tooltip
  would cover the data, use a **reading card** under the chart instead
  (`.sp-card`), which also works on touch.
- **Numbered insights:** list with a circled number (24px, 1.3px ink ring,
  `--panel` fill, `--f-data` 600 12px). Use for "what to look at" next to a
  chart.
- **Data table:** inside `<details>` under the chart ("Show the data"),
  1px `--rule` row lines, `--f-data` for numbers and row headers, caption in
  `--ink-3` 12px.
- **Notes and method:** `<section class="method">` at the end of every
  project, `h2` "Notes and method", `.method-grid` with `h3` cards (1 column,
  2 from 640px, 4 from 1000px). Last card is always "Sources" and ends with
  the path of the analysis script.
- **Illustrations** (atom, pool, nucleus logo): flat shapes, ink outlines,
  data colors only where they mean something (protons red, neutrons blue). No
  realistic rendering, no textures, no gradients.

## 6. Charts

These complement the visualization rules in `CLAUDE.md`.

- **Marks:** lines 2px (`stroke-linejoin/linecap: round`); context lines
  1.5px at .55 opacity. Dots filled with the series color; hollow dots
  (`--panel` fill) for a different state (e.g. not held, estimated). Bands at
  .17 opacity. Cells and bars with no stroke, or a `--bg` hairline when they
  touch.
- **Axes:** no domain line. Gridlines `--grid`, horizontal only unless the x
  values need reading. Tick labels `--ink-3`; category or time axis labels
  `--ink-2`. One baseline in `--ink-3` 1px. Axis titles 12px, only when the
  unit is not obvious from the tick labels.
- **Direct labels** at the end of a line or next to a group, `--f-data` 13px,
  600 and `--ink` for the story, 400 and `--ink-3` for context.
- **Annotations:** 1px `--ink-2` leader, small `--panel` circle with ink ring,
  `--f-data` 600 12px label. At most two or three per view.
- **Reference lines** (a limit, a threshold, a gap): dashed `3 4` in
  `--ink-3`.
- **Selection:** 1.5px `--ink` ring around the selected mark; dimming others
  to .18-.3.
- **Big number** (one headline value): display 700, 36px phone / 44px
  desktop, on the highlighter.
- **Motion:** only to show a change of state, 300-900 ms, `easeCubicOut`;
  scroll-driven steps fade at .3s. Everything checks
  `prefers-reduced-motion: reduce` and jumps to the end state.
- **No JavaScript:** the headline, text and data table still tell the story;
  controls and the SVG stage are hidden (`:not(.js)`).

## 7. A new project page, step by step

1. Frontmatter: `layout`, `title` (short, a name for the sheet),
   `description` (one sentence, used in the register and link previews),
   `date`, `tags` (first tag is the Topic column), `eyebrow` (Subject in the
   cartouche), `status`, `code: MHL-00N`, `rev: A`, `thumb` (only if it should
   be a featured sheet on the home page). A featured sheet also needs
   `src/components/viz/<slug>/Thumb.astro`: a small SVG built from the project
   data at build time, tokens only, with an `aria-label` that states the
   finding. The home page finds it by slug and shows the two newest projects
   that have both; `src/pages/index.astro` does not change.
2. Intro block: headline `h1` stating the finding with a number, 2-4 short
   paragraphs in `.prose`, and something on the right on desktop (illustration,
   title block of key figures) so the band is full.
3. The chart component(s), styled only with tokens and the components above.
4. Optional numbered insights beside or under the chart.
5. Data table in `<details>`.
6. Notes and method section.
7. Open Graph images in the same style: `public/og/<slug>.png` (1200x630) and
   `public/og/<slug>-square.png` (1200x1200).

## 8. Design checklist (add to phase 6 QA)

- [ ] No literal colors or font names in the new component; only tokens.
- [ ] Red (`--cat-2`) marks the story and nothing else.
- [ ] At most one highlighter band per screen; no yellow data.
- [ ] Display / body / data fonts each in their role; sentence case; no
      tracked uppercase.
- [ ] Square corners, no shadows, no gradients.
- [ ] No empty half-width bands on desktop.
- [ ] Light and dark both checked; new data colors validated with
      `check:palette` on all four surfaces.
- [ ] Touch targets 44px; focus outline 2px `--ink` visible.
