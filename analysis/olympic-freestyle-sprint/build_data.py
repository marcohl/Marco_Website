"""Build the data for the olympic-freestyle-sprint project (MHL-002).

Reads the Olympedia final-results extract in raw/, verifies its integrity,
checks it against a second source and known reference values, and writes
src/data/olympic-freestyle-sprint/series.json.

Units: all times are seconds (float). Olympedia gives tenths until 1968 and
hundredths from 1972; `decimals` keeps the printed resolution of each time.

Sources (accessed 2026-10-18):
  - Final results: Olympedia result pages, https://www.olympedia.org/results/<id>
  - Event index:   https://www.olympedia.org/event_names/{551,553,587,588}
  - Games not held / held 2021: https://www.olympedia.org/editions
  - Second source for champion times: Wikipedia event pages and the
    "100 metre freestyle" page (see SECOND_SOURCE).
  - Absences: Wikipedia "List of Olympic Games boycotts", "1920 Summer
    Olympics", "1948 Summer Olympics".
"""
import json
import re
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "raw" / "olympedia_finals_extract.txt"
OUT = ROOT / "src" / "data" / "olympic-freestyle-sprint" / "series.json"
RESULT_URL = "https://www.olympedia.org/results/{}"
ACCESSED = "2026-10-18"

SERIES = {
    "M100": {"distance_m": 100, "sex": "men", "index": "https://www.olympedia.org/event_names/553"},
    "W100": {"distance_m": 100, "sex": "women", "index": "https://www.olympedia.org/event_names/588"},
    "M50": {"distance_m": 50, "sex": "men", "index": "https://www.olympedia.org/event_names/551"},
    "W50": {"distance_m": 50, "sex": "women", "index": "https://www.olympedia.org/event_names/587"},
}

# Games not held. Source: https://www.olympedia.org/editions ("Not held due to war").
NOT_HELD = [
    {"year": 1916, "host": "Berlin", "reason": "war"},
    {"year": 1940, "host": "Helsinki", "reason": "war"},
    {"year": 1944, "host": "London", "reason": "war"},
]

# Champion times from a second source. Wikipedia "100 metre freestyle" page for
# M100/W100 (except W100 1992, see note); Wikipedia per-Games event pages for
# M50/W50. 2024 50 m: Wikipedia event pages plus SuperSport and Swimming World.
# W100 1992: the aggregate Wikipedia page says 54.65; the 1992 event page (which
# cites the official report) and Olympedia say 54.64. 54.64 is used.
SECOND_SOURCE = {
    "M100": {1908: "1:05.6", 1912: "1:03.4", 1920: "1:01.4", 1924: "59.0", 1928: "58.6",
             1932: "58.2", 1936: "57.6", 1948: "57.3", 1952: "57.4", 1956: "55.4",
             1960: "55.2", 1964: "53.4", 1968: "52.2", 1972: "51.22", 1976: "49.99",
             1980: "50.40", 1984: "49.80", 1988: "48.63", 1992: "49.02", 1996: "48.74",
             2000: "48.30", 2004: "48.17", 2008: "47.21", 2012: "47.52", 2016: "47.58",
             2020: "47.02", 2024: "46.40"},
    "W100": {1912: "1:22.2", 1920: "1:13.6", 1924: "1:12.4", 1928: "1:11.0", 1932: "1:06.8",
             1936: "1:05.9", 1948: "1:06.3", 1952: "1:06.8", 1956: "1:02.0", 1960: "1:01.2",
             1964: "59.5", 1968: "1:00.0", 1972: "58.59", 1976: "55.65", 1980: "54.79",
             1984: "55.92", 1988: "54.93", 1992: "54.64", 1996: "54.50", 2000: "53.83",
             2004: "53.84", 2008: "53.12", 2012: "53.00", 2016: "52.70", 2020: "51.96",
             2024: "52.16"},
    "M50": {1988: "22.14", 1992: "21.91", 1996: "22.13", 2000: "21.98", 2004: "21.93",
            2008: "21.30", 2012: "21.34", 2016: "21.40", 2020: "21.07", 2024: "21.25"},
    "W50": {1988: "25.49", 1992: "24.79", 1996: "24.87", 2000: "24.32", 2004: "24.58",
            2008: "24.06", 2012: "24.05", 2016: "24.07", 2020: "23.81", 2024: "23.71"},
}

# Known reference values read independently of the DOM extract.
REFERENCE = {
    ("M100", 1908): "1:05.6", ("M100", 1988): "48.63", ("M100", 2024): "46.40",
    ("W100", 1988): "54.93", ("M50", 1988): "22.14", ("W50", 1988): "25.49",
}

