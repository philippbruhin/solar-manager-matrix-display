# -----------------------------------------------------------------------------
# Module: User Interface (UI) for Matrix Portal M4
#
# Purpose
# -------
# This module defines the class `HomeEnergyUI`, which builds the on-screen scene
# (icons + text labels) once and then updates the numbers in place. The UI shows:
#   • House consumption (top-right, white)
#   • Solar production  (middle-right, yellow)
#   • Battery SoC (%)   (bottom-left, green or red if very low)
#   • Water temperature (bottom-right, blue, followed by a small ° dot and "C")
#
# How the layout is built (DisplayIO concepts)
# --------------------------------------------
# • Display root: We create one `displayio.Group()` called `root`. This becomes
#   the display's scene via `self.display.root_group = root`.
# • Icons: Small BMPs are loaded from disk using `OnDiskBitmap` and placed as
#   `displayio.TileGrid` objects. They are appended to `root`.
# • Text: Numbers and units are `bitmap_label.Label` objects using `terminalio.FONT`.
#   These are also appended to `root`. We position text by setting `label.x` and `label.y`.
#
# Placement helpers
# -----------------
# • `right_align_label(lbl, display_width, right_margin, top_y, row_h)`:
#     - Reads the label’s `bounding_box` (a tuple `(x, y, width, height)` measured
#       in pixels within the label’s own coordinate system).
#     - Positions the label so its right edge sits at `display_width - right_margin`.
#     - Vertically centers the label inside the row spanning from `top_y` with height `row_h`.
#
# • `vcenter_label(lbl, top_y, row_h)`:
#     - Uses `lbl.bounding_box[3]` (the label’s pixel height) and `lbl.bounding_box[1]`
#       (the label’s internal top offset) to compute a y that visually centers it
#       in the given row rectangle.
#
# About `bounding_box`
# --------------------
# A label’s `bounding_box` is a 4-tuple `(x, y, w, h)`:
#   - `x`, `y`: internal offsets applied by `bitmap_label` (often 0 or small values)
#   - `w`, `h`: the label’s pixel width/height for its current text and scale
# We never draw the bounding box—it's a measurement tool. We use its `w`/`h` to
# place labels flush to the right and to center them vertically so that numbers line up.
#
# Update cycle
# ------------
# The UI is created in `__init__()` only once. The `update()` method:
#   1) receives new numbers (watts, % SoC, temperature in °C),
#   2) formats the power values (W vs kW),
#   3) updates label texts and minor positions,
#   4) swaps the battery icon + color if SoC < 6%.
# No groups are rebuilt during updates—this keeps refreshes smooth and fast.
#
# Configuration
# -------------
# All colors, file paths, margins, sizes, and fine-tuning offsets live in `config.py`.
# Tweaks to spacing or palette should be done there, not here.
# -----------------------------------------------------------------------------

import displayio
from .helpers import load_icon, right_align_label, vcenter_label, make_degree_dot, make_label
import config as C


