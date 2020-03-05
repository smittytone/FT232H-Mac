#!/usr/bin/env python

# IMPORTS
import time
import sys
import board
import busio
import digitalio
from ssd1306_circuitpython import SSD1306OLED
from enum import Enum
from random import seed
from random import randint

class EYE_STATE(Enum):
    OPEN = 0
    CLOSED = 1

class EYE_MOOD(Enum):
    NORMAL = 0
    CROSS = 1
    SAD = 2

class PUPIL_SIZE(Enum):
    SMALL = 0
    NORMAL = 1
    BIG = 2

# CONSTANTS
DELAY = 0.5

# Set up eye data
PUPIL_SIZES = [2, 6, 10];
PUPIL_POSNS = [
    47, 16, 81, 16,     # Face on      0
    40, 16, 74, 16,     # Left         1
    54, 16, 88, 16,     # Right        2
    47, 9, 81, 9,       # Up           3
    47, 24, 81, 24,     # Down         4
    43, 12, 77, 12,     # Up left      5
    51, 12, 85, 12,     # Up right     6
    51, 20, 85, 20,     # Down right   7
    43, 20, 77, 20,     # Down left    8
    51, 20, 77, 20      # Doh!         9
]

def eyes_open(oled, pupil_size, pupil_dir):
    # Draw blank open eyes
    eyes_clear(oled)

    # Draw in the pupils
    a = pupil_dir << 2;
    oled.circle(PUPIL_POSNS[a], PUPIL_POSNS[a + 1], PUPIL_SIZES[pupil_size], 0, True)
    oled.circle(PUPIL_POSNS[a + 2], PUPIL_POSNS[a + 3], PUPIL_SIZES[pupil_size], 0, True);

def eyes_closed(oled):
    # Draw blank closed eyes
    oled.circle(47, 16, 14, 0, True).circle(81, 16, 14, 0, True);

def eyes_clear(oled):
    # Draw blank open eyes
    oled.circle(47, 16, 16, 1, True).circle(81, 16, 16, 1, True)

# START
if __name__ == '__main__':
    # Set the random seed
    seed()

    # Set up I2C on the FT232H Breakout
    i2c = busio.I2C(board.SCL, board.SDA)

    # Set up the RST pin
    reset = digitalio.DigitalInOut(board.D7)
    reset.direction = digitalio.Direction.OUTPUT

    # Set up OLED display
    display = SSD1306OLED(i2c, 0x3C, reset)

    mood_changed = False
    mood = EYE_MOOD.NORMAL
    eye_state = EYE_STATE.OPEN
    next_state = EYE_STATE.CLOSED
    pupil_direction = randint(0, 8)
    blink_count = 0
    mood_count = 0

    while True:
        blink_count += 1
        mood_count += 1
        next_state = -1

        if mood_changed is True:
            mood = new_mood
            mood_changed = False
            mood_count = 0

        if eye_state == EYE_STATE.CLOSED:
            # Draw the closed eyes
            eyes_closed(display);

            if blink_count > 0:
                blink_count = 0
                next_state = EYE_STATE.OPEN
        else:
            # Only adjust eye direction if they eyes are open
            r = randint(0, 100)
            if pupil_direction > 0:
                if r > 20: pupil_direction = 0
            else:
                if r > 80: pupil_direction = randint(0, 8)
                if r == 3: pupil_direction = 9

        # Draw eyes open
        eyes_open(display, PUPIL_SIZE.NORMAL.value, pupil_direction)

        # Should we close next time?
        if blink_count > 3 and randint(0, 10) > 6:
            blink_count = 0
            next_state = EYE_STATE.CLOSED

        # Add eyebrows if necessary
        if mood == EYE_MOOD.CROSS:
            # Clear the space above each eye
            display.line(38, -10, 64, 0, 10, 0).line(66, 0, 92, -10, 10, 0)

            if eye_state == EYE_STATE.CLOSED:
                # Eye is closed, so close the outline
                display.line(68, 9, 86, 1, 2, 1).line(42, 1, 60, 9, 2, 1)
        elif mood == EYE_MOOD.SAD:
            # Clear the space above each eye
            display.line(32, 0, 56, -10, 10, 0).line(72, -10, 96, 0, 10, 0)

            if eye_state == EYE_STATE.CLOSED:
                # Eye is closed, so close the outline
                display.line(34, 9, 53, 1, 2, 1).line(75, 1, 94, 9, 2, 1)

        # Did the eye state change? Set the new state now for the next iteration
        if next_state != -1: eye_state = next_state
        display.draw()

        # Look for a change of mood every 60s
        if mood_count > 120:
            r = randint(0, 1000)
            if r >= 950 and mood != EYE_MOOD.CROSS:
                mood_changed = True
                new_mood = EYE_MOOD.CROSS
            elif r <= 50 and mood != EYE_MOOD.SAD:
                mood_changed = True
                new_mood = EYE_MOOD.SAD
            elif mood != EYE_MOOD.NORMAL:
                mood_changed = True
                new_mood = EYE_MOOD.NORMAL

        # Pause for breath
        time.sleep(DELAY)

# Exit on break
sys.exit(-1)
