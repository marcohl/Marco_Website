# Brief: Olympic champion times, all individual pool events (working title)

- **Slug:** `olympic-freestyle-sprint` (kept: same page and URL, as agreed with Marco on 2026-10-28)
- **Code:** MHL-002
- **Revision:** B (scope widened from 50/100 m freestyle to the 28 individual pool events)
- **Status:** phase 1 approved 2026-10-28 (thesis A, B as closing note; 10 km out); phase 2 (data) done, checks pass; phase 3 (form) waiting for Marco
- **Started:** 2026-10-18; rev B started 2026-10-28

## The one sentence
**Approved by Marco, 2026-10-28: A as the headline, B as the closing note.** Both computed from
`src/data/olympic-freestyle-sprint/events.json`. The two candidates:

**A. Keep the approved story, now for every old event.**
"In the nine events swum since 1924 or earlier, at least 81 % of the Olympic speed-up came before 1976."
Share of total change = (first champion time - best champion time up to 1976) / (first champion time -
2024 champion time). Values: men 100 m free 81 %, women 100 m free 88 %, men 400 m free 91 %, women 400 m
free 90 %, men 1500 m free 94 %, men 100 m back 89 %, women 100 m back 83 %, men 200 m breast 85 %,
women 200 m breast 81 %. Weak point: the first points are not like-for-like (see data caveats), and
the claim cannot be made for events that joined later (see B).

**B. A same-window claim for all 26 events that exist in both 1988 and 2024.**
"Since 1988 the Olympic champion has got faster in all 26 events, by 1.8 % to 7.0 %."
The gain is smallest in freestyle from 200 m up (1.8 % to 3.7 %, women's 800 m the lowest) and largest in
the 50 m, butterfly, breaststroke and backstroke races (3.6 % to 7.0 % for every other event). Same window for every
event, so no like-for-like problem with early Games. Weak point: "all faster" is a weaker headline than A,
and 3.6 % (women's 400 m medley) sits below 3.7 % (women's 200 m free), so the freestyle/other split is a tendency, not a rule.

Chosen: A as the headline (it continues the approved text and is the stronger finding), B as the
closing note, shown in the compare view. Needs the Words phase to say plainly that A is a shape claim about
champions' best times, and what it does not say (no cause).

## Question and reader
- Question the chart answers: where, in 116 years, did Olympic swimming get faster, event by event?
- Main reader: curious general public. Second reader: recruiter or peer who opens the method and code.
- They know swimming is timed to the hundredth. They do not know that most events are younger than they
  think (women's 800 m free joined in 1968, men's 800 m free in 2020), that the early races were not swum
  in a normal pool, or that butterfly was once a breaststroke variant.

## Scope
- In: champion time per Olympic Games, 1908-2024, for the 28 individual pool events of the Paris 2024
  programme (14 per sex): freestyle 50, 100, 200, 400, 800, 1500 m; backstroke 100, 200; breaststroke 100,
  200; butterfly 100, 200; medley 200, 400. 486 finals in total.
  - Layers kept from rev A: champion line; finalist band (1st to 8th) only where all eight times exist;
    marks for different course (1908, 1912), political absences (1980, 1984), co-champions, Games not held;
    Tokyo 2020 plotted at 2021.
  - Tables for every event in `<details>`, grouped by stroke.
- Out: relays; 10 km marathon swimming (open water, not timed like a pool race); the 1904 races (yards);
  1896-1906 open-water races and the 1906 Intercalated Games; discontinued events (men's 400 m breaststroke,
  500 m, 1000 m, 4000 m, women's 300 m freestyle); world-record progression; suit technology beyond an annotation;
  doping (no source in hand, no claim).
- The 10 km marathon is out (Marco, 2026-10-28).

## Data
| Dataset | Source (URL) | Accessed | Units | Notes |
|---|---|---|---|---|
| Final results, positions 1-8, 28 events, 1908-2024 | Olympedia, https://www.olympedia.org/results/<id> per final; event index pages https://www.olympedia.org/event_names/<id> (ids in `build_data.py`) | 2026-10-28 (50/100 m freestyle first read 2026-10-18) | seconds | 486 finals |
| Second source for champion times | Wikipedia "Swimming at the YYYY Summer Olympics - Men's/Women's N metre stroke", all 486 pages | 2026-10-28 | seconds | `analysis/olympic-freestyle-sprint/second_source_wikipedia.txt` |
| Games not held, Tokyo held 2021 | https://www.olympedia.org/editions | 2026-10-18 | n/a | |
| Absences | Wikipedia "List of Olympic Games boycotts", "1920 Summer Olympics", "1948 Summer Olympics" | 2026-10-18 | n/a | Rule-based list in the data; the chart marks 1980 and 1984 |
| Early courses | Wikipedia 1908 men's 100 m page; 1912 swimming page | 2026-10-18 | n/a | |

Checks that pass in `build_data.py` (run 2026-10-28):
- CRC32 of every block of the raw extract and of the second-source file.
- Editions per event equal the programme list (28 events, 486 finals). The same lists equal the years on
  the 28 Olympedia index pages (one-time comparison in the browser), except a 1920 women's "400 m freestyle"
  that was a 300 m race; it is left out.
- All 486 champion times equal the Wikipedia time, except two explained ones: men's 100 m free 1920 (Wikipedia prints
  the first final, 1:00.4; Olympedia the re-swim, 1:01.4) and women's 800 m free 1984 (8:24.96 in Wikipedia's
  Final table, 8:24.95 in its summary box and in Olympedia).
