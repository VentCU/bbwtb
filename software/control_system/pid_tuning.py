#!/usr/bin/python
#
# TicDevice and PID test
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

import matplotlib.pyplot as plt
from time import sleep
from actuators.motor import Motor
import pigpio
from sensors.rotary_encoder import RotaryEncoder
import numpy as np


def savitzky_golay(y, window_size, order, deriv=0, rate=1):

    import numpy as np
    from math import factorial
    
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))

    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

motor = Motor(RotaryEncoder(pigpio.pi(), 18, 16))

encoder_u_limit = 400
encoder_l_limit = 0

vel_arr = []
en_pose_arr = []
tic_pose_arr = []
x = []
zeros = []
setpoints_en = []
setpoints_tic = []
i = 0

# initialize the goal of the motor
goal = encoder_u_limit

if __name__ == "__main__":

    import time
    start = time.time()
    printed = False

    while True:

        result, vel = motor.move_to_encoder_pose(goal)

        if i is not 0:

            if result and not printed:
                printed = True
                print(time.time() - start)
                print("====")
            vel_arr.append(vel)
            en_pose_arr.append(motor.encoder_position())
            tic_pose_arr.append(motor.motor_position())
            x.append(i)
            zeros.append(0)
            setpoints_en.append(400)
            setpoints_tic.append(12800)

        i = i + 1
 
        if i > 800:
            print("terminated")
            break

accel = np.append(np.diff(vel_arr) / np.diff(x), np.array([0]))

fig, axs = plt.subplots(4)
fig.suptitle('plots')
axs[0].plot(x, vel_arr)
axs[0].plot(x, zeros)
axs[1].plot(x, en_pose_arr)
axs[1].plot(x, setpoints_en)
axs[2].plot(x, tic_pose_arr)
axs[2].plot(x, setpoints_tic)
accel_s = savitzky_golay(accel, 50, 5) # window size 51, polynomial order 3
axs[3].plot(x, accel)
axs[3].plot(x, accel_s)
plt.show()
motor.tic_device.set_target_position(0)
motor.destructor()

exit()


