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
channel = AnalogIn(ads, ADS.P1)

# var for formula
pressure_range = 450
voltage_upper = 5
voltage_lower = 0
depth = 0.0
water_pressure =  0.0



#button = Button(4, False)
# Loop to read the analog inputs continually
while True:
    voltage_reading = channel.voltage
    old_pressure = channel.value / 1023 * 5
    depth = (voltage_reading - 0.075) / 0.092
    water_pressure = depth * 0.433
    print("Voltage:     ", voltage_reading)
    print("Depth:   ", depth)
    print("PSIG:    ", water_pressure)
    print("Channel value:  ", channel.value)
    print("\n")

    time.sleep(1.5)
