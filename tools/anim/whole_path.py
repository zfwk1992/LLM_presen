"""The whole path in one picture: tokens -> IDs -> vectors -> Transformer -> probabilities -> one token -> back to the input."""
import os, sys
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, strip_colours, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                     PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H, FPS, S)

END = 23.5
TOK = ["The", "·ECU", "·reads", "·the", "·CAN", "·bus"]
IDS = ["791", "29012", "16181", "279", "20644", "5951"]
ROW = [190, 232, 274, 316, 358, 400]
XT, XI, XV, XO = 150, 268, 388, 742          # tokens, IDs, vectors, output vectors
BX0, BX1 = 478, 652                            # transformer box
SCORES = [("·bus", 58), ("·frame", 21), ("·message", 12), ("·signal", 6)]
CAPS = [
    (0.8, 1, "The input is a list of tokens; each token has an ID"),
    (3.6, 2, "Each ID is looked up: n tokens become n vectors"),
    (6.4, 3, "All n vectors go in together: one forward pass, not token by token"),
    (9.2, 4, "Each output vector predicts the token after it: only the last is new"),
    (11.8, 5, "That one vector is matched against every token: one score each"),
    (14.6, 6, "One token is picked and appended to the input"),
    (17.8, 7, "Next round: n + 1 vectors, one more forward pass. That is the loop"),
]


def chip(f, cx, cy, tok, a, orange=False):
    fm = mono(17)
    w = fm.getlength(tok) / S + 20
    col, fill = (ORANGE, ORANGE_F) if orange else (BLUE, BLUE_F)
    f.rrect((cx - w / 2, cy - 15, cx + w / 2, cy + 15), 6, fill=fill, outline=col, a=a)
    f.text((cx, cy), tok, fm, col, a, "mm")
    return w


