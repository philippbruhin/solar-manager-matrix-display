# -----------------------------------------------------------------------------
# Module: Global Configuration – Theme, Layout, and Timing
#
# Purpose
# -------
# This file defines all static configuration constants used throughout the
# Matrix Portal project. It acts as the *single source of truth* for:
#   • asset paths (icons, bitmaps)
#   • display colors (RGB palette)
#   • layout geometry (margins, coordinates, spacing)
#   • fine optical corrections ("nudges")
#   • network polling intervals and timeouts (non-sensitive behavior)
#
# Design principle
# ----------------
# No hard-coded visual constants should appear inside `ui.py` or other logic.
# If you want to adjust margins, change colors, or replace icons, you do it
# here — and the entire app updates automatically.
#
# Data types
# ----------
# • Paths ........ strings (file paths to BMP icons under /app/assets/)
# • Colors ....... integers in RGB888 format (0xRRGGBB)
# • Coordinates .. integer pixel values
# • Timing ....... integers or floats (seconds)
#
# Naming conventions
# ------------------
#   ICON_*   → bitmap file paths
#   COL_*    → color constants
#   *_W/H    → width or height in pixels
#   *_Y      → y-position baseline for a row
#   *_NUDGE  → small optical corrections (±1 px)
#
# How this file is used
# ---------------------
# Import pattern:
#     import config as C
# Usage examples:
#     C.COL_BLUE        → blue color value
#     C.ICON_HOUSE      → file path for house icon
#     C.POLL_INTERVAL_S → fetch interval in seconds
#
# Layout summary for 64×32 LED matrix
# -----------------------------------
#  [Row 0] House consumption   → top row, white
#  [Row 1] Solar generation    → second row, yellow
#  [Row 2] Battery SoC (%)     → bottom-left, green/red
#           Water temperature  → bottom-right, blue
#
# Adjust margins or icon sizes here to reposition elements.
# -----------------------------------------------------------------------------

# -------------------- Asset paths --------------------
ASSETS_DIR = "/app/assets/"

ICON_HOUSE      = ASSETS_DIR + "icon-house.bmp"          # 10×10 pixels
ICON_SUN        = ASSETS_DIR + "icon-sun.bmp"            # 10×10 pixels
ICON_BATT_FULL  = ASSETS_DIR + "icon-battery-full.bmp"   # 6×10 pixels
ICON_BATT_EMPTY = ASSETS_DIR + "icon-battery-empty.bmp"  # 6×10 pixels
ICON_SHOWER     = ASSETS_DIR + "icon-shower.bmp"         # 8×10 pixels

# -------------------- Colors -------------------------
# Colors are defined in 24-bit RGB (0xRRGGBB).
COL_WHITE  = 0xFFFFFF
COL_YELLOW = 0xFFFF00
COL_GREEN  = 0x00FF00
COL_RED    = 0xFF0000
COL_BLUE   = 0x50C8FF    # “ice blue” accent color

# -------------------- Geometry / layout (pixels) -----
# All coordinates are defined relative to the 64×32 matrix.
LEFT_MARGIN   = 1
RIGHT_MARGIN  = 1

TOP_ICON_H     = 10   # Height of the two upper icon rows
BOTTOM_ICON_H  = 10   # Height of the bottom row
SOC_ICON_W     = 6    # Battery icon width in pixels
TEMP_ICON_W    = 8    # Shower/temperature icon width
ROW_Y          = [0, 11]  # Y positions for the two upper rows
BOTTOM_Y       = 22       # Y position for bottom row
GAP_ICON_TEXT  = 1        # Horizontal space between icon and text
DEG_W          = 3        # Width/height of degree dot bitmap (3×3 px)

# -------------------- Fine-tuning ("nudges") ---------
# These sub-pixel shifts help text and symbols look visually balanced.
KW_RIGHT_NUDGE  = 1   # Shift kW/W text slightly right for optical centering
DEG_RIGHT_NUDGE = 2   # Horizontal nudge for the degree symbol
NUM_RIGHT_NUDGE = 1   # Nudge for numeric temperature alignment

# -------------------- Network behavior ---------------
# These are non-sensitive runtime settings (safe to store in code).
POLL_INTERVAL_S = 60   # Seconds between HTTP fetches
HTTP_TIMEOUT_S  = 5    # Timeout per HTTP request (seconds)
