import time
import random

# vars
currentstateA = 0
prevstateA = 0
prevmillisA = 0
rpmA = 0

def rpm_value():
    # mock environment ( makes random val for pulses)
    global currentstateA, prevstateA, prevmillisA, rpmA

    # simulating a random pulse every 500ms to 2000ms
    durationA = random.randint(500, 2000)

    # sim pulse logic
    currentstateA = 1 if random.random() > 0.5 else 0  # random HIGH/LOW

    if prevstateA != currentstateA:  # simulate state change
        if currentstateA == 0:  # LOW to HIGH transition
            rpmA = 60000 // durationA  # RPM calc
            prevmillisA = int(time.time() * 1000)  # time for next calc

    # sim 2-sec timeout to set RPM zero
    if (int(time.time() * 1000) - prevmillisA) >= 2000:
        rpmA = 0

    prevstateA = currentstateA  # state for next cycle
    print(f"Mock RPM: {rpmA}")  # debugging output

def monitor_rpm(sensor_data_queue):
    global rpmA
    try:
        while True:
            rpm_value()  # sim RPM readings

            # update queue with fake RPM value
            if not sensor_data_queue.empty():
                latest_data = sensor_data_queue.get()
            else:
                latest_data = {
                    'depth': 0,
                    'water_pressure': 0,
                    'pressure_speed': 0,
                    'battery_voltage': 0,
                    'rpm': 0,
                    'leak_status': 0,
                    'temperature': 0
                }

            latest_data['rpm'] = rpmA  # update RPM 
            sensor_data_queue.put(latest_data)

            time.sleep(0.5)  # sim update rate

    except KeyboardInterrupt:
        print("Mock RPM monitoring stopped")
