class OneWire:

    # Errors and error messages
    READ_NO_ERR = 0
    READ_ERR_NO_DEVICES = 1
    READ_ERR_NO_BUS = 2
    READ_NO_ERR_MESSAGE = "No Error."
    READ_ERR_NO_DEVICES_MESSAGE = "No 1-Wire device connected."
    READ_ERR_NO_BUS_MESSAGE = "No 1-Wire circuit detected."

    # Properties
    uart = None
    current_id = None
    devices = None
    next_device = 0
    read_error = 0
    errors = None

    def __init__(self, uart):
        import serial
        self.uart = serial.Serial(uart)
        self.devices = []
        self.current_id = []
        self.errors = [self.READ_NO_ERR_MESSAGE,
                       self.READ_ERR_NO_DEVICES_MESSAGE,
                       self.READ_ERR_NO_BUS_MESSAGE]
        self.init()

    def init(self):
        # Reset and test the bus if it's good, enumerate the devices on the bus
        # Returns true if the initialization is successful, false if not
        if self.reset(): self.discover_devices()
        return (self.read_error == self.READ_NO_ERR_MESSAGE)

    def reset(self):
        # Reset the 1-Wire bus and check for connected devices
        # Returns true only if there is at least one valid 1-Wire device connected
        # On error, a reason code is saved in _readError, and this can be
        # read using get_error_code()

        # Configure UART for 1-Wire RESET timing
        self.uart.baudrate = 9600
        self.uart.open()
        self.uart.write(0xF0)
        #self.uart.flush()
        read_value = self.uart.read()[0]
        print(read_value)
        if read_value == 0xF0:
            # UART RX will read TX if there are no devices connected
            self.read_error = self.READ_ERR_NO_DEVICES_MESSAGE
            return False
        elif read_value == -1:
            # A general UART read error - most likely nothing wired up
            self.read_error = self.READ_ERR_NO_BUS_MESSAGE
            return False

        # Switch UART to 1-Wire data speed timing
        self.uart.baudrate = 115200
        self.read_error = self.READ_NO_ERR_MESSAGE
        return True

    def discover_devices(self):
        # Enumerate the devices on the 1-Wire bus and store their unique 1-Wire IDs
        # in the 'devices' array
        self.devices = []
        self.current_id = [0,0,0,0,0,0,0,0]

        # Begin the enumeration at address 65
        self.next_device = 65

        while True:
            if self.next_device <= 0: break
            self.next_device = self.search(self.next_device)
            self.devices.append(self.current_id)

    def get_device_count(self):
        # Returns the number of devices on the 1-Wire bus
        return len(self.devices)

    def get_device(self, device_index):
        # Returns a specific device’s ID
        if device_index < 0 or device_index > self.get_device_count(): return None
        return self.devices[device_index]

    def get_devices(self):
        # Returns the array containing all the connected devices’ IDs
        return self.devices

    def get_error_code(self):
        # Returns the current read error information this is cleared
        # every time reset() is called
        return (self.read_error, self.errors[self.read_error])

    def write_byte(self, byte):
        # Write a byte of data or a command to the 1-Wire bus
        byte = 0
        for i in range(0, 8):
            # Run through the bits in the byte, extracting the
            # LSB (bit 0) and sending it to the bus
            self.read_write_bit(byte & 0x01)
            byte = byte >> 1

    def read_byte(self):
        # Read a byte from the 1-Wire bus
        byte = 0
        for b in range(0, 8):
            # Build up byte bit by bit, LSB first
            byte = (byte >> 1) + 0x80 * self.read_write_bit(1)
        return byte

    # 1-Wire command functions - these are single-byte standard commands
    # see https:#electricimp.com/docs/resources/onewire/

    def skip_rom(self):
        # Ignore device ID(s)
        self.write_byte(0xCC)

    def read_rom(self):
        # Read a device’s ID
         self.write_byte(0x33)

    def search_rom(self):
        # Begin enumerating IDs
         self.write_byte(0xF0)

    def match_rom(self):
        # Select a device with a specific ID
        # Next 64 bits to be written will be the known ID
         self.write_byte(0x55)

    #-------------------- PRIVATE METHODS --------------------#

    def read_write_bit(self, bit):
        # Clock out a bit-as-a-byte value then immediately
        # clock in a byte-as-a-bit value and return it
        bit = 0xFF if bit else 0x00
        self.uart.write(bit)
        self.uart.flush()
        rv = 1 if self.uart.read()[0] == 0xFF else 0
        return rv

    def search(self, next_node):
        # Device enumeration support function. Progresses one step up the tree
        # from the current device, returning the next current device along.
        # Called by discover_devices()
        last_fork_point = 0

        # Reset the bus and exit if no device found
        if self.reset():
            # If there are 1-Wire device(s) on the bus - for which one_wire_reset()
            # checks - this function readies them by issuing the 1-Wire SEARCH command (0xF0)
            self.search_rom()

            # Work along the 64-bit ROM code, bit by bit, from LSB to MSB
            for i in range(64, -1, -1):
                byte = int((i - 1) / 8)

                # Read bit from bus
                bit = self.read_write_bit(1)

                # Read the next bit, the first's complement
                if self.read_write_bit(1):
                    if bit:
                        # If first bit is 1 too, this indicates no further devices
                        # so put pointer back to the start and break out of the loop
                        last_fork_point = 0
                        break
                elif not bit:
                    # First and second bits are both 0
                    if next_node > i or (next_node != i and self.current_id[byte] & 1):
                        # Take the '1' direction on this point
                        bit = 1
                        last_fork_point = i

                # Write the 'direction' bit. If it's, say, 1, then all further
                # devices with a 0 at the current ID bit location will go offline
                self.read_write_bit(bit)

                # Shift out the previous path bits, add on the msb side the new chosen path bit
                self.current_id[byte] = (self.current_id[byte] >> 1) + 0x80 * bit

        # Return the last fork point for next search
        return last_fork_point