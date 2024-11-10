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

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1
channel = AnalogIn(ads, ADS.P0)

button = Button(4, False)

def read_sensor_values():
    pressure = channel.value/1023 *5
    #print(pressure)
    print(channel.value)
iteration = 0
data = []
while True:
    if iteration < 100:
        data.append(channel.value)
        iteration += 1
    else:
        total = 0
        for d in data:
            total += d
        data = []    
        print(total/100)
        iteration = 0
    #time.sleep(1)
	
