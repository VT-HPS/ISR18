import time
import math
import IMU
import datetime
import os
import sys
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import Button
import adafruit_ina260

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading values.
'''
magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0
'''
magXmin = -1762
magYmin = -2534
magZmin = 0
magXmax = 622
magYmax = 928
magZmax = 6871

'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''
############### END Calibration offsets #################

#########################################################
#                  Sensor Variables                     #
#########################################################
# Battery Values
expect_voltage = 12.6
warning_voltage = 11.5  # warn the user when voltage drops below this
shutoff_voltage = 11  # shutoff or sternly warn when the voltage drops below this

class Sensors():
    def __init__(self, pressure_channel1, pressure_channel2):
        channel1 = pressure_channel1
        channel2 = pressure_channel2
    
    def read_sensor_vals(self):
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        pressure1 = self.channel1.value / 1023 * 5
        pressure2 = self.channel2.value / 1023 * 5
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()
        return ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2

    def pitch_calculation(self):
        pass

    def yaw_calculation(self):
        pass

    def battery_testing(self, voltage_data):
        for voltage in voltage_data:
            if voltage > warning_voltage:
                return

        for voltage in voltage_data:
            if voltage > shutoff_voltage:
                print("warning")
        
        print("shutdown")
            
    def output_all_data_vals(self):
        pass
