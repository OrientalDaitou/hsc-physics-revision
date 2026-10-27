"""Ch1 figure: paths for the same launch speed (20 m/s) at different angles, level ground, no air.
Complementary angles (15/75, 30/60) land at the same place; 45 deg goes furthest.
Run:  python3 -I src/mod5/figures/ch1_angles.py   (writes ch1_angles.pdf)"""
import sys
import pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                   # noqa: E402
import numpy as np                               # noqa: E402

g, u = 9.8, 20.0
fig, ax = hscplot.figure(width_mm=120, height_mm=56)
groups = [((45,), 0), ((30, 60), 1), ((15, 75), 2)]
for angles, i in groups:
    for th in angles:
        r = np.radians(th)
        T = 2 * u * np.sin(r) / g
        t = np.linspace(0, T, 300)
        x = u * np.cos(r) * t
        y = u * np.sin(r) * t - 0.5 * g * t**2
        st = hscplot.series(i)
        ax.plot(x, y, color=st["color"], linestyle=st["linestyle"], lw=1.8 if th == 45 else 1.4)
        k = np.argmax(y)
        ax.annotate(f"{th}°", (x[k], y[k]), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", color=hscplot.INK, fontsize=8.5)
for th in (15, 30, 45):
    R = u**2 * np.sin(np.radians(2 * th)) / g
    ax.plot([R], [0], marker="o", color=hscplot.INK, markersize=3.5, zorder=5, clip_on=False)
ax.text(27.5, 20.5, "Where they land (range):\n"
        "15° and 75°:  20.4 m\n30° and 60°:  35.3 m\n45°:  40.8 m (the furthest)",
        va="top", ha="left", color=hscplot.INK, fontsize=8.5, linespacing=1.35)
ax.set_xlim(0, 44)
ax.set_ylim(0, 21.5)
ax.set_xlabel("horizontal distance (m)", labelpad=2)
ax.set_ylabel("height (m)")
ax.set_xticks([0, 10, 20, 30, 40])
ax.tick_params(axis="x", pad=2)
ax.set_aspect("equal")
hscplot.save(fig, __file__)
