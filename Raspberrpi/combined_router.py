import meshtastic
import meshtastic.serial_interface
import time
import logging
from pubsub import pub

def onReceive(packet, interface): # Called when a packet arrives
    print(f"Received: {packet}")

def onConnection(interface, topic=pub.AUTO_TOPIC): # Called when we (re)connect to the radio
    print(f"Connected to radio at {interface.devPath}")
    
def configure_meshtastic_router():
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        print("Attempting to configure device as router...")
        
        # Subscribe to messages
        pub.subscribe(onReceive, "meshtastic.receive")
        pub.subscribe(onConnection, "meshtastic.connection.established")
        
        # Initialize the interface with modified parameters
        interface = meshtastic.serial_interface.SerialInterface(
            devPath='COM9',
            debugOut=True,
            noProto=False,
            connectNow=True
        )
        
        print("Setting router configuration...")
        try:
            # Set device as router
            interface.localConfig.device.role = 'ROUTER'
            interface.localConfig.device.is_router = True
            
            # Configure radio settings
            interface.localConfig.lora.tx_power = 30  # Max power
            interface.localConfig.lora.hop_limit = 3   # Allow message forwarding
            
            # Enable routing features
            interface.localConfig.device.rebroadcast_mode = 'ALL'
            
            # Save changes
            print("Saving configuration...")
            interface.writeConfig()
            
            # Wait for changes to take effect
            time.sleep(5)
            
            # Verify configuration
            print("\nCurrent Configuration:")
            print(f"Role: {interface.localConfig.device.role}")
            print(f"Is Router: {interface.localConfig.device.is_router}")
            print(f"TX Power: {interface.localConfig.lora.tx_power}")
            print(f"Hop Limit: {interface.localConfig.lora.hop_limit}")
            
            # Monitor for any responses
            print("\nMonitoring for messages (30 seconds)...")
            time.sleep(30)
            
        except Exception as config_error:
            print(f"Error during configuration: {config_error}")
        
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if 'interface' in locals():
            interface.close()
        print("Configuration complete")

if __name__ == "__main__":
    configure_meshtastic_router()

