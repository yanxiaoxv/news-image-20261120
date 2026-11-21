#!/usr/bin/env python3
"""THE WORLD TODAY - Friday 20 November 2026.

Entry for the make.fun news-image-20261120 competition: a single image
that summarises one day's world news, drawn entirely in code with
Pillow. No photographs, no network access, fully deterministic.

How this file works
-------------------
This one file holds both halves of the entry:

* the drawing program - data tables (NUMBERS, CARDS, BRIEFS, MAP_ROWS),
  a set of small hand-drawn icons, and render(), which builds the
  1024x768 PNG from scratch; and

* the competition entrypoint. Run with no arguments, it takes the
  bundled entry.png beside this file, validates it (PNG signature,
  at most 1 MiB, at most 1024x1024 pixels) and copies it to
  /output/entry.png, creating /output when needed. If /output is not
  writable it falls back to ./output/entry.png and then to ./entry.png
  in the current directory.

Run with --render to regenerate entry.png from the code instead:

    python3 main.py            # validate + copy the bundled image
    python3 main.py --render   # rebuild entry.png deterministically
"""

import math
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

W, H = 1024, 768
PAPER = (246, 241, 227)
INK = (20, 33, 61)
BODY = (58, 58, 54)
FAINT = (133, 126, 108)
CARD_BG = (255, 254, 248)
CARD_EDGE = (216, 210, 192)
RED = (193, 39, 45)
WHITE = (255, 255, 255)
MAP_DOT = (157, 184, 200)

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_PNG = os.path.join(HERE, "entry.png")

# ----------------------------------------------------------------- fonts

_FONT_FILES = {
    "serif": ("LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"),
    "sans": ("LiberationSans-Regular.ttf", "DejaVuSans.ttf"),
    "bold": ("LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"),
}
_FONT_DIRS = ("/usr/share/fonts/truetype/liberation",
              "/usr/share/fonts/truetype/dejavu")
_font_cache = {}


def font(kind, size):
    """Load a truetype font by family kind and size, with caching."""
    key = (kind, size)
    if key not in _font_cache:
        names = _FONT_FILES[kind]
        path = None
        for directory in _FONT_DIRS:
            for name in names:
                candidate = os.path.join(directory, name)
                if os.path.exists(candidate):
                    path = candidate
                    break
            if path:
                break
        if path is None:
            raise FileNotFoundError("no font file found for %r" % (kind,))
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]

# ------------------------------------------------------------------ data

NUMBERS = [
    ("-5.1%", "Nikkei 225's Friday fall at the close, its fifth-biggest point drop - Reuters"),
    ("$92.57", "Brent crude's Friday settlement, up 0.6% on the day - Reuters"),
    ("35%", "Electricity's share of world energy that COP31's draft targets by 2035 - Reuters"),
    ("65,000", "Approved tents still awaiting entry into Gaza as winter nears - UN via Scoop"),
    ("879,868", "Advanced AI chips in US approvals for Chinese firms, newly disclosed - IANS"),
    ("118", "Glenn Phillips's century for New Zealand against India at Wellington - Reuters"),
]

