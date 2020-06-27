#
# alarm handler class.
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#
import sys
from alarms.alarms import *
sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/actuators')
from actuators import buzzer
sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/configs')
from configs import gpio_map


class AlarmHandler:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller
        self.buzzer = buzzer.Buzzer(gpio_map.BUZZER_PIN_1)
        
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
            raise alarm

    def over_pressure(self):
        self.controller.start_ventilation()     # TODO: this needs to be threaded

    def under_pressure(self):
        pass

    def position_error(self):
        pass

    def homing_error(self):
        pass

    def system_fault(self):
        pass

    # TODO: handler function for each alarm type

# test
if __name__ is "__main__":
    buz = buzzer.Buzzer(gpio_map.BUZZER_PIN_1)
    ctr = 0
    while(ctr < 100):
        sleep(0.1)
        ctr += 1
        buz.enable_buzzer()
    buz.disable_buzzer()