"""Forces and speed on an elliptical orbit (to scale, e = 0.5).

Run:  python3 -I src/mod5/figures/ch4_ellipseforces.py
Makes ch4_ellipseforces.pdf next to this script.
Blue arrows: velocity (length proportional to the real speed, from
v^2 = GM(2/r - 1/a)). Red arrows: direction of gravity (towards the Sun; drawn
the same length at every point). Dashed red: the part of gravity along the
velocity (speeds the planet up) or against it (slows it down).
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch   # noqa: E402

a, e = 1.0, 0.5
b = a * np.sqrt(1 - e**2)


def pos(E):
    return np.array([a * (np.cos(E) - e), b * np.sin(E)])


def vel_dir(E):
    d = np.array([-a * np.sin(E), b * np.cos(E)])     # anticlockwise motion
    return d / np.linalg.norm(d)


def speed(E):
    r = np.linalg.norm(pos(E))
    return np.sqrt(2 / r - 1 / a)


def arrow(ax, p, q, color, ls="-", lw=1.3):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9, color=color,
                                 lw=lw, linestyle=ls, zorder=5, shrinkA=0, shrinkB=0))


fig, ax = hscplot.figure(width_mm=106, height_mm=84)
ax.set_aspect("equal")
ax.axis("off")
EE = np.linspace(0, 2 * np.pi, 400)
X, Y = pos(EE)
ax.plot(X, Y, color=hscplot.INK, lw=0.9)
ax.add_patch(Circle((0, 0), 0.055, facecolor=hscplot.RAY, edgecolor=hscplot.INK, lw=0.6, zorder=6))
ax.text(0.0, -0.10, "Sun", ha="center", va="top", fontsize=8.5)

vscale = 0.30                     # arrow length per unit speed
Flen = 0.42
points = {
    "P": 0.0,                     # perihelion
    "Q": np.pi / 2,                     # moving away from the Sun (upper half)
    "A": np.pi,                   # aphelion
    "S": -np.pi / 2,                    # moving towards the Sun (lower half)
}
for name, E in points.items():
    p = pos(E)
    vd = vel_dir(E)
    v = speed(E)
    arrow(ax, p, p + vscale * v * vd, hscplot.VELOCITY)
    fd = -p / np.linalg.norm(p)
    arrow(ax, p, p + Flen * fd, hscplot.FORCE)
    if name in ("Q", "S"):
        comp = np.dot(fd, vd) * Flen
        out = p / np.linalg.norm(p)            # small sideways shift so arrows do not overlap
        n = np.array([-vd[1], vd[0]])
        n = n if np.dot(n, out) > 0 else -n
        q0 = p + 0.07 * n
        arrow(ax, q0, q0 + comp * vd, hscplot.FORCE, ls="--", lw=1.1)
    ax.add_patch(Circle(p, 0.035, facecolor="#D9E3EE", edgecolor=hscplot.INK, lw=0.7, zorder=7))
    print(name, "r =", np.linalg.norm(p), "speed =", v, "angle F-v (deg) =",
          np.degrees(np.arccos(np.dot(fd, vd))))

# labels
pP, pQ, pA, pS = (pos(points[k]) for k in "PQAS")
ax.text(pP[0] + 0.05, pP[1] - 0.05, "perihelion\nfastest\n$F \\perp v$", fontsize=8.5, ha="left", va="top")
# Essentials layout fix: label centred on the point and a little further left, so the
# downward velocity arrow at aphelion does not touch the word "aphelion"
ax.text(pA[0] - 0.07, pA[1], "aphelion\nslowest\n$F \\perp v$", fontsize=8.5, ha="right", va="center")
ax.text(pQ[0] + 0.0, pQ[1] + 0.13, "moving away:\npart of $F$ against $v$,\nso it slows down", fontsize=8.5,
        ha="center", va="bottom")
ax.text(pS[0] + 0.0, pS[1] - 0.13, "moving closer:\npart of $F$ along $v$,\nso it speeds up", fontsize=8.5,
        ha="center", va="top")
ax.text(pP[0] + 0.08, pP[1] + vscale * speed(0.0) - 0.02, "$v$", color=hscplot.VELOCITY, fontsize=9.5)
ax.text(pP[0] - 0.22, pP[1] + 0.05, "$F$", color=hscplot.FORCE, fontsize=9.5)
ax.set_xlim(-1.95, 1.05)
ax.set_ylim(-1.45, 1.45)
hscplot.save(fig, __file__)
