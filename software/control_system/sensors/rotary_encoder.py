#
# rotary encoder class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#


import RPi.GPIO as GPIO
import threading


class RotaryEncoder:

    def __init__(self, port_a, port_b, callback):

        # GPIO Ports
        self.enc_a = port_a  # Encoder input A: input GPIO 4
        self.enc_b = port_b  # Encoder input B: input GPIO 14

        self.rotary_counter = 0     # Start counting from 0
        self.current_a = 0          # Assume that rotary switch is not
        self.current_b = 0          # moving while we init software

        self.thread_lock = threading.Lock()  # create lock for rotary switch

        if callback is None:
            raise Exception("Must provide a encoder value callback")
        self.callback = callback

        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)  # Use BCM mode

        # define the Encoder switch inputs
        GPIO.setup(self.enc_a, GPIO.IN)
        GPIO.setup(self.enc_b, GPIO.IN)

        # setup callback thread for the A and B encoder
        # use interrupts for all inputs
        GPIO.add_event_detect(self.enc_a, GPIO.RISING, callback=self.rotary_interrupt)
        GPIO.add_event_detect(self.enc_b, GPIO.RISING, callback=self.rotary_interrupt)
        
    def rotary_interrupt(self, A_or_B):

        # read both of the switches
        switch_a = GPIO.input(self.enc_a)
        switch_b = GPIO.input(self.enc_b)

        # now check if state of A or B has changed
        # if not that means that bouncing caused it
        if self.current_a == switch_a and self.current_b == switch_b:  # Same interrupt as before (Bouncing)?
            return  # ignore interrupt!

        self.current_a = switch_a  # remember new state
        self.current_b = switch_b  # for next bouncing check

        if switch_a and switch_b:               # Both one active? Yes -> end of sequence
            self.thread_lock.acquire()          # get lock
            if A_or_B == self.enc_b:            # Turning direction depends on
                self.rotary_counter += 1
            else:
                self.rotary_counter -= 1
            
            self.callback(self.rotary_counter)

            self.thread_lock.release()

    def get_position(self):
        return self.rotary_counter


def encoder_callback(value):
    print(value)


# Main loop. Demonstrate reading, direction and speed of turning left/rignt
if __name__ == "__main__":

    # TODO test encoder
    # TODO add callback method
    RotatoryEncoder(22, 24, callback=encoder_callback)

