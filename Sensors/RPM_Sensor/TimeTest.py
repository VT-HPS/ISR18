from gpiozero import Button
import time
print("Hi")
button = Button(4, False)
prevState = 0
prevTime = time.time()

while True:
    currentState = button.value
    if prevState != currentState and currentState == 1:
        duration = time.time() - prevTime
        rpm = (60000000 / duration)
        prevTime = time.time()
    else:
        rpm = 0
