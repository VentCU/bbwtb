
import RPi.GPIO as GPIO
from time import sleep

class PowerSwitch():

    def __init__(self, PIN):
        self.switch_pin = PIN
        self.callback = None

        # Broadcom GPIO #s, NOT straight pin numbers on board
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN,
                              GPIO.RISING,
                              callback=self.switch_callback,
                              bouncetime=100)

    def get_status(self):
        return GPIO.input(self.switch_pin)

    def switch_callback(self, state):
        if self.callback is not None:
            sleep(0.01)
            self.callback(self.get_status())
