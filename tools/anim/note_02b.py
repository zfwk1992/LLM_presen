"""Add a clarifying note to 02b: cosine similarity is a property of the space, not a pipeline step."""
import os, sys
import numpy as np
from PIL import Image, ImageSequence
from inside_transformer import Frame, inter, ORANGE, ORANGE_F, INK, GREY, W, H

src, out, prev = sys.argv[1], sys.argv[2], sys.argv[3]
write = len(sys.argv) > 4 and sys.argv[4] == "write"
F = [np.asarray(f.convert("RGB")).copy() for f in ImageSequence.Iterator(Image.open(os.path.join(src, "02_embedding.gif")))][172:349]
BOX = (860, 546, 1230, 640)
region = np.stack([fr[BOX[1]:BOX[3], BOX[0]:BOX[2]] for fr in F])
print("frames", len(F), "region min value (255 = empty in every frame):", int(region.min()))

fr_ = Frame(0)
fr_.rrect((BOX[0] + 1, BOX[1] + 1, BOX[2] - 1, BOX[3] - 1), 10, fill=ORANGE_F, outline=ORANGE, width=1.3)
fr_.text((BOX[0] + 18, BOX[1] + 22), "Not a step in the pipeline", inter(14, 700), ORANGE)
for k, s in enumerate(["This is not computed before the vectors go in.",
                       "It only shows what training produced.",
                       "The vectors go straight into the network."]):
    fr_.text((BOX[0] + 18, BOX[1] + 44 + 17 * k), s, inter(11.8, 600 if k == 2 else 400), INK if k == 2 else GREY)
note = np.asarray(fr_.im.resize((W, H), Image.LANCZOS))[BOX[1]:BOX[3], BOX[0]:BOX[2]].astype(float)

START, FADE = 132, 8
res, ps = [], []
for i, fr in enumerate(F):
    a = min(1.0, max(0.0, (i - START) / FADE))
    a = 1 - (1 - a) ** 3
    o = fr.copy()
    if a > 0:
        bg = fr[BOX[1]:BOX[3], BOX[0]:BOX[2]].astype(float)
        patch = np.rint(bg + (note - bg) * a).astype(np.uint8)
        # stay within 256 colours: keep the frame's colours, add the most common new ones, snap the rest
        pal = np.unique(fr.reshape(-1, 3), axis=0)
        uniq, inv, cnt = np.unique(patch.reshape(-1, 3), axis=0, return_inverse=True, return_counts=True)
        known = (uniq[:, None, :] == pal[None, :, :]).all(-1).any(1)
        room = 256 - len(pal)
        new = np.where(~known)[0]
        keep = new[np.argsort(-cnt[new])][:max(room, 0)]
        full = np.concatenate([pal, uniq[keep]]).astype(int)
        d = ((uniq[:, None, :].astype(int) - full[None, :, :]) ** 2).sum(-1)
        o[BOX[1]:BOX[3], BOX[0]:BOX[2]] = full[d.argmin(1)][inv.reshape(-1)].reshape(patch.shape).astype(np.uint8)
    res.append(o)
Image.fromarray(res[-1]).save(os.path.join(prev, "p02b_last.png"))
if write:
    for a in res:
        rgb = Image.fromarray(a)
        cols = rgb.getcolors(maxcolors=256)
        assert cols is not None
        pl = [v for _, c in cols for v in c]
        pimg = Image.new("P", (1, 1)); pimg.putpalette(pl + [0] * (768 - len(pl)))
        p = rgb.quantize(palette=pimg, dither=Image.Dither.NONE); p.info.clear()
        ps.append(p)
    path = os.path.join(out, "02b_embedding_space.gif")
    ps[0].save(path, save_all=True, append_images=ps[1:], duration=[50] * (len(ps) - 1) + [3000], optimize=False, disposal=1)
    print("written %.2f MB" % (os.path.getsize(path) / 1e6))
