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

    def get_scale_factor( self,  tic_count ):
        """
        allow changing pid time scale factor depending on desired travel distance
        Should fit fine b.c. at degree 4 the residual was too small to count
        
        @param tic_count: the total distance the motor should move
        @return:     the pid time scale factor to allow correct motor movement
        """
        degree = 4
        #tic_count = [100,250,300,500,650]
        #scalefactor = [.01555,.0072,.00615,.00415,.0035]
        #np.polyfit( tic_count , scalefactor , degree , full = True)
        
        # polyfit returns coefficients in x**n + .. + x**0 order
        coefficients = [ 4.61471861e-13,
             -8.54025974e-10,  5.93469697e-07, -1.91823377e-04, 2.96055195e-02 ]
        pid_scale_factor = 0
        for c in coefficients:
            raised = pow( tic_count, degree )
            pid_scale_factor += c*raised
            degree -= 1
        return pid_scale_factor 

    def move_to_encoder_pose_with_dur(self, pose, dist, dur):
        """
        use a pid controller to reach the target position specified in the
        parameter of the method over the duration specified in the parameter
        of the method.

        @param pose: the target position of the motor
        @param dist: the total distance the motor should move
        @param dur: the target duration the move should take (in seconds)
        @return:     true of the motor has reached its goal
        """

        if dur <= 0: return False   # cannot move in negative or zero time
        
        dynamic_pid_time_scale = self.get_scale_factor( abs(dist) )
        scale_factor = dynamic_pid_time_scale * abs(dist) / dur
        # scale_factor = PID_TIME_SCALE_FACTOR * abs(dist) / dur
        
        # ensure scale_factor remains within velocity bounds
        if scale_factor > 10: scale_factor = 10                 # TODO: replace with max vel const
        elif scale_factor < 0.01: scale_factor = 0.01           # TODO: replace with min vel const

        return self.move_to_encoder_pose(pose, vel_const=scale_factor)

    def move_to_encoder_pose(self, pose, vel_const=1):
        """
        use a pid controller to reach the target
        position specified in the parameter of the
        method.

        @param vel_const: the constant that get multiplied to the pid output
        @param pose: the target position of the motor
        @return:     true if the motor has reached its goal
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
