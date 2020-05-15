import RPi.GPIO as GPIO
import threading
from time import sleep


class RotatoryEncoder:

    def __init__(self):

        # TODO
        pass

    def get_position(self):

        # TODO
        pass

# GPIO Ports
enc_a = 4               # Encoder input A: input GPIO 4
enc_b = 14              # Encoder input B: input GPIO 14

rotary_counter = 0      # Start counting from 0
current_A = 1           # Assume that rotary switch is not
current_B = 1           # moving while we init software

thread_lock = threading.Lock()  # create lock for rotary switch


# initialize interrupt handlers
def init():

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)  # Use BCM mode

    # define the Encoder switch inputs
    GPIO.setup(enc_a, GPIO.IN)
    GPIO.setup(enc_b, GPIO.IN)

    # setup callback thread for the A and B encoder
    # use interrupts for all inputs
    GPIO.add_event_detect(enc_a, GPIO.RISING, callback=rotary_interrupt)  # NO bouncetime
    GPIO.add_event_detect(enc_b, GPIO.RISING, callback=rotary_interrupt)  # NO bouncetime


# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):

    global rotary_counter, current_a, current_b, thread_lock

    # read both of the switches
    switch_a = GPIO.input(enc_a)
    switch_b = GPIO.input(enc_b)

    # now check if state of A or B has changed
    # if not that means that bouncing caused it
    if current_a == switch_a and current_b == switch_b:  # Same interrupt as before (Bouncing)?
        return  # ignore interrupt!

    current_a = switch_a                # remember new state
    current_b = switch_b                # for next bouncing check

    if (switch_a and switch_b):         # Both one active? Yes -> end of sequence
        thread_lock.acquire()           # get lock
        if A_or_B == enc_b:             # Turning direction depends on
            rotary_counter += 1         # which input gave last interrupt
        else:                           # so depending on direction either
            rotary_counter -= 1         # increase or decrease counter
        thread_lock.release()           # and release lock


# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():

    global rotary_counter, thread_lock

    new_counter = 0                         # for faster reading with locks

    init()                                  # Init interrupts, GPIO, ...

    while True:                             # start test

        sleep(0.1)                          # sleep 100 msec

        # because of threading make sure no thread
        # changes value until we get them
        # and reset them

        thread_lock.acquire()               # get lock for rotary switch
        new_counter = rotary_counter        # get counter value
        rotary_counter = 0                  # RESET IT TO 0
        thread_lock.release()               # and release lock

        if new_counter != 0:  # Counter has CHANGED
            print(new_counter)


# start main demo function
main()
