#########################################################################
#                             Imports                                   #
#########################################################################
import argparse
import math
import time
import pigpio
import ast
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
from matplotlib import pyplot as plt

#########################################################################
#                             Constants                                 #
#########################################################################

# Battery Values
warning_voltage = 11.5  # warn the user when voltage drops below this
shutoff_voltage = 11  # shutoff or sternly warn when the voltage drops below this

# Constants
sample_time_delay = 1  # read every 1 second
voltage_sample_size = 10  # store and check last 10 voltage readings

# IMU Sensor Values
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading values.

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


#########################################################################
#                         Variable Decleration                          #
#########################################################################

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
ina260 = adafruit_ina260.INA260(i2c)

# Create an ADS 1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channels
channel1 = AnalogIn(ads, ADS.P0)
channel2 = AnalogIn(ads, ADS.P1)

# Calibration Start Button
start_button = Button(26)

# Define a button for each RPM sensor
brpm1 = Button(23)
brpm2 = Button(24)

#########################################################################
#                                  Code                                 #
#########################################################################

def setup():
    # Initialize IMU
    IMU.detectIMU()     #Detect if BerryIMU is connected.
    if(IMU.BerryIMUversion == 99):
        print(" No BerryIMU found... exiting ")
        sys.exit()
    IMU.initIMU()       #Initialize the accelerometer, gyroscope and compass 

def main():
    
    while True:
        print("Fuck")
        
def read_sensor_values():
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    pressure1 = channel1.value / 1023 * 5
    pressure2 = channel2.value / 1023 * 5
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()
    return ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2

def check_battery_voltage(voltage_data):
    """Checks if the battery voltage is low and returns 0 if it is above the warning voltage,
    1 if the voltage is in the warning but not shutoff area, 2 if the voltage is below or equal to shutoff"""
    
    for voltage in voltage_data:
        if voltage >= warning_voltage:
            return 0
        elif voltage < warning_voltage and voltage > shutoff_voltage:
            return 1
        elif voltage <= shutoff_voltage:
            return 2
        
def low_battery_warning():
    print("Hey man your battery is low")

def dead_battery_warning():
    print("your battery is dead bro")