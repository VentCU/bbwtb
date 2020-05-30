class Alarm(Exception):

    def __init__(self, alarm_type):
        self.type = alarm_type

class OVER_PRESSURE_ALARM(Alarm):
    pass


# TODO: class for each alarm type
