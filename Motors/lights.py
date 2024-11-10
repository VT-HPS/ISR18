import RPi.GPIO as GPIO #imports servo library
import time


# code to program lights
<<<<<<< HEAD

GPIO.setmode(GPIO.BCM) 
GPIO_PIN = 8
=======
# figure out difference between duty cycle and 

GPIO.setmode(GPIO.BCM) 
GPIO_PIN = 24
>>>>>>> fdf49efe132d447142b72f511aae981a55f99d76


# Set the GPIO pin as an output
GPIO.setup(GPIO_PIN, GPIO.OUT)

# PWM?? - mimmum pwm signal
<<<<<<< HEAD
pwm = GPIO.PWM(GPIO_PIN, 3)

# Sleep time setting
sleep_time = 5

try:
    pwm.start(19)
    time.sleep(sleep_time)
    pwm.start(11)
    time.sleep(sleep_time)
=======
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
        pwm.ChangeDutyCycle(0)
        pwm.ChangeDutyCycle(19)
        pwm.ChangeDutyCycle(0)
>>>>>>> fdf49efe132d447142b72f511aae981a55f99d76
    

finally:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()