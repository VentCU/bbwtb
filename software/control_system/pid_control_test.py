#!/usr/bin/python

from time import sleep
import time
import threading
from pid_controller import PID
from actuators.tic import *
<<<<<<< HEAD
from sensors.rotary_encoder import RotatoryEncoder
import pigpio
from encoder_new import decoder
=======
from sensors.rotary_encoder import RotaryEncoder
>>>>>>> 03c26994e9da1b0532fd21d645e03383cb2b937f

# define some global vars
encoder_value = 0


def callback(way):
    global encoder_value
    encoder_value += way


# create a motor controller object
ticdev = TicDevice()
ticdev.open(vendor=0x1ffb, product_id=0x00CB)

<<<<<<< HEAD

pi = pigpio.pi()

decoder = decoder(pi, 18, 16, callback)
=======
# create the rotary encoder
try:

encoder = RotaryEncoder(16, 18, callback=encoder_callback)
>>>>>>> 03c26994e9da1b0532fd21d645e03383cb2b937f

pid = PID(P=100, D=12.0, I=0)

encoder_u_limit = 400
encoder_l_limit = 0

pid.setpoint = encoder_u_limit

if __name__ == "__main__":

    while True:

        # sleep(0.01)
        pid.update(encoder_value)
        value = pid.output * 15000.0 if pid.output < 1000000 else 100000
        ticdev.get_variables()
        motor_pose = ticdev.variables['current_position']
        ticdev.set_target_velocity(int(value))
        print("{}, {}, {}".format(int(value), encoder_value, motor_pose))
<<<<<<< HEAD
    
        if (encoder_value == encoder_u_limit and value == 0):
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_l_limit
        elif (encoder_value == encoder_l_limit and value == 0):
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_u_limit
            
        
ticdev.hault_and_hold()

decoder.cancel()
pi.stop()

exit()
=======

#         if (encoder_value == encoder_u_limit and value == 0):
#             # print("updating setpoint")
#             sleep(1.5)
#             pid.setpoint = encoder_l_limit
#         elif (encoder_value == encoder_l_limit and value == 0):
#             # print("updating setpoint")
#             sleep(1.5)
#             pid.setpoint = encoder_u_limit



ticdev.hault_and_hold()

exit()
>>>>>>> 03c26994e9da1b0532fd21d645e03383cb2b937f
