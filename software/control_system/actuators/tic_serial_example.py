#
# Tic Motor controller Serial example code
#
# (c) VentCU, 2020, All Rights Reserved.

import serial
from tic_serial import TicSerial

# Choose the serial port name.
port_name = "/dev/ttyAMA0"

# Choose the baud rate (bits per second).  This must match the baud rate in
# the Tic's serial settings.
baud_rate = 9600

# Change this to a number between 0 and 127 that matches the device number of
# your Tic if there are multiple serial devices on the line and you want to
# use the Pololu Protocol.
device_number = None

port = serial.Serial(port_name, baud_rate, timeout=0.1, write_timeout=0.1)

tic = TicSerial(port, device_number)

position = tic.get_current_position()
print("Current position is {}.".format(position))

new_target = -200 if position > 0 else 200
print("Setting target position to {}.".format(new_target))
tic.set_target_position(new_target)
