#!/usr/bin/python


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

pid = PID()

encoder_u_limit = 200
encoder_l_limit = -200

if __name__ == "__main__":
    
    while True:
        
        pid.setpoint = encoder_u_limit
        pid.update(encoder_value)
        value = pid.output

        print(value)

