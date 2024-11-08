from gpiozero import LED
from time import sleep
import RPi.GPIO
import neopixel_write
import board
import digitalio

#print(dir(board))
pin = digitalio.DigitalInOut(board.D18)#board.NEOPIXEL)
pin.direction = digitalio.Direction.OUTPUT
pixel_on = bytearray([255, 255, 255])
while(True):
    neopixel_write.neopixel_write(pin, pixel_on)