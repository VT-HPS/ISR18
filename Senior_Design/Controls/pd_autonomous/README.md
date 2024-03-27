# Autonomous PD Controller
An autonomous control system that factors proportional and derivative action.

## Structure:

Pitch and yaw code are implemented separately to allow for independent function across independent axes.  However, their functionality is largely the same.  Both reactions consider the respective pitch and yaw angles of the submarine itself.  However, pitch reaction considers depth as well.

## Methods:

Reaction is carried out by altering fin angles.  This is done using the pigpio library.

Kp represents the gain of proportional control, while Kd represents the gain of derivative control.  Essentially, these are values which weight the proportional/derivative estimates for reaction.  Because adjustments of pitch and yaw occur independent of each other, these gain values differ for each dimension.

Calculations for calculating error and adjustign values is ongoing.

## Values (Storage & Retrieval):

Initial values are stored in init_val.txt, separated by commas according to the following format:

Kp_pitch, Kd_pitch, desired_depth, desired_angle_pitch, Kp_yaw, Kd_yaw, desired_angle_yaw

Desired values should not be altered.  They should always be:
* desired_depth = 15
* desired_angle_pitch = 0
* desired_angle_yaw = 0

On each cycle, the current values are then written to out_val.txt according to the same format.  As such, these out values can be plugged direclty into the next run after the "learning" phase, by simply renaming and overwriting the old init_val.txt file.