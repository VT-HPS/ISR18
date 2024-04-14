import argparse
import math
import time
import pigpio
import ast

DEFAULT_SPEED = 0
ANGLE_0_PWM = 900
ANGLE_MAX_PWM = 2100
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100

CURRENT_FIN_ANGLE = 0
MAX_FIN_ONE_DIR = 16.25

DEPTH_RAND_TRACK = 15
DEPTH_READING_PLACEHOLDER = 15

# Function that takes a fin angle and determines the appropriate motor angle where the middle is half the full travel range
def map_fin_to_motor(fin_angle):
    return (fin_angle * 4) + (TRAVEL_RANGE_ANGLE / 2)

# Function that takes an motor angle and figures outs the approriate pwm in microseconds
def map_angle_to_pwm(angle):
    return math.floor((((ANGLE_MAX_PWM - ANGLE_0_PWM) / TRAVEL_RANGE_ANGLE) * angle) + ANGLE_0_PWM)

# Function that determines duty cycle based on pwm signal and current frequency
def pwm_to_dc(pwm_time):
    HZ_US = 1000000 # Conversion from 1 hertz to 1000000 microseconds
    return (pwm_time / (HZ_US / PWM_FREQ)) * 100

def fin_angle_to_dc(fin_angle):
    motor_angle = map_fin_to_motor(fin_angle)
    angle_pwm = map_angle_to_pwm(motor_angle)
    return pwm_to_dc(angle_pwm)