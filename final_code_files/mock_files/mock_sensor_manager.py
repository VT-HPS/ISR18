import os
import datetime
import csv
import time
import random  # For generating mock sensor values

# Mock functions for sensors
def mock_read_pressure():
    """ Simulates pressure sensor readings. """
    return [0, 0, random.uniform(0.5, 3.0), random.uniform(0, 100), random.uniform(1, 10)]

def mock_read_leak_status():
    """ Simulates leak status (0 or 1). """
    return random.choice([0, 1])

def mock_read_temp():
    """ Simulates temperature readings. """
    return round(random.uniform(20, 30), 2)

def manage_sensors(queue):
    """ Simulated sensor manager that generates mock data for testing. """
    # # Create log file
    # curr_time = datetime.datetime.now()
    # filename = f"logs/{curr_time.month}_{curr_time.day}_{curr_time.hour}_{curr_time.minute}_test.csv"

    # # Write header to CSV
    # with open(filename, 'a') as csvfile:
    #     header = [
    #         "Depth", "Water Pressure", "Speed", "Battery Voltage", "RPM", "Leak Status", "Temperature"
    #     ]
    #     writer = csv.writer(csvfile)
    #     writer.writerow(header)

    try:
        while True:
            # Generate mock sensor data
            pressure_data = mock_read_pressure()
            depth = pressure_data[3]
            water_pressure = pressure_data[4]
            pressure_speed = pressure_data[2]
            battery_voltage = random.uniform(11.0, 14.0)
            leak_status = mock_read_leak_status()
            temperature = mock_read_temp()

            # Retrieve latest data from queue to update other values
            if not queue.empty():
                latest_data = queue.get()
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

            latest_data.update({
                'depth': depth,
                'water_pressure': water_pressure,
                'pressure_speed': pressure_speed,
                'battery_voltage': battery_voltage,
                'leak_status': leak_status,
                'temperature': temperature
            })

            try:
                queue.put_nowait(latest_data)  # Non-blocking put
            except queue.Full:
                print("Mock Sensor Manager: Queue is full! Removing oldest entry.")
                queue.get()  # Remove oldest entry
                queue.put_nowait(latest_data)  # Add newest data



            # # Write to CSV
            # with open(filename, 'a') as csvfile:
            #     data = [
            #         depth, water_pressure, pressure_speed, battery_voltage,
            #         latest_data['rpm'], leak_status, temperature
            #     ]
            #     writer = csv.writer(csvfile)
            #     writer.writerow(data)

            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Sensor manager shutting down.")
