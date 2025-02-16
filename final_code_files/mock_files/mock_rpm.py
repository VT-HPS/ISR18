import time
import datetime
import random

# Mock version: can run on my laptop cuz its rainy outside

def pulse_detected(sensor_data_queue):
    # random vals
    rpm = random.randint(500, 2000)  

    # get queue data
    if not sensor_data_queue.empty():
        latest_data = sensor_data_queue.get()
    else:
        # default values if queue is empty
        latest_data = {
            'depth': 0,
            'water_pressure': 0,
            'pressure_speed': 0,
            'battery_voltage': 0,
            'rpm': 0,
            'leak_status': 0,
            'temperature': 0
        }

    latest_data['rpm'] = rpm  # update only rpm

    sensor_data_queue.put(latest_data)  # put updated data back into the queue
    print(f"Updated RPM: {rpm}")  # debugging print

def monitor_rpm(sensor_data_queue):
    # simulated RPM monitor loop
    try:
        while True:
            pulse_detected(sensor_data_queue)  # generates new RPM valus
            time.sleep(1)  # 1 sec sensor update
    except KeyboardInterrupt:
        print("RPM monitoring stopped")
