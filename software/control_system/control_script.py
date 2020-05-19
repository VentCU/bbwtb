#
# Control system script for
# VentCU - An open source ventilator
# 
# (c) VentCU, 2020. All Rights Reserved. 
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

import pigpio

from actuators.tic_usb import *
from sensors.pressure_sensor import PressureSensor
from sensors.limit_switch import LimitSwitch
from sensors.rotary_encoder import RotaryEncoder
from configs.gpio_map import *


class VentilatorController:

    def __init__(self):

        # create a motor controller object
        self.ticdev = TicDevice()
        self.ticdev.open(vendor=0x1ffb, product_id=0x00CB)

        # create the rotary encoder
        pi = pigpio.pi()
        self.encoder = RotaryEncoder(pi, ENCODER_A_PLUS_PIN, ENCODER_B_PLUS_PIN, callback=self.encoder_callback)

        # create a pressure sensor object
        self.pressure_sensor = PressureSensor()

        # create the limit switches
        self.upper_switch = LimitSwitch(ABSOLUTE_SWITCH_PIN)
        self.lower_switch = LimitSwitch(CONTACT_SWITCH_PIN)

        # init class variables
        self.encoder_value = 0              # the current encoder value
        self.contact_encoder_val = 0        # at the point of contact of the ambu bag, what's the encoder value.
        self.abs_limit_encoder_val = 0      # at the point of abs limit, what's the encoder value.
        self.homing_finished = False
        self.__homing_dir = 1

    def start(self):

        while True:
            if self.homing_finished is False:
                self.initial_homing_procedure()
            else:
                print("Homing completed")

    def encoder_callback(self, value):
        self.encoder_value += value

    def initial_homing_procedure(self):

        if self.homing_finished is True:
            raise Exception("Homing is already finished, why are you homing again?")

        # making contact with upper switch
        if self.upper_switch.get_status() is 0 and self.lower_switch.get_status() is 1:

            ticdev.halt_and_hold()
            ticdev.get_variables()
            motor_pose = ticdev.variables['current_position']
            self.abs_limit_encoder_val = self.encoder_value
            self.__homing_dir = -1
            print("Upper bound for motor reached. \n "
                  "Motor current position: {}".format(motor_pose))

        # making contact with lower switch
        elif self.upper_switch.get_status() is 1 and self.lower_switch.get_status() is 0:

            ticdev.halt_and_hold()
            ticdev.get_variables()
            motor_pose = ticdev.variables['current_position']
            self.contact_encoder_val = self.encoder_value
            self.homing_finished = True
            print("Lower bound for motor reached. \n "
                  "Motor current position: {}".format(motor_pose))

        # no contact with any switch
        elif self.upper_switch.get_status() is 1 and self.lower_switch.get_status() is 1:
            ticdev.set_target_velocity(self.__homing_dir * 2000000)

        # contact with both switchs -- error
        elif self.upper_switch.get_status() is 0 and self.lower_switch.get_status() is 0:
            raise Exception("Both contact switches are pressed. Fatal error.")  # Todo: error handling.


