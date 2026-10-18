# Brief: Olympic Sprint Freestyle (working title)

- **Slug:** `olympic-freestyle-sprint`
- **Code:** MHL-002
- **Status:** publish (text approved 2026-10-18; set to published, not pushed)
- **Started:** 2026-10-18

## The one sentence
Used in the page (headline: "More than 80% of the Olympic 100 m speed-up came before 1976"; intro: 29% and 37% faster, 81% and 88% by 1976). Waiting for Marco's approval.

Numbers from `src/data/olympic-freestyle-sprint/series.json`: men 65.6 s (1908) to
46.40 s (2024); women 82.2 s (1912) to 52.16 s (2024). The share by 1976 is the best
champion time up to that year divided by the total change. The first points are not
like-for-like (see data caveats), so the text must say so.

## Question and reader
- Question the chart answers: where, in 116 years, did the Olympic sprint get faster?
- Main reader: curious general public.
- They know swimming is timed to the hundredth; they do not know that the 50 m
  freestyle only joined the Games in 1988, or that early Olympic races were not
  swum in a normal pool.

## What the data says so far (read 2026-10-18, to re-check in the Words phase)
1. Early gain: yes. By 1976 the 100 m had made 81 % (men) and 88 % (women) of its
   total gain. By 1964: 64 % and 76 %.
2. The 50 m is not flat. Since 1988: 50 m men -4.0 %, women -7.0 %; 100 m men -4.6 %,
   women -5.0 %. Both distances keep improving at a similar rate. Closing note only.
3. Women/men time ratio in the 100 m: 1.30 (1912), 1.09 (1980), about 1.12 since 2000.
4. 2008 suits: visible in men only (47.21 in 2008, 47.52 in 2012, 47.58 in 2016,
   47.02 in 2020). Causes need a source before they are mentioned.
5. Today's 8th place (2024) would have won gold at every Games up to 2004 (100 m men,
   50 m both sexes) and up to 2008 (100 m women).
6. Spread between 1st and 8th: from about 3 s (1948) to about 1 s; men's 100 m 2024
   is wider again because of the 46.40 world record.

## Scope
- In the MVP: line chart of the Olympic champion's time, 50 m and 100 m freestyle,
  men and women, 1908-2024.
  - Controls: distance (50 / 100 m); sex (men / women / both, inactive series stays
    grey as context).
  - Layers: champion line; band of finalists (positions 1-8) only where all eight
    times exist (from 1948 in the 100 m, from 1988 in the 50 m); annotation marks.
  - Fixed x axis 1908-2024, linear time, so gaps are real gaps. The 50 m series
    starts in 1988; the empty space carries "event not contested until 1988".
  - X marker on editions not held (1916, 1940, 1944), with a legend line
    ("not held due to war", source Olympedia).
  - A different marker on 1980 and 1984 (political absences), with a legend line.
  - Tokyo 2020 is drawn at 2021, labelled "Tokyo 2020, held 2021".
  - Co-champions kept: two points on the same time (men 50 m 2000; women 100 m 1984, 2016).
  - Legend line for the early courses: 1908 a 100 m pool swum straight with no turns,
    1912 open water in Stockholm harbour. Style of the 1912 point decided in Form.
  - Text panel on the right with the insights (Words phase).
- Out: 1896-1906 and the 1904 100 yards (open water / not metric); other strokes and
  distances, relays, world-record progression, suit technology beyond one annotation.

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| Final results positions 1-8, 100 m men 1908-2024 | Olympedia, https://www.olympedia.org/event_names/553 (per-Games pages in `raw/` extract) | 2026-10-18 | seconds | |
| Same, 100 m women 1912-2024 | https://www.olympedia.org/event_names/588 | 2026-10-18 | seconds | |
| Same, 50 m men 1988-2024 | https://www.olympedia.org/event_names/551 | 2026-10-18 | seconds | |
| Same, 50 m women 1988-2024 | https://www.olympedia.org/event_names/587 | 2026-10-18 | seconds | |
| Second source for champion times | Wikipedia "100 metre freestyle" and per-Games event pages | 2026-10-18 | seconds | All 73 equal to Olympedia |
| Games not held, Tokyo held 2021 | https://www.olympedia.org/editions | 2026-10-18 | n/a | |
| Absences | Wikipedia "List of Olympic Games boycotts", "1920 Summer Olympics", "1948 Summer Olympics" | 2026-10-18 | n/a | Rule-based list kept in `series.json`; chart shows 1980, 1984 |
| Early courses | Wikipedia 1908 men's 100 m page; 1912 swimming page | 2026-10-18 | n/a | |

Known reference values: men 100 m 1988 48.63; women 100 m 1988 54.93; men 50 m 1988
22.14; women 50 m 1988 25.49; men 100 m 1908 1:05.6, 2024 46.40.

Data caveats:
- `raw/olympedia_finals_extract.txt` is the table text copied from each page, not the
  original HTML (the shell cannot reach olympedia.org). Each block has a CRC32 that
  `build_data.py` checks.
