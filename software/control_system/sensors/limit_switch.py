#
# Limit Switch Sensor Class
#

import RPi.GPIO as GPIO
import sys
from time import sleep


class LimitSwitch:

    def __init__(self, PIN):
        self.switch_pin = PIN

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_status(self):
        return GPIO.input(self.switch_pin)


# Main loop. Demonstrate reading limit switch value.
# Switch configured for NO (normally opened)
# Returns 0 when pressed, 1 when open
def test():
    limit_switch = LimitSwitch(23)  # GPIO 23

    while True:
        print(limit_switch.get_status())
        sleep(0.01)


# start main demo function
if __name__ == "__main__":
    test()
    # print(test.get_switch_status())
