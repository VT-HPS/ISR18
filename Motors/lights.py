import RPi.GPIO as GPIO #imports servo library
import time


# code to program lights

GPIO.setmode(GPIO.BCM) 
GPIO_PIN = 8


# Set the GPIO pin as an output
GPIO.setup(GPIO_PIN, GPIO.OUT)

# PWM?? - mimmum pwm signal
pwm = GPIO.PWM(GPIO_PIN, 3)

# Sleep time setting
sleep_time = 5

try:
    pwm.start(19)
    time.sleep(sleep_time)
    pwm.start(11)
    time.sleep(sleep_time)
    

finally:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()