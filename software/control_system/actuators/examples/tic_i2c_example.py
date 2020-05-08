#
# Tic Motor controller I2C example code
# 
# (c) VentCU, 2020, All Rights Reserved.

from smbus2 import SMBus
from ..tic_i2c import TicI2C

# 
# NOTE: You might nee to change the 'SMBus(3)' line below to specify the
#   correct I2C device.
# NOTE: You might need to change the 'address = 11' line below to match
#   the device number of your Tic.

# Open a handle to "/dev/i2c-3", representing the I2C bus.
bus = SMBus(3)
 
# Select the I2C address of the Tic (the device number).
address = 14
 
tic = TicI2C(bus, address)
 
position = tic.get_current_position()
print("Current position is {}.".format(position))

new_target = -200 if position > 0 else 200
print("Setting target position to {}.".format(new_target));
tic.exit_safe_start()
tic.set_target_position(new_target)
