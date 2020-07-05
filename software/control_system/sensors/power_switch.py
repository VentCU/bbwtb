
import RPi.GPIO as GPIO


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

    def contacted(self):
        return 1 if GPIO.input(self.switch_pin) else 0

    def switch_callback(self):
        if self.callback is not None:
            self.callback(self.contacted())
