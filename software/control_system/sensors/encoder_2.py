#!/usr/bin/python
#-------------------------------------------------------------------------------
# FileName:     Rotary_Encoder-1a.py
# Purpose:      This program decodes a rotary encoder switch.
#

#
# Note:         All dates are in European format DD-MM-YY[YY]
#
# Author:       Paul Versteeg
#
# Created:      23-Nov-2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from time import sleep


# Global constants & variables
# Constants
__author__ = 'Paul Versteeg'

counter = 10  # starting point for the running directional counter

# GPIO Ports
Enc_A = 24  # Encoder input A: input GPIO 23 (active high)
Enc_B = 22  # Encoder input B: input GPIO 24 (active high)


def init():
    '''
    Initializes a number of settings and prepares the environment
    before we start the main program.
    '''
    print("Rotary Encoder Test Program")

    GPIO.setwarnings(True)

    # Use the Raspberry Pi BCM pins
    GPIO.setmode(GPIO.BCM)

    # define the Encoder switch inputs
    GPIO.setup(Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
    GPIO.setup(Enc_B, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=1) # bouncetime in mSec
    #
    return


def rotation_decode(Enc_A):
    '''
    This function decodes the direction of a rotary encoder and in- or
    decrements a counter.

    The code works from the "early detection" principle that when turning the
    encoder clockwise, the A-switch gets activated before the B-switch.
    When the encoder is rotated anti-clockwise, the B-switch gets activated
    before the A-switch. The timing is depending on the mechanical design of
    the switch, and the rotational speed of the knob.

    This function gets activated when the A-switch goes high. The code then
    looks at the level of the B-switch. If the B switch is (still) low, then
    the direction must be clockwise. If the B input is (still) high, the
    direction must be anti-clockwise.

    All other conditions (both high, both low or A=0 and B=1) are filtered out.

    To complete the click-cycle, after the direction has been determined, the
    code waits for the full cycle (from indent to indent) to finish.

    '''

    global counter

    sleep(0.002) # extra 2 mSec de-bounce time

    # read both of the switches
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        counter += 1
        print("direction -> ", counter)
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        counter -= 1
        print("direction <- ", counter)
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return

    else: # discard all other combinations
        return



def main():
    '''
    The main routine.

    '''

    try:

        init()
        while True :
            #
            # wait for an encoder click
            sleep(1)

    except KeyboardInterrupt: # Ctrl-C to terminate the program
        GPIO.cleanup()


if __name__ == '__main__':
    main()
