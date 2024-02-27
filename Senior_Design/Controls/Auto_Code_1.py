import argparse
import math
import time
import pigpio

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

def get_depth_data(rand):
    if rand == True:
        if DEPTH_RAND_TRACK >= 18:
            DEPTH_RAND_TRACK -= 1
        elif DEPTH_RAND_TRACK < 18 and DEPTH_RAND_TRACK > 15:
            DEPTH_RAND_TRACK -= 0.5
        elif DEPTH_RAND_TRACK <= 15 and DEPTH_RAND_TRACK > 10:
            DEPTH_RAND_TRACK += 0.5
        elif DEPTH_RAND_TRACK <= 10:
            DEPTH_RAND_TRACK += 1
            
        return DEPTH_RAND_TRACK

    else:
        return DEPTH_READING_PLACEHOLDER

if __name__ == "__main__":
    # Set GPIO mode
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)
    
    while True:
        depth = get_depth_data(True)
        pitch_angle = 0
        
        if (depth < 13 and pitch_angle > 12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 13 and pitch_angle > 8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-13))
        elif (depth < 13 and pitch_angle > 4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-11))
        elif (depth < 13 and pitch_angle > 0):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-9))
        elif (depth < 13 and pitch_angle > -4):
            print("Down mid")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-4))
        elif (depth < 13 and pitch_angle > -8):
            print("Down mid")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 13 and pitch_angle > -12):
            print("start correcting")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 13 and pitch_angle < -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(7))
        elif (depth < 15 and pitch_angle < 12):
            print("Down slow")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 15 and pitch_angle > 8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 15 and pitch_angle > 4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-6))
        elif (depth < 15 and pitch_angle > 0):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth < 15 and pitch_angle > -4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 15 and pitch_angle > -8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(3))
        elif (depth < 15 and pitch_angle > -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(8))
        elif (depth < 15 and pitch_angle < -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle < 12):
            print("Down slow")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 17 and pitch_angle > 8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-8))
        elif (depth < 17 and pitch_angle > 4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-3))
        elif (depth < 17 and pitch_angle > 0):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 17 and pitch_angle > -4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 17 and pitch_angle > -8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(6))
        elif (depth < 17 and pitch_angle > -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle < -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))
        elif (depth > 17 and pitch_angle > 12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-7))
        elif (depth > 17 and pitch_angle > 8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth > 17 and pitch_angle > 4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth > 17 and pitch_angle > 0):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth > 17 and pitch_angle > -4):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(9))
        elif (depth > 17 and pitch_angle > -8):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(11))
        elif (depth > 17 and pitch_angle > -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(13))
        elif (depth > 17 and pitch_angle < -12):
            print("Down fast")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))