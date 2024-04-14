

# Initialize lists to store data
time_data = []
voltage_data = [0] * voltage_sample_size  # Initialize with zeros
voltage_data_index = 0

# Define states for each button
prevState1 =  0
prevState2 = 0

prevTime1 = time.time()
prevTime2 = time.time()

rpm1 = 0
rpm2 = 0



gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0


a = datetime.datetime.now()

def log_sensor_values():
    ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2 = read_sensor_values()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("sensor_data.txt", "a") as f:
        f.write(f"Timestamp, ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, Pressure1, Pressure2\n")
        f.write(f"{timestamp}, {ACCx}, {ACCy}, {ACCz}, {GYRx}, {GYRy}, {GYRz}, {MAGx}, {MAGy}, {MAGz}, {pressure1}, {pressure2}\n")
        print("Sensor data logged.")


log_button.wait_for_press()
log_sensor_values()

# Read the data from the logged sensor values and create adjusted variables
with open("sensor_data.txt", "r") as f:
    lines = f.readlines()
    headers = lines[0].strip().split(", ")
    values = lines[1].strip().split(", ")
    adjusted_values = []
    for header, value in zip(headers, values):
        if header != "Timestamp":
            original_name = header.split("_")[0]
            adjusted_name = f"{original_name}_adjusted"
            exec(f"{adjusted_name} = {value}")
            adjusted_values.append(f"{adjusted_name}: {value}")

# Print the adjusted variables
print("Adjusted Sensor Values:")
for adjusted_value in adjusted_values:
    print(adjusted_value)

# Subtract adjusted values from themselves to reset them to 0
for header in headers:
    if header != "Timestamp":
        original_name = header.split("_")[0]
        adjusted_name = f"{original_name}_adjusted"
        exec(f"{adjusted_name} -= {adjusted_name}")

while True:
    voltage_data[voltage_data_index] = ina260.voltage
    voltage_data_index = (voltage_data_index + 1) % voltage_sample_size
        
    if check_for_low_battery(voltage_data):
        low_battery_warning()
        
    if check_for_dead_battery(voltage_data):
        dead_battery_warning()

    currentState1 = brpm1.value
    if prevState1 != currentState1:
        if currentState1 == 1:
            duration = time.time() - prevTime1
            rpm1 = (60 / duration)
            prevTime1 = time.time()
            print(rpm1)
    prevState1 = currentState1

    currentState2 = brpm2.value
    if prevState2 != currentState2:
        if currentState2 == 1:
            duration = time.time() - prevTime2
            rpm2 = (60 / duration)
            prevTime2 = time.time()
            print(rpm2)
    prevState2 = currentState2

    #time.sleep(0.5)
    
    ACCx, ACCy, ACCz, GYRx, GYRy, GYRz, MAGx, MAGy, MAGz, pressure1, pressure2 = read_sensor_values()

    # Subtract adjusted values from sensor readings
    ACCx -= ACCx_adjusted
    ACCy -= ACCy_adjusted
    ACCz -= ACCz_adjusted
    GYRx -= GYRx_adjusted
    GYRy -= GYRy_adjusted
    GYRz -= GYRz_adjusted
    pressure1 -= Pressure1_adjusted
    pressure2 -= Pressure2_adjusted
    MAGx -= MAGx_adjusted
    MAGy -= MAGy_adjusted
    MAGz -= MAGz_adjusted

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
    gyroXangle=rate_gyr_x*LP
    gyroYangle=rate_gyr_y*LP
    gyroZangle=rate_gyr_z*LP

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

    outputString = "\n"

    if 1:                       #Change to '0' to stop showing the angles from the accelerometer
       outputString += "#  ACCX Angle %5.2f ACCY Angle %5.2f  #  " % (AccXangle, AccYangle)

    if 1:                       #Change to '0' to stop  showing the angles from the gyro
       outputString +="\n# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)

    if 1:                       #Change to '0' to stop  showing the angles from the complementary filter
        outputString +="\n#  CFangleX Angle %5.2f   CFangleY Angle %5.2f  #" % (CFangleX,CFangleY)

    if 1:                       #Change to '0' to stop  showing the heading
        outputString +="\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)
    
    if 1:
        outputString +="\t# PRESSURE %5.2f#" % (pressure)

    if 1:
        outputString +="\t# RPM1 %5.2f RPM2 %5.2f#" % (rpm1,rpm2)

    print(outputString, end='')
