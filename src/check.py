import serial.tools.list_ports
from pymodbus.client import ModbusSerialClient
import logging
import time

# --- CONFIGURATION (MUST BE CORRECT!) ---
# 1. SERIAL CONFIG
TARGET_PORT = 'COM3'  # <<< CHANGE THIS: e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux
BAUD_RATE = 9600      # <<< CHANGE THIS: Must match your sensor's settings
METHOD = 'rtu'
TIMEOUT = 3

# 2. MODBUS CONFIG
SLAVE_UNIT = 1        # <<< CHANGE THIS: Address of your sensor (usually 1, 2, or higher)
REGISTER_ADDRESS = 40001 # <<< CHANGE THIS: The specific address you want to read (e.g., 40001 for a temperature value)
READ_COUNT = 1        # Number of registers to read

# Setup Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def check_serial_ports():
    """Lists available serial ports."""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("!!! No serial ports found. !!!")
        return False
    print("--- Available Serial Ports ---")
    for port in sorted(ports):
        print(f"  > {port.device}: {port.description}")
    print("------------------------------")
    return True

def test_modbus_rtu():
    """Connects to the port and attempts to read a register."""
    
    # 1. Check Port Availability
    if not check_serial_ports():
        return

    print(f"\n--- Starting Modbus RTU Test on {TARGET_PORT} ---")
    
    # 2. Initialize Client
    client = ModbusSerialClient(
        port=TARGET_PORT,
        baudrate=BAUD_RATE,
        method=METHOD,
        timeout=TIMEOUT,
        # Common parity settings (uncomment the one that matches your sensor)
        # parity='N', stopbits=1, bytesize=8 # Standard N-8-1
        parity='E', stopbits=1, bytesize=8 # Common E-8-1 (for many meters/PLCs)
    )

    # 3. Connect and Read
    try:
        if client.connect():
            print(f"Connection to port {TARGET_PORT} successful.")
            
            # Note: The pymodbus library handles the 4xxxx offset automatically.
            # You usually pass the register number MINUS 40001 (e.g., 0 for 40001) or the actual address.
            # Let's pass the address minus 1 (0-based indexing for the register map).
            # If your register is 40001, the address to pass is 0.
            register_to_read = REGISTER_ADDRESS - 40001 
            
            print(f"Attempting to read Holding Register at Address {REGISTER_ADDRESS} (Internal: {register_to_read})...")

            # Function Code 03: Read Holding Registers
            result = client.read_holding_registers(register_to_read, READ_COUNT, unit=SLAVE_UNIT)

            if result.isError():
                print("\n!!! MODBUS READ FAILED !!!")
                print(f"  Error Type: {result}")
                print("  Possible causes: Wrong Slave ID, Wrong Register Address, or Mismatch in Baudrate/Parity.")
            else:
                print("\n✅ MODBUS READ SUCCESSFUL! ✅")
                print(f"  Slave Unit ID: {SLAVE_UNIT}")
                print(f"  Register Value(s): {result.registers}")
                print(f"  Raw response (if available): {result}")

        else:
            print(f"!!! Failed to connect to port {TARGET_PORT}. Check if the port is correct and not in use. !!!")

    except Exception as e:
        print(f"\n!!! An unexpected error occurred: {e} !!!")

    finally:
        if client.is_connected:
            client.close()
            print("Client connection closed.")

if __name__ == "__main__":
    test_modbus_rtu()