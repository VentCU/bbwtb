#
# Limit Switch Sensor Class
#

import RPi.GPIO as GPIO
import sys
from time import sleep


class LimitSwitch:

    def __init__(self, PIN):
        self.switch_pin = PIN
        self.callback = None

        #Broadcom GPIO #s, NOT straight pin numbers on board
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN, GPIO.RISING,
                              callback=self.switch_callback,
                              bouncetime=100)

    def get_status(self):
        return GPIO.input(self.switch_pin)

    def contacted(self):
        return 1 if GPIO.input(self.switch_pin) else 0

    def switch_callback(self, state):
        if self.callback is not None:
            self.callback(self.contacted())

# Main loop. Demonstrate reading limit switch value.
# Switch configured for NC (normally closed)
# Returns 1 when pressed, 0 when open
def test():
    limit_switch = LimitSwitch(17)  # GPIO 23

    while True:
        print(limit_switch.get_status())
        sleep(0.01)


# start main demo function
if __name__ == "__main__":
    test()
