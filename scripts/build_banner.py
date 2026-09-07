"""Build profile-coast.svg and profile-coast-narrow.svg from scripts/banner-template.svg.

The template holds the illustration with live <text> elements. This script
converts the text to outlines with Atkinson Hyperlegible Next so the banner
renders identically on every platform, and produces a taller narrow variant
with larger lettering for phone widths.

Usage: python scripts/build_banner.py [--fonts DIR]
Fonts: Atkinson Hyperlegible Next TTFs named bold.ttf and regular.ttf.
"""
import argparse
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "banner-template.svg"
_fonts = {}


def fmt(v):
    s = f"{v:.1f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def outline(fonts_dir, s, x, y, size, fill, weight="regular", spacing=0.0):
    key = weight
    if key not in _fonts:
        _fonts[key] = TTFont(str(Path(fonts_dir) / f"{weight}.ttf"))
    f = _fonts[key]
    gs, cmap, hmtx, upm = f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    k = size / upm
    pen = SVGPathPen(gs, ntos=fmt)
    cx = x
    for ch in s:
        name = cmap.get(ord(ch), ".notdef")
        gs[name].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += hmtx[name][0] * k + spacing
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'


TEXT_RE = re.compile(r'[ \t]*<text x="(?P<x>[\d.]+)" y="(?P<y>[\d.]+)" font-size="(?P<size>[\d.]+)"'
                     r'(?: font-weight="(?P<weight>\d+)")?(?: letter-spacing="(?P<spacing>-?[\d.]+)")?'
                     r' fill="(?P<fill>#[0-9a-fA-F]+)">(?P<text>.*?)</text>\n')


def render(fonts_dir, svg, scale=1.0, y_shift=0.0, x_shift=0.0):
    def repl(m):
        weight = "bold" if m.group("weight") == "700" else "regular"
        spacing = float(m.group("spacing") or 0) * scale
        text = m.group("text").replace("&amp;", "&")
        return "    " + outline(fonts_dir, text, float(m.group("x")) + x_shift, float(m.group("y")) * scale + y_shift,
                                float(m.group("size")) * scale, m.group("fill"), weight, spacing) + "\n"
    out = TEXT_RE.sub(repl, svg)
    return out.replace("    text { font-family: 'Atkinson Hyperlegible Next', 'Segoe UI', sans-serif; }\n", "")


def narrow(svg, height=560, shift=200):
    svg = svg.replace('width="1200" height="360" viewBox="0 0 1200 360"', f'width="1200" height="{height}" viewBox="0 0 1200 {height}"')
    svg = svg.replace('<rect width="1200" height="360" rx="22"/>', f'<rect width="1200" height="{height}" rx="22"/>')
    svg = svg.replace('<rect width="1200" height="360" fill="white"/>', f'<rect width="1200" height="{height}" fill="white"/>')
    svg = svg.replace('<path fill="url(#sky)" d="M0 0h1200v360H0z"/>', f'<path fill="url(#sky)" d="M0 0h1200v{height}H0z"/>')
    # drop the landscape so the taller sky has room for larger lettering
    svg = svg.replace("    <!-- Mountain silhouettes taper into the water. -->\n", f'    <g transform="translate(0 {shift})">\n    <!-- Mountain silhouettes taper into the water. -->\n')
    svg = svg.replace('    <path d="M0 328Q139 304 274 328T525 360H0Z" fill="#102d3a"/>\n', '    <path d="M0 328Q139 304 274 328T525 360H0Z" fill="#102d3a"/>\n    </g>\n')
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default="fonts")
    args = ap.parse_args()
    template = TEMPLATE.read_text(encoding="utf-8")
    (ROOT / "profile-coast.svg").write_text(render(args.fonts, template), encoding="utf-8")
    (ROOT / "profile-coast-narrow.svg").write_text(render(args.fonts, narrow(template), scale=1.55, y_shift=-10), encoding="utf-8")
    print("wrote profile-coast.svg and profile-coast-narrow.svg")


if __name__ == "__main__":
    main()
