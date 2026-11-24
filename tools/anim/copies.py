"""02e: one small network, used once per token (same weights), linked by attention, stacked in layers."""
from PIL import Image
from inside_transformer import (Frame, inter, ease, clamp, strip_colours, INK, GREY, LIGHT, PURPLE, PURPLE_F, PURPLE_B,
                                PURPLE_HI, ORANGE, DARK, W, H)
from gifout import header, chip, captions, main, mix

END = 22.5
TOK = ["The", "·ECU", "·reads", "·the", "·CAN"]
CX = [300, 430, 560, 690, 820]
CAPS = [
    (0.8, 1, "One token: its vector of d numbers goes through one small network"),
    (5.0, 2, "Five tokens: the same network is used five times, at the same time"),
    (9.6, 3, "Attention links the copies: each token reads the ones before it"),
    (14.6, 4, "Attention + MLP is one layer. All columns pass layer after layer"),
    (18.2, 5, "The last column has seen everything: its output gives the next token"),
]


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "One Network, Copied for Every Token")
    lab = inter(12, 500)

    # ---- layer box and the top-to-bottom sweep sit behind everything else
    L = v(9.7)
    f.rrect((236, 212, 884, 386), 12, fill=(250, 248, 254), outline=PURPLE_B, a=L)
    for (t0, t1, y0, y1) in ((16.0, 17.2, 216, 366), (17.2, 17.7, 452, 464)):
        s = (t - t0) / (t1 - t0)
        if 0 < s < 1:
            y = y0 + (y1 - y0) * s
            f.rrect((240, y, 880, y + 16), 6, fill=PURPLE_HI, a=0.55 * (1 - abs(s - 0.5) * 1.4))
    # shared weights: one dotted line running through all five MLP boxes
    sw = v(5.2)
    x = CX[0] - 44
    while x < 930:
        f.line((x, 325), (min(x + 4, 930), 325), PURPLE, 0.55 * sw, 1.3)
        x += 9

    # ---- left labels
    f.text((56, 140), "tokens", lab, GREY, v(0.9))
    f.text((56, 186), "vectors", lab, GREY, v(1.3))
    f.text((56, 232), "Layer 1", inter(13, 700), PURPLE, L)
    f.text((56, 262), "attention", lab, GREY, v(9.9))
    f.text((56, 325), "MLP", lab, GREY, v(2.4))
    f.text((CX[0] + 56, 186), "←  d numbers wide", inter(11.5, 600), ORANGE, v(1.7) * (1 - v(4.9, 0.3)))

    # ---- columns
    for i, cx in enumerate(CX):
        b = 0.9 if i == 0 else 5.3 + 0.32 * (i - 1)
        t_strip, t_in, t_mlp, t_out = (b + 0.5, b + 1.0, b + 1.5, b + 2.4) if i == 0 else (b + 0.12, b + 0.25, b + 0.4, b + 0.65)
        chip(f, cx, 140, TOK[i], v(b))
        f.arrow((cx, 158), (cx, 175), LIGHT, 1, 1.3, prog=v(t_strip - 0.1, 0.25), head=4)
        f.strip(cx, 178, strip_colours(i, 1), v(t_strip))
        f.arrow((cx, 197), (cx, 302), LIGHT, 1, 1.3, prog=v(t_in, 0.4), head=4)
        m = v(t_mlp, 0.35)
        grow = 5 * (1 - m)
        hot = clamp(1 - abs(t - (t_mlp + 0.25)) / 0.3)
        f.rrect((cx - 40 - grow, 305 - grow, cx + 40 + grow, 345 + grow), 7, fill=mix(PURPLE_F, PURPLE_HI, hot), outline=PURPLE, a=m)
        f.text((cx, 325 - 6 * v(5.2)), "MLP", inter(12.5, 700), PURPLE, m, "mm")
        f.text((cx, 334), "same weights", inter(9.5, 500), PURPLE, m * v(5.2), "mm")
        f.arrow((cx, 347), (cx, 395), LIGHT, 1, 1.3, prog=v(t_out - 0.15, 0.3), head=4)
        f.strip(cx, 398, strip_colours(i, 2), v(t_out))

    # ---- attention: each column reads the columns before it (never the other way)
    for j in range(1, 5):
        for i in range(j):
            f.arrow((CX[i], 246), (CX[j] - 5, 280), PURPLE, 0.8, 1.5, prog=v(10.5 + 0.55 * (j - 1), 0.5), head=4.5)
    for i, cx in enumerate(CX):
        n = v(9.9 + 0.05 * i)
        f.circle((cx, 240), 5, fill=(255, 255, 255), outline=PURPLE, a=n)
        f.circle((cx, 284), 5, fill=(255, 255, 255), outline=PURPLE, a=n)

    # ---- more layers
    d4 = v(14.8)
    for k in range(3):
        f.circle((560, 424 + 6 * k), 1.6, fill=PURPLE_B, a=d4)
    f.text((578, 430), "…  N layers, each with its own weights", inter(12, 400), GREY, d4)
    LN = v(15.1)
    f.rrect((236, 446, 884, 476), 9, fill=PURPLE_F, outline=PURPLE_B, a=LN)
    f.text((56, 461), "Layer N", inter(13, 700), PURPLE, LN)
    f.text((560, 461), "attention  +  MLP", inter(12.5, 600), PURPLE, LN, "mm")
    f.text((56, 496), "final vectors", lab, GREY, v(15.5))
    for i, cx in enumerate(CX):
        f.strip(cx, 488, strip_colours(i, 3), v(15.5 + 0.08 * i))

    # ---- next token from the last column
    h5 = v(18.4)
    f.rrect((CX[4] - 53, 483, CX[4] + 53, 509), 6, outline=ORANGE, a=h5, width=2)
    f.arrow((CX[4], 512), (CX[4], 541), ORANGE, 1, 1.7, prog=v(18.8, 0.35))
    chip(f, CX[4], 560, "·bus", v(19.2), orange=True)
    f.text((CX[4] - 44, 560), "matched against every vocabulary token  →  next token", inter(12, 500), GREY, v(19.4), "rm")

    # ---- right-hand notes
    nA = v(1.6)
    f.text((930, 136), "Width = d", inter(14, 700), INK, nA)
    f.text((930, 157), "the size of one vector,", inter(12, 400), GREY, nA)
    f.text((930, 174), "not the number of tokens", inter(12, 400), GREY, nA)
    nC = v(10.3)
    f.text((930, 216), "Attention = the links", inter(14, 700), PURPLE, nC)
    f.text((930, 237), "each token reads the tokens before it;", inter(12, 400), GREY, nC)
    f.text((930, 254), "earlier tokens never read later ones", inter(12, 400), GREY, nC)
    f.rrect((930, 298, 1200, 352), 9, fill=PURPLE_F, outline=PURPLE, a=sw)
    f.text((1065, 316), "one set of weights", inter(13.5, 700), PURPLE, sw, "mm")
    f.text((1065, 335), "for this layer", inter(11, 500), PURPLE, sw, "mm")
    f.text((930, 372), "stored once, used in every column", inter(12, 400), GREY, v(6.6))
    f.text((930, 389), "5 tokens  →  5 columns, no extra weights", inter(12, 400), GREY, v(7.2))
    nD = v(15.2)
    f.text((930, 436), "Layer by layer", inter(14, 700), INK, nD)
    f.text((930, 457), "every column passes layer 1,", inter(12, 400), GREY, nD)
    f.text((930, 474), "then every column passes layer 2, …", inter(12, 400), GREY, nD)
    c7 = v(20.6)
    f.rrect((930, 534, 1232, 592), 9, fill=DARK, a=c7)
    f.text((1081, 553), "One set of weights.", inter(13, 600), (255, 255, 255), c7, "mm")
    f.text((1081, 573), "One column per token.", inter(13, 600), (255, 255, 255), c7, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [3.0, 4.6, 6.2, 8.8, 10.8, 12.4, 14.0, 15.6, 16.6, 17.5, 19.0, 20.0, 21.2, 22.5], "copies")
