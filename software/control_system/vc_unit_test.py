#
#
# unit testing script for the ventilator
# controller class
#

import pigpio
from configs.gpio_map import *
from actuators.motor import Motor
from sensors.rotary_encoder import RotaryEncoder
from sensors.limit_switch import LimitSwitch
from sensors.power_switch import PowerSwitch
from ventilator_controller import VentilatorController

if __name__ == "__main__":
    encoder = RotaryEncoder(pigpio.pi(), ENCODER_B_PLUS_PIN, ENCODER_A_PLUS_PIN)
    contact_switch = LimitSwitch(CONTACT_SWITCH_PIN)
    absolute_switch = LimitSwitch(ABSOLUTE_SWITCH_PIN)
    power_switch = PowerSwitch(POWER_SWITCH_PIN)

    # instantiate actuators
    motor = Motor(encoder)

    # instantiate controller
    controller = VentilatorController(motor,
                                      None,
                                      absolute_switch,
                                      contact_switch,
                                      power_switch)

    controller.start_homing()

    controller.start_ventilation()
