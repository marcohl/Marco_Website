"""Build the data for "Where Bolivia makes its electricity" (bolivia-power-plants).

Run from the repository root:

    python3 analysis/bolivia-power-plants/build_data.py

Inputs (all in analysis/bolivia-power-plants/):
  cndc_capacity_2025.csv                    CNDC Memoria y Resultados 2025, p. 49, transcribed
  plant_locations.csv                       coordinates per plant, with source and precision
  memoria_production_by_source_1996_2025.csv  from extract_sources.py (Memoria 2025, pp. 103-106)
  raw/genbruta_<year>.(xls|xlsx|zip)        CNDC gross generation per unit, MWh
  raw/ne_10m_admin_1_bolivia.geojson        Natural Earth department borders

Outputs (src/data/bolivia-power-plants/):
  plants.json       one record per plant: capacity (MW), 2025 generation (GWh), location, department
  history.json      SIN gross generation by source, 1996-2025 (GWh)
  departments.json  simplified department polygons (GeoJSON, WGS84)

Every check below must pass; a failed check stops the script.
"""

import csv
import io
import json
import math
import re
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE.parents[1] / "src" / "data" / "bolivia-power-plants"
REF_YEAR = 2025
HOURS_2025 = 8760

FAILED = []


def check(name, ok, detail=""):
    print(f"[{'ok' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        FAILED.append(name)


def close(a, b, tol):
    return abs(a - b) <= tol


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s).lower()).strip("-")


# ---------------------------------------------------------------- capacity
cap = pd.read_csv(HERE / "cndc_capacity_2025.csv")

# CNDC Memoria 2025, p. 14 and the summary table on p. 5: capacity by type, MW
REF_CAP_BY_TYPE = {
    "gas_cc": 1651.34,
    "gas_oc": 722.91,
    "hydro": 715.81,
    "wind": 135.00,
    "solar": 167.58,
    "biomass": 125.00,
    "diesel_dual_fuel": 13.26,
}
cap["type_ref"] = cap["tech_cndc"].replace({"diesel": "diesel_dual_fuel", "dual_fuel": "diesel_dual_fuel"})
by_type = cap.groupby("type_ref")["capacity_mw"].sum()
for t, ref in REF_CAP_BY_TYPE.items():
    check(f"capacity {t} = {ref} MW", close(by_type.get(t, 0), ref, 0.011), f"{by_type.get(t, 0):.2f}")
check("capacity SIN total = 3530.90 MW", close(cap["capacity_mw"].sum(), 3530.90, 0.011), f"{cap['capacity_mw'].sum():.2f}")

units = cap.groupby(cap["tech_cndc"].isin(["hydro", "wind", "solar"]).map({True: "x", False: "thermal"}))["n_units"].sum()
units_by = cap.groupby("tech_cndc")["n_units"].sum()
check("units: hydro 54, wind 40, solar 62, thermal and biomass 82",
      units_by["hydro"] == 54 and units_by["wind"] == 40 and units_by["solar"] == 62 and units["thermal"] == 82,
      f"hydro {units_by['hydro']}, wind {units_by['wind']}, solar {units_by['solar']}, thermal {units['thermal']}")

# subtotals printed on p. 49
REF_SUBTOTALS = {
    "Guaracachi": 345.95, "Aranjuez": 35.19, "Valle Hermoso": 79.45, "Carrasco": 133.36,
    "El Alto": 49.95, "Bulo Bulo": 92.79, "Moxos": 5.70, "Entre Ríos": 526.77, "Del Sur": 505.83,
    "Warnes": 570.57, "Aguaí": 59.00,
}
plant_cap = cap.groupby("plant")["capacity_mw"].sum()
bad = {p: round(plant_cap[p], 2) for p, v in REF_SUBTOTALS.items() if not close(plant_cap[p], v, 0.011)}
check("plant subtotals match p. 49", not bad, str(bad) if bad else "")

