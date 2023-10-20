from gpiozero import Button
import time
button = Button(2)
prevState = 0
prevTime = time.time()
rpm = 0

while True:
    currentState = button.value
    if prevState != currentState:
        if currentState == 1:
            duration = time.time() - prevTime
            rpm = (60 / duration)
            prevTime = time.time()
            print(rpm)
    prevState = currentState

    