# (kicker, tag, headline, detail, icon, accent, pin (col, row) or None)
CARDS = [
    ("KYIV - UKRAINE WAR", "CONFIRMED - KYIV POST",
     "Russia pounds Kyiv with ballistic missiles",
     "Explosions and fires in three districts before dawn on Friday; homes and an infrastructure site were hit.",
     "missile", (179, 57, 46), (34, 3)),
    ("ANTALYA - COP31 ENDGAME", "NO DEAL YET - HURRIYET / AFP",
     "COP31 talks extended as no deal is reached on Friday",
     "Kurum adjourns Friday's plenary with finance and fossil fuels unresolved; a third draft is due Saturday.",
     "leaf", (46, 125, 79), (31, 6)),
    ("ASIA - MARKETS ON FRIDAY", "DATA - REUTERS",
     "Asia slides as AI rout ends in worst week since 2020",
     "Nikkei closes 5.1% down, Kospi 5.2%, Taiex down 6.6%. Wall Street follows: S&P 500 -3.7%, Nasdaq -5.3% on Friday.",
     "chart", (36, 80, 126), (56, 5)),
    ("RIYADH - ENERGY", "DATA - REUTERS",
     "Oil edges higher after Houthi missiles target Riyadh",
     "Brent settles at $92.57 on Friday, up 0.6% on the day; Hormuz tanker scares keep supply fears alive.",
     "flame", (201, 106, 30), (38, 9)),
    ("WASHINGTON - SUMMIT FALLOUT", "CONFIRMED - AFP",
     "Trump defends Xi-Putin summit at White House",
     "He calls the trip 'momentous', touts $17bn in deals and says Putin wants the war ended by diplomacy.",
     "globe", (31, 122, 114), None),
    ("WASHINGTON - TECH CONTROLS", "REPORTED - IANS",
     "US approved 879,868 AI chips for Chinese firms, records show",
     "House Foreign Affairs Committee records prompt demands for public hearings on export controls.",
     "chip", (106, 74, 158), (11, 4)),
    ("SEOUL - COURTS", "CONFIRMED - REUTERS",
     "Appeals court upholds Kakao founder's acquittal",
     "Kim Beom-su is cleared again over SM Entertainment share charges; prosecutors' appeal is rejected.",
     "scales", (138, 109, 59), (54, 4)),
    ("MOGADISHU - DIPLOMACY", "REPORTED - BANGKOK POST",
     "Somalia expels UAE ambassador, alleging interference",
     "The envoy is ordered out in a sharp public rift between Mogadishu and Abu Dhabi, the paper reports.",
     "plane", (91, 107, 124), (38, 11)),
    ("GAZA - AID AND RETURN", "CONFIRMED - SCOOP",
     "Gazans return home as Israel ends rare ground operation",
     "Families go back after the army pulls out; some 65,000 approved tents still await entry before winter.",
     "tent", (107, 125, 42), (35, 8)),
    ("BRUSSELS - EU-UK RESET", "REPORTED - BANGKOK POST",
     "EU and UK eye a 'reset' deal at Brussels summit",
     "Both sides gather at Burnham's Brussels summit to patch up ties years after the Brexit divorce.",
     "stars", (43, 94, 167), (28, 2)),
    ("EUROPE - COST OF LIVING", "REPORTED - BANGKOK POST",
     "Europe's protesters join forces over costs and militarisation",
     "Movements in several countries coordinate; Stiglitz says Europe's young are right to be worried.",
     "sign", (160, 61, 99), (27, 4)),
    ("SILICON VALLEY - BIG TECH", "REPORTED - BANGKOK POST",
     "Meta 'reevaluating' 2030 net-zero target amid AI buildout",
     "The Facebook owner signals its climate pledge may bend as data-centre demand for power surges.",
     "cloud", (84, 110, 122), None),
    ("UNITED STATES - ENVIRONMENT", "REPORTED - BANGKOK POST",
     "US auctions first deep-sea mining leases, despite court ruling",
     "The first-ever sale goes ahead, setting up a fresh legal fight over seabed minerals and ocean life.",
     "waves", (23, 112, 126), None),
    ("WORLDWIDE - HEALTH", "REPORT - UN NEWS",
     "UN: patients running out of options as antibiotics fail",
     "Common infections grow harder to treat as resistance spreads, the UN warns in a report out Friday.",
     "pill", (176, 58, 72), None),
    ("WELLINGTON - CRICKET", "CONFIRMED - REUTERS",
     "Phillips hits 118 as New Zealand reach 317-6",
     "His second Test century, with Nicholls unbeaten on 146, puts the hosts on top at lunch on day two.",
     "cricket", (47, 107, 58), (61, 16)),
]

BRIEFS = [
    (16, "UN survey: digital government advances, but divides persist (UN)"),
    (17, "UN expert hails ICJ Myanmar verdict: 'called by its true name' (UN)"),
    (18, "Trump says he is too busy to meet North Korea's Kim again (AFP)"),
    (19, "Latin oil shares fall: Petrobras -1.7%, YPF -2.9% (Rio Times)"),
    (20, "Kamala Harris meets President Macron in Paris (Le Monde)"),
    (21, "Spain's prime minister admits 'mistakes' in election debate (AP)"),
    (22, "Storms soak Florida's Space Coast; people and horses rescued (AP)"),
    (23, "Pochettino calls for 'love' in first address as Man Utd coach (MyKhel)"),
    (24, "Marathon champion Jepchirchir banned three years over EPO (MyKhel)"),
    (25, "Rakshitha stuns Olympic champion Chen Yufei in Hong Kong (MyKhel)"),
    (26, "Fiona the hippo dies after swallowing a hat (Bangkok Post)"),
    (27, "Japan's Takaichi seeks 'constructive' ties with China (Manila Times)"),
]

