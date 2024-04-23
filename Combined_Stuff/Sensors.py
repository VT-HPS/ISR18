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

MIN_PRESSURE = 0 # psi
MAX_PRESSURE = 500 # psi

WATER_DENSITY = 62.4 # lb/ft^3
WATER_DENSITY_METRIC = 997 # kg /m^3
PSI_TO_PASCALS = 6894.76

# Previous calibration assumed that on a 0 - 1023 digital input, the depth of water would be 0 - 1023
# inches. In other words, they perfectly scaled. The ADC used here is not 0 - 1023, so we need to scale
# this value.
ADC_HIGH = 2**16 - 1 # Upper limit of 0 to X scale of digital input from analog to digital convertor
DIGITAL_TO_INCHES = (2**10 - 1) / ADC_HIGH # Scales to inches based on previous calibration


def digital_to_inches(digital_input):
    return DIGITAL_TO_INCHES * digital_input

class Sensors():
    def __init__(self, pressure_channel1, pressure_channel2):
        self.channel1 = pressure_channel1
        self.channel2 = pressure_channel2
        self.yaw = 0
        self.prev_yaw_time = time.time()
        self.pitch = 0
        self.prev_pitch_time = time.time()
    
    def pitch_calculation(self, gyrz):
        cur_time = time.time()
        dt = cur_time - self.prev_pitch_time
        self.prev_pitch_time = cur_time
        self.pitch += dt * gyrz
        

    def yaw_calculation(self, gyry):
        cur_time = time.time()
        dt = cur_time - self.prev_yaw_time
        self.prev_yaw_time = cur_time
        self.yaw += dt * gyry

    def reset_values(self):
        self.yaw = 0
        self.pitch = 0

    def battery_testing(self, voltage_data):
        for voltage in voltage_data:
            if voltage > warning_voltage:
                return

        for voltage in voltage_data:
            if voltage > shutoff_voltage:
                print("warning")
        
        print("shutdown")
        
    # Input is a voltage reading
    def depth_calculation(self, static_pressure_reading):
        return digital_to_inches(static_pressure_reading) / 12 # output in feet

    # Returns velocity in knots
    def velocity_calculation(self, dyn_press_read, stat_press_read):
        dyn_press_in = digital_to_inches(dyn_press_read) # inches of water
        stat_press_in = digital_to_inches(stat_press_read) # inches of water

        inches_to_pascals = WATER_DENSITY / 12**3 * 6895
        dyn_press = dyn_press_in * inches_to_pascals
        stat_press = stat_press_in * inches_to_pascals

        velocity_m_per_s = math.sqrt( abs((2 / WATER_DENSITY_METRIC) * (dyn_press - stat_press)))
        m_per_s_to_knots = 1.94384449

        return velocity_m_per_s * m_per_s_to_knots
            

    def read_sensor_vals(self):
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        dynamic_pressure_reading = self.channel1.value
        static_pressure_reading = self.channel2.value
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()
        self.pitch_calculation(GYRy)
        self.yaw_calculation(GYRz)
        depth = self.depth_calculation(static_pressure_reading)
        velocity = self.velocity_calculation(dynamic_pressure_reading, static_pressure_reading)
 
        return ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, dynamic_pressure_reading, static_pressure_reading, self.yaw, self.pitch, depth, velocity
