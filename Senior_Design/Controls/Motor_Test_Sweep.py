import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()

# Define GPIO pins connected to the servos
servo_gpio_pin_1 = 18
servo_gpio_pin_2 = 19

# Set servo ranges (1000 to 2000 microseconds)
servo_min_pulse = 900
servo_max_pulse = 2100

# Set PWM frequency (Hz)
pwm_frequency = 100

# Sleep time
sleep_time = 0.01

# Configure PWM frequency for both servos
pi.set_PWM_frequency(servo_gpio_pin_1, pwm_frequency)
pi.set_PWM_frequency(servo_gpio_pin_2, pwm_frequency)

try:
    while True:
        # Sweep servo 1 from minimum to maximum position
        for pulse in range(servo_min_pulse, servo_max_pulse + 1, 10):
            pi.set_servo_pulsewidth(servo_gpio_pin_1, pulse)
            time.sleep(sleep_time)
        
        # Sweep servo 1 from maximum to minimum position
        for pulse in range(servo_max_pulse, servo_min_pulse - 1, -10):
            pi.set_servo_pulsewidth(servo_gpio_pin_1, pulse)
            time.sleep(sleep_time)
        
        # Sweep servo 2 from minimum to maximum position
        for pulse in range(servo_min_pulse, servo_max_pulse + 1, 10):
            pi.set_servo_pulsewidth(servo_gpio_pin_2, pulse)
            time.sleep(sleep_time)
        
        # Sweep servo 2 from maximum to minimum position
        for pulse in range(servo_max_pulse, servo_min_pulse - 1, -10):
            pi.set_servo_pulsewidth(servo_gpio_pin_2, pulse)
            time.sleep(sleep_time)

except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_PWM_dutycycle(servo_gpio_pin_1, 0)  # Stop PWM for servo 1
    pi.set_PWM_dutycycle(servo_gpio_pin_2, 0)  # Stop PWM for servo 2
    pi.stop()  # Close pigpio connection

