if __name__ == "__main__":

    # Set GPIO mode
    pwm = pigpio.pi()

    # Set PWM pin
    PWM_PIN = 18
    pwm.set_mode(PWM_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(PWM_PIN, PWM_FREQ)
    pwm.set_PWM_range(PWM_PIN, 100)

    for depth_angle in data_tuples:
        depth = depth_angle[0]
        pitch_angle = depth_angle[1]

        print(depth, pitch_angle)
        
        if (depth < 13 and pitch_angle > 12):
            print("1")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 13 and pitch_angle > 8):
            print("2")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-13))
        elif (depth < 13 and pitch_angle > 4):
            print("3")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-11))
        elif (depth < 13 and pitch_angle > 0):
            print("4")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-9))
        elif (depth < 13 and pitch_angle > -4):
            print("5")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-4))
        elif (depth < 13 and pitch_angle > -8):
            print("6")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 13 and pitch_angle > -12):
            print("7")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 13 and pitch_angle < -12):
            print("8")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(7))
        elif (depth < 15 and pitch_angle > 12):
            print("9")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-15))
        elif (depth < 15 and pitch_angle > 8):
            print("10")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 15 and pitch_angle > 4):
            print("11")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-6))
        elif (depth < 15 and pitch_angle > 0):
            print("12")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth < 15 and pitch_angle > -4):
            print("13")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 15 and pitch_angle > -8):
            print("14")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(3))
        elif (depth < 15 and pitch_angle > -12):
            print("15")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(8))
        elif (depth < 15 and pitch_angle < -12):
            print("16")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle > 12):
            print("17")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-10))
        elif (depth < 17 and pitch_angle > 8):
            print("18")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-8))
        elif (depth < 17 and pitch_angle > 4):
            print("19")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-3))
        elif (depth < 17 and pitch_angle > 0):
            print("20")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth < 17 and pitch_angle > -4):
            print("21")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth < 17 and pitch_angle > -8):
            print("22")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(6))
        elif (depth < 17 and pitch_angle > -12):
            print("23")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(10))
        elif (depth < 17 and pitch_angle < -12):
            print("24")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))
        elif (depth > 17 and pitch_angle > 12):
            print("25")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-7))
        elif (depth > 17 and pitch_angle > 8):
            print("26")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(-2))
        elif (depth > 17 and pitch_angle > 4):
            print("27")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(0))
        elif (depth > 17 and pitch_angle > 0):
            print("28")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(2))
        elif (depth > 17 and pitch_angle > -4):
            print("29")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(9))
        elif (depth > 17 and pitch_angle > -8):
            print("30")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(11))
        elif (depth > 17 and pitch_angle > -12):
            print("31")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(13))
        elif (depth > 17 and pitch_angle < -12):
            print("32")
            pwm.set_PWM_dutycycle(PWM_PIN, fin_angle_to_dc(15))
