#!/usr/bin/env python

# IMPORTS
import time
import board
import busio
from htk1633segment_circuitpython import HT16K33Segment

# CONSTANTS
DELAY = 0.01

# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    # and instantiate the display
    i2c = busio.I2C(board.SCL, board.SDA)
    display = HT16K33Segment(i2c)
    count = 9999

    while True:
        # Convert 'count' into Binary-Coded Decimal (BCD)
        bcd = int(str(count), 16)

        # Display 'count' as decimal digits
        display.set_number((bcd & 0xF000) >> 12, 0)
        display.set_number((bcd & 0x0F00) >> 8, 1)
        display.set_number((bcd & 0xF0) >> 4, 2)
        display.set_number((bcd & 0x0F), 3)
        display.update()

        count -= 1
        if count < 0:
            break

        # Pause for breath
        time.sleep(DELAY)
