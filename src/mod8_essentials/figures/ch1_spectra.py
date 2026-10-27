"""Chapter 1 figure: the three kinds of spectrum (continuous, emission, absorption).

Hydrogen's four visible Balmer lines (656.3, 486.2, 434.1, 410.2 nm, from the data-sheet R as in Chapter 3) are drawn
at their true wavelengths, so the emission and absorption lines line up.
Run:  python3 -I src/mod8/figures/ch1_spectra.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402

H_LINES = [656.3, 486.2, 434.1, 410.2]                   # nm (Balmer series)
LMIN, LMAX = 390.0, 710.0


def wavelength_rgb(lam):
    """Approximate colour of light of wavelength lam (nm), as an RGB triple."""
    if lam < 380 or lam > 780:
        return (0, 0, 0)
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
    # dim the colours near the ends of human vision
    if lam < 420:
        f = 0.3 + 0.7 * (lam - 380) / 40
    elif lam > 700:
        f = 0.3 + 0.7 * (780 - lam) / 80
    else:
        f = 1.0
    return tuple((f * x) ** 0.8 for x in (r, g, bb))


def rainbow(n=700):
    lam = np.linspace(LMIN, LMAX, n)
    return np.array([[wavelength_rgb(x) for x in lam]])


fig, axes = hscplot.figure(width_mm=128, height_mm=56, nrows=3, sharex=True)
fig.subplots_adjust(hspace=1.25)
titles = [
    "Continuous spectrum: every colour (hot, dense object, e.g. a lamp filament)",
    "Emission spectrum of hydrogen: bright lines (hot, thin hydrogen gas)",
    "Absorption spectrum of hydrogen: dark lines (cooler hydrogen gas in front of a hot source)",
]
for i, ax in enumerate(axes):
    ax.grid(False)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    if i in (0, 2):
        ax.imshow(rainbow(), extent=(LMIN, LMAX, 0, 1), aspect="auto")
    else:
        ax.add_patch(__import__("matplotlib").patches.Rectangle(
            (LMIN, 0), LMAX - LMIN, 1, color="#111111"))
    if i == 1:
        for L in H_LINES:
            ax.plot([L, L], [0, 1], color=wavelength_rgb(L), lw=2.6, solid_capstyle="butt")
    if i == 2:
        for L in H_LINES:
            ax.plot([L, L], [0, 1], color="#111111", lw=2.0, solid_capstyle="butt")
    ax.set_xlim(LMIN, LMAX)
    ax.set_ylim(0, 1)
    ax.set_title(titles[i], loc="left", fontsize=8.5, color=hscplot.INK, pad=3)
    ax.tick_params(axis="x", labelbottom=(i == 2), length=2 if i < 2 else 3)
for L, ha, dx in [(410.2, "right", 2), (434.1, "left", -2), (486.2, "center", 0),
                  (656.3, "center", 0)]:
    axes[1].annotate(f"{L:.1f}", (L, 0.0), xytext=(dx, -2), textcoords="offset points",
                     ha=ha, va="top", fontsize=6.5, color=hscplot.MUTED)
axes[2].set_xlabel("Wavelength (nm)")
axes[2].set_xticks([400, 450, 500, 550, 600, 650, 700])
hscplot.save(fig, __file__)