# ---------------------------------------------------------------- generation 2025, per unit
UNIT_TO_PLANT = [
    (r"^COR", "Corani"), (r"^SJS1", "San José 1"), (r"^SJS2", "San José 2"), (r"^SIS", "Santa Isabel"),
    (r"^ZON", "Zongo"), (r"^TIQ", "Tiquimani"), (r"^BOT", "Botijlaca"), (r"^CUT", "Cuticucho"),
    (r"^SRO", "Santa Rosa"), (r"^SAI", "Sainani"), (r"^CHU", "Chururaqui"), (r"^HAR", "Harca"),
    (r"^CAH", "Cahua"), (r"^HUA", "Huaji"), (r"^MIG", "Miguilla"), (r"^ANG", "Angostura"),
    (r"^CHO", "Choquetanga"), (r"^CRB", "Carabuco"), (r"^CHJ", "Chojlla"), (r"^YAN", "Yanacachi"),
    (r"^KAN", "Kanata"), (r"^QUE", "Quehata"), (r"^SJA", "San Jacinto"), (r"^MIS", "Misicuni"),
    (r"^QOL", "Qollpana"), (r"^EWA", "Warnes (wind)"), (r"^ESJU", "San Julián"), (r"^EDO", "El Dorado"),
    (r"^UYU", "Uyuni"), (r"^YUN", "Yunchará"), (r"^ORU", "Oruro"),
    (r"^GCH", "Guaracachi"), (r"^SCZ", "Santa Cruz"), (r"^UNA", "Unagro"), (r"^SBU", "San Buenaventura"),
    (r"^ARJ", "Aranjuez"), (r"^VHE", "Valle Hermoso"), (r"^CAR", "Carrasco"), (r"^ALT", "El Alto"),
    (r"^BUL", "Bulo Bulo"), (r"^MOX", "Moxos"), (r"^ERI", "Entre Ríos"), (r"^SUR", "Del Sur"),
    (r"^WAR", "Warnes"), (r"^AGU", "Aguaí"), (r"^GBE", "Guabirá"), (r"^IAG", "IAGSA"),
]


def unit_type(code, plant):
    """CNDC type of a generating unit, for the check against the published breakdown."""
    hydro = {"Corani", "San José 1", "San José 2", "Santa Isabel", "Zongo", "Tiquimani", "Botijlaca",
             "Cuticucho", "Santa Rosa", "Sainani", "Chururaqui", "Harca", "Cahua", "Huaji", "Miguilla",
             "Angostura", "Choquetanga", "Carabuco", "Chojlla", "Yanacachi", "Kanata", "Quehata",
             "San Jacinto", "Misicuni"}
    if plant in hydro:
        return "hydro"
    if plant in {"Qollpana", "Warnes (wind)", "San Julián", "El Dorado"}:
        return "wind"
    if plant in {"Uyuni", "Yunchará", "Oruro"}:
        return "solar"
    if plant in {"Unagro", "San Buenaventura", "Aguaí", "Guabirá", "IAGSA"}:
        return "biomass"
    if plant == "Moxos":
        return "diesel"
    if plant == "Aranjuez" and code in {"ARJ01", "ARJ02", "ARJ03"}:
        return "dual_fuel"
    if code in {"GCH09", "GCH10", "GCH12"} or plant in {"Del Sur"}:
        return "gas_cc"
    if plant == "Entre Ríos" and re.match(r"ERI[345]\d", code):
        return "gas_cc"
    if plant == "Warnes" and code != "WAR05":
        return "gas_cc"
    return "gas_oc"


def read_genbruta(year):
    path = next(RAW.glob(f"genbruta_{year}.*"))
    if path.suffix == ".zip":
        z = zipfile.ZipFile(path)
        name = z.namelist()[0]
        data, engine = io.BytesIO(z.read(name)), ("xlrd" if name.endswith(".xls") else None)
    else:
        data, engine = path, ("xlrd" if path.suffix == ".xls" else None)
    return pd.read_excel(data, sheet_name=None, header=None, engine=engine)


def genbruta_total_mwh(sheet, with_months=False):
    """Value in the TOTAL column of the 'Total Generación bruta' row (and how many months are filled)."""
    header_row = next(i for i, r in sheet.iterrows() if any(str(v).strip().upper() == "TOTAL" for v in r.values))
    tcol = next(j for j, v in enumerate(sheet.iloc[header_row].values) if str(v).strip().upper() == "TOTAL")
    row = next(i for i, r in sheet.iterrows() if re.search(r"total generaci", " ".join(map(str, r.values[:3])), re.I))
    months = sum(1 for j in range(tcol - 12, tcol) if pd.notna(sheet.iat[row, j]) and float(sheet.iat[row, j]) > 0)
    total = float(sheet.iat[row, tcol])
    return (total, months) if with_months else total


