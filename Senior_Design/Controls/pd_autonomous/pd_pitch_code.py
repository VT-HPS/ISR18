import pd_input as input

# Get initial & desired values for pitch
Kp_pitch, Kd_pitch = input.get_init_gain("pitch")
desired_depth, desired_angle_pitch = input.get_init_desired("pitch")

