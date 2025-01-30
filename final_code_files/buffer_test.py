import time
import importlib
import globals  # Import the global buffer

def main():
    print("Starting main.py to check globals.gui_data_buffer updates...\n")
    
    while True:
        # Reload globals.py to get the latest gui_data_buffer
        importlib.reload(globals)  

        # Print the global buffer contents
        print("Current gui_data_buffer:", globals.gui_data_buffer)

        # Wait 2 seconds before printing again
        time.sleep(2)

if __name__ == "__main__":
    main()
