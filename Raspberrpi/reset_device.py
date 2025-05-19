import serial
import time

def reset_device():
    try:
        # Open serial port with Meshtastic settings
        ser = serial.Serial('COM9', 115200, timeout=1)
        print(f"Successfully opened {ser.name} at 115200 baud")
        
        # Send factory reset command
        print("Sending factory reset command...")
        reset_cmd = bytes([0x94, 0xc3, 0x00, 0x00])  # Header for factory reset
        ser.write(reset_cmd)
        time.sleep(2)
        
        # Read any response
        print("Waiting for response...")
        for i in range(10):  # Try reading for 10 seconds
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Received data length: {len(response)} bytes")
                if any(32 <= b <= 126 for b in response):  # Check for printable ASCII
                    print(f"Received data ASCII: {response}")
            time.sleep(1)
            
        ser.close()
        print("\nDevice reset attempted. Please wait 30 seconds for the device to complete the reset process.")
        print("After reset, try the meshtastic --info command again.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    reset_device()

