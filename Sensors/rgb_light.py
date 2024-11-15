from gpiozero import LED
from time import sleep
import RPi.GPIO
import neopixel_write
import board
import digitalio
import adafruit_blinka
import spi_install.bin

#from Battery_Warning import check_for_low_battery, check_for_dead_battery

pixel_pin = board.D18
num_pixels = 1


pin = digitalio.DigitalInOut(board.D18)#uses pin 18 as signal
pin.direction = digitalio.Direction.OUTPUT
pixel_on = bytearray([0, 255, 0])
#pixel_off = bytearray([0,0,0])
neopixel_write.neopixel_write(pin, pixel_on)

while(True):
    #if(check_for_low_battery == True):
    #    pixel_on = bytearray([255, 255,0])#turns yellow if battery is low
    #elif(check_for_dead_battery == True):
        #pixel_on = bytearray([255,0,0])#turns red if battery is dead
    #else:
        #pixel_on = bytearray([0, 255, 0])#turns green if battery is ok
    print("working")
    neopixel_write.neopixel_write(pin, pixel_on)#lights up led
