"""06b: from chunks to vectors with an embedding model, and how that differs from the embedding layer inside the LLM."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, BLUE, BLUE_F, PURPLE, ORANGE,
                                PANEL, PANEL_B, DARK, W, H, S)
from gifout import rag_header, captions, main, mix, para, vec, chip, CHUNKS, GREEN, GREEN_F, TEAL, TEAL_F

END = 24.0
CAPS = [
    (0.8, 1, "Each chunk goes through an embedding model: a separate network, not the LLM"),
    (3.8, 2, "Out comes one vector for the whole chunk: its meaning as about 1,000 numbers"),
    (6.6, 3, "Vector, text and metadata are stored together in the vector database"),
    (9.2, 4, "Repeat for every chunk, once. This is the offline indexing step"),
    (12.2, 5, "Careful: this is not the embedding layer inside the LLM"),
    (15.8, 6, "Inside the LLM: one vector per token. Here: one vector per passage"),
]
ROWS = [("Input", "one token", "a whole passage"),
        ("How", "a table lookup, no computation", "a full network reads the passage"),
        ("Output", "250 tokens  →  250 vectors", "250 tokens  →  1 vector"),
        ("Captures", "the token by itself, no context", "what the passage is about"),
        ("Used for", "the first step inside the LLM", "finding similar text, outside the LLM")]


def render(t):
    f = Frame(t)
    v = f.v
    rag_header(f, "From Chunks to Vectors", 2)
    cap = inter(10.5, 700)

    # ---- one chunk through the embedding model
    a = v(1.0)
    cid, sec, page, text = CHUNKS[0]
    f.rrect((56, 126, 372, 214), 8, fill=(255, 255, 255), outline=GREEN, a=a, width=1.3)
    f.rrect((56, 126, 372, 148), 8, fill=GREEN_F, a=a)
    f.text((68, 137), f"chunk {cid}   {sec}  ·  {page}", mono(10.2), GREEN, a)
    para(f, 68, 162, text, inter(10.4, 400), INK, a, 294, 14.5, max_lines=3)
    f.arrow((378, 170), (418, 170), TEAL, 1, 1.7, prog=v(1.6, 0.3))
    m = v(1.8)
    f.rrect((422, 130, 640, 210), 12, fill=TEAL_F, outline=TEAL, a=m, width=1.8)
    s = (t - 2.4) / 1.1
    if 0 < s < 1:
        f.rrect((430 + 170 * s, 138, 460 + 170 * s, 202), 7, fill=(170, 222, 230), a=0.8 * (1 - abs(s - 0.5) * 1.3))
    f.text((531, 158), "Embedding model", inter(15, 700), TEAL, m, "mm")
    f.text((531, 180), "a separate, smaller network", inter(11, 500), INK, m, "mm")
    f.text((531, 196), "not the LLM that answers you", inter(11, 400), GREY, m, "mm")
    f.arrow((646, 170), (686, 170), TEAL, 1, 1.7, prog=v(3.7, 0.3))
    va = v(4.0)
    vec(f, 692, 150, 412, 24, va, cell=11, h=18)
    f.text((692, 184), "1 vector for the whole chunk", inter(12, 700), INK, va)
    f.text((692, 202), "[ 0.21, −0.64, 0.08, 0.37, … ]   about 1,000 numbers", mono(10.2), GREY, v(4.5))
    f.text((1232, 137), "size depends on the model", inter(10, 400), LIGHT, v(4.5), "rm")

    # ---- the vector database
    d = v(6.8)
    f.text((56, 236), "VECTOR DATABASE", cap, LIGHT, d)
    f.rrect((56, 248, 1232, 356), 9, fill=PANEL, outline=PANEL_B, a=d, width=1)
    for x, name in ((72, "ID"), (150, "VECTOR"), (452, "TEXT  (kept next to the vector)"), (1040, "METADATA")):
        f.text((x, 262), name, inter(9.2, 700), LIGHT, d)
    for i, (cid, sec, page, text) in enumerate(CHUNKS):
        ra = v(7.0 if i == 0 else 9.4 + 0.5 * (i - 1))
        y = 284 + 22 * i
        f.text((72, y), cid, mono(11), GREEN, ra)
        vec(f, 150, y - 7, 412 + i, 24, ra, cell=10, h=14)
        f.text((452, y), text[:74] + " …", inter(10.6, 400), INK, ra)
        f.text((1040, y), f"{sec}  ·  {page}", mono(10.2), GREY, ra)
    f.text((72, 346), "…   1,840 rows, built once and reused for every question", inter(10.8, 600), INK, v(10.6))

    # ---- two different things called "embedding"
    L, R = v(12.4), v(13.4)
    f.text((56, 376), "TWO DIFFERENT THINGS ARE CALLED “EMBEDDING”", cap, ORANGE, v(12.3))
    f.rrect((56, 390, 634, 600), 10, fill=(255, 255, 255), outline=BLUE, a=L, width=1.5)
    f.rrect((654, 390, 1232, 600), 10, fill=(255, 255, 255), outline=TEAL, a=R, width=1.5)
    f.text((72, 409), "Embedding layer inside the LLM", inter(13.5, 700), BLUE, L)
    f.text((618, 409), "pages 02a–02d", inter(10.5, 500), GREY, L, "rm")
    f.text((670, 409), "Embedding model for search", inter(13.5, 700), TEAL, R)
    f.text((1216, 409), "this page", inter(10.5, 500), GREY, R, "rm")
    toks = ["The", "·Dcm", "·receives", "…"]
    for side, base, al in ((0, 76, L), (1, 674, R)):
        x = base
        cxs = []
        for tk in toks:
            w = mono(11).getlength(tk) / S + 14
            f.rrect((x, 428, x + w, 448), 5, fill=BLUE_F, outline=BLUE, a=al, width=1.1)
            f.text((x + w / 2, 438), tk, mono(11), BLUE, al, "mm")
            cxs.append(x + w / 2)
            x += w + 26
        if side == 0:
            for j, cx in enumerate(cxs):
                f.arrow((cx, 450), (cx, 462), LIGHT, al, 1.2, head=3.5)
                vec(f, cx - 21, 465, 50 + j, 6, al, cell=6, h=10)
            f.text((x + 4, 458), "one vector per token", inter(11, 700), BLUE, al)
        else:
            for cx in cxs:
                f.line((cx, 450), (cx, 458), LIGHT, al, 1.2)
            f.line((cxs[0], 458), (cxs[-1], 458), LIGHT, al, 1.2)
            mid = (cxs[0] + cxs[-1]) / 2
            f.arrow((mid, 458), (mid, 464), LIGHT, al, 1.2, head=3.5)
            f.rrect((mid - 70, 465, mid + 70, 479), 4, fill=TEAL_F, outline=TEAL, a=al, width=1.1)
            f.text((mid, 472), "network + pooling", inter(9, 700), TEAL, al, "mm")
            f.arrow((mid + 74, 472), (mid + 104, 472), LIGHT, al, 1.2, head=3.5)
            vec(f, mid + 110, 467, 412, 6, al, cell=6, h=10)
            f.text((mid + 160, 472), "one vector per passage", inter(11, 700), TEAL, al)
    for i, (name, left, right) in enumerate(ROWS):
        ra = v(16.0 + 0.5 * i)
        y = 500 + 19 * i
        f.text((72, y), name, inter(10.5, 700), GREY, ra)
        f.text((142, y), left, inter(11.2, 600 if i == 2 else 400), INK, ra)
        f.text((670, y), name, inter(10.5, 700), GREY, ra)
        f.text((740, y), right, inter(11.2, 600 if i == 2 else 400), INK, ra)

    c = v(19.6)
    f.rrect((56, 610, 1232, 646), 9, fill=DARK, a=c)
    f.text((644, 628), "Same idea (meaning as direction), different job:  one feeds the network, the other is for searching.",
           inter(12.5, 600), (255, 255, 255), c, "mm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [1.6, 2.9, 4.6, 6.0, 7.6, 9.8, 11.4, 12.9, 14.4, 16.4, 17.6, 18.8, 20.6, 24.0], "rag2")
