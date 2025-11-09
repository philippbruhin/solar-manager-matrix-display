# 🌞 Matrix Display for Solar Manager (Adafruit Matrix Portal M4)

<img src="docs/display_front.jpg" width="500" alt="Matrix Portal display showing live energy data">

## 💡 Project idea

After installing solar panels at home, I wanted to **see my energy flow in real time** —  
how much power is produced, how much is used, and where it goes (e.g., EV, heat pump, boiler).

This small display gives a quick visual overview of:
- 🏠 **House consumption**
- ☀️ **Solar generation**
- 🔋 **Battery state of charge**
- 🚿 **Hot water temperature**

It helps build intuition for how much energy different devices use,  
and shows how simple changes (like lowering the floor heating by 1°C) affect power draw.

This project connects to a **Solar Manager** gateway via its **local API**  
and displays live energy data on an **Adafruit Matrix Portal M4** with a 64×32 RGB LED matrix.

---

## 🧱 Hardware used

| Component | Description | Link |
|------------|--------------|------|
| [Adafruit Matrix Portal M4](https://www.adafruit.com/product/4812) | Main controller board with SAMD51 + ESP32 for Wi-Fi | [Digi-Key CH](https://www.digikey.ch/en/products/detail/adafruit-industries-llc/4812/15189153) |
| 64×32 RGB LED Matrix (HUB75) | Display panel | Included in the starter kit |
| USB-C cable | For power & programming | – |

💡 The Matrix Portal M4 already includes:
- a **SAMD51 microcontroller** (runs CircuitPython and drives the LED matrix)
- an **ESP32 co-processor** (handles Wi-Fi over SPI)

---

## 🧰 Software setup

### 1. Install CircuitPython
1. Connect the Matrix Portal M4 to your computer via **USB-C**.  
   It appears as a drive called `MATRIXBOOT`.
2. Copy the latest CircuitPython firmware (`.uf2` file) from  
   👉 [https://circuitpython.org/board/matrixportal_m4/](https://circuitpython.org/board/matrixportal_m4/)  
   onto the drive.
3. The board will reboot automatically and show a new drive called `CIRCUITPY`.

To update the ESP32 Wi-Fi firmware, follow:  
🔗 [Adafruit guide: Upgrading ESP32 firmware](https://learn.adafruit.com/upgrading-esp32-firmware/upgrade-all-in-one-esp32-airlift-firmware)

---

### 2. Development environment

You can edit files directly on the `CIRCUITPY` drive.

Two simple options:
- 🟣 **[Mu Editor](https://codewith.mu/)** – Adafruit’s beginner-friendly editor (recommended in tutorials)
- 🔵 **[Visual Studio Code](https://code.visualstudio.com/)** – my preferred option, with the **“Serial Monitor”** extension to view logs.

In VS Code, open the `CIRCUITPY` folder and use the serial monitor tab to see live output.

<img src="docs/serial_monitor.png" width="600" alt="VS Code Serial Monitor connected to Matrix Portal">

---

## ⚙️ Configuration

Copy the provided `settings.example.toml` to `settings.toml`  
and fill in your own credentials:

```toml
WIFI_SSID = "YourNetworkName"
WIFI_PASSWORD = "YourWifiPassword"
SOLAR_MANAGER_LOCAL_API_BASE_URL = "http://192.168.1.109/v2/point"
SOLAR_MANAGER_DEVICE_TEMP_ID = "68fb58ae04591f98546c0e4c"
