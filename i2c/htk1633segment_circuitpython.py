class HT16K33Segment:
    """
    A simple driver for the I2C-connected Holtek HT16K33 controller chip and a four-digit,
    seven-segment LED connected to it.
    For example: https://learn.adafruit.com/adafruit-7-segment-led-featherwings/overview
    This release is written for CircuitPython

    Version:   1.0.0
    Author:    smittytone
    Copyright: 2020, Tony Smith
    Licence:   MIT
    """

    HT16K33_BLINK_CMD = 0x80
    HT16K33_BLINK_DISPLAY_ON = 0x01
    HT16K33_CMD_BRIGHTNESS = 0xE0
    HT16K33_SYSTEM_ON = 0x21
    HT16K33_COLON_ROW = 0x04
    HT16K33_MINUS_CHAR = 0x10
    HT16K33_DEGREE_CHAR = 0x11

    # The positions of the segments within the buffer
    pos = [0, 2, 6, 8]

    # Bytearray of the key alphanumeric characters we can show:
    # 0-9, A-F, minus, degree
    chars = b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x5F\x7C\x58\x5E\x7B\x71\x40\x63'


    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self.address = address
        self.buffer = bytearray(16)
        self._write_cmd(self.HT16K33_SYSTEM_ON)
        self.set_blink_rate()
        self.set_brightness(15)

    def set_blink_rate(self, rate=0):
        """
        Set the display's flash rate.

        Only four values (in Hz) are permitted: 0, 2, 1, and 0,5.

        Args:
            rate (int): The chosen flash rate. Default: 0Hz.
        """
        rates = (0, 2, 1, 0.5)
        if rate not in rates: return
        rate = rate & 0x03
        self.blink_rate = rate
        self._write_cmd(self.HT16K33_BLINK_CMD | self.HT16K33_BLINK_DISPLAY_ON | rate << 1)

    def set_brightness(self, brightness=15):
        """
        Set the display's brightness (ie. duty cycle).

        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).

        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        if brightness < 0 or brightness > 15: brightness = 15
        brightness = brightness & 0x0F
        self.brightness = brightness
        self._write_cmd(self.HT16K33_CMD_BRIGHTNESS | brightness)

    def set_glyph(self, glyph, digit=0, has_dot=False):
        """
        Present a user-defined character glyph at the specified digit.

        Glyph values are 8-bit integers representing a pattern of set LED segments.
        The value is calculated by setting the bit(s) representing the segment(s) you want illuminated.
        Bit-to-segment mapping runs clockwise from the top around the outside of the matrix; the inner segment is bit 6:

                0
                _
            5 |   | 1
              |   |
                - <----- 6
            4 |   | 2
              | _ |
                3

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            glyph (int):   The glyph pattern.
            digit (int):   The digit to show the glyph. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.
        """
        if not 0 <= digit <= 3: return
        self.buffer[self.pos[digit]] = glyph
        if has_dot is True: self.buffer[self.pos[digit]] |= 0b10000000

    def set_number(self, number, digit=0, has_dot=False):
        """
        Present single decimal value (0-9) at the specified digit.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            number (int):  The number to show.
            digit (int):   The digit to show the number. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.
        """
        self.set_char(str(number), digit, has_dot)

    def set_char(self, char, digit=0, has_dot=False):
        """
        Present single alphanumeric character at the specified digit.

        Only characters from the class' character set are available:
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d ,e, f, -, degree symbol.
        Other characters can be defined and presented using 'set_glyph()'.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            char (string): The character to show.
            digit (int):   The digit to show the number. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.
        """
        if not 0 <= digit <= 3: return
        char = char.lower()
        if char in 'abcdef':
            char_val = ord(char) - 87
        elif char == '-':
            char_val = self.HT16K33_MINUS_CHAR
        elif char in '0123456789':
            char_val = ord(char) - 48
        elif char == ' ':
            char_val = 0x00
        else:
            return

        self.buffer[self.pos[digit]] = self.chars[char_val]
        if has_dot is True: self.buffer[self.pos[digit]] |= 0b10000000

    def set_colon(self, is_set=True):
        """
        Set or unset the display's central colon symbol.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            isSet (bool): Whether the colon is lit (True) or not (False). Default: True.
        """
        self.buffer[self.HT16K33_COLON_ROW] = 0x02 if is_set is True else 0x00

    def clear(self):
        """
        Clears the display.

        This method clears the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.
        """
        buff = self.buffer
        for index in range(16): buff[index] = 0x00

    def update(self):
        """
        Writes the current display buffer to the display itself.

        Call this method after clearing the buffer or writing characters to the buffer to update
        the LED.
        """
        buffer = bytearray(17)
        buffer[1:] = self.buffer
        self.i2c.writeto(self.address, bytes(buffer))

    def _write_cmd(self, byte):
        """
        Writes a single command to the HT16K33. A private method.

        Args:
            byte (int): The command value to send.
        """
        temp = bytearray(1)
        temp[0] = byte
        self.i2c.writeto(self.address, temp)
