#!/usr/bin/env python

# IMPORTS
import time
import board
import busio
import adafruit_mcp9808
from htk1633segment_circuitpython import HT16K33Segment

# CONSTANTS
DELAY = 1.0

# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    # and instantiate the display
    i2c = busio.I2C(board.SCL, board.SDA)
    mcp = adafruit_mcp9808.MCP9808(i2c)
    display = HT16K33Segment(i2c)

    while True:
        # Convert 'count' into a float string with two decimal
        # places, padding with initial zeroes as necessary
        reading_temp = mcp.temperature
        display_temp = "{:.2f}".format(reading_temp)
        if reading_temp >= 0 and len(display_temp) < 5:
            display_temp = "0" + display_temp

        # Display 'temp'
        display.set_char(display_temp[0], 0)
        # 'True' to add a decimal point after this digit
        display.set_char(display_temp[1], 1, True)
        display.set_char(display_temp[3], 2)
        display.set_char(display_temp[4], 3)
        display.update()

        # Pause for breath
        time.sleep(DELAY)