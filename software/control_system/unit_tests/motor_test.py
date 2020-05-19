#!/usr/bin/python
#
# TicDevice and PID test
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#


from time import sleep
from actuators.motor import Motor
import pigpio
from sensors.rotary_encoder import RotaryEncoder

motor = Motor(RotaryEncoder(pigpio.pi(), 18, 16))

encoder_u_limit = 400
encoder_l_limit = 0

# initialize the goal of the motor
goal = encoder_u_limit

if __name__ == "__main__":

    while True:

        result = motor.move_to_encoder_pose(goal)
    
        if motor.encoder_position() == encoder_u_limit and result is True:
            print("updating setpoint")
            sleep(1.5)
            goal = encoder_l_limit
        elif motor.encoder_position() == encoder_l_limit and result is True:
            print("updating setpoint")
            sleep(1.5)
            goal = encoder_u_limit

motor.destructor()

exit()

