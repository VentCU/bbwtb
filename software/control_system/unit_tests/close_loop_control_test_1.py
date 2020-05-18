# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from ..actuators.tic_usb import *
from ..sensors.rotary_encoder import RotatoryEncoder
from time import sleep

# define some global vars
encoder_value = 0


def encoder_callback(value):
    global encoder_value
    encoder_value = value


# create a motor controller object
motor_controller = TicUSB()

# create the rotary encoder
encoder = RotatoryEncoder(16, 18, callback=encoder_callback)

while encoder_value < 200:
    sleep(0.0001)
    # print("encoder: {}".format(encoder_value))
    pass

motor_controller.hault_and_hold()
print("finished moving half a rotation: pose: {}".format(encoder_value))
