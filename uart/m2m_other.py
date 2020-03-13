#!/usr/bin/env python

# IMPORTS
import sys
import os
import time
import serial
from random import seed
from random import randint

# Seed the random number generator
seed()

# Load in the file of conversation strings
file_path = "m2m_lines.txt"
if not os.path.exists(file_path):
    print("[ERROR] File " + file_path + " does not exist, exiting")
    sys.exit(-1)
with open(file_path, "r") as file: lines = list(file)

# Set up the serial port
serial_port = serial.Serial('/dev/tty.usbserial-FTWHFLU9')
serial_port.baudrate = 2400
serial_port.timeout = 10.0

# Loop
while True:
    # Wait for an incoming message
    print("WAITING...", end="\r", flush=True)
    v = serial_port.read_until()

    if len(v) == 0:
        # No message? read_until() timed out so bail
        print("Conversation over")
        break

    # Print the incoming message
    print("Other says: ", v[0:len(v)-1].decode("utf-8"))

    # Choose a response
    r = randint(0, len(lines) - 1)
    print(" FTDI says: ", lines[r])

    # Send the encoded response
    serial_port.write(lines[r].encode('utf-8'))
    serial_port.flush()

# Loop complete so close the serial port and quit
serial_port.close()