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

        #Text tab
        tab_text = self.init_tab_text()
        tabs.addTab(tab_text, "Text")

        #layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(tabs, 0, 0)
        layout.addWidget(btn_submit, 1, 0)

    #action for APPLY button
    def submit(self):
        for category in self.options:
            for option in self.options[category]:
                if 'bool' in option:
                    self.settings.set_value(category, option, self.options[category][option].isChecked())
                elif 'color' not in option and 'type' not in option and 'list' not in option:
                    self.settings.set_value(category, option, self.options[category][option].value())
        
        self.settings.save_config()
        self.mainwindow.update_settings()
    
    #opens a color picker dialog for choosing colors
    def get_color(self, category, option):
        color = QColorDialog().getColor(self.settings.get_value(category, option))
        self.settings.set_value(category, option, color)
        self.settings.save_config()
        self.mainwindow.update_settings()
    
    #create the text tab
    def init_tab_text(self):
        tab_text = QWidget()

        text_size = QSpinBox()
        text_size.setRange(1, 100)
        text_size.setValue(float(self.settings.get_value('Text', 'font_size')))

        text_color = QPushButton("Text Color")
        text_color.clicked.connect(lambda: self.get_color('Text', 'text_color'))

        text_shadow = QCheckBox("Shadow")
        text_shadow.setChecked(self.settings.get_value('Text', 'shadow_bool'))

        text_shadow_color = QPushButton("Shadow Color")
        text_shadow_color.clicked.connect(lambda: self.get_color('Text', 'shadow_color'))

        self.options['Text'] = {
            'font_size': text_size,
            'text_color': text_color,
            'shadow_bool': text_shadow,
            'shadow_color': text_shadow_color
        }

        text_titles_container = QWidget()

        self.text_titles = self.settings.get_section_list('Titles')
        self.text_titles_list = QListWidget()
        self.text_titles_list.addItems(self.text_titles)
        
        text_titles_add = QPushButton('Add')
        text_titles_add.clicked.connect(lambda: self.add_title())

        text_titles_remove = QPushButton('Remove')
        text_titles_remove.clicked.connect(lambda: self.remove_title())

        text_titles_up = QPushButton('Up')
        text_titles_up.clicked.connect(lambda: self.move_title_up())

        text_titles_down = QPushButton('Down')
        text_titles_down.clicked.connect(lambda: self.move_title_down())

        text_titles_layout = QGridLayout()
        text_titles_container.setLayout(text_titles_layout)
        text_titles_layout.addWidget(self.text_titles_list, 0, 0, 4, 1)
        text_titles_layout.addWidget(text_titles_add, 0, 1)
        text_titles_layout.addWidget(text_titles_remove, 1, 1)
        text_titles_layout.addWidget(text_titles_up, 2, 1)
        text_titles_layout.addWidget(text_titles_down, 3, 1)

        tab_text_layout = QVBoxLayout()
        tab_text.setLayout(tab_text_layout)
        for w in self.options['Text']:
            tab_text_layout.addWidget(self.options['Text'][w])
        tab_text_layout.addWidget(text_titles_container)

        return tab_text
    
    #add a title to the list
    def add_title(self):
        text, ok = QInputDialog.getText(self, 'Add A Title', 'Title:')
        if ok and text:
            self.text_titles.append(text)
            self.title_list_update()

    #remove selected title from the list
    def remove_title(self):
        current_row = self.text_titles_list.currentRow()
        if current_row >= 0:
            self.text_titles.remove(self.text_titles[current_row])
            self.title_list_update()
    
    #move title up in the list
    def move_title_up(self):
        current_row = self.text_titles_list.currentRow()
        if current_row > 0:
            temp = self.text_titles[current_row]
            self.text_titles[current_row] = self.text_titles[current_row-1]
            self.text_titles[current_row-1] = temp
            self.title_list_update()
            self.text_titles_list.setCurrentRow(current_row-1)
    
    #move title down in list
    def move_title_down(self):
        current_row = self.text_titles_list.currentRow()
        if current_row >= 0 and current_row < len(self.text_titles)-1:
            temp = self.text_titles[current_row]
            self.text_titles[current_row] = self.text_titles[current_row+1]
            self.text_titles[current_row+1] = temp
            self.title_list_update()
            self.text_titles_list.setCurrentRow(current_row+1)
    
    #update the list and the settings on title list change
    def title_list_update(self):
        self.text_titles_list.clear()
        self.text_titles_list.addItems(self.text_titles)
        self.settings.set_section_list('Titles', 'title', self.text_titles)
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

        wheel_fg_color = QPushButton("Line Color")
        wheel_fg_color.clicked.connect(lambda: self.get_color('Wheel', 'fg_color'))

        bg_type = self.settings.get_value('Wheel', 'bg_type')
        wheel_bg_type = QComboBox()
        wheel_bg_type.addItem('Solid')
        wheel_bg_type.addItem('Multicolor')
        wheel_bg_type.addItem('Image')
        wheel_bg_type.setCurrentText(bg_type)
        wheel_bg_type.activated.connect(lambda: self.wheel_bg_type_change())

        '''UNDER CONSTRUCTION'''
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
        '''****************'''
        
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
