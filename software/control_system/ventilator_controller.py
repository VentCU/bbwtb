#
# ventilator controller class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from time import sleep

# define some constants
ENCODER_ONE_ROTATION = 400
TIC_ONE_ROTATION = 12800


class VentilatorController:

    def __init__(self, motor, pressure_sensor, upper_switch, lower_switch):

        self.motor = motor
        self.pressure_sensor = pressure_sensor
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch
        self.lower_switch.callback = self.contact_switch_callback

        # init class variables
        self.pose_at_contact = 0        # position of the motor enc when arm contacts ambu bag
        self.contact_encoder_val = 0    # at the point of contact of the ambu bag, what's the encoder value.
        self.contact_tic_val = 0
        self.abs_limit_encoder_val = 0  # at the point of abs limit, what's the encoder value.
        self.homing_finished = False
        self.__homing_dir = 1
        self.motor_lower_target = 0     # the target pose of motor when the arm is coming down.
        self.motor_upper_target = 0
        self.motor_current_target = 0

    def start(self):

        while True:
            if self.homing_finished is False:
                self.initial_homing_procedure()
            else:

                if self.motor_lower_target is 0 and self.motor_upper_target is 0:
                    raise Exception("homing finished but the motor target pose is still zero. FATAL BUG")

                result, vel = self.motor.move_to_encoder_pose(self.motor_current_target)

                # switching directions
                if self.motor.encoder_position() == self.motor_upper_target and result is True:
                    print("{}, {}, {}".format(vel, self.motor.encoder_position(), self.motor.motor_position()))
                    sleep(1.5)
                    self.motor_current_target = self.motor_lower_target

                elif self.motor.encoder_position() == self.motor_lower_target and result is True:
                    print("{}, {}, {}".format(vel, self.motor.encoder_position(), self.motor.motor_position()))
                    sleep(1.5)
                    self.motor_current_target = self.motor_upper_target

    def initial_homing_procedure(self):

        if self.homing_finished is True:
            raise Exception("Homing is already finished, why are you homing again?")  # Todo: error handling

        # making contact with upper switch
        if self.upper_switch.contacted() and not self.lower_switch.contacted():

            # moving upward
            if self.__homing_dir == 1:
                self.motor.stop()
                # self.abs_limit_encoder_val = self.motor.encoder_position()
                self.motor.stop_set_pose(0)
                self.motor.encoder.reset_position()
                self.__homing_dir = -1
                print("Upper bound for motor reached. \n "
                      "Motor current position: {}".format(self.motor.motor_position()))
                sleep(0.5)

            # moving downward, upper bound set
            else:
                self.motor.set_velocity(self.__homing_dir * 2000000)

        # making contact with lower switch
        elif not self.upper_switch.contacted() and self.lower_switch.contacted():

            self.motor.stop()
            self.contact_encoder_val = self.motor.encoder_position()
            self.contact_tic_val = self.motor.motor_position()
            self.homing_finished = True
            self.motor_lower_target = int(self.contact_encoder_val + ENCODER_ONE_ROTATION * 1 / 2) # todo: tidal volume param
            self.motor_upper_target = int(self.contact_encoder_val - ENCODER_ONE_ROTATION * 1)
            print("Lower bound for motor reached. \n "
                  "Motor current position: {}".format(self.motor.motor_position()))
            sleep(0.5)

        # no contact with any switch
        elif not self.upper_switch.contacted() and not self.lower_switch.contacted():
            self.motor.set_velocity(self.__homing_dir * 2000000)

        # contact with both switches -- error
        elif self.upper_switch.contacted() and self.lower_switch.contacted():
            raise Exception("Both contact switches are pressed. Fatal error.")  # Todo: error handling.

    def contact_switch_callback(self, status):
        if status is 1:
            self.pose_at_contact = self.motor.encoder_position()
            print("At contact, the error is: {} {}".format(self.pose_at_contact - self.contact_encoder_val,
                                                           self.motor.motor_position() - self.contact_tic_val))