MAP_ROWS = [
    "                                                                ",
    "        ####      ##                                            ",
    "     #########  ####        ############## ######               ",
    "    ##########   ##       #######################  ##           ",
    "     ########            #####  ################   ####  ###    ",
    "      ######              ###   ##############      ########    ",
    "       ####    #           ##    ##########          ######     ",
    "       #####  ###               ########             ####       ",
    "        ########                 ######              ##         ",
    "         ######                   ####     ##                   ",
    "          ####                    ## ##   ####                  ",
    "          ###                      #####  ######    ##          ",
    "          ##                        ###    ####    ####         ",
    "          #                                   ##   ######       ",
    "                                                        ##      ",
    "                                                         #  ##  ",
    "                                                            ##  ",
    "                                                                ",
]

FOOTER = ("Sources: Reuters - AP - AFP - CNA - UN News - APEC - Kyiv Post - "
          "Bangkok Post - IANS - full sourcing in the README. Drawn entirely "
          "in code; no photographs.")

# ----------------------------------------------------------- text layout

def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with draw.textlength.

    Words are split on whitespace. A word that is wider than the line
    on its own is kept whole on its own line rather than broken.
    """
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if current and draw.textlength(trial, font=fnt) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def fit(draw, text, fnt, width, max_lines):
    """Wrap text to at most max_lines lines, ellipsising the last one."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "...", font=fnt) > width:
        last = last[:-1].rstrip()
    lines[-1] = last + "..."
    return lines

# ----------------------------------------------------------------- icons
# Each icon draws into a 46x46 box whose top-left corner is (x, y).
# c is the card's accent colour.

def icon_missile(d, x, y, c):
    d.polygon([(x + 34, y + 3), (x + 40, y + 9), (x + 24, y + 27), (x + 17, y + 20)], fill=c)
    d.polygon([(x + 17, y + 20), (x + 10, y + 19), (x + 15, y + 26)], fill=INK)
    d.polygon([(x + 24, y + 27), (x + 25, y + 34), (x + 18, y + 29)], fill=INK)
    d.polygon([(x + 19, y + 28), (x + 9, y + 40), (x + 13, y + 41), (x + 21, y + 33)], fill=(230, 126, 34))
    d.line([(x + 10, y + 42), (x + 4, y + 45)], fill=(230, 126, 34), width=2)


def icon_leaf(d, x, y, c):
    d.ellipse([x + 8, y + 6, x + 40, y + 34], fill=c)
    d.polygon([(x + 8, y + 34), (x + 20, y + 40), (x + 10, y + 44)], fill=c)
    d.line([(x + 12, y + 40), (x + 36, y + 10)], fill=PAPER, width=2)
    d.line([(x + 20, y + 28), (x + 28, y + 27)], fill=PAPER, width=1)
    d.line([(x + 25, y + 21), (x + 33, y + 20)], fill=PAPER, width=1)


def icon_chart(d, x, y, c):
    d.line([(x + 5, y + 5), (x + 5, y + 40)], fill=INK, width=2)
    d.line([(x + 5, y + 40), (x + 42, y + 40)], fill=INK, width=2)
    d.line([(x + 8, y + 12), (x + 17, y + 18), (x + 25, y + 15), (x + 33, y + 26), (x + 41, y + 33)], fill=c, width=3)
    d.polygon([(x + 41, y + 33), (x + 33, y + 32), (x + 39, y + 25)], fill=c)


def icon_flame(d, x, y, c):
    d.polygon([(x + 23, y + 3), (x + 33, y + 20), (x + 35, y + 30), (x + 30, y + 40),
               (x + 16, y + 40), (x + 11, y + 30), (x + 14, y + 18)], fill=c)
    d.ellipse([x + 17, y + 26, x + 29, y + 42], fill=(246, 190, 60))


