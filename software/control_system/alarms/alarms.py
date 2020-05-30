#
# Alarm classes, defines types of alarms
# that can be handled by the ventilator.
#
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#


class Alarm(Exception):

    def __init__(self, message, alarm_type):
        self.message = message
        self.type = alarm_type


class OVER_PRESSURE_ALARM(Alarm):
    pass


class UNDER_PRESSURE_ALARM(Alarm):
    pass

class HOMING_ALARM(Alarm):
    pass


class POSITION_ALARM(Alarm):
    pass


class SYSTEM_ALARM(Alarm):
    pass

# TODO: do we need more alarm types?
