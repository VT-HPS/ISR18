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

# Servo range
servo_min_angle = 0
servo_max_angle = 180

# Sleep time
sleep_time = 1

# Function to move servo to a specific angle
def move_servo(servo_pin, angle):
    pulse_width = servo_min_pulse + (servo_max_pulse - servo_min_pulse) * (angle / servo_max_angle)
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
time.sleep(1)

# # PRESSURE SETUP ---------------------------------
# # Initialize the I2C interface
# i2c = busio.I2C(board.SCL, board.SDA)

# # Create an ADS 1115 object
# ads = ADS.ADS1115(i2c)

# # Define the analog input channel
# channel1 = AnalogIn(ads, ADS.P0)
# channel2 = AnalogIn(ads, ADS.P1)

# # var for formula
# pressure_range = 450
# voltage_upper = 5
# voltage_lower = 0


# RUNNING LOOP -------------------------------------
try:
    while True:
        # Example: Sweep from 0 to 180 degrees for servo 1
        move_servo(servo_gpio_pin_2, servo_min_angle)
        move_servo(servo_gpio_pin_1, servo_min_angle)
        time.sleep(sleep_time)
        
        # Sweep back from 180 to 0 degrees for servo 1
        move_servo(servo_gpio_pin_2, servo_max_angle)
        move_servo(servo_gpio_pin_1, servo_max_angle)
        time.sleep(sleep_time)
        
        # lights cycling code
        pwm.ChangeDutyCycle(0)
        time.sleep(sleep_time)
        pwm.ChangeDutyCycle(19)
        time.sleep(sleep_time)
        pwm.ChangeDutyCycle(0)
        
        # # pressure logging code
        # voltage_reading1 = channel1.voltage
        # old_pressure1 = channel1.value / 1023 * 5
        # pressure1 = (pressure_range * (voltage_reading1 - voltage_lower) ) / (voltage_upper - voltage_lower)
        
        # voltage_reading2 = channel2.voltage
        # old_pressure2 = channel2.value / 1023 * 5
        # pressure2 = (pressure_range * (voltage_reading2 - voltage_lower) ) / (voltage_upper - voltage_lower)

        # data = [
        #     {"Old Pressure1": old_pressure1, 
        #     "Channel Value1": channel1.value, 
        #     "Voltage1": voltage_reading1,
        #     "Pressure1": pressure1,
        #     "Old Pressure2": old_pressure2, 
        #     "Channel Value2": channel2.value, 
        #     "Voltage2": voltage_reading2,
        #     "Pressure2": pressure2}
        #     ]
        
        # with open('test.csv', 'a', newline='') as csvfile:
        #     fieldnames = ['Old Pressure1', 'Channel Value1', 'Voltage1', 'Pressure1',
        #                   'Old Pressure2', 'Channel Value2', 'Voltage2', 'Pressure2']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerows(data)
        
        time.sleep(0.5)
        
        
except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_servo_pulsewidth(servo_gpio_pin_1, 0)  # Stop servo 1
    pi.set_servo_pulsewidth(servo_gpio_pin_2, 0)  # Stop servo 2
    pi.stop()  # Close pigpio connection
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()