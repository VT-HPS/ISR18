import time
from gpiozero import Button

# RPM Buttons
brpm1 = Button(23)
brpm2 = Button(24)

rpmPrevState1 = 0
rpmPrevState2 = 0

rpmCurrentState1 = 0
rpmCurrentState2 = 0

prevTime1 = time.time()
prevTime2 = time.time()

rpm1 = 0
rpm2 = 0

def monitor_RPM():
    global rpm1, rpm2
    while True:
        rpmCurrentState1 = brpm1.value
        if rpmPrevState1 != rpmCurrentState1:
            if rpmCurrentState1 == 1:
                duration = time.time() - prevTime1
                rpm1 = (60 / duration)
                prevTime1 = time.time()
                print(rpm1)
        rpmPrevState1 = rpmCurrentState1

        rpmCurrentState2 = brpm2.value
        if rpmPrevState2 != rpmCurrentState2:
            if rpmCurrentState2 == 1:
                duration = time.time() - prevTime2
                rpm2 = (60 / duration)
                prevTime2 = time.time()
                print(rpm2)
        rpmPrevState2 = rpmCurrentState2

def get_rpm():
    return rpm1, rpm2