import time
import datetime
import os
from gpiozero import Button


def joe_rpm():
    moving_average_count = 5
    # RPM Buttons
    brpm1 = Button(23)
    brpm2 = Button(24)

    rpm1_prev_state = 0
    rpm2_prev_state = 0

    prevTime1 = time.time()
    prevTime2 = time.time()

    rpm1 = 0
    rpm2 = 0

    log_time = time.time()
    rpm1_10_time_entries = [time.time()]
    rpm2_10_time_entries = [time.time()]
    data_to_log = []

    while True:
        rpm1_state = brpm1.value
        rpm2_state = brpm2.value

        if rpm1_state != rpm1_prev_state:
            if rpm1_state == 1:
                time_secs = time.time()
                if (len(rpm1_10_time_entries) >= moving_average_count):
                    rpm1_10_time_entries.pop(0)
                duration = time_secs - rpm1_10_time_entries[0]
                rpm1_10_time_entries.append(time_secs)
                rpm1 = (60 / duration) * (len(rpm1_10_time_entries) - 1)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_to_log += f"Sensor1, {timestamp}"
        rpm1_prev_state = rpm1_state

        if rpm2_state != rpm2_prev_state:
            if rpm2_state == 1:
                time_secs = time.time()
                if (len(rpm2_10_time_entries) >= moving_average_count):
                    rpm2_10_time_entries.pop(0)
                duration = time_secs - rpm2_10_time_entries[0]
                rpm2_10_time_entries.append(time_secs)
                rpm2 = (60 / duration) * (len(rpm2_10_time_entries) - 1)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_to_log += f"Sensor2, {timestamp}"
        rpm2_prev_state = rpm2_state
        
        if (time.time() - log_time >= 10):
            with open(f"bulk_rpm_data.csv", "a") as f:
                for entry in data_to_log:
                    f.write(entry)
            print("Data logged")
            data_to_log = []
            log_time = time.time()
        

if __name__ == "__main__":
    # Define the file path with the run number
    sensor_file_path = os.path.join("/home/hps/ISR18/Combined_Stuff/Data_Logging_Files", f"bulk_rpm_data.csv")

    with open(sensor_file_path, "a") as f:
        f.write(f"RPM Number, Timestamp\n")
        print("Sensor data logged.")
    
    joe_rpm()
