"""Build the data for the nuclear-reactors-world project.

Sources (all in analysis/nuclear-reactors-world/raw/, never edited):
  wna_reactor_table_2026-11-11.tsv        WNA "World Nuclear Power Reactors & Uranium Requirements",
                                          page dated 2026-11-11. Sets the country counts.
  wna_profiles_2026-11-11_part*.txt       WNA country profiles, reactor tables only, read 2026-11-11 in
                                          Chrome. Cell text joined with " | ", runs of spaces collapsed,
                                          lines trimmed. One CRC32 per country block in
                                          wna_profiles_2026-11-11_crc32.txt.
  Global-Nuclear-Power-Tracker-August-2026.xlsx
                                          Global Energy Monitor, August 2026 release, CC BY 4.0.
                                          Gives site coordinates, and the unit lists WNA does not publish
                                          (operating units of France and the USA, Pakistan's unit under
                                          construction).

Rule (Marco, 2026-11-11): WNA sets which units exist and their status. GEM fills what WNA lacks.
Every unit is assigned to a site; the map draws sites. Units are counted, not MW.

Run from the repo root:  python3 analysis/nuclear-reactors-world/build_data.py
Writes src/data/nuclear-reactors-world/{sites.json,countries.json}. Any failed check stops the script.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
import zlib
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "analysis/nuclear-reactors-world/raw"
OUT = ROOT / "src/data/nuclear-reactors-world"

WNA_TABLE = RAW / "wna_reactor_table_2026-11-11.tsv"
WNA_CRC = RAW / "wna_profiles_2026-11-11_crc32.txt"
GEM_XLSX = RAW / "Global-Nuclear-Power-Tracker-August-2026.xlsx"

STATES = ("operating", "construction", "planned")
FAILS: list[str] = []


def check(ok: bool, msg: str) -> None:
    print(("  ok    " if ok else "  FAIL  ") + msg)
    if not ok:
        FAILS.append(msg)


# --------------------------------------------------------------------------------------------
# 1. WNA country table
# --------------------------------------------------------------------------------------------
# WNA country label -> GEM "Country/Area" label
COUNTRY = {
    "Korea RO (South)": "South Korea", "USA": "United States", "UAE": "United Arab Emirates",
    "Turkey": "Türkiye",
}
# WNA table label -> name shown on the page
LABEL = {"Korea RO (South)": "South Korea", "USA": "United States", "UAE": "United Arab Emirates"}
# WNA profile slug -> WNA table label
SLUG_COUNTRY = {
    "argentina": "Argentina", "armenia": "Armenia", "bangladesh": "Bangladesh", "belarus": "Belarus",
    "belgium": "Belgium", "brazil": "Brazil", "bulgaria": "Bulgaria", "canada-nuclear-power": "Canada",
    "china-nuclear-power": "China", "czech-republic": "Czech Republic", "egypt": "Egypt",
    "finland": "Finland", "france": "France", "hungary": "Hungary", "india": "India", "iran": "Iran",
    "japan-nuclear-power": "Japan", "kazakhstan": "Kazakhstan", "south-korea": "Korea RO (South)",
    "mexico": "Mexico", "netherlands": "Netherlands", "pakistan": "Pakistan", "poland": "Poland",
    "romania": "Romania", "russia-nuclear-power": "Russia", "slovakia": "Slovakia",
    "slovenia": "Slovenia", "south-africa": "South Africa", "spain": "Spain", "sweden": "Sweden",
    "switzerland": "Switzerland", "turkey": "Turkey", "ukraine": "Ukraine",
    "united-arab-emirates": "UAE", "united-kingdom": "United Kingdom", "usa-nuclear-power": "USA",
    "uzbekistan": "Uzbekistan", "vietnam": "Vietnam",
}


def num(s: str) -> int:
    return int(s.replace(",", ""))


def read_wna_table() -> tuple[dict, dict]:
    rows = [l.rstrip("\n").split("\t") for l in WNA_TABLE.open(encoding="utf-8") if not l.startswith("#")]
    rows = rows[2:]  # two header rows
    countries, world = {}, None
    for r in rows:
        if not r[0]:
            continue
        name = r[0].replace("†", "").strip()
        rec = {"operating": num(r[3]), "operating_mwe_net": num(r[4]),
               "construction": num(r[5]), "construction_mwe_gross": num(r[6]),
               "planned": num(r[7]), "planned_mwe_gross": num(r[8]),
               "proposed": num(r[9]), "suspended_construction_note": "†" in r[0]}
        if name.startswith("WORLD"):
            world = rec
        else:
            countries[name] = rec
    return countries, world


# --------------------------------------------------------------------------------------------
# 2. WNA country profiles
# --------------------------------------------------------------------------------------------
def read_profiles() -> dict[str, list[dict]]:
    expected = dict(x.split(":") for x in WNA_CRC.read_text().split())
    blocks = {}
    for f in sorted(RAW.glob("wna_profiles_2026-11-11_part*.txt")):
        text = f.read_text(encoding="utf-8")
        for b in re.split(r"(?=^### )", text, flags=re.M):
            if not b.strip():
                continue
            slug = b.split("\n", 1)[0][4:].split("/")[1]
            crc = "%08x" % zlib.crc32(b.encode("utf-8"))
            if crc != expected.get(slug):
                FAILS.append(f"CRC32 {slug}: {crc} != {expected.get(slug)}")
            tables = []
            for t in re.split(r"^## ?", b, flags=re.M)[1:]:
                lines = t.split("\n")
                heading, header, data = lines[0], lines[1], [l for l in lines[2:] if l.strip()]
                cells = lambda l: re.split(r" ?\| ?", l)
                tables.append({"heading": heading, "header": cells(header),
                               "rows": [cells(l) for l in data]})
            blocks[slug] = tables
    return blocks


# Which profile table holds which state, and which column has the unit or site name.
# Table index = position after the "# Updated" line (0-based, as listed in the brief work log).
OPERATING_TABLE = {s: (0, 0) for s in SLUG_COUNTRY}
OPERATING_TABLE.update({"pakistan": (0, 1)})
for s in ("bangladesh", "egypt", "kazakhstan", "poland", "turkey", "usa-nuclear-power",
          "uzbekistan", "vietnam", "france"):
    OPERATING_TABLE.pop(s)  # no operating units, or no operating table (France: units from GEM)

CONSTRUCTION_TABLE = {  # slug: (table index, name column)
    "argentina": (1, 0), "bangladesh": (0, 0), "brazil": (1, 0), "canada-nuclear-power": (1, 0),
    "china-nuclear-power": (1, 0), "egypt": (0, 0), "hungary": (1, 0), "india": (1, 0),
    "iran": (1, 0), "japan-nuclear-power": (1, 0), "south-korea": (1, 0),
    "russia-nuclear-power": (1, 0), "turkey": (0, 0), "ukraine": (1, 0), "united-kingdom": (1, 0),
}
PLANNED_TABLE = {  # slug: (table index, name column, capacity column)
    "belarus": (1, 0, 2), "bulgaria": (1, 0, 3), "canada-nuclear-power": (2, 1, 2),
    "china-nuclear-power": (2, 0, 2), "czech-republic": (1, 0, 2), "hungary": (2, 0, 2),
    "india": (2, 0, 3), "iran": (2, 0, 2), "kazakhstan": (0, 0, 2), "poland": (0, 0, 2),
    "romania": (1, 0, 2), "russia-nuclear-power": (2, 0, 2), "sweden": (1, 0, 2),
    "ukraine": (2, 0, 2), "united-kingdom": (2, 1, 4), "uzbekistan": (0, 0, 2),
    "vietnam": (0, 1, 3),  # rows are single units named plant-unit ("Ninh Thuan 1-2"), see ONE_PER_ROW
}
ONE_PER_ROW = {"vietnam"}
# Rows in a planned table that are not planned units: totals, and rows after a "Total planned" line
# (those are proposed). Handled in planned_units().

# Documented reconciliation rules (each one printed and stated in the page notes)
PLANNED_ADJUST = {
    # China profile lists 41 planned; two of them already started construction and also appear in the
    # construction table (San'ao 4 on 2026-11-10, Xuwei HTR-PM 600-1 on 2026-11-06). WNA table: 39.
    ("China", "Cangnan/San'ao 4-6"): 2,
    ("China", "Xuwei HTR 1"): 0,
}
# France: the WNA table counts 2 planned units, the profile does not say which. Counted, not drawn
# (Marco, 2026-11-11: no site is assumed).
FRANCE_PLANNED = [{"name": "2 planned units, site not named", "site": "site not named", "units": 2}]
# Japan: the profile lists Higashidori 1 (Tepco) as planned and deferred; the WNA table has 0 planned
# for Japan. The table wins, so Japan has no planned units here.


def unit_count(name: str, cap: str) -> int:
    m = re.search(r"(\d+)\s*x\s*(\d+)", cap)
    if m:  # "2x1250" (units x MWe) or, in the India profile, "700 x 2" (MWe x units)
        a, b = int(m.group(1)), int(m.group(2))
        return a if a <= 20 else b
    m = re.search(r"(\d+)\s*&\s*(\d+)\s*$", name)
    if m:
        return 2
    m = re.search(r"(\d+)\s*-\s*(\d+)\s*$", name)
    if m and int(m.group(2)) > int(m.group(1)):
        return int(m.group(2)) - int(m.group(1)) + 1
    return 1


def table_units(blocks, slug, spec, state):
    tix, col = spec[0], spec[1]
    t = blocks[slug][tix + 1]  # +1 skips the "# Updated" pseudo-table
    out = []
    for r in t["rows"]:
        name = r[col].strip() if len(r) > col else ""
        if not name or re.match(r"(?i)total", name):
            continue
        out.append({"country": SLUG_COUNTRY[slug], "name": name, "units": 1, "state": state,
                    "source": "WNA profile"})
    return out


def planned_units(blocks, slug, spec):
    tix, col, capcol = spec
    t = blocks[slug][tix + 1]
    out = []
    for r in t["rows"]:
        if re.search(r"(?i)total", " ".join(r)):
            break  # every planned table ends with a total row; rows after it are proposed
        name = r[col].strip() if len(r) > col else ""
        if not name:
            continue
        cap = r[capcol] if len(r) > capcol else ""
        n = 1 if slug in ONE_PER_ROW else unit_count(name, cap)
        key = (SLUG_COUNTRY[slug], name)
        if key in PLANNED_ADJUST:
            print(f"  note  planned adjust {key}: {n} -> {PLANNED_ADJUST[key]}")
            n = PLANNED_ADJUST[key]
        if n:
            out.append({"country": SLUG_COUNTRY[slug], "name": name, "units": n, "state": "planned",
                        "source": "WNA profile"})
    return out


# --------------------------------------------------------------------------------------------
# 3. GEM
# --------------------------------------------------------------------------------------------
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def read_gem() -> pd.DataFrame:
    g = pd.read_excel(GEM_XLSX, sheet_name="Data")
    g["project"] = g["Project Name"].str.replace(r"\s*nuclear power plant\s*$", "", regex=True)
    g["pkey"] = g["project"].map(norm)
    return g


# WNA site name (after unit numbers are stripped) -> GEM project name, where the names differ.
SITE_ALIAS: dict[tuple[str, str], str | None] = {
    ("Belarus", "Ostrovets"): "Astravets",
    ("China", "San'ao"): "Cangnan San'ao", ("China", "Cangnan/San'ao"): "Cangnan San'ao",
    ("China", "Shidaowan Guohe One"): "Shidao Bay", ("China", "Shidaowan"): "Shidao Bay",
    ("China", "Xudabao"): "Xudapu", ("China", "Xuwei"): "Jiangsu Xuwei",
    ("China", "Changjiang"): "Changjiang", ("China", "Huaneng Xiapu"): "Xiapu",
    ("China", "Bohai Shipyard"): "CGN Bohai ACPR50S",
    ("India", "PFBR"): "Kalpakkam",
    ("Iran", "Darkhovin"): "Darkhovain",
    ("Japan", "Higashi Dori"): "Higashidori (Tohoku)",
    ("Vietnam", "Ninh Thuan"): "Ninh Thuận 1",
    ("United Kingdom", "Sizewell"): "Sizewell",
    # Not in the GEM release, or no site named by WNA: counted in the tables, not drawn on the map.
    ("Russia", "Reftinskaya"): None,
    ("France", "site not named"): None,
}


def wna_site(name: str) -> str:
    s = re.sub(r"(?i)\s*nuclear power plant", "", name)
    s = re.sub(r"\s*\(.*?\)\s*", " ", s).strip()
    s = s.replace("’", "'").strip('"')
    pat = re.compile(r"[\s-]*(\d+\s*[&-]\s*\d+|\d+|SMR-?\s*\d*|[A-Z]\d+|HTR(-PM)?\s*\d*|FNPP)$")
    prev = None
    while prev != s:
        prev, s = s, pat.sub("", s).strip(" ,-")
    return s


def match_site(country_gem: str, site: str, gem: pd.DataFrame):
    """Return the GEM project name for a WNA site, or None."""
    if (country_gem, site) in SITE_ALIAS:
        return SITE_ALIAS[(country_gem, site)] or "NO_LOCATION"
    g = gem[gem["Country/Area"] == country_gem]
    projects = g.drop_duplicates("pkey")[["project", "pkey"]]
    k = norm(site)
    if not k:
        return None
    exact = projects[projects.pkey == k]
    if len(exact):
        return exact.project.iloc[0]
    pre = projects[projects.pkey.map(lambda p: k.startswith(p) and len(p) >= 4)]
    if len(pre):
        return pre.loc[pre.pkey.str.len().idxmax(), "project"]
    pre = projects[projects.pkey.map(lambda p: p.startswith(k) and len(k) >= 4)]
    if len(pre) == 1:
        return pre.project.iloc[0]
    return None


# --------------------------------------------------------------------------------------------
# 4. Assemble
# --------------------------------------------------------------------------------------------
def main() -> None:
    print("WNA country table")
    countries, world = read_wna_table()
    for st in STATES + ("proposed",):
        s = sum(c[st] for c in countries.values())
        check(s == world[st], f"{st}: countries sum {s} = WORLD row {world[st]}")
    check(world["operating"] == 443 and world["construction"] == 82 and world["planned"] == 119,
          "WORLD row 443 / 82 / 119 (as read on 2026-11-11)")
    check(countries["China"]["construction"] == 41, "China under construction = 41")

    print("WNA profiles")
    blocks = read_profiles()
    check(not [f for f in FAILS if f.startswith("CRC32")], f"CRC32 of {len(blocks)} country blocks")

    units: list[dict] = []
    for slug, spec in OPERATING_TABLE.items():
        units += table_units(blocks, slug, spec, "operating")
    for slug, spec in CONSTRUCTION_TABLE.items():
        units += table_units(blocks, slug, spec, "construction")
    for slug, spec in PLANNED_TABLE.items():
        units += planned_units(blocks, slug, spec)
    for p in FRANCE_PLANNED:
        units.append({"country": "France", "name": p["name"], "units": p["units"], "state": "planned",
                      "source": "WNA table count; no site named", "site_hint": p["site"]})

    print("GEM")
    gem = read_gem()
    check(len(gem) == 1825 and gem["GEM unit ID"].is_unique, "GEM: 1825 rows, unique unit ids")
    fill = [("France", "operating", "operating"), ("USA", "operating", "operating"),
            ("Pakistan", "construction", "construction")]
    for wna_c, state, gem_status in fill:
        g = gem[(gem["Country/Area"] == COUNTRY.get(wna_c, wna_c)) & (gem.Status == gem_status)]
        check(len(g) == countries[wna_c][state],
              f"GEM fills {wna_c} {state}: {len(g)} units = WNA table {countries[wna_c][state]}")
        for _, r in g.iterrows():
            units.append({"country": wna_c, "name": f"{r.project} {r['Unit Name']}", "units": 1,
                          "state": state, "source": "GEM", "site_hint": r.project})

    print("Counts per country and state, WNA profiles + GEM fills vs WNA table")
    got = defaultdict(int)
    for u in units:
        got[(u["country"], u["state"])] += u["units"]
    for c, rec in sorted(countries.items()):
        for st in STATES:
            if got[(c, st)] != rec[st]:
                check(False, f"{c} {st}: units {got[(c, st)]} != table {rec[st]}")
    for st in STATES:
        tot = sum(v for (c, s), v in got.items() if s == st)
        check(tot == world[st], f"{st}: {tot} units = WORLD {world[st]}")

    print("Sites")
    unmatched = []
    for u in units:
        cg = COUNTRY.get(u["country"], u["country"])
        site = u.get("site_hint") or wna_site(u["name"])
        u["wna_site"] = site
        u["gem_project"] = match_site(cg, site, gem)
        if u["gem_project"] is None:
            unmatched.append((u["country"], u["name"], site))
    check(not unmatched, f"every unit has a GEM site ({len(unmatched)} unmatched)")
    for x in unmatched:
        print("        unmatched:", x)

    print("Site assignments where the WNA name differs from the GEM project name (review list)")
    seen = set()
    for u in units:
        k = (u["country"], u["wna_site"], u["gem_project"])
        if k not in seen and norm(u["wna_site"]) != norm(u["gem_project"] or ""):
            seen.add(k)
            print(f"        {u['country']}: {u['wna_site']!r} -> {u['gem_project']!r}")

    if FAILS:
        print(f"\n{len(FAILS)} check(s) failed. Stopping.")
        sys.exit(1)

    build_outputs(units, countries, world, gem)


GEM_STATE = {"operating": {"operating"}, "construction": {"construction"},
             "planned": {"pre-construction", "announced"}}


def build_outputs(units, countries, world, gem):
    sites: dict[tuple, dict] = {}
    no_location = defaultdict(int)
    for u in units:
        if u["gem_project"] == "NO_LOCATION":
            no_location[(u["country"], u["wna_site"], u["state"])] += u["units"]
            continue
        cg = COUNTRY.get(u["country"], u["country"])
        key = (cg, u["gem_project"])
        if key not in sites:
            g = gem[(gem["Country/Area"] == cg) & (gem.project == u["gem_project"])]
            lat, lon = g.Latitude.astype(float), g.Longitude.astype(float)
            spread_km = max(lat.max() - lat.min(), lon.max() - lon.min()) * 111
            exact = g["Location Accuracy"] == "exact"
            pos = g[exact] if exact.any() else g  # exact unit positions when the site has any
            sites[key] = {
                "site": u["gem_project"], "country": LABEL.get(u["country"], u["country"]),
                "lat": round(float(pos.Latitude.astype(float).median()), 4),
                "lon": round(float(pos.Longitude.astype(float).median()), 4),
                "location": "exact" if exact.any() else "approximate",
                "gem_unit_spread_km": round(float(spread_km), 1),
                "units": {st: 0 for st in STATES}, "names": {st: [] for st in STATES},
                "gem_units": {st: int(g.Status.isin(GEM_STATE[st]).sum()) for st in STATES},
            }
        s = sites[key]
        s["units"][u["state"]] += u["units"]
        s["names"][u["state"]].append(u["name"])

    print("Outputs")
    mapped = {st: sum(s["units"][st] for s in sites.values()) for st in STATES}
    unmapped = {st: sum(v for (c, n, s2), v in no_location.items() if s2 == st) for st in STATES}
    for st in STATES:
        check(mapped[st] + unmapped[st] == world[st],
              f"{st}: {mapped[st]} on the map + {unmapped[st]} without location = {world[st]}")
    far = [s for s in sites.values() if s["gem_unit_spread_km"] > 25]
    check(not far, f"GEM units of each site within 25 km of each other ({len(far)} sites beyond)")
    for s in far:
        print("        spread:", s["site"], s["country"], s["gem_unit_spread_km"], "km")

    # IAEA PRIS cross-check (world level only; the country panels are not readable as text)
    pris = (RAW / "pris_home_2026-11-11.txt").read_text()
    p_uc = int(re.search(r"(\d+) reactors\s+\d+ countries\s+In Operation", pris).group(1))
    p_op = int(re.search(r"In Operation[\s\S]*?(\d+) reactors", pris).group(1))
    p_su = int(re.search(r"Suspended Operation[\s\S]*?(\d+) reactors", pris).group(1))
    print(f"  info  PRIS 2026-11-11: in operation {p_op} + suspended operation {p_su} = {p_op + p_su}"
          f" vs WNA operable {world['operating']}; under construction {p_uc} vs WNA {world['construction']}")
    check(abs(p_op + p_su - world["operating"]) <= 10 and abs(p_uc - world["construction"]) <= 10,
          "WNA within 10 units of PRIS for operating (+suspended) and under construction")

    china_share = countries["China"]["construction"] / world["construction"]
    print(f"  value China share of units under construction: {countries['China']['construction']}"
          f" / {world['construction']} = {china_share:.3%}")
    diff = sum(abs(s["units"][st] - s["gem_units"][st]) for s in sites.values() for st in STATES)
    print(f"  info  WNA vs GEM unit count differences summed over sites and states: {diff}")

    OUT.mkdir(parents=True, exist_ok=True)
    site_list = sorted(sites.values(), key=lambda s: (s["country"], s["site"]))
    meta = {
        "units": "reactor units (count); no capacity is used",
        "states": {"operating": "WNA 'operable': connected to the grid",
                   "construction": "WNA 'under construction': first concrete poured "
                                   "(includes units where construction is suspended)",
                   "planned": "WNA 'planned': approvals, funding or commitment in place, "
                              "mostly expected to operate within 15 years"},
        "sources": {
            "counts": "World Nuclear Association, World Nuclear Power Reactors & Uranium Requirements, "
                      "page dated 2026-11-11, accessed 2026-11-11",
            "units": "World Nuclear Association country profiles, accessed 2026-11-11; France and USA "
                     "operating units and Pakistan's unit under construction from GEM",
            "locations": "Global Energy Monitor, Global Nuclear Power Tracker, August 2026 release, CC BY 4.0",
        },
        "assumptions": [
            "China planned: San'ao 4 and Xuwei HTR-PM 600-1 appear in both the construction and the "
            "planned tables of the WNA China profile; counted as under construction only (WNA table: 39 planned).",
            "France planned: the WNA table counts 2 planned units without naming them; counted, not drawn.",
            "Japan planned: the WNA Japan profile lists Higashidori 1 (Tepco) as planned and deferred; "
            "the WNA table has 0 planned for Japan, and the table is used.",
            "Site coordinates are the median of the GEM unit coordinates of the matched project, using only "
            "units with an exact location when the project has any.",
        ],
        "no_location": [{"country": c, "site": n, "state": s2, "units": v}
                        for (c, n, s2), v in sorted(no_location.items())],
        "world": {st: world[st] for st in STATES},
    }
    (OUT / "sites.json").write_text(json.dumps({"meta": meta, "sites": site_list}, ensure_ascii=False,
                                               separators=(",", ":")))
    clist = [{"country": LABEL.get(c, c), **{st: r[st] for st in STATES}, "proposed": r["proposed"]}
             for c, r in countries.items()]
    clist.sort(key=lambda r: (-r["construction"], -r["operating"]))
    (OUT / "countries.json").write_text(json.dumps({"meta": {"source": meta["sources"]["counts"],
                                                             "units": "reactor units"},
                                                    "world": world, "countries": clist},
                                                   ensure_ascii=False, separators=(",", ":")))
    print(f"  wrote {len(site_list)} sites and {len(clist)} countries to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
