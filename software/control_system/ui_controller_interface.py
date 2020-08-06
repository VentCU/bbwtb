#
# UIControllerInterface class
# VentCU - An open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
#

import logging
from time import sleep
import threading

from alarms.alarm_handler import AlarmHandler
from alarms.alarms import *

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Worker takes in a function and runs it within a QRunnable
# so that in can run in a separate thread within the QThreadPool
# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs
        """
        self.fn(*self.args, **self.kwargs)


class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.logger = logging.getLogger('ui_controller_interface')
        
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.threadpool = QThreadPool()
        self.alarm_handler = AlarmHandler(self.ui, self.controller)
        threading.excepthook = self.except_alarm_hook

        self.modified_volume = self.controller.volume
        self.modified_bpm = self.controller.bpm
        self.modified_ie = self.controller.ie

        self.interface_elements()

        self.ventilate_thread_spawned = False

    def interface_elements(self):

        self.controller.state_change_sender.state_change_signal.connect(
            lambda: self.state_change()
        )

        self.controller.shutdown_sender.shutdown_signal.connect(
            lambda: self.try_controller_method( self.controller.set_state, parameters=self.controller.OFF_STATE )
        )

        """
        start_homing window elements
        """
        self.ui.stack.start_homing.start_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.set_state, parameters=self.controller.HOMING_STATE )
        )

        """
        confirm_homing window elements
        """
        self.ui.stack.confirm_homing.rehome_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.set_state, parameters=self.controller.HOMING_STATE )
        )

        self.update_label(self.ui.stack.confirm_homing.bag_size_label, self.controller.bag_size)     # TODO: format text as inches

        """
        edit_parameters window elements
        """
        def update_edit_parameters_elements():
            if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
                self.ui.stack.edit_parameters.back_button.hide()
            else:
                self.ui.stack.edit_parameters.back_button.show()

        self.ui.stack.confirm_homing.confirm_button.clicked.connect(update_edit_parameters_elements)
        self.ui.stack.main_window.edit_parameters_button.clicked.connect(update_edit_parameters_elements)

        self.update_label(self.ui.stack.edit_parameters.TV_label, self.controller.volume)
        self.update_label(self.ui.stack.edit_parameters.BPM_label, self.controller.bpm)
        self.update_label(self.ui.stack.edit_parameters.IE_label, self.controller.ie)

        # TODO: redefine logical values for increasing and decreasing
        self.ui.stack.edit_parameters.tidal_increase_button.clicked.connect(
            lambda: self.modify_interface_parameters(volume=self.modified_volume + 10)
        )
        self.ui.stack.edit_parameters.tidal_decrease_button.clicked.connect(
            lambda: self.modify_interface_parameters(volume=self.modified_volume - 10)
        )
        self.ui.stack.edit_parameters.bpm_increase_button.clicked.connect(
            lambda: self.modify_interface_parameters(bpm=self.modified_bpm + 1)
        )
        self.ui.stack.edit_parameters.bpm_decrease_button.clicked.connect(
            lambda: self.modify_interface_parameters(bpm=self.modified_bpm - 1)
        )
        self.ui.stack.edit_parameters.ie_increase_button.clicked.connect(
            lambda: self.modify_interface_parameters(ie=self.modified_ie + 1)
        )
        self.ui.stack.edit_parameters.ie_decrease_button.clicked.connect(
            lambda: self.modify_interface_parameters(ie=self.modified_ie - 1)
        )

        """
        confirm_parameters window elements
        """
        def update_confirm_parameters_elements():
            if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
                self.update_label(self.ui.stack.confirm_parameters.confirm_button, "Start")
            else:
                self.update_label(self.ui.stack.confirm_parameters.confirm_button,  "Confirm" )

            self.update_label(self.ui.stack.confirm_parameters.confirm_TV_label, self.modified_volume)
            self.update_label(self.ui.stack.confirm_parameters.confirm_BPM_label, self.modified_bpm)
            self.update_label(self.ui.stack.confirm_parameters.confirm_IE_label, self.modified_ie)

        self.ui.stack.edit_parameters.set_button.clicked.connect(update_confirm_parameters_elements)

        # begin main ventilate thread
        self.ui.stack.confirm_parameters.confirm_button.clicked.connect(
            lambda: self.start_ventilate_thread()
        )

        """
        main_window window elements
        """
        self.update_label(self.ui.stack.main_window.set_TV_label, self.controller.volume)
        self.update_label(self.ui.stack.main_window.set_BPM_label, self.controller.bpm)
        self.update_label(self.ui.stack.main_window.set_IE_label, self.controller.ie)

        # TODO: connect graph to pressure data from controller

        # TODO: connect the following
        # self.update_label(self.ui.stack.main_window.set_PEEP_label, value )
        # self.update_label(self.ui.stack.main_window.set_PIP_label, value )
        # self.update_label(self.ui.stack.main_window.set_PLAT_label, value )
        # self.update_label(self.ui.stack.main_window.measured_TV_label, value )
        # self.update_label(self.ui.stack.main_window.measured_BPM_label, value )
        # self.update_label(self.ui.stack.main_window.measured_IE_label, value )
        # self.update_label(self.ui.stack.main_window.measured_PEEP_label, value )
        # self.update_label(self.ui.stack.main_window.measured_PIP_label, value )
        # self.update_label(self.ui.stack.main_window.measured_PLAT_label, value )
        # self.update_label(self.ui.stack.main_window.message_log_label, value )

    def modify_interface_parameters(self, volume=None, bpm=None, ie=None):
        # update local modified parameters
        if volume: self.modified_volume = volume    # TODO: add bounds
        if bpm: self.modified_bpm = bpm             # TODO: add bounds
        if ie: self.modified_ie = ie                # TODO: add bounds

        # update display elements
        self.update_label(self.ui.stack.edit_parameters.TV_label, self.modified_volume)
        self.update_label(self.ui.stack.edit_parameters.BPM_label, self.modified_bpm)
        self.update_label(self.ui.stack.edit_parameters.IE_label, self.modified_ie)

    def start_ventilate_thread(self):
        # update controller parameters from interface parameters
        self.try_controller_method( self.controller.update_tidal_volume, parameters=self.modified_volume )
        self.try_controller_method( self.controller.update_bpm, parameters=self.modified_bpm )
        self.try_controller_method( self.controller.update_ie, parameters=self.modified_ie )

        if( not self.ventilate_thread_spawned ):
            # spawn ventilate thread
            self.new_thread("ventilate_thread", self.controller.start_ventilation)
            self.ventilate_thread_spawned = True
    
    def update_label(self, label, value):
        label.setText( str(value) )

    def new_thread(self, name, target_method):
        worker = Worker(target_method)
        self.threadpool.start(worker)
        # print("New thread spawned: " + name)
        self.logger.info(f"New thread spawned: {name}")


    def start_homing(self):
        self.ui.stack.QtStack.setCurrentWidget(self.ui.stack.homing)
        self.new_thread("homing_thread", self.controller.start_homing)

    def state_change(self):
        # start homing if state changes to homing state
        if self.controller.current_state is self.controller.HOMING_STATE:
            self.start_homing()

        # switch window if homing successfuly completes
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.QtStack.setCurrentWidget(self.ui.stack.confirm_homing)

    def try_controller_method(self, method, state_to_set=None, parameters=None):
        if state_to_set is not None:
            self.controller.set_state(state_to_set)

        try:
            if parameters is None:
                method()
            else:
                method(parameters)
        except Alarm as alarm:
            self.alarm_handler.handle_alarms(alarm)

    def except_alarm_hook(self, args):
        if args.exc_type is type(Alarm):
            self.alarm_handler.handle_alarms(args.exc_value)   # TODO: verify that raising exception kills thread
        else:
            raise args.exec_value