- Silver, bronze and positions 4-8 come from Olympedia only.
- Time resolution: tenths up to 1968, hundredths from 1972.
- Finals before 1948 have fewer than eight timed finishers, so no band there.
- One champion discrepancy found and resolved: women 100 m 1992 is 54.64 (Olympedia and
  the Wikipedia event page citing the official report); the aggregate Wikipedia page
  says 54.65.
- 1920 men 100 m: the final was re-swum; the official time (1:01.4) is the re-swim.
- 1960 men 100 m: Olympedia lists the silver (55.1) faster than the gold (55.2).

## Form and interaction (phase 3, for Marco's OK)
Form: line over time (the question is change over time). One y axis in seconds,
lower is faster, fixed for each distance and window (it does not rescale when you switch
sex, so the grey context line stays fully visible); switching redraws with a 400-500 ms fade. Greyscale
sketch with real data: see the image sent in chat on 2026-10-18.

Layers, bottom to top: grid; band 1st to 8th place (only where all 8 times exist:
from 1948 in the 100 m, from 1988 in the 50 m; broken at gaps); champion line
(broken where Games were not held); markers; direct labels at the line end
("Men", "Women"); up to four numbered annotation marks tied to the insights text.

Marks: filled dot = champion; hollow diamond = different course (1908 straight
pool, 1912 open water); hollow dot = major nations absent (1980, 1984); ringed dot =
co-champions; x in a lane under the x axis = Games not held (1916, 1940, 1944). The
lane keeps the x off the data, so no y value is invented. Legend lines for each.

Axes: x is linear time, fixed 1908-2024 (the 50 m series fills only the last third and
the rest says "event not contested until 1988"). Tokyo 2020 sits at 2021. A small
"lower = faster" cue on the y axis.

Controls: Distance [50 m | 100 m], default 100. Swimmers [Women | Men | Both],
default Both; inactive series stays grey when one sex is selected. Window
[1908-2024 | Since 1988] (optional): rescales both axes to show the recent detail the
full view squashes.

Reading a value: hover on desktop; tap or drag on phone selects the nearest edition by
x (27 editions in about 300 px leave no room for per-point targets). Vertical guide plus
a card pinned under the chart on every screen size (a floating card covered the data
in the build test; on wide screens the two sexes sit side by side): Games and year ("held 2021" for Tokyo), champion(s), country, time as the
source prints it plus seconds, silver and bronze with times, 8th-place time when it
exists, and the edition note if any (1908 and 1912 course, 1920 re-swim, absences).
Keyboard: the chart takes focus; left/right arrows step editions, Home/End jump, Esc
clears. Previous/next buttons for touch. The card is also an aria-live region.
Record flags (OR/WR) are not reliable in the current data; they stay out of the card
until sourced.

Layout, desktop (>= 1000 px): headline across the top; figure about 64 % on the left,
insights about 36 % on the right, top-aligned; legend under the figure; then the
table `<details>`; then "Notes and method".

    eyebrow
    H1: a sentence with the number
    +---------------------------------+  +------------------+
    | [50|100] [Women|Men|Both] [Win] |  | 1  insight       |
    | y axis, bands, lines, marks     |  | 2  insight       |
    | x axis                          |  | 3  insight       |
    | lane: x x  x                    |  | 4  insight       |
    | legend                          |  |                  |
    +---------------------------------+  +------------------+
    > Table view
    Notes and method

Layout, phone (360 px): headline, two lines of intro, controls on two rows (44 px
targets), chart full width (about 320 px tall), edition card pinned under the chart
(never over the finger), legend in two columns, insights as a numbered list, table,
method. The SVG viewBox follows the container size and redraws on resize, so text
stays 11-12 px; fewer x ticks and at most three annotation marks.

Without JavaScript: headline, text and a server-rendered table still carry the story.

Build plan: `src/components/viz/olympic-freestyle-sprint/SprintChart.astro` (markup,
controls, d3 script), `SprintTable.astro`, page
`src/pages/projects/olympic-freestyle-sprint.mdx`. Plain Astro, d3 v7 modules, tokens
only. Men/women colours come from the site tokens and go through `check:palette`.
Out of the MVP: a second index chart comparing 50 and 100 m since 1988 (the closer
stays in the text).

## Decisions (Marco, 2026-10-18)
- 50 m and 100 m, with selector; start in 1908; X for not-held years.
- Thesis direction: where the gain happened (curve shape); the 50 m since 1988 as a closer.
- Absence marker only for 1980 and 1984.
- Tokyo 2020 plotted at 2021.

## Open questions
- Course by edition: 1920 (Stade Nautique d'Anvers) and 1924 (Piscine des Tourelles)
  pool length and type not found yet. The legend wording depends on it.
- 1960 men 100 m: why the silver time is faster than the gold. Source before mentioning.
- Approve the one sentence above (the 1908 and 1912 starting points are not like-for-like).
- Title.