def icon_globe(d, x, y, c):
    d.ellipse([x + 4, y + 4, x + 42, y + 42], outline=c, width=3)
    d.ellipse([x + 15, y + 4, x + 31, y + 42], outline=c, width=1)
    d.line([(x + 4, y + 23), (x + 42, y + 23)], fill=c, width=1)
    d.line([(x + 23, y + 4), (x + 23, y + 42)], fill=c, width=1)


def icon_chip(d, x, y, c):
    d.rectangle([x + 12, y + 12, x + 34, y + 34], outline=c, width=3)
    d.rectangle([x + 19, y + 19, x + 27, y + 27], fill=c)
    for i in range(3):
        px = x + 16 + i * 7
        d.line([(px, y + 4), (px, y + 12)], fill=c, width=2)
        d.line([(px, y + 34), (px, y + 42)], fill=c, width=2)
        py = y + 16 + i * 7
        d.line([(x + 4, py), (x + 12, py)], fill=c, width=2)
        d.line([(x + 34, py), (x + 42, py)], fill=c, width=2)


def icon_scales(d, x, y, c):
    d.line([(x + 23, y + 6), (x + 23, y + 38)], fill=INK, width=3)
    d.line([(x + 7, y + 10), (x + 39, y + 10)], fill=INK, width=3)
    d.rectangle([x + 14, y + 40, x + 32, y + 43], fill=INK)
    # The two pans hang at fixed canvas x positions (10 and 36), not at
    # box-relative ones: the left pan spilling past the card's left edge
    # is part of the approved final image, so it is kept as drawn.
    for cx in (10, 36):
        d.line([(cx, y + 10), (cx - 6, y + 25)], fill=c, width=2)
        d.line([(cx, y + 10), (cx + 6, y + 25)], fill=c, width=2)
        d.pieslice([cx - 8, y + 18, cx + 8, y + 32], 0, 180, fill=c)


def icon_plane(d, x, y, c):
    d.polygon([(x + 4, y + 22), (x + 42, y + 6), (x + 30, y + 40), (x + 22, y + 30)], fill=c)
    d.line([(x + 22, y + 30), (x + 42, y + 6)], fill=INK, width=1)
    d.line([(x + 6, y + 42), (x + 16, y + 42)], fill=INK, width=2)


def icon_tent(d, x, y, c):
    d.polygon([(x + 23, y + 6), (x + 43, y + 38), (x + 3, y + 38)], outline=c, width=3)
    d.polygon([(x + 23, y + 20), (x + 31, y + 38), (x + 15, y + 38)], fill=c)
    d.line([(x + 2, y + 42), (x + 44, y + 42)], fill=INK, width=2)


def icon_stars(d, x, y, c):
    for i in range(8):
        ang = 2 * math.pi * i / 8
        cx = x + 23 + 14 * math.cos(ang)
        cy = y + 21 + 14 * math.sin(ang)
        d.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=(232, 178, 32))
    d.text((x + 23, y + 22), "E", font=font("bold", 17), fill=c, anchor="mm")


def icon_sign(d, x, y, c):
    d.rectangle([x + 8, y + 5, x + 38, y + 25], fill=c)
    d.line([(x + 12, y + 12), (x + 34, y + 12)], fill=PAPER, width=2)
    d.line([(x + 12, y + 18), (x + 29, y + 18)], fill=PAPER, width=2)
    d.line([(x + 23, y + 25), (x + 23, y + 42)], fill=INK, width=3)


def icon_cloud(d, x, y, c):
    d.ellipse([x + 6, y + 12, x + 26, y + 30], fill=c)
    d.ellipse([x + 18, y + 6, x + 40, y + 28], fill=c)
    d.rectangle([x + 8, y + 20, x + 38, y + 29], fill=c)
    d.polygon([(x + 25, y + 26), (x + 19, y + 38), (x + 24, y + 38), (x + 21, y + 45),
               (x + 30, y + 33), (x + 25, y + 33)], fill=(232, 178, 32))


def icon_waves(d, x, y, c):
    for yy in (12, 21, 30):
        for i in range(3):
            d.arc([x + 3 + i * 14, y + yy - 5, x + 15 + i * 14, y + yy + 5], 180, 360, fill=c, width=2)
    d.line([(x + 23, y + 34), (x + 23, y + 42)], fill=INK, width=2)
    d.polygon([(x + 19, y + 40), (x + 27, y + 40), (x + 23, y + 45)], fill=INK)


