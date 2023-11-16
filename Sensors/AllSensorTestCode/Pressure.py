import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import time
from gpiozero import Button
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS 1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)


button = Button(4, False)
# Loop to read the analog inputs continually
while True:
    pressure = channel.value / 1023 * 5
    print("Pressure: ", pressure, "Button Value: ", button.value)
    time.sleep(0.5)
