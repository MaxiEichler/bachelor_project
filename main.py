## This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO, set_ASA
from hardware.I2C import init_I2C, switch_expander
#from logic.GUI_connection import process_coordinates


def main():
    print("starting program...")
    #print(process_coordinates())  # Example usage of the function

# 
if __name__ == "__main__":
    main()
    init_GPIO()  # Initialize GPIO pins for ASA communication
    init_I2C()   # Initialize I2C communication with the expanders  
    #switch_expander(4, "data")  # Example usage of the switch_expander function
    #switch_expander(4, "power")  # Example usage of the switch_expander function
    #set_ASA("Y7-X15", 1, "A")
    app.run(debug=True, use_reloader=False)
