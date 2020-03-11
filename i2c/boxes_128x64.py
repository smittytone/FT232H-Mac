#!/usr/bin/env python

# IMPORTS
import time
import sys
import board
import busio
import digitalio
from ssd1306_circuitpython import SSD1306OLED
from random import seed
from random import randint

# CONSTANTS
DELAY = 0.5

# FUNCTIONS
def make_rect():
    return (randint(-10, 137), randint(-10, 53), randint(10, 80), randint(10, 20))

# START
if __name__ == '__main__':
    # Set the random seed
    seed()

    # Set up I2C on the FT232H Breakout
    i2c = busio.I2C(board.SCL, board.SDA)

    # Set up the RST pin
    reset = digitalio.DigitalInOut(board.D7)
    reset.direction = digitalio.Direction.OUTPUT

    # Set up the OLED display
    display = SSD1306OLED(reset, i2c, 0x3D, 128, 64)

    # Draw boxes in a loop
    while True:
        r = randint(0, 100)
        if r == 50:
            display.clear()
        else:
            rect = make_rect()
            is_full = True if r > 50 else False
            display.rect(rect[0], rect[1], rect[2], rect[3], is_full)

        display.draw()
        time.sleep(DELAY)

# Exit on break
sys.exit(-1)
