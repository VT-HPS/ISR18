# import time
# import RPi.GPIO as GPIO

# # Define GPIO pin for RPM sensor
# RPM_SENSOR_PIN = 17  # Adjust this to match your wiring

# # Global variables matching Arduino code
# currentstateA = 0
# prevstateA = 0
# prevmillisA = 0
# rpmA = 0

# def rpm_value():
#     global currentstateA, prevstateA, prevmillisA, rpmA

#     currentstateA = GPIO.input(RPM_SENSOR_PIN)

#     if prevstateA != currentstateA:
#         if currentstateA == GPIO.HIGH:  
#             durationA = int(time.time() * 1000) - prevmillisA  
#             if durationA > 0:
#                 rpmA = 60000 // durationA  
#             prevmillisA = int(time.time() * 1000)

#     if (int(time.time() * 1000) - prevmillisA) >= 2000:
#         rpmA = 0

#     prevstateA = currentstateA 
#     print(f"RPM: {rpmA}") 

# def monitor_rpm(sensor_data_queue):
#     global rpmA

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(RPM_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     try:
#         while True:
#             rpm_value()  
#             if not sensor_data_queue.empty():
#                 latest_data = sensor_data_queue.get()
#             else:
#                 latest_data = {
#                     'depth': 0,
#                     'water_pressure': 0,
#                     'pressure_speed': 0,
#                     'battery_voltage': 0,
#                     'rpm': 0,
#                     'leak_status': 0,
#                     'temperature': 0
#                 }

#             latest_data['rpm'] = rpmA  
#             sensor_data_queue.put(latest_data)

#             time.sleep(0.01) 

#     except KeyboardInterrupt:
#         print("RPM monitoring stopped")
#     finally:
#         GPIO.cleanup() 


###########################################################################

### Ciruit test code:
import time
import RPi.GPIO as GPIO

# define GPIO pin for RPM sensor (test circuit)
RPM_SENSOR_PIN = 17  

# vars
currentstateA = 0
prevstateA = 0
prevmillisA = 0
rpmA = 0

def rpm_value():
    # reads circuit input and calc rpm
    global currentstateA, prevstateA, prevmillisA, rpmA

    # read RPMA sensor state
    currentstateA = GPIO.input(RPM_SENSOR_PIN)

    # ff there is a change in input
    if prevstateA != currentstateA:
        if currentstateA == GPIO.HIGH:  # LOW to HIGH transition
            durationA = int(time.time() * 1000) - prevmillisA  # time difference in ms
            if durationA > 0:
                rpmA = 60000 // durationA  # RPM calculation
            prevmillisA = int(time.time() * 1000)  # store time for next calculation

    # no pulse detected for 2 seconds, set RPM to 0
    if (int(time.time() * 1000) - prevmillisA) >= 2000:
        rpmA = 0

    prevstateA = currentstateA  # store this scan for next cycle
    print(f"RPM: {rpmA}")  # show real-time RPM

def main():
    # runs loop
    global rpmA

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RPM_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Press the test circuit button to simulate RPM sensor pulses.")
    print("Press CTRL+C to stop.\n")

    try:
        while True:
            rpm_value()  # read pulses and calc RPM
            time.sleep(0.01)  # 10ms delay

    except KeyboardInterrupt:
        print("\nRPM monitoring stopped.")
    finally:
        GPIO.cleanup()  

if __name__ == "__main__":
    main()

