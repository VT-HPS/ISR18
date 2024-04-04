#!/usr/bin/python
#
#       This is the base code needed to get usable angles from a BerryIMU
#       using a Complementary filter. The readings can be improved by
#       adding more filters, E.g Kalman, Low pass, median filter, etc..
#       See berryIMU.py for more advanced code.
#
#       The BerryIMUv1, BerryIMUv2 and BerryIMUv3 are supported
#
#       This script is python 2.7 and 3 compatible
#
#       Feel free to do whatever you like with this code.
#       Distributed as-is; no warranty is given.
#
#       https://ozzmaker.com/berryimu/


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

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS 1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)

# Define the button pin
button_pin = 4
button = Button(button_pin)

# Define the log button pin
log_button_pin = 27
log_button = Button(log_button_pin)

# Initialize variables for button press capture
button_pressed = False
button_press_time = None

data = []

# Loop to read the analog inputs continually
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

# Compass Calibration values
magXmin = -1762
magYmin = -2534
magZmin = 0
magXmax = 622
magYmax = 928
magZmax = 6871

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

IMU.detectIMU()     # Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       # Initialise the accelerometer, gyroscope, and compass

a = datetime.datetime.now()

while True:
    # Read button press
    if button.is_pressed:
        if not button_pressed:
            button_press_time = datetime.datetime.now()
            button_pressed = True
    else:
        button_pressed = False
        button_press_time = None

    # Read log button press
    if log_button.is_pressed:
        # Record data when log button is pressed
        data.append({
            'time': datetime.datetime.now(),
            # Add other sensor data here if needed
        })

    # time.sleep(0.5)
    
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()

    if (ACCx + ACCy + ACCz == 0) or (GYRx + GYRy + GYRz == 0):
       time.sleep(0.1)
       continue
    
    pressure = channel.value / 1023 * 5

    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    outputString = "Loop Time %5.2f " % ( LP )

    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN

    gyroXangle += rate_gyr_x * LP
    gyroYangle += rate_gyr_y * LP
    gyroZangle += rate_gyr_z * LP

    AccXangle =  (math.atan2(ACCy, ACCz) * RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz, ACCx) + M_PI) * RAD_TO_DEG

    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0

    CFangleX = AA * (CFangleX + rate_gyr_x * LP) + (1 - AA) * AccXangle
    CFangleY = AA * (CFangleY + rate_gyr_y * LP) + (1 - AA) * AccYangle

    heading = 180 * math.atan2(MAGy, MAGx) / M_PI

    if heading < 0:
        heading += 360

    accXnorm = ACCx / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm / math.cos(pitch))

    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):
        magXcomp = MAGx * math.cos(pitch) + MAGz * math.sin(pitch)
    else:
        magXcomp = MAGx * math.cos(pitch) - MAGz * math.sin(pitch)

    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):
        magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * math.cos(roll) - MAGz * math.sin(roll) * math.cos(pitch)
    else:
        magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * math.cos(roll) + MAGz * math.sin(roll) * math.cos(pitch)

    tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp) / M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360

    outputString = "\n"

    if 1:
       outputString += "#  ACCX Angle %5.2f ACCY Angle %5.2f  #  " % (AccXangle, AccYangle)

    if 1:
       outputString += "\n# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle, gyroYangle, gyroZangle)

    if 1:
        outputString += "\n#  CFangleX Angle %5.2f   CFangleY Angle %5.2f  #" % (CFangleX, CFangleY)

    if 1:
        outputString += "\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading, tiltCompensatedHeading)

    # Display button press information
    if button_pressed:
        outputString += "\t# Button pressed at: {} #".format(button_press_time)

    print(outputString, end='')

    # slow program down a bit, makes the output more readable
