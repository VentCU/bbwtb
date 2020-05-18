#
# Limit Switch Sensor Class
#

import RPi.GPIO as GPIO
import sys


# TODO add feature, new thread for emergency stop
# TODO Test
class LimitSwitch:

    def __init__(self, PIN):

        self.switch_pin = PIN

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_switch_status(self):

        return GPIO.input(self.switch_pin)



# Main loop. Demonstrate reading limit switch value.
def main():

    limit_switch = LimitSwitch(16) # GPIO 23

    while True:

        print( limit_switch.get_switch_status() )
        sleep(0.01)


# start main demo function
main()
