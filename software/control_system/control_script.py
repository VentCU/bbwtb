
# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from actuators.tic_usb import *
# can't import PressureSensor yet bc it is built on arduino libraries
# from sensors.pressure_sensor import PressureSensor
from sensors.limit_switch import LimitSwitch
from sensors.rotary_encoder import RotaryEncoder

# create a motor controller object
motor_controller = TicUSB()

encoder_value = 0

def encoder_callback(value):
    global encoder_value
    encoder_value = value

# create the rotary encoder
encoder = RotaryEncoder(16, 18, callback=encoder_callback)

# create a pressure sensor object
# pressure_sensor = PressureSensor()

# create the limit switches
upper_switch = LimitSwitch(23)   # TODO determine the ports
# lower_switch = LimitSwitch()

motor_controller.enter_safe_start()
motor_controller.set_target_velocity(199999)

while True:

    if upper_switch.get_switch_status() is 0:
       motor_controller.hault_and_hold()
       break

print("f u noah")

