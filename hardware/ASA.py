# This code will handle the ASA (Analogue Swich Array) hardware component.
import time
from datetime import datetime
import pigpio

pi = pigpio.pi()

delay = 0.01

CLK = 22
STB_A = 4
STB_B = 0
DAT = 27
RST = 17

def log(message):
    print(f"{datetime.now().strftime('%M:%S.%f')[:-3]} - {message}")

# Initialize the GPIO pins and reset the ASA
def init_GPIO():
    pi.set_mode(CLK, pigpio.OUTPUT)
    pi.set_mode(STB_A, pigpio.OUTPUT)
    pi.set_mode(STB_B, pigpio.OUTPUT)
    pi.set_mode(DAT, pigpio.OUTPUT)
    pi.set_mode(RST, pigpio.OUTPUT)

    log(f"Reset: 1")
    time.sleep(0.1)
    pi.write(RST, 1)
    log(f"Reset: 0")
    pi.write(RST, 0)
    time.sleep(0.1)
    print("GPIO initialized")

# This map converts the Y-X coordinates to the corresponding address in the ASA
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
    "AB_5": 0, "AB_6": 0, "AB_7": 0, "AB_8": 0,
    "AA_1": 0, "AA_2": 0, "AA_3": 0, "AA_4": 0,
    "AA_5": 0, "AA_6": 0, "AA_7": 0, "AA_8": 0,
    "BB_1": 0, "BB_2": 0, "BB_3": 0, "BB_4": 0,
    "BB_5": 0, "BB_6": 0, "BB_7": 0, "BB_8": 0
}

# This map connects the status_map key to the address_map index of Chip A
connection_map_chip_A = {
    "AB_1": 0, "AB_2": 1, "AB_3": 2, "AB_4": 3,
    "AB_5": 4, "AB_6": 5, "AB_7": 6, "AB_8": 7,
    "AA_1": 8, "AA_2": 9, "AA_3": 10, "AA_4": 11,
    "AA_5": 12, "AA_6": 13, "AA_7": 14, "AA_8": 15
}

# This map connects the status_map key to the address_map index of Chip B
connection_map_chip_B = {
    "AB_1": 0, "AB_2": 1, "AB_3": 2, "AB_4": 3,
    "AB_5": 4, "AB_6": 5, "AB_7": 6, "AB_8": 7,
    "BB_1" : 8, "BB_2" : 9, "BB_3" : 10, "BB_4" : 11,
    "BB_5" : 12, "BB_6" : 13, "BB_7" : 14, "BB_8" : 15,
}

def reset_ASA():
    pi.write(RST, 1)
    time.sleep(delay)
    pi.write(RST, 0)
    time.sleep(delay)

def set_ASA(address, state, chip):
    # address: Y0-X0
    # state: 1 or 0
    # chip: "A" or "B"

    pi.write(RST, 0)
    time.sleep(delay)

    log(f"address: {address}")
    log(f"state: {state}")
    log(f"chip: {chip}")

    #print("statusmap at the start: ", status_map))

    # Convert hex string to integer
    address_int = int(address_map[address], 16)

    print("value from address_map: ", bin(address_int))

    # Shift address_int left by 1 and add state bit
    address_int = (address_int << 1) | state

    print("value after shift: ", bin(address_int))

    # Determine strobe pin
    match chip:
        case "A":
            STB = STB_A
        case "B":
            STB = STB_B
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

        if address_int & 0x80:
            pi.write(DAT, 1)
            log("DAT 1")
            time.sleep(delay)
        else:
            pi.write(DAT, 0)
            log("DAT 0")
            time.sleep(delay)

        pi.write(CLK, 0)  # SK HIGH
        #log("CLK 0")
        time.sleep(delay)

        pi.write(CLK, 1)
        #log("CLK 1")
        time.sleep(delay)

        #print("value befor: ", value)
        address_int <<= 1
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

# This function will reset the ASA by toggling the RST pin
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