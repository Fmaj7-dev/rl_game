import math
import numpy as np

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QImage)

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

        # add consts
        self.MAX_SPEED = 240/fps
        self.ACCEL = 0.4
        self.INERTIA = 0.95
        self.FRICTION = 0.97
        self.STEER = 0.8
        self.CAR_HEIGHT = 44
        self.CAR_WIDTH = 16

        # add pixmap
        pix = QPixmap("../resources/red_car3.png")
        self.car = scene.addPixmap( pix )

        image = QPixmap.toImage(pix)
        grayscale = image.convertToFormat(QImage.Format_Grayscale8)

        self.gray_pix = QPixmap.fromImage( grayscale )
        self.gray_pix.setMask(pix.createMaskFromColor(Qt.transparent))

        self.car.setPos(self.x, self.y)
        self.car.setRotation(angle)
        self.car.setOffset((-pix.width())/2 , (-pix.height())/2)

        # add lasers
        self.lasers = []
        for _ in range(10):
            self.lasers.append(scene.addLine(self.x, self.y, self.x, self.y-100))
        
        self.ellipses = []
        for _ in range(10):
            self.ellipses.append(scene.addEllipse(-3,-3,5,5) )

    def getPosition(self):
        return self.x, self.y
    
    def getAngle(self):
        return self.angle
    
    def setCrashed(self):
        if self.crashed:
            return

        self.car.setPixmap(self.gray_pix)
        self.crashed = True
        
        for laser in self.lasers:
            self.scene.removeItem(laser)

        for ellipse in self.ellipses:
            self.scene.removeItem(ellipse)
        
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
        # store point and length of laser
        self.endPoints = endPoints
        self.lengths = lengths

        for i, end in enumerate(endPoints):
            self.lasers[i].setLine(self.x, self.y, end[0], end[1])
            self.ellipses[i].setPos(end[0], end[1])


class Map():
    def __init__(self, scene, view):
        self.background = QPixmap ("../resources/maps/level1/background.png")
        self.collision = QPixmap("../resources/maps/level1/collision.png")
        _ = scene.addPixmap(self.background)
        view.resize(self.background.size().width(), self.background.size().height() )

    def isColliding(self, car):
        points = car.getAllCollisionPoints()
        
        for point in points:
            x = point[0]
            y = point[1]

            pixel = self.collision.toImage().pixel(x, y)
            colors = QColor(pixel).getRgb()

            if colors[0:3] == (0,0,0):
                return True

        return False

    def laserCollision(self, car):
        x, y = car.getPosition()
        lasers = car.getLaserAngles()
        angle = car.getAngle()
        length = 500

        endPoints = []

        for laser in lasers:
            absolute_angle = angle + laser
            
            y_increment = length * math.cos( math.radians( absolute_angle ) )
            x_increment = length * math.sin( math.radians( absolute_angle ) )

            # absolute position of corner
            y_abs = y - y_increment
            x_abs = x + x_increment

            endPoints.append( (x_abs, y_abs) )

            #pixel = self.collision.toImage().pixel(x_abs, y_abs)
            #colors = QColor(pixel).getRgb()

        #car.setEndPoints(endPoints)

        laserEnds = []
        laserEndLengths = []
        for endPoint in endPoints:
            dx = (endPoint[0] - x )/length
            dy = (endPoint[1] - y )/length

            for i in range(length):
                check_x = x + dx*i
                check_y = y + dy*i

                pixel = self.collision.toImage().pixel(check_x, check_y)
                #print("x: "+str(check_x)+ "y: "+str(check_y))
                colors = QColor(pixel).getRgb()

                if colors[0:3] == (0,0,0):
                    laserEnds.append((check_x, check_y))
                    laserEndLengths.append(i)
                    break
        
        car.setEndPoints(laserEnds, laserEndLengths)
        

class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        self.timerId = 0

        self.scene = QGraphicsScene(self)

        """self.pixmap = QPixmap ("../resources/maps/level1/background.png")
        _ = scene.addPixmap(self.pixmap)
        self.resize(self.pixmap.size().width(), self.pixmap.size().height() )"""
        self.map = Map( self.scene, self)

        self.fps = 60

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