"""
Grady Landers
Demo Wheel - mainwindow.py
Code for the window that will be displayed at runtime and contain the titular Demo Wheel.
"""

#imports
import random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush, QPainter, QPen, QPolygonF, QAction
from PyQt6.QtCore import QPointF, QPropertyAnimation, QEasingCurve
from settingswindow import SettingsWindow
from demowheel import DemoWheel
from custombutton import CustomButton
from settings import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        #initialization
        super().__init__()
        self.settings = Settings()
        self.settings_window = SettingsWindow(self, self.settings)
        self.spinning = False

        #setting in toolbar
        toolbar = QToolBar('toolbar')
        self.addToolBar(toolbar)

        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(lambda: self.open_settings())
        toolbar.addAction(settings_action)

        #gui elements
        self.setWindowTitle("Funhaus Demo Wheel")
        btn_spin = QPushButton("SPIN")
        btn_spin.clicked.connect(lambda: self.spin())
        self.draw_scene()
        self.canvas_view = QGraphicsView(self.canvas)
        if self.settings.get_value('Background', 'type') == 'Image':
            self.canvas_view.setStyleSheet("border-image: url('"+self.settings.get_value('Background', 'image')+"') 0 0 0 0 stretch stretch")
        self.canvas_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.canvas_view.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.setCentralWidget(self.canvas_view)

    #opens the settings
    def open_settings(self):
        self.settings_window.show()
        self.settings_window.activateWindow()

    #spins the wheel
    def spin(self):
        self.toggle_spinning()
        diameter = float(self.settings.get_value('Wheel', 'size'))
        self.spin_anim.setDuration(2000)
        self.spin_anim.setEndValue(2*diameter+random.random()*360)
        self.spin_anim.start()

    #switches the status of spinning flag
    def toggle_spinning(self):
        self.spinning = not self.spinning
        self.button.toggle_hover_events()

    #signal that settings have been changed and a refresh is necessary
    def update_settings(self):
        self.draw_scene()
        self.canvas_view.setScene(self.canvas)
        if self.settings.get_value('Background', 'type') == 'Image':
            self.canvas_view.setStyleSheet("border-image: url('"+self.settings.get_value('Background', 'image')+"') 0 0 0 0 stretch stretch")
        else:
            self.canvas_view.setStyleSheet("border-image: none")

    #initiate the scene and add the custom components
    def draw_scene(self):
        self.canvas = QGraphicsScene()
        self.wheel = DemoWheel(0, 0, self.settings)
        self.canvas.addItem(self.wheel)
        self.button = CustomButton(self.settings, self.spin)
        self.canvas.addItem(self.button)
        self.canvas.addItem(self.draw_pointer())
        if self.settings.get_value('Background', 'type') == 'Solid':
            self.canvas.setBackgroundBrush(QBrush(self.settings.get_value('Background', 'color')))

        #animation
        self.spin_anim = QPropertyAnimation(self.wheel.adapter, b'rotation')
        self.spin_anim.setStartValue(0)
        self.spin_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.spin_anim.finished.connect(lambda: self.toggle_spinning())

    #create the pointer object
    def draw_pointer(self):
        radius = float(self.settings.get_value('Wheel', 'size')) / 2
        base = radius * 0.2
        color = self.settings.get_value('Wheel', 'fg_color')
        brush = QBrush(color)
        pen = QPen(color)
        pen.setWidth(2)
        
        pointer = QGraphicsPolygonItem(
            QPolygonF([
                QPointF(base*0.15, radius),
                QPointF(-base*0.85, radius-base/2),
                QPointF(-base*0.85, radius+base/2)
            ])
        )
        pointer.setBrush(brush)
        pointer.setPen(pen)

        return pointer
