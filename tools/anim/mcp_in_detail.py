"""07c: MCP as a sequence of messages. Startup (initialize, tools/list) and one tool call during the DCM task.
The LLM only ever talks to the harness; the harness's MCP client talks to the server."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, PURPLE, PURPLE_F, PURPLE_B,
                                ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import header, captions, main, mix, GREEN, GREEN_F, TEAL, TEAL_F, YELLOW, YELLOW_F

END = 24.0
XL, XH, XS, XB = 160, 480, 840, 1130            # lifelines: LLM, harness, MCP server, what the server uses
CAPS = [
    (0.8, 1, "A config file tells the harness which MCP servers to start"),
    (3.4, 2, "At startup: initialize, then tools/list. The server describes its tools"),
    (6.8, 3, "That tool schema joins the tool definitions in every prompt"),
    (9.6, 4, "During the task the LLM writes a tool call, exactly as for a built-in tool"),
    (12.6, 5, "The harness sees the mcp__ prefix and forwards it as a JSON-RPC tools/call"),
    (15.6, 6, "The server does the work (here: the RAG search) and returns text"),
    (19.0, 7, "The harness turns it into a tool_result. The LLM never talks to the server"),
]


def render(t):
    f = Frame(t)
    v = f.v
    header(f, "MCP in Detail: Who Talks to Whom", "EXTENDING CAPABILITIES  ·  MCP IN DETAIL", GREEN)
    f.text((1232, 45), "the tool:  search_spec,  provided by the “spec” MCP server", inter(12, 600), GREEN, v(0.1, 0.5), "rm")

    # ---- lifelines
    a = v(0.9)
    heads = [(XL, "LLM", "predicts tokens", PURPLE, PURPLE_F, 86),
             (XH, "Harness  (Claude Code)", "holds one MCP client per server", TEAL, TEAL_F, 150),
             (XS, "MCP server  “spec”", "a small program, local or remote", GREEN, GREEN_F, 130),
             (XB, "Spec index", "embedding model + vector DB", (107, 114, 128), PANEL, 100)]
    for x, name, sub, col, fill, hw in heads:
        f.rrect((x - hw, 108, x + hw, 152), 9, fill=fill, outline=col, a=a, width=1.6)
        f.text((x, 123), name, inter(12.5, 700), col, a, "mm")
        f.text((x, 140), sub, inter(9.8, 400), GREY, a, "mm")
        f.line((x, 152), (x, 566), (206, 210, 220), a, 1.2)
    f.text(((XL + XH) / 2, 166), "the model API", inter(9.5, 700), LIGHT, a, "mm")
    f.text(((XH + XS) / 2, 166), "MCP:  JSON-RPC 2.0 over stdio or HTTP", inter(9.5, 700), GREEN, a, "mm")
    f.text(((XS + XB) / 2, 166), "whatever the server needs", inter(9.5, 700), LIGHT, a, "mm")

    def msg(y, x0, x1, label, t0, col, font=None, sub=None, dashed=False):
        pr = v(t0, 0.45)
        if pr <= 0.01:
            return
        d = 1 if x1 > x0 else -1
        f.arrow((x0 + 4 * d, y), (x1 - 4 * d, y), col, 1, 1.6, prog=pr, head=5)
        la = v(t0 + 0.25)
        f.text(((x0 + x1) / 2, y - 9), label, font or mono(9.8), col if col != LIGHT else GREY, la, "mm")
        if sub:
            f.text(((x0 + x1) / 2, y + 10), sub, mono(9.2), GREY, la, "mm")

    def band(y0, y1, text, t0):
        ba = v(t0)
        f.rrect((40, y0, 1244, y1), 8, fill=(248, 250, 252), a=ba * 0.9)
        f.text((52, y0 + 11), text, inter(9.5, 700), LIGHT, ba)

    # ---- startup
    band(176, 300, "AT STARTUP  ·  before you type anything", 3.2)
    for x, *_ in heads:                                  # redraw lifelines over the band
        f.line((x, 176), (x, 300), (206, 210, 220), v(3.2), 1.2)
    msg(212, XH, XS, "initialize", 3.6, GREEN)
    msg(240, XH, XS, "tools/list", 4.4, GREEN)
    msg(268, XS, XH, "tools: [ search_spec + description + input schema ]", 5.2, GREEN)
    n = v(7.0)
    f.rrect((XH - 200, 278, XH + 12, 296), 5, fill=TEAL_F, outline=TEAL, a=n, width=1.1)
    f.text((XH - 94, 287), "kept as  mcp__spec__search_spec", mono(8.8), TEAL, n, "mm")
    f.arrow((XH - 204, 287), (XL + 60, 287), TEAL, n, 1.3, head=4.5)
    f.text((XL - 96, 287), "listed in every prompt", inter(9.8, 700), TEAL, v(7.4))

    # ---- during the task
    band(312, 566, "DURING THE TASK  ·  LLM call 3 of the DCM example", 9.4)
    for x, *_ in heads:
        f.line((x, 312), (x, 566), (206, 210, 220), v(9.4), 1.2)
    msg(346, XH, XL, "the prompt  ·  17.7k tokens", 9.8, TEAL, inter(10.5, 600))
    msg(380, XL, XH, "tool_use   mcp__spec__search_spec", 10.8, ORANGE, None, '{ query: "Dcm integration PduR ComM" }')
    r = v(12.8)
    f.rrect((XH - 150, 404, XH + 150, 424), 6, fill=TEAL_F, outline=TEAL, a=r, width=1.2)
    f.text((XH, 414), "prefix mcp__spec__  →  that server   ·   permission ok", inter(9.6, 600), TEAL, r, "mm")
    msg(448, XH, XS, "tools/call   search_spec", 13.6, GREEN, None, '{ query: "Dcm integration PduR ComM" }')
    msg(476, XS, XB, "embed the question, compare vectors", 15.8, (107, 114, 128), inter(10, 600))
    msg(500, XB, XS, "top 3 chunks", 16.6, (107, 114, 128), inter(10, 600))
    msg(526, XS, XH, 'result   content: [ { type: "text", text: … } ]', 17.4, GREEN, None, '"#412 …   #413 …   #414 …"')
    msg(552, XH, XL, "tool_result  ·  3 passages as text  ·  in the prompt of call 4", 19.2, TEAL, inter(10.2, 600))

    # ---- config and conclusion
    c0 = v(1.0)
    f.rrect((40, 578, 420, 640), 8, fill=DARK, a=c0)
    f.text((54, 592), ".mcp.json", mono(10), (148, 163, 184), c0)
    f.text((54, 610), '"spec": { "command": "python",', mono(10.4), (255, 255, 255), c0)
    f.text((54, 627), '          "args": ["spec_server.py"] }', mono(10.4), (255, 255, 255), c0)
    f.text((432, 592), "how the harness knows the server exists", inter(10.5, 600), GREY, v(1.6))
    c = v(20.4)
    f.rrect((432, 602, 1244, 640), 9, fill=GREEN_F, outline=GREEN, a=c, width=1.4)
    f.text((838, 621), "The LLM writes a tool call. The harness's MCP client does the talking. The answer returns as text.",
           inter(12, 700), GREEN, c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.4, 4.2, 5.0, 6.2, 8.0, 10.4, 11.6, 13.4, 14.6, 16.4, 17.2, 18.4, 20.0, 24.0], "mcp")
