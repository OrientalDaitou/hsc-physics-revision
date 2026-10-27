"""Shared helpers for the Module 7 Chapter 1 figures (wavelength -> colour)."""
import numpy as np


def wl_rgb(w, gamma=0.8):
    """Approximate sRGB colour of light of wavelength w (nm), 380-780 nm.
    Piecewise-linear approximation (after D. Bruton); good enough for drawings."""
    if w < 380 or w > 780:
        return (0.0, 0.0, 0.0)
    if w < 440:
        r, g, b = -(w - 440) / 60, 0.0, 1.0
    elif w < 490:
        r, g, b = 0.0, (w - 440) / 50, 1.0
    elif w < 510:
        r, g, b = 0.0, 1.0, -(w - 510) / 20
    elif w < 580:
        r, g, b = (w - 510) / 70, 1.0, 0.0
    elif w < 645:
        r, g, b = 1.0, -(w - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if w < 420:
        k = 0.3 + 0.7 * (w - 380) / 40
    elif w > 700:
        k = 0.3 + 0.7 * (780 - w) / 80
    else:
        k = 1.0
    return tuple((k * x) ** gamma for x in (r, g, b))


def rainbow_image(w_min, w_max, n=600, rows=2):
    """An image array (rows x n x 3) of the visible colours from w_min to w_max (nm)."""
    ws = np.linspace(w_min, w_max, n)
    row = np.array([wl_rgb(w) for w in ws])
    return np.repeat(row[None, :, :], rows, axis=0)
