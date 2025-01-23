# Pseudo-code for HPS Submarine Steering Guidance

# Need code to start running when Pi is booted

# Initial Variables
buttonPressed = False

# Overall Loop
while True:
    
    button = read some pin

    if button:

        buttonPressed = not buttonPressed
        # Wait so that button is not spammed

    if on: # will always need to run, maybe take outside of if loop
        # Measure battery voltage, current
        # Measure temperature sensor
        # Check leak sensor
        if water:
            # Go into some error mode and shut off components
            # Turn outside lights on solid in error mode
            # Wait in this loop
        if batteryLow:
            # Display warning on screen (small), turn an LED on inside the ECAN


    if not buttonPressed:

        # Screen says "Standby"
        # Turn light on dimly

    
    if buttonPressed:
        # Turn on light brightly
        # Read RPM sensor
        # Read IMU sensor
        # Read Pressure Sensor
        # Log data

        # Adjust GUI based on gathered data
        # If there is any blatantly incorrect data, create an error message
    
    # wait a little based on desired loop time (so lights blink)
    # turn lights off
    # wait a little based on desired loop time (so lights blink)


