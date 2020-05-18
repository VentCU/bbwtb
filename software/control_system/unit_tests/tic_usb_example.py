#
# Tic Motor controller usb example code
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#


from tic_usb import TicUSB

tic = TicUSB()

position = tic.get_current_position()
print("Current position is {}.".format(position))

new_target = -200 if position > 0 else 200
print("Setting target position to {}.".format(new_target))
tic.set_target_position(new_target)
