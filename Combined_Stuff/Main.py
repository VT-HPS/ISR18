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
import threading
from .Servo import *
import Sensors
from .Autonomous_Reactive import *
import Battery_Warning


############################################################################
#                               Variables                                  #
############################################################################

log_time = time.time()

G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

DEFAULT_SPEED = 0
ANGLE_0_PWM = 900
ANGLE_MAX_PWM = 2100
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100

CURRENT_FIN_ANGLE = 0
MAX_FIN_ONE_DIR = 16.25

IDEAL_DEPTH = 6
DEPTH_RAND_TRACK = 15
DEPTH_READING_PLACEHOLDER = 15

warning_voltage = 11.5  # warn the user when voltage drops below this
shutoff_voltage = 11  # shutoff or sternly warn when the voltage drops below this

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

# Constants
voltage_sample_size = 10  # store and check last 10 voltage readings


############################################################################
#                               Initialize                                 #
############################################################################

# Code for logging data every 100 iterations
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_to_log = []

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

# Set GPIO mode
pwm_pitch = pigpio.pi()
pwm_yaw = pigpio.pi()

# Set PWM pin
PWM_PITCH_PIN = 18 # Servo 2
PWM_YAW_PIN = 19 # Servo 1

pwm_pitch.set_mode(PWM_PITCH_PIN, pigpio.OUTPUT)
pwm_pitch.set_PWM_frequency(PWM_PITCH_PIN, PWM_FREQ)
pwm_pitch.set_PWM_range(PWM_PITCH_PIN, 100)

pwm_yaw.set_mode(PWM_PITCH_PIN, pigpio.OUTPUT)
pwm_yaw.set_PWM_frequency(PWM_PITCH_PIN, PWM_FREQ)
pwm_yaw.set_PWM_range(PWM_PITCH_PIN, 100)

# Test runs
run_number = 0

# Setup Sensor Class
sensors = Sensors(channel1, channel2)

############################################################################
#                               Functions                                  #
############################################################################

def main():
    # Initialize IMU 
    IMU.detectIMU()     #Detect if BerryIMU is connected.
    if(IMU.BerryIMUversion == 99):
        print(" No BerryIMU found... exiting ")
        sys.exit()
    IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

    # Zero servos
    pwm_pitch.set_PWM_dutycycle(PWM_PITCH_PIN, fin_angle_to_dc(0))
    pwm_yaw.set_PWM_dutycycle(PWM_YAW_PIN, fin_angle_to_dc(0))

    # Check Battery Voltage
    voltage_data = []
    for _ in range(10):
        voltage_data.append(sensors.read_sensor_vals())
        
    sensors.battery_testing(voltage_data)

    # Wait for button press
    while wait_button.value == 0:
        continue

    # start runs
    try:
        while True:
            reset_loop()
    finally:
        cleanup()
    
    # Setup Datalogging
        
def create_run_log():
    
    # Define the file path with the run number
    sensor_file_path = os.path.join("/home/hps/ISR18/Combined_Stuff/Data_Logging_Files", f"sensor_data_run_{run_number}.csv")

    with open(sensor_file_path, "a") as f:
        f.write(f"Timestamp, ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2, yaw, pitch, depth, velocity\n")
        print("Sensor data logged.")


# wait_button.wait_for_press()
# log_sensor_values()

def do_run():
    # Ensure button is no longer pressed
    while wait_button.value == 1:
        continue

    #servo time for measuring adjustment timing
    servo_time = time.time()

    # start run loop
    wait_button_pressed = False
    while not wait_button_pressed:
        ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2, yaw, pitch, depth, velocity = sensors.read_sensor_values()
        
        # current time - the last time the servos were adjusted >= 500 ms
        if time.time() - servo_time >= 0.5:
            
            # autonomous function
            set_pitch = pitch_auto_control(pitch, depth, IDEAL_DEPTH)
            set_yaw = yaw_auto_control(yaw)
            
            # set servos
            pwm_pitch.set_PWM_dutycycle(PWM_PITCH_PIN, fin_angle_to_dc(set_pitch))
            pwm_yaw.set_PWM_dutycycle(PWM_YAW_PIN, fin_angle_to_dc(set_yaw))

            # reset servo time
            servo_time = time.time()

        # log the sensor data to array
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sensor_data = f"{timestamp}, {ACCx}, {ACCy}, {ACCz}, {GYRx}, {GYRy}, {GYRz}, {MAGx}, {MAGy}, {MAGz}, {pressure1}, {pressure2}, {yaw}, {pitch}, {depth}, {velocity}\n"
        data_to_log.append(sensor_data)

        # log to sensor data file every 10 seconds
        if time.time() - log_time >= 10:
            with open(f"sensor_data_run_{run_number}.csv", "a") as f:
                for data_entry in data_to_log:
                    f.write(data_entry)
            print("Data logged.")
            data_to_log = []
            log_time = time.time()
    
        if wait_button.value == 1:
            wait_button_pressed = True

    sensors.reset_values()

    run_number += 1



def reset_loop():
    if time.time() - log_time < 10:
        with open(f"sensor_data_run_{run_number}.csv", "a") as f:
            for data_entry in data_to_log:
                f.write(data_entry)
        print("Data logged.")
        data_to_log = []
        log_time = time.time()
    
    create_run_log()
    do_run()
    pass

def cleanup():
    with open(f"sensor_data_run_{run_number}.csv", "a") as f:
        for data_entry in data_to_log:
                f.write(data_entry)
    print("Data logged.")
    data_to_log = []

    Battery_Warning.check_for_low_battery

    pass

if __name__ == "__main__":
    main()