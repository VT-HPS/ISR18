import RPi.GPIO as GPIO #imports servo library
import time


def run_lights():
    # code to program lights
    # figure out difference between duty cycle and 

    GPIO.setmode(GPIO.BCM) 
    GPIO_PIN = 5


    # Set the GPIO pin as an output
    GPIO.setup(GPIO_PIN, GPIO.OUT)

    # PWM?? - mimmum pwm signal
    pwm = GPIO.PWM(GPIO_PIN, 100)


    # Sleep time setting
    sleep_time = 1
    #pwm.start()
    #GPIO.output(GPIO_pin, GPIO.HIGH)
    #pwm.start(11)
    #13-17 is when the light is brightest, further testing for brightest signal
    pwm.start(11) # starts the signal at the minmum value (11-19)
    time.sleep(4)
    try:
        pwm.ChangeDutyCycle(13)
        time.sleep(4)
        pwm.ChangeDutyCycle(17)
        time.sleep(4)
        pwm.ChangeDutyCycle(0)
        

    finally:
        # Clean up GPIO
        pwm.stop()
        GPIO.cleanup()
        
        
def run_standby_lights(thread, pwm):
    while True:
        if thread.activated():
            print("standby lights")
            time.sleep(1)
    
    """while (not thread.stopped()):
        pwm.ChangeDutyCycle(13)
        time.sleep(4)
        pwm.ChangeDutyCycle(17)
        time.sleep(4)
        pwm.ChangeDutyCycle(0)"""


def run_active_lights(thread, pwm):
    while True:
        if thread.activated():
            print("active lights")
            time.sleep(1)
    
    '''while (not thread.stopped()):
        pwm.ChangeDutyCycle(11)
        time.sleep(4)
        pwm.ChangeDutyCycle(14)
        time.sleep(4)
        pwm.ChangeDutyCycle(0)'''