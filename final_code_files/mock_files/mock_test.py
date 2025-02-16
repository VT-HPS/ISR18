import time

def test_queue_access(sensor_data_queue):
    # tries to grab data from queue
    print("testing queue access")

    try:
        while True:
            if not sensor_data_queue.empty():
                if not sensor_data_queue.empty():
                    data = list(sensor_data_queue.queue)[-1]  # peek at the latest entry
                    print(f"Mock Test: Queue Data Retrieved: {data}")
                else:
                    print("Mock Test: Queue is empty.")

                print(f"Mock Test: Queue Data Retrieved: {data}")  # print the values
            else:
                print("Mock Test: Queue is empty. Waiting for data")

            time.sleep(1)  # Check queue every second

    except KeyboardInterrupt:
        print("Test stopped.")

