#!/usr/bin/env python

class NOKIA5110:
    """
    Hardware driver for the Nokia 5110 display, an LCD driven by
    a PCD8544 controller chip
    Adapted by Tony Smith from a variety of sources:
        http://playground.arduino.cc/Code/PCD8544
        http://www.microsyl.com/index.php/2010/03/24/nokia-lcd-library/
    """

    # Constants
    NOKIA_5110_CMD = 0
    NOKIA_5110_DATA = 1
    NOKIA_5110_WIDTH = 84
    NOKIA_5110_HEIGHT = 48

    # ASCII is an array of Ascii characters, each defined by an
    # array of five 8-bit values specifying a 5 x 8 pixel matrix
    # NOTE we pad characters in the code
    ASCII = [
        [0x00, 0x00, 0x00, 0x00, 0x00], # 20
        [0x00, 0x00, 0x5f, 0x00, 0x00], # 21 !
        [0x00, 0x07, 0x00, 0x07, 0x00], # 22 "
        [0x14, 0x7f, 0x14, 0x7f, 0x14], # 23 #
        [0x24, 0x2a, 0x7f, 0x2a, 0x12], # 24 $
        [0x23, 0x13, 0x08, 0x64, 0x62], # 25 %
        [0x36, 0x49, 0x55, 0x22, 0x50], # 26 &
        [0x00, 0x05, 0x03, 0x00, 0x00], # 27 '
        [0x00, 0x1c, 0x22, 0x41, 0x00], # 28 (
        [0x00, 0x41, 0x22, 0x1c, 0x00], # 29 )
        [0x14, 0x08, 0x3e, 0x08, 0x14], # 2a *
        [0x08, 0x08, 0x3e, 0x08, 0x08], # 2b +
        [0x00, 0x50, 0x30, 0x00, 0x00], # 2c ,
        [0x08, 0x08, 0x08, 0x08, 0x08], # 2d -
        [0x00, 0x60, 0x60, 0x00, 0x00], # 2e .
        [0x20, 0x10, 0x08, 0x04, 0x02], # 2f /
        [0x3e, 0x51, 0x49, 0x45, 0x3e], # 30 0
        [0x00, 0x42, 0x7f, 0x40, 0x00], # 31 1
        [0x42, 0x61, 0x51, 0x49, 0x46], # 32 2
        [0x21, 0x41, 0x45, 0x4b, 0x31], # 33 3
        [0x18, 0x14, 0x12, 0x7f, 0x10], # 34 4
        [0x27, 0x45, 0x45, 0x45, 0x39], # 35 5
        [0x3c, 0x4a, 0x49, 0x49, 0x30], # 36 6
        [0x01, 0x71, 0x09, 0x05, 0x03], # 37 7
        [0x36, 0x49, 0x49, 0x49, 0x36], # 38 8
        [0x06, 0x49, 0x49, 0x29, 0x1e], # 39 9
        [0x00, 0x36, 0x36, 0x00, 0x00], # 3a :
        [0x00, 0x56, 0x36, 0x00, 0x00], # 3b ;
        [0x08, 0x14, 0x22, 0x41, 0x00], # 3c <
        [0x14, 0x14, 0x14, 0x14, 0x14], # 3d =
        [0x00, 0x41, 0x22, 0x14, 0x08], # 3e >
        [0x02, 0x01, 0x51, 0x09, 0x06], # 3f ?
        [0x32, 0x49, 0x79, 0x41, 0x3e], # 40 @
        [0x7e, 0x11, 0x11, 0x11, 0x7e], # 41 A
        [0x7f, 0x49, 0x49, 0x49, 0x36], # 42 B
        [0x3e, 0x41, 0x41, 0x41, 0x22], # 43 C
        [0x7f, 0x41, 0x41, 0x22, 0x1c], # 44 D
        [0x7f, 0x49, 0x49, 0x49, 0x41], # 45 E
        [0x7f, 0x09, 0x09, 0x09, 0x01], # 46 F
        [0x3e, 0x41, 0x49, 0x49, 0x7a], # 47 G
        [0x7f, 0x08, 0x08, 0x08, 0x7f], # 48 H
        [0x00, 0x41, 0x7f, 0x41, 0x00], # 49 I
        [0x20, 0x40, 0x41, 0x3f, 0x01], # 4a J
        [0x7f, 0x08, 0x14, 0x22, 0x41], # 4b K
        [0x7f, 0x40, 0x40, 0x40, 0x40], # 4c L
        [0x7f, 0x02, 0x0c, 0x02, 0x7f], # 4d M
        [0x7f, 0x04, 0x08, 0x10, 0x7f], # 4e N
        [0x3e, 0x41, 0x41, 0x41, 0x3e], # 4f O
        [0x7f, 0x09, 0x09, 0x09, 0x06], # 50 P
        [0x3e, 0x41, 0x51, 0x21, 0x5e], # 51 Q
        [0x7f, 0x09, 0x19, 0x29, 0x46], # 52 R
        [0x46, 0x49, 0x49, 0x49, 0x31], # 53 S
        [0x01, 0x01, 0x7f, 0x01, 0x01], # 54 T
        [0x3f, 0x40, 0x40, 0x40, 0x3f], # 55 U
        [0x1f, 0x20, 0x40, 0x20, 0x1f], # 56 V
        [0x3f, 0x40, 0x38, 0x40, 0x3f], # 57 W
        [0x63, 0x14, 0x08, 0x14, 0x63], # 58 X
        [0x07, 0x08, 0x70, 0x08, 0x07], # 59 Y
        [0x61, 0x51, 0x49, 0x45, 0x43], # 5a Z
        [0x00, 0x7f, 0x41, 0x41, 0x00], # 5b [
        [0x02, 0x04, 0x08, 0x10, 0x20], # 5c \
        [0x00, 0x41, 0x41, 0x7f, 0x00], # 5d ],
        [0x04, 0x02, 0x01, 0x02, 0x04], # 5e ^
        [0x40, 0x40, 0x40, 0x40, 0x40], # 5f _
        [0x00, 0x01, 0x02, 0x04, 0x00], # 60 `
        [0x20, 0x54, 0x54, 0x54, 0x78], # 61 a
        [0x7f, 0x48, 0x44, 0x44, 0x38], # 62 b
        [0x38, 0x44, 0x44, 0x44, 0x20], # 63 c
        [0x38, 0x44, 0x44, 0x48, 0x7f], # 64 d
        [0x38, 0x54, 0x54, 0x54, 0x18], # 65 e
        [0x08, 0x7e, 0x09, 0x01, 0x02], # 66 f
        [0x0c, 0x52, 0x52, 0x52, 0x3e], # 67 g
        [0x7f, 0x08, 0x04, 0x04, 0x78], # 68 h
        [0x00, 0x44, 0x7d, 0x40, 0x00], # 69 i
        [0x20, 0x40, 0x44, 0x3d, 0x00], # 6a j
        [0x7f, 0x10, 0x28, 0x44, 0x00], # 6b k
        [0x00, 0x41, 0x7f, 0x40, 0x00], # 6c l
        [0x7c, 0x04, 0x18, 0x04, 0x78], # 6d m
        [0x7c, 0x08, 0x04, 0x04, 0x78], # 6e n
        [0x38, 0x44, 0x44, 0x44, 0x38], # 6f o
        [0x7c, 0x14, 0x14, 0x14, 0x08], # 70 p
        [0x08, 0x14, 0x14, 0x18, 0x7c], # 71 q
        [0x7c, 0x08, 0x04, 0x04, 0x08], # 72 r
        [0x48, 0x54, 0x54, 0x54, 0x20], # 73 s
        [0x04, 0x3f, 0x44, 0x40, 0x20], # 74 t
        [0x3c, 0x40, 0x40, 0x20, 0x7c], # 75 u
        [0x1c, 0x20, 0x40, 0x20, 0x1c], # 76 v
        [0x3c, 0x40, 0x30, 0x40, 0x3c], # 77 w
        [0x44, 0x28, 0x10, 0x28, 0x44], # 78 x
        [0x0c, 0x50, 0x50, 0x50, 0x3c], # 79 y
        [0x44, 0x64, 0x54, 0x4c, 0x44], # 7a z
        [0x00, 0x08, 0x36, 0x41, 0x00], # 7b [
        [0x00, 0x00, 0x7f, 0x00, 0x00], # 7c |
        [0x00, 0x41, 0x36, 0x08, 0x00], # 7d ]
        [0x10, 0x08, 0x08, 0x10, 0x08], # 7e ~
        [0x78, 0x46, 0x41, 0x46, 0x78], # 7f DEL
    ]

    def __init__(self, rst, ce, dc, din, clk, bl):
        import board
        import digitalio
        import time

        # Store the pins
        self.pin_ce = ce
        self.pin_rst = rst
        self.pin_dc = dc
        self.pin_din = din
        self.pin_clk = clk
        self.pin_bl = bl

        # Configure the pins as outputs
        self.pin_ce.direction = digitalio.Direction.OUTPUT
        self.pin_rst.direction = digitalio.Direction.OUTPUT
        self.pin_dc.direction = digitalio.Direction.OUTPUT
        self.pin_din.direction = digitalio.Direction.OUTPUT
        self.pin_clk.direction = digitalio.Direction.OUTPUT
        self.pin_bl.direction = digitalio.Direction.OUTPUT

        # Reset the PCD8544
        self.pin_rst.value = False
        time.sleep(0.01)
        self.pin_rst.value = True

        # Switch off the backlight
        self.backlight(False)

        # Initialise the PCD8544
        # Send Function command (0x20) to select either  the
        # basic command set (+0), or extended command set (+1)
        self.write(self.NOKIA_5110_CMD, 0x21)

        # Set the LCD contrast command
        # Try 0xB1 (good @ 3.3V) or 0xBF if your display is too dark
        self.write(self.NOKIA_5110_CMD, 0xAA)

        # Set the LCD temperature coefficient: 0x04 + 0-3
        self.write(self.NOKIA_5110_CMD, 0x04)

        # Set LCD bias voltage: 0x10 + 0-7
        self.write(self.NOKIA_5110_CMD, 0x14)

        # Send Function command (0x20) to select either
        # horizontal screen addressing (+0) or vertical addressing (+2)
        self.write(self.NOKIA_5110_CMD, 0x20);

        # Set LCD display mode (0x08) plus
        #  0 - All pixels clear (0x08)
        #  1 - All pixels set (0x09)
        #  4 - Normal video (0x0C)
        #   5 - Inverse video (0x0D)
        self.write(self.NOKIA_5110_CMD, 0x0C);

    def clear(self):
        """
        Clear the LCD
        """
        for i in range(0, self.NOKIA_5110_WIDTH * int(self.NOKIA_5110_HEIGHT / 8)):
            self.write(self.NOKIA_5110_DATA, 0x00)
        self.move(0, 0)

    def backlight(self, on_or_off=True):
        """
        Turn the backlight on or off

        Args:
            on_or_off (bool) Set the backlight on (True) or off (False). Default: True
        """
        self.pin_bl.value = on_or_off

    def move(self, x, y):
        """
        Position the cursor at column x, row y

        Args:
            x (int) The X co-ordinate (0-83)
            y (int) The Y co-ordinate (0-5)
        """
        self.write(self.NOKIA_5110_CMD, 0x80 | x)
        self.write(self.NOKIA_5110_CMD, 0x40 | y)

    def print_text(self, print_string):
        """
        Write a string of chracters to the LCD by taking each individual
        character and writing it with print_char().
        The PCD8544 chip will move the cursor for you, wrapping the line
        and scrolling if necessary

        args:
            print_string (string) The string to print
        """
        if len(print_string) == 0 or print_string == None: return
        for i in range(0, len(print_string)):
            self.print_char(print_string[i])

    def print_char(self, a_char):
        """
        Writes a 5 x 8 character graphic from the ASCII array to the screen
        at the current cursor position

        Args:
            a_char (string) A single character
        """
        glyph = self.ASCII[ord(a_char) - 0x20]
        self.write(self.NOKIA_5110_DATA, 0x00)
        for i in range(0, 5):
            self.write(self.NOKIA_5110_DATA, glyph[i])
        self.write(self.NOKIA_5110_DATA, 0x00)

    def print_bitmap(self, bitmap_array):
        """
        Writes an array of 8-bit values to the LCD at
        the current cursor position
        """
        if bitmap_array == None or len(bitmap_array) == 0: return
        for i in range(0, self.NOKIA_5110_WIDTH * int(self.NOKIA_5110_HEIGHT / 8)):
            self.write(self.NOKIA_5110_DATA, bitmap_array[i])

    def write(self, data_or_cmd, value):
        """"
        Write a command or data value to the display.

        There are two memory banks in the LCD: one for data, another for
        commands. Select the one you want by setting pin DC high (data) or
        low (command). Then signal the data/command transmission by setting
        pin CE low, writing the data/command, them setting CE high

        Args:
            data_or_cmd (bool) Is the value data (True) or a command (False)
            value (integer) The command or data byte to be written
        """
        self.pin_dc.value = True if data_or_cmd == self.NOKIA_5110_DATA else False

        # Send the data
        self.pin_ce.value = False
        self.write_byte(value)
        self.pin_ce.value = True

    def write_byte(self, value):
        """
        Write a single byte to the display

        Takes a byte of data and writes it out to the 5110 bit by bit,
	    most significant bit first, least significant bit last.
	    Each bit is signalled by setting pin CLK low and setting CLK
	    high after the bit has been sent. The bit is sent on pin DIN.

        Args:
            value (integer) The byte to be written
        """
        for i in range(7, -1, -1):
            self.pin_clk.value = False
            self.pin_din.value = True if value & 0x80 else False
            value = value << 1
            self.pin_clk.value = True
