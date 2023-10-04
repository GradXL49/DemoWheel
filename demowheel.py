"""
Grady Landers
Demo Wheel - demowheel.py
Custom class for the DemoWheel object. Enables the entire group to be animated.
Made with assistance from https://engineersjourney.wordpress.com/2012/09/05/pyqt-and-animating-qgraphicsitem-objects/
"""

#imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush, QPen, QPolygonF, QFont
from PyQt6.QtCore import QPointF, QObject, pyqtProperty
import math

#DemoWheel class
class DemoWheel(QGraphicsItem):
    def __init__(self, xc, yc, settings):
        super(DemoWheel, self).__init__()
        self.xc = xc
        self.yc = yc
        self.settings = settings
        diameter = float(settings.get_value('Wheel', 'size'))
        radius = diameter / 2
        self.setPos(xc+radius, yc+radius)
        self.adapter = DemoWheelAdapter(self, self)

        wheel = QGraphicsEllipseItem(xc-radius, yc-radius, diameter, diameter, self)

        brush = QBrush(settings.get_value('Wheel', 'bg_color'))
        wheel.setBrush(brush)

        pen = QPen(settings.get_value('Wheel', 'fg_color'))
        pen.setWidth(2)
        wheel.setPen(pen)

        self.font = QFont()
        self.font.setPointSize(int(settings.get_value('Text', 'font_size')))
        titles = settings.get_section_list('Titles')
        l = len(titles)
        for i in range(l):
            x = radius * math.cos(2*math.pi*i/l) + xc
            y = radius * math.sin(2*math.pi*i/l) + yc
            line = QGraphicsPolygonItem(QPolygonF([QPointF(xc, yc),QPointF(x, y)]), self)
            line.setPen(pen)
            if i == 0:
                xy1 = [x,y]
                xy = [x,y]
            else:
                self.draw_title(titles[i], x, y, xy[0], xy[1])
                xy = [x,y]
        self.draw_title(titles[0], xy[0], xy[1], xy1[0], xy1[1])

    def draw_title(self, text, x1, y1, x2, y2):
        tx = (x1+x2)/2
        ty = (y1+y2)/2
        
        theta = math.atan((y2-y1)/(x2-x1))
        offset = self.font.pointSize()*16/12 #convert point size to pixels
        if ty > self.yc:
            offset = -offset
        off_x = offset * math.cos(theta)
        off_y = offset * math.sin(theta)

        title = QGraphicsTextItem(text, self)
        title.setPos(tx+off_x, ty+off_y)
        angle = calc_clockwise_angle(tx, ty, self.xc, self.yc)
        title.setRotation(angle)
        title.setFont(self.font)
        title.setDefaultTextColor(self.settings.get_value('Text', 'text_color'))
        title.setZValue(1)

        if self.settings.get_value('Text', 'shadow_bool'):
            offset = offset * 0.9
            off_x = offset * math.cos(theta)
            off_y = offset * math.sin(theta)

            shadow = QGraphicsTextItem(text, self)
            shadow.setPos(tx+off_x, ty+off_y)
            shadow.setRotation(angle)
            shadow.setFont(self.font)
            shadow.setDefaultTextColor(self.settings.get_value('Text', 'shadow_color'))

#adapter class to fascilitate animation
class DemoWheelAdapter(QObject):
    def __init__(self, parent, object_to_animate):
        super(DemoWheelAdapter, self).__init__()
        self.object_to_animate = object_to_animate
    
    def __get_rotation(self):
        return self.object_to_animate.rotation()
    
    def __set_rotation(self, angle):
        self.object_to_animate.setRotation(angle)
    
    rotation = pyqtProperty(float, __get_rotation, __set_rotation)

#utility for figuring out the rotaion of a title
def calc_clockwise_angle(x, y, xc, yc):
    delta = math.sqrt(math.pow(xc-x,2)+math.pow(yc-y,2))
    if x < xc:
        xd = xc - x
        theta = math.degrees(math.acos(xd/delta))
        if y > yc:
            theta = 360 - theta
    else:
        xd = x - xc
        theta = math.degrees(math.acos(xd/delta))
        if y < yc:
            theta = 180 - theta
        else:
            theta = theta + 180
    
    return theta