def icon_pill(d, x, y, c):
    d.rounded_rectangle([x + 5, y + 14, x + 41, y + 30], radius=8, outline=c, width=3)
    d.rounded_rectangle([x + 5, y + 14, x + 23, y + 30], radius=8, fill=c)
    d.rectangle([x + 15, y + 15, x + 23, y + 29], fill=c)
    for cx, cy in ((36, 8), (10, 40), (38, 40)):
        d.ellipse([x + cx - 3, y + cy - 3, x + cx + 3, y + cy + 3], outline=c, width=2)


def icon_cricket(d, x, y, c):
    d.polygon([(x + 8, y + 6), (x + 17, y + 3), (x + 26, y + 22), (x + 24, y + 34),
               (x + 15, y + 36), (x + 12, y + 24)], fill=(196, 154, 92), outline=INK, width=1)
    d.line([(x + 12, y + 30), (x + 8, y + 42)], fill=INK, width=3)
    d.ellipse([x + 28, y + 28, x + 42, y + 42], fill=c)
    d.arc([x + 31, y + 29, x + 39, y + 41], 90, 270, fill=PAPER, width=1)


ICONS = {
    "missile": icon_missile,
    "leaf": icon_leaf,
    "chart": icon_chart,
    "flame": icon_flame,
    "globe": icon_globe,
    "chip": icon_chip,
    "scales": icon_scales,
    "plane": icon_plane,
    "tent": icon_tent,
    "stars": icon_stars,
    "sign": icon_sign,
    "cloud": icon_cloud,
    "waves": icon_waves,
    "pill": icon_pill,
    "cricket": icon_cricket,
}

# --------------------------------------------------------------- drawing

def draw_masthead(d):
    d.text((14, 4), "THE WORLD TODAY", font=font("serif", 43), fill=INK)
    d.rounded_rectangle([748, 10, 1010, 38], radius=14, fill=RED)
    d.text((879, 24), "FRIDAY - 20 NOV 2026", font=font("bold", 16), fill=WHITE, anchor="mm")
    d.text((1010, 44), "ONE IMAGE - THE WHOLE DAY'S NEWS", font=font("bold", 10), fill=BODY, anchor="ra")
    d.rectangle([14, 60, 1010, 63], fill=RED)


def draw_numbers(d):
    d.text((14, 69), "THE DAY IN NUMBERS", font=font("bold", 11), fill=RED)
    col_w = 996 / 6
    for i, (big, cap) in enumerate(NUMBERS):
        cx = 14 + i * col_w
        if i > 0:
            d.line([(cx - 5, 88), (cx - 5, 126)], fill=CARD_EDGE, width=1)
        d.text((cx, 84), big, font=font("bold", 26), fill=INK)
        lines = fit(d, cap, font("sans", 9), col_w - 12, 3)
        for j, line in enumerate(lines):
            d.text((cx, 114 + j * 11), line, font=font("sans", 9), fill=BODY)
    d.line([(14, 150), (1010, 150)], fill=FAINT, width=1)


def draw_card(d, x, y, index, card):
    kicker, tag, headline, detail, icon, accent, _pin = card
    w, h = 328, 91
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_EDGE)
    d.rectangle([x, y, x + w, y + 3], fill=accent)
    d.rectangle([x + 6, y + 7, x + 25, y + 26], fill=RED)
    d.text((x + 15.5, y + 16.5), str(index + 1), font=font("bold", 12), fill=WHITE, anchor="mm")
    d.text((x + 31, y + 9), kicker, font=font("bold", 9), fill=accent)
    tag_font = font("bold", 7)
    tw = d.textlength(tag, font=tag_font)
    tx = x + w - 6 - tw
    d.rectangle([tx - 5, y + 7, x + w - 6, y + 20], outline=accent)
    d.text((tx, y + 9), tag, font=tag_font, fill=accent)
    ICONS[icon](d, x + 5, y + 36, accent)
    x0 = x + 58
    head_lines = fit(d, headline, font("bold", 14), 262, 2)
    yy = y + 31
    for line in head_lines:
        d.text((x0, yy), line, font=font("bold", 14), fill=INK)
        yy += 17
    detail_lines = fit(d, detail, font("sans", 9), 262, 3 if len(head_lines) == 1 else 2)
    dy = yy + 1
    for line in detail_lines:
        d.text((x0, dy), line, font=font("sans", 9), fill=BODY)
        dy += 12


