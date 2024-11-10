import time
import board
import adafruit_ina260
import matplotlib.pyplot as plt

i2c = board.I2C()  # uses board.SCL and board.SDA
ina260 = adafruit_ina260.INA260(i2c)

# Initialize lists to store data
time_data = []
voltage_data = []

# Open a text file for writing data
with open("battery_data.txt", "w") as file:
    file.write("Timestamp (s), Current (mA), Voltage (V), Power (mW)\n")
    start_time = time.time()  # Record the start time

    while True:
        try:
            # Append current timestamp and measurements to respective lists
            timestamp = time.time() - start_time
            current = ina260.current
            voltage = ina260.voltage
            power = ina260.power
            time_data.append(timestamp)
            voltage_data.append(voltage)

            # Print and write to file
            print(
                "Time: %.2f s Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
                % (timestamp, current, voltage, power)
            )
            file.write("%.2f, %.2f, %.2f, %.2f\n" % (timestamp, current, voltage, power))

            # Plot voltage over time
            plt.plot(time_data, voltage_data)
            plt.xlabel('Time (Sec)')
            plt.ylabel('Voltage (V)')
            plt.title('Voltage Over Time')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.draw()
            plt.pause(1)  # Pause for 1 second between updates

        except KeyboardInterrupt:
            # Save the final plot when interrupted by the user
            plt.savefig('voltage_plot.png')
            print("Program stopped by user. Saving final plot as 'voltage_plot.png'.")
            break
