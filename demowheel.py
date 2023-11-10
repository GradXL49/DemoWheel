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

        wheel = QGraphicsEllipseItem(xc-self.radius, yc-self.radius, diameter, diameter)
        self.wheel_rect = wheel.rect()

        brush = QBrush(settings.get_value('Wheel', 'bg_color'))
        wheel.setBrush(brush)

        self.pen = QPen(settings.get_value('Wheel', 'fg_color'))
        self.pen.setWidth(2)
        if not self.multicolor:
            wheel.setPen(self.pen)
            wheel.setParentItem(self)

        self.font = QFont()
        self.font.setPointSize(int(settings.get_value('Text', 'font_size')))
        titles = settings.get_section_list('Titles')
        self.l = len(titles)
        self.arc_length = 360 / self.l
        for i in range(self.l):
            x = self.radius * math.cos(2*math.pi*i/self.l) + xc
            y = self.radius * math.sin(2*math.pi*i/self.l) + yc
            if self.multicolor:
                self.draw_piece(x, y, self.bg_colors[i%len(self.bg_colors)])
            else:
                line = QGraphicsPolygonItem(QPolygonF([QPointF(xc, yc),QPointF(x, y)]), self)
                line.setPen(self.pen)
            self.draw_title(titles[i], i+0.5)

    def draw_piece(self, x, y, color):
        #make a painter path that draws an arc within the bounds of the wheel from the center to the given point then clockwise for the arc length
        path = QPainterPath(QPointF(self.xc, self.yc))
        path.arcTo(self.wheel_rect, calc_clockwise_angle(self.xc, self.yc, x, y), self.arc_length)

        #use the painter path to create a unique graphics item shape
        piece = QGraphicsPathItem(path, self)
        piece.setBrush(QBrush(color))
        piece.setPen(QPen(color))
        piece.setZValue(-1)
    
    def draw_title(self, text, i):
        #get the point in the middle of the piece at 90% of the radius (just inside the circle)
        tx = self.radius * 0.98 * math.cos(2*math.pi*i/self.l) + self.xc
        ty = self.radius * 0.98 * math.sin(2*math.pi*i/self.l) + self.yc

        #create and configure the text, rotate towards center
        title = QGraphicsTextItem(text, self)
        angle = calc_clockwise_angle(tx, ty, self.xc, self.yc) #rotate towards the center of the wheel
        title.setRotation(angle)
        title.setFont(self.font)
        title.setDefaultTextColor(self.settings.get_value('Text', 'text_color'))
        title.setZValue(1)

        #treat the line perpendicular to the found point as a right triangle to find an offset point on that line
        if ty == self.yc:
            theta = math.atan(0)
        else:
            theta = math.atan(-((self.xc-tx)/(self.yc-ty))) #use the slope of the tangent line by calculating negative reciprocal of slope to center
        offset = title.boundingRect().height()/2
        if ty >= self.yc:
             offset = -offset
        off_x = offset * math.cos(theta)
        off_y = offset * math.sin(theta)
        
        #place centered at the calculated point with offset
        title.setPos(tx+off_x, ty+off_y)

        #optionally display a shadow inline and slightly below the original text
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
