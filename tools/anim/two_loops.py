"""04e: the agent loop is a program (the harness) calling the LLM again and again; inside each call runs the generation loop.
Same session as the previous pages; calls 4 and 5 are skipped in the drawing to keep it readable."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, PURPLE, PURPLE_F, PURPLE_B,
                                PURPLE_HI, ORANGE, PANEL, PANEL_B, DARK, W, H)
from gifout import example_header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F, SLATE, SLATE_F

END = 23.5
LX = [330, 560, 790, 1020]                      # LLM calls drawn
HX = [445, 675, 905, 1140]                      # harness actions after each call
CALLNO = [1, 2, 3, 6]
WROTE = ['Skill("dcm-integration")', 'Bash("extract_dcm_config")', 'search_spec("Dcm …")', "the integration plan"]
NTOK = ["24 tokens, one by one", "31 tokens, one by one", "22 tokens, one by one", "260 tokens, one by one"]
ACT = [("run Skill", "SKILL.md  ·  +2.1k"), ("run Bash", "script output  ·  +0.9k"), ("run search_spec", "3 passages  ·  +1.8k"),
       ("show answer", "no tool call: stop")]
SIZE = ["14.7k", "16.8k", "17.7k", "22.5k"]
# times: prompt arrow down, call box, generating pulse, reply arrow up, harness action
TD = [1.6, 8.1, 11.7, 14.4]
TC = [2.0, 8.5, 12.0, 14.8]
TP = [3.6, 8.8, 12.2, 15.0]
TU = [5.7, 10.0, 13.2, 16.6]
TA = [6.1, 10.4, 13.6, 17.0]
BASE = (300, SLATE, SLATE_F)
ADDED = [(43, GREEN, GREEN_F), (18, YELLOW, YELLOW_F), (37, TEAL, TEAL_F), (49, YELLOW, YELLOW_F), (12, YELLOW, YELLOW_F)]
NADD = [0, 1, 2, 5]                              # how many results each drawn call already has
CAPS = [
    (0.8, 1, "The harness builds the prompt and calls the LLM"),
    (3.4, 2, "Inside the call, the generation loop writes a tool call token by token"),
    (5.6, 3, "The harness runs the tool and adds the result to the prompt"),
    (8.0, 4, "Then it calls the LLM again, sending everything so far"),
    (11.6, 5, "This repeats until the reply contains no tool call"),
    (18.4, 6, "Two loops: the harness loops over LLM calls, the LLM loops over tokens"),
]


def render(t):
    f = Frame(t)
    v = f.v
    example_header(f, "Two Loops: the Harness Around the LLM", 5)

    # ---- two lanes
    la = v(0.6)
    f.rrect((56, 126, 1232, 236), 12, fill=(240, 249, 250), a=la)
    f.rrect((56, 268, 1232, 378), 12, fill=(248, 245, 254), a=la)
    f.text((72, 150), "HARNESS", inter(12, 700), TEAL, la)
    f.text((72, 168), "Claude Code", inter(11.5, 500), GREY, la)
    f.text((72, 184), "a program", inter(11.5, 400), GREY, la)
    f.text((72, 292), "LLM", inter(12, 700), PURPLE, la)
    f.text((72, 310), "predicts tokens,", inter(11.5, 400), GREY, la)
    f.text((72, 326), "nothing else", inter(11.5, 400), GREY, la)

    def hbox(cx, title, sub, a, final=False):
        col, fill = (GREEN, GREEN_F) if final else (TEAL, TEAL_F)
        f.rrect((cx - 66, 151, cx + 66, 211), 9, fill=fill, outline=col, a=a, width=1.6)
        f.text((cx, 172), title, inter(12.5, 700), col, a, "mm")
        f.text((cx, 192), sub, inter(10, 500), GREY, a, "mm")

    hbox(236, "build prompt", "join all the parts", v(1.0))
    for k in range(4):
        src = 236 if k == 0 else HX[k - 1]
        # prompt goes down to the LLM
        f.arrow((src + 20, 213), (LX[k] - 34, 283), TEAL, 1, 1.7, prog=v(TD[k], 0.4))
        mx = (src + 20 + LX[k] - 34) / 2
        f.text((mx + 9, 248), SIZE[k], mono(10.5), TEAL, v(TD[k] + 0.2), "lm")
        # the call
        a = v(TC[k])
        f.rrect((LX[k] - 78, 285, LX[k] + 78, 361), 10, fill=PURPLE_F, outline=PURPLE, a=a, width=1.6)
        s = (t - TP[k]) / 1.3
        if 0 < s < 1:
            f.rrect((LX[k] - 72 + 118 * s, 291, LX[k] - 46 + 118 * s, 355), 6, fill=PURPLE_HI, a=0.8 * (1 - abs(s - 0.5) * 1.3))
        f.text((LX[k], 301), f"LLM call #{CALLNO[k]}", inter(12.5, 700), PURPLE, a, "mm")
        w = v(TP[k] + 0.9)
        f.text((LX[k], 323), WROTE[k], mono(9.6) if k < 3 else inter(11.5, 600), ORANGE if k < 3 else GREEN, w, "mm")
        f.text((LX[k], 344), NTOK[k], inter(9.8, 500), GREY, w, "mm")
        # reply goes up to the harness
        col = ORANGE if k < 3 else GREEN
        f.arrow((LX[k] + 34, 283), (HX[k] - 20, 213), col, 1, 1.7, prog=v(TU[k], 0.4))
        f.text(((LX[k] + 34 + HX[k] - 20) / 2 - 10, 248), "tool_use" if k < 3 else "text", mono(10.5), col, v(TU[k] + 0.2), "rm")
        hbox(HX[k], ACT[k][0], ACT[k][1], v(TA[k]), final=(k == 3))
    f.text((905, 370), "calls 4 and 5 follow the same pattern", inter(10, 600), PURPLE, v(14.6), "mm")

    # ---- what each call receives
    f.text((56, 410), "WHAT EACH CALL RECEIVES  (every call re-sends everything so far)", inter(10.5, 700), LIGHT, v(2.0))
    for k in range(4):
        a = v(TC[k])
        y = 430 + 30 * k
        f.text((56, y + 10), f"call #{CALLNO[k]}", inter(12, 600), PURPLE, a)
        x = 130
        f.rrect((x, y, x + BASE[0], y + 20), 4, fill=BASE[2], outline=BASE[1], a=a, width=1.1)
        if k == 0:
            f.text((x + 10, y + 10), "system + tools + CLAUDE.md + skill list + your request", inter(9.8, 500), GREY, a)
        x += BASE[0]
        for wd, col, fill in ADDED[:NADD[k]]:
            f.rrect((x, y, x + wd, y + 20), 4, fill=fill, outline=col, a=a, width=1.1)
            x += wd
        f.text((x + 10, y + 10), SIZE[k] + " tokens", mono(11), INK, a)
    f.text((130, 558), "grey: the starting prompt", inter(10.5, 400), GREY, v(2.4))
    f.text((290, 558), "colours: tool results added along the way", inter(10.5, 400), GREY, v(8.6))

    # ---- the two loops, named
    n = v(18.6)
    f.text((1232, 112), "OUTER LOOP  ·  run by the harness  ·  6 rounds in this example", inter(10.5, 700), TEAL, n, "rm")
    f.text((1232, 394), "INNER LOOP  ·  inside every call  ·  one token per forward pass", inter(10.5, 700), PURPLE, n, "rm")
    c = v(19.8)
    f.rrect((820, 440, 1232, 540), 10, fill=DARK, a=c)
    f.text((1026, 463), "Agent  =  a program calling the LLM in a loop", inter(13.5, 600), (255, 255, 255), c, "mm")
    f.text((1026, 490), "The LLM never changes and never acts.", inter(12, 400), (200, 205, 215), c, "mm")
    f.text((1026, 510), "It only receives a longer prompt each time.", inter(12, 400), (200, 205, 215), c, "mm")
    f.text((1026, 560), "token counts are illustrative", inter(10.5, 400), LIGHT, c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [1.4, 3.0, 4.2, 6.4, 9.2, 10.6, 12.6, 13.8, 15.6, 17.4, 19.0, 20.4, 22.0, 23.5], "loops")
