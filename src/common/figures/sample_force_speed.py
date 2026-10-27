"""Sample figure: centripetal force against speed for three radii (m = 2.0 kg).

Run:  python3 -I src/common/figures/sample_force_speed.py
Makes sample_force_speed.pdf next to this script.
"""
import sys
import pathlib

sys.dont_write_bytecode = True                            # keep source folders clean
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))      # src/common
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402

m = 2.0                                  # kg
v = np.linspace(0, 10, 201)              # m/s
radii = [1.0, 2.0, 4.0]                  # m

fig, ax = hscplot.figure(width_mm=118, height_mm=68)
for i, r in enumerate(radii):
    F = m * v**2 / r
    ax.plot(v, F, **hscplot.series(i))
    hscplot.label_end(ax, v[-1], F[-1], f"$r$ = {r:.0f} m", hscplot.SERIES[i])

# doubling the speed on the r = 1 m curve: 3 m/s -> 6 m/s gives 18 N -> 72 N
for vv in (3.0, 6.0):
    FF = m * vv**2 / 1.0
    ax.plot([vv], [FF], marker="o", color=hscplot.SERIES[0], markersize=4.5, zorder=5)
    ax.plot([vv, vv], [0, FF], color=hscplot.MUTED, lw=0.6, ls=(0, (2, 2)))
ax.annotate("double the speed\n(3 → 6 m s$^{-1}$):\nforce × 4 (18 → 72 N)",
            xy=(6.0, 72), xytext=(2.6, 120), color=hscplot.INK,
            arrowprops=dict(arrowstyle="->", color=hscplot.MUTED, lw=0.7))

ax.set_xlim(0, 10)
ax.set_ylim(0, 210)
ax.set_xlabel("Speed $v$ (m s$^{-1}$)")
ax.set_ylabel("Centripetal force $F_\\mathrm{c}$ (N)")
hscplot.save(fig, __file__)
