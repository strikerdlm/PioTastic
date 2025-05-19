import meshtastic
import meshtastic.serial_interface
import time
import serial.tools.list_ports
from pubsub import pub
import os
import traceback
import datetime
import json
from math import radians, cos, sin, asin, sqrt

# --- Global Settings ---
DEBUG = False # Set to True for verbose debug output to console

# --- Global Containers ---
NODE_STATS = {}          # For storing node statistics and messages
LOG_FILE = None          # For the log file object
USER_MAP = {             # Moved USER_MAP here for clarity with other globals
    '!938bed48': 'HOME',
    '!5919307a': 'BadBite',
    '!3b6d61f7': 'Byte_61f7', # Added new user
    '!072031ef': 'Byte_31ef',   # Added another new user
    # Add more mappings as needed
}

class BytesEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts bytes to hex strings."""
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()  # Convert bytes to hex string
        try:
            # First attempt to convert to a dict
            return obj.__dict__
        except AttributeError:
            try:
                # Try to convert to a string if it has a string representation
                return str(obj)
            except:
                pass
        return super().default(obj)

ASCII_TITLE = r"""
  ____    _    ____  ____ ___ ____   ____   ___  __  __
 | __ )  / \  |  _ \| __ )_ _| __ ) / ___| / _ \|  \/  |
 |  _ \ / _ \ | | | |  _ \ | |  _ \ \___ \| | | | |\/| |
 | |_) / ___ \| |_| | |_) || | |_) | ___) | |_| | |  | |
 |____/_/   \_\____/|____/___|____(_)____/ \___/|_|  |_|
              BadBite COM (Silent Logger Mode)
