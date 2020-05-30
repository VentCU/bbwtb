#
# ventilator controller class for
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: wx2214@columbia.edu
#          neil.nie@columbia.edu
#

from time import sleep
from datetime import datetime as time
from configs.ventilation_configs import *
from alarms.alarms import *


class State:
    def __init__(self):
        pass


class VentilatorController:

    def __init__(self, motor, pressure_sensor, upper_switch, lower_switch):

        # alarms
        self.current_alarms = []

        # states
        self.START_STATE = State()
        self.HOMING_STATE = State()
        self.HOMING_VERIF_STATE = State()
        self.INSP_STATE = State()
        self.INSP_PAUSE_STATE = State()
        self.EXP_STATE = State()
        self.EXP_PAUSE_STATE = State()
        self.PAUSE_STATE = State()
        self.OFF_STATE = State()
        self.DEBUG_STATE = State()

        self.current_state = self.OFF_STATE
        self._entering_state = False
        self._t_state_timer = 0                 # absolute time (s) at start of current state

        # cycle parameters
        self.cycle_count = 0
        # self._t_now = time.now()
        self._t_cycle_start = time.now()        # absolute time (s) at start of cycle
        self._t_insp_end = time.now()           # calculated time (s) at end of insp
        self._t_insp_pause_end = time.now()     # calculated time (s) at end of insp pause
        self._t_exp_end = time.now()            # calculated time (s) at end of exp
        self._t_exp_pause_end = time.now()      # calculated time (s) at end of exp pause
        self._t_period = time.now()             # calculated time (s) at end of cycle
        self._t_period_actual = time.now()      # absolute time (s) at end of cycle
        self._t_loop_start = time.now()         # absolute time (s) at start of control loop

        # ventilation parameters
        self.volume = 0                         # TODO: set default values
        self.bpm = 30                           # TODO: set default values
        self.ie = 0                             # TODO: set default values

        # localize actuators and sensors
        self.motor = motor
        self.pressure_sensor = pressure_sensor
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch

        self.lower_switch.callback = self.contact_switch_callback
        self.upper_switch.callback = self.limit_switch_callback

        # motion get_variables
        self.bag_clear_pos = 0

        # motor helper variables
        self._pose_at_contact = 0               # position of the encoder when arm contacts ambu bag
        self._homing_dir = 1
        self.motor_lower_target = 0             # the target pose of motor when the arm is coming down.
        self.motor_upper_target = 0             # the target pose of motor when the arm is going up.
        self.motor_current_target = 0

        # TODO: clean up class variables
        # =========================================
        self.contact_encoder_val = 0    # at the point of contact of the ambu bag, what's the encoder value.
        self.contact_tic_val = 0
        self.abs_limit_encoder_val = 0  # at the point of abs limit, what's the encoder value.
        # =========================================


    #############################
    ## Base Method Definitions ##
    #############################

    # set the state of the finite state machine
    def set_state(self, state):
        """
        Calling set_state in a unsafe way is not defined.
        """
        self._entering_state = True
        self.current_state = state
        self._t_state_timer = time.now()

    # calculate time parameters of ventilation
    def calculate_wave_form(self, tidal_volume, ie_ratio, bpm):
        # TODO: use tidal volume parameter
        self._t_period = 60.0 / bpm    # seconds per breath
        self._t_insp_pause_end = self._t_cycle_start + self._t_period / (1 + ie_ratio)     # TODO: understand this
        self._t_insp_end = self._t_cycle_start + self._t_insp_pause_end - INSP_HOLD_DUR    # TODO: understand this
        self._t_exp_end = min(self._t_insp_pause_end + MAX_EXP_DUR,                        # TODO: understand this
                              self._t_period - MIN_EXP_PAUSE)

        self._t_exp_pause_end = self._t_exp_end + MIN_EXP_PAUSE
        # TODO: convert self.volume to encoder position
        # self.motor_upper_target =
        # self.motor_lower_target =


    ###########################
    ## Main Ventilation Loop ##
    ###########################

    def start_ventilation(self):
        while True:
            self.ventilate()
        # TODO

    def stop_ventilation(self):
        # TODO
        pass

    def ventilate(self):

        self._t_loop_start = time.now()
        self.calculate_wave_form(tidal_volume=self.volume,
                                 ie_ratio=self.ie,
                                 bpm=self.bpm)

        # main finite state machine

        # ==
        if self.current_state is self.START_STATE:
            if self._entering_state:
                self._entering_state = False

        # ==
        elif self.current_state is self.HOMING_STATE:
            if self._entering_state:
                self._entering_state = False

            self.home()

        # ==
        elif self.current_state is self.HOMING_VERIF_STATE:
            if self._entering_state:
                self._entering_state = False

            self.set_state(self.INSP_STATE)

        # ==
        elif self.current_state is self.INSP_STATE:
            if self._entering_state:
                self._entering_state = False
                self._t_period_actual = time.now() - self._t_cycle_start
                self._t_cycle_start = time.now()
                self.cycle_count += 1

            # TODO: change/update this method
            result, _ = self.motor.move_to_encoder_pose(pose=self.motor_current_target,
                                                        vel_const=self.bpm_to_velocity_constant())

            if self.motor.encoder_position() == self.motor_upper_target and result is True:
                self.log_motor_position()
                self.motor_current_target = self.motor_lower_target
                self.set_state(self.INSP_PAUSE_STATE)

            if time.now() > self._t_insp_end:
                raise SYSTEM_ALARM("Inspiration exceeds time limit")

        # ==
        elif self.current_state is self.INSP_PAUSE_STATE:
            if self._entering_state:
                self._entering_state = False

            self.motor.stop()

            if time.now() > self._t_insp_pause_end:
                self.set_state(self.EXP_STATE)

        # ==
        elif self.current_state is self.EXP_STATE:
            if self._entering_state:
                self._entering_state = False

            # TODO: change/update this method
            result, _ = self.motor.move_to_encoder_pose(pose=self.motor_current_target,
                                                        vel_const=self.bpm_to_velocity_constant())

            if self.motor.encoder_position() == self.motor_lower_target and result is True:
                self.log_motor_position()
                self.motor_current_target = self.motor_upper_target
                self.set_state(self.EXP_PAUSE_STATE)

            if time.now() > self._t_exp_end:
                raise SYSTEM_ALARM("Expiration exceeds time limit")

        # ==
        elif self.current_state is self.EXP_PAUSE_STATE:
            if self._entering_state:
                self._entering_state = False

            self.motor.stop()

            if time.now() > self._t_exp_pause_end:
                self.set_state(self.HOMING_VERIF_STATE)

        # ==
        elif self.current_state is self.PAUSE_STATE: # TODO: define off behavior
            if self._entering_state:
                self._entering_state = False

        # ==
        elif self.current_state is self.OFF_STATE:  # TODO: define off behavior
            if self._entering_state:
                self._entering_state = False

        # ==
        if self.current_state is self.DEBUG_STATE:  # TODO: define debug behavior
            self.motor.stop()

        # TODO: add delay to loop if there is extra time

    def home(self):
        """
        Homing method for the ventilator
        """
        if self.current_state is not self.HOMING_STATE:
            raise HOMING_ALARM("Attempted homing outside homing state")

        # making contact with upper switch
        if self.upper_switch.contacted() and not self.lower_switch.contacted():

            # moving upward
            if self._homing_dir == 1:
                self.motor.stop()
                self.motor.stop_set_pose(0)
                self.motor.encoder.reset_position()
                self._homing_dir = -1
                self.log_motor_position("Homing upper bound reached")
                sleep(0.25)

            # moving downward, upper bound set
            else:
                self.motor.set_velocity(self._homing_dir * HOMING_VELOCITY)

        # making contact with lower switch
        elif not self.upper_switch.contacted() and self.lower_switch.contacted():

            self.motor.stop()
            self._pose_at_contact = self.motor.encoder_position()
            self.contact_tic_val = self.motor.motor_position()

            # todo: need to change this
            self.motor_lower_target = int(self._pose_at_contact - ENCODER_ONE_ROTATION * 4 / 5)
            self.motor_upper_target = int(self._pose_at_contact + ENCODER_ONE_ROTATION * 1 / 100)
            self.motor_current_target = self.motor_upper_target

            # change state
            self.set_state(self.HOMING_VERIF_STATE)

            self.log_motor_position("Homing lower bound reached")
            print("=== Homing Finished ===")
            sleep(0.25)

        # no contact with any switch
        elif not self.upper_switch.contacted() and not self.lower_switch.contacted():
            self.motor.set_velocity(self._homing_dir * HOMING_VELOCITY)

        # contact with both switches -- error
        elif self.upper_switch.contacted() and self.lower_switch.contacted():
            raise HOMING_ALARM("Both contact switches are pressed")

    def contact_switch_callback(self, status):
        """
        This method is called when the contact
        switch on the arm comes into contact with
        the ambu bag
        @param status: the status of the switch
        """
        if status is 1 and self._pose_at_contact is None:
            self._pose_at_contact = self.motor.encoder_position()
            self.log_motor_position(message="Contacted ambu bag")

    def limit_switch_callback(self, status):
        """
        This method is called when the limit switch
        on the frame comes into contact with the arm
        @param status: the status of the switch
        """
        if self.current_state is not self.HOMING_STATE:
            self.stop_ventilation()
            raise SYSTEM_ALARM("Limit switch tripped")

    def bpm_to_velocity_constant(self):
        """
        convert bpm value to a velocity constant.
        This velocity constant value is passed
        to the motor
        @return: velocity constant.
        """
        return self.bpm * VELOCITY_FACTOR

    def log_motor_position(self, message=""):
        """
        Print the motor position with a custom
        message if needed.
        @param message: a custom message to
        be printed.
        """
        print("{} encoder: {}, motor controller: {}".format(message,
                                                            self.motor.encoder_position(),
                                                            self.motor.motor_position()))

    def update_bpm(self, value):
        self.bpm = value

    def update_ie(self, value):
        self.ie = value

    def update_tidal_volume(self, value):
        self.volume = value

    # TODO: write alarm functions -> sound buzzer, etc.
