"""Kepler's second law: equal areas in equal times (to scale, e = 0.6).

Run:  python3 -I src/mod5/figures/ch4_equalareas.py
Makes ch4_equalareas.pdf next to this script.
The two shaded sectors are swept in the same time (8 % of one period each).
Positions come from Kepler's equation M = E - e sin E, so the areas are exact.
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from matplotlib.patches import Polygon, Circle, FancyArrowPatch  # noqa: E402

a, e = 1.0, 0.6
b = a * np.sqrt(1 - e**2)
frac = 0.08                       # fraction of the period for each sector


def solve_E(M):
    E = M.copy() if hasattr(M, "copy") else M
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def pos(E):
    # Sun (focus) at the origin, perihelion on the +x side
    return a * (np.cos(E) - e), b * np.sin(E)


def sector(M1, M2, n=120):
    M = np.linspace(M1, M2, n)
    x, y = pos(solve_E(M))
    pts = np.column_stack([np.r_[0, x], np.r_[0, y]])
    return pts, x, y


# area check (shoelace)
def area(pts):
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


d = 2 * np.pi * frac
p1, x1, y1 = sector(-d / 2, d / 2)
p2, x2, y2 = sector(np.pi - d / 2, np.pi + d / 2)
print("areas:", area(p1), area(p2), "exact:", frac * np.pi * a * b)

fig, ax = hscplot.figure(width_mm=84, height_mm=52)
ax.set_aspect("equal")
ax.axis("off")
E = np.linspace(0, 2 * np.pi, 400)
X, Y = pos(E)
ax.plot(X, Y, color=hscplot.INK, lw=0.9)
for p in (p1, p2):
    ax.add_patch(Polygon(p, closed=True, facecolor=hscplot.SERIES[2], alpha=0.30, edgecolor=hscplot.SERIES[2], lw=0.8))
# thicker arcs showing the path travelled in each time interval
ax.plot(x1, y1, color=hscplot.VELOCITY, lw=2.2)
ax.plot(x2, y2, color=hscplot.VELOCITY, lw=2.2)
# Sun
ax.add_patch(Circle((0, 0), 0.06, facecolor=hscplot.RAY, edgecolor=hscplot.INK, lw=0.6, zorder=5))
ax.text(-0.04, -0.12, "Sun", ha="center", va="top", fontsize=8.5, color=hscplot.INK)
# labels
ax.text(0.27, 0.02, "$A_1$", fontsize=9.5, ha="center", va="center", color=hscplot.INK)
ax.text(-1.15, 0.0, "$A_2$", fontsize=9.5, ha="center", va="center", color=hscplot.INK)
ax.text(0.47, 0.40, "$\\Delta t_1$", fontsize=9, color=hscplot.VELOCITY, ha="left")
ax.text(-1.68, 0.19, "$\\Delta t_2$", fontsize=9, color=hscplot.VELOCITY, ha="right")
ax.text(0.47, -0.42, "near the Sun:\nlong arc, fast", fontsize=8, color=hscplot.INK, ha="left", va="top")
ax.text(-1.68, -0.22, "far away:\nshort arc, slow", fontsize=8, color=hscplot.INK, ha="right", va="top")
# direction of motion (anticlockwise) on the top of the orbit
Et = np.array([1.75, 1.95])
xt, yt = pos(Et)
ax.add_patch(FancyArrowPatch((xt[0], yt[0] + 0.0), (xt[1], yt[1]), arrowstyle="-|>", mutation_scale=9,
                             color=hscplot.MUTED, lw=1.0))
ax.text(xt[0] - 0.05, yt[0] + 0.07, "motion", fontsize=8, color=hscplot.MUTED, ha="center", va="bottom")
ax.set_xlim(-2.1, 1.0)
ax.set_ylim(-0.9, 0.95)
hscplot.save(fig, __file__)
