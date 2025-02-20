import RPi.GPIO as GPIO #imports servo library
import time
import leak_class
import board
import digitalio

GPIO.setmode(GPIO.BCM)  # Use Broadcom numbering scheme
GPIO.setup(7, GPIO.OUT)  # Set the pin as output

leak_sensor = leak_class(23)

try:

    leak_value = leak_sensor.read_value()
    
    if(leak_value == 1):
        GPIO.output(7, GPIO.LOW)
    else:
       GPIO.output(7, GPIO.HIGH) 


finally:
    GPIO.cleanup()