from gpiozero import LED
from time import sleep
import RPi.GPIO
#import neopixel_write
import board
import digitalio

#from Battery_Warning import check_for_low_battery, check_for_dead_battery
#from leak import leak as leak_check

white_ledLeak = LED(2)
#yellow_ledLeak = LED(24) this is probably not needed since leak is either on or off
red_ledLeak = LED(3)

green_ledBat = LED(17)
yellow_ledBat = LED(27)
red_ledBat = LED(22)


while(True):#comment out this "while(True):" when combining code assuming this will just go on the main loop

    #Actual lights code
    #white_ledLeak.off()
    #red_ledLeak.off()
    
    green_ledBat.off()
    yellow_ledBat.off()
    red_ledBat.off()
    #battery lights
    #if(check_for_low_battery == True):
    #    yellow_ledBat.on()#turns yellow if battery is low
    #elif(check_for_dead_battery == True):
        #red_ledBat.on()#turns red if battery is dead
    #else:
        #green_ledBat.on()#turns green if battery is ok

    #Leak lights
    #if(leak_check == True):
     #   red_ledLeak.on()
    #else:
     #   white_led.on()
    
    #Test code
    white_ledLeak.on()
    red_ledLeak.on()
    
    green_ledBat.on()
    yellow_ledBat.on()
    red_ledBat.on()
    
    print("working")