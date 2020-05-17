# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from .actuators.tic_usb import *
from .sensors.pressure_sensor import PressureSensor
from .sensors.rotary_encoder import RotatoryEncoder
from time import sleep

# define some global vars
encoder_value = 0


def encoder_callback(value):
    global encoder_value
    encoder_value = value
    print(encoder_value)


# create a motor controller object
motor_controller = TicUSB()

# create the rotary encoder
encoder = RotatoryEncoder(16, 18, callback=encoder_callback)

# create a pressure sensor object
pressure_sensor = PressureSensor()

while True:

    sleep(0.01)

    pass
