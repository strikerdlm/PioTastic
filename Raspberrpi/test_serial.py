import serial
import time
from serial.tools import list_ports


def find_meshtastic_port():
    """Scan serial ports and return the port for a LilyGO/Meshtastic device if found."""
    ports = list(list_ports.comports())
    print("Available serial ports:")
    for p in ports:
        print(f"  {p.device}: {p.description} [{p.manufacturer}]")
    for p in ports:
        desc = (p.description or '').lower()
        manu = (p.manufacturer or '').lower()
        if 'lilygo' in desc or 'meshtastic' in desc or 'lilygo' in manu or 'meshtastic' in manu:
            print(f"Found Meshtastic device on {p.device}")
            return p.device
    # Fallback: try to find a CP210x or CH9102 device (common for Meshtastic)
    for p in ports:
        desc = (p.description or '').lower()
        if 'cp210' in desc or 'ch910' in desc:
            print(f"Found likely Meshtastic device (CP210x/CH910x) on {p.device}")
            return p.device
    print("No Meshtastic/LilyGO device found. Please check your connection.")
    return None

def test_serial_connection():
    port = find_meshtastic_port()
    if not port:
        print("ERROR: Could not find a Meshtastic/LilyGO device to connect to.")
        return
    try:
        # Use standard Meshtastic baud rate
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Successfully opened {ser.name} at 115200 baud")
        print(f"Port settings: {ser.get_settings()}")
        
        # Send a carriage return to trigger any response
        print("Sending carriage return...")
        ser.write(b'\r\n')
        time.sleep(1)
        
        # Try to read any response
        print("Attempting to read response...")
        for i in range(5):  # Try reading a few times
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Received data length: {len(response)} bytes")
                print(f"Received data hex: {response.hex()}")
                if any(32 <= b <= 126 for b in response):  # Check for printable ASCII
                    print(f"Received data ASCII: {response}")
            else:
                print(f"No data available (attempt {i+1}/5)")
            time.sleep(1)
            
        ser.close()
        print("Port closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_serial_connection()

