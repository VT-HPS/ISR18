#!/usr/bin/python
#
#       This program includes a number of calculations to improve the
#       values returned from a BerryIMU. If this is new to you, it
#       may be worthwhile first to look at berryIMU-simple.py, which
#       has a much more simplified version of code which is easier
#       to read.
#
#
#       The BerryIMUv1, BerryIMUv2 and BerryIMUv3 are supported
#
#       This script is python 2.7 and 3 compatible
#
#       Feel free to do whatever you like with this code.
#       Distributed as-is; no warranty is given.
#
#       https://ozzmaker.com/berryimu/


import time
import math
import IMU
import datetime
import os
import sys
import pigpio

DEFAULT_SPEED = 0
ANGLE_0_PWM = 850
ANGLE_MAX_PWM = 2150
TRAVEL_RANGE_ANGLE = 130
PWM_FREQ = 100


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant


################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading value.

magXmin = -1116
magYmin = -2164
magZmin = 2272
magXmax = 1398
magYmax = 254
magZmax = 3839


'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''
############### END Calibration offsets #################


#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0




def kalmanFilterY ( accAngle, gyroRate, DT):
    y=0.0
    S=0.0

    global KFangleY
    global Q_angle
    global Q_gyro
    global y_bias
    global YP_00
    global YP_01
    global YP_10
    global YP_11

    KFangleY = KFangleY + DT * (gyroRate - y_bias)

    YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
    YP_01 = YP_01 + ( - DT * YP_11 )
    YP_10 = YP_10 + ( - DT * YP_11 )
    YP_11 = YP_11 + ( + Q_gyro * DT )

    y = accAngle - KFangleY
    S = YP_00 + R_angle
    K_0 = YP_00 / S
    K_1 = YP_10 / S

    KFangleY = KFangleY + ( K_0 * y )
    y_bias = y_bias + ( K_1 * y )

    YP_00 = YP_00 - ( K_0 * YP_00 )
    YP_01 = YP_01 - ( K_0 * YP_01 )
    YP_10 = YP_10 - ( K_1 * YP_00 )
    YP_11 = YP_11 - ( K_1 * YP_01 )

    return KFangleY

def kalmanFilterX ( accAngle, gyroRate, DT):
    x=0.0
    S=0.0

    global KFangleX
    global Q_angle
    global Q_gyro
    global x_bias
    global XP_00
    global XP_01
    global XP_10
    global XP_11


    KFangleX = KFangleX + DT * (gyroRate - x_bias)

    XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
    XP_01 = XP_01 + ( - DT * XP_11 )
    XP_10 = XP_10 + ( - DT * XP_11 )
    XP_11 = XP_11 + ( + Q_gyro * DT )

    x = accAngle - KFangleX
    S = XP_00 + R_angle
    K_0 = XP_00 / S
    K_1 = XP_10 / S

    KFangleX = KFangleX + ( K_0 * x )
    x_bias = x_bias + ( K_1 * x )

    XP_00 = XP_00 - ( K_0 * XP_00 )
    XP_01 = XP_01 - ( K_0 * XP_01 )
    XP_10 = XP_10 - ( K_1 * XP_00 )
    XP_11 = XP_11 - ( K_1 * XP_01 )

    return KFangleX

# Function that takes an angle and figures outs the approriate pwm in microseconds
def map_angle_to_pwm(angle):
    return math.floor((((ANGLE_MAX_PWM - ANGLE_0_PWM) / TRAVEL_RANGE_ANGLE) * angle) + ANGLE_0_PWM)

# Function that determines duty cycle based on pwm signal and current frequency
def pwm_to_dc(pwm_time):
    HZ_US = 1000000 # Conversion from 1 hertz to 1000000 microseconds
    return (pwm_time / (HZ_US / PWM_FREQ)) * 100

def map_value(value, from_min, from_max, to_min, to_max):
    # Map value from one range to another
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
kalmanX = 0.0
kalmanY = 0.0

a = datetime.datetime.now()

