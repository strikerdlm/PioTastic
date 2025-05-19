import serial
import serial.tools.list_ports
import meshtastic
import meshtastic.serial_interface
import time
import argparse
import os
import json
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt
import datetime # Added for logging timestamps
import base64 # Added for PSK decoding
import traceback # Moved import traceback to the top

# --- Global Settings ---
DEBUG = True  # Set to True for verbose debug output
MQTT_TOPIC = "wio/environmental_station/data"
LOG_FILE = None # Added for logging
LOG_FILENAME = None # Added for logging

# --- MQTT Client Setup ---
mqtt_client = None
mqtt_connected = False
# Instead, use specific timers:
last_meshtastic_sent_time = 0
last_mqtt_sent_time = 0
last_wio_data_block_update_time = 0 # ADDED: Timer for Wio data block updates
last_wio_raw_print_time = 0 # ADDED: Timer for Wio Raw print statements
latest_complete_data_block = None # Added for timed sending
currently_printing_raw_block = False # ADDED: Flag to control raw printing for an entire block

def on_connect(client, userdata, flags, rc, properties=None):
    global mqtt_connected
    if rc == 0:
        if DEBUG: print("MQTT: Connected successfully.")
        mqtt_connected = True
        log_activity("mqtt_connected", {"client_id": client._client_id.decode() if client._client_id else "Unknown", "result_code": rc})
    else:
        print(f"MQTT: Connection failed with code {rc}")
        mqtt_connected = False
        log_activity("mqtt_connect_failed", {"client_id": client._client_id.decode() if client._client_id else "Unknown", "result_code": rc, "flags": flags})

def on_publish(client, userdata, mid, properties=None):
    if DEBUG: print(f"MQTT: Published message with mid {mid}")
    log_activity("mqtt_published_ack", {"client_id": client._client_id.decode() if client._client_id else "Unknown", "message_id": mid})

def on_disconnect(client, userdata, rc, properties=None):
    global mqtt_connected
    print(f"MQTT: Disconnected with result code {rc}")
    mqtt_connected = False
    log_activity("mqtt_disconnected_event", {"client_id": client._client_id.decode() if client._client_id else "Unknown", "result_code": rc})
    # Optionally, you can attempt to reconnect here
    # if rc != 0:
    #     print("MQTT: Unexpected disconnection. Attempting to reconnect...")
    #     # Implement reconnection logic if needed, e.g., client.reconnect()

