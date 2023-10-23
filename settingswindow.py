'''
Grady Landers
Demo Wheel - settingswindow.py
Code for the window that contains the settings for the main window.
'''

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
        self.setWindowTitle('Settings')
        self.setFixedSize(400, 400)
        tabs = QTabWidget()
        #tabs.setTabPosition(QTabWidget.TabPosition.West)
        btn_submit = QPushButton('Apply')
        btn_submit.clicked.connect(lambda: self.submit())

        #Wheel tab
        tab_wheel = self.init_tab_wheel()
        tabs.addTab(tab_wheel, 'Wheel')

        #Text tab
        tab_text = self.init_tab_text()
        tabs.addTab(tab_text, 'Text')

        #background tab
        tab_background = self.init_tab_bg()
        tabs.addTab(tab_background, 'Scene')

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
                elif 'color' not in option and 'type' not in option and 'list' not in option and 'image' not in option:
                    self.settings.set_value(category, option, self.options[category][option].value())
        
        self.settings.save_config()
        self.mainwindow.update_settings()
    
    #opens a color picker dialog for choosing colors
    def get_color(self, category, option):
        color = QColorDialog().getColor(self.settings.get_value(category, option))
        if color.isValid():
            self.settings.set_value(category, option, color)
            self.settings.save_config()
            self.mainwindow.update_settings()
    
    #create the text tab
    def init_tab_text(self):
        tab_text = QWidget()

        text_size = QSpinBox()
        text_size.setRange(1, 100)
        text_size.setValue(float(self.settings.get_value('Text', 'font_size')))

        text_color = QPushButton('Text Color')
        text_color.clicked.connect(lambda: self.get_color('Text', 'text_color'))

        text_shadow = QCheckBox('Shadow')
        text_shadow.setChecked(self.settings.get_value('Text', 'shadow_bool'))

        text_shadow_color = QPushButton('Shadow Color')
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
        if current_row >= 0 and len(self.text_titles) > 1:
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
        
        wheel_bg_color = QPushButton('Background Color')
        wheel_bg_color.clicked.connect(lambda: self.get_color('Wheel', 'bg_color'))
        wheel_bg_color.setHidden(True)

        wheel_fg_color = QPushButton('Line Color')
        wheel_fg_color.clicked.connect(lambda: self.get_color('Wheel', 'fg_color'))

        bg_type = self.settings.get_value('Wheel', 'bg_type')
        wheel_bg_type = QComboBox()
        wheel_bg_type.addItem('Solid')
        wheel_bg_type.addItem('Multicolor')
        #wheel_bg_type.addItem('Image')
        wheel_bg_type.setCurrentText(bg_type)
        wheel_bg_type.activated.connect(lambda: self.wheel_bg_type_change())

        wheel_colors_container = QWidget()
        wheel_colors_container.setHidden(True)

        self.wheel_colors = self.settings.get_section_list('Wheel_Colors')
        self.wheel_bg_color_list = QListWidget()
        i = 0
        for c in self.wheel_colors:
            self.wheel_bg_color_list.addItem('Color '+str(i)+': '+str(c.getRgb()))
            i += 1
        
        wheel_colors_add = QPushButton('Add')
        wheel_colors_add.clicked.connect(lambda: self.add_color())

        wheel_colors_remove = QPushButton('Remove')
        wheel_colors_remove.clicked.connect(lambda: self.remove_color())

        wheel_colors_up = QPushButton('Up')
        wheel_colors_up.clicked.connect(lambda: self.move_color_up())

        wheel_colors_down = QPushButton('Down')
        wheel_colors_down.clicked.connect(lambda: self.move_color_down())

        wheel_colors_layout = QGridLayout()
        wheel_colors_container.setLayout(wheel_colors_layout)
        wheel_colors_layout.addWidget(self.wheel_bg_color_list, 0, 0, 4, 1)
        wheel_colors_layout.addWidget(wheel_colors_add, 0, 1)
        wheel_colors_layout.addWidget(wheel_colors_remove, 1, 1)
        wheel_colors_layout.addWidget(wheel_colors_up, 2, 1)
        wheel_colors_layout.addWidget(wheel_colors_down, 3, 1)

        if bg_type == 'Solid':
            wheel_bg_color.setHidden(False)
        elif bg_type == 'Multicolor':
            wheel_colors_container.setHidden(False)
        
        self.options['Wheel'] = {
            'size': wheel_size,
            'fg_color': wheel_fg_color,
            'bg_type': wheel_bg_type,
            'bg_color': wheel_bg_color,
            'bg_color_list': wheel_colors_container
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
    
    #add a wheel color for the multicolor background
    def add_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.wheel_colors.append(color)
            self.wheel_colors_update()
    
    #remove selected wheel color from the list
    def remove_color(self):
        current_row = self.wheel_bg_color_list.currentRow()
        if current_row >= 0 and len(self.wheel_colors) > 1:
            self.wheel_colors.remove(self.wheel_colors[current_row])
            self.wheel_colors_update()
    
    #move selected wheel color up in the list
    def move_color_up(self):
        current_row = self.wheel_bg_color_list.currentRow()
        if current_row > 0:
            temp = self.wheel_colors[current_row]
            self.wheel_colors[current_row] = self.wheel_colors[current_row-1]
            self.wheel_colors[current_row-1] = temp
            self.wheel_colors_update()
            self.wheel_bg_color_list.setCurrentRow(current_row-1)

    #move selected wheel color down in the list
    def move_color_down(self):
        current_row = self.wheel_bg_color_list.currentRow()
        if current_row >= 0 and current_row < len(self.wheel_colors)-1:
            temp = self.wheel_colors[current_row]
            self.wheel_colors[current_row] = self.wheel_colors[current_row+1]
            self.wheel_colors[current_row+1] = temp
            self.wheel_colors_update()
            self.wheel_bg_color_list.setCurrentRow(current_row+1)
    
    #update the list and the settings on color list change
    def wheel_colors_update(self):
        self.wheel_bg_color_list.clear()
        i = 0
        for c in self.wheel_colors:
            self.wheel_bg_color_list.addItem('Color '+str(i)+': '+str(c.getRgb()))
            i += 1
        self.settings.set_section_list('Wheel_Colors', 'color', self.wheel_colors)
        self.settings.save_config()
        self.mainwindow.update_settings()

    #create the background tab
    def init_tab_bg(self):
        tab_bg = QWidget()

        current_bg_type = self.settings.get_value('Background', 'type')
        bg_type = QComboBox()
        bg_type.addItem('Solid')
        bg_type.addItem('Image')
        bg_type.setCurrentText(current_bg_type)
        bg_type.activated.connect(lambda: self.bg_type_change())

        bg_color = QPushButton('Background Color')
        bg_color.clicked.connect(lambda: self.get_color('Background', 'color'))
        bg_color.setHidden(True)

        bg_image = QPushButton('Background Image')
        bg_image.setHidden(True)

        if current_bg_type == 'Solid':
            bg_color.setHidden(False)
        elif current_bg_type == 'Image':
            bg_image.setHidden(False)

        self.options['Background'] = {
            'type': bg_type,
            'color': bg_color,
            'image': bg_image
        }

        button_color = QPushButton('Button Color')
        button_color.clicked.connect(lambda: self.get_color('Button', 'bg_color'))

        button_text = QPushButton('Button Text')
        button_text.clicked.connect(lambda: self.get_color('Button', 'fg_color'))

        button_hover_color = QPushButton('Hover Color')
        button_hover_color.clicked.connect(lambda: self.get_color('Button', 'bg_hover_color'))

        button_hover_text = QPushButton('Hover Text')
        button_hover_text.clicked.connect(lambda: self.get_color('Button', 'fg_hover_color'))

        button_disable_color = QPushButton('Disabled Color')
        button_disable_color.clicked.connect(lambda: self.get_color('Button', 'bg_disable_color'))

        button_disable_text = QPushButton('Disabled Text')
        button_disable_text.clicked.connect(lambda: self.get_color('Button', 'fg_disable_color'))

        self.options['Button'] = {
            'bg_color': button_color,
            'fg_color': button_text,
            'bg_hover_color': button_hover_color,
            'fg_hover_color': button_hover_text,
            'bg_disable_color': button_disable_color,
            'fg_disable_color': button_disable_text
        }

        tab_bg_layout = QVBoxLayout()
        tab_bg.setLayout(tab_bg_layout)
        for w in self.options['Background']:
            tab_bg_layout.addWidget(self.options['Background'][w])
        for w in self.options['Button']:
            tab_bg_layout.addWidget(self.options['Button'][w])
        
        return tab_bg
    
    #handle change of background type
    def bg_type_change(self):
        current = self.options['Background']['type'].currentText()
        self.settings.set_value('Background', 'type', current)

        if current == 'Solid':
            self.options['Background']['color'].setHidden(False)
            self.options['Background']['image'].setHidden(True)
        elif current == 'Image':
            self.options['Background']['image'].setHidden(False)
            self.options['Background']['color'].setHidden(True)
