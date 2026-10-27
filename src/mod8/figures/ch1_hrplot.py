"""Chapter 1 figure: results of the key experiment 'Plotting an HR diagram from star data'.

Ten real stars (approximate catalogue values: surface temperature in K, absolute visual
magnitude M). Same values as the data table in ch1.tex.
Horizontal: temperature on a log scale, hot on the LEFT. Vertical: absolute magnitude,
bright (negative) at the TOP. Shaded ovals show the groups a student should circle.
Run:  python3 -I src/mod8/figures/ch1_hrplot.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from matplotlib.patches import Ellipse                    # noqa: E402

lg = np.log10

# name, T (K), absolute magnitude M, label offset (points), horizontal alignment
STARS = [
    ("Sun", 5772, 4.8, (6, -2), "left"),
    ("Sirius A", 9940, 1.4, (6, -3), "left"),
    ("Vega", 9600, 0.6, (6, 2), "left"),
    ("Barnard's star", 3130, 13.2, (-6, 3), "right"),
    ("Proxima Centauri", 3040, 15.5, (-6, 0), "right"),
    ("Sirius B", 25000, 11.2, (0, -11), "center"),
    ("Procyon B", 7700, 13.0, (0, -11), "center"),
    ("Aldebaran", 3900, -0.6, (-6, 0), "right"),
    ("Betelgeuse", 3600, -5.9, (-6, -1), "right"),
    ("Rigel", 12100, -7.8, (6, 0), "left"),
]

fig, ax = hscplot.figure(width_mm=116, height_mm=66)
ax.set_xlim(lg(32000), lg(2500))          # reversed: hot on the left
ax.set_ylim(17.5, -10.5)                  # reversed: bright at the top

# shaded groups (drawn first, under the points): the main sequence as a thick band,
# the other groups as ovals
ms = [(12500, -0.6), (9800, 1.0), (5772, 4.8), (4200, 8.8), (3300, 12.6), (2950, 16.3)]
ax.plot([lg(t) for t, _ in ms], [m for _, m in ms], color="#8e98a6", lw=16, alpha=0.30,
        solid_capstyle="round", zorder=1)
ax.text(lg(7600), 8.2, "main sequence", rotation=0, ha="center", va="center",
        fontsize=8, fontweight="bold", color=hscplot.INK, zorder=4)
groups = [
    # centre x (log T), centre y (M), width (log T), height (mag), colour, label, label xy
    (lg(13500), 12.2, 0.66, 4.4, "#1971c2", "white dwarfs", (lg(14500), 15.4)),   # covers Sirius B and Procyon B
    (lg(3900), -0.6, 0.13, 2.8, "#e8590c", "giant", (lg(3900), 1.9)),
    (lg(6600), -6.9, 0.85, 3.6, "#c2255c", "supergiants", (lg(6600), -9.4)),
]
for x, y, w, h, col, lab, (lx, ly) in groups:
    ax.add_patch(Ellipse((x, y), w, h, angle=0, color=col, alpha=0.18, lw=0, zorder=1))
    ax.text(lx, ly, lab, ha="center", va="center", fontsize=8, fontweight="bold",
            color=hscplot.INK, zorder=4)

for name, T, M, off, ha in STARS:
    ax.plot([lg(T)], [M], "o", ms=5.5, mfc=hscplot.SERIES[0], mec="white", mew=0.7,
            zorder=5)
    ax.annotate(name, (lg(T), M), xytext=off, textcoords="offset points", ha=ha,
                va="center", fontsize=7.5, color=hscplot.INK, zorder=6)

tt = [30000, 20000, 10000, 6000, 4000, 3000]
ax.set_xticks([lg(t) for t in tt])
ax.set_xticklabels([f"{t:,}".replace(",", " ") for t in tt])
ax.set_xlabel("Surface temperature (K)   $\\leftarrow$ hotter      cooler $\\rightarrow$")
ax.set_yticks([-10, -5, 0, 5, 10, 15])
ax.set_yticklabels(["$-$10", "$-$5", "0", "+5", "+10", "+15"])
ax.set_ylabel("Absolute magnitude $M$  (brighter $\\uparrow$)")
hscplot.save(fig, __file__)
