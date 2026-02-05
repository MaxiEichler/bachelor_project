# This code will do I2C communication using the smbus library in Python.
# This is needed to interface the I2C Expander to expand the IO of the Raspberry Pi.
# The expander will only switch mosfets and switches between data and power traces.

from smbus2 import SMBus
import time

Device_Bus = 1  
Device_Address_U300 = 0b01000000 # I2C address of expander U300 for BB01 - BB08
Device_Address_U301 = 0b01000010 # I2C address of expander U301 for BB09 - BB16
Device_Address_U302 = 0b01000100 # I2C address of expander U302 for BB18 - BB25
Device_Address_U303 = 0b01000110 # I2C address of expander U303 for BB26 - BB33

address_map = { # MCP23017 Registe Addresses Table 3-1 
    0x00: "IODIRA",     0x01: "IODIRB",     0x02: "IPOLA",      0x03: "IPOLB",
    0x04: "GPINTENA",   0x05: "GPINTENB",   0x06: "DEFVALA",    0x07: "DEFVALB",
    0x08: "INTCONA",    0x09: "INTCONB",    0x0A: "IOCON",      0x0B: "IOCON",
    0x0C: "GPPUA",      0x0D: "GPPUB",      0x0E: "INTFA",      0x0F: "INTFB",
    0x10: "INTCAPA",    0x11: "INTCAPB",    0x12: "GPIOA",      0x13: "GPIOB",
    0x14: "OLATA",      0x15: "OLATB"
}

# Initialize I2C bus and configure expanders
with SMBus(Device_Bus) as bus:

    # Set all pins of all expanders as outputs
    bus.write_byte_data(Device_Address_U300, address_map(IODIRA), 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U300, address_map(IODIRB), 0x00) # Set all pins of port B as output
    bus.write_byte_data(Device_Address_U301, address_map(IODIRA), 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U301, address_map(IODIRB), 0x00) # Set all pins of port B as output
    bus.write_byte_data(Device_Address_U302, address_map(IODIRA), 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U302, address_map(IODIRB), 0x00) # Set all pins of port B as output
    bus.write_byte_data(Device_Address_U303, address_map(IODIRA), 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U303, address_map(IODIRB), 0x00) # Set all pins of port B as output

def switch_expander(BB, mode, state):
    # BB: breadboard number (1-33)
    # mode: "data" or "power"
    # state: "high" or "low"

    # get expander address based on breadboard number
    match BB:
        case BB01 | BB02 | BB03 | BB04 | BB05 | BB06 | BB07 | BB08:
            expander_address = Device_Address_U300
        case BB09 | BB10 | BB11 | BB12 | BB13 | BB14 | BB15 | BB16:
            expander_address = Device_Address_U301
        case BB18 | BB19 | BB20 | BB21 | BB22 | BB23 | BB24 | BB25:
            expander_address = Device_Address_U302
        case BB26 | BB27 | BB28 | BB29 | BB30 | BB31 | BB32 | BB33:
            expander_address = Device_Address_U303

    # read current GPIO registar state
    if mode == power:
        old_value = bus.read_byte_data(expander_address, address_map[GPIOA])
    elif mode == data:
        old_value = bus.read_byte_data(expander_address, address_map[GPIOB])

    # write new GPIO registar state
    if state == high:
        # Set pin high
        new_value = old_value | (1 << BB)
    elif state == low:
        # Set pin low
        new_value = old_value & ~(1 << BB)

    # send new register value to expander
    if mode == power:
        bus.write_byte_data(expander_address, address_map[GPIOA], new_value)
    elif mode == data:
        bus.write_byte_data(expander_address, address_map[GPIOB], new_value)

