"""Shared pieces for the newer pages: header, caption pill, token chip, GIF writer."""
import os, sys
from PIL import Image
from inside_transformer import (Frame, inter, mono, ease, clamp, INK, BLUE, BLUE_F, PURPLE, ORANGE, ORANGE_F,
                                PANEL, PANEL_B, W, H, FPS, S)


def mix(c0, c1, m):
    m = clamp(m)
    return tuple(round(a + (b - a) * m) for a, b in zip(c0, c1))


GREEN, GREEN_F = (30, 158, 106), (226, 245, 236)
TEAL, TEAL_F = (20, 148, 165), (222, 242, 245)
YELLOW, YELLOW_F = (202, 138, 4), (253, 243, 215)
SLATE, SLATE_F = (107, 114, 128), (229, 231, 235)


REQUEST = "How do we integrate DCM into this project?"
SKILL = "dcm-integration"


def example_header(f, title, part):
    """Header for the five pages that follow one request through the agent."""
    header(f, title, f"FROM LLM TO AI AGENT  ·  ONE EXAMPLE, PART {part} OF 5", PURPLE)
    a0 = f.v(0.1, 0.5)
    f.text((1232, 45), "the request:  “" + REQUEST + "”", inter(12, 600), BLUE, a0, "rm")


# Three chunks of the (illustrative) Dcm specification, shared by the RAG pages.
CHUNKS = [
    ("#412", "§7.2.1", "p. 212",
     "The Dcm receives diagnostic requests from the PduR. Reception starts with Dcm_StartOfReception; "
     "the data is copied with Dcm_CopyRxData and finished by Dcm_TpRxIndication."),
    ("#413", "§7.2.1", "p. 213",
     "The response is sent with PduR_DcmTransmit. The PduR fetches the data through Dcm_CopyTxData "
     "and confirms with Dcm_TpTxConfirmation."),
    ("#414", "§7.2.2", "p. 213",
     "While a request is processed, the Dcm keeps the channel awake by calling ComM_DCM_ActiveDiagnostic "
     "and releases it with ComM_DCM_InactiveDiagnostic."),
]
OVERLAP = "… finished by Dcm_TpRxIndication."


def rag_header(f, title, part):
    header(f, title, f"EXTENDING CAPABILITIES  ·  RAG IN DETAIL, PART {part} OF 3", GREEN)
    f.text((1232, 45), "the document:  AUTOSAR_SWS_Dcm.pdf  ·  600 pages", inter(12, 600), GREEN, f.v(0.1, 0.5), "rm")


def wrap(text, font, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if font.getlength(trial) / S <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines


def para(f, x, y, text, font, col, a, maxw, lh, max_lines=99):
    """Draw wrapped text; returns the y of the line after the last one."""
    lines = wrap(text, font, maxw)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,;") + " …"
    for i, line in enumerate(lines):
        f.text((x, y + lh * i), line, font, col, a)
    return y + lh * len(lines)


def vec(f, x, y, seed, n, a=1.0, cell=10, h=14):
    """A small vector strip with n cells."""
    import random
    from inside_transformer import CELLS
    r = random.Random(seed)
    for i in range(n):
        f.rrect((x + i * (cell + 1), y, x + i * (cell + 1) + cell, y + h), 2, fill=CELLS[r.randrange(len(CELLS))], a=a)


def settings_header(f, title):
    """Header for the Claude Code pages that reuse the same request."""
    header(f, title, "CLAUDE CODE  ·  THE SAME EXAMPLE", ORANGE)
    f.text((1232, 45), "the request:  “" + REQUEST + "”", inter(12, 600), BLUE, f.v(0.1, 0.5), "rm")


def header(f, title, tag="LLM FUNDAMENTALS", col=BLUE):
    a0 = f.v(0.1, 0.5)
    f.spaced((56, 45), tag, inter(12, 700), col, a0, 1.7)
    f.text((56, 77), title, inter(30, 700), INK, a0)


def chip(f, cx, cy, tok, a, orange=False, size=17):
    fm = mono(size)
    w = fm.getlength(tok) / S + 20
    col, fill = (ORANGE, ORANGE_F) if orange else (BLUE, BLUE_F)
    f.rrect((cx - w / 2, cy - 15, cx + w / 2, cy + 15), 6, fill=fill, outline=col, a=a)
    f.text((cx, cy), tok, fm, col, a, "mm")
    return w


def captions(f, caps):
    t = f.t
    for k, (st, num, txt) in enumerate(caps):
        nxt = caps[k + 1][0] if k + 1 < len(caps) else 1e9
        a = min(ease((t - st) / 0.3), 1 - ease((t - (nxt - 0.6)) / 0.3))
        if a <= 0.003:
            continue
        fc = inter(19, 500)
        w = fc.getlength(txt) / S + 86
        x0 = 640 - w / 2
        f.rrect((x0, 657, x0 + w, 695), 19, fill=PANEL, outline=PANEL_B, a=a, width=1)
        f.circle((x0 + 22, 676), 4, fill=ORANGE, a=a)
        f.circle((x0 + 47, 676), 11, outline=INK, a=a, width=1.4)
        f.text((x0 + 47, 676.5), str(num), inter(13.5, 600), INK, a, "mm")
        f.text((x0 + 66, 676), txt, fc, INK, a)


def main(render, end, keys, prefix):
    """python script.py out.gif            -> full GIF (plays once, holds on the last frame)
       python script.py dir preview 3 9.5  -> PNG frames at those times"""
    out = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        os.makedirs(out, exist_ok=True)
        for tt in [float(x) for x in sys.argv[3:]]:
            render(tt).save(os.path.join(out, f"{prefix}_{tt:05.1f}.png"))
        return
    n = int(end * FPS) + 1
    mosaic = Image.new("RGB", (W, H * len(keys)), (255, 255, 255))
    for k, tk in enumerate(keys):
        mosaic.paste(render(tk), (0, H * k))
    pal = mosaic.quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pl = pal.getpalette()[:765]
    for key in (ORANGE, BLUE, PURPLE):  # keep the accent colours exact
        j = min(range(255), key=lambda q: sum((pl[q * 3 + c] - key[c]) ** 2 for c in range(3)))
        pl[j * 3:j * 3 + 3] = list(key)
    pal.putpalette(pl)
    ps = []
    for i in range(n):
        fr = Image.new("RGB", (W, H), (255, 255, 255)) if i < 2 else render(i / FPS)
        p = fr.quantize(palette=pal, dither=Image.Dither.NONE); p.info.clear()
        ps.append(p)
    ps[0].save(out, save_all=True, append_images=ps[1:], duration=[50] * (n - 1) + [3000], optimize=False, disposal=1)
    print("frames", n, "size %.2f MB" % (os.path.getsize(out) / 1e6))
