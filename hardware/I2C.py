# This code will do I2C communication using the smbus library in Python.
# This is needed to interface the I2C Expander to expand the IO of the Raspberry Pi.
# The expander will only switch mosfets and switches between data and power traces.

from smbus2 import SMBus
import time

bus = SMBus(1)
Device_Bus = 1  
Device_Address_U300 = 0x20 #0b00100000 # I2C address of expander U300 for BB01 - BB08
Device_Address_U301 = 0x21 # I2C address of expander U301 for BB09 - BB16
Device_Address_U302 = 0x22 # I2C address of expander U302 for BB18 - BB25
Device_Address_U303 = 0x23 # I2C address of expander U303 for BB26 - BB33

address_map = { # MCP23017 Registe Addresses Table 3-1 
    "IODIRA": 0x00,     "IODIRB": 0x01,     "IPOLA": 0x02,      "IPOLB": 0x03,
    "GPINTENA": 0x04,   "GPINTENB": 0x05,   "DEFVALA": 0x06,    "DEFVALB": 0x07,
    "INTCONA": 0x08,    "INTCONB": 0x09,    "IOCON": 0x0A,      "IOCON": 0x0B,
    "GPPUA": 0x0C,      "GPPUB": 0x0D,      "INTFA": 0x0E,      "INTFB": 0x0F,
    "INTCAPA": 0x10,    "INTCAPB": 0x11,    "GPIOA": 0x12,      "GPIOB": 0x13,
    "OLATA": 0x14,      "OLATB": 0x15
}

# Initialize I2C bus and configure expanders
def init_I2C():
    #with SMBus(Device_Bus) as bus:
    # Set all pins of all expanders as outputs
    bus.write_byte_data(Device_Address_U300, address_map["IODIRA"], 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U300, address_map["IODIRB"], 0x00) # Set all pins of port B as output
    bus.write_byte_data(Device_Address_U301, address_map["IODIRA"], 0x00) # Set all pins of port A as output
    bus.write_byte_data(Device_Address_U301, address_map["IODIRB"], 0x00) # Set all pins of port B as output
    #bus.write_byte_data(Device_Address_U302, address_map["IODIRA"], 0x00) # Set all pins of port A as output
    #bus.write_byte_data(Device_Address_U302, address_map["IODIRB"], 0x00) # Set all pins of port B as output
    #bus.write_byte_data(Device_Address_U303, address_map["IODIRA"], 0x00) # Set all pins of port A as output
    #bus.write_byte_data(Device_Address_U303, address_map["IODIRB"], 0x00) # Set all pins of port B as output
    print("I2C initialized and expanders configured as outputs")

def switch_expander(BB, mode):
    # BB: breadboard number (1-33)
    # mode: "data" or "power"
    state = 1

    print("BB: ", BB, "mode: ", mode)

    # get expander address based on breadboard number
    match BB:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8:
            expander_address = Device_Address_U300
            local_pin = BB - 1
        case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16:
            expander_address = Device_Address_U301
            local_pin = BB - 9
        case 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25:
            expander_address = Device_Address_U302
            local_pin = BB - 18
        case 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33:
            expander_address = Device_Address_U303
            local_pin = BB - 26

    # read current GPIO registar state
    if mode == "power":
        old_value = bus.read_byte_data(expander_address, address_map["GPIOA"])
    elif mode == "data":
        old_value = bus.read_byte_data(expander_address, address_map["GPIOB"])

    # write new GPIO registar state
    if state == 1:
        # Set pin high
        new_value = old_value | (1 << BB)
    elif state == 0:
        # Set pin low
        new_value = old_value & ~(1 << BB)

    # send new register value to expander
    if mode == "power":
        bus.write_byte_data(expander_address, address_map["GPIOA"], new_value)
        print("expander address: ", expander_address, "GPIOA: ", new_value)
    elif mode == "data":
        bus.write_byte_data(expander_address, address_map["GPIOB"], new_value)
        print("expander address: ", expander_address, "GPIOB: ", new_value)

