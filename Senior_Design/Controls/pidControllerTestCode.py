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

# Working variables for PID
last_time = 0
input_yaw = 0.0
input_pitch = 0.0
output_yaw = 0.0
output_pitch = 0.0
setpoint_yaw = 0.0
setpoint_pitch = 0.0
err_sum_yaw = 0.0
err_sum_pitch = 0.0
last_err_yaw = 0.0
last_err_pitch = 0.0
kp_yaw = 0.0
ki_yaw = 0.0
kd_yaw = 0.0
kp_pitch = 0.0
ki_pitch = 0.0
kd_pitch = 0.0

def compute():
    global last_time, input_yaw, input_pitch, output_yaw, output_pitch, setpoint_yaw, setpoint_pitch
    global err_sum_yaw, err_sum_pitch, last_err_yaw, last_err_pitch, kp_yaw, ki_yaw, kd_yaw, kp_pitch, ki_pitch, kd_pitch

    # Get current time in milliseconds
    now = time.time() * 1000  # Current time in milliseconds
    time_change = (now - last_time) / 1000.0  # Convert to seconds

    # Compute yaw PID terms
    error_yaw = setpoint_yaw - input_yaw
    err_sum_yaw += error_yaw * time_change
    ##d_err_yaw = (error_yaw - last_err_yaw) / time_change if time_change > 0 else 0.0
    output_yaw = kp_yaw * error_yaw + ki_yaw * err_sum_yaw + kd_yaw ## * d_err_yaw

    # Compute pitch PID terms
    error_pitch = setpoint_pitch - input_pitch
    err_sum_pitch += error_pitch * time_change
    ## d_err_pitch = (error_pitch - last_err_pitch) / time_change if time_change > 0 else 0.0
    output_pitch = kp_pitch * error_pitch + ki_pitch * err_sum_pitch + kd_pitch ## * d_err_pitch


    # Update previous errors for next cycle
    last_err_yaw = error_yaw
    last_err_pitch = error_pitch
    last_time = now

def set_tunings(Kp_yaw, Ki_yaw, Kd_yaw, Kp_pitch, Ki_pitch, Kd_pitch):
    global kp_yaw, ki_yaw, kd_yaw, kp_pitch, ki_pitch, kd_pitch
    kp_yaw = Kp_yaw
    ki_yaw = Ki_yaw
    kd_yaw = Kd_yaw
    kp_pitch = Kp_pitch
    ki_pitch = Ki_pitch
    kd_pitch = Kd_pitch



def read_sensor_vals(self):
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    dynamic_pressure_reading = self.channel1.value
    static_pressure_reading = self.channel2.value
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()
    self.pitch_calculation(GYRy)
    self.yaw_calculation(GYRz)
    depth = self.depth_calculation(static_pressure_reading)
    velocity = self.velocity_calculation(dynamic_pressure_reading, static_pressure_reading)
    return ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, dynamic_pressure_reading, static_pressure_reading, self.yaw, self.pitch, depth, velocity


# Example usage:
# Set tunings for yaw and pitch
set_tunings(Kp_yaw=1.0, Ki_yaw=0.1, Kd_yaw=0.01, Kp_pitch=1.0, Ki_pitch=0.1, Kd_pitch=0.01)

# Simulating sensor values (yaw and pitch angles)
input_yaw = 45.0  # Current yaw angle (degrees)
input_pitch = 10.0  # Current pitch angle (degrees)

# Desired setpoints for yaw and pitch
setpoint_yaw = 90.0  # Desired yaw angle (degrees)
setpoint_pitch = 0.0  # Desired pitch angle (degrees)

# Run the PID computation
compute()

# Output the results for yaw and pitch
print(f"PID Output for Yaw: {output_yaw}")
print(f"PID Output for Pitch: {output_pitch}")
