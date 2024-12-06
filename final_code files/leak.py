import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM)
leak_pin = 23

GPIO.setup(leak_pin, GPIO.IN)
sleep_time = 3

try:
    while True:
        leak = GPIO.input(leak_pin)

       # time.sleep(sleep_time)

finally:
    GPIO.cleanup()