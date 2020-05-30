
class Alarm(Exception):

    def __init__(self, alarm_type):
        self.type = alarm_type


class OVER_PRESSURE_ALARM(Alarm):

    def __init__(self, message):
        self.message = message
        pass


class UNDER_PRESSURE_ALARM(Alarm):

    def __init__(self, message):
        self.message = message
        pass


class HOMING_ALARM(Alarm):

    def __init__(self, message):
        self.message = message
        pass


class POSITION_ALARM(Alarm):

    def __init__(self, message):
        self.message = message
        pass


class SYSTEM_ALARM(Alarm):

    def __init__(self, message):
        self.message = message

# TODO: do we need more alarm types?
