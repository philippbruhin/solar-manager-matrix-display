# 🌞 Matrix Display for Solar Manager

This repository contains the CircuitPython firmware for driving a 64×32 RGB LED matrix (HUB75) using an Adafruit Matrix Portal M4. The display shows live energy data from the Solar Manager gateway via its local API.

This readme is meant only for the code and how to run it on the micro controller. Information about Solar Manager itself and this project in general, is documented separately on the GH Pages site in German.

This small display gives a quick visual overview of:
- 🏠 **House consumption**
- ☀️ **Solar generation**
- 🔋 **Battery state of charge**
- 🚿 **Hot water temperature**

![Screen Segmentation](./docs/assets/img/matrix-display-screen-segmentation.jpg)

It helps build intuition for how much energy different devices use  and shows how small changes (like lowering the floor heating by 1 °C) affect power draw.

This project connects to a **Solar Manager** gateway via its **local API** and displays live energy data on an **Adafruit Matrix Portal M4** with a 64×32 RGB LED matrix. So make sure you enalbe the local API on [web.solar-manager.ch/my-devices/](https://web.solar-manager.ch/my-devices/).

![Enable Local API](./docs/assets/img/solar-manager-local-api.png)

## 🧱 Hardware used

| Component | Description | Link |
|------------|--------------|------|
| [Adafruit Matrix Portal M4](https://www.adafruit.com/product/4812) | Main controller board with SAMD51 + ESP32 for Wi-Fi | [Digi-Key CH](https://www.digikey.ch/en/products/detail/adafruit-industries-llc/4812/15189153) |
| 64×32 RGB LED Matrix (HUB75) | Display panel | Included in the starter kit |
| USB-C cable and power supply | For power & programming | Included, but with **US plug** – not usable in Switzerland |

💡 The Matrix Portal M4 includes:
- a **SAMD51 microcontroller** (runs CircuitPython and drives the LED matrix)
- an **ESP32 co-processor** (handles Wi-Fi via SPI)

> The kit’s USB power supply includes a **US plug**. You can use any 5 V / 2 A (or higher) USB-C power adapter instead.

## 🧰 Firmware & library setup

### 1. Update CircuitPython firmware (do this first)

1. Connect the Matrix Portal M4 to your computer via **USB-C**.  
   It will appear as a drive named `MATRIXBOOT`.
2. Download the latest **CircuitPython firmware (.uf2)** from:  
   👉 [https://circuitpython.org/board/matrixportal_m4/](https://circuitpython.org/board/matrixportal_m4/)
3. Drag and drop the file onto the `MATRIXBOOT` drive.  
   The board will reboot and reappear as `CIRCUITPY`.

You can also update the ESP32 Wi-Fi firmware if needed:  
🔗 [Adafruit: Upgrade ESP32 AirLift firmware](https://learn.adafruit.com/upgrading-esp32-firmware/upgrade-all-in-one-esp32-airlift-firmware)

### 2. CircuitPython libraries

This project uses the **Adafruit CircuitPython Bundle v10.x**,  
and all necessary libraries are already included in the `/lib` folder of this repository.

You **do not need to install anything manually** if you use this version.

However:

> ⚠️ If you later install a newer CircuitPython firmware (e.g., v11 or higher), you must also update the libraries to match that version.

You can always download the latest bundle here:  
👉 [https://circuitpython.org/libraries](https://circuitpython.org/libraries)

Simply unzip the bundle and copy the updated libraries you need into the `/lib` folder on `CIRCUITPY`.

## 📁 Project file overview

```
CIRCUITPY/
│
├── code.py
├── config.py
├── ui.py
├── helpers.py
│
├── assets/
│   ├── icon-battery-empty.bmp
│   ├── icon-battery-full.bmp
│   ├── icon-house.bmp
│   ├── icon-shower.bmp
│   ├── icon-sun.bmp
│
├── settings.toml   ← created by you, not in repo
├── settings.example.toml
│
└── lib/            ← CircuitPython libraries

```

| File / Folder             | Purpose                      | Notes                                                         |
| ------------------------- | ---------------------------- | ------------------------------------------------------------- |
| **code.py**               | Main application entry point | Starts Wi-Fi, fetches Solar Manager data, updates the display |
| **config.py**             | Configuration values         | Colors, layout positions, refresh intervals, display settings |
| **ui.py**                 | User interface rendering     | Loads icons, draws text, builds the display group             |
| **helpers.py**            | Utility functions            | Value formatting, number helpers, safe parsing                |
| **assets/**               | Bitmap icons used in UI      | `.bmp` files for solar, house, battery, boiler, etc.          |
| **settings.toml**         | Your private configuration   | Wi-Fi credentials + Solar Manager API URL (**not in repo**)   |
| **settings.example.toml** | Template for settings        | Copy to `settings.toml` and fill your values                  |
| **lib/**                  | CircuitPython libraries      | Needed by the Matrix Portal (bundled in repo)                 |

## ⚙️ Configuration

Copy the provided `settings.example.toml` to `settings.toml`  
and fill in your own credentials:

```toml
WIFI_SSID = "YourNetworkName"
WIFI_PASSWORD = "YourWifiPassword"
SOLAR_MANAGER_LOCAL_API_BASE_URL = "http://<your-local-solar-manager-ip>/v2/point"
SOLAR_MANAGER_DEVICE_TEMP_ID = "68f..."

⚠️ Never upload your real settings.toml to GitHub — it contains private data.
The file is ignored by .gitignore, and only settings.example.toml is part of the repository.

This project uses the local Solar Manager API —
simple HTTP, no authentication, and ideal for a small microcontroller.
