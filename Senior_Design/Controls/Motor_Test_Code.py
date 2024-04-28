import argparse
import math
import RPi.GPIO as GPIO
import time
import pigpio

DEFAULT_SPEED = 0
ANGLE_0_PWM = 850
ANGLE_MAX_PWM = 2150
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100

# Argument parsing function
def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--position", type=int, default=DEFAULT_SPEED, help=f"Initial Position in degrees that the motor should start in, default\
                        is the angle 0 (900). Position must be greater than 0 or less than {TRAVEL_RANGE_ANGLE}")
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
    return (pwm_time / (HZ_US / PWM_FREQ)) * 100
    
    
if __name__ == "__main__":
    args = parse_cli()
    angle_pwm = map_angle_to_pwm(args.position)
    angle_dc = pwm_to_dc(angle_pwm)

    # Set GPIO mode
    #GPIO.setmode(GPIO.BCM)
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm_PIN_2 = 19
    #GPIO.setup(PWM_PIN, GPIO.OUT)
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)
    # Set PWM frequency
    #pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)
    
    try:
        #pwm.start(angle_dc)
        pwm.set_PWM_dutycycle(PWM_PIN, angle_dc)
        
        while True:
            angle = int(input("Desired Angle: "))
            
            if angle < 0 or angle > TRAVEL_RANGE_ANGLE:
                print(f"Please enter an angle between 0 and {TRAVEL_RANGE_ANGLE}")
                continue
            
            angle_pwm = map_angle_to_pwm(angle)
            angle_dc = pwm_to_dc(angle_pwm)
            pwm.set_PWM_dutycycle(PWM_PIN, angle_dc)
            print(f"DC: {angle_dc}, PWM: {angle_pwm}, Angle: {angle}")
            
            time.sleep(3)

        
    finally:
        # Clean up GPIO
        #pwm.stop()
        #GPIO.cleanup()
        print("Done")