def render(t):
    f = Frame(t)
    v = f.v
    a0 = v(0.1, 0.5)
    f.spaced((56, 45), "LLM FUNDAMENTALS", inter(12, 700), BLUE, a0, 1.7)
    f.text((56, 77), "From Tokens to the Next Token: the Whole Path", inter(30, 700), INK, a0)
    hd, tag = inter(12.5, 700), inter(11.5, 400)

    def row_times(i):  # the 6th row arrives in the second round
        if i < 5:
            return 0.9 + 0.12 * i, 1.7 + 0.12 * i, 3.9 + 0.12 * i, 6.9 + 0.06 * i, 9.4 + 0.1 * i
        return 17.9, 18.4, 18.9, 19.3, 19.8

    # ---- headers and shape tags
    f.text((XT, 150), "tokens", hd, INK, v(0.9), "mm")
    f.text((XI, 150), "token IDs", hd, INK, v(1.6), "mm")
    f.text((XV, 150), "vectors", hd, INK, v(3.8), "mm")
    f.text(((BX0 + BX1) / 2, 150), "Transformer", hd, PURPLE, v(6.5), "mm")
    f.text((XO, 150), "output vectors", hd, INK, v(9.3), "mm")
    grow = v(18.9, 0.5)
    ty = 398 + 42 * grow
    n_txt = "n = 6" if t > 18.2 else "n = 5"
    f.text((XT, ty), n_txt, tag, GREY, v(1.3), "mm")
    f.text((XI, ty), "n integers", tag, GREY, v(2.4), "mm")
    f.text((XV, ty), "n × d numbers", tag, GREY, v(4.6), "mm")
    f.text(((BX0 + BX1) / 2, ty), "same weights every round", tag, GREY, v(7.0), "mm")
    f.text((XO, ty), "n × d numbers", tag, GREY, v(10.0), "mm")

    # ---- transformer box
    tb = v(6.5)
    by1 = 380 + 42 * grow
    f.rrect((BX0, 166, BX1, by1), 12, fill=PURPLE_F, outline=PURPLE_B, a=tb)
    sweep = (t - 7.5) / 1.3 if t < 17 else (t - 19.2) / 0.9
    if 0 < sweep < 1:
        x = BX0 + 8 + (BX1 - BX0 - 46) * sweep
        f.rrect((x, 174, x + 30, by1 - 8), 8, fill=PURPLE_HI, a=tb * (1 - abs(sweep - 0.5) * 1.2))
    # which forward pass this is: the whole input goes through once per generated token
    second = ease((t - 19.2) / 0.4)
    bcx = (BX0 + BX1) / 2
    f.rrect((bcx - 62, 184, bcx + 62, 208), 12, fill=PURPLE, a=tb)
    f.text((bcx, 196), "forward pass #1", inter(11.5, 700), (255, 255, 255), tb * (1 - second), "mm")
    f.text((bcx, 196), "forward pass #2", inter(11.5, 700), (255, 255, 255), tb * second, "mm")
    f.text((bcx, 226), "whole input at once", inter(11, 500), PURPLE, tb, "mm")
    f.text(((BX0 + BX1) / 2, 262), "N layers", inter(14, 700), PURPLE, tb, "mm")
    f.text(((BX0 + BX1) / 2, 283), "attention + MLP", inter(12, 500), PURPLE, tb, "mm")
    note = v(7.0)
    f.text((433, 128), "all together, straight in", inter(11.5, 700), ORANGE, note, "mm")
    f.line((433, 137), (433, 172), ORANGE, 0.55 * note, 1)

    # ---- rows
    dim_old = 1 - 0.68 * v(10.3)            # rows 1..4 of the output fade back: only the last is used
    move = v(19.9)                           # highlight moves from row 5 to row 6
    for i in range(6):
        t_tok, t_id, t_vec, t_in, t_out = row_times(i)
        y = ROW[i]
        a = v(t_tok)
        w = chip(f, XT, y, TOK[i], a, orange=(i == 5))
        f.arrow((XT + w / 2 + 6, y), (XI - 34, y), LIGHT, 1, 1.3, prog=v(t_id - 0.2, 0.3), head=4)
        f.text((XI, y), IDS[i], mono(14), INK, v(t_id), "mm")
        f.arrow((XI + 30, y), (XV - 54, y), LIGHT, 1, 1.3, prog=v(t_vec - 0.2, 0.3), head=4)
        f.strip(XV, y - 8, strip_colours(i % 5, 1 if i < 5 else 0), v(t_vec))
        f.arrow((XV + 53, y), (BX0 - 3, y), LIGHT, 1, 1.3, prog=v(t_in, 0.35), head=4)
        f.arrow((BX1 + 3, y), (XO - 54, y), LIGHT, 1, 1.3, prog=v(t_out - 0.2, 0.3), head=4)
        if i < 4:
            oa = v(t_out) * dim_old
        elif i == 4:
            oa = v(t_out) * (1 - 0.68 * move)
        else:
            oa = v(t_out)
        f.strip(XO, y - 8, strip_colours(i % 5, 3 if i < 5 else 2), oa)
    hy = ROW[4] + 42 * move
    f.rrect((XO - 53, hy - 13, XO + 53, hy + 13), 6, outline=ORANGE, a=v(10.5), width=2)

    # ---- probabilities
    # The one output vector is not a token. It is matched against the vector of EVERY vocabulary token,
    # which gives one score per token; the scores become probabilities.
    f.arrow((XO + 57, hy), (818, hy), ORANGE, 1, 1.7, prog=v(11.9, 0.35))
    p5 = v(12.1)
    f.rrect((822, 226, 1092, 424), 10, fill=PANEL, outline=PANEL_B, a=p5)
    f.text((838, 245), "matched against every token", hd, INK, p5)
    f.text((838, 262), "1 output vector  →  one score per token", inter(10.8, 400), GREY, p5)
    tiny = inter(10, 600)
    f.text((838, 284), "TOKEN", tiny, LIGHT, p5)
    f.text((918, 284), "ITS VECTOR", tiny, LIGHT, p5)
    f.text((996, 284), "PROBABILITY", tiny, LIGHT, p5)
    fade2 = 1 - 0.7 * v(20.2)
    pick = v(14.8)
    f.rrect((830, 295, 1084, 317), 5, fill=ORANGE_F, outline=ORANGE, a=pick * fade2, width=1.3)
    for k, (tok, pct) in enumerate(SCORES):
        y = 306 + 23 * k
        a = v(12.3 + 0.12 * k) * fade2
        g = ease((t - (12.9 + 0.12 * k)) / 0.7)
        col = ORANGE if (k == 0 and t > 14.8) else (157, 123, 226)
        f.text((838, y), tok, mono(12.5), INK, a)
        # the token's own vector: the best match looks like the output vector
        cols = strip_colours(4, 3) if k == 0 else strip_colours(k, 2)
        for c, cc in enumerate(cols):
            f.rrect((918 + c * 7.5, y - 6, 918 + c * 7.5 + 6.5, y + 6), 1.5, fill=cc, a=a)
        f.rrect((996, y - 6, 996 + max(3, 48 * pct / 58 * g), y + 6), 3, fill=col, a=a)
        f.text((996 + 48 * pct / 58 * g + 6, y), f"{round(pct * g)}%", mono(11.5), GREY, a)
    f.text((838, 400), "… one row for each of the ~100,000 tokens", inter(10.8, 400), LIGHT, v(13.2) * fade2)

    # ---- pick and loop back
    f.arrow((1094, 306), (1128, 306), ORANGE, 1, 1.7, prog=v(15.1, 0.3))
    f.text((1166, 281), "picked", tag, GREY, v(15.3), "mm")
    chip(f, 1166, 306, "·bus", v(15.3), orange=True)
    # dashed loop: down from the chip, left along the bottom, up into the token column
    pts = [(1166, 324), (1166, 492), (84, 492), (84, 400), (108, 400)]
    NS = len(pts) - 1
    seg = [((pts[k][0] - pts[k + 1][0]) ** 2 + (pts[k][1] - pts[k + 1][1]) ** 2) ** 0.5 for k in range(NS)]
    total = sum(seg)
    done = total * ease((t - 15.8) / 1.6)
    pos, last = 0.0, None
    for k in range(NS):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        n = int(seg[k] // 6)
        for j in range(n):
            s0, s1 = j * 6, j * 6 + 3.5
            if pos + s1 > done:
                break
            u0, u1 = s0 / seg[k], s1 / seg[k]
            f.line((x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0), (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1), ORANGE, 0.9, 1.6)
        pos += seg[k]
    if done >= total - 1:
        f.arrow((104, 400), (115, 400), ORANGE, 1, 1.6)
    f.text((658, 477), "appended to the input", inter(12, 700), ORANGE, v(16.6), "mm")

    # ---- conclusion
    c7 = v(21.0)
    f.rrect((372, 532, 908, 570), 9, fill=DARK, a=c7)
    f.text((640, 551), "Vectors in  →  probabilities out  →  one token  →  repeat", inter(14, 600), (255, 255, 255), c7, "mm")
    f.text((640, 592), "One forward pass per generated token. The prompt goes in all at once, not token by token.", inter(12, 600), INK, v(21.4), "mm")
    f.text((640, 613), "Cosine similarity is not a step on this path: it only describes the vector space.", inter(12, 400), GREY, v(21.8), "mm")

    # ---- caption pill
    for k, (st, num, txt) in enumerate(CAPS):
        nxt = CAPS[k + 1][0] if k + 1 < len(CAPS) else 1e9
        a = min(ease((t - st) / 0.3), 1 - ease((t - (nxt - 0.6)) / 0.3))
        if a <= 0.003:
            continue
        fc = inter(19, 500)
        tw = fc.getlength(txt) / S
        w = tw + 86
        x0 = 640 - w / 2
        f.rrect((x0, 657, x0 + w, 695), 19, fill=PANEL, outline=PANEL_B, a=a, width=1)
        f.circle((x0 + 22, 676), 4, fill=ORANGE, a=a)
        f.circle((x0 + 47, 676), 11, outline=INK, a=a, width=1.4)
        f.text((x0 + 47, 676.5), str(num), inter(13.5, 600), INK, a, "mm")
        f.text((x0 + 66, 676), txt, fc, INK, a)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    out = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        os.makedirs(out, exist_ok=True)
        for tt in [float(x) for x in sys.argv[3:]]:
            render(tt).save(os.path.join(out, f"whole_{tt:05.1f}.png"))
    else:
        n = int(END * FPS) + 1
        keys = [2.8, 5.6, 8.0, 9.0, 10.4, 11.4, 13.6, 15.5, 16.6, 17.6, 19.0, 20.3, 21.6, 23.5]
        mosaic = Image.new("RGB", (W, H * len(keys)), (255, 255, 255))
        for k, tk in enumerate(keys):
            mosaic.paste(render(tk), (0, H * k))
        pal = mosaic.quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pl = pal.getpalette()[:765]
        for key in (ORANGE, BLUE, PURPLE):
            j = min(range(255), key=lambda q: sum((pl[q * 3 + c] - key[c]) ** 2 for c in range(3)))
            pl[j * 3:j * 3 + 3] = list(key)
        pal.putpalette(pl)
        ps = []
        for i in range(n):
            fr = Image.new("RGB", (W, H), (255, 255, 255)) if i < 2 else render(i / FPS)
            p = fr.quantize(palette=pal, dither=Image.Dither.NONE); p.info.clear()
            ps.append(p)
        ps[0].save(out, save_all=True, append_images=ps[1:], duration=[50] * (n - 1) + [3000], optimize=False, disposal=1)
        print("frames", n, "size %.2f MB" % (os.path.getsize(out) / 1e6))
