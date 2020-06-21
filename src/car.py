
# external
import math
import numpy as np

# qt
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage, QPen)

# project
from neural_network import NeuralNetwork

class Car():
    def __init__(self, scene, x, y, angle, fps):
        self.scene = scene

        self.x = x
        self.y = y
        self.angle = angle

        self.speed = 0

        self.inertia_x = 0
        self.inertia_y = 0

        self.crashed = False

        self.score = 0

        self.lengths = []

        self.nn = NeuralNetwork(10, 6, 4, 'zero')

        self.previous_score = 0

        # add consts (FIXME: load this from a file)
        self.MAX_SPEED = 240/fps
        self.ACCEL = 0.4
        self.INERTIA = 0.90
        #self.INERTIA = 0
        self.FRICTION = 0.97
        self.STEER = 0.8
        self.CAR_HEIGHT = 44
        self.CAR_WIDTH = 16

        self.INIT_POS_X = x
        self.INIT_POS_Y = y
        self.INIT_ANGLE = angle

        # add pixmaps
        self.pix = QPixmap("../resources/red_car3.png")
        self.car = scene.addPixmap( self.pix )
        self.car.setZValue(10)

        image = QPixmap.toImage(self.pix)
        grayscale = image.convertToFormat(QImage.Format_Grayscale8)

        self.gray_pix = QPixmap.fromImage( grayscale )
        self.gray_pix.setMask(self.pix.createMaskFromColor(Qt.transparent))

        # init pos, rot
        self.car.setPos(self.x, self.y)
        self.car.setRotation(angle)
        self.car.setOffset((-self.pix.width())/2 , (-self.pix.height())/2)

        self.addLasers()

        self.addEllipses()

    def addLasers(self):
        # add lasers
        self.lasers = []
        pen = QPen(QColor(128,128,128))
        for _ in range(10):
            self.lasers.append(self.scene.addLine(self.x, self.y, self.x, self.y-100, pen))

    def addEllipses(self):
        # and ellipses 
        self.ellipses = []
        pen = QPen(QColor(200,0,0))
        for _ in range(10):
            self.ellipses.append(self.scene.addEllipse(-3,-3,5,5, pen) )

    def removeLasers(self):
        # remove lasers
        for laser in self.lasers:
            self.scene.removeItem(laser)
        self.lasers = []

    def removeEllipses(self):
        # remove ellipses
        for ellipse in self.ellipses:
            self.scene.removeItem(ellipse)
        self.ellipses = []


    def getPosition(self):
        return self.x, self.y
    
    def reset(self):
        self.x = self.INIT_POS_X
        self.y = self.INIT_POS_Y
        self.angle = self.INIT_ANGLE

        self.car.setPos(self.x, self.y)
        self.car.setRotation(self.angle)

        self.removeLasers()
        self.removeEllipses()

        self.addLasers()
        self.addEllipses()

    def getAngle(self):
        return self.angle
    
    def isCrashed(self):
        return self.crashed

    def setCrashed(self, crash=True):
        self.crashed = crash

        if self.crashed:
            self.car.setPixmap(self.gray_pix)

            self.removeLasers()
            self.removeEllipses()
        else:
            self.car.setPixmap(self.pix)
        
        
    def moveForward(self):
        y_increment = self.speed * math.cos( math.radians( self.angle ) )
        x_increment = self.speed * math.sin( math.radians( self.angle ) )

        self.inertia_y = self.INERTIA * self.inertia_y + (1-self.INERTIA) * y_increment
        self.inertia_x = self.INERTIA * self.inertia_x + (1-self.INERTIA) * x_increment

        self.y -= self.inertia_y
        self.x += self.inertia_x

        self.car.setPos(self.x, self.y)

    def steerRight(self):
        if self.crashed == True:
            return

        self.angle += self.speed * self.STEER
        self.car.setRotation(self.angle)
    
    def steerLeft(self):
        if self.crashed == True:
            return

        self.angle -= self.speed * self.STEER
        self.car.setRotation(self.angle)

    def accelerate(self):
        self.speed += self.ACCEL
        self.speed = np.clip(self.speed, 0, self.MAX_SPEED)

    def decelerate(self):
        self.speed -= self.ACCEL
        self.speed = np.clip(self.speed, -self.MAX_SPEED/2, self.MAX_SPEED)

    def update(self):
        if self.crashed == True:
            return

        self.speed *= self.FRICTION

        if self.speed < 0.1 and self.speed > -0.1:
            self.speed = 0

        self.moveForward()

    def setScore(self, score):
        self.previous_score = self.score
        self.score = score

    def getScore(self):
        return self.score

    def getPreviousScore(self):
        return self.previous_score

    # get absolute pixel value of car corner for collision
    def getCollisionPoint(self, rel_x, rel_y):
        x, y = self.x, self.y
        
        # distance center - corner
        l = math.sqrt(((self.y+rel_y)-self.y)**2 + ((self.x+rel_x) - self.x)**2)

        # angle corner center
        alpha = math.degrees(math.atan( -(rel_x)/(rel_y) ))
        if rel_y < 0:
            alpha += (90-alpha)*2

        # total angle of corner
        angle = self.angle + alpha

        # absolute increment of corner
        y_increment = l * math.cos( math.radians( angle ) )
        x_increment = l * math.sin( math.radians( angle ) )

        # absolute position of corner
        y -= y_increment
        x += x_increment

        return x, y

    def getAllCollisionPoints(self):
        points = []
        points.append (self.getCollisionPoint(self.CAR_WIDTH/2, self.CAR_HEIGHT/2))
        points.append (self.getCollisionPoint(self.CAR_WIDTH/2, -self.CAR_HEIGHT/2))
        points.append (self.getCollisionPoint(-self.CAR_WIDTH/2, self.CAR_HEIGHT/2))
        points.append (self.getCollisionPoint(-self.CAR_WIDTH/2, -self.CAR_HEIGHT/2))
        
        return points

    def getLaserAngles(self):
        return (0, 22, 45, 90, 135, 180, -135, -90, -45, -22)

    def setEndPoints(self, endPoints, lengths):
        if self.crashed:
            return

        # store point and length of laser
        self.endPoints = endPoints
        self.lengths = lengths

        for i, end in enumerate(endPoints):
            self.lasers[i].setLine(self.x, self.y, end[0], end[1])
            self.ellipses[i].setPos(end[0], end[1])

    def getEndPoints(self):
        return self.endPoints

    def getEndPointLengths(self):
        return self.lengths

    def getWeightSet(self):
        return self.nn.getArr()

    def setWeightSet(self, weights):
        self.nn.setWeights(weights)

    def getNNStructure(self):
        return self.nn.getStructure()

    def runNN(self):
        if len(self.lengths) != 10:
            #print("-------> len self.lengths: " + str(len(self.lengths)))
            return

        output = self.nn.forward(self.lengths)
        
        if float(output[0]) > 0:
            self.accelerate()
        if float(output[1]) > 0:
            self.decelerate()
        if float(output[2]) > 0:
            self.steerLeft()
        if float(output[3]) > 0:
            self.steerRight()
        #if float(output[4]) > 0:
        #    pass
