"""Ch1 figure: graphs against time for one projectile on level ground.
Top row: horizontal motion (s_x, v_x, a_x). Bottom row: vertical motion (s_y, v_y, a_y).
Launch: u_x = 9.0 m/s, u_y = 12.0 m/s (u = 15 m/s at 53.1 deg), g = 9.8 m/s^2, up positive.
Time of flight 2*12.0/9.8 = 2.449 s; range 9.0 * 2.449 = 22.04 m.
Run:  python3 -I src/mod5/figures/ch1_motiongraphs.py   (writes ch1_motiongraphs.pdf)"""
import sys
import pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                   # noqa: E402
import numpy as np                               # noqa: E402
import matplotlib.pyplot as plt                  # noqa: E402

g, ux, uy = 9.8, 9.0, 12.0
T = 2 * uy / g
ttop = uy / g
t = np.linspace(0, T, 300)
print(f"T = {T:.3f} s, range = {ux * T:.2f} m, t_top = {ttop:.3f} s, h_max = {uy**2 / (2 * g):.2f} m")

hscplot.setup(font_size=8)
fig, axes = plt.subplots(2, 3, figsize=(146 * hscplot.MM, 82 * hscplot.MM))
fig.subplots_adjust(wspace=0.55, hspace=0.75)
A, B = hscplot.SERIES[0], hscplot.SERIES[1]


def style(ax, ylabel, title):
    ax.set_xlabel("$t$ (s)", labelpad=1)
    ax.set_ylabel(ylabel, labelpad=0)
    ax.set_title(title, loc="left", color=hscplot.BRAND, fontweight="bold", pad=3, fontsize=8)
    ax.set_xlim(0, 2.6)
    ax.set_xticks([0, 1, 2])


# ---- top row: horizontal motion
ax = axes[0, 0]
ax.plot(t, ux * t, color=A)
style(ax, "$s_x$ (m)", "Horizontal position")
ax.set_ylim(0, 25)
ax.text(0.12, 18.0, "straight line\nthrough 0", color=hscplot.INK)

ax = axes[0, 1]
ax.plot(t, np.full_like(t, ux), color=A)
style(ax, "$v_x$ (m s$^{-1}$)", "Horizontal velocity")
ax.set_ylim(0, 14)
ax.text(0.15, 10.3, "constant", color=hscplot.INK)

ax = axes[0, 2]
ax.plot(t, np.zeros_like(t), color=B, ls="--", lw=1.6)
style(ax, "$a_x$ (m s$^{-2}$)", "Horizontal acceleration")
ax.set_ylim(-14, 4)
ax.text(0.12, -6.0, "0 always", color=hscplot.INK)

# ---- bottom row: vertical motion
ax = axes[1, 0]
ax.plot(t, uy * t - 0.5 * g * t**2, color=A)
style(ax, "$s_y$ (m)", "Height")
ax.set_ylim(0, 10)
ax.axvline(ttop, color=hscplot.MUTED, lw=0.6, ls=(0, (2, 2)))
ax.text(0.55, 1.0, "parabola", color=hscplot.INK)
ax.text(ttop + 0.06, 8.4, "top", color=hscplot.INK)

ax = axes[1, 1]
ax.plot(t, uy - g * t, color=A)
style(ax, "$v_y$ (m s$^{-1}$)", "Vertical velocity")
ax.set_ylim(-14, 14)
ax.axhline(0, color=hscplot.INK, lw=0.6)
ax.plot([ttop], [0], marker="o", color=B, markersize=3.5, zorder=5)
ax.text(1.32, 3.0, "0 at\nthe top", color=hscplot.INK)
ax.text(0.08, -12.6, "gradient\n$-9.8$", color=hscplot.INK)

ax = axes[1, 2]
ax.plot(t, np.full_like(t, -g), color=B, ls="--")
style(ax, "$a_y$ (m s$^{-2}$)", "Vertical acceleration")
ax.set_ylim(-14, 4)
ax.axhline(0, color=hscplot.INK, lw=0.6)
ax.text(0.12, -7.4, "$-9.8$ always", color=hscplot.INK)

hscplot.save(fig, __file__)
