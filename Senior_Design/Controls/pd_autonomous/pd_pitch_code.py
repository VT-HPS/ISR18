import pigpio

import pd_input as input
import pd_error_adjust as erradj

PWM_FREQ = 100

def main_loop(data_stream):
    """
    Runs autonomous controls to adjust fin pitch angles in response to depth and previous fin angles.
    This is a PD control system with basic proportional and derivative controls.

    Comment out pigpio/pwm stuff on local machines.

    Parameters:
    - data_stream: a list of tuple values
    """
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)

    # Get initial values
    Kp_pitch, Kd_pitch = input.get_init_gain("pitch")
    desired_depth, desired_angle_pitch = input.get_init_desired("pitch")

    prev_error = 0

    # Keep adjusting while data is coming in
    num_runs = 0
    for depth, angle_pitch in data_stream:
        # TODO: Figure out data getting to code via data_stream
        # Calculate error
        error, derror = erradj.calculate_error_pitch(desired_angle_pitch, angle_pitch, desired_depth, depth, prev_error)

        # Adjust pd parameters according to error
        Kp_pitch, Kd_pitch = erradj.adjust_pd_params(Kp_pitch, Kd_pitch, error, prev_error)

        WRITE_PERIOD = 200 # the system will write out_val.txt one out of every WRITE_PERIOD runs
        num_runs = num_runs % WRITE_PERIOD
        if (num_runs == 0):
            # TODO: complete a write_out function
            print(f"PITCH\nKp:\t{Kp_pitch}\nKd:\t{Kd_pitch}")

        fin_angle = erradj.pd_controller_action(Kp_pitch, Kd_pitch, error, derror)

        # print(fin_angle)
        pwm.set_PWM_dutycycle(PWM_PIN, erradj.fin_angle_to_dc(fin_angle))
        
        prev_error = error

        num_runs += 1

stream = []
for i in range(-50, 50):
    for j in range(-50, 50):
        stream.append((i, j))
        
main_loop(stream)