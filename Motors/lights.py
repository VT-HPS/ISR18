import RPi.GPIO as GPIO #imports servo library
import time


# code to program lights
# figure out difference between duty cycle and 

GPIO.setmode(GPIO.BCM) 
GPIO_PIN = 24


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
    while True: # dont need sleep time bc of duty cycle
        
        switch = True # switch is 1, which means lights should be on

        if(switch):
         pwm.ChangeDutyCycle(19)

        else:
            pwm.ChangeDutyCycle(0)
    

finally:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()