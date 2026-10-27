"""Mod 8 ch3: Bohr's ground-state orbit compared with Schrodinger's 1s and 2p orbitals.

Dots are random samples of where ONE electron could be found (3-D positions projected on
a plane). 1s: radial probability P(r) ~ r^2 exp(-2r/a0) (gamma, shape 3, scale a0/2),
most likely distance = a0 (the Bohr radius). 2p (m = 0): P(r) ~ r^4 exp(-r/a0)
(gamma, shape 5, scale a0), angular density ~ cos^2(theta).
Run:  python3 -I src/mod8/figures/ch3_clouds.py   (writes ch3_clouds.pdf)
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402

rng = np.random.default_rng(3)
N = 5000

# 1s
r1 = rng.gamma(3.0, 0.5, N)                 # in units of a0
u1 = rng.uniform(-1, 1, N)                  # cos(theta), uniform for a sphere
ph1 = rng.uniform(0, 2 * np.pi, N)
x1 = r1 * np.sqrt(1 - u1**2) * np.cos(ph1)
z1 = r1 * u1

# 2p (m = 0): cos(theta) density ~ u^2 on [-1, 1]
r2 = rng.gamma(5.0, 1.0, N)
u2 = np.sign(rng.uniform(-1, 1, N)) * rng.uniform(0, 1, N) ** (1 / 3)
ph2 = rng.uniform(0, 2 * np.pi, N)
x2 = r2 * np.sqrt(1 - u2**2) * np.cos(ph2)
z2 = r2 * u2

fig, axes = hscplot.figure(width_mm=132, height_mm=50, ncols=3)
fig.subplots_adjust(wspace=0.08)
lim = [2.6, 2.6, 11.0]
for ax, L in zip(axes, lim):
    ax.set_aspect("equal")
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.axis("off")

# (a) Bohr
ax = axes[0]
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=hscplot.BRAND, lw=1.2)
ax.plot([0], [0], "o", color=hscplot.FORCE, ms=5)
ax.plot([np.cos(0.7)], [np.sin(0.7)], "o", color=hscplot.VELOCITY, ms=4.5)
ta = np.linspace(0.75, 1.55, 40)
ax.plot(1.3 * np.cos(ta), 1.3 * np.sin(ta), color=hscplot.VELOCITY, lw=1.0)
ax.annotate("", xy=(1.3 * np.cos(1.62), 1.3 * np.sin(1.62)),
            xytext=(1.3 * np.cos(1.5), 1.3 * np.sin(1.5)),
            arrowprops=dict(arrowstyle="-|>", color=hscplot.VELOCITY, lw=1.0, mutation_scale=8))
ax.text(0, -1.55, "electron on a fixed circle\n(radius = Bohr radius)", ha="center", va="top",
        fontsize=7.5, color=hscplot.INK)
ax.set_title("(a) Bohr:\nground state", fontsize=8.5, color=hscplot.INK)

# (b) 1s
ax = axes[1]
ax.scatter(x1, z1, s=0.6, color=hscplot.SERIES[0], alpha=0.45, linewidths=0)
ax.plot(np.cos(t), np.sin(t), color=hscplot.INK, lw=0.8, ls=(0, (3, 2)))
ax.plot([0], [0], "o", color=hscplot.FORCE, ms=3.5)
ax.text(0, -2.45, "dashed circle: most likely\ndistance (Bohr radius)", ha="center", va="top",
        fontsize=7.5, color=hscplot.INK)
ax.set_title("(b) Schrödinger:\n1s orbital", fontsize=8.5, color=hscplot.INK)

# (c) 2p
ax = axes[2]
ax.scatter(x2, z2, s=0.6, color=hscplot.SERIES[1], alpha=0.45, linewidths=0)
ax.plot([0], [0], "o", color=hscplot.FORCE, ms=3.5)
ax.text(0, -10.4, "a 2p orbital: two lobes,\nzero chance in the middle plane", ha="center",
        va="top", fontsize=7.5, color=hscplot.INK)
ax.set_title("(c) Schrödinger:\n2p orbital", fontsize=8.5, color=hscplot.INK)
hscplot.save(fig, __file__)
