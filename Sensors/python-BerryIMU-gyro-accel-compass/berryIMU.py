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


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant


################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading value.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0


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


# Working variables for PID
last_time = 0
input_yaw = 0.0
input_pitch = 0.0
output_yaw = 0.0
output_pitch = 0.0
setpoint_yaw = 0.0
setpoint_pitch = 0.0
err_sum_yaw = 0.0
err_sum_pitch = 0.0
last_err_yaw = 0.0
last_err_pitch = 0.0
kp_yaw = 0.0
ki_yaw = 0.0
kd_yaw = 0.0
kp_pitch = 0.0
ki_pitch = 0.0
kd_pitch = 0.0

def compute():
    global last_time, input_yaw, input_pitch, output_yaw, output_pitch, setpoint_yaw, setpoint_pitch
    global err_sum_yaw, err_sum_pitch, last_err_yaw, last_err_pitch, kp_yaw, ki_yaw, kd_yaw, kp_pitch, ki_pitch, kd_pitch

    # Get current time in milliseconds
    now = time.time() * 1000  # Current time in milliseconds
    time_change = (now - last_time) / 1000.0  # Convert to seconds

    # Compute yaw PID terms
    error_yaw = setpoint_yaw - input_yaw
    err_sum_yaw += error_yaw * time_change
    ##d_err_yaw = (error_yaw - last_err_yaw) / time_change if time_change > 0 else 0.0
    output_yaw = kp_yaw * error_yaw + ki_yaw * err_sum_yaw + kd_yaw ## * d_err_yaw

    # Compute pitch PID terms
    error_pitch = setpoint_pitch - input_pitch
    err_sum_pitch += error_pitch * time_change
    ## d_err_pitch = (error_pitch - last_err_pitch) / time_change if time_change > 0 else 0.0
    output_pitch = kp_pitch * error_pitch + ki_pitch * err_sum_pitch + kd_pitch ## * d_err_pitch


    # Update previous errors for next cycle
    last_err_yaw = error_yaw
    last_err_pitch = error_pitch
    last_time = now

def set_tunings(Kp_yaw, Ki_yaw, Kd_yaw, Kp_pitch, Ki_pitch, Kd_pitch):
    global kp_yaw, ki_yaw, kd_yaw, kp_pitch, ki_pitch, kd_pitch
    kp_yaw = Kp_yaw
    ki_yaw = Ki_yaw
    kd_yaw = Kd_yaw
    kp_pitch = Kp_pitch
    ki_pitch = Ki_pitch
    kd_pitch = Kd_pitch



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

while True:


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
    if heading < 0:
        heading += 360





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




    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360


    ##################### END Tilt Compensation ########################



    if 0:                       #Change to '0' to stop showing the angles from the accelerometer
        outputString += "#  ACCX Angle %5.2f ACCY Angle %5.2f  #  " % (AccXangle, AccYangle)

    if 0:                       #Change to '0' to stop  showing the angles from the gyro
        outputString +="\t# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)

    if 0:                       #Change to '0' to stop  showing the angles from the complementary filter
        outputString +="\t#  CFangleX Angle %5.2f   CFangleY Angle %5.2f  #" % (CFangleX,CFangleY)
        with open("cfangle.txt", "a") as f:
            print(outputString, file=f)
            ##print("I have a question.", file=f)
        print(outputString)


    if 0:                       #Change to '0' to stop  showing the heading
        outputString +="\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)

    if 0:                       #Change to '0' to stop  showing the angles from the Kalman filter
        outputString +="# kalmanX %5.2f   kalmanY %5.2f #" % (kalmanX,kalmanY)


    # Example usage:
    # Set tunings for yaw and pitch
    set_tunings(Kp_yaw=1.0, Ki_yaw=0.1, Kd_yaw=0.01, Kp_pitch=1.0, Ki_pitch=0.1, Kd_pitch=0.01)

    # Simulating sensor values (yaw and pitch angles)
    input_yaw = 45.0  # Current yaw angle (degrees)
    input_pitch = math.asin(accXnorm)  # Current pitch angle (degrees)

    # Desired setpoints for yaw and pitch
    setpoint_yaw = 90.0  # Desired yaw angle (degrees)
    setpoint_pitch = 0.0  # Desired pitch angle (degrees)

    # Run the PID computation
    compute()

    # Output the results for yaw and pitch
    #print(f"PID Output for Yaw: {output_yaw}")
    print(f"PID Output for Pitch: {output_pitch}")


    #slow program down a bit, makes the output more readable
    time.sleep(0.03)
