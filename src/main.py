import math
import numpy as np

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage)

from car import Car
from map import Map

class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        self.timerId = 0
        self.fps = 60

        self.scene = QGraphicsScene(self)

        # create map
        self.map = Map( self.scene, self)

        # create car
        self.car = Car( self.scene, 110, 400, 0, self.fps)

        self.setScene( self.scene )
        self.setCacheMode( QGraphicsView.CacheBackground )
        self.setViewportUpdateMode( QGraphicsView.BoundingRectViewportUpdate )
        self.setRenderHint( QPainter.Antialiasing )
        self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        # keyboard status
        self.keyUp = False
        self.keyDown = False
        self.keyRight = False
        self.keyLeft = False

        # create timer
        self.startTimer(1000 / self.fps)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.keyUp = True
        if key == Qt.Key_Down:
            self.keyDown = True
        if key == Qt.Key_Right:
            self.keyRight = True
        if key == Qt.Key_Left:
            self.keyLeft = True
        if key == Qt.Key_Space:
            self.car = Car(self.scene, 110, 400, 0, self.fps)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.keyUp = False
        if key == Qt.Key_Down:
            self.keyDown = False
        if key == Qt.Key_Right:
            self.keyRight = False
        if key == Qt.Key_Left:
            self.keyLeft = False

    def timerEvent(self, event):
        if self.keyUp:
            self.car.accelerate()
        if self.keyDown:
            self.car.decelerate()
        if self.keyRight:
            self.car.steerRight()
        if self.keyLeft:
            self.car.steerLeft()

        self.car.update()

        if self.map.isColliding(self.car):
            self.car.setCrashed()

        self.map.laserCollision(self.car)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.show()

    sys.exit(app.exec_())