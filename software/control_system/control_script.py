#

# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from .actuators.tic_serial import *
from .sensors.pressure_sensor import PressureSensor
from .sensors.limit_switch import LimitSwitch
from .sensors.rotary_encoder import RotatoryEncoder

# create a motor controller object
_port = serial_port(port_name="/dev/ttyACM0", baud_rate=9600)
motor_controller = TicSerial(port=_port, device_number=None)

# create the rotary encoder
encoder = RotatoryEncoder()

# create a pressure sensor object
pressure_sensor = PressureSensor()

# create the limit switches
upper_switch = LimitSwitch()   # TODO determine the ports
lower_switch = LimitSwitch()


while True:

    pass


