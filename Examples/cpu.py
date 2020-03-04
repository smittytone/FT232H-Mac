#!/usr/bin/env python

# IMPORTS
import time
import sys
import board
import busio
import psutil
from htk1633segment_circuitpython import HT16K33Segment

# CONSTANTS
DELAY = 0.5

# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    # and instantiate the display
    i2c = busio.I2C(board.SCL, board.SDA)
    display = HT16K33Segment(i2c)
    display.set_brightness(2)

    while True:
        # Get the CPU utilization and calculate
        # the Binary-Coded Decimal (BCD) form
        cpu = int(psutil.cpu_percent())
        bcd = int(str(cpu), 16)

        # Display the percentage as decimal digits
        display.set_number((bcd & 0x0F00) >> 8, 1)
        display.set_number((bcd & 0xF0) >> 4, 2)
        display.set_number((bcd & 0x0F), 3)
        display.update()

        # Pause for breath
        time.sleep(DELAY)

# Exit on break
sys.exit(-1)
