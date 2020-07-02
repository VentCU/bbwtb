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
    buzzer1 = Buzzer(25)
    buzzer2 = Buzzer(8)
    
    beep_ctr = 0

    while(beep_ctr < 5):
        beep_ctr +=1
        
        dur_ctr = 0
        while(dur_ctr < 100000):
            dur_ctr += 1
            buzzer1.enable_buzzer()
            buzzer2.enable_buzzer()
        
        buzzer1.disable_buzzer()
        buzzer2.disable_buzzer()

        sleep(1)

if __name__ == "__main__":
    buzzer_test()
