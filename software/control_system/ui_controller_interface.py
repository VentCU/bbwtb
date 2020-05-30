
from alarms.alarm_handler import AlarmsHandler


class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.alarm_handler = AlarmsHandler(self.ui, self.controller)

        self.interface_elements()

    def interface_elements(self):

        self.ui.stack.start.start_button.clicked.connect( lambda:
            try:
                self.controller.start()
            except Alarm:
                self.alarm_handler.over_pressure()
        )

        # TODO: connect UI elements....
