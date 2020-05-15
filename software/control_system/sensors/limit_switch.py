#
# Limit Switch Sensor Class
#

import RPi.GPIO as GPIO
import sys


# TODO Test
class LimitSwitch:

    def __init__(self, PIN):

        self.switch_pin = PIN

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_switch_status(self):

        return GPIO.input(self.switch_pin)
