from gpiozero import LED
from time import sleep
import RPi.GPIO

led = LED(17)

while True:
    led.on()
    
