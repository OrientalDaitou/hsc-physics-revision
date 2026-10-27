"""Alpha-particle paths near one gold nucleus (Rutherford scattering).

Paths are computed, not sketched: a repulsive inverse-square (Coulomb) force
from a fixed nucleus at the origin, integrated with RK4 from far away.
Units: distance in units of the head-on closest approach d0, speed far away = 1,
so  a = 0.5 * r_hat / r^2  (because 1/2 m v0^2 = k q1 q2 / d0).
Check printed below: each deflection angle matches tan(theta/2) = d0 / (2 b).
Run: python3 -I src/mod8/figures/ch2_alpha_paths.py
"""
import sys, pathlib, math
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot
import numpy as np
from matplotlib.patches import Circle


def path(b, x0=-400.0, dt0=0.003, rmax=400.0):
    """Path of an alpha that starts far to the left with impact parameter b."""
    s = np.array([x0, b, 1.0, 0.0])

    def f(st):
        x, y, vx, vy = st
        r3 = (x * x + y * y) ** 1.5
        return np.array([vx, vy, 0.5 * x / r3, 0.5 * y / r3])

    pts = [s[:2].copy()]
    for _ in range(2000000):
        dt = dt0 * max(1.0, math.hypot(s[0], s[1]) / 2)   # bigger steps far away
        k1 = f(s); k2 = f(s + dt / 2 * k1); k3 = f(s + dt / 2 * k2); k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(s[:2].copy())
        if math.hypot(s[0], s[1]) > rmax and s[0] * s[2] + s[1] * s[3] > 0:
            break
    pts = np.array(pts)
    theta = math.degrees(math.atan2(s[3], s[2]))
    return pts, theta


XMIN, XMAX, YMIN, YMAX = -9.0, 6.0, -4.3, 6.6
fig, ax = hscplot.figure(width_mm=104, height_mm=76)
ax.set_aspect("equal")
ax.axis("off")
ax.grid(False)

# The back-scattered path (tiny b) leaves at a small angle above the axis, so it
# stays below the incoming paths with larger b. The window is chosen so that no
# two paths cross inside the picture (they would cross further out).
# (b, label, text position, point on the path the leader line goes to;
#  (-3.5, 0.389) lies on the outgoing head-on path, checked numerically)
cases = [
    (0.03, "almost head-on: turned back", (-8.9, 1.6), (-3.5, 0.389)),
    (-0.6, "close: large deflection", (1.6, -3.3), None),
    (2.0, "medium distance:\nsmall deflection", (2.9, 2.75), None),
    (5.0, "far away: tiny deflection", (-8.9, 6.15), None),
]
for b, lab, pos, tip in cases:
    pts, theta = path(b)
    expected = 2 * math.degrees(math.atan(1 / (2 * abs(b))))
    print(f"b = {b:5.2f} d0: deflection {abs(theta):6.1f} deg (expected {expected:6.1f})")
    inside = (pts[:, 0] > XMIN - 1) & (pts[:, 0] < XMAX + 1) & \
             (pts[:, 1] > YMIN - 1) & (pts[:, 1] < YMAX + 1)
    idx = np.where(inside)[0]
    p = pts[idx[0]:idx[-1] + 1]          # one continuous piece (clipped by the axes)
    ax.plot(p[:, 0], p[:, 1], color=hscplot.ACCEL, lw=1.4, solid_capstyle="round")
    # arrowheads: one on the way in (x = -7), one on the way out
    i_in = int(np.argmin(np.abs(p[:len(p) // 2, 0] + 7.0)))
    r = np.hypot(p[:, 0], p[:, 1])
    out = np.where((np.arange(len(p)) > np.argmin(r)) & (r > 4.2))[0]
    for i in (i_in, out[0] if len(out) else len(p) - 5):
        ax.annotate("", xy=p[i + 4], xytext=p[i],
                    arrowprops=dict(arrowstyle="-|>", color=hscplot.ACCEL, lw=1.2,
                                    mutation_scale=12))
    if tip is None:
        ax.text(pos[0], pos[1], lab, fontsize=8, color=hscplot.INK, ha="left", va="top",
                linespacing=1.15)
    else:
        ax.annotate(lab, xy=tip, xytext=pos, fontsize=8, color=hscplot.INK, ha="left",
                    va="center", arrowprops=dict(arrowstyle="-", color=hscplot.MUTED,
                                                 lw=0.6, shrinkA=2, shrinkB=0))

ax.add_patch(Circle((0, 0), 0.25, color=hscplot.FORCE, zorder=5))
ax.text(0.4, -0.25, "gold nucleus (+)", fontsize=8, color=hscplot.FORCE, ha="left",
        va="top")
ax.text(-8.9, -1.4, "alpha particles (+)\ncome in from the left", fontsize=8,
        color=hscplot.MUTED, ha="left", va="top", linespacing=1.15)
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
hscplot.save(fig, __file__)
