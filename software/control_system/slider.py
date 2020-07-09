import sys
from PyQt5.QtWidgets import  QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class DebbugingSlider():

  def __init__(self , custom_name_list = None ):
      self.name_value_dict = {}
      self.label_keys = []
      self.name_range = 4
      self.idx = 0
      if( custom_name_list ):
          self.name_range = len(custom_name_list)
          for name in custom_name_list:
            self.label_keys.append(name)
      else :
        self.label_keys = [" Encoder Rotation Scalar ",
                          " BPM ",
                          "OTHER3","OTHER4","OTHER5","OTHER6","OTHER7","OTHER8"]
      app = QApplication(sys.argv)
      window = QWidget()
      vbox = QVBoxLayout()
      for count in range(4):
        self.make_slider( count , window , vbox )
      window.setLayout(vbox)
      window.setGeometry(50,50,320,200)
      window.setWindowTitle("Parameter tuning")
      window.show()
      sys.exit(app.exec_())

  def get_value( self, key_name ):
      """Get Slider Value Helper function"""
      return self.name_value_dict[ key_name ]

  def change_value( self, widget_dict ):
      """Slot function."""
      widget_dict["value_label"].setText(str(widget_dict["slider"].value()))
      self.name_value_dict[ widget_dict["name_label"] ] = widget_dict["slider"].value()

  def make_slider( self, count , win , vbox):
      """Slider + text constructor."""
      start_val = 0
      # make text display
      name_label = QLabel( self.label_keys[self.idx])
      value_label = QLabel(str(start_val))
      value_label.setFont(QtGui.QFont("Sanserif", 15))
      value_label.setFont(QtGui.QFont("Sanserif", 15))
      vbox.setAlignment(Qt.AlignCenter)

      # make slider
      mySlider = QSlider(Qt.Horizontal,win)
      mySlider.setTickPosition(QSlider.TicksBelow)
      mySlider.setTickInterval( 1 )
      mySlider.setMinimum(0)
      mySlider.setMaximum(10)
      mySlider.setOrientation(Qt.Horizontal)

      # add widgets
      vbox.addWidget(name_label)
      vbox.addWidget(value_label)
      vbox.addWidget(mySlider)

      # object retrieval
      self.name_value_dict[ self.label_keys[self.idx] ] = start_val
      widget_dict = {"slider" :mySlider , "value_label":value_label ,"name_label":name_label}
      mySlider.valueChanged[int].connect( lambda: self.change_value(widget_dict) )
      self.idx += 1 


if __name__ == '__main__':
    DebbugingSlider()




