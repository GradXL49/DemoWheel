"""
Grady Landers
Demo Wheel - settingswindow.py
Code for the window that contains the settings for the main window.
"""

#imports
from PyQt6.QtWidgets import *

class SettingsWindow(QWidget):
    def __init__(self, mainwindow, settings):
        #initialization
        super().__init__()
        self.mainwindow = mainwindow
        self.settings = settings
        self.options = {}

        #gui elements
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 400)
        tabs = QTabWidget()
        #tabs.setTabPosition(QTabWidget.TabPosition.West)
        btn_submit = QPushButton("Apply")
        btn_submit.clicked.connect(lambda: self.submit())

        #Wheel tab
        tab_wheel = self.init_tab_wheel()
        tabs.addTab(tab_wheel, "Wheel")

        #Titles tab
        

        #layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(tabs, 0, 0)
        layout.addWidget(btn_submit, 1, 0)

    #action for APPLY button
    def submit(self):
        for category in self.options:
            for option in self.options[category]:
                if 'color' not in option and 'type' not in option and 'list' not in option:
                    self.settings.set_value(category, option, self.options[category][option].value())
        
        self.settings.save_config()
        self.mainwindow.update_settings()
    
    #opens a color picker dialog for choosing colors
    def get_color(self, category, option):
        color = QColorDialog().getColor(self.settings.get_value(category, option))
        self.settings.set_value(category, option, color)
        self.settings.save_config()
        self.mainwindow.update_settings()

    #create the wheel tab
    def init_tab_wheel(self):
        tab_wheel = QWidget()

        wheel_size = QDoubleSpinBox()
        wheel_size.setRange(100, 1000)
        wheel_size.setValue(float(self.settings.get_value('Wheel', 'size')))
        
        wheel_bg_color = QPushButton("Background Color")
        wheel_bg_color.clicked.connect(lambda: self.get_color('Wheel', 'bg_color'))
        wheel_bg_color.setHidden(True)

        wheel_fg_color = QPushButton("Text Color")
        wheel_fg_color.clicked.connect(lambda: self.get_color('Wheel', 'fg_color'))

        bg_type = self.settings.get_value('Wheel', 'bg_type')
        wheel_bg_type = QComboBox()
        wheel_bg_type.addItem('Solid')
        wheel_bg_type.addItem('Multicolor')
        wheel_bg_type.addItem('Image')
        wheel_bg_type.setCurrentText(bg_type)
        wheel_bg_type.activated.connect(lambda: self.wheel_bg_type_change())

        wheel_colors = self.settings.get_section('Wheel_Colors')
        wheel_bg_color_list = QListWidget()
        for i in range(len(wheel_colors)):
            wheel_bg_color_list.addItem('Color '+str(i))
        wheel_bg_color_list.setHidden(True)

        if bg_type == 'Solid':
            wheel_bg_color.setHidden(False)
        elif bg_type == 'Multicolor':
            wheel_bg_color_list.setHidden(False)
        else:
            pass
        
        self.options['Wheel'] = {
            'size': wheel_size,
            'fg_color': wheel_fg_color,
            #'bg_type': wheel_bg_type,
            'bg_color': wheel_bg_color,
            #'bg_color_list': wheel_bg_color_list
        }

        tab_wheel_layout = QVBoxLayout()
        tab_wheel.setLayout(tab_wheel_layout)
        for w in self.options['Wheel']:
            tab_wheel_layout.addWidget(self.options['Wheel'][w])

        return tab_wheel
    
    #handle dynamic settings for wheel bg type
    def wheel_bg_type_change(self):
        bg_type = self.options['Wheel']['bg_type'].currentText()
        self.settings.set_value('Wheel', 'bg_type', bg_type)

        if bg_type == 'Solid':
            self.options['Wheel']['bg_color'].setHidden(False)
            self.options['Wheel']['bg_color_list'].setHidden(True)
        elif bg_type == 'Multicolor':
            self.options['Wheel']['bg_color'].setHidden(True)
            self.options['Wheel']['bg_color_list'].setHidden(False)
        else:
            pass
