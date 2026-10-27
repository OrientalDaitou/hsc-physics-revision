"""Module 8, Chapter 4: the band of stability (N against Z), with decay arrows.

Run:  python3 -I src/mod8/figures/ch4_band.py   ->  ch4_band.pdf

The centre line of the band uses the standard estimate of the most stable Z
for each mass number A:  Z = A / (1.98 + 0.0155 A^(2/3)).
The dots are real stable nuclides (Z, N): C-12, Ca-40, Fe-56, Sn-120, Pb-208. U-238 (unstable, Z = 92) is shown beyond the end of the band.
Arrow directions: beta-minus (Z+1, N-1), beta-plus (Z-1, N+1), alpha (Z-2, N-2).
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

import numpy as np                                        # noqa: E402

A = np.arange(1, 241, 0.5)
Zs = A / (1.98 + 0.0155 * A ** (2 / 3))
Ns = A - Zs
half_width = 1.5 + 0.045 * Zs          # drawn width of the band (schematic)

fig, ax = hscplot.figure(width_mm=114, height_mm=70)
ax.grid(False)

stable = Zs <= 82.5
ax.fill_between(Zs[stable], Ns[stable] - half_width[stable], Ns[stable] + half_width[stable],
                color=hscplot.SERIES[0], alpha=0.30, lw=0, zorder=2)
ax.plot(Zs[stable], Ns[stable], color=hscplot.SERIES[0], lw=1.2, zorder=3)
beyond = (Zs >= 82) & (Zs <= 95)
ax.plot(Zs[beyond], Ns[beyond], color=hscplot.SERIES[0], lw=1.0, ls=(0, (3, 2)), zorder=3)

# N = Z line
z = np.linspace(0, 100, 2)
ax.plot(z, z, color=hscplot.MUTED, lw=0.8, ls=(0, (4, 3)))
ax.text(88, 80, "$N = Z$", color=hscplot.MUTED, ha="left", va="center")

# Z = 82 line
ax.plot([82, 82], [0, 158], color=hscplot.MUTED, lw=0.7, ls=":")
ax.text(83.5, 8, "$Z = 82$\n(lead)", color=hscplot.MUTED, ha="left", va="bottom", fontsize=8)

# real stable nuclides
pts = [("C-12", 6, 6), ("Ca-40", 20, 20),
       ("Fe-56", 26, 30), ("Sn-120", 50, 70), ("Pb-208", 82, 126)]
for name, zz, nn in pts:
    ax.plot(zz, nn, "o", color=hscplot.INK, ms=3.2, zorder=5)
offsets = {"Ca-40": (5, -4),
           "Fe-56": (5, -4), "Sn-120": (5, -4), "Pb-208": (-6, 4)}
for name, zz, nn in pts:
    if name not in offsets:
        continue
    dx, dy = offsets[name]
    ha = "right" if dx < 0 else "left"
    ax.annotate(name, (zz, nn), xytext=(dx, dy), textcoords="offset points",
                ha=ha, va="center", fontsize=7.5, color=hscplot.INK)
# C-12 sits close to the x-axis: label above it, with a thin leader line
ax.annotate("C-12", (6, 6), xytext=(4, 24), textcoords="data", ha="center",
            va="bottom", fontsize=7.5, color=hscplot.INK,
            arrowprops=dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6,
                            shrinkA=1, shrinkB=2.5))

# U-238 beyond the band
ax.plot(92, 146, "o", mfc="white", mec=hscplot.INK, ms=3.6, zorder=5)
ax.annotate("U-238", (92, 146), xytext=(4, 3), textcoords="offset points",
            ha="left", va="bottom", fontsize=7.5)

arrow = dict(arrowstyle="-|>", lw=1.3, mutation_scale=9)
# beta-minus: too many neutrons, above the band, moves Z+1, N-1
ax.annotate("", xy=(37, 49), xytext=(30, 56), arrowprops=dict(color=hscplot.FORCE, **arrow))
ax.text(3, 60, "too many neutrons\n" r"$\rightarrow\ \beta^{-}$ decay ($Z+1$, $N-1$)",
        color=hscplot.FORCE, ha="left", va="bottom", fontsize=8)
# beta-plus: too few neutrons, below the band, moves Z-1, N+1
ax.annotate("", xy=(44, 55), xytext=(51, 48), arrowprops=dict(color=hscplot.VELOCITY, **arrow))
ax.text(52, 46, "too few neutrons\n" r"$\rightarrow\ \beta^{+}$ decay ($Z-1$, $N+1$)",
        color=hscplot.VELOCITY, ha="left", va="top", fontsize=8)
# alpha: Z > 82, moves Z-2, N-2
ax.annotate("", xy=(84, 138), xytext=(92, 146), arrowprops=dict(color=hscplot.FIELD, **arrow))
ax.text(79, 150, r"$Z > 82$: $\alpha$ decay ($Z-2$, $N-2$)", color=hscplot.FIELD,
        ha="right", va="center", fontsize=8)

ax.set_xlim(0, 100)
ax.set_ylim(0, 160)
# label along the band: angle measured in display coordinates
i0, i1 = np.searchsorted(Zs, 58), np.searchsorted(Zs, 66)
(x0, y0), (x1, y1) = ax.transData.transform([(Zs[i0], Ns[i0]), (Zs[i1], Ns[i1])])
angle = np.degrees(np.arctan2(y1 - y0, x1 - x0))
ax.text(60, 89, "band of stability", rotation=angle, rotation_mode="anchor",
        color=hscplot.BRAND, ha="center", va="bottom", fontsize=8.5)
ax.set_xticks(range(0, 101, 20))
ax.set_yticks(range(0, 161, 20))
ax.set_xlabel("Atomic number $Z$ (number of protons)")
ax.set_ylabel("Neutron number $N$")
hscplot.save(fig, __file__)
