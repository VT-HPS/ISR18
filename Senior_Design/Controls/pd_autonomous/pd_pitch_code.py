# import pigpio

import pd_io as io
import pd_error_adjust as erradj

PWM_FREQ = 100

def main_loop(data_stream):
    """
    Runs autonomous controls to adjust fin pitch angles in response to depth and previous fin angles.
    This is a PD control system with basic proportional and derivative controls.

    When actually using this code, do the following:
        * Un-comment pigpio
        * Un-comment PWM section
        * Un-comment pwm set duty cycle
        * Remove print(fin_angle)

    Parameters:
    - data_stream: a list of tuple values
    """
    # PWM setup
    # pwm = pigpio.pi()

    # PWM_PIN = 18
    # pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    # pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    # pwm.set_PWM_range(PWM_PIN, 100)

    # Get initial values
    Kp_pitch, Kd_pitch = io.get_init_gain("pitch")
    desired_depth, desired_angle_pitch = io.get_init_desired("pitch")

    prev_error = 0

    # Keep adjusting while data is coming in
    num_runs = 0
    for depth, angle_pitch in data_stream:
        # Calculate error
        error, derror = erradj.calculate_error_pitch(desired_angle_pitch, angle_pitch, desired_depth, depth, prev_error)

        # Adjust pd parameters according to error
        Kp_pitch, Kd_pitch = erradj.adjust_pd_params(Kp_pitch, Kd_pitch, error, prev_error)
        prev_error = error

        # Write gain values every WRITE_PERIOD cycles
        WRITE_PERIOD = 200
        num_runs = num_runs % WRITE_PERIOD
        if (num_runs == 0):
            io.write_out(Kp_pitch, Kd_pitch, "pitch")

        # Transform change to fin angle
        fin_angle = erradj.pd_controller_action_pitch(Kp_pitch, Kd_pitch, error, derror)

        print(fin_angle)
        # pwm.set_PWM_dutycycle(PWM_PIN, erradj.fin_angle_to_dc(fin_angle))
        
        num_runs += 1

if __name__ == "__main__":
    # TODO: link data stream
    # main_loop(data_stream)

    # TEST THIS CODE AGAINST OLD if-statement VALUES
    for i in range(12, 18, 2):
        print(f"DEPTH = {i}")
        for j in range(14, -14, -4):
            main_loop([(i, j)])
        print()