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
serial_port = serial.Serial("/dev/tty.usbserial-1470")
serial_port.baudrate = 2400
serial_port.timeout = 10.0

# Set up the conversation's message count
message_total = randint(20, 40)
message_count = 0

# Loop
while True:
    # Increment the message counter
    message_count += 1

    # Choose a conversation line
    r = randint(0, len(lines) - 1)
    line = lines[r]
    number = "{:02d}.".format(message_count)
    print(number + " FTS23H says:", line[0:len(line)-1])

    # send the line
    serial_port.write(line.encode('utf-8'))
    serial_port.flush()

    # Wait for the response
    print("WAITING", end="\r", flush=True)
    v = serial_port.read_until()
    print("    Other says: ", v.decode("utf-8"))

    # End the conversation after sending all the messages
    if message_count >= message_total:
        break

# Loop complete so close the serial port and quit
serial_port.close()
sys.exit(-1)