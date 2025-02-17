import new_gui
import threading
from queue import Queue

def testing():
    import time
    while True:
        gui.set_standby()
        time.sleep(2)
        gui.set_active()
        time.sleep(4)


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