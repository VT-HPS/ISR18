import time
import RPi.GPIO as GPIO

# Define GPIO pins for RPM sensors
RPM_SENSOR_PIN_A = 23  # First RPM sensor
RPM_SENSOR_PIN_B = 25  # Second RPM sensor

# Global variables
currentstateA = 0
prevstateA = 0
prevmillisA = 0
rpmA = 0

currentstateB = 0
prevstateB = 0
prevmillisB = 0
rpmB = 0

def rpm_value(sensor_pin, prev_state, prev_millis, rpm):
    """
    Reads the RPM sensor and calculates RPM.
    """
    current_state = GPIO.input(sensor_pin)

    # Detect change in state
    if prev_state != current_state:
        if current_state == GPIO.HIGH:  # LOW to HIGH transition
            duration = int(time.time() * 1000) - prev_millis  # Time difference in ms
            if duration > 0:
                rpm = 60000 // duration  # RPM calculation
            prev_millis = int(time.time() * 1000)  # Store time for next calculation

    # No pulse detected for 2 seconds, set RPM to 0
    if (int(time.time() * 1000) - prev_millis) >= 2000:
        rpm = 0

    return current_state, prev_millis, rpm

def monitor_rpm(sensor_data_queue):
    """
    Continuously monitors both RPM sensors and updates the shared sensor_data_queue.
    """
    global rpmA, rpmB

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RPM_SENSOR_PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RPM_SENSOR_PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            global prevstateA, prevmillisA, prevstateB, prevmillisB
            prevstateA, prevmillisA, rpmA = rpm_value(RPM_SENSOR_PIN_A, prevstateA, prevmillisA, rpmA)
            prevstateB, prevmillisB, rpmB = rpm_value(RPM_SENSOR_PIN_B, prevstateB, prevmillisB, rpmB)

            # Compute average RPM
            averaged_rpm = (rpmA + rpmB) / 2

            # Print RPM values
            print(f"RPM A: {rpmA}, RPM B: {rpmB}, Averaged RPM: {averaged_rpm}")

            # Fetch latest data from queue or create new default data
            if not sensor_data_queue.empty():
                latest_data = sensor_data_queue.get()
            else:
                latest_data = {
                    'depth': 0,
                    'water_pressure': 0,
                    'pressure_speed': 0,
                    'battery_voltage': 0,
                    'rpm': 0,
                    'leak_status': 0,
                    'temperature': 0
                }

            # Update RPM value
            latest_data['rpm'] = averaged_rpm  
            sensor_data_queue.put(latest_data)

            time.sleep(0.01)  # Small delay to allow processing

    except KeyboardInterrupt:
        print("Real RPM monitoring stopped.")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
