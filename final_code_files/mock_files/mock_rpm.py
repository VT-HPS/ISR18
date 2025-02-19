import time
import RPi.GPIO as GPIO

# Define GPIO pin for RPM sensor
RPM_SENSOR_PIN = 17  # Adjust this if needed

# Global variables
currentstateA = 0
prevstateA = 0
prevmillisA = 0
rpmA = 0

def rpm_value():
    """
    Reads the RPM sensor and calculates RPM.
    """
    global currentstateA, prevstateA, prevmillisA, rpmA

    # Read RPM sensor state
    currentstateA = GPIO.input(RPM_SENSOR_PIN)

    # Detect change in state
    if prevstateA != currentstateA:
        if currentstateA == GPIO.HIGH:  # LOW to HIGH transition
            durationA = int(time.time() * 1000) - prevmillisA  # time difference in ms
            if durationA > 0:
                rpmA = 60000 // durationA  # RPM calculation
            prevmillisA = int(time.time() * 1000)  # Store time for next calculation

    # No pulse detected for 2 seconds, set RPM to 0
    if (int(time.time() * 1000) - prevmillisA) >= 2000:
        rpmA = 0

    prevstateA = currentstateA  # Store this scan for next cycle
    print(f"Real RPM: {rpmA}")  # Debugging output

def monitor_rpm(sensor_data_queue):
    """
    Continuously monitors RPM and updates the shared sensor_data_queue.
    """
    global rpmA

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RPM_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            rpm_value()  # Read RPM

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
            latest_data['rpm'] = rpmA  
            sensor_data_queue.put(latest_data)

            time.sleep(0.01)  # Small delay to allow processing

    except KeyboardInterrupt:
        print("Real RPM monitoring stopped.")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
