"""
Manages collecting the sensor data, add sensor data to queue, log data into csv
"""

import os
import datetime
import csv
import Pressure
import leak
import time
import re
#from leak import LeakSensor

# temperature pressure imports
import board
#import adafruit_sht31d


"""
WHAT NEEDS TO BE WORKED ON
1. Change sensor code to be for one read of the sensor only
2. Move sensor setup and cleanup code to this file
"""


def manage_sensors(queue):
    #################
    # LOGGING SETUP #
    #################
    
    # see if log directory exists
    if (not os.path.exists(os.getcwd() + "/final_code_files/logs")):
        # make log directory
        os.mkdir("final_code_files/logs")
        
        # set run number variable (don't need to find since we just created it)
        run_number = 1
    
    else:
        # find run number 
        numbers = []
        runs_list = os.listdir("final_code_files/logs/")
        
        # regex to extract the run number (last digits before ".csv")
        # underscore + multiple digits + .csv for the pattern
        pattern = re.compile(r'_(\d+)\.csv$')
        
        # loop through each file, store each run number (last character)
        for name in runs_list:
            # use regex to store the run number
            match = pattern.search(name)
            if match:
                numbers.append(int(match.group(1)))
            
        # set run number as highest recorded run number (plus one)
        run_number = max(numbers) + 1
    
    # naming conventions for logs is <month>_<day>_<hour>_<minute>_<run number>
    # use this filename for the csv to log the data
    curr_time = datetime.datetime.now()
    filename = f"final_code_files/logs/{curr_time.month}_{curr_time.day}_{curr_time.hour}_{curr_time.minute}_{run_number}.csv" 
    
    # write header to csv file
    with open(filename, 'a') as csvfile:
        header = [
            "Depth",
            "Water Pressure",
            "Speed",
            "Battery Voltage",
            "RPM",
            "Leak Status",
            "Temperature"
        ]
        writer = csv.writer(csvfile)
        writer.writerow(header)
        csvfile.close()
        
    ################
    # SENSOR SETUP #
    ################
    
    
    #leak_sensor = LeakSensor()

    
    
    
    try:
        #for i in range(15):
        count = 0
        while True:
            ##################
            # SENSOR READING #
            ##################
            
            # read the sensors
            # TODO PLACEHOLDER VALUES REPLACE WITH FUNCTION CALLS
            #depth, water_pressure, pressure_speed = Pressure.read_pressure()
            # THE FOLLOWING IS TEMPORARY DUMMY DATA
            depth = count + 1
            water_pressure = count + 6
            pressure_speed = count + 10
            battery_voltage = 3
            rpm = count
            leak_status = leak.read_leak_status()
            temperature = count + 8
            
            gui_data_buffer = {
                'depth': depth,
                'water_pressure': water_pressure,
                'pressure_speed': pressure_speed,
                'battery_voltage': battery_voltage,
                'rpm': rpm,
                'leak_status': leak_status,
                'temperature': temperature
            }
            queue.put(gui_data_buffer)
            count += 1 # TEMPORARY TESTING CODE
            
            # write data to csv
            with open(filename, 'a') as csvfile:
                data = [
                    depth,
                    water_pressure,
                    pressure_speed,
                    battery_voltage,
                    rpm,
                    leak_status,
                    temperature
                ]
                writer = csv.writer(csvfile)
                writer.writerow(data)
                csvfile.close()
            time.sleep(1)
        
    finally:
        ##################
        # SENSOR CLEANUP #
        ##################
        
        # cleanup everything (gpio, pwm, file naming)
        """ Here we need to pull some of the cleaunp code from the sensors. Anything from
        the sensor stuff right now should probably end up here"""
        pass