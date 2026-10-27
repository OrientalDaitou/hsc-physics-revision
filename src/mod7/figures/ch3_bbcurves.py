"""Black body curves (Planck's law) at 4500 K, 5500 K and 6500 K.
Used in ch3.tex, Section 'Black body radiation and Planck's quanta'.
Run: python3 -I ch3_bbcurves.py"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot
import numpy as np
import matplotlib.colors as mcolors

h, c, b = 6.626e-34, 3.00e8, 2.898e-3
kB = 1.380649e-23            # only used to draw the curves (not on the data sheet)


def planck(lam, T):
    return (2 * h * c**2 / lam**5) / np.expm1(h * c / (lam * kB * T))


fig, ax = hscplot.figure(width_mm=84, height_mm=60)
lam_nm = np.linspace(60, 2000, 1500)
lam = lam_nm * 1e-9
ref = planck(b / 6500, 6500)              # 6500 K peak = 1

# visible band: faint rainbow
vis = np.linspace(400, 700, 300)
cmap = mcolors.LinearSegmentedColormap.from_list(
    "vis", ["#7B3FBF", "#2F5BEA", "#21A8A0", "#3DBE3D", "#E8D21F", "#F08C1A", "#D9342B"])
ax.imshow(vis[np.newaxis, :], extent=(400, 700, 0, 1.15), aspect="auto",
          cmap=cmap, alpha=0.22, zorder=0)
ax.text(550, 1.17, "visible", ha="center", va="bottom", color=hscplot.INK, fontsize=7.5)
ax.text(200, 1.17, "UV", ha="center", va="bottom", color=hscplot.MUTED, fontsize=7.5)
ax.text(1100, 1.17, "infrared", ha="center", va="bottom", color=hscplot.MUTED, fontsize=7.5)

temps = [6500, 5500, 4500]
for i, T in enumerate(temps):
    y = planck(lam, T) / ref
    ax.plot(lam_nm, y, **hscplot.series(i), zorder=3)
    pk = b / T * 1e9
    ypk = planck(b / T, T) / ref
    ax.plot([pk, pk], [0, ypk], color=hscplot.SERIES[i], lw=0.8, ls=(0, (2, 2)), zorder=2)
    ax.plot(pk, ypk, "o", color=hscplot.SERIES[i], ms=3.2, zorder=4)
    ax.annotate(f"{T} K, peak {pk:.0f} nm", (pk, ypk), xytext=(6, 3), textcoords="offset points",
                color=hscplot.INK, fontsize=7.5, va="bottom", zorder=5,
                bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.5))

ax.set_xlim(0, 2000)
ax.set_ylim(0, 1.15)
ax.set_xticks([0, 500, 1000, 1500, 2000])
ax.set_xlabel("Wavelength $\\lambda$ (nm)")
ax.set_ylabel("Intensity (relative)")
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
hscplot.save(fig, __file__)
