"""Figure: the electromagnetic spectrum (log wavelength scale, frequency on top).

Band edges (approximate, commonly used in HSC texts):
radio > 1 m; microwave 1 mm - 1 m; infrared 700 nm - 1 mm; visible 400-700 nm;
ultraviolet 10-400 nm; X-ray 0.01-10 nm; gamma < 0.01 nm (overlaps X-rays).
Frequencies use c = 3.00e8 m/s (f = c / lambda).
Run: python3 -I src/mod7/figures/ch1_emspectrum.py
"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
sys.path.insert(0, str(HERE))
import hscplot                                   # noqa: E402
from ch1_common import rainbow_image             # noqa: E402
import numpy as np                               # noqa: E402
from matplotlib.patches import Rectangle         # noqa: E402

C = 3.00e8


def X(lam):
    """x coordinate = -log10(wavelength in m): long waves on the left."""
    return -np.log10(lam)


bands = [  # name, long edge (m), short edge (m), colour, typical source
    ("Radio", 1e3, 1.0, "#DCE8F7", "AC currents in\nantennas"),
    ("Microwaves", 1.0, 1e-3, "#D7EFE4", "antennas,\nmicrowave ovens"),
    ("Infrared", 1e-3, 700e-9, "#FBE3D3", "warm and\nhot objects"),
    ("", 700e-9, 400e-9, None, ""),
    ("UV", 400e-9, 10e-9, "#E6DDF8", "very hot\nobjects,\natoms"),
    ("X-rays", 10e-9, 1e-11, "#E4E7EB", "fast electrons\nhitting metal"),
    ("Gamma", 1e-11, 1e-14, "#F6D9E2", "atomic\nnuclei"),
]
fig, ax = hscplot.figure(width_mm=140, height_mm=56)
ax.grid(False)
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
ax.set_yticks([])
y0, h = 0.0, 1.0
for name, a, b_, col, src in bands:
    x0, x1 = X(a), X(b_)
    if col is None:      # visible: real colours, red (700 nm) on the left
        ax.imshow(rainbow_image(700, 400, n=200), extent=(x0, x1, y0, y0 + h),
                  aspect="auto", zorder=2)
        continue
    ax.add_patch(Rectangle((x0, y0), x1 - x0, h, facecolor=col, edgecolor="white", lw=1.2, zorder=1))
    ax.text((x0 + x1) / 2, y0 + h / 2, name, ha="center", va="center", fontsize=8.5,
            color=hscplot.INK, fontweight="bold", zorder=3)
    ax.text((x0 + x1) / 2, y0 - 0.10, src, ha="center", va="top", fontsize=7.2,
            color=hscplot.MUTED, linespacing=1.15)

# frequency scale on a thin line just above the bar
yf = 1.22
ax.plot([X(1e3), X(1e-14)], [yf, yf], color=hscplot.INK, lw=0.6)
for lamt in (1e3, 1.0, 1e-3, 1e-6, 1e-9, 1e-12):
    f = C / lamt
    xx = X(lamt)
    ax.plot([xx, xx], [yf, yf + 0.06], color=hscplot.INK, lw=0.6)
    ax.text(xx, yf + 0.09, f"3 × 10$^{{{int(np.floor(np.log10(f)))}}}$", ha="center",
            va="bottom", fontsize=7.0, color=hscplot.INK)
ax.text(X(1e3), yf + 0.42, "Frequency $f$ (Hz)", ha="left", va="bottom", fontsize=7.4,
        color=hscplot.INK)

# visible light blown up, above the bar (same orientation: red on the left)
vx0, vx1 = 3.6, 8.6
vy0, vh = 1.95, 0.5
ax.imshow(rainbow_image(700, 400, n=400), extent=(vx0, vx1, vy0, vy0 + vh), aspect="auto", zorder=2)
ax.add_patch(Rectangle((vx0, vy0), vx1 - vx0, vh, fill=False, edgecolor=hscplot.INK, lw=0.6, zorder=3))
ax.text(vx0 - 0.1, vy0 + vh / 2, "red\n700 nm", ha="right", va="center", fontsize=7.2,
        color=hscplot.INK, linespacing=1.1)
ax.text(vx1 + 0.1, vy0 + vh / 2, "violet\n400 nm", ha="left", va="center", fontsize=7.2,
        color=hscplot.INK, linespacing=1.1)
ax.text((vx0 + vx1) / 2, vy0 + vh + 0.06, "Visible light", ha="center", va="bottom",
        fontsize=8, color=hscplot.INK, fontweight="bold")
for xa, xb in ((X(700e-9), vx0), (X(400e-9), vx1)):
    ax.plot([xa, xb], [y0 + h, vy0], color=hscplot.MUTED, lw=0.6, zorder=0)

# arrow: increasing frequency
ax.annotate("", xy=(14.0, 2.2), xytext=(10.4, 2.2),
            arrowprops=dict(arrowstyle="->", color=hscplot.BRAND, lw=1.0))
ax.text(12.2, 2.3, "higher frequency,\nshorter wavelength,\nmore energy",
        ha="center", va="bottom", fontsize=7.2, color=hscplot.BRAND, linespacing=1.15)

# bottom axis: wavelength
ticks = np.arange(-3, 15, 3)
ax.set_xticks(ticks)
ax.set_xticklabels([f"10$^{{{-t}}}$" if t != 0 else "1" for t in ticks])
ax.spines["bottom"].set_position(("data", -0.92))
ax.tick_params(axis="x", pad=2)
ax.text(X(1e3), -1.46, "Wavelength $\\lambda$ (m)", ha="left", va="top", fontsize=7.6,
        color=hscplot.INK)
ax.text(X(1e-14), -1.46, "All of these travel at $c$ = 3.00 × 10$^{8}$ m s$^{-1}$ in a vacuum.",
        ha="right", va="top", fontsize=7.6, color=hscplot.INK)
ax.set_xlim(X(1e3), X(1e-14))
ax.set_ylim(-1.7, 3.05)
hscplot.save(fig, __file__)
