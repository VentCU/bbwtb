#
# ventilator controller class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from time import sleep


class VentilatorController:

    def __init__(self, motor, pressure_sensor, upper_switch, lower_switch):

        self.motor = motor
        self.pressure_sensor = pressure_sensor
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch

        # init class variables
        self.contact_encoder_val = 0    # at the point of contact of the ambu bag, what's the encoder value.
        self.abs_limit_encoder_val = 0  # at the point of abs limit, what's the encoder value.
        self.homing_finished = False
        self.__homing_dir = 1

    def start(self):

        while True:
            if self.homing_finished is False:
                self.initial_homing_procedure()
            else:
                print("Homing completed")
                break

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
            self.homing_finished = True
            print("Lower bound for motor reached. \n "
                  "Motor current position: {}".format(self.motor.motor_position()))
            sleep(0.5)

        # no contact with any switch
        elif not self.upper_switch.contacted() and not self.lower_switch.contacted():
            self.motor.set_velocity(self.__homing_dir * 2000000)

        # contact with both switches -- error
        elif self.upper_switch.contacted() and self.lower_switch.contacted():
            raise Exception("Both contact switches are pressed. Fatal error.")  # Todo: error handling.
