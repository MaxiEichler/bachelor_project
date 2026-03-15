# This code will handle the ASA (Analogue Swich Array) hardware component.
import time
from datetime import datetime
import pigpio

pi = pigpio.pi()

delay = 0.01

CLK = 11
STB_A = 17
STB_B = 18
STB_C = 19
STB_D = 20
DAT = 24
RST = 25


def log(message):
    print(f"{datetime.now().strftime('%M:%S.%f')[:-3]} - {message}")

def init_GPIO():
    pi.set_mode(CLK, pigpio.OUTPUT)
    pi.set_mode(STB_A, pigpio.OUTPUT)
    pi.set_mode(STB_B, pigpio.OUTPUT)
    pi.set_mode(STB_C, pigpio.OUTPUT)
    pi.set_mode(STB_D, pigpio.OUTPUT)
    pi.set_mode(DAT, pigpio.OUTPUT)
    pi.set_mode(RST, pigpio.OUTPUT)

    
    log(f"Reset: 1")
    time.sleep(0.1)
    pi.write(RST, 1)
    log(f"Reset: 0")
    print("GPIO initialized")


address_map = {
    "Y0-X0": "0x00", "Y1-X0": "0x10", "Y2-X0": "0x20", "Y3-X0": "0x30", "Y4-X0": "0x40", "Y5-X0": "0x50", "Y6-X0": "0x60", "Y7-X0": "0x70",
    "Y0-X1": "0x01", "Y1-X1": "0x11", "Y2-X1": "0x21", "Y3-X1": "0x31", "Y4-X1": "0x41", "Y5-X1": "0x51", "Y6-X1": "0x61", "Y7-X1": "0x71",
    "Y0-X2": "0x02", "Y1-X2": "0x12", "Y2-X2": "0x22", "Y3-X2": "0x32", "Y4-X2": "0x42", "Y5-X2": "0x52", "Y6-X2": "0x62", "Y7-X2": "0x72",
    "Y0-X3": "0x03", "Y1-X3": "0x13", "Y2-X3": "0x23", "Y3-X3": "0x33", "Y4-X3": "0x43", "Y5-X3": "0x53", "Y6-X3": "0x63", "Y7-X3": "0x73", 
    "Y0-X4": "0x04", "Y1-X4": "0x14", "Y2-X4": "0x24", "Y3-X4": "0x34", "Y4-X4": "0x44", "Y5-X4": "0x54", "Y6-X4": "0x64", "Y7-X4": "0x74",
    "Y0-X5": "0x05", "Y1-X5": "0x15", "Y2-X5": "0x25", "Y3-X5": "0x35", "Y4-X5": "0x45", "Y5-X5": "0x55", "Y6-X5": "0x65", "Y7-X5": "0x75",
    "Y0-X6": "0x06", "Y1-X6": "0x16", "Y2-X6": "0x26", "Y3-X6": "0x36", "Y4-X6": "0x46", "Y5-X6": "0x56", "Y6-X6": "0x66", "Y7-X6": "0x76",
    "Y0-X7": "0x07", "Y1-X7": "0x17", "Y2-X7": "0x27", "Y3-X7": "0x37", "Y4-X7": "0x47", "Y5-X7": "0x57", "Y6-X7": "0x67", "Y7-X7": "0x77",
    "Y0-X8": "0x08", "Y1-X8": "0x18", "Y2-X8": "0x28", "Y3-X8": "0x38", "Y4-X8": "0x48", "Y5-X8": "0x58", "Y6-X8": "0x68", "Y7-X8": "0x78",
    "Y0-X9": "0x09", "Y1-X9": "0x19", "Y2-X9": "0x29", "Y3-X9": "0x39", "Y4-X9": "0x49", "Y5-X9": "0x59", "Y6-X9": "0x69", "Y7-X9": "0x79",
    "Y0-X10": "0x0A", "Y1-X10": "0x1A", "Y2-X10": "0x2A", "Y3-X10": "0x3A", "Y4-X10": "0x4A", "Y5-X10": "0x5A", "Y6-X10": "0x6A", "Y7-X10": "0x7A",
    "Y0-X11": "0x0B", "Y1-X11": "0x1B", "Y2-X11": "0x2B", "Y3-X11": "0x3B", "Y4-X11": "0x4B", "Y5-X11": "0x5B", "Y6-X11": "0x6B", "Y7-X11": "0x7B",
    "Y0-X12": "0x0C", "Y1-X12": "0x1C", "Y2-X12": "0x2C", "Y3-X12": "0x3C", "Y4-X12": "0x4C", "Y5-X12": "0x5C", "Y6-X12": "0x6C", "Y7-X12": "0x7C",
    "Y0-X13": "0x0D", "Y1-X13": "0x1D", "Y2-X13": "0x2D", "Y3-X13": "0x3D", "Y4-X13": "0x4D", "Y5-X13": "0x5D", "Y6-X13": "0x6D", "Y7-X13": "0x7D",
    "Y0-X14": "0x0E", "Y1-X14": "0x1E", "Y2-X14": "0x2E", "Y3-X14": "0x3E", "Y4-X14": "0x4E", "Y5-X14": "0x5E", "Y6-X14": "0x6E", "Y7-X14": "0x7E",
    "Y0-X15": "0x0F", "Y1-X15": "0x1F", "Y2-X15": "0x2F", "Y3-X15": "0x3F", "Y4-X15": "0x4F", "Y5-X15": "0x5F", "Y6-X15": "0x6F", "Y7-X15": "0x7F"
}

