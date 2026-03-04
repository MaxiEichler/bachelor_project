## This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO, set_ASA
from hardware.I2C import init_I2C, switch_expander
#from logic.GUI_connection import process_coordinates
import time
from datetime import datetime
import RPi.GPIO as GPIO

INPUT_DAT = 23
INPUT_STB = 27

def gpio_callback(channel):
    """
    This runs in the BACKGROUND only when the pin changes.
    It does not block the main loop.
    """
    state = GPIO.input(channel)
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    state_label = "HIGH" if state else "LOW"
    
    # Print finding (or log to file)
    print(f"   [Background Monitor] {timestamp} -> GPIO {channel}: {state_label}")

def setup_monitoring():
    """Configures the background listener."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_DAT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INPUT_STB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # This line starts the background thread.
    # bouncetime=50 prevents one press from registering as multiple clicks (switch bounce)
    GPIO.add_event_detect(INPUT_DAT, GPIO.BOTH, callback=gpio_callback, bouncetime=10)
    GPIO.add_event_detect(INPUT_STB, GPIO.BOTH, callback=gpio_callback, bouncetime=10)
    print(f"--- Monitoring started on GPIO {INPUT_DAT} and {INPUT_STB} ---")

def main():
    print("starting program...")
    #print(process_coordinates())  # Example usage of the function
    try:
        # 1. Start the monitoring logic
        setup_monitoring()

        # 2. Run your existing main program logic here
        print("Starting Main Program... (The monitor will report automatically)")
        init_GPIO()  # Initialize GPIO pins for ASA communication
        init_I2C()   # Initialize I2C communication with the expanders  
        switch_expander(1, "data", 1)  # Example usage of the switch_expander function
        #switch_expander(4, "power")  # Example usage of the switch_expander function
        #set_ASA("Y7-X15", 1, "A")
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
        GPIO.cleanup()
if __name__ == "__main__":
    #setup_gpio()  # Setup GPIO pins and event detection
    main()



