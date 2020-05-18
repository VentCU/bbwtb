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

pid = PID(P=100, D=10.0, I=0)

encoder_u_limit = 150
encoder_l_limit = 0

pid.setpoint = encoder_u_limit

if __name__ == "__main__":
    
    while True:
    
        pid.update(encoder_value)
        value = pid.output * 15000.0 if pid.output < 1000000 else 100000
        
        motor_pose = motor_controller.get_current_position()
        motor_controller.set_target_velocity(int(value))
        print("{}, {}, {}".format(int(value), encoder_value, motor_pose))
    
        if (encoder_value == encoder_u_limit and value == 0):
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_l_limit
        elif (encoder_value == encoder_l_limit and value == 0):
            # print("updating setpoint")
            sleep(1.5)
            pid.setpoint = encoder_u_limit
            
        
    
motor_controller.hault_and_hold()

exit()