#!/usr/bin/python
#
# TicDevice and PID test
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#


from time import sleep
from actuators.pid_controller import PID
from actuators.tic_usb import *
import pigpio
from sensors.rotary_encoder import RotaryEncoder


# define some global vars
encoder_value = 0

# create a motor controller object
ticdev = TicDevice()
ticdev.open(vendor=0x1ffb, product_id=0x00CB)

# create the encoder object
pi = pigpio.pi()
encoder = RotaryEncoder(pi, 18, 16)

# create the PID controller
pid = PID(P=100, D=12.0, I=0)

encoder_u_limit = 400
encoder_l_limit = 0

pid.setpoint = encoder_u_limit

if __name__ == "__main__":

    while True:

        encoder_value = encoder.value()
        pid.update(encoder_value)
        value = pid.output * 15000.0 if pid.output < 1000000 else 100000
        ticdev.get_variables()
        motor_pose = ticdev.variables['current_position']
        ticdev.set_target_velocity(int(value))
        print("{}, {}, {}".format(int(value), encoder_value, motor_pose))
    
        if encoder_value == encoder_u_limit and value == 0:
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_l_limit
        elif encoder_value == encoder_l_limit and value == 0:
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_u_limit
            
        
ticdev.halt_and_hold()
encoder.cancel()
pi.stop()

exit()

