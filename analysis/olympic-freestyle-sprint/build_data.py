"""Build the data for the olympic-freestyle-sprint project (MHL-002).

Scope: the 28 individual pool events of the Paris 2024 programme (14 per sex:
freestyle 50/100/200/400/800/1500 m, backstroke 100/200, breaststroke 100/200,
butterfly 100/200, medley 200/400), every Olympic edition from 1908 to 2024.

Reads the Olympedia final-results extract in raw/, verifies its integrity,
checks every champion time against a second source and known reference values,
and writes src/data/olympic-freestyle-sprint/events.json.

Units: all times are seconds (float). Olympedia gives tenths of a second until
1968 and hundredths from 1972; `decimals` keeps the printed resolution of each time.

Sources (accessed 2026-10-28; the freestyle 50/100 m part first on 2026-10-18):
  - Final results: Olympedia result pages, https://www.olympedia.org/results/<id>
  - Event index:   https://www.olympedia.org/event_names/<id> (see EVENTS)
  - Games not held / held 2021: https://www.olympedia.org/editions
  - Second source for champion times: Wikipedia per-Games event pages, stored in
    second_source_wikipedia.txt.
  - Absences: Wikipedia "List of Olympic Games boycotts", "1920 Summer
    Olympics", "1948 Summer Olympics".

One-time check done in the browser on 2026-10-28: the years listed on the 28 Olympedia
event index pages (status "Olympic", 1908 onwards, metres) equal the years in the raw
extract, with one exception: the index lists a 1920 women's "400 m freestyle" that was
a 300 m race. It is left out of the extract and of EXPECTED_YEARS.
"""
import json
import re
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "raw" / "olympedia_finals_extract.txt"
SECOND = HERE / "second_source_wikipedia.txt"
OUT = ROOT / "src" / "data" / "olympic-freestyle-sprint" / "events.json"
RESULT_URL = "https://www.olympedia.org/results/{}"
INDEX_URL = "https://www.olympedia.org/event_names/{}"
ACCESSED = "2026-10-28"

STROKES = {"FR": "freestyle", "BK": "backstroke", "BR": "breaststroke", "FL": "butterfly", "IM": "medley"}

# Olympedia event_names ids (the page title of each was read on 2026-10-28).
INDEX_ID = {
    "M50FR": 551, "M100FR": 553, "M200FR": 555, "M400FR": 557, "M800FR": 560, "M1500FR": 563,
    "M100BK": 570, "M200BK": 572, "M100BR": 573, "M200BR": 574, "M100FL": 577, "M200FL": 578,
    "M200IM": 579, "M400IM": 580,
    "W50FR": 587, "W100FR": 588, "W200FR": 589, "W400FR": 591, "W800FR": 592, "W1500FR": 2570,
    "W100BK": 595, "W200BK": 596, "W100BR": 597, "W200BR": 598, "W100FL": 599, "W200FL": 600,
    "W200IM": 601, "W400IM": 602,
}

# Games with a swimming programme, 1908-2024 (1916, 1940 and 1944 were not held).
GAMES = [1908, 1912] + list(range(1920, 1937, 4)) + list(range(1948, 2025, 4))


def _from(start, skip=()):
    return [y for y in GAMES if y >= start and y not in skip]


# Years each event was contested, 1908 onwards. Checked against the Olympedia event index
# pages (see the module docstring); the counts are 10, 27, 15, 27, 2, 27, 26, 16, 15, 27, 15,
# 18, 13, 16 for the men's events in the order of INDEX_ID, and the women's counts follow.
EXPECTED_YEARS = {
    "M50FR": _from(1988), "M100FR": _from(1908), "M200FR": _from(1968), "M400FR": _from(1908),
    "M800FR": [2020, 2024], "M1500FR": _from(1908),
    "M100BK": _from(1908, skip=(1964,)), "M200BK": _from(1964),
    "M100BR": _from(1968), "M200BR": _from(1908),
    "M100FL": _from(1968), "M200FL": _from(1956),
    "M200IM": _from(1968, skip=(1976, 1980)), "M400IM": _from(1964),
    "W50FR": _from(1988), "W100FR": _from(1912), "W200FR": _from(1968), "W400FR": _from(1924),
    "W800FR": _from(1968), "W1500FR": [2020, 2024],
    "W100BK": _from(1924), "W200BK": _from(1968),
    "W100BR": _from(1968), "W200BR": _from(1924),
    "W100FL": _from(1956), "W200FL": _from(1968),
    "W200IM": _from(1968, skip=(1976, 1980)), "W400IM": _from(1964),
}
EVENTS = {}
for _id, _years in EXPECTED_YEARS.items():
    _m = re.fullmatch(r"([MW])(\d+)([A-Z]{2})", _id)
    EVENTS[_id] = {"sex": "men" if _m[1] == "M" else "women", "distance_m": int(_m[2]),
                   "stroke": STROKES[_m[3]], "index": INDEX_URL.format(INDEX_ID[_id])}

