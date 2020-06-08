# external
import math
import numpy as np
import threading

# qt
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage)

# project
from car import Car
from map import Map
from neuroevol import NeuroEvol

class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        np.random.seed(42)

        self.timerId = 0
        self.fps = 30
        self.frame = 0
        self.png_sequence = 0

        self.mode = "neuro_evol"
        #self.mode = "manual"

        if self.mode == "manual":
            self.num_cars = 1
        elif self.mode == "neuro_evol":
            self.num_cars = 20

        self.scene = QGraphicsScene(self)

        self.text_generation = self.scene.addText("Generation: 0")
        self.text_score = self.scene.addText("Best score: 0")

        # text position
        self.text_generation.setPos(200, 150)
        self.text_generation.setZValue(10)
        self.text_generation.setDefaultTextColor(Qt.red)

        self.text_score.setPos(200, 170)
        self.text_score.setZValue(10)
        self.text_score.setDefaultTextColor(Qt.red)

        # create scene map
        self.map = Map( self.scene, self) 

        # create cars
        self.cars = []
        for _car in range(self.num_cars):
            self.cars.append(Car( self.scene, 100, 250, 0, self.fps))

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
        self.frame += 1
        gen, score = self.neuroevol.run()
        self.text_generation.setPlainText("Generation: "+str(gen))
        self.text_score.setPlainText("Best score: "+str(score))

        self.timer.singleShot(0, self.runNeuroEvol)

        """if gen < 10 or gen % 50 == 0:
            self.png_sequence += 1
            pixmap = self.grab()
            pixmap.save("../video/neuroevol"+str(self.png_sequence)+".png")"""

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
        self.frame += 1

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

                #self.map.updateScore(car)

                if self.map.isColliding(car):
                    car.setCrashed()

                self.map.laserCollision(car)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.show()

    sys.exit(app.exec_())