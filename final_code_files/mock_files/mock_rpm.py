import time
import random

# Define GPIO pins for RPM sensors (mocked, no actual GPIO usage)
RPM_SENSOR_PIN_A = 23  # First RPM sensor
RPM_SENSOR_PIN_B = 25  # Second RPM sensor

# Global variables
rpmA = 0
rpmB = 0

def rpm_value():
    """
    Generates a random RPM value to simulate sensor data.
    """
    return random.randint(500, 3000)  # Simulated RPM range

def monitor_rpm(sensor_data_queue):
    """
    Continuously generates mock RPM sensor data and updates the shared sensor_data_queue.
    """
    global rpmA, rpmB

    try:
        while True:
            rpmA = rpm_value()
            rpmB = rpm_value()

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
        print("Mock RPM monitoring stopped.")
