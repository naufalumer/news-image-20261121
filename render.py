#!/usr/bin/env python3
"""Render the 21 Nov 2026 world-news front page, 1024x1024 PNG."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/make-fun/news-image-20261121-repo/entry.png"
FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 44)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_SUB = font("DejaVuSans.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 11)
F_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_HEAD_LEAD = font("DejaVuSans-Bold.ttf", 21)
F_DECK = font("DejaVuSans.ttf", 11)
F_DECK_LEAD = font("DejaVuSans.ttf", 13)
F_FOOT = font("DejaVuSans.ttf", 11)
F_CAP = font("DejaVuSans-Bold.ttf", 10)

INK = (18, 18, 18)
PAPER = (242, 233, 211)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
GREY = (105, 98, 80)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((20, 10), "WORLD NEWS", font=F_TITLE, fill=(255, 255, 255))
d.text((20, 62), "SATURDAY, 21 NOVEMBER 2026", font=F_DATE, fill=(255, 214, 90))
d.text((W - 20, 14), "THE DAY IN", font=font("DejaVuSans-Bold.ttf", 16),
       fill=(255, 255, 255), anchor="ra")
d.text((W - 20, 36), "13 STORIES", font=font("DejaVuSans-Bold.ttf", 16),
       fill=(255, 214, 90), anchor="ra")
d.text((W - 20, 62), "AS REPORTED TODAY", font=font("DejaVuSans.ttf", 13),
       fill=(200, 210, 230), anchor="ra")
d.rectangle([0, 104, W, 108], fill=RED)

# ---------- flag helpers ----------
def flag_box(x, y, w, h, stripes, vertical=False):
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)
    n = len(stripes)
    for i, c in enumerate(stripes):
        if vertical:
            d.rectangle([x + i * w // n, y, x + (i + 1) * w // n, y + h], fill=c)
        else:
            d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)

def star(cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)

def draw_flag(kind, x, y, w=52, h=34):
    if kind == "poland":
        flag_box(x, y, w, h, [(255, 255, 255), (220, 20, 60)])
    elif kind == "myanmar":
        flag_box(x, y, w, h, [(254, 203, 0), (52, 168, 83), (234, 40, 57)])
        star(x + w // 2, y + h // 2, 9, (255, 255, 255))
    elif kind == "turkey":
        d.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
        d.ellipse([x + 12, y + 7, x + 28, y + 27], fill=(255, 255, 255))
        d.ellipse([x + 15, y + 9, x + 29, y + 25], fill=(227, 10, 23))
        star(x + 36, y + 17, 6, (255, 255, 255))
    elif kind == "oman":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 122, 61))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(206, 17, 38))
        d.rectangle([x, y, x + 11, y + h], fill=(206, 17, 38))
    elif kind == "uk":
        d.rectangle([x, y, x + w, y + h], fill=(1, 33, 105))
        d.rectangle([x, y + h // 2 - 5, x + w, y + h // 2 + 5], fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 5, y, x + w // 2 + 5, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + h // 2 - 2, x + w, y + h // 2 + 2], fill=(200, 16, 46))
        d.rectangle([x + w // 2 - 2, y, x + w // 2 + 2, y + h], fill=(200, 16, 46))
    elif kind == "eu":
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        import math
        for i in range(12):
            a = 2 * math.pi * i / 12 - math.pi / 2
            d.ellipse([x + w // 2 + 13 * math.cos(a) - 2, y + h // 2 + 10 * math.sin(a) - 2,
                       x + w // 2 + 13 * math.cos(a) + 2, y + h // 2 + 10 * math.sin(a) + 2],
                      fill=(255, 204, 0))
    elif kind == "denmark":
        d.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
        d.rectangle([x, y + h // 2 - 4, x + w, y + h // 2 + 4], fill=(255, 255, 255))
        d.rectangle([x + 15, y, x + 23, y + h], fill=(255, 255, 255))
    elif kind == "india":
        flag_box(x, y, w, h, [(255, 153, 51), (255, 255, 255), (19, 136, 8)])
        d.ellipse([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7, y + h // 2 + 7],
                  outline=(0, 0, 128), width=2)
    elif kind == "usa":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x, y, x + w * 2 // 5, y + 4 * h // 7], fill=(60, 59, 110))
        for r in range(3):
            for c in range(4):
                d.ellipse([x + 3 + c * 8, y + 3 + r * 6, x + 6 + c * 8, y + 6 + r * 6],
                          fill=(255, 255, 255))
    elif kind == "france":
        flag_box(x, y, w, h, [(0, 85, 164), (255, 255, 255), (239, 65, 53)], vertical=True)
    elif kind == "iran":
        flag_box(x, y, w, h, [(0, 122, 61), (255, 255, 255), (218, 0, 0)])
    elif kind == "nvidia":
        d.rectangle([x, y, x + w, y + h], fill=(118, 185, 0))
        d.text((x + w // 2, y + h // 2 - 8), "NVIDIA", font=F_CAP,
               fill=(255, 255, 255), anchor="ma")
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)

def portrait(x, y, r, hair, skin=(232, 190, 150), name=""):
    d.ellipse([x - r, y - r, x + r, y + r], fill=skin, outline=(60, 60, 60), width=1)
    d.pieslice([x - r, y - r, x + r, y + r - 6], 180, 360, fill=hair)
    d.ellipse([x - r + 4, y - 4, x - r + 12, y + 4], fill=(30, 30, 30))
    d.ellipse([x + r - 12, y - 4, x + r - 4, y + 4], fill=(30, 30, 30))
    d.arc([x - 8, y + 2, x + 8, y + 14], 20, 160, fill=(120, 60, 40), width=2)
    if name:
        d.text((x, y + r + 3), name, font=F_CAP, fill=INK, anchor="ma")

def wrap(text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    # wrap by pixel width
    out = []
    for ln in lines:
        words, cur = ln.split(), ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=fnt) <= width:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = wd
        if cur:
            out.append(cur)
    return out

def card(x, y, w, h, kicker, headline, deck, visual, lead=False):
    d.rectangle([x, y, x + w, y + h], fill=(251, 245, 229),
                outline=(168, 152, 124), width=1)
    d.rectangle([x, y, x + w, y + 3], fill=RED)
    pad = 10
    tx = x + pad
    ty = y + 9
    d.text((tx, ty), kicker, font=F_KICK, fill=RED)
    ty += 15
    hf = F_HEAD_LEAD if lead else F_HEAD
    df = F_DECK_LEAD if lead else F_DECK
    lh = 24 if lead else 18
    dlh = 17 if lead else 14
    maxw = w - 2 * pad - (118 if visual == "trio" else 62 if visual else 0)
    for ln in wrap(headline, hf, maxw):
        d.text((tx, ty), ln, font=hf, fill=INK)
        ty += lh
    ty += 2
    for ln in wrap(deck, df, w - 2 * pad):
        d.text((tx, ty), ln, font=df, fill=(40, 40, 40))
        ty += dlh
    if visual:
        vx = x + w - 62
        vy = y + 9
        if visual == "trio":
            portrait(vx - 40, vy + 14, 13, (240, 210, 90), name="TRUMP")
            portrait(vx - 6, vy + 14, 13, (20, 20, 20), name="XI")
            portrait(vx + 28, vy + 14, 13, (200, 190, 170), name="PUTIN")
        elif visual == "uk-eu":
            draw_flag("uk", vx - 4, vy, 30, 20)
            draw_flag("eu", vx + 30, vy, 30, 20)
            d.text((vx + 26, vy + 24), "UK + EU", font=F_CAP, fill=INK, anchor="ma")
        elif visual == "us-iran":
            draw_flag("usa", vx - 4, vy, 30, 20)
            draw_flag("iran", vx + 30, vy, 30, 20)
            d.text((vx + 26, vy + 24), "USA + IRAN", font=F_CAP, fill=INK, anchor="ma")
        else:
            draw_flag(visual, vx - 4, vy, 56, 36)

# ---------- lead card ----------
card(12, 118, 1000, 138, "LEAD  |  POLAND  —  FRIDAY",
     "Russian missiles land in Poland",
     "Friday: two Russian missiles and a suspected drone came down in south-east Poland during a huge "
     "Russian attack on Ukraine. A Kh-101 cruise missile fell near Nowy Lipowiec, about 50 km from the "
     "border. PM Donald Tusk called it a likely deliberate provocation, timed with the Koalicja 26.2 "
     "exercise of 11 nations. NATO chief Mark Rutte: a \u201cgrave violation\u201d. No injuries in Poland; "
     "8 killed, 28 hurt in Ukraine overnight.",
     "poland", lead=True)

# ---------- grid: 12 cards, 3 cols x 4 rows ----------
GX, GY, CW, CH, GAP = 12, 266, 326, 172, 11
CARDS = [
    ("CHINA  —  THURSDAY", "Trump, Xi and Putin meet in Shenzhen",
     "Thursday: the first-ever trilateral meeting of the US, Chinese and Russian leaders, 90 minutes at "
     "Kylin Villa. Joint statement: dialogue on cutting nuclear risks; \u201ca nuclear war cannot be won "
     "and must never be fought\u201d. Few specifics, and no Ukraine breakthrough.",
     "trio"),
    ("THE HAGUE  —  THURSDAY", "World court: Myanmar guilty of Rohingya genocide",
     "The ICJ ruled 9-6 on Thursday: the first time a state has been found to have committed genocide. "
     "About 10,000 Rohingya were killed in the 2017 clearance operations. The court ordered reparations "
     "and the return of the displaced; Myanmar dismissed the ruling Friday as \u201cunfair\u201d.",
     "myanmar"),
    ("TURKEY  —  FRIDAY", "COP31 goes into overtime",
     "Climate talks in Antalya spilled past their Friday deadline. The draft deal strips out ALL mention "
     "of fossil fuels after objections from Saudi Arabia and oil producers; a $120bn adaptation-finance "
     "target was dropped. A third draft is due Saturday morning. October 2026 was 1.8\u00b0C warmer than "
     "the mid-1800s.",
     "turkey"),
    ("USA  —  FRIDAY", "Wall Street rout: S&P 500 enters correction",
     "Friday: the S&P 500 fell 3.7% to 6,910, its 7th straight loss, down over 10% from its 6 October "
     "record high. Nasdaq fell 5.3%, negative for the year. Nvidia fell 14% (CEO Jensen Huang has "
     "departed); Anthropic shares fell 9% to $88.30, a day after the biggest IPO in US history.",
     "nvidia"),
    ("OMAN  —  FRIDAY", "Tanker hit in the Strait of Hormuz",
     "Friday, about 15:00 UTC: a tanker was struck by an unknown projectile 8 nautical miles north of "
     "Khasab, Oman; fire on board, no casualties. The fourth tanker hit near Khasab in three days, as "
     "transits fall amid the US-Iran confrontation.",
     "oman"),
    ("BRUSSELS  —  FRIDAY", "UK and EU seal post-Brexit reset",
     "At Friday\u2019s summit: deals on food trade without checks (worth +\u00a35.1bn a year), youth "
     "mobility (100,000 a year, ages 18-31, up to 3 years, from 2030) and linked carbon markets. The "
     "tuition-fee deal was pushed back six months. PM Andy Burnham called it a \u201cwin-win\u201d.",
     "uk-eu"),
    ("DENMARK  —  FRIDAY", "Denmark foils \u2018Russian plot to kill rapper\u2019",
     "Security service PET said Friday that Russian intelligence planned to assassinate US-Ukrainian "
     "rapper Kyivstoner at a concert near Copenhagen on 25 September. Three men were arrested five "
     "minutes before the show with loaded pistols; two were charged. Denmark expelled Russia\u2019s "
     "defence attach\u00e9.",
     "denmark"),
    ("INDIA  —  FRIDAY", "Cyclone Akvan hits India\u2019s east coast",
     "Friday morning: the storm crossed the coast near Gopalpur, Odisha, with winds of 70-80 km/h "
     "gusting to 90; extremely heavy rain (over 21 cm) in Odisha. It weakened to a deep depression, "
     "with a flash-flood risk.",
     "india"),
    ("USA  —  FRIDAY", "Virginia\u2019s first measles death of 2026",
     "A child aged 0-4 died after testing positive for measles \u2014 the first measles death in "
     "Virginia since 1978. The state has reported 220 measles cases this year, and the US has lost its "
     "measles elimination status.",
     "usa"),
    ("FRANCE  —  FRIDAY", "Paris court: racist police beating, officers jailed",
     "Friday evening: three officers were sentenced over the 2020 beating of music producer Michel "
     "Zecler; the court recognised the racist nature of the violence, with jail time included in the "
     "sentences.",
     "france"),
    ("USA / IRAN  —  FRIDAY", "Trump: \u2018in no rush\u2019 on Iran",
     "Friday: Trump said he is not rushing decisions on Iran and may wait until 2027. A US naval "
     "blockade is in place and the Treasury says Iran has no crude oil at sea for buyers. Netanyahu is "
     "pressing for more strikes.",
     "us-iran"),
    ("INDIA  —  SATURDAY", "Sensex rallies; India fight back in Wellington",
     "Saturday: the Sensex rose 898 to 83,919.71, Nifty 25,800.60. Cricket: India 159/1 at stumps on "
     "Day 2 of the Wellington Test vs New Zealand, trailing by 209 runs.",
     "india"),
]

for i, (kick, head, deck, vis) in enumerate(CARDS):
    r, c = divmod(i, 3)
    card(GX + c * (CW + GAP), GY + r * (CH + GAP), CW, CH, kick, head, deck, vis)

# ---------- footer ----------
fy = GY + 4 * CH + 3 * GAP + 6
d.text((12, fy), "Sources: Reuters  ·  AP  ·  UN News  ·  WSJ  ·  CNN  ·  Le Monde  ·  NPR  ·  IMD",
       font=F_FOOT, fill=GREY)
d.text((W - 12, fy), "21 NOV 2026", font=font("DejaVuSans-Bold.ttf", 11),
       fill=GREY, anchor="ra")

img.save(OUT, optimize=True)
print("saved", OUT)
