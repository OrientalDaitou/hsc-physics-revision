"""The ultraviolet catastrophe: classical (Rayleigh-Jeans) prediction vs the
measured black body curve (Planck's law) at 5000 K.
Run: python3 -I ch3_uvcat.py"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot
import numpy as np

h, c, b = 6.626e-34, 3.00e8, 2.898e-3
kB = 1.380649e-23            # only used to draw the curves (not on the data sheet)
T = 5000


def planck(lam):
    return (2 * h * c**2 / lam**5) / np.expm1(h * c / (lam * kB * T))


def rj(lam):
    return 2 * c * kB * T / lam**4


fig, ax = hscplot.figure(width_mm=82, height_mm=58)
lam_nm = np.linspace(40, 4000, 2000)
lam = lam_nm * 1e-9
ref = planck(b / T)
ymax = 2.6

ax.axvspan(0, 400, color=hscplot.FIELD, alpha=0.08, lw=0, zorder=0)
ax.text(200, 2.85, "UV", ha="center", va="top", color=hscplot.FIELD, fontsize=7.5)

y_rj = rj(lam) / ref
keep = y_rj <= ymax
ax.plot(lam_nm[keep], y_rj[keep], color=hscplot.SERIES[1], ls="--", lw=1.5, zorder=3)
ax.plot(lam_nm, planck(lam) / ref, color=hscplot.SERIES[0], ls="-", lw=1.6, zorder=3)

x_top = lam_nm[keep][0]
ax.annotate("", xy=(x_top - 60, ymax + 0.25), xytext=(x_top + 15, ymax - 0.05),
            arrowprops=dict(arrowstyle="-|>", color=hscplot.SERIES[1], lw=1.2))
ax.text(x_top + 200, ymax + 0.2, "classical prediction\n(Rayleigh–Jeans):\ngoes to infinity",
        color=hscplot.INK, fontsize=7.5, va="top")
ax.text(1500, 0.95, "measured curve\n(Planck's formula fits it)", color=hscplot.INK,
        fontsize=7.5, va="bottom", ha="left")
ax.annotate("", xy=(830, 0.80), xytext=(1480, 1.05),
            arrowprops=dict(arrowstyle="-|>", color=hscplot.MUTED, lw=0.8))
ax.text(2350, 0.42, "they come closer and\ncloser at long wavelengths", color=hscplot.INK,
        fontsize=7.5, ha="left", va="bottom")
ax.annotate("", xy=(3600, 0.09), xytext=(3400, 0.40),
            arrowprops=dict(arrowstyle="-|>", color=hscplot.MUTED, lw=0.8))

ax.set_xlim(0, 4000)
ax.set_ylim(0, ymax + 0.3)
ax.set_xticks([0, 1000, 2000, 3000, 4000])
ax.set_xlabel("Wavelength $\\lambda$ (nm)")
ax.set_ylabel("Intensity (relative)")
ax.text(3950, 1.55, "T = 5000 K", ha="right", va="top", color=hscplot.MUTED, fontsize=7.5)
hscplot.save(fig, __file__)
