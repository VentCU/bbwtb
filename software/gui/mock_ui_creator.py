# PyQt Mock UI for VentCU,
# an open source ventilator
#
# (c) VentCU, 2020. All Rights Reserved.
# Contact: i.noah@columbia.edu

from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("mock.ui")
window.show()

app.exec_()
