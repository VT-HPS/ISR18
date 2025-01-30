"""
Manages collecting the sensor data, add data to global buffer, log data
"""

import os
import globals
import datetime
import csv
import Pressure
import leak
#from leak import LeakSensor

gui_data_buffer = globals.gui_data_buffer

def manage_sensors():
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
        
        # loop through each file, store each run number (last character)
        for name in runs_list:
            numbers.append(int(name[len(name) - 5]))
            
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
        
    ###########################
    # PUT SETUP CODE BELOW HERE
    ###########################
    
    
    #leak_sensor = LeakSensor()

    
    
    
    try:
        for i in range(15):
        #while True:
            # read the sensors
            # TODO PLACEHOLDER VALUES REPLACE WITH FUNCTION CALLS
            depth, water_pressure, pressure_speed = Pressure.read_pressure()
            battery_voltage = 3
            rpm = 4
            leak_status = leak.read_leak_status()
            temperature = 6
            
            # write data to global buffer
            globals.gui_data_buffer['depth'].append(depth)
            globals.gui_data_buffer['water_pressure'].append(water_pressure)
            globals.gui_data_buffer['pressure_speed'].append(pressure_speed)
            globals.gui_data_buffer['battery_voltage'].append(battery_voltage)
            globals.gui_data_buffer['rpm'].append(rpm)
            globals.gui_data_buffer['leak_status'].append(leak_status)
            globals.gui_data_buffer['temperature'].append(temperature)

            print("updated buffer:", gui_data_buffer)

            # pop old data from global buffer
            for sensor_key, sensor_data in globals.gui_data_buffer.items():
                    if len(sensor_data) > 4:
                        sensor_data.pop()
            
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
        
    finally:
        # cleanup everything (gpio, pwm, file naming)
        """ Here we need to pull some of the cleaunp code from the sensors. Anything from
        the sensor stuff right now should probably end up here"""
        pass


# TODO REMOVE FOR FINAL VERSION
if __name__ == "__main__":
    manage_sensors()

    # What do you want me to work on? - Wyatt
# what would be great is if you can go into each of the sensors files and take them out of a loop
# also we need to move their setup code to here i think? because we want each of the sensors to just provide
# a function to read one value at a time so we can run all of them here in a while loop
# so like the temp sensor would have like read_temp() and we can call that and it returns one value
# we then log that and pass to global buffer
# actually i didn't think about the setup code that might be an issue? probably not tho