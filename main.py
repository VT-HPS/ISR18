"""
This is the main file to control the whole program. Current plan is to spawn threads to run tasks concurrently. 
Look into using the rc.local file on pi to run this file on startup
We need to spin off the rpm sensor separately, the lights on their own, and the gui on its own
"""
from final_code_files.new_gui import SpeedDepthHeadingGauges
from final_code_files.lights import run_lights
import globals
import threading

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