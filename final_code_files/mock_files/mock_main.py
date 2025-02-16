import threading
import time
import mock_rpm
import mock_sensor_manager
import mock_gui
import mock_test
from queue import Queue

def main():
    sensor_data_queue = Queue()

    # Start sensor manager thread
    sensor_thread = threading.Thread(target=mock_sensor_manager.manage_sensors, daemon=True, args=(sensor_data_queue,))
    sensor_thread.start()

    # Start RPM monitoring thread
    rpm_thread = threading.Thread(target=mock_rpm.monitor_rpm, daemon=True, args=(sensor_data_queue,))
    rpm_thread.start()

    # Wait until the queue has at least one entry
    print("Mock Main: Waiting for sensor data...")
    while sensor_data_queue.empty():
        time.sleep(0.5)  # Wait for sensors to populate data

    print("Mock Main: Sensor data received. Starting GUI...")

    # Start queue test in a separate thread
    test_thread = threading.Thread(target=mock_test.test_queue_access, daemon=True, args=(sensor_data_queue,))
    test_thread.start()

    # Start GUI
    app = mock_gui.SpeedDepthHeadingGauges(sensor_data_queue)
    app.mainloop()

if __name__ == "__main__":
    main()
