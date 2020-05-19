#
# motor class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from actuators.tic_usb import *
from sensors.rotary_encoder import RotaryEncoder

class Motor:

    def __init__(self, rotary_encoder):

        # create a motor controller object
        self.motor = TicDevice()
        self.motor.open(vendor=0x1ffb, product_id=0x00CB)

        self.encoder = rotary_encoder

    def set_velocity(self, velocity):
        self.motor.set_target_velocity(velocity)

    def stop(self):
        self.motor.halt_and_hold()

    def motor_position(self):
        self.motor.get_variables()
        return self.motor.variables['current_position']

    def encoder_position(self):
        return self.encoder.value()
