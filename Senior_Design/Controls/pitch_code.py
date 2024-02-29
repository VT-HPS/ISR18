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

# Argument parsing function
def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", type=str, required=True, help=f"Data that should be used to test the positions of the motor, should be in the form of a list of tuples")
    return parser.parse_args()

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

def parse_tuple_list(input_string):
    try:
        # Use ast.literal_eval to safely evaluate the string as a Python literal
        tuple_list = ast.literal_eval(input_string)
        
        # Check if the parsed object is a list of tuples
        if not isinstance(tuple_list, list) or not all(isinstance(item, tuple) for item in tuple_list):
            raise ValueError("Input is not a valid list of tuples.")
        
        return tuple_list
    except (SyntaxError, ValueError) as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    # Arguments
    args = parse_cli()
    data_tuples = parse_tuple_list(args.data)

    # Set GPIO mode
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)

    for depth_angle in data_tuples:
        depth = depth_angle[0]
        pitch_angle = depth_angle[1]

        print(depth, pitch_angle)
        
        if (depth < 13 and pitch_angle > 12):
            print("1")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 13 and pitch_angle > 8):
            print("2")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-13))
        elif (depth < 13 and pitch_angle > 4):
            print("3")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-11))
        elif (depth < 13 and pitch_angle > 0):
            print("4")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-9))
        elif (depth < 13 and pitch_angle > -4):
            print("5")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-4))
        elif (depth < 13 and pitch_angle > -8):
            print("6")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 13 and pitch_angle > -12):
            print("7")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 13 and pitch_angle < -12):
            print("8")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(7))
        elif (depth < 15 and pitch_angle > 12):
            print("9")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 15 and pitch_angle > 8):
            print("10")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 15 and pitch_angle > 4):
            print("11")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-6))
        elif (depth < 15 and pitch_angle > 0):
            print("12")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth < 15 and pitch_angle > -4):
            print("13")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 15 and pitch_angle > -8):
            print("14")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(3))
        elif (depth < 15 and pitch_angle > -12):
            print("15")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(8))
        elif (depth < 15 and pitch_angle < -12):
            print("16")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle > 12):
            print("17")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 17 and pitch_angle > 8):
            print("18")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-8))
        elif (depth < 17 and pitch_angle > 4):
            print("19")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-3))
        elif (depth < 17 and pitch_angle > 0):
            print("20")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 17 and pitch_angle > -4):
            print("21")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 17 and pitch_angle > -8):
            print("22")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(6))
        elif (depth < 17 and pitch_angle > -12):
            print("23")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle < -12):
            print("24")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))
        elif (depth > 17 and pitch_angle > 12):
            print("25")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-7))
        elif (depth > 17 and pitch_angle > 8):
            print("26")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth > 17 and pitch_angle > 4):
            print("27")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth > 17 and pitch_angle > 0):
            print("28")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth > 17 and pitch_angle > -4):
            print("29")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(9))
        elif (depth > 17 and pitch_angle > -8):
            print("30")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(11))
        elif (depth > 17 and pitch_angle > -12):
            print("31")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(13))
        elif (depth > 17 and pitch_angle < -12):
            print("32")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))

        time.sleep(1)