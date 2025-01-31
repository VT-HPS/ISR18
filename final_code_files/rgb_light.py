from gpiozero import LED
import RPi.GPIO
import board

from sensor_manager import battery_voltage#check_for_low_battery, check_for_dead_battery
from leak import leak as leak_check

white_ledLeak = LED(2)
#yellow_ledLeak = LED(24) this is probably not needed since leak is either on or off
red_ledLeak = LED(3)

green_ledBat = LED(17)
yellow_ledBat = LED(27)
red_ledBat = LED(22)


#while(True):#comment out this "while(True):" when combining code assuming this will just go on the main loop

    #switches lights if they should change
white_ledLeak.off()
red_ledLeak.off()
    
green_ledBat.off()
yellow_ledBat.off()
red_ledBat.off()

    #battery lights
if(battery_voltage < 11):
    red_ledBat.on()#turns red light on if battery is dead
elif(battery_voltage < 11.5):
    red_ledBat.on()#turns ryellow on if battery is low
else:
    green_ledBat.on()#turns green if battery is ok

    #Leak lights
if(leak_check == True):
    red_ledLeak.on()#truns red light on if there is a leak
else:
    white_ledLeak.on()#turns white light on if no leak
    