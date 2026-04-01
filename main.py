## This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO, set_ASA, manualset, reset_ASA
from hardware.I2C import init_I2C, switch_expander
from logic.Routing import set_path
import time
from datetime import datetime
import pigpio

pi = pigpio.pi()

def callback(gpio, level, tick):
    print(f"{datetime.now().strftime('%M:%S.%f')[:-3]} - {level}")

def main():
    print("starting program...")
    #print(process_coordinates())  # Example usage of the function
    try:
        # 2. Run your existing main program logic here
        print("Starting Main Program... (The monitor will report automatically)")
        init_GPIO()  # Initialize GPIO pins for ASA communication
        init_I2C()   # Initialize I2C communication with the expanders  
        #switch_expander(5, "power")  # Example usage of the switch_expander function
        #switch_expander(6, "power")  # Example usage of the switch_expander function
        #set_ASA("Y6-X8", 1, "A")
        #set_ASA("Y7-X8", 1, "A")
        #set_path(9, 10, "data")
        #manualset()
        #reset_ASA()
        app.run(debug=True, use_reloader=False)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        pi.stop()  # Clean up pigpio resources
if __name__ == "__main__":
    #setup_gpio()  # Setup GPIO pins and event detection
    main()



