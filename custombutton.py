"""
Grady Landers
Demo Wheel - custombutton.py
Custom class for a unique button object. Enables the object to listen for a click event on it.
"""

from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QPen, QFont

class CustomButton(QGraphicsRectItem):
    def __init__(self, settings, onclick, parent=None):
        #give the button the passed function as its click action
        self.onclick = onclick
        
        #initialize colors and other required information, create rect position below and centered on the wheel given the current settings
        radius = float(settings.get_value('Wheel', 'size')) / 2
        height = radius * 0.2
        rect = QRectF(radius-height, radius*2+25, height*2, height)
        self.normal_brush = QBrush(settings.get_value('Button', 'bg_color'))
        self.normal_pen = QPen(settings.get_value('Button', 'fg_color'))
        self.normal_pen.setWidth(2)
        self.hover_brush = QBrush(settings.get_value('Button', 'bg_hover_color'))
        self.hover_pen = QPen(settings.get_value('Button', 'fg_hover_color'))
        self.hover_pen.setWidth(2)
        self.disable_brush = QBrush(settings.get_value('Button', 'bg_disable_color'))
        self.disable_pen = QPen(settings.get_value('Button', 'fg_disable_color'))
        self.disable_pen.setWidth(2)
        
        #initialize the object
        super(CustomButton, self).__init__(rect, parent)
        self.setBrush(self.normal_brush)
        self.setPen(self.normal_pen)

        #allow the object to listen for various mouse events
        self.setAcceptHoverEvents(True)

        #create and place the text centered on the button
        font = QFont()
        font.setPixelSize(int(height/2))
        self.text = QGraphicsTextItem('SPIN', self)
        self.text.setFont(font)
        self.text.setPos(radius-self.text.boundingRect().width()/2, radius*2+25+height/2-self.text.boundingRect().height()/2)
        self.text.setDefaultTextColor(self.normal_pen.color())

    #override to perform the passed onclick action, then return to normal color
    def mousePressEvent(self, event):
        if self.brush() == self.hover_brush:
            self.onclick()
    
    #override to change color when mouse enters
    def hoverEnterEvent(self, event):
        self.setBrush(self.hover_brush)
        self.setPen(self.hover_pen)
        self.text.setDefaultTextColor(self.hover_pen.color())

    #override to return to original color when mouse leaves
    def hoverLeaveEvent(self, event):
        self.set_normal()
    
    #simply set the color scheme to normal
    def set_normal(self):
        self.setBrush(self.normal_brush)
        self.setPen(self.normal_pen)
        self.text.setDefaultTextColor(self.normal_pen.color())
    
    #simply set the color scheme to disabled
    def set_disabled(self):
        self.setBrush(self.disable_brush)
        self.setPen(self.disable_pen)
        self.text.setDefaultTextColor(self.disable_pen.color())
    
    #toggle allowing hover and being disabled
    def toggle_hover_events(self):
        state = self.acceptHoverEvents()
        if state:
            self.setAcceptHoverEvents(False)
            self.set_disabled()
        else:
            self.setAcceptHoverEvents(True)
            self.set_normal()
