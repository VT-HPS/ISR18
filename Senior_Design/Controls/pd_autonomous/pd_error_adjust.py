from typing import Tuple

num_runs = 0

"""
Functions for calculating error, adjusting parameters, and writing new values.
"""

def calculate_error_pitch(
    depth: float,
    angle_pitch: float,
    desired_depth: float,
    desired_angle_pitch: float,
    previous_error: float
) -> Tuple[float, float]:
    """
    This function acts along the pitch dimension only.

    It calculates the error under the current conditions compared to the desired conditions.
    It also returns the derivative of the error, which is the difference between consecutive errors.

    Currently, the function does not weight differences in pitch and depth errors differently.
    This raises the issue of one dominating the other, or units otherwise having an outsized role.

    NOTE This function contains two weightings which are set by the user: w_de and w_pe!
    These weightings can be altered to have the system react more to error in depth vs angle_pitch.
    TODO: Adjust these weightings (they're naively set at the moment).

    Parameters:
    - depth: current depth of sub
    - angle_pitch: current pitch angle of sub
    - desired_depth: desired depth of sub
    - desired_angle_pitch: desired pitch angle of sub

    Returns a tuple of the following:
    - The error value associated with the current positioning,
    - The derivative of the error
    """
    # Weightings directly alter how much error along depth and angle_pitch contribute to error
    w_de = 0.01 # TODO: adjust these weightings
    w_pe = 0.01

    depth_error = w_de * (desired_depth - depth)
    angle_pitch_error = w_pe * (desired_angle_pitch - angle_pitch) # TODO: nonlinear transformation

    error = depth_error + angle_pitch_error
    derror = error - previous_error

    return (error, derror)


def calculate_error_yaw(
    desired_angle_yaw: float,
    angle_yaw: float,
    prev_error: float
) -> Tuple[float, float]:
    """
    This is the sister function to calulcate_error_pitch.  That is, it functions the same,
    but without consideration to depth.

    Changes made to one function should be considered in changes to the other.

    See sister documentation for more info.
    """
    w_ye = 0.01 # TODO: adjust this weighting

    error = w_ye * (desired_angle_yaw - angle_yaw)
    derror = error - prev_error

    return (error, derror)


def adjust_pd_params(
    Kp: float,
    Kd: float,
    error: float,
    derror: float
) -> Tuple[float, float]:
    """
    Adjusts the Kp and Kd in response to the current error and its derivative.
    Greater error's (and derror's) result in greater changes to Kp and Kd.

    NOTE This function contains one weighting to be set by the user: learning_rate!
    learning_rate can be altered to directly control the rate at which
    the system adjusts Kp and Kd in response to errors.
    TODO: Adjust learning_rate (it is naively set at the moment).

    Parameters:
    - Kp: the proportional gain value (weighting of response to proportional change in error)
    - Kd: the derivative gain value (weighting of response to derivative change in error)
    - error: the error (weighted for pitch; unweighted for yaw)
    - derror: the difference betwee this and the previous errors (simplified derivative)

    Returns a tuple of the following:
    - The new proportional gain (Kp)
    - The new derivative gain (Kd)
    """
    # Weighting directly alters the rate at which the system adjusts Kp and Kd in response to error
    learning_rate = 0.01 # TODO: adjust learning rate to be reasonable against Kp and Kd values

    Kp_new = Kp + (learning_rate * error)
    Kd_new = Kd + (learning_rate * derror)

    return Kp_new, Kd_new


def pd_controller_action_pitch(
    Kp: float,
    Kd: float,
    error: float,
    derror: float
) -> float:
    """
    Calculates the control action (fin angle) in response to error and derror.
    Bounds the control action by [-15, 15] degrees.

    Parameters:
    - Kp: the proportional gain value (weighting of response to proportional change in error)
    - Kd: the derivative gain value (weighting of response to derivative change in error)
    - error: the error (weighted for pitch; unweighted for yaw)
    - derror: the difference betwee this and the previous errors (simplified derivative)

    Returns:
    - The angle to which the fin should be set to error-correct
    """
    weighted_error = (Kp * error) + (Kd * derror)

    # Transforming simple weighted error into the angle
    control_action = ((22 / 0.2652) * (weighted_error - 0.143169)) - 15 # TODO: apply nonlinear transformation function
                                                                        # or, at least, readjust weightings according to adjusted values

    fin_angle = max(-15, min(15, control_action))
    return fin_angle


def pd_controller_action_yaw(
    Kp: float,
    Kd: float,
    error: float,
    derror: float
) -> float:
    """
    Sister function to pd_controller_action_pitch.

    This function uses different transformation functions.
    """
    weighted_error = (Kp * error) + (Kd * derror)

    control_action = (30 / .28) * weighted_error

    fin_angle = max(-15, min(15, control_action))
    return fin_angle


"""
Functions to convert desire fin_angle to an actionable duty cycle.
"""
import argparse
import math

DEFAULT_SPEED = 0
ANGLE_0_PWM = 900
ANGLE_MAX_PWM = 2100
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100

CURRENT_FIN_ANGLE = 0
MAX_FIN_ONE_DIR = 16.25

DEPTH_RAND_TRACK = 15
DEPTH_READING_PLACEHOLDER = 15

# Argument parsing function
def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", type=str, required=True, help=f"Data that should be used to test the positions of the motor, should be in the form of a list of tuples")
    return parser.parse_args()

# Function that takes a fin angle and determines the appropriate motor angle where the middle is half the full travel range
def map_fin_to_motor(fin_angle):
    return (fin_angle * 4) + (TRAVEL_RANGE_ANGLE / 2)

# Function that takes an motor angle and figures outs the approriate pwm in microseconds
def map_angle_to_pwm(angle):
    return math.floor((((ANGLE_MAX_PWM - ANGLE_0_PWM) / TRAVEL_RANGE_ANGLE) * angle) + ANGLE_0_PWM)

# Function that determines duty cycle based on pwm signal and current frequency
def pwm_to_dc(pwm_time):
    HZ_US = 1000000 # Conversion from 1 hertz to 1000000 microseconds
    return (pwm_time / (HZ_US / PWM_FREQ)) * 100

def fin_angle_to_dc(fin_angle):
    motor_angle = map_fin_to_motor(fin_angle)
    angle_pwm = map_angle_to_pwm(motor_angle)
    return pwm_to_dc(angle_pwm)