gb = read_genbruta(REF_YEAR)
sheet = gb[list(gb)[0]]
header_row = next(i for i, r in sheet.iterrows() if any(str(v).strip().upper() == "TOTAL" for v in r.values))
tcol = next(j for j, v in enumerate(sheet.iloc[header_row].values) if str(v).strip().upper() == "TOTAL")

unit_rows = []
for i in range(header_row + 1, len(sheet)):
    code = sheet.iat[i, 1]
    val = sheet.iat[i, tcol]
    if isinstance(code, str) and code.strip() and pd.notna(val):
        code = code.strip().upper().replace(" ", "")
        plant = next((p for pat, p in UNIT_TO_PLANT if re.match(pat, code)), None)
        unit_rows.append((code, plant, float(val)))

unassigned = [c for c, p, _ in unit_rows if p is None]
check("every genbruta 2025 unit is assigned to a plant", not unassigned, ", ".join(unassigned))
gen_unit = pd.DataFrame(unit_rows, columns=["code", "plant", "mwh"])
gen_unit["type"] = [unit_type(c, p) for c, p in zip(gen_unit["code"], gen_unit["plant"])]

total_2025 = genbruta_total_mwh(sheet)
check("genbruta 2025: units sum to the file total", close(gen_unit["mwh"].sum(), total_2025, 1.0),
      f"{gen_unit['mwh'].sum():,.1f} vs {total_2025:,.1f} MWh")
check("genbruta 2025 total = 11,795.7 GWh (Memoria p. 15)", close(total_2025 / 1000, 11795.7, 0.05),
      f"{total_2025 / 1000:,.2f} GWh")

# Memoria 2025, p. 16: gross generation by type, GWh
REF_GEN_BY_TYPE = {"gas_cc": 7210.69, "hydro": 3354.21, "solar": 355.48, "biomass": 345.06,
                   "wind": 289.89, "gas_oc": 240.38, "diesel": 0.01, "dual_fuel": 0.00}
gen_type = gen_unit.groupby("type")["mwh"].sum() / 1000
for t, ref in REF_GEN_BY_TYPE.items():
    check(f"generation 2025 {t} = {ref} GWh", close(gen_type.get(t, 0.0), ref, 0.01), f"{gen_type.get(t, 0.0):.2f}")

gen_plant = gen_unit.groupby("plant")["mwh"].sum() / 1000  # GWh
missing_gen = sorted(set(plant_cap.index) - set(gen_plant.index))
check("every plant in the capacity table has 2025 generation rows", not missing_gen, ", ".join(missing_gen))

# ---------------------------------------------------------------- locations and departments
loc = pd.read_csv(HERE / "plant_locations.csv").set_index("plant")
check("every plant has a location", set(plant_cap.index) <= set(loc.index),
      ", ".join(sorted(set(plant_cap.index) - set(loc.index))))
check("no location without a plant", set(loc.index) <= set(plant_cap.index),
      ", ".join(sorted(set(loc.index) - set(plant_cap.index))))
check("precision is exact or approximate", set(loc["precision"]) <= {"exact", "approximate"})

geo = json.loads((RAW / "ne_10m_admin_1_bolivia.geojson").read_text(encoding="utf-8"))
DEPT_NAME = {"El Beni": "Beni"}


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return polys


