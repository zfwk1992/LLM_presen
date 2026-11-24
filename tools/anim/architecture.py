"""09b: the whole architecture. The LLM talks only to the harness; the harness reaches built-in tools, skills,
MCP servers (one of them doing the RAG search) and returns everything as text in the prompt."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import header, captions, main, mix, REQUEST, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F, SLATE, SLATE_F

END = 24.5
# right-hand capabilities: y0, title, line 1, line 2, colour, fill
CAPB = [
    (112, "Built-in tools", "Read · Grep · Bash · Edit", "work on your project files", ORANGE, ORANGE_F),
    (192, "Skills", "folders on disk: SKILL.md + scripts", "how to do a kind of task", GREEN, GREEN_F),
    (272, "MCP server  “spec”", "embedding model + vector DB", "this is where the RAG search runs", TEAL, TEAL_F),
    (352, "MCP server  “jira”", "talks to the Jira API", "connected, not needed this time", TEAL, TEAL_F),
    (432, "Sub-agents", "a second loop with its own context", "not needed this time", PURPLE, PURPLE_F),
]
# the session: start time, what the LLM asks for, which capability, result label, segment (width, colour, fill)
STEPS = [
    (7.2, 'Skill("dcm-integration")', 1, "SKILL.md", (34, GREEN, GREEN_F)),
    (10.6, 'Bash("extract_dcm_config.py …")', 0, "script output", (16, YELLOW, YELLOW_F)),
    (13.6, 'mcp__spec__search_spec("Dcm …")', 2, "3 spec passages", (30, TEAL, TEAL_F)),
    (16.8, 'Read("docs/architecture.md")', 0, "architecture.md", (38, YELLOW, YELLOW_F)),
]
T_ANSWER = 19.6
BASE = [(60, SLATE, SLATE_F, "system"), (150, ORANGE, ORANGE_F, "tool definitions (built-in + MCP)"), (30, TEAL, TEAL_F, "CLAUDE.md"),
        (20, GREEN, GREEN_F, "skills"), (8, BLUE, (200, 215, 250), "")]
CAPS = [
    (0.8, 1, "The LLM talks to one thing only: the harness"),
    (3.6, 2, "At startup the harness collects what exists: tools, MCP servers, skills"),
    (7.0, 3, "Call 1: the model asks for a skill; the harness reads it from disk"),
    (10.4, 4, "Call 2: a built-in tool runs your script on your machine"),
    (13.4, 5, "Call 3: an MCP server does the RAG search and returns text"),
    (16.6, 6, "Every result comes back as text in the prompt, until the model answers"),
]
HX0, HX1, HY0, HY1 = 250, 640, 196, 500


def dot(f, pts, pr, col):
    """A packet travelling along a polyline."""
    if not 0 < pr < 1:
        return
    seg = [((pts[i][0] - pts[i + 1][0]) ** 2 + (pts[i][1] - pts[i + 1][1]) ** 2) ** 0.5 for i in range(len(pts) - 1)]
    d = sum(seg) * pr
    for i, s in enumerate(seg):
        if d <= s:
            u = d / s
            f.circle((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u), 5.5, fill=col)
            return
        d -= s


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "The Whole Picture: Everything Goes Through the Harness", "EXTENDING CAPABILITIES  ·  PUTTING IT TOGETHER", GREEN)
    f.text((1232, 45), "the request:  “" + REQUEST + "”", inter(12, 600), BLUE, v(0.1, 0.5), "rm")

    # ---- static structure
    a = v(0.9)
    f.rrect((330, 112, 560, 162), 12, fill=PURPLE_F, outline=PURPLE, a=a, width=1.8)
    f.text((445, 129), "LLM", inter(16, 700), PURPLE, a, "mm")
    f.text((445, 148), "tokens in, tokens out", inter(10.5, 500), PURPLE, a, "mm")
    f.rrect((HX0, HY0, HX1, HY1), 14, fill=(240, 249, 250), outline=TEAL, a=a, width=2)
    f.text((HX0 + 18, HY0 + 20), "Harness  (Claude Code)", inter(15, 700), TEAL, a)
    f.text((HX0 + 18, HY0 + 40), "the only program the LLM is connected to", inter(10.8, 400), GREY, a)
    for (x0, y0, x1, y1, name, sub) in ((270, 256, 440, 310, "Prompt builder", "joins all the parts"),
                                        (450, 256, 620, 310, "Agent loop", "call, check, repeat"),
                                        (270, 322, 440, 376, "Permissions", "may this run?"),
                                        (450, 322, 620, 376, "Tool router", "who can do this?")):
        f.rrect((x0, y0, x1, y1), 8, fill=(255, 255, 255), outline=TEAL, a=a, width=1.2)
        f.text(((x0 + x1) / 2, y0 + 19), name, inter(12, 700), TEAL, a, "mm")
        f.text(((x0 + x1) / 2, y0 + 38), sub, inter(10, 400), GREY, a, "mm")
    f.arrow((405, HY0 - 2), (405, 166), TEAL, a, 1.6, head=5)
    f.arrow((485, 166), (485, HY0 - 2), ORANGE, a, 1.6, head=5)
    f.text((396, 180), "the prompt", inter(9.8, 700), TEAL, a, "rm")
    f.text((494, 180), "one reply", inter(9.8, 700), ORANGE, a, "lm")
    f.rrect((56, 300, 190, 366), 10, fill=BLUE_F, outline=BLUE, a=a, width=1.5)
    f.text((123, 322), "You", inter(14, 700), BLUE, a, "mm")
    f.text((123, 344), "one request", inter(10.5, 400), GREY, a, "mm")
    f.arrow((194, 322), (HX0 - 4, 322), BLUE, a, 1.6, head=5)
    f.arrow((HX0 - 4, 346), (194, 346), GREEN, v(T_ANSWER + 1.2), 1.6, head=5)
    f.text((222, 360), "answer", inter(9.5, 700), GREEN, v(T_ANSWER + 1.2), "mm")

    # ---- capabilities on the right
    for i, (y0, name, l1, l2, col, fill) in enumerate(CAPB):
        ca = v(3.8 + 0.3 * i)
        used = any(st[2] == i for st in STEPS)
        flash = 0.0
        for (ts, _, ci, _, _) in STEPS:
            if ci == i:
                flash = max(flash, clamp(1 - abs(t - (ts + 1.5)) / 0.7))
        f.rrect((760, y0, 1232, y0 + 68), 10, fill=mix(fill if used else (247, 248, 250), (255, 255, 255), 0) if not flash else mix(fill, col, 0.35 * flash),
                outline=col if used else (200, 204, 214), a=ca, width=1.5 + 1.0 * flash)
        f.text((776, y0 + 19), name, inter(13, 700), col if used else GREY, ca)
        f.text((776, y0 + 39), l1, inter(11, 500), INK if used else GREY, ca)
        f.text((776, y0 + 55), l2, inter(10, 400), GREY, ca)
        f.arrow((HX1 + 4, 349), (756, y0 + 34), col if used else (200, 204, 214), ca, 1.3, head=4.5)
    f.text((700, 124), "at startup: tool list,", inter(9.5, 600), GREY, v(5.4), "mm")
    f.text((700, 137), "skill descriptions", inter(9.5, 600), GREY, v(5.4), "mm")

    # ---- the prompt at the bottom
    pa = v(1.6)
    f.text((HX0, 524), "THE PROMPT  (what the LLM receives at each call)", inter(10.5, 700), LIGHT, pa)
    x = HX0
    for (wd, col, fill, name) in BASE:
        hi = clamp(1 - abs(t - 5.8) / 1.0) if name.startswith("tool") or name == "skills" else 0
        f.rrect((x, 538, x + wd, 566), 4, fill=mix(fill, col, 0.3 * hi), outline=col, a=pa, width=1.2)
        if name and wd > 40:
            f.text((x + wd / 2, 552), name, inter(9, 600), col if col != SLATE else GREY, pa, "mm")
        x += wd
    shown = []
    for (ts, _, _, label, (wd, col, fill)) in STEPS:
        g = v(ts + 2.4, 0.5)
        if g > 0.003:
            f.rrect((x, 538, x + wd * g, 566), 4, fill=fill, outline=col, a=pa, width=1.2)
            shown.append((label, col, g))
        x += wd * g
    lx = x + 16
    for k, (label, col, g) in enumerate(shown):
        s_ = ("+ " if k == 0 else "·  ") + label
        f.text((lx, 552), s_, inter(10.5, 700), col, g)
        lx += inter(10.5, 700).getlength(s_) / 2 + 10
    f.text((HX0, 580), "fixed part, the same at every call", inter(9.5, 400), GREY, v(2.2))
    f.text((HX0 + 300, 580), "tool results, added one by one as text", inter(9.5, 400), GREY, v(STEPS[0][0] + 2.6))
    f.line((445, 536), (445, HY1 + 2), TEAL, pa * 0.6, 1.2)

    # ---- the session: reply text inside the harness, packets travelling
    for i, (ts, call, ci, label, _) in enumerate(STEPS):
        nxt = STEPS[i + 1][0] if i + 1 < len(STEPS) else T_ANSWER
        la = min(v(ts + 0.7, 0.3), 1 - v(nxt - 0.2, 0.3))
        f.rrect((270, 392, 620, 446), 8, fill=ORANGE_F, outline=ORANGE, a=la, width=1.3)
        f.text((284, 408), f"LLM call {i + 1} asks for", inter(10, 700), ORANGE, la)
        f.text((284, 428), call, mono(10.8), INK, la)
        y_cap = CAPB[ci][0] + 34
        col = CAPB[ci][4]
        dot(f, [(405, HY0), (405, 166)], (t - ts) / 0.5, TEAL)                      # prompt up
        dot(f, [(485, 166), (485, HY0)], (t - ts - 0.5) / 0.5, ORANGE)              # reply down
        dot(f, [(HX1, 349), (760, y_cap)], (t - ts - 1.1) / 0.6, col)               # out to the capability
        dot(f, [(760, y_cap), (HX1, 349)], (t - ts - 1.9) / 0.6, col)               # result back
        dot(f, [(445, HY1), (445, 536)], (t - ts - 2.4) / 0.4, col)                 # into the prompt
    fa = v(T_ANSWER + 0.6, 0.3)
    f.rrect((270, 392, 620, 446), 8, fill=GREEN_F, outline=GREEN, a=fa, width=1.3)
    f.text((284, 408), "LLM call 6: no tool call", inter(10, 700), GREEN, fa)
    f.text((284, 428), "the integration plan  →  back to you", inter(11.5, 600), INK, fa)
    dot(f, [(405, HY0), (405, 166)], (t - T_ANSWER) / 0.5, TEAL)
    dot(f, [(485, 166), (485, HY0)], (t - T_ANSWER - 0.5) / 0.5, GREEN)
    dot(f, [(HX0, 346), (194, 346)], (t - T_ANSWER - 1.1) / 0.6, GREEN)
    f.text((445, 470), "(call 5, a Grep, works the same way)", inter(9.8, 400), GREY, v(17.6) * (1 - v(T_ANSWER + 0.4)), "mm")

    # ---- conclusion
    c = v(21.6)
    f.rrect((56, 598, 1232, 638), 10, fill=DARK, a=c)
    f.text((644, 618), "The LLM sees only the prompt.  The harness is its only door to files, skills, MCP servers and RAG.  Everything returns as text.",
           inter(12.5, 600), (255, 255, 255), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.4, 4.6, 5.8, 8.0, 8.8, 9.8, 11.6, 12.8, 14.8, 16.0, 18.2, 20.6, 22.4, 24.5], "arch")
