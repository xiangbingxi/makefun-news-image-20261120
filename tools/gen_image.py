#!/usr/bin/env python3
"""Render the front page for Friday 20 November 2026 as one 1024x1024 PNG.

Own work: every story below was checked against reporting published on
20 November 2026 (see NEWS.md for the source of each line). The drawing is
done with PIL primitives only -- no photos, no downloaded art, no network.
Deterministic: a fixed seed drives the paper texture and the hand-drawn
wobble, so repeated runs produce identical bytes.

Run:  python3 tools/gen_image.py   (writes entry.png next to main.ts)
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 25, 20)
FAINT = (90, 86, 74)
RED = (178, 34, 24)
BLUE = (31, 78, 121)
GREEN = (46, 110, 62)
AMBER = (176, 112, 8)
RIVER = (58, 110, 140)
ORANGE = (198, 84, 24)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words, lines, cur = text.split(), [], ""
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


def wobbly(draw, pts, color, width=2, seed=7, amp=1.6):
    """A polyline with a slight hand-drawn wobble (seeded, deterministic)."""
    rnd = random.Random(seed)
    j = [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in pts]
    draw.line(j, fill=color, width=width, joint="curve")


def burst(draw, cx, cy, r, color, seed=3, spikes=11):
    """Jagged explosion starburst."""
    rnd = random.Random(seed)
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rr = r if i % 2 == 0 else r * (0.35 + rnd.random() * 0.25)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color, outline=INK)


# ---------------------------------------------------------------- stories
# (tag, headline, one-line summary, source) -- featured four are drawn big.
LEAD = (
    "UKRAINE",
    "Missiles smash three Kyiv bridges",
    "Russian ballistic missiles hit three Dnipro crossings in the biggest bridge "
    "attack of the war. Six were killed in Kyiv and eight across Ukraine; a "
    "Kharkiv emergency hospital was hit too.",
    "Reuters / BBC / Ukrainska Pravda",
)
CARDS = [
    (
        "INDIA",
        "Cyclone Akvan slams India's east coast",
        "Landfall near Gopalpur, Odisha, winds over 90 km/h. Over 300,000 evacuated; "
        "India's third cyclone in under a month.",
        "Reuters",
        "cyclone",
    ),
    (
        "MARKETS",
        "Asia's AI sell-off deepens",
        "Nikkei -5.1%, Taiwan -6.3%, Kospi -5.2% as the AI rally unravels. Anthropic's "
        "record $81bn debut (+17%) could not stop the rout.",
        "Bloomberg / CNBC",
        "chart",
    ),
    (
        "CLIMATE",
        "COP31 ends in deadlock",
        "Draft drops any fossil-fuel phase-out and the $120bn adaptation fund; "
        "talks spill into overtime.",
        "Reuters / CNA / UN News",
        "globe",
    ),
]
# The remaining 32 stories, in the order they appear in the numbered index.
# (tag, headline, source) -- headlines are written to stand alone.
INDEX = [
    ("UKRAINE", "Kharkiv hospital hit as drones strike city", "Ukrainska Pravda"),
    ("UKRAINE", "Kyiv strikes Crimean Bridge for a second day", "Reuters"),
    ("SAUDI ARABIA", "Houthi missile damages Riyadh's tallest tower", "Reuters"),
    ("GULF", "Tanker hit in Strait of Hormuz; two burning", "Reuters"),
    ("YEMEN", "Coalition hits Houthi sites in Sanaa and Taiz", "Arab News"),
    ("IRAQ", "Handover begins in militia stronghold", "Arab News"),
    ("HAITI", "Police kill 34 suspected gang members", "ARN News Centre"),
    ("VENEZUELA", "US and Venezuela sign military deal", "OneTurn"),
    ("GEORGIA", "Russia and Georgia talk again in Minsk", "Reuters"),
    ("MIDDLE EAST", "US carrier Roosevelt sent to the region", "Business Insider"),
    ("CHINA-US", "Maritime safety talks held in Shanghai", "Reuters"),
    ("THE HAGUE", "World court: Myanmar committed genocide", "OneTurn / ARN"),
    ("CHINA", "Trump, Xi and Putin meet in Shenzhen", "OneTurn"),
    ("UK-EU", "Landmark post-Brexit 'reset' deal", "Arab News / BBC"),
    ("TRADE", "US-China truce will not be extended", "USTR"),
    ("EL SALVADOR", "Bukele moves towards a third term", "NPR"),
    ("SOUTH KOREA", "Ex-PM Han's sentence overturned", "DW"),
    ("SPAIN", "Lula in Madrid before snap election", "Euronews"),
    ("NIGERIA", "Jail terms for suicide attempt to end", "BBC"),
    ("TUNISIA", "Rights defender jailed for five years", "Amnesty Intl"),
    ("PALESTINE", "King Charles sends historic message", "Arab News"),
    ("GREENLAND", "Denmark ratifies Trump Greenland deal", "ARN News Centre"),
    ("MALAYSIA", "10,000 Rohingya to be resettled", "Reuters"),
    ("ECONOMY", "IMF: public debt nears 100% of GDP", "Morning Briefing"),
    ("SRI LANKA", "Rates rise to 9% in Sri Lanka", "Global Map News"),
    ("KENYA", "US wins $60bn rare-earth project", "Business in Africa"),
    ("GUINEA", "Guinea now No. 3 iron-ore exporter", "Business Insider"),
    ("TECH", "Gemini can now drive a Mac", "Rorise"),
    ("TECH", "Italy fines Meta 805m euros", "Morning Briefing"),
    ("CULTURE", "GTA 6 tops $2.3bn in launch sales", "OneTurn"),
    ("FIJI", "Drought disaster declared in Fiji", "FBC"),
    ("USA", "Magnitude 5.0 quake in California", "BriefWire"),
]
# Big numbers for the strip between the cards and the index.
NUMBERS = [
    ("100+", "missiles and 400+\ndrones fired at Ukraine"),
    ("300,000", "evacuated ahead\nof Cyclone Akvan"),
    ("-5.1%", "Nikkei's fall\nin one day"),
    ("$81bn", "Anthropic's\nrecord IPO"),
    ("$120bn", "adaptation fund\ncut from COP31 draft"),
    ("100,000", "youth visas a year\nin the UK-EU deal"),
]

# ---------------------------------------------------------------- drawing
def draw_kyiv(draw, x, y, w, h):
    """Hand-drawn Kyiv: skyline, the Dnipro, three bridges, one broken."""
    draw.rectangle([x, y, x + w, y + h], fill=(223, 232, 238), outline=INK, width=2)
    # skyline blocks
    rnd = random.Random(11)
    bx = x + 12
    while bx < x + w - 40:
        bw, bh = rnd.randint(22, 46), rnd.randint(26, 62)
        draw.rectangle([bx, y + h - 78 - bh, bx + bw, y + h - 78], fill=(70, 84, 96), outline=INK)
        bx += bw + 6
    # river band
    draw.rectangle([x, y + h - 78, x + w, y + h], fill=RIVER, outline=INK)
    for i in range(5):  # current ripples
        rx = x + 20 + i * 68
        draw.arc([rx, y + h - 58, rx + 44, y + h - 40], 200, 340, fill=(255, 255, 255), width=2)
    # three bridges: arches over the river
    for i, bx0 in enumerate((x + 18, x + 138, x + 258)):
        bw = 104
        by = y + h - 118
        if i == 1:  # the broken middle bridge
            draw.arc([bx0, by, bx0 + bw, by + 78], 180, 270, fill=INK, width=4)
            draw.line([bx0 + 52, by + 2, bx0 + 66, by + 34], fill=INK, width=4)
            draw.line([bx0 + 66, by + 34, bx0 + 58, by + 62], fill=INK, width=3)
        else:
            draw.arc([bx0, by, bx0 + bw, by + 78], 180, 360, fill=INK, width=4)
            draw.line([bx0, by + 38, bx0 + bw, by + 38], fill=INK, width=4)
        for px in range(bx0 + 8, bx0 + bw - 4, 16):
            draw.line([px, by + 38, px, by + 52], fill=INK, width=2)
    burst(draw, x + 90, y + 58, 24, ORANGE, seed=5)
    burst(draw, x + 90, y + 58, 12, (240, 200, 60), seed=6, spikes=7)
    burst(draw, x + 320, y + 72, 16, ORANGE, seed=9)
    # smoke curls
    for sx, sy, sr in ((x + 116, y + 44, 9), (x + 130, y + 32, 12), (x + 302, y + 58, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=(90, 90, 90), width=2)
    draw.text((x + 10, y + 6), "KYIV, UKRAINE \u2014 THE DNIPRO, AT DAWN",
              font=font(SANS_B, 12), fill=INK)


def draw_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 230, 238), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 + 2
    for k in range(6):  # spiral arms
        pts = []
        for t in range(0, 270, 6):
            a = math.radians(t + k * 60)
            r = 6 + t * 0.12
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.85))
        draw.line(pts, fill=BLUE, width=3)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=INK)
    for i in range(7):  # rain slashes, kept to the right of the label
        rx = x + 176 + i * 18
        draw.line([rx, y + 10, rx - 8, y + 30], fill=BLUE, width=2)
    draw.text((x + 10, y + 6), "BAY OF BENGAL", font=font(SANS_B, 11), fill=BLUE)


def draw_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 244, 238), outline=INK, width=2)
    draw.line([x + 22, y + 12, x + 22, y + h - 18], fill=INK, width=2)
    draw.line([x + 22, y + h - 18, x + w - 10, y + h - 18], fill=INK, width=2)
    for i in range(4):  # gridlines
        gy = y + 16 + i * 18
        draw.line([x + 22, gy, x + w - 10, gy], fill=(220, 210, 196), width=1)
    pts = [(x + 28, y + 22), (x + 70, y + 30), (x + 112, y + 26), (x + 154, y + 44),
           (x + 196, y + 52), (x + 238, y + 70), (x + 278, y + 84)]
    wobbly(draw, pts, RED, width=4, seed=21)
    draw.polygon([(x + 278, y + 84), (x + 268, y + 76), (x + 270, y + 90)], fill=RED)
    draw.text((x + 30, y + 8), "NIKKEI -5.1%   TAIWAN -6.3%   KOSPI -5.2%",
              font=font(SANS_B, 11), fill=RED)


def draw_globe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 236, 224), outline=INK, width=2)
    cx, cy, r = x + w // 2, y + h // 2 + 4, 38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 214, 232), outline=INK, width=2)
    for k in (-1, 0, 1):  # latitude lines
        ry = r * 0.55 if k else r * 0.12
        draw.arc([cx - r, cy - ry, cx + r, cy + ry], 0, 360, fill=BLUE, width=2)
    draw.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], 0, 360, fill=BLUE, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=GREEN, width=3)
    burst(draw, x + w - 34, y + 22, 15, (240, 200, 60), seed=31, spikes=8)
    draw.text((x + 10, y + 6), "ANTALYA, TURKIYE", font=font(SANS_B, 11), fill=GREEN)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rnd = random.Random(20261120)
    for _ in range(900):  # paper speckle
        d.point((rnd.randint(0, W - 1), rnd.randint(0, H - 1)), fill=(238, 232, 214))
    M = 28
    # ---- masthead
    d.line([M, 26, W - M, 26], fill=INK, width=3)
    d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.text((M, 106), "FRIDAY, 20 NOVEMBER 2026", font=font(SANS_B, 16), fill=INK)
    d.text((W // 2, 106), "ONE DAY  ·  ONE PAGE", font=font(SANS_B, 16),
           fill=INK, anchor="ma")
    d.text((W - M, 106), "36 STORIES  ·  7 REGIONS", font=font(SANS_B, 16),
           fill=INK, anchor="ra")
    d.line([M, 132, W - M, 132], fill=INK, width=2)
    d.line([M, 137, W - M, 137], fill=INK, width=5)
    # ---- lead story: text left, art right
    ly = 152
    d.text((M, ly), "LEAD STORY  —  UKRAINE", font=font(SANS_B, 14), fill=RED)
    head = font(SERIF_B, 46)
    for i, ln in enumerate(wrap(d, LEAD[1], head, 560)):
        d.text((M, ly + 24 + i * 50), ln, font=head, fill=INK)
    deck = font(SERIF, 17)
    dy = ly + 24 + 2 * 50 + 8
    for i, ln in enumerate(wrap(d, LEAD[2], deck, 560)):
        d.text((M, dy + i * 22), ln, font=deck, fill=INK)
    dy += len(wrap(d, LEAD[2], deck, 560)) * 22 + 6
    d.text((M, dy), "6 killed in Kyiv  ·  8 across Ukraine  ·  3 bridges shut",
           font=font(SANS_B, 14), fill=RED)
    d.text((M, dy + 22), "Source: " + LEAD[3], font=font(SANS_I, 12), fill=FAINT)
    draw_kyiv(d, 612, ly + 4, 384, 218)
    d.text((612, ly + 228), "Three Dnipro crossings hit overnight; traffic halted.",
           font=font(SERIF_I, 12), fill=FAINT)
    # ---- three illustrated cards
    cy = 392
    cw, gap = 312, 12
    for i, (tag, headl, summ, src, art) in enumerate(CARDS):
        x = M + i * (cw + gap)
        if art == "cyclone":
            draw_cyclone(d, x, cy, cw, 84)
        elif art == "chart":
            draw_chart(d, x, cy, cw, 84)
        else:
            draw_globe(d, x, cy, cw, 84)
        d.text((x, cy + 92), tag, font=font(SANS_B, 12), fill=RED)
        hf = font(SERIF_B, 19)
        hl = wrap(d, headl, hf, cw)
        for j, ln in enumerate(hl):
            d.text((x, cy + 110 + j * 22), ln, font=hf, fill=INK)
        sf = font(SANS, 12)
        sy = cy + 110 + len(hl) * 22 + 2
        sl = wrap(d, summ, sf, cw)
        for j, ln in enumerate(sl):
            d.text((x, sy + j * 15), ln, font=sf, fill=INK)
        d.text((x, sy + len(sl) * 15 + 4), "Source: " + src,
               font=font(SANS_I, 10), fill=FAINT)
    # ---- the day in numbers
    ny = 600
    d.line([M, ny, W - M, ny], fill=INK, width=2)
    nw = (W - 2 * M) // len(NUMBERS)
    for i, (big, cap) in enumerate(NUMBERS):
        x = M + i * nw
        d.text((x + nw // 2, ny + 6), big, font=font(SERIF_B, 24),
               fill=RED if i % 2 == 0 else INK, anchor="ma")
        for j, ln in enumerate(cap.split("\n")):
            d.text((x + nw // 2, ny + 34 + j * 12), ln, font=font(SANS, 11),
                   fill=FAINT, anchor="ma")
        if i:
            d.line([x, ny + 6, x, ny + 56], fill=(214, 206, 188), width=1)
    d.line([M, ny + 62, W - M, ny + 62], fill=INK, width=2)
    # ---- the day in 36 stories: four columns, tag + headline
    iy = 670
    d.text((M, iy), "THE DAY IN 36 STORIES", font=font(SERIF_B, 20), fill=INK)
    d.text((W - M, iy + 2), "Numbered in order of importance",
           font=font(SERIF_I, 12), fill=FAINT, anchor="ra")
    cols = 4
    colw = (W - 2 * M - (cols - 1) * 16) // cols
    per_col = 8
    top = iy + 28

    def rich_lines(segments, width):
        """Wrap (text, font) segments into lines of (text, font, fill) words."""
        words = []
        for text, fnt, fill in segments:
            for w in text.split(" "):
                words.append((w, fnt, fill))
        lines, cur, cur_w = [], [], 0
        for w, fnt, fill in words:
            ww = d.textlength(w + " ", font=fnt)
            if cur and cur_w + ww > width:
                lines.append(cur)
                cur, cur_w = [], 0
            cur.append((w, fnt, fill))
            cur_w += ww
        if cur:
            lines.append(cur)
        return lines

    for ci in range(cols):
        x = M + ci * (colw + 16)
        y = top
        for k, (tag, headl, src) in enumerate(INDEX[ci * per_col:(ci + 1) * per_col]):
            num = ci * per_col + k + 2  # the lead story is No. 1
            segs = [(f"{num}. {tag} \u2014 ", font(SANS_B, 11), BLUE),
                    (headl, font(SERIF_B, 13), INK)]
            for li, line in enumerate(rich_lines(segs, colw)):
                cx = x
                for w, fnt, fill in line:
                    d.text((cx, y + li * 15), w, font=fnt, fill=fill)
                    cx += d.textlength(w + " ", font=fnt)
            y += len(rich_lines(segs, colw)) * 15 + 5
        if ci < cols - 1:
            d.line([x + colw + 8, top, x + colw + 8, y], fill=(214, 206, 188), width=1)
    # ---- footer
    fy = 990
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    d.text((W // 2, fy + 7), "Sources: Reuters · BBC · Ukrainska Pravda · Arab News · CNA · Carbon Brief · UN News · "
           "Bloomberg · CNBC · NPR · DW · Euronews · Amnesty International · FBC · Business Insider · OneTurn · FXStreet · TechCrunch",
           font=font(SANS, 9), fill=FAINT, anchor="ma")
    d.text((W // 2, fy + 20), "Events of Friday 20 November 2026, as reported that day  ·  The World in One Day",
           font=font(SANS, 9), fill=FAINT, anchor="ma")
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
