import new_gui
import threading
from queue import Queue
from gpiozero import Button
import lights
from stoppable_thread import StoppableThread
import RPi.GPIO as GPIO #imports servo library

def testing():
    # SETUP CODE HERE - things to run only once, like GPIO for the lights
    button = Button(24) # placeholder pin for now, don't know what this should be
    prev_state = 0
    standby = False
    switch = True
    
    #initialize gpio
    GPIO.setmode(GPIO.BCM) 
    GPIO_PIN = 24
    # Set the GPIO pin as an output
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    # PWM?? - mimmum pwm signal
    pwm = GPIO.PWM(GPIO_PIN, 100)
    pwm.start(11)
    
    standby_lights = StoppableThread(target = lights.run_standby_lights, args = (pwm, ), daemon = True)
    active_lights = StoppableThread(target = lights.run_active_lights, args = (pwm, ), daemon = True)
    standby_lights.start()
    active_lights.start()
    
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
                active_lights.deactivate()
                standby_lights.activate()
                
                # Set GUI to be in standby mode
                #gui.set_standby()
                print("in standby")
                pass
            
            else: # sets to active state, turns everything on
                # Start the lights thread for standby
                standby_lights.deactivate()
                active_lights.activate()
                
                # Set GUI to be in active mode
                #gui.set_active()
                print("in active")
                pass

        prev_state = curr_state
        switch = False



if __name__ == "__main__":
    # create the queue for sensor data
    sensor_data_queue = Queue()
    
    # initialize gui to pass into main
    gui = new_gui.SpeedDepthHeadingGauges(sensor_data_queue)
    
    # initialize and run main function as a thread
    #main_thread = threading.Thread(target = main, args = (sensor_data_queue, gui, ), daemon = True)
    #main_thread.start()
    test = threading.Thread(target = testing, daemon = False)
    test.start()
    
    # run gui - MUST BE AT END
    #gui.mainloop()