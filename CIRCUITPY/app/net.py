# -----------------------------------------------------------------------------
# Module: Network Helper – Wi-Fi and HTTP for Matrix Portal M4
#
# Purpose
# -------
# This module manages all network connectivity for the Matrix Portal M4 board.
# The Matrix Portal includes two processors:
#
#   • SAMD51 (main MCU) ........ runs CircuitPython and your program.
#   • ESP32 (co-processor) ..... handles Wi-Fi, controlled over SPI.
#
# The SAMD51 communicates with the ESP32 using an SPI bus plus a few control pins.
# Through this link, we can connect to a Wi-Fi network and perform HTTP requests.
#
# Overview of responsibilities
# ----------------------------
#  • Initialize and manage the single ESP32 SPI control instance.
#  • Connect to a Wi-Fi network using credentials from settings.toml.
#  • Provide convenience functions for:
#        - connecting and retrieving IP address
#        - creating an HTTP session (adafruit_requests)
#        - fetching and parsing JSON payloads
#
# API Summary
# -----------
#  get_esp() .................. returns (or creates) the global ESP32 object.
#  ensure_wifi_connected() .... ensures Wi-Fi is connected, returns (esp, ssid, ip).
#  connect_and_get_ip() ....... returns (ssid, ip) for simple status displays.
#  connect_and_get_ip_and_http() returns (ssid, ip, http_session) for API access.
#  fetch_json(http, url) ...... perform GET → decode JSON → return dict.
#
# Settings.toml
# -------------
# Required variables:
#     WIFI_SSID="YourNetwork"
#     WIFI_PASSWORD="YourPassword"
#
# Optional: used by other modules (API URL, etc.)
#
# Typical call flow
# -----------------
# In code.py:
#     ssid, ip, http = net.connect_and_get_ip_and_http()
#     data = net.fetch_json(http, "http://192.168.1.109/v2/point")
#
# Libraries involved
# ------------------
#  - busio ..................... sets up the SPI bus (SCK, MOSI, MISO)
#  - digitalio ................. handles control pins (CS, BUSY, RESET)
#  - adafruit_esp32spi ......... main driver for the ESP32
#  - adafruit_esp32spi_socketpool.SocketPool
#       provides a socket interface for HTTP clients
#  - adafruit_requests ......... lightweight HTTP client for CircuitPython
# -----------------------------------------------------------------------------

import json
import os
import time
import board, busio, digitalio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_socketpool as socketpool
import adafruit_requests as requests

# -----------------------------------------------------------------------------
# Global state
# -----------------------------------------------------------------------------
# We keep a single ESP32 controller object in memory.
# Multiple modules can import this file and call get_esp(), which will return
# the same instance rather than reinitializing the hardware.
_esp = None


# -----------------------------------------------------------------------------
# Utility: IPv4 bytearray → dotted string
# -----------------------------------------------------------------------------
def _ipv4_to_str(ip) -> str:
    """
    Convert esp.ip_address (a bytearray, e.g. b'\xC0\xA8\x01\x64')
    into a human-readable dotted string (e.g. '192.168.1.100').
    """
    if not ip:
        return "0.0.0.0"
    return ".".join(str(b) for b in ip)


# -----------------------------------------------------------------------------
# ESP32 initialization
# -----------------------------------------------------------------------------
def get_esp():
    """
    Return the global ESP32 instance, creating it if necessary.

    The ESP32 co-processor is connected to the SAMD51 via SPI.
    This function wires up:
        - busio.SPI(board.SCK, board.MOSI, board.MISO)
        - control pins:
            * CS    (chip select)
            * BUSY  (ESP32 ready flag)
            * RESET (hardware reset)
    and returns a configured adafruit_esp32spi.ESP_SPIcontrol object.
    """
    global _esp
    if _esp is None:
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        cs    = digitalio.DigitalInOut(board.ESP_CS)
        ready = digitalio.DigitalInOut(board.ESP_BUSY)
        reset = digitalio.DigitalInOut(board.ESP_RESET)
        _esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, ready, reset)
    return _esp


# -----------------------------------------------------------------------------
# Wi-Fi connection logic
# -----------------------------------------------------------------------------
def ensure_wifi_connected(timeout_s: int = 20):
    """
    Ensure that the ESP32 is connected to Wi-Fi.

    Steps:
      1. Read credentials from settings.toml (WIFI_SSID, WIFI_PASSWORD).
      2. If not already connected, attempt to connect using esp.connect_AP().
      3. Wait until connected or raise a timeout error.
      4. Return (esp_instance, ssid, ip_string).

    Parameters
    ----------
    timeout_s : int
        Maximum time to wait before aborting connection (seconds).

    Returns
    -------
    tuple : (esp, ssid, ip_string)
    """
    ssid = os.getenv("WIFI_SSID")
    pw   = os.getenv("WIFI_PASSWORD")
    if not ssid or not pw:
        raise RuntimeError("Missing WIFI_SSID or WIFI_PASSWORD in settings.toml")

    esp = get_esp()

    # Connect if not already online
    if not esp.is_connected:
        esp.connect_AP(ssid.encode("utf-8"), pw.encode("utf-8"))
        t0 = time.monotonic()
        while not esp.is_connected:
            if time.monotonic() - t0 > timeout_s:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.2)

    ip = _ipv4_to_str(esp.ip_address)
    return esp, ssid, ip


# -----------------------------------------------------------------------------
# Convenience wrappers for higher-level code
# -----------------------------------------------------------------------------
def connect_and_get_ip(timeout_s: int = 20):
    """
    Connect to Wi-Fi and return only (ssid, ip).
    Used by the startup splash to show network info.
    """
    _, ssid, ip = ensure_wifi_connected(timeout_s)
    return ssid, ip


def connect_and_get_ip_and_http(timeout_s: int = 20):
    """
    Connect to Wi-Fi and return (ssid, ip, http_session).

    After ensuring the ESP32 is connected, this function:
      • Creates a SocketPool from the ESP32 object.
      • Builds a requests.Session using that pool.
      • Returns the session so it can be used for HTTP GETs/POSTs.

    The returned `http` behaves similarly to Python's `requests` module
    but is optimized for microcontrollers.
    """
    esp, ssid, ip = ensure_wifi_connected(timeout_s)

    # Create one SocketPool per session.
    # This object provides the sockets used by adafruit_requests.
    pool = socketpool.SocketPool(esp)

    # Build a new HTTP session.  Second argument is SSL context (None = plain HTTP).
    http = requests.Session(pool, None)

    return ssid, ip, http


# -----------------------------------------------------------------------------
# JSON fetch helper
# -----------------------------------------------------------------------------
def fetch_json(http, url: str, timeout: float = 5.0) -> dict:
    """
    Perform an HTTP GET request and parse the response as JSON.

    Parameters
    ----------
    http : requests.Session
        Active HTTP session created by connect_and_get_ip_and_http().
    url : str
        Full URL to request (e.g., "http://192.168.1.109/v2/point").
    timeout : float
        Maximum number of seconds to wait for a response.

    Returns
    -------
    dict : parsed JSON object from the server.
    """
    r = http.get(url, timeout=timeout)
    try:
        # adafruit_requests may provide .content or .text depending on the backend.
        raw = getattr(r, "content", None)
        if raw is None:  # fallback for text-only response
            txt = getattr(r, "text", "")
            raw = txt.encode("utf-8", "ignore")

        data = json.loads(raw.decode("utf-8", "ignore"))
        return data
    finally:
        # Always close the request to free resources on the ESP32 side.
        try:
            r.close()
        except Exception:
            pass
