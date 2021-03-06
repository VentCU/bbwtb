# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '')))

import pigpio
from actuators.tic_usb import *
from sensors.rotary_encoder import RotaryEncoder
from time import sleep

# define some global vars
encoder_value = 0


def encoder_callback(value):
    global encoder_value
    encoder_value = value
    

# create a motor controller object
motor_controller = TicDevice()
motor_controller.open(vendor=0x1ffb, product_id=0x00CB)

# create the rotary encoder
encoder = RotaryEncoder(pigpio.pi(), 16, 18)

encoder_u_limit = 200
encoder_l_limit = -200

controller_limit = 12800

while True:

    # from lower to upper
    motor_controller.enter_safe_start()
    motor_controller.set_target_position(controller_limit)
    while encoder_value < encoder_u_limit:
        sleep(0.0001)

    motor_controller.hault_and_hold()
    print("half a rotation: pose: {} {}".format(encoder_value,
                                                motor_controller.get_current_position()))
    sleep(1)

    # from upper to lower
    motor_controller.enter_safe_start()
    motor_controller.set_target_position(-controller_limit)
    while encoder_value > encoder_l_limit:
        sleep(0.0001)

    motor_controller.hault_and_hold()
    print("half a rotation: pose: {} {}".format(encoder_value,
                                                motor_controller.get_current_position()))
    sleep(1)

    pass
