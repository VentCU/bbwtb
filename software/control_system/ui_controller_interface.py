
from alarms.alarm_handler import AlarmHandler
from alarms.alarms import *


class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.alarm_handler = AlarmHandler(self.ui, self.controller)

        self.interface_elements()

    def interface_elements(self):

        self.ui.stack.start.start_button.clicked.connect(
            lambda: self.try_start_ventilation()
        )

        # TODO: connect UI elements....

    def try_start_ventilation(self):
        try:
            self.controller.start_ventilation()
        except Alarm as alarm:
            self.alarm_handler.handle_alarms(alarm)