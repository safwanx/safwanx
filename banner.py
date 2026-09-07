"""
Generates banner.svg: name and subtitle on the site's gradient, with a
frisbee thrown across the banner behind the name, spinning, with a shadow.

Text is converted to paths with fontTools so it renders identically everywhere.
Fonts: Atkinson Hyperlegible Next (Google Fonts) in ./fonts as bold.ttf and medium.ttf.
Run with an argument like "-2.4s" to freeze a preview frame at that timeline offset.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = {"bold": "fonts/bold.ttf", "medium": "fonts/medium.ttf"}
_fonts = {}


def font(weight):
    if weight not in _fonts:
        _fonts[weight] = TTFont(FONTS[weight])
    return _fonts[weight]


def fmt(v):
    s = f"{v:.1f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def text(s, x, y, size, fill, weight="medium", anchor="middle", opacity=None):
    f = font(weight)
    gs, cmap, hmtx, upm = f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    k = size / upm
    names = [cmap.get(ord(c), ".notdef") for c in s]
    width = sum(hmtx[n][0] for n in names) * k
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs, ntos=fmt)
    cx = x
    for n in names:
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += hmtx[n][0] * k
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{pen.getCommands()}" fill="{fill}"{op}/>'


W, H, R = 1200, 240, 36
DUR = "6.4s"
FLIGHT = "M -110 172 C 240 92, 640 66, 1320 150"
GROUND = 212
KEYTIMES = "0;0.14;0.86;1"
KEYPOINTS = "0;0;1;1"
SPLINES = "0 0 1 1;0.3 0.05 0.6 1;0 0 1 1"


def motion(path, begin="0s", rotate=None):
    rot = f' rotate="{rotate}"' if rotate else ""
    return (f'<animateMotion path="{path}" dur="{DUR}" begin="{begin}" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{KEYTIMES}" keyPoints="{KEYPOINTS}" keySplines="{SPLINES}"{rot}/>')


def build(offset="0s"):
    def t(b):
        # shift every timeline by the preview offset so a still frame lands mid-flight
        return b if offset == "0s" else f"{float(offset[:-1]) + float(b[:-1]):.2f}s"

    trail = "".join(
        f'<g opacity="{op}"><g transform="rotate(-5)"><use href="#disc"/></g>{motion(FLIGHT, t(b), "auto")}</g>'
        for op, b in (("0.28", "0.06s"), ("0.16", "0.12s"), ("0.08", "0.18s"))
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">',
        '<title id="t">Safwan Nabeel. Machine learning researcher and engineer. A frisbee glides across the banner.</title>',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c3f2a"/><stop offset="1" stop-color="#1e1611"/></linearGradient>',
        '<radialGradient id="glow" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>',
        '<linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf8f3"/><stop offset="1" stop-color="#e3d9cc"/></linearGradient>',
        f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>',
        # disc: rim underside, top face, flight rings, and a marker that orbits to show spin
        '<g id="disc">'
        '<ellipse cx="0" cy="5" rx="42" ry="10" fill="#b5a897"/>'
        '<ellipse cx="0" cy="0" rx="42" ry="10" fill="url(#top)"/>'
        '<ellipse cx="0" cy="-0.6" rx="32" ry="6.4" fill="none" stroke="#9c3f2a" stroke-opacity="0.35" stroke-width="1.1"/>'
        '<ellipse cx="0" cy="-0.6" rx="20" ry="4" fill="none" stroke="#9c3f2a" stroke-opacity="0.25" stroke-width="1"/>'
        f'<circle r="2.8" fill="#9c3f2a"><animateMotion path="M 27 -0.6 A 27 5.4 0 1 1 -27 -0.6 A 27 5.4 0 1 1 27 -0.6" dur="0.5s" begin="{t("0s")}" repeatCount="indefinite"/></circle>'
        "</g>",
        "</defs>",
        f'<g clip-path="url(#clip)">',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
        # shadow on an implied ground, narrower and fainter while the disc is high
        f'<ellipse cx="0" cy="{GROUND}" rx="34" ry="4" fill="#000" opacity="0.28">'
        f'<animate attributeName="rx" values="36;36;24;36;36" keyTimes="0;0.14;0.5;0.86;1" dur="{DUR}" begin="{t("0s")}" repeatCount="indefinite"/>'
        f'{motion("M -110 0 L 1320 0", t("0s"))}</ellipse>',
        trail,
        f'<g><g transform="rotate(-5)"><use href="#disc"/></g>{motion(FLIGHT, t("0s"), "auto")}</g>',
        text("Safwan Nabeel", W / 2, 124, 56, "#ffffff", "bold"),
        text("Machine learning researcher and engineer", W / 2, 164, 19, "#ffffff", "medium", opacity="0.88"),
        "</g>",
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    offset = sys.argv[1] if len(sys.argv) > 1 else "0s"
    name = "banner.svg" if offset == "0s" else f"banner-preview{offset}.svg"
    with open(name, "w", encoding="utf-8") as fh:
        fh.write(build(offset))
    print("wrote", name)