# Order used in the output: stroke, then distance, then men before women.
_STROKE_ORDER = list(STROKES.values())
EVENT_ORDER = sorted(EVENTS, key=lambda e: (_STROKE_ORDER.index(EVENTS[e]["stroke"]),
                                            EVENTS[e]["distance_m"], EVENTS[e]["sex"] != "men"))

# Games not held. Source: https://www.olympedia.org/editions ("Not held due to war").
NOT_HELD = [
    {"year": 1916, "host": "Berlin", "reason": "war"},
    {"year": 1940, "host": "Helsinki", "reason": "war"},
    {"year": 1944, "host": "London", "reason": "war"},
]

# Known reference values read independently of the DOM extract (2026-10-18).
REFERENCE = {
    ("M100FR", 1908): "1:05.6", ("M100FR", 1988): "48.63", ("M100FR", 2024): "46.40",
    ("W100FR", 1988): "54.93", ("M50FR", 1988): "22.14", ("W50FR", 1988): "25.49",
}

# Editions where the second source prints another champion time than Olympedia, and why.
# W100FR 1992: the aggregate Wikipedia page "100 metre freestyle" says 54.65; the 1992 event
# page (which cites the official report) and Olympedia say 54.64. 54.64 is used.
SECOND_SOURCE_DIFFS = {
    ("M100FR", 1920): "The Wikipedia page prints the first final (1:00.4). The final was re-swum "
                      "and Olympedia gives the re-swim (1:01.4).",
    ("W800FR", 1984): "Wikipedia's Final table prints 8:24.96, its summary box and Olympedia 8:24.95.",
}
# Editions where Olympedia lists a lower-placed finalist with a faster time.
KNOWN_ORDER_ANOMALIES = {("M100FR", 1960), ("M200BR", 1948), ("W200BR", 1948)}
# Editions with more than one gold medal.
EXPECTED_TIES = {("W100FR", 1984), ("W100FR", 2016), ("M50FR", 2000)}

