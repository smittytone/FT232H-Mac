#!/usr/bin/env python

# IMPORTS
import time
import sys
import board
import busio
import digitalio
import psutil
from ssd1306_circuitpython import SSD1306OLED

# CONSTANTS
DELAY = 0.5

# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    i2c = busio.I2C(board.SCL, board.SDA)

    # Set up the RST pin
    reset = digitalio.DigitalInOut(board.D7)
    reset.direction = digitalio.Direction.OUTPUT

    display = SSD1306OLED(i2c, 0x3C, reset)
    display.set_inverse()

    # Get initial values
    data = psutil.net_io_counters()
    start_out_packets = data.packets_sent
    start_in_packets = data.packets_recv
    out_packets = 0
    in_packets = 0
    head = "**SYSTEM INFORMATION**"
    head_centre = int((127 - display.length_of_string(head)) / 2)
    if head_centre < 0: head_centre = 0

    while True:
        # Get the CPU utilization and calculate
        # the Binary-Coded Decimal (BCD) form
        display.clear()
        display.move(head_centre, 0).text(head)
        display.move(0, 8).text("CPU:")
        display.move(64, 8).text("Mem:")
        display.move(0, 16).text("Pkts in:")
        display.move(0, 24).text("Pkts out:")

        cpu = int(psutil.cpu_percent())
        display.move(30, 8).text(str(cpu) + "%")

        data = psutil.virtual_memory()
        mem = (data.used / data.total) * 100
        display.move(88, 8).text("{:.1f}%".format(mem))

        data = psutil.net_io_counters()
        out_packets = data.packets_sent - start_out_packets
        if out_packets > 99999:
            start_out_packets = data.packets_sent
            out_packets = 0
        display.move(50, 24).text(str(out_packets))

        in_packets = data.packets_recv - start_in_packets
        if in_packets > 99999:
            start_in_packets = data.packets_recv
            in_packets = 0
        display.move(50, 16).text(str(in_packets))



        display.draw()

        # Pause for breath
        time.sleep(DELAY)

# Exit on break
sys.exit(-1)
