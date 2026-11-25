#!/usr/bin/env python3
"""Draw the news image for make.fun news-image-20261125.

A one-page newspaper front page, 1024x1024, drawn entirely in code with
Pillow: masthead, stat strip, region tabs, 3 lead stories with drawn
illustrations, 10 more stories, a world map with numbered pins, a numbered
list of 22 more stories, and a date-check box. Every story was verified
against wire reporting read up to 01:30 UTC, Wednesday 25 November 2026
(see the DATE CHECK box in the image).

Deterministic: fixed layout, fixed fonts, no randomness, no timestamps,
no network. The JPEG encoder (libjpeg via Pillow) is deterministic for
identical pixels and settings, so repeated runs are byte-identical.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (26, 42, 74)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GREY = (90, 90, 90)
LIGHTGREY = (210, 205, 190)
TEAL = (0, 110, 110)
GOLD = (180, 140, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, leading=None):
    """Draw lines of text; returns the y just below the last line."""
    x, y = xy
    lh = leading if leading is not None else int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, label, fill=RED):
    """Small white-on-colour tag; returns its width."""
    fnt = SANS_B(11)
    w = int(draw.textlength(label, font=fnt)) + 12
    draw.rectangle([x, y, x + w, y + 16], fill=fill)
    draw.text((x + 6, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def flame(draw, cx, base_y, s):
    """A stylised flame: orange outer, yellow inner."""
    draw.polygon(
        [(cx - s, base_y), (cx - s * 0.55, base_y - s * 1.5),
         (cx, base_y - s * 0.8), (cx + s * 0.5, base_y - s * 1.7),
         (cx + s, base_y)],
        fill=(230, 110, 20))
    draw.polygon(
        [(cx - s * 0.45, base_y), (cx - s * 0.2, base_y - s * 0.9),
         (cx + s * 0.35, base_y - s * 0.7), (cx + s * 0.45, base_y)],
        fill=(250, 200, 40))


def smoke(draw, cx, cy, r, fill=(120, 120, 120)):
    for dx, dy, rr in ((-r, 0, r), (0, -r, int(r * 1.1)), (r, -r // 2, r)):
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=fill)


# ---------------------------------------------------------------- stories
# (kicker, location line, headline, summary, source)
LEADS = [
    ("CIA: BREACHED", "1 LANGLEY, US \u00b7 CYBER",
     "CIA and spy chief's office hit by cyberattack",
     "CNN reports a breach at the CIA and the Director of National "
     "Intelligence touching classified systems \u2014 the latest in a run "
     "of US government hacks.",
     "CNN"),
    ("HUAWEI: GUILTY", "2 NEW YORK \u00b7 TECH TRIAL",
     "Huawei convicted of stealing trade secrets",
     "A US jury finds Huawei guilty on 10 of 12 counts, including bank "
     "fraud and conspiracy to steal trade secrets; racketeering dropped.",
     "US Justice Dept, FT"),
    ("RIYADH: STRUCK", "3 RIYADH, SAUDI ARABIA \u00b7 GULF WAR",
     "Houthi strike hits Riyadh tower; 11 hurt",
     "A drone hits a skyscraper in the financial district as Iran says "
     "three more tankers struck mines in the Strait of Hormuz.",
     "Reuters, Saudi Civil Defence"),
]

MEDIUMS = [
    ("SHIP SUNK", "BENGHAZI, LIBYA \u00b7 WAR AT SEA",
     "Ukraine sinks Russian warship off Libya",
     "Zelensky confirms a drone strike sank a Russian corvette in "
     "Benghazi harbour.", "Reuters"),
    ("700,000 DEAD", "KYIV \u00b7 UKRAINE WAR",
     "700,000 Russian soldiers killed, data show",
     "Leaked figures judged authentic put Russian dead past 700,000 "
     "in nearly five years of war.", "Mediazona"),
    ("EBOLA: 5,775 DEAD", "ITURI, DR CONGO \u00b7 HEALTH",
     "WHO pulls staff from Ebola hospital",
     "Health workers sheltered three days under fire in Akwe before "
     "being evacuated.", "WHO"),
    ("$132BN BACKLOG", "ROUND ROCK, US \u00b7 EARNINGS",
     "Dell smashes forecasts on AI servers",
     "EPS $9.45 vs $6.59 expected; AI server backlog $132.3bn; "
     "guidance raised.", "Dell, reports"),
    ("\u22125.9%", "NEW YORK \u00b7 MARKETS",
     "Nvidia slides as AI rally cools",
     "Nasdaq falls 1.48% after Monday's 6.5% surge; Dow tops 50,000 "
     "for the first time.", "Investopedia"),
    ("MEDAL OF FREEDOM", "WASHINGTON \u00b7 US POLITICS",
     "Trump honours Giuliani",
     "The ex-New York mayor is honoured at the White House.",
     "Washington Post"),
    ("TURKEYS SPARED", "WASHINGTON \u00b7 THANKSGIVING",
     "Trump pardons Freedom and Feathers",
     "The annual pardon goes ahead on the eve of Thanksgiving.",
     "Reuters"),
    ("PUNJAB PACT", "NEW DELHI \u00b7 INDIA POLITICS",
     "BJP and Akali Dal reunite for Punjab",
     "The two parties announce an alliance for the 2027 Punjab polls "
     "after six years apart.", "Jagran Josh"),
    ("NATO: ON WATCH", "BRUSSELS \u00b7 SECURITY",
     "NATO to send early-warning jets to Poland",
     "After missiles landed in Poland.",
     "Reports"),
    ("ENGLAND LEVEL", "MELBOURNE \u00b7 CRICKET",
     "England beat Australia in 2nd T20I",
     "England chase 185 to win by eight wickets and level the "
     "five-match series 1\u20131.", "Reports"),
]

# (number, text) — every item was reported on 24-25 November 2026.
MORE = [
    (14, "Israel: Iran developing chemical weapons, defence minister says (CBS)"),
    (15, "Gaza: Israeli strike kills Hamas security chief Naeem Abu Nahel"),
    (16, "US: Senate votes 51-48 against curbing Trump's Iran war powers"),
    (17, "Yemen: Houthis threaten Saudi ports over Hodeidah order"),
    (18, "Brussels: EU readies 22nd Russia sanctions package for 26-27 Nov"),
    (19, "US: Treasury sanctions Iranian shadow banks; rial hits record low"),
    (20, "Iran: Truck drivers strike over collapsing economy"),
    (21, "Venezuela: Hegseth signs US-Venezuela military pact"),
    (22, "Ecuador: US suspends joint ops after deadly raid abuse probe"),
    (23, "Markets: Anthropic shares fall below $83 IPO price"),
    (24, "Pharma: Sanofi to buy Insmed in biggest deal in three years"),
    (25, "Tech: OPPO launches Find X9 Ultra globally, first for Ultra line"),
    (26, "Tennis: Sinner has knee surgery in Turku after Wimbledon win"),
    (27, "Football: Man Utd fume at Yoro red card; Pochettino leads protest"),
    (28, "Football: Man City held by Napoli; Guardiola's pace questioned"),
    (29, "Nepal: India pledges \u20b915,000 crore aid after floods"),
    (30, "UK: Burnham orders panel on nuclear-test veterans' health"),
    (31, "UK: Ministers consult public on changing age of consent"),
    (32, "Iowa: Army to detonate lead azide; residents told to evacuate"),
    (33, "Gaming: GTA 6 soundtrack aims for Billboard No. 1 debut"),
    (34, "Climate: Strong El Ni\u00f1o to bring wet US winter, NOAA says"),
    (35, "Australia: PM's Prizes for Science honour top researchers"),
]

STATS = [
    ("10/12", "counts Huawei found guilty on"),
    ("700,000", "Russian soldiers killed in Ukraine"),
    ("5,775", "Ebola deaths in DR Congo"),
    ("$132.3bn", "Dell's AI server backlog"),
    ("11", "hurt in Riyadh tower strike"),
    ("50,000", "Dow Jones closes above, first time"),
]

REGIONS = [
    ("EUROPE", 9, (30, 80, 160)),
    ("MIDDLE EAST", 9, (178, 34, 34)),
    ("AMERICAS", 8, (0, 110, 110)),
    ("ASIA-PACIFIC", 6, (200, 130, 30)),
    ("AFRICA", 2, (110, 90, 160)),
    ("WORLD", 1, (100, 100, 100)),
]

# (lon, lat) of stories 1-13, for the map pins.
PINS = [
    (-77.1, 38.9), (-74.0, 40.7), (46.7, 24.7), (20.1, 32.1), (30.5, 50.4),
    (28.8, -1.7), (-96.8, 30.6), (-74.0, 40.7), (-74.0, 40.7), (77.2, 28.6),
    (4.4, 50.8), (144.9, -37.8), (46.7, 24.7),
]


# ------------------------------------------------------------- illustrations
def illo_cia(draw, x, y, w, h):
    """A dark operations room: screens, a padlock, red warning lights."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 40))
    # wall of screens
    for i, (sx, sw) in enumerate(((x + 14, 88), (x + 116, 88), (x + 218, 88))):
        draw.rectangle([sx, y + 14, sx + sw, y + 62], fill=(8, 40, 50),
                       outline=(60, 140, 160), width=1)
        for row in range(5):
            yy = y + 20 + row * 8
            draw.line([sx + 6, yy, sx + 6 + (60 - row * 9), yy],
                      fill=(90, 220, 180), width=2)
    # red alert banner on the middle screen
    draw.rectangle([x + 116, y + 14, x + 204, y + 30], fill=RED)
    draw.text((x + 122, y + 17), "BREACH", font=SANS_B(11),
              fill=(255, 255, 255))
    # padlock, centre bottom
    px, py = x + w // 2, y + 92
    draw.rectangle([px - 22, py - 6, px + 22, py + 20], fill=(200, 170, 60),
                   outline=(120, 100, 20), width=2)
    draw.arc([px - 14, py - 22, px + 14, py + 2], 180, 360,
             fill=(200, 170, 60), width=4)
    draw.ellipse([px - 3, py + 2, px + 3, py + 8], fill=(16, 24, 40))
    draw.rectangle([px - 1, py + 7, px + 1, py + 14], fill=(16, 24, 40))
    # blinking warning dots
    for dx in (x + 30, x + 290):
        draw.ellipse([dx - 4, y + 84, dx + 4, y + 92], fill=RED)


