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

    # Get initial values
    data = psutil.net_io_counters()
    start_packets = data.packets_recv
    packets = 0

    while True:
        # Get the CPU utilization and calculate
        # the Binary-Coded Decimal (BCD) form
        data = psutil.net_io_counters()
        packets = data.packets_recv - start_packets
        if packets > 9999:
            start_packets = data.packets_recv
            packets = 0

        # Display the percentage as decimal digits
        bcd = int(str(packets), 16)
        display.set_number((bcd & 0xF000) >> 12, 0)
        display.set_number((bcd & 0x0F00) >> 8, 1)
        display.set_number((bcd & 0xF0) >> 4, 2)
        display.set_number((bcd & 0x0F), 3)
        display.update()

        # Pause for breath
        time.sleep(DELAY)

# Exit on break
sys.exit(-1)
