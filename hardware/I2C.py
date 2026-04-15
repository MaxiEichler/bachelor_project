# This code will do I2C communication using the smbus library in Python.
# This is needed to interface the I2C Expander to expand the IO of the Raspberry Pi.
# The expander will only switch mosfets and switches between data and power traces.

from smbus2 import SMBus
import time

bus = SMBus(1)
Device_Bus = 1  
Device_Address_U300 = 0x20 #0b00100000 # I2C address of expander U300

# MCP23017 Registe Addresses Table 3-1 
address_map = {
    "IODIRA": 0x00,     "IODIRB": 0x01,     "IPOLA": 0x02,      "IPOLB": 0x03,
    "GPINTENA": 0x04,   "GPINTENB": 0x05,   "DEFVALA": 0x06,    "DEFVALB": 0x07,
    "INTCONA": 0x08,    "INTCONB": 0x09,    "IOCON": 0x0A,      "IOCON": 0x0B,
    "GPPUA": 0x0C,      "GPPUB": 0x0D,      "INTFA": 0x0E,      "INTFB": 0x0F,
    "INTCAPA": 0x10,    "INTCAPB": 0x11,    "GPIOA": 0x12,      "GPIOB": 0x13,
    "OLATA": 0x14,      "OLATB": 0x15
}

# This mapping is used to determine which bit corresponds to which BB data mode
BB_data_map = {
    1: 0, 2: 2, 3: 4, 4: 6,
    5: 0, 6: 2, 7: 4, 8: 6,
    9: 0, 10: 2, 11: 4, 12: 6,
    13: 0, 14: 2, 15: 4, 16: 6
}

# This mapping is used to determine which bit corresponds to which BB power mode
BB_power_map = {
    1: 1, 2: 3, 3: 5, 4: 7,
    5: 1, 6: 3, 7: 5, 8: 7,
    9: 1, 10: 3, 11: 5, 12: 7, 
    13: 1, 14: 3, 15: 5, 16: 7
}   

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

# Initialize I2C bus and configure expanders
def init_I2C():
    # Set all pins of expander as outputs and set IOCON to BANK 0 for easier addressing
    bus.write_byte_data(Device_Address_U300, address_map["IOCON"], 0x00)  # Set IOCON to BANK 0
    bus.write_byte_data(Device_Address_U300, address_map["IODIRA"], 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U300, address_map["IODIRB"], 0x00) # Set all pins of port B as output
    print("I2C initialized and expanders configured as outputs")
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////

def switch_expander(BB, mode):
    # BB: 1-16
    # mode: "data" or "power"

    #print("BB: ", BB, "mode: ", mode)

    # Determine which register and local pin to modify based on BB and mode
    if BB < 9:
        reg_name = "GPIOA"
        local_pin = BB - 1 
    else:        
        reg_name = "GPIOB"
        local_pin = BB - 9

    reg_addr = address_map[reg_name]

    # Determine the state to set based on mode
    if mode == "data":
        state = 0
    elif mode == "power":
        state = 1

    # Read - Modify - Write
    try:
        # Read the current value of the register
        old_value = bus.read_byte_data(Device_Address_U300, reg_addr)
        
        # Modify the specific bit for the BB and mode
        if state == 1:
            new_value = old_value | (1 << local_pin)
        else:
            new_value = old_value & ~(1 << local_pin)

        # Write the new value back to the expander
        bus.write_byte_data(Device_Address_U300, reg_addr, new_value)
        #print(f"BB{BB} [{mode}] set to {state} on {hex(Device_Address_U300)} {reg_name} (Val: {bin(new_value)})")
        
    except Exception as e:
        print(f"I2C Error: {e}")