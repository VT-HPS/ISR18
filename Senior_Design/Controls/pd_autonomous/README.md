# Autonomous PD Controller
An autonomous control system that factors proportional and derivative action.
IMPORTANT: Read "Establishing Values" section.

## Structure:

Pitch and yaw code are implemented separately to allow for independent function across independent axes.  However, their functionality is largely the same.  Both reactions consider the respective pitch and yaw angles of the submarine itself.  However, pitch reaction considers depth as well.

## Methods:

Reaction is carried out by altering fin angles.  This is done using the pigpio library.

Kp represents the gain of proportional control, while Kd represents the gain of derivative control.  Essentially, these are values which weight the proportional/derivative estimates for reaction.  Because adjustments of pitch and yaw occur independent of each other, these gain values differ for each dimension.

Derivative, in this use case, is simply the change in values between iterations.

## Values (Storage & Retrieval):

Initial values are stored in init_val.txt, separated by commas according to the following format:

Kp_pitch, Kd_pitch, desired_depth, desired_angle_pitch, Kp_yaw, Kd_yaw, desired_angle_yaw

Desired values should not be altered.  They should always be:
* desired_depth = 15
* desired_angle_pitch = 0
* desired_angle_yaw = 0

Periodically (every 1 / WRITE_PERIOD cycles), the system outputs the current Kp and Kd for each dimension.  WRITE_PERIOD is currently set to 200, meaning that this print-out occurs every 200 cycles (we estimate every 2 seconds).  Increase this value to save computational resources, decrease it to increase the rate at which we save our values.  Currently, writing is done by printing out the values.  TODO: complete a write_out function that writes these values to a text file instead.

## Establishing Values:

The user must establish the following values for proper usage...

### PITCH:
* w_pe: the weighting of pitch angle error
* w_de: the weighting of depth error

These weightings act against each other, trading off the response of the system to changes in depth and pitch angle.  As such, sensitivity can be changed.  Because small changes in pitch angle can have a huge effect on the system, the user may wish to make w_pe much larger than w_de.  These weighting values can be found in calculate_error_pitch() in pd_error_adjust.py

### YAW:
* w_ye: the weighting of yaw angle error
This value can be found in the (yet uncreated) calculate_error_yaw() in pd_error_adjust.py

### PITCH AND YAW:
These three weightings should be altered to convert units.  That is, if we had just used 1 for these weightings, the error values would be huge and Kp, and Kd would have to be changed.

Essentially, these weightings combine mathematically with Kp and Kd. (With the exception that w_pe and w_de add fine-tuning tradeoffs between different types of error.)  However, these weightings should be altered so that the units don't have an outsized effect on the learning rate.

### LEARNING RATE
learning_rate governs the rate at which Kp and Kd adjust to changes over time.