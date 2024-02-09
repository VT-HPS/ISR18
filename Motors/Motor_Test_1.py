import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
GPIO_PIN = 25

# Set the GPIO pin as an output
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz
pwm = GPIO.PWM(GPIO_PIN, 100)

# Sleep time setting
sleep_time = 3 

try:
    # Start PWM with a duty cycle of 21% (2100 microseconds)
    pwm.start(22)

    # Wait for 5 seconds
    time.sleep(sleep_time)
    
    # Start PWM with a duty cycle of 15% (1500 microseconds)
    pwm.ChangeDutyCycle(15)

    # Wait for 5 seconds
    time.sleep(sleep_time)

    # Change the duty cycle to 9% (900 microseconds)
    pwm.ChangeDutyCycle(8)

    # Wait for 5 seconds
    time.sleep(sleep_time)

finally:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()
