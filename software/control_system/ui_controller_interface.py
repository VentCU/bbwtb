#
# UIControllerInterface class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

from time import sleep
from alarms.alarm_handler import AlarmHandler
from alarms.alarms import *
import threading

class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.alarm_handler = AlarmHandler(self.ui, self.controller)
        threading.excepthook = self.except_alarm_hook

        self.interface_elements()

    def interface_elements(self):

        # start_homing window elements
        self.ui.stack.start_homing.start_button.clicked.connect(
            lambda:
                self.try_controller_method( self.controller.home() )
        )

           # switch window if homing successfuly completes
        if (self.controller.current_state is self.controller.HOMING_VERIF_STATE):
            self.ui.stack.QtStack.setCurrentWidget(self.ui.stack.confirm_homing)
        

        # confirm_homing window elements
        self.ui.stack.confirm_homing.rehome_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.home() )
        )

        self.ui.stack.confirm_homing.bag_size_label.setText( self.controller.bag_size )     # TODO: format text as inches

        # edit_parameters window elements
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.edit_parameters.back_button.hide()

        self.ui.stack.edit_parameters.tidal_volume_label.setText( self.controller.volume )
        self.ui.stack.edit_parameters.bpm_label.setText( self.controller.bpm )
        self.ui.stack.edit_parameters.ie_ratio_label.setText( self.controller.ie )

        # TODO: redefine logical values for increasing and decreasing
        self.ui.stack.edit_parameters.tidal_increase_button.connect(
            lambda: self.try_controller_method( self.controller.update_tidal_volume(self.controller.volume + 1) )
        )
        self.ui.stack.edit_parameters.tidal_decrease_button.connect(
            lambda: self.try_controller_method( self.controller.update_tidal_volume(self.controller.volume - 1) )
        )

        self.ui.stack.edit_parameters.bpm_increase_button.connect(
            lambda: self.try_controller_method( self.controller.update_bpm(self.controller.bpm + 1) )
        )
        self.ui.stack.edit_parameters.bpm_decrease_button.connect(
            lambda: self.try_controller_method( self.controller.update_bpm(self.controller.bpm - 1) )
        )

        self.ui.stack.edit_parameters.ie_increase_button.connect(
            lambda: self.try_controller_method( self.controller.update_ie(self.controller.ie + 1) )
        )
        self.ui.stack.edit_parameters.ie_decrease_button.connect(
            lambda: self.try_controller_method( self.controller.update_ie(self.controller.ie - 1) )
        )

        # confirm_parameters window elements
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.confirm_parameters.confirm_button.setText( "Start Ventilation" )
        else:
            self.ui.stack.confirm_parameters.confirm_button.setText( "Confirm" )      # TODO: determine if necessary

        self.ui.stack.confirm_parameters.confirm_button.connect(
            lambda: self.try_controller_method( self.controller.start_ventilation() )
            self.ventilate_thread = threading.Thread(target=self.controller.start_ventilation(), args=(), daemon=True)
            self.ventilate_thread.start()
        )

        # main_window window elements
        self.ui.stack.main_window.tidal_label.setText( self.controller.volume )
        self.ui.stack.main_window.bpm_label.setText( self.controller.bpm )
        self.ui.stack.main_window.ie_label.setText( self.controller.ie )
        # TODO: connect graph to pressure data from controller


    def try_controller_method(self, method):

        try:
            method()
        except Alarm as alarm:
            self.alarm_handler.handle_alarms(alarm)

    def except_alarm_hook(args):

        if args.exc_type is type(Alarm):
            self.alarm_handler.handle_alarms(args.exc_value)   # TODO: verify that raising exception kills thread

        else:
            raise args.exec_value
