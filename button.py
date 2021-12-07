from graphics import *

class Button:
    def __init__(self, window, center, width, height, label):

        w = width/2.0
        h = height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rectangle = Rectangle(p1, p2)
        self.rectangle.setFill('lightgray')
        self.rectangle.draw(window)
        self.label = Text(center, label)
        self.label.draw(window)
        self.deactivate()

    def clicked(self, p):
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rectangle.setWidth(2)
        self.active = True

    def deactivate(self):
        self.label.setFill('darkgray')
        self.rectangle.setWidth(1)
        self.active = False

