from gpiozero import Button
import time
print("Hi")
button = Button(4, False)
while True:
    print(button.value)
    time.sleep(0.3)