import board
import time
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

# var for formula
pressure_range = 450
voltage_upper = 5
voltage_lower = 0



#button = Button(4, False)
# Loop to read the analog inputs continually
while True:
    voltage_reading = channel.voltage
    old_pressure = channel.value / 1023 * 5
    pressure = (pressure_range * (voltage_reading - voltage_lower) ) / (voltage_upper - voltage_lower)
    print("Old Pressure: ", old_pressure)
    print("Channel Value: ", channel.value)
    print("Voltage: ", voltage_reading)
    print("Pressure:    ", pressure)

    time.sleep(0.5)
