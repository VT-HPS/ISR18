import argparse
import math
import RPI.GPIO as GPIO
import time

DEFAULT_SPEED = 0
ANGLE_0_PWM = 900
ANGLE_MAX_PWM = 2100
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100

# Argument parsing function
def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--position", type=int, default=DEFAULT_SPEED, help=f"Initial Position in degrees that the motor should start in, default\
                        is the angle 0 (800us). Position must be greater than 0 or less than {TRAVEL_RANGE_ANGLE}")
    args = parser.parse_args()
    
    if args.position is not None and (args.position < 0 or args.position > TRAVEL_RANGE_ANGLE):
        parser.error(f"Position angle must be between 0 and {TRAVEL_RANGE_ANGLE} inclusive")
    
    return args

# Function that takes an angle and figures outs the approriate pwm in microseconds
def map_angle_to_pwm(angle):
    return math.floor((((ANGLE_MAX_PWM - ANGLE_0_PWM) / TRAVEL_RANGE_ANGLE) * angle) + ANGLE_0_PWM)

# Function that determines duty cycle based on pwm signal and current frequency
def pwm_to_dc(pwm_time):
    HZ_US = 1000000 # Conversion from 1 hertz to 1000000 microseconds
    return math.floor((HZ_US / PWM_FREQ) / pwm_time)
    
    
if __name__ == "__main__":
    args = parse_cli()
    angle_pwm = map_angle_to_pwm(args.position)
    angle_dc = pwm_to_dc(angle_pwm)

    # Set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # Set PWM pin
    PWM_PIN = 18
    GPIO.setup(PWM_PIN, GPIO.OUT)

    # Set PWM frequency
    pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)
    
    try:
        pwm.start(angle_dc)
        
        while True:
            angle = input("Desired Angle: ")
            
            if angle < 0 or angle > TRAVEL_RANGE_ANGLE:
                print(f"Please enter an angle between 0 and {TRAVEL_RANGE_ANGLE}")
                continue
            
            angle_pwm = map_angle_to_pwm(angle)
            angle_dc = pwm_to_dc(angle_pwm)
            pwm.ChangeDutyCycle(angle_dc)
            
            time.sleep(3)

        
    finally:
        # Clean up GPIO
        pwm.stop()
        GPIO.cleanup()