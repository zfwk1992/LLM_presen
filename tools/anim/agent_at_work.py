"""04e: a simulated agent session. Request: "Analyze how DCM is integrated in this project."
Left: the project on disk. Middle: what the agent does, call by call. Right: the prompt growing."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H, S)
from gifout import header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F, SLATE, SLATE_F

END = 24.0
TS = [2.6, 6.0, 9.2, 12.4, 15.6, 18.8]          # start of each LLM call
# file, description, badge at start, (step that touches it, badge afterwards), colour of that badge
FILES = [
    ("CLAUDE.md", "project notes", "in the prompt", None),
    ("skills/dcm-guide/SKILL.md", "how to analyse Dcm here", "1 line in prompt", (0, "loaded", GREEN)),
    ("skills/misra-check/SKILL.md", "MISRA rule checks", "1 line in prompt", None),
    ("docs/AUTOSAR_SWS_Dcm.pdf", "the specification, 600 pages", "", (4, "3 passages", TEAL)),
    ("config/Dcm.arxml", "Dcm configuration", "", (1, "read", YELLOW)),
    ("src/Dcm/Dcm_Dsl.c", "session layer", "", (3, "read", YELLOW)),
    ("src/Dcm/Dcm_Dsp.c", "service processing", "", None),
    ("src/PduR/PduR_Cfg.c", "PDU routing", "", (2, "searched", YELLOW)),
    ("src/…   214 more files", "the rest of the project", "", None),
]
STEPS = [
    ("A skill matches this task. Load it first.", 'Skill("dcm-guide")', "SKILL.md loaded: a 4-step checklist", "+2.1k", 1),
    ("Checklist step 1: find the Dcm configuration.", 'Read("config/Dcm.arxml")', "3 protocols, 14 UDS services configured", "+6.3k", 4),
    ("How do requests reach Dcm? Check the routing.", 'Grep("Dcm", "src/PduR/")', "PduR_Cfg.c: 2 PDUs routed to Dcm", "+0.8k", 7),
    ("Now the session handling code.", 'Read("src/Dcm/Dcm_Dsl.c")', "612 lines", "+9.4k", 5),
    ("Compare with what the standard requires.", 'search_spec("Dcm PduR interface")', "3 passages from SWS_Dcm, out of 600 pages", "+1.8k", 3),
    ("I have enough. Write the answer.", None, None, None, None),
]
ANSWER = ["Dcm is reached through PduR (2 routed PDUs). Dsl handles sessions,",
          "Dsp the 14 UDS services. Configured in Dcm.arxml. Matches SWS_Dcm §7.2."]
SEG = [(162, SLATE, SLATE_F, "start", "14.7k"), (23, GREEN, GREEN_F, "SKILL.md", "+2.1k"), (69, YELLOW, YELLOW_F, "Dcm.arxml", "+6.3k"),
       (9, YELLOW, YELLOW_F, "grep result", "+0.8k"), (103, YELLOW, YELLOW_F, "Dcm_Dsl.c", "+9.4k"), (20, TEAL, TEAL_F, "spec passages", "+1.8k")]
TOTALS = ["14.7k", "16.8k", "23.1k", "23.9k", "33.3k", "35.1k"]
CAPS = [
    (0.8, 1, "One request. Project notes and skill descriptions are already in the prompt"),
    (2.6, 2, "Call 1: the model sees a matching skill and asks to load it"),
    (6.0, 3, "Call 2: following the skill, it asks to read the Dcm configuration"),
    (9.2, 4, "Calls 3 and 4: it asks to search the routing, then to read the code"),
    (15.6, 5, "Call 5: it asks the spec. Only 3 passages of 600 pages come back"),
    (18.8, 6, "Call 6: no tool call this time. It writes the answer and the loop ends"),
]


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "An Agent at Work, Call by Call", "FROM LLM TO AI AGENT", PURPLE)
    cap = inter(10.5, 700)

    # ================= left: the project on disk
    pa = v(0.9)
    f.text((56, 122), "YOUR PROJECT  (on disk)", cap, LIGHT, pa)
    done = v(21.4)
    for i, (name, desc, badge0, touch) in enumerate(FILES):
        y0 = 136 + 46 * i
        hit = 0.0
        if touch:
            k, badge1, bcol = touch
            hit = v(TS[k] + 1.3, 0.3)
            flash = clamp(1 - abs(t - (TS[k] + 1.6)) / 0.6)
        else:
            flash = 0
        fill = mix((250, 250, 251), ORANGE_F, flash)
        out = mix(PANEL_B, ORANGE, max(flash, 0))
        untouched = touch is None and i in (2, 6, 8)
        f.rrect((56, y0, 330, y0 + 40), 6, fill=fill, outline=out, a=pa * (1 - 0.45 * done * untouched), width=1.2)
        f.text((66, y0 + 13), name, mono(10.6), INK, pa * (1 - 0.5 * done * untouched))
        f.text((66, y0 + 29), desc, inter(9.8, 400), GREY, pa * (1 - 0.5 * done * untouched))
        # badges
        if badge0:
            a0 = v(1.4) * (1 - hit)
            f.text((322, y0 + 29), badge0, inter(9.5, 700), TEAL, pa * a0, "rm")
        if touch:
            f.text((322, y0 + 29), badge1, inter(9.8, 700), bcol, pa * hit, "rm")
        if untouched and i != 2:
            f.text((322, y0 + 29), "never opened", inter(9.5, 600), LIGHT, done, "rm")

    # ================= middle: the transcript
    ua = v(1.0)
    f.text((380, 122), "WHAT THE AGENT DOES", cap, LIGHT, ua)
    f.rrect((380, 134, 960, 160), 6, fill=BLUE_F, outline=BLUE, a=ua, width=1.3)
    f.text((392, 147), "USER", inter(10, 700), BLUE, ua)
    f.text((434, 147), "Analyze how DCM is integrated in this project.", inter(12.5, 600), INK, ua)
    for k, (think, call, result, size, row) in enumerate(STEPS):
        t0 = TS[k]
        a = v(t0, 0.35)
        if a <= 0.003:
            continue
        y0 = 168 + 67 * k
        last = call is None
        hgt = 62 if not last else 78
        f.rrect((380, y0, 960, y0 + hgt), 8, fill=(255, 255, 255), outline=PURPLE_B if not last else GREEN, a=a, width=1.3)
        s = (t - t0) / 0.9
        if 0 < s < 1:
            f.rrect((386 + 520 * s, y0 + 5, 430 + 520 * s, y0 + hgt - 5), 6, fill=PURPLE_HI, a=0.6 * (1 - abs(s - 0.5) * 1.3))
        f.rrect((390, y0 + 8, 456, y0 + 26), 9, fill=PURPLE, a=a)
        f.text((423, y0 + 17), f"LLM CALL {k + 1}", inter(8.8, 700), (255, 255, 255), a, "mm")
        f.text((466, y0 + 17), "“" + think + "”", inter(12, 500), INK, v(t0 + 0.5))
        if not last:
            ca = v(t0 + 0.9)
            f.text((392, y0 + 37), "asks for", inter(9.8, 600), ORANGE, ca)
            f.text((466, y0 + 37), call, mono(11.2), ORANGE, ca)
            ra = v(t0 + 2.0)
            f.text((392, y0 + 53), "harness", inter(9.8, 600), GREEN, ra)
            f.text((466, y0 + 53), "ran it:  " + result, inter(11.2, 500), GREEN, ra)
            f.text((950, y0 + 53), size, mono(10.5), GREY, ra, "rm")
            # the harness reaches into the project
            y_row = 136 + 46 * row + 20
            la = v(t0 + 1.2, 0.3) * (1 - 0.75 * v(t0 + 2.6, 0.5))
            f.arrow((378, y0 + 37), (334, y_row), ORANGE, la, 1.6, head=5)
        else:
            f.text((392, y0 + 37), "writes", inter(9.8, 600), GREEN, v(t0 + 1.0))
            f.text((466, y0 + 37), "no tool call", mono(11.2), GREEN, v(t0 + 1.0))
            for j, line in enumerate(ANSWER):
                f.text((392, y0 + 54 + 15 * j), line, inter(11, 600), INK, v(t0 + 1.5 + 0.4 * j))

    # ================= right: the prompt
    ra = v(1.2)
    f.text((985, 122), "THE PROMPT  (context window)", cap, LIGHT, ra)
    y = 136
    n_now = 0
    for j, (h, col, fill, name, size) in enumerate(SEG):
        tj = 1.2 if j == 0 else TS[j - 1] + 2.0
        g = v(tj, 0.5)
        if g <= 0.003:
            break
        n_now = j
        f.rrect((985, y, 1065, y + h * g), 3, fill=fill, outline=col, a=ra, width=1.2)
        ly = y + max(h, 12) / 2
        if j == 3:
            ly = y + 4
        f.text((1075, ly), name, inter(10.8, 600), col if j else GREY, g)
        f.text((1228, ly), size, mono(10.5), GREY, g, "rm")
        y += h * g
    f.text((1075, 136 + 100), "system prompt, tools,", inter(9.8, 400), GREY, ra)
    f.text((1075, 136 + 114), "CLAUDE.md, skill list,", inter(9.8, 400), GREY, ra)
    f.text((1075, 136 + 128), "your request", inter(9.8, 400), GREY, ra)
    calls = sum(1 for x in TS if t >= x)
    f.text((985, 548), TOTALS[n_now] + " tokens", inter(17, 700), INK, ra)
    f.text((985, 570), f"LLM calls so far: {calls}", inter(11.5, 500), GREY, ra)
    f.text((985, 588), "sent again in full at every call", inter(10.5, 400), LIGHT, v(6.4))

    # ================= conclusion
    c = v(21.6)
    f.rrect((380, 592, 960, 632), 9, fill=DARK, a=c)
    f.text((670, 612), "6 LLM calls  ·  5 tool runs by the harness  ·  the model never opened a file itself", inter(12.5, 600), (255, 255, 255), c, "mm")
    f.text((985, 618), "token counts are illustrative", inter(10, 400), LIGHT, c)

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.0, 3.6, 5.4, 7.6, 8.8, 10.6, 12.0, 14.0, 15.2, 17.4, 18.6, 20.6, 22.4, 24.0], "work")
