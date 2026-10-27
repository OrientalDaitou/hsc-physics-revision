"""Chapter 1 figure: redshift of hydrogen absorption lines.

Top: lines measured in the laboratory. Bottom: the same pattern from a galaxy
moving away at v = 0.035c (10 500 km/s, the galaxy of Worked example 1.3).
Every wavelength is multiplied by (1 + z) with z = 0.035.
Run:  python3 -I src/mod8/figures/ch1_redshift.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
import matplotlib.patheffects as pe                       # noqa: E402

H_LINES = [656.3, 486.2, 434.1, 410.2]
Z = 0.035
LMIN, LMAX = 390.0, 720.0


def wavelength_rgb(lam):
    if lam < 440:
        r, g, bb = -(lam - 440) / 60, 0.0, 1.0
    elif lam < 490:
        r, g, bb = 0.0, (lam - 440) / 50, 1.0
    elif lam < 510:
        r, g, bb = 0.0, 1.0, -(lam - 510) / 20
    elif lam < 580:
        r, g, bb = (lam - 510) / 70, 1.0, 0.0
    elif lam < 645:
        r, g, bb = 1.0, -(lam - 645) / 65, 0.0
    else:
        r, g, bb = 1.0, 0.0, 0.0
    if lam < 420:
        f = 0.3 + 0.7 * (lam - 380) / 40
    elif lam > 700:
        f = 0.3 + 0.7 * (780 - lam) / 80
    else:
        f = 1.0
    return tuple((f * x) ** 0.8 for x in (r, g, bb))


lam = np.linspace(LMIN, LMAX, 700)
img = np.array([[wavelength_rgb(x) for x in lam]])

fig, axes = hscplot.figure(width_mm=120, height_mm=46, nrows=2, sharex=True)
fig.subplots_adjust(hspace=1.0)
titles = ["Hydrogen absorption lines measured in a laboratory (source not moving)",
          "The same lines in light from a distant galaxy: every line has moved towards the red end"]
for i, ax in enumerate(axes):
    ax.grid(False)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.imshow(img, extent=(LMIN, LMAX, 0, 1), aspect="auto")
    for L in H_LINES:
        x = L * (1 + Z) if i == 1 else L
        ax.plot([x, x], [0, 1], color="#111111", lw=2.0, solid_capstyle="butt")
    ax.set_xlim(LMIN, LMAX)
    ax.set_ylim(0, 1)
    ax.set_title(titles[i], loc="left", fontsize=8.5, color=hscplot.INK, pad=3)
    ax.tick_params(axis="x", labelbottom=(i == 1), length=2 if i == 0 else 3)
# in the galaxy strip: faint dashed line where each line was, arrow to where it is now
for L in H_LINES:
    L2 = L * (1 + Z)
    halo = [pe.withStroke(linewidth=2.2, foreground="#444444")]
    axes[1].plot([L, L], [0, 1], color="white", lw=0.9, ls=(0, (2, 2)), path_effects=halo)
    axes[1].annotate("", xy=(L2 - 0.8, 0.5), xytext=(L, 0.5),
                     arrowprops=dict(arrowstyle="-|>", color="white", lw=0.9,
                                     mutation_scale=7, shrinkA=0, shrinkB=0,
                                     path_effects=halo))
axes[0].text(659.5, 0.5, "656.3 nm", ha="left", va="center", fontsize=7, color="white")
axes[1].text(682.5, 0.5, "679.3 nm", ha="left", va="center", fontsize=7, color="white")
axes[1].set_xlabel("Wavelength (nm)")
hscplot.save(fig, __file__)