def setup_mqtt_client():
    global mqtt_client
    try:
        # Ensure .env is in the same directory as this script or adjust path
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        env_loaded = False
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            env_loaded = True
        else:
            if DEBUG: print(f"MQTT: .env file not found at {dotenv_path}. Trying to load from current dir or environment vars.")
            load_dotenv() # Tries current dir or already set env vars
            # Check if still loaded after attempting default paths
            if os.getenv("HIVEMQ_CLUSTER_URL"): # Check one var as proxy for successful load
                 env_loaded = True

        log_activity("mqtt_setup_env_load", {"dotenv_path_checked": dotenv_path, "env_loaded_successfully": env_loaded})
            
        cluster_url = os.getenv("HIVEMQ_CLUSTER_URL")
        username = os.getenv("HIVEMQ_USERNAME")
        password = os.getenv("HIVEMQ_PASSWORD")

        if not all([cluster_url, username, password]):
            print("MQTT Error: Missing one or more credentials. Please check .env file (HIVEMQ_CLUSTER_URL, HIVEMQ_USERNAME, HIVEMQ_PASSWORD) or environment variables.")
            log_activity("mqtt_setup_error", {"reason": "Missing credentials", "needed": ["HIVEMQ_CLUSTER_URL", "HIVEMQ_USERNAME", "HIVEMQ_PASSWORD"]})
            return None

        client = paho.Client(client_id="wio_to_meshtastic_bridge", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect

        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        client.username_pw_set(username, password)
        
        if DEBUG: print(f"MQTT: Attempting to connect to broker at {cluster_url}:8883")
        log_activity("mqtt_connect_attempt", {"cluster_url": cluster_url, "port": 8883, "client_id":"wio_to_meshtastic_bridge"})
        client.connect(cluster_url, 8883)
        client.loop_start()
        # Connection status is handled by on_connect callback, which can also log
        return client
    except Exception as e:
        print(f"MQTT Setup Error: {e}")
        log_activity("mqtt_setup_exception", {"error": str(e), "traceback": traceback.format_exc() if DEBUG else "Set DEBUG for traceback"})
        if DEBUG: import traceback; traceback.print_exc()
        return None

# --- End MQTT Client Setup ---

# --- Logging Setup ---
def make_serializable(obj):
    """Recursively make objects JSON serializable."""
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(make_serializable(item) for item in obj)
    elif isinstance(obj, bytes):
        return obj.hex()  # Convert bytes to hex string
    elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        # Fallback for objects, trying to get their __dict__
        # Be cautious with this, as it might expose too much or fail for complex objects
        try:
            return make_serializable(obj.__dict__)
        except RecursionError: # Protect against objects that might reference themselves or cause deep recursion
            return f"UNSERIALIZABLE_OBJECT_RECURSION:{str(type(obj))}"
        except Exception:
             return f"UNSERIALIZABLE_OBJECT:{str(type(obj))}"
    else:
        try:
            # For basic types that are already serializable or can be converted to string
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            return str(obj)
        except Exception:
            return f"UNSERIALIZABLE_TYPE:{str(type(obj))}"

def log_activity(event_type: str, details: dict):
    """Logs an activity to the global log file."""
    global LOG_FILE, DEBUG
    if not LOG_FILE:
        if DEBUG: print(f"Log Activity Error: Log file not initialized. Event: {event_type}")
        return

    try:
        now_dt = datetime.datetime.now()
        log_entry = {
            'timestamp': now_dt.isoformat(),
            'event_type': event_type,
            'details': make_serializable(details) # Ensure details are serializable
        }
        json_log_entry = json.dumps(log_entry)
        LOG_FILE.write(json_log_entry + "\n")
        LOG_FILE.flush() # Flush after each write
    except Exception as e:
        print(f"[CRITICAL LOG ERROR] Failed to write log entry. Event: {event_type}, Error: {e}")
        if DEBUG: import traceback; traceback.print_exc()
# --- End Logging Setup ---

def list_available_serial_ports():
    """Lists all available serial ports with their descriptions."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Serial: No serial ports detected on this system.")
        return []
    print("Serial: Available serial ports:")
    for i, port_info in enumerate(ports):
        print(f"  {i + 1}: {port_info.device} - {port_info.description} [VID:{port_info.vid:04X}, PID:{port_info.pid:04X}, SN:{port_info.serial_number}]")
    return ports

def find_specific_device_port(device_name, keywords, vid_pid_pairs=None, exclude_port=None, target_device_path=None, target_description=None):
    """Finds a specific device port based on keywords, VID/PID, and a specific target path/description."""
    if vid_pid_pairs is None:
        vid_pid_pairs = []
    ports = list(serial.tools.list_ports.comports())
    found_ports = []

    # Stage 0: Check for specific target device path and description if provided (highest priority)
    if target_device_path and target_description:
        for port_info in ports:
            if port_info.device == target_device_path and target_description.lower() in port_info.description.lower():
                if exclude_port and port_info.device == exclude_port:
                    if DEBUG: print(f"Serial: find_specific_device_port - Skipping excluded port {port_info.device} for {device_name} (target match)")
                    continue
                print(f"Serial: [PRIORITY] Found target {device_name} by specific path/description: {port_info.device}")
                log_activity("serial_found_priority_target", {"device_name": device_name, "port": port_info.device, "description": port_info.description})
                return port_info.device # Return immediately if the priority target is found

    # Stage 1: Match by VID/PID
    for port_info in ports:
        if exclude_port and port_info.device == exclude_port:
            if DEBUG: print(f"Serial: find_specific_device_port - Skipping excluded port {port_info.device} for {device_name} (VID/PID check)")
            continue
        if port_info.vid and port_info.pid:
            for vid, pid, name_check in vid_pid_pairs:
                if port_info.vid == vid and port_info.pid == pid:
                    if name_check is None or name_check.lower() in port_info.description.lower():
                        if DEBUG: print(f"Serial: Found {device_name} by VID/PID: {port_info.device} ({port_info.description})")
                        if port_info.device not in found_ports: found_ports.append(port_info.device)
                        break # Found a VID/PID match for this port_info, move to next port_info
    
    # Stage 2: Match by keywords if no VID/PID matches found yet for this port
    for port_info in ports:
        if port_info.device in found_ports: continue # Already found by VID/PID
        if exclude_port and port_info.device == exclude_port:
            if DEBUG: print(f"Serial: find_specific_device_port - Skipping excluded port {port_info.device} for {device_name} (keyword check)")
            continue
        if any(keyword.lower() in port_info.description.lower() for keyword in keywords):
            if DEBUG: print(f"Serial: Found potential {device_name} by keyword in description: {port_info.device} ({port_info.description})")
            if port_info.device not in found_ports: found_ports.append(port_info.device)
        elif port_info.manufacturer and any(keyword.lower() in port_info.manufacturer.lower() for keyword in keywords):
            if DEBUG: print(f"Serial: Found potential {device_name} by keyword in manufacturer: {port_info.device} ({port_info.manufacturer})")
            if port_info.device not in found_ports: found_ports.append(port_info.device)
    
    if len(found_ports) == 1:
        print(f"Serial: Automatically selected {found_ports[0]} for {device_name}.")
        return found_ports[0]
    elif len(found_ports) > 1:
        print(f"Serial: Multiple potential ports found for {device_name}: {found_ports}")
        # In full auto mode, we don't want to call select_port_interactive here.
        # Instead, we rely on the higher-level functions (connect_meshtastic, connect_wio_terminal)
        # to provide the target_device_path and target_description for a definitive match.
        # If those aren't provided or don't match, and we still have multiple, it's an ambiguous situation.
        log_activity("serial_multiple_ports_ambiguous", {"device_name": device_name, "found_ports": found_ports})
        print(f"Serial: Ambiguous - multiple ports for {device_name} and no definitive target. Returning None.")
        return None 
        
    return None

def select_port_interactive(prompt_message, candidate_ports):
    """Allows the user to select a port from a list of candidates via CLI. THIS SHOULD NOT BE CALLED IN FULLY AUTOMATIC MODE."""
    # This function should ideally not be reached if auto-selection is working correctly.
    # If it is, it means there's an unhandled ambiguity or failure in auto-detection.
    print(f"[WARNING] Interactive port selection triggered for {prompt_message.split(':')[0]}. This should not happen in fully automatic mode.")
    log_activity("serial_interactive_prompt_unexpected", {"prompt": prompt_message, "candidates": candidate_ports})
    # For safety in a headless environment, if this is ever called, return None to prevent hanging.
    return None 

def connect_meshtastic(cli_port=None, wio_port=None):
    """Connects to a Meshtastic device with improved detection and fallback."""
    print("\nMeshtastic: Initializing connection...")
    if wio_port and DEBUG: print(f"Meshtastic: Note - Wio Terminal is connected on {wio_port}. This port will be excluded if possible.")
    iface = None
    meshtastic_keywords = ['CP210x', 'CH340', 'CH910', 'USB Serial', 'Meshtastic', 'ACM0']
    meshtastic_vid_pids = [
        (0x10C4, 0xEA60, "CP210x"),
        (0x1A86, 0x7523, "CH340"),
        (0x0403, 0x6001, "FTDI"),
        (0x1A86, 0x55D4, "USB Single Serial") # Target Meshtastic
    ]

    # Target Meshtastic device specifics
    TARGET_MESH_PATH = '/dev/ttyACM0'
    TARGET_MESH_DESC = 'USB Single Serial'

    if cli_port:
        if cli_port == wio_port:
            print(f"Meshtastic Warning: Specified port --mesh_port {cli_port} is already in use by Wio Terminal.")
            # Fall through to auto-detection
        else:
            print(f"Meshtastic: Attempting connection to specified port: {cli_port}")
            log_activity("meshtastic_connect_attempt_cli", {"port": cli_port})
            try:
                iface = meshtastic.serial_interface.SerialInterface(devPath=cli_port)
                print(f"Meshtastic: Successfully connected to node {iface.myInfo.my_node_num} on specified port {cli_port}.")
                log_activity("meshtastic_connect_success_cli", {"port": cli_port, "node_num": iface.myInfo.my_node_num, "node_info": make_serializable(iface.myInfo)})
                return iface
            except Exception as e:
                print(f"Meshtastic Error: Could not connect on specified port {cli_port}: {e}")
                log_activity("meshtastic_connect_error_cli", {"port": cli_port, "error": str(e)})
                # Fall through if specified port fails

    # Auto-detection: Pass target path and description to find_specific_device_port
    print(f"Meshtastic: Searching for device (Target: {TARGET_MESH_PATH} - '{TARGET_MESH_DESC}')...")
    log_activity("meshtastic_connect_autodetect_start", {"excluded_port": wio_port, "target_path": TARGET_MESH_PATH, "target_desc": TARGET_MESH_DESC})
    auto_detected_port = find_specific_device_port(
        "Meshtastic Device", 
        meshtastic_keywords, 
        meshtastic_vid_pids, 
        exclude_port=wio_port, 
        target_device_path=TARGET_MESH_PATH, 
        target_description=TARGET_MESH_DESC
    )
    
    if auto_detected_port:
        try:
            print(f"Meshtastic: Attempting connection to auto-detected/targeted port: {auto_detected_port}")
            iface = meshtastic.serial_interface.SerialInterface(devPath=auto_detected_port)
            print(f"Meshtastic: Successfully connected to node {iface.myInfo.my_node_num} on {auto_detected_port}.")
            log_activity("meshtastic_connect_success_auto", {"port": auto_detected_port, "node_num": iface.myInfo.my_node_num, "node_info": make_serializable(iface.myInfo)})
            return iface
        except Exception as e:
            print(f"Meshtastic Error: Could not connect on auto-detected/targeted port {auto_detected_port}: {e}")

    print("Meshtastic: Failed to establish connection. No manual port selection prompt in this mode.")
    log_activity("meshtastic_connect_failed_all_attempts", {})
    return None

def connect_wio_terminal(cli_port=None):
    """Connects to the Wio Terminal serial port with improved detection and fallback."""
    print("\nWio Terminal: Initializing connection...")
    log_activity("wio_connect_start", {"cli_port_arg": cli_port})
    ser = None
    wio_keywords = ['Seeeduino', 'Wio', 'WioTerminal', 'USB Serial Device', 'ACM1']
    wio_vid_pids = [
        (0x2886, 0x802F, "Wio Terminal"), # VID 0x2886, PID 0x802F
        (0x2886, 0x002F, "Wio Terminal Bootloader")
    ]
    # Target Wio Terminal device specifics
    TARGET_WIO_PATH = '/dev/ttyACM1'
    TARGET_WIO_DESC = 'Seeed Wio Terminal'

    if cli_port:
        print(f"Wio Terminal: Attempting connection to specified port: {cli_port}")
        log_activity("wio_connect_attempt_cli", {"port": cli_port})
        try:
            ser = serial.Serial(cli_port, 115200, timeout=1)
            print(f"Wio Terminal: Successfully connected on specified port {cli_port}.")
            log_activity("wio_connect_success_cli", {"port": cli_port})
            return ser
        except serial.SerialException as e:
            print(f"Wio Terminal Error: Could not connect on specified port {cli_port}: {e}")
            log_activity("wio_connect_error_cli", {"port": cli_port, "error": str(e)})

    print(f"Wio Terminal: Searching for device (Target: {TARGET_WIO_PATH} - '{TARGET_WIO_DESC}')...")
    log_activity("wio_connect_autodetect_start", {"target_path": TARGET_WIO_PATH, "target_desc": TARGET_WIO_DESC})
    auto_detected_port = find_specific_device_port(
        "Wio Terminal", 
        wio_keywords, 
        wio_vid_pids, 
        target_device_path=TARGET_WIO_PATH, 
        target_description=TARGET_WIO_DESC
    )

    if auto_detected_port:
        try:
            print(f"Wio Terminal: Attempting connection to auto-detected/targeted port: {auto_detected_port}")
            ser = serial.Serial(auto_detected_port, 115200, timeout=1)
            print(f"Wio Terminal: Successfully connected on {auto_detected_port}.")
            return ser
        except serial.SerialException as e:
            print(f"Wio Terminal Error: Could not connect on auto-detected/targeted port {auto_detected_port}: {e}")

    print("Wio Terminal: Failed to establish connection. No manual port selection prompt in this mode.")
    log_activity("wio_connect_failed_all_attempts", {})
    return None

# NEW function to handle only Meshtastic sending
def send_data_to_meshtastic(data_lines, mesh_interface):
    if not mesh_interface:
        if DEBUG: print("Meshtastic: Interface not available. Skipping send.")
        log_activity("meshtastic_send_skipped", {"reason": "Interface not available", "num_data_lines": len(data_lines) if data_lines else 0})
        return

    if not data_lines:
        if DEBUG: print("Meshtastic: No data lines to send.")
        log_activity("meshtastic_send_skipped", {"reason": "No data lines provided"})
        return

    log_activity("meshtastic_send_batch_start", {"num_data_lines": len(data_lines)})
    label_map = {
        "RPI_TIMESTAMP": "Timestamp", # MODIFIED: Use RPI_TIMESTAMP
        "TEMP": "Temperature", "HUMIDITY": "Humidity",
        "PRESSURE": "Pressure", "UV": "UV Intensity", "NO2": "NO2",
        "C2H5OH": "C2H5OH", "VOC": "VOC", "CO": "CO", "CPM": "CPM",
        "USVH": "Radiation (uSv/h)"
    }

    for line in data_lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value_and_unit = parts[1].strip()
            label = label_map.get(key, key)
            message = f"{label}: {value_and_unit}"
            try:
                if DEBUG: print(f"Meshtastic: Sending to channel 1: {message}")
                mesh_interface.sendText(message, channelIndex=1)
                log_activity("meshtastic_send_text_success", {"message": message, "channel_index_attempted": 1, "node_id": mesh_interface.myInfo.my_node_num if hasattr(mesh_interface, 'myInfo') else 'Unknown'})
                time.sleep(0.5) # Keep a small delay between messages
            except Exception as e:
                print(f"Meshtastic: Error sending message '{message}': {e}")
                log_activity("meshtastic_send_text_error", {"message": message, "error": str(e)})
        else:
            if DEBUG: print(f"Meshtastic Parser: Could not parse line for Meshtastic: {line}")
            log_activity("meshtastic_parse_line_error", {"line": line})
    log_activity("meshtastic_send_batch_complete", {})

# NEW function to handle only MQTT publishing
def publish_data_to_mqtt(data_lines, mqtt_client_instance):
    global mqtt_connected # Needs to know if client is connected

    if not mqtt_client_instance:
        if DEBUG: print("MQTT: Client not initialized. Skipping publish.")
        log_activity("mqtt_publish_skipped", {"reason": "Client not initialized", "num_data_lines": len(data_lines) if data_lines else 0})
        return
    
    if not mqtt_connected:
        if DEBUG: print("MQTT: Client not connected. Skipping publish.")
        log_activity("mqtt_publish_skipped", {"reason": "Client not connected", "num_data_lines": len(data_lines) if data_lines else 0})
        return

    if not data_lines:
        if DEBUG: print("MQTT: No data lines to publish.")
        log_activity("mqtt_publish_skipped", {"reason": "No data lines provided"})
        return

    mqtt_payload = {}
    for line in data_lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip().lower() # Ensure lowercase keys for MQTT
            value_and_unit = parts[1].strip()
            value_str = value_and_unit.split(' ')[0]
            try:
                if '.' in value_str:
                    mqtt_payload[key] = float(value_str)
                else:
                    mqtt_payload[key] = int(value_str)
            except ValueError:
                if key == "rpi_timestamp": # MODIFIED: Check for rpi_timestamp for MQTT
                    mqtt_payload[key] = value_and_unit
                else: # Other non-numeric values
                    mqtt_payload[key] = value_and_unit # Store as is
        else:
            if DEBUG: print(f"MQTT Parser: Could not parse line for MQTT: {line}")
            log_activity("mqtt_parse_line_error", {"line": line})

    if mqtt_payload:
        try:
            json_payload = json.dumps(mqtt_payload)
            if DEBUG: print(f"MQTT: Publishing to {MQTT_TOPIC}: {json_payload}")
            result = mqtt_client_instance.publish(MQTT_TOPIC, json_payload, qos=1)
            log_activity("mqtt_publish_attempt", {"topic": MQTT_TOPIC, "payload_keys": list(mqtt_payload.keys()), "qos": 1})
            result.wait_for_publish(timeout=5) # Wait for publish confirmation
            if result.rc == paho.MQTT_ERR_SUCCESS:
                 if DEBUG: print(f"MQTT: Successfully published message mid {result.mid}")
                 # on_publish callback will also log MQTT_ERR_SUCCESS
            else:
                print(f"MQTT: Failed to publish message. Result code: {result.rc}")
                log_activity("mqtt_publish_failed_after_wait", {"topic": MQTT_TOPIC, "result_code": result.rc, "message_id": result.mid})
        except Exception as e:
            print(f"MQTT: Error publishing message: {e}")
            log_activity("mqtt_publish_exception", {"topic": MQTT_TOPIC, "error": str(e), "traceback": traceback.format_exc() if DEBUG else "Set DEBUG for traceback"})
    else:
        if DEBUG: print("MQTT: Payload was empty after parsing. Nothing to publish.")
        log_activity("mqtt_publish_skipped", {"reason": "Empty payload after parsing", "num_data_lines": len(data_lines)})

def main():
    global mqtt_client, LOG_FILE, LOG_FILENAME
    global last_meshtastic_sent_time, last_mqtt_sent_time, latest_complete_data_block
    global last_wio_data_block_update_time, last_wio_raw_print_time
    global currently_printing_raw_block # ADDED: Make new flag global

    parser = argparse.ArgumentParser(description="Reads sensor data from Wio Terminal, broadcasts via Meshtastic, and publishes to MQTT.")
    parser.add_argument('--wio_port', help='Specify the Wio Terminal serial port (e.g., COM3 or /dev/ttyACM1)')
    parser.add_argument('--mesh_port', help='Specify the Meshtastic device serial port (e.g., COM4 or /dev/ttyACM0)')
    args = parser.parse_args()

    # --- Log File Setup ---
    log_dir = "logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}")
        except OSError as e:
            print(f"[ERROR] Could not create log directory '{log_dir}': {e}. Logging disabled.")
            # Not returning, as the app might still function, just without file logging.
    
    if os.path.exists(log_dir): # Proceed only if log_dir exists or was created
        LOG_FILENAME = os.path.join(log_dir, f"wio_meshtastic_bridge_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jsonl")
        try:
            LOG_FILE = open(LOG_FILENAME, "a", encoding="utf-8")
            print(f"Logging activity to: {LOG_FILENAME}")
            log_activity("script_start", {"args": vars(args), "debug_mode": DEBUG})
        except IOError as e:
            print(f"[ERROR] Could not open log file '{LOG_FILENAME}': {e}. File logging disabled.")
            LOG_FILE = None # Ensure LOG_FILE is None if open failed
    # --- End Log File Setup ---

    # Enhanced connection logic
    wio_ser = connect_wio_terminal(args.wio_port)
    wio_connected_port = None # Initialize here
    if not wio_ser:
        print("Wio Terminal connection failed. Please check the device and suggestions above. Exiting.")
        return
    else:
        wio_connected_port = wio_ser.port # Get port if connection successful

    meshtastic_interface = connect_meshtastic(args.mesh_port, wio_port=wio_connected_port) # Pass wio_connected_port
    if not meshtastic_interface:
        print("Meshtastic device connection failed. The script will not be able to send Meshtastic messages.")
        # Decide if you want to exit or continue without Meshtastic
        # For now, we allow it to continue if Wio is connected, to allow MQTT publishing.
        # If Meshtastic is critical, uncomment: 
        # if wio_ser: wio_ser.close()
        # return 
    else:
        # Configure Meshtastic SECONDARY channel (index 1)
        try:
            print("Meshtastic: Configuring SECONDARY channel 'Environ' (index 1)...")
            log_activity("meshtastic_channel_config_start", {"channel_name": "Environ", "channel_index": 1, "role": "SECONDARY"})
            
            local_node = None
            max_retries = 5
            retry_delay = 2 # seconds
            for attempt in range(max_retries):
                local_node = meshtastic_interface.getNode('^local')
                if local_node and hasattr(local_node, 'localConfig') and \
                   hasattr(local_node.localConfig, 'channels') and \
                   local_node.localConfig.channels is not None:
                    if DEBUG: print(f"Meshtastic: Successfully fetched local_node with channel config on attempt {attempt + 1}.")
                    break
                if DEBUG: print(f"Meshtastic: Attempt {attempt + 1}/{max_retries} to get local_node config failed. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            
            # Check if local_node and its necessary attributes are populated after retries
            if not (local_node and hasattr(local_node, 'localConfig') and \
               hasattr(local_node.localConfig, 'channels') and local_node.localConfig.channels is not None):
                print("Meshtastic Error: Could not get local node or its channel configuration after multiple retries.")
                log_activity("meshtastic_channel_config_error", {"reason": "Failed to get local_node or channels attribute after retries"})
                # Depending on criticality, you might choose to raise an exception or continue without channel config
                # For now, we'll print an error and proceed, messages will go to primary channel or fail.
                # raise Exception("Failed to access node channels configuration after retries.") 
            else:
                # Proceed with channel configuration if data is available
                if len(local_node.localConfig.channels) < 2:
                    print("Meshtastic Error: Device does not have channel at index 1 available for configuration.")
                    print("  You might need to add/enable it first using Meshtastic CLI or another client.")
                    log_activity("meshtastic_channel_config_error", {"reason": "Channel index 1 not available", "num_channels": len(local_node.localConfig.channels)})
                else:
                    environ_channel_obj = local_node.localConfig.channels[1]
                    environ_channel_settings = environ_channel_obj.settings
                    
                    environ_channel_obj.role = meshtastic.Channel.Role.SECONDARY
                    environ_channel_settings.name = "Environ"
                    
                    # Default PSK "AQ==" (public)
                    # If you want to set a custom PSK, replace "AQ==" with your base64 encoded PSK
                    # For example, for a PSK of b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
                    # psk_b64 = base64.b64encode(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10').decode('ascii')
                    psk_b64 = "AQ==" 
                    psk_bytes = base64.b64decode(psk_b64)
                    environ_channel_settings.psk = psk_bytes
                    
                    local_node.writeConfig("channels") 
                    
                    print("Meshtastic: SECONDARY Channel 'Environ' (index 1) configuration applied.")
                    log_activity("meshtastic_channel_config_success", {"channel_name": "Environ", "channel_index": 1, "role": "SECONDARY"})

        except Exception as e:
            print(f"Meshtastic Error: Failed to configure SECONDARY 'Environ' channel (index 1): {e}")
            # Ensure traceback is available for logging if DEBUG is true
            tb_str = traceback.format_exc() if DEBUG else "Set DEBUG for traceback"
            log_activity("meshtastic_channel_config_exception", {"channel_name": "Environ", "channel_index": 1, "error": str(e), "traceback": tb_str})
            if DEBUG: traceback.print_exc()

    mqtt_client = setup_mqtt_client()
    if mqtt_client:
        print("MQTT: Client setup initiated. Waiting for connection status...")
        time.sleep(3) # Give MQTT time to connect
        if not mqtt_connected:
            print("MQTT: Warning - Client connected to broker but connection callback not confirmed or failed. Check broker status and credentials.")
    else:
        print("MQTT: Client setup failed. MQTT publishing will be disabled.")

    print("\nApplication Main Loop: Listening for data from Wio Terminal...")
    if not meshtastic_interface: print(" (Meshtastic functionality disabled due to connection failure)")
    if not mqtt_client or not mqtt_connected: print(" (MQTT publishing disabled or connection issue)")
    
    current_data_block = []
    in_data_block = False
    last_meshtastic_sent_time = time.time() # Initialize timers
    last_mqtt_sent_time = time.time()
    last_wio_data_block_update_time = time.time() # ADDED: Initialize Wio update timer
    last_wio_raw_print_time = time.time() # ADDED: Initialize Wio Raw print timer
    currently_printing_raw_block = False # ADDED: Flag to control raw printing for an entire block

    try:
        while True:
            current_time_for_timers = time.time() # Fetch current time once for all timer checks in this iteration

            if wio_ser.in_waiting > 0:
                try:
                    line = wio_ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        # Raw printing decision is now per-block, flag set on START_DATA
                        # The actual printing of raw lines happens after START_DATA logic
                        
                        if line == "START_DATA":
                            # Add RPi system timestamp when a new data block starts
                            current_data_block = [f"RPI_TIMESTAMP:{datetime.datetime.now().isoformat()}"]
                            in_data_block = True
                            # if DEBUG: print("Wio: START_DATA detected.") # MOVED: Now conditional below
                            log_activity("wio_data_event", {"event": "START_DATA"})

                            # Decide if this entire block should be printed raw
                            if current_time_for_timers - last_wio_raw_print_time >= 60:
                                currently_printing_raw_block = True
                                last_wio_raw_print_time = current_time_for_timers # Reset timer
                                if DEBUG: # ADDED: Condition for these prints
                                    print("Wio: START_DATA detected.")
                                    print(f"Wio Raw (Block Start): {line}") 
                            else:
                                currently_printing_raw_block = False
                        
                        elif line == "END_DATA":
                            # if DEBUG and currently_printing_raw_block: # MOVED: END_DATA raw print below
                            #     print(f"Wio Raw (Block End): {line}")
                            
                            if in_data_block:
                                # if DEBUG: print("Wio: END_DATA detected.") # MOVED: Now conditional below
                                
                                # Wio data block update logic (remains the same, uses its own timer)
                                # Its specific DEBUG prints are about storage, not raw Wio reception, so they stay.
                                if current_time_for_timers - last_wio_data_block_update_time >= 60:
                                    if current_data_block:
                                        latest_complete_data_block = list(current_data_block)
                                        last_wio_data_block_update_time = current_time_for_timers 
                                        if DEBUG and currently_printing_raw_block: # MODIFIED: Add currently_printing_raw_block condition
                                            print(f"Wio (Storage): Stored new data block ({len(latest_complete_data_block)} lines) from Wio. Storage interval timer reset.")
                                        log_activity("wio_data_block_updated", {"block_size": len(latest_complete_data_block)})
                                    else:
                                        if DEBUG and currently_printing_raw_block: # MODIFIED: Add currently_printing_raw_block condition
                                            print("Wio (Storage): END_DATA, 60s storage interval met, but current Wio block was empty.")
                                        log_activity("wio_data_event", {"event": "END_DATA_EMPTY_BLOCK_ON_STORAGE_INTERVAL"})
                                else:
                                    if DEBUG and currently_printing_raw_block: # MODIFIED: Add currently_printing_raw_block condition
                                        print(f"Wio (Storage): END_DATA, but <60s since last Wio data storage. New Wio data ignored for storage. Time since last: {current_time_for_timers - last_wio_data_block_update_time:.2f}s")
                                    log_activity("wio_data_block_ignored_storage_interval", {"current_block_size": len(current_data_block) if current_data_block else 0, "time_since_last_storage": current_time_for_timers - last_wio_data_block_update_time})
                                
                                # Print END_DATA related messages only if the block was designated for raw printing
                                if DEBUG and currently_printing_raw_block:
                                    print(f"Wio Raw (Block End): {line}") # Print END_DATA raw
                                    print("Wio: END_DATA detected.")      # Print END_DATA event notification

                                current_data_block = [] 
                                in_data_block = False
                                # currently_printing_raw_block flag persists until next START_DATA makes a new decision
                            else:
                                print("Warning: END_DATA received without START_DATA.")
                                log_activity("wio_data_warning", {"warning": "END_DATA without START_DATA"})
                        
                        elif in_data_block: # This is a data line within a block
                            if line.startswith("TIMESTAMP:"):
                                if DEBUG and currently_printing_raw_block: # Still log if we are raw printing the block
                                    print(f"Wio Raw (Ignored Wio Timestamp): {line}")
                                log_activity("wio_data_event", {"event": "IGNORED_WIO_TIMESTAMP", "line": line})
                                # Skip appending this line
                            else:
                                current_data_block.append(line)
                                if DEBUG and currently_printing_raw_block: # Print other data lines raw if block was chosen
                                    if len(line) < 150: print(f"Wio Raw: {line}")
                                    else: print(f"Wio Raw: (line too long to print, len={len(line)})")
                except UnicodeDecodeError:
                    print("Warning: Could not decode line from Wio Terminal (not UTF-8). Ensure Wio sketch sends UTF-8.")
                    log_activity("wio_decode_error", {"error": "UnicodeDecodeError"})
                except serial.SerialException as e:
                    print(f"Serial error reading from Wio Terminal: {e}. Attempting to reconnect...")
                    log_activity("wio_serial_exception", {"error": str(e), "action": "Attempting reconnect"})
                    if wio_ser: wio_ser.close()
                    time.sleep(5)
                    # Preserve original CLI arg or last known port for reconnect attempt
                    reconnect_port_arg = args.wio_port if args.wio_port else (wio_ser.port if wio_ser and hasattr(wio_ser, 'port') else None)
                    wio_ser = connect_wio_terminal(reconnect_port_arg)
                    if not wio_ser:
                        print("Failed to reconnect Wio Terminal. Exiting program.")
                        log_activity("wio_reconnect_failed", {"port_arg_tried": reconnect_port_arg})
                        break # Exit main while loop
                    else:
                        print("Successfully reconnected to Wio Terminal.")
                        log_activity("wio_reconnect_success", {"port": wio_ser.port})
            
            # Meshtastic timed sending logic (5 minutes = 300 seconds)
            if current_time_for_timers - last_meshtastic_sent_time >= 300:
                if latest_complete_data_block:
                    if DEBUG: print(f"Timer (Meshtastic): 5min interval reached. Sending latest captured data block ({len(latest_complete_data_block)} lines).")
                    log_activity("meshtastic_timed_send_triggered", {"data_block_size": len(latest_complete_data_block)})
                    send_data_to_meshtastic(latest_complete_data_block, meshtastic_interface)
                    # We don't clear latest_complete_data_block here, MQTT might need it
                elif DEBUG:
                    print("Timer (Meshtastic): 5min interval reached, but no complete data block from Wio to send.")
                    log_activity("meshtastic_timed_send_skipped_no_data", {})
                last_meshtastic_sent_time = current_time_for_timers

            # MQTT timed sending logic (2.5 minutes = 150 seconds)
            if current_time_for_timers - last_mqtt_sent_time >= 150:
                if latest_complete_data_block:
                    if DEBUG: print(f"Timer (MQTT): 2.5min interval reached. Publishing latest captured data block ({len(latest_complete_data_block)} lines).")
                    log_activity("mqtt_timed_publish_triggered", {"data_block_size": len(latest_complete_data_block)})
                    publish_data_to_mqtt(latest_complete_data_block, mqtt_client)
                elif DEBUG:
                    print("Timer (MQTT): 2.5min interval reached, but no complete data block from Wio to publish.")
                    log_activity("mqtt_timed_publish_skipped_no_data", {})
                last_mqtt_sent_time = current_time_for_timers
            
            time.sleep(0.1) # Retain sleep to prevent busy-waiting

    except KeyboardInterrupt:
        print("\nExiting program (Keyboard Interrupt)...")
        log_activity("script_shutdown_interrupt", {"reason": "KeyboardInterrupt"})
    except Exception as e:
        print(f"[FATAL] Unhandled exception in main loop: {e}")
        # Ensure traceback is available for logging if DEBUG is true
        tb_str = traceback.format_exc() if DEBUG else "Set DEBUG for traceback"
        log_activity("script_fatal_exception", {"error": str(e), "traceback": tb_str})
        if DEBUG: traceback.print_exc()
    finally:
        print("Cleaning up resources...")
        log_activity("script_shutdown", {"reason": "Normal exit or unhandled exception in main try block"})
        if wio_ser and wio_ser.is_open:
            wio_ser.close()
            print("Wio Terminal serial port closed.")
            log_activity("wio_serial_closed", {"port": wio_ser.port if hasattr(wio_ser, 'port') else 'N/A'})
        if meshtastic_interface:
            meshtastic_interface.close()
            print("Meshtastic interface closed.")
            # Assuming meshtastic_interface has a port attribute or similar if needed for logging
            log_activity("meshtastic_closed", {"details": "Interface closed"})
        
        if mqtt_client:
            if DEBUG: print("MQTT: Disconnecting client...")
            # Ensure traceback is available for logging if DEBUG is true, though less likely needed here
            tb_str_mqtt_disconnect = traceback.format_exc() if DEBUG else "Set DEBUG for traceback"
            log_activity("mqtt_disconnect_start", {"client_id": mqtt_client._client_id.decode() if mqtt_client._client_id else "Unknown"})
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
            if DEBUG: print("MQTT: Client disconnected.")
            log_activity("mqtt_disconnected", {"client_id": mqtt_client._client_id.decode() if mqtt_client._client_id else "Unknown"})

        if LOG_FILE:
            print(f"Closing log file: {LOG_FILENAME}")
            LOG_FILE.close()
            LOG_FILE = None # Set to None after closing

        print("Cleanup complete. Application finished.")

if __name__ == "__main__":
    main() 