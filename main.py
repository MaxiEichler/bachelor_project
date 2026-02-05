# This is the main file that will run the program.
from gui.app import app
from hardware.ASA import init_GPIO
#from logic.GUI_connection import process_coordinates

def main():
    print("starting program...")
    #print(process_coordinates())  # Example usage of the function

# 
if __name__ == "__main__":
    main()
    init_GPIO()  # Initialize GPIO pins for ASA communication
    app.run(debug=True, use_reloader=False)