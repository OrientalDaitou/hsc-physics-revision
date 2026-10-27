"""Chapter 1 figure: black body curves for three temperatures.

Planck's law (shape only, arbitrary units). Peaks from Wien's law with the
data-sheet value b = 2.898e-3 m K.
Run:  python3 -I src/mod8/figures/ch1_blackbody.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402
from decimal import Decimal, ROUND_HALF_UP                # noqa: E402

h, c, k, b = 6.626e-34, 3.00e8, 1.381e-23, 2.898e-3


def planck(lam_nm, T):
    lam = lam_nm * 1e-9
    return 2 * h * c**2 / lam**5 / (np.exp(h * c / (lam * k * T)) - 1)


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
    return (r, g, bb)


temps = [6000, 5000, 4000]
lam = np.linspace(50, 2000, 800)
scale = planck(b / 6000 * 1e9, 6000)          # tallest peak = 100

fig, ax = hscplot.figure(width_mm=112, height_mm=56)
# visible band as a faint rainbow
vis = np.linspace(380, 750, 200)
img = np.array([[wavelength_rgb(x) for x in vis]])
ax.imshow(img, extent=(380, 750, 0, 125), aspect="auto", alpha=0.22, zorder=0)
ax.text(565, 119, "visible light", ha="center", va="center", fontsize=8, color=hscplot.INK)
for i, T in enumerate(temps):
    y = 100 * planck(lam, T) / scale
    ax.plot(lam, y, zorder=3, **hscplot.series(i))
    lp = b / T * 1e9
    yp = 100 * planck(lp, T) / scale
    ax.plot([lp], [yp], "o", color=hscplot.SERIES[i], ms=3.5, zorder=4)
    lab = Decimal(str(lp)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    if T in (5000, 4000):   # labels in clear space to the right, with leader lines
        ax.annotate(f"{T} K: peak at {lab} nm", (lp, yp),
                    xytext=(1150, 46) if T == 5000 else (1300, 24),
                    textcoords="data", fontsize=8, color=hscplot.INK, va="bottom",
                    arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6))
    else:
        ax.annotate(f"{T} K: peak at {lab} nm", (lp, yp), xytext=(14, -3),
                    textcoords="offset points", fontsize=8, color=hscplot.INK, va="bottom")
ax.set_xlim(0, 2000)
ax.set_ylim(0, 125)
ax.set_yticks([])
ax.set_xlabel("Wavelength $\\lambda$ (nm)")
ax.set_ylabel("Intensity (relative)")
hscplot.save(fig, __file__)
