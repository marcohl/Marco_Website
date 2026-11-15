"""One-time extraction of the inputs that cannot be read directly by build_data.py.

Run from the repository root:

    python3 analysis/bolivia-power-plants/extract_sources.py --gem "<path to Global Integrated Power September 2026 V2.xlsx>"

What it does (outputs are committed; the inputs are not, see the brief):
1. GEM Global Integrated Power Tracker (September 2026, 34 MB, delivered by e-mail
   after a form, so it cannot be fetched by a script): keeps the Bolivia rows only
   -> raw/gem_gipt_2026-09_bolivia.csv
2. Natural Earth 10m admin-1 polygons (GitHub mirror): keeps Bolivia only
   -> raw/ne_10m_admin_1_bolivia.geojson
3. CNDC Memoria y Resultados 2025 (raw/memyres_2025.pdf): reads the table
   "Producción bruta (GWh) periodo 1996-2025" (pp. 103-106) with `pdftotext -layout`
   (poppler) and writes the subtotal rows by source and the total row
   -> memoria_production_by_source_1996_2025.csv

Each output's SHA-256 is printed so the brief can record it.
"""

import argparse
import csv
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
NE_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_10m_admin_1_states_provinces.geojson"
)
YEARS = list(range(1996, 2026))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract_gem(xlsx_path):
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb["Power facilities"]
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    country = header.index("Country/area")
    keep = [r for r in rows if r[country] == "Bolivia"]
    out = RAW / "gem_gipt_2026-09_bolivia.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(keep)
    print(f"GEM: source sha256 {sha256(xlsx_path)}")
    print(f"GEM: {len(keep)} Bolivia rows -> {out.name} sha256 {sha256(out)}")


def extract_natural_earth():
    with urllib.request.urlopen(NE_URL, timeout=120) as r:
        data = json.load(r)
    feats = [f for f in data["features"] if f["properties"].get("adm0_a3") == "BOL"]
    keep_props = ("name", "iso_3166_2", "adm0_a3")
    for f in feats:
        f["properties"] = {k: f["properties"].get(k) for k in keep_props}
    out = RAW / "ne_10m_admin_1_bolivia.geojson"
    out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    print(f"Natural Earth: {len(feats)} departments -> {out.name} sha256 {sha256(out)}")


def parse_number(tok):
    tok = tok.strip()
    neg = tok.startswith("(") and tok.endswith(")")
    tok = tok.strip("()").replace(".", "").replace(",", ".")
    v = float(tok)
    return -v if neg else v


def numbers_in(line):
    return re.findall(r"\(?\d{1,3}(?:\.\d{3})*,\d\)?", line)


def extract_memoria():
    pdf = RAW / "memyres_2025.pdf"
    text = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True
    ).stdout
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if "PRODUCCIÓN BRUTA (GWh) PERIODO 1996 - 2025" in l)
    end = next(i for i in range(start, len(lines)) if "Generación Total" in lines[i])
    block = lines[start : end + 1]

    sections = {
        "Hidroeléctricas": "hydro",
        "Eólicas": "wind",
        "Solar": "solar",
        "Biomasa": "biomass",
        "Termoeléctricas": "thermal",
    }
    current = None
    rows = {}
    for line in block:
        s = line.strip()
        if s in sections:
            current = sections[s]
            continue
        if s.startswith("Subtotal") and current and current not in rows:
            vals = [parse_number(t) for t in numbers_in(line)]
            # series are right-aligned: the last value is 2025
            rows[current] = dict(zip(YEARS[-len(vals):], vals))
        if "Generación Total" in s:
            vals = [parse_number(t) for t in numbers_in(line)]
            rows["total"] = dict(zip(YEARS[-len(vals):], vals))
    missing = set(sections.values()) | {"total"}
    missing -= set(rows)
    if missing:
        raise SystemExit(f"Memoria: rows not found: {missing}")

    out = HERE / "memoria_production_by_source_1996_2025.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "hydro_gwh", "wind_gwh", "solar_gwh", "biomass_gwh", "thermal_gwh", "total_gwh"])
        for y in YEARS:
            w.writerow([y] + [rows[k].get(y, 0.0) for k in ("hydro", "wind", "solar", "biomass", "thermal", "total")])
    print(f"Memoria: production by source 1996-2025 -> {out.name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gem", help="path to the GEM GIPT xlsx (only needed to refresh the GEM extract)")
    args = ap.parse_args()
    if args.gem:
        extract_gem(args.gem)
    extract_natural_earth()
    extract_memoria()
