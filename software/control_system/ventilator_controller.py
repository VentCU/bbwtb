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
import datetime
import logging
from configs.ventilation_configs import *
from alarms.alarms import *
from threading import Lock
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import sys
sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/actuators')
from buzzer import Buzzer
sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/sensors')
from pressure_sensor import PressureSensor


def add_secs(tm, secs):
    full_date = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, tm.microsecond)
    full_date = full_date + datetime.timedelta(seconds=secs)
    return full_date

def subtract_secs(tm, secs):
    full_date = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, tm.microsecond)
    full_date = full_date - datetime.timedelta(seconds=secs)
    return full_date

class State:
    def __init__(self, name):
        self.name = name

class StateChangeSender(QtCore.QObject):
    state_change_signal = pyqtSignal()

class ShutdownSender(QtCore.QObject):
    shutdown_signal = pyqtSignal()

class AlarmSender(QtCore.QObject):
    alarm_signal = pyqtSignal(Alarm)
    
class UpdateMeasuredParametersSender(QtCore.QObject):
    update_measured_parameters_signal = pyqtSignal() 
    
class VentilatorController:

    measured_parameters_sender = UpdateMeasuredParametersSender() 

    state_change_sender = StateChangeSender()
    shutdown_sender = ShutdownSender()
    alarm_sender = AlarmSender() 

    def __init__(self, motor, pressure_sensor,
                         upper_switch, lower_switch, power_switch ):
        self.buzzer_1 = Buzzer(25)
        self.buzzer_2 = Buzzer(8)

        self.pressure_sensor = PressureSensor()

        #logger
        self.logger = logging.getLogger('ventilator_controller')

        # alarms
        self.current_alarms = []

        # states
        self.START_STATE = State("START_STATE")
        self.HOMING_STATE = State("HOMING_STATE")
        self.HOMING_VERIF_STATE = State("HOMING_VERIF_STATE")
        self.INSP_STATE = State("INSP_STATE")
        self.INSP_PAUSE_STATE = State("INSP_PAUSE")
        self.EXP_STATE = State("EXP_STATE")
        self.EXP_PAUSE_STATE = State("EXP_PAUSE_STATE")
        self.PAUSE_STATE = State("PAUSE_STATE")
        self.OFF_STATE = State("OFF_STATE")
        self.DEBUG_STATE = State("DEBUG_STATE")

        self.current_state = self.OFF_STATE
        self._entering_state = False
        self._state_lock = Lock()
        self._t_state_timer = 0                 # absolute time (s) at start of current state

        # cycle parameters
        self.cycle_count = 0
        self._t_cycle_start = time.now()        # absolute time (s) at start of cycle
        self._t_insp_end = time.now()           # calculated time (s) at end of insp
        self._t_insp_pause_end = time.now()     # calculated time (s) at end of insp pause
        self._t_exp_end = time.now()            # calculated time (s) at end of exp
        self._t_exp_pause_end = time.now()      # calculated time (s) at end of exp pause
        self._t_period = time.now()             # calculated time (s) at end of cycle
        self._t_period_actual = time.now()      # absolute time (s) at end of cycle
        self._t_loop_start = time.now()         # absolute time (s) at start of control loop

        # ventilation parameters
        self.volume = 400
        self.bpm = 20
        self.ie = 1

        # physical parameters
        self.bag_size = 7                       # diameter of the ambu bag (in)

        # localize actuators and sensors
        self.motor = motor
        self.pressure_sensor = pressure_sensor
        self.upper_switch = upper_switch
        self.lower_switch = lower_switch
        self.power_switch = power_switch

        self.lower_switch.callback = self.contact_switch_callback
        self.upper_switch.callback = self.limit_switch_callback
        self.power_switch.callback = self.power_switch_callback

        # motion get_variables
        self.bag_clear_pos = 0

        # motor helper variables
        self._pose_at_contact = 0               # position of the encoder when arm contacts ambu bag
        self._homing_dir = 1
        self.motor_lower_target = 0             # the target pose of motor when the arm is coming down.
        self.motor_upper_target = 0             # the target pose of motor when the arm is going up.
        self.motor_current_target = 0
        self.motor_prev_target = 0

        self.measure_volume = 0
        self.measure_bpm    = 0
        self.measure_ie     = {"insp_time":time.now(),"exp_time":time.now(),"last_exp_pause_end":time.now(),"ie_ratio":""}
        
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

        self.logger.info("State change: " + self.current_state.name)

        with self._state_lock:
            self._entering_state = True
            self.current_state = state
            self._t_state_timer = time.now()

        self.logger.info(" --> " + self.current_state.name)

        self.state_change_sender.state_change_signal.emit()


    # calculate time parameters of ventilation
    def calculate_wave_form(self, tidal_volume, ie_ratio, bpm):

        self._t_period = 60.0 / bpm  # seconds per breath
        _t_period_end = add_secs(self._t_cycle_start, self._t_period)

        self._t_insp_pause_end = add_secs(self._t_cycle_start, self._t_period / (1 + ie_ratio))  # TODO: understand this
        self._t_insp_end = add_secs(self._t_cycle_start, (self._t_period / (1 + ie_ratio) - INSP_HOLD_DUR)) # self._t_cycle_start + self._t_insp_pause_end -   # TODO: understand this
        self._t_exp_end = min(add_secs(self._t_insp_pause_end, MAX_EXP_DUR),  # TODO: understand this
                              subtract_secs(_t_period_end, MIN_EXP_PAUSE))

        self._t_exp_pause_end = _t_period_end # add_secs(self._t_exp_end, MIN_EXP_PAUSE)

        self.logger.info("start:          " + str(time.now()))
        self.logger.info("insp end:       " + str(self._t_insp_end))
        self.logger.info("insp pause end: " + str(self._t_insp_pause_end))
        self.logger.info("exp end:        " + str(self._t_exp_end))
        self.logger.info("exp pause end:  " + str(self._t_exp_pause_end))
        
        # TODO: use tidal volume parameter
        # TODO: convert self.volume to encoder position
        # self.motor_upper_target =
        # self.motor_lower_target =
    
    def _set_motor_target(self, target):
        self.motor_prev_target = self.motor_current_target
        self.motor_current_target = target


    ###########################
    ## Main Ventilation Loop ##
    ###########################

    def start_ventilation(self):

        self.set_state(self.START_STATE)

        while True:
            self.ventilate()

    def stop_ventilation(self):
        self.logger.info("about to stop the motor")
        self.buzzer_1.disable_buzzer()
        self.buzzer_2.disable_buzzer()
        self.motor.stop()
        self.motor.destructor()

    def check_pressure(self):
        self.pressure_sensor.update_data()
        if self.pressure_sensor.get_raw_pressure() > 50:
            self.buzzer_1.enable_buzzer()
            self.buzzer_2.enable_buzzer()
            self.alarm_sender.alarm_signal.emit(
                UNDER_PRESSURE_ALARM("UNDER PRESSURE, check tube connections"))

    def ventilate(self):

        self._t_loop_start = time.now()
        self.buzzer_1.disable_buzzer()
        self.buzzer_2.disable_buzzer()
        # main finite state machine
        self.check_pressure()

        # == START_STATE == #
        if self.current_state is self.START_STATE:
            if self._entering_state:
                self._entering_state = False

            # does nothing in the start state
            self.set_state(self.INSP_STATE)
            self.current_state = self.INSP_STATE

        # == HOMING_STATE == #
        elif self.current_state is self.HOMING_STATE:
            if self._entering_state:
                self._entering_state = False

            # do nothing, ui_controller_interface will spawn homing thread

        # == HOMING_VERIF_STATE == #
        elif self.current_state is self.HOMING_VERIF_STATE:
            if self._entering_state:
                self._entering_state = False

        # == INSP_STATE == #
        elif self.current_state is self.INSP_STATE:
            if self._entering_state:
                self._entering_state = False
                self._t_period_actual = time.now() - self._t_cycle_start
                self.measure_bpm = 60.0 / self._t_period_actual.total_seconds()
                self.logger.info("freq: " + str(1.0 / self._t_period_actual.total_seconds()))
                self.logger.info("cur tar" + str(self.motor_current_target))
                self.logger.info("prev tar" + str(self.motor_prev_target))
                self.logger.info("lower: " + str(self.motor_lower_target))
                self.logger.info("upper: " + str(self.motor_upper_target))
                self._t_cycle_start = time.now()
                self.calculate_wave_form(tidal_volume=self.volume,
                                         ie_ratio=self.ie,
                                         bpm=self.bpm)
                self.cycle_count += 1

            # TODO: change/update this method
            result, _ = self.motor.move_to_encoder_pose_with_dur(
                                        pose=self.motor_current_target,
                                        dist=abs(self.motor_current_target
                                                    -self.motor_prev_target),
                                        dur=(self._t_insp_end-self._t_cycle_start).total_seconds()
                                        )

            if self.motor.encoder_position() == self.motor_lower_target and result is True:
                self.log_motor_position("Lower target reached (insp end actual: " + str(time.now()) + ")")
                self._set_motor_target(self.motor_upper_target)
                self.set_state(self.INSP_PAUSE_STATE)
            # TODO: commenting out for now because time is a construct
            # USER_CHECK_ALARM -- machine can keep running but user should check machine
            # if time.now() > self._t_insp_end:
            #    self.buzzer_1.enable_buzzer()
            #    self.buzzer_2.enable_buzzer()
            #    raise SYSTEM_ALARM("Inspiration exceeds time limit")

        # == INSP_PAUSE_STATE == #
        elif self.current_state is self.INSP_PAUSE_STATE:
            if self._entering_state:
                self._entering_state = False

            self.motor.stop()

            if time.now() > self._t_insp_pause_end:
                self.set_state(self.EXP_STATE)
                self.measure_ie["insp_time"] = self._t_insp_pause_end - self.measure_ie["last_exp_pause_end"] # end insp - start  # but doesn't work on the first first cycle

        # == EXP_STATE == #
        elif self.current_state is self.EXP_STATE:
            if self._entering_state:
                self._entering_state = False

            # TODO: change/update this method
            result, _ = self.motor.move_to_encoder_pose_with_dur(
                                        pose=self.motor_current_target,
                                        dist=abs(self.motor_current_target
                                                    -self.motor_prev_target),
                                        dur=(self._t_exp_end-self._t_insp_pause_end).total_seconds()
                                        )

            if self.motor.encoder_position() == self.motor_upper_target and result is True:
                self.log_motor_position("Upper target reached (exp end actual: " + str(time.now()) + ")")
                self._set_motor_target(self.motor_lower_target)
                self.set_state(self.EXP_PAUSE_STATE)
            # TODO: commenting out for now because time is a construct
            # USER_CHECK_ALARM -- machine can keep running but user should check machine
            # if time.now() > self._t_exp_end:
            #    self.buzzer_1.enable_buzzer()
            #    self.buzzer_2.enable_buzzer()
            #    raise SYSTEM_ALARM("Expiration exceeds time limit")

        # == EXP_PAUSE_STATE == #
        elif self.current_state is self.EXP_PAUSE_STATE:
            if self._entering_state:
                self._entering_state = False

            self.motor.stop()
            # update_measured_parameters()
            if time.now() > self._t_exp_pause_end:
                self.set_state(self.INSP_STATE)
                # self.set_state(self.HOMING_VERIF_STATE)
                self.measure_ie["last_exp_pause_end"] = self._t_exp_pause_end
                self.measure_ie["exp_time"] = self._t_exp_pause_end - self._t_insp_pause_end  # end insp - start
                # self.measure_ie["ie_ratio"] = f"{int(self.measure_ie['insp_time'].total_seconds())}/{int(self.measure_ie['exp_time'].total_seconds())}"
                
                self.measure_ie["ie_ratio"] = round(self.measure_ie['exp_time'].total_seconds() / 
                                              self.measure_ie['insp_time'].total_seconds())
                self.measured_parameters_sender.update_measured_parameters_signal.emit()
            
        # == PAUSE_STATE == #
        elif self.current_state is self.PAUSE_STATE: # TODO: define off behavior
            if self._entering_state:
                self._entering_state = False
            self.motor.stop()

        # == OFF_STATE == #
        elif self.current_state is self.OFF_STATE:  # TODO: define off behavior
            if self._entering_state:
                self._entering_state = False
            self.motor.stop()

        # == DEBUG_STATE == #
        if self.current_state is self.DEBUG_STATE:  # TODO: define debug behavior
            self.motor.stop()

        # TODO: add delay to loop if there is extra time



    def start_homing(self):
        self.buzzer_1.disable_buzzer()
        self.buzzer_2.disable_buzzer()

        if self.current_state is not self.HOMING_STATE:
            self.buzzer_1.enable_buzzer()
            self.buzzer_2.enable_buzzer()
            raise HOMING_ALARM("Attempted homing outside homing state")

        self.logger.info("=== Homing Started ===")

        self.clear_limit_switches()
        self.logger.info("Cleared limit switches")

        while self.current_state is self.HOMING_STATE:
            self.home()


    def clear_limit_switches(self):

        while self.upper_switch.contacted():
            self.motor.set_velocity(-1 * HOMING_VELOCITY)

        while self.lower_switch.contacted():
            self.motor.set_velocity(HOMING_VELOCITY)


    def home(self):
        """
        Homing method for the ventilator
        """

        if self.current_state is not self.HOMING_STATE:
            self.buzzer_1.enable_buzzer()
            self.buzzer_2.enable_buzzer()
            self.alarm_sender.alarm_signal.emit(
                HOMING_ALARM("Attempted homing outside homing state"))
        
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

            # TODO: set bag_size appropriately

            # change state
            if self._homing_dir != 1:
                self.set_state(self.HOMING_VERIF_STATE)
                self._homing_dir = 1
            else:
                self.buzzer_1.enable_buzzer()
                self.buzzer_2.enable_buzzer()
                self.alarm_sender.alarm_signal.emit(
                    HOMING_ALARM("Reached lower bound before upper bound, check pulley winding"))

            self.log_motor_position("Homing lower bound reached")
            self.logger.info("=== Homing Finished ===")
            sleep(0.25)

        # no contact with any switch
        elif not self.upper_switch.contacted() and not self.lower_switch.contacted():
            self.motor.set_velocity(self._homing_dir * HOMING_VELOCITY)

        # contact with both switches -- error
        elif self.upper_switch.contacted() and self.lower_switch.contacted():
            self.buzzer_1.enable_buzzer()
            self.buzzer_2.enable_buzzer()
            self.motor.stop()
            self.alarm_sender.alarm_signal.emit(
                HOMING_ALARM("Both contact switches are pressed"))

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
        #         if self.current_state is not self.HOMING_STATE:
        #             self.stop_ventilation()
        #             raise SYSTEM_ALARM("Limit switch tripped")
        pass

    def power_switch_callback(self, status):
        """
        This method is called when the power switch is flipped
        @param status: the status of the switch
        """
        if status is 0:
            self.logger.info("Power Switch Flipped: OFF")
            if self.current_state is not self.HOMING_STATE:
                self.set_state(self.PAUSE_STATE)
        
        else:
            self.logger.info("Power Switch Flipped: ON")
            if self.current_state is not self.HOMING_STATE:
                self.set_state(self.HOMING_STATE)

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
        log the motor position with a custom
        message if needed.
        @param message: a custom message to
        be logged
        """
        self.logger.info("{} encoder: {}, motor controller: {}".format(message,
                                                            self.motor.encoder_position(),
                                                            self.motor.motor_position()))

    # TODO: raise errors for values outside defined bounds

    def update_bpm(self, value):
        self.bpm = value
        self.logger.info('BPM set to: ' + str(value))

    def update_ie(self, value):
        self.ie = value
        self.logger.info('IE set to: ' + str(value))

    def update_tidal_volume(self, value):
        if( TIDAL_VOLUME_MAX < value ): # TODO signal in gui that the value is illegal
            value = TIDAL_VOLUME_MAX
        elif ( value < TIDAL_VOLUME_MIN ):
            value = TIDAL_VOLUME_MIN
        self.volume = value

        self.motor_lower_target = int(self._pose_at_contact - ENCODER_ONE_ROTATION * self.volume * TV_PULLEY_CONVERT_FACTOR)
        self.motor_upper_target = int(self._pose_at_contact)
        # this line below is trying to fix a bug with the _set_motor_target method. 
        # because we don't want the prev_target value to be zero. 
        if(self.current_state is self.EXP_STATE or
             self.current_state is self.INSP_PAUSE_STATE):
            # _set_motor_target assigns the current_target to prev_target
            #     here, set current_target to lower_target
            #     so that prev_target is assigned to lower_target and 
            #     the last update sets current_target to upper_target
            self.motor_current_target = self.motor_lower_target
            self._set_motor_target(self.motor_upper_target)
        else:
            self.motor_current_target = self.motor_upper_target
            self._set_motor_target(self.motor_lower_target)

        self.logger.info("lower target: "+ str(self.motor_lower_target))
        self.logger.info("upper target: "+ str(self.motor_upper_target))
        self.logger.info('TV set to: ' + str(value))

    # TODO: write alarm functions -> sound buzzer, etc.
