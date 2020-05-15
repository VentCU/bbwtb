# Uses the pySerial library to send and receive data from a Tic.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".
# NOTE: You will need to change the "port_name =" line below to specify the
#   right serial port.

import serial
import subprocess


def serial_port(port_name, baud_rate):
    return serial.Serial(port_name, baud_rate, timeout=0.1, write_timeout=0.1)


def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))


class TicSerial(object):
    def __init__(self, port, device_number=None):
        self.port = port
        self.device_number = device_number

    def send_command(self, cmd, *data_bytes):
        if self.device_number is None:
            header = [cmd]  # Compact protocol
        else:
            header = [0xAA, self.device_number, cmd & 0x7F]  # Pololu protocol

        print(bytes(header + list(data_bytes)))
        self.port.write(bytes(header + list(data_bytes)))

    # Sends the "Exit safe start" command.
    def exit_safe_start(self):
        self.send_command(0x83)

    # Sets the target position.
    # For more information about what this command does, see the
    # "Set target position" command in the "Command reference" section of the
    # Tic user's guide.
    def set_target_position(self, target):
        self.send_command(0xE0,
                          ((target >> 7) & 1) | ((target >> 14) & 2) |
                          ((target >> 21) & 4) | ((target >> 28) & 8),
                          target >> 0 & 0x7F,
                          target >> 8 & 0x7F,
                          target >> 16 & 0x7F,
                          target >> 24 & 0x7F)

    def set_max_speed(self, speed):
        ticcmd('--max-speed', str(speed))

    def set_starting_speed(self, speed):
        ticcmd('--starting-speed', str(speed))

    # Gets one or more variables from the Tic.
    def get_variables(self, offset, length):
        self.send_command(0xA1, offset, length)
        result = self.port.read(length)
        if len(result) != length:
            raise RuntimeError("Expected to read {} bytes, got {}."
                               .format(length, len(result)))
        return bytearray(result)

    # Gets the "Current position" variable from the Tic.
    def get_current_position(self):
        b = self.get_variables(0x22, 4)
        position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
        if position >= (1 << 31):
            position -= (1 << 32)
        return position

