import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
leak_pin = 23

# Set the GPIO pin as an input to read leaks
GPIO.setup(leak_pin, GPIO.IN)
sleep_time = 3

try:
    while True:
        leak = GPIO.input(leak_pin)
        if leak == 1:
            print("There is leak")
        time.sleep(sleep_time)

finally:
    GPIO.cleanup()