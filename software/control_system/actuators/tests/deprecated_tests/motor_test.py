#!/usr/bin/python
#
# TicDevice and PID test
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

import matplotlib.pyplot as plt
from time import sleep
from actuators.motor import Motor
import pigpio
from sensors.rotary_encoder import RotaryEncoder
import numpy as np

motor = Motor(RotaryEncoder(pigpio.pi(), 18, 16))

encoder_u_limit = 400
encoder_l_limit = 0

# initialize the goal of the motor
goal = encoder_u_limit

i = 0

if __name__ == "__main__":

    while i < 10:

        result, vel = motor.move_to_encoder_pose(goal)
       
        print(vel)
        if motor.encoder_position() == encoder_u_limit and result is True:
            print("{}, {}, {}".format(vel, motor.encoder_position(), motor.motor_position()))
            # print("updating setpoint")
            sleep(1.5)
            i += 2
            goal = encoder_l_limit

        elif motor.encoder_position() == encoder_l_limit and result is True:
            print("{}, {}, {}".format(vel, motor.encoder_position(), motor.motor_position()))
            # print("updating setpoint")
            sleep(1.5)
            goal = encoder_u_limit


motor.tic_device.set_target_position(0)
motor.destructor()
exit()

