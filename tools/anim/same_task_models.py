"""10d: the same request run with three model sizes. Same prompts and tools; different speed, price per token and judgement.
All timings, costs and outcomes are illustrative."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import settings_header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F

END = 22.5
T0, RATE = 3.0, 12.0                      # animation second at which the clock starts; simulated seconds per animation second
X0, PXS = 262, 4.55                       # timeline origin and pixels per simulated second
# name, example, colour, fill, seconds per call, calls, index of a wasted call, cost units, result lines, result colour
LANES = [
    ("Smaller model", "e.g. Haiku", TEAL, TEAL_F, 5, 7, 3, 1,
     ["plan with 3 of 4 steps", "missed the Rte ports", "1 call wasted on the wrong file"], YELLOW),
    ("Mid-size model", "e.g. Sonnet", BLUE, BLUE_F, 12, 6, None, 3,
     ["complete plan, 4 steps", "followed all 5 workflow steps"], GREEN),
    ("Larger model", "e.g. Opus", ORANGE, ORANGE_F, 20, 6, None, 5,
     ["complete plan, 4 steps", "also flags a ComM dependency", "the workflow did not mention"], GREEN),
]
LY = [132, 262, 392]
CAPS = [
    (0.8, 1, "Same request, same harness, same skill: only the model differs"),
    (3.0, 2, "Each call takes longer with a bigger model: more compute per token"),
    (6.2, 3, "The smaller model is done first, but took a wrong turn and missed a step"),
    (9.4, 4, "The larger models follow the whole workflow; the largest notices more"),
    (14.6, 5, "The token counts are about the same. The price per token is not"),
    (18.4, 6, "Model = how good each decision is, and what each token costs"),
]


def render(t):
    f = Frame(t)
    v = f.v
    settings_header(f, "Same Request, Three Models")
    clock = max(0.0, (t - T0) * RATE)      # simulated seconds elapsed

    for li, (name, eg, col, fill, sec, n, wasted, cost, result, rcol) in enumerate(LANES):
        y0 = LY[li]
        a = v(0.9 + 0.2 * li)
        f.rrect((56, y0, 1232, y0 + 118), 10, fill=(250, 250, 251), outline=PANEL_B, a=a, width=1)
        f.text((72, y0 + 26), name, inter(15, 700), col, a)
        f.text((72, y0 + 48), eg, inter(11.5, 500), GREY, a)
        f.text((72, y0 + 76), f"{sec} s per call", mono(10.5), GREY, a)
        f.text((72, y0 + 94), f"{n} calls", mono(10.5), GREY, a)
        # calls on a common time axis
        for k in range(n):
            start = k * sec
            if clock <= start:
                break
            prog = clamp((clock - start) / (sec - 1))
            x = X0 + start * PXS
            wd = (sec - 1) * PXS * prog
            bad = wasted == k
            f.rrect((x, y0 + 30, x + wd, y0 + 66), 5, fill=(243, 232, 232) if bad else fill,
                    outline=(190, 80, 80) if bad else col, a=a, width=1.3)
            if prog > 0.6:
                last = k == n - 1
                f.text((x + (sec - 1) * PXS / 2, y0 + 48), "✓" if last else ("×" if bad else str(k + 1)),
                       inter(11.5, 700), GREEN if last else ((190, 80, 80) if bad else col), a, "mm")
        total = n * sec
        done = v(T0 + total / RATE, 0.3)
        f.text((X0 + total * PXS + 6, y0 + 48), f"done in {total} s", inter(11.5, 700), col, done)
        if wasted is not None:
            f.text((X0 + (wasted + 0.5) * sec * PXS - 2, y0 + 80), "wrong file", inter(9.5, 600), (190, 80, 80),
                   v(T0 + (wasted + 1) * sec / RATE), "mm")
        # result
        ra = v(T0 + total / RATE + 0.3)
        f.text((900, y0 + 22), "RESULT", inter(9.5, 700), LIGHT, ra)
        for j, line in enumerate(result):
            f.text((900, y0 + 42 + 17 * j), line, inter(11.8, 700 if j == 0 else 400), rcol if j == 0 else INK, ra)
        # cost
        ca = v(14.8 + 0.3 * li)
        f.text((1120, y0 + 22), "COST", inter(9.5, 700), LIGHT, ca)
        g = ease((t - (15.0 + 0.3 * li)) / 0.7)
        for u in range(cost):
            f.rrect((1120 + u * 21, y0 + 36, 1120 + u * 21 + 17, y0 + 36 + 26 * g), 3, fill=col, a=ca)
        f.text((1120, y0 + 84), f"≈ {cost}×", inter(13, 700), INK, ca)

    # time axis
    ax = v(2.6)
    for s in (0, 30, 60, 90, 120):
        x = X0 + s * PXS
        f.line((x, 512), (x, 518), LIGHT, ax, 1)
        f.text((x, 528), f"{s} s", mono(10), GREY, ax, "mm")
    if T0 < t < T0 + 10.2:
        cx = X0 + min(clock, 120) * PXS
        f.line((cx, 128), (cx, 512), (150, 156, 170), 0.6, 1)

    tk = v(15.4)
    f.text((262, 552), "Tokens processed in every lane:  about 113k input  +  under 1k output", inter(12.5, 600), INK, tk)
    f.text((262, 572), "(the prompt is re-sent at every call, so input dominates)", inter(11.5, 400), GREY, tk)
    c = v(18.6)
    f.rrect((56, 592, 1232, 634), 10, fill=DARK, a=c)
    f.text((644, 613), "The model sets the price and speed of every token, and how good each decision is.  It does not change the loop.",
           inter(12.5, 600), (255, 255, 255), c, "mm")
    f.text((1232, 552), "timings, costs and outcomes are illustrative", inter(10.5, 400), LIGHT, v(2.6), "rm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.4, 4.0, 5.4, 6.6, 8.0, 9.6, 11.0, 12.6, 13.6, 15.4, 16.6, 18.0, 20.0, 22.5], "models")
