# external
import math
import numpy as np
import threading

# qt
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage, QPen)

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

        self.weights = []
        self.addNN(135, 235, 150, 200)

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
        gen, score, best_weights = self.neuroevol.run()
        self.text_generation.setPlainText("Generation: "+str(gen))
        self.text_score.setPlainText("Best score: "+str(score))

        self.timer.singleShot(0, self.runNeuroEvol)

        """if gen < 10 or gen % 50 == 0:
            self.png_sequence += 1
            pixmap = self.grab()
            pixmap.save("../video/neuroevol"+str(self.png_sequence)+".png")"""
        self.updateWeights(best_weights)

    def addNN(self, origin_x, origin_y, width, height):
        self.neurons = []
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.end_x = origin_x + width 
        self.end_y = origin_y + height

        # number of neurons on level X
        self.nn_level1 = 10
        self.nn_level2 = 6
        self.nn_level3 = 4

        self.neuron_size = 7
        offset = self.neuron_size/2

        self.pen_size = 3

        self.neuron_pen = QPen(Qt.black)

        # draw first level of neurons
        origin_x_level1 = self.origin_x
        origin_y_level1 = self.origin_y
        end_y_level1 = self.end_y
        space_level1 = (end_y_level1 - origin_y_level1) / self.nn_level1

        for i in range(self.nn_level1):
            neuron = self.scene.addEllipse(origin_x_level1 -offset, origin_y_level1+ i*space_level1 -offset, self.neuron_size, self.neuron_size, self.neuron_pen, Qt.white)
            neuron.setZValue(10)
            self.neurons.append(neuron)

        # draw second level of neurons
        origin_x_level2 = (self.origin_x + self.end_x)/2
        origin_y_level2 = self.origin_y + (self.nn_level1 - self.nn_level2)/2 * space_level1

        for i in range(self.nn_level2):
            neuron = self.scene.addEllipse(origin_x_level2-offset, origin_y_level2+ i*space_level1-offset, self.neuron_size, self.neuron_size, self.neuron_pen, Qt.white) 
            neuron.setZValue(10)
            self.neurons.append(neuron)

        # draw third level of neurons
        origin_x_level3 = self.end_x
        origin_y_level3 = self.origin_y + (self.nn_level1 - self.nn_level3)/2 * space_level1

        for i in range(self.nn_level3):
            neuron = self.scene.addEllipse(origin_x_level3-offset, origin_y_level3+ i*space_level1-offset, self.neuron_size, self.neuron_size, self.neuron_pen, Qt.white) 
            neuron.setZValue(10)
            self.neurons.append(neuron)

        pen = QPen(QColor(255,255, 0), self.pen_size)

        # draw first bunch of weights
        for i in range(self.nn_level2):
            end_x = origin_x_level2
            end_y = origin_y_level2+ i*space_level1

            for i in range(self.nn_level1):
                origin_x = origin_x_level1
                origin_y = origin_y_level1+ i*space_level1

                line = self.scene.addLine(origin_x, origin_y, end_x, end_y, pen)
                self.weights.append(line)

        # draw second bunc of weights
        for i in range(self.nn_level3):
            end_x = origin_x_level3
            end_y = origin_y_level3+ i*space_level1
            for i in range(self.nn_level2):
                origin_x = origin_x_level2
                origin_y = origin_y_level2+ i*space_level1

                self.weights.append(self.scene.addLine(origin_x, origin_y, end_x, end_y, pen))


    def updateWeights(self, weights):
        if weights is None:
            return

        W0_start = 0
        W0_end = self.nn_level2 * self.nn_level1
        W0_tmp = weights[W0_start : W0_end ]
        W0_tmp = np.clip(W0_tmp, -1, 1)

        for i, weight in enumerate(W0_tmp):
            r,g,b = 0,0,0
            if weight < 0:
                r = 255
                g = 255 + weight*255
            else:
                r = 255 - weight*255
                g = 255

            pen = QPen(QColor(r,g,b), self.pen_size)
            self.weights[i].setPen(pen)

        b0_end = W0_end + self.nn_level2

        W1_start = b0_end
        W1_end = b0_end + self.nn_level3*self.nn_level2
        W1_tmp = weights[W1_start : W1_end]
        W1_tmp = np.clip(W1_tmp, -1, 1)

        for i, weight in enumerate(W1_tmp):
            r,g,b = 0,0,0
            if weight < 0:
                r = 255
                g = 255 + weight*255
            else:
                r = 255 - weight*255
                g = 255

            pen = QPen(QColor(r,g,b), self.pen_size)
            self.weights[i].setPen(pen)

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