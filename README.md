# Project Overview

This project integrates a Wio Terminal for environmental sensing with a Raspberry Pi for data processing, Meshtastic network communication, and potentially as a Meshtastic router.

**Wio Terminal (`Wioterminal/` directory):**
*   The `Environmental_box.ino` sketch configures the Wio Terminal as a comprehensive environmental data logger.
*   It collects data from various sensors, including:
    *   BME680: Temperature, humidity, and barometric pressure.
    *   Multichannel Gas Sensor: NO2, C2H5OH (Ethanol), VOCs (Volatile Organic Compounds), and CO (Carbon Monoxide).
    *   UV Sensor: Ultraviolet light intensity.
    *   Geiger Counter: Radiation levels (CPM and µSv/h).
    *   RTC: Real-Time Clock for timestamping.
*   The Wio Terminal displays this data on its TFT screen, logs it to an SD card, and outputs structured data via the USB serial port.

**Raspberry Pi (`Raspberrpi/` directory):**
*   Python scripts on the Raspberry Pi interface with both the Wio Terminal and Meshtastic devices.
*   `wio_to_meshtastic.py`: This script reads the structured serial data from the Wio Terminal, parses the sensor readings, relays them as individual messages over a connected Meshtastic network, and also publishes the complete sensor data block as a JSON object to an MQTT broker.
*   `grove_gas_meshtastic_sender.py`: Appears to be another script for sending gas sensor data via Meshtastic, potentially for a different gas sensor setup or a more direct connection.
*   Meshtastic Control & Routing: Other scripts like `meshtastic_router.py`, `configure_router.py`, `set_client.py`, `meshtastic_receive.py`, `connect_device.py`, and `reset_device.py` provide utilities to:
    *   Configure and manage a Meshtastic node running on the Raspberry Pi (e.g., as a router or client).
    *   Send and receive Meshtastic messages.
    *   Connect to and reset Meshtastic devices.
*   `distance_calculator.py`: A utility likely used for calculating distances, possibly between Meshtastic nodes.
*   `test_serial.py`: A script for testing serial communications.

**MQTT Integration (via `wio_to_meshtastic.py`):**
*   The `wio_to_meshtastic.py` script now supports publishing sensor data to an MQTT broker.
*   This allows for integration with various IoT dashboards and services (e.g., Node-RED, IoT MQTT Panel, Adafruit IO).
*   **Configuration:** To enable MQTT publishing, create a `.env` file in the `Raspberrpi/` directory with your HiveMQ Cloud (or other MQTT broker) credentials:
    ```env
    HIVEMQ_CLUSTER_URL=your_cluster_url_here
    HIVEMQ_USERNAME=your_username_here
    HIVEMQ_PASSWORD=your_password_here
    ```
*   **Topic:** Data is published to the topic `wio/environmental_station/data` by default.
*   **Payload:** The sensor data is published as a JSON object, for example:
    ```json
    {
      "timestamp": "DD:MM:YY, HH:MM",
      "temp": 23.45,
      "humidity": 45.21,
      "pressure": 760.12,
      "uv": 2.50,
      "no2": 0.031,
      "c2h5oh": 0.000,
      "voc": 0.102,
      "co": 0.015,
      "cpm": 12,
      "usvh": 0.08
    }
    ```

The overall architecture allows for remote environmental monitoring where the Wio Terminal collects data locally, and the Raspberry Pi transmits this data over a long-range, off-grid Meshtastic network and simultaneously publishes it to an MQTT broker for wider accessibility and dashboarding. The Raspberry Pi can also serve other Meshtastic network functions.

The following sections detail how to set up and use the Python scripts for controlling Meshtastic devices, which form a core part of the Raspberry Pi's functionality in this project.

# Controlling Meshtastic Devices with Python

This guide provides step-by-step instructions for controlling Meshtastic devices using Python.

## Prerequisites

Before getting started, ensure you have:

1. A Meshtastic-compatible device (like TTGO T-Beam, Heltec, etc.)
2. Python 3 installed on your system
   - Check with: `python3 -V`
   - If not installed, download from [python.org](https://python.org)
3. Required serial drivers:
   - For CP210X USB to UART bridge
   - For CH9102 (newer boards)
   - Check device manager or system settings to verify driver installation

## Installation

1. Install pip (Python package installer) if not already installed:
   ```bash
   python3 -m ensurepip --upgrade
   ```

2. Install pytap2 (if needed for other functionalities, not directly by these scripts):
   ```bash
   pip3 install --upgrade pytap2
   ```

3. Install the Meshtastic Python package and other dependencies:
   ```bash
   pip3 install --upgrade "meshtastic[cli]" pyserial paho-mqtt python-dotenv
   ```

   Note: The `[cli]` suffix installs optional dependencies for command-line interface support. `pyserial` is for serial communication, `paho-mqtt` for MQTT, and `python-dotenv` for loading credentials from the `.env` file.

## Basic Usage

### 1. Connecting to a Device

```python
import meshtastic
import meshtastic.serial_interface

# Connect to the first available device
interface = meshtastic.serial_interface.SerialInterface()

# Or specify a port manually
# interface = meshtastic.serial_interface.SerialInterface(devPath="/dev/ttyUSB0")
```

### 2. Sending Messages

```python
# Send a text message (broadcast to all nodes)
interface.sendText("Hello mesh network!")

# Send to a specific node
interface.sendText("Hello specific node!", destinationId="!abcd1234")

# Send binary data
interface.sendData(b"Binary data here")
```

### 3. Receiving Messages

```python
from pubsub import pub

def onReceive(packet, interface): 
    print(f"Received: {packet}")

def onConnection(interface, topic=pub.AUTO_TOPIC): 
    print("Connected to radio")
    interface.sendText("Connected!")

# Subscribe to message events
pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")
```

### 4. Configuration

```python
# Set WiFi credentials (for ESP32 devices)
interface.sendText("--set wifi_ap_mode false --setstr wifi_ssid myssid --setstr wifi_password mypass")

# Set node parameters
interface.sendText("--setalt 120")  # Set altitude
interface.sendText("--setlat 37.7749")  # Set latitude
interface.sendText("--setlon -122.4194")  # Set longitude
```

## Common Operations

### Check Device Info
```python
print(f"My node info: {interface.myInfo}")
print(f"Nodes in network: {interface.nodes}")
```

### Channel Settings
```python
# Get current channel settings
print(f"Channel: {interface.localNode.channels[0]}")

# Change channel name
interface.localNode.writeConfig("channel.name", "mychannel")
```

### Close Connection
```python
interface.close()
```

## Event Types

Subscribe to specific events using these topics:

- `meshtastic.receive.text` - Text messages
- `meshtastic.receive.position` - Position updates
- `meshtastic.receive.user` - User info updates
- `meshtastic.connection.established` - Connection established
- `meshtastic.connection.lost` - Connection lost
- `meshtastic.node.updated` - Node database changes

## Troubleshooting

1. Permission Denied ('/dev/ttyUSB0'):
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and back in for changes to take effect
   ```

2. MacOS Big Sur Issues:
   ```bash
   pip3 install -U --pre pyserial
   ```

3. Device Not Found:
   - Check USB connection
   - Verify correct drivers are installed
   - Try different USB ports
   - Check device permissions

## Additional Resources

- [Meshtastic Python API Documentation](https://meshtastic.org/docs/software/python/cli)
- [Meshtastic GitHub Repository](https://github.com/meshtastic/python)
- [Meshtastic Community Forum](https://meshtastic.discourse.group/)

## License

This project uses the GPL-3.0 license. See the LICENSE file for details. 