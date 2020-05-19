#
# motor class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from actuators.tic_usb import *
from actuators.pid_controller import PID
from configs.motor_configs import *


class Motor:

    def __init__(self, rotary_encoder):
        # create a motor controller object
        self.motor = TicDevice()
        self.motor.open(vendor=0x1ffb, product_id=0x00CB)
        self.pid = PID(P=PID_P_GAIN, I=PID_I_GAIN, D=PID_D_GAIN)
        self.encoder = rotary_encoder

    def set_velocity(self, velocity):
        """

        @param velocity: the target velocity of the motor.
        """
        self.motor.set_target_velocity(velocity)

    def move_to_encoder_pose(self, pose):
        """
        use a pid controller to reach the target
        position specified in the parameter of the
        method.

        @param pose: the target position of the motor
        @return:     true of the motor has reached its goal
        """

        self.pid.setpoint = pose
        encoder_value = self.encoder.value()
        self.pid.update(encoder_value)
        value = self.pid.output * 15000.0 if self.pid.output < 1000000 else 100000
        self.motor.set_target_velocity(int(value))

        if self.pid.output == 0:
            return True
        else:
            return False

    def stop(self):
        self.motor.halt_and_hold()

    def motor_position(self):
        self.motor.get_variables()
        return self.motor.variables['current_position']

    def encoder_position(self):
        return self.encoder.value()

    def destructor(self):
        self.motor.halt_and_hold()
        self.motor.deenergize()
        self.encoder.cancel()
        print("The motor has been stopped."
              "The motor has been deenergized"
              ""
              "Warning: program should exit")
