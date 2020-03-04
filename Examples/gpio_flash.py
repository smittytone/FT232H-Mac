#!/usr/bin/env python

# IMPORTS
import time
import board
import digitalio

# Set up the LED on pin C0 and
# configure the pin as DIGITAL OUT
led = digitalio.DigitalInOut(board.C0)
led.direction = digitalio.Direction.OUTPUT

# Loop infinitely to flash the LED
while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
