class SSD1306Pro:
    """
    A simple driver for the I2C-connected Solomon SSD1306 controller chip and an OLED display.
    For example: https:#learn.adafruit.com/adafruit-7-segment-led-featherwings/overview
    This release is written for CircuitPython

    Version:   1.0.0
    Author:    smittytone
    Copyright: 2020, Tony Smith
    Licence:   MIT
    """

    # CONSTANTS
    SSD1306_SETCONTRAST = 0x81
    SSD1306_DISPLAYALLON_RESUME = 0xA4
    SSD1306_DISPLAYALLON = 0xA5
    SSD1306_NORMALDISPLAY = 0xA6
    SSD1306_INVERTDISPLAY = 0xA7
    SSD1306_DISPLAYOFF = 0xAE
    SSD1306_DISPLAYON = 0xAF
    SSD1306_SETDISPLAYOFFSET = 0xD3
    SSD1306_SETCOMPINS = 0xDA
    SSD1306_SETVCOMDETECT = 0xDB
    SSD1306_SETDISPLAYCLOCKDIV = 0xD5
    SSD1306_SETPRECHARGE = 0xD9
    SSD1306_SETMULTIPLEX = 0xA8
    SSD1306_SETLOWCOLUMN = 0x00
    SSD1306_SETHIGHCOLUMN = 0x10
    SSD1306_SETSTARTLINE = 0x40
    SSD1306_MEMORYMODE = 0x20
    SSD1306_COLUMNADDR = 0x21
    SSD1306_PAGEADDR = 0x22
    SSD1306_COMSCANINC = 0xC0
    SSD1306_COMSCANDEC = 0xC8
    SSD1306_SEGREMAP = 0xA1
    SSD1306_CHARGEPUMP = 0x8D
    SSD1306_EXTERNALVCC = 0x01
    SSD1306_SWITCHCAPVCC = 0x02
    SSD1306_ACTIVATE_SCROLL = 0x2F
    SSD1306_DEACTIVATE_SCROLL = 0x2E
    SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
    SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
    SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
    SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
    SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A
    SSD1306_WRITETOBUFFER = 0x40

    HIGH = 1
    LOW = 0
    ALPHA_COUNT = 96

    CHARSET = [
        [0x00, 0x00],					# space - Ascii 32
        [0xfa],							# !
        [0xe0, 0xc0, 0x00, 0xe0, 0xc0],	# "
        [0x24, 0x7e, 0x24, 0x7e, 0x24],	# #
        [0x24, 0xd4, 0x56, 0x48],		# $
        [0xc6, 0xc8, 0x10, 0x26, 0xc6],	# %
        [0x6c, 0x92, 0x6a, 0x04, 0x0a],	# &
        [0xc0],							# '
        [0x7c, 0x82],					# (
        [0x82, 0x7c],					# )
        [0x10, 0x7c, 0x38, 0x7c, 0x10],	# *
        [0x10, 0x10, 0x7c, 0x10, 0x10],	# +
        [0x06, 0x07],					# ,
        [0x10, 0x10, 0x10, 0x10, 0x10],	# -
        [0x06, 0x06],					# .
        [0x04, 0x08, 0x10, 0x20, 0x40],	# /
        [0x7c, 0x8a, 0x92, 0xa2, 0x7c],	# 0 - Ascii 48
        [0x42, 0xfe, 0x02],				# 1
        [0x46, 0x8a, 0x92, 0x92, 0x62],	# 2
        [0x44, 0x92, 0x92, 0x92, 0x6c],	# 3
        [0x18, 0x28, 0x48, 0xfe, 0x08],	# 4
        [0xf4, 0x92, 0x92, 0x92, 0x8c],	# 5
        [0x3c, 0x52, 0x92, 0x92, 0x8c],	# 6
        [0x80, 0x8e, 0x90, 0xa0, 0xc0],	# 7
        [0x6c, 0x92, 0x92, 0x92, 0x6c],	# 8
        [0x60, 0x92, 0x92, 0x94, 0x78],	# 9
        [0x36, 0x36],					# : - Ascii 58
        [0x36, 0x37],					# ;
        [0x10, 0x28, 0x44, 0x82],		# <
        [0x24, 0x24, 0x24, 0x24, 0x24],	# =
        [0x82, 0x44, 0x28, 0x10],		# >
        [0x60, 0x80, 0x9a, 0x90, 0x60],	# ?
        [0x7c, 0x82, 0xba, 0xaa, 0x78],	# @
        [0x7e, 0x90, 0x90, 0x90, 0x7e],	# A - Ascii 65
        [0xfe, 0x92, 0x92, 0x92, 0x6c],	# B
        [0x7c, 0x82, 0x82, 0x82, 0x44],	# C
        [0xfe, 0x82, 0x82, 0x82, 0x7c],	# D
        [0xfe, 0x92, 0x92, 0x92, 0x82],	# E
        [0xfe, 0x90, 0x90, 0x90, 0x80],	# F
        [0x7c, 0x82, 0x92, 0x92, 0x5c],	# G
        [0xfe, 0x10, 0x10, 0x10, 0xfe],	# H
        [0x82, 0xfe, 0x82],				# I
        [0x0c, 0x02, 0x02, 0x02, 0xfc],	# J
        [0xfe, 0x10, 0x28, 0x44, 0x82],	# K
        [0xfe, 0x02, 0x02, 0x02, 0x02],	# L
        [0xfe, 0x40, 0x20, 0x40, 0xfe],	# M
        [0xfe, 0x40, 0x20, 0x10, 0xfe],	# N
        [0x7c, 0x82, 0x82, 0x82, 0x7c],	# O
        [0xfe, 0x90, 0x90, 0x90, 0x60],	# P
        [0x7c, 0x82, 0x92, 0x8c, 0x7a],	# Q
        [0xfe, 0x90, 0x90, 0x98, 0x66],	# R
        [0x64, 0x92, 0x92, 0x92, 0x4c],	# S
        [0x80, 0x80, 0xfe, 0x80, 0x80],	# T
        [0xfc, 0x02, 0x02, 0x02, 0xfc],	# U
        [0xf8, 0x04, 0x02, 0x04, 0xf8],	# V
        [0xfc, 0x02, 0x3c, 0x02, 0xfc],	# W
        [0xc6, 0x28, 0x10, 0x28, 0xc6],	# X
        [0xe0, 0x10, 0x0e, 0x10, 0xe0],	# Y
        [0x86, 0x8a, 0x92, 0xa2, 0xc2],	# Z - Ascii 90
        [0xfe, 0x82, 0x82],				# [
        [0x40, 0x20, 0x10, 0x08, 0x04],	# \
        [0x82, 0x82, 0xfe],				# ]
        [0x20, 0x40, 0x80, 0x40, 0x20],	# ^
        [0x02, 0x02, 0x02, 0x02, 0x02],	# _
        [0xc0, 0xe0],					# '
        [0x04, 0x2a, 0x2a, 0x2a, 0x1e],	# a - Ascii 97
        [0xfe, 0x22, 0x22, 0x22, 0x1c],	# b
        [0x1c, 0x22, 0x22, 0x22],		# c
        [0x1c, 0x22, 0x22, 0x22, 0xfc],	# d
        [0x1c, 0x2a, 0x2a, 0x2a, 0x10],	# e
        [0x10, 0x7e, 0x90, 0x90, 0x80],	# f
        [0x18, 0x25, 0x25, 0x25, 0x3e],	# g
        [0xfe, 0x20, 0x20, 0x20, 0x1e],	# h
        [0xbe, 0x02],					# i
        [0x02, 0x01, 0x01, 0x21, 0xbe],	# j
        [0xfe, 0x08, 0x14, 0x22],		# k
        [0xfe, 0x02],					# l
        [0x3e, 0x20, 0x18, 0x20, 0x1e],	# m
        [0x3e, 0x20, 0x20, 0x20, 0x1e],	# n
        [0x1c, 0x22, 0x22, 0x22, 0x1c],	# o
        [0x3f, 0x22, 0x22, 0x22, 0x1c],	# p
        [0x1c, 0x22, 0x22, 0x22, 0x3f],	# q
        [0x22, 0x1e, 0x22, 0x20, 0x10],	# r
        [0x12, 0x2a, 0x2a, 0x2a, 0x04],	# s
        [0x20, 0x7c, 0x22, 0x22, 0x04],	# t
        [0x3c, 0x02, 0x02, 0x3e],		# u
        [0x38, 0x04, 0x02, 0x04, 0x38],	# v
        [0x3c, 0x06, 0x0c, 0x06, 0x3c],	# w
        [0x22, 0x14, 0x08, 0x14, 0x22],	# x
        [0x39, 0x05, 0x06, 0x3c],		# y
        [0x26, 0x2a, 0x2a, 0x32],		# z - Ascii 122
        [0x10, 0x7c, 0x82, 0x82],		# {
        [0xee],							# |
        [0x82, 0x82, 0x7c, 0x10],		# }
        [0x40, 0x80, 0x40, 0x80],		# ~
        [0x60, 0x90, 0x90, 0x60] 		# Degrees sign - Ascii 127
    ]

    COS_TABLE = [
        0.000,0.035,0.070,0.105,0.140,0.174,0.208,0.243,0.276,0.310,0.343,0.376,0.408,0.439,0.471,0.501,0.531,0.561,0.589,0.617,0.644,
        0.671,0.696,0.721,0.745,0.768,0.790,0.810,0.830,0.849,0.867,0.884,0.900,0.915,0.928,0.941,0.952,0.962,0.971,0.979,0.985,0.991,
        0.995,0.998,1.000,1.000,0.999,0.997,0.994,0.990,0.984,0.977,0.969,0.960,0.949,0.938,0.925,0.911,0.896,0.880,0.863,0.845,0.826,
        0.806,0.784,0.762,0.739,0.715,0.690,0.664,0.638,0.610,0.582,0.554,0.524,0.494,0.463,0.432,0.400,0.368,0.335,0.302,0.268,0.234,
        0.200,0.166,0.131,0.096,0.062,0.027,-0.008,-0.043,-0.078,-0.113,-0.148,-0.182,-0.217,-0.251,-0.284,-0.318,-0.351,-0.383,-0.415,
        -0.447,-0.478,-0.508,-0.538,-0.567,-0.596,-0.624,-0.651,-0.677,-0.702,-0.727,-0.750,-0.773,-0.795,-0.815,-0.835,-0.854,-0.872,
        -0.888,-0.904,-0.918,-0.931,-0.944,-0.955,-0.964,-0.973,-0.981,-0.987,-0.992,-0.996,-0.998,-1.000,-1.000,-0.999,-0.997,-0.993,
        -0.988,-0.982,-0.975,-0.967,-0.957,-0.947,-0.935,-0.922,-0.908,-0.893,-0.876,-0.859,-0.840,-0.821,-0.801,-0.779,-0.757,-0.733,
        -0.709,-0.684,-0.658,-0.631,-0.604,-0.575,-0.547,-0.517,-0.487,-0.456,-0.424,-0.392,-0.360,-0.327,-0.294,-0.260,-0.226,-0.192,
        -0.158,-0.123,-0.088,-0.053,-0.018
    ]

    SIN_TABLE = [
        1.000,0.999,0.998,0.994,0.990,0.985,0.978,0.970,0.961,0.951,0.939,0.927,0.913,0.898,0.882,0.865,0.847,0.828,0.808,0.787,
        0.765,0.742,0.718,0.693,0.667,0.641,0.614,0.586,0.557,0.528,0.498,0.467,0.436,0.404,0.372,0.339,0.306,0.272,0.238,0.204,
        0.170,0.135,0.101,0.066,0.031,-0.004,-0.039,-0.074,-0.109,-0.144,-0.178,-0.213,-0.247,-0.280,-0.314,-0.347,-0.379,-0.412,
        -0.443,-0.474,-0.505,-0.535,-0.564,-0.593,-0.620,-0.647,-0.674,-0.699,-0.724,-0.747,-0.770,-0.792,-0.813,-0.833,-0.852,
        -0.870,-0.886,-0.902,-0.916,-0.930,-0.942,-0.953,-0.963,-0.972,-0.980,-0.986,-0.991,-0.995,-0.998,-1.000,-1.000,-0.999,
        -0.997,-0.994,-0.989,-0.983,-0.976,-0.968,-0.959,-0.948,-0.936,-0.924,-0.910,-0.895,-0.878,-0.861,-0.843,-0.823,-0.803,
        -0.782,-0.759,-0.736,-0.712,-0.687,-0.661,-0.635,-0.607,-0.579,-0.550,-0.520,-0.490,-0.459,-0.428,-0.396,-0.364,-0.331,
        -0.298,-0.264,-0.230,-0.196,-0.162,-0.127,-0.092,-0.057,-0.022,0.013,0.048,0.083,0.117,0.152,0.187,0.221,0.255,0.288,
        0.322,0.355,0.387,0.419,0.451,0.482,0.512,0.542,0.571,0.599,0.627,0.654,0.680,0.705,0.730,0.753,0.776,0.797,0.818,0.837,
        0.856,0.874,0.890,0.906,0.920,0.933,0.945,0.956,0.966,0.974,0.981,0.988,0.992,0.996,0.999,1.000
    ]


    def __init__(self, i2c, address=0x3C, RSTpin=None, width=128, height=32):
        import time

        self.i2c = i2c
        self.address = address
        self.rst = RSTpin
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.buffer = bytearray(width * int(height / 8))

        # Toggle the RST pin over 1ms + 10ms
        self.rst.value = True
        time.sleep(0.001)
        self.rst.value = False
        time.sleep(0.01)
        self.rst.value = True

        # Write the display settings
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYOFF]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETDISPLAYCLOCKDIV, 0x80]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETMULTIPLEX, 0x1F]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETDISPLAYOFFSET, 0x00]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETSTARTLINE]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_CHARGEPUMP, 0x14]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_MEMORYMODE, 0x00]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SEGREMAP]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_COMSCANDEC]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETCOMPINS, 0x02]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETCONTRAST, 0x8F]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETPRECHARGE, 0xF1]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETVCOMDETECT, 0x40]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYALLON_RESUME]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_NORMALDISPLAY]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYON]))

        c = 0x03
        if self.height == 64: c = 0x07
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_COLUMNADDR, 0x00, self.width - 1]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_PAGEADDR, 0x00, c]))

        # Clear the display
        self.clear()
        self.draw()

    def clear(self):
        """
        Clears the display buffer by creating a new one

        Returns:
            The display object
        """
        self.buffer = bytearray(self.width * int(self.height / 8))
        return self

    def set_inverse(self, is_inverse=True):
        """
        Set the entire display to black-on-white or white-on-black

        Args:
            is_inverse (bool): should the display be black-on-white (True) or white-on-black (False).
        """
        if is_inverse is True:
            self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_INVERTDISPLAY]));
        else:
            self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_NORMALDISPLAY]));

    def draw(self):
        """
        Draw the current buffer contents on the screen
        """
        self._render()

    def home(self):
        """
        Set the cursor to the home position, (0, 0), at the top left of the screen

        Returns:
            The display object
        """
        self.move(0, 0)
        return self

    def move(self, x, y):
        """
        Set the cursor to the specified position

        Args:
            x (int) The X co-ordinate in the range 0 - 127
            y (int) The Y co-ordinate in the range 0 - 32 or 64, depending on model

        Returns:
            The display object
        """
        if x < 0 or x > (self.width - 1) or y < 0 or y > (self.height - 1): return
        self.x = x
        self.y = y
        return self

    def plot(self, x, y, color=1):
        """
        Plot a point (or clear) the pixel at the specified co-ordnates

        Args:
            x (int) The X co-ordinate in the range 0 - 127
            y (int) The Y co-ordinate in the range 0 - 32 or 64, depending on model
            color (int) The color of the pixel: 1 for set, 0 for clear. Default: 1

        Returns:
            The display object
        """
        # Bail if any co-ordinates are off the screen
        # TODO better error reporting
        if x < 0 or x > (self.width - 1) or y < 0 or y > (self.height - 1): return

        # Get the buffer byte holding the pixel
        byte = self._coords_to_index(x, y)
        value = self.buffer[byte]
        bit = y - ((y >> 3) << 3)

        if color == 1:
            # Set the pixel
            value = value | (1 << bit)
        else:
            # Clear the pixel
            value = value & ~(1 << bit)

        # Write the buffer byte back
        self.buffer[byte] = value
        return self

    def line(self, x, y, tox, toy, thick=1, color=1):
        """
        Draw a line between the specified co-ordnates

        Args:
            x (int) The start X co-ordinate in the range 0 - 127
            y (int) The start Y co-ordinate in the range 0 - 32 or 64, depending on model
            tox (int) The end X co-ordinate in the range 0 - 127
            toy (int) The end Y co-ordinate in the range 0 - 32 or 64, depending on model
            think (int) The thickness of the line in pixels. Default: 1
            color (int) The color of the pixel: 1 for set, 0 for clear. Default: 1

        Returns:
            The display object
        """
        # Make sure we have a thickness of at least one pixel
        if thick < 1: thick = 1;

        # If necessary swap x and tox so we always scan L-R
        if x > tox:
            a = x;
            x = tox;
            tox = a

        # Calculate the line gradient
        m = float(toy - y) / float(tox - x);
        dy = 0

        # Run for 'thick' times to generate thickness
        for j in range(0, thick):
            # Run from x to tox, calculating the y offset at each point
            for i in range(x, tox):
                dy = y + int(m * (i - x)) + j;
                if i >= 0 and i < self.width and dy >= 0 and dy < self.height:
                    self.plot(i, dy, color)
        return self

    def circle(self, x, y, radius, color=1, fill=False):
        """
        Draw a circle at the specified co-ordnates

        Args:
            x (int) The centre X co-ordinate in the range 0 - 127
            y (int) The centre Y co-ordinate in the range 0 - 32 or 64, depending on model
            radius (int) The radius of the circle
            color (int) The color of the pixel: 1 for set, 0 for clear. Default: 1
            fill (bool) Should the circle be solid (true) or outline (false). Default: false

        Returns:
            The display object
        """
        for i in range(0, 180):
            a = x - int(radius * self.SIN_TABLE[i])
            b = y - int(radius * self.COS_TABLE[i])

            if a >= 0 and a < self.width and b >= 0 and b < self.height:
                self.plot(a, b, color)

                if fill is True:
                    if a > x:
                        j = x
                        while True:
                            self.plot(j, b, color)
                            j += 1
                            if j >= a: break
                    else:
                        j = a + 1
                        while True:
                            self.plot(j, b, color)
                            j += 1
                            if j > x: break
        return self

    def rect(self, x, y, width, height, fill=False):
        """
        Draw a rectangle at the specified co-ordinates

        Args:
            x (int) The start X co-ordinate in the range 0 - 127
            y (int) The start Y co-ordinate in the range 0 - 32 or 64, depending on model
            width (int) The width of the rectangle
            height (int) The height of the rectangle
            fill (bool) Should the rectangle be solid (true) or outline (false). Default: false

        Returns:
            The display object
        """
        # Make sure we only draw on the screen
        if x < 0: x = 0
        if x + width > self.width: width = self.width - x
        if y < 0: y = 0
        if y + height > self.height: height = self.height - y

        for i in range(y, y + height):
            for j in range(x, x + width):
                self.plot(j, i)
                if fill is False and x < j < x + width - 1 and y < i < y + height - 1:
                    self.plot(j, i, 0)
        return self

    def text(self, print_string=None):
        """
        Write a line of text at the current cursor co-ordinates

        Args:
            print_string (string) The text to print

        Returns:
            The display object
        """
        # Bail if any co-ordinates are off the screen
        # TODO better error reporting
        if print_string is None or len(print_string) == 0: return self

        x = self.x
        y = self.y

        for i in range(0, len(print_string)):
            asc = ord(print_string[i]) - 32
            glyph = self.CHARSET[asc]

            for j in range(0, len(glyph) + 1):
                # j adds to x
                if j == len(glyph) and x < 128:
                    c = 0x00
                else:
                    c = self._flip(glyph[j])
                z = -1
                for k in range(0, 8):
                    # k adds to y
                    # z is the bit value in y; deals with y + k extending
                    # beyond byte boundary
                    if ((y + k) % 8) == 0 and k != 0:
                        z = 0
                    else:
                        z += 1

                    b = self._coords_to_index(x , y + k)
                    v = self.buffer[b]
                    if c & (1 << z) != 0: v = v | (1 << z)
                    self.buffer[b] = v

                # Move on one pixel
                x += 1
                if x > 127:
                    # Right side hit, so move to next text line
                    if y + 8 < self.height:
                        x = 0
                        y += 8
                    else:
                        break
        return self

    def length_of_string(self, print_string):
        """
        Calculate the length in pixels of a proportionally spaced string

        Args:
            print_string (string) The text to print

        Returns:
            The string's length in pixels
        """
        length = 0
        if print_string is None or len(print_string) == 0: return -1
        for i in range(0, len(print_string)):
            asc = ord(print_string[i]) - 32
            glyph = self.CHARSET[asc]
            length += (len(glyph) + 1)
        return length

    # PRIVATE FUNCTIONS

    def _render(self):
        """
        Write the display buffer out to I2C
        """
        buffer = bytearray(len(self.buffer) + 1)
        buffer[1:] = self.buffer
        buffer[0] = self.SSD1306_WRITETOBUFFER
        self.i2c.writeto(self.address, bytes(buffer))

    def _coords_to_index(self, x, y):
        """
        Convert pixel co-ordinates to a bytearray index
        Calling function should check for valid co-ordinates first

        Returns:
            An index value (integer)
        """
        return ((y >> 3) * self.width) + x

    def _indexToCoords(self, idx):
        """
        Convert bytearray index to pixel co-ordinates

        Returns:
            X and Y co-ordinates in a tuple
        """
        y = idx >> 4
        x = idx - (y << 4)
        return (x, y)

    def _flip(self, value):
        """
        Rotates the character array from the saved state
        to that required by the screen orientation

        Returns:
            Flipped value as integer
        """
        flipped = 0
        for i in range (0, 8):
            if (value & (1 << i)) > 0:
                flipped += (1 << (7 - i))
        return flipped