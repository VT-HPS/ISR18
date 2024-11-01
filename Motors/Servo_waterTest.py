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
pwm1.start(7.5)  # Start PWM with 0 duty cycle (servo off)
pwm2.start(7.5)

# Define duty cycles for the servo's range (1000 to 2100 microseconds pulse width)
duty_cycle_min = 6.0  # Corresponds to 0 degrees (~1000us pulse width)
duty_cycle_max = 8.0  # Corresponds to 100 degrees (~2100us pulse width)

min_pos = -15
max_pos = 15

# Control Surface max rotational velocity (degrees/second)
max_speed = 6
time_per_degree = 1/max_speed*.2

# Convert degrees to duty cycle steps
degree_range = max_pos-min_pos
DC_range = duty_cycle_max-duty_cycle_min
DC_perDeg = DC_range/degree_range

step_time = .1


def move_servos(start_deg, end_deg):
     start_DC = (start_deg+15)/degree_range*DC_range+duty_cycle_min
     end_DC = (end_deg+15)/degree_range*DC_range+duty_cycle_min\
     
     print(start_DC)
     print(end_DC)
     if start_DC < end_DC:
          step = DC_perDeg
     else:
          step = -DC_perDeg


     current_DC = start_DC
     while (step > 0 and current_DC < end_DC) or (step < 0 and current_DC > end_DC):
          current_DC = current_DC+step
          
          pwm1.ChangeDutyCycle(current_DC)
          pwm2.ChangeDutyCycle(current_DC)
          print("value of current DC", current_DC)
          time.sleep(time_per_degree)
        

     pwm1.ChangeDutyCycle(end_DC)
     pwm2.ChangeDutyCycle(end_DC)


while True:
     move_servos(-15,15)
     time.sleep(.5)

     move_servos(15,-15)
     time.sleep(.5)