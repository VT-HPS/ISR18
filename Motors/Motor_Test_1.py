import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
GPIO_PIN = 18

# Set the GPIO pin as an output
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz
pwm = GPIO.PWM(GPIO_PIN, 100)

# Sleep time setting
sleep_time = 1
pwm.start(15)

while True:
    # Start PWM with a duty cycle of 21% (2100 microseconds)
    pwm.ChangeDutyCycle(21)

    # Wait for 5 seconds
    time.sleep(sleep_time)
    
    # Start PWM with a duty cycle of 15% (1500 microseconds)
    pwm.ChangeDutyCycle(15)

    # Wait for 5 seconds
    time.sleep(sleep_time)

    # Change the duty cycle to 9% (900 microseconds)
    pwm.ChangeDutyCycle(9)

    time.sleep(sleep_time)
    pwm.ChangeDutyCycle(15)

    # Wait for 5 seconds
    time.sleep(sleep_time)