def draw_cards(d):
    gx, gy = 14, 157
    for i, card in enumerate(CARDS):
        draw_card(d, gx + (i % 3) * 333, gy + (i // 3) * 96, i, card)


def draw_bottom(d):
    by = 640
    d.text((14, by), "WHERE IT HAPPENED", font=font("bold", 10), fill=RED)
    d.text((14, by + 13), "5 = WASHINGTON (SEE 6) - 12 = CALIFORNIA - 13 = USA - 14 = WORLDWIDE (OFF THE MAP)",
           font=font("sans", 7), fill=FAINT)
    x0, y0 = 18, by + 26
    cell_w, cell_h = 5.05, 3.55
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                d.ellipse([x0 + c * cell_w, y0 + r * cell_h,
                           x0 + c * cell_w + 2.4, y0 + r * cell_h + 2.4], fill=MAP_DOT)
    for i, card in enumerate(CARDS):
        pin = card[6]
        if pin is None:
            continue
        col, row = pin
        cx = x0 + col * cell_w + 1
        cy = y0 + row * cell_h + 1
        d.ellipse([cx - 5.5, cy - 5.5, cx + 5.5, cy + 5.5], fill=RED)
        d.text((cx, cy - 0.5), str(i + 1), font=font("bold", 7 if i + 1 < 10 else 6),
               fill=WHITE, anchor="mm")


def draw_briefs(d):
    bx = 366
    d.text((bx, 640), "ALSO ON 20 NOVEMBER", font=font("bold", 10), fill=RED)
    d.text((1010, 641), "THE REST OF THE DAY, IN ONE LINE EACH", font=font("sans", 8), fill=FAINT, anchor="ra")
    col2_w = (1010 - 366 - 14) / 2
    for j, (num, text) in enumerate(BRIEFS):
        cx = bx + (j // 6) * (col2_w + 14)
        cy = 640 + 20 + (j % 6) * 15
        d.text((cx, cy), str(num), font=font("bold", 9), fill=RED)
        lines = fit(d, text, font("sans", 9), col2_w - 20, 1)
        for line in lines:
            d.text((cx + 19, cy), line, font=font("sans", 9), fill=BODY)


def render(path=ENTRY_PNG):
    """Build the image from the data tables and save it as a PNG."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_cards(d)
    draw_bottom(d)
    draw_briefs(d)
    d.text((14, 756), FOOTER, font=font("sans", 7), fill=FAINT)
    img.save(path, optimize=True)
    return path

# ------------------------------------------------------------- entrypoint

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB
MAX_SIDE = 1024


def validate(path):
    """Check the bundled PNG against the competition's limits."""
    with open(path, "rb") as fh:
        head = fh.read(8)
    if head != PNG_SIGNATURE:
        raise ValueError("%s is not a PNG file" % path)
    if os.path.getsize(path) > MAX_BYTES:
        raise ValueError("%s is larger than 1 MiB" % path)
    with Image.open(path) as img:
        if img.width > MAX_SIDE or img.height > MAX_SIDE:
            raise ValueError("%s is larger than 1024x1024" % path)


def deliver():
    """Validate the bundled entry.png and copy it to the output path."""
    validate(ENTRY_PNG)
    try:
        os.makedirs("/output", exist_ok=True)
        target = "/output/entry.png"
        shutil.copyfile(ENTRY_PNG, target)
        return target
    except OSError:
        pass
    try:
        os.makedirs("./output", exist_ok=True)
        target = "./output/entry.png"
        shutil.copyfile(ENTRY_PNG, target)
        return target
    except OSError:
        target = "./entry.png"
        shutil.copyfile(ENTRY_PNG, target)
        return target


def main(argv):
    if "--render" in argv:
        render()
        print("rendered %s" % ENTRY_PNG)
        return 0
    target = deliver()
    print("wrote %s" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
