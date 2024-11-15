from gpiozero import LED
from time import sleep
import RPi.GPIO
import neopixel_write
import board
import digitalio
import neopixel
import time

pixelNum = 1
PixelOrder = neopixel.GRB
spi = board.SPI
color = (0xFF0000, 0X00FF00, 0X000FF)
delay = 0.1
pixel = neopixel.NeoPixelSPI(spi, pixelNum, pixel_order = PixelOrder, auto_write = False)


#from Battery_Warning import check_for_low_battery, check_for_dead_battery


pin = digitalio.DigitalInOut(board.D18)#uses pin 18 as signal
pin.direction = digitalio.Direction.OUTPUT
pixel_on = bytearray([0, 255, 0])
#pixel_off = bytearray([0,0,0])

while(True):
    #if(check_for_low_battery == True):
    #    pixel_on = bytearray([255, 255,0])#turns yellow if battery is low
    #elif(check_for_dead_battery == True):
        #pixel_on = bytearray([255,0,0])#turns red if battery is dead
    #else:
        #pixel_on = bytearray([0, 255, 0])#turns green if battery is ok
    neopixel_write.neopixel_write(pin, pixel_on)#lights up led