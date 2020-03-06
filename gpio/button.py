#!/usr/bin/env python

# IMPORTS
import time
import os
import board
import digitalio

# CONSTANTS
DEBOUNCE_MAX = 40

# START

# Set up the button on pin C0 and
# configure the pin as DIGITAL IN
button = digitalio.DigitalInOut(board.C0)
button.direction = digitalio.Direction.INPUT

# Set up the LED on pin D7 and
# configure the pin as DIGITAL OUT
# NOTE connect other LED pin to GND
led = digitalio.DigitalInOut(board.D7)
led.direction = digitalio.Direction.OUTPUT

# Initialize the debounce counter
debounce_count = 0

while True:
    if button.value == True:
        # Button pressed, so start counting milliseconds
        # to check for a consistent push on the button
        debounce_count += 1
        if debounce_count == DEBOUNCE_MAX:
            # Button has been held down for DEBOUNCE_MAX
            # milliseconds, so trigger a press action
            # NOTE In the following line, replace the contents
            #      of the double-quotes with a simple shell
            #      command of your own
            os.system("open /Applications/Squinter.app")
            led.value = True
    else:
        # Button released, so just clear the debounce counter
        debounce_count = 0
        led.value = False
    # Pause for a millisecond
    time.sleep(0.001)

# Exit on break
sys.exit(-1)