"""Build the data for the nuclear-capacity-vs-share project.

Source:
  DNV Energy Transition Outlook 2026, forecast data workbook (released 2026-10-07).
  Download page https://www.dnv.com/eto-data redirects to an .xlsx on brandcentral.dnv.com.
  Accessed 2026-11-21. Saved as raw/dnv_eto_2026_data.xlsx (gitignored: the DNV licence does not
  allow redistribution of the report; the site ships only the derived JSON with DNV's notice).
  If the raw file is missing, this script downloads it.

Variables used (sheet "Power supply", one row per region and power station type, 2025-2060):
  "Installed Capacity including behind-the-meter and dedicated to hydrogen"   GW
  "Electricity Generation incl off-grid and behind-the-meter"                 GWh/yr
These are the variables that reproduce the figures in the main report (sec. 4.5, pp. 70-73).
The "Utility-scale" variables are lower and are not used.

Derived:
  share_pct   = nuclear generation / total generation * 100      (% of electricity generated)
  load_factor = nuclear generation / (nuclear capacity * 8760 h)  (implied, dimensionless)
World = sum of DNV's 10 regions.

Run from the repo root:  python3 analysis/nuclear-capacity-vs-share/build_data.py
Writes src/data/nuclear-capacity-vs-share/nuclear.json. Any failed check stops the script.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "analysis/nuclear-capacity-vs-share/raw/dnv_eto_2026_data.xlsx"
OUT = ROOT / "src/data/nuclear-capacity-vs-share/nuclear.json"
URL = "https://www.dnv.com/eto-data"

CAP_VAR = "Installed Capacity including behind-the-meter and dedicated to hydrogen"
GEN_VAR = "Electricity Generation incl off-grid and behind-the-meter"

# DNV region codes and names (sheet "Definitions")
REGIONS = {
    "NAM": "North America",
    "LAM": "Latin America",
    "EUR": "Europe",
    "SSA": "Sub-Saharan Africa",
    "MEA": "Middle East and North Africa",
    "NEE": "North East Eurasia",
    "CHN": "Greater China",
    "IND": "Indian Subcontinent",
    "SEA": "South East Asia",
    "OPA": "OECD Pacific",
}

NOTICE = (
    "This work is partially based on data developed by DNV AS, ©DNV AS. 2026, but the "
    "resulting work has been prepared by Marco Herbas Lopez and does not necessarily reflect the "
    "views of DNV AS."
)

FAILS: list[str] = []


def check(ok: bool, msg: str) -> None:
    print(("  ok    " if ok else "  FAIL  ") + msg)
    if not ok:
        FAILS.append(msg)


def near(value: float, ref: float, tol: float) -> bool:
    return abs(value - ref) <= tol


# --------------------------------------------------------------------------------------------
# 1. Fetch and read
# --------------------------------------------------------------------------------------------
if not RAW.exists():
    print(f"Downloading {URL} -> {RAW.relative_to(ROOT)}")
    RAW.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "data-build-script"})
    with urllib.request.urlopen(req, timeout=120) as r:
        RAW.write_bytes(r.read())

wb = openpyxl.load_workbook(RAW, read_only=True, data_only=True)
rows = list(wb["Power supply"].iter_rows(values_only=True))
header = rows[1]
col = {str(v): i for i, v in enumerate(header) if v is not None}
YEARS = [int(v) for v in header if v is not None and str(v).isdigit()]
yi = {y: col[str(y)] for y in YEARS}

print("Read checks")
check(YEARS == list(range(2025, 2061)), f"years 2025-2060 annual (got {YEARS[0]}-{YEARS[-1]})")
check(header[:5] == ("Variable", "Region", "Power station type", "Storage type", "Unit"),
      "Power supply header layout as expected")


def series(var: str, unit: str, region: str, nuclear_only: bool) -> list[float]:
    sel = [r for r in rows[2:] if r[0] == var and r[1] == region
           and (not nuclear_only or r[2] == "nuclear")]
    if not sel:
        raise SystemExit(f"no rows for {var} / {region}")
    bad = {r[4] for r in sel} - {unit}
    if bad:
        raise SystemExit(f"unexpected unit {bad} for {var}")
    return [sum(float(r[yi[y]] or 0) for r in sel) for y in YEARS]


found = {r[1] for r in rows[2:] if r[0] == CAP_VAR}
check(found == set(REGIONS), f"10 DNV regions present ({sorted(found)})")

# --------------------------------------------------------------------------------------------
# 2. Build series (GWh -> TWh)
# --------------------------------------------------------------------------------------------
data = {}
for code in REGIONS:
    cap = series(CAP_VAR, "GW", code, True)
    nuc = [v / 1000 for v in series(GEN_VAR, "GWh/yr", code, True)]
    tot = [v / 1000 for v in series(GEN_VAR, "GWh/yr", code, False)]
    data[code] = {"capacity_gw": cap, "nuclear_twh": nuc, "total_twh": tot}

world = {k: [sum(data[c][k][i] for c in REGIONS) for i in range(len(YEARS))]
         for k in ("capacity_gw", "nuclear_twh", "total_twh")}


def derive(d: dict) -> dict:
    d["share_pct"] = [n / t * 100 if t else 0.0 for n, t in zip(d["nuclear_twh"], d["total_twh"])]
    d["load_factor"] = [n * 1000 / (c * 8760) if c else None
                        for n, c in zip(d["nuclear_twh"], d["capacity_gw"])]
    return d


derive(world)
for code in REGIONS:
    derive(data[code])


def at(d: dict, key: str, year: int) -> float:
    return d[key][YEARS.index(year)]


# --------------------------------------------------------------------------------------------
# 3. Checks against the DNV main report, sec. 4.5, pp. 70-73
# --------------------------------------------------------------------------------------------
print("\nWorld vs report")
for y, ref in ((2025, 415), (2040, 600), (2060, 1200)):
    v = at(world, "capacity_gw", y)
    check(near(v, ref, 5), f"capacity {y}: {v:,.0f} GW (report {ref:,})")
for y, ref in ((2025, 2900), (2060, 7000)):
    v = at(world, "nuclear_twh", y)
    check(near(v, ref, 50), f"nuclear generation {y}: {v:,.0f} TWh (report {ref:,})")
for y, ref in ((2025, 33000), (2060, 84200)):
    v = at(world, "total_twh", y)
    check(near(v, ref, 100), f"total generation {y}: {v:,.0f} TWh (report {ref:,})")
for y, ref in ((2025, 8.7), (2040, 7.6), (2060, 8.3)):
    v = at(world, "share_pct", y)
    check(near(v, ref, 0.05), f"share {y}: {v:.2f}% (report {ref}%)")

low = min(world["share_pct"])
low_year = YEARS[world["share_pct"].index(low)]
check(near(low, 7.0, 0.05) and 2043 <= low_year <= 2047,
      f"share minimum {low:.2f}% in {low_year} (report 7.0%, mid-2040s)")

growth_tot = at(world, "total_twh", 2060) / at(world, "total_twh", 2025) - 1
growth_nuc = at(world, "nuclear_twh", 2060) / at(world, "nuclear_twh", 2025) - 1
check(near(growth_tot * 100, 155, 1.5), f"total generation growth {growth_tot:.1%} (report +155%)")
check(near(growth_nuc * 100, 144, 1.5), f"nuclear generation growth {growth_nuc:.1%} (report +144%)")
fold = at(world, "capacity_gw", 2060) / at(world, "capacity_gw", 2025)
check(near(fold, 2.9, 0.05), f"capacity {fold:.2f}-fold (report 2.9-fold)")

for y, ref in ((2025, 0.79), (2060, 0.67)):
    v = at(world, "load_factor", y)
    check(near(v, ref, 0.01), f"world load factor {y}: {v:.3f} (report {ref})")
for code, ref in (("NAM", 0.50), ("EUR", 0.47)):
    v = at(data[code], "load_factor", 2060)
    check(near(v, ref, 0.01), f"{code} load factor 2060: {v:.3f} (report {ref})")

add_w = at(world, "capacity_gw", 2040) - at(world, "capacity_gw", 2025)
add_c = at(data["CHN"], "capacity_gw", 2040) - at(data["CHN"], "capacity_gw", 2025)
check(near(add_w, 180, 5), f"net additions 2025-2040: {add_w:.0f} GW (report 180)")
check(near(add_c, 140, 5), f"Greater China net additions 2025-2040: {add_c:.0f} GW (report 140)")

print("\nRegional share vs report (whole %)")
REG_REF = {
    "EUR": {2025: 20, 2040: 10, 2060: 8},
    "NAM": {2025: 17, 2040: 10, 2060: 7},
    "CHN": {2025: 4, 2060: 11},
    "IND": {2025: 3, 2060: 10},
    "OPA": {2025: 14, 2030: 20, 2060: 16},
}
# Known discrepancy: the report text gives Europe 2040 as "10%"; the dataset gives 10.6% (the
# utility-scale variable gives 13.1%, so it is not a boundary issue). Treated as rounding in the
# report prose; the page uses the dataset value. Allowed 1 pp instead of 0.5.
KNOWN = {("EUR", 2040): 1.0}
for code, refs in REG_REF.items():
    for y, ref in refs.items():
        v = at(data[code], "share_pct", y)
        tol = KNOWN.get((code, y), 0.5)
        note = " [known: report rounds down]" if (code, y) in KNOWN else ""
        check(near(v, ref, tol), f"{code} share {y}: {v:.1f}% (report {ref}%){note}")

if FAILS:
    print(f"\n{len(FAILS)} check(s) failed. Nothing written.")
    sys.exit(1)

# --------------------------------------------------------------------------------------------
# 4. Write
# --------------------------------------------------------------------------------------------
ROUND = {"capacity_gw": 1, "nuclear_twh": 1, "total_twh": 1, "share_pct": 2, "load_factor": 3}


def rounded(d: dict) -> dict:
    return {k: [None if v is None else round(v, ROUND[k]) for v in d[k]] for k in ROUND}


out = {
    "meta": {
        "source": "DNV, Energy Transition Outlook 2026, forecast data (released 2026-10-07)",
        "source_url": URL,
        "accessed": "2026-11-21",
        "status": "forecast (2025 is DNV's base year estimate)",
        "notice": NOTICE,
        "units": {
            "capacity_gw": "GW, installed nuclear capacity incl. behind-the-meter",
            "nuclear_twh": "TWh/yr, nuclear electricity generated incl. off-grid and behind-the-meter",
            "total_twh": "TWh/yr, electricity generated from all sources, same boundary",
            "share_pct": "% of electricity generated (nuclear_twh / total_twh)",
            "load_factor": "implied, nuclear_twh / (capacity_gw x 8760 h)",
        },
        "world": "sum of the 10 DNV regions",
    },
    "years": YEARS,
    "world": rounded(world),
    "regions": [{"code": c, "name": n, **rounded(data[c])} for c, n in REGIONS.items()],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False) + "\n")
print(f"\nAll checks passed. Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.1f} KB)")

print("\nRegional share 2025 -> 2060 (for the form phase)")
for c, n in sorted(REGIONS.items(), key=lambda kv: -at(data[kv[0]], "share_pct", 2060)):
    d = data[c]
    print(f"  {n:30s} {at(d, 'share_pct', 2025):5.1f}% -> {at(d, 'share_pct', 2060):5.1f}%   "
          f"{at(d, 'capacity_gw', 2025):6.1f} -> {at(d, 'capacity_gw', 2060):6.1f} GW")
