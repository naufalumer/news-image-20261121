#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Pillow only, build time. Every pictured story was checked against
reporting first published (or happening) on 21 November 2026; see
NEWS_FACTS.md beside this file. Flags are drawn from rectangles,
circles and polygons: no photographs, no downloads, no network.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
IVORY = (247, 242, 231)
PAPER = (252, 249, 242)
NAVY = (20, 33, 61)
NAVY_SOFT = (38, 54, 90)
GOLD = (176, 134, 47)
GOLD_SOFT = (212, 175, 105)
INK = (26, 26, 26)
GREY = (92, 88, 80)
RED = (155, 44, 44)
LINE = (201, 192, 172)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, rotation=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rotation + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(draw, text, fnt, width):
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


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.35)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text):
    f = font(SANS_B, 17)
    draw.text((x, y), text, font=f, fill=GOLD)
    return y + 24


def headline(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.12)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def flag_turkiye(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
    cx, cy, r = x + w * 0.42, y + h / 2, h * 0.30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    cx2, r2 = cx + r * 0.28, r * 0.80
    draw.ellipse([cx2 - r2, cy - r2, cx2 + r2, cy + r2], fill=(227, 10, 23))
    sx = x + w * 0.66
    draw.polygon(star_points(sx, cy, h * 0.17, h * 0.07), fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_usa(draw, x, y, w, h):
    for i in range(13):
        col = (179, 25, 66) if i % 2 == 0 else (255, 255, 255)
        y0 = y + h * i / 13
        draw.rectangle([x, y0, x + w, y0 + h / 13 + 1], fill=col)
    cw, ch = w * 0.40, h * 7 / 13
    draw.rectangle([x, y, x + cw, y + ch], fill=(10, 49, 97))
    for r in range(5):
        for c in range(6):
            px = x + cw * (c + 0.5) / 6
            py = y + ch * (r + 0.5) / 5
            draw.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4],
                         fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_iran(draw, x, y, w, h):
    for i, col in enumerate([(0, 122, 61), (255, 255, 255), (218, 0, 0)]):
        y0 = y + h * i / 3
        draw.rectangle([x, y0, x + w, y0 + h / 3 + 1], fill=col)
    draw.rectangle([x + w * 0.46, y + h * 0.30, x + w * 0.54, y + h * 0.70],
                   fill=(218, 0, 0))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon(star_points(x + w * 0.20, y + h * 0.28, h * 0.22, h * 0.09),
                 fill=(255, 222, 0))
    for sx, sy in [(0.42, 0.12), (0.52, 0.26), (0.52, 0.46), (0.42, 0.58)]:
        draw.polygon(star_points(x + w * sx, y + h * sy, h * 0.09, h * 0.04),
                     fill=(255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_japan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(188, 0, 45))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_spain(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h * 0.25], fill=(170, 21, 27))
    draw.rectangle([x, y + h * 0.25, x + w, y + h * 0.75], fill=(241, 191, 0))
    draw.rectangle([x, y + h * 0.75, x + w, y + h], fill=(170, 21, 27))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(31, 93, 140),
                 outline=NAVY, width=3)
    # abstract landmasses in gold-green
    draw.ellipse([cx - r * 0.72, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=(196, 164, 92))
    draw.ellipse([cx + r * 0.05, cy - r * 0.10, cx + r * 0.70, cy + r * 0.55],
                 fill=(196, 164, 92))
    draw.ellipse([cx - r * 0.25, cy + r * 0.35, cx + r * 0.25, cy + r * 0.80],
                 fill=(176, 148, 80))
    for k in range(1, 4):
        x0 = cx - r + 2 * r * k / 4
        draw.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(255, 255, 255))
        draw.line([x0, cy - r, x0, cy + r], fill=(255, 255, 255), width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)


