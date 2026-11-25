"""Build-time card renderer (Pillow only; never imported by main.py).

Renders three static PNGs for the README:
  cover.png          — hero: the winning review comment as a GitHub-style card
  card-winner.png    — the winning line, large, as an approval comment
  card-finalists.png — the top 4 tournament lines with their scores

Run:  python3 make_cards.py   (writes PNGs next to this file)
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 23)        # GitHub dark canvas
PANEL = (22, 27, 34)     # card panel
PANEL_EDGE = (48, 54, 61)
GREEN = (63, 185, 80)    # approval green
GOLD = (210, 153, 34)    # dread gold
TEXT = (230, 237, 243)
MUTED = (139, 148, 158)
FAINT = (110, 119, 129)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded_panel(draw, box, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=PANEL, outline=PANEL_EDGE, width=2)


def approval_pill(draw, x, y):
    """Green APPROVED pill; returns its right edge."""
    label = "APPROVED"
    f = font(SANS_BOLD, 26)
    w = int(draw.textlength(label, font=f)) + 44
    draw.rounded_rectangle([x, y, x + w, y + 44], radius=22, fill=GREEN)
    draw.text((x + 22, y + 8), label, font=f, fill=(13, 17, 23))
    return x + w


def wrap(draw, text, f, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return lines


WINNER = "Ship it. My grandchildren will maintain this code. I have made my peace with that."
FINALISTS = [
    ("C3  ·  24/25  ·  WINNER", WINNER),
    ("A1  ·  24/25", "LGTM. The tests pass, the heat death of the universe continues, and this diff changes neither."),
    ("A3  ·  23/25", "Ship it. Entropy increases either way; at least this way the build is green."),
    ("H2  ·  24/25", "Approved. Whatever happens next happens with my blessing and without my involvement."),
]


def cover():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # faint code lines in the background
    code_f = font(MONO, 22)
    code_lines = [
        "+ def merge_pr(self, reviewer):",
        "+     if reviewer.is_tired and tests.are_green:",
        "+         return reviewer.approve(quietly=True)",
        "-     # TODO: fix before the heat death",
        "+     # too late now — ship it",
    ]
    y = 36
    for line in code_lines:
        d.text((48, y), line, font=code_f, fill=(38, 46, 56))
        y += 34
    # hero panel
    rounded_panel(d, [48, 240, 1152, 560])
    # title
    d.text((84, 268), "TWO DAYS OF QUIET DREAD", font=font(SANS_BOLD, 34), fill=GOLD)
    d.text((84, 312), "one code-review comment  ·  82 characters  ·  approves the PR",
           font=font(SANS, 24), fill=MUTED)
    # approval pill + winner line
    approval_pill(d, 84, 360)
    lines = wrap(d, WINNER, font(SANS_BOLD, 34), width=44)
    y = 424
    for line in lines:
        d.text((84, y), line, font=font(SANS_BOLD, 34), fill=TEXT)
        y += 46
    d.text((84, 576), "make.fun  ·  $2 bounty  ·  10 paid places  ·  40 candidates, knockout tournament",
           font=font(SANS, 20), fill=FAINT)
    img.save("cover.png")


def winner_card():
    W, H = 1024, 512
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    rounded_panel(d, [32, 32, 992, 480])
    # avatar circle + reviewer name
    d.ellipse([64, 64, 128, 128], fill=(31, 111, 235))
    d.text((84, 82), "kr", font=font(SANS_BOLD, 30), fill=(255, 255, 255))
    d.text((148, 70), "kangris-uk", font=font(SANS_BOLD, 30), fill=TEXT)
    d.text((148, 106), "reviewed  ·  approved this pull request", font=font(SANS, 24), fill=MUTED)
    approval_pill(d, 148, 148)
    # the comment, quoted
    d.text((64, 224), "\u201c", font=font(SANS_BOLD, 90), fill=GOLD)
    lines = wrap(d, WINNER, font(SANS_BOLD, 38), width=33)
    y = 250
    for line in lines:
        d.text((128, y), line, font=font(SANS_BOLD, 38), fill=TEXT)
        y += 52
    d.text((96, 420), "82 characters  ·  tournament winner, 24/25",
           font=font(SANS, 22), fill=FAINT)
    img.save("card-winner.png")


def finalists_card():
    W, H = 1024, 768
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((48, 36), "TOP 4 OF 40 — KNOCKOUT TOURNAMENT", font=font(SANS_BOLD, 32), fill=GOLD)
    d.text((48, 80), "scored on the judge brief, criteria in order: approval + dread, first-read laugh,",
           font=font(SANS, 22), fill=MUTED)
    d.text((48, 108), "quiet understatement, real-paste voice, fresh turn of phrase.",
           font=font(SANS, 22), fill=MUTED)
    y = 156
    for tag, text in FINALISTS:
        rounded_panel(d, [48, y, 976, y + 128])
        d.text((76, y + 14), tag, font=font(SANS_BOLD, 22),
               fill=GREEN if "WINNER" in tag else GOLD)
        lines = wrap(d, text, font(SANS, 26), width=52)
        ly = y + 48
        for line in lines:
            d.text((76, ly), line, font=font(SANS, 26), fill=TEXT)
            ly += 34
        y += 148
    img.save("card-finalists.png")


if __name__ == "__main__":
    cover()
    winner_card()
    finalists_card()
    print("wrote cover.png, card-winner.png, card-finalists.png")
