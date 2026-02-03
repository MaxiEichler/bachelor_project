# This code will handle the ASA (Analogue Swich Array) hardware component.
import time
import RPI.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)  # Clock pin
GPIO.setup(24, GPIO.OUT)  # Data out pin
GPIO.setup(17, GPIO.OUT)   # Strobe A pin
GPIO.setup(18, GPIO.OUT)   # Strobe B pin
GPIO.setup(19, GPIO.OUT)   # Strobe C pin
GPIO.setup(20, GPIO.OUT)   # Strobe D pin
GPIO.setup(26, GPIO.OUT)   # Reset pin

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

def set_ASA(address, state, chip):
    # This function will set switch in the ASA to state

    # var for when strobe pin is triggered
    x = 0

    # Turn hex number into a fixed 7 bit binary number
    hex_number = address_map[address]
    value = int(hex_number, 16)

    # Append state bit
    if state == 1:
        dat = (value << 1) | 1  # Append 1 to the right
    elif state == 0:
        dat = value << 1        # Append 0 to the right

    # Format to 8 bit binary string
    binary_7bit = format(dat, '08b')

    # Reset ASA chip before sending data
    GPIO.output(17, 0)  # Strobe A
    GPIO.output(18, 0)  # Strobe B
    GPIO.output(19, 0)  # Strobe C
    GPIO.output(20, 0)  # Strobe D
    GPIO.output(24, 0)  # Data out

    # Determine strobe pin based on chip
    match chip:
        case A: strobe = 17 # Strobe A
        case B: strobe = 18 # Strobe B
        case C: strobe = 19 # Strobe C
        case D: strobe = 20 # Strobe D

    # Send data to ASA via 3 wire SPI
    for i in list(binary_7bit):
        GPIO.output(11, 0)  #clock low
        time.sleep(0.01)
        GPIO.output(24, i)  #data out
        GPIO.output(11, 1)  #clock high
        time.sleep(0.01)
        x = x +1
        if x == 8:
            GPIO.output(strobe, 1)  # Strobe high
            time.sleep(0.01)
            GPIO.output(strobe, 0)  # Strobe low
            time.sleep(0.01)
            x = 0