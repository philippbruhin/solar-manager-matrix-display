# 🌞 Matrix Display for Solar Manager (Adafruit Matrix Portal M4)

## 💡 Project idea

After installing solar panels at home, I wanted to **see my energy flow in real time** —  
how much power is produced, how much is used, and where it goes (e.g., EV, heat pump, boiler).

This small display gives a quick visual overview of:
- 🏠 **House consumption**
- ☀️ **Solar generation**
- 🔋 **Battery state of charge**
- 🚿 **Hot water temperature**

It helps build intuition for how much energy different devices use  
and shows how small changes (like lowering the floor heating by 1 °C) affect power draw.

This project connects to a **Solar Manager** gateway via its **local API**  
and displays live energy data on an **Adafruit Matrix Portal M4** with a 64×32 RGB LED matrix.

---

## ⚡ What the Solar Manager does

The [**Solar Manager**](https://www.solarmanager.ch/) is a smart energy controller that optimizes your self-consumption.

It measures your **solar production**, **household consumption**, and **battery level**,  
and automatically distributes power to where it’s most useful.

For example:
- When a lot of sunlight is available, it can **heat water** or **charge your EV**.
- When clouds reduce production, it **pauses less important loads**.
- At night, it can **draw from your home battery** instead of the grid.

This increases your **self-consumption** — meaning you use more of your own solar energy  
instead of feeding it into the grid at a low rate.  
The more solar energy you use directly, the higher your **autonomy** and **efficiency**.

Unlike nuclear or fossil power, solar energy is **weather-dependent**.  
Production varies daily, so adapting your consumption (for example, running the dishwasher  
or heating water when the sun is shining) helps balance supply and demand.

By using more of your own clean energy, you reduce stress on the public grid,  
save costs, and make your home more sustainable.

---

## 🧱 Hardware used

| Component | Description | Link |
|------------|--------------|------|
| [Adafruit Matrix Portal M4](https://www.adafruit.com/product/4812) | Main controller board with SAMD51 + ESP32 for Wi-Fi | [Digi-Key CH](https://www.digikey.ch/en/products/detail/adafruit-industries-llc/4812/15189153) |
| 64×32 RGB LED Matrix (HUB75) | Display panel | Included in the starter kit |
| USB-C cable and power supply | For power & programming | Included, but with **US plug** – not usable in Switzerland 🇨🇭 |

💡 The Matrix Portal M4 includes:
- a **SAMD51 microcontroller** (runs CircuitPython and drives the LED matrix)
- an **ESP32 co-processor** (handles Wi-Fi via SPI)

> ⚠️ The kit’s USB power supply includes a **US plug**.  
> You can use any 5 V / 2 A (or higher) USB-C power adapter instead.

---

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

---

### 2. CircuitPython libraries

This project uses the **Adafruit CircuitPython Bundle v10.x**,  
and all necessary libraries are already included in the `/lib` folder of this repository.

You **do not need to install anything manually** if you use this version.

However:

> ⚠️ If you later install a newer CircuitPython firmware (e.g., v11 or higher),  
> you must also update the libraries to match that version.

You can always download the latest bundle here:  
👉 [https://circuitpython.org/libraries](https://circuitpython.org/libraries)

Simply unzip the bundle and copy the updated libraries you need into the `/lib` folder on `CIRCUITPY`.

---

## 🧮 Folder structure

TODO


---

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
