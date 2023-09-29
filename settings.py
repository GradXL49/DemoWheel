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
                'bg_type': 'Solid',
                'bg_color_0': '255,0,0,255',
                'bg_color_1': '0,255,0,255',
                'bg_color_2': '0,0,255,255'
            }
            self.save_config()
        
        #read the settings file and hold the configuration
        self.config.read('settings.ini')

    #save the current configuration to the settings file
    def save_config(self):
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
    
    def get_value(self, section, setting):
        value = self.config[section][setting]
        if 'color' in setting:
            color = value.split(',')
            return QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
        return value
    
    def set_value(self, section, setting, value):
        if isinstance(value, QColor):
            value = str(value.getRgb()).replace('(', '').replace(')', '').replace(' ', '')
        self.config[section][setting] = str(value)
