"""Chapter 1 figure: a simplified Hertzsprung-Russell diagram.

Horizontal: surface temperature on a log scale, hot on the LEFT.
Left axis: luminosity in solar units (log scale). Right axis: absolute magnitude,
from M = 4.83 - 2.5 log10(L / Lsun), so L = 1 Lsun sits at M = +4.8.
Dashed lines: stars of equal radius, L/Lsun = (R/Rsun)^2 (T/5772 K)^4.
Main-sequence points: approximate values for dwarfs O5V ... M6V.
Sun-like path (badge 1 sits beside the Sun marker): 1 main sequence -> 2 red giant -> (planetary nebula) -> 3 white dwarf.
Run:  python3 -I src/mod8/figures/ch1_hr.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from matplotlib.patches import FancyArrowPatch            # noqa: E402

TSUN = 5772.0
lg = np.log10

fig, ax = hscplot.figure(width_mm=128, height_mm=90)
ax.grid(False)
XMIN, XMAX = lg(40000), lg(2400)          # reversed: hot on the left
YMIN, YMAX = -4.3, 6.3
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)

# light background colour for each spectral class (approximate star colours)
classes = [("O", 40000, 30000, "#9bb0ff"), ("B", 30000, 10000, "#aabfff"),
           ("A", 10000, 7500, "#cad7ff"), ("F", 7500, 6000, "#f8f7ff"),
           ("G", 6000, 5000, "#fff4ea"), ("K", 5000, 3500, "#ffd2a1"),
           ("M", 3500, 2400, "#ffb56c")]
for name, t1, t2, col in classes:
    ax.axvspan(lg(t1), lg(t2), color=col, alpha=0.45, lw=0, zorder=0)
    ax.text((lg(t1) + lg(t2)) / 2, YMAX + 0.12, name, ha="center", va="bottom",
            fontsize=9, fontweight="bold", color=hscplot.INK)
ax.text(lg(40000), YMAX + 0.12, "Class:", ha="right", va="bottom", fontsize=8,
        color=hscplot.MUTED)

# lines of equal radius
T = np.logspace(lg(2400), lg(40000), 100)
for R, lab, tl in [(0.01, "0.01 R$_\\odot$", 33000), (1, "1 R$_\\odot$", 3300),
                   (100, "100 R$_\\odot$", 2700), (1000, "1000 R$_\\odot$", 4700)]:
    y = 2 * lg(R) + 4 * lg(T / TSUN)
    ax.plot(lg(T), y, color="#7b6fb0", lw=0.7, ls=(0, (4, 3)), zorder=1)
    yl = 2 * lg(R) + 4 * lg(tl / TSUN)
    ax.text(lg(tl), yl + 0.18, lab, fontsize=7, color="#5a4f93", ha="center",
            va="bottom", rotation=0, zorder=2)

# main sequence band (approximate dwarf values: T in K, log L)
ms = [(41000, 5.3), (31500, 4.6), (22000, 3.6), (15700, 2.7), (11400, 1.9),
      (9700, 1.55), (8200, 1.12), (7200, 0.72), (6500, 0.48), (5800, 0.0),
      (5300, -0.33), (4500, -0.75), (3900, -1.1), (3500, -1.7), (3100, -2.4),
      (2800, -3.0)]
mx = [lg(t) for t, _ in ms]
my = [l for _, l in ms]
ax.plot(mx, my, color="#8e98a6", lw=13, alpha=0.55, solid_capstyle="round", zorder=2)
ax.text(lg(12000), 2.45, "Main sequence", rotation=-37, fontsize=8.5,
        fontweight="bold", color=hscplot.INK, ha="center", va="center", zorder=6)

# giants, supergiants, white dwarfs: drawn as wide translucent bands
def band(points, col, lw):
    ax.plot([lg(t) for t, _ in points], [l for _, l in points], color=col, lw=lw,
            alpha=0.30, solid_capstyle="round", zorder=3)


band([(5100, 1.0), (4500, 2.0), (3700, 3.1)], "#e8590c", 16)              # red giants
band([(28000, 5.0), (3400, 5.0)], "#c2255c", 15)                          # supergiants (red end covers 3300 K, star P of WE1.7)
band([(28000, 2 * lg(0.012) + 4 * lg(28000 / TSUN)),
      (6500, 2 * lg(0.012) + 4 * lg(6500 / TSUN))], "#1971c2", 11)         # white dwarfs
for lab, t, l in [("Red giants", 4050, 1.55), ("Supergiants", 9000, 5.0),
                  ("White dwarfs", 9800, -3.65)]:
    ax.text(lg(t), l, lab, ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=hscplot.INK, zorder=6)

# the Sun
ax.plot([lg(TSUN)], [0], "o", ms=7, mfc="#ffd43b", mec=hscplot.INK, mew=0.8, zorder=7)
ax.plot([lg(TSUN)], [0], "o", ms=1.5, color=hscplot.INK, zorder=8)
ax.text(lg(TSUN) - 0.035, -0.55, "Sun (G2V)", fontsize=8, color=hscplot.INK, zorder=8,
        ha="left")

# path of a Sun-like star: 1 -> 2 (red giant) -> planetary nebula -> 3 (white dwarf)
path_col = hscplot.BRAND
a1 = FancyArrowPatch((lg(5600), 0.3), (lg(4000), 2.9), connectionstyle="arc3,rad=-0.25",
                     arrowstyle="-|>", mutation_scale=9, color=path_col, lw=1.2, zorder=7)
a2 = FancyArrowPatch((lg(3900), 3.5), (lg(33000), 3.5), connectionstyle="arc3,rad=0.0",
                     arrowstyle="-|>", mutation_scale=9, color=path_col, lw=1.1,
                     ls=(0, (3, 2)), zorder=7)
a3 = FancyArrowPatch((lg(33000), 3.5), (lg(17000), -2.0), connectionstyle="arc3,rad=0.2",
                     arrowstyle="-|>", mutation_scale=9, color=path_col, lw=1.1,
                     ls=(0, (3, 2)), zorder=7)
for a in (a1, a2, a3):
    ax.add_patch(a)


def badge(x, y, s):
    ax.text(x, y, s, ha="center", va="center", fontsize=7.5, fontweight="bold",
            color="white", zorder=9,
            bbox=dict(boxstyle="circle,pad=0.18", fc=path_col, ec="none"))


badge(lg(TSUN) + 0.052, 0.0, "1")             # right next to the Sun marker
badge(lg(3500), 2.9, "2")
badge(lg(13500), -1.85, "3")
ax.text(lg(11500), 3.62, "outer layers drift off (planetary nebula)", fontsize=7,
        color=path_col, ha="center", va="bottom", zorder=8)

# axes and ticks
tt = [40000, 20000, 10000, 6000, 4000, 3000]
ax.set_xticks([lg(t) for t in tt])
ax.set_xticklabels([f"{t:,}".replace(",", " ") for t in tt])
ax.set_xlabel("Surface temperature (K)   $\\leftarrow$ hotter      cooler $\\rightarrow$")
yt = list(range(-4, 7, 2))
ax.set_yticks(yt)
ax.set_yticklabels(["$10^{%d}$" % k if k not in (0,) else "1" for k in yt])
ax.set_ylabel("Luminosity $L/L_\\odot$  (Sun = 1)")
sec = ax.secondary_yaxis("right", functions=(lambda y: 4.83 - 2.5 * y,
                                             lambda M: (4.83 - M) / 2.5))
sec.set_yticks([-10, -5, 0, 5, 10, 15])
sec.set_yticklabels(["$-$10", "$-$5", "0", "+5", "+10", "+15"])
sec.set_ylabel("Absolute magnitude $M$  (smaller = brighter)")
ax.spines["right"].set_visible(True)
ax.spines["top"].set_visible(True)
for s in ("top", "right"):
    ax.spines[s].set_color(hscplot.INK)
    ax.spines[s].set_linewidth(0.6)
hscplot.save(fig, __file__)