def illo_huawei(draw, x, y, w, h):
    """A courtroom: judge's bench, gavel, and a phone on the stand."""
    draw.rectangle([x, y, x + w, y + h], fill=(96, 78, 58))
    draw.rectangle([x, y, x + w, y + 34], fill=(60, 48, 36))
    # flags behind the bench
    draw.rectangle([x + 26, y + 8, x + 46, y + 34], fill=(178, 34, 34))
    draw.rectangle([x + 274, y + 8, x + 294, y + 34], fill=(30, 80, 160))
    # bench
    draw.rectangle([x + 20, y + 40, x + w - 20, y + 66], fill=(120, 72, 32))
    draw.rectangle([x + 20, y + 40, x + w - 20, y + 46], fill=(150, 100, 50))
    # gavel
    draw.rectangle([x + 130, y + 52, x + 190, y + 60], fill=(90, 55, 25))
    draw.rectangle([x + 150, y + 40, x + 170, y + 54], fill=(90, 55, 25))
    draw.rectangle([x + 148, y + 60, x + 172, y + 64], fill=(60, 35, 15))
    # phone on the stand, screen glowing
    draw.rectangle([x + 226, y + 48, x + 268, y + 96], fill=(10, 10, 14),
                   outline=(200, 200, 200), width=2)
    draw.rectangle([x + 231, y + 54, x + 263, y + 90], fill=(70, 130, 200))
    draw.text((x + 238, y + 66), "5G", font=SANS_B(16), fill=(255, 255, 255))
    # verdict stamp
    draw.text((x + 24, y + 76), "GUILTY 10/12", font=SANS_B(20), fill=RED)


