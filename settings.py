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
    def __init__(self, mainwindow):
        self.config = configparser.ConfigParser()
        self.mainwindow = mainwindow
        #if the file doesn't exist, create it first
        if not os.path.isfile('settings.ini'):
            self.config['Wheel'] = {
                'size': 500,
                'bg_color': '255,100,0',
                'fg_color': '0,0,0'
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
            return QColor(int(color[0]), int(color[1]), int(color[2]))
        return value
    
    def set_value(self, section, setting, value):
        if isinstance(value, QColor):
            value = value.getRgb()
            print(value)
        self.config[section][setting] = value
        self.mainwindow.update_settings()
