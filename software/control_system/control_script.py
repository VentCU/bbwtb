
# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from .actuators.tic_usb import *
from .sensors.pressure_sensor import PressureSensor
from .sensors.limit_switch import LimitSwitch
from .sensors.rotary_encoder import RotatoryEncoder

# create a motor controller object
motor_controller = TicUSB()

# create the rotary encoder
encoder = RotatoryEncoder(22, 24)

# create a pressure sensor object
pressure_sensor = PressureSensor()

# create the limit switches
upper_switch = LimitSwitch()   # TODO determine the ports
lower_switch = LimitSwitch()


while True:

    pass


