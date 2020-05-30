from alarms import *

class AlarmHandler:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

    def handle_alarms(self, ALARM):

        if type(ALARM) is type(OVER_PRESSURE_ALARM):        # TODO: check that this works
            self.controller.current_alarms.append(ALARM)
            self.over_pressure()

        # elif ...

    def over_pressure(self):
        self.controller.alarm_condition = True
        self.controller.start_ventilation()


    # TODO: handler function for each alarm type
