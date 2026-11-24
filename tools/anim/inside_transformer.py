"""02c: how token vectors enter and flow through the Transformer. Same visual style as the other pages."""
import os, sys, random
from PIL import Image, ImageDraw, ImageFont
import matplotlib

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = os.path.join(HERE, "fonts", "Inter-var.ttf")
MONO = os.path.join(matplotlib.get_data_path(), "fonts", "ttf", "DejaVuSansMono.ttf")
S, W, H, FPS, END = 2, 1280, 720, 20, 23.0

INK, GREY, LIGHT = (31, 36, 48), (107, 114, 128), (156, 163, 175)
BLUE, BLUE_F = (47, 111, 235), (227, 236, 253)
PURPLE, PURPLE_F, PURPLE_B, PURPLE_HI = (124, 77, 214), (237, 231, 251), (149, 117, 222), (205, 190, 244)
ORANGE, ORANGE_F = (217, 119, 66), (250, 233, 224)
PANEL, PANEL_B, DARK = (243, 244, 246), (229, 231, 235), (29, 34, 48)
CELLS = [(93, 140, 235), (140, 173, 240), (190, 208, 245), (222, 231, 250), (247, 214, 198), (240, 184, 160), (232, 160, 128)]

_f = {}
def inter(size, w=400):
    k = ("i", size, w)
    if k not in _f:
        f = ImageFont.truetype(INTER, round(size * S)); f.set_variation_by_axes([min(32, max(14, size)), w]); _f[k] = f
    return _f[k]
def mono(size):
    k = ("m", size)
    if k not in _f:
        _f[k] = ImageFont.truetype(MONO, round(size * S))
    return _f[k]

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def P(v): return round(v * S)
def C(col, a): return (col[0], col[1], col[2], round(255 * clamp(a)))

TOK = ["The", "·ECU", "·reads", "·the", "·CAN"]
CX = [236, 372, 508, 644, 780]
ATT = [0.10, 0.38, 0.27, 0.07, 0.18]  # how much ·CAN reads from each token (illustrative)
SCORES = [("·bus", 58), ("·frame", 21), ("·message", 12), ("·signal", 6)]
CAPS = [
    (0.8, 1, "Each token ID is looked up: one vector per token"),
    (4.6, 2, "Position is added, so the model knows the word order"),
    (7.6, 3, "Attention: each vector pulls in information from earlier tokens"),
    (12.0, 4, "MLP: then every vector is transformed on its own"),
    (14.4, 5, "Repeat for N layers: same shape, richer meaning"),
    (17.2, 6, "The last vector is scored against every token in the vocabulary"),
    (20.6, None, "One forward pass, done. Next: the generation loop"),
]

def strip_colours(col, stage):
    r = random.Random(1000 + col * 17)
    base = [r.randrange(len(CELLS)) for _ in range(8)]
    if stage >= 1:
        r2 = random.Random(2000 + col * 31)
        for k in r2.sample(range(8), 3):
            base[k] = r2.randrange(len(CELLS))
    if stage >= 2:
        r3 = random.Random(3000 + col * 7 + stage * 101)
        base = [r3.randrange(len(CELLS)) for _ in range(8)]
    return [CELLS[i] for i in base]


