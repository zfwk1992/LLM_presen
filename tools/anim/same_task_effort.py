"""10e: the same request and the same model at four effort levels. More effort = more thinking and more rounds.
All counts are illustrative."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, PURPLE, PURPLE_F, PURPLE_B,
                                ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import settings_header, captions, main, mix, GREEN, GREEN_F

END = 23.0
# level, dots, calls, thinking width per call, start time, what it does, input tokens (k), cost multiple
LANES = [
    ("low", 1, 4, 6, 3.2, "loads the skill, runs the script, checks Os/Rte. Skips the spec lookup", 68, "0.6×"),
    ("medium", 2, 6, 14, 5.8, "the session you just saw: all five workflow steps", 113, "1×"),
    ("high", 3, 9, 20, 8.8, "also reads the PduR and ComM config and re-checks the spec", 216, "1.9×"),
    ("max", 5, 14, 26, 11.4, "also reads the Dcm sources, verifies each step, lists open questions", 504, "4.5×"),
]
LY = [128, 226, 324, 422]
CAPS = [
    (0.8, 1, "Same request, same model: only the effort level differs"),
    (3.0, 2, "Low: few steps and little thinking. It skips the spec lookup"),
    (5.6, 3, "Medium: the session you just saw, all five workflow steps"),
    (8.6, 4, "High and max: more thinking, more checks, more calls"),
    (15.6, 5, "Tokens grow faster than calls: every call re-sends a longer prompt"),
    (19.0, 6, "Effort = how much work, not how smart. Pick it to fit the task"),
]


def render(t):
    f = Frame(t)
    v = f.v
    settings_header(f, "Same Request, Same Model, Four Effort Levels")

    for li, (name, dots, n, think, ts, what, ktok, mult) in enumerate(LANES):
        y0 = LY[li]
        a = v(0.9 + 0.15 * li)
        f.rrect((56, y0, 1232, y0 + 88), 10, fill=(250, 250, 251), outline=PANEL_B, a=a, width=1)
        f.text((72, y0 + 26), name, mono(16), INK, a)
        for d in range(5):
            f.circle((76 + d * 11, y0 + 48), 3.4, fill=ORANGE if d < dots else None, outline=ORANGE, a=a, width=1.2)
        f.text((72, y0 + 70), f"{n} LLM calls", mono(10.5), GREY, v(ts + 0.25 * n))
        # the calls: purple = thinking, orange = the tool call it writes, green = the final answer
        x = 218
        for k in range(n):
            ka = v(ts + 0.25 * k, 0.3) * a
            last = k == n - 1
            f.rrect((x, y0 + 16, x + think, y0 + 50), 4, fill=PURPLE_F, outline=PURPLE_B, a=ka, width=1.2)
            f.rrect((x + think, y0 + 16, x + think + 16, y0 + 50), 4, fill=GREEN_F if last else ORANGE_F,
                    outline=GREEN if last else ORANGE, a=ka, width=1.2)
            x += think + 20
        f.text((218, y0 + 70), what, inter(11.3, 400), INK, v(ts + 0.25 * n))
        # tokens and cost
        ca = v(15.8 + 0.25 * li)
        g = ease((t - (16.0 + 0.25 * li)) / 0.8)
        f.rrect((930, y0 + 20, 930 + max(3, 210 * ktok / 504 * g), y0 + 42), 4, fill=(203, 213, 225), outline=(148, 163, 184), a=ca, width=1.1)
        f.text((930, y0 + 60), f"{round(ktok * g)}k input tokens", mono(11), INK, ca)
        f.text((1222, y0 + 60), "cost ≈ " + mult, inter(13, 700), INK, ca, "rm")

    lg = v(3.4)
    f.rrect((218, 522, 232, 536), 3, fill=PURPLE_F, outline=PURPLE_B, a=lg, width=1.2)
    f.text((240, 529), "thinking", inter(11, 400), GREY, lg)
    f.rrect((312, 522, 326, 536), 3, fill=ORANGE_F, outline=ORANGE, a=lg, width=1.2)
    f.text((334, 529), "a tool call  (then the harness runs it)", inter(11, 400), GREY, lg)
    f.rrect((566, 522, 580, 536), 3, fill=GREEN_F, outline=GREEN, a=lg, width=1.2)
    f.text((588, 529), "the final answer", inter(11, 400), GREY, lg)
    f.text((1232, 529), "all counts are illustrative", inter(10.5, 400), LIGHT, lg, "rm")

    n5 = v(17.2)
    f.text((218, 556), "From medium to max:  calls × 2.3,  tokens × 4.5.", inter(12.5, 700), INK, n5)
    f.text((218, 576), "Each extra call re-sends everything gathered so far, so later calls are the expensive ones.", inter(11.5, 400), GREY, n5)
    c = v(19.2)
    f.rrect((56, 594, 1232, 636), 10, fill=DARK, a=c)
    f.text((644, 606), "Effort changes how many rounds and how much thinking.  It does not change the model.",
           inter(12.5, 600), (255, 255, 255), c, "mm")
    f.text((644, 624), "A plan for an unfamiliar integration: medium or high.   A one-line fix: low.",
           inter(11.5, 400), (200, 205, 215), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.4, 4.0, 5.2, 6.6, 8.0, 9.6, 11.0, 12.6, 14.4, 16.2, 17.4, 18.6, 20.4, 23.0], "effort")
