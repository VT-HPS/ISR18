import time
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

# Initialize a button on GPIO pin 4 with a pull-down resistor, 
# allowing interaction via the button variable.
button = Button(4, False)

IMU.detectIMU()     # Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print("No BerryIMU found... exiting")
    sys.exit()
IMU.initIMU()       # Initialise the accelerometer, gyroscope and compass

while True:
    # Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()
    pressure = channel.value / 1023 * 5
    button_value = button.value
    
    time.sleep(0.5)

    # Save the sensor values to a file
    with open("sensor_data.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}, {ACCx}, {ACCy}, {ACCz}, {GYRx}, {GYRy}, {GYRz}, {MAGx}, {MAGy}, {MAGz}, {pressure}, {button_value}\n")

    time.sleep(0.5)  # Sleep for a bit to avoid too frequent file writes
