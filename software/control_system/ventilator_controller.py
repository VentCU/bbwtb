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
HOMING_VELOCITY = 4000000
VELOCITY_FACTOR = 1/12
# todo: set hold in time const.

"""

The Machine FSM

-- start
-- homing

-- homing verification
-- inspiratory phase
-- inspiratory pause
-- expiratory phase
-- expiratory pause

-- pause
-- halt (off)
-- debug

"""

class State:
    def __init__():
        pass


class VentilatorController:

    def __init__(self, motor, pressure_sensor, upper_switch, lower_switch):

        self.START_STATE = State()
        self.OFF_STATE = State()
        # todo: finish off the states
        # .. 

        self.current_state = self.OFF_STATE

        self._entering_state = False
        self.cycle_count = 0
        self.t_cycle_start = 0
        self.t_inspiratory_end = 0
        

        self.motor = motor
        self.pressure_sensor = pressure_sensor
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch
        self.lower_switch.callback = self.contact_switch_callback

        # =========================================
        # init class variables
        self.pose_at_contact = 0        # position of the motor enc when arm contacts ambu bag
        self.contact_encoder_val = 0    # at the point of contact of the ambu bag, what's the encoder value.
        self.contact_tic_val = 0
        self.abs_limit_encoder_val = 0  # at the point of abs limit, what's the encoder value.
        self.homing_finished = False
        self._homing_dir = 1
        self._initial_contact = True
        self.motor_lower_target = 0     # the target pose of motor when the arm is coming down.
        self.motor_upper_target = 0
        self.motor_current_target = 0
        self.bpm = 30 # todo: set default value

    def start(self):

        while True:
            if self.homing_finished is False:
                self.initial_homing_procedure()
            else:
                
                if self.motor_lower_target is 0 and self.motor_upper_target is 0:
                    raise Exception("homing finished but the motor target pose is still zero. FATAL BUG")

                result, vel = self.motor.move_to_encoder_pose(pose=self.motor_current_target,
                                                              vel_const=self.bpm_to_velocity_constant())

                # switching directions
                if self.motor.encoder_position() == self.motor_upper_target and result is True:
                    print("{}, {}, {}".format(vel, self.motor.encoder_position(), self.motor.motor_position()))
                    sleep(0.20)  # todo: parameterize this!
                    self.motor_current_target = self.motor_lower_target
                    self._initial_contact = True

                elif self.motor.encoder_position() == self.motor_lower_target and result is True:
                    print("{}, {}, {}".format(vel, self.motor.encoder_position(), self.motor.motor_position()))
                    sleep(0.20)
                    self.motor_current_target = self.motor_upper_target

    def initial_homing_procedure(self):

        if self.homing_finished is True:
            raise Exception("Homing is already finished, why are you homing again?")  # Todo: error handling

        # making contact with upper switch
        if self.upper_switch.contacted() and not self.lower_switch.contacted():

            # moving upward
            if self._homing_dir == 1:
                self.motor.stop()
                # self.abs_limit_encoder_val = self.motor.encoder_position()
                self.motor.stop_set_pose(0)
                self.motor.encoder.reset_position()
                self._homing_dir = -1
                print("Upper bound for motor reached. \n"
                      "Motor current position: {}".format(self.motor.motor_position()))
                sleep(0.5)

            # moving downward, upper bound set
            else:
                self.motor.set_velocity(self._homing_dir * HOMING_VELOCITY)

        # making contact with lower switch
        elif not self.upper_switch.contacted() and self.lower_switch.contacted():

            self.motor.stop()
            self.contact_encoder_val = self.motor.encoder_position()
            self.contact_tic_val = self.motor.motor_position()
            self.homing_finished = True
            
            self.motor_lower_target = int(self.contact_encoder_val - ENCODER_ONE_ROTATION * 4 / 5) # todo: tidal volume param
            self.motor_upper_target = int(self.contact_encoder_val + ENCODER_ONE_ROTATION * 1 / 10)
            self.motor_current_target = self.motor_upper_target
            
            print("Lower bound for motor reached.\n"
                  "Motor current position: {} {}".format(self.motor.encoder_position(),
                                                         self.motor.motor_position()))
            print("=== Homing Finished ===")
            sleep(0.5)

        # no contact with any switch
        elif not self.upper_switch.contacted() and not self.lower_switch.contacted():
            self.motor.set_velocity(self._homing_dir * HOMING_VELOCITY)

        # contact with both switches -- error
        elif self.upper_switch.contacted() and self.lower_switch.contacted():
            raise Exception("Both contact switches are pressed. Fatal error.")  # Todo: error handling.

    def stop(self):
        self.motor.destructor()

    def contact_switch_callback(self, status):
        if status is 1 and self._initial_contact:
            self._initial_contact = False
            self.pose_at_contact = self.motor.encoder_position()
            print("At contact, the error is: {} {}".format(self.pose_at_contact - self.contact_encoder_val,
                                                           self.motor.motor_position() - self.contact_tic_val))

    def bpm_to_velocity_constant(self):
        """
        convert bpm value to a velocity constant.
        This velocity constant value is passed
        to the motor
        @return: velocity constant.
        """
        return self.bpm * VELOCITY_FACTOR

    def update_bpm(self, value):
        self.bpm = value

    def set_state(self, state):
        """
        Calling set_state in a unsafe way is not defined. 
        """
        self._entering_state = True
        self.current_state = state

    # def calculation(self, bpm, tidal_v, ie_ratio):
    #     cycle_time = 1 / bpm
    #     i_time = cycle_time * ie_ratio
    #     e_time = cycle_time - i_time

    #     down_dist = 0
    #     up_dist = 0

