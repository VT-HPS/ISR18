import RPi.GPIO as GPIO
import time

sensor_Pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_Pin, GPIO.IN)
while(True):
    time.sleep(0.5)
    print(GPIO.input(sensor_Pin))

GPIO.cleanup()