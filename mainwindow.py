"""
Grady Landers
Demo Wheel - mainwindow.py
Code for the window that will be displayed at runtime and contain the titular Demo Wheel.
"""

#imports
import random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush, QPainter, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, QEasingCurve
from settingswindow import SettingsWindow
from demowheel import DemoWheel
from settings import Settings

class MainWindow(QWidget):
    def __init__(self):
        #initialization
        super().__init__()
        self.settings = Settings(self)
        self.settings_window = SettingsWindow()
        self.titles = [
            "Tony Hawk Pro Skater 2",
            "Star Wars: The Force Unleashed",
            "Borderlands",
            "Toe Jam and Earl",
            "Serious Sam",
            "PC Building Simulator",
            "Avatar",
            "Brothers in Arms",
            "LOTR Online",
            "Mario Kart"
        ]
        self.spinning = False

        #gui elements
        self.setWindowTitle("Funhaus Demo Wheel")
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(lambda: self.open_settings())
        btn_spin = QPushButton("SPIN")
        btn_spin.clicked.connect(lambda: self.spin())
        self.canvas = QGraphicsScene()
        self.wheel = DemoWheel(0, 0, self.titles, self.settings)
        self.canvas.addItem(self.wheel)
        self.canvas_view = QGraphicsView(self.canvas)
        self.canvas_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(btn_settings, 0, 0)
        layout.addWidget(self.canvas_view, 1, 0)
        layout.addWidget(btn_spin, 2, 0)

        #animation
        self.spin_anim = QPropertyAnimation(self.wheel.adapter, b'rotation')
        self.spin_anim.setDuration(1500)
        self.spin_anim.setStartValue(0)
        self.spin_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.spin_anim.finished.connect(lambda: self.toggle_spinning())

    #opens the settings
    def open_settings(self):
        self.settings_window.show()

    #spins the wheel
    def spin(self):
        self.toggle_spinning()
        self.spin_anim.setEndValue(900+random.random()*360)
        self.spin_anim.start()

    def toggle_spinning(self):
        self.spinning = not self.spinning

    def update_settings(self):
        self.wheel = DemoWheel(0, 0, self.titles, self.settings)
