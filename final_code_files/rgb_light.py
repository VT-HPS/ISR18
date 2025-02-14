from gpiozero import LED
import RPi.GPIO
import board

from sensor_manager import battery_voltage#check_for_low_battery, check_for_dead_battery
from leak import leak as leak_check

white_ledLeak = LED(2)#2
#yellow_ledLeak = LED(24) this is probably not needed since leak is either on or off
red_ledLeak = LED(3)#3

green_ledBat = LED(17)#17
yellow_ledBat = LED(27)#27
red_ledBat = LED(22)#22


while(True):#comment out this "while(True):" when combining code assuming this will just go on the main loop

    #battery lights
    if(battery_voltage < 11):
        red_ledBat.on()#turns red light on if battery is dead
        green_ledBat.off()
        yellow_ledBat.off()
    elif(battery_voltage < 11.5):
        yellow_ledBat.on()#turns yellow light on if voltage is low
        green_ledBat.off()
        yellow_ledBat.off()
    else:
        green_ledBat.on()#turns green if battery is ok
        yellow_ledBat.off()
        red_ledBat.off()
        #Leak lights
    if(leak_check == True):
        red_ledLeak.on()#truns red light on if there is a leak
        white_ledLeak.off()
    else:
        white_ledLeak.on()#turns white light on if no leak
        red_ledLeak.off()
    