def readData():
    global a, gyroXangle, gyroYangle, gyroZangle, CFangleX, CFangleY, IMU, AA, RAD_TO_DEG, M_PI, magXmin, magXmax, magYmin, magYmax, magZmin, magZmax, G_GAIN

    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    #Apply compass calibration
    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2

    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    outputString = "Loop Time %5.2f " % ( LP )

    #Convert Gyro raw to degrees per second
    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN

    #Calculate the angles from the gyro.
    gyroXangle+=rate_gyr_x*LP
    gyroYangle+=rate_gyr_y*LP
    gyroZangle+=rate_gyr_z*LP

   #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0


    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
    CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle

    #Kalman filter used to combine the accelerometer and gyro values.
    kalmanY = kalmanFilterY(AccYangle, rate_gyr_y,LP)
    kalmanX = kalmanFilterX(AccXangle, rate_gyr_x,LP)


    #Calculate heading
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI

    #Only have our heading between 0 and 360
    # if heading < 0:
    #    heading += 360

    ####################################################################
    ###################Tilt compensated heading#########################
    ####################################################################
    #Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


    #Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))


    #Calculate the new tilt compensated values
    #The compass and accelerometer are orientated differently on the the BerryIMUv1, v2 and v3.
    #This needs to be taken into consideration when performing the calculations

    #X compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    else:                                                                #LSM9DS1
        magXcomp = MAGx*math.cos(pitch)-MAGz*math.sin(pitch)

    #Y compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)
    else:                                                                #LSM9DS1
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)

    pitch = pitch * 180/math.pi
    roll = roll * 180/math.pi


    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360

    return heading, pitch, roll

heading, pitch, roll = readData()
headingStart = heading
rollStart = roll
pitchStart = pitch

# Servo Setup
# Initialize pigpio
pi = pigpio.pi()

# Define GPIO pins connected to the servos
servo_gpio_pin_1 = 19
servo_gpio_pin_2 = 18

# Set servo ranges (MAX_min: 800, MAX_max: 2200)
servo_min_pulse = 900
servo_max_pulse = 2100

# Set PWM frequency (Hz)
pwm_frequency = 100

# Sleep time
sleep_time = 0.01

# Configure PWM frequency for both servos
pi.set_PWM_frequency(servo_gpio_pin_1, pwm_frequency)
pi.set_PWM_frequency(servo_gpio_pin_2, pwm_frequency)

prev_time = time.time()

try:
    while True:
        heading, pitch, roll = readData()
        heading = heading - headingStart
        if heading <= -180:
            heading += 360
        if heading >= 180:
            heading -= 360
        roll = roll - rollStart
        pitch = pitch - pitchStart
        outputString = "# Heading: %5.2f   roll: %5.2f    pitch: %5.2f" % (heading, roll, pitch)
        
        curr_time = time.time()
        
        mapped_pitch_pulse = map_value(roll, -60, 60, servo_min_pulse, servo_max_pulse)
        mapped_yaw_pulse = map_value(heading, -60, 60, servo_min_pulse, servo_max_pulse)
        
        if mapped_pitch_pulse < servo_min_pulse:
            mapped_pitch_pulse = servo_min_pulse
        elif mapped_pitch_pulse > servo_max_pulse:
            mapped_pitch_pulse = servo_max_pulse
            
        if mapped_yaw_pulse < servo_min_pulse:
            mapped_yaw_pulse = servo_min_pulse
        elif mapped_yaw_pulse > servo_max_pulse:
            mapped_yaw_pulse = servo_max_pulse
        
        if curr_time - prev_time > 0.2:
            print(outputString)
            print(mapped_pitch_pulse, mapped_yaw_pulse)
            pi.set_servo_pulsewidth(servo_gpio_pin_1, mapped_pitch_pulse)
            pi.set_servo_pulsewidth(servo_gpio_pin_2, mapped_yaw_pulse)
            prev_time = curr_time

except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pi.set_PWM_dutycycle(servo_gpio_pin_1, 0)  # Stop PWM for servo 1
    pi.set_PWM_dutycycle(servo_gpio_pin_2, 0)  # Stop PWM for servo 2
    pi.stop()  # Close pigpio connection



