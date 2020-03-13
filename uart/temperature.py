#!/usr/bin/env python

# IMPORTS
import time
from onewire import OneWire

# START
if __name__ == '__main__':
    # Set up 1-Wire on the UART
    ow = OneWire("/dev/cu.usbserial-1470")

    # Loop to take the temperature and display it
    while True:
        temp_lsb = 0
        temp_msb = 0
        temp_celsius = 0
        minus_flag = False

        if ow.reset():
            ow.skip_rom()
            ow.write_byte(0x44)
            time.sleep(0.8)
            ow.reset()
            ow.skip_rom()
            ow.write_byte(0xBE)

            # Read the 16-bit temperature as big endian
            temp_lsb = ow.read_byte()
            temp_lsb = ow.read_byte()

            # Check for a negative temperature
            if temp_msb > 7:
                minus_flag = True
                temp_msb -= 8

            ow.reset()

            # Clear sign bits, if any
            temp_msb = temp_msb & 7

            # Convert to 16-bit value, then divide by 16
            # to recover decimal point values
            temp_celsius = ((temp_msb << 8) + temp_lsb) / 16.0
            print("Temperature: {:3.2f}˚C".format(temp_celsius))
        else:
            print(ow.read_error)

        time.sleep(10)

sys.exit(-1)