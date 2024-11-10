import pigpio
import time

# Servo Setup
# Initialize pigpio
pi = pigpio.pi()

# Define GPIO pins connected to the servos
servo_gpio_pin_1 = 19
servo_gpio_pin_2 = 18

# Set servo pulse width limits (in microseconds)
servo_min_pulse = 900
servo_max_pulse = 2100

# Sleep time
sleep_time = 1

# Function to move servo to a specific angle
def move_servo(servo_pin, angle):
    pulse_width = servo_min_pulse + (servo_max_pulse - servo_min_pulse) * (angle / 180)
    pi.set_servo_pulsewidth(servo_pin, pulse_width)

try:
    while True:
        # Example: Sweep from 0 to 180 degrees for servo 1
        for angle in range(0, 180, 180):
            move_servo(servo_gpio_pin_2, angle)
            move_servo(servo_gpio_pin_1, angle)
            time.sleep(sleep_time)
        
        # Sweep back from 180 to 0 degrees for servo 1
        for angle in range(180, 0, -180):
            move_servo(servo_gpio_pin_2, angle)
            move_servo(servo_gpio_pin_1, angle)
            time.sleep(sleep_time)
        
        

except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_servo_pulsewidth(servo_gpio_pin_1, 0)  # Stop servo 1
    pi.set_servo_pulsewidth(servo_gpio_pin_2, 0)  # Stop servo 2
    pi.stop()  # Close pigpio connection

