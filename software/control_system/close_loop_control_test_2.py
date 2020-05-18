# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from actuators.tic_usb import *
from sensors.rotary_encoder import RotatoryEncoder
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
