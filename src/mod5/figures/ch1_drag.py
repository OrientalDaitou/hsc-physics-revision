"""Ch1 figure: the same launch (30 m/s at 45 deg) with and without air resistance.
Drag model: a_drag = -k |v| v with k = 0.005 per metre (roughly a baseball, k about 0.006 per metre;
a real tennis ball has k of about 0.02 per metre). Numbers in the caption are rounded ("about").
This is only to show the SHAPE change; HSC questions about air resistance are qualitative.
Run:  python3 -I src/mod5/figures/ch1_drag.py   (writes ch1_drag.pdf, prints the numbers)"""
import sys
import pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                   # noqa: E402
import numpy as np                               # noqa: E402

g = 9.8

def fly(u, th, k, dt=1e-3):
    x, y = 0.0, 0.0
    vx, vy = u * np.cos(np.radians(th)), u * np.sin(np.radians(th))
    xs, ys, t, tup = [x], [y], 0.0, None
    while True:
        v = np.hypot(vx, vy)
        ax_, ay_ = -k * v * vx, -g - k * v * vy
        # one RK2 (midpoint) step
        vxm, vym = vx + 0.5 * dt * ax_, vy + 0.5 * dt * ay_
        vm = np.hypot(vxm, vym)
        x += vxm * dt
        y += vym * dt
        vy_old = vy
        vx += -k * vm * vxm * dt
        vy += (-g - k * vm * vym) * dt
        t += dt
        if tup is None and vy_old > 0 >= vy:
            tup = t
        if y < 0:
            # linear interpolation back to y = 0
            f = ys[-1] / (ys[-1] - y)
            x = xs[-1] + f * (x - xs[-1])
            t = t - dt + f * dt
            xs.append(x)
            ys.append(0.0)
            break
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys), t, tup, np.degrees(np.arctan(-vy / vx)), np.hypot(vx, vy)

x0, y0, T0, tu0, a0, v0 = fly(30, 45, 0.0)
x1, y1, T1, tu1, a1, v1 = fly(30, 45, 0.005)
print(f"no air : R={x0[-1]:.1f} m H={y0.max():.2f} m t_up={tu0:.2f} t_down={T0-tu0:.2f} landing {a0:.1f} deg below, {v0:.1f} m/s")
print(f"with air: R={x1[-1]:.1f} m H={y1.max():.2f} m t_up={tu1:.2f} t_down={T1-tu1:.2f} landing {a1:.1f} deg below, {v1:.1f} m/s")
best = max(range(30, 50), key=lambda th: fly(30, th, 0.005, dt=2e-3)[0][-1])
print(f"best angle with air ~ {best} deg")

fig, ax = hscplot.figure(width_mm=118, height_mm=44)
ax.plot(x0, y0, **hscplot.series(0))
ax.plot(x1, y1, **hscplot.series(1))
ax.annotate("no air resistance\n(the model)", xy=(84.0, 7.2), xytext=(76.5, 21.5),
            color=hscplot.INK, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=hscplot.MUTED, lw=0.6))
ax.annotate("with air resistance:\nlower, shorter, steeper fall", xy=(64.0, 6.5), xytext=(36, 6.0),
            color=hscplot.INK, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=hscplot.MUTED, lw=0.6))
ax.set_xlim(0, 95)
ax.set_ylim(0, 25)
ax.set_aspect("equal")
ax.set_xlabel("horizontal distance (m)")
ax.set_ylabel("height (m)")
hscplot.save(fig, __file__)
