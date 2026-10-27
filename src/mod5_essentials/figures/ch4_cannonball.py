"""Newton's cannonball: horizontal launches from a very high mountain (no air).

Run:  python3 -I src/mod5/figures/ch4_cannonball.py
Makes ch4_cannonball.pdf next to this script.
Units: Earth radius = 1, GM = 1. The mountain is drawn far too high so that
the paths can be seen. Paths A and B hit the ground, C is a circle, D an ellipse.
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from matplotlib.patches import Circle, Polygon, FancyArrowPatch  # noqa: E402

R = 1.0
r0 = 1.18                          # launch radius (top of the mountain)
vc = np.sqrt(1.0 / r0)             # circular-orbit speed at r0


def path(k, tmax=40.0, dt=1e-3):
    """Integrate a launch at speed k*vc, horizontally to the right, from (0, r0)."""
    x, y = 0.0, r0
    vx, vy = k * vc, 0.0
    xs, ys = [x], [y]
    t = 0.0
    ang0 = np.arctan2(y, x)
    turned = 0.0
    prev = ang0
    while t < tmax:
        def acc(px, py):
            r3 = (px * px + py * py) ** 1.5
            return -px / r3, -py / r3
        # RK4
        ax1, ay1 = acc(x, y)
        ax2, ay2 = acc(x + 0.5 * dt * vx, y + 0.5 * dt * vy)
        ax3, ay3 = acc(x + 0.5 * dt * (vx + 0.5 * dt * ax1), y + 0.5 * dt * (vy + 0.5 * dt * ay1))
        ax4, ay4 = acc(x + dt * (vx + 0.5 * dt * ax2), y + dt * (vy + 0.5 * dt * ay2))
        nx = x + dt * (vx + dt / 6 * (ax1 + ax2 + ax3))
        ny = y + dt * (vy + dt / 6 * (ay1 + ay2 + ay3))
        vx += dt / 6 * (ax1 + 2 * ax2 + 2 * ax3 + ax4)
        vy += dt / 6 * (ay1 + 2 * ay2 + 2 * ay3 + ay4)
        x, y = nx, ny
        t += dt
        xs.append(x)
        ys.append(y)
        a = np.arctan2(y, x)
        d = (a - prev + np.pi) % (2 * np.pi) - np.pi
        turned += d
        prev = a
        if np.hypot(x, y) < R:
            break
        if abs(turned) > 2 * np.pi:
            break
    return np.array(xs), np.array(ys)


fig, ax = hscplot.figure(width_mm=78, height_mm=82)
ax.set_aspect("equal")
ax.axis("off")

# Earth and mountain
ax.add_patch(Circle((0, 0), R, facecolor="#E3ECF6", edgecolor=hscplot.INK, lw=0.8, zorder=1))
ax.text(0, -0.05, "Earth", ha="center", va="center", color=hscplot.INK, fontsize=9)
ax.add_patch(Polygon([[-0.16, np.sqrt(R**2 - 0.16**2) - 0.01], [0, r0], [0.16, np.sqrt(R**2 - 0.16**2) - 0.01]],
                     closed=True, facecolor="#C8B79A", edgecolor=hscplot.INK, lw=0.7, zorder=3))

cols = [hscplot.MUTED, hscplot.MUTED, hscplot.SERIES[0], hscplot.SERIES[1]]
styles = ["-", "-", "-", "--"]
labels = {0.5: "A", 0.76: "B", 1.0: "C", 1.08: "D"}
for (k, lab), col, ls in zip(labels.items(), cols, styles):
    xs, ys = path(k)
    ax.plot(xs, ys, color=col, ls=ls, lw=1.2 if lab in "CD" else 1.0, zorder=2)
    if lab == "A":
        # inside the Earth, just below where A lands (clear of the C and D lines)
        ax.text(xs[-1] - 0.02, ys[-1] - 0.06, "A", color=hscplot.INK, fontsize=9,
                ha="center", va="top")
    elif lab == "B":
        ax.text(xs[-1] + 0.06, ys[-1], "B", color=hscplot.INK, fontsize=9, ha="left", va="center")

# labels for C and D
ax.text(-0.93, -0.70, "C", color=hscplot.SERIES[0], fontsize=9, fontweight="bold")
xsD, ysD = path(1.08)
iD = np.argmin(ysD)
ax.text(xsD[iD] + 0.06, ysD[iD] + 0.06, "D", color=hscplot.SERIES[1], fontsize=9, fontweight="bold")

# launch velocity arrow at the mountain top
ax.add_patch(FancyArrowPatch((0.0, r0), (0.42, r0), arrowstyle="-|>", mutation_scale=9,
                             color=hscplot.VELOCITY, lw=1.3, zorder=5))
ax.text(0.21, r0 + 0.07, "launch speed", color=hscplot.VELOCITY, fontsize=8.5, va="bottom", ha="center")

# on orbit C: velocity (tangent) and gravity (to the centre) at angle 200 deg
ang = np.radians(200)
P = np.array([r0 * np.cos(ang), r0 * np.sin(ang)])
tang = np.array([np.sin(ang), -np.cos(ang)])          # clockwise motion
ax.add_patch(FancyArrowPatch(P, P + 0.55 * tang, arrowstyle="-|>", mutation_scale=9,
                             color=hscplot.VELOCITY, lw=1.3, zorder=5))
ax.text(*(P + 0.5 * tang + np.array([-0.16, 0.0])), "$v$", color=hscplot.VELOCITY, fontsize=9.5,
        zorder=7, bbox=dict(facecolor="white", edgecolor="none", pad=0.6))   # hides the D line
ax.add_patch(FancyArrowPatch(P, P * 0.62, arrowstyle="-|>", mutation_scale=9,
                             color=hscplot.FORCE, lw=1.3, zorder=5))
ax.text(*(P * 0.62 + np.array([0.02, 0.07])), "$F$", color=hscplot.FORCE, fontsize=9.5)
ax.add_patch(Circle(P, 0.035, facecolor="#D9E3EE", edgecolor=hscplot.INK, lw=0.7, zorder=6))

ax.set_xlim(-1.55, 1.55)
ax.set_ylim(-1.75, 1.45)
hscplot.save(fig, __file__)
