import math
import numpy as np
import threading

from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage)

from car import Car
from map import Map
from neuroevol import NeuroEvol

class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        self.timerId = 0
        self.fps = 30

        self.mode = "manual"
        #self.mode = "manual"

        if self.mode == "manual":
            self.num_cars = 1
        elif self.mode == "neuro_evol":
            self.num_cars = 20

        self.scene = QGraphicsScene(self)

        # create map
        self.map = Map( self.scene, self)

        # create cars
        self.cars = []
        for _car in range(self.num_cars):
            self.cars.append(Car( self.scene, 110, 400, 0, self.fps))

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
        if self.mode == "manual":
            self.startTimer(1000 / self.fps)

        elif self.mode == "neuro_evol":
            self.neuroevol = NeuroEvol(self.cars, self.map)
            self.timer = QTimer()
            self.timer.singleShot(0, self.runNeuroEvol)

    def runNeuroEvol(self):
        self.neuroevol.run()
        self.timer.singleShot(0, self.runNeuroEvol)

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
            if self.mode == "manual":
                self.cars[0] = Car(self.scene, 110, 400, 0, self.fps)

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
        if self.mode == "manual":
            if self.keyUp:
                self.cars[0].accelerate()
            if self.keyDown:
                self.cars[0].decelerate()
            if self.keyRight:
                self.cars[0].steerRight()
            if self.keyLeft:
                self.cars[0].steerLeft()

            for car in self.cars:
                car.update()

                if self.map.isColliding(car):
                    car.setCrashed()

                self.map.laserCollision(car)
        elif self.mode == "neuro_evol":
            self.neuroevol.start()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.show()

    sys.exit(app.exec_())