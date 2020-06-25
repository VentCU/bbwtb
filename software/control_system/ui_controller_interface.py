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

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Worker takes in a function and runs it within a QRunnable
# so that in can run in a separate thread within the QThreadPool
# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
    
    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs
        '''
        self.fn(*self.args, **self.kwargs)


class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.threadpool = QThreadPool()
        self.alarm_handler = AlarmHandler(self.ui, self.controller)
        threading.excepthook = self.except_alarm_hook

        self.interface_elements()

    def interface_elements(self):

        self.controller.state_change_sender.state_change_signal.connect(
            lambda: self.state_change()
        )

        # start_homing window elements
        self.ui.stack.start_homing.start_button.clicked.connect(
            lambda: self.start_homing()
        )

        # confirm_homing window elements
        self.ui.stack.confirm_homing.rehome_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.start_homing )
        )

        self.ui.stack.confirm_homing.bag_size_label.setText( str(self.controller.bag_size) )     # TODO: format text as inches

        # edit_parameters window elements
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.edit_parameters.back_button.hide()

        self.ui.stack.edit_parameters.TV_label.setText( str(self.controller.volume) )
        self.ui.stack.edit_parameters.BPM_label.setText( str(self.controller.bpm) )
        self.ui.stack.edit_parameters.IE_label.setText( str(self.controller.ie) )

        # TODO: redefine logical values for increasing and decreasing
        self.ui.stack.edit_parameters.tidal_increase_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_tidal_volume(self.controller.volume + 1) )
        )
        self.ui.stack.edit_parameters.tidal_decrease_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_tidal_volume(self.controller.volume - 1) )
        )

        self.ui.stack.edit_parameters.bpm_increase_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_bpm(self.controller.bpm + 1) )
        )
        self.ui.stack.edit_parameters.bpm_decrease_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_bpm(self.controller.bpm - 1) )
        )

        self.ui.stack.edit_parameters.ie_increase_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_ie(self.controller.ie + 1) )
        )
        self.ui.stack.edit_parameters.ie_decrease_button.clicked.connect(
            lambda: self.try_controller_method( self.controller.update_ie(self.controller.ie - 1) )
        )

        # confirm_parameters window elements
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.confirm_parameters.confirm_button.setText( "Start Ventilation" )
        else:
            self.ui.stack.confirm_parameters.confirm_button.setText( "Confirm" )      # TODO: determine if necessary
        
        print(self.controller.ie)
        print(self.controller.bpm)
        print(self.controller.volume)

        self.ui.stack.confirm_parameters.confirm_button.clicked.connect(
            lambda: self.new_thread("ventilate_thread", self.controller.start_ventilation)
        )

        # main_window window elements
        self.ui.stack.main_window.set_TV_label.setText( str(self.controller.volume) )
        self.ui.stack.main_window.set_BPM_label.setText( str(self.controller.bpm) )
        self.ui.stack.main_window.set_IE_label.setText( str(self.controller.ie) )

        # TODO: connect graph to pressure data from controller

        # TODO: connect the following
        # self.ui.stack.main_window.set_PEEP_label.setText( str() )
        # self.ui.stack.main_window.set_PIP_label.setText( str() )
        # self.ui.stack.main_window.set_PLAT_label.setText( str() )
        # self.ui.stack.main_window.measured_TV_label.setText( str() )
        # self.ui.stack.main_window.measured_BPM_label.setText( str() )
        # self.ui.stack.main_window.measured_IE_label.setText( str() )
        # self.ui.stack.main_window.measured_PEEP_label.setText( str() )
        # self.ui.stack.main_window.measured_PIP_label.setText( str() )
        # self.ui.stack.main_window.measured_PLAT_label.setText( str() )

        # self.ui.stack.main_window.message_log_label.setText( str() )



    def new_thread(self, name, target_method):
        """ self.new_thread = threading.Thread(target=target_method, args=(), daemon=True)
        self.new_thread.setName(name)
        self.new_thread.start() """
        worker = Worker(target_method)
        self.threadpool.start(worker)
        print("New thread spawned: " + name)


    def start_homing(self):
        self.ui.stack.QtStack.setCurrentWidget(self.ui.stack.homing)

        self.new_thread("homing_thread", self.controller.start_homing)


    def state_change(self):
    
        # switch window if homing successfuly completes
        if self.controller.current_state is self.controller.HOMING_VERIF_STATE:
            self.ui.stack.QtStack.setCurrentWidget(self.ui.stack.confirm_homing)


    def try_controller_method(self, method, state_to_set=None):
        if state_to_set is not None:
            self.controller.set_state(state_to_set)

        try:
            method()
        except Alarm as alarm:
            self.alarm_handler.handle_alarms(alarm)

    def except_alarm_hook(args):

        if args.exc_type is type(Alarm):
            self.alarm_handler.handle_alarms(args.exc_value)   # TODO: verify that raising exception kills thread

        else:
            raise args.exec_value
