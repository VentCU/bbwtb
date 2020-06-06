#
# buzzer class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#
import RPi.GPIO as GPIO
import sys
from time import sleep

class Buzzer:
    
    def __init__(self, PIN):
        self.buzzer_pin = PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT, initial=0)

    def enable_buzzer(self):
        GPIO.output(self.buzzer_pin, 1)

    def disable_buzzer(self):
        GPIO.output(self.buzzer_pin, 0)

    
    # TODO: this.

def buzzer_test():
    buzzer = Buzzer(25)
    ctr = 0
    while(ctr < 100):
        sleep(0.1)
        ctr += 1
        buzzer.enable_buzzer()
    buzzer.disable_buzzer()

if __name__ == "__main__":
    buzzer_test()
