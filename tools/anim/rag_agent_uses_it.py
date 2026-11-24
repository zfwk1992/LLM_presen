"""06c: how the agent uses the index. A tool call searches by vector; the TEXT of the best chunks returns to the prompt."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, PURPLE, PURPLE_F, PURPLE_B,
                                ORANGE, ORANGE_F, PANEL, PANEL_B, DARK, W, H)
from gifout import rag_header, captions, main, mix, para, vec, CHUNKS, GREEN, GREEN_F, TEAL, TEAL_F

END = 23.0
# id, section, text snippet, similarity, vector seed
DB = [("#97", "§5.1", "Dependencies to other modules: header file structure …", 0.41, 97),
      ("#412", "§7.2.1", "The Dcm receives diagnostic requests from the PduR …", 0.91, 412),
      ("#413", "§7.2.1", "The response is sent with PduR_DcmTransmit …", 0.88, 413),
      ("#414", "§7.2.2", "… keeps the channel awake by calling ComM_DCM_Active…", 0.86, 414),
      ("#655", "§8.3", "Dcm_GetSesCtrlType returns the active session …", 0.22, 655),
      ("#1502", "§10.2", "Configuration container DcmDsdServiceTable …", 0.18, 1502)]
TOP = {1, 2, 3}
CAPS = [
    (0.8, 1, "In call 3 the LLM writes a tool call: search the specification"),
    (3.4, 2, "The harness runs the search tool. The question is embedded by the same model"),
    (7.4, 3, "The question vector is compared with all 1,840 chunk vectors"),
    (11.4, 4, "The three closest chunks win. This is cosine similarity at work"),
    (14.2, 5, "Their text, not their vectors, goes back as the tool result"),
    (17.6, 6, "The LLM reads 3 passages instead of 600 pages. It never sees a vector"),
]


def render(t):
    f = Frame(t)
    v = f.v
    rag_header(f, "How the Agent Uses It", 3)
    cap = inter(10.5, 700)

    # ---- row 1: tool call -> search tool -> embedding model -> question vector
    a = v(1.0)
    f.rrect((56, 126, 330, 214), 10, fill=(255, 255, 255), outline=PURPLE_B, a=a, width=1.4)
    f.rrect((68, 136, 140, 154), 9, fill=PURPLE, a=a)
    f.text((104, 145), "LLM CALL 3", inter(8.8, 700), (255, 255, 255), a, "mm")
    f.text((150, 145), "writes a tool call", inter(11, 500), GREY, a)
    f.text((68, 172), 'search_spec("Dcm integration', mono(11), ORANGE, v(1.5))
    f.text((68, 189), '            PduR ComM")', mono(11), ORANGE, v(1.5))
    f.text((68, 205), "just text, as always", inter(9.8, 400), LIGHT, v(2.0))
    f.arrow((336, 170), (372, 170), ORANGE, 1, 1.7, prog=v(3.5, 0.3))
    b = v(3.7)
    f.rrect((376, 130, 612, 210), 12, fill=TEAL_F, outline=TEAL, a=b, width=1.8)
    f.text((494, 158), "Search tool", inter(15, 700), TEAL, b, "mm")
    f.text((494, 180), "run by the harness", inter(11, 500), INK, b, "mm")
    f.text((494, 196), "e.g. provided by an MCP server", inter(10.5, 400), GREY, b, "mm")
    f.arrow((618, 170), (654, 170), TEAL, 1, 1.7, prog=v(4.3, 0.3))
    e = v(4.5)
    f.rrect((658, 130, 858, 210), 12, fill=(255, 255, 255), outline=TEAL, a=e, width=1.8)
    s = (t - 4.9) / 0.9
    if 0 < s < 1:
        f.rrect((666 + 150 * s, 138, 696 + 150 * s, 202), 7, fill=(170, 222, 230), a=0.8 * (1 - abs(s - 0.5) * 1.3))
    f.text((758, 160), "Embedding model", inter(13.5, 700), TEAL, e, "mm")
    f.text((758, 182), "the same one used", inter(10.5, 400), GREY, e, "mm")
    f.text((758, 196), "to build the index", inter(10.5, 400), GREY, e, "mm")
    f.arrow((864, 170), (900, 170), TEAL, 1, 1.7, prog=v(5.5, 0.3))
    q = v(5.8)
    f.text((906, 140), "QUESTION VECTOR", cap, LIGHT, q)
    vec(f, 906, 152, 9001, 24, q, cell=11, h=18)
    f.text((906, 186), "the question as about 1,000 numbers", inter(11, 500), INK, q)
    f.text((906, 203), "same space as the chunk vectors", inter(10.5, 400), GREY, q)

    # ---- row 2: compare with every row
    d = v(7.6)
    f.text((56, 234), "VECTOR DATABASE  ·  1,840 chunks", cap, LIGHT, d)
    f.rrect((56, 246, 800, 462), 9, fill=PANEL, outline=PANEL_B, a=d, width=1)
    for x, name in ((72, "ID"), (130, "VECTOR"), (310, "TEXT STORED WITH IT"), (656, "SIMILARITY")):
        f.text((x, 260), name, inter(9.2, 700), LIGHT, d)
    picked = v(11.6)
    for i, (cid, sec, text, sim, seed) in enumerate(DB):
        y = 284 + 29 * i
        top = i in TOP
        ra = d * (1 if top else 1 - 0.6 * picked)
        if top:
            f.rrect((64, y - 13, 792, y + 13), 5, fill=GREEN_F, outline=GREEN, a=d * picked, width=1.3)
        f.text((72, y), cid, mono(11), GREEN if top else GREY, ra)
        vec(f, 130, y - 7, seed, 15, ra, cell=10, h=14)
        f.text((310, y), text, inter(10.4, 400), INK, ra)
        sa = v(8.4 + 0.4 * i)
        g = ease((t - (8.5 + 0.4 * i)) / 0.6)
        f.rrect((656, y - 6, 656 + max(2, 84 * sim * g), y + 6), 3, fill=GREEN if top else (176, 184, 198), a=ra * sa)
        f.text((750, y), f"{sim * g:.2f}", mono(11), INK, ra * sa)
    f.text((72, 452), "…  and 1,834 more rows", inter(10, 400), LIGHT, d)
    # the question vector is compared with every row
    cmp_ = v(7.9)
    f.line((1040, 216), (1040, 258), TEAL, cmp_, 1.5)
    f.line((1040, 258), (806, 258), TEAL, cmp_, 1.5)
    f.arrow((812, 258), (802, 258), TEAL, cmp_, 1.5, head=5)
    f.text((1048, 240), "compared with every row", inter(10.8, 700), TEAL, cmp_)
    f.text((1048, 256), "cos θ = a · b / (‖a‖ ‖b‖)", mono(10), GREY, v(8.6))

    # ---- the result is text
    r = v(14.4)
    f.arrow((806, 370), (836, 370), GREEN, 1, 1.7, prog=v(14.2, 0.3))
    f.rrect((840, 282, 1232, 462), 10, fill=(255, 255, 255), outline=GREEN, a=r, width=1.5)
    f.text((854, 298), "tool_result", mono(11.5), GREEN, r)
    f.text((1218, 298), "the TEXT of the top 3  ·  about 1,800 tokens", inter(9.8, 600), GREY, r, "rm")
    for i, (cid, sec, page, text) in enumerate(CHUNKS):
        ya = v(14.8 + 0.35 * i)
        y0 = 320 + 46 * i
        f.text((854, y0), f"{cid}  {sec}  {page}", mono(9.8), GREEN, ya)
        para(f, 854, y0 + 15, text, inter(10, 400), INK, ya, 366, 13.5, max_lines=2)

    k = v(15.8)
    f.rrect((56, 478, 800, 524), 9, fill=GREEN_F, outline=GREEN, a=k, width=1.4)
    f.text((428, 492), "Vectors are only used to FIND the right pieces.", inter(13, 700), GREEN, k, "mm")
    f.text((428, 511), "What goes into the prompt is their text.", inter(12, 500), INK, k, "mm")
    n = v(17.8)
    f.arrow((1036, 466), (1036, 484), GREEN, 1, 1.7, prog=v(17.7, 0.3))
    f.text((1036, 498), "appended to the prompt  (+1.8k)", inter(11.5, 700), GREEN, n, "mm")
    f.text((1036, 515), "LLM call 4 reads it like any other text", inter(10.8, 400), GREY, n, "mm")

    c = v(18.8)
    f.rrect((56, 548, 1232, 590), 9, fill=DARK, a=c)
    f.text((644, 569), "600 pages stay on disk.   3 passages enter the prompt.   The LLM never sees a vector from this database.",
           inter(12.8, 600), (255, 255, 255), c, "mm")
    f.text((1232, 612), "similarity values, section numbers and wording are illustrative", inter(10.5, 400), LIGHT, v(7.8), "rm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.2, 4.0, 5.3, 6.6, 8.2, 9.4, 10.8, 12.4, 13.8, 15.2, 16.6, 18.2, 20.0, 23.0], "rag3")
