import numpy as np
import matplotlib.pyplot as plt

import sys, os
# Get the directory path of py2.py
current_dir = os.path.dirname(__file__)

# Construct the path to py1.py relative to py2.py
relative_path = os.path.join(current_dir, '..', 'Combined_Stuff')
sys.path.append(relative_path)

from Autonomous_Reactive import pitch_auto_control, yaw_auto_control

# CONSTANTS
START_YAW = 0
DEV_YAW = 0.2
START_PITCH = 0
DEV_PITCH = 0.2
START_DEPTH = 15
DEV_DEPTH = 0.1
IDEAL_DEPTH = 15

DIVIDER = 10

def generate_data(num_points, ideal_depth):
    """
    Generate pseudo-random data for controlling pitch and yaw of a submarine.

    Args:
        num_points (int): The number of data points to generate.
        ideal_depth (float): The ideal depth of the submarine.

    Returns:
        tuple: A tuple containing two NumPy arrays: one for pitch and one for yaw.
    """
    pitch_data = []
    yaw_data = []
    depth_data = []

    pitch = START_PITCH  # Initial pitch angle
    yaw = START_YAW  # Initial yaw angle
    depth = START_DEPTH # Initial depth
    for _ in range(num_points):

        # Estimate change to depth
        depth -= pitch_auto_control(pitch, depth, IDEAL_DEPTH) / DIVIDER

        # Update pitch and yaw using control functions
        pitch += pitch_auto_control(pitch, depth, IDEAL_DEPTH) / DIVIDER
        yaw += yaw_auto_control(yaw) / DIVIDER

        # Append to data arrays
        pitch_data.append(pitch)
        yaw_data.append(yaw)
        depth_data.append(depth)

        # Do a random modification
        pitch += np.random.uniform(-DEV_PITCH, DEV_PITCH)
        yaw += np.random.uniform(-DEV_YAW, DEV_YAW)
        depth += np.random.uniform(-DEV_DEPTH, DEV_DEPTH)

    return np.array(pitch_data), np.array(yaw_data), np.array(depth_data)

def plot_data(pitch_data, yaw_data, depth_data):
    """
    Plot the generated pitch and yaw data.

    Args:
        pitch_data (ndarray): NumPy array containing pitch data.
        yaw_data (ndarray): NumPy array containing yaw data.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(pitch_data, label='Pitch', color='blue')
    plt.plot(yaw_data, label='Yaw', color='red')
    plt.plot(depth_data, label='Depth', color='green')
    plt.xlabel('Time')
    plt.ylabel('Angle (degrees) / Depth (Feet)')
    plt.title('Pitch, Yaw, and Depth Control of Submarine')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    num_points = 100
    ideal_depth = 100  # Assign the ideal depth here
    pitch_data, yaw_data, depth_data = generate_data(num_points, ideal_depth)
    plot_data(pitch_data, yaw_data, depth_data)
