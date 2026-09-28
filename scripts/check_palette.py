"""Validate a categorical palette for colorblind safety and contrast.

Usage:
  python3 scripts/check_palette.py "#4A7FB5,#D9661A" --surface "#F4F6F7"

Checks every pair of colors:
  - normal-vision difference (OKLab distance x100, want >= 15)
  - difference under protanopia, deuteranopia, tritanopia
    (Machado et al. 2009, severity 1.0; want >= 8, 6-8 only with direct labels)
and each color's WCAG contrast against the surface (want >= 3:1 for marks).
"""
import argparse
import itertools
import math

CVD = {
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def hex_to_lin(h):
    h = h.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]


def mat(m, v):
    return [min(1, max(0, sum(m[r][c] * v[c] for c in range(3)))) for r in range(3)]


def oklab(lin):
    r, g, b = lin
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (x ** (1 / 3) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def de(a, b):
    return math.dist(oklab(a), oklab(b)) * 100


def luminance(lin):
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("palette", help="comma-separated hex colors")
    ap.add_argument("--surface", default="#FFFFFF")
    args = ap.parse_args()
    cols = [c.strip() for c in args.palette.split(",")]
    surf = hex_to_lin(args.surface)
    ok = True

    print(f"Surface {args.surface}")
    for c in cols:
        cr = contrast(hex_to_lin(c), surf)
        flag = "PASS" if cr >= 3 else "WARN"
        # contrast below 3:1 is a warning: it requires visible labels or a table view
        print(f"  [{flag}] {c} contrast {cr:.2f}:1")

    for a, b in itertools.combinations(cols, 2):
        la, lb = hex_to_lin(a), hex_to_lin(b)
        normal = de(la, lb)
        worst = min((de(mat(m, la), mat(m, lb)), k) for k, m in CVD.items())
        n_ok, c_ok = normal >= 15, worst[0] >= 8
        ok &= n_ok and worst[0] >= 6
        print(f"  [{'PASS' if n_ok else 'FAIL'}] {a} vs {b} normal dE {normal:.1f}")
        tag = "PASS" if c_ok else ("WARN" if worst[0] >= 6 else "FAIL")
        print(f"  [{tag}] {a} vs {b} worst CVD dE {worst[0]:.1f} ({worst[1]})")

    print("RESULT:", "OK" if ok else "FIX PALETTE")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
