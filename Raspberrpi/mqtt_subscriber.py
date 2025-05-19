print("DEBUG: Script started.")

import paho.mqtt.client as paho
from paho import mqtt
import os
from dotenv import load_dotenv
import json
import time
from collections import deque
from datetime import datetime

# Rich imports will be removed or commented out
# try:
#     from rich.live import Live
#     from rich.table import Table
#     from rich.panel import Panel
#     from rich.layout import Layout
#     from rich.text import Text
#     from rich.console import Console, Group
#     from rich.columns import Columns
#     from rich import box
#     print("DEBUG: Rich library imports successful.")
# except ImportError as e:
#     print(f"DEBUG: FAILED to import Rich library components: {e}")
#     # import sys # No longer exiting if Rich fails, as it's not essential
#     # sys.exit(1)

# --- Configuration ---
MQTT_BROKER_TOPIC = "wio/environmental_station/data"
# MAX_LOG_MESSAGES = 10  # No longer needed for Rich log
# MAX_DATA_POINTS = 20   # No longer needed for Rich stats

# --- Global state for dashboard (simplified or removed) ---
# dashboard_data = { # Simplified, as Rich UI is removed
#     "connected": False,
#     "last_message_time": None,
#     "message_count": 0,
#     # "latest_readings": {}, # Will print directly
#     # "log_messages": deque(maxlen=MAX_LOG_MESSAGES),
#     # "recent_temps": deque(maxlen=MAX_DATA_POINTS),
#     # "recent_humidity": deque(maxlen=MAX_DATA_POINTS),
#     "connection_status_text": "Disconnected", # Still useful for basic logging
#     "broker_url": ""
# }
connection_status = {"connected": False, "status_text": "Disconnected", "broker_url": ""}


expected_keys = ["rpi_timestamp", "temp", "humidity", "pressure", "uv", "no2", "c2h5oh", "voc", "co", "cpm", "usvh"]

# Initialize console for occasional prints if needed outside Live
# console = Console() # Rich console removed

def add_log_message(message: str, level: str = "INFO"):
    # print(f"DEBUG: add_log_message CALLED with: '{message}', level: '{level}'") # Original debug
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"LOG [{timestamp} {level}] {message}") # Simplified logging

# def update_dashboard_data(payload_json: dict): # This function was for Rich UI state
    # dashboard_data["last_message_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # dashboard_data["message_count"] += 1
    
    # current_readings = {}
    # for key in expected_keys:
    #     current_readings[key] = payload_json.get(key, "N/A")
    # dashboard_data["latest_readings"] = current_readings

    # if "temp" in payload_json and isinstance(payload_json["temp"], (int, float)):
    #     dashboard_data["recent_temps"].append(payload_json["temp"])
    # if "humidity" in payload_json and isinstance(payload_json["humidity"], (int, float)):
    #     dashboard_data["recent_humidity"].append(payload_json["humidity"])
    
    # add_log_message(f"Data received (for Rich). Temp: {current_readings.get('temp', 'N/A')}", "DATA")

# def calculate_stats(data_deque: deque): # This was for Rich UI
#     if not data_deque:
#         return {"min": "N/A", "max": "N/A", "avg": "N/A"}
#     valid_data = [x for x in data_deque if isinstance(x, (int, float))]
#     if not valid_data:
#         return {"min": "N/A", "max": "N/A", "avg": "N/A"}
#     return {
#         "min": f"{min(valid_data):.2f}",
#         "max": f"{max(valid_data):.2f}",
#         "avg": f"{sum(valid_data) / len(valid_data):.2f}"
#     }

# def generate_dashboard_layout() -> Panel: # This was for Rich UI
#     print("DEBUG: generate_dashboard_layout() CALLED (but Rich is disabled)")
#     return None # Placeholder

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        connection_status["connected"] = True
        connection_status["status_text"] = "Connected"
        add_log_message(f"Connected to MQTT Broker (rc: {rc})", "INFO")
        client.subscribe(MQTT_BROKER_TOPIC, qos=1)
        add_log_message(f"Subscribed to {MQTT_BROKER_TOPIC}", "INFO")
    else:
        connection_status["connected"] = False
        connection_status["status_text"] = f"Connection Failed (rc: {rc})"
        add_log_message(f"Failed to connect to MQTT Broker, code {rc}", "ERROR")

