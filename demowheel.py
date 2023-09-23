"""
Grady Landers
Demo Wheel - demowheel.py
Custom class for the DemoWheel object. Enables the entire group to be animated.
Made with assistance from https://engineersjourney.wordpress.com/2012/09/05/pyqt-and-animating-qgraphicsitem-objects/
"""

#imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF, QObject, pyqtProperty
import math

#DemoWheel class
class DemoWheel(QGraphicsItem):
    def __init__(self, x, y, diameter, titles):
        super(DemoWheel, self).__init__()
        radius = diameter / 2
        xc = x + radius
        yc = y + radius
        self.setPos(xc, yc)
        self.adapter = DemoWheelAdapter(self, self)

        wheel = QGraphicsEllipseItem(x, y, diameter, diameter, self)

        brush = QBrush(Qt.GlobalColor.blue)
        wheel.setBrush(brush)

        pen = QPen(Qt.GlobalColor.darkBlue)
        pen.setWidth(2)
        wheel.setPen(pen)

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
                title = QGraphicsTextItem(titles[i], self)
                tx = (x+xy[0])/2
                ty = (y+xy[1])/2
                title.setPos(tx, ty)
                angle = calc_clockwise_angle(tx, ty, radius)
                title.setRotation(angle)
                xy = [x,y]
        title = QGraphicsTextItem(titles[0], self)
        tx = (xy[0]+xy1[0])/2
        ty = (xy[1]+xy1[1])/2
        title.setPos(tx, ty)
        angle = calc_clockwise_angle(tx, ty, radius)
        title.setRotation(angle)

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
def calc_clockwise_angle(x, y, radius):
    delta = math.sqrt(math.pow(radius-x,2)+math.pow(radius-y,2))
    if x < radius:
        xd = radius - x
        theta = math.degrees(math.acos(xd/delta))
        if y > radius:
            theta = 360 - theta
    else:
        xd = x - radius
        theta = math.degrees(math.acos(xd/delta))
        if y < radius:
            theta = 180 - theta
        else:
            theta = theta + 180
    
    return theta
