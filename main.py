## This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO, set_ASA, manualset, reset_ASA
from hardware.I2C import init_I2C, switch_expander
from logic.Routing import set_path

pi = pigpio.pi()

def main():
    print("starting program...")
    try:
        print("Starting Main Program... (The monitor will report automatically)")
        init_GPIO()  # Initialize GPIO pins for ASA communication
        init_I2C()   # Initialize I2C communication with the expanders  
        app.run(debug=True, use_reloader=False)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        pi.stop()  # Clean up pigpio resources
if __name__ == "__main__":
    #setup_gpio()  # Setup GPIO pins and event detection
    main()



