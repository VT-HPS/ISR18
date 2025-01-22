from gpiozero import Button
import time
button = Button(23, False)
while True:
    print(button.value)
    time.sleep(0.01)
