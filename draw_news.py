#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

A newspaper-style single image summing up the day's world news.
Deterministic: fixed palette, fixed layout, no randomness, no time
or network access. Writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
NAVY = (18, 38, 74)
RED = (178, 32, 44)
TEAL = (13, 110, 102)
GOLD = (176, 124, 30)
GREY = (90, 88, 82)
LINE = (60, 58, 52)
SKY = (214, 228, 238)
SEA = (46, 92, 128)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    f = font(SANS_B, 15)
    draw.text((x, y), label, font=f, fill=color)
    return y + 22


def rule(draw, x0, y, x1, width=2, fill=LINE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictograms
def ship(draw, x, y, s):
    """Container ship, side view, scaled by s (width ~ 3.4*s)."""
    hull = (x, y + int(1.5 * s), x + int(3.4 * s), y + int(2.1 * s))
    draw.polygon(
        [(x, y + int(1.5 * s)), (x + int(3.4 * s), y + int(1.5 * s)),
         (x + int(3.1 * s), y + int(2.1 * s)), (x + int(0.3 * s), y + int(2.1 * s))],
        fill=RED)
    draw.rectangle([x + int(0.5 * s), y + int(0.9 * s), x + int(1.1 * s), y + int(1.5 * s)],
                   fill=TEAL)
    draw.rectangle([x + int(1.2 * s), y + int(0.9 * s), x + int(1.8 * s), y + int(1.5 * s)],
                   fill=GOLD)
    draw.rectangle([x + int(1.9 * s), y + int(0.9 * s), x + int(2.5 * s), y + int(1.5 * s)],
                   fill=NAVY)
    draw.rectangle([x + int(2.7 * s), y + int(0.7 * s), x + int(3.0 * s), y + int(1.5 * s)],
                   fill=(240, 240, 235))
    draw.line([(x, y + int(2.35 * s)), (x + int(3.4 * s), y + int(2.35 * s))],
              fill=SEA, width=3)
    for wx in (0.5, 1.2, 1.9, 2.6):
        draw.line([(x + int(wx * s), y + int(2.6 * s)),
                   (x + int((wx + 0.4) * s), y + int(2.6 * s))], fill=SEA, width=2)


def flame(draw, cx, base, h, w):
    """Simple flame shape."""
    pts = [(cx - w // 2, base), (cx - w // 3, base - h // 2),
           (cx - w // 6, base - h // 3), (cx, base - h),
           (cx + w // 6, base - h // 2), (cx + w // 3, base - h // 3),
           (cx + w // 2, base)]
    draw.polygon(pts, fill=(226, 88, 34))
    draw.polygon([(cx - w // 5, base), (cx, base - h // 2),
                  (cx + w // 5, base)], fill=(245, 196, 66))


def missile(draw, x, y, s):
    draw.polygon([(x, y), (x + int(0.5 * s), y + int(0.4 * s)),
                  (x, y + int(0.8 * s))], fill=RED)
    draw.rectangle([x, y + int(0.8 * s), x + int(0.5 * s), y + int(2.6 * s)],
                   fill=NAVY)
    draw.polygon([(x, y + int(2.6 * s)), (x + int(0.5 * s), y + int(2.6 * s)),
                  (x + int(0.25 * s), y + int(3.1 * s))], fill=NAVY)
    draw.polygon([(x - int(0.25 * s), y + int(2.2 * s)), (x, y + int(2.2 * s)),
                  (x, y + int(2.7 * s))], fill=RED)
    draw.polygon([(x + int(0.5 * s), y + int(2.2 * s)),
                  (x + int(0.75 * s), y + int(2.2 * s)),
                  (x + int(0.5 * s), y + int(2.7 * s))], fill=RED)
    draw.polygon([(cx, cy) for cx, cy in
                  [(x + int(0.25 * s), y + int(3.1 * s)),
                   (x + int(0.05 * s), y + int(3.7 * s)),
                   (x + int(0.45 * s), y + int(3.7 * s))]], fill=(245, 196, 66))


def jet(draw, x, y, s):
    draw.polygon([(x, y + int(0.5 * s)), (x + int(3.2 * s), y + int(0.9 * s)),
                  (x + int(3.2 * s), y + int(1.1 * s)), (x, y + int(1.5 * s))],
                 fill=(120, 124, 130))
    draw.polygon([(x + int(0.9 * s), y), (x + int(1.5 * s), y + int(0.6 * s)),
                  (x + int(1.1 * s), y + int(1.0 * s))], fill=(90, 94, 100))
    draw.polygon([(x + int(1.6 * s), y + int(1.5 * s)),
                  (x + int(2.0 * s), y + int(2.3 * s)),
                  (x + int(1.5 * s), y + int(1.6 * s))], fill=(90, 94, 100))
    draw.ellipse([x + int(2.9 * s), y + int(0.85 * s),
                  x + int(3.35 * s), y + int(1.15 * s)], fill=(245, 196, 66))


def tanker(draw, x, y, s):
    draw.rectangle([x, y + int(0.4 * s), x + int(2.2 * s), y + int(1.4 * s)],
                   fill=(200, 200, 195), outline=LINE, width=2)
    draw.rectangle([x + int(2.3 * s), y + int(0.7 * s), x + int(3.0 * s), y + int(1.4 * s)],
                   fill=RED)
    draw.ellipse([x + int(0.3 * s), y + int(1.4 * s), x + int(0.9 * s), y + int(2.0 * s)],
                 fill=INK)
    draw.ellipse([x + int(1.5 * s), y + int(1.4 * s), x + int(2.1 * s), y + int(2.0 * s)],
                 fill=INK)
    draw.ellipse([x + int(2.4 * s), y + int(1.4 * s), x + int(2.9 * s), y + int(1.9 * s)],
                 fill=INK)
    flame(draw, x + int(1.1 * s), y + int(0.4 * s), int(1.0 * s), int(0.9 * s))


def gavel(draw, x, y, s):
    draw.rectangle([x, y, x + int(1.6 * s), y + int(0.5 * s)], fill=(122, 82, 40))
    draw.line([(x + int(0.8 * s), y + int(0.5 * s)),
               (x + int(0.8 * s), y + int(2.0 * s))], fill=(122, 82, 40), width=int(0.28 * s))
    draw.rectangle([x + int(0.2 * s), y + int(2.0 * s), x + int(1.4 * s), y + int(2.3 * s)],
                   fill=(122, 82, 40))


def chart_down(draw, x, y, w, h):
    pts = [(x, y + int(0.15 * h)), (x + w // 4, y + int(0.35 * h)),
           (x + w // 2, y + int(0.25 * h)), (x + 3 * w // 4, y + int(0.6 * h)),
           (x + w, y + int(0.95 * h))]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.line([(x, y + h), (x + w, y + h)], fill=GREY, width=2)
    draw.polygon([(x + w, y + int(0.95 * h)), (x + w - 12, y + int(0.95 * h) - 4),
                  (x + w - 4, y + int(0.95 * h) + 10)], fill=RED)


def bars(draw, x, y, w, h):
    vals = [0.45, 0.62, 0.5, 0.8, 1.0]
    bw = w // 6
    for i, v in enumerate(vals):
        bx = x + i * (bw + 4)
        bh = int(h * v)
        draw.rectangle([bx, y + h - bh, bx + bw, y + h],
                       fill=RED if i == len(vals) - 1 else NAVY)


# ------------------------------------------------------------------- stories
LEAD = {
    "kicker": "TRADE  •  WASHINGTON",
    "headline": "US proposes new tariffs on 14 trading partners",
    "deck": "Washington unveils country-specific duties aimed at factory "
            "overcapacity, hitting China, the EU, Japan and India — a second "
            "act for the tariff war.",
}

PANELS = [
    {"kicker": "MIDDLE EAST", "color": RED,
     "headline": "Houthis strike Saudi ports and oil refinery",
     "deck": "Missiles are intercepted over Riyadh as Yemen's Houthis claim "
             "hits on the Ras Tanura refinery; oil climbs towards $95 a barrel.",
     "pic": "flame"},
    {"kicker": "ASIA", "color": NAVY,
     "headline": "Kim orders wider nuclear deployment",
     "deck": "North Korea's leader calls for tactical nuclear weapons across "
             "more domains and faster production, ignoring Trump's overture.",
     "pic": "missile"},
    {"kicker": "WAR IN UKRAINE", "color": TEAL,
     "headline": "Ukraine hits Russian airbase; five jets damaged",
     "deck": "Kyiv says drones struck Savasleyka airfield and two oil "
             "refineries, as missiles hit the capital.",
     "pic": "jet"},
    {"kicker": "DISASTER  •  EGYPT", "color": RED,
     "headline": "Cairo tanker fire kills at least 31",
     "deck": "A fuel tanker overturns and bursts into flames on the ring road "
             "around the capital; about 21 more are hurt.",
     "pic": "tanker"},
    {"kicker": "ISRAEL", "color": NAVY,
     "headline": "Judges urge end to Netanyahu trial",
     "deck": "Israeli judges recommend prosecutors drop the long-running "
             "corruption case, saying conviction looks unlikely.",
     "pic": "gavel"},
    {"kicker": "MARKETS", "color": TEAL,
     "headline": "AI sell-off drags Nasdaq toward bear market",
     "deck": "US stocks slide again as selling in AI-linked shares continues; "
             "tariff fears add to the pain for investors.",
     "pic": "chart"},
]

ALSO = [
    "Macy's 100th Thanksgiving Day Parade postponed to Saturday as a storm bears down on New York",
    "First Pakistani astronaut boards China's Tiangong space station",
    "COP31 climate talks collapse as OPEC blames the EU",
]


def draw_pic(draw, kind, x, y, w, h):
    if kind == "flame":
        flame(draw, x + w // 2, y + h - 6, h - 14, w // 2)
    elif kind == "missile":
        missile(draw, x + w // 2 - 14, y + 2, 16)
    elif kind == "jet":
        jet(draw, x + 2, y + h // 2 - 16, 22)
    elif kind == "tanker":
        tanker(draw, x + 2, y + h // 2 - 18, 20)
    elif kind == "gavel":
        gavel(draw, x + w // 2 - 24, y + 6, 26)
    elif kind == "chart":
        chart_down(draw, x + 6, y + 8, w - 12, h - 20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 34  # margin

    # ---- masthead
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((m, 14), "THE WORLD IN ONE PAGE",
           font=font(SERIF, 52), fill=(250, 246, 236))
    d.text((m, 76), "THURSDAY 26 NOVEMBER 2026  •  WORLD NEWS  •  ONE DAY, ONE IMAGE",
           font=font(SANS_B, 17), fill=(214, 200, 150))
    rule(d, m, 118, W - m, width=3)

    # ---- lead story
    ly = 132
    d.rectangle([m, ly, W - m, ly + 248], outline=LINE, width=2)
    d.rectangle([m, ly, W - m, ly + 248], fill=(255, 253, 247))
    d.rectangle([m, ly, W - m, ly + 248], outline=LINE, width=2)
    tx = m + 22
    y = ly + 16
    y = kicker(d, tx, y, LEAD["kicker"], RED)
    y = text_block(d, tx, y + 4, LEAD["headline"], font(SERIF, 40), INK, 560, leading=46)
    y = text_block(d, tx, y + 10, LEAD["deck"], font(SERIF_R, 21), (52, 50, 46), 560,
                   leading=28)
    # illustration: ship + tariff bars on the right
    ix = W - m - 330
    d.rectangle([ix, ly + 16, W - m - 20, ly + 232], fill=SKY)
    ship(d, ix + 26, ly + 80, 56)
    bars(d, ix + 30, ly + 34, 250, 52)

    # ---- six panels, two rows of three
    pw = (W - 2 * m - 2 * 18) // 3
    ph = 208
    top = 404
    for row in range(2):
        for col in range(3):
            p = PANELS[row * 3 + col]
            x0 = m + col * (pw + 18)
            y0 = top + row * (ph + 16)
            d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 253, 247),
                        outline=LINE, width=2)
            px = x0 + 14
            py = y0 + 12
            py = kicker(d, px, py, p["kicker"], p["color"])
            # pictogram in a small box at the right of the headline area
            pic_w, pic_h = 74, 56
            d.rectangle([x0 + pw - pic_w - 12, y0 + 10,
                         x0 + pw - 12, y0 + 10 + pic_h], fill=SKY)
            draw_pic(d, p["pic"], x0 + pw - pic_w - 12, y0 + 10, pic_w, pic_h)
            y = text_block(d, px, py + 2, p["headline"], font(SERIF, 22), INK,
                           pw - pic_w - 30, leading=26)
            text_block(d, px, y + 8, p["deck"], font(SANS, 15), (52, 50, 46),
                       pw - 28, leading=20)

    # ---- also-today strip
    ay = 852
    d.rectangle([m, ay, W - m, ay + 108], fill=NAVY)
    d.text((m + 20, ay + 12), "ALSO TODAY",
           font=font(SANS_B, 17), fill=(214, 200, 150))
    y = ay + 38
    for item in ALSO:
        d.text((m + 20, y), "•", font=font(SANS_B, 16), fill=(214, 200, 150))
        y = text_block(d, m + 42, y, item, font(SANS, 15), (245, 242, 234),
                       W - 2 * m - 62, leading=19)
        y += 2

    # ---- footer
    d.text((m, 976), "All events happened or were first reported on Thursday 26 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((W - m - 210, 976), "THE WORLD IN ONE PAGE",
           font=font(SANS_B, 14), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