# This map shows which connection of ASA are free (0) or used (1)
status_map = {
    "AB_1": 0, "AB_2": 0, "AB_3": 0, "AB_4": 0,
    "AC_1": 0, "AC_2": 0, "AC_3": 0, "AC_4": 0,
    "AD_1": 0, "AD_2": 0, "AD_3": 0, "AD_4": 0,
    "BD_1": 0, "BD_2": 0, "BD_3": 0, "BD_4": 0,
    "CB_1": 0, "CB_2": 0, "CB_3": 0, "CB_4": 0,
    "CD_1": 0, "CD_2": 0, "CD_3": 0, "CD_4": 0
}

connection_map = {
    "AB_1": 0, "AB_2": 1, "AB_3": 2, "AB_4": 3,
    "AB_5": 4, "AB_6": 5, "AB_7": 6, "AB_8": 7
}

# This map connects the status_map key to the address_map index of Chip A
connection_map_chip_A = {
    "AB_1": 0, "AB_2": 1, "AB_3": 2, "AB_4": 3,
    "AB_5": 4, "AB_6": 5, "AB_7": 6, "AB_8": 7
}

# This map connects the status_map key to the address_map index of Chip B
connection_map_chip_B = {
    "AB_1": 8, "AB_2": 9, "AB_3": 10, "AB_4": 11,
    "CB_1": 0, "CB_2": 1, "CB_3": 2, "CB_4": 3,
    "BD_1": 7, "BD_2": 6, "BD_3": 15, "BD_4": 14
}

# This map connects the status_map key to the address_map index of Chip C
connection_map_chip_C = {
    "AC_1": 11, "AC_2": 10, "AC_3": 9, "AC_4": 8,
    "CB_1": 14, "CB_2": 15, "CB_3": 6, "CB_4": 7,
    "CD_1": 0, "CD_2": 1, "CD_3": 2, "CD_4": 3
}

# This map connects the status_map key to the address_map index of Chip D
connection_map_chip_D = {
    "AD_1": 0, "AD_2": 1, "AD_3": 2, "AD_4": 3,
    "BD_1": 14, "BD_2": 15, "BD_3": 6, "BD_4": 7,
    "CD_1": 8, "CD_2": 9, "CD_3": 10, "CD_4": 11
}

def set_ASA(address, state, chip):
    # address: Y0-X0
    # state: 1 or 0
    # chip: "A", "B", "C" or "D"

    #ypi.write(RST, 1)
    #time.sleep(delay)
    pi.write(RST, 0)
    time.sleep(delay)

    log(f"address: {address}")
    log(f"state: {state}")
    log(f"chip: {chip}")

    #print("statusmap at the start: ", status_map))

    # Convert hex string to integer
    value = int(address_map[address], 16)

    print("value from address_map: ", bin(value))

    value = (value << 1) | state

    print("value after shift: ", bin(value))

    # Determine strobe pin
    match chip:
        case "A":
            STB = 17
        case "B":
            STB = 18
        case "C":
            STB = 19
        case "D":
            STB = 20
        case _:
            raise ValueError("Invalid chip selected")

    # STB LOW
    pi.write(STB, 0)
    #log("STB 0")
    time.sleep(delay)

    # DAT LOW
    pi.write(DAT, 0)
    #log("DAT 0")
    time.sleep(delay)

    pi.write(CLK, 0)
    #log("CLK 0")
    time.sleep(delay)

    print("start sending data: ")
    # Send 8 address bits (MSB first)
    for _ in range(7):

        #pi.write(CLK, 0)  # SK LOW
        #log("SK 0")
        #time.sleep(delay)

        if value & 0x80:
            pi.write(DAT, 1)
            log("DAT 1")
            time.sleep(delay)
        else:
            pi.write(DAT, 0)
            log("DAT 0")
            time.sleep(delay)

        pi.write(CLK, 0)  # SK HIGH
       # log("CLK 0")
        time.sleep(delay)

        pi.write(CLK, 1)
        #log("CLK 1")
        time.sleep(delay)

        #print("value befor: ", value)
        value <<= 1
        #print("value after: ", value)

    pi.write(CLK, 0)  # SK LOW
    #log("CLK 0")
    time.sleep(delay)

    # Send state bit
    if state == 1:
        pi.write(DAT, 1)
        log("DAT 1")
        time.sleep(delay)
    else:
        pi.write(DAT, 0)
        log("DAT 0")
        time.sleep(delay)

    pi.write(STB, 0)
    #log("STB 0")
    time.sleep(delay)

    # STB HIGH
    pi.write(STB, 1)
    #log("STB 1")
    time.sleep(delay)

    # STB LOW
    pi.write(STB, 0)
    #log("STB 0")
    time.sleep(delay)

    pi.write(DAT, 0)
    #log("DAT 0")
    time.sleep(delay)
#print("statusmap at the end: ", status_map)

def reset_ASA():
    pi.write(RST, 1)
    time.sleep(delay)
    pi.write(RST, 0)
    time.sleep(delay)
    log("ASA reset complete")

def manualset():
    pi.write(RST, 1)
    time.sleep(delay)
    pi.write(RST, 0)
    time.sleep(delay)

    pi.write(STB_A, 0)
    time.sleep(delay)
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)

    # Y0 X0 = 0x00 -> 0b00000001
    #1
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #2
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #3
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #4
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #5
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #6
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    #7
    pi.write(DAT, 0)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    pi.write(CLK, 1)
    time.sleep(delay)
    pi.write(CLK, 0)
    time.sleep(delay)
    #8
    pi.write(DAT, 1)
    time.sleep(delay)
    pi.write(STB_B, 0)
    time.sleep(delay)
    pi.write(STB_B, 1)
    time.sleep(delay)
    pi.write(STB_B, 0)
    time.sleep(delay)
    pi.write(DAT, 0)
    time.sleep(delay)

    print("Manual set complete")