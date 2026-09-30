"""Build the waffle data for the uranium-enrichment project.

Converts U-235 enrichment levels (mass %) into atom counts per 1,000 atoms and
writes src/data/uranium-enrichment/waffles.json.

Sources:
  - Natural abundance: IUPAC CIAAW, https://www.ciaaw.org/uranium.htm
  - Atomic masses: AME2020 (via NIST)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src" / "data" / "uranium-enrichment" / "waffles.json"

M235 = 235.0439299  # u
M238 = 238.0507882  # u
NATURAL_U235_ATOM = 0.007204  # atom fraction (U-234 ignored, 0.0054 %)
SAMPLE = 1000


def atom_fraction(mass_fraction: float) -> float:
    """U-235 atom fraction from U-235 mass fraction (binary U-235/U-238 mix)."""
    n235 = mass_fraction / M235
    n238 = (1 - mass_fraction) / M238
    return n235 / (n235 + n238)


def mass_fraction(atom_frac: float) -> float:
    m235 = atom_frac * M235
    m238 = (1 - atom_frac) * M238
    return m235 / (m235 + m238)


cases = [
    {"id": "natural", "title": "Natural uranium", "kicker": "As mined",
     "u235_mass_pct": round(mass_fraction(NATURAL_U235_ATOM) * 100, 3),
     "u235_atom_pct": NATURAL_U235_ATOM * 100},
    {"id": "leu", "title": "Enriched to 5%", "kicker": "Low-enriched · reactor fuel",
     "u235_mass_pct": 5.0, "u235_atom_pct": atom_fraction(0.05) * 100},
    {"id": "heu", "title": "Enriched to 90%", "kicker": "Highly enriched · weapons-grade",
     "u235_mass_pct": 90.0, "u235_atom_pct": atom_fraction(0.90) * 100},
]

TAILS = 0.0025  # assumed U-235 mass fraction of depleted tails (typical 0.2-0.3 %)
XF = mass_fraction(NATURAL_U235_ATOM)  # natural feed, mass fraction


def feed_per_kg(xp: float) -> float:
    """kg of natural uranium per kg of product: F/P = (xp - xt) / (xf - xt)."""
    return (xp - TAILS) / (XF - TAILS)


for c in cases:
    c["feed_kg_per_kg"] = 1.0 if c["id"] == "natural" else round(feed_per_kg(c["u235_mass_pct"] / 100), 1)
    c["u235_atoms_exact"] = round(c["u235_atom_pct"] / 100 * SAMPLE, 2)
    # The grid shows the headline percentage the public knows (mass % for
    # enriched fuel, atom % for natural). The notes explain the <1 atom gap.
    shown_pct = c["u235_atom_pct"] if c["id"] == "natural" else c["u235_mass_pct"]
    c["u235_atoms_shown"] = round(shown_pct / 100 * SAMPLE)
    c["u235_atom_pct"] = round(c["u235_atom_pct"], 3)

# --- sanity checks against known reference values ---------------------------
checks = {
    "natural mass % ~ 0.711": abs(cases[0]["u235_mass_pct"] - 0.711) < 0.002,
    "5 wt% ~ 5.06 at%": abs(cases[1]["u235_atom_pct"] - 5.06) < 0.01,
    "90 wt% ~ 90.1 at%": abs(cases[2]["u235_atom_pct"] - 90.11) < 0.02,
    "natural shows 7 atoms": cases[0]["u235_atoms_shown"] == 7,
    "5% fuel needs ~10.3 kg natural per kg": abs(cases[1]["feed_kg_per_kg"] - 10.3) < 0.05,
    "4.5% check vs textbook 9.2 kg": abs(feed_per_kg(0.045) - 9.22) < 0.02,
}
for name, ok in checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if not all(checks.values()):
    raise SystemExit("Checks failed; data not written.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"sample_size": SAMPLE, "cases": cases}, indent=2) + "\n")
print(f"Wrote {OUT.relative_to(ROOT)}")
for c in cases:
    print(f"  {c['id']:8s} mass {c['u235_mass_pct']:>7}%  atom {c['u235_atom_pct']:>7}%  "
          f"exact {c['u235_atoms_exact']:>7}  shown {c['u235_atoms_shown']}")
