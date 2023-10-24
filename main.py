"""
Grady Landers
Demo Wheel - main.py
Desktop app for facilitating the random selection process of the Funhaus Demo Wheel show.
This is the main file that initializes and runs the app.
"""

#imports
from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow
import qdarktheme
import sys

#start PyQt application
app = QApplication([])
qdarktheme.setup_theme()

#initialize the main window
mw = MainWindow()
mw.showMaximized()

#run the window and exit when done
sys.exit(app.exec())