EXPECTED_YEARS = {
    "M100": [1908, 1912] + list(range(1920, 1937, 4)) + list(range(1948, 2025, 4)),
    "W100": [1912] + list(range(1920, 1937, 4)) + list(range(1948, 2025, 4)),
    "M50": list(range(1988, 2025, 4)),
    "W50": list(range(1988, 2025, 4)),
}
EXPECTED_TIES = {("W100", 1984), ("W100", 2016), ("M50", 2000)}
# Editions where Olympedia lists a lower-placed finalist with a faster time.
KNOWN_ORDER_ANOMALIES = {("M100", 1960)}

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
NOC_NAME = {
    "USA": "United States", "HUN": "Hungary", "SWE": "Sweden", "ANZ": "Australasia", "GBR": "Great Britain",
    "JPN": "Japan", "AUS": "Australia", "BRA": "Brazil", "GER": "Germany", "URS": "Soviet Union",
    "FRG": "West Germany", "GDR": "East Germany", "FRA": "France", "EUN": "Unified Team", "RUS": "Russia",
    "NED": "Netherlands", "RSA": "South Africa", "CAN": "Canada", "BEL": "Belgium", "CHN": "China",
    "ROU": "Romania", "ROC": "ROC", "DEN": "Denmark", "ARG": "Argentina", "CRO": "Croatia",
    "HKG": "Hong Kong", "BLR": "Belarus",
}

