"""Link-preview images for the nuclear-capacity-vs-share project.

Writes public/og/nuclear-capacity-vs-share.png (1200x630) and -square.png (1200x1200).
Run from the repo root after build_data.py:  python3 analysis/nuclear-capacity-vs-share/build_og.py

How: the SVG is composed here with every text run converted to outlines from the site's own
font (Atkinson Hyperlegible Next, @fontsource-variable package), so the result does not depend on
the fonts installed on the machine. Node's sharp (already in node_modules) rasterizes the SVG.
Colors are read from the light Isotype tokens (body.iso block in src/styles/tokens.css).
Numbers come from src/data/nuclear-capacity-vs-share/nuclear.json.
Needs fonttools and brotli (analysis/requirements.txt).
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/data/nuclear-capacity-vs-share/nuclear.json"
FONT = ROOT / "node_modules/@fontsource-variable/atkinson-hyperlegible-next/files/atkinson-hyperlegible-next-latin-wght-normal.woff2"
OUT = ROOT / "public/og"
SLUG = "nuclear-capacity-vs-share"

# ---- tokens (light Isotype) -------------------------------------------------------------------
css = (ROOT / "src/styles/tokens.css").read_text()
block = css[css.index("body.iso {"):]
block = block[: block.index("}")]
T = dict(re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})", block))
for k in ("bg", "panel", "ink", "ink-2", "ink-3", "rule", "grid", "marker", "cat-1", "cat-2"):
    assert k in T, f"token --{k} not found in body.iso"

# ---- data -------------------------------------------------------------------------------------
d = json.loads(DATA.read_text())
Y, w = d["years"], d["world"]
n = len(Y) - 1
cap0, cap1 = w["capacity_gw"][0], w["capacity_gw"][n]
sh0, sh1 = w["share_pct"][0], w["share_pct"][n]
fold = f"{cap1 / cap0:.1f}"

# ---- text to outlines -------------------------------------------------------------------------
_base = TTFont(FONT)
_inst: dict[int, TTFont] = {}


def font(wght: int) -> TTFont:
    if wght not in _inst:
        _inst[wght] = instancer.instantiateVariableFont(TTFont(FONT), {"wght": wght})
    return _inst[wght]


def text(s: str, x: float, y: float, size: float, wght: int = 400, fill: str = "ink", anchor: str = "start") -> tuple[str, float]:
    """Return (svg <path>, width) for one line of text, baseline at y."""
    f = font(wght)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    k = size / f["head"].unitsPerEm
    width = sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in s) * k
    if anchor == "end":
        x -= width
    elif anchor == "middle":
        x -= width / 2
    out, cx = [], x
    for c in s:
        g = cmap.get(ord(c), ".notdef")
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        out.append(pen.getCommands())
        cx += hmtx[g][0] * k
    return f'<path fill="{T[fill]}" d="{" ".join(out)}"/>', width


def lines(parts: list[str], x: float, y: float, size: float, lead: float, wght: int, fill: str = "ink") -> str:
    return "".join(text(p, x, y + i * lead, size, wght, fill)[0] for i, p in enumerate(parts))


# ---- chart ------------------------------------------------------------------------------------
def chart(x0: float, y0: float, cw: float, ch: float, fs: float) -> str:
    """Two stacked panels: capacity (GW) on top, share (%) below. Never two y-axes."""
    gap = 3.2 * fs
    ph = (ch - 1.6 * fs - gap - 2.2 * fs) / 2
    lx = lambda i: x0 + (Y[i] - Y[0]) / (Y[n] - Y[0]) * (cw - 4.2 * fs)
    top, bot = y0 + 1.6 * fs, y0 + 1.6 * fs + ph + gap
    yc = lambda v: top + ph - v / 1300 * ph
    ys = lambda v: bot + ph - v / 10 * ph
    path = lambda f, vals: "M" + " L".join(f"{lx(i):.1f},{f(v):.1f}" for i, v in enumerate(vals))
    s = []
    s.append(text("Nuclear capacity, GW", x0, top - 0.6 * fs, fs, 700)[0])
    s.append(text("Nuclear share of world electricity", x0, bot - 0.6 * fs, fs, 700)[0])
    for b in (yc(0), ys(0)):
        s.append(f'<line x1="{x0}" x2="{lx(n)}" y1="{b:.1f}" y2="{b:.1f}" stroke="{T["rule"]}" stroke-width="1.5"/>')
    s.append(f'<line x1="{x0}" x2="{lx(n)}" y1="{ys(sh0):.1f}" y2="{ys(sh0):.1f}" stroke="{T["ink-3"]}" stroke-width="1.5" stroke-dasharray="6 6"/>')
    s.append(f'<path d="{path(yc, w["capacity_gw"])}" fill="none" stroke="{T["cat-1"]}" stroke-width="{fs * 0.22:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="{path(ys, w["share_pct"])}" fill="none" stroke="{T["cat-2"]}" stroke-width="{fs * 0.28:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    ex = lx(n) + 0.5 * fs
    s.append(text(f"{cap1:,.0f}", ex, yc(cap1) + 0.35 * fs, fs, 700)[0])
    s.append(text(f"{cap0:,.0f}", x0, yc(cap0) - 0.6 * fs, fs, 400, "ink-2")[0])
    s.append(text(f"{sh1:.1f}%", ex, ys(sh1) + 0.35 * fs, fs, 700)[0])
    s.append(text(f"{sh0:.1f}%", x0, ys(sh0) - 0.6 * fs, fs, 400, "ink-2")[0])
    for yr, anchor in ((Y[0], "start"), (Y[n], "end")):
        s.append(text(str(yr), lx(Y.index(yr)), bot + ph + 1.5 * fs, fs * 0.9, 400, "ink-3", anchor)[0])
    return "".join(s)


def headline(x: float, y: float, size: float, lead: float, split: list[str]) -> str:
    """Headline lines; the fold figure gets the highlighter band behind it."""
    out = []
    for i, line in enumerate(split):
        by = y + i * lead
        if f"{fold} times" in line:
            pre = line.split(f"{fold} times")[0]
            _, pw = text(pre, 0, 0, size, 800)
            _, hw = text(f"{fold} times", 0, 0, size, 800)
            out.append(f'<rect x="{x + pw - size * .08:.1f}" y="{by - size * .78:.1f}" width="{hw + size * .16:.1f}" height="{size * .98:.1f}" fill="{T["marker"]}"/>')
        out.append(text(line, x, by, size, 800)[0])
    return "".join(out)


def svg(W: int, H: int, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>{body}</svg>')


def panel(x, y, pw, ph) -> str:
    return f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="12" fill="{T["panel"]}"/>'


foot = f"Data: DNV Energy Transition Outlook 2026, forecast. Chart: Marco Herbas Lopez"
eyebrow = f"Nuclear power to {Y[n]}"

# 1200 x 630
wide = svg(1200, 630, "".join([
    text(eyebrow, 64, 108, 26, 600, "ink-2")[0],
    headline(64, 172, 46, 56, ["Nuclear capacity", f"grows {fold} times", f"by {Y[n]}. Its share", "of the world's", "electricity does not."]),
    panel(620, 64, 516, 462),
    chart(652, 96, 400, 410, 20),
    text(foot, 64, 586, 20, 400, "ink-3")[0],
]))

# 1200 x 1200
square = svg(1200, 1200, "".join([
    text(eyebrow, 80, 130, 32, 600, "ink-2")[0],
    headline(80, 214, 66, 78, [f"Nuclear capacity grows {fold} times", f"by {Y[n]}. Its share of the world's", "electricity does not."]),
    panel(80, 420, 1040, 660),
    chart(130, 470, 860, 580, 28),
    text(foot, 80, 1140, 24, 400, "ink-3")[0],
]))

OUT.mkdir(parents=True, exist_ok=True)
for name, s in ((f"{SLUG}.png", wide), (f"{SLUG}-square.png", square)):
    tmp = OUT / (name + ".svg")
    tmp.write_text(s)
    js = "require('sharp')(process.argv[1]).png().toFile(process.argv[2]).then(i=>console.log(process.argv[2].split('/').pop(), i.width+'x'+i.height))"
    subprocess.run(["node", "-e", js, str(tmp), str(OUT / name)], check=True, cwd=ROOT)
    tmp.unlink()
