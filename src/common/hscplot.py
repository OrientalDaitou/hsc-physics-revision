"""hscplot.py - matplotlib house style for the HSC Physics revision books.

Use it from a figure script that sits in src/<mod>/figures/:

    import sys, pathlib
    HERE = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE.parents[1] / "common"))   # src/common
    import hscplot

    fig, ax = hscplot.figure(width_mm=120, height_mm=70)
    ax.plot(x, y, **hscplot.series(0))
    hscplot.save(fig, __file__)        # writes <script name>.pdf next to the script

Run it with:  python3 -I src/<mod>/figures/chN_name.py

Then include the PDF at its natural size (do not scale it, so the text stays
the same size as the book's small text):
    \\includegraphics{figures/chN_name.pdf}
"""
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib import font_manager                 # noqa: E402

# Colours (same hex values as hscphys.sty)
INK = "#1E2430"
MUTED = "#5F6B78"
RULE = "#C9D0D8"
BRAND = "#1F3A60"
SERIES = ["#2A78D6", "#EB6834", "#1BAF7A"]          # colour-blind-safe set of three
LINESTYLES = ["-", "--", ":"]
MARKERS = ["o", "s", "^"]
FORCE, VELOCITY, ACCEL, FIELD, RAY = "#D6336C", "#1971C2", "#E8590C", "#6741D9", "#F08C00"

MM = 1 / 25.4


def _find_font(filename):
    """Locate a TeX Live font file (Lato is in TeX Live)."""
    for kpse in ("kpsewhich", "/Library/TeX/texbin/kpsewhich"):
        exe = shutil.which(kpse) or (kpse if Path(kpse).exists() else None)
        if not exe:
            continue
        try:
            out = subprocess.run([exe, filename], capture_output=True, text=True,
                                 timeout=20).stdout.strip()
        except Exception:
            out = ""
        if out and Path(out).exists():
            return out
    guess = Path("/usr/local/texlive/2026/texmf-dist/fonts/truetype/typoland/lato") / filename
    return str(guess) if guess.exists() else None


def setup(font_size=9):
    """Apply the house style. Called automatically by figure()."""
    family = "DejaVu Sans"
    found = [_find_font(f"Lato-{s}.ttf") for s in ("Regular", "Italic", "Bold", "BoldItalic")]
    if all(found):
        for f in found:
            font_manager.fontManager.addfont(f)
        family = "Lato"
    plt.rcParams.update({
        "font.family": family,
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size - 0.5,
        "ytick.labelsize": font_size - 0.5,
        "legend.fontsize": font_size - 0.5,
        "mathtext.fontset": "custom",
        "mathtext.rm": family,
        "mathtext.it": f"{family}:italic",
        "mathtext.bf": f"{family}:bold",
        "mathtext.fallback": "stixsans",
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": RULE,
        "grid.linewidth": 0.4,
        "axes.axisbelow": True,
        "xtick.color": INK,
        "ytick.color": INK,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "lines.linewidth": 1.4,
        "lines.markersize": 4.5,
        "legend.frameon": False,
        "pdf.fonttype": 42,          # embed TrueType text (searchable, sharp)
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "figure.dpi": 150,
    })


def figure(width_mm=120, height_mm=70, **kw):
    """New figure with one axes, sized in millimetres (text block = 150 mm)."""
    setup()
    fig, ax = plt.subplots(figsize=(width_mm * MM, height_mm * MM), **kw)
    return fig, ax


def series(i, with_marker=False):
    """Style for data series i (0, 1, 2): colour + line style (+ marker)."""
    st = {"color": SERIES[i % 3], "linestyle": LINESTYLES[i % 3]}
    if with_marker:
        st["marker"] = MARKERS[i % 3]
    return st


def label_end(ax, x, y, text, color, dx=3, dy=0, **kw):
    """Direct label at the end of a line (offset in points)."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                va="center", ha="left", color=INK, fontsize=plt.rcParams["font.size"],
                **kw)


def save(fig, script_file):
    """Save as a PDF with the same name as the script, next to it."""
    out = Path(script_file).with_suffix(".pdf")
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out}")
    return out