# Absences, source https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts
# (1956, 1976, 1980, 1984, 1988) and the 1920 / 1948 Games pages.
ABSENT = {
    1920: {"reason": "not invited after World War I",
           "source": "https://en.wikipedia.org/wiki/1920_Summer_Olympics",
           "countries": ["Germany", "Austria", "Hungary", "Bulgaria", "Turkey"]},
    1948: {"reason": "not invited (Allied occupation)",
           "source": "https://en.wikipedia.org/wiki/1948_Summer_Olympics",
           "countries": ["Germany", "Japan"]},
    1956: {"reason": "boycott", "source": "https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts",
           "countries": ["Egypt", "Iraq", "Lebanon", "Liechtenstein", "Monaco", "Netherlands",
                         "Netherlands Antilles", "Cambodia", "Panama", "Spain", "Switzerland", "China"]},
    1976: {"reason": "boycott", "source": "https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts",
           "countries": ["Afghanistan", "Albania", "Algeria", "Benin", "Cameroon", "Central African Republic",
                         "Chad", "Republic of the Congo", "Egypt", "Ethiopia", "Gabon", "Gambia", "Ghana",
                         "Guyana", "Iraq", "Kenya", "Libya", "Lesotho", "Madagascar", "Malawi", "Mali",
                         "Morocco", "Myanmar", "Niger", "Nigeria", "Somalia", "Sri Lanka", "Sudan",
                         "Eswatini", "Syria", "Chinese Taipei", "Tanzania", "Togo", "Tunisia", "Uganda",
                         "Upper Volta", "Zambia"]},
    1980: {"reason": "boycott", "source": "https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts",
           "countries": ["Albania", "Antigua and Barbuda", "Argentina", "Bahamas", "Bahrain", "Bangladesh",
                         "Barbados", "Belize", "Bermuda", "Bolivia", "Canada", "Cayman Islands",
                         "Central African Republic", "Chad", "Chile", "China", "Egypt", "El Salvador", "Fiji",
                         "Gabon", "Gambia", "Ghana", "Haiti", "Honduras", "Hong Kong", "Indonesia", "Iran",
                         "Israel", "Ivory Coast", "Japan", "Kenya", "South Korea", "Liberia", "Liechtenstein",
                         "Malawi", "Malaysia", "Mauritania", "Monaco", "Mauritius", "Morocco",
                         "Netherlands Antilles", "Niger", "North Yemen", "Norway", "Pakistan", "Panama",
                         "Papua New Guinea", "Paraguay", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
                         "Somalia", "Sudan", "Suriname", "Eswatini", "Chinese Taipei", "Thailand", "Togo",
                         "Tunisia", "Turkey", "United Arab Emirates", "United States",
                         "United States Virgin Islands", "Upper Volta", "Uruguay", "West Germany", "Zaire"]},
    1984: {"reason": "boycott", "source": "https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts",
           "countries": ["Afghanistan", "Albania", "Angola", "Bulgaria", "Cuba", "Czechoslovakia",
                         "East Germany", "Ethiopia", "Hungary", "Iran", "Laos", "Libya", "Mongolia",
                         "North Korea", "Poland", "South Yemen", "Soviet Union", "Upper Volta", "Vietnam"]},
    1988: {"reason": "boycott", "source": "https://en.wikipedia.org/wiki/List_of_Olympic_Games_boycotts",
           "countries": ["Albania", "Cuba", "Ethiopia", "Madagascar", "Nicaragua", "North Korea", "Seychelles"]},
}
# Country names for the NOC codes Olympedia uses. Names must match the spelling in ABSENT.
NOC_NAME = {
    "USA": "United States", "HUN": "Hungary", "SWE": "Sweden", "ANZ": "Australasia", "GBR": "Great Britain",
    "JPN": "Japan", "AUS": "Australia", "BRA": "Brazil", "GER": "Germany", "URS": "Soviet Union",
    "FRG": "West Germany", "GDR": "East Germany", "FRA": "France", "EUN": "Unified Team", "RUS": "Russia",
    "NED": "Netherlands", "RSA": "South Africa", "CAN": "Canada", "BEL": "Belgium", "CHN": "China",
    "ROU": "Romania", "ROC": "ROC", "DEN": "Denmark", "ARG": "Argentina", "CRO": "Croatia",
    "HKG": "Hong Kong", "BLR": "Belarus", "AUT": "Austria", "BUL": "Bulgaria", "CRC": "Costa Rica",
    "CUB": "Cuba", "ESP": "Spain", "FIN": "Finland", "GRE": "Greece", "IRL": "Ireland", "ITA": "Italy",
    "KAZ": "Kazakhstan", "KOR": "South Korea", "LTU": "Lithuania", "MEX": "Mexico", "NOR": "Norway",
    "NZL": "New Zealand", "PHI": "Philippines", "POL": "Poland", "SGP": "Singapore", "SLO": "Slovenia",
    "SRB": "Serbia", "SUI": "Switzerland", "SUR": "Suriname", "SVK": "Slovakia", "TTO": "Trinidad and Tobago",
    "TUN": "Tunisia", "UKR": "Ukraine", "VEN": "Venezuela", "YUG": "Yugoslavia", "ZIM": "Zimbabwe",
}

