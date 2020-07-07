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

    def move_to_encoder_pose_with_dur(self, pose, dur):
        """
        use a pid controller to reach the target position specified in the
        parameter of the method over the duration specified in the parameter
        of the method.

        @param pose: the target position of the motor
        @param pose: the target duration the move should take (in seconds)
        @return:     true of the motor has reached its goal
        """

        if dur <= 0: return False   # cannot move in negative or zero time

        distance = abs(pose - self.encoder_position())
        scale_factor = PID_TIME_SCALE_FACTOR * distance / dur

        self.move_to_encoder_pose(pose, vel_const=scale_factor)

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
        print("The motor has been stopped.\n"
              "The motor has been deenergized\n"
              "\n"
              "Warning: program should exit\n")


def motor_test():

    import time
    import pigpio
    from ..configs.gpio_map import *

    encoder = RotaryEncoder(pigpio.pi(), ENCODER_B_PLUS_PIN, ENCODER_A_PLUS_PIN)
    motor = Motor(encoder)

    start = time.time()
    motor.move_to_encoder_pose_with_dur(motor.encoder_position()+100, 10)
    end = time.time()

    print(end - start)

if __name__ == "__main__":
    motor_test()
