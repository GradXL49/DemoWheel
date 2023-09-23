"""
Grady Landers
Demo Wheel - settingswindow.py
Code for the window that contains the settings for the main window.
"""

#imports
from PyQt6.QtWidgets import *

class SettingsWindow(QWidget):
    def __init__(self):
        #initialization
        super().__init__()

        #gui elements
        self.setWindowTitle("Settings")
