#
# main ventilator class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

import pigpio

from actuators.motor import Motor
from sensors.rotary_encoder import RotaryEncoder
from sensors.limit_switch import LimitSwitch
from sensors.pressure_sensor import PressureSensor
from configs.gpio_map import *
# from sensors.flow_sensor import FlowSensor

from ventilator_controller import VentilatorController

from gui.ui import UI


class Ventilator:

    def __init__(self):

        # instantiate sensors
        self.encoder = RotaryEncoder(pigpio.pi(), ENCODER_B_PLUS_PIN, ENCODER_A_PLUS_PIN)
        self.contact_switch = LimitSwitch(CONTACT_SWITCH_PIN)
        self.absolute_switch = LimitSwitch(ABSOLUTE_SWITCH_PIN)
        self.pressure_sensor = PressureSensor()
        # self.flow_sensor = FlowSensor(FLOW_SENSOR_PIN)

        # instantiate actuators
        self.motor = Motor(self.encoder)

        # instantiate controller
        self.controller = VentilatorController(self.motor,
                                               self.pressure_sensor,
                                               self.absolute_switch,
                                               self.contact_switch)

        # instantiate ui
        # self.ui = UI()


def test():
    test_ventilator = Ventilator()
    test_ventilator.controller.start()


if __name__ == "__main__":
    test()
