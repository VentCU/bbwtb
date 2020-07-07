#!/usr/bin/python

import sys, getopt
import time
import pigpio
from configs.gpio_map import *
from configs.motor_configs import *
from actuators.motor import Motor
from sensors.rotary_encoder import RotaryEncoder

def motor(test_method):

    if test_method == "move_to_encoder_pose_with_dur":

        target_time = 1
        target_dist = -100

        encoder = RotaryEncoder(pigpio.pi(), ENCODER_B_PLUS_PIN, ENCODER_A_PLUS_PIN)
        motor = Motor(encoder)

        def go_to_target():
            start = time.time()
            result = False
            while result is not True:
                result, val = motor.move_to_encoder_pose_with_dur(target_pose, target_dist, target_time)
            end = time.time()
            motor.stop()
        
            print("Target time: " + str(target_time) )
            print("Elapsed Time: " + str(end - start) )

        target_pose = motor.encoder_position() + target_dist
        go_to_target()
        target_pose = motor.encoder_position() - target_dist
        go_to_target()


def main_tester():

    test_class = ''
    test_method = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:m:", ["class=", "method="])
    except getopt.GetoptError:
        print('tester.py -c <test-class> -m <test-method>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h":
            print('tester.py -c <test-class> -m <test-method>')
            sys.exit()
        elif opt == "-c":
            test_class = arg
        elif opt == "-m":
            test_method = arg

    eval(test_class + '("' + test_method + '")')


if __name__ == "__main__":
    main_tester()

