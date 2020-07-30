#
# main ventilator class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

import signal
import sys
import pigpio

from logger import LoggerInit
from actuators.motor import Motor
from sensors.rotary_encoder import RotaryEncoder
from sensors.limit_switch import LimitSwitch
from sensors.power_switch import PowerSwitch
from sensors.pressure_sensor import PressureSensor
from configs.gpio_map import *
# from sensors.flow_sensor import FlowSensor

from ventilator_controller import VentilatorController
from gui.ui import UI
from ui_controller_interface import UIControllerInterface


class Ventilator:

    def __init__(self):

        # start logger
        logger = LoggerInit()

        # instantiate sensors
        self.encoder = RotaryEncoder(pigpio.pi(), ENCODER_B_PLUS_PIN, ENCODER_A_PLUS_PIN)
        self.contact_switch = LimitSwitch(CONTACT_SWITCH_PIN)
        self.absolute_switch = LimitSwitch(ABSOLUTE_SWITCH_PIN)
        self.power_switch = PowerSwitch(POWER_SWITCH_PIN)
        # self.pressure_sensor = PressureSensor()
        # self.flow_sensor = FlowSensor(FLOW_SENSOR_PIN)

        # instantiate actuators
        self.motor = Motor(self.encoder)

        # instantiate controller
        self.controller = VentilatorController(self.motor,
                                               None,
                                               self.absolute_switch,
                                               self.contact_switch,
                                               self.power_switch)

        # instantiate ui
        self.ui = UI()

        self.ui_controller_interface = UIControllerInterface(self.ui, self.controller)

    def at_exit(self, sig, frame):
        print("Exiting program...")
        self.controller.stop_ventilation()
        sys.exit(0)


def test():
    test_ventilator = Ventilator()
    signal.signal(signal.SIGINT, test_ventilator.at_exit)
    sys.exit(test_ventilator.ui.app.exec_())


if __name__ == "__main__":
    test()
