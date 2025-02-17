"""
This is the main file to control the whole program. Current plan is to spawn threads to run tasks concurrently. 
Look into using the rc.local file on pi to run this file on startup
We need to spin off the rpm sensor separately, the lights on their own, and the gui on its own
Probably use a try:except here in main for main code so that a keyboard interrupt will tear down
everything and shut down sensors correctly
So it also turns out that the gui needs to be run separately outside of the main function for anything to work
Since the gui is "blocking", it doesn't let anything else run alongside so the main() function is being
run as its own thread so they run concurrently


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
    put back into standby
"""
import new_gui
import threading
import sensor_manager
from queue import Queue
from gpiozero import Button
#import lights
import stoppable_thread


def main(queue):
    # SETUP CODE HERE - things to run only once, like GPIO for the lights
    button = Button(2) # placeholder pin for now, don't know what this should be
    prev_state = 0
    standby = False
    switch = True
    
    # create and run rpm thread
    # TODO need a file for this lmao
    #rpm_thread = threading.Thread(target=rpm.monitor_rpm, daemon=True, args=(queue,))
    #rpm_thread.start()
    
    # create and run sensor manager thread
    sensor_thread = threading.Thread(target = sensor_manager.manage_sensors, daemon = True, args = (queue, ))
    sensor_thread.start()
    
    # TODO probably hank's rgb lights here
    #rgb_thread = threading.Thread(target = PLACEHOLDER, daemon = True, args = (PLACEHOLDER, ))
    #rgb_thread.start()
    
    # main loop, takes care of state switching and launching threads when necessary
    while True:
        curr_state = button.value
        if (prev_state == 1 and curr_state == 0):
            # change the state
            switch = True
        
        if switch: # indicates switching of states
            standby = not standby # changes the current state
            
            if standby: # sets it to standby state, kills old threads and makes new ones
                # Start the lights thread for standby
                #standby_lights = StoppableThread(target = PLACEHOLDER, daemon = True)
                #standby_lights.start()
                
                # Set GUI to be in standby mode
                pass
            
            else: # sets to active state, turns everything on
                # Start the lights thread for active
                #active_lights = StoppableThread(target = PLACEHOLDER, daemon = True)
                #active_lights.start()
                
                # Set GUI to be in active mode
                pass

        prev_state = curr_state
        switch = False
        break
    
    
    # create and run lights thread
    #lights_thread = threading.Thread(target = lights.run_lights, daemon = True)
    #lights_thread.start()

def testing():
    import time
    while True:
        gui.set_standby()
        time.sleep(2)
        gui.set_active()
        time.sleep(2)


if __name__ == "__main__":
    # create the queue for sensor data
    sensor_data_queue = Queue()
    
    # initialize gui to pass into main
    gui = new_gui.SpeedDepthHeadingGauges(sensor_data_queue)
    
    # initialize and run main function as a thread
    #main_thread = threading.Thread(target = main, args = (sensor_data_queue, gui, ), daemon = True)
    #main_thread.start()
    test = threading.Thread(target = testing, daemon = True)
    test.start()
    
    # run gui - MUST BE AT END
    gui.mainloop()