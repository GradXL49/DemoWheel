'''
Grady Landers
Demo Wheel - settingswindow.py
Code for the window that contains the settings for the main window.
'''

#imports
from PyQt6.QtWidgets import *
from settingwidget import SettingWidget

class SettingsWindow(QWidget):
    def __init__(self, mainwindow, settings):
        #initialization
        super().__init__()
        self.mainwindow = mainwindow
        self.settings = settings
        self.options = {}

        #gui elements
        self.setWindowTitle('Settings')
        self.setFixedSize(400, 450)
        tabs = QTabWidget()

        #Wheel tab
        tab_wheel = self.init_tab_wheel()
        tabs.addTab(tab_wheel, 'Wheel')

        #Text tab
        tab_text = self.init_tab_text()
        tabs.addTab(tab_text, 'Titles')

        #background tab
        tab_background = self.init_tab_bg()
        tabs.addTab(tab_background, 'Scene')

        #themes tab
        tab_theme = self.init_tab_theme()
        tabs.addTab(tab_theme, 'Themes')

        #layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(tabs)
    
    #when a control value is changed update the settings
    def change_value(self, category, option):
        value = self.options[category][option].get_value()
        if value is None:
            print('ERROR: Invalid value.')
        else:
            self.settings.set_value(category, option, value)
            self.settings.save_config()
            self.mainwindow.update_settings()
    
    #opens a color picker dialog for choosing colors
    def get_color(self, category, option):
        color = QColorDialog().getColor(self.settings.get_value(category, option))
        if color.isValid():
            self.settings.set_value(category, option, color)
            self.settings.save_config()
            self.mainwindow.update_settings()
            self.options[category][option].get_control().setStyleSheet('background-color: rgba'+str(color.getRgb()))
    
    #create the text tab
    def init_tab_text(self):
        tab_text = QWidget()

        text_size = SettingWidget('Text Size', float(self.settings.get_value('Text', 'font_size')))
        text_size.get_control().setRange(1, 100)
        text_size.get_control().valueChanged.connect(lambda: self.change_value('Text', 'font_size'))

        text_color = SettingWidget('Text Color', self.settings.get_value('Text', 'text_color'))
        text_color.get_control().clicked.connect(lambda: self.get_color('Text', 'text_color'))

        text_shadow = SettingWidget('Shadow', self.settings.get_value('Text', 'shadow_bool'))
        text_shadow.get_control().stateChanged.connect(lambda: self.change_value('Text', 'shadow_bool'))

        text_shadow_color = SettingWidget('Shadow Color', self.settings.get_value('Text', 'shadow_color'))
        text_shadow_color.get_control().clicked.connect(lambda: self.get_color('Text', 'shadow_color'))

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

        wheel_size = SettingWidget('Wheel Size', 0.0)
        wheel_size.get_control().setRange(100, 1000)
        wheel_size.get_control().setValue(float(self.settings.get_value('Wheel', 'size')))
        wheel_size.get_control().valueChanged.connect(lambda: self.change_value('Wheel', 'size'))
        
        wheel_bg_color = SettingWidget('Background Color', self.settings.get_value('Wheel', 'bg_color'))
        wheel_bg_color.get_control().clicked.connect(lambda: self.get_color('Wheel', 'bg_color'))
        wheel_bg_color.setHidden(True)

        wheel_fg_color = SettingWidget('Line Color', self.settings.get_value('Wheel', 'fg_color'))
        wheel_fg_color.get_control().clicked.connect(lambda: self.get_color('Wheel', 'fg_color'))
        wheel_fg_color.setHidden(True)

        bg_type = self.settings.get_value('Wheel', 'bg_type')
        wheel_bg_type = SettingWidget('Background Type', bg_type)
        wheel_bg_type.get_control().addItem('Solid')
        wheel_bg_type.get_control().addItem('Multicolor')
        wheel_bg_type.get_control().setCurrentText(bg_type)
        wheel_bg_type.get_control().activated.connect(lambda: self.wheel_bg_type_change())

        wheel_colors_container = QWidget()
        wheel_colors_container.setHidden(True)

        label_colors = QLabel('Colors:')

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
        wheel_colors_layout.addWidget(label_colors, 0, 0)
        wheel_colors_layout.addWidget(self.wheel_bg_color_list, 1, 0, 4, 1)
        wheel_colors_layout.addWidget(wheel_colors_add, 1, 1)
        wheel_colors_layout.addWidget(wheel_colors_remove, 2, 1)
        wheel_colors_layout.addWidget(wheel_colors_up, 3, 1)
        wheel_colors_layout.addWidget(wheel_colors_down, 4, 1)

        if bg_type == 'Solid':
            wheel_bg_color.setHidden(False)
            wheel_fg_color.setHidden(False)
        elif bg_type == 'Multicolor':
            wheel_colors_container.setHidden(False)
        
        self.options['Wheel'] = {
            'size': wheel_size,
            'bg_type': wheel_bg_type,
            'bg_color': wheel_bg_color,
            'fg_color': wheel_fg_color,
            'bg_color_list': wheel_colors_container
        }

        tab_wheel_layout = QVBoxLayout()
        tab_wheel.setLayout(tab_wheel_layout)
        for w in self.options['Wheel']:
            tab_wheel_layout.addWidget(self.options['Wheel'][w])

        return tab_wheel
    
    #handle dynamic settings for wheel bg type
    def wheel_bg_type_change(self):
        bg_type = self.options['Wheel']['bg_type'].get_control().currentText()
        self.settings.set_value('Wheel', 'bg_type', bg_type)

        if bg_type == 'Solid':
            self.options['Wheel']['bg_color'].setHidden(False)
            self.options['Wheel']['fg_color'].setHidden(False)
            self.options['Wheel']['bg_color_list'].setHidden(True)
        elif bg_type == 'Multicolor':
            self.options['Wheel']['bg_color'].setHidden(True)
            self.options['Wheel']['fg_color'].setHidden(True)
            self.options['Wheel']['bg_color_list'].setHidden(False)
        
        self.settings.save_config()
        self.mainwindow.update_settings()
    
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
        bg_type = SettingWidget('Background Type', current_bg_type)
        bg_type.get_control().addItem('Solid')
        bg_type.get_control().addItem('Image')
        bg_type.get_control().setCurrentText(current_bg_type)
        bg_type.get_control().activated.connect(lambda: self.bg_type_change())

        bg_color = SettingWidget('Background Color', self.settings.get_value('Background', 'color'))
        bg_color.get_control().clicked.connect(lambda: self.get_color('Background', 'color'))
        bg_color.setHidden(True)

        bg_image = SettingWidget('Background Image', 'FILEPATH')
        bg_image.get_control().clicked.connect(lambda: self.get_image())
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

        button_color = SettingWidget('Button Color', self.settings.get_value('Button', 'bg_color'))
        button_color.get_control().clicked.connect(lambda: self.get_color('Button', 'bg_color'))

        button_text = SettingWidget('Button Text Color', self.settings.get_value('Button', 'fg_color'))
        button_text.get_control().clicked.connect(lambda: self.get_color('Button', 'fg_color'))

        button_hover_color = SettingWidget('Hover Color', self.settings.get_value('Button', 'bg_hover_color'))
        button_hover_color.get_control().clicked.connect(lambda: self.get_color('Button', 'bg_hover_color'))

        button_hover_text = SettingWidget('Hover Text Color', self.settings.get_value('Button', 'fg_hover_color'))
        button_hover_text.get_control().clicked.connect(lambda: self.get_color('Button', 'fg_hover_color'))

        button_disable_color = SettingWidget('Disabled Color', self.settings.get_value('Button', 'bg_disable_color'))
        button_disable_color.get_control().clicked.connect(lambda: self.get_color('Button', 'bg_disable_color'))

        button_disable_text = SettingWidget('Disabled Text Color', self.settings.get_value('Button', 'fg_disable_color'))
        button_disable_text.get_control().clicked.connect(lambda: self.get_color('Button', 'fg_disable_color'))

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
        current = self.options['Background']['type'].get_control().currentText()
        self.settings.set_value('Background', 'type', current)

        if current == 'Solid':
            self.options['Background']['color'].setHidden(False)
            self.options['Background']['image'].setHidden(True)
        elif current == 'Image':
            self.options['Background']['image'].setHidden(False)
            self.options['Background']['color'].setHidden(True)
        
        self.settings.save_config()
        self.mainwindow.update_settings()
    
    #find an image to use as the background
    def get_image(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setDirectory(self.settings.get_value('Background', 'image'))
        if dialog.exec():
            image = dialog.selectedFiles()
            self.settings.set_value('Background', 'image', image[0])
            self.settings.save_config()
            self.mainwindow.update_settings()
    
    #create the themes tab
    def init_tab_theme(self):
        tab_theme = QWidget()

        self.themes = self.settings.get_theme_list()
        self.themes_list = QListWidget()
        self.themes_list.addItems(self.themes)
        
        themes_add = QPushButton('Save New')
        themes_add.clicked.connect(lambda: self.add_theme())

        themes_apply = QPushButton('Apply')
        themes_apply.clicked.connect(lambda: self.apply_theme())

        themes_rename = QPushButton('Rename')
        themes_rename.clicked.connect(lambda: self.rename_theme())

        themes_duplicate = QPushButton('Duplicate')
        themes_duplicate.clicked.connect(lambda: self.duplicate_theme())

        themes_delete = QPushButton('Delete')
        themes_delete.clicked.connect(lambda: self.delete_theme())

        tab_theme_layout = QGridLayout()
        tab_theme.setLayout(tab_theme_layout)
        tab_theme_layout.addWidget(self.themes_list, 0, 0, 5, 1)
        tab_theme_layout.addWidget(themes_add, 0, 1)
        tab_theme_layout.addWidget(themes_apply, 1, 1)
        tab_theme_layout.addWidget(themes_rename, 2, 1)
        tab_theme_layout.addWidget(themes_duplicate, 3, 1)
        tab_theme_layout.addWidget(themes_delete, 4, 1)

        return tab_theme
    
    #check the given title to make sure it's acceptable
    def check_title(self, title):
        valid = True

        if title == '' or not title.replace(' ', '').isalnum():
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Invalid Theme Name')
            dlg.setText("Theme names can't be empty and must not contain special characters.")
            dlg.exec()
            valid = False
        else:
            for theme in self.themes:
                if title.lower() == theme.lower():
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle('Theme Name Taken')
                    dlg.setText('The name entered is already in use. Theme names must be unique.')
                    valid = False
                    dlg.exec()
        
        return valid
    
    #add the current theme
    def add_theme(self):
        title, ok = QInputDialog.getText(self, 'Name Your Theme', 'Title:')
        if ok and self.check_title(title):
            self.settings.save_theme(title)
            self.themes.append(title)
            self.themes_list_update()

    #apply selected theme
    def apply_theme(self):
        current_row = self.themes_list.currentRow()
        if current_row >= 0:
            self.settings.apply_theme(current_row)
            self.mainwindow.update_settings()
            self.reload()
    
    #rename selected theme
    def rename_theme(self):
        current_row = self.themes_list.currentRow()
        if current_row >= 0:
            title, ok = QInputDialog.getText(self, 'Name Your Theme', 'Title:')
            if ok and self.check_title(title):
                self.settings.rename_theme(current_row, title)
                self.themes[current_row] = title
                self.themes_list_update()
    
    #duplicate selected theme
    def duplicate_theme(self):
        current_row = self.themes_list.currentRow()
        if current_row >= 0:
            self.settings.duplicate_theme(current_row)
            self.themes.append(self.themes[current_row]+' Copy')
            self.themes_list_update()
    
    #delete selected theme
    def delete_theme(self):
        current_row = self.themes_list.currentRow()
        if current_row >= 0:
            self.settings.delete_theme(current_row)
            self.themes.remove(self.themes[current_row])
            self.themes_list_update()
    
    #update list of themes
    def themes_list_update(self):
        self.themes_list.clear()
        self.themes_list.addItems(self.themes)
    
    #reload to get latest settings values
    def reload(self):
        self.options = {}

        tabs = QTabWidget()

        #Wheel tab
        tab_wheel = self.init_tab_wheel()
        tabs.addTab(tab_wheel, 'Wheel')

        #Text tab
        tab_text = self.init_tab_text()
        tabs.addTab(tab_text, 'Titles')

        #background tab
        tab_background = self.init_tab_bg()
        tabs.addTab(tab_background, 'Scene')

        #themes tab
        tab_theme = self.init_tab_theme()
        tabs.addTab(tab_theme, 'Themes')

        #layout
        layout = self.layout()
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
        layout.addWidget(tabs)