class Frame:
    def __init__(self, t):
        self.t = t
        self.im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def v(self, t0, dur=0.4):
        return ease((self.t - t0) / dur)

    def text(self, xy, s, font, col, a=1.0, anchor="lm"):
        if a > 0.003:
            self.d.text((P(xy[0]), P(xy[1])), s, font=font, fill=C(col, a), anchor=anchor)

    def spaced(self, xy, s, font, col, a, gap):
        x = xy[0]
        for ch in s:
            self.text((x, xy[1]), ch, font, col, a)
            x += font.getlength(ch) / S + gap

    def rrect(self, box, r, fill=None, outline=None, a=1.0, width=1.5):
        if a <= 0.003:
            return
        b = [P(box[0]), P(box[1]), P(box[2]), P(box[3])]
        self.d.rounded_rectangle(b, radius=P(r), fill=C(fill, a) if fill else None,
                                 outline=C(outline, a) if outline else None, width=round(width * S))

    def line(self, p, q, col, a=1.0, width=1.5):
        if a > 0.003:
            self.d.line([P(p[0]), P(p[1]), P(q[0]), P(q[1])], fill=C(col, a), width=max(1, round(width * S)))

    def arrow(self, p, q, col, a=1.0, width=1.5, prog=1.0, head=5):
        if a <= 0.003 or prog <= 0.01:
            return
        x = p[0] + (q[0] - p[0]) * prog; y = p[1] + (q[1] - p[1]) * prog
        self.line(p, (x, y), col, a, width)
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = (dx * dx + dy * dy) ** 0.5 or 1
        ux, uy = dx / n, dy / n
        pts = [(x + ux * 1.5, y + uy * 1.5), (x - ux * head - uy * head * 0.6, y - uy * head + ux * head * 0.6),
               (x - ux * head + uy * head * 0.6, y - uy * head - ux * head * 0.6)]
        self.d.polygon([(P(a_), P(b_)) for a_, b_ in pts], fill=C(col, a))

    def circle(self, c, r, fill=None, outline=None, a=1.0, width=1.5):
        if a > 0.003:
            self.d.ellipse([P(c[0] - r), P(c[1] - r), P(c[0] + r), P(c[1] + r)], fill=C(fill, a) if fill else None,
                           outline=C(outline, a) if outline else None, width=round(width * S))

    def strip(self, cx, y, cols, a=1.0, dy=0.0):
        if a <= 0.003:
            return
        x0 = cx - 47.5
        for k, col in enumerate(cols):
            self.rrect((x0 + k * 12, y + dy, x0 + k * 12 + 11, y + 16 + dy), 2, fill=col, a=a)

    def strip_x(self, cx, y, c_old, c_new, m, a=1.0):
        cols = [tuple(round(o + (n - o) * m) for o, n in zip(co, cn)) for co, cn in zip(c_old, c_new)]
        self.strip(cx, y, cols, a)


