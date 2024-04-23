import math

# TODO Implement error checking for "out of bounds" pitch, yaw, or depth

# Should all be less than 45 degrees
# All variables are in angular degrees
MAX_CONTROL_YAW = 15 # Maximum angle of the yaw based control surfaces
MAX_AUTO_YAW_ANGLE = 15 # Maximum angle which we want to try to maintain auto controls
MAX_CONTROL_PITCH = 15 # Maximum angle of the pitch based control surfaces
MAX_AUTO_PITCH_ANGLE = 15 # Maximum angle which we want to try to maintain auto controls, set 1 foot more expected

# Deviation of ideal depth to consider alternative parameters (FT)
IDEAL_DEPTH_DIFF = 0

def set_ideal_depth(depth):
    IDEAL_DEPTH_DIFF = depth

"""
Compute the pitch angle of the control surfaces given the current pitch angle

Args:
    pitch (float): current pitch of the submarine (degrees)
    depth (float): current depth of the submarine (feet)
    ideal_depth (float): ideal depth of the submarine

Returns:
    float: The required pitch of the control surfaces (degrees)
    
"""
def pitch_auto_control(pitch, depth, ideal_depth):
    if depth < ideal_depth - IDEAL_DEPTH_DIFF or pitch > MAX_AUTO_PITCH_ANGLE:
        return -MAX_CONTROL_PITCH
    elif depth > ideal_depth + IDEAL_DEPTH_DIFF or pitch < -MAX_AUTO_PITCH_ANGLE:
        return MAX_CONTROL_PITCH
    else:
        multiplyer = MAX_CONTROL_PITCH / math.sin(2 * MAX_AUTO_PITCH_ANGLE)
        return multiplyer * -math.sin(2 * pitch)

"""
Compute the yaw angle of the control surfaces given the current yaw angle

Args:
    yaw (float): current yaw of the submarine (degrees)

Returns:
    float: The required yaw of the control surfaces (degrees)
    
"""
def yaw_auto_control(yaw):

    # If the abs of yaw exceed the auto controls angle, just set to max controls angle
    if yaw > MAX_AUTO_YAW_ANGLE:
        return -MAX_CONTROL_YAW
    elif yaw < -MAX_AUTO_YAW_ANGLE:
        return MAX_CONTROL_YAW
    # Assume a sin(2*theta) distribution if inside this range
    else:
        multiplyer = MAX_CONTROL_YAW / math.sin(2 * MAX_AUTO_YAW_ANGLE)
        return multiplyer * -math.sin(2 * yaw)