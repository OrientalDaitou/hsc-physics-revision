"""Module 8, Chapter 4: binding energy per nucleon against mass number.

Run:  python3 -I src/mod8/figures/ch4_becurve.py   ->  ch4_becurve.pdf

Labelled points (MeV per nucleon) were calculated from AME2020 atomic masses
(section 8 of the author's calculation check):
H-2 1.112, He-4 7.074, Li-7 5.606, C-12 7.680, O-16 7.976, Fe-56 8.790,
Sr-94 (fragment) ~8.59, Xe-140 (fragment) ~8.29, U-235 7.591.
The connecting line uses standard values for stable nuclides (light nuclei
joined point to point, so the He-4 spike shows). A = 3 is He-3 (2.573, as in
Worked example 4.8). Ni-62 (8.795) is very slightly above Fe-56, so Fe-56 is
labelled 'near the peak'.
"""
import sys
import pathlib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "common"))
import hscplot                                            # noqa: E402

# backbone of the curve: (A, binding energy per nucleon in MeV)
line = [(2, 1.112), (3, 2.573), (4, 7.074), (6, 5.332), (7, 5.606), (9, 6.463),
        (11, 6.928), (12, 7.680), (14, 7.476), (16, 7.976), (19, 7.779), (20, 8.032),
        (23, 8.112), (24, 8.261), (28, 8.448), (32, 8.493), (40, 8.551), (56, 8.790),
        (62, 8.795), (64, 8.736), (88, 8.733), (90, 8.710), (120, 8.505), (138, 8.393),
        (184, 8.005), (197, 7.916), (208, 7.867), (232, 7.615), (238, 7.570)]

fig, ax = hscplot.figure(width_mm=120, height_mm=70)
ax.plot([a for a, b in line], [b for a, b in line], color=hscplot.BRAND, lw=1.3, zorder=3)

labelled = [("H-2", 2, 1.112, (5, 0), "left"), ("Li-7", 7, 5.606, (5, -2), "left"),
            ("Fe-56 (near the peak)", 56, 8.790, (0, 7), "center"), ("U-235", 235, 7.591, (-2, -9), "center")]
for name, a, b, off, ha in labelled:
    ax.plot(a, b, "o", color=hscplot.INK, ms=3.4, zorder=5)
    ax.annotate(name, (a, b), xytext=off, textcoords="offset points", ha=ha, va="center",
                fontsize=8, color=hscplot.INK)
# crowded light nuclei: labels with thin leader lines
lead = dict(arrowstyle="-", color=hscplot.MUTED, lw=0.6, shrinkA=1, shrinkB=2.5)
for name, a, b, xt, yt in [("He-4", 4, 7.074, 10, 8.75), ("C-12", 12, 7.680, 24, 6.85)]:
    ax.plot(a, b, "o", color=hscplot.INK, ms=3.4, zorder=5)
    ax.annotate(name, (a, b), xytext=(xt, yt), textcoords="data", ha="left" if xt > a else "center",
                va="center", fontsize=8, color=hscplot.INK, arrowprops=lead)

# fission fragments (neutron-rich, so a little below the stable line)
frag = [("Sr-94", 94, 8.594), ("Xe-140", 140, 8.291)]
for name, a, b in frag:
    ax.plot(a, b, "s", mfc="white", mec=hscplot.SERIES[1], ms=3.6, zorder=5)
    ax.annotate(name, (a, b), xytext=(-4, -6), textcoords="offset points", ha="right",
                va="center", fontsize=8, color=hscplot.SERIES[1])

# fusion arrow (light nuclei join -> up the left side)
ax.annotate("", xy=(4, 6.75), xytext=(2.6, 1.6),
            arrowprops=dict(arrowstyle="-|>", color=hscplot.SERIES[2], lw=1.6, mutation_scale=10))
# white box behind the long labels so grid lines do not cross the words
textbox = dict(boxstyle="square,pad=0.2", fc="white", ec="none")
ax.text(12, 3.2, "FUSION\nlight nuclei join:\nproducts more tightly bound\n"
        r"$\rightarrow$ energy released", color=hscplot.SERIES[2], ha="left", va="center",
        fontsize=8, bbox=textbox)

# fission arrows (U-235 splits into two fragments -> up the right side)
for a, b in [(140, 8.291), (94, 8.594)]:
    ax.annotate("", xy=(a + 2, b - 0.13), xytext=(232, 7.48),
                arrowprops=dict(arrowstyle="-|>", color=hscplot.SERIES[1], lw=1.3,
                                mutation_scale=9, connectionstyle="arc3,rad=0.2"))
ax.text(232, 5.2, "FISSION\nheavy nucleus splits:\nproducts more tightly bound\n"
        r"$\rightarrow$ energy released", color=hscplot.SERIES[1], ha="right", va="center",
        fontsize=8, bbox=textbox)

ax.set_xlim(0, 250)
ax.set_ylim(0, 9.6)
ax.set_xticks(range(0, 251, 50))
ax.set_yticks(range(0, 10, 1))
ax.set_xlabel("Mass number $A$ (number of nucleons)")
ax.set_ylabel("Binding energy per nucleon (MeV)")
hscplot.save(fig, __file__)
