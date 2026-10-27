"""White light through a grating with 300 lines per mm (d = 3.33 um).

Each wavelength from 400 nm to 700 nm is drawn at the angles given by
d sin(theta) = m lambda, for m = 0, +-1, +-2, +-3. Each order has its own row
under one angle axis, so the overlap of orders 2 and 3 (21.1 to 24.8 degrees)
can be seen. Run: python3 -I ch2_spectra.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402
import numpy as np                                        # noqa: E402
import matplotlib.pyplot as plt                           # noqa: E402


def wl_rgb(w):
    """Approximate colour of light of wavelength w (nm), 380-780 nm (Bruton)."""
    if w < 440:
        r, g, b = -(w - 440) / 60, 0.0, 1.0
    elif w < 490:
        r, g, b = 0.0, (w - 440) / 50, 1.0
    elif w < 510:
        r, g, b = 0.0, 1.0, -(w - 510) / 20
    elif w < 580:
        r, g, b = (w - 510) / 70, 1.0, 0.0
    elif w < 645:
        r, g, b = 1.0, -(w - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    f = 0.35 + 0.65 * (w - 380) / 40 if w < 420 else (0.35 + 0.65 * (780 - w) / 80 if w > 700 else 1.0)
    return (r * f, g * f, b * f)


d = 1 / 300e3
lams = np.arange(400, 701, 2)
ROWS = {1: (0.68, 1.0), 2: (0.34, 0.66), 3: (0.0, 0.32)}
DARK = "#15181f"

hscplot.setup()
fig, ax = plt.subplots(figsize=(140 * hscplot.MM, 50 * hscplot.MM))
ax.set_facecolor("white")
ax.grid(False)
for m, (y0, y1) in ROWS.items():
    ax.fill_between([-42, 42], y0, y1, color=DARK, lw=0)
    for sgn in (1, -1):
        for w in lams:
            th = np.degrees(np.arcsin(m * w * 1e-9 / d))
            ax.plot([sgn * th, sgn * th], [y0, y1], color=wl_rgb(w), lw=1.1,
                    solid_capstyle="butt")
    ax.plot([0, 0], [y0, y1], color="white", lw=2.2)
    ax.text(-43.5, (y0 + y1) / 2, f"m = {m}", ha="right", va="center", fontsize=7.5,
            color=hscplot.INK, clip_on=False)
ax.set_xlim(-42, 42)
ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xticks(range(-40, 41, 10))
ax.set_xlabel("Angle from the central line, θ (degrees)")
for side in ("left", "right", "top"):
    ax.spines[side].set_visible(False)
# overlap of orders 2 and 3 (positive side): dashed white lines through rows 2 and 3
a3 = np.degrees(np.arcsin(3 * 400e-9 / d))     # 21.1 deg, violet of order 3
b2 = np.degrees(np.arcsin(2 * 700e-9 / d))     # 24.8 deg, red of order 2
for xx in (a3, b2):
    ax.plot([xx, xx], [0.0, 0.66], color="white", lw=0.8, ls=(0, (2, 1.5)))
ax.annotate("orders 2 and 3 overlap", xy=((a3 + b2) / 2, 0.64), xytext=(30.5, 0.84),
            fontsize=7, color="white", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color="white", lw=0.6))
ax.text(0, 1.03, "m = 0 (white)", ha="center", va="bottom", fontsize=7.5,
        color=hscplot.INK, clip_on=False)
hscplot.save(fig, __file__)
