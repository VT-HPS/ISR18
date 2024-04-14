if __name__ == "__main__":
    # Arguments
    args = parse_cli()
    data_list = parse_list(args.data)

    # Set GPIO mode
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)

    for yaw_angle in data_list:

        print(yaw_angle)

        if (yaw_angle > 12):
            print("1")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (yaw_angle > 8):
            print("2")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (yaw_angle > 4):
            print("3")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-5))
        elif (yaw_angle > 0):
            print("4")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (yaw_angle == 0):
            print("5")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (yaw_angle > -4):
            print("6")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (yaw_angle > -8):
            print("7")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(5))
        elif (yaw_angle > -12):
            print("8")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (yaw_angle < -12):
            print("9")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))
        


        