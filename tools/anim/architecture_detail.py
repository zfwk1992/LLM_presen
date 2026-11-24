"""09c: inside the harness. One round of the loop step by step, and the check that ends it.
The LLM decides that the task is done (by not asking for a tool); the harness only checks."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, PURPLE_F,
                                PURPLE_B, PURPLE_HI, ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import header, captions, main, mix, REQUEST, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F

END = 24.5
CAPS = [
    (0.8, 1, "The harness keeps the whole conversation and builds the prompt from it"),
    (3.8, 2, "The prompt goes to the model provider; one reply comes back"),
    (6.8, 3, "The harness parses the reply and asks one question: is there a tool call?"),
    (9.6, 4, "Yes: check permission, then route it to the right executor"),
    (13.2, 5, "The result becomes text, is appended, and the next round starts"),
    (15.8, 6, "Same path every round. One day the reply contains no tool call"),
    (18.6, 7, "Then the loop ends. The LLM decided; the harness only checked"),
]
EXEC = [(76, "Built-in tools", "your files, your shell"), (270, "Skill loader", "skills/ on disk"),
        (464, "Sub-agent", "own loop, own context"), (658, "MCP clients", "one per server")]


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "Inside the Harness: One Round, and How It Stops", "EXTENDING CAPABILITIES  ·  THE ARCHITECTURE IN DETAIL", GREEN)
    f.text((1232, 45), "the request:  “" + REQUEST + "”", inter(12, 600), BLUE, v(0.1, 0.5), "rm")

    def hot(tc, dur=0.7):
        return clamp(1 - abs(t - tc) / dur)

    def box(x0, y0, x1, y1, num, title, sub, a, h=0.0, col=TEAL, fill=(255, 255, 255)):
        f.rrect((x0, y0, x1, y1), 9, fill=mix(fill, TEAL_F if col == TEAL else fill, 0) if h <= 0 else mix(fill, col, 0.28 * h),
                outline=col, a=a, width=1.4 + 1.2 * h)
        tx = x0 + 12
        if num:
            f.circle((x0 + 20, y0 + 19), 10, fill=col, a=a)
            f.text((x0 + 20, y0 + 19.5), str(num), inter(11, 700), (255, 255, 255), a, "mm")
            tx = x0 + 36
        f.text((tx, y0 + 19), title, inter(12.5, 700), col, a)
        f.text((x0 + 12, y0 + 41), sub, inter(10.2, 400), GREY, a)

    second = t >= 15.8                                    # the last round

    # ---- model provider
    a = v(0.9)
    f.text((440, 104), "MODEL PROVIDER  ·  over the network", inter(9.5, 700), LIGHT, a)
    hl = max(hot(4.9, 0.8), hot(16.9, 0.5))
    f.rrect((440, 114, 680, 170), 12, fill=mix(PURPLE_F, PURPLE_HI, hl), outline=PURPLE, a=a, width=1.8)
    f.text((500, 132), "LLM", inter(17, 700), PURPLE, a, "mm")
    f.text((500, 153), "tokens in, tokens out", inter(9.5, 500), PURPLE, a, "mm")
    f.rrect((566, 124, 670, 160), 7, fill=(255, 255, 255), outline=PURPLE_B, a=a, width=1.1)
    f.text((618, 135), "prompt cache", inter(9.5, 700), PURPLE, a, "mm")
    f.text((618, 150), "unchanged prefix", inter(8.5, 400), GREY, a, "mm")

    # ---- harness zone
    f.rrect((56, 192, 860, 562), 14, fill=(244, 250, 251), outline=TEAL, a=a, width=2)
    f.text((76, 207), "HARNESS  ·  Claude Code  ·  a program on your machine", inter(9.5, 700), TEAL, a)

    box(76, 222, 246, 282, 1, "Conversation store", "every message so far", v(1.0), max(hot(1.7), hot(16.1, 0.4), hot(14.9, 0.6)))
    box(276, 222, 446, 282, 2, "Prompt builder", "joins all the parts", v(1.4), max(hot(2.8), hot(16.4, 0.4)))
    f.arrow((248, 252), (272, 252), TEAL, v(1.6), 1.5, head=4.5)
    f.text((76, 296), "your request starts here", inter(9.8, 600), BLUE, v(1.2))
    # up to the LLM and back
    up = v(3.9, 0.5)
    f.line((400, 222), (400, 142), TEAL, up, 1.6)
    f.arrow((400, 142), (436, 142), TEAL, up, 1.6, head=5)
    f.text((392, 180), "the whole prompt", inter(9.8, 700), TEAL, up, "rm")
    dn = v(5.3, 0.5)
    f.line((680, 142), (745, 142), ORANGE, dn, 1.6)
    f.arrow((745, 142), (745, 218), ORANGE, dn, 1.6, head=5)
    f.text((754, 180), "one reply", inter(9.8, 700), ORANGE, dn)
    box(650, 222, 840, 282, 3, "Reply parser", "", v(5.6), max(hot(6.2), hot(17.3, 0.4)))
    f.text((662, 263), "tool_use  mcp__spec__search_spec", mono(8.6), ORANGE, v(5.9) * (1 - v(15.6, 0.3)))
    f.text((662, 263), "text:  the integration plan", mono(9.2), GREEN, v(17.4, 0.3))

    # ---- the stop check
    d = v(7.0)
    dh = max(hot(7.9, 0.9), hot(18.0, 0.6))
    cx, cy = 745, 360
    pts = [(cx, cy - 40), (cx + 96, cy), (cx, cy + 40), (cx - 96, cy)]
    S2 = 2
    dcol = GREEN if second and t > 17.6 else ORANGE
    f.d.polygon([(round(x * S2), round(y * S2)) for x, y in pts], fill=(*mix((255, 255, 255), dcol, 0.25 * dh), round(255 * d)),
                outline=(*dcol, round(255 * d)), width=round((1.6 + 1.2 * dh) * S2))
    f.circle((cx - 52, cy - 1), 10, fill=dcol, a=d)
    f.text((cx - 52, cy - 0.5), "4", inter(11, 700), (255, 255, 255), d, "mm")
    f.text((cx + 8, cy - 8), "tool call", inter(11.5, 700), dcol, d, "mm")
    f.text((cx + 8, cy + 8), "in the reply?", inter(11.5, 700), dcol, d, "mm")
    f.arrow((745, 284), (745, 317), ORANGE, d, 1.5, head=4.5)

    # ---- YES branch
    ya = v(9.8)
    f.arrow((646, 360), (620, 360), ORANGE, ya, 1.6, head=5)
    f.text((634, 346), "YES", inter(10, 700), ORANGE, ya, "mm")
    box(456, 330, 616, 390, 5, "Permissions", "may this run?", ya, hot(10.3))
    f.arrow((452, 360), (430, 360), TEAL, v(10.6), 1.5, head=4.5)
    box(266, 330, 426, 390, 6, "Tool router", "who can do this?", v(10.6), hot(11.1))
    for i, (x0, name, sub) in enumerate(EXEC):
        ea = v(11.2 + 0.12 * i)
        h = hot(12.2, 0.9) if i == 3 else 0
        box(x0, 428, x0 + 180, 484, None, name, sub, ea, h)
        f.arrow((346, 392), (x0 + 90, 424), TEAL if i == 3 else (170, 205, 212), ea, 1.3, head=4)
    ma = v(12.0)
    f.arrow((842, 456), (896, 456), TEAL, ma, 1.6, head=5)
    f.rrect((900, 414, 1232, 500), 10, fill=TEAL_F, outline=TEAL, a=ma, width=1.5)
    f.text((916, 430), "MCP SERVERS  ·  local or remote", inter(9.5, 700), TEAL, ma)
    f.text((916, 450), "“spec”   →  embedding model + vector DB  (RAG)", inter(10.6, 600 if not second else 400), INK, ma)
    f.text((916, 468), "“jira”   →  Jira API", inter(10.6, 400), GREY, ma)
    f.text((916, 486), "“bitbucket”   →  repositories, pull requests", inter(10.6, 400), GREY, ma)

    # ---- result and the loop back
    ra = v(13.4)
    f.rrect((76, 510, 838, 546), 8, fill=mix(GREEN_F, GREEN, 0.25 * hot(13.9)), outline=GREEN, a=ra, width=1.4)
    f.circle((96, 528), 10, fill=GREEN, a=ra)
    f.text((96, 528.5), "7", inter(11, 700), (255, 255, 255), ra, "mm")
    f.text((114, 528), "Result as text  ·  appended to the conversation as a tool_result", inter(12, 700), GREEN, ra)
    for x0, _, _ in EXEC:
        f.arrow((x0 + 90, 486), (x0 + 90, 507), (150, 200, 175), ra, 1.2, head=4)
    lp = v(14.2, 0.6)
    f.line((76, 528), (64, 528), GREEN, lp, 1.6)
    f.line((64, 528), (64, 252), GREEN, lp, 1.6)
    f.arrow((64, 252), (73, 252), GREEN, lp, 1.6, head=5)
    f.circle((82, 340), 10, fill=GREEN, a=lp)
    f.text((82, 340.5), "8", inter(11, 700), (255, 255, 255), lp, "mm")
    f.text((98, 334), "next round:", inter(10, 700), GREEN, lp)
    f.text((98, 348), "back to step 1", inter(10, 400), GREEN, lp)

    # ---- what the prompt contains
    pa = v(2.4)
    f.rrect((900, 196, 1232, 318), 10, fill=(255, 255, 255), outline=PANEL_B, a=pa, width=1.2)
    f.text((916, 212), "WHAT STEP 2 PUTS INTO THE PROMPT", inter(9.5, 700), LIGHT, pa)
    for i, s in enumerate(["system prompt", "tool definitions  (built-in + from MCP servers)", "CLAUDE.md  ·  one line per skill",
                           "the whole conversation: your request,", "every reply, every tool result"]):
        f.text((916, 232 + 17 * i), ("·  " if i < 4 else "   ") + s, inter(10.8, 400), INK, pa)

    # ---- NO branch
    na = v(18.8)
    f.arrow((843, 360), (896, 360), GREEN, na, 1.8, head=5.5)
    f.text((869, 346), "NO", inter(10, 700), GREEN, na, "mm")
    f.rrect((900, 334, 1232, 388), 10, fill=GREEN_F, outline=GREEN, a=na, width=1.8)
    f.text((916, 352), "Done: the reply is the answer", inter(13, 700), GREEN, na)
    f.text((916, 372), "shown to you, the loop ends", inter(10.8, 400), INK, na)

    # ---- who decides
    c = v(20.0)
    f.rrect((56, 574, 716, 640), 10, fill=DARK, a=c)
    f.text((74, 592), "Who decides that the task is finished?", inter(12.5, 700), (255, 255, 255), c)
    f.text((74, 612), "The LLM: it reads everything so far and writes an answer instead of a tool call.", inter(11, 400), (214, 219, 228), c)
    f.text((74, 628), "The harness does not judge. It only checks whether the reply contains a tool call.", inter(11, 400), (214, 219, 228), c)
    s = v(20.8)
    f.rrect((730, 574, 1232, 640), 10, fill=YELLOW_F, outline=YELLOW, a=s, width=1.3)
    f.text((746, 592), "Safety stops, enforced by the harness", inter(12, 700), YELLOW, s)
    f.text((746, 612), "you interrupt  ·  maximum rounds reached", inter(11, 400), INK, s)
    f.text((746, 628), "context window full  ·  permission denied", inter(11, 400), INK, s)

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [1.7, 2.8, 4.9, 6.2, 7.9, 10.3, 11.1, 12.2, 13.9, 14.9, 16.9, 18.0, 21.4, 24.5], "archd")