def render(t):
    f = Frame(t)
    v = f.v
    a0 = v(0.1, 0.5)
    f.spaced((56, 45), "LLM FUNDAMENTALS", inter(12, 700), BLUE, a0, 1.7)
    f.text((56, 77), "From Vectors into the Transformer", inter(30, 700), INK, a0)

    lab = inter(12, 500)
    # ---- S1 tokens + embedding
    f.text((56, 140), "tokens", lab, GREY, v(0.9))
    for i, (tok, cx) in enumerate(zip(TOK, CX)):
        a = v(0.9 + 0.15 * i)
        fm = mono(19)
        w = fm.getlength(tok) / S + 22
        f.rrect((cx - w / 2, 123, cx + w / 2, 157), 7, fill=BLUE_F, outline=BLUE, a=a)
        if tok.startswith("·"):
            dw = fm.getlength("·") / S
            x0 = cx - (w - 22) / 2
            f.text((x0, 140), "·", fm, (140, 170, 235), a)
            f.text((x0 + dw, 140), tok[1:], fm, BLUE, a)
        else:
            f.text((cx, 140), tok, fm, BLUE, a, "mm")
        f.arrow((cx, 160), (cx, 182), LIGHT, 1.0, 1.4, prog=v(1.9 + 0.2 * i, 0.3))
        f.strip(cx, 186, strip_colours(i, 0), v(2.1 + 0.2 * i), dy=-6 * (1 - v(2.1 + 0.2 * i)))
    f.text((56, 194), "embedding", lab, GREY, v(1.9))
    n1 = v(3.1)
    f.text((890, 138), "5 tokens  →  5 vectors", inter(14, 700), INK, n1)
    f.text((890, 159), "each vector is a list of d numbers (thousands)", inter(12, 400), GREY, n1)
    f.text((890, 177), "nothing is compared yet: just a table lookup", inter(12, 400), GREY, n1)

    # ---- S2 position
    f.text((56, 240), "+ position", lab, GREY, v(4.9))
    for i, cx in enumerate(CX):
        a = v(4.9 + 0.12 * i)
        f.rrect((cx - 27, 209, cx + 27, 225), 8, fill=PANEL, outline=PANEL_B, a=a, width=1)
        f.text((cx, 217), f"+ pos {i + 1}", inter(10.5, 600), GREY, a, "mm")
        b = v(5.7 + 0.1 * i)
        f.strip_x(cx, 232, strip_colours(i, 0), strip_colours(i, 1), v(5.9 + 0.1 * i, 0.5), b)
    n2 = v(6.3)
    f.text((890, 222), "Order matters", inter(14, 700), INK, n2)
    f.text((890, 243), "“ECU reads CAN” ≠ “CAN reads ECU”", inter(12, 400), GREY, n2)

    # ---- S3 layer 1: attention
    L = v(7.7)
    f.rrect((176, 272, 846, 412), 12, fill=(250, 248, 254), outline=PURPLE_B, a=L)
    f.text((56, 290), "Layer 1", inter(13, 700), PURPLE, L)
    f.text((56, 321), "attention", lab, GREY, v(8.0))
    for i, cx in enumerate(CX):
        f.arrow((cx, 251), (cx, 287), LIGHT, 1.0, 1.4, prog=v(7.9 + 0.05 * i, 0.3))
    # faint lines: every position reads from itself and earlier positions
    for j in range(4):
        for i in range(j + 1):
            pr = v(8.4 + 0.08 * j, 0.5)
            x = CX[i] + (CX[j] - CX[i]) * pr; y = 300 + 42 * pr
            f.line((CX[i], 300), (x, y), PURPLE_B, 0.30 * clamp(pr * 3), 1)
    for i in range(5):
        pr = v(9.3 + 0.2 * i, 0.5)
        x = CX[i] + (CX[4] - CX[i]) * pr; y = 300 + 42 * pr
        f.line((CX[i], 300), (x, y), PURPLE, 0.9 * clamp(pr * 3), 1 + 9 * ATT[i])
    for i, cx in enumerate(CX):
        n = v(8.0 + 0.05 * i)
        f.circle((cx, 296), 5, fill=(255, 255, 255), outline=PURPLE, a=n)
        last = i == 4
        f.circle((cx, 346), 5.5 if last else 5, fill=PURPLE if last and t > 9.3 else (255, 255, 255), outline=PURPLE, a=n)
    n3 = v(9.8)
    f.rrect((890, 276, 1232, 408), 10, fill=(250, 248, 254), outline=PURPLE_B, a=n3, width=1.2)
    f.text((906, 296), "Where is similarity used?", inter(13.5, 700), PURPLE, n3)
    for k, s in enumerate(["Inside attention: the weight between two",
                           "tokens is a dot product of their vectors",
                           "(after learned projections).",
                           "It decides how much ·CAN reads from ·ECU."]):
        f.text((906, 320 + 19 * k), s, inter(12.3, 500 if k == 3 else 400), INK if k == 3 else GREY, n3)
    f.text((906, 398 - 4), "thicker line = larger weight", inter(11, 400), LIGHT, n3)

    # ---- S4 MLP
    f.text((56, 384), "MLP", lab, GREY, v(12.1))
    for i, cx in enumerate(CX):
        a = v(12.1 + 0.05 * i)
        pulse = clamp(1 - abs(t - (12.5 + 0.18 * i)) / 0.25)
        fill = tuple(round(p + (h - p) * pulse) for p, h in zip(PURPLE_F, PURPLE_HI))
        f.arrow((cx, 352), (cx, 369), PURPLE_B, a, 1.2, head=4)
        f.rrect((cx - 32, 371, cx + 32, 397), 6, fill=fill, outline=PURPLE_B, a=a, width=1.2)
        f.text((cx, 384), "MLP", inter(11, 700), PURPLE, a, "mm")
        f.arrow((cx, 398), (cx, 421), LIGHT, 1.0, 1.4, prog=v(13.0 + 0.1 * i, 0.3))
        f.strip(cx, 424, strip_colours(i, 2), v(13.2 + 0.1 * i), dy=-5 * (1 - v(13.2 + 0.1 * i)))

    # ---- S5 N layers
    d5 = v(14.6)
    for k in range(3):
        f.circle((508, 449 + 6 * k), 1.6, fill=PURPLE_B, a=d5)
    f.text((526, 455), "…  the same two steps, layer after layer", inter(12, 400), GREY, d5)
    LN = v(15.1)
    f.rrect((176, 472, 846, 502), 9, fill=PURPLE_F, outline=PURPLE_B, a=LN)
    f.text((56, 487), "Layer N", inter(13, 700), PURPLE, LN)
    f.text((511, 487), "attention  +  MLP", inter(12.5, 600), PURPLE, LN, "mm")
    for i, cx in enumerate(CX):
        f.strip(cx, 514, strip_colours(i, 3), v(15.7 + 0.1 * i), dy=-5 * (1 - v(15.7 + 0.1 * i)))
    f.text((56, 522), "final vectors", lab, GREY, v(15.7))
    f.text((508, 549), "shape never changes:  n vectors  ×  d numbers", inter(12, 400), GREY, v(16.2), "mm")

    # ---- S6 output
    h6 = v(17.4)
    f.rrect((CX[4] - 53, 509, CX[4] + 53, 535), 6, outline=ORANGE, a=h6, width=2)
    f.arrow((836, 522), (886, 522), ORANGE, 1.0, 1.8, prog=v(17.7, 0.35))
    p6 = v(17.9)
    f.rrect((890, 440, 1232, 604), 10, fill=PANEL, outline=PANEL_B, a=p6)
    f.text((906, 461), "Next-token scores", inter(14, 700), INK, p6)
    f.text((906, 480), "final vector · each token's vector  →  softmax", inter(11.5, 400), GREY, p6)
    for k, (tok, pct) in enumerate(SCORES):
        y = 506 + 21 * k
        a = v(18.2 + 0.12 * k)
        g = ease((t - (18.5 + 0.12 * k)) / 0.7)
        f.text((906, y), tok, mono(13), INK, a)
        f.rrect((1000, y - 7, 1000 + max(3, 150 * pct / 58 * g), y + 7), 3, fill=(157, 123, 226), a=a)
        f.text((1000 + 150 * pct / 58 * g + 8, y), f"{round(pct * g)}%", mono(11.5), GREY, a)
    f.text((906, 591), "… every other token in the vocabulary", inter(11, 400), LIGHT, v(19.0))

    # ---- S7 conclusion
    c7 = v(20.8)
    f.rrect((890, 612, 1232, 646), 8, fill=DARK, a=c7)
    f.text((1061, 629), "No similarity step in between: vectors go straight in.", inter(12, 600), (255, 255, 255), c7, "mm")

    # ---- caption pill
    for k, (st, num, txt) in enumerate(CAPS):
        nxt = CAPS[k + 1][0] if k + 1 < len(CAPS) else 1e9
        a = min(ease((t - st) / 0.3), 1 - ease((t - (nxt - 0.6)) / 0.3))
        if a <= 0.003:
            continue
        fc = inter(19, 500)
        tw = fc.getlength(txt) / S
        extra = 30 if num else 0
        w = tw + 56 + extra
        x0 = 640 - w / 2
        f.rrect((x0, 657, x0 + w, 695), 19, fill=PANEL, outline=PANEL_B, a=a, width=1)
        f.circle((x0 + 22, 676), 4, fill=ORANGE, a=a)
        x = x0 + 36
        if num:
            f.circle((x + 11, 676), 11, outline=INK, a=a, width=1.4)
            f.text((x + 11, 676.5), str(num), inter(13.5, 600), INK, a, "mm")
            x += 30
        f.text((x, 676), txt, fc, INK, a)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    out = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        os.makedirs(out, exist_ok=True)
        for t in [float(x) for x in sys.argv[3:]]:
            render(t).save(os.path.join(out, f"c02_{t:05.1f}.png"))
    else:
        n = int(END * FPS) + 1
        # one shared palette for every frame, so unchanged pixels stay identical and the file stays small
        keys = [3.8, 5.3, 6.9, 9.0, 10.5, 11.5, 12.6, 13.6, 15.4, 16.6, 18.6, 19.6, 21.0, 23.0]
        mosaic = Image.new("RGB", (W, H * len(keys)), (255, 255, 255))
        for k, tk in enumerate(keys):
            mosaic.paste(render(tk), (0, H * k))
        pal = mosaic.quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pl = pal.getpalette()[:765]
        for key in (ORANGE, BLUE, PURPLE):  # keep the accent colours exact
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
