# Uses the pySerial library to send and receive data from a Tic.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".
# NOTE: You will need to change the "port_name =" line below to specify the
#   right serial port.

import serial
import subprocess
import yaml


def serial_port(port_name, baud_rate):
    return serial.Serial(port_name, baud_rate, timeout=0.5, write_timeout=0.5)


def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))


class TicSerial(object):
    def __init__(self):
        pass

    # Sends the "Exit safe start" command.
    def exit_safe_start(self):
        ticcmd('--exit-safe-start')

    # Sets the target position.
    # For more information about what this command does, see the
    # "Set target position" command in the "Command reference" section of the
    # Tic user's guide.
    def set_target_position(self, target):
        ticcmd('--exit-safe-start', '--position', str(target))

    def set_max_speed(self, speed):
        ticcmd('--max-speed', str(speed))

    def set_starting_speed(self, speed):
        ticcmd('--starting-speed', str(speed))

    # Gets the "Current position" variable from the Tic.
    def get_current_position(self):
        
        status = yaml.load(ticcmd('-s', '--full'))
 
        position = status['Current position']
        print("Current position is {}.".format(position))
        return position
