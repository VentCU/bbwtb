#
# Alarm classes, defines types of alarms
# that can be handled by the ventilator.
#
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#


class Alarm(Exception):

    # TODO: the alarm type param hasn't been implemented
    def __init__(self, message="ALARM", alarm_type=0):
        self.message = message
        self.exc_type = alarm_type


class OVER_PRESSURE_ALARM(Alarm):
    # need pressure sensor readings
    pass


class UNDER_PRESSURE_ALARM(Alarm):
    # need pressure sensor readings
    pass

class HOMING_ALARM(Alarm):
    pass


class POSITION_ALARM(Alarm):
    pass


class SYSTEM_ALARM(Alarm):
    pass

# TODO: do we need more alarm types?
