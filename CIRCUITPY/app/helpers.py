# -----------------------------------------------------------------------------
# Module: UI Helper Functions
#
# Purpose
# -------
# This module provides small utility functions that simplify layout code in
# `ui.py`. Each helper wraps a few lines of repetitive DisplayIO logic into a
# clean, readable function so the main UI class stays easy to follow.
#
# DisplayIO recap
# ---------------
# • DisplayIO manages all graphics on the Matrix Portal.
# • Every visual element (icon, label, etc.) is a `TileGrid` or a `Label`
#   that can be placed anywhere using pixel coordinates (x, y).
# • Groups (`displayio.Group`) hold these elements so the display can draw them.
#
# Functions in this file
# ----------------------
# load_icon(path)
#     Load a BMP file from disk and wrap it in a TileGrid ready for placement.
#
# right_align_label(label, display_width, right_margin, top_y, row_h)
#     Align a label’s right edge to the display’s right side and vertically
#     center it in the row between top_y and top_y + row_h.
#
# vcenter_label(label, top_y, row_h)
#     Vertically center a label inside a given row rectangle.
#
# make_degree_dot(color)
#     Build a 3×3 TileGrid bitmap that looks like a small ° (degree) dot,
#     using a transparent background.
#
# make_label(color)
#     Create a text label using the default `terminalio` font and a given color.
# -----------------------------------------------------------------------------

import displayio
from adafruit_display_text import bitmap_label
import terminalio
import config as C


def load_icon(path: str) -> displayio.TileGrid:
    """
    Load a BMP icon from the filesystem and return it as a TileGrid.

    The returned TileGrid can be positioned on screen using .x and .y.

    Example:
        house = load_icon("/app/assets/icon-house.bmp")
        house.x, house.y = 0, 0
        root.append(house)
    """
    odb = displayio.OnDiskBitmap(path)
    return displayio.TileGrid(odb, pixel_shader=odb.pixel_shader, x=0, y=0)


def right_align_label(lbl: bitmap_label.Label,
                      display_width: int,
                      right_margin: int,
                      top_y: int,
                      row_h: int):
    """
    Align a text label so that its right edge touches the display’s right margin
    and it appears vertically centered in a given row.

    Parameters
    ----------
    lbl : bitmap_label.Label
        The label object to position.
    display_width : int
        Total display width in pixels (e.g., 64 for a 64×32 matrix).
    right_margin : int
        Spacing to leave between the label’s right edge and the display edge.
    top_y : int
        The pixel y-coordinate of the row’s top edge.
    row_h : int
        The pixel height of the row region.

    Explanation
    -----------
    Each label has a `bounding_box` property:
        (x_offset, y_offset, width, height)
    - `width` and `height` describe how many pixels the label’s text occupies.
    - `x_offset` and `y_offset` handle small internal shifts (padding).

    We use this bounding box to:
      1. Compute the x-position so the right edge = display_width - right_margin.
      2. Compute the y-position so the label is vertically centered in the row.
    """
    bb = lbl.bounding_box  # (x_offset, y_offset, width, height)
    lbl.x = (display_width - right_margin) - bb[2]
    lbl.y = top_y + (row_h // 2) - (bb[3] // 2) - bb[1]


def vcenter_label(lbl: bitmap_label.Label, top_y: int, row_h: int):
    """
    Vertically center a label in a rectangular row of height row_h.

    We again use lbl.bounding_box to get the label’s pixel height and top offset
    so we can place it by eye in the vertical middle of the row.

    Formula:
        lbl.y = top_y + (row_h // 2) - (label_height // 2) - label_top_offset
    """
    bb = lbl.bounding_box
    lbl.y = top_y + (row_h // 2) - (bb[3] // 2) - bb[1]


def make_degree_dot(color=C.COL_RED) -> displayio.TileGrid:
    """
    Create a tiny ° (degree) dot as a 3×3 bitmap.

    The bitmap uses a 2-color palette:
        index 0 → transparent background
        index 1 → colored foreground (the dot)

    The shape is a small diamond (4 lit pixels) that looks circular on screen.

    Returns
    -------
    displayio.TileGrid
        A ready-to-draw 3×3 pixel element that can be positioned using .x and .y.
    """
    bmp = displayio.Bitmap(C.DEG_W, C.DEG_W, 2)
    pal = displayio.Palette(2)
    pal[0] = 0x000000       # transparent background
    pal[1] = color          # dot color
    pal.make_transparent(0)

    # Draw a 4-pixel diamond centered within the 3×3 grid
    bmp[1,0] = 1; bmp[2,1] = 1; bmp[1,2] = 1; bmp[0,1] = 1

    return displayio.TileGrid(bmp, pixel_shader=pal, x=0, y=0)


def make_label(color: int) -> bitmap_label.Label:
    """
    Create a simple text label using the built-in terminal font.

    Returns a bitmap_label.Label that starts with empty text and the
    specified color. The text can later be updated with .text = "new value".

    Example:
        lbl = make_label(C.COL_WHITE)
        lbl.text = "123 W"
        lbl.x, lbl.y = 10, 5
        root.append(lbl)
    """
    return bitmap_label.Label(terminalio.FONT, text="", scale=1, color=color)
