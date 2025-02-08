import csv
import time
import os
import datetime
import math
import random
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import Button

class PressureSensor:
    def __init__(self):
        # Initialize the I2C interface for communication with the ADS1115 ADC
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create an ADS 1115 object to interface with the ADC
        ads = ADS.ADS1115(i2c)

        # Define the analog input channels for the pressure sensors
        self.channel_0 = AnalogIn(ads, ADS.P0) # Inside sensor
        self.channel_1 = AnalogIn(ads, ADS.P1) # Outside/nose sensor
        self.water_density = 997  # Density of water in kg/m^3

        # Setup log directory and ensure it exists
        log_dir = "pressure_logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            run_number = 1
        else:
            # if a file exists, find the run number and increase it for new file.
            numbers = [int(f.split('_')[-1].split('.')[0]) for f in os.listdir(log_dir) if f.endswith(".csv")]
            run_number = max(numbers) + 1 if numbers else 1

        # timestamped filename for storing the data
        curr_time = datetime.datetime.now()
        self.filename = f"{log_dir}/{curr_time.month}_{curr_time.day}_{curr_time.hour}_{curr_time.minute}_{run_number}.csv"

        # header to CSV file
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Depth Inside (ft)", "Pressure Inside (PSIG)", "Velocity (m/s)", "Depth Outside (m)", "Pressure Outside (PSIG)", "Voltage Inside", "Voltage Outside", "Channel Inside", "Channel Outside"])

    def read_pressure(self):  # Read and process sensor data

        voltage_reading_inside = self.channel_0.voltage
        voltage_reading_outside = self.channel_1.voltage

        # Channel values from the sensors
        channel_reading_inside = self.channel_0.value
        channel_reading_outside = self.channel_1.value

        # Convert voltage readings to depth (in feet)
        depth_inside = (voltage_reading_inside - 0.075) / 0.092
        depth_outside = (voltage_reading_outside - 0.075) / 0.092

        # Convert depth values to pressure (in PSIG)
        water_pressure_inside = depth_inside * 0.433
        water_pressure_outside = depth_outside * 0.433  # Static pressure

        # Convert pressure values to Pascals
        pa_pressure_inside = water_pressure_inside * 6894.76
        pa_pressure_outside = water_pressure_outside * 6894.76

        # Calculate velocity using Bernoulli's equation
        velocity_squared = (2 * (pa_pressure_inside - pa_pressure_outside)) / self.water_density

        # Handle negative velocity squared cases
        # Handle negative velocity for reverse motion
        if velocity_squared < 0:
            pressure_velocity = -math.sqrt(abs(velocity_squared))  # Reverse flow
            print(f"Warning: Reverse flow: Velocity: {pressure_velocity:.2f} m/s")
        else:
            pressure_velocity = math.sqrt(velocity_squared)  # Normal forward flow

        return depth_inside, water_pressure_inside, pressure_velocity, depth_outside, water_pressure_outside, voltage_reading_inside, voltage_reading_outside, channel_reading_inside, channel_reading_outside

        #return depth_inside, water_pressure_inside, pressure_velocity, depth_outside, water_pressure_outside


    def log_data(self, interval=1):
        # Continuously log data at a specified interval
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            try:
                while True:
                    # Read sensor data
                    depth_inside, pressure_inside, velocity, depth_outside, pressure_outside, voltage_inside, voltage_outside, channel_inside, channel_outside = self.read_pressure()
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                    # Write data to CSV file
                    writer.writerow([timestamp, depth_inside, pressure_inside, velocity, depth_outside, pressure_outside, voltage_inside, voltage_outside, channel_inside, channel_outside])

                    # Print the recorded values to the console for real-time monitoring
                    print(f"{timestamp}, Depth Inside: {depth_inside:.2f}ft, Pressure Inside: {pressure_inside:.2f} PSIG, Velocity: {velocity:.2f} m/s, Depth Outside: {depth_outside:.2f}ft, Pressure Outside: {pressure_outside:.2f} PSIG")
                    
                    # Wait for the specified interval before recording next data point
                    time.sleep(interval)
            except KeyboardInterrupt:
                # Stop logging when user interrupts the process (Ctrl+C)
                print("Logging stopped.")

if __name__ == "__main__":
    sensor = PressureSensor()
    sensor.log_data()