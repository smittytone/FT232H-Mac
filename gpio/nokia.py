#!/usr/bin/env python

# IMPORTS
import time
import os
import board
import digitalio
from nokia5110_circuitpython import NOKIA5110

# CONSTANTS
DEBOUNCE_MAX = 40

dude = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0xC0, 0xE0, 0xF0, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0xF8, 0xF0, 0xC0, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0xE0, 0xF8,
    0xF8, 0x10, 0xC0, 0xF0, 0xF0, 0x30, 0x80, 0xC0,
    0xC0, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0xC0, 0xF0, 0xFC, 0xFE,
    0xFC, 0xF0, 0xE0, 0x80, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC,
    0xF8, 0xFC, 0xFC, 0xFE, 0x7E, 0x7F, 0x3F, 0x3F,
    0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x3F,
    0x3F, 0x7F, 0x7E, 0xFE, 0xFC, 0xFC, 0xF8, 0xFC,
    0xFF, 0xFF, 0xFF, 0x7F, 0x1F, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xE0, 0xFC, 0xFC, 0xFF, 0xFF, 0xFF,
    0xF8, 0xFE, 0xFF, 0xFF, 0xE1, 0xFC, 0xFF, 0xFF,
    0x07, 0x00, 0x00, 0x00,
    0x00, 0x18, 0x1E, 0x0F, 0x0F, 0x0F, 0xFF, 0xFF,
    0xFF, 0xEF, 0x0F, 0x0F, 0x1E, 0x18, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0xC0, 0xF8, 0xFE, 0xFF, 0xFF, 0xFF, 0x3F,
    0x0F, 0x73, 0xF1, 0xF0, 0xE0, 0xE0, 0xE0, 0xC0,
    0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0xE0,
    0xF0, 0xF0, 0xF8, 0xF8, 0xF1, 0x63, 0x0F, 0x3F,
    0xFF, 0xFF, 0xFF, 0xFE, 0xF0, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x07, 0x0F, 0xDF, 0xFF, 0xFF, 0xFF,
    0x7F, 0x7F, 0x7F, 0x3F, 0x3F, 0x1F, 0x07, 0x01,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x0F,
    0x3F, 0x7F, 0xFE, 0xF8, 0xE0, 0xC0, 0x00, 0x00,
    0x00, 0xC0, 0xE0, 0xF0, 0xF0, 0xF8, 0xF8, 0xF8,
    0xFC, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0,
    0x80, 0x00, 0x00, 0x01, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x83,
    0x83, 0xC3, 0x43, 0x01, 0x00, 0x00, 0x00, 0xC0,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0xFC, 0xF8,
    0xF8, 0xF8, 0xF0, 0xFE, 0xFF, 0xFF, 0x07, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E,
    0x3C, 0x7C, 0x7B, 0xF3, 0xF3, 0xE3, 0xE3, 0xE1,
    0xE1, 0xC1, 0xC0, 0xC3, 0xCF, 0xDF, 0xFF, 0xFF,
    0xFF, 0xFE, 0xFC, 0xF8, 0xF0, 0xF0, 0xE0, 0xE0,
    0xE0, 0xC3, 0xC3, 0xC3, 0xC3, 0xC3, 0xC3, 0xE3,
    0xE1, 0xE0, 0xF0, 0xF0, 0xF8, 0xFC, 0xFE, 0x7F,
    0x3F, 0x1F, 0x07, 0x03, 0x00, 0x01, 0x81, 0xF1,
    0xFF, 0xFF, 0x3F, 0x07, 0x03, 0x01, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01,
    0x01, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x03, 0x03, 0x03, 0x03, 0x07, 0x07, 0x07,
    0x07, 0x0F, 0x0F, 0x0F, 0x0F, 0x07, 0x07, 0x07,
    0x07, 0x07, 0x03, 0x03, 0x01, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x07,
    0x07, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00
]
# START

# Set up the button on pin C0 and
# configure the pin as DIGITAL IN
# rst, ce, dc, din, clk, bl
display = NOKIA5110(digitalio.DigitalInOut(board.C7), digitalio.DigitalInOut(board.C6), digitalio.DigitalInOut(board.C5), digitalio.DigitalInOut(board.C4), digitalio.DigitalInOut(board.C3), digitalio.DigitalInOut(board.C2))

display.clear()

display.backlight()
time.sleep(0.1)
display.backlight(False)
time.sleep(0.1)
display.backlight()
time.sleep(0.1)
display.backlight(False)
time.sleep(0.1)
display.backlight()

display.print_bitmap(dude)
display.move(0,5)
display.print_text("Hello World")

while True:
    time.sleep(1)

# Exit on break
sys.exit(-1)