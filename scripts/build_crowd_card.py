"""Build the crowd-reliability case card on the profile's slate palette.

Produces assets/crowd-snow-case.png (wide, for desktop) and
assets/crowd-snow-case-narrow.png (stacked, for phones). Values come from
assets/crowd-case-values.csv; the photo is assets/crowd-0814.jpg (JHU-CROWD++
test image 0814). No model outputs are synthesized.

Usage: python scripts/build_crowd_card.py [--fonts DIR] [--photo PATH]
Fonts: Atkinson Hyperlegible Next TTFs named bold.ttf, medium.ttf, regular.ttf.
"""
import argparse
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

SLATE = (21, 43, 60)
PANEL = (41, 75, 89)
LIGHT = (232, 239, 240)
MUTED = (139, 184, 201)
TEAL = (145, 210, 193)


def load_case():
    rows = list(csv.DictReader((ASSETS / "crowd-case-values.csv").open(encoding="utf-8")))
    by_model = {r["model"]: r for r in rows}
    gt = float(rows[0]["gt_count"])
    models = [
        ("STEERER", "JHU evaluation", by_model["steerer_jhu"]),
        ("MPCount", "QNRF to JHU transfer", by_model["mpcount_qnrf_on_jhu"]),
    ]
    return gt, models


class Fonts:
    def __init__(self, folder):
        self.folder = Path(folder)

    def __call__(self, weight, size):
        return ImageFont.truetype(str(self.folder / f"{weight}.ttf"), size)


def rounded_card(w, h, radius=20):
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=SLATE + (255,))
    return card


def paste_photo(card, photo, box, radius=12):
    x, y, h = box
    w = round(h * photo.width / photo.height)
    im = photo.resize((w, h), Image.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    card.paste(im, (x, y), mask)
    return w


def panel(draw, F, box, name, subtitle, row, pad=28, name_size=34, sub_size=22, label_size=22, value_size=32):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=16, fill=PANEL)
    draw.text((x0 + pad, y0 + 22), name, font=F("bold", name_size), fill=LIGHT)
    draw.text((x0 + pad, y0 + 22 + name_size + 10), subtitle, font=F("regular", sub_size), fill=MUTED)
    lines = [
        ("Predicted", f"{float(row['pred_count']):,.1f}", LIGHT),
        ("Absolute error", f"{float(row['abs_error']):,.1f}", LIGHT),
        ("Risk percentile", f"{100 * float(row['risk_percentile']):.1f}%", TEAL),
    ]
    top = y0 + 22 + name_size + 10 + sub_size + 26
    step = value_size + 16
    for i, (label, value, color) in enumerate(lines):
        y = top + i * step
        draw.text((x0 + pad, y + (value_size - label_size) // 2 + 1), label, font=F("regular", label_size), fill=MUTED)
        draw.text((x1 - pad, y), value, font=F("bold", value_size), fill=color, anchor="ra")
    return top + 3 * step


def build_wide(F, photo, gt, models):
    W, H, PAD = 1600, 700, 56
    card = rounded_card(W, H)
    draw = ImageDraw.Draw(card)
    draw.text((PAD, 50), "Same image. Two missed counts.", font=F("bold", 50), fill=LIGHT)
    pw = paste_photo(card, photo, (PAD, 136, 520))
    x = PAD + pw + PAD
    draw.text((x, 142), "JHU-CROWD++ · image 0814 · snow", font=F("regular", 24), fill=MUTED)
    draw.text((x, 178), f"{gt:,.0f} people annotated", font=F("bold", 44), fill=LIGHT)
    gap = 28
    pw_ = (W - PAD - x - gap) // 2
    y0 = 254
    for i, (name, sub, row) in enumerate(models):
        px = x + i * (pw_ + gap)
        panel(draw, F, (px, y0, px + pw_, y0 + 300), name, sub, row)
    note = F("regular", 20)
    draw.text((x, 592), "Risk percentiles are ranked within each evaluation setting.", font=note, fill=MUTED)
    draw.text((x, 622), "Lower means ranked as less risky. Not a confidence probability.", font=note, fill=MUTED)
    return card


def build_narrow(F, photo, gt, models):
    W, H, PAD = 900, 1200, 48
    card = rounded_card(W, H)
    draw = ImageDraw.Draw(card)
    draw.text((PAD, 44), "Same image. Two missed counts.", font=F("bold", 44), fill=LIGHT)
    pw = paste_photo(card, photo, (PAD, 118, 380))
    x = PAD + pw + 40
    draw.text((x, 126), "JHU-CROWD++ · image 0814 · snow", font=F("regular", 22), fill=MUTED)
    draw.text((x, 164), f"{gt:,.0f} people", font=F("bold", 40), fill=LIGHT)
    draw.text((x, 212), "annotated", font=F("bold", 40), fill=LIGHT)
    draw.text((x, 290), "Both models missed most", font=F("regular", 24), fill=MUTED)
    draw.text((x, 322), "of the crowd. Only one", font=F("regular", 24), fill=MUTED)
    draw.text((x, 354), "was flagged as risky.", font=F("regular", 24), fill=MUTED)
    y0 = 540
    for name, sub, row in models:
        panel(draw, F, (PAD, y0, W - PAD, y0 + 270), name, sub, row, value_size=30)
        y0 += 270 + 24
    note = F("regular", 21)
    draw.text((PAD, 1122), "Risk percentiles are ranked within each evaluation setting.", font=note, fill=MUTED)
    draw.text((PAD, 1152), "Lower means ranked as less risky. Not a confidence probability.", font=note, fill=MUTED)
    return card


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default="fonts")
    ap.add_argument("--photo", default=str(ASSETS / "crowd-0814.jpg"))
    args = ap.parse_args()
    F = Fonts(args.fonts)
    photo = Image.open(args.photo).convert("RGB")
    gt, models = load_case()
    build_wide(F, photo, gt, models).save(ASSETS / "crowd-snow-case.png", optimize=True)
    build_narrow(F, photo, gt, models).save(ASSETS / "crowd-snow-case-narrow.png", optimize=True)
    print("wrote crowd-snow-case.png and crowd-snow-case-narrow.png")


if __name__ == "__main__":
    main()
