import new_gui
import threading
from queue import Queue
from gpiozero import Button

def testing():
    # SETUP CODE HERE - things to run only once, like GPIO for the lights
    button = Button(2) # placeholder pin for now, don't know what this should be
    prev_state = 0
    standby = False
    switch = True
    
    # main loop, takes care of state switching and launching threads when necessary
    while True:
        curr_state = button.value
        if (prev_state == 1 and curr_state == 0):
            # change the state
            switch = True
        
        if switch: # indicates switching of states
            standby = not standby # changes the current state
            
            if standby: # sets it to standby state, kills old threads and makes new ones
                # Set GUI to be in standby mode
                gui.set_standby()
                pass
            
            else: # sets to active state, turns everything on
                # Set GUI to be in active mode
                gui.set_active()
                pass

        prev_state = curr_state
        switch = False

"""
def testing():
    import time
    while True:
        gui.set_standby()
        time.sleep(2)
        gui.set_active()
        time.sleep(4)"""


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