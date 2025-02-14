# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT


def read_temp(sensor):
    # Create sensor object, communicating over the board's default I2C bus
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    
    return sensor.temperature

def read_humidity():
     # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C() # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    sensor = adafruit_sht31d.SHT31D(i2c)
    
    return sensor.relative_humidity