def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][:2]
        xj, yj = ring[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def department_of(lat, lon):
    hits = []
    for f in geo["features"]:
        for poly in rings(f["geometry"]):
            if in_ring(lon, lat, poly[0]) and not any(in_ring(lon, lat, h) for h in poly[1:]):
                hits.append(DEPT_NAME.get(f["properties"]["name"], f["properties"]["name"]))
    return hits


dept = {}
for p in plant_cap.index:
    hits = department_of(loc.at[p, "lat"], loc.at[p, "lon"])
    dept[p] = hits[0] if len(hits) == 1 else None
    if len(hits) != 1:
        check(f"{p} falls in exactly one department", False, str(hits))

# CNDC genbruta 2025, sheet "MWh - DEPAR": production by department
dep_sheet = gb["MWh - DEPAR"]
hdr = next(i for i, r in dep_sheet.iterrows() if str(r.values[0]).strip().upper() == "MES")
tot = next(i for i, r in dep_sheet.iterrows() if str(r.values[0]).strip().upper() == "TOTAL")
ref_dept = {norm(dep_sheet.iat[hdr, j]): float(dep_sheet.iat[tot, j]) / 1000
            for j in range(1, dep_sheet.shape[1]) if norm(dep_sheet.iat[hdr, j]) != "TOTAL"}
ours = defaultdict(float)
for p, g in gen_plant.items():
    ours[norm(dept[p])] += g
diff = {d: round(ours.get(d, 0) - v, 2) for d, v in ref_dept.items() if not close(ours.get(d, 0), v, 0.05)}
check("2025 generation by department matches CNDC (from plant locations)", not diff, str(diff) if diff else "")

# ---------------------------------------------------------------- history
hist = pd.read_csv(HERE / "memoria_production_by_source_1996_2025.csv")
parts = hist[["hydro_gwh", "wind_gwh", "solar_gwh", "biomass_gwh", "thermal_gwh"]].sum(axis=1)
# The Memoria total adds and removes small local generation (Trinidad, Moxos, Las Carreras): <= 9.1 GWh
gap = (hist["total_gwh"] - parts).abs()
check("history: sources add up to the total (within local adjustments, 0.2 GWh)", (gap <= 0.2).all(),
      f"max gap {gap.max():.2f} GWh in {int(hist.loc[gap.idxmax(), 'year'])}")
mism, partial = {}, {}
for y in range(2005, REF_YEAR + 1):
    book = read_genbruta(y)
    t, months = genbruta_total_mwh(book[list(book)[0]], with_months=True)
    if months < 12:
        # CNDC never completed some annual files (they stop mid-year); the Memoria is the full record
        partial[y] = months
        continue
    m = float(hist.loc[hist["year"] == y, "total_gwh"].iloc[0])
    if not close(t / 1000, m, 0.06):
        mism[y] = (round(t / 1000, 1), m)
print(f"       genbruta files with fewer than 12 months (not compared): {partial}")
check("history: Memoria totals match every complete genbruta file 2005-2025", not mism, str(mism) if mism else "")
check("history 2025 matches the plant data", close(float(hist.iloc[-1]["total_gwh"]), gen_plant.sum(), 0.06))

# ---------------------------------------------------------------- outputs
MAIN_TECH = {}
for p, g in cap.groupby("plant"):
    t = g.groupby("tech_cndc")["capacity_mw"].sum()
    MAIN_TECH[p] = t.idxmax()

plants = []
for p in sorted(plant_cap.index, key=lambda q: -plant_cap[q]):
    g = cap[cap["plant"] == p]
    mw = round(float(plant_cap[p]), 2)
    gwh = round(float(gen_plant[p]), 2)
    plants.append({
        "id": slug(p),
        "name": p,
        "operator": g["agent"].iloc[0],
        "tech": MAIN_TECH[p],
        "capacity_mw": mw,
        "capacity_by_tech_mw": {k: round(float(v), 2) for k, v in g.groupby("tech_cndc")["capacity_mw"].sum().items()},
        "units": int(g["n_units"].sum()),
        "generation_2025_gwh": gwh,
        "capacity_factor_2025": round(gwh * 1000 / (mw * HOURS_2025), 3) if mw else None,
        "department": dept[p],
        "lat": float(loc.at[p, "lat"]),
        "lon": float(loc.at[p, "lon"]),
        "location_precision": loc.at[p, "precision"],
        "location_source": f"{loc.at[p, 'source']} {loc.at[p, 'source_ref']}",
        "location_note": loc.at[p, "note"] if isinstance(loc.at[p, "note"], str) else None,
    })

by_dept = defaultdict(lambda: {"capacity_mw": 0.0, "generation_2025_gwh": 0.0})
for r in plants:
    by_dept[r["department"]]["capacity_mw"] += r["capacity_mw"]
    by_dept[r["department"]]["generation_2025_gwh"] += r["generation_2025_gwh"]
departments_summary = sorted(
    ({"department": d, "capacity_mw": round(v["capacity_mw"], 2), "generation_2025_gwh": round(v["generation_2025_gwh"], 1)}
     for d, v in by_dept.items()), key=lambda r: -r["capacity_mw"])

meta = {
    "reference_year": REF_YEAR,
    "units": {
        "capacity_mw": "MW, CNDC capacity at the end of 2025 (effective capacity; thermal units at mean site temperature)",
        "generation_2025_gwh": "GWh, gross generation in 2025",
        "capacity_factor_2025": "generation / (capacity x 8,760 h); capacity at year end",
    },
    "sources": [
        "CNDC, Memoria y Resultados 2025, https://www.cndc.bo/wp-content/uploads/memorias/memyres_2025.pdf",
        "CNDC, Generación bruta 2025 (genbruta_2025.xlsx), https://www.cndc.bo/estadisticas/",
        "Global Energy Monitor, Global Integrated Power Tracker, September 2026 release (CC BY 4.0)",
        "OpenStreetMap contributors (ODbL)",
        "Natural Earth, admin-1 boundaries (public domain)",
    ],
    "generation_2025_gwh_by_type": {k: round(float(v), 2) for k, v in gen_type.items()},
    "capacity_mw_by_type": {k: round(float(v), 2) for k, v in cap.groupby("tech_cndc")["capacity_mw"].sum().items()},
    "totals": {
        "capacity_mw": round(float(plant_cap.sum()), 2),
        "generation_2025_gwh": round(float(gen_plant.sum()), 1),
        "plants": len(plants),
    },
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "plants.json").write_text(json.dumps({"meta": meta, "departments": departments_summary, "plants": plants},
                                            ensure_ascii=False, indent=1), encoding="utf-8")

history = {
    "meta": {
        "units": "GWh, gross generation of the SIN",
        "source": "CNDC, Memoria y Resultados 2025, 'Producción bruta (GWh) periodo 1996-2025', pp. 103-106",
        "note": "thermal = natural gas, plus diesel and dual-fuel engines (below 0.2 GWh a year since 2016)",
    },
    "series": [
        {"year": int(r.year), "hydro": r.hydro_gwh, "thermal": r.thermal_gwh, "wind": r.wind_gwh,
         "solar": r.solar_gwh, "biomass": r.biomass_gwh, "total": r.total_gwh}
        for r in hist.itertuples()
    ],
}
(OUT / "history.json").write_text(json.dumps(history, ensure_ascii=False, indent=1), encoding="utf-8")


def simplify(points, tol):
    """Douglas-Peucker on a list of [lon, lat]."""
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0][:2], points[-1][:2]
    dx, dy = x2 - x1, y2 - y1
    norm2 = dx * dx + dy * dy
    best, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        px, py = points[i][:2]
        if norm2 == 0:
            d = math.hypot(px - x1, py - y1)
        else:
            d = abs(dy * px - dx * py + x2 * y1 - y2 * x1) / math.sqrt(norm2)
        if d > best:
            best, idx = d, i
    if best <= tol:
        return [points[0], points[-1]]
    return simplify(points[: idx + 1], tol)[:-1] + simplify(points[idx:], tol)