class HomeEnergyUI:
    """Displays house consumption, solar production, battery SoC, and water temperature."""

    def __init__(self, display):
        # Keep a reference to the display object provided by Matrix().display
        self.display = display

        # Create a single root group that holds everything drawn on screen.
        # This becomes the scene shown by the display.
        root = displayio.Group()
        self.display.root_group = root

        # --- Top section: house and solar power (icons on the left, numbers right-aligned) ---
        self.icon_house = load_icon(C.ICON_HOUSE)
        self.icon_house.x = C.LEFT_MARGIN
        self.icon_house.y = C.ROW_Y[0]

        self.icon_solar = load_icon(C.ICON_SUN)
        self.icon_solar.x = C.LEFT_MARGIN
        self.icon_solar.y = C.ROW_Y[1]

        root.append(self.icon_house)
        root.append(self.icon_solar)

        # Text labels for the two top rows (numbers only; units handled by formatter)
        self.lbl_consumption = make_label(C.COL_WHITE)
        self.lbl_solar = make_label(C.COL_YELLOW)
        root.append(self.lbl_consumption)
        root.append(self.lbl_solar)

        # --- Bottom-left: battery state of charge (icon + "%") ---
        self.icon_batt = load_icon(C.ICON_BATT_FULL)
        self.icon_batt.y = C.BOTTOM_Y
        self.lbl_soc = make_label(C.COL_GREEN)
        root.append(self.icon_batt)
        root.append(self.lbl_soc)

        # --- Bottom-right: water temperature (icon + number + ° dot + "C") ---
        self.icon_temp = load_icon(C.ICON_SHOWER)
        self.icon_temp.y = C.BOTTOM_Y
        self.lbl_temp = make_label(C.COL_BLUE)            # numeric temperature
        self.deg_dot = make_degree_dot(C.COL_BLUE)        # tiny 3×3 dot right after the number
        self.lbl_unit = make_label(C.COL_BLUE)            # the letter "C"
        self.lbl_unit.text = "C"

        root.append(self.icon_temp)
        root.append(self.lbl_temp)
        root.append(self.deg_dot)
        root.append(self.lbl_unit)

    # -------------------------------------------------------------------------
    # Update method – called repeatedly to refresh displayed values
    # -------------------------------------------------------------------------
    def update(self, house_kw: float, solar_kw: float, batt_soc: int, water_temp_c: float):
        """Refresh displayed data based on new numeric values."""
        W = self.display.width

        # --- Top rows: format watt/kilowatt values for display ---
        def _fmt_w_or_kw(w):
            # Rule of thumb:
            #   - 0 or negative → show "0 W"
            #   - 1 .. 9999     → show whole watts, e.g., "452 W"
            #   - 10000+         → show kilowatts with one decimal, e.g., "10.2 kW"
            if w <= 0:
                return "0 W"          # zero is always watts
            if w < 9999:
                return f"{int(w):d} W"  # integers look cleaner for small values
            return f"{w/1000:.1f} kW"

        # Update label texts (these two numbers are right-aligned)
        self.lbl_consumption.text = _fmt_w_or_kw(house_kw)  # house_kw is watts now
        self.lbl_solar.text       = _fmt_w_or_kw(solar_kw)  # solar_kw is watts now

        # Right-align each label within its row rectangle.
        # `right_align_label` uses the label's bounding_box width to place the right edge
        # at (display width - right margin) and vertically centers it in the row.
        right_align_label(self.lbl_consumption, W, C.RIGHT_MARGIN, C.ROW_Y[0], C.TOP_ICON_H)
        right_align_label(self.lbl_solar,       W, C.RIGHT_MARGIN, C.ROW_Y[1], C.TOP_ICON_H)

        # Apply small optical nudges from config to make the right edge look perfectly aligned.
        self.lbl_consumption.x += C.KW_RIGHT_NUDGE
        self.lbl_solar.x       += C.KW_RIGHT_NUDGE

        # --- Battery SoC (bottom-left) ---
        # The battery icon sticks to the left margin; the "%"-label sits to its right.
        self.icon_batt.x = C.LEFT_MARGIN

        # Choose icon and color based on SoC. Below 6% → red text and empty icon.
        if batt_soc < 6:
            # Critical battery level
            self.icon_batt.bitmap = displayio.OnDiskBitmap(C.ICON_BATT_EMPTY)
            self.lbl_soc.color = C.COL_RED
        else:
            # Normal battery
            self.icon_batt.bitmap = displayio.OnDiskBitmap(C.ICON_BATT_FULL)
            self.lbl_soc.color = C.COL_GREEN

        # Update SoC text and position it vertically centered in the bottom row.
        self.lbl_soc.text = f"{int(batt_soc):02d}%"
        self.lbl_soc.x = self.icon_batt.x + C.SOC_ICON_W + C.GAP_ICON_TEXT
        vcenter_label(self.lbl_soc, C.BOTTOM_Y, C.BOTTOM_ICON_H)

        # --- Water temperature (bottom-right) ---
        # The temperature area is a compact block: [icon][gap][number][° dot][gap]["C"]
        # We compute the block width so we can right-align the whole block against the screen edge.
        t_num = str(int(round(water_temp_c)))
        self.lbl_temp.text = t_num

        # Measure number and "C" using their bounding boxes; these widths drive the layout math.
        bb_num = self.lbl_temp.bounding_box
        bb_unit = self.lbl_unit.bounding_box

        # Block width = icon + gap + number + degree dot + small gap + "C"
        block_w = (
            + C.TEMP_ICON_W
            + C.GAP_ICON_TEXT
            + bb_num[2]
            + C.DEG_W
            + 1
            + bb_unit[2]
        )

        # Right-align the whole temperature block by placing the left edge of the icon.
        self.icon_temp.x = W - C.RIGHT_MARGIN - block_w

        # Place the numeric label right after the icon + gap; center it vertically in the row.
        self.lbl_temp.x = self.icon_temp.x + C.TEMP_ICON_W + C.GAP_ICON_TEXT
        vcenter_label(self.lbl_temp, C.BOTTOM_Y, C.BOTTOM_ICON_H)
        self.lbl_temp.x += C.NUM_RIGHT_NUDGE  # tiny optical nudge to look centered by eye

        # Position the degree dot:
        #   - exactly after the number's pixel width (bbn[2])
        #   - nudged 1 px down so the tiny 3×3 dot looks optically centered
        bbn = self.lbl_temp.bounding_box
        baseline_top = self.lbl_temp.y + bbn[1]
        self.deg_dot.x = self.lbl_temp.x + bbn[2]  # place dot immediately after the number
        self.deg_dot.y = max(C.BOTTOM_Y, baseline_top) + 1

        # Finally, place the "C" one pixel after the degree dot and vertically center it.
        self.lbl_unit.x = self.deg_dot.x + C.DEG_W + 1
        vcenter_label(self.lbl_unit, C.BOTTOM_Y, C.BOTTOM_ICON_H)