"""

def clear_console(): # This will still work if needed for initial setup
    os.system('cls' if os.name == 'nt' else 'clear')

# Renamed try_connect_meshtastic_device to avoid conflict if this script is imported
# This internal version is used by find_and_select_meshtastic_port
def try_connect_meshtastic_device_internal(port_path):
    """Internal helper to connect to a Meshtastic device on a specific port."""
    if DEBUG: print(f"[try_connect_internal] Attempting Meshtastic connection on port: {port_path}...")
    iface = None
    try:
        if DEBUG: print(f"[try_connect_internal] PRE-INIT: Instantiating SerialInterface for {port_path}")
        iface = meshtastic.serial_interface.SerialInterface(
            devPath=port_path, debugOut=False, noProto=False, connectNow=True)
        if DEBUG: print(f"[try_connect_internal] POST-INIT: SerialInterface for {port_path}. Waiting for info...")
        time.sleep(1.5) # Reduced from 3s
        if DEBUG: print(f"[try_connect_internal] POST-SLEEP: Done waiting for {port_path}.")

        if iface and hasattr(iface, 'myInfo') and iface.myInfo is not None:
            if DEBUG: print(f"[try_connect_internal] SUCCESS: myInfo for {port_path}.")
            return iface
        else:
            status = "myInfo not available" if (iface and hasattr(iface, 'myInfo')) else "interface issue/myInfo missing"
            if not iface: status = "interface object is None"
            if DEBUG: print(f"[try_connect_internal] FAILED_INFO: {port_path} partial. {status}.")
            if iface: iface.close()
            return None
    except meshtastic.util.WaitForConnectionError:
        if DEBUG: print(f"[try_connect_internal] Meshtastic WaitForConnectionError on {port_path}: Device busy/unresponsive.")
    except meshtastic.MeshtasticError as e:
        if DEBUG: print(f"[try_connect_internal] MeshtasticError on {port_path}: {e}")
    except serial.serialutil.SerialException as e:
        if DEBUG: print(f"[try_connect_internal] SerialException on {port_path}: {e}.")
    except Exception as e:
        if DEBUG: print(f"[try_connect_internal] Unexpected error on {port_path}: {e}"); traceback.print_exc()
    
    if iface: # Ensure closure if an exception occurred mid-process
        if DEBUG: print(f"[try_connect_internal] Closing interface for {port_path} due to exception.")
        try: iface.close()
        except: pass # Ignore errors during close in exception handler
    return None

def find_and_select_meshtastic_port(cli_port=None):
    """Attempts to find and select the Meshtastic port through multiple stages."""
    print("\nMeshtastic Device Detection:")
    iface = None
    connected_port_path = None
    tried_ports = set()

    # Common Meshtastic device identifiers
    meshtastic_keywords = ['CP210x', 'CH340', 'CH910', 'USB Serial', 'Meshtastic', 'ACM0', 'UART']
    meshtastic_vid_pids = [
        (0x10C4, 0xEA60, "CP210x"),
        (0x1A86, 0x7523, "CH340"),
        (0x0403, 0x6001, "FTDI"),
        (0x239A, None, "Adafruit"),
        (0x303A, None, "Espressif"),
        (0x1A86, 0x55D4, "USB Single Serial") # Added specific target Meshtastic device VID/PID
    ]

    # Stage 1: Try CLI specified port
    if cli_port:
        print(f"  Stage 1: Trying specified port: {cli_port}")
        iface = try_connect_meshtastic_device_internal(cli_port)
        tried_ports.add(cli_port)
        if iface:
            connected_port_path = cli_port
            return iface, connected_port_path
        print(f"    Failed on specified port {cli_port}.")

    # Stage 2: Try auto-detection using VID/PID and then keywords
    print("  Stage 2: Trying auto-detection (VID/PID & keywords)...")
    all_ports = list(serial.tools.list_ports.comports())

    # Attempt 2a: Match by VID/PID (prioritizing the specific Meshtastic device)
    if not iface:
        if DEBUG: print("    Stage 2a: Checking by VID/PID...")
        # First, look for the exact target Meshtastic: /dev/ttyACM0, VID 1A86, PID 55D4
        for port_info in all_ports:
            if port_info.device == '/dev/ttyACM0' and port_info.vid == 0x1A86 and port_info.pid == 0x55D4 and "USB Single Serial" in port_info.description:
                if port_info.device not in tried_ports:
                    print(f"    [PRIORITY] Found target Meshtastic device: {port_info.device} ({port_info.description})")
                    iface = try_connect_meshtastic_device_internal(port_info.device)
                    tried_ports.add(port_info.device)
                    if iface:
                        connected_port_path = port_info.device
                        return iface, connected_port_path
        
        # If not found, try other known Meshtastic VID/PIDs
        if not iface:
            for port_info in all_ports:
                if port_info.device in tried_ports: continue
                if port_info.vid and port_info.pid:
                    for vid, pid_match, name_check in meshtastic_vid_pids:
                        if port_info.vid == vid and (pid_match is None or port_info.pid == pid_match):
                            if name_check is None or name_check.lower() in port_info.description.lower():
                                print(f"    Trying VID/PID matched port: {port_info.device} ({port_info.description})")
                                iface = try_connect_meshtastic_device_internal(port_info.device)
                                tried_ports.add(port_info.device)
                                if iface:
                                    connected_port_path = port_info.device
                                    return iface, connected_port_path
                                break 
        if not iface and DEBUG: print("    Stage 2a: No conclusive match by VID/PID or connection failed.")

    # Attempt 2b: Match by keywords
    if not iface:
        if DEBUG: print("    Stage 2b: Checking by keywords...")
        for port_info in all_ports:
            if port_info.device in tried_ports: continue
            desc_lower = port_info.description.lower()
            mfc_lower = port_info.manufacturer.lower() if port_info.manufacturer else ""
            if any(k.lower() in desc_lower for k in meshtastic_keywords) or \
               any(k.lower() in mfc_lower for k in meshtastic_keywords):
                print(f"    Trying keyword matched port: {port_info.device} ({port_info.description})")
                iface = try_connect_meshtastic_device_internal(port_info.device)
                tried_ports.add(port_info.device)
                if iface:
                    connected_port_path = port_info.device
                    return iface, connected_port_path
        if not iface and DEBUG: print("    Stage 2b: No conclusive match by keywords or connection failed.")

    if not iface:
        print("    Auto-detection (VID/PID & keyword) failed or connection unsuccessful.")
        print("    FATAL: Could not auto-select Meshtastic device. No input prompt in non-interactive mode.")
        return None, None # No manual selection in headless mode

    # Fallback - Should ideally not be reached if auto-selection is comprehensive
    # The previous patch for manual input is removed to ensure no prompts
    # If the script reaches here, it means all auto-detection attempts failed.
    # print("  Stage 3: Fallback - Manual port selection.") -> This part is removed.

    return None, None # Explicitly return None if no device is found and connected


# --- NodeStats Class, haversine, on_receive, make_serializable (Assume these are correctly defined as in your file) ---
class NodeStats:
    """Collect metrics and compute 5-minute descriptive statistics, plus position and message history."""
    def __init__(self):
        self.records = []
        self.lat = None
        self.lon = None
        self.altitude = None
        self.temp = None
        self.last_seen = None
        self.messages = []
        self.extra_fields = {}

    def add_metrics(self, ts, metrics: dict):
        self.records.append({'ts': ts, **metrics})
        self.last_seen = ts
        cutoff = ts - datetime.timedelta(minutes=5)
        self.records = [r for r in self.records if r['ts'] >= cutoff]
        temp = metrics.get('temperature')
        if temp is not None:
            self.temp = temp

    def update_position(self, lat, lon, altitude):
        self.lat, self.lon, self.altitude = lat, lon, altitude

    def add_message(self, ts, from_id, text):
        self.messages.append((ts, from_id, text))
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]

    def set_extra_fields(self, decoded, exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = set()
        self.extra_fields = {k: v for k, v in decoded.items() if k not in exclude_keys}

    def summarize(self):
        fields = ['batteryLevel', 'voltage', 'channelUtilization', 'airUtilTx', 'uptimeSeconds']
        latest = {f: None for f in fields}
        mean = {f: None for f in fields}
        if self.records:
            latest_record = self.records[-1]
            for f in fields:
                latest[f] = latest_record.get(f)
            for f in fields:
                vals = [r.get(f) for r in self.records if r.get(f) is not None]
                if vals:
                    mean[f] = sum(vals) / len(vals)
        return latest, mean

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def on_receive(packet, interface):
    global DEBUG
    try:
        now_dt = datetime.datetime.now()
        now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
        from_id = packet.get('fromId', 'Unknown')
        portnum = packet.get('decoded', {}).get('portnum', 'Unknown')

        if DEBUG:
            # Access USER_MAP which is now guaranteed to be globally defined before this function
            user_display = USER_MAP.get(from_id, from_id) 
            print(f"[{now_str}] RX: ID={user_display}, Portnum={portnum}, Packet={packet.get('decoded')}")

        # NODE_STATS is now guaranteed to be globally defined before this function
        node_stat = NODE_STATS.setdefault(from_id, NodeStats())
        text = None
        if 'decoded' in packet and 'text' in packet['decoded']:
            text = packet['decoded']['text']
        elif 'payload' in packet:
            try:
                text = packet['payload'].decode('utf-8', errors='ignore')
            except Exception:
                text = str(packet['payload'])

        if text:
            node_stat.add_message(now_str, from_id, text)

        if portnum == 'TELEMETRY_APP' and 'telemetry' in packet['decoded']:
            metrics = packet['decoded']['telemetry'].get('deviceMetrics', {})
            node_stat.add_metrics(now_dt, metrics)
            temp = metrics.get('temperature')
            if temp is not None:
                node_stat.temp = temp

        if portnum == 'POSITION_APP' and 'position' in packet['decoded']:
            pos = packet['decoded']['position']
            lat = pos.get('latitude') or pos.get('latitudeI', 0)/1e7
            lon = pos.get('longitude') or pos.get('longitudeI', 0)/1e7
            alt = pos.get('altitude')
            node_stat.update_position(lat, lon, alt)

        if from_id == '!5919307a':
            if 'decoded' in packet:
                d = packet['decoded']
                for key_temp in ['temperature', 'temp']:
                    if key_temp in d and d[key_temp] is not None:
                        node_stat.temp = d[key_temp]
                if 'position' in d:
                    pos_badbite = d['position']
                    lat_bb = pos_badbite.get('latitude') or pos_badbite.get('latitudeI',0)/1e7
                    lon_bb = pos_badbite.get('longitude') or pos_badbite.get('longitudeI',0)/1e7
                    alt_bb = pos_badbite.get('altitude')
                    node_stat.update_position(lat_bb, lon_bb, alt_bb)
            if 'payload' in packet.get('decoded', {}):
                raw_payload = packet['decoded']['payload']
                try:
                    decoded_text = bytes.fromhex(raw_payload.hex()).decode('utf-8', errors='ignore')
                except Exception:
                    decoded_text = None
                if decoded_text:
                    node_stat.add_message(now_str, from_id, f"[PayloadDecoded] {decoded_text}")

        if 'decoded' in packet:
            exclude_keys = {'text', 'payload', 'portnum', 'position', 'telemetry'}
            node_stat.set_extra_fields(packet['decoded'], exclude_keys=exclude_keys)

        # LOG_FILE is globally defined
        if LOG_FILE:
            try:
                serializable_packet = make_serializable(packet)
                LOG_FILE.write(json.dumps({'ts': now_str, 'packet': serializable_packet}) + "\n")
                LOG_FILE.flush()
            except Exception as e:
                print(f"[ERROR] Log write error: {e}")
                if DEBUG:
                    traceback.print_exc()
                try:
                    LOG_FILE.write(json.dumps({'ts': now_str, 'packet_from': from_id, 'packet_type': portnum, 'error': 'serialization_failed'}) + "\n")
                    LOG_FILE.flush()
                except Exception as log_fallback_e:
                    print(f"[ERROR] Log fallback write error: {log_fallback_e}")

    except Exception as e:
        print(f"[ERROR] Unhandled exception in on_receive: {e}")
        if DEBUG:
            print(f"Raw packet causing error: {packet}")
            traceback.print_exc()

def connect_and_listen(cli_port_arg=None): # Renamed from the previous `connect_and_listen`
    interface = None
    connected_port = None # Store the successfully connected port path

    clear_console()
    print(ASCII_TITLE)

    # Call the new function to find and connect to the Meshtastic port
    interface, connected_port = find_and_select_meshtastic_port(cli_port_arg)

    if not interface:
        print("\n---------------------------------------------------------------------")
        print("FATAL: Could not connect to any Meshtastic device after all attempts.")
        print("Please ensure your Meshtastic device is properly connected via USB,")
        print("drivers are installed, and the device is powered on.")
        print("If the device is listed but fails to connect, try resetting the device.")
        print("---------------------------------------------------------------------")
        return

    print(f"\nSuccessfully connected to Meshtastic Node ID: {interface.myInfo.my_node_num} on port {connected_port}")

    global LOG_FILE
    log_dir = "logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as e:
            print(f"[ERROR] Could not create log directory '{log_dir}': {e}")
            if interface: interface.close()
            return

    log_name = os.path.join(log_dir, f"meshtastic_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jsonl")

    try:
        LOG_FILE = open(log_name, "a", encoding="utf-8")
    except IOError as e:
        print(f"[ERROR] Could not open log file '{log_name}': {e}")
        if interface: interface.close()
        return

    pub.subscribe(on_receive, "meshtastic.receive")

    print(f"Meshtastic listener started. Logging to: {log_name}")
    print("Application is running in silent mode. Press Ctrl+C to exit.")
    if DEBUG:
        print("DEBUG mode is ON. Verbose output will be shown for received packets.")

    try:
        while True:
            time.sleep(1)
            if LOG_FILE:
                LOG_FILE.flush()
    except KeyboardInterrupt:
        print("\nExiting program...")
    except Exception as e:
        print(f"[ERROR] Unhandled exception in main loop: {e}")
        if DEBUG:
            traceback.print_exc()
    finally:
        print("Cleaning up...")
        if interface:
            interface.close()
            print(f"Meshtastic interface on {connected_port} closed.")
        if LOG_FILE:
            LOG_FILE.close()
            print(f"Log file '{log_name}' closed.")
        print("Cleanup complete. Exiting.")

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(make_serializable(item) for item in obj)
    elif isinstance(obj, bytes):
        return obj.hex()
    elif hasattr(obj, '__dict__'):
        return make_serializable(obj.__dict__)
    else:
        try:
            return str(obj)
        except:
            return "UNSERIALIZABLE"

if __name__ == "__main__":
    connect_and_listen()