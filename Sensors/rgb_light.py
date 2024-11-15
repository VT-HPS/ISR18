from gpiozero import LED
from time import sleep
import RPi.GPIO
import neopixel_write
import board
import digitalio
import neopixel_spi as neopixel
import time

NUM_PIXELS = 12
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1

spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               auto_write=False)

while True:
    for color in COLORS:
        for i in range(NUM_PIXELS):
            pixels[i] = color
            pixels.show()
            time.sleep(DELAY)
            pixels.fill(0)
            print("working")


#pin = digitalio.DigitalInOut(board.D18)#uses pin 18 as signal
#pin.direction = digitalio.Direction.OUTPUT
#pixel_on = bytearray([0, 255, 0])
#pixel_off = bytearray([0,0,0])

#while(True):
    #if(check_for_low_battery == True):
    #    pixel_on = bytearray([255, 255,0])#turns yellow if battery is low
    #elif(check_for_dead_battery == True):
        #pixel_on = bytearray([255,0,0])#turns red if battery is dead
    #else:
        #pixel_on = bytearray([0, 255, 0])#turns green if battery is ok
#    neopixel_write.neopixel_write(pin, pixel_on)#lights up led