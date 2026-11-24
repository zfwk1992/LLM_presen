"""06a: from a PDF specification to text chunks. Plain text processing; no model involved yet.
Section numbers, pages and wording are illustrative."""
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, GREY, LIGHT, ORANGE, ORANGE_F, PANEL, PANEL_B,
                                DARK, W, H)
from gifout import rag_header, captions, main, mix, wrap, para, CHUNKS, OVERLAP, GREEN, GREEN_F, YELLOW, YELLOW_F

END = 22.0
CAPS = [
    (0.8, 1, "The specification is a 600-page PDF: far too big for the prompt"),
    (3.8, 2, "Step 1: extract the plain text. Layout, headers and page breaks go"),
    (7.4, 3, "Step 2: cut the text into chunks of a few hundred tokens"),
    (11.4, 4, "Chunks follow the section structure and overlap a little"),
    (14.6, 5, "Each chunk keeps its metadata: id, section, page"),
    (17.6, 6, "Result: about 1,800 small pieces. Still text, not vectors"),
]


def render(t):
    f = Frame(t)
    v = f.v
    rag_header(f, "From a PDF to Chunks", 1)
    cap = inter(10.5, 700)

    # ---- the PDF
    pa = v(1.0)
    f.text((60, 118), "THE PDF", cap, LIGHT, pa)
    for off in (10, 5):
        f.rrect((60 + off, 132 + off, 296 + off, 512 + off), 4, fill=(255, 255, 255), outline=PANEL_B, a=pa, width=1)
    f.rrect((60, 132, 296, 512), 4, fill=(255, 255, 255), outline=(170, 176, 190), a=pa, width=1.3)
    f.text((74, 148), "AUTOSAR  ·  Diagnostic Communication Manager", inter(7.6, 500), LIGHT, pa)
    f.line((74, 158), (282, 158), PANEL_B, pa, 1)
    f.text((74, 176), "7.2   Interaction with other modules", inter(10, 700), INK, pa)
    f.text((74, 198), "7.2.1   PduR", inter(9.5, 700), INK, pa)
    y = 212
    for wd in (208, 200, 208, 190, 208, 120):
        f.rrect((74, y, 74 + wd, y + 5), 2, fill=(214, 218, 226), a=pa); y += 11
    f.text((74, y + 14), "7.2.2   ComM", inter(9.5, 700), INK, pa); y += 28
    for wd in (208, 196, 208, 90):
        f.rrect((74, y, 74 + wd, y + 5), 2, fill=(214, 218, 226), a=pa); y += 11
    y += 10
    for r in range(4):                                   # a table
        for c in range(3):
            f.rrect((74 + c * 70, y + r * 14, 74 + c * 70 + 68, y + r * 14 + 12), 1,
                    fill=(236, 239, 244) if r == 0 else None, outline=(206, 210, 220), a=pa, width=0.8)
    y += 68
    f.rrect((74, y, 282, y + 58), 3, outline=(206, 210, 220), a=pa, width=0.8)   # a figure
    f.text((178, y + 29), "figure", inter(8.5, 500), LIGHT, pa, "mm")
    f.text((178, 500), "212 of 600", inter(7.6, 500), LIGHT, pa, "mm")
    f.text((60, 536), "600 pages  ·  about 450,000 tokens", inter(11.5, 600), INK, v(1.6))
    f.text((60, 554), "tables and figures need extra care", inter(10.5, 400), GREY, v(2.2))

    # ---- step 1: plain text
    ta = v(4.0)
    f.arrow((312, 322), (346, 322), LIGHT, 1, 1.6, prog=v(3.9, 0.3))
    f.text((352, 118), "1   EXTRACTED TEXT", cap, LIGHT, ta)
    f.rrect((352, 132, 648, 512), 8, fill=PANEL, outline=PANEL_B, a=ta, width=1)
    body, head = inter(10.6, 400), inter(10.6, 700)
    yy = 152
    cuts = []
    f.text((366, yy), "7.2.1 Interaction with PduR", head, INK, v(4.3)); yy += 18
    yy = para(f, 366, yy, CHUNKS[0][3], body, INK, v(4.7), 268, 15.5) + 3
    cuts.append(yy)
    yy += 8
    yy = para(f, 366, yy, CHUNKS[1][3], body, INK, v(5.2), 268, 15.5) + 3
    cuts.append(yy)
    yy += 8
    f.text((366, yy), "7.2.2 Interaction with ComM", head, INK, v(5.7)); yy += 18
    yy = para(f, 366, yy, CHUNKS[2][3], body, INK, v(6.1), 268, 15.5) + 3
    cuts.append(yy)
    f.text((366, yy + 14), "…", head, LIGHT, v(6.3))
    for i, cy in enumerate(cuts):
        ca = v(7.7 + 0.35 * i, 0.3)
        x = 360
        while x < 640:
            f.line((x, cy), (min(x + 5, 640), cy), ORANGE, ca, 1.4); x += 9
    f.text((640, cuts[0] - 9), "cut", inter(9.5, 700), ORANGE, v(7.7), "rm")

    # ---- step 2: chunks
    f.arrow((664, 322), (698, 322), LIGHT, 1, 1.6, prog=v(8.3, 0.3))
    f.text((704, 118), "2   CHUNKS", cap, LIGHT, v(8.5))
    meta = clamp(1 - abs(t - 15.6) / 1.4)
    for i, (cid, sec, page, text) in enumerate(CHUNKS):
        a = v(8.6 + 0.7 * i)
        y0 = 132 + 114 * i
        f.rrect((704, y0, 1232, y0 + 102), 8, fill=(255, 255, 255), outline=GREEN, a=a, width=1.3)
        f.rrect((704, y0, 1232, y0 + 26), 8, fill=mix(GREEN_F, (190, 232, 210), meta), a=a)
        f.text((718, y0 + 13), f"chunk {cid}", mono(11), GREEN, a)
        f.text((816, y0 + 13), f"{sec}   ·   {page}   ·   about 250 tokens", mono(10.2), GREY, a)
        ty = y0 + 44
        if i == 1:                                        # overlap with the previous chunk
            oa = v(11.7)
            w = inter(11, 400).getlength(OVERLAP) / 2 + 8
            f.rrect((714, ty - 9, 714 + w, ty + 9), 3, fill=YELLOW_F, outline=YELLOW, a=a * oa, width=1)
            f.text((718, ty), OVERLAP, inter(11, 400), INK, a * max(oa, 0.0))
            f.text((714 + w + 8, ty), "overlap: repeated from #412", inter(9.8, 700), YELLOW, a * oa)
            ty += 17 * oa
        para(f, 718, ty, text + " …", inter(11, 400), INK, a, 498, 16, max_lines=3)
    f.text((1222, 145), "metadata", inter(9.8, 700), GREEN, meta, "rm")
    f.text((704, 484), "…  1,840 chunks in total", inter(12.5, 700), INK, v(17.8))
    f.text((704, 503), "each a few hundred tokens, each with its id, section and page", inter(11, 400), GREY, v(18.1))
    f.text((704, 524), "A sentence cut in half would lose its meaning: hence sections and overlap.", inter(10.8, 400), GREY, v(12.4))

    c = v(18.8)
    f.rrect((352, 572, 1232, 612), 9, fill=DARK, a=c)
    f.text((792, 592), "Chunking is ordinary text processing.  No AI model has been used yet.", inter(13, 600), (255, 255, 255), c, "mm")
    f.text((1232, 628), "section numbers, pages and wording are illustrative", inter(10.5, 400), LIGHT, v(4.4), "rm")

    captions(f, CAPS)
    return f.im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    main(render, END, [2.6, 4.6, 5.6, 6.8, 8.2, 9.4, 10.6, 12.2, 13.6, 15.6, 16.8, 18.4, 20.0, 22.0], "rag1")