def on_message(client, userdata, msg):
    try:
        payload_json = json.loads(msg.payload.decode())
        # update_dashboard_data(payload_json) # No longer updating Rich dashboard state
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"DATA [{timestamp}] Received: {json.dumps(payload_json)}") # Print raw data
        # Optional: Print specific fields
        # temp = payload_json.get("temp", "N/A")
        # humidity = payload_json.get("humidity", "N/A")
        # print(f"DATA [{timestamp}] Temp: {temp}, Humidity: {humidity}")

    except json.JSONDecodeError:
        add_log_message(f"JSONDecodeError for payload: {msg.payload.decode()[:50]}...", "ERROR")
    except Exception as e:
        add_log_message(f"Error processing message: {e}", "ERROR")

def on_disconnect(client, userdata, rc, properties=None):
    connection_status["connected"] = False
    connection_status["status_text"] = f"Disconnected (rc: {rc})"
    add_log_message(f"Disconnected from MQTT Broker (rc: {rc})", "WARN")


def main_mqtt_client_loop():
    print("DEBUG: main_mqtt_client_loop started (Simplified - No Rich UI).")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    add_log_message(f"Calculated .env path: {dotenv_path}", "DEBUG")

    if os.path.exists(dotenv_path):
        add_log_message(f".env file found at {dotenv_path}. Attempting to load.", "DEBUG")
        load_dotenv(dotenv_path)
        test_url_after_load = os.getenv("HIVEMQ_CLUSTER_URL")
        add_log_message(f"Loaded .env from {dotenv_path}. HIVEMQ_CLUSTER_URL is {'SET' if test_url_after_load else 'NOT SET'}.", "DEBUG")
    else:
        add_log_message(f".env file NOT found at {dotenv_path}. Will rely on pre-set environment variables.", "WARN")

    cluster_url = os.getenv("HIVEMQ_CLUSTER_URL")
    username = os.getenv("HIVEMQ_USERNAME")
    password = os.getenv("HIVEMQ_PASSWORD")
    connection_status["broker_url"] = cluster_url or "Not Set"

    add_log_message(f"Credentials after attempting load: URL set: {bool(cluster_url)}, User set: {bool(username)}, Pass set: {bool(password)}", "DEBUG")

    if not all([cluster_url, username, password]):
        add_log_message("CRITICAL: Missing MQTT credentials (URL, Username, or Password). Cannot connect. Please check .env file or environment variables.", "CRITICAL")
        print("[CRITICAL] MQTT Error: Missing credentials. Script cannot connect. Check logs.")
        return

    client = paho.Client(client_id=f"cli_dashboard_subscriber_{os.getpid()}", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username, password)

    add_log_message(f"Attempting to connect to broker: {cluster_url}:8883...", "INFO")
    try:
        client.connect(cluster_url, 8883, keepalive=60)
        client.loop_start()
        
        add_log_message("MQTT client loop started. Waiting for messages...", "INFO")
        while True:
            # You can add checks here, e.g., to reconnect if connection_status["connected"] is false
            # For now, just keep the main thread alive.
            if not connection_status["connected"] and connection_status["status_text"] != "Connecting...": # Basic reconnect logic placeholder
                add_log_message("Attempting to reconnect...", "WARN")
                connection_status["status_text"] = "Connecting..."
                try:
                    # client.reconnect() # paho has automatic reconnect, but can be managed explicitly
                    # For simplicity, we rely on paho's auto-reconnect or restart script if persistent issues.
                    # If manual reconnect is needed, one might call client.connect() again,
                    # but ensure loop is stopped/started correctly.
                    # This simple loop doesn't implement full robust reconnection.
                    pass # Rely on paho's built-in mechanisms for now or manual restart.
                except Exception as recon_e:
                    add_log_message(f"Error during manual reconnect attempt: {recon_e}", "ERROR")

            time.sleep(1)

    except KeyboardInterrupt:
        add_log_message("Script stopped by user (KeyboardInterrupt).", "INFO")
        print("\nScript stopped by user.")
    except Exception as e:
        add_log_message(f"MQTT connection/loop error: {e}", "CRITICAL")
        print(f"[CRITICAL] MQTT error: {e}")
    finally:
        add_log_message("Disconnecting MQTT client...", "INFO")
        if client.is_connected(): # Check if connected before stopping loop/disconnecting
             client.loop_stop()
             client.disconnect()
        print("MQTT client disconnected.")


if __name__ == "__main__":
    print("DEBUG: __main__ block started (Simplified - No Rich UI).")
    # dashboard_data["latest_readings"] = {key: "N/A" for key in expected_keys} # No longer needed for Rich
    add_log_message("Script initializing...", "INFO")
    
    try:
        main_mqtt_client_loop()
    except Exception as e:
        print(f"DEBUG: Unhandled error in main_mqtt_client_loop call: {e}")
        add_log_message(f"Main execution error: {e}", "CRITICAL")
    finally:
        print("Script shutdown complete.")