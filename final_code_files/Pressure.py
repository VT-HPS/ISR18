#import board
import time
#import busio
import math
#import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.analog_in import AnalogIn
#from gpiozero import Button

def _init_(self):
    # Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create an ADS 1115 object
    ads = ADS.ADS1115(i2c)

    # Define the analog input channel
    channel_0 = AnalogIn(ads, ADS.P0) # inside sensor
    channel_1 = AnalogIn(ads, ADS.P1) # nose/outside sensor
    water_density = 997 #kg/m^3


def read_pressure1(self): # real method

    # various readings
    voltage_reading_inside = self.channel_0.voltage
    voltage_reading_outside = self.channel_1.voltage

    depth_inside = (voltage_reading_inside - 0.075) / 0.092
    depth_outside = (voltage_reading_outside - 0.075) / 0.092

    # units are PSIG
    water_pressure_inside = depth_inside * 0.433
    water_pressure_outside = depth_outside * 0.433 # static pressure

    # units are in Pascals
    pa_pressure_inside = water_pressure_inside * 6894.76
    pa_pressure_outside = water_pressure_outside * 6894.76
    pressure_velocity = math.sqrt( (2 * (pa_pressure_inside - pa_pressure_outside)) / self.water_density)

    return depth_inside, water_pressure_inside, pressure_velocity

def read_pressure(): #dummy method
    return 10.0, 20.0, 30.0 # depth, pressure, velocity