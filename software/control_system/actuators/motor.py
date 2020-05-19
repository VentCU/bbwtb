#
# motor class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from actuators.tic import *
from sensors.rotary_encoder import RotaryEncoder

class Motor:

    def __init__(self, rotary_encoder):

        self.motor = TicDevice()
        self.motor.open(vendor=0x1ffb, product_id=0x00CB)

        self.encoder = rotary_encoder
