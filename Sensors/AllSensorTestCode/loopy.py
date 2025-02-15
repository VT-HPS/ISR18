"""
This is the main file to control the whole program. Current plan is to spawn threads to run tasks concurrently. 
Look into using the rc.local file on pi to run this file on startup
We need to spin off the rpm sensor separately, the lights on their own, and the gui on its own
Probably use a try:except here in main for main code so that a keyboard interrupt will tear down
everything and shut down sensors correctly


turn on:
    gui in standby
    start reading sensors (leak, temp, battery, etc)
    sensors also start logging data
    lights flashing (dimmer)
    lights in ecan

first button press:
    gui activates
    lights change (brighter or faster?)
    
second button press:
    turn everything off
    cleanup functions for sensors (gpio, pwm)
    put back into standby (back to standby)
"""
print("I hate here")

import new_gui
import threading
import berryIMU
from queue import Queue
#import lights
print("Hello?")

# currently we are missing some functionality with the button presses and such. 
# this code right now runs the sensor manager and the gui. 
def main():
    # create the queue for sensor data
    # sensor_data_queue = Queue()
    
    # create and run sensor manager thread
    print("SHIT")
    sensor_thread = threading.Thread(target = berryIMU.read_sensors, daemon = True)
    sensor_thread.start()
    
    # create and run lights thread
    #lights_thread = threading.Thread(target = lights.run_lights, daemon = True)
    #lights_thread.start()

    print("fuck")
    # create and run gui (MUST BE RUN AT END OF METHOD)
    app = new_gui.SpeedDepthHeadingGauges()
    app.mainloop()


if __name__ == "__main__":
    print("ALL IS LOST")
    main()