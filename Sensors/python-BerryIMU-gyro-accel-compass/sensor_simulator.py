import time
import datetime
import random

def generate_random_data(min_val, max_val):
    return random.uniform(min_val, max_val)

while True:
    # Simulate accelerometer readings (replace with actual sensor ranges)
    ACCx = generate_random_data(-10, 10)
    ACCy = generate_random_data(-10, 10)
    ACCz = generate_random_data(-10, 10)

    # Simulate gyroscope readings (replace with actual sensor ranges)
    GYRx = generate_random_data(-500, 500)
    GYRy = generate_random_data(-500, 500)
    GYRz = generate_random_data(-500, 500)

    # Simulate magnetometer readings (replace with actual sensor ranges)
    MAGx = generate_random_data(-4800, 4800)
    MAGy = generate_random_data(-4800, 4800)
    MAGz = generate_random_data(-4800, 4800)

    # Simulate pressure sensor reading (replace with actual sensor range)
    pressure = generate_random_data(0, 5)  # Assuming 0 to 5 volts

    # Simulate button press (0 or 1)
    button_value = random.choice([0, 1])
    
    # Save the simulated sensor values to a file
    with open("sensor_data.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}, {ACCx}, {ACCy}, {ACCz}, {GYRx}, {GYRy}, {GYRz}, {MAGx}, {MAGy}, {MAGz}, {pressure}, {button_value}\n")

    # Print for debug
    print(f"Data saved: ACCx={ACCx}, ACCy={ACCy}, ACCz={ACCz}, GYRx={GYRx}, GYRy={GYRy}, GYRz={GYRz}, MAGx={MAGx}, MAGy={MAGy}, MAGz={MAGz}, pressure={pressure}, button={button_value}")

    time.sleep(0.5)  # Sleep for a bit to simulate sensor reading frequency