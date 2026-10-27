"""Double-slit interference pattern: fringe strip and brightness graph.

Brightness I = cos^2(pi y / dy) * envelope, with the single-slit envelope of a
slit whose width is 1/5 of the slit separation (first envelope zero at 5 dy).
x-axis in units of the fringe spacing dy. Run: python3 -I ch2_doubleslit.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402
import numpy as np                                        # noqa: E402
import matplotlib.pyplot as plt                           # noqa: E402
from matplotlib.colors import LinearSegmentedColormap     # noqa: E402

x = np.linspace(-4.4, 4.4, 3001)                          # y / dy
env = np.sinc(x / 5.0) ** 2                               # a = d/5
I = np.cos(np.pi * x) ** 2 * env

hscplot.setup()
fig, (axs, ax) = plt.subplots(2, 1, figsize=(128 * hscplot.MM, 56 * hscplot.MM),
                              gridspec_kw={"height_ratios": [1, 3.3], "hspace": 0.08},
                              sharex=True)
cmap = LinearSegmentedColormap.from_list("red", ["#000000", "#e8262b", "#ffd0c8"])
axs.imshow(np.tile(I, (10, 1)), extent=[x[0], x[-1], 0, 1], aspect="auto", cmap=cmap,
           vmin=0, vmax=1.0)
axs.set_yticks([])
axs.grid(False)
for s in ("left", "bottom"):
    axs.spines[s].set_visible(False)
axs.tick_params(bottom=False)
axs.set_title("What you see on the screen", fontsize=8, color=hscplot.INK, pad=3)

ax.plot(x, I, color=hscplot.SERIES[0], lw=1.4)
ax.plot(x, env, color=hscplot.MUTED, lw=0.8, ls=(0, (3, 2)))
ax.set_ylim(0, 1.32)
ax.set_xlim(x[0], x[-1])
ax.set_yticks([])
ax.set_ylabel("Brightness")
ticks = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
ax.set_xticks(ticks)
ax.set_xticklabels([("0" if t == 0 else (f"{t}Δy" if abs(t) != 1 else ("Δy" if t > 0 else "−Δy"))).replace("-", "−") for t in ticks])
ax.set_xlabel("Distance from the centre of the pattern, y")
# labels on maxima and minima
for m in (0, 1, 2, 3):
    for sgn in ((1,) if m == 0 else (1, -1)):
        xm = sgn * m
        ym = float(np.interp(xm, x, I))
        ax.text(xm, ym + 0.10, f"m = {m}", ha="center", va="bottom", fontsize=7.5,
                color=hscplot.SERIES[0],
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
for k, xm, yt in ((1, 0.5, 0.42), (2, 1.5, 0.42)):
    name = {1: "1st", 2: "2nd"}[k]
    ax.annotate(f"{name}\ndark", xy=(xm, 0.01), xytext=(xm, yt), ha="center",
                va="bottom", fontsize=6.8, color=hscplot.INK,
                arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.5))
# fringe spacing arrow between m = -1 and m = -2
ax.annotate("", xy=(-2, 1.18), xytext=(-1, 1.18),
            arrowprops=dict(arrowstyle="<->", color=hscplot.INK, lw=0.7))
ax.text(-1.5, 1.21, "Δy", ha="center", va="bottom", fontsize=8, color=hscplot.INK)
ax.text(-3.55, 0.50, "envelope\n(single-slit\ndiffraction)", ha="center", va="bottom",
        fontsize=6.8, color=hscplot.MUTED)
hscplot.save(fig, __file__)
