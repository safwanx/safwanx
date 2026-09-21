"""Build the identity-leakage result card on the profile's slate palette.

Produces assets/privacy-leakage.png (wide) and assets/privacy-leakage-narrow.png (phones).
Every number is quoted from the abstract of "Anonymized but Not Anonymous" (ACCV 2026):
cross-view C2 probes, coverage-adjusted Rank-1. Nothing is synthesized.

Usage: python scripts/build_privacy_card.py [--fonts DIR]
Fonts: Atkinson Hyperlegible Next TTFs named bold.ttf, medium.ttf, regular.ttf.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1] / "assets"

SLATE = (21, 43, 60)
PANEL = (41, 75, 89)
LIGHT = (232, 239, 240)
MUTED = (139, 184, 201)
TEAL = (145, 210, 193)
CORAL = (220, 170, 145)

GROUPS = [
    ("Face recognition", [("Original video", 83.1, TEAL), ("Face blurred", 3.4, CORAL)]),
    ("Person re-identification", [("Original video", 85.3, TEAL), ("Face blurred", 84.7, CORAL)]),
]
TITLE = "Blur the face. The person is still there."
SOURCE = "NTU120-Privacy-21K · cross-view probes · 38-identity gallery"
NOTES = ["Coverage-adjusted Rank-1, quoted from the paper.",
         "Linkability in the tested setting, not a formal privacy guarantee."]


class Fonts:
    def __init__(self, folder):
        self.folder = Path(folder)

    def __call__(self, weight, size):
        return ImageFont.truetype(str(self.folder / f"{weight}.ttf"), size)


def card(w, h, radius=20):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=SLATE + (255,))
    return im


def group(draw, F, x, y, width, name, rows, name_size, label_size, value_size, bar_h, label_w):
    draw.text((x, y), name, font=F("bold", name_size), fill=LIGHT)
    y += name_size + 22
    track = width - label_w - 130
    for label, value, color in rows:
        draw.text((x, y + (bar_h - label_size) // 2 - 2), label, font=F("regular", label_size), fill=MUTED)
        bx = x + label_w
        draw.rounded_rectangle([bx, y, bx + track, y + bar_h], radius=bar_h // 2, fill=PANEL)
        fill_w = max(bar_h, round(track * value / 100))
        draw.rounded_rectangle([bx, y, bx + fill_w, y + bar_h], radius=bar_h // 2, fill=color)
        draw.text((bx + track + 18, y + (bar_h - value_size) // 2 - 3), f"{value:.1f}%", font=F("bold", value_size), fill=color)
        y += bar_h + 20
    return y


def build_wide(F):
    W, H, PAD = 1600, 540, 56
    im = card(W, H)
    d = ImageDraw.Draw(im)
    d.text((PAD, 50), TITLE, font=F("bold", 50), fill=LIGHT)
    d.text((PAD, 124), SOURCE, font=F("regular", 24), fill=MUTED)
    gap = 72
    col = (W - 2 * PAD - gap) // 2
    for i, (name, rows) in enumerate(GROUPS):
        group(d, F, PAD + i * (col + gap), 214, col, name, rows, 36, 24, 34, 40, 196)
    for i, line in enumerate(NOTES):
        d.text((PAD, 434 + i * 32), line, font=F("regular", 21), fill=MUTED)
    return im


def build_narrow(F):
    W, H, PAD = 900, 880, 48
    im = card(W, H)
    d = ImageDraw.Draw(im)
    d.text((PAD, 44), "Blur the face.", font=F("bold", 52), fill=LIGHT)
    d.text((PAD, 104), "The person is still there.", font=F("bold", 52), fill=LIGHT)
    d.text((PAD, 186), "NTU120-Privacy-21K · cross-view probes", font=F("regular", 26), fill=MUTED)
    d.text((PAD, 220), "38-identity gallery", font=F("regular", 26), fill=MUTED)
    y = 300
    for name, rows in GROUPS:
        y = group(d, F, PAD, y, W - 2 * PAD, name, rows, 38, 27, 38, 46, 214) + 40
    for i, line in enumerate(NOTES):
        d.text((PAD, 784 + i * 34), line, font=F("regular", 23), fill=MUTED)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default="fonts")
    F = Fonts(ap.parse_args().fonts)
    build_wide(F).save(ASSETS / "privacy-leakage.png", optimize=True)
    build_narrow(F).save(ASSETS / "privacy-leakage-narrow.png", optimize=True)
    print("wrote privacy-leakage.png and privacy-leakage-narrow.png")


if __name__ == "__main__":
    main()
