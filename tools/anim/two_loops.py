"""04c: the agent loop is a program (the harness) calling the LLM again and again; inside each call runs the generation loop."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, PURPLE, PURPLE_F, PURPLE_B,
                                PURPLE_HI, ORANGE, PANEL, PANEL_B, DARK, W, H)
from gifout import header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F, SLATE, SLATE_F

END = 23.5
LX = [330, 560, 790, 1020]                      # LLM calls
HX = [445, 675, 905, 1140]                      # harness actions after each call
WROTE = ['Skill("dcm-guide")', 'Grep("Dcm_")', 'Read("Dcm_Dsl.c")', "the final answer"]
NTOK = ["24 tokens, one by one", "19 tokens, one by one", "21 tokens, one by one", "310 tokens, one by one"]
ACT = [("run Skill", "SKILL.md  ·  +2.1k"), ("run Grep", "38 matches  ·  +1.2k"), ("run Read", "612 lines  ·  +9.4k"),
       ("show answer", "no tool call: stop")]
SIZE = ["14.7k", "16.8k", "18.0k", "27.4k"]
# times: prompt arrow down, call box, generating pulse, reply arrow up, harness action
TD = [1.6, 8.1, 11.7, 14.4]
TC = [2.0, 8.5, 12.0, 14.8]
TP = [3.6, 8.8, 12.2, 15.0]
TU = [5.7, 10.0, 13.2, 16.6]
TA = [6.1, 10.4, 13.6, 17.0]
BAR = [(300, SLATE, SLATE_F, "system + tools + CLAUDE.md + skill list + your message"), (43, GREEN, GREEN_F, ""),
       (25, YELLOW, YELLOW_F, ""), (192, YELLOW, YELLOW_F, "")]
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
    header(f, "Agent Loop = a Program Calling the LLM Again and Again", "FROM LLM TO AI AGENT", PURPLE)

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
        mx, my = (src + 20 + LX[k] - 34) / 2, 248
        f.text((mx + 9, my), SIZE[k], mono(10.5), TEAL, v(TD[k] + 0.2), "lm")
        # the call
        a = v(TC[k])
        f.rrect((LX[k] - 78, 285, LX[k] + 78, 361), 10, fill=PURPLE_F, outline=PURPLE, a=a, width=1.6)
        s = (t - TP[k]) / 1.3
        if 0 < s < 1:
            f.rrect((LX[k] - 72 + 118 * s, 291, LX[k] - 46 + 118 * s, 355), 6, fill=PURPLE_HI, a=0.8 * (1 - abs(s - 0.5) * 1.3))
        f.text((LX[k], 301), f"LLM call #{k + 1}", inter(12.5, 700), PURPLE, a, "mm")
        w = v(TP[k] + 0.9)
        f.text((LX[k], 323), WROTE[k], mono(10.8) if k < 3 else inter(11.5, 600), ORANGE if k < 3 else GREEN, w, "mm")
        f.text((LX[k], 344), NTOK[k], inter(9.8, 500), GREY, w, "mm")
        # reply goes up to the harness
        col = ORANGE if k < 3 else GREEN
        f.arrow((LX[k] + 34, 283), (HX[k] - 20, 213), col, 1, 1.7, prog=v(TU[k], 0.4))
        f.text(((LX[k] + 34 + HX[k] - 20) / 2 - 10, 248), "tool_use" if k < 3 else "text", mono(10.5), col, v(TU[k] + 0.2), "rm")
        hbox(HX[k], ACT[k][0], ACT[k][1], v(TA[k]), final=(k == 3))

    # ---- what each call receives
    f.text((56, 410), "WHAT EACH CALL RECEIVES  (every call re-sends everything so far)", inter(10.5, 700), LIGHT, v(2.0))
    for k in range(4):
        a = v(TC[k])
        y = 430 + 30 * k
        f.text((56, y + 10), f"call #{k + 1}", inter(12, 600), PURPLE, a)
        x = 130
        for j in range(k + 1):
            wd, col, fill, txt = BAR[j]
            f.rrect((x, y, x + wd, y + 20), 4, fill=fill, outline=col, a=a, width=1.1)
            if j == 0 and k == 0:
                f.text((x + 10, y + 10), txt, inter(9.8, 500), GREY, a)
            x += wd
        f.text((x + 10, y + 10), SIZE[k] + " tokens", mono(11), INK, a)
    f.text((130, 558), "grey: the starting prompt", inter(10.5, 400), GREY, v(2.4))
    f.text((290, 558), "green / yellow: tool results added along the way", inter(10.5, 400), GREY, v(8.6))

    # ---- the two loops, named
    n = v(18.6)
    f.text((1232, 112), "OUTER LOOP  ·  run by the harness  ·  4 rounds here", inter(10.5, 700), TEAL, n, "rm")
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
