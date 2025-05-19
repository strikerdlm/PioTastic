import meshtastic
import meshtastic.serial_interface
import time
import logging

def connect_to_device():
    # Enable detailed debugging
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        print("Attempting to connect to device...")
        # Initialize with extended timeout and debug flags
        interface = meshtastic.serial_interface.SerialInterface(
            devPath='COM9',
            debugOut=True,
            connectNow=False  # Don't connect immediately
        )
        
        print("Interface created, attempting connection...")
        # Manual connect with more detailed error handling
        interface.connect()
        
        print("Connected! Requesting device info...")
        # Get basic device information
        print(f"Firmware Version: {interface.myInfo.firmware_version}")
        print(f"Node ID: {interface.myInfo.my_node_num}")
        print(f"Radio config: {interface.localConfig.lora}")
        
        # Close the connection properly
        interface.close()
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if hasattr(e, '__traceback__'):
            import traceback
            print("Detailed traceback:")
            traceback.print_tb(e.__traceback__)

if __name__ == "__main__":
    connect_to_device()

