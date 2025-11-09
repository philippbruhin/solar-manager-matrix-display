# -----------------------------------------------------------------------------
# Project: Matrix Portal M4 (64x32 HUB75) – Home Energy Overview for
# Solar Manager from Solar Manager AG in Switzerland.
#
# What this file does (entry point)
# ---------------------------------
# • Initializes the LED matrix display (HUB75 via MatrixPortal driver).
# • Connects Wi-Fi using the ESP32 co-processor (controlled over SPI).
#   - Credentials (WIFI_SSID / WIFI_PASSWORD) come from settings.toml.
# • Shows a centered, scrolling startup message:
#       "Connected to <SSID>  IP: <IP>"
#   If Wi-Fi fails, it scrolls: "Wi-Fi Error – Offline Mode".
# • Builds the UI once and then, on a fixed schedule:
#       - fetches JSON from your local API
#       - maps the values into (house W, solar W, batt %, water °C)
#       - calls ui.update(...) without rebuilding the scene
#
# Where SPI is used (short version)
# ---------------------------------
# The SAMD51 (CircuitPython) talks to the ESP32 over SPI in app/net.py:
#     spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# This SPI link is used by the ESP32 driver to join Wi-Fi and open sockets.
#
# Runtime configuration (settings.toml)
# -------------------------------------
# WIFI_SSID="..."
# WIFI_PASSWORD="..."
# SOLAR_MANAGER_LOCAL_API_BASE_URL="http://<your-local-solar-manager-ip>/v2/point"
# SOLAR_MANAGER_DEVICE_TEMP_ID="68fb58..."   # device id that reports temperature
#
# Files
# -----
# code.py           : this file (entry point / loop)
# config.py         : colors, icons, layout, nudges (visuals only)
# app/ui.py         : scene construction + update logic
# app/helpers.py    : small UI helpers (icons, alignment, degree dot, labels)
# app/net.py        : ESP32 over SPI, Wi-Fi connect, HTTP session, fetch_json
# app/assets/*.bmp  : icon bitmaps
# -----------------------------------------------------------------------------

import os, time, displayio, terminalio
from adafruit_display_text import bitmap_label
from adafruit_matrixportal.matrix import Matrix

from app.ui import HomeEnergyUI
from app import net
import config as C


# -------------------- Display init --------------------
displayio.release_displays()
display = Matrix().display
W, H = display.width, display.height


# -------------------- Startup scrolling banner --------------------
def scroll_once(text: str, color: int = C.COL_WHITE, step_px: int = 1, step_delay_s: float = 0.03):
    """
    Scroll a single line of ASCII text (A–Z, 0–9, etc.) across the display once.
    The text is vertically centered and moves from right to left.
    """
    group = displayio.Group()
    label = bitmap_label.Label(terminalio.FONT, text=text, color=color)
    group.append(label)
    display.root_group = group

    bb = label.bounding_box
    label.x = W                                # start off-screen on the right
    label.y = (H // 2) - (bb[3] // 2) - bb[1]  # vertical center

    while (label.x + bb[2]) > 0:
        label.x -= step_px
        time.sleep(step_delay_s)


# -------------------- Networking knobs --------------------
API_URL         = os.getenv("SOLAR_MANAGER_LOCAL_API_BASE_URL") or ""
DEVICE_TEMP_ID  = os.getenv("SOLAR_MANAGER_DEVICE_TEMP_ID") or ""


# -------------------- Wi-Fi connect + banner --------------------
try:
    ssid, ip = net.connect_and_get_ip()
    scroll_once(f"Connected to {ssid}  IP: {ip}  ", color=C.COL_WHITE)
except Exception:
    scroll_once("Wi-Fi Error – Offline Mode  ", color=C.COL_WHITE)


# -------------------- Build UI -------------------------
ui = HomeEnergyUI(display)


# -------------------- HTTP session (if possible) -------
try:
    _, _, http = net.connect_and_get_ip_and_http()
except Exception:
    http = None  # remain in offline mode; UI shows last values


# -------------------- JSON → UI mapping ----------------
def map_values(payload: dict):
    """
    Extract values from the API payload and return:
        (house_w, solar_w, batt_soc, water_temp_c)
    Notes:
      - Power values are in W (convert to kW only in the UI formatter).
      - Temperature is read from the device with id == DEVICE_TEMP_ID (if set).
    """
    house_w  = float(payload.get("cW", 0))   # consumption W
    solar_w  = float(payload.get("pW", 0))   # PV W (use "pvW" if your API uses that)
    batt_soc = int(payload.get("soc", 0))

    water_temp = 0.0
    if DEVICE_TEMP_ID:
        for d in payload.get("devices", []):
            if d.get("_id") == DEVICE_TEMP_ID and ("temperature" in d):
                water_temp = float(d["temperature"])
                break

    return house_w, solar_w, batt_soc, water_temp


# -------------------- Main loop ------------------------
last_values = (0.0, 0.0, 0, 0.0)  # safe initial state

while True:
    t0 = time.monotonic()
    try:
        if http and API_URL:
            data = net.fetch_json(http, API_URL, timeout=C.HTTP_TIMEOUT_S)
            last_values = map_values(data or {})
        # if offline or no URL, keep last_values
        ui.update(*last_values)
    except Exception:
        # keep previous on screen; try again next cycle
        ui.update(*last_values)

    # simple cadence control
    elapsed = time.monotonic() - t0
    sleep_s = C.POLL_INTERVAL_S - elapsed
    if sleep_s > 0:
        time.sleep(sleep_s)
