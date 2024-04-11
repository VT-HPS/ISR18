# import pigpio

import pd_io as io
import pd_error_adjust as erradj

PWM_FREQ = 100

def main_loop(data_stream):
    """
    Runs autonomous controls to adjust fin yaw angles in response to previous fin angles.
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
    Kp_yaw, Kd_yaw = io.get_init_gain("yaw")
    desired_angle_yaw = io.get_init_desired("yaw")

    prev_error = 0

    # Keep adjusting while data is coming in
    num_runs = 0
    for angle_yaw in data_stream:
        # Calculate error
        error, derror = erradj.calculate_error_yaw(desired_angle_yaw, angle_yaw, prev_error)

        # Adjust pd parameters according to error
        Kp_yaw, Kd_yaw = erradj.adjust_pd_params(Kp_yaw, Kd_yaw, error, prev_error)
        prev_error = error

        # Write gain values every WRITE_PERIOD cycles
        WRITE_PERIOD = 200
        num_runs = num_runs % WRITE_PERIOD
        if (num_runs == 0):
            io.write_out(Kp_yaw, Kd_yaw, "yaw")

        # Transform change to fin angle
        fin_angle = erradj.pd_controller_action_yaw(Kp_yaw, Kd_yaw, error, derror)

        print(fin_angle)
        # pwm.set_PWM_dutycycle(PWM_PIN, erradj.fin_angle_to_dc(fin_angle))
        
        num_runs += 1

if __name__ == "__main__":
    # TODO: link data stream
    # main_loop(data_stream)

    # TEST THIS CODE AGAINST OLD if-statement VALUES
    for i in range(13, 0, -4):
        print(f"angle: {i}")
        main_loop([i])

    print("angle: 0")
    main_loop([0])
    
    for i in range(-1, -14, -4):
        print(f"angle: {i}")
        main_loop([i])