sys.setrecursionlimit(20000)
features = []
for f in geo["features"]:
    polys = []
    for poly in rings(f["geometry"]):
        outer = [[round(x, 3), round(y, 3)] for x, y in simplify([c[:2] for c in poly[0]], 0.005)]
        # d3-geo wants exterior rings clockwise (negative shoelace area in lon/lat)
        area2 = sum(outer[i][0] * outer[i + 1][1] - outer[i + 1][0] * outer[i][1] for i in range(len(outer) - 1))
        if area2 > 0:
            outer.reverse()
        if len(outer) >= 4:
            polys.append([outer])
    features.append({"type": "Feature",
                     "properties": {"name": DEPT_NAME.get(f["properties"]["name"], f["properties"]["name"])},
                     "geometry": {"type": "MultiPolygon", "coordinates": polys}})
(OUT / "departments.json").write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")

print()
print(f"plants: {len(plants)}, capacity {meta['totals']['capacity_mw']} MW, generation 2025 {meta['totals']['generation_2025_gwh']} GWh")
for r in departments_summary:
    print(f"  {r['department']:<11} {r['capacity_mw']:>8.2f} MW  {r['generation_2025_gwh']:>8.1f} GWh")
approx = [r["name"] for r in plants if r["location_precision"] == "approximate"]
print(f"approximate locations ({len(approx)}): {', '.join(approx)}; "
      f"{sum(r['capacity_mw'] for r in plants if r['location_precision'] == 'approximate'):.2f} MW")

if FAILED:
    print(f"\n{len(FAILED)} check(s) failed: {FAILED}")
    sys.exit(1)
print("\nall checks passed")
