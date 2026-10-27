"""Figure: what moving, rotating and dense stars do to absorption lines.

Hydrogen lines (Balmer, R = 1.097e7 m^-1): 410.2, 434.1, 486.2, 656.3 nm.
Shifts are EXAGGERATED for the drawing: each line moves by lambda * v / c with
v / c = 0.015 (real stars: about 0.0001). Every line moves by the same FRACTION of
its wavelength, so the pattern is kept. Broad lines: 4 times wider, same centres.
Run: python3 -I src/mod7/figures/ch1_starlines.py
"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
sys.path.insert(0, str(HERE))
import hscplot                                   # noqa: E402
from ch1_common import wl_rgb                    # noqa: E402
import numpy as np                               # noqa: E402

R = 1.097e7
LAB = [1e9 / (R * (1 / 4 - 1 / n**2)) for n in (3, 4, 5, 6)]
BETA = 0.015
W0, W1 = 400, 700
ws = np.linspace(W0, W1, 1200)
base = np.array([wl_rgb(w) for w in ws])


def strip(centres, half_width=1.4, soft=False):
    out = base.copy()
    for L in centres:
        if soft:   # broad, fuzzy line: smooth dip
            depth = np.exp(-0.5 * ((ws - L) / (2.2 * half_width)) ** 2)
            out = out * (1 - 0.92 * depth[:, None])
        else:
            out[np.abs(ws - L) < half_width] = 0.0
    return out[None, :, :]


rows = [
    (strip(LAB), "Laboratory (source not moving): the reference"),
    (strip([L * (1 + BETA) for L in LAB]), "Star moving away: every line shifts to longer wavelength (redshift)"),
    (strip([L * (1 - BETA) for L in LAB]), "Star moving towards us: every line shifts to shorter wavelength (blueshift)"),
    (strip(LAB, soft=True), "Fast-rotating star, or a denser atmosphere: wider lines, same centres"),
]
fig, axs = hscplot.figure(width_mm=124, height_mm=60, nrows=4, sharex=True)
for ax, (img, title) in zip(axs, rows):
    ax.imshow(img, extent=(W0, W1, 0, 1), aspect="auto")
    ax.set_yticks([])
    ax.grid(False)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, loc="left", fontsize=8, color=hscplot.INK, pad=2.5)
    ax.tick_params(axis="x", length=2)
    for L in LAB:     # guide lines at the laboratory positions
        ax.plot([L, L], [-0.25, 1.25], color=hscplot.INK, lw=0.5, ls=(0, (1.5, 1.5)), clip_on=False)
axs[-1].set_xticks(range(400, 701, 50))
axs[-1].set_xlabel("Wavelength (nm)   (dotted lines = laboratory positions; shifts exaggerated)")
fig.subplots_adjust(hspace=0.9)
hscplot.save(fig, __file__)
