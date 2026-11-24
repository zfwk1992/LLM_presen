"""02f: generation adds one column per new token; earlier columns are cached; the weights never change."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, strip_colours, INK, GREY, LIGHT, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, PANEL, PANEL_B, DARK, W, H)
from gifout import header, chip, captions, main, mix

END = 22.5
TOK = ["The", "·ECU", "·reads", "·the", "·CAN", "·bus", "·every"]
CX = [150 + 104 * i for i in range(7)]
BORN = [0.9] * 5 + [8.2, 15.4]          # when a column appears
CACHED = [7.8] * 5 + [15.0, 99]         # when it becomes "already computed"
ROWS = [(232, "Layer 1"), (296, "Layer 2"), (424, "Layer N")]
CAPS = [
    (0.8, 1, "The prompt: 5 tokens, 5 columns, all computed in one pass"),
    (4.6, 2, "The last column gives the next token"),
    (7.4, 3, "The new token becomes column 6: only this column is new work"),
    (11.0, 4, "It reads the saved results of the columns before it"),
    (14.6, 5, "Every new token adds one column: more to read, same weights"),
    (18.6, 6, "Longer context costs more per step; the network never changes"),
]


def lerp(a, b, m):
    return a + (b - a) * clamp(m)


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "A New Token Adds a Column")

    # ---- which forward pass
    p2, p3 = v(8.2, 0.4), v(15.4, 0.4)
    f.rrect((112, 108, 470, 132), 12, fill=PURPLE, a=v(0.9))
    for a, s in ((v(0.9) * (1 - p2), "forward pass #1  ·  5 columns computed together"),
                 (p2 * (1 - p3), "forward pass #2  ·  1 new column"),
                 (p3, "forward pass #3  ·  1 new column")):
        f.text((291, 120), s, inter(12, 700), (255, 255, 255), a, "mm")

    # ---- reads from the cache: horizontal lines behind the columns, into the new column
    for k, (t0, dur) in ((5, (11.2, 1.0)), (6, (16.3, 0.8))):
        pr = ease((t - t0) / dur)
        gone = 1 - v(CACHED[k], 0.4) if k == 5 else 1
        if pr > 0.01:
            for y, _ in ROWS:
                x1 = CX[0] + 38 + (CX[k] - 44 - CX[0] - 38) * pr
                f.line((CX[0] + 38, y), (x1, y), ORANGE, 0.85 * gone, 1.6)
                if pr > 0.97:
                    f.arrow((CX[k] - 50, y), (CX[k] - 39, y), ORANGE, gone, 1.6, head=5)

    # ---- columns
    for k, cx in enumerate(CX):
        a = v(BORN[k], 0.5)
        if a <= 0.003:
            continue
        c = v(CACHED[k], 0.5)
        new = k >= 5
        f.rrect((cx - 38, 196, cx + 38, 470), 10, fill=mix((250, 248, 254), (247, 248, 250), c),
                outline=mix(ORANGE if new else PURPLE_B, (209, 213, 219), c), a=a, width=1.8 if new else 1.5)
        for y, name in ROWS:
            f.rrect((cx - 30, y - 23, cx + 30, y + 23), 6, fill=mix(PURPLE_F, PANEL, c), outline=mix(PURPLE_B, PANEL_B, c), a=a, width=1.2)
            f.text((cx, y - 6), name, inter(10.5, 700), mix(PURPLE, LIGHT, c), a, "mm")
            f.text((cx, y + 8), "attn + MLP", inter(8.8, 500), mix(PURPLE, LIGHT, c), a, "mm")
        for j in range(3):
            f.circle((cx, 354 + 6 * j), 1.5, fill=mix(PURPLE_B, LIGHT, c), a=a)
        f.text((cx, 458), "saved", inter(9.5, 700), LIGHT, a * c, "mm")
        # sweep: the pass that computes this column
        t0, t1 = ((1.6, 3.0) if k < 5 else (9.0, 10.6) if k == 5 else (15.9, 17.2))
        s = (t - t0) / (t1 - t0)
        if 0 < s < 1:
            y = 202 + 246 * s
            f.rrect((cx - 34, y, cx + 34, y + 14), 5, fill=PURPLE_HI, a=0.7 * (1 - abs(s - 0.5) * 1.3))
        # output vector under the column
        t_out = 3.3 if k < 5 else (12.6 if k == 5 else 17.4)
        cols = strip_colours(k % 5, 3 if k < 5 else 2)
        oa = v(t_out) * lerp(1, 0.35, v(4.9) if k < 4 else c)
        for q, cc in enumerate(cols):
            f.rrect((cx - 35.5 + q * 9, 482, cx - 35.5 + q * 9 + 8, 494), 2, fill=cc, a=oa)

    # ---- token chips: the prompt, then each generated token travels from "output" to "input"
    for k in range(5):
        chip(f, CX[k], 160, TOK[k], v(BORN[k]), size=15)
    for k, (t_pick, t_move, nxt) in ((4, (5.4, 7.4, "·bus")), (5, (13.4, 14.6, "·every")), (6, (18.0, 99, "·10"))):
        a = v(t_pick)
        if a <= 0.003:
            continue
        f.rrect((CX[k] - 37, 479, CX[k] + 37, 497), 5, outline=ORANGE, a=v(t_pick - 0.6) * (1 - v(t_move, 0.3)), width=1.8)
        f.arrow((CX[k], 499), (CX[k], 513), ORANGE, 1, 1.6, prog=v(t_pick - 0.3, 0.3) * (1 - v(t_move, 0.3)), head=4.5)
        m = ease((t - t_move) / 0.8)
        x = lerp(CX[k], CX[min(k + 1, 6)], m)
        y = lerp(532, 160, m)
        chip(f, x, y, nxt, a, orange=True, size=15)
        if m < 0.02:
            f.text((CX[k], 556), "next token", inter(11, 500), GREY, a, "mm")

    # ---- right panel: what this pass costs
    pa = v(1.2)
    f.rrect((880, 170, 1232, 330), 10, fill=PANEL, outline=PANEL_B, a=pa)
    f.text((896, 192), "This forward pass", inter(14, 700), INK, pa)
    rows = [("tokens in context", ("5", "6", "7")), ("columns computed now", ("5", "1", "1")),
            ("columns read from memory", ("0", "5", "6")), ("weights", ("same", "same", "same"))]
    for r, (name, vals) in enumerate(rows):
        y = 224 + 27 * r
        f.text((896, y), name, inter(12, 400), GREY, pa)
        for a, val in ((1 - p2, vals[0]), (p2 * (1 - p3), vals[1]), (p3, vals[2])):
            f.text((1216, y), val, inter(14, 700), PURPLE if r == 3 else INK, pa * a, "rm")
    n6 = v(18.9)
    f.text((880, 362), "Longer context", inter(14, 700), INK, n6)
    f.text((880, 383), "every new column has more columns to read,", inter(12, 400), GREY, n6)
    f.text((880, 400), "so each step costs a little more", inter(12, 400), GREY, n6)
    c7 = v(20.4)
    f.rrect((880, 428, 1232, 486), 9, fill=DARK, a=c7)
    f.text((1056, 447), "New token = new column.", inter(13, 600), (255, 255, 255), c7, "mm")
    f.text((1056, 467), "The weights stay the same.", inter(13, 600), (255, 255, 255), c7, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.2, 4.2, 6.6, 7.8, 9.8, 12.2, 13.8, 15.0, 16.6, 17.6, 18.4, 19.6, 21.0, 22.5], "addcol")
