#import RPi.GPIO as GPIO
import time


def __init__(self, pin = 6):
    self.leak_pin = pin
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(self.leak_pin, GPIO.IN)

def read_leak_status1(self): #real method
    return GPIO.input(self.leak_pin)

        # time.sleep(sleep_time)

def read_leak_status(): # dummy method
    return False
    
def leak_cleanup(self):
    #GPIO.cleanup()
    return 0