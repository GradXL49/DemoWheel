"""
Grady Landers
Demo Wheel - settings.py
Class to contain and verify all of the user settings.
"""

#imports
import configparser
import os
from PyQt6.QtGui import QColor

class Settings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        #if the file doesn't exist, create it first with defaults
        if not os.path.isfile('settings.ini'):
            self.config['Wheel'] = {
                'size': '800',
                'bg_color': '255,100,0,255',
                'fg_color': '0,0,0,255',
                'bg_type': 'Solid'
            }
            self.config['Wheel_Colors'] = {
                'bg_color_0': '255,0,0,255',
                'bg_color_1': '0,255,0,255',
                'bg_color_2': '0,0,255,255'
            }
            self.config['Text'] = {
                'font_size': '15',
                'text_color': '0,0,0,255',
                'shadow_bool': 'False',
                'shadow_color': '255,255,255,255'
            }
            self.config['Titles'] = {
                'title_0': "Tony Hawk Pro Skater 2",
                'title_1': "Star Wars: The Force Unleashed",
                'title_2': "Borderlands",
                'title_3': "Toe Jam and Earl",
                'title_4': "Serious Sam",
                'title_5': "PC Building Simulator",
                'title_6': "Avatar",
                'title_7': "Brothers in Arms",
                'title_8': "LOTR Online",
                'title_9': "Mario Kart"
            }
            self.config['Background'] = {
                'type': 'Image',
                'color': '60,60,60,255',
                'image': 'images/wave.jpg'
            }
            self.save_config()
        
        #read the settings file and hold the configuration
        self.config.read('settings.ini')

    #save the current configuration to the settings file
    def save_config(self):
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
    
    #retrieve the requested setting value
    def get_value(self, section, setting):
        value = self.config[section][setting]
        if 'color' in setting:
            color = value.split(',')
            value = QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
        elif 'bool' in setting:
            if value.lower() == 'true':
                value = True
            else:
                value = False
        return value
    
    #retrieve the requested section tuple
    def get_section(self, section):
        return self.config[section]
    
    #retrieve the requested section as a list of its values
    def get_section_list(self, section):
        values = []
        for setting in self.config[section]:
            values.append(self.get_value(section, setting))
        return values
    
    #set the specified setting to the given value
    def set_value(self, section, setting, value):
        if isinstance(value, QColor):
            value = str(value.getRgb()).replace('(', '').replace(')', '').replace(' ', '')
        self.config[section][setting] = str(value)

    #reset the settings of the specified section with the given list of values
    def set_section_list(self, section, setting, values):
        self.config[section] = {}
        for i in range(len(values)):
            self.set_value(section, setting+str(i), values[i])