def main():
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.text((28, 22), "T H E   W O R L D   I N   O N E   P A G E",
           font=font(SERIF_B, 21), fill=GOLD_SOFT)
    d.text((28, 56), "SATURDAY 21 NOVEMBER 2026",
           font=font(SERIF_B, 46), fill=(250, 247, 240))
    d.line([28, 146, W - 28, 146], fill=GOLD, width=2)
    d.text((28, 124), "The day's news, drawn from reporting first published on 21 November 2026",
           font=font(SANS, 15), fill=(190, 196, 214))

    # ---- lead: COP31 ----
    x0, y0, x1, y1 = 28, 176, 648, 566
    d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 6], fill=GOLD)
    y = y0 + 20
    y = kicker(d, x0 + 20, y, "CLIMATE  ·  ANTALYA, TURKIYE")
    y = headline(d, x0 + 20, y + 4, "CLIMATE TALKS RUN INTO OVERTIME",
                 font(SERIF_B, 46), x1 - x0 - 40)
    y = para(d, x0 + 20, y + 8,
             "Nearly 200 nations fail to agree a deal on the final scheduled "
             "day, as the draft drops all mention of ending fossil fuels. A "
             "bloc led by France and Panama demands a stronger text.",
             font(SANS, 20), x1 - x0 - 40)
    globe(d, x0 + 105, y1 - 62, 62)
    flag_turkiye(d, x0 + 205, y1 - 92, 96, 60)
    d.text((x0 + 320, y1 - 88), "The '35 by 35' goal:",
           font=font(SANS_B, 19), fill=INK)
    para(d, x0 + 320, y1 - 62,
         "electricity to 35% of all energy by 2035",
         font(SANS, 18), x1 - x0 - 340, fill=GREY)

    # ---- right column, top: Iran ----
    x0, y0, x1, y1 = 668, 176, 996, 356
    d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 6], fill=RED)
    flag_usa(d, x1 - 156, y0 + 14, 68, 32)
    flag_iran(d, x1 - 80, y0 + 14, 68, 32)
    y = y0 + 16
    y = kicker(d, x0 + 16, y, "US  ·  IRAN")
    y = headline(d, x0 + 16, y + 2, "TRUMP WEIGHS IRAN STRIKES",
                 font(SERIF_B, 27), x1 - x0 - 32)
    y = para(d, x0 + 16, y + 6,
             "US commanders warn time is running out. Trump says he is in "
             "no rush: a decision after the New Year.",
             font(SANS, 16), x1 - x0 - 32, fill=GREY)

    # ---- right column, bottom: China-Japan ----
    x0, y0, x1, y1 = 668, 372, 996, 566
    d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 6], fill=NAVY_SOFT)
    flag_china(d, x1 - 156, y0 + 14, 68, 32)
    flag_japan(d, x1 - 80, y0 + 14, 68, 32)
    y = y0 + 16
    y = kicker(d, x0 + 16, y, "CHINA  ·  JAPAN")
    y = headline(d, x0 + 16, y + 2, "BEIJING PRESSES TOKYO",
                 font(SERIF_B, 27), x1 - x0 - 32)
    y = para(d, x0 + 16, y + 6,
             "China tells Japan to clarify its remarks after APEC. Tokyo's "
             "leader did not meet Taiwan's envoy in Shenzhen.",
             font(SANS, 16), x1 - x0 - 32, fill=GREY)

    # ---- bottom left: Spain / Amnesty ----
    x0, y0, x1, y1 = 28, 586, 648, 856
    d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 6], fill=(170, 21, 27))
    y = y0 + 20
    y = kicker(d, x0 + 20, y, "SPAIN  ·  HUMAN RIGHTS")
    y = headline(d, x0 + 20, y + 4, "AMNESTY: POLICE FORCE 'EXCESSIVE' IN STRIKE",
                 font(SERIF_B, 33), x1 - x0 - 40)
    y = para(d, x0 + 20, y + 8,
             "Amnesty International reports today that Spanish police used "
             "excessive force during the country's first general strike in "
             "14 years, held on 11 November over the housing crisis.",
             font(SANS, 19), x1 - x0 - 40)
    flag_spain(d, x0 + 20, y1 - 62, 108, 54)
    d.text((x0 + 148, y1 - 52), "Unions UGT and CCOO called the walkout.",
           font=font(SANS, 17), fill=GREY)

    # ---- bottom right: also today ----
    x0, y0, x1, y1 = 668, 586, 996, 856
    d.rectangle([x0, y0, x1, y1], fill=NAVY, outline=LINE, width=1)
    y = y0 + 20
    d.text((x0 + 20, y), "ALSO TODAY", font=font(SANS_B, 18), fill=GOLD_SOFT)
    y += 30
    y = headline(d, x0 + 20, y, "A CHRISTMAS WISH: A CEASEFIRE",
                 font(SERIF_B, 28), x1 - x0 - 40, fill=(250, 247, 240))
    y = para(d, x0 + 20, y + 8,
             "First Lady Melania Trump: her Christmas wish is another "
             "ceasefire in Ukraine.",
             font(SANS, 17), x1 - x0 - 40, fill=(205, 210, 224))
    flag_usa(d, x0 + 20, y1 - 52, 84, 42)

    # ---- footer ----
    d.line([28, 884, W - 28, 884], fill=GOLD, width=2)
    para(d, 28, 900,
         "Sources: Reuters · AP · UN News · Financial Times · Asahi Shimbun · "
         "Amnesty International · Daily Mail — all first reported 21 November 2026.",
         font(SANS, 15), W - 56, fill=GREY)
    d.text((28, 956), "THE WORLD IN ONE PAGE  ·  21 NOVEMBER 2026",
           font=font(SANS_B, 14), fill=NAVY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    main()
