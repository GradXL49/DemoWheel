"""
Grady Landers
Demo Wheel - settingwidget.py
Custom class for a bundled setting control widget. Automatically combines the control and the label for less code in the app window.
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor

class SettingWidget(QWidget):
    def __init__(self, label:str, value):
        #initialize
        super(SettingWidget, self).__init__()

        #create and set layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        #crate and add label
        self.label = QLabel(label+':')
        layout.addWidget(self.label)

        #create and add control
        if isinstance(value, QColor):
            self.control = QPushButton()
            self.control.setStyleSheet('background-color: rgba'+str(value.getRgb()))
        elif type(value) is float:
            self.control = QSpinBox()
            self.control.setValue(value)
        elif type(value) is str:
            if value is 'FILEPATH':
                self.control = QPushButton('Choose File...')
            else:
                self.control = QComboBox()
        elif type(value) is bool:
            self.control = QCheckBox()
            self.control.setChecked(value)
        else:
            print('ERROR: Unexpected value type.')
        layout.addWidget(self.control)
    
    def get_control(self):
        return self.control
    
    def get_value(self):
        try:
            value = self.control.value()
        except:
            try: value = self.control.isChecked()
            except: value = None
        return value
