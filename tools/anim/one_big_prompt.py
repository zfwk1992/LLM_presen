"""04a: what the LLM actually receives. You type one line; the harness assembles one long token sequence."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import header, chip, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F, SLATE, SLATE_F

END = 22.5
# name, where it comes from, tokens (illustrative), colours
PARTS = [
    ("System prompt", "written by Claude Code: how to behave", 3200, SLATE, SLATE_F),
    ("Tool definitions", "Read, Grep, Bash, Edit, Skill, MCP tools …", 9500, ORANGE, ORANGE_F),
    ("CLAUDE.md", "your project notes, loaded every session", 1400, TEAL, TEAL_F),
    ("Skill list", "one line per skill, e.g. dcm-guide", 600, GREEN, GREEN_F),
    ("Your message", "“Investigate how DCM works”", 9, BLUE, BLUE_F),
]
TOTAL = sum(p[2] for p in PARTS)
CARD_Y = [124, 190, 256, 322, 420]
SX0, SX1, SY0, SY1 = 470, 640, 124, 524
seg, y = [], SY0
for name, _, n, _, _ in PARTS:
    h = max(4.0, (SY1 - SY0 - 4) * n / (TOTAL - 9)) if n > 9 else 4.0
    seg.append((y, y + h)); y += h
CAPS = [
    (0.8, 1, "You type one short message"),
    (3.6, 2, "The harness adds the rest: system prompt, tools, CLAUDE.md, skill list"),
    (7.0, 3, "Everything is joined into one long token sequence"),
    (11.6, 4, "That whole sequence goes into the LLM at once"),
    (15.0, 5, "Skills: only the one-line descriptions are in it, not the full text"),
    (18.6, 6, "The context window is the prompt: you typed a tiny part of it"),
]


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "What the LLM Actually Receives", "FROM LLM TO AI AGENT", PURPLE)
    f.text((56, 108), "WHERE IT COMES FROM", inter(10.5, 700), LIGHT, v(0.9))
    f.text((SX0, 108), "ONE TOKEN SEQUENCE", inter(10.5, 700), LIGHT, v(7.1))

    # ---- source cards (your message first, the harness parts later)
    for i, (name, sub, n, col, fill) in enumerate(PARTS):
        a = v(0.9) if i == 4 else v(3.8 + 0.35 * i)
        y0 = CARD_Y[i]
        f.rrect((56, y0, 400, y0 + 56), 8, fill=fill, outline=col, a=a, width=1.3)
        f.rrect((56, y0, 62, y0 + 56), 3, fill=col, a=a)
        f.text((76, y0 + 19), name, inter(13.5, 700), col, a)
        f.text((76, y0 + 39), sub, inter(11.5, 400), GREY, a)
    f.text((56, 404), "YOU", inter(10.5, 700), BLUE, v(0.9))
    f.text((56, 492), "the only part you typed", inter(11.5, 500), BLUE, v(1.6))

    # ---- the strip: every part becomes a segment, in proportion to its token count
    f.rrect((SX0 - 3, SY0 - 3, SX1 + 3, SY1 + 3), 6, outline=PANEL_B, a=v(7.1), width=1.2)
    for i, (name, sub, n, col, fill) in enumerate(PARTS):
        m = ease((t - (7.3 + 0.55 * i)) / 0.8)
        if m <= 0.001:
            continue
        cy0 = CARD_Y[i]
        s0, s1 = seg[i]
        x0 = 56 + (SX0 - 56) * m; x1 = 400 + (SX1 - 400) * m
        y0 = cy0 + (s0 - cy0) * m; y1 = cy0 + 56 + (s1 - cy0 - 56) * m
        f.rrect((x0, y0, x1, y1), 3 if m > 0.9 else 8, fill=fill, outline=col, a=0.35 + 0.65 * m, width=1.2)
        la = v(7.3 + 0.55 * i + 0.7)
        ly = (s0 + s1) / 2
        if i == 3:
            ly = 502
        if i == 4:
            ly = 538
            f.line((SX1 + 6, 524), (SX1 + 18, 536), col, la, 1)
        elif i == 3:
            f.line((SX1 + 6, (s0 + s1) / 2), (SX1 + 18, 502), col, la, 1)
        f.text((SX1 + 22, ly), name, inter(12, 600), col, la)
        f.text((SX1 + 22 + inter(12, 600).getlength(name) / 2 + 8, ly), f"{n:,} tokens", mono(11), GREY, la)

    # ---- into the LLM
    g = v(11.7)
    f.line((856, SY0), (856, SY1), LIGHT, g, 1.3)
    f.line((848, SY0), (856, SY0), LIGHT, g, 1.3)
    f.line((848, SY1), (856, SY1), LIGHT, g, 1.3)
    f.arrow((858, 324), (896, 324), PURPLE, 1, 1.8, prog=v(12.0, 0.4))
    f.rrect((900, 268, 1180, 380), 14, fill=PURPLE_F, outline=PURPLE, a=g, width=1.8)
    s = (t - 12.5) / 1.2
    if 0 < s < 1:
        f.rrect((908 + 232 * s, 276, 938 + 232 * s, 372), 8, fill=PURPLE_HI, a=0.8 * (1 - abs(s - 0.5) * 1.3))
    f.text((1040, 312), "LLM", inter(24, 700), PURPLE, g, "mm")
    f.text((1040, 344), "the same network as before", inter(12, 500), PURPLE, g, "mm")
    f.text((900, 160), f"All {TOTAL:,} tokens", inter(14, 700), INK, v(12.4))
    f.text((900, 181), "become vectors and go in together:", inter(12, 400), GREY, v(12.4))
    f.text((900, 198), "one forward pass", inter(12, 600), INK, v(12.4))
    f.text((900, 226), "The LLM sees tokens. It has no idea", inter(12, 400), GREY, v(13.2))
    f.text((900, 243), "which part you typed.", inter(12, 400), GREY, v(13.2))
    f.arrow((1040, 384), (1040, 414), PURPLE, 1, 1.8, prog=v(13.8, 0.3))
    f.text((1040, 432), "next token  →  the generation loop starts", inter(12, 600), PURPLE, v(14.0), "mm")

    # ---- skills: only the descriptions
    k = v(15.2)
    f.rrect((470, 556, 860, 622), 9, fill=GREEN_F, outline=GREEN, a=k, width=1.3)
    f.text((486, 575), "dcm-guide: only its one-line description is in here", inter(12.3, 700), GREEN, k)
    f.text((486, 594), "The full SKILL.md is added later, if the model", inter(11.8, 400), GREY, k)
    f.text((486, 610), "decides the task needs it (see the next pages)", inter(11.8, 400), GREY, k)

    # ---- conclusion
    c = v(18.8)
    f.rrect((880, 478, 1232, 560), 10, fill=DARK, a=c)
    f.text((1056, 502), "The context window is the prompt.", inter(13.5, 600), (255, 255, 255), c, "mm")
    f.text((1056, 524), f"You typed 9 of its {TOTAL:,} tokens.", inter(13.5, 600), (255, 255, 255), c, "mm")
    f.text((1056, 544), "numbers are illustrative", inter(10.5, 400), (170, 176, 190), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.6, 5.6, 6.8, 8.2, 9.4, 10.8, 12.3, 13.0, 14.4, 16.0, 17.8, 19.4, 21.0, 22.5], "prompt")
