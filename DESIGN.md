---
name: Marco Herbas Lopez
description: Energy data you can count. Picture statistics in flat poster colours on a cool paper ground.
colors:
  paper: "#EDF0F1"
  panel: "#FFFFFF"
  ink: "#15181C"
  ink-2: "#3C424A"
  ink-3: "#565D67"
  rule: "#C5CCD2"
  grid: "#DDE2E6"
  context-blue: "#2F5D9E"
  story-red: "#D63B26"
  group-green: "#286B4A"
  field-blue: "#2F5D9E"
  field-red: "#B8321F"
  field-green: "#286B4A"
  field-ochre: "#F0B429"
  on-field: "#FFFFFF"
  on-ochre: "#15181C"
  marker: "#F0B429"
typography:
  display:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "clamp(44px, 9vw, 80px)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "32px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "26px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1
  figure:
    fontFamily: "Atkinson Hyperlegible Next Variable, Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "72px"
    fontWeight: 800
    lineHeight: 1
rounded:
  base: "6px"
  inner: "4px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "12px"
  md: "20px"
  lg: "28px"
  xl: "56px"
  page-gutter: "20px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "0 24px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.ink-2}"
    textColor: "{colors.paper}"
  step-button:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 16px"
    height: "44px"
  step-button-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  picture-panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.base}"
    padding: "28px"
  project-tile:
    backgroundColor: "{colors.field-blue}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.base}"
  project-tile-ochre:
    backgroundColor: "{colors.field-ochre}"
    textColor: "{colors.on-ochre}"
  next-project-tile:
    backgroundColor: "{colors.field-blue}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.base}"
    padding: "22px 24px"
---

# Design system: Marco Herbas Lopez

## Overview

**Creative north star: "The Counting Wall"**

The site counts things with you. Every number is a row of identical little pictograms you can count, in the Vienna Method tradition of Neurath's picture statistics, and one of them is coloured differently. The home page opens with 1,000 uranium atoms, 7 of them red, and three buttons that turn that into 50 and then 900. Everything else (the project tiles, the language row, the next-project tile) borrows that vocabulary: flat cut-paper shapes, saturated poster colour, black text, soft 6px corners.

The voice is relaxed but credible. It says "Energy data you can count." and "Write to me", not slogans. Copy is sentence case, percentages are written tight ("84%"), and nothing is invented: no clients, no CV padding, no phone number. Depth does not exist. Surfaces are flat, separated by colour and a one-pixel rule at most. The one typeface is Atkinson Hyperlegible Next, used heavy for headings and regular for reading, so the page feels chunky and friendly without being childish.

The build matches the OWN-WORLD brief. One divergence: the four chart pages still carry Blueline-era internals (dashed graticules, an extra technology palette on the Bolivia map, a square tooltip). They sit inside the new frame and are listed under drift at the end, not treated as the system.

**Key characteristics:**
- Rows of identical symbols, one coloured differently, are the signature.
- Flat colour fields (blue, red, green, ochre) hold the project tiles; text sits on them in white, or black on ochre.
- Red means the story and nothing else.
- One typeface, two weights doing the work (800 and 400/600).
- Light and dark themes, following the visitor's system setting until they choose.

## Colors

A cool off-white ground, black ink, Neurath blue for context and signal red for the one thing the visitor should count. Green and ochre appear as colour fields and as a second group, never as the story.

All values below are the light theme and are the normative tokens in the frontmatter. The dark theme keeps the same roles with lifted values: paper `#11151B`, panel `#1A2029`, ink `#EDF0F1`, context blue `#7EA2DA`, story red `#FF6A50`, group green `#5FBF8F`. The colour fields (`--field-*`) do not change between themes.

