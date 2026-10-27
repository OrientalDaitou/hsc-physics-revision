"""Mod 8 ch3: continuous spectrum, hydrogen emission spectrum, hydrogen absorption spectrum.

Hydrogen Balmer wavelengths from the Rydberg equation with data-sheet R:
1/lambda = R (1/2^2 - 1/n^2), n = 3, 4, 5, 6 -> 656.3, 486.2, 434.1, 410.2 nm.
Run:  python3 -I src/mod8/figures/ch3_spectra.py   (writes ch3_spectra.pdf)
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402

R = 1.097e7
lines = [1e9 / (R * (1 / 4 - 1 / n**2)) for n in (3, 4, 5, 6)]   # nm


def wl_rgb(wl):
    """Approximate colour of a wavelength in nm (Bruton's method), 380-750 nm."""
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    # fade near the ends of the visible range
    if wl < 420:
        f = 0.3 + 0.7 * (wl - 380) / 40
    elif wl > 700:
        f = 0.3 + 0.7 * (750 - wl) / 50
    else:
        f = 1.0
    return np.array([r, g, b]) * f


wl = np.linspace(400, 700, 1201)
rainbow = np.array([wl_rgb(w) for w in wl])

fig, axes = hscplot.figure(width_mm=128, height_mm=38, nrows=3, sharex=True)
fig.subplots_adjust(hspace=0.75)
titles = ["Continuous spectrum (hot solid, e.g. a lamp filament)",
          "Hydrogen emission spectrum (hot hydrogen gas); line wavelengths in nm",
          "Hydrogen absorption spectrum (white light through cooler hydrogen gas)"]
for k, ax in enumerate(axes):
    ax.grid(False)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_yticks([])
    if k == 0:
        img = rainbow[np.newaxis, :, :]
    elif k == 1:
        img = np.zeros((1, wl.size, 3))
        for L in lines:
            sel = np.abs(wl - L) < 1.3
            img[0, sel, :] = wl_rgb(L) * 0.75 + 0.25
    else:
        img = rainbow[np.newaxis, :, :].copy()
        for L in lines:
            sel = np.abs(wl - L) < 1.3
            img[0, sel, :] = 0.0
    ax.imshow(img, aspect="auto", extent=(400, 700, 0, 1), interpolation="nearest")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 1)
    ax.set_title(titles[k], loc="left", fontsize=8, color=hscplot.INK, pad=2.5)
    if k == 1:
        for L in lines:
            ax.text(L + 2.5, 0.5, f"{L:.0f}", ha="left", va="center", fontsize=6.5,
                    color="white")
axes[-1].set_xticks(range(400, 701, 50))
axes[-1].set_xlabel("Wavelength (nm)")
hscplot.save(fig, __file__)