def illo_riyadh(draw, x, y, w, h):
    """Night over Riyadh: a tower struck, smoke, and the desert skyline."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 55))
    draw.ellipse([x + w - 52, y + 12, x + w - 28, y + 36], fill=(240, 230, 200))
    # skyline
    base = y + h - 26
    bx = x + 8
    for bw, bh in ((34, 52), (26, 70), (40, 44), (30, 62), (36, 50), (28, 74)):
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(12, 12, 26))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if (wx * 7 + wy * 3) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
        bx += bw + 6
    # the struck tower, right side, with smoke and flame
    tx = x + w - 78
    draw.rectangle([tx, y + 14, tx + 34, base], fill=(200, 200, 210))
    draw.rectangle([tx + 4, y + 18, tx + 30, y + 40], fill=(60, 60, 80))
    smoke(draw, tx + 17, y + 12, 8, fill=(160, 160, 160))
    flame(draw, tx + 17, y + 42, 10)
    # incoming drone trail
    draw.line([x + 20, y + 10, tx + 8, y + 34], fill=(255, 220, 150), width=2)
    draw.ellipse([tx + 4, y + 30, tx + 12, y + 38], fill=(255, 160, 40))
    # fires on the ground
    flame(draw, x + 90, base + 2, 9)
    flame(draw, x + 210, base + 2, 11)


def illo_medium(draw, idx, x, y, w, h):
    """Small iconic scene for medium story idx (0-9)."""
    if idx == 0:  # Benghazi: ship on a dark sea, explosion
        draw.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(10, 25, 50))
        draw.rectangle([x + 30, y + 30, x + 160, y + 46], fill=(10, 10, 10))
        draw.rectangle([x + 70, y + 18, x + 100, y + 30], fill=(10, 10, 10))
        flame(draw, x + 60, y + 30, 10)
        flame(draw, x + 120, y + 30, 12)
        smoke(draw, x + 140, y + 12, 6)
    elif idx == 1:  # Ukraine war: helmets and candles
        draw.rectangle([x, y, x + w, y + h], fill=(60, 70, 60))
        for hx in (x + 40, x + 90, x + 140):
            draw.ellipse([hx - 16, y + 22, hx + 16, y + 44], fill=(70, 90, 60))
            draw.rectangle([hx - 18, y + 40, hx + 18, y + 46], fill=(50, 65, 45))
    elif idx == 2:  # Ebola: clinic tent, cross
        draw.rectangle([x, y, x + w, y + h], fill=(220, 220, 205))
        draw.polygon([(x + 30, y + 16), (x + 160, y + 16), (x + 175, y + h - 8),
                      (x + 15, y + h - 8)], fill=(255, 255, 255),
                     outline=RED, width=2)
        draw.rectangle([x + 88, y + 26, x + 102, y + 52], fill=RED)
        draw.rectangle([x + 80, y + 34, x + 110, y + 44], fill=RED)
    elif idx == 3:  # Dell: server racks with blinking lights
        draw.rectangle([x, y, x + w, y + h], fill=(30, 40, 60))
        for rx in (x + 16, x + 72, x + 128):
            draw.rectangle([rx, y + 10, rx + 48, y + h - 8], fill=(15, 20, 30),
                           outline=(90, 120, 150), width=1)
            for ry in range(y + 16, y + h - 12, 10):
                draw.rectangle([rx + 6, ry, rx + 10, ry + 4], fill=(90, 220, 180))
                draw.rectangle([rx + 14, ry, rx + 40, ry + 4], fill=(60, 90, 120))
        draw.text((x + 10, y + 2), "$132bn", font=SANS_B(12),
                  fill=(255, 255, 255))
    elif idx == 4:  # Stocks: falling red chart
        draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        for gy in range(y + 12, y + h - 8, 12):
            draw.line([x + 8, gy, x + w - 8, gy], fill=(230, 230, 230))
        draw.line([(x + 14, y + 14), (x + 60, y + 22), (x + 100, y + 20),
                   (x + 140, y + 38), (x + 178, y + 54)], fill=RED, width=3)
        draw.polygon([(x + 178, y + 54), (x + 168, y + 50), (x + 172, y + 44)],
                     fill=RED)
        draw.text((x + 12, y + 4), "\u22125.9%", font=SANS_B(13), fill=DARKRED)
    elif idx == 5:  # Medal of Freedom: gold medal and ribbon
        draw.rectangle([x, y, x + w, y + h], fill=(26, 42, 74))
        draw.polygon([(x + 80, y + 4), (x + 110, y + 4), (x + 100, y + 34)],
                     fill=(178, 34, 34))
        draw.polygon([(x + 80, y + 4), (x + 110, y + 4), (x + 100, y + 34)],
                     outline=(255, 255, 255), width=1)
        draw.ellipse([x + 68, y + 30, x + 122, y + h - 6], fill=(255, 215, 60),
                     outline=(180, 140, 40), width=3)
        draw.text((x + 88, y + 42), "\u2605", font=SANS_B(20), fill=DARKRED)
    elif idx == 6:  # Turkeys: two white turkeys on a farm
        draw.rectangle([x, y, x + w, y + h], fill=(140, 190, 110))
        draw.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 140, 70))
        for tx in (x + 50, x + 120):
            draw.ellipse([tx - 18, y + 26, tx + 18, y + 56], fill=(255, 255, 255))
            draw.ellipse([tx - 8, y + 16, tx + 8, y + 30], fill=(255, 255, 255))
            draw.polygon([(tx - 6, y + 20), (tx + 6, y + 20), (tx, y + 28)],
                         fill=(230, 110, 20))
            draw.rectangle([tx - 8, y + 52, tx + 8, y + h - 2],
                           fill=(230, 150, 60))
    elif idx == 7:  # Punjab: ballot box and flags
        draw.rectangle([x, y, x + w, y + h], fill=(240, 220, 180))
        draw.rectangle([x + 18, y + 14, x + 78, y + 44], fill=(255, 140, 0))
        draw.rectangle([x + 18, y + 29, x + 78, y + 44], fill=(255, 255, 255))
        draw.rectangle([x + 18, y + 44 - 15, x + 78, y + 44], fill=(0, 130, 60))
        draw.rectangle([x + 108, y + 18, x + 168, y + 52], fill=(255, 255, 255),
                       outline=RED, width=2)
        draw.rectangle([x + 120, y + 24, x + 156, y + 30], fill=RED)
        draw.text((x + 130, y + 32), "\u2713", font=SANS_B(16), fill=RED)
    elif idx == 8:  # NATO: radar plane over Poland
        draw.rectangle([x, y, x + w, y + h], fill=(170, 200, 220))
        draw.ellipse([x + 20, y + 40, x + 60, y + 56], fill=(255, 255, 255))
        draw.ellipse([x + 90, y + 46, x + 130, y + 58], fill=(255, 255, 255))
        # plane silhouette
        draw.polygon([(x + 60, y + 24), (x + 150, y + 28), (x + 150, y + 34),
                      (x + 60, y + 32)], fill=(60, 70, 90))
        draw.polygon([(x + 95, y + 16), (x + 115, y + 16), (x + 110, y + 28),
                      (x + 100, y + 28)], fill=(60, 70, 90))
        draw.ellipse([x + 98, y + 10, x + 112, y + 20], fill=(90, 100, 120))
        # radar arcs
        for r in (10, 20, 30):
            draw.arc([x + 150 - r, y + 30 - r, x + 150 + r, y + 30 + r],
                     -60, 60, fill=RED, width=2)
    else:  # Cricket: green pitch, stumps, ball
        draw.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
        draw.rectangle([x + 60, y + 8, x + 130, y + h - 8], fill=(220, 200, 150))
        for sx in (x + 66, x + 72, x + 78):
            draw.rectangle([sx, y + 14, sx + 3, y + 30], fill=(255, 220, 120))
        draw.ellipse([x + 150, y + 34, x + 164, y + 48], fill=(178, 34, 34))
        draw.text((x + 12, y + 40), "185", font=SANS_B(15), fill=(255, 255, 255))


# --------------------------------------------------------------------- map
# Crude continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-55, 52),
     (-60, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -55),
     (-75, -40), (-80, -20), (-80, 10)],
    [(-10, 36), (0, 44), (10, 45), (20, 40), (30, 36), (30, 42), (25, 45),
     (20, 55), (10, 58), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -15), (35, -25), (28, -33), (20, -35),
     (15, -30), (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(30, 36), (40, 36), (45, 30), (50, 25), (58, 25), (62, 25), (70, 20),
     (78, 8), (80, 15), (90, 22), (95, 15), (100, 8), (105, 2), (110, 10),
     (115, 20), (120, 30), (127, 35), (130, 42), (140, 45), (145, 50),
     (158, 60), (170, 66), (178, 65), (170, 60), (160, 55), (140, 50),
     (130, 45), (120, 40), (110, 35), (100, 30), (90, 28), (80, 30),
     (70, 35), (60, 40), (50, 42), (40, 45), (30, 42), (30, 36)],
    [(113, -22), (125, -12), (135, -12), (142, -10), (150, -20), (153, -27),
     (150, -37), (140, -38), (130, -32), (120, -34), (113, -22)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 235))
    draw.rectangle([x, y, x + w, y + h], outline=GREY, width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (90 - lat) / 180.0 * h)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=(232, 214, 170), outline=(150, 130, 100))
    # numbered pins for stories 1-13; the Europe/Middle-East cluster is
    # spread with leader lines so the numbers stay legible at this scale.
    offsets = [(-14, 10), (-8, -12), (0, 0), (0, 0), (0, 0), (0, 0),
               (-14, -10), (14, -10), (0, 12), (0, 0), (0, 0), (0, 0), (16, 6)]
    for i, ((lon, lat), (dx, dy)) in enumerate(zip(PINS, offsets), start=1):
        px, py = proj(lon, lat)
        ox, oy = px + dx, py + dy
        if dx or dy:
            draw.line([px, py, ox, oy], fill=RED, width=1)
        r = 7
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        fnt = SANS_B(8)
        tw = draw.textlength(str(i), font=fnt)
        draw.text((ox - tw / 2, oy - 5), str(i), font=fnt, fill=(255, 255, 255))


# ------------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top banner
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((14, 5), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=(255, 255, 255))
    right = ("35 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED "
             "WEDNESDAY 25 NOVEMBER 2026")
    d.text((W - 14 - d.textlength(right, font=SANS_B(12)), 6), right,
           font=SANS_B(12), fill=(255, 255, 255))

    # --- masthead
    title = "Wednesday 25 November 2026"
    tf = SERIF_B(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf, fill=INK)
    sub = ("CIA hit by cyberattack \u00b7 Huawei guilty of trade-secret theft "
           "\u00b7 Houthi strike hits Riyadh tower")
    sf = SERIF_I(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 86), sub, font=sf, fill=DARKRED)

    # --- stat strip (single-line labels so nothing touches the tabs)
    d.line([14, 110, W - 14, 110], fill=INK, width=2)
    d.line([14, 156, W - 14, 156], fill=INK, width=2)
    cell_w = (W - 28) / 6
    stat_labels = ["counts Huawei guilty on", "Russian soldiers killed",
                   "Ebola deaths in DR Congo", "Dell's AI server backlog",
                   "hurt in Riyadh tower strike", "Dow closes above, 1st time"]
    for i, ((num, _), label) in enumerate(zip(STATS, stat_labels)):
        cx = 14 + i * cell_w
        if i:
            d.line([cx, 114, cx, 152], fill=LIGHTGREY, width=1)
        nf = SANS_B(26)
        d.text((cx + (cell_w - d.textlength(num, font=nf)) / 2, 113), num,
               font=nf, fill=RED)
        lf = SANS(10)
        d.text((cx + (cell_w - d.textlength(label, font=lf)) / 2, 142), label,
               font=lf, fill=GREY)

    # --- region tabs (fixed widths so the WORLD tab is not cut off)
    x = 14
    tab_widths = [260, 210, 185, 160, 95, 86]
    for (name, n, color), seg_w in zip(REGIONS, tab_widths):
        d.rectangle([x, 162, x + seg_w - 1, 180], fill=color)
        lab = f"{name} {n}"
        lf = SANS_B(11)
        d.text((x + (seg_w - d.textlength(lab, font=lf)) / 2, 166), lab,
               font=lf, fill=(255, 255, 255))
        x += seg_w

    # --- 3 lead stories (kicker overlaid on the illustration, top-left)
    lead_w, lead_gap = 320, 12
    lead_x0 = 14
    illos = (illo_cia, illo_huawei, illo_riyadh)
    for i, (tag, loc, head, summ, src) in enumerate(LEADS):
        x = lead_x0 + i * (lead_w + lead_gap)
        illos[i](d, x, 188, lead_w, 112)
        d.rectangle([x, 188, x + lead_w - 1, 299], outline=GREY, width=1)
        kicker(d, x + 5, 193, tag)
        d.text((x, 306), f"{i + 1} {loc}", font=SANS_B(11), fill=DARKRED)
        hf = SERIF_B(19)
        y = text_block(d, (x, 324), wrap(d, head, hf, lead_w), hf, leading=22)
        bf = SANS(12)
        y = text_block(d, (x, y + 2), wrap(d, summ, bf, lead_w), bf, leading=15)
        d.text((x, y + 1), f"({src})", font=SANS(10), fill=GREY)

    # --- 10 medium stories, 2 rows x 5 (kicker overlaid on illustration)
    med_w, med_gap = 192, 8
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            tag, loc, head, summ, src = MEDIUMS[idx]
            x = 14 + col * (med_w + med_gap)
            y = 428 + row * 144
            illo_medium(d, idx, x, y, med_w, 58)
            d.rectangle([x, y, x + med_w - 1, y + 57], outline=GREY, width=1)
            kicker(d, x + 4, y + 4, tag)
            d.text((x, y + 63), f"{idx + 4} {loc}", font=SANS_B(9), fill=DARKRED)
            hf = SERIF_B(13)
            yy = text_block(d, (x, y + 77),
                            wrap(d, head, hf, med_w), hf, leading=15)
            bf = SANS(10)
            yy = text_block(d, (x, yy + 1),
                            wrap(d, summ, bf, med_w), bf, leading=12)
            d.text((x, yy), f"({src})", font=SANS(9), fill=GREY)

    # --- map + list
    d.line([14, 720, W - 14, 720], fill=INK, width=2)
    d.text((14, 726), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((14, 742), "pins match story numbers", font=SANS(10), fill=GREY)
    draw_map(d, 14, 760, 280, 150)
    d.text((14, 916), "Red numbers mark stories 1\u201313 on the map.",
           font=SANS(9), fill=GREY)

    lx = 312
    d.text((lx, 726), "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 22 MORE STORIES",
           font=SANS_B(12), fill=INK)
    col_w = (W - 14 - lx) // 2
    lf = SANS(10)
    for ci in range(2):
        cx = lx + ci * col_w
        y = 746
        for num, item in MORE[ci * 11:(ci + 1) * 11]:
            lines = wrap(d, f"{num}  {item}", lf, col_w - 10)
            y = text_block(d, (cx, y), lines, lf, leading=12)
            y += 3

    # --- date check
    d.rectangle([14, 930, W - 14, 988], outline=RED, width=2)
    d.text((22, 936), "DATE CHECK", font=SANS_B(11), fill=DARKRED)
    df = SANS(11)
    dc = ("Wires read up to 01:30 UTC, 25 Nov 2026. Every story was reported "
          "on 24\u201325 November 2026. Left out: COP31 collapse (22 Nov), "
          "Bolsonaro in intensive care (22 Nov), Peru quake (20 Nov), "
          "GTA 6 release (19 Nov).")
    text_block(d, (22, 952), wrap(d, dc, df, W - 44), df, leading=13)

    # --- sources + footer
    d.text((14, 992),
           "Sources: CNN, Reuters, AP, BBC, WHO, US Justice Dept, Financial "
           "Times, Investopedia, Mediazona. Every story names its outlet. "
           "Pictures and map: original, drawn in code.",
           font=SANS(9), fill=GREY)
    d.line([14, 1008, W - 14, 1008], fill=INK, width=1)
    d.text((14, 1012), "THE WORLD IN ONE DAY", font=SANS_B(10), fill=INK)
    foot = "WEDNESDAY 25 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - 14 - d.textlength(foot, font=SANS_B(10)), 1012), foot,
           font=SANS_B(10), fill=INK)

    img.save(OUT, "JPEG", quality=90, optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
