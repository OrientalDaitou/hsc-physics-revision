"""Single-slit diffraction patterns for a narrow and a wide slit (qualitative).

Red laser 650 nm, screen 2.00 m away, slit widths 0.040 mm and 0.080 mm.
Intensity I = (sin b / b)^2 with b = pi a sin(theta) / lambda, each curve scaled
to the same peak height. Run: python3 -I ch2_singleslit.py
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402
import numpy as np                                        # noqa: E402

lam, L = 650e-9, 2.00
y = np.linspace(-0.080, 0.080, 2001)                      # m on the screen
theta = np.arctan(y / L)


def single(a):
    b = np.pi * a * np.sin(theta) / lam
    return np.sinc(b / np.pi) ** 2                        # np.sinc(x) = sin(pi x)/(pi x)


fig, ax = hscplot.figure(width_mm=72, height_mm=46)
ax.plot(y * 1e3, single(0.040e-3), **hscplot.series(0), label="narrow slit")
ax.plot(y * 1e3, single(0.080e-3), **hscplot.series(1), label="wide slit (2 × wider)")
ax.set_xlim(-80, 80)
ax.set_ylim(0, 1.42)
ax.set_yticks([])
ax.set_xticks([-80, -40, 0, 40, 80])
ax.set_xlabel("Position on the screen (mm)")
ax.set_ylabel("Brightness")
ax.legend(loc="upper left", fontsize=7.5, handlelength=1.8, borderaxespad=0.2)
ax.annotate("central\nmaximum", xy=(10, 0.70), xytext=(33, 0.72), fontsize=7.5,
            color=hscplot.INK, arrowprops=dict(arrowstyle="->", color=hscplot.MUTED, lw=0.6))
hscplot.save(fig, __file__)
