import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()

# Define GPIO pins connected to the servos
servo_gpio_pin_1 = 18
servo_gpio_pin_2 = 19

# Set servo ranges (1000 to 2000 microseconds)
servo_min_pulse = 1000
servo_max_pulse = 2000

# Set PWM frequency (Hz)
pwm_frequency = 100

# Configure PWM frequency for both servos
pi.set_PWM_frequency(servo_gpio_pin_1, pwm_frequency)
pi.set_PWM_frequency(servo_gpio_pin_2, pwm_frequency)

try:
    while True:
        # Move servo 1 to minimum position
        pi.set_servo_pulsewidth(servo_gpio_pin_1, servo_min_pulse)
        print("Servo 1 moved to minimum position")
        
        # Move servo 2 to minimum position
        pi.set_servo_pulsewidth(servo_gpio_pin_2, servo_min_pulse)
        print("Servo 2 moved to minimum position")
        
        time.sleep(1)
        
        # Move servo 1 to maximum position
        pi.set_servo_pulsewidth(servo_gpio_pin_1, servo_max_pulse)
        print("Servo 1 moved to maximum position")
        
        # Move servo 2 to maximum position
        pi.set_servo_pulsewidth(servo_gpio_pin_2, servo_max_pulse)
        print("Servo 2 moved to maximum position")
        
        time.sleep(3)

except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_PWM_dutycycle(servo_gpio_pin_1, 0)  # Stop PWM for servo 1
    pi.set_PWM_dutycycle(servo_gpio_pin_2, 0)  # Stop PWM for servo 2
    pi.stop()  # Close pigpio connection