- The 73 freestyle 50/100 m finals read on 2026-10-18 equal the 2026-10-28 read in names, countries, times and dates.
- Six reference values (1988 winners in 50 and 100 m, men's 100 m 1908 and 2024).
- Times never decrease with position, except three documented editions (below).

Data caveats:
- `raw/olympedia_finals_extract.txt` is cell text read from each result page in Chrome, not the original
  HTML (the shell cannot reach olympedia.org). Each block carries a CRC32 that `build_data.py` checks.
- Only finalists with a printed time are kept. DNS and DQ rows are dropped, so a final with a DNS or DQ has fewer
  than 8 rows and no band (for example women's 200 m medley 2024).
- Silver, bronze and positions 4-8 come from Olympedia only.
- Time resolution: tenths up to 1968, hundredths from 1972.
- Finals before 1948 mostly have fewer than eight timed finishers, so no band there.
- Co-champions: men's 50 m free 2000, women's 100 m free 1984 and 2016.
- Order anomalies in Olympedia: men's 100 m free 1960 (silver 55.1 faster than gold 55.2), men's 200 m breaststroke
  1948 (4th 2:43.7 faster than bronze 2:43.9; Wikipedia says timekeepers and judges disagreed, flagged "citation
  needed"), women's 200 m breaststroke 1948 (5th 3:06.2, 6th 3:06.1; reason not found). None is mentioned
  in text until sourced.
- Women's 100 m free 1992 is 54.64 (Olympedia and the event page citing the official report); the aggregate
  Wikipedia page says 54.65.
- Like-for-like problems, to state on the page: 1908 men's 100 m was one length of a purpose-built pool; 1912 was
  open water in Stockholm harbour; 1920 and 1924 pools not confirmed; 1920 men's 100 m free is a re-swim; until
  1956 the butterfly arm action was allowed in breaststroke races, so the early 200 m breaststroke times
  (men 1908-1952, women 1924-1952) are a different race (source: Wikipedia 1948 women's 200 m breaststroke page;
  check its reference). Hand timing to 0.1 s changed to electronic timing with hundredths in 1972 (the exact change
  and date need a source).

## Form and interaction (phase 3, for Marco's OK once the thesis is chosen)
Kept from rev A (approved): line over time, one y axis in seconds, fixed per event, lower is faster; same
marks and layers; hover/tap card pinned under the chart; keyboard steps editions; no JavaScript falls back to
headline, text and tables.

Changes proposed:
1. Event picker: stroke [Freestyle | Backstroke | Breaststroke | Butterfly | Medley], then distance, then
   sex [Women | Men | Both]. Default view: 100 m freestyle, both sexes (the page people already know).
2. y axis format: seconds for races under 2 min, m:ss from 2 min up; ticks chosen per event.
3. Window toggle: all editions, or since 1988 (the common window for 26 events).
4. New view "Compare events" (decide with the thesis): one line per event of the chosen sex, y = % of the total improvement
   reached (0 % at the first edition, 100 % at 2024), selected event in the accent colour, others grey.
   One measure, one axis. Directly shows claim A.
5. Tables: one per event in `<details>`, grouped by stroke.
6. Callouts: 1920 re-swim, 1908/1912 course, 2020 held in 2021, plus the sourced rule change in breaststroke;
   unsourced anomalies stay out.
7. Phone (360 px): pickers collapse into two rows of segmented controls; compare view shows the selected line only
   plus a grey envelope.

Build plan: `SprintChart.astro` gets the event picker and compare view (or a second component
`CompareChart.astro` if the file gets too large); `SprintTable.astro` takes any event; the home-page
thumbnail reads the 100 m free series from `events.json` ids `M100FR` and `W100FR`; `series.json` is deleted when the
components switch to `events.json`. Colours only from `tokens.css`; any new categorical colour goes through `check:palette`.

## Decisions (Marco)
- 2026-10-18: 50 m and 100 m with selector; start in 1908; X for not-held years; absence marker only for 1980
  and 1984; Tokyo 2020 at 2021.
- 2026-10-28: widen to all individual pool events (relays out); update the existing page (same URL).
- 2026-10-28: thesis A (headline) with B as closing note; 10 km marathon out.

## Open questions
- Form and interaction of rev B (section above).
- Course by edition: 1920 (Stade Nautique d'Anvers) and 1924 (Piscine des Tourelles) pool length and type not found.
- Reasons for the three order anomalies above.
- Start of electronic timing and hundredths: source needed before the text says it.
- Title: the slug stays `olympic-freestyle-sprint`; the page title and headline should drop "sprint freestyle".
