# IMPORTS
import pigpio
import time

import RPi.GPIO as GPIO #imports servo library

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import csv

# SERVO SETUP -----------------------
# Initialize pigpio
pi = pigpio.pi('localhost', 8888)

# Define GPIO pins connected to the servos
servo_gpio_pin_1 = 19
servo_gpio_pin_2 = 18

# Set servo pulse width limits (in microseconds)
servo_min_pulse = 900
servo_max_pulse = 2100

# Sleep time
sleep_time = 1

# Function to move servo to a specific angle
def move_servo(servo_pin, angle):
    pulse_width = servo_min_pulse + (servo_max_pulse - servo_min_pulse) * (angle / 180)
    pi.set_servo_pulsewidth(servo_pin, pulse_width)
    
# LIGHTS SETUP ----------------------------
# code to program lights
# figure out difference between duty cycle and 

GPIO.setmode(GPIO.BCM) 
GPIO_PIN = 24

# Set the GPIO pin as an output
GPIO.setup(GPIO_PIN, GPIO.OUT)

# PWM?? - mimmum pwm signal
pwm = GPIO.PWM(GPIO_PIN, 100)

# Sleep time setting
sleep_time = 1
#pwm.start()
#GPIO.output(GPIO_pin, GPIO.HIGH)
#pwm.start(11)
#13-17 is when the light is brightest, further testing for brightest signal
pwm.start(11) # starts the signal at the minmum value (11-19)
time.sleep(4)

# PRESSURE SETUP ---------------------------------
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


# RUNNING LOOP -------------------------------------
try:
    while True:
        # Example: Sweep from 0 to 180 degrees for servo 1
        for angle in range(0, 180, 180):
            move_servo(servo_gpio_pin_2, angle)
            move_servo(servo_gpio_pin_1, angle)
            time.sleep(sleep_time)
        
        # Sweep back from 180 to 0 degrees for servo 1
        for angle in range(180, 0, -180):
            move_servo(servo_gpio_pin_2, angle)
            move_servo(servo_gpio_pin_1, angle)
            time.sleep(sleep_time)
        
        # lights cycling code
        pwm.ChangeDutyCycle(0)
        pwm.ChangeDutyCycle(19)
        pwm.ChangeDutyCycle(0)
        
        # pressure logging code
        voltage_reading = channel.voltage
        old_pressure = channel.value / 1023 * 5
        pressure = (pressure_range * (voltage_reading - voltage_lower) ) / (voltage_upper - voltage_lower)

        data = [
            {"Old Pressure": old_pressure, 
            "Channel Value": channel.value, 
            "Voltage": voltage_reading,
            "Pressure": pressure}
            ]
        
        with open('test.csv', 'w', newline='') as csvfile:
            fieldnames = ['Old Pressure', 'Channel Value', 'Voltage', 'Pressure']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        time.sleep(0.5)
        
        
except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_servo_pulsewidth(servo_gpio_pin_1, 0)  # Stop servo 1
    pi.set_servo_pulsewidth(servo_gpio_pin_2, 0)  # Stop servo 2
    pi.stop()  # Close pigpio connection
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()