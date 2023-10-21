"""
Grady Landers
Demo Wheel - demowheel.py
Custom class for the DemoWheel object. Enables the entire group to be animated.
Made with assistance from https://engineersjourney.wordpress.com/2012/09/05/pyqt-and-animating-qgraphicsitem-objects/
"""

#imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush, QPen, QPolygonF, QFont, QPainterPath
from PyQt6.QtCore import QPointF, QObject, pyqtProperty
import math

#DemoWheel class
class DemoWheel(QGraphicsItem):
    def __init__(self, xc, yc, settings):
        super(DemoWheel, self).__init__()
        self.xc = xc
        self.yc = yc
        self.settings = settings
        self.multicolor = self.settings.get_value('Wheel', 'bg_type') == 'Multicolor'
        self.bg_colors = self.settings.get_section_list('Wheel_Colors')
        diameter = float(settings.get_value('Wheel', 'size'))
        self.radius = diameter / 2
        self.setPos(xc+self.radius, yc+self.radius)
        self.adapter = DemoWheelAdapter(self, self)

        wheel = QGraphicsEllipseItem(xc-self.radius, yc-self.radius, diameter, diameter, self)
        self.wheel_rect = wheel.rect()

        brush = QBrush(settings.get_value('Wheel', 'bg_color'))
        wheel.setBrush(brush)

        pen = QPen(settings.get_value('Wheel', 'fg_color'))
        pen.setWidth(2)
        wheel.setPen(pen)

        self.font = QFont()
        self.font.setPointSize(int(settings.get_value('Text', 'font_size')))
        titles = settings.get_section_list('Titles')
        l = len(titles)
        self.arc_length = 360 / l
        for i in range(l):
            x = self.radius * math.cos(2*math.pi*i/l) + xc
            y = self.radius * math.sin(2*math.pi*i/l) + yc
            if self.multicolor:
                    self.draw_piece(x, y, self.bg_colors[i%len(self.bg_colors)])
            line = QGraphicsPolygonItem(QPolygonF([QPointF(xc, yc),QPointF(x, y)]), self)
            line.setPen(pen)
            if i == 0:
                xy1 = [x,y]
                xy = [x,y]
            else:
                self.draw_title(titles[i], x, y, xy[0], xy[1])
                xy = [x,y]
        self.draw_title(titles[0], xy[0], xy[1], xy1[0], xy1[1])

    def draw_piece(self, x, y, color):
        path = QPainterPath(QPointF(self.xc, self.yc))
        path.arcTo(self.wheel_rect, calc_clockwise_angle(x, y, self.xc, self.yc), self.arc_length)

        piece = QGraphicsPathItem(path, self)
        piece.setBrush(QBrush(color))

        # arc_path = QPainterPath(QPointF(x1, y1))
        # arc_path.arcMoveTo(x2, y2, 100, 100, 100)
        # arc_piece = QGraphicsPathItem(arc_path, self)
        # arc_piece.setBrush(brush)

        # big_piece = QGraphicsPolygonItem(QPolygonF([
        #     QPointF(x1, y1),
        #     QPointF(x2, y2),
        #     QPointF(self.xc, self.yc)
        # ]), self)
        # big_piece.setBrush(brush)
    
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
