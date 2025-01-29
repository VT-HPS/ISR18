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
from new_gui import SpeedDepthHeadingGauges
from lights import run_lights
import globals
import threading


# THIS FILE IS A MESS RIGHT NOW
# the important thing is in the section: if __name__ == "__main__"
# this is the code that shows that we can do threading. more to come soon

def main():
    # start the gui
    app = SpeedDepthHeadingGauges()
    t1 = threading.Thread(target=app.mainloop())
    t2 = threading.Thread(target=run_lights())
    
    t1.start()
    t2.start()



if __name__ == "__main__":
    #main()
    #run_lights()

    app = SpeedDepthHeadingGauges()
    #app.mainloop()
    #t1 = threading.Thread(target=app.mainloop)
    t2 = threading.Thread(target=run_lights)
    
    #t1.start()
    t2.start()

    app.mainloop()