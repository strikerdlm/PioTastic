# Project Overview

This project integrates a Wio Terminal for environmental sensing with a Raspberry Pi for data processing, Meshtastic network communication, and MQTT publishing. The system is designed for robust, automated environmental data collection and off-grid/IoT transmission.

---

## System Architecture

- **Wio Terminal (`Wioterminal/Environmental_box.ino`)**: Collects environmental data from multiple sensors, displays it, logs to SD card, and streams structured data over USB serial.
- **Raspberry Pi (`Raspberrpi/`)**: Runs Python scripts to:
  - Listen to the Wio Terminal's serial output.
  - Relay sensor data to a Meshtastic network (LoRa mesh).
  - Publish sensor data to an MQTT broker for IoT dashboards.
  - Log all activity and data for debugging and analysis.
- **Meshtastic**: Provides long-range, off-grid mesh networking for sensor data.
- **MQTT**: Enables integration with cloud dashboards and IoT services.

---

## Wio Terminal: Environmental Sensing & Serial Protocol

- **Sensors Used:**
  - BME680: Temperature, humidity, barometric pressure.
  - Grove Multichannel Gas Sensor (GMXXX): NO2, C2H5OH (Ethanol), VOC, CO (with calibration and live Rs/R0 calculation).
  - UV Sensor: Ultraviolet light intensity.
  - Geiger Counter: Radiation (CPM, µSv/h).
  - RTC: Real-Time Clock for timestamping (using `RTC_SAMD51.h`).
- **Display:**
  - All sensor readings are shown on the TFT screen with color-coded status.
- **SD Card Logging:**
  - Data is logged as CSV to `test.csv` on the SD card.
- **Serial Output Protocol:**
  - Data is streamed over USB serial in a block format for easy parsing:
    ```
    START_DATA
    TIMESTAMP:DD:MM:YY, HH:MM
    TEMP:23.45 C
    HUMIDITY:45.21 %
    PRESSURE:760.12 mmHg
    UV:2.50 mW/cm2
    NO2:0.031 ppm
    C2H5OH:0.000 ppm
    VOC:0.102 ppm
    CO:0.015 ppm
    CPM:12
    USVH:0.08 uSv/h
    END_DATA
    ```
  - Each block is output every second.
  - Calibration for gas sensors is performed at startup and can fall back to defaults if needed.

---

## Raspberry Pi: Data Processing & Communication

### Main Scripts

- **`wio_to_meshtastic.py`**
  - Reads serial data from the Wio Terminal.
  - Parses each data block (between `START_DATA` and `END_DATA`).
  - Every 5 minutes: Sends the latest complete data block to the Meshtastic network (on a dedicated secondary channel, "Environ").
  - Every 2.5 minutes: Publishes the latest data block as a JSON object to an MQTT broker (topic: `wio/environmental_station/data`).
  - Adds a Raspberry Pi system timestamp (`RPI_TIMESTAMP`) to each data block.
  - Handles robust device auto-detection, error logging, and reconnection.
  - All activity and errors are logged to a timestamped file in the `logs/` directory.
  - MQTT credentials are loaded from a `.env` file in `Raspberrpi/`:
    ```env
    HIVEMQ_CLUSTER_URL=your_cluster_url_here
    HIVEMQ_USERNAME=your_username_here
    HIVEMQ_PASSWORD=your_password_here
    ```

- **`set_client.py`**
  - Connects to a Meshtastic device and listens for all incoming packets.
  - Logs all received packets (with timestamps and node/user mapping) to a file in `logs/`.
  - Maintains statistics and message history for each node.
  - No user interaction required; runs in silent logger mode.

- **`run_all.py`**
  - Orchestrates both `set_client.py` and `wio_to_meshtastic.py`.
  - Supports normal (interactive) and `--nohup` (background/daemon) modes.
  - In `--nohup` mode, all output is redirected to log files in `logs/` and the processes are automatically restarted if they crash.

### Running the System

1. **Install Dependencies** (on Raspberry Pi):
   ```bash
   pip3 install --upgrade "meshtastic[cli]" pyserial paho-mqtt python-dotenv
   ```
2. **Prepare MQTT Credentials:**
   - Create a `.env` file in `Raspberrpi/` as shown above.
3. **Connect Devices:**
   - Plug in the Wio Terminal and Meshtastic device via USB.
4. **Run the System:**
   - **Normal mode:**
     ```bash
     python3 run_all.py
     ```
   - **Background/daemon mode:**
     ```bash
     python3 run_all.py --nohup
     # Logs will be in Raspberrpi/logs/
     ```
   - Both scripts will auto-detect the correct serial ports. No manual selection is needed.

### Log Files
- All logs (data, errors, debug info) are written to the `logs/` directory with timestamped filenames.
- In `--nohup` mode, stdout/stderr for each script is also logged.

### Data Flow
- **Wio Terminal → Pi:**
  - Serial data blocks as described above.
- **Pi → Meshtastic:**
  - Each sensor reading is sent as a separate message to the "Environ" channel (index 1) every 5 minutes.
- **Pi → MQTT:**
  - The entire data block is published as a JSON object every 2.5 minutes.

---

## Troubleshooting & Tips

- **Device Not Found:**
  - Ensure both Wio Terminal and Meshtastic are connected and powered.
  - Check for correct drivers (CP210x, CH9102, etc.).
  - If a device is not detected, try reconnecting or rebooting.
- **MQTT Issues:**
  - Check `.env` credentials and broker status.
  - All MQTT connection and publish events are logged for debugging.
- **Meshtastic Channel Setup:**
  - The script configures a secondary channel named "Environ" (index 1) with a default PSK. Ensure your Meshtastic device supports multiple channels.
- **Logs:**
  - Review the `logs/` directory for detailed activity and error logs.
- **Debug Mode:**
  - Set `DEBUG = True` in the scripts for verbose output.
- **Safe Shutdown:**
  - Use Ctrl+C to stop in normal mode. In `--nohup` mode, kill the `run_all.py` process.

---

## References
- [Meshtastic Python API Documentation](https://meshtastic.org/docs/software/python/cli)
- [Seeed Studio Wio Terminal Documentation](https://wiki.seeedstudio.com/Wio-Terminal-Getting-Started/)
- [Grove Multichannel Gas Sensor](https://wiki.seeedstudio.com/Grove-Multichannel_Gas_Sensor/)
- [BME680 Sensor](https://wiki.seeedstudio.com/Grove-BME680-Gas-Sensor/)

---

## License

This project uses the GPL-3.0 license. See the LICENSE file for details. 