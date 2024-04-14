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

############################################################################
#                               Initialize                                 #
############################################################################

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
ina260 = adafruit_ina260.INA260(i2c)

# Create an ADS 1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channels
channel1 = AnalogIn(ads, ADS.P0)
channel2 = AnalogIn(ads, ADS.P1)

# Define a button for wait and data logging
wait_button = Button(26)

def main():
    # Initialize IMU 
    IMU.detectIMU()     #Detect if BerryIMU is connected.
    if(IMU.BerryIMUversion == 99):
        print(" No BerryIMU found... exiting ")
        sys.exit()
    IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

def main_loop():
    pass

def reset_loop():
    pass

def cleanup():
    pass

if __name__ == "__main__":
    pass
    