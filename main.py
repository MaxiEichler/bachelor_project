## This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO, set_ASA, manualset, reset_ASA
from hardware.I2C import init_I2C, switch_expander
from logic.Routing import set_path
#from logic.GUI_connection import process_coordinates
import time
from datetime import datetime
import pigpio

pi = pigpio.pi()

INPUT_DAT = 23
INPUT_STB = 27

def callback(gpio, level, tick):
    print(f"{datetime.now().strftime('%M:%S.%f')[:-3]} - {level}")

def main():
    print("starting program...")
    #print(process_coordinates())  # Example usage of the function
    try:
        # 1. Start the monitoring logic
        cb = pi.callback(INPUT_DAT, pigpio.EITHER_EDGE, callback)
        ab = pi.callback(INPUT_STB, pigpio.EITHER_EDGE, callback)

        # 2. Run your existing main program logic here
        print("Starting Main Program... (The monitor will report automatically)")
        init_GPIO()  # Initialize GPIO pins for ASA communication
        #init_I2C()   # Initialize I2C communication with the expanders  
        #switch_expander(1, "data", 1)  # Example usage of the switch_expander function
        #switch_expander(4, "power")  # Example usage of the switch_expander function
        #set_ASA("Y0-X8", 1, "B")
        #set_ASA("Y1-X8", 1, "B")
        #set_path(9, 10, "data")
        #manualset()
        #reset_ASA()
        app.run(debug=True, use_reloader=False)
        counter = 0
        while True:
            # SIMULATION: This represents your normal code running
            print(f"Main program is working... (Cycle {counter})")
            time.sleep(2) # Simulating a task that takes time
            counter += 1
            
            # Note: Even while 'sleep' is happening, the GPIO monitor 
            # will still trigger if you toggle the pin!

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        pi.stop()  # Clean up pigpio resources
if __name__ == "__main__":
    #setup_gpio()  # Setup GPIO pins and event detection
    main()