# One entry per statement. `series` is an event id or "ALL". Every text needs a source.
ANNOTATIONS = [
    {"series": "M100FR", "year": 1920, "type": "re-swim",
     "text": "The final was re-swum after Norman Ross was disqualified on a protest. The time shown is the "
             "re-swim (1:01.4). The first final, with a faster 1:00.4 for the winner, is not the official result.",
     "source": "https://www.olympedia.org/results/4649"},
    {"series": "M100FR", "year": 1960, "type": "order",
     "text": "Olympedia lists the silver medallist 0.1 s faster than the gold medallist. The reason is not in "
             "this data; source it before any text mentions it.",
     "source": "https://www.olympedia.org/results/5489", "needs_source": True},
    {"series": "M100FR", "year": 1908, "type": "course",
     "text": "First Games with a purpose-built 100 m pool. The race was a single length of the pool, "
             "with no turns. Earlier Olympic swimming was in open water.",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1908_Summer_Olympics_%E2%80%93_Men%27s_100_metre_freestyle"},
    {"series": "M200BR", "year": 1948, "type": "order",
     "text": "Olympedia lists the 3rd-place time (2:43.9) slower than the 4th-place time (2:43.7). Wikipedia says "
             "the timekeepers had the 4th-place swimmer 0.2 s faster, while the judges ruled that the bronze "
             "medallist touched first (marked 'citation needed' on Wikipedia, so not confirmed).",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1948_Summer_Olympics_%E2%80%93_Men%27s_200_metre_breaststroke",
     "needs_source": True},
    {"series": "W200BR", "year": 1948, "type": "order",
     "text": "Olympedia lists the 5th-place time (3:06.2) slower than the 6th-place time (3:06.1). "
             "The reason is not in this data; source it before any text mentions it.",
     "source": "https://www.olympedia.org/results/5227", "needs_source": True},
    {"series": "M200BR", "year": 1956, "type": "rules",
     "text": "Until 1956 the butterfly arm action was allowed in breaststroke races. Butterfly became its own "
             "event in 1956 and was banned from breaststroke, so the early 200 m breaststroke times (men 1908-1952, "
             "women 1924-1952) are not like-for-like with the later ones. The 1948 women's page says this; "
             "check its cited reference in the Words phase.",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1948_Summer_Olympics_%E2%80%93_Women%27s_200_metre_breaststroke",
     "needs_source": True},
    {"series": "W200BR", "year": 1956, "type": "rules",
     "text": "Same rule change as the men's 200 m breaststroke: butterfly became its own event in 1956 and was "
             "banned from breaststroke.",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1948_Summer_Olympics_%E2%80%93_Women%27s_200_metre_breaststroke",
     "needs_source": True},
    {"series": "ALL", "year": 1912, "type": "open-water",
     "text": "Swum on a 100 m course built in Stockholm harbour (open water), not in a pool.",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1912_Summer_Olympics"},
    {"series": "ALL", "year": 2020, "type": "held-later",
     "text": "The Tokyo 2020 Games were held in 2021.",
     "source": "https://www.olympedia.org/editions"},
]

# Marco's decisions, 2026-10-18: the chart marks only 1980 and 1984 for political absences
# (the rule-based list in `absence_flags` stays in the data for the text); Tokyo 2020 is
# plotted at the year it was held (2021), labelled "Tokyo 2020, held 2021".
CHART_MARKER_YEARS = {1980, 1984}

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail and not ok else ""))


def read_blocks(path, label):
    """Read a text file made of '#C<n> crc:<hex>' blocks and verify each block's CRC32."""
    blocks, cur = [], None
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = re.fullmatch(r"#C(\d+) crc:([0-9a-f]{8})", line)
        if m:
            cur = {"n": int(m[1]), "crc": m[2], "lines": []}
            blocks.append(cur)
        elif line and not line.startswith("#"):
            cur["lines"].append(line)
    bad = [b["n"] for b in blocks
           if format(zlib.crc32("\n".join(b["lines"]).encode("utf-8")), "08x") != b["crc"]]
    check(f"{label} checksums ({len(blocks)} blocks)", not bad, f"bad blocks {bad}")
    return [ln for b in blocks for ln in b["lines"]]


def to_seconds(text):
    m = re.fullmatch(r"(?:(\d+):)?(\d+)\.(\d+)", text)
    if not m:
        raise ValueError(f"bad time {text!r}")
    sec = int(m[1] or 0) * 60 + int(m[2]) + int(m[3]) / 10 ** len(m[3])
    return round(sec, 2), len(m[3])


def parse_line(line):
    ev, yr, rid, date, rows = line.split("~", 4)
    finalists = []
    for row in rows.split("|"):
        pos, name, noc, t, medal, note = row.split("~")
        sec, dec = to_seconds(t) if t else (None, None)
        finalists.append({"pos": pos, "name": name or None, "noc": noc or None, "time_text": t or None,
                          "time_s": sec, "decimals": dec, "medal": medal or None, "note": note or None})
    return ev, int(yr), int(rid), date, finalists


