import RPi.GPIO as GPIO
import time 

class leak_class:
    def __init__(self, leakPin):
        self.leakPin = leakPin
        GPIO.setup(leakPin, GPIO.IN)
        self.value = None


    def read_value(self):
        # Simulate reading a value from the sensor
        # Replace this with actual sensor reading logic
        leak = GPIO.input(leakPin)
        if leak == HIGH:
            self.value = 1 # Example temperature value
        else:
            self.value = 0
        return self.value

    def display_value(self):
        if self.value is not None:
            print(f"Leak sensor: {self.value}")
        else:
            print(f"Leak Sensor: No value read yet.")