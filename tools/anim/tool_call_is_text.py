"""04b: inside one LLM call. The reply is generated token by token; a tool call is just text the harness then acts on."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, PURPLE, PURPLE_F, PURPLE_B,
                                PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H, S)
from gifout import example_header, SKILL, header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, SLATE, SLATE_F

END = 24.0
TOKS = ['{"', 'type', '":', ' "', 'tool', '_use', '",', ' "', 'name', '":', ' "', 'Skill', '",',
        ' "', 'input', '":', ' {"', 'skill', '":', ' "', 'dcm', '-integration', '"}}', '<end>']
T0, DT = 3.6, 0.3                      # first token, interval
T_DONE = T0 + DT * len(TOKS)           # 10.8
CAPS = [
    (0.8, 1, "The whole prompt goes into the LLM"),
    (3.2, 2, "The reply comes out one token at a time: one forward pass each"),
    (8.2, 3, "The tokens spell a tool call. To the LLM it is just text"),
    (11.2, 4, "The LLM stops at <end>. Nothing has been executed yet"),
    (14.0, 5, "The harness reads the text and runs the tool on your machine"),
    (18.0, 6, "The result is added to the prompt, ready for the next LLM call"),
]


def render(t):
    f = Frame(t)
    v = f.v
    example_header(f, "Call 1: What the LLM Returns", 2)

    # ---- the prompt (same strip as the previous page), growing at the end
    pa = v(0.9)
    add_out = v(11.6, 0.6)             # the reply itself joins the context
    add_res = v(19.0, 0.8)             # then the tool result
    f.text((56, 118), "PROMPT", inter(10.5, 700), LIGHT, pa)
    segs = [(86, SLATE, SLATE_F), (176, ORANGE, ORANGE_F), (30, TEAL, TEAL_F), (14, GREEN, GREEN_F), (4, BLUE, (200, 215, 250))]
    y = 132
    for h, col, fill in segs:
        f.rrect((56, y, 150, y + h), 3, fill=fill, outline=col, a=pa, width=1.2)
        y += h
    f.rrect((56, y, 150, y + 6 * add_out), 2, fill=ORANGE_F, outline=ORANGE, a=pa * add_out, width=1.2)
    y += 6 * add_out
    f.rrect((56, y, 150, y + 50 * add_res), 3, fill=GREEN_F, outline=GREEN, a=pa * add_res, width=1.2)
    y += 50 * add_res
    for a, s in ((1 - add_out, "14,710 tokens"), (add_out * (1 - add_res), "14,734 tokens"), (add_res, "16,834 tokens")):
        f.text((103, y + 16), s, mono(11), GREY, pa * a, "mm")
    f.text((160, 148), "system", inter(10.5, 500), LIGHT, pa)
    f.text((160, 300), "tools", inter(10.5, 500), LIGHT, pa)
    f.text((160, 409), "CLAUDE.md", inter(10.5, 500), LIGHT, pa)
    f.text((160, 430), "skill list", inter(10.5, 500), LIGHT, pa)
    f.text((160, 446), "your message", inter(10.5, 600), BLUE, pa)
    f.text((160, 453 + 6), "its own reply", inter(10.5, 600), ORANGE, pa * add_out) if add_out > 0.5 else None
    f.text((160, 485), "SKILL.md text", inter(10.5, 600), GREEN, pa * add_res)

    # ---- the LLM and the pass counter
    la = v(1.4)
    f.arrow((236, 300), (292, 300), PURPLE, 1, 1.8, prog=v(1.8, 0.4))
    f.rrect((296, 250, 436, 350), 12, fill=PURPLE_F, outline=PURPLE, a=la, width=1.8)
    n_done = int(clamp((t - T0) / (DT * len(TOKS))) * len(TOKS) + 1e-6)
    phase = ((t - T0) / DT) % 1 if T0 <= t < T_DONE else -1
    if phase >= 0:
        f.rrect((302, 256, 430, 344), 8, fill=PURPLE_HI, a=0.75 * (1 - phase))
    f.text((366, 288), "LLM", inter(20, 700), PURPLE, la, "mm")
    k = min(len(TOKS), n_done + (1 if T0 <= t < T_DONE else 0))
    f.text((366, 320), f"forward pass #{max(k, 1)}" if t >= T0 else "ready", inter(11.5, 600), PURPLE, la, "mm")
    f.text((366, 372), "one pass  =  one token", inter(11.5, 500), GREY, v(3.4), "mm")

    # ---- the reply, token by token
    oa = v(3.0)
    f.arrow((440, 300), (486, 300), PURPLE, 1, 1.8, prog=v(3.3, 0.3))
    f.text((492, 150), "THE LLM'S REPLY  (generated, not typed by anyone)", inter(10.5, 700), LIGHT, oa)
    f.rrect((490, 164, 890, 412), 10, fill=DARK, a=oa)
    fm = mono(14)
    x, y = 506, 196
    for i, tok in enumerate(TOKS):
        w = fm.getlength(tok) / S + 10
        if x + w > 878:
            x, y = 506, y + 34
        a = v(T0 + DT * i, 0.25)
        end = tok == "<end>"
        fresh = clamp(1 - (t - (T0 + DT * i)) / 0.5)
        col = mix((58, 65, 82), ORANGE, fresh) if not end else (127, 29, 29)
        f.rrect((x, y - 13, x + w - 3, y + 13), 4, fill=col, a=a)
        f.text((x + (w - 3) / 2, y), tok.replace(" ", "·"), fm, (255, 255, 255), a, "mm")
        x += w
    # loop arrow: each new token goes back in before the next pass
    lp = v(4.2) * (1 - v(T_DONE, 0.4))
    f.line((690, 414), (690, 440), LIGHT, lp, 1.3)
    f.line((690, 440), (366, 440), LIGHT, lp, 1.3)
    f.arrow((366, 440), (366, 388), LIGHT, lp, 1.3, head=4.5)
    f.text((528, 453), "each new token is appended, then the next pass runs", inter(11, 500), GREY, lp, "mm")
    # readable version of what was written
    r = v(8.4)
    f.rrect((490, 478, 890, 536), 9, fill=ORANGE_F, outline=ORANGE, a=r, width=1.3)
    f.text((506, 497), "Read as text, it says:", inter(11.5, 500), GREY, r)
    f.text((506, 518), 'use the tool "Skill" with skill = "dcm-integration"', inter(13, 700), ORANGE, r)
    st = v(11.4)
    f.text((690, 556), "24 tokens, 24 forward passes. Then the LLM is finished.", inter(12, 600), INK, st, "mm")
    f.text((690, 575), "No file was read. No command was run.", inter(12, 400), GREY, st, "mm")

    # ---- the harness acts
    ha = v(14.2)
    f.arrow((894, 250), (936, 250), ORANGE, 1, 1.8, prog=v(14.3, 0.35))
    f.rrect((940, 196, 1232, 304), 12, fill=TEAL_F, outline=TEAL, a=ha, width=1.8)
    f.text((958, 220), "Harness  (Claude Code)", inter(15, 700), TEAL, ha)
    f.text((958, 244), "an ordinary program, not a model", inter(11.5, 500), GREY, ha)
    f.text((958, 268), "parses the text  ·  checks permission", inter(11.5, 400), INK, v(14.8))
    f.text((958, 286), "then runs the tool", inter(11.5, 600), INK, v(15.3))
    ta = v(15.8)
    f.arrow((1086, 308), (1086, 342), TEAL, 1, 1.8, prog=v(15.7, 0.3))
    f.rrect((940, 346, 1232, 420), 12, fill=GREEN_F, outline=GREEN, a=ta, width=1.8)
    f.text((958, 370), "Tool: Skill", inter(15, 700), GREEN, ta)
    f.text((958, 394), "reads " + SKILL + "/SKILL.md from your disk", inter(11.5, 400), INK, ta)
    ra = v(17.0)
    f.arrow((1086, 424), (1086, 458), GREEN, 1, 1.8, prog=v(16.9, 0.3))
    f.rrect((940, 462, 1232, 520), 10, fill=(255, 255, 255), outline=GREEN, a=ra, width=1.5)
    f.text((958, 482), "tool_result", mono(12.5), GREEN, ra)
    f.text((958, 503), "the SKILL.md text  ·  about 2,100 tokens", inter(11.5, 400), INK, ra)
    # result travels back to the prompt
    back = ease((t - 18.2) / 1.4)
    if back > 0.01:
        f.line((1086, 524), (1086, 600), GREEN, 0.9, 1.5)
        x1 = 1086 + (103 - 1086) * back
        f.line((1086, 600), (x1, 600), GREEN, 0.9, 1.5)
        if back > 0.98:
            f.arrow((103, 600), (103, 548), GREEN, 1, 1.5, head=5)
    f.text((600, 616), "appended to the prompt  →  the harness calls the LLM again", inter(12, 700), GREEN, v(19.4), "mm")

    c = v(20.8)
    f.rrect((940, 546, 1232, 584), 9, fill=DARK, a=c)
    f.text((1086, 565), "The LLM writes. The harness acts.", inter(13, 600), (255, 255, 255), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.6, 4.4, 6.0, 7.6, 9.4, 10.9, 12.6, 14.9, 16.2, 17.6, 19.0, 20.2, 21.6, 24.0], "toolcall")