def build_edition(ev, games_year, rid, date, finalists):
    champs = [f for f in finalists if f["medal"] == "Gold"]
    podium = [f for f in finalists if int(f["pos"].lstrip("=")) <= 3]
    rest = [{"pos": f["pos"], "time_s": f["time_s"], "time_text": f["time_text"]}
            for f in finalists if int(f["pos"].lstrip("=")) > 3]
    timed = [f["time_s"] for f in finalists if f["time_s"] is not None]
    complete = len(finalists) == 8 and len(timed) == 8
    return {
        "games_year": games_year, "held_year": int(date[-4:]), "plot_year": int(date[-4:]), "date": date,
        "result_id": rid, "url": RESULT_URL.format(rid),
        "champions": [{k: c[k] for k in ("name", "noc", "time_s", "time_text", "decimals", "note")} for c in champs],
        "podium": [{k: p[k] for k in ("pos", "name", "noc", "time_s", "time_text", "medal")} for p in podium],
        "others": rest,
        "n_finalists": len(finalists), "n_timed": len(timed),
        "band": {"fastest": min(timed), "slowest": max(timed)} if complete else None,
    }


def main():
    lines = read_blocks(RAW, "raw extract")
    data = {k: {} for k in EVENTS}
    for line in lines:
        ev, yr, rid, date, fin = parse_line(line)
        if ev not in data or yr in data[ev]:
            check(f"unknown or duplicate edition {ev} {yr}", False)
            continue
        data[ev][yr] = build_edition(ev, yr, rid, date, fin)
    check(f"{len(lines)} finals read; one per expected edition ({sum(len(v) for v in EXPECTED_YEARS.values())})",
          len(lines) == sum(len(v) for v in EXPECTED_YEARS.values()))

    for ev in EVENT_ORDER:
        years = sorted(data[ev])
        check(f"{ev}: editions match expected list ({len(EXPECTED_YEARS[ev])})", years == EXPECTED_YEARS[ev],
              f"extra {sorted(set(years) - set(EXPECTED_YEARS[ev]))}, missing {sorted(set(EXPECTED_YEARS[ev]) - set(years))}")
    check("held year equals Games year, except Tokyo 2020 held 2021",
          all(e["held_year"] == (2021 if y == 2020 else y) for ev in EVENTS for y, e in data[ev].items()))
    # A tie for a place leaves a medal unawarded (two golds: no silver), so count podium rows, not medal names.
    check("every edition has a champion and at least three podium rows",
          all(e["champions"] and len(e["podium"]) >= 3 for ev in EVENTS for e in data[ev].values()))
    check("at most 8 finalists with a time per edition", all(e["n_finalists"] <= 8 for ev in EVENTS for e in data[ev].values()))

    ties = {(ev, y) for ev in EVENTS for y, e in data[ev].items() if len(e["champions"]) > 1}
    check("co-champions only where expected", ties == EXPECTED_TIES, str(sorted(ties)))
    check("co-champions have identical times",
          all(len({c["time_s"] for c in data[ev][y]["champions"]}) == 1 for ev, y in ties))

    # Second source: one Wikipedia champion time per edition.
    second = {}
    for line in read_blocks(SECOND, "second-source file"):
        ev, yr, t = line.split("~")
        second[(ev, int(yr))] = t.split("/")
    check("second source covers every edition exactly", set(second) == {(ev, y) for ev in EVENTS for y in data[ev]})
    diffs = {}
    for (ev, y), times in second.items():
        if y not in data.get(ev, {}):
            continue  # reported by the coverage check above
        mine = {c["time_text"] for c in data[ev][y]["champions"]}
        if not set(times) <= mine:
            diffs[(ev, y)] = (sorted(mine), times)
    check(f"champion times equal second source in all editions except the {len(SECOND_SOURCE_DIFFS)} explained ones",
          set(diffs) == set(SECOND_SOURCE_DIFFS), str(diffs))
    for (ev, y), (mine, theirs) in sorted(diffs.items()):
        print(f"       explained: {ev} {y}: Olympedia {mine}, Wikipedia {theirs}. {SECOND_SOURCE_DIFFS.get((ev, y), 'UNEXPLAINED')}")
    for (ev, y), t in REFERENCE.items():
        check(f"reference value {ev} {y} = {t}", data[ev][y]["champions"][0]["time_text"] == t)

    anomalies = set()
    for ev in EVENTS:
        for y, e in data[ev].items():
            seq = [p["time_s"] for p in e["podium"] if p["time_s"] is not None]
            seq += [o["time_s"] for o in e["others"] if o["time_s"] is not None]
            if any(b < a for a, b in zip(seq, seq[1:])):
                anomalies.add((ev, y))
    check("times non-decreasing by position (except documented anomalies)",
          anomalies == KNOWN_ORDER_ANOMALIES, f"found {sorted(anomalies)}")

    medal_nocs = {p["noc"] for ev in EVENTS for e in data[ev].values() for p in e["podium"]}
    check("every medal-winning NOC has a name mapping", medal_nocs <= set(NOC_NAME), str(sorted(medal_nocs - set(NOC_NAME))))

    # Absence flags: an edition is flagged for an event when a nation that medalled in the
    # same event at the previous or next Games was absent for political reasons.
    flags = []
    for year, info in sorted(ABSENT.items()):
        per = {}
        for ev in EVENT_ORDER:
            years = sorted(data[ev])
            if year not in years:
                continue
            i = years.index(year)
            neigh = [years[j] for j in (i - 1, i + 1) if 0 <= j < len(years)]
            hit = sorted({p["noc"] for ny in neigh for p in data[ev][ny]["podium"]
                          if NOC_NAME.get(p["noc"]) in info["countries"]})
            per[ev] = {"neighbour_editions": neigh, "absent_medal_nations": hit}
        flags.append({"year": year, "chart_marker": year in CHART_MARKER_YEARS,
                      "reason": info["reason"], "source": info["source"],
                      "countries_absent": info["countries"], "series": per})

    check("chart markers only on 1980 and 1984",
          {f["year"] for f in flags if f["chart_marker"]} == CHART_MARKER_YEARS)
    check("Tokyo 2020 is plotted at 2021", all(data[ev][2020]["plot_year"] == 2021 for ev in EVENTS))

    if not all(CHECKS):
        sys.exit("Checks failed; data not written.")

    events_out = []
    for ev in EVENT_ORDER:
        meta = EVENTS[ev]
        events_out.append({"id": ev, "distance_m": meta["distance_m"], "sex": meta["sex"],
                           "stroke": meta["stroke"], "event_index": meta["index"],
                           "editions": [data[ev][y] for y in sorted(data[ev])]})

    out = {
        "units": "seconds", "accessed": ACCESSED,
        "notes": {
            "source": "Olympedia final results; champion times cross-checked with Wikipedia event pages.",
            "resolution": "Tenths of a second up to 1968, hundredths from 1972 (see `decimals`).",
            "finalists": "Only finalists with a printed time are kept (DNS, DQ and untimed rows are dropped), "
                         "so `n_finalists` counts finalists with a time.",
            "band": "`band` is set only when all 8 finalists have a time; otherwise null.",
            "plot": "Use `plot_year` for the x position (Tokyo 2020 is 2021). `chart_marker` in `absence_flags` says which absences the chart shows.",
            "scope": "28 individual pool events of the Paris 2024 programme, Olympic Games 1908-2024. "
                     "Relays, 10 km marathon swimming, yard races and discontinued events are out.",
            "single_source": "Silver, bronze and positions 4-8 come from Olympedia only.",
        },
        "noc_names": NOC_NAME,
        "not_held": [dict(n, source="https://www.olympedia.org/editions") for n in NOT_HELD],
        "absence_flags": flags,
        "annotations": ANNOTATIONS,
        "events": events_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")

    print("\nBand coverage (first edition with all 8 finalists timed; editions with a band):")
    for ev in EVENT_ORDER:
        ys = sorted(data[ev])
        comp = [y for y in ys if data[ev][y]["band"]]
        gaps = [y for y in ys if comp and y >= comp[0] and not data[ev][y]["band"]]
        print(f"  {ev:7s} from {comp[0] if comp else '-'}; {len(comp)}/{len(ys)} editions; gaps after: {gaps}")
    print("\nAbsence flags (absent nations that medalled at the neighbouring Games):")
    for f in flags:
        hits = {ev: s["absent_medal_nations"] for ev, s in f["series"].items() if s["absent_medal_nations"]}
        print(f"  {f['year']}: {len(hits)} events flagged" if hits else f"  {f['year']}: none")
    print("\nFirst-to-last look (champion time, seconds; not a thesis):")
    for ev in EVENT_ORDER:
        ys = sorted(data[ev])
        a, b = data[ev][ys[0]]["champions"][0]["time_s"], data[ev][ys[-1]]["champions"][0]["time_s"]
        print(f"  {ev:7s} {ys[0]}: {a:8.2f} -> {ys[-1]}: {b:8.2f}  change {100*(b-a)/a:+.1f} %")


if __name__ == "__main__":
    main()
