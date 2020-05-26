# This Python file uses the following encoding: utf-8
# from PySide2.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from random import uniform


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set default plot colors
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # Load the UI Page
        uic.loadUi('mock.ui', self)

        self.edit_parameters_window = EditParameters(self)
        self.edit_parameters_button.clicked.connect(lambda: self.edit_parameters_window.show())

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

        pressure_data = []
        flow_data = []
        volume_data = []

        pen_red = pg.mkPen(color=(255, 0, 0), width=3)
        pen_blue = pg.mkPen(color=(0, 0, 255), width=3)
        pen_green = pg.mkPen(color=(100, 160, 100), width=3)
        self.pressure_curve = self.pressure_graph.plot(x_axis, pressure_data, pen=pen_red)
        self.flow_curve = self.flow_graph.plot(x_axis, flow_data, pen=pen_blue)
        self.volume_curve = self.volume_graph.plot(x_axis, volume_data,pen=pen_green)

        self.pressure_graph.setMouseEnabled(x=False, y=False)
        self.flow_graph.setMouseEnabled(x=False, y=False)
        self.volume_graph.setMouseEnabled(x=False, y=False)

        self.pressure_graph.setMenuEnabled(False)
        self.flow_graph.setMenuEnabled(False)
        self.volume_graph.setMenuEnabled(False)

        # Labeling the x-axis takes up too much space
        # self.pressure_graph.setLabel('bottom', 'Time', 's')
        # self.flow_graph.setLabel('bottom', 'Time', 's')
        # self.volume_graph.setLabel('bottom', 'Time', 's')

        # set graph labels
        self.pressure_graph.setLabel('left', 'Pressure', 'cmH2O')
        self.flow_graph.setLabel('left', 'Flow', 'L/m')
        self.volume_graph.setLabel('left', 'Volume', 'L')

        # set the y axis range
        self.pressure_graph.setYRange(0, 50)
        self.flow_graph.setYRange(-60, 60)
        self.volume_graph.setYRange(0, 1)

        self.pressure_graph.setXRange(0, chunk_size)
        self.flow_graph.setXRange(0, chunk_size)
        self.volume_graph.setXRange(0, chunk_size)

        # hide the little A buttons
        self.pressure_graph.hideButtons()
        self.flow_graph.hideButtons()
        self.volume_graph.hideButtons()

    def update_plots(self):
        global chunk_size, x_axis, pressure_data, flow_data, volume_data, plot_ptr

        # Clear plot if chunk size reached
        if plot_ptr == chunk_size:
            x_axis = []

            pressure_data = []
            flow_data = []
            volume_data = []

            plot_ptr = 0

        x_axis.append(plot_ptr)

        pressure_data.append( uniform(0, 50) )
        flow_data.append( uniform(-60, 60) )
        volume_data.append( uniform(0, 1) )

        self.pressure_curve.setData(x_axis, pressure_data)
        self.flow_curve.setData(x_axis, flow_data)
        self.volume_curve.setData(x_axis, volume_data)

        plot_ptr += 1



class EditParameters(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(EditParameters, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('edit_parameters.ui', self)


class UI():

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        main = MainWindow()
        main.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    ui = UI()


#if __name__ == "__main__":
#    app = QApplication([])
#    # ...
#    sys.exit(app.exec_())
