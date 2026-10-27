"""ch3_falling.pdf: emf-time graph for a small magnet dropped from rest through a horizontal coil.
Model: flux through the coil from a small magnet (dipole) on the coil's axis,
Phi(z) = Phi_max / (1 + (z/a)^2)^1.5, z = height of magnet above the coil centre.
Magnet released from rest at height h above the coil; free fall (the small braking force is ignored).
emf = -N dPhi/dt, shown in arbitrary units (only the shape matters).
Run: python3 -I src/mod6/figures/ch3_falling.py
"""
import sys, pathlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot
import numpy as np

g, a, h = 9.8, 0.025, 0.060          # m s^-2, coil radius (m), release height above coil centre (m)
t = np.linspace(0.0, 0.25, 5001)
z = h - 0.5 * g * t**2               # height above the coil centre (negative = below)
phi = 1.0 / (1.0 + (z / a)**2)**1.5
emf = -np.gradient(phi, t)
emf /= np.max(np.abs(emf[z > 0]))    # first pulse peak = -1 or +1
# choose the sign so the first pulse is positive (the sign depends on the meter connections)
if emf[np.argmax(np.abs(emf * (z > 0)))] < 0:
    emf = -emf

first = (z > 0); second = (z < 0)
A1 = np.trapezoid(emf[first], t[first]); A2 = np.trapezoid(emf[second], t[second])
i1 = np.argmax(np.abs(emf * first)); i2 = np.argmax(np.abs(emf * second))
t0 = np.sqrt(2 * h / g)
print(f"magnet reaches coil centre at t = {t0:.4f} s, speed {g*t0:.3f} m/s")
print(f"pulse 1 peak {emf[i1]:+.3f} at t={t[i1]:.4f} s; pulse 2 peak {emf[i2]:+.3f} at t={t[i2]:.4f} s; ratio {abs(emf[i2]/emf[i1]):.3f}")
print(f"areas: {A1:+.5f}, {A2:+.5f} (equal size, opposite sign)")

win = (t >= 0) & (t < t0 + 0.060)
fig, ax = hscplot.figure(width_mm=118, height_mm=58)
tm = (t - t0) * 1000                  # ms, zero when the magnet is at the coil centre
ax.axhline(0, color=hscplot.INK, lw=0.6)
ax.plot(tm[win], emf[win], lw=1.4, **hscplot.series(0))
ax.fill_between(tm[win], emf[win], 0, color=hscplot.SERIES[0], alpha=0.15, lw=0)
ax.set_xlim(-115, 60)
ax.set_ylim(-1.75, 1.35)
ax.set_yticks([])
ax.set_xlabel("Time $t$ (ms), with $t = 0$ when the magnet is at the centre of the coil")
ax.set_ylabel("Induced emf $\\varepsilon$ (V, arbitrary scale)")
ax.annotate("1: magnet approaching,\nflux increasing", xy=(tm[i1], emf[i1]), xytext=(-112, 0.62),
            fontsize=8.5, color=hscplot.INK, arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6))
ax.annotate("$\\varepsilon = 0$: magnet at\nthe centre", xy=(0, 0), xytext=(4, 0.62),
            fontsize=8.5, color=hscplot.INK, arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6))
ax.annotate("2: magnet leaving, flux decreasing.\nFaster, so taller and narrower", xy=(tm[i2], emf[i2]),
            xytext=(-112, -1.35), fontsize=8.5, color=hscplot.INK,
            arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6))
hscplot.save(fig, __file__)
