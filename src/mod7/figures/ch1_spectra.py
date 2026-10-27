"""Figure: the three kinds of spectra, drawn for hydrogen on one wavelength scale.

Hydrogen visible (Balmer) lines from 1/lambda = R(1/2^2 - 1/n^2), R = 1.097e7 m^-1:
656.3, 486.2, 434.1, 410.2 nm.
Run: python3 -I src/mod7/figures/ch1_spectra.py
"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
sys.path.insert(0, str(HERE))
import hscplot                                   # noqa: E402
from ch1_common import wl_rgb                    # noqa: E402
import numpy as np                               # noqa: E402

R = 1.097e7
H_LINES = [1e9 / (R * (1 / 4 - 1 / n**2)) for n in (3, 4, 5, 6)]
W0, W1 = 400, 700
ws = np.linspace(W0, W1, 900)


def strip(kind):
    rgb = np.array([wl_rgb(w) for w in ws])
    if kind == "continuous":
        return rgb[None, :, :]
    if kind == "emission":
        out = np.zeros_like(rgb)
        for L in H_LINES:
            m = np.abs(ws - L) < 1.5
            out[m] = rgb[m] if L > 420 else np.clip(rgb[m] * 1.6, 0, 1)
        return out[None, :, :]
    if kind == "absorption":
        out = rgb.copy()
        for L in H_LINES:
            out[np.abs(ws - L) < 1.5] = 0.0
        return out[None, :, :]


rows = [("continuous", "Continuous spectrum", "all wavelengths, no gaps"),
        ("emission", "Emission (line) spectrum of hydrogen", "bright lines on a dark background"),
        ("absorption", "Absorption spectrum of hydrogen", "dark lines at the same wavelengths")]
fig, axs = hscplot.figure(width_mm=118, height_mm=46, nrows=3, sharex=True)
for ax, (kind, title, desc) in zip(axs, rows):
    ax.imshow(strip(kind), extent=(W0, W1, 0, 1), aspect="auto")
    ax.set_yticks([])
    ax.grid(False)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_title(f"{title}: {desc}", loc="left", fontsize=8, color=hscplot.INK, pad=2.5)
    ax.tick_params(axis="x", length=2)
axs[-1].set_xticks(range(400, 701, 50))
for L in H_LINES:
    axs[1].text(L + 3, 0.5, f"{L:.0f}", ha="left", va="center", fontsize=6.8, color="white")
axs[-1].set_xlabel("Wavelength (nm)")
fig.subplots_adjust(hspace=0.95)
hscplot.save(fig, __file__)
