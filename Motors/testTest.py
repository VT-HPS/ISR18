import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
servo1_pin = 18
servo2_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Set PWM frequency
pwm_frequency = 100

# Create PWM instance on the servo pin with the specified frequency
pwm1 = GPIO.PWM(servo1_pin, pwm_frequency)
pwm2 = GPIO.PWM(servo2_pin, pwm_frequency)
pwm1.start(0)  # Start PWM with 0 duty cycle (servo off)
pwm2.start(0)

# Define duty cycles for the servo's range (1000 to 2100 microseconds pulse width)
duty_cycle_min = 5.0  # Corresponds to 0 degrees (~1000us pulse width)
duty_cycle_max = 10.5  # Corresponds to 100 degrees (~2100us pulse width)

# Time settings for the motion
period = 5  # 5 seconds for a full back-and-forth motion
half_period = period / 2  # Time to go from min to max

try:
    while True:
        # Move the servo from 0 to 100 degrees
        pwm1.ChangeDutyCycle(duty_cycle_max)
        pwm2.ChangeDutyCycle(duty_cycle_max)
        time.sleep(half_period)

except KeyboardInterrupt:
    # Clean up the GPIO pins on keyboard interrupt (Ctrl+C)
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