ANNOTATIONS = [
    {"series": "M100", "year": 1920, "type": "re-swim",
     "text": "The final was re-swum after Norman Ross was disqualified on a protest. The time shown is the "
             "re-swim (1:01.4). The first final, with a faster 1:00.4 for the winner, is not the official result.",
     "source": "https://www.olympedia.org/results/4649"},
    {"series": "M100", "year": 1960, "type": "order",
     "text": "Olympedia lists the silver medallist 0.1 s faster than the gold medallist. The reason is not in "
             "this data; source it before any text mentions it.",
     "source": "https://www.olympedia.org/results/5489", "needs_source": True},
    {"series": "M100", "year": 1908, "type": "course",
     "text": "First Games with a purpose-built 100 m pool. The race was a single length of the pool, "
             "with no turns. Earlier Olympic swimming was in open water.",
     "source": "https://en.wikipedia.org/wiki/Swimming_at_the_1908_Summer_Olympics_%E2%80%93_Men%27s_100_metre_freestyle"},
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


def read_extract(path):
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
    check(f"raw extract checksums ({len(blocks)} blocks)", not bad, f"bad blocks {bad}")
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
    lines = read_extract(RAW)
    data = {k: {} for k in SERIES}
    for line in lines:
        ev, yr, rid, date, fin = parse_line(line)
        data[ev][yr] = build_edition(ev, yr, rid, date, fin)

    for ev in SERIES:
        years = sorted(data[ev])
        check(f"{ev}: editions match expected list ({len(EXPECTED_YEARS[ev])})", years == EXPECTED_YEARS[ev])
        check(f"{ev}: held year equals Games year, except Tokyo 2020 held 2021",
              all(e["held_year"] == (2021 if y == 2020 else y) for y, e in data[ev].items()))
        check(f"{ev}: every edition has a champion", all(e["champions"] for e in data[ev].values()))

    ties = {(ev, y) for ev in SERIES for y, e in data[ev].items() if len(e["champions"]) > 1}
    check("co-champions only where expected (W100 1984, W100 2016, M50 2000)", ties == EXPECTED_TIES, str(sorted(ties)))
    check("co-champions have identical times",
          all(len({c["time_s"] for c in data[ev][y]["champions"]}) == 1 for ev, y in ties))

    bad2 = []
    for ev, ref in SECOND_SOURCE.items():
        check(f"{ev}: second-source list covers every edition", sorted(ref) == sorted(data[ev]))
        for y, t in ref.items():
            if any(c["time_text"] != t for c in data[ev][y]["champions"]):
                bad2.append((ev, y))
    check("champion times equal second source in all 73 editions", not bad2, str(bad2))
    for (ev, y), t in REFERENCE.items():
        check(f"reference value {ev} {y} = {t}", data[ev][y]["champions"][0]["time_text"] == t)

    anomalies = set()
    for ev in SERIES:
        for y, e in data[ev].items():
            seq = [p["time_s"] for p in e["podium"] if p["time_s"] is not None]
            seq += [o["time_s"] for o in e["others"] if o["time_s"] is not None]
            if any(b < a for a, b in zip(seq, seq[1:])):
                anomalies.add((ev, y))
    check("times non-decreasing by position (except documented anomalies)", anomalies == KNOWN_ORDER_ANOMALIES, str(sorted(anomalies)))

    medal_nocs = {p["noc"] for ev in SERIES for e in data[ev].values() for p in e["podium"]}
    check("every medal-winning NOC has a name mapping", medal_nocs <= set(NOC_NAME), str(sorted(medal_nocs - set(NOC_NAME))))

    # Absence flags: an edition is flagged for a series when a nation that medalled in the
    # same event at the previous or next Games was absent for political reasons.
    flags = []
    for year, info in sorted(ABSENT.items()):
        per = {}
        for ev in SERIES:
            years = sorted(data[ev])
            if year not in years:
                continue
            i = years.index(year)
            neigh = [years[j] for j in (i - 1, i + 1) if 0 <= j < len(years)]
            hit = sorted({p["noc"] for ny in neigh for p in data[ev][ny]["podium"]
                          if NOC_NAME[p["noc"]] in info["countries"]})
            per[ev] = {"neighbour_editions": neigh, "absent_medal_nations": hit}
        flags.append({"year": year, "chart_marker": year in CHART_MARKER_YEARS,
                      "reason": info["reason"], "source": info["source"],
                      "countries_absent": info["countries"], "series": per})

    check("chart markers only on 1980 and 1984",
          {f["year"] for f in flags if f["chart_marker"]} == CHART_MARKER_YEARS)
    check("Tokyo 2020 is plotted at 2021",
          all(data[ev][2020]["plot_year"] == 2021 for ev in SERIES))

    series_out = []
    for ev, meta in SERIES.items():
        series_out.append({"id": ev, "distance_m": meta["distance_m"], "sex": meta["sex"],
                           "event_index": meta["index"],
                           "editions": [data[ev][y] for y in sorted(data[ev])]})

    if not all(CHECKS):
        sys.exit("Checks failed; data not written.")

    out = {
        "units": "seconds", "accessed": ACCESSED,
        "notes": {
            "source": "Olympedia final results (positions 1-8); champion times cross-checked with Wikipedia.",
            "resolution": "Tenths of a second up to 1968, hundredths from 1972 (see `decimals`).",
            "band": "`band` is set only when all 8 finalists have a time; otherwise null.",
            "plot": "Use `plot_year` for the x position (Tokyo 2020 is 2021). `chart_marker` in `absence_flags` says which absences the chart shows.",
            "scope": "Olympic Games 1908-2024. 50 m freestyle on the programme from 1988; women's 100 m from 1912.",
            "single_source": "Silver, bronze and positions 4-8 come from Olympedia only.",
        },
        "noc_names": NOC_NAME,
        "not_held": [dict(n, source="https://www.olympedia.org/editions") for n in NOT_HELD],
        "absence_flags": flags,
        "annotations": ANNOTATIONS,
        "series": series_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")

    print("\nBand coverage (first edition with all 8 finalists timed, and later gaps):")
    for ev in SERIES:
        ys = sorted(data[ev])
        comp = [y for y in ys if data[ev][y]["band"]]
        missing_after = [y for y in ys if y >= comp[0] and not data[ev][y]["band"]]
        print(f"  {ev:5s} complete from {comp[0]}; complete in {len(comp)}/{len(ys)} editions; gaps after: {missing_after}")
    print("\nAbsence flags (absent nations that medalled at the neighbouring Games):")
    for f in flags:
        hits = {ev: s["absent_medal_nations"] for ev, s in f["series"].items() if s["absent_medal_nations"]}
        print(f"  {f['year']}: {hits if hits else 'none'}")
    print("\nFirst-to-last look (champion time, seconds; not a thesis):")
    for ev in SERIES:
        ys = sorted(data[ev])
        a, b = data[ev][ys[0]]["champions"][0]["time_s"], data[ev][ys[-1]]["champions"][0]["time_s"]
        print(f"  {ev:5s} {ys[0]}: {a:6.2f} -> {ys[-1]}: {b:6.2f}  change {100*(b-a)/a:+.1f} %")
    print("  Since 1988 for the 100 m, to compare with the 50 m on the same years:")
    for ev in ("M100", "W100"):
        a, b = data[ev][1988]["champions"][0]["time_s"], data[ev][2024]["champions"][0]["time_s"]
        print(f"  {ev:5s} 1988: {a:6.2f} -> 2024: {b:6.2f}  change {100*(b-a)/a:+.1f} %")


if __name__ == "__main__":
    main()
