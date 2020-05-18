#!/usr/bin/python

from time import sleep
import time
from pid_controller import PID
from actuators.tic_usb import TicUSB
from sensors.rotary_encoder import RotatoryEncoder

# define some global vars
encoder_value = 0


def encoder_callback(value):
    global encoder_value
    encoder_value = value

# create a motor controller object
motor_controller = TicUSB()

# create the rotary encoder
encoder = RotatoryEncoder(16, 18, callback=encoder_callback)

pid = PID(P=100, D=2.0, I=0)

encoder_u_limit = 100
encoder_l_limit = 0

if __name__ == "__main__":
    
    while True:
        
        pid.setpoint = encoder_u_limit
        pid.update(encoder_value)
        value = pid.output * 20000.0 if pid.output < 1000000 else 100000
        
        motor_pose = 0 # motor_controller.get_current_position()
        motor_controller.set_target_velocity(int(value))
        print("{}, {}, {}".format(int(value), encoder_value, motor_pose))
        
        sleep(0.5)
        

motor_controller.hault_and_hold()

exit()
        # print(time.time() - start)