from gpiozero import LED
import RPi.GPIO
import board

#from sensor_manager import battery_voltage
#from leak import leak as leak_check

#gpio 9 is ground for warning lights
white_ledLeak = LED(21)
#yellow_ledLeak = LED(24)  probably not needed since leak is either on or off
red_ledLeak = LED(26)

green_ledBat = LED(20)
yellow_ledBat = LED(16)
red_ledBat = LED(21)

def run_warning_lights(bat_voltage, is_leak):
    while(True):

        #battery lights
        if(bat_voltage < 11):
            red_ledBat.on()#turns red light on if battery is dead
            green_ledBat.off()
            yellow_ledBat.off()
        elif(bat_voltage < 11.5):
            yellow_ledBat.on()#turns yellow light on if voltage is low
            green_ledBat.off()
            yellow_ledBat.off()
        else:
            green_ledBat.on()#turns green if battery is ok
            yellow_ledBat.off()
            red_ledBat.off()
            #Leak lights
        if(is_leak == True):
            red_ledLeak.on()#truns red light on if there is a leak
            white_ledLeak.off()
        else:
            white_ledLeak.on()#turns white light on if no leak
            red_ledLeak.off()
        