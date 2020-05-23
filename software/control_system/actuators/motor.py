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
        self.tic_device = TicDevice()
        self.tic_device.open(vendor=0x1ffb, product_id=0x00CB)
        self.pid = PID(P=PID_P_GAIN, I=PID_I_GAIN, D=PID_D_GAIN)
        self.encoder = rotary_encoder

    def set_velocity(self, velocity):
        """

        @param velocity: the target velocity of the motor.
        """
        self.tic_device.set_target_velocity(velocity)

    def move_to_encoder_pose(self, pose, vel_const=1):
        """
        use a pid controller to reach the target
        position specified in the parameter of the
        method.

        @param vel_const: the constant that get multiplied to the pid output
        @param pose: the target position of the motor
        @return:     true of the motor has reached its goal
        """

        self.pid.setpoint = pose
        encoder_value = self.encoder.value()
        self.pid.update(encoder_value)
        value = self.pid.output * vel_const
        self.tic_device.set_target_velocity(int(value))
        
        if self.pid.output == 0:
            return True, int(value)
        else:
            return False, int(value)

    def stop(self):
        self.tic_device.halt_and_hold()

    def stop_set_pose(self, pose):
        self.tic_device.halt_and_set_position(pose)

    def motor_position(self):
        self.tic_device.get_variables()
        return self.tic_device.variables['current_position']

    def encoder_position(self):
        return self.encoder.value()

    def destructor(self):
        self.tic_device.halt_and_hold()
        self.tic_device.deenergize()
        self.encoder.cancel()
        print("The motor has been stopped."
              "The motor has been deenergized"
              ""
              "Warning: program should exit")