### Primary
- **Signal Red** (`story-red` #D63B26, dark #FF6A50): the story, as chart marks and key figures: the lit atoms and the big count on the home page. Nothing else may be this colour.
- **Poster Red Field** (`field-red` #B8321F): the red project tile and the closing "Write to me" band at the end of the home page, where no story mark is on screen. Darker than Signal Red so white text clears contrast.

### Secondary
- **Neurath Blue** (`context-blue` / `field-blue` #2F5D9E, dark mark #7EA2DA): context, meaning every unlit atom, link underlines, the default tile field and the next-project tile.
- **Field Green** (`group-green` / `field-green` #286B4A, dark mark #5FBF8F): a second group that is not the story, such as women versus men, and the green tile field.

### Tertiary
- **Ochre Field** (`field-ochre` #F0B429): a tile field, the text-highlight band and the selection colour. Text on it is ink, never white.

### Neutral
- **Cool Paper** (`paper` #EDF0F1): page ground.
- **White Panel** (`panel` #FFFFFF): the surface that holds a picture statistic or a chart thumbnail.
- **Ink** (`ink` #15181C): headings, body emphasis, pressed buttons.
- **Ink 2** (`ink-2` #3C424A): running text and lead paragraphs.
- **Ink 3** (`ink-3` #565D67): small labels and secondary facts.
- **Rule** (`rule` #C5CCD2) and **Grid** (`grid` #DDE2E6): the one-pixel header and footer rules, button outlines, chart gridlines.

### Named rules
**The Red Is The Story Rule.** Signal red marks the thing the visitor is meant to count or compare, once per view. It is never decoration, never a second button colour on the same screen as a red mark, and never a hover state.

**The Colour Is Fill Rule.** Colour lives in fills (tiles, marks, buttons). Text over a field is white, or ink on ochre. Coloured text is reserved for the one key figure.

**The Three Slots Rule.** Charts use three categorical slots: context blue, story red, group green. A fourth hue needs a written reason on the page that introduces it.

## Typography

**Display, body and data font:** Atkinson Hyperlegible Next (variable, with system-ui as fallback). The tokens also hold Barlow Semi Condensed and Literata, but the Isotype world points display and body both at Atkinson, so those two are legacy.

**Character:** Open, wide-apertured letterforms made for legibility, set heavy where it speaks and light where it explains. Tabular figures keep counts steady while they change.

### Hierarchy
- **Display** (800, clamp(44px, 9vw, 80px), 1.02, -0.025em): the home headline only.
- **Headline** (800, 32px, 1.1, -0.01em): section headings (Projects, About). Project page h2s are 800 at 28px.
- **Title** (800, 26px, 1.1): tile titles; 36px on the double-width newest tile at 960px and up.
- **Body** (400, 19px for lead paragraphs, 17px base and on small screens, 1.5 to 1.6): text colour is ink-2. Keep reading text near 46 to 64 characters (`--measure` 64ch; the hero lead is 46ch, the About lead 60ch).
- **Label** (600, 16 to 18px): buttons, navigation, meta lines. Sentence case, no tracking, no uppercase.
- **Figure** (800, 56px, 72px from 560px, tabular numerals): the live count beside the atom grid, in Signal Red.

### Named rules
**The Sentence Case Rule.** Every heading, button and label is sentence case. No all-caps labels, no small-caps kickers above headings, no tracked-out eyebrows.

**The Tight Percent Rule.** Percentages sit against the number: "84%", never "84 %". Counts use thousands separators: "1,000".

## Layout

One centred column, max 1180px, 20px side gutter, 40px top and 64px bottom padding on each section wrapper (sections trim these to 24 to 48px). Layouts are mobile first and change at 560px, 700px and 960px.

The hero is a two-column grid at 960px and up (5fr text, 7fr picture, 56px gap). Below that the atom grid follows the headline, lead and buttons directly, before any other prose. The gallery is one column on phones and two from 700px, with a 16 to 20px gap; the newest project spans both columns and, at 960px, lays its picture and text side by side. There is one gallery on the site and each project appears in it once. About is a lead paragraph and a three-column fact list (one column on phones). The page then closes on a full-width Poster Red Field band holding one large "Write to me" link.

Spacing is a loose 4px-based rhythm: 8, 12, 16, 20, 28 and 56px are the working steps. Touch targets are at least 44px tall. Reading text uses `text-wrap: pretty` and headings `balance`.

## Elevation & Depth

Flat. There are no shadows anywhere in the system. Depth is carried by colour fields against the paper ground, white panels on paper, and a one-pixel rule under the header and above the footer. Focus is the only thing that lifts: a 3px ink outline offset 3px on tiles and a 2px outline offset 2px on buttons and links.

### Named rules
**The No Shadow Rule.** No box-shadow, no hard offset shadow, no glow. Separate surfaces with colour or a rule.

## Shapes

Soft cut-paper. Tiles, panels, key-figure boxes and the next-project tile use a 6px radius; the white figure inside a tile uses 4px; buttons, step buttons and the theme toggle are full pills (999px). Chart marks stay geometric and identical: the atom is a filled nucleus with one tilted orbit, 12px on a 12px pitch, grouped in tens (8px gaps) so rows can be counted. The language row uses four small speech-bubble shapes in the four field colours. The nucleus logo is flat discs, red protons and blue neutrons, with a paper-coloured outline.

## Components

### Buttons
- **Shape:** full pill (999px), 48px tall for the main action.
- **Primary ("Write to me"):** ink pill with paper 700 text, 0 24px padding. Hover goes to ink-2 over 0.2s. Never red: in the hero it sits next to the red atoms.
- **Secondary link ("See the projects"):** plain 600 text with a 2px blue underline, 44px minimum height.
- **Step buttons (atom counter):** outlined pills, 1.5px rule border, 44px tall, label plus a muted percentage ("As mined 0.7%"). The pressed state fills with ink and paper text and sets `aria-pressed`. On phones the percentage is hidden. They appear only when JavaScript runs.
- **Theme toggle:** a small outlined pill in the header, labelled "Dark theme" or "Light theme" for what it switches to.

### Picture panel (signature)
The atom counter. A white panel (6px radius, 28px padding, 14px on phones) holds the live count in Signal Red, the step buttons, an SVG of 1,000 `<use>` references to a single `<symbol>` in rows of 40, and a key. Lit atoms are Signal Red, the rest Neurath Blue; a colour change eases over 0.25s and the lit atoms fill in reading order. A screen-reader-only live region repeats the count. Without JavaScript it shows natural uranium and the buttons stay hidden.

### Project tiles
- **Corner style:** 6px, clipped.
- **Background:** one colour field per tile in the order blue, red, green, ochre, repeating. Text is white, or ink on ochre.
- **Content:** the chart thumbnail on a white 4px-radius mat (16:10), then a band with an 800 title, a one-line description and a meta line (month, year and first tag).
- **Hover and focus:** the title underlines (3px, offset 5px). Focus shows a 3px ink outline.

### Navigation
- Header: nucleus mark, name in 800, a one-line descriptor (hidden below 560px), and links Projects, About, Contact in 600. Below 700px the links wrap to a second row. A one-pixel rule closes the header.
- A skip link ("Skip to content") sits above everything and appears on focus.
- Project pages open with a meta line: Projects / subject · month year.
- A **next-project tile** closes each project page: a blue field, a 15px label and an 800 title, same hover and focus as the gallery tiles.

### Key-figure box
A white panel with a 6px radius and no border, cells separated by the one-pixel rule. Small label at 14px in ink-2, value at 800. On phones it folds to two columns.

### Highlighter band
A marker-coloured band behind exactly one key figure, never a mark and never text colour.

## Do's and Don'ts

### Do:
- **Do** express every number as something countable first: a row of identical symbols with one coloured differently, then the digits.
- **Do** keep red for the story only, in both themes.
- **Do** keep copy relaxed but credible, in sentence case, with percentages written "84%".
- **Do** give each project one tile in one gallery and let its field colour rotate blue, red, green, ochre.
- **Do** keep a table, keyboard path and no-JS fallback for every chart.
- **Do** use only Atkinson Hyperlegible Next, with tabular numerals on counts.
- **Do** keep touch targets at least 44px tall and text contrast at AA in both themes.

### Don't:
- **Don't** use blueprint, drawing-sheet or revision-box language, or the cajetin vocabulary of the earlier world, in copy or in code comments for new work.
- **Don't** duplicate the gallery with a second list or a repeated thumbnail row.
- **Don't** use shadows or cream-and-serif defaults.
- **Don't** invent clients, testimonials, jobs or credentials, and don't add a phone number.
- **Don't** add dependencies to dress up a surface; use the system fonts already installed and plain SVG.
- **Don't** use uppercase labels, small kickers above headings or glyph icons; draw the symbol.

### Drift in the build, not part of the system
The chart internals still use Blueline-era rules: dashed graticules, a square 0-radius tooltip, and the five-colour generation palette for Bolivia (`--tech-*`, an approved one-off with ink outlines). The header toggle also keeps a 40px minimum height. New surfaces should follow the sections above, not these.
