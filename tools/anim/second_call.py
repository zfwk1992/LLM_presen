"""04c: the second LLM call. Everything is sent again, now including the SKILL.md workflow; the LLM follows its first step."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import example_header, REQUEST, SKILL, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, SLATE, SLATE_F

END = 23.0
WORKFLOW = ["1. Run scripts/extract_dcm_config.py on the EcuC ARXML",
            "2. Look up the requirements in the Dcm specification",
            "3. Read docs/architecture.md",
            "4. Check the Os and Rte definitions",
            "5. Then propose the changes"]
CAPS = [
    (0.8, 1, "Call 2 starts: the harness sends everything again, from the top"),
    (3.6, 2, "New at the end: what the LLM wrote, and the full SKILL.md text"),
    (7.6, 3, "Now the LLM can read your workflow. It starts with step 1"),
    (11.0, 4, "Again it only writes a request: run the extraction script"),
    (13.6, 5, "The harness runs the script; the result joins the prompt"),
    (16.8, 6, "Call 3 will receive all of this: the prompt only ever grows"),
]
X0, X1 = 56, 520


def block(f, y0, y1, tag, col, fill, a):
    f.rrect((X0, y0, X1, y1), 7, fill=fill, outline=col, a=a, width=1.3)
    w = inter(9.2, 700).getlength(tag) / 2 + 14
    f.rrect((X0 + 8, y0 + 7, X0 + 8 + w, y0 + 23), 8, fill=col, a=a)
    f.text((X0 + 8 + w / 2, y0 + 15), tag, inter(9.2, 700), (255, 255, 255), a, "mm")
    return X0 + 8 + w + 10


def render(t):
    f = Frame(t)
    v = f.v
    example_header(f, "Call 2: Everything Is Sent Again", 3)
    f.text((X0, 118), "THE PROMPT FOR CALL 2  (one sequence, in this order)", inter(10.5, 700), LIGHT, v(0.9))

    # ---- unchanged part
    a = v(1.0)
    x = block(f, 132, 196, "SYSTEM", SLATE, SLATE_F, a)
    f.text((x, 147), "system prompt  ·  tool definitions", inter(12, 600), INK, a)
    f.text((X0 + 14, 170), "CLAUDE.md  ·  skill list  (one line per skill)", inter(11.5, 400), GREY, a)
    f.text((X0 + 14, 186), "14,700 tokens", mono(10.5), GREY, a)
    a = v(1.5)
    x = block(f, 202, 234, "USER", BLUE, BLUE_F, a)
    f.text((x, 218), REQUEST, inter(12, 600), INK, a)
    m1 = v(2.2)
    f.line((530, 134), (530, 232), LIGHT, m1, 1.3)
    f.text((540, 176), "identical to call 1", inter(11, 600), GREY, m1)
    f.text((540, 192), "(read from the cache)", inter(10.5, 400), LIGHT, m1)

    # ---- new in call 2
    a = v(3.8)
    x = block(f, 240, 272, "ASSISTANT", ORANGE, ORANGE_F, a)
    f.text((x, 256), 'tool_use  Skill("' + SKILL + '")', mono(11.2), ORANGE, a)
    a = v(4.4)
    x = block(f, 278, 400, "USER · TOOL_RESULT", GREEN, GREEN_F, a)
    f.text((x, 293), "SKILL.md   2,100 tokens", mono(10.8), GREEN, a)
    for i, line in enumerate(WORKFLOW):
        la = v(4.9 + 0.25 * i)
        hot = clamp(1 - abs(t - 9.4) / 1.6) if i == 0 else 0
        if hot > 0.01:
            f.rrect((X0 + 8, 303 + 18 * i, X1 - 8, 321 + 18 * i), 4, fill=(190, 232, 210), a=la * hot)
        f.text((X0 + 16, 312 + 18 * i), line, inter(11.2, 600 if i == 0 and t > 8.6 else 400), INK, la)
    m2 = v(5.6)
    f.line((530, 242), (530, 398), GREEN, m2, 1.3)
    f.text((540, 312), "new in call 2", inter(11, 700), GREEN, m2)
    f.text((540, 328), "what the LLM wrote in call 1", inter(10.5, 400), GREY, m2)
    f.text((540, 343), "+ the skill's full text", inter(10.5, 400), GREY, m2)

    # ---- the LLM reads it and replies
    la = v(7.8)
    f.arrow((716, 250), (760, 250), PURPLE, 1, 1.8, prog=v(7.9, 0.35))
    f.rrect((764, 204, 892, 296), 12, fill=PURPLE_F, outline=PURPLE, a=la, width=1.8)
    s = (t - 8.3) / 1.2
    if 0 < s < 1:
        f.rrect((770 + 86 * s, 210, 800 + 86 * s, 290), 7, fill=PURPLE_HI, a=0.8 * (1 - abs(s - 0.5) * 1.3))
    f.text((828, 240), "LLM", inter(20, 700), PURPLE, la, "mm")
    f.text((828, 268), "call #2", inter(11.5, 600), PURPLE, la, "mm")
    f.text((828, 312), "16,834 tokens in", mono(10.5), GREY, v(8.2), "mm")
    ra = v(9.6)
    f.arrow((896, 250), (930, 250), PURPLE, 1, 1.8, prog=v(9.5, 0.3))
    f.text((934, 136), "THE LLM'S REPLY", inter(10.5, 700), LIGHT, ra)
    f.rrect((934, 148, 1232, 300), 10, fill=DARK, a=ra)
    f.text((950, 172), "“The skill says to start with", inter(12, 500), (226, 229, 236), ra)
    f.text((950, 190), "the EcuC values.”", inter(12, 500), (226, 229, 236), ra)
    ca = v(11.2)
    f.text((950, 222), "tool_use", mono(11), ORANGE, ca)
    f.text((950, 242), 'Bash("python scripts/', mono(11), (255, 255, 255), ca)
    f.text((950, 258), "  extract_dcm_config.py", mono(11), (255, 255, 255), ca)
    f.text((950, 274), '  config/EcuC.arxml")', mono(11), (255, 255, 255), ca)
    f.text((1083, 316), "still only text: nothing has run yet", inter(11, 500), GREY, v(12.0), "mm")

    # ---- the harness runs it
    ha = v(13.8)
    f.arrow((1083, 330), (1083, 352), TEAL, 1, 1.8, prog=v(13.7, 0.3))
    f.rrect((934, 356, 1232, 414), 10, fill=TEAL_F, outline=TEAL, a=ha, width=1.6)
    f.text((950, 376), "Harness  (Claude Code)", inter(13.5, 700), TEAL, ha)
    f.text((950, 397), "runs the script on your machine", inter(11.5, 400), INK, ha)
    xa = v(15.0)
    f.arrow((1083, 418), (1083, 440), GREEN, 1, 1.8, prog=v(14.9, 0.3))
    f.rrect((934, 444, 1232, 502), 10, fill=(255, 255, 255), outline=GREEN, a=xa, width=1.5)
    f.text((950, 464), "script output  ·  900 tokens", mono(10.8), GREEN, xa)
    f.text((950, 485), "3 protocols  ·  14 UDS services  ·  2 PDUs", inter(11.5, 600), INK, xa)

    # ---- appended for call 3
    back = ease((t - 16.9) / 1.0)
    if back > 0.01:
        x1 = 934 + (524 - 934) * back
        f.line((934, 473), (x1, 473), GREEN, 0.9, 1.5)
        if back > 0.97:
            f.arrow((534, 473), (523, 473), GREEN, 1, 1.5, head=5)
    a = v(17.4)
    x = block(f, 406, 438, "ASSISTANT", ORANGE, ORANGE_F, a)
    f.text((x, 422), 'tool_use  Bash("…extract_dcm_config.py…")', mono(10.6), ORANGE, a)
    a = v(17.9)
    x = block(f, 444, 500, "USER · TOOL_RESULT", GREEN, GREEN_F, a)
    f.text((x, 459), "script output", mono(10.8), GREEN, a)
    f.text((X0 + 16, 484), "3 protocols  ·  14 UDS services  ·  2 PDUs to route", inter(11.2, 400), INK, a)
    m3 = v(18.3)
    f.line((530, 408), (530, 498), ORANGE, m3, 1.3)
    f.text((540, 440), "added for call 3", inter(11, 700), ORANGE, m3)
    for aa, s_ in ((v(1.2) * (1 - v(17.6)), "16,834 tokens"), (v(17.6), "17,765 tokens")):
        f.text((X0, 522), s_, inter(15, 700), INK, aa)
    f.text((X0 + 132, 523), "sent in call 2" if t < 17.6 else "will be sent in call 3", inter(11.5, 400), GREY, v(1.2))

    c = v(19.6)
    f.rrect((56, 556, 1232, 606), 10, fill=DARK, a=c)
    f.text((644, 572), "Every call:  send everything so far  →  the LLM writes one reply  →  the harness runs it  →  append", inter(13, 600), (255, 255, 255), c, "mm")
    f.text((644, 592), "Your workflow is followed because the LLM reads it in the prompt, not because the harness executes it.", inter(11.5, 400), (200, 205, 215), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.6, 4.6, 6.6, 8.8, 9.6, 10.6, 12.4, 14.4, 16.0, 17.2, 18.6, 20.2, 21.6, 23.0], "second")
