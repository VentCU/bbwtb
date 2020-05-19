#
# main ventilator class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from gpio_map import *

from actuators.motor import Motor

# from sensors.flow_sensor import FlowSensor
# from sensors.pressure_sensor import PressureSensor
# from sensors.limit_switch import LimitSwitch

from gui.ui import UI


class Ventilator:

    def __init__(self):

        # instantiate sensors
        # self.encoder = RotaryEncoder( encoder_a_plus_pin, encoder_b_plus_pin )
        # self.contact_switch = LimitSwitch( contact_switch_pin )
        # self.absolute_switch = LimitSwitch( absolute_switch_pin )
        # self.flow_sensor = FlowSensor( flow_sensor_pin )
        # self.pressure_graph = PressureSensor ( pressure_sensor_pin )

        # instantiate actuators
        # self.motor = Motor(encoder)

        # instantiate ui
        self.ui = UI()

def test():
    test_ventilator = Ventilator()

if __name__ == "__main__":
    test()
