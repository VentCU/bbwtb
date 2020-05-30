#
# alarm handler class.
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from alarms.alarms import *


class AlarmHandler:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

    def handle_alarms(self, alarm):

        self.controller.current_alarms.append(alarm)
        self.controller.alarm_condition = True

        if type(alarm) is type(OVER_PRESSURE_ALARM):        # TODO: check that this works
            self.over_pressure()

        elif type(alarm) is type(UNDER_PRESSURE_ALARM):
            self.under_pressure()

        elif type(alarm) is type(HOMING_ALARM):
            self.homing_error()

        elif type(alarm) is type(POSITION_ALARM):
            self.position_error()

        elif type(alarm) is type(SYSTEM_ALARM):
            self.system_fault()

        else:
            raise Exception("Undefined alarm type.")

    def over_pressure(self):
        self.controller.start_ventilation()

    def under_pressure(self):
        pass

    def position_error(self):
        pass

    def homing_error(self):
        pass

    def system_fault(self):
        pass

    # TODO: handler function for each alarm type
