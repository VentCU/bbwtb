



#!/usr/bin/env pythoncvncserver

import RPi.GPIO as GPIO
import time

RoAPin = 16    # pin11
RoBPin = 18    # pin12
RoZPin = 15    # pin13

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def setup():
    
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoZPin, GPIO.IN)
    
    # GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    # rotaryClear()

def rotaryDeal():
    
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    Last_RoB_Status = GPIO.input(RoBPin)
    
    # ****** Debugging
    print("Value: {} {} {}".format(GPIO.input(RoAPin), GPIO.input(RoBPin), GPIO.input(RoZPin)))
    # ******
    
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            print('globalCounter = %d' % globalCounter)
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
            print('globalCounter = %d' % globalCounter)


def loop():
    global globalCounter
    while True:
        rotaryDeal()
#       print 'globalCounter = %d' % globalCounter

def destroy():
    GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()