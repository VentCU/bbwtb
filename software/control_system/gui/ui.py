from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from random import uniform
import logging

sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/gui')
from slider import DebbugingSlider

sys.path.append('/home/pi/Workspace/bbwtb/software/control_system/sensors')
from pressure_sensor import PressureSensor

pyqt_logger = logging.getLogger('PyQt5')
pyqt_logger.setLevel(logging.CRITICAL)

class WindowStack(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(WindowStack, self).__init__(*args, **kwargs)

        self.QtStack = QtWidgets.QStackedLayout()

        # Instantiate windows
        self.start = Start()
        self.start_homing = StartHoming()
        self.homing = Homing()
        self.confirm_homing = ConfirmHoming()
        self.edit_parameters = EditParameters()
        self.confirm_parameters = ConfirmParameters()
        self.main_window = MainWindow()
        self.alarm_condition = AlarmCondition()

        # Add windows to stack
        self.QtStack.addWidget(self.start)
        self.QtStack.addWidget(self.start_homing)
        self.QtStack.addWidget(self.homing)
        self.QtStack.addWidget(self.confirm_homing)
        self.QtStack.addWidget(self.edit_parameters)
        self.QtStack.addWidget(self.confirm_parameters)
        self.QtStack.addWidget(self.main_window)
        self.QtStack.addWidget(self.alarm_condition)

        self.setup_window_navigation()

        # set starting window
        self.QtStack.setCurrentWidget(self.start)


    def setup_window_navigation(self):

        # start window buttons
        self.start.start_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.start_homing)
        )

        # start_homing window buttons
        self.start_homing.start_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.homing)
        )
        self.start_homing.cancel_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.start)
        )

        # confirm_homing window buttons
        self.confirm_homing.rehome_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.homing)
        )
        self.confirm_homing.confirm_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.edit_parameters)
        )

        # edit_parameters window buttons
        self.edit_parameters.back_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.main_window)
        )
        self.edit_parameters.set_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.confirm_parameters)
        )

        # confirm_parameters window buttons
        self.confirm_parameters.confirm_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.main_window)
        )
        self.confirm_parameters.cancel_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.edit_parameters)
        )

        # main_window window buttons
        self.main_window.edit_parameters_button.clicked.connect(
            lambda: self.QtStack.setCurrentWidget(self.edit_parameters)
        )




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set default plot colors
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # Load the UI Page
        uic.loadUi('gui/main_window.ui', self)

        self.initialize_plots()

        self.timer = pg.QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plots)
        self.timer.start()

    def initialize_plots(self):
        global chunk_size, x_axis, pressure_data, flow_data, volume_data, plot_ptr

        chunk_size = 100

        x_axis = []
        plot_ptr = 0 # last updated x value

        self.pressure_sensor = PressureSensor()

        pressure_data = []
        # flow_data = []
        # volume_data = []

        pen_red = pg.mkPen(color=(255, 0, 0), width=3)
        # pen_blue = pg.mkPen(color=(0, 0, 255), width=3)
        # pen_green = pg.mkPen(color=(100, 160, 100), width=3)
        self.pressure_curve = self.pressure_graph.plot(x_axis, pressure_data, pen=pen_red)
        # self.flow_curve = self.flow_graph.plot(x_axis, flow_data, pen=pen_blue)
        # self.volume_curve = self.volume_graph.plot(x_axis, volume_data,pen=pen_green)

        self.pressure_graph.setMouseEnabled(x=False, y=False)
        # self.flow_graph.setMouseEnabled(x=False, y=False)
        # self.volume_graph.setMouseEnabled(x=False, y=False)

        self.pressure_graph.setMenuEnabled(False)
        # self.flow_graph.setMenuEnabled(False)
        # self.volume_graph.setMenuEnabled(False)

        # Labeling the x-axis takes up too much space
        # self.pressure_graph.setLabel('bottom', 'Time', 's')
        # self.flow_graph.setLabel('bottom', 'Time', 's')
        # self.volume_graph.setLabel('bottom', 'Time', 's')

        # set graph labels
        self.pressure_graph.setLabel('left', 'Pressure', 'cmH2O')
        # self.flow_graph.setLabel('left', 'Flow', 'L/m')
        # self.volume_graph.setLabel('left', 'Volume', 'L')

        # set the y axis range
        self.pressure_graph.setYRange(0, 100)
        # self.flow_graph.setYRange(-60, 60)
        # self.volume_graph.setYRange(0, 1)

        self.pressure_graph.setXRange(0, chunk_size)
        # self.flow_graph.setXRange(0, chunk_size)
        # self.volume_graph.setXRange(0, chunk_size)

        # hide the little A buttons
        self.pressure_graph.hideButtons()
        # self.flow_graph.hideButtons()
        # self.volume_graph.hideButtons()

    def update_plots(self):
        global chunk_size, x_axis, pressure_data, plot_ptr #, flow_data, volume_data

        self.pressure_sensor.update_data()
        # Clear plot if chunk size reached
        if plot_ptr == chunk_size:
            x_axis = []

            pressure_data = []
            # flow_data = []
            # volume_data = []

            plot_ptr = 0

        x_axis.append(plot_ptr)

        pressure_data.append(self.pressure_sensor.get_raw_pressure())
        # flow_data.append( uniform(-60, 60) )
        # volume_data.append( uniform(0, 1) )

        self.pressure_curve.setData(x_axis, pressure_data)
        # self.flow_curve.setData(x_axis, flow_data)
        # self.volume_curve.setData(x_axis, volume_data)

        plot_ptr += 1



class EditParameters(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(EditParameters, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/edit_parameters.ui', self)

class ConfirmParameters(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ConfirmParameters, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/confirm_parameters.ui', self)


class Start(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Start, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/start.ui', self)


class StartHoming(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(StartHoming, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/start_homing.ui', self)


class Homing(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Homing, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/homing.ui', self)


class ConfirmHoming(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ConfirmHoming, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/confirm_homing.ui', self)


class AlarmCondition(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AlarmCondition, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('gui/alarm_condition.ui', self)


class UI():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.stack = WindowStack()
        self.debug_slider = DebbugingSlider()


if __name__ == '__main__':
    ui = UI()
