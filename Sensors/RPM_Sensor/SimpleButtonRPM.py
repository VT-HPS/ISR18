from gpiozero import Button
import time
import threading

button = Button(2)
prevState = 0
prevTime = time.time()
rpm = 0

def button_rpm():
    while True:
        currentState = button.value
        if prevState != currentState:
            if currentState == 1:
                duration = time.time() - prevTime
                rpm = (60 / duration)
                prevTime = time.time()
                time.sleep(0.01)
        #print(f"raw rpm: {rpm}")
        prevState = currentState

def read_rpm():
    while True:
        time.sleep(1)
        print(rpm)

if __name__ == "__main__":
    t1 = threading.Thread(target=button_rpm, daemon=True)
    t2 = threading.Thread(target=read_rpm, daemon=True)

    t1.start()
    t2.start()
