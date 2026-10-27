"""Figure: black-body (continuous) spectra of three stars, from Planck's law.

Peaks from Wien's law with the data-sheet value b = 2.898e-3 m K:
7000 K -> 414 nm, 5500 K -> 527 nm, 3800 K -> 763 nm (762.6).
Run: python3 -I src/mod7/figures/ch1_blackbody.py
"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
sys.path.insert(0, str(HERE))
import hscplot                                   # noqa: E402
from ch1_common import rainbow_image             # noqa: E402
import numpy as np                               # noqa: E402

h, c, k, b = 6.626e-34, 3.00e8, 1.381e-23, 2.898e-3
lam_nm = np.linspace(80, 2000, 1200)
lam = lam_nm * 1e-9


def planck(T):
    return 2 * h * c**2 / lam**5 / np.expm1(h * c / (lam * k * T))


temps = [7000, 5500, 3800]
norm = planck(7000).max()
fig, ax = hscplot.figure(width_mm=106, height_mm=52)
ax.imshow(rainbow_image(400, 700, n=300), extent=(400, 700, -0.055, -0.005), aspect="auto", zorder=3)
ax.axvspan(400, 700, color="#F1F3F5", zorder=0)
ax.text(550, 0.62, "visible", ha="center", va="center", fontsize=7.5, color=hscplot.MUTED)
for i, T in enumerate(temps):
    I = planck(T) / norm
    ax.plot(lam_nm, I, **hscplot.series(i), zorder=4)
    lmax = b / T * 1e9
    Imax = I.max()
    ax.plot([lmax], [Imax], "o", color=hscplot.SERIES[i], ms=3.5, zorder=5)
    ax.plot([lmax, lmax], [0, Imax], color=hscplot.SERIES[i], lw=0.6, ls=(0, (2, 2)), zorder=4)
    label = f"{T} K\n$\\lambda_\\mathrm{{max}}$ = {lmax:.0f} nm"
    if T in (5500, 3800):   # labels in clear space on the right, with an arrow
        ax.annotate(label, (lmax, Imax), xytext=(1150, 0.55 if T == 5500 else 0.27),
                    textcoords="data", ha="left", va="bottom", fontsize=7.5,
                    color=hscplot.INK, linespacing=1.1, zorder=6,
                    arrowprops=dict(arrowstyle="->", color=hscplot.MUTED, lw=0.7))
    else:
        ax.annotate(label, (lmax, Imax), xytext=(10, 6),
                    textcoords="offset points", ha="left", va="bottom", fontsize=7.5,
                    color=hscplot.INK, linespacing=1.1, zorder=6)
ax.set_xlim(0, 2000)
ax.set_ylim(-0.06, 1.2)
ax.set_yticks([0, 0.5, 1.0])
ax.set_xlabel("Wavelength $\\lambda$ (nm)")
ax.set_ylabel("Intensity (relative)")
hscplot.save(fig, __